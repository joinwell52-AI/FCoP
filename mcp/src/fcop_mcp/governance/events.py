"""Event Logger — append-only audit event stream.

This is the "audit blood vessel" of the FCoP governance system.
Without this, Layer 3 (fcop_check / post-hoc audit) has nothing to reconcile against.

Design:
  - append-only: never overwrite, never delete
  - structured JSON lines (one event per line)
  - emit is synchronous and blocking: event MUST be persisted
    before execution decision is returned to caller
  - default log path: <project_dir>/fcop_events.jsonl
    (overridable via FCOP_EVENT_LOG env var)

Event schema:
  {
    "type":           "tool_call_intercept",
    "tool":           str,
    "risk":           "Safe" | "Sensitive" | "Critical",
    "decision":       "ALLOW" | "REVIEW" | "BLOCK",
    "args_hash":      str (sha256 hex),
    "approval_token": str | null,
    "session_id":     str | null,
    "timestamp":      float (unix epoch, UTC),
    "emitted_at":     float (unix epoch, UTC)
  }
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

_lock = threading.Lock()

_DEFAULT_LOG_NAME = "fcop_events.jsonl"


def _resolve_log_path() -> Path:
    """Resolve event log file path.

    Priority:
      1. FCOP_EVENT_LOG env var (absolute or relative)
      2. <cwd>/fcop_events.jsonl
    """
    env_path = os.environ.get("FCOP_EVENT_LOG")
    if env_path:
        return Path(env_path)
    return Path.cwd() / _DEFAULT_LOG_NAME


def emit_event(event: dict[str, Any]) -> None:
    """Write a governance event to the append-only audit log.

    Thread-safe.  Raises on I/O error (caller must handle or the
    interceptor should fail closed rather than silently drop events).
    """
    event = dict(event)
    event.setdefault("emitted_at", time.time())

    log_path = _resolve_log_path()
    line = json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n"

    with _lock, log_path.open("a", encoding="utf-8") as fh:
        fh.write(line)
