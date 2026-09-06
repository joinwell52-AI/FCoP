"""Versioned read-only MCP projections. The root Git specification is authority."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from importlib.resources import files
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError
from fcop.errors import V4ProtocolError

from fcop_mcp.disposition import RESOURCES
from fcop_mcp.projection import invoke_v4
from fcop_mcp.routing import WorkspaceRouter

_HANDLERS = {
    "fcop://config": "resource_config", "fcop://status": "resource_status",
    "fcop://rules": "resource_rules", "fcop://protocol": "resource_protocol",
    "fcop://spec": "resource_spec_zh", "fcop://spec/en": "resource_spec_en",
    "fcop://letter/en": "resource_letter_en", "fcop://letter/zh": "resource_letter_zh",
    "fcop://prompt/install": "resource_install_prompt_zh",
    "fcop://prompt/install/en": "resource_install_prompt_en",
    "fcop://teams": "resource_teams_index",
}


def spec_projection(declared: str, lang: str) -> str:
    registry = json.loads(files("fcop_mcp").joinpath("_specs.json").read_text(encoding="utf-8"))
    entry = registry[f"{declared}/{lang}"]
    payload = entry["content"]
    if hashlib.sha256(payload.encode("utf-8")).hexdigest() != entry["sha256"]:
        raise ResourceError("toolkit:SPEC_PROJECTION_DIGEST_MISMATCH")
    return (
        f"> Read-only specification projection; workspace protocol: {declared}\n"
        f"> Source: {entry['source_path']} @ {entry['source_commit']}\n"
        f"> Source payload SHA-256: {entry['sha256']}\n\n{payload}"
    )


def register_resources(
    mcp: FastMCP, legacy: Any, router_factory: Callable[[], WorkspaceRouter],
    *, replace: bool = False,
) -> None:
    for uri, policy in RESOURCES.items():
        original = getattr(legacy, _HANDLERS[uri])

        def build(uri: str, policy: str, original: Any) -> Callable[[], str]:
            def read() -> str:
                from fcop_mcp.adapter import CURRENT_ROUTER

                if policy == "PROFILE_CATALOG":
                    return str(original())
                router = router_factory()
                token = CURRENT_ROUTER.set(router)
                try:
                    if uri in {"fcop://config", "fcop://status"} and not (router.root / "fcop/fcop.json").exists():
                        return str(original())
                    route = router.route()
                    if policy == "VERSIONED_SPEC":
                        return spec_projection(route.declared_protocol, "en" if uri.endswith("/en") else "zh")
                    if route.declared_protocol == "v3":
                        return str(original())
                    if policy == "RULES_PENDING_WP4C" or policy == "GUIDANCE":
                        raise ResourceError(json.dumps({
                            "code": "toolkit:V4_GUIDANCE_UNAVAILABLE", "resource": uri,
                            "protocol_version": "4.0", "available": False,
                            "reason": "v4 guidance has not been delivered by WP4C; no legacy fallback",
                        }))
                    if uri == "fcop://config":
                        return route.project.config_path.read_text(encoding="utf-8")
                    return json.dumps(invoke_v4(route, "get_team_status", "STATUS", {}))
                except V4ProtocolError as exc:
                    raise ResourceError(json.dumps({
                        "code": exc.code, "operation_ref": exc.operation_ref,
                        "subject_ref": exc.subject_ref, "resource": uri,
                    })) from exc
                finally:
                    CURRENT_ROUTER.reset(token)

            read.__name__ = original.__name__
            read.__doc__ = f"Read-only {policy} projection. Profile content is not authorization."
            return read

        if replace:
            mcp.local_provider.remove_resource(uri)
        mime = "application/json" if uri in {"fcop://config", "fcop://teams"} else "text/markdown"
        mcp.resource(uri, mime_type=mime)(build(uri, policy, original))
