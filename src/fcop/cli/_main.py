"""Top-level ``fcop`` command-line entry point.

Dispatches subcommands (currently only ``migrate-workspace``). When
invoked with no subcommand we print the historical 0.5→0.6 MCP-server
migration message — preserving the contract enforced by
``tests/test_fcop/test_compat_cli.py`` so users who upgraded from the
old MCP-server-as-CLI era still get actionable guidance and a non-zero
exit code.

The two responsibilities are split deliberately:

* :func:`main` — pure dispatch + argv parsing. Stays small.
* The legacy 0.5→0.6 message lives in :mod:`fcop._compat_cli` and is
  imported lazily so tests that exercise just the new subcommands
  don't need to touch the legacy text.

This module is internal API — only the *console-script behaviour* is
public (per ADR-0001). Callers should not ``import fcop.cli._main``.
"""

from __future__ import annotations

import argparse
import sys
from typing import IO

from fcop.cli import migrate_workspace as _migrate_ws


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fcop",
        description=(
            "FCoP — Agent Runtime Protocol library CLI. "
            "Most users only need 'fcop migrate-workspace'; everything "
            "else lives in the Python library API."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=False)
    _migrate_ws.add_subparser(sub)
    return parser


def main(argv: list[str] | None = None, *, stdout: IO[str] | None = None) -> int:
    """Console-script entry point.

    Returns the process exit code. ``argv`` defaults to ``sys.argv[1:]``;
    tests pass it explicitly to avoid monkey-patching.
    """
    args_list = list(argv) if argv is not None else sys.argv[1:]

    if not args_list:
        # Preserve the 0.5→0.6 compat behaviour: bare ``fcop`` prints
        # the migration guidance to stderr and exits non-zero. Imported
        # lazily so the legacy module's stderr write is not triggered by
        # the new subcommand path.
        from fcop._compat_cli import main as _legacy_main

        return _legacy_main()

    parser = _build_parser()
    args = parser.parse_args(args_list)

    if not getattr(args, "cmd", None):
        parser.print_help(file=stdout or sys.stdout)
        return 0

    func = getattr(args, "func", None)
    if func is None:
        # Subparser without a func — defensive; shouldn't happen for
        # registered subcommands.
        parser.print_help(file=stdout or sys.stdout)
        return 1

    return func(args, stdout=stdout)  # type: ignore[no-any-return]


if __name__ == "__main__":  # pragma: no cover — manual invocation
    sys.exit(main())
