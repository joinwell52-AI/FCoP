"""Explicit readers resolve only their requested canonical report graphs."""

from pathlib import Path
from typing import Any

import pytest

from fcop.errors import V4ProtocolError
from fcop.v4 import reports
from tests.test_fcop.test_v4_report_queries import corrupt, files, setup_report


def another_report(app: Any) -> tuple[str, str, dict[str, Any]]:
    task = app.task("Unrelated task")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    report = app.project.write_report(
        workspace_id=app.workspace_id, sender="ME", recipient="ME", subject_ref=task,
        body="Unrelated evidence", attempt_id=attempt, report_kind="final", result="done",
    )
    return task, attempt, report


def test_explicit_queries_do_not_resolve_unrelated_graphs(tmp_path: Path, monkeypatch: Any) -> None:
    app, task, attempt, first = setup_report(tmp_path)
    other_task, other_attempt, _ = another_report(app)
    before = files(tmp_path)
    calls: list[tuple[str, str]] = []
    original = reports.report_head

    def tracked(creation: Any, subject: str, run: str) -> Any:
        calls.append((subject, run))
        return original(creation, subject, run)

    monkeypatch.setattr(reports, "report_head", tracked)
    app.project.read_report(first["report_id"])
    assert calls == [(task, attempt)]
    calls.clear()
    app.project.list_reports(subject_ref=task, head_only=True)
    assert calls == [(task, attempt)]
    calls.clear()
    app.project.list_reports()
    assert set(calls) == {(task, attempt), (other_task, other_attempt)}
    assert files(tmp_path) == before


def test_foreign_ambiguous_graph_does_not_poison_target(tmp_path: Path) -> None:
    app, task, attempt, first = setup_report(tmp_path)
    other_task, other_attempt, other = another_report(app)
    replacement = app.project.write_report(
        workspace_id=app.workspace_id, sender="ME", recipient="ME", subject_ref=other_task,
        body="Foreign competing final", attempt_id=other_attempt, report_kind="replacement",
        result="done", references=[other["report_id"]],
    )
    corrupt(Path(replacement["path"]), report_kind="final", references=[])
    before = files(tmp_path)
    assert app.project.read_report(first["report_id"])["is_head"] is True
    assert len(app.project.list_reports(subject_ref=task, attempt_id=attempt, head_only=True)) == 1
    for action in (
        lambda: app.project.list_reports(),
        lambda: app.project.read_report(other["report_id"]),
    ):
        with pytest.raises(V4ProtocolError) as caught:
            action()
        assert caught.value.code == "REPORT_HEAD_AMBIGUOUS"
    assert files(tmp_path) == before


def test_located_report_change_is_not_silently_accepted(tmp_path: Path, monkeypatch: Any) -> None:
    app, _, _, first = setup_report(tmp_path)
    original = reports.ReportQueries.list_reports

    def changed(self: Any, **kwargs: Any) -> Any:
        path = Path(first["path"])
        path.write_bytes(path.read_bytes().replace(b"Original evidence", b"Modified evidence"))
        return original(self, **kwargs)

    monkeypatch.setattr(reports.ReportQueries, "list_reports", changed)
    with pytest.raises(V4ProtocolError) as caught:
        app.project.read_report(first["report_id"])
    assert caught.value.code == "RECOVERY_REQUIRED"


def test_foreign_malformed_envelope_still_rejected(tmp_path: Path) -> None:
    app, _, _, first = setup_report(tmp_path)
    _, _, other = another_report(app)
    Path(other["path"]).write_bytes(b"invalid frontmatter")
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError):
        app.project.read_report(first["report_id"])
    assert files(tmp_path) == before
