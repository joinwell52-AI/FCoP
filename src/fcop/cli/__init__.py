"""FCoP command-line interface.

The ``fcop`` console script's main entry point lives in
:mod:`fcop.cli._main`. It dispatches to subcommands (currently only
``migrate-workspace``); when invoked with no subcommand it preserves
the historical 0.5→0.6 migration message so users who upgraded from
the old MCP-server-as-CLI era still see actionable guidance.

This module is part of the ``fcop`` library's **internal API**: only
the console script entry point and the documented subcommand surface
(``fcop migrate-workspace …``) are covered by ADR-0001's API stability
charter. Re-homing the helper modules in a future minor is allowed.
"""

from __future__ import annotations

__all__: list[str] = []
