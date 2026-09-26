"""Public offline Tool Catalog; no server/runtime import or second metadata table."""
from __future__ import annotations

from fcop_mcp.canonical_tools import MANIFEST

__all__ = ["get_tool_catalog"]


def get_tool_catalog(name: str | None = None) -> list[dict]:
    """Return fresh deterministic metadata rows from the authoritative registry.

    Unknown names raise KeyError. Signatures remain owned by the actual registered
    handlers and are intentionally not duplicated into a display-only catalog.
    """
    names = sorted(MANIFEST) if name is None else [name]
    return [{k: v for k, v in MANIFEST[key].items() if k != "handler"} for key in names]


def export_tool_explorer() -> list[dict]:
    """Generate Explorer rows and input schemas from the same registered handlers."""
    from fcop_mcp.registry import export_manifest
    return export_manifest()
