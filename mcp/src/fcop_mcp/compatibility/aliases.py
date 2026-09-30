"""4.0.5-only opt-in Python alias; not an MCP registration."""
import warnings
from typing import Any

from fcop import Project

from fcop_mcp.canonical_tools import create_task


def write_task(core: Project, **kwargs: Any) -> dict[str, Any]:
    warnings.warn("write_task is deprecated; use create_task (shim retained for 4.0.5 only)", DeprecationWarning, stacklevel=2)
    return create_task(core, **kwargs)
