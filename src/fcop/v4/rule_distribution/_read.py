"""Version-selected read facts, owned by Project, never by a transport."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fcop.v4.encoding import parse_json, safe_path

from ._contract import MODULES
from ._errors import reject
from ._files import ARTIFACT, current_bytes, external_file, json_bytes, path_at
from ._loader import _Package, load, sha
from ._selection import select

if TYPE_CHECKING:
    from fcop import Project

_SELECTION = "RULE_SELECTION_INVALID"
_CONTEXT = {
    "manifest_path",
    "host_profile_path",
    "workspace_id",
    "protocol_version",
    "assembly_id",
    "selected_modules",
    "selected_languages",
    "admin_selection_ref",
    "recorded_at",
}
_SPEC = {
    "path": "spec/fcop-4.0-spec.md",
    "revision": "5c27e1bc90dce799aa7fa89e6cc717e01d47693e",
    "sha256": "9e6fd97ed4f3fa4bf9178babd54fd671fe4cc5f7bf7b8ee985d1726fb8c0e491",
}


def request_shape(request: Mapping[str, Any], allowed: set[str], action: str) -> None:
    if set(request) - (_CONTEXT | allowed):
        reject(_SELECTION, action, "Unknown read request fields")
    # Reuse the accepted executable-input guard without a deployment call.
    from ._deployment import _safe_request

    _safe_request(request, action)


def package_read(request: Mapping[str, Any], action: str) -> _Package:
    source = request.get("manifest_path")
    if source is None:
        source = str(Path(__file__).resolve().parents[2] / "rules/_data/v4/manifest.json")
    before = external_file(source, ARTIFACT, action)
    package = load(source, action)
    if sha(before) != package.manifest_sha256:
        reject(ARTIFACT, action, "Manifest changed during read")
    for artifact in package.artifacts:
        raw = external_file(str(Path(source).parent / artifact["source_path"]), ARTIFACT, action)
        if raw != package.raw[artifact["module_id"], artifact["language"]]:
            reject(ARTIFACT, action, "Artifact changed during read")
    if external_file(source, ARTIFACT, action) != before:
        reject(ARTIFACT, action, "Manifest changed after artifact verification")
    return package


def specification_identity(action: str) -> dict[str, str]:
    # The wheel carries a fixed citation, not another copy of the specification.
    # In a source checkout verify the actual authoritative bytes as well.
    checkout = Path(__file__).resolve().parents[4]
    if (checkout / ".git").exists():
        source = str(checkout / _SPEC["path"])
        raw = external_file(source, ARTIFACT, action)
        if sha(raw) != _SPEC["sha256"] or external_file(source, ARTIFACT, action) != raw:
            reject(ARTIFACT, action, "Frozen specification source drift")
    return dict(_SPEC)


def read_resource(root: Path, version: str, request: Mapping[str, Any]) -> dict[str, Any]:
    action = "read_resource"
    request_shape(request, {"resource_uri", "transport", "network"}, action)
    if request.get("protocol_version", version) != version:
        reject(_SELECTION, action, "Requested version differs from the workspace")
    if (
        request.get("transport", "stdio-local") not in ("stdio-local", "relay-inprocess")
        or request.get("network", False) is not False
    ):
        reject(_SELECTION, action, "Only explicit local reads are supported")
    uri = request.get("resource_uri")
    guidance = {
        f"fcop://guidance/{assembly}/{language}": (assembly, language)
        for assembly in ("sequential", "parallel")
        for language in ("en", "zh")
    }
    if not isinstance(uri, str) or uri not in {
        "fcop://rules",
        "fcop://protocol",
        "fcop://team",
        *guidance,
    }:
        reject(_SELECTION, action, "Unknown or noncanonical resource URI")
    result: dict[str, Any] = {
        "resource_uri": uri,
        "protocol_version": version,
        "mime_type": "text/markdown",
    }
    if version != "4.0":
        from fcop.rules import get_protocol_commentary, get_rules
        from fcop.teams import get_available_teams

        if uri in guidance and uri != "fcop://guidance/sequential/en":
            reject(_SELECTION, action, "Legacy guidance has no v4 assembly or language selection")
        if uri == "fcop://team":
            content: Any = {
                "teams": [
                    {"name": t.name, "roles": list(t.roles), "leader": t.leader}
                    for t in get_available_teams()
                ]
            }
            result["mime_type"] = "application/json"
            raw = json_bytes(content)
        else:
            content = get_protocol_commentary() if uri == "fcop://protocol" else get_rules()
            raw = content.encode("utf-8")
        return {**result, "content": content, "sha256": sha(raw)}
    if uri == "fcop://protocol":
        identity = specification_identity(action)
        return {**result, "content": identity, "sha256": identity["sha256"]}
    if uri == "fcop://team":
        unavailable = {"available": False, "reason": "fixed_team_roles_are_not_fcop_4_core"}
        return {
            **result,
            **unavailable,
            "mime_type": "application/json",
            "content": unavailable,
            "sha256": sha(json_bytes(unavailable)),
        }
    package = package_read(request, action)
    if uri == "fcop://rules":
        return {**result, "content": package.manifest, "sha256": package.manifest_sha256}
    assembly, language = guidance[uri]
    modules = MODULES[:-1] if assembly == "sequential" else MODULES
    expected = {
        "assembly_id": assembly,
        "selected_modules": list(modules),
        "selected_languages": [language],
    }
    if any(key in request and request[key] != value for key, value in expected.items()):
        reject(_SELECTION, action, "URI and explicit selection disagree")
    # A read-only language selection, not a Host profile or adoption claim.
    selection = select(root, package, expected, action, validated_profile={"languages": [language]})
    raw = selection["guidance"]
    return {
        **result,
        "content": raw.decode("utf-8"),
        "sha256": sha(raw),
        "manifest_sha256": package.manifest_sha256,
        "artifacts": selection["artifacts"],
    }


def inspect_layers(root: Path, request: Mapping[str, Any]) -> dict[str, Any]:
    from ._receipts import adoption_chain, deployment_chain, verify_history

    action = "inspect_layers"
    request_shape(request, {"adoption_receipt_ref", "deployment_receipt_ref"}, action)
    workspace = parse_json(safe_path(root, "fcop/fcop.json").read_bytes())["workspace_id"]
    package = package_read(request, action)
    ref = request.get("adoption_receipt_ref")
    deployment_ref = request.get("deployment_receipt_ref")
    targets = []
    if deployment_ref is not None:
        deployment = deployment_chain(root, deployment_ref, workspace, action)
        verify_history(root, workspace, deployment_ref, action)
        if ref is not None and ref != deployment["adoption_receipt_ref"]:
            reject("RULE_ADOPTION_REQUIRED", action, "Selected receipts disagree")
        ref = deployment["adoption_receipt_ref"]
        for target in deployment["targets"]:
            raw = current_bytes(root, target["path"], action)
            digest = sha(raw) if raw is not None else None
            targets.append(
                {
                    "path": target["path"],
                    "sha256": digest,
                    "recorded_sha256": target["after_sha256"],
                    "drifted": digest != target["after_sha256"],
                }
            )
    adopted = adoption_chain(root, ref, workspace, action) if ref is not None else None
    return {
        "disk_manifest_sha256": package.manifest_sha256,
        "index_manifest_sha256": package.manifest_sha256,
        "index_invalidation_evidence": "uncached_current_read",
        "adopted_manifest_sha256": adopted["rule_manifest_sha256"] if adopted else None,
        "host_entry_sha256": targets[0]["sha256"] if len(targets) == 1 else None,
        "host_entries": targets,
        "runtime_consumption_verified": None,
    }


def legacy(project: Project, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
    from fcop.v4.creation import _Creation

    if not isinstance(action, str) or not isinstance(request, Mapping):
        reject(_SELECTION, "rule_distribution", "Invalid action request")
    if request.get("protocol_version") == "4.0" or action == "adopt":
        reject(
            "RULE_ADOPTION_REQUIRED", action, "Explicit v4 adoption is required; no legacy fallback"
        )
    if _Creation.open_if_declared(project.path) is not None:
        reject(_SELECTION, action, "Workspace declaration changed")
    if not project.config_path.is_file():
        from fcop.errors import V4ProtocolError, _V4Code

        raise V4ProtocolError(
            _V4Code.UNSUPPORTED_WORKSPACE_VERSION,
            "Explicit workspace required",
            operation_ref=action,
        )
    value = parse_json(project.config_path.read_bytes(), classification=True)
    version = str(value.get("protocol_version", value.get("version", "")))
    if not version or request.get("protocol_version", version) != version:
        reject(_SELECTION, action, "Explicit known workspace version required")
    if (
        "protocol_version" in value
        and "version" in value
        and str(value["version"]).split(".")[0] != version.split(".")[0]
    ):
        reject(_SELECTION, action, "Conflicting version declarations")
    if action == "read_resource":
        return read_resource(project.path, version, request)
    if action == "redeploy":
        if set(request) - {"force", "protocol_version"} or request.get("force", False) is not False:
            reject(
                "RULE_OWNERSHIP_CONFLICT",
                action,
                "Legacy route must preserve existing Host entries",
            )
        from fcop.project import _plan_protocol_rules_deployment

        for relative, _ in _plan_protocol_rules_deployment():
            path_at(project.path, str(relative), "RULE_OWNERSHIP_CONFLICT", action)
        # The existing writer is the sole writer; no v4 directory or receipt.
        result = project.deploy_protocol_rules(force=False)
        return {
            "protocol_version": version,
            "written_paths": [p.relative_to(project.path).as_posix() for p in result.deployed],
        }
    reject(
        "RULE_ADOPTION_REQUIRED", action, "This action requires an explicitly adopted v4 workspace"
    )
