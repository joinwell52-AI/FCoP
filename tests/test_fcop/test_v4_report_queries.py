"""WP4B.2/.2a public read boundary contracts, separate from frozen tests."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
import yaml
from examples.v4.application import Application

from fcop.errors import V4ProtocolError


def files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def setup_report(root: Path) -> tuple[Application, str, str, dict[str, Any]]:
    app = Application(root)
    task = app.task("Read projection")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    result = app.project.write_report(
        workspace_id=app.workspace_id, sender="ME", recipient="ME", subject_ref=task,
        body="Original evidence", attempt_id=attempt, report_kind="final", result="done",
    )
    return app, task, attempt, result


def corrupt(path: Path, **changes: Any) -> None:
    _, front, body = path.read_text(encoding="utf-8").split("---", 2)
    fields = yaml.safe_load(front)
    fields.update(changes)
    path.write_bytes(("---\n" + yaml.safe_dump(fields, sort_keys=False) + "---" + body).encode())


def test_query_replacement_metadata_and_t3(tmp_path: Path) -> None:
    app, task, attempt, first = setup_report(tmp_path)
    old = app.project.read_report(first["report_id"])
    assert old["is_head"] is True
    second = app.project.write_report(
        workspace_id=app.workspace_id, sender="QA", recipient="ME", subject_ref=task,
        body="Replacement evidence", attempt_id=attempt, report_kind="replacement", result="done",
        references=[first["report_id"]],
    )
    before = files(tmp_path)
    rows = app.project.list_reports(subject_ref=task, attempt_id=attempt)
    assert len(rows) == 2
    head = app.project.read_report(Path(second["path"]).name)
    old = app.project.read_report(first["report_id"])
    assert head["is_head"] is True and old["is_head"] is False
    assert head["head_ref"] == old["head_ref"] == second["report_id"]
    assert head["replaces"] == first["report_id"] and old["replaces"] is None
    assert old["head_digest"] == hashlib.sha256(Path(second["path"]).read_bytes()).hexdigest()
    assert not Path(old["path"]).is_absolute() and "\\" not in old["path"]
    assert "Original evidence" in old["content"]
    assert app.project.list_reports(head_only=True) == [head]
    assert app.project.list_reports(sender="QA") == [head]
    assert len(app.project.list_reports(limit=1, offset=1)) == 1
    assert app.project.list_reports(limit=0) == []
    assert app.project.list_reports(subject_ref="TASK-absent") == []
    assert files(tmp_path) == before
    app.move(task, "active", "review", "submit_task", report_ref=second["report_id"])
    event = app.project.inspect_state(task_id=task)["last_transition"]
    assert second["report_id"] in event["evidence_ref"]
    assert head["head_digest"] in event["evidence_digest"]


@pytest.mark.parametrize("case,code", [
    ("multiple", "REPORT_HEAD_AMBIGUOUS"), ("replacement-fork", "REPORT_HEAD_AMBIGUOUS"),
    ("cycle", "REPORT_REQUIRED"), ("self", "REPORT_HEAD_AMBIGUOUS"),
    ("missing", "REPORT_HEAD_AMBIGUOUS"), ("cross-subject", "REPORT_HEAD_AMBIGUOUS"),
    ("cross-attempt", "REPORT_HEAD_AMBIGUOUS"),
])
def test_query_graph_errors_match_t3(tmp_path: Path, case: str, code: str) -> None:
    app, task, attempt, first = setup_report(tmp_path)
    path = Path(first["path"])
    if case in {"multiple", "replacement-fork", "cycle"}:
        second = app.project.write_report(
            workspace_id=app.workspace_id, sender="ME", recipient="ME", subject_ref=task,
            body="Later", attempt_id=attempt, report_kind="replacement", result="done",
            references=[first["report_id"]],
        )
        if case == "multiple":
            corrupt(Path(second["path"]), report_kind="final", references=[])
        elif case == "cycle":
            corrupt(path, report_kind="replacement", references=[second["report_id"]])
        else:
            extra_id = "REPORT-" + uuid4().hex
            extra = path.with_name(extra_id + ".md")
            extra.write_bytes(Path(second["path"]).read_bytes())
            corrupt(extra, report_id=extra_id)
    else:
        target = first["report_id"]
        if case == "missing":
            target = "REPORT-missing"
        elif case.startswith("cross-"):
            extra_id = "REPORT-" + uuid4().hex
            extra = path.with_name(extra_id + ".md")
            extra.write_bytes(path.read_bytes())
            changes = {"report_id": extra_id}
            if case == "cross-subject":
                changes["subject_ref"] = app.task("Other task")
            else:
                changes["attempt_id"] = uuid4().urn
            corrupt(extra, **changes)
            target = extra_id
        corrupt(path, report_kind="replacement", references=[target])
    before = files(tmp_path)
    for act in (
        lambda: app.project.list_reports(subject_ref=task, attempt_id=attempt, head_only=True),
        lambda: app.project.list_reports(limit=0, offset=999),
        lambda: app.project.read_report(first["report_id"]),
        lambda: app.move(task, "active", "review", "submit_task", report_ref=first["report_id"]),
    ):
        with pytest.raises(V4ProtocolError) as caught:
            act()
        assert caught.value.code == code
        assert files(tmp_path) == before


def test_empty_and_bad_query_arguments(tmp_path: Path) -> None:
    app = Application(tmp_path)
    task = app.task("Empty")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    assert app.project.list_reports() == []
    before = files(tmp_path)
    for kwargs, code in [
        ({"subject_ref": task, "attempt_id": attempt, "head_only": True}, "REPORT_REQUIRED"),
        ({"attempt_id": attempt}, "INVALID_ENVELOPE"),
        ({"limit": -1}, "INVALID_ENVELOPE"), ({"offset": -1}, "INVALID_ENVELOPE"),
    ]:
        with pytest.raises(V4ProtocolError) as caught:
            app.project.list_reports(**kwargs)
        assert caught.value.code == code
    assert files(tmp_path) == before


@pytest.mark.parametrize("damage", ["utf8", "schema", "malformed"])
def test_invalid_report_never_skipped(tmp_path: Path, damage: str) -> None:
    app, _, _, report = setup_report(tmp_path)
    path = Path(report["path"])
    if damage == "schema":
        corrupt(path, version=3)
    else:
        path.write_bytes(b"\xff" if damage == "utf8" else b"not frontmatter")
    before = files(tmp_path)
    for act in (lambda: app.project.list_reports(limit=0), lambda: app.project.read_report(path.name)):
        with pytest.raises(V4ProtocolError):
            act()
    assert files(tmp_path) == before


@pytest.mark.parametrize("locator", ["../REPORT-escape.md", "fcop/reports/REPORT-a.md", "REPORT-", "REPORT-a.md.md"])
def test_exact_report_locator(tmp_path: Path, locator: str) -> None:
    app = Application(tmp_path)
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError):
        app.project.read_report(locator)
    assert files(tmp_path) == before


@pytest.mark.parametrize("query", ["list", "read"])
@pytest.mark.parametrize("writer", ["replacement", "corruption"])
def test_query_concurrent_writer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                 query: str, writer: str) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    from fcop.v4 import reports

    app, task, attempt, first = setup_report(tmp_path)
    entered, release, writing = Event(), Event(), Event()
    original = reports.report_head

    def paused(*args: Any, **kwargs: Any) -> Any:
        entered.set()
        assert release.wait(10)
        return original(*args, **kwargs)

    monkeypatch.setattr(reports, "report_head", paused)

    def read() -> Any:
        try:
            if query == "list":
                return app.project.list_reports(head_only=True)
            return [app.project.read_report(first["report_id"])]
        except V4ProtocolError as error:
            return error.code

    def write() -> None:
        writing.set()
        if writer == "replacement":
            app.project.write_report(
                workspace_id=app.workspace_id, sender="ME", recipient="ME", subject_ref=task,
                body="Concurrent", attempt_id=attempt, report_kind="replacement", result="done",
                references=[first["report_id"]],
            )
        else:
            path = Path(first["path"])
            identity = "REPORT-" + uuid4().hex
            path.with_name(identity + ".md").write_bytes(
                path.read_bytes().replace(first["report_id"].encode(), identity.encode()))

    with ThreadPoolExecutor(max_workers=2) as pool:
        reader = pool.submit(read)
        assert entered.wait(10)
        concurrent = pool.submit(write)
        assert writing.wait(10)
        if writer == "corruption":
            concurrent.result(timeout=10)
        else:
            assert not concurrent.done()  # Reader holds the same family boundary.
        release.set()
        result = reader.result(timeout=10)
        concurrent.result(timeout=10)
    if writer == "corruption":
        assert result in {"REPORT_HEAD_AMBIGUOUS", "RECOVERY_REQUIRED"}
    elif isinstance(result, str):
        assert result == "RECOVERY_REQUIRED"
    else:
        assert len(result) == 1 and result[0]["is_head"] is True
    monkeypatch.setattr(reports, "report_head", original)
    if writer == "replacement":
        assert len(app.project.list_reports(head_only=True)) == 1
