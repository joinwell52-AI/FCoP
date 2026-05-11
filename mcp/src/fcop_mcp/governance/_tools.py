"""Governance MCP tool implementations.

These functions are registered as @mcp.tool in server.py.
Kept here to avoid bloating server.py further.
"""

from __future__ import annotations

import datetime
import json
from collections import Counter

from .events import _resolve_log_path


def _load_events(risk_filter: str = "", tag_filter: str = "") -> tuple[list[dict], int]:
    """Load events from the log, apply optional filters. Returns (filtered, total)."""
    log_path = _resolve_log_path()
    if not log_path.exists():
        return [], 0

    raw_lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    all_events: list[dict] = []
    for line in raw_lines:
        try:
            all_events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    total = len(all_events)
    if risk_filter:
        all_events = [e for e in all_events if e.get("risk") == risk_filter]
    if tag_filter:
        all_events = [e for e in all_events if e.get("tag") == tag_filter]

    return all_events, total


def _fmt_ts(ts: float) -> str:
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


RISK_ICON = {"Safe": "✓", "Sensitive": "⚠", "Critical": "✗"}


def impl_list_governance_events(last_n: int, risk: str, tag: str) -> str:
    log_path = _resolve_log_path()
    if not log_path.exists():
        return (
            "Governance event log not found.\n"
            f"Expected: {log_path}\n"
            "The log is created automatically when fcop-mcp handles the first tool call."
        )

    events, total = _load_events(risk, tag)
    shown = events[-last_n:]

    lines = [
        f"=== FCoP Governance Events (showing {len(shown)} of {total} total) ===",
        f"Log: {log_path}",
        f"Filters: risk={risk or 'all'}, tag={tag or 'all'}",
        "",
    ]

    if not shown:
        lines.append("(no events match filters)")
        return "\n".join(lines)

    for ev in shown:
        ts = ev.get("ts") or ev.get("emitted_at", 0.0)
        icon = RISK_ICON.get(ev.get("risk", ""), "?")
        lines.append(
            f"{icon} [{_fmt_ts(ts)}] {ev.get('tool', '?'):<28} "
            f"risk={ev.get('risk', '?'):<10} tag={ev.get('tag', '?'):<14} "
            f"args={ev.get('args_hash', '')[:12]}  session={ev.get('session_id') or '-'}"
        )

    counts = Counter(ev.get("risk", "?") for ev in shown)
    lines += [
        "",
        f"Summary: Safe={counts.get('Safe', 0)}  "
        f"Sensitive={counts.get('Sensitive', 0)}  "
        f"Critical={counts.get('Critical', 0)}",
    ]
    return "\n".join(lines)


def impl_get_governance_summary() -> str:
    log_path = _resolve_log_path()
    if not log_path.exists():
        return "Governance log not found. No tool calls have been processed yet."

    events, _ = _load_events()
    if not events:
        return "Governance log is empty."

    risk_counts: Counter = Counter(ev.get("risk", "unknown") for ev in events)
    tool_counts: Counter = Counter(ev.get("tool", "unknown") for ev in events)
    critical_events = [ev for ev in events if ev.get("tag") == "CRITICAL_TAG"]

    lines = [
        "=== FCoP Governance Summary ===",
        "",
        f"Total tool calls logged: {len(events)}",
        "",
        "By risk level:",
        f"  ✓ Safe:      {risk_counts.get('Safe', 0)}",
        f"  ⚠ Sensitive: {risk_counts.get('Sensitive', 0)}",
        f"  ✗ Critical:  {risk_counts.get('Critical', 0)}",
        "",
        "Top 10 tools by call count:",
    ]

    for tool, count in tool_counts.most_common(10):
        lines.append(f"  {count:4d}  {tool}")

    if critical_events:
        lines += [
            "",
            f"⚠ CRITICAL_TAG events ({len(critical_events)}) — verify these have Task + Review coverage:",
        ]
        for ev in critical_events[-10:]:
            ts = ev.get("ts") or ev.get("emitted_at", 0.0)
            lines.append(
                f"  [{_fmt_ts(ts)}] {ev.get('tool', '?')}  "
                f"args_hash={ev.get('args_hash', '')[:12]}"
            )

    return "\n".join(lines)
