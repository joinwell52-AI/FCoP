"""MCP result projection and trusted startup construction."""

from __future__ import annotations

import inspect
import re
from collections.abc import Callable, Mapping
from contextvars import ContextVar
from functools import wraps
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.tools import ToolResult
from fcop.errors import V4ProtocolError, _V4Code
from mcp.types import CallToolResult

from fcop_mcp.disposition import TOOLS
from fcop_mcp.projection import invoke_v4
from fcop_mcp.routing import WorkspaceRouter, check_package_compatibility

CURRENT_ROUTER: ContextVar[WorkspaceRouter | None] = ContextVar("fcop_mcp_router", default=None)


def _additional_fields(policy: str) -> dict[str, tuple[Any, Any]]:
    fields: dict[str, tuple[Any, Any]] = {}
    if policy == "CREATE_TASK":
        fields = {key: (str | None, None) for key in ("workspace_id", "operation_id", "branch_of")}
    elif policy == "APPEND_AUTHORIZATION":
        fields = {key: (str | None, None) for key in (
            "profile_ref", "from_stage", "to_stage", "attempt_id", "family_digest",
            "issued_at", "expires_at",
        )}
        fields["issuer_proof"] = (Any, None)
    elif policy.startswith("APPEND_"):
        fields = {"workspace_id": (str | None, None), "references": (list[str] | None, None)}
        if policy == "APPEND_REPORT":
            fields.update(attempt_id=(str | None, None), report_kind=(str, "final"), result=(str | None, None))
        elif policy == "APPEND_ISSUE":
            fields.update(subject_ref=(str | None, None), recipient=(str | None, None))
        else:
            fields.update({key: (str | None, None) for key in (
                "recipient", "review_kind", "attempt_id", "family_digest", "authorization_ref",
                "profile_ref", "issued_at", "expires_at", "authorization_scope", "operation_kind",
            )})
            fields.update(transition=(dict[str, str] | None, None), issuer_proof=(Any, None))
    elif policy in {"T3", "T4", "T5", "T7"}:
        fields = {"report_ref": (str | None, None)} if policy != "T7" else {}
        if policy != "T3":
            fields.update({key: (str | None, None) for key in (
                "review_ref", "authorization_ref", "profile_ref",
            )})
        if policy == "T7":
            fields.update(actor=(str, "agent"), family_digest=(str | None, None))
    elif policy in {"BOOTSTRAP", "BOOTSTRAP_PROFILE", "NEW_WORKSPACE"}:
        fields = {"protocol_version": (str | None, None), "profiles": (list[str] | None, None)}
    elif policy == "INSPECT":
        fields = {"include_family_digest": (bool, False)}
    elif policy == "LIST_REPORT":
        fields = {"attempt_id": (str, ""), "head_only": (bool, False)}
    elif policy == "LIST_TASK":
        fields = {key: (str, "") for key in ("stage", "parent", "branch_of")}
        fields["references"] = (list[str] | None, None)
    elif policy == "LIST_REVIEW":
        fields = {key: (str, "") for key in (
            "review_kind", "subject_ref", "attempt_id", "authorization_ref", "profile_ref",
        )}
        fields["references"] = (list[str] | None, None)
    return fields


def register_legacy_routes(
    mcp: FastMCP, legacy: Any, router_factory: Callable[[], WorkspaceRouter],
    *, replace: bool = False,
) -> None:
    for name, policy in TOOLS.items():
        if name == "reopen_task":
            continue
        original = getattr(legacy, name)
        signature = inspect.signature(original, eval_str=True)
        additions = {key: value for key, value in _additional_fields(policy).items()
                     if key not in signature.parameters}
        parameters = [*signature.parameters.values(), *(
            inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, default=default, annotation=annotation)
            for key, (annotation, default) in additions.items()
        )]
        expanded = signature.replace(parameters=parameters, return_annotation=Any)

        def build(original: Any, name: str, policy: str, expanded: inspect.Signature,
                  additions: dict[str, tuple[Any, Any]]) -> Callable[..., Any]:
            @wraps(original)
            def invoke(**kwargs: Any) -> Any:
                bound = expanded.bind(**kwargs)
                bound.apply_defaults()
                args = dict(bound.arguments)
                router = router_factory()
                token = CURRENT_ROUTER.set(router)
                try:
                    legacy_args = {k: v for k, v in args.items() if k not in additions}
                    if policy == "GLOBAL_READ":
                        return original(**legacy_args)
                    if policy == "BIND":
                        target = Path(args["path"]).expanduser().resolve()
                        # Binding an empty existing directory authorizes no business write.
                        from fcop import Project

                        if target.is_dir() and Project(target).config_path.exists():
                            WorkspaceRouter(target, trusted_profiles=router._trusted_profiles).route()
                        if router.binding_source == "trusted server binding":
                            if not target.is_dir():
                                raise V4ProtocolError(_V4Code.INVALID_ENVELOPE,
                                                      "Binding target must be an existing directory", operation_ref=name)
                            router.root = target
                            return ToolResult(structured_content={"bound": str(target), "business_writes": 0})
                        result = original(**legacy_args)
                        if target.is_dir():
                            router.root = target
                        return result
                    if policy in {"BOOTSTRAP", "BOOTSTRAP_PROFILE"}:
                        if args.get("protocol_version") == "4.0":
                            from fcop import Project

                            if policy == "BOOTSTRAP_PROFILE":
                                from fcop_mcp.projection import unavailable

                                raise unavailable(name)
                            project = Project(router.root, trusted_profiles=router._trusted_profiles)
                            return ToolResult(structured_content=project.create_workspace(
                                protocol_version="4.0", profiles=args.get("profiles") or [],
                            ))
                        if args.get("protocol_version") not in {None, "3.0", "3.2.5"}:
                            raise V4ProtocolError(_V4Code.UNSUPPORTED_WORKSPACE_VERSION,
                                                  "Unsupported explicit bootstrap version", operation_ref=name)
                        if not (router.root / "fcop/fcop.json").exists():
                            return original(**legacy_args)
                    if not (router.root / "fcop/fcop.json").exists() and policy in {"STATUS", "OPTIONAL_OBSERVATION", "DISCOVERY"}:
                        return original(**legacy_args)
                    route = router.route()
                    if route.declared_protocol == "v3":
                        if any(args[key] != default for key, (_, default) in additions.items()):
                            raise V4ProtocolError(_V4Code.UNSUPPORTED_WORKSPACE_VERSION,
                                                  "v4-only inputs cannot be sent to legacy writers", operation_ref=name)
                        return original(**legacy_args)
                    if policy == "APPEND_AUTHORIZATION" and "expires_at" not in kwargs:
                        raise V4ProtocolError(_V4Code.AUTHORIZATION_INVALID,
                                              "expires_at must be explicit, including null", operation_ref=name)
                    if policy == "NEW_WORKSPACE":
                        from fcop import Project

                        if args.get("protocol_version") != "4.0":
                            raise V4ProtocolError(_V4Code.UNSUPPORTED_WORKSPACE_VERSION,
                                                  "New v4 workspaces require explicit protocol_version", operation_ref=name)
                        slug = args["slug"]
                        if not re.fullmatch(r"[a-z][a-z0-9-]{0,39}", slug):
                            raise V4ProtocolError(_V4Code.INVALID_ENVELOPE, "Invalid workspace slug", operation_ref=name)
                        target = router.root / "workspace" / slug
                        if (router.root / "workspace").is_symlink() or target.is_symlink():
                            raise V4ProtocolError(_V4Code.INVALID_ENVELOPE, "Symlink workspace target", operation_ref=name)
                        project = Project(target, trusted_profiles=router._trusted_profiles)
                        return ToolResult(structured_content=project.create_workspace(
                            protocol_version="4.0", profiles=args.get("profiles") or [],
                        ))
                    if (policy == "CREATE_TASK" or (policy.startswith("APPEND_") and policy != "APPEND_AUTHORIZATION")) and args.get("workspace_id") is None:
                        raise V4ProtocolError(_V4Code.INVALID_ENVELOPE,
                                              "v4 writes require workspace_id", operation_ref=name)
                    return ToolResult(structured_content=invoke_v4(route, name, policy, args))
                except V4ProtocolError as exc:
                    return core_error(exc)
                finally:
                    CURRENT_ROUTER.reset(token)

            invoke.__signature__ = expanded  # type: ignore[attr-defined]
            invoke.__annotations__ = {key: parameter.annotation for key, parameter in expanded.parameters.items()}
            invoke.__annotations__["return"] = Any
            invoke.__doc__ = (original.__doc__ or "") + (
                "\n\nVersion policy: " + policy + ". Legacy prose above applies to v3. "
                "v4 dispatch uses public Project operations and structured results; actor is not authority."
            )
            return invoke

        if replace:
            mcp.local_provider.remove_tool(name)
        metadata = getattr(original, "__fastmcp__", None)
        mcp.tool(name=name, output_schema=None,
                 tags=getattr(metadata, "tags", None),
                 annotations=getattr(metadata, "annotations", None))(
                     build(original, name, policy, expanded, additions))


class CoreErrorResult(ToolResult):
    """Carry Core's fields in the standard MCP error result, not a success string."""

    def to_mcp_result(self) -> CallToolResult:
        return CallToolResult(
            isError=True, content=self.content, structuredContent=self.structured_content,
        )


def core_error(exc: V4ProtocolError) -> CoreErrorResult:
    return CoreErrorResult(content=[], structured_content={
        "code": exc.code,
        "operation_ref": exc.operation_ref,
        "subject_ref": exc.subject_ref,
        "message": str(exc),
    })


def register_reopen(mcp: FastMCP, router_factory: Callable[[], WorkspaceRouter]) -> None:
    @mcp.tool(tags={"tier:L2"})
    def reopen_task(
        task_id: str, review_ref: str, authorization_ref: str,
        profile_ref: str, actor: str, lang: str = "",
    ) -> ToolResult:
        """Request only v4 T6 done->active. Actor is audit data, never authority.

        The independent authorization and reopen REVIEW are validated and consumed
        by Project. Trusted evaluators can only be installed at server startup.
        Repeating the same formal request returns the Core's existing result.
        """
        del lang
        try:
            route = router_factory().route()
            if route.declared_protocol != "v4":
                raise V4ProtocolError(
                    _V4Code.UNSUPPORTED_WORKSPACE_VERSION, "reopen_task requires v4",
                    operation_ref="reopen_task", subject_ref=task_id,
                )
            result = route.project.transition(
                task_id=task_id, from_stage="done", to_stage="active", tool="reopen_task",
                actor=actor, review_ref=review_ref, authorization_ref=authorization_ref,
                profile_ref=profile_ref,
            )
            return ToolResult(structured_content=result)
        except V4ProtocolError as exc:
            return core_error(exc)


def create_server(
    root: Path | str, *, trusted_profiles: Mapping[str, Callable[..., str]] | None = None,
) -> FastMCP:
    """Create a server with a startup-only trusted Profile registry."""
    from fcop_mcp import server

    check_package_compatibility()
    router = WorkspaceRouter(root, trusted_profiles=trusted_profiles)
    mcp = FastMCP("fcop")
    from fcop_mcp.governance import FCoPGovernanceMiddleware

    def legacy_audit() -> bool:
        try:
            return router.route().declared_protocol == "v3"
        except V4ProtocolError:
            return False

    mcp.add_middleware(FCoPGovernanceMiddleware(audit_enabled=legacy_audit))
    register_legacy_routes(mcp, server, lambda: router)
    register_reopen(mcp, lambda: router)
    from fcop_mcp.branches import register_branches

    register_branches(mcp, lambda: router)
    from fcop_mcp.resources import register_resources

    register_resources(mcp, server, lambda: router)
    # These catalog reads intentionally do not require workspace binding.
    for uri, handler in (
        ("fcop://teams/{team}", server.resource_team_readme),
        ("fcop://teams/{team}/{role}", server.resource_team_role_zh),
        ("fcop://teams/{team}/{role}/en", server.resource_team_role_en),
    ):
        mcp.resource(uri, mime_type="text/markdown")(handler)
    return mcp
