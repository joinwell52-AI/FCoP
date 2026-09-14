"""Private read-only rule-distribution dispatch behind the sole Project entry."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.encoding import read_json, safe_path

from ._errors import reject
from ._loader import load
from ._selection import operation_scope, select

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation


def _unavailable(action: str) -> NoReturn:
    raise V4ProtocolError(
        _V4Code.OPERATION_NOT_IMPLEMENTED, "This rule-distribution operation is not implemented",
        operation_ref=action, subject_ref="fcop:rule-distribution",
    )


def _dispatch(root: Path, action: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
    # 4.0.3 ownership boundary: these historical operations must not even
    # inspect a target, receipt, backup or caller-supplied Host profile.
    # Keep the public entry/signature, but retire the Host materialization plane.
    if action in {
        "redeploy", "inspect_profile", "status", "adopt", "plan", "apply",
        "verify_deployment", "rollback", "inspect_failure", "rollback_partial",
        "measure_context",
    }:
        raise V4ProtocolError(
            _V4Code.OPERATION_NOT_IMPLEMENTED,
            "Host-file rule distribution is retired; use package/MCP rule resources",
            operation_ref=action, subject_ref="fcop:rule-distribution",
        )
    if action == "build_artifacts":
        from ._artifacts import build_artifacts

        return build_artifacts(root, request)
    if action == "read_resource":
        from ._read import read_resource

        return read_resource(root, "4.0", request)
    if action == "inspect_layers":
        from ._read import inspect_layers

        return inspect_layers(root, request)
    if action == "shadow":
        from ._shadow import shadow

        return shadow(request)
    if action not in {"validate", "select", "validate_operation_scope"}:
        _unavailable(action)
    package = load(request.get("manifest_path"), action)
    if action == "validate":
        return package.summary()
    selected = select(root, package, request, action)
    if action == "select":
        return selected
    return operation_scope(selected, request, action)


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
