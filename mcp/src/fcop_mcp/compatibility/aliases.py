"""4.0.5-only opt-in Python alias; not an MCP registration."""
import warnings

from fcop_mcp.canonical_tools import create_task


def write_task(core, **kwargs):
    warnings.warn("write_task is deprecated; use create_task (shim retained for 4.0.5 only)", DeprecationWarning, stacklevel=2)
    return create_task(core, **kwargs)
