"""Governance drift signal detection — GAL Layer 3 scanning (ADR-0031).

Called by fcop_check() to detect governance gaps and emit ALERT files.
Returns a list of alert_ids created in this scan (empty if no gaps found).

Signal definitions (ADR-0031 §3):
  S1 missing_independent_verdict  — CRITICAL_TAG events without a Review file
  S2 commit_flood_without_governance — many governance events, no review
  S3 critical_tool_unreviewed     — alias of S1 for tool-level check
  S4 long_running_without_reconciliation — open tasks older than threshold
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from fcop_mcp.gal._alerts import create_alert


def _project_root() -> Path:
    base = os.environ.get("FCOP_PROJECT_PATH", "")
    return Path(base) if base else Path.cwd()


# ── Signal S1 / S3: CRITICAL_TAG events without corresponding Review ──────────

def _scan_critical_unreviewed(root: Path) -> list[str]:
    """Detect CRITICAL_TAG tool calls that have no matching Review."""
    events_path = root / "fcop_events.jsonl"
    if not events_path.exists():
        return []

    # Collect CRITICAL_TAG events in last 24h
    cutoff = time.time() - 86_400
    critical_tools: list[dict] = []
    try:
        with events_path.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                    if e.get("tag") == "CRITICAL_TAG" and e.get("ts", 0) >= cutoff:
                        critical_tools.append(e)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []

    if not critical_tools:
        return []

    # Check if any Review file exists in fcop/reviews/ in the same window
    reviews_dir = root / "fcop" / "reviews"
    review_count = 0
    if reviews_dir.exists():
        for rf in reviews_dir.glob("REVIEW-*.md"):
            try:
                mtime = rf.stat().st_mtime
                if mtime >= cutoff:
                    review_count += 1
            except OSError:
                continue

    if review_count > 0:
        return []

    # No reviews found — governance gap
    tool_names = list({e.get("tool", "?") for e in critical_tools})
    oldest_ts = min(e.get("ts", time.time()) for e in critical_tools)
    age_h = (time.time() - oldest_ts) / 3600

    alert_id = create_alert(
        severity="high",
        alert_type="critical_tool_unreviewed",
        summary_lines=[
            f"过去 24h 内检测到 {len(critical_tools)} 次 CRITICAL_TAG 工具调用",
            f"涉及工具：{', '.join(tool_names)}",
            f"最早事件距今约 {age_h:.1f}h",
            "对应时间窗内无任何 Review 文件（fcop/reviews/）",
        ],
        suggestion="ADMIN 请确认上述高风险操作已有对应 Review 或 human_approval 记录。",
        context={
            "critical_event_count": len(critical_tools),
            "tools": ", ".join(tool_names),
            "window_hours": 24,
            "review_files_found": review_count,
        },
    )
    return [alert_id]


# ── Signal S4: long-running open tasks without report ────────────────────────

def _scan_stale_tasks(root: Path) -> list[str]:
    """Detect open TASK-*.md files older than 24h without a REPORT."""
    tasks_dir = root / "fcop" / "tasks"
    if not tasks_dir.exists():
        return []

    cutoff = time.time() - 86_400  # 24h threshold
    stale: list[str] = []
    for tf in tasks_dir.glob("TASK-*.md"):
        try:
            if tf.stat().st_mtime < cutoff:
                text = tf.read_text(encoding="utf-8", errors="ignore")
                # Simple heuristic: if file contains "status: open" and no archive marker
                if "status: open" in text and "archived" not in text.lower():
                    stale.append(tf.name)
        except OSError:
            continue

    if not stale:
        return []

    alert_id = create_alert(
        severity="low",
        alert_type="long_running_without_reconciliation",
        summary_lines=[
            f"检测到 {len(stale)} 个 Task 处于 open 状态超过 24h 未归档",
            *[f"  - {name}" for name in stale[:5]],
            *(["  - ...（更多）"] if len(stale) > 5 else []),
        ],
        suggestion="ADMIN 或任务负责 Agent 确认任务状态，推进 report → archive 闭环。",
        context={"stale_task_count": len(stale)},
    )
    return [alert_id]


# ── Public entry point ────────────────────────────────────────────────────────

def run_drift_scan() -> tuple[int, str]:
    """Run all drift signal scans. Returns (alert_count, summary_text)."""
    root = _project_root()
    created: list[str] = []

    created += _scan_critical_unreviewed(root)
    created += _scan_stale_tasks(root)

    if not created:
        return 0, "GAL: 未检测到治理漂移信号。"

    lines = [
        f"⚠ GAL: 检测到 {len(created)} 个新治理告警",
        "",
    ]
    for aid in created:
        lines.append(f"  - {aid}  →  fcop/alerts/{aid}.md")
    lines += [
        "",
        "运行 `list_alerts` 工具查看详情，ADMIN 确认后更新 status 字段。",
    ]
    return len(created), "\n".join(lines)
