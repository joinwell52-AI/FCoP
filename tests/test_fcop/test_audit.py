"""Tests for Project.audit() and scan_* methods (ADR-0032).

Three scenario fixtures:
- ``empty_project`` — truly empty dir, scope=new
- ``fcop_project``  — initialized fcop project, scope=upgrade / new
- ``takeover_project`` — legacy non-fcop project with typical violations

Each scan_* method is tested independently via the takeover fixture.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fcop import InspectionReport, Project


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture()
def empty_project(tmp_path: Path) -> Project:
    """Truly empty directory — scope=new."""
    return Project(tmp_path)


@pytest.fixture()
def fcop_project(tmp_path: Path) -> Project:
    """Initialized fcop project with protocol rules deployed."""
    proj = Project(tmp_path)
    proj.init(team="dev-team", lang="zh")
    proj.deploy_protocol_rules()
    return proj


@pytest.fixture()
def takeover_project(tmp_path: Path) -> Project:
    """Legacy non-fcop project with typical violations."""
    # No fcop.json, lots of files
    fcop_dir = tmp_path / "fcop"
    fcop_dir.mkdir()
    (fcop_dir / "tasks").mkdir()
    (fcop_dir / "reports").mkdir()
    (fcop_dir / "issues").mkdir()
    (fcop_dir / "reviews").mkdir()
    (fcop_dir / "shared").mkdir()

    # Rule 2 violation: REPORT file in tasks/ instead of reports/
    (fcop_dir / "tasks" / "REPORT-001.md").write_text(
        "---\nprotocol: fcop\nkind: report\nreport_id: REPORT-001\n---\n# Report\n",
        encoding="utf-8",
    )
    # Grass-roots role file (no kind:)
    (fcop_dir / "PM-01.md").write_text(
        "# PM 角色定义\n这是草根角色书。\n",
        encoding="utf-8",
    )
    # Rogue manifest
    (fcop_dir / "codeflow.json").write_text(
        json.dumps({"custom": "manifest"}),
        encoding="utf-8",
    )
    # Ghost prefix
    (fcop_dir / "tasks" / "DRAFT-feature.md").write_text(
        "# 草稿\n",
        encoding="utf-8",
    )
    # No .cursor/rules/ at all, no AGENTS.md, no CLAUDE.md
    return Project(tmp_path)


# ── InspectionReport unit tests ────────────────────────────────────────────


def test_inspection_report_counts() -> None:
    from fcop.inspection import InspectionReport, RemediationStep, Violation

    step = RemediationStep(action="fix it", command="echo done", tier=1)
    v0 = Violation("P0-001", "P0", "Rule 0", "summary", [], "impact", [step])
    v1 = Violation("P1-001", "P1", "Rule 2", "summary", [], "impact", [step])
    v2 = Violation("P2-001", "P2", "Rule 5", "summary", [], "impact", [step])

    from datetime import datetime, timezone

    report = InspectionReport(
        inspection_id="INSPECTION-20260512-001",
        scope="takeover",
        project_path=Path("/tmp/proj"),
        inspected_at=datetime.now(tz=timezone.utc),
        fcop_version="1.3.0",
        fcop_rules_version_local=None,
        fcop_rules_version_package="2.3.0",
        overall_status="blocked",
        violations=[v0, v1, v2],
    )
    assert report.p0_count == 1
    assert report.p1_count == 1
    assert report.p2_count == 1
    assert report.estimated_total_minutes == 3 * 5  # default 5 min per step


def test_inspection_report_to_markdown_contains_execution_block() -> None:
    from datetime import datetime, timezone

    from fcop.inspection import InspectionReport, RemediationStep, Violation

    step = RemediationStep(
        action="Deploy rules",
        command="redeploy_rules()",
        executor="ADMIN",
        estimated_minutes=1,
        tier=1,
        rollback="git checkout -- .",
    )
    v = Violation("P0-001", "P0", "Rule 0", "Missing rules", [".cursor/rules/fcop-rules.mdc"], "big impact", [step])
    report = InspectionReport(
        inspection_id="INSPECTION-20260512-001",
        scope="takeover",
        project_path=Path("/tmp/test"),
        inspected_at=datetime.now(tz=timezone.utc),
        fcop_version="1.3.0",
        fcop_rules_version_local=None,
        fcop_rules_version_package="2.3.0",
        overall_status="blocked",
        violations=[v],
    )
    md = report.to_markdown()
    assert "kind: inspection" in md
    assert "INSPECTION-20260512-001" in md
    assert "▶ 执行块" in md
    assert "Tier 1" in md
    assert "redeploy_rules()" in md
    assert "git checkout" in md  # rollback
    assert "复检建议" in md


def test_inspection_report_to_dict() -> None:
    from datetime import datetime, timezone

    from fcop.inspection import InspectionReport, RemediationStep, Violation

    step = RemediationStep(action="fix", command="echo", tier=1)
    v = Violation("P1-001", "P1", "Rule 2", "misplaced", ["fcop/tasks/REPORT-001.md"], "impact", [step])
    report = InspectionReport(
        inspection_id="INSPECTION-20260512-002",
        scope="takeover",
        project_path=Path("/tmp/p"),
        inspected_at=datetime.now(tz=timezone.utc),
        fcop_version="1.3.0",
        fcop_rules_version_local=None,
        fcop_rules_version_package="2.3.0",
        overall_status="needs_remediation",
        violations=[v],
    )
    d = report.to_dict()
    assert d["overall_status"] == "needs_remediation"
    assert d["p1_violations"] == 1
    assert d["violations"][0]["violation_id"] == "P1-001"
    assert d["violations"][0]["remediation"][0]["command"] == "echo"


# ── scan_* unit tests ──────────────────────────────────────────────────────


def test_scan_cursor_rules_detects_missing(takeover_project: Project) -> None:
    violations = takeover_project._scan_cursor_rules()
    p0 = [v for v in violations if v.severity == "P0"]
    assert p0, "Should detect missing protocol rules"
    evidence_flat = " ".join(" ".join(v.evidence) for v in p0)
    assert "fcop-rules.mdc" in evidence_flat or "AGENTS.md" in evidence_flat


def test_scan_cursor_rules_clean(fcop_project: Project) -> None:
    # Initialized project should have the rules deployed
    violations = fcop_project._scan_cursor_rules()
    p0 = [v for v in violations if v.severity == "P0"]
    assert not p0, "Initialized project should have no P0 cursor-rules violations"


def test_scan_shared_deployment_detects_empty(takeover_project: Project) -> None:
    violations = takeover_project._scan_shared_deployment()
    assert violations, "Empty shared/ should yield a violation"
    assert violations[0].severity in ("P0", "P1")


def test_scan_shared_deployment_clean(fcop_project: Project) -> None:
    violations = fcop_project._scan_shared_deployment()
    assert not violations, "Initialized project shared/ should be compliant"


def test_scan_misplaced_envelopes(takeover_project: Project) -> None:
    violations = takeover_project._scan_misplaced_envelopes()
    assert violations, "REPORT in tasks/ should be flagged"
    assert violations[0].severity == "P1"
    assert any("REPORT-001.md" in e for e in violations[0].evidence)


def test_scan_legacy_role_docs(takeover_project: Project) -> None:
    violations = takeover_project._scan_legacy_role_docs()
    assert violations, "Grass-roots PM-01.md should be flagged"
    assert any("PM-01.md" in e for e in violations[0].evidence)


def test_scan_legacy_manifests(takeover_project: Project) -> None:
    violations = takeover_project._scan_legacy_manifests()
    assert violations, "codeflow.json should be flagged"
    assert any("codeflow.json" in e for e in violations[0].evidence)


def test_scan_ghost_prefixes(takeover_project: Project) -> None:
    violations = takeover_project._scan_ghost_prefixes()
    assert violations, "DRAFT-feature.md should be flagged"
    assert any("DRAFT" in e for e in violations[0].evidence)


# ── Project.audit() integration tests ─────────────────────────────────────


def test_audit_new_scope_returns_report(empty_project: Project) -> None:
    report = empty_project.audit(scope="new", output="stdout")
    assert isinstance(report, InspectionReport)
    assert report.scope == "new"


def test_audit_takeover_finds_violations(takeover_project: Project) -> None:
    report = takeover_project.audit(scope="takeover", output="stdout")
    assert report.overall_status in ("needs_remediation", "blocked")
    assert report.p0_count > 0 or report.p1_count > 0


def test_audit_writes_file(takeover_project: Project) -> None:
    report = takeover_project.audit(scope="takeover", output="file")
    shared = takeover_project.shared_dir
    expected = shared / f"{report.inspection_id}-takeover.md"
    assert expected.exists(), f"Expected {expected} to be written"
    content = expected.read_text(encoding="utf-8")
    assert "kind: inspection" in content
    assert "▶ 执行块" in content


def test_audit_auto_scope_infers_takeover(takeover_project: Project) -> None:
    report = takeover_project.audit(scope="auto", output="stdout")
    # Non-empty dir without fcop.json → takeover
    assert report.scope == "takeover"


def test_audit_green_project(fcop_project: Project) -> None:
    report = fcop_project.audit(scope="new", output="stdout")
    # Initialized project should be fully green
    assert report.overall_status == "green"
    assert not report.violations
