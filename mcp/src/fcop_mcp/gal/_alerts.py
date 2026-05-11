"""Governance Alert Layer (GAL) — ADR-0031.

Provides two operations:
- create_alert(): write a new ALERT-*.md file into fcop/alerts/
- list_alerts():  read and filter existing ALERT files

Design constraints:
- ALERT files are append-only (never modified after creation)
- status transitions (open → acknowledged → resolved) are done by ADMIN
  editing the file; GAL never rewrites them
- create_alert() is internal; only fcop_check() drift scanning calls it
"""
from __future__ import annotations

import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_lock = threading.Lock()


# ── Path resolution ───────────────────────────────────────────────────────────

def _alerts_dir() -> Path:
    """Return the alerts directory, creating it if needed."""
    base = os.environ.get("FCOP_PROJECT_PATH", "")
    root = Path(base) if base else Path.cwd()
    alerts = root / "fcop" / "alerts"
    alerts.mkdir(parents=True, exist_ok=True)
    return alerts


def _next_alert_id(alerts_dir: Path, date_str: str) -> str:
    """Generate the next sequential alert ID for today."""
    prefix = f"ALERT-{date_str}-"
    existing = sorted(
        p.stem for p in alerts_dir.glob(f"{prefix}*.md")
    )
    if existing:
        last_num = int(existing[-1].split("-")[-1])
    else:
        last_num = 0
    return f"{prefix}{last_num + 1:03d}"


# ── Create ────────────────────────────────────────────────────────────────────

_VALID_SEVERITIES = {"high", "medium", "low"}
_VALID_TYPES = {
    "missing_independent_verdict",
    "commit_flood_without_governance",
    "critical_tool_unreviewed",
    "long_running_without_reconciliation",
}


def create_alert(
    severity: str,
    alert_type: str,
    summary_lines: list[str],
    suggestion: str = "ADMIN review recommended",
    context: dict[str, Any] | None = None,
) -> str:
    """Write a new ALERT-*.md file. Returns the alert_id."""
    if severity not in _VALID_SEVERITIES:
        severity = "medium"
    if alert_type not in _VALID_TYPES:
        alert_type = "missing_independent_verdict"

    now = datetime.now(tz=timezone.utc)
    date_str = now.strftime("%Y%m%d")
    ts_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    with _lock:
        alerts_dir = _alerts_dir()
        alert_id = _next_alert_id(alerts_dir, date_str)
        path = alerts_dir / f"{alert_id}.md"

        summary_block = "\n".join(f"- {line}" for line in summary_lines)
        ctx_block = ""
        if context:
            ctx_lines = "\n".join(f"  {k}: {v}" for k, v in context.items())
            ctx_block = f"\n## 上下文\n\n```\n{ctx_lines}\n```\n"

        content = (
            f"---\n"
            f"alert_id: {alert_id}\n"
            f"severity: {severity}\n"
            f"type: {alert_type}\n"
            f"status: open\n"
            f"created_at: \"{ts_iso}\"\n"
            f"---\n\n"
            f"## 治理缺口摘要\n\n"
            f"{summary_block}\n"
            f"{ctx_block}\n"
            f"## 建议关注\n\n"
            f"{suggestion}\n"
        )
        path.write_text(content, encoding="utf-8")

    return alert_id


# ── List ──────────────────────────────────────────────────────────────────────

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_FIELD_RE = re.compile(r'^(\w+):\s*"?([^"\n]+)"?\s*$', re.MULTILINE)


def _parse_frontmatter(text: str) -> dict[str, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    return dict(_FIELD_RE.findall(m.group(1)))


def list_alerts(
    status: str = "",
    severity: str = "",
    last_n: int = 20,
) -> str:
    """Return a formatted summary of ALERT files."""
    alerts_dir = _alerts_dir()
    files = sorted(alerts_dir.glob("ALERT-*.md"), reverse=True)

    parsed: list[dict[str, str]] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
            meta = _parse_frontmatter(text)
            meta["_file"] = f.name
            # Extract summary block
            body = _FRONTMATTER_RE.sub("", text).strip()
            meta["_body_preview"] = body[:200]
            parsed.append(meta)
        except Exception:
            continue

    # Filter
    if status:
        parsed = [p for p in parsed if p.get("status", "") == status.lower()]
    if severity:
        parsed = [p for p in parsed if p.get("severity", "") == severity.lower()]

    parsed = parsed[:last_n]

    if not parsed:
        filters = []
        if status:
            filters.append(f"status={status}")
        if severity:
            filters.append(f"severity={severity}")
        filter_str = f" (过滤条件: {', '.join(filters)})" if filters else ""
        return f"fcop/alerts/ 目录下无匹配告警{filter_str}。\n\n治理告警由 fcop_check() 自动检测并写入，ADMIN 请运行 fcop_check() 触发扫描。"

    _SEVERITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🔵"}
    _STATUS_LABEL = {"open": "待处理", "acknowledged": "已知晓", "resolved": "已解决"}

    open_count = sum(1 for p in parsed if p.get("status") == "open")
    lines = [
        f"# 治理告警（Governance Alerts）",
        f"",
        f"共 {len(parsed)} 条" + (f"，其中 **{open_count} 条待处理**" if open_count else "，全部已处理"),
        "",
    ]

    for p in parsed:
        sev = p.get("severity", "medium")
        icon = _SEVERITY_ICON.get(sev, "⚪")
        st = p.get("status", "open")
        st_label = _STATUS_LABEL.get(st, st)
        lines += [
            f"---",
            f"### {icon} {p.get('alert_id', p['_file'])}",
            f"",
            f"- **类型**: `{p.get('type', '?')}`",
            f"- **严重度**: {sev}",
            f"- **状态**: {st_label}",
            f"- **时间**: {p.get('created_at', '?')}",
            f"",
            f"{p['_body_preview']}",
            f"",
        ]

    lines += [
        "---",
        "",
        "> 状态更新：ADMIN 直接编辑对应 ALERT-*.md 文件中的 `status` 字段",
        "> （`open` → `acknowledged` → `resolved`）。",
    ]

    return "\n".join(lines)
