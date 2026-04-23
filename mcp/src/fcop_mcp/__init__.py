"""fcop-mcp — the MCP server shell around the :mod:`fcop` library.

This package is intentionally thin: it takes the public API of
:class:`fcop.Project` / :mod:`fcop.teams` / :mod:`fcop.rules` and
re-exposes it via FastMCP ``@tool`` and ``@resource`` decorators so
that Cursor, Claude Desktop, and any other Model Context Protocol
client can drive the same behaviours as a native Python caller.

End users should run ``fcop-mcp`` (installed console script) or
``python -m fcop_mcp``; they should never need to import this package.

For library-level use (no MCP transport, no fastmcp dependency), install
the sibling package :mod:`fcop` and use :class:`fcop.Project` directly.

Design principles (see adr/ADR-0001, ADR-0002, ADR-0003):

* **Thin wrapper**: every tool delegates to exactly one call on a
  :class:`fcop.Project` method. No business logic lives here.
* **Surface stability**: tool names, parameter names, and return
  shapes are locked for the 0.6.x series. New capabilities become
  new tools, never modifications to existing tools.
* **Env-aware**: ``FCOP_PROJECT_DIR`` / ``FCOP_ROOM_KEY`` etc. are
  read **here**, not in the library. The library stays pure.
"""

from __future__ import annotations

from fcop_mcp._version import __version__

__all__ = ["__version__"]
