"""Register only manifest handlers against an immutable process-owned root."""
from __future__ import annotations

import inspect
from collections.abc import Callable, Mapping
from functools import wraps
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from fastmcp import FastMCP
from fastmcp.tools import ToolResult
from fcop import Project
from fcop.errors import V4ProtocolError
from mcp.types import CallToolResult

from fcop_mcp.canonical_tools import MANIFEST


class CoreErrorResult(ToolResult):
    def to_mcp_result(self) -> CallToolResult:
        return CallToolResult(isError=True, content=self.content, structuredContent=self.structured_content)


def bind(entry: Mapping[str, Any], root: Path, trusted_profiles: Mapping[str, Callable[..., str]]) -> Callable[..., ToolResult]:
    fn = entry["handler"]
    signature = inspect.signature(fn, eval_str=True)
    signature = signature.replace(parameters=list(signature.parameters.values())[1:])

    @wraps(fn)
    def invoke(**kwargs: Any) -> ToolResult:
        try:
            core = (SimpleNamespace(path=root) if fn.__name__ == "validate_workspace"
                    else Project(root, trusted_profiles=trusted_profiles))
            if fn.__name__ not in {"init_workspace", "validate_workspace"}:
                from fcop.workspace import _open
                _open(root)
            return ToolResult(structured_content=fn(core, **kwargs))
        except V4ProtocolError as exc:
            return CoreErrorResult(content=[], structured_content=dict(code=exc.code,
                operation_ref=exc.operation_ref, subject_ref=exc.subject_ref, message=str(exc)))
    invoke.__dict__["__signature__"] = signature
    invoke.__annotations__ = {k: v.annotation for k, v in signature.parameters.items()}
    invoke.__annotations__["return"] = ToolResult
    return invoke


def create_server(root: Path | str, *, trusted_profiles: Mapping[str, Callable[..., str]] | None = None) -> FastMCP:
    from fcop_mcp._version import __version__
    from fcop_mcp.routing import check_package_compatibility
    check_package_compatibility()
    bound_root = Path(root).resolve()
    profiles = dict(trusted_profiles or {})
    mcp = FastMCP("fcop", version=__version__)
    for entry in MANIFEST.values():
        mcp.tool(name=entry["name"], description=entry["description"], output_schema=None)(bind(entry, bound_root, profiles))
    from fcop_mcp.canonical_resources import register_resources
    register_resources(mcp, bound_root)
    return mcp


def export_manifest() -> list[dict[str, Any]]:
    from fastmcp.tools import FunctionTool
    result = []
    for entry in MANIFEST.values():
        tool = FunctionTool.from_function(bind(entry, Path.cwd(), {}))
        result.append({k: v for k, v in entry.items() if k != "handler"} | {"inputSchema": tool.parameters})
    return result
