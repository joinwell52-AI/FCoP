"""Inspection data classes for fcop_audit() — ADR-0032.

Three core types:

- :class:`RemediationStep`  — a single copy-paste-ready remediation command.
- :class:`Violation`        — one protocol compliance finding with remediation.
- :class:`InspectionReport` — the full audit output (= inspection + plan).

The rendered Markdown follows the L3 format defined in ADR-0032 §6:
  frontmatter → summary → P0/P1/P2 violations → Execution Block → re-check tip.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

__all__ = [
    "RemediationStep",
    "Violation",
    "InspectionReport",
    "ViolationSeverity",
    "InspectionScope",
    "OverallStatus",
]

ViolationSeverity = Literal["P0", "P1", "P2"]
InspectionScope = Literal["new", "upgrade", "takeover"]
OverallStatus = Literal["green", "needs_remediation", "blocked"]


@dataclass(frozen=True)
class RemediationStep:
    """One copy-paste-ready remediation action.

    Attributes:
        action:             Human-readable one-liner describing what this step does.
        command:            The actual shell / MCP command (PowerShell default).
        command_unix:       Unix/bash equivalent when *command* is PowerShell-specific.
        executor:           Who should run this step.
        estimated_minutes:  Rough time estimate.
        tier:               Execution priority (1=now / 2=this sprint / 3=later).
        rollback:           How to undo this step if something goes wrong.
        precondition:       Required precondition before executing (if any).
    """

    action: str
    command: str
    command_unix: str | None = None
    executor: Literal["ADMIN", "PM", "OPS", "mixed"] = "ADMIN"
    estimated_minutes: int = 5
    tier: Literal[1, 2, 3] = 1
    rollback: str | None = None
    precondition: str | None = None


@dataclass(frozen=True)
class Violation:
    """One protocol compliance finding.

    Attributes:
        violation_id:   Sequential ID like "P0-001", "P1-003".
        severity:       P0 = blocking / P1 = normative / P2 = cosmetic.
        rule_violated:  Short rule reference, e.g. "Rule 2 (桶错位)".
        summary:        One sentence description.
        evidence:       List of file paths / counts that prove the violation.
        impact:         Business / governance impact.
        remediation:    Ordered list of :class:`RemediationStep`.
        scan_source:    Name of the ``_scan_*`` method that produced this.
    """

    violation_id: str
    severity: ViolationSeverity
    rule_violated: str
    summary: str
    evidence: list[str]
    impact: str
    remediation: list[RemediationStep]
    scan_source: str = ""


@dataclass
class InspectionReport:
    """Full audit output: compliance findings + tiered remediation plan.

    Calling :meth:`to_markdown` produces the L3 report (ADR-0032 §6)
    which is written to ``fcop/shared/INSPECTION-{date}-{NNN}-{scope}.md``.
    """

    inspection_id: str
    scope: InspectionScope
    project_path: Path
    inspected_at: datetime
    fcop_version: str
    fcop_rules_version_local: str | None
    fcop_rules_version_package: str
    overall_status: OverallStatus
    violations: list[Violation] = field(default_factory=list)

    # Computed in __post_init__
    p0_count: int = field(init=False, default=0)
    p1_count: int = field(init=False, default=0)
    p2_count: int = field(init=False, default=0)
    estimated_total_minutes: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        self.p0_count = sum(1 for v in self.violations if v.severity == "P0")
        self.p1_count = sum(1 for v in self.violations if v.severity == "P1")
        self.p2_count = sum(1 for v in self.violations if v.severity == "P2")
        self.estimated_total_minutes = sum(
            s.estimated_minutes
            for v in self.violations
            for s in v.remediation
        )

    # ── Rendering ─────────────────────────────────────────────────────────

    def to_markdown(self) -> str:
        """Render the L3 report (frontmatter + violations + Execution Block)."""
        parts: list[str] = []

        # ── YAML frontmatter ─────────────────────────────────────────────
        status_icon = {"green": "🟢", "needs_remediation": "🟠", "blocked": "🔴"}.get(
            self.overall_status, "⚪"
        )
        parts.append("---")
        parts.append("protocol: fcop")
        parts.append("version: 1")
        parts.append("kind: inspection")
        parts.append(f"inspection_id: {self.inspection_id}")
        parts.append(f"scope: {self.scope}")
        parts.append(f"project: {self.project_path}")
        parts.append(f"inspector: SYSTEM (fcop_audit {self.fcop_version})")
        parts.append(f'inspected_at: "{self.inspected_at.isoformat()}"')
        parts.append(f"fcop_version: {self.fcop_version}")
        if self.fcop_rules_version_local:
            parts.append(f"fcop_rules_version_local: {self.fcop_rules_version_local}")
        else:
            parts.append("fcop_rules_version_local: null")
        parts.append(f"fcop_rules_version_package: {self.fcop_rules_version_package}")
        parts.append(f"overall_status: {self.overall_status}")
        parts.append(f"p0_violations: {self.p0_count}")
        parts.append(f"p1_violations: {self.p1_count}")
        parts.append(f"p2_violations: {self.p2_count}")
        parts.append(f"estimated_total_minutes: {self.estimated_total_minutes}")
        parts.append("---")
        parts.append("")

        # ── Title ────────────────────────────────────────────────────────
        parts.append(
            f"# 体检报告 · {self.project_path.name} (scope: {self.scope})"
        )
        parts.append("")

        # ── Summary ──────────────────────────────────────────────────────
        parts.append("## 摘要")
        parts.append("")
        parts.append(f"- **状态**: {status_icon} {self.overall_status}")
        parts.append(
            f"- **违规分档**: P0 阻塞性 {self.p0_count} 项"
            f" / P1 规范性 {self.p1_count} 项"
            f" / P2 整洁性 {self.p2_count} 项"
        )
        if self.estimated_total_minutes:
            parts.append(
                f"- **预估整改时长**: ~{self.estimated_total_minutes} 分钟"
            )
        else:
            parts.append("- **预估整改时长**: N/A（无违规）")
        parts.append("")

        if self.overall_status == "blocked":
            parts.append(
                "> ⛔ **BLOCKED**：存在 P0 级阻塞性违规，必须先修复再继续开发。"
            )
            parts.append("")

        if not self.violations:
            parts.append("✅ **无违规发现**。项目符合 fcop 协议规范。")
            parts.append("")
        else:
            # ── Violations by severity ───────────────────────────────────
            for severity, label in [
                ("P0", "P0 · 阻塞性违规（必须先修）"),
                ("P1", "P1 · 规范性违规（本 sprint 内修）"),
                ("P2", "P2 · 整洁性违规（后续清理）"),
            ]:
                group = [v for v in self.violations if v.severity == severity]
                if not group:
                    continue
                parts.append(f"## {label}")
                parts.append("")
                for v in group:
                    parts.extend(_render_violation(v))
            # ── Execution Block ──────────────────────────────────────────
            parts.extend(_render_execution_block(self.violations))

        # ── Re-check tip ─────────────────────────────────────────────────
        parts.append("## 复检建议")
        parts.append("")
        parts.append("完成 Tier 1 后运行：")
        parts.append("")
        parts.append("```")
        parts.append('fcop_audit(scope="auto")')
        parts.append("```")
        parts.append("")
        parts.append(
            f"复检报告将落 `fcop/shared/{self.inspection_id[:-3]}NNN-{self.scope}.md`，"
            "不覆盖本份（append-only）。"
        )
        parts.append("")

        return "\n".join(parts)

    def to_dict(self) -> dict[str, Any]:
        """Machine-readable JSON representation for downstream tooling."""
        return {
            "inspection_id": self.inspection_id,
            "scope": self.scope,
            "project_path": str(self.project_path),
            "inspected_at": self.inspected_at.isoformat(),
            "fcop_version": self.fcop_version,
            "fcop_rules_version_local": self.fcop_rules_version_local,
            "fcop_rules_version_package": self.fcop_rules_version_package,
            "overall_status": self.overall_status,
            "p0_violations": self.p0_count,
            "p1_violations": self.p1_count,
            "p2_violations": self.p2_count,
            "estimated_total_minutes": self.estimated_total_minutes,
            "violations": [
                {
                    "violation_id": v.violation_id,
                    "severity": v.severity,
                    "rule_violated": v.rule_violated,
                    "summary": v.summary,
                    "evidence": v.evidence,
                    "impact": v.impact,
                    "scan_source": v.scan_source,
                    "remediation": [
                        {
                            "action": s.action,
                            "command": s.command,
                            "command_unix": s.command_unix,
                            "executor": s.executor,
                            "estimated_minutes": s.estimated_minutes,
                            "tier": s.tier,
                            "rollback": s.rollback,
                            "precondition": s.precondition,
                        }
                        for s in v.remediation
                    ],
                }
                for v in self.violations
            ],
        }

    def to_json(self) -> str:
        """JSON string of :meth:`to_dict`."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ── Internal rendering helpers ─────────────────────────────────────────────


def _render_violation(v: Violation) -> list[str]:
    lines: list[str] = []
    lines.append(f"### {v.violation_id} · {v.rule_violated}")
    lines.append("")
    lines.append(f"**{v.summary}**")
    lines.append("")
    if v.evidence:
        lines.append("- **实证**:")
        for e in v.evidence:
            lines.append(f"  - `{e}`")
    lines.append(f"- **影响**: {v.impact}")
    lines.append("")
    if v.remediation:
        first = v.remediation[0]
        lines.append("- **整改命令**:")
        lines.append(f"  ```{'powershell' if _is_powershell(first.command) else ''}")
        lines.append(f"  {first.command}")
        if first.command_unix:
            lines.append(f"  # unix: {first.command_unix}")
        lines.append("  ```")
        lines.append(f"- **执行人**: {first.executor}")
        lines.append(f"- **预估**: {first.estimated_minutes} 分钟")
        if first.rollback:
            lines.append(f"- **回滚**: `{first.rollback}`")
        if first.precondition:
            lines.append(f"- ⚠️ **前置条件**: {first.precondition}")
        lines.append(f"- **Tier**: {first.tier}")
    lines.append("")
    return lines


def _render_execution_block(violations: list[Violation]) -> list[str]:
    """Render the Execution Block — all remediation steps grouped by tier."""
    lines: list[str] = []
    lines.append("---")
    lines.append("")
    lines.append("## ▶ 执行块 · Execution Block")
    lines.append("")
    lines.append(
        "> 按 Tier 顺序执行。每步命令可直接复制；执行前请确认无未提交工作（`git status`）。"
    )
    lines.append("")

    for tier, tier_label in [
        (1, "Tier 1 · 立即（今日内，无前置，低风险）"),
        (2, "Tier 2 · 本 sprint（1~2 天，有前置依赖）"),
        (3, "Tier 3 · 后续清理（下一 sprint，低优先）"),
    ]:
        tier_steps: list[tuple[Violation, RemediationStep]] = []
        for v in violations:
            for s in v.remediation:
                if s.tier == tier:
                    tier_steps.append((v, s))

        if not tier_steps:
            continue

        est = sum(s.estimated_minutes for _, s in tier_steps)
        lines.append(f"### {tier_label}（预计 ~{est} 分钟）")
        lines.append("")

        for i, (v, s) in enumerate(tier_steps, 1):
            lines.append(f"#### 步骤 {i} · {s.action}")
            if s.precondition:
                lines.append(f"⚠️ **前置**: {s.precondition}")
                lines.append("")
            lang = "powershell" if _is_powershell(s.command) else ""
            lines.append(f"```{lang}")
            lines.append(s.command)
            lines.append("```")
            if s.command_unix:
                lines.append("```bash")
                lines.append("# unix:")
                lines.append(s.command_unix)
                lines.append("```")
            lines.append(f"**执行人**: {s.executor}　|　**关联**: {v.violation_id}")
            if s.rollback:
                lines.append(f"**回滚**: `{s.rollback}`")
            lines.append("")

    return lines


def _is_powershell(cmd: str) -> bool:
    """Heuristic: command looks like PowerShell if it uses Get-*, ForEach-Object, etc."""
    ps_keywords = ("Get-", "ForEach-Object", "Out-File", "Set-Content", "Select-Object")
    return any(kw in cmd for kw in ps_keywords)
