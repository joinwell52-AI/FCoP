"""Thin Branch tools. All locks, validation and durable merge facts belong to Core."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastmcp import FastMCP
from fastmcp.tools import ToolResult
from fcop.errors import V4ProtocolError, _V4Code

from fcop_mcp.adapter import core_error
from fcop_mcp.routing import WorkspaceRouter


def register_branches(mcp: FastMCP, router_factory: Callable[[], WorkspaceRouter]) -> None:
    def project() -> Any:
        route = router_factory().route()
        if route.declared_protocol != "v4":
            raise V4ProtocolError(_V4Code.UNSUPPORTED_WORKSPACE_VERSION, "Branch tools require v4")
        return route.project

    @mcp.tool(tags={"tier:L2"})
    def create_branch(
        root_task_id: str,
        workspace_id: str,
        operation_id: str,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        priority: str = "P2",
    ) -> ToolResult:
        """Create a Branch through Core T1; unavailable family digest is null with reasons."""
        try:
            core = project()
            result = core.create_task(
                workspace_id=workspace_id,
                operation_id=operation_id,
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
                priority=priority,
                branch_of=root_task_id,
            )
            family = core.inspect_family(root_task_id=root_task_id)
            return ToolResult(
                structured_content={
                    **result,
                    "root_task_id": root_task_id,
                    "branch_task_id": result["task_id"],
                    "family_digest": family["family_digest"],
                    "merge_ready": family["merge_ready"],
                    "reasons": family["reasons"],
                }
            )
        except V4ProtocolError as exc:
            return core_error(exc)

    @mcp.tool(tags={"tier:L1"})
    def inspect_family(root_task_id: str) -> ToolResult:
        """Read a canonical ordered family, precise REPORT heads, readiness and convergence facts."""
        try:
            return ToolResult(
                structured_content=project().inspect_family(root_task_id=root_task_id)
            )
        except V4ProtocolError as exc:
            return core_error(exc)

    @mcp.tool(tags={"tier:L2"})
    def merge_branches(
        root_task_id: str,
        workspace_id: str,
        expected_family_digest: str,
        branch_report_heads: dict[str, str],
        conclusion: str,
        conflict_resolution: str,
        operation_id: str,
        sender: str,
        recipient: str,
    ) -> ToolResult:
        """Core atomically materializes the caller's decision. Never chooses a winner or archives Root."""
        try:
            return ToolResult(
                structured_content=project().merge_branches(
                    workspace_id=workspace_id,
                    root_task_id=root_task_id,
                    expected_family_digest=expected_family_digest,
                    branch_report_heads=branch_report_heads,
                    conclusion=conclusion,
                    conflict_resolution=conflict_resolution,
                    operation_id=operation_id,
                    sender=sender,
                    recipient=recipient,
                )
            )
        except V4ProtocolError as exc:
            return core_error(exc)
