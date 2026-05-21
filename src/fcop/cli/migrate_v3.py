"""``fcop migrate --to-v3`` subcommand — v2 → FCoP 3.0 layout migration.

Thin argparse wrapper around :mod:`fcop.lifecycle.migrate`. The
engine, planning, and apply logic all live there; this module only
handles command-line glue + dry-run-first ergonomics.

Usage (per spec §9):

    fcop migrate --to-v3            # dry-run (default)
    fcop migrate --to-v3 --apply    # actually do it
    fcop migrate --to-v3 --apply --workspace docs/agents/
                                    # explicit workspace dir

Exit codes:

    0 — success (dry-run completed, or apply finished successfully)
    1 — apply failed (an underlying error surfaced)
    2 — refused (MIXED topology, or other plan-level abort)

Design constraint (per chat agreement on 2026-05-21): adding this
subcommand must not change the behaviour of any existing subcommand
or the bare ``fcop`` invocation. The dispatcher in
``fcop.cli._main`` registers us alongside ``migrate-workspace``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import IO

from fcop.lifecycle import migrate as _engine
from fcop.lifecycle.detect import Topology

__all__ = [
    "add_subparser",
    "run",
]


def add_subparser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the ``migrate`` subparser on the top-level dispatcher.

    The subcommand is called ``migrate`` (not ``migrate-v3``) so the
    user-facing command stays ``fcop migrate --to-v3``. The
    ``--to-v3`` flag is required to make the intent explicit and to
    leave room for future ``--to-vN`` targets without breaking the
    sub-command name.
    """
    p = subparsers.add_parser(
        "migrate",
        help="Migrate an FCoP workspace between protocol versions.",
        description=(
            "Migrate this project's FCoP workspace to a newer protocol "
            "version. Currently the only supported target is 3.0 "
            "(--to-v3), which moves tasks/log/* into the _lifecycle/ "
            "topology and stamps a baseline transition event onto "
            "every migrated file. Dry-run by default; pass --apply "
            "to execute."
        ),
    )
    p.add_argument(
        "--to-v3",
        action="store_true",
        required=True,
        help="Migrate to FCoP 3.0 _lifecycle/ topology. Required.",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the move. Without this flag the command is a dry-run.",
    )
    p.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help=(
            "Explicit workspace directory (relative or absolute). "
            "When omitted, the migrator auto-detects fcop/ first, "
            "then docs/agents/ for 0.7.x legacy layouts."
        ),
    )
    p.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root. Default: current working directory.",
    )
    p.set_defaults(func=_dispatch)


def _resolve(project_root: Path, p: Path | None) -> Path | None:
    if p is None:
        return None
    return p if p.is_absolute() else (project_root / p).resolve()


def _dispatch(args: argparse.Namespace, *, stdout: IO[str] | None = None) -> int:
    """argparse callback: build plan, optionally apply, print summary."""
    out = stdout or sys.stdout
    project_root = Path(args.project_root).resolve()
    workspace = _resolve(project_root, args.workspace)

    plan_obj = _engine.plan(project_root, workspace_root=workspace)

    if args.apply:
        if plan_obj.topology_before.topology == Topology.MIXED:
            out.write(_engine.render_summary(plan_obj, applied=False))
            out.write(
                "ERROR: refusing to apply — MIXED topology. "
                "Resolve the half-migrated state by hand and re-run.\n"
            )
            return 2
        try:
            _engine.apply(plan_obj)
        except Exception as exc:  # noqa: BLE001 — surface any failure
            out.write(_engine.render_summary(plan_obj, applied=False))
            out.write(f"ERROR: {exc}\n")
            return 1

    out.write(
        _engine.render_summary(plan_obj, applied=args.apply and plan_obj.applied)
    )
    return 0


def run(argv: list[str] | None = None, *, stdout: IO[str] | None = None) -> int:
    """Standalone entry point — used by tests so they can drive the
    subcommand without going through the top-level ``fcop`` parser.
    """
    parser = argparse.ArgumentParser(prog="fcop migrate")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_subparser(sub)
    args = parser.parse_args(["migrate", *(argv or [])])
    return _dispatch(args, stdout=stdout)
