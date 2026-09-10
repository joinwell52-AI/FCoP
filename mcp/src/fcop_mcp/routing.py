"""Server-owned workspace binding; no lifecycle or authorization implementation."""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from types import MappingProxyType
from typing import Any

from fcop import Project
from fcop.errors import V4ProtocolError, _V4Code

PACKAGE_COMPATIBILITY = frozenset({("3.2.5", "3.2.5"), ("4.0.0rc1", "4.0.0rc1"), ("4.0.0", "4.0.0"), ("4.0.1", "4.0.1")})


def check_package_compatibility() -> None:
    """Exact development package pair; release combinations are owned by WP4D."""
    try:
        pair = (version("fcop"), version("fcop-mcp"))
    except PackageNotFoundError as exc:
        raise RuntimeError("toolkit:MCP_PACKAGE_INCOMPATIBLE: missing package metadata") from exc
    if pair not in PACKAGE_COMPATIBILITY:
        raise RuntimeError(f"toolkit:MCP_PACKAGE_INCOMPATIBLE: unsupported pair {pair!r}")


@dataclass(frozen=True)
class Route:
    workspace_path: Path
    declared_protocol: str
    project: Project
    capabilities: frozenset[str]


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate manifest key")
        result[key] = value
    return result


class WorkspaceRouter:
    """Trusted startup registry, copied once; manifests never install evaluators."""

    def __init__(
        self, root: Path | str, *, trusted_profiles: Mapping[str, Callable[..., str]] | None = None,
        binding_source: str = "trusted server binding",
    ) -> None:
        self.root = Path(root).resolve()
        self.binding_source = binding_source
        self._trusted_profiles = MappingProxyType(dict(trusted_profiles or {}))

    def route(self) -> Route:
        project = Project(self.root, trusted_profiles=self._trusted_profiles)
        path = project.config_path
        try:
            raw = path.read_bytes()
            value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
            if not isinstance(value, dict):
                raise ValueError("Manifest must be an object")
        except (OSError, UnicodeError, ValueError) as exc:
            raise V4ProtocolError(
                _V4Code.UNSUPPORTED_WORKSPACE_VERSION,
                "Cannot classify the declared workspace",
                operation_ref="workspace_binding", subject_ref=str(self.root),
            ) from exc
        protocol = value.get("protocol", "fcop")
        if protocol != "fcop":
            raise V4ProtocolError(
                _V4Code.UNSUPPORTED_PROTOCOL, "Unsupported declared protocol",
                operation_ref="workspace_binding", subject_ref=str(self.root),
            )
        version = value.get("protocol_version", value.get("version"))
        if version == "4.0":
            # Project construction, not MCP, validates the v4 identity and Encoding.
            declared = "v4"
        elif str(version) in {"1", "2", "3"} or (
            isinstance(version, str) and re.fullmatch(r"[123](?:\.\d+){1,2}", version)
        ):
            declared = "v3"
        else:
            raise V4ProtocolError(
                _V4Code.UNSUPPORTED_WORKSPACE_VERSION, "Unsupported declared workspace version",
                operation_ref="workspace_binding", subject_ref=str(self.root),
            )
        return Route(self.root, declared, project, frozenset({declared}))

    def bind(self, root: Path | str) -> Route:
        candidate = WorkspaceRouter(root, trusted_profiles=self._trusted_profiles)
        route = candidate.route()
        self.root = candidate.root
        return route
