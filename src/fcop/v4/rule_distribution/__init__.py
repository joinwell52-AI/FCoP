"""Private read-only rule-distribution dispatch behind the sole Project entry."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.encoding import read_json, safe_path

from ._errors import reject
from ._loader import contained, load, read_file, sha
from ._selection import operation_scope, profile, select

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation


def _unavailable(action: str) -> NoReturn:
    raise V4ProtocolError(
        _V4Code.OPERATION_NOT_IMPLEMENTED, "This rule-distribution operation is not implemented",
        operation_ref=action, subject_ref="fcop:rule-distribution",
    )


def _receipt_preflight(root: Path, ref: Any, kind: str, code: str, action: str) -> None:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        reject(code, action, "Explicit receipt identity required")
    path, digest = ref["path"], ref["sha256"]
    if not isinstance(path, str) or not path.startswith(f"fcop/internal/rule-distribution/{kind}/"):
        reject(code, action, "Receipt namespace invalid")
    raw = read_file(contained(root, path, code, action), code, action)
    if not isinstance(digest, str) or sha(raw) != digest:
        reject(code, action, "Receipt byte identity mismatch")
    # These necessary checks cannot establish adoption/deployment. No receipt
    # is consumed, trusted, created or returned in this implementation stage.


def _dispatch(root: Path, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
    if action == "build_artifacts":
        from ._artifacts import build_artifacts

        return build_artifacts(root, request)
    if action == "measure_context":
        from ._measurement import measure_context

        return measure_context(root, request)
    if action == "read_resource":
        from ._read import read_resource

        return read_resource(root, "4.0", request)
    if action == "inspect_layers":
        from ._read import inspect_layers

        return inspect_layers(root, request)
    if action == "shadow":
        from ._shadow import shadow

        return shadow(request)
    if action == "redeploy":
        reject("RULE_ADOPTION_REQUIRED", action, "v4 requires explicit adoption and deployment")
    if action in {"inspect_profile", "status", "adopt", "plan", "apply", "verify_deployment", "rollback", "inspect_failure", "rollback_partial"}:
        from ._deployment import dispatch

        return dispatch(root, action, request)
    if action not in {"validate", "select", "validate_operation_scope", "inspect_profile", "plan", "apply", "rollback"}:
        _unavailable(action)
    if action == "apply":
        _receipt_preflight(root, request.get("adoption_receipt_ref"), "adoptions", "RULE_ADOPTION_REQUIRED", action)
        _unavailable(action)
    if action == "rollback":
        _receipt_preflight(root, request.get("deployment_receipt_ref"), "deployments", "RULE_DEPLOYMENT_RECOVERY_REQUIRED", action)
        _unavailable(action)
    if action == "inspect_profile":
        profile(request, action)
        _unavailable(action)
    package = load(request.get("manifest_path"), action)
    if action == "validate":
        return package.summary()
    selected = select(root, package, request, action)
    if action == "select":
        return selected
    if action == "validate_operation_scope":
        return operation_scope(selected, request, action)
    host = profile(request, action)
    # A lower bound proves overflow without generating any Host projection.
    if len(selected["guidance"]) > host["max_projection_bytes"]:
        reject("RULE_PROJECTION_LIMIT", action, "Selected raw sources already exceed Host byte bound")
    for target in host["target_paths"]:
        path = root / target
        if path.exists() or path.is_symlink():
            reject("RULE_OWNERSHIP_CONFLICT", action, "Existing target has no proven distribution ownership")
    _unavailable(action)


def _bind(creation: _Creation) -> Callable[..., Mapping[str, Any]]:
    def rule_distribution(*, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
        from fcop.v4.creation import _manifest

        if not isinstance(action, str) or not isinstance(request, Mapping):
            reject("RULE_SELECTION_INVALID", "rule_distribution", "Invalid request shape")
        try:
            current = _manifest(read_json(safe_path(creation.root, "fcop/fcop.json")))
        except V4ProtocolError as exc:
            if action == "adopt" and exc.code == "UNSUPPORTED_WORKSPACE_VERSION":
                reject("RULE_ADOPTION_REQUIRED", action, "Adoption requires a current 4.0 declaration")
            raise
        if current != creation.manifest or request.get("workspace_id", current["workspace_id"]) != current["workspace_id"]:
            if action == "adopt":
                reject("RULE_ADOPTION_REQUIRED", action, "Adoption workspace identity mismatch")
            raise V4ProtocolError(_V4Code.WORKSPACE_ID_MISMATCH, "Workspace declaration changed", operation_ref=action)
        if request.get("protocol_version", "4.0") != "4.0":
            if action == "adopt":
                reject("RULE_ADOPTION_REQUIRED", action, "Adoption requires the declared 4.0 version")
            raise V4ProtocolError(_V4Code.UNSUPPORTED_WORKSPACE_VERSION, "Rule package requires 4.0", operation_ref=action)
        return _dispatch(creation.root, action, request)

    return rule_distribution
