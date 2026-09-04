"""WP3B production behavior tests for T2/T3, locks, and private receipts."""

from __future__ import annotations

import json
import multiprocessing
import shutil
import time
from pathlib import Path
from queue import Empty
from typing import Any

import pytest

from fcop import Project
from fcop.errors import V4ProtocolError, _V4Code
from tests.conformance.v4.fixtures import (
    ATTEMPT_A,
    ATTEMPT_B,
    WorkspaceFixture,
    read_frontmatter,
    sha256_bytes,
    snapshot_tree,
)
from tests.conformance.v4.scenarios import create_request, report_request, transition_request


def _operation_worker(
    root: str, action: str, kwargs: dict[str, Any], start: Any, output: Any
) -> None:
    start.wait()
    try:
        result = getattr(Project(root), action)(**kwargs)
        output.put(("ok", result))
    except BaseException as exc:  # process boundary transports only facts
        output.put(("error", getattr(exc, "code", type(exc).__name__)))


def _hold_family_lock(
    workspace_id: str, task_id: str, acquired: Any, release: Any
) -> None:
    from fcop.v4.linearization import family_boundary

    with family_boundary(Path.cwd(), workspace_id, task_id):
        acquired.set()
        release.wait(5)


def _run_race(root: Path, calls: list[tuple[str, dict[str, Any]]]) -> list[tuple[str, Any]]:
    context = multiprocessing.get_context("spawn")
    start = context.Event()
    output = context.Queue()
    processes = [
        context.Process(
            target=_operation_worker,
            args=(str(root), action, kwargs, start, output),
        )
        for action, kwargs in calls
    ]
    for process in processes:
        process.start()
    start.set()
    results: list[tuple[str, Any]] = []
    try:
        for _ in processes:
            results.append(output.get(timeout=20))
    except Empty as exc:
        raise AssertionError("concurrent production operation did not return") from exc
    finally:
        for process in processes:
            process.join(20)
            if process.is_alive():
                process.terminate()
                process.join()
    assert all(process.exitcode == 0 for process in processes)
    return results


@pytest.fixture
def workspace(tmp_path: Path) -> WorkspaceFixture:
    return WorkspaceFixture(tmp_path).create(profiles=[])


def _receipt_paths(root: Path) -> list[Path]:
    return sorted((root / "fcop" / "operations").glob("transition-*.json"))


def _receipt(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_receipt(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def test_t2_commits_one_event_attempt_and_relative_receipt(workspace: WorkspaceFixture) -> None:
    source = workspace.task("TASK-WP3B-T2", stage="inbox", body="unchanged body")
    fields = read_frontmatter(source)
    fields["extension_field"] = {"kept": True}
    # Arrangement-only fixture mutation adds an unknown legal extension.
    from tests.conformance.v4.fixtures import _frontmatter

    source.write_bytes(_frontmatter(fields, "unchanged body"))
    result = Project(workspace.root).transition(
        **transition_request("TASK-WP3B-T2", "inbox", "active", tool="claim_task")
    )

    paths = workspace.task_paths("TASK-WP3B-T2")
    assert len(paths) == 1 and paths[0].parent.name == "active"
    target_fields = read_frontmatter(paths[0])
    assert len(target_fields["transitions"]) == 1
    event = target_fields["transitions"][0]
    assert event["attempt_id"] == result["attempt_id"]
    assert event["attempt_id"].startswith("urn:uuid:")
    assert event["from"] == "inbox" and event["to"] == "active"
    assert event["by"] == "ME" and event["tool"] == "claim_task"
    assert target_fields["extension_field"] == {"kept": True}
    assert paths[0].read_text(encoding="utf-8").endswith("unchanged body\n")
    receipt = _receipt(workspace.root / result["receipt_ref"])
    assert receipt["stage"] == "COMMITTED"
    assert receipt["source_path"].startswith("fcop/_lifecycle/inbox/")
    assert receipt["target_path"].startswith("fcop/_lifecycle/active/")
    assert "\\" not in receipt["source_path"] and ":" not in receipt["source_path"]


@pytest.mark.parametrize(
    ("from_stage", "to_stage", "tool"),
    [
        ("active", "review", "claim_task"),
        ("inbox", "review", "claim_task"),
        ("inbox", "active", "submit_task"),
    ],
)
def test_t2_wrong_edge_or_tool_is_zero_write(
    workspace: WorkspaceFixture, from_stage: str, to_stage: str, tool: str
) -> None:
    workspace.task("TASK-WP3B-BAD-T2", stage="inbox")
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(
            **transition_request("TASK-WP3B-BAD-T2", from_stage, to_stage, tool=tool)
        )
    assert caught.value.code == "INVALID_TRANSITION"
    assert snapshot_tree(workspace.root) == before


def test_t2_two_processes_create_one_event_and_one_receipt(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-RACE-T2", stage="inbox")
    request = transition_request("TASK-WP3B-RACE-T2", "inbox", "active", tool="claim_task")
    results = _run_race(workspace.root, [("transition", request), ("transition", request)])
    assert all(status == "ok" for status, _ in results)
    paths = workspace.task_paths("TASK-WP3B-RACE-T2")
    assert len(paths) == 1 and paths[0].parent.name == "active"
    assert len(read_frontmatter(paths[0])["transitions"]) == 1
    assert len(_receipt_paths(workspace.root)) == 1
    assert len({value["attempt_id"] for _, value in results}) == 1


def test_t2_never_overwrites_preexisting_target(workspace: WorkspaceFixture) -> None:
    source = workspace.task("TASK-WP3B-TARGET", stage="inbox", body="source")
    target = workspace.task("TASK-WP3B-TARGET", stage="active", body="different")
    old = source.read_bytes(), target.read_bytes()
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(
            **transition_request("TASK-WP3B-TARGET", "inbox", "active", tool="claim_task")
        )
    assert caught.value.code == "TARGET_ALREADY_EXISTS_DIFFERENT"
    assert (source.read_bytes(), target.read_bytes()) == old


def test_t3_commits_unique_head_and_full_byte_digest(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-T3", stage="active", attempt_id=ATTEMPT_A)
    project = Project(workspace.root)
    report = project.write_report(**report_request("TASK-WP3B-T3", ATTEMPT_A))
    report_path = Path(report["path"])
    result = project.transition(
        **transition_request(
            "TASK-WP3B-T3", "active", "review", tool="submit_task",
            report_ref=report["report_id"],
        )
    )
    task = read_frontmatter(workspace.task_paths("TASK-WP3B-T3")[0])
    event = task["transitions"][-1]
    assert event["evidence_ref"] == [report["report_id"]]
    assert event["evidence_digest"] == [sha256_bytes(report_path.read_bytes())]
    assert result["attempt_id"] == ATTEMPT_A and result["status"] == "COMMITTED"
    assert _receipt(workspace.root / result["receipt_ref"])["stage"] == "COMMITTED"


@pytest.mark.parametrize(
    ("case", "expected"),
    [
        ("missing", "REPORT_REQUIRED"),
        ("ambiguous", "REPORT_HEAD_AMBIGUOUS"),
        ("old", "ATTEMPT_MISMATCH"),
    ],
)
def test_t3_head_failures_are_atomic(
    workspace: WorkspaceFixture, case: str, expected: str
) -> None:
    workspace.task("TASK-WP3B-HEAD", stage="active", attempt_id=ATTEMPT_B)
    report_ref = None
    if case == "ambiguous":
        workspace.report("REPORT-WP3B-A", task_id="TASK-WP3B-HEAD", attempt_id=ATTEMPT_B)
        workspace.report("REPORT-WP3B-B", task_id="TASK-WP3B-HEAD", attempt_id=ATTEMPT_B)
    elif case == "old":
        workspace.report("REPORT-WP3B-OLD", task_id="TASK-WP3B-HEAD", attempt_id=ATTEMPT_A)
        report_ref = "REPORT-WP3B-OLD"
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(
            **transition_request(
                "TASK-WP3B-HEAD", "active", "review", tool="submit_task",
                report_ref=report_ref,
            )
        )
    assert caught.value.code == expected
    assert snapshot_tree(workspace.root) == before


def test_t3_accepts_replacement_head_and_rejects_explicit_old_head(
    workspace: WorkspaceFixture,
) -> None:
    workspace.task("TASK-WP3B-REPLACE", stage="active", attempt_id=ATTEMPT_A)
    project = Project(workspace.root)
    first = project.write_report(**report_request("TASK-WP3B-REPLACE", ATTEMPT_A))
    replacement = project.write_report(
        **report_request(
            "TASK-WP3B-REPLACE",
            ATTEMPT_A,
            report_kind="replacement",
            references=[first["report_id"]],
        )
    )
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        project.transition(
            **transition_request(
                "TASK-WP3B-REPLACE", "active", "review", tool="submit_task",
                report_ref=first["report_id"],
            )
        )
    assert caught.value.code == "REPORT_HEAD_AMBIGUOUS"
    assert snapshot_tree(workspace.root) == before
    project.transition(
        **transition_request(
            "TASK-WP3B-REPLACE", "active", "review", tool="submit_task",
            report_ref=replacement["report_id"],
        )
    )


def test_report_change_after_digest_cannot_commit(
    workspace: WorkspaceFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace.task("TASK-WP3B-EVIDENCE", stage="active", attempt_id=ATTEMPT_A)
    report = workspace.report(
        "REPORT-WP3B-EVIDENCE", task_id="TASK-WP3B-EVIDENCE", attempt_id=ATTEMPT_A
    )
    import fcop.v4.lifecycle as lifecycle

    original = lifecycle.publish_prepared

    def publish_then_tamper(root: Path, receipt: dict[str, Any]) -> Path:
        path = original(root, receipt)
        report.write_bytes(report.read_bytes() + b"tampered\n")
        return path

    monkeypatch.setattr(lifecycle, "publish_prepared", publish_then_tamper)
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(
            **transition_request(
                "TASK-WP3B-EVIDENCE", "active", "review", tool="submit_task",
                report_ref="REPORT-WP3B-EVIDENCE",
            )
        )
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert workspace.task_paths("TASK-WP3B-EVIDENCE")[0].parent.name == "active"


def test_t3_never_calls_authorization_profile(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-NO-AUTH", stage="active", attempt_id=ATTEMPT_A)
    workspace.report("REPORT-WP3B-NO-AUTH", task_id="TASK-WP3B-NO-AUTH", attempt_id=ATTEMPT_A)
    calls: list[object] = []

    def forbidden(*args: object, **kwargs: object) -> str:
        calls.append((args, kwargs))
        raise AssertionError("T3 called authorization")

    Project(workspace.root, trusted_profiles={"profile:test": forbidden}).transition(
        **transition_request(
            "TASK-WP3B-NO-AUTH", "active", "review", tool="submit_task",
            report_ref="REPORT-WP3B-NO-AUTH",
        )
    )
    assert calls == []


def test_report_replacement_and_t3_are_linearizable(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-REPORT-RACE", stage="active", attempt_id=ATTEMPT_A)
    first = Project(workspace.root).write_report(
        **report_request("TASK-WP3B-REPORT-RACE", ATTEMPT_A)
    )
    replacement_request = report_request(
        "TASK-WP3B-REPORT-RACE",
        ATTEMPT_A,
        report_kind="replacement",
        references=[first["report_id"]],
    )
    transition = transition_request(
        "TASK-WP3B-REPORT-RACE", "active", "review", tool="submit_task"
    )
    results = _run_race(
        workspace.root,
        [("write_report", replacement_request), ("transition", transition)],
    )
    assert any(status == "ok" and "to_stage" in value for status, value in results)
    path = workspace.task_paths("TASK-WP3B-REPORT-RACE")[0]
    event = read_frontmatter(path)["transitions"][-1]
    assert path.parent.name == "review"
    assert len(event["evidence_ref"]) == 1
    evidence = workspace.envelope_paths(event["evidence_ref"][0])[0]
    assert event["evidence_digest"] == [sha256_bytes(evidence.read_bytes())]


def test_branch_create_and_root_t3_are_linearizable(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-ROOT-RACE", stage="active", attempt_id=ATTEMPT_A)
    workspace.report("REPORT-WP3B-ROOT-RACE", task_id="TASK-WP3B-ROOT-RACE", attempt_id=ATTEMPT_A)
    branch = create_request("wp3b-branch-race", branch_of="TASK-WP3B-ROOT-RACE")
    transition = transition_request(
        "TASK-WP3B-ROOT-RACE", "active", "review", tool="submit_task",
        report_ref="REPORT-WP3B-ROOT-RACE",
    )
    results = _run_race(workspace.root, [("create_task", branch), ("transition", transition)])
    assert any(status == "ok" and "to_stage" in value for status, value in results)
    root_paths = workspace.task_paths("TASK-WP3B-ROOT-RACE")
    assert len(root_paths) == 1 and root_paths[0].parent.name == "review"
    branch_successes = [value for status, value in results if status == "ok" and "task_id" in value and "to_stage" not in value]
    branch_errors = [value for status, value in results if status == "error"]
    assert bool(branch_successes) != bool(branch_errors)
    if branch_successes:
        branch_paths = workspace.task_paths(branch_successes[0]["task_id"])
        assert len(branch_paths) == 1 and branch_paths[0].parent.name == "inbox"
    else:
        assert branch_errors == ["ROOT_NOT_ACTIVE"]


def test_branch_after_root_t3_is_rejected(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-ROOT-DONE", stage="active", attempt_id=ATTEMPT_A)
    workspace.report("REPORT-WP3B-ROOT-DONE", task_id="TASK-WP3B-ROOT-DONE", attempt_id=ATTEMPT_A)
    project = Project(workspace.root)
    project.transition(
        **transition_request(
            "TASK-WP3B-ROOT-DONE", "active", "review", tool="submit_task",
            report_ref="REPORT-WP3B-ROOT-DONE",
        )
    )
    with pytest.raises(V4ProtocolError) as caught:
        project.create_task(**create_request("wp3b-late-branch", branch_of="TASK-WP3B-ROOT-DONE"))
    assert caught.value.code == "ROOT_NOT_ACTIVE"


def test_branch_of_branch_is_rejected_without_create(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-ROOT", stage="active", attempt_id=ATTEMPT_A)
    workspace.task("TASK-WP3B-BRANCH", stage="active", branch_of="TASK-WP3B-ROOT")
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).create_task(
            **create_request("wp3b-depth-two", branch_of="TASK-WP3B-BRANCH")
        )
    assert caught.value.code == "BRANCH_DEPTH_EXCEEDED"
    assert snapshot_tree(workspace.root) == before


def test_distinct_standalone_tasks_do_not_share_family_lock(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-LOCK-A", stage="inbox")
    workspace.task("TASK-WP3B-LOCK-B", stage="inbox")
    context = multiprocessing.get_context("spawn")
    acquired, release = context.Event(), context.Event()
    holder = context.Process(
        target=_hold_family_lock,
        args=(workspace.workspace_id, "TASK-WP3B-LOCK-A", acquired, release),
    )
    holder.start()
    assert acquired.wait(10)
    started = time.monotonic()
    try:
        Project(workspace.root).transition(
            **transition_request("TASK-WP3B-LOCK-B", "inbox", "active", tool="claim_task")
        )
    finally:
        release.set()
        holder.join(10)
    assert time.monotonic() - started < 2
    assert holder.exitcode == 0


def _committed_t2(
    workspace: WorkspaceFixture, task_id: str
) -> tuple[dict[str, Any], dict[str, Any], bytes, Path, Path]:
    source = workspace.task(task_id, stage="inbox", body="source")
    source_bytes = source.read_bytes()
    request = transition_request(task_id, "inbox", "active", tool="claim_task")
    result = Project(workspace.root).transition(**request)
    receipt_path = workspace.root / result["receipt_ref"]
    return request, _receipt(receipt_path), source_bytes, receipt_path, Path(result["path"])


def test_prepared_source_only_resumes_exact_transaction(workspace: WorkspaceFixture) -> None:
    request, receipt, source_bytes, receipt_path, target = _committed_t2(
        workspace, "TASK-WP3B-PREPARED"
    )
    source = workspace.root / receipt["source_path"]
    source.write_bytes(source_bytes)
    target.unlink()
    receipt["stage"] = "PREPARED"
    _write_receipt(receipt_path, receipt)
    result = Project(workspace.root).transition(**request)
    assert result["attempt_id"] == receipt["attempt_id"]
    assert not source.exists() and target.exists()
    assert _receipt(receipt_path)["stage"] == "COMMITTED"


def test_target_visible_with_prepared_receipt_is_indeterminate(
    workspace: WorkspaceFixture,
) -> None:
    request, receipt, source_bytes, receipt_path, target = _committed_t2(
        workspace, "TASK-WP3B-PREPARED-TARGET"
    )
    source = workspace.root / receipt["source_path"]
    source.write_bytes(source_bytes)
    receipt["stage"] = "PREPARED"
    _write_receipt(receipt_path, receipt)
    before = source.read_bytes(), target.read_bytes(), receipt_path.read_bytes()
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(**request)
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert (source.read_bytes(), target.read_bytes(), receipt_path.read_bytes()) == before


def test_target_durable_duplicate_mechanically_converges(workspace: WorkspaceFixture) -> None:
    request, receipt, source_bytes, receipt_path, target = _committed_t2(
        workspace, "TASK-WP3B-DUPLICATE"
    )
    source = workspace.root / receipt["source_path"]
    source.write_bytes(source_bytes)
    receipt["stage"] = "TARGET_DURABLE"
    _write_receipt(receipt_path, receipt)
    result = Project(workspace.root).transition(**request)
    assert result["status"] == "COMMITTED"
    assert not source.exists() and target.exists()
    assert len(read_frontmatter(target)["transitions"]) == 1


def test_source_absent_target_durable_completes_receipt(workspace: WorkspaceFixture) -> None:
    request, receipt, _, receipt_path, target = _committed_t2(
        workspace, "TASK-WP3B-COMPLETE-RECEIPT"
    )
    receipt["stage"] = "TARGET_DURABLE"
    _write_receipt(receipt_path, receipt)
    Project(workspace.root).transition(**request)
    assert target.exists() and _receipt(receipt_path)["stage"] == "COMMITTED"


def test_target_durable_without_target_is_indeterminate(workspace: WorkspaceFixture) -> None:
    request, receipt, source_bytes, receipt_path, target = _committed_t2(
        workspace, "TASK-WP3B-MISSING-TARGET"
    )
    source = workspace.root / receipt["source_path"]
    source.write_bytes(source_bytes)
    target.unlink()
    receipt["stage"] = "TARGET_DURABLE"
    _write_receipt(receipt_path, receipt)
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(**request)
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert source.exists() and not target.exists()


def test_different_digest_duplicate_preserves_every_copy(workspace: WorkspaceFixture) -> None:
    request, receipt, source_bytes, receipt_path, target = _committed_t2(
        workspace, "TASK-WP3B-DIVERGENT"
    )
    source = workspace.root / receipt["source_path"]
    source.write_bytes(source_bytes)
    target.write_bytes(target.read_bytes() + b"different\n")
    receipt["stage"] = "TARGET_DURABLE"
    _write_receipt(receipt_path, receipt)
    before = source.read_bytes(), target.read_bytes(), receipt_path.read_bytes()
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(**request)
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert (source.read_bytes(), target.read_bytes(), receipt_path.read_bytes()) == before


@pytest.mark.parametrize("damage", ["corrupt", "escape", "duplicate"])
def test_receipt_damage_fails_closed_and_preserves_bytes(
    workspace: WorkspaceFixture, damage: str
) -> None:
    request, receipt, _, receipt_path, _ = _committed_t2(
        workspace, f"TASK-WP3B-RECEIPT-{damage}"
    )
    if damage == "corrupt":
        receipt_path.write_bytes(b"{broken")
    elif damage == "escape":
        receipt["source_path"] = "../outside.md"
        _write_receipt(receipt_path, receipt)
    else:
        duplicate = receipt_path.with_name("transition-00000000000040008000000000000000.json")
        duplicate.write_bytes(receipt_path.read_bytes())
    before = snapshot_tree(workspace.root)
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(**request)
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert snapshot_tree(workspace.root) == before


def test_failure_before_prepared_keeps_source(
    workspace: WorkspaceFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = workspace.task("TASK-WP3B-BEFORE-PREPARED", stage="inbox")
    import fcop.v4.lifecycle as lifecycle

    def fail_prepared(root: Path, receipt: dict[str, Any]) -> Path:
        del root, receipt
        raise V4ProtocolError(_V4Code.RECOVERY_REQUIRED, "injected private test boundary")

    monkeypatch.setattr(lifecycle, "publish_prepared", fail_prepared)
    with pytest.raises(V4ProtocolError):
        Project(workspace.root).transition(
            **transition_request(
                "TASK-WP3B-BEFORE-PREPARED", "inbox", "active", tool="claim_task"
            )
        )
    assert source.exists() and not _receipt_paths(workspace.root)


def test_failure_after_target_publish_preserves_indeterminate_evidence(
    workspace: WorkspaceFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = workspace.task("TASK-WP3B-AFTER-TARGET", stage="inbox")
    request = transition_request("TASK-WP3B-AFTER-TARGET", "inbox", "active", tool="claim_task")
    import fcop.v4.lifecycle as lifecycle

    original = lifecycle.set_stage

    def fail_target_stage(root: Path, path: Path, value: dict[str, Any], stage: str) -> dict[str, Any]:
        if stage == "TARGET_DURABLE":
            raise V4ProtocolError(_V4Code.RECOVERY_REQUIRED, "injected private test boundary")
        return original(root, path, value, stage)

    monkeypatch.setattr(lifecycle, "set_stage", fail_target_stage)
    with pytest.raises(V4ProtocolError):
        Project(workspace.root).transition(**request)
    target = workspace.root / "fcop/_lifecycle/active/TASK-WP3B-AFTER-TARGET.md"
    assert source.exists() and target.exists()
    monkeypatch.setattr(lifecycle, "set_stage", original)
    before = source.read_bytes(), target.read_bytes()
    with pytest.raises(V4ProtocolError) as caught:
        Project(workspace.root).transition(**request)
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert (source.read_bytes(), target.read_bytes()) == before


def test_response_loss_after_source_delete_does_not_repeat_event(
    workspace: WorkspaceFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace.task("TASK-WP3B-RESPONSE-LOSS", stage="inbox")
    request = transition_request("TASK-WP3B-RESPONSE-LOSS", "inbox", "active", tool="claim_task")
    import fcop.v4.lifecycle as lifecycle

    original = lifecycle.set_stage

    def fail_committed(root: Path, path: Path, value: dict[str, Any], stage: str) -> dict[str, Any]:
        if stage == "COMMITTED":
            raise V4ProtocolError(_V4Code.RECOVERY_REQUIRED, "lost response boundary")
        return original(root, path, value, stage)

    monkeypatch.setattr(lifecycle, "set_stage", fail_committed)
    with pytest.raises(V4ProtocolError):
        Project(workspace.root).transition(**request)
    monkeypatch.setattr(lifecycle, "set_stage", original)
    result = Project(workspace.root).transition(**request)
    task = read_frontmatter(Path(result["path"]))
    assert result["status"] == "COMMITTED" and len(task["transitions"]) == 1


def test_receipt_survives_project_relocation(workspace: WorkspaceFixture) -> None:
    request, _, _, receipt_path, _ = _committed_t2(workspace, "TASK-WP3B-MOVED")
    destination = workspace.root.parent / "moved-workspace"
    shutil.move(str(workspace.root), destination)
    moved_receipt = destination / receipt_path.relative_to(workspace.root)
    value = _receipt(moved_receipt)
    assert not Path(value["source_path"]).is_absolute()
    result = Project(destination).transition(**request)
    assert result["status"] == "COMMITTED"
    assert Path(result["path"]).is_file()


def test_inspect_state_uses_path_now_and_rejects_ambiguity(workspace: WorkspaceFixture) -> None:
    workspace.task("TASK-WP3B-INSPECT", stage="active", attempt_id=ATTEMPT_A)
    project = Project(workspace.root)
    result = project.inspect_state(task_id="TASK-WP3B-INSPECT")
    assert result["stage"] == "active" and result["current_attempt_id"] == ATTEMPT_A
    workspace.task("TASK-WP3B-INSPECT", stage="review", attempt_id=ATTEMPT_A)
    with pytest.raises(V4ProtocolError) as caught:
        project.inspect_state(task_id="TASK-WP3B-INSPECT")
    assert caught.value.code == "STATE_AMBIGUOUS"
