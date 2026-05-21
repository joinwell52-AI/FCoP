"""FCoP 3.0 lifecycle layer — reference implementation.

This sub-package is the in-code form of the FCoP 3.0 protocol:

* :mod:`fcop.lifecycle.state` — Rule A (path is the NOW truth) and
  the 5-bucket directory topology.
* :mod:`fcop.lifecycle.transitions` — the allowed-transitions table
  (Rule C: explicit tool invocation only).
* :mod:`fcop.lifecycle.events` — the append-only ``transitions:``
  array inside file frontmatter (Rules E / F / G).
* :mod:`fcop.lifecycle.atomic` — the write-then-rename atomic commit
  pattern (spec §2.4).

This is the **public** programmable surface of FCoP 3.0. Stability
contract: anything re-exported here follows semver against the
``fcop`` package version — breaking changes need a MAJOR bump.

Design notes:

* Zero coupling to :mod:`fcop.project`. Hosts that only want the
  protocol primitives can ``from fcop.lifecycle import ...`` without
  pulling the full v2-compatible facade.
* Zero coupling to MCP / LLM SDKs. Same rationale as the parent
  :mod:`fcop` package.
* Errors raised from this sub-package (notably
  :class:`IllegalTransitionError` and :class:`CrossDeviceError`) do
  not inherit :class:`fcop.errors.FcopError` — they are protocol-
  layer errors that callers may adapt at their own boundary.

Quick example::

    from pathlib import Path
    from datetime import datetime, timezone
    from fcop.lifecycle import (
        Stage,
        TransitionEvent,
        commit,
        create,
        ensure_lifecycle_dirs,
    )

    root = Path("./myproject")
    ensure_lifecycle_dirs(root)

    # 1. Create a task in inbox/.
    create_event = TransitionEvent(
        at=datetime.now(timezone.utc),
        from_stage=None,
        to_stage=Stage.INBOX,
        by="PM-01",
        tool="create_task",
    )
    result = create(
        "TASK-20260521-001-PM-to-DEV.md",
        "---\\nprotocol: fcop\\nversion: 3\\ntype: TASK\\n---\\nbody\\n",
        create_event,
        project_root=root,
    )
    print(result.destination_path)  # → .../_lifecycle/inbox/TASK-...md

    # 2. Claim it: inbox → active.
    claim_event = TransitionEvent(
        at=datetime.now(timezone.utc),
        from_stage=Stage.INBOX,
        to_stage=Stage.ACTIVE,
        by="DEV-01",
        tool="claim_task",
    )
    commit(result.destination_path, Stage.ACTIVE, claim_event, project_root=root)
"""

from __future__ import annotations

from fcop.lifecycle.atomic import (
    AtomicCommitResult,
    CrossDeviceError,
    commit,
    create,
)
from fcop.lifecycle.events import (
    FRONTMATTER_FENCE,
    MIGRATION_TOOL_NAME,
    TransitionEvent,
    append_event_to_frontmatter,
    event_from_mapping,
    event_to_mapping,
    read_events,
    synthetic_baseline_event,
)
from fcop.lifecycle.state import (
    LIFECYCLE_DIRNAME,
    STAGE_NAMES,
    Stage,
    ensure_lifecycle_dirs,
    lifecycle_root,
    same_mount,
    stage_dir,
    stage_of_path,
)
from fcop.lifecycle.transitions import (
    ALLOWED_TRANSITIONS,
    IllegalTransitionError,
    TransitionSpec,
    is_allowed,
    tool_for,
    validate_transition,
)

__all__ = [
    # state.py
    "LIFECYCLE_DIRNAME",
    "STAGE_NAMES",
    "Stage",
    "ensure_lifecycle_dirs",
    "lifecycle_root",
    "same_mount",
    "stage_dir",
    "stage_of_path",
    # transitions.py
    "ALLOWED_TRANSITIONS",
    "IllegalTransitionError",
    "TransitionSpec",
    "is_allowed",
    "tool_for",
    "validate_transition",
    # events.py
    "FRONTMATTER_FENCE",
    "MIGRATION_TOOL_NAME",
    "TransitionEvent",
    "append_event_to_frontmatter",
    "event_from_mapping",
    "event_to_mapping",
    "read_events",
    "synthetic_baseline_event",
    # atomic.py
    "AtomicCommitResult",
    "CrossDeviceError",
    "commit",
    "create",
]
