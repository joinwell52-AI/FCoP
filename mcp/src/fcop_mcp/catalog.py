"""Public offline Tool Catalog; no server/runtime import or second metadata table."""
from __future__ import annotations

from fcop_mcp.disposition import TOOLS

__all__ = ["get_tool_catalog"]


def get_tool_catalog(name: str | None = None) -> list[dict[str, str]]:
    """Return fresh deterministic name/disposition rows from the authoritative registry.

    Unknown names raise KeyError. Signatures remain owned by the actual registered
    handlers and are intentionally not duplicated into a display-only catalog.
    """
    names = sorted(TOOLS) if name is None else [name]
    return [{"name": key, "disposition": TOOLS[key]} for key in names]
