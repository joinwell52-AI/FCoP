"""WP3A implementation evidence; no imports from the frozen v4 driver."""

from __future__ import annotations

import hashlib
import inspect
import json
import multiprocessing
from pathlib import Path
from typing import Any

import pytest
import yaml

from fcop import Project
from fcop.errors import FcopError, V4ProtocolError
from fcop.v4.encoding import operation_lock, publish


def snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def fields(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8").split("---\n", 2)[1])


def workspace(root: Path) -> tuple[Project, dict[str, Any]]:
    project = Project(root)
    manifest = project.create_workspace()
    request = {
        "workspace_id": manifest["workspace_id"],
        "operation_id": "same-key",
        "sender": "ME",
        "recipient": "ME",
        "subject": "Task",
        "body": "body\n",
    }
    return project, request


def _create_worker(root: str, request: dict[str, Any], barrier: Any, queue: Any) -> None:
    barrier.wait(timeout=10)
    try:
        queue.put(("ok", Project(root).create_task(**request)))
    except V4ProtocolError as exc:
        queue.put(("error", exc.code))


def race(root: Path, requests: list[dict[str, Any]]) -> list[tuple[str, Any]]:
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    barrier = ctx.Barrier(len(requests))
    children = [
        ctx.Process(target=_create_worker, args=(str(root), req, barrier, queue))
        for req in requests
    ]
    try:
        for child in children:
            child.start()
        results = [queue.get(timeout=20) for _ in children]
        for child in children:
            child.join(timeout=10)
            assert child.exitcode == 0
        return results
    finally:
        for child in children:
            if child.is_alive():
                child.terminate()
                child.join(timeout=5)
        queue.close()


@pytest.mark.parametrize("different", [False, True])
def test_spawn_same_key_and_restart(tmp_path: Path, different: bool) -> None:
    project, request = workspace(tmp_path)
    requests = [request, {**request, "body": "different\n"} if different else request]
    results = race(tmp_path, requests)
    successes = [value for status, value in results if status == "ok"]
    failures = [value for status, value in results if status == "error"]
    assert len(successes) == (1 if different else 2)
    assert failures == (["OPERATION_ID_CONFLICT"] if different else [])
    assert len({item["task_id"] for item in successes}) == 1
    result = successes[0]
    assert len(list((tmp_path / "fcop/_lifecycle").glob("*/TASK-*.md"))) == 1
    assert len(list((tmp_path / "fcop/operations").glob("*.json"))) == 1
    task = fields(result["path"])
    assert len(task["transitions"]) == 1
    winner = (
        requests[0]
        if Path(result["path"]).read_text(encoding="utf-8").endswith("\nbody\n")
        else requests[1]
    )
    before = snapshot(tmp_path)
    restarted = race(tmp_path, [winner])[0]
    assert restarted[0] == "ok" and restarted[1]["existing"] is True
    assert project.create_task(**winner)["existing"] is True
    for name in ("task_id", "path", "digest"):
        assert restarted[1][name] == result[name]
    assert snapshot(tmp_path) == before


def test_digest_normalization_and_t1_oracle(tmp_path: Path) -> None:
    project, request = workspace(tmp_path)
    raw = {**request, "subject": "e\u0301", "body": "a\r\nb\rc\n\n", "references": ["Z", "A", "A"]}
    first = project.create_task(**raw)
    before = snapshot(tmp_path)
    second = project.create_task(
        **{
            **raw,
            "subject": "é",
            "body": "a\nb\nc\n",
            "operation_kind": "create_task",
            "priority": "P2",
            "references": ["A", "Z"],
            "parent": None,
            "branch_of": None,
            "thread_key": "different-profile-thread",
            "risk_level": "high",
        }
    )
    assert second["existing"] and second["task_id"] == first["task_id"]
    assert snapshot(tmp_path) == before
    expected = {
        "contract": "fcop-create-task-v1",
        "workspace_id": request["workspace_id"],
        "operation_id": "same-key",
        "operation_kind": "create_task",
        "sender": "ME",
        "recipient": "ME",
        "subject": "é",
        "body": "a\nb\nc\n",
        "priority": "P2",
        "parent": None,
        "branch_of": None,
        "references": ["A", "Z"],
    }
    encoded = json.dumps(
        expected, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    assert first["digest"] == hashlib.sha256(encoded).hexdigest()
    task = fields(first["path"])
    assert "status" not in task and Path(first["path"]).parent.name == "inbox"
    event = task["transitions"][0]
    assert event == {
        "at": task["created_at"],
        "from": None,
        "to": "inbox",
        "by": "ME",
        "tool": "create_task",
    }
    assert all(item["code"] == "REFERENCE_UNRESOLVED" for item in first["warnings"])


@pytest.mark.parametrize(
    "change,code",
    [
        (
            {"workspace_id": "urn:uuid:22222222-2222-4222-8222-222222222222"},
            "WORKSPACE_ID_MISMATCH",
        ),
        ({"operation_id": "../escape"}, "INVALID_ENVELOPE"),
        ({"operation_id": "x" * 129}, "INVALID_ENVELOPE"),
        ({"operation_kind": "lifecycle_transition"}, "INVALID_ENVELOPE"),
        ({"parent": "TASK-missing"}, "RELATION_INVALID"),
        ({"parent": ["TASK-one", "TASK-two"]}, "RELATION_INVALID"),
        ({"branch_of": "../outside"}, "RELATION_INVALID"),
        ({"references": ["../outside"]}, "RELATION_INVALID"),
        ({"sender": ""}, "INVALID_ENVELOPE"),
        ({"body": None}, "INVALID_ENVELOPE"),
        ({"body": "invalid\ud800"}, "INVALID_ENVELOPE"),
    ],
)
def test_rejection_zero_writes(tmp_path: Path, change: dict[str, Any], code: str) -> None:
    project, request = workspace(tmp_path)
    before = snapshot(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.create_task(**{**request, **change})
    assert isinstance(caught.value, FcopError)
    assert caught.value.code == code
    assert caught.value.operation_ref
    assert caught.value.subject_ref
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize(
    "key",
    [
        "profile_evaluator",
        "profile_resolver",
        "policy",
        "trusted_profiles",
        "profile_result",
        "caller_judge",
    ],
)
def test_caller_judge_never_writes(tmp_path: Path, key: str) -> None:
    project, request = workspace(tmp_path)
    before = snapshot(tmp_path)
    with pytest.raises(V4ProtocolError):
        project.create_task(**{**request, key: lambda **_: "AUTHORIZED"})
    assert snapshot(tmp_path) == before


def test_trusted_registry_copied_frozen_and_never_evaluated(tmp_path: Path) -> None:
    calls = []

    def evaluator(**kwargs: Any) -> str:
        calls.append(kwargs)
        return "DENIED"

    original = {"profile:test": evaluator}
    project = Project(tmp_path, trusted_profiles=original)
    manifest = project.create_workspace(profiles=["profile:test"])
    original["profile:test"] = lambda **_: "AUTHORIZED"
    assert project._trusted_profiles["profile:test"] is evaluator
    with pytest.raises(TypeError):
        project._trusted_profiles["profile:test"] = original["profile:test"]
    project.create_task(
        workspace_id=manifest["workspace_id"],
        operation_id="no-auth",
        sender="ME",
        recipient="ME",
        subject="T1",
        body="body",
    )
    assert calls == []


@pytest.mark.parametrize(
    "change,code",
    [
        ({"protocol": "other"}, "UNSUPPORTED_PROTOCOL"),
        ({"protocol_version": "4.1"}, "UNSUPPORTED_WORKSPACE_VERSION"),
        ({"encoding": {"name": "unknown", "version": "4.0"}}, "UNSUPPORTED_ENCODING"),
    ],
)
def test_unsupported_manifest_fail_closed(
    tmp_path: Path, change: dict[str, Any], code: str
) -> None:
    _, _request_fields = workspace(tmp_path)
    path = tmp_path / "fcop/fcop.json"
    data = json.loads(path.read_bytes())
    path.write_bytes((json.dumps({**data, **change}) + "\n").encode())
    before = snapshot(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        Project(tmp_path)
    assert caught.value.code == code
    assert snapshot(tmp_path) == before


def test_create_duplicate_and_derive_identity(tmp_path: Path) -> None:
    source = tmp_path / "source"
    project, request = workspace(source)
    before = snapshot(source)
    with pytest.raises(V4ProtocolError):
        project.create_workspace()
    with pytest.raises(V4ProtocolError) as caught:
        project.derive_workspace(
            destination=tmp_path / "mirror", mode="independent-writable", retain_workspace_id=True
        )
    assert caught.value.code == "WORKSPACE_ID_CLONE_CONFLICT"
    assert not (tmp_path / "mirror").exists()
    derived = project.derive_workspace(
        destination=tmp_path / "derived", mode="independent-writable", retain_workspace_id=False
    )
    assert derived["workspace_id"] != request["workspace_id"]
    assert snapshot(source) == before
    assert Project(source).is_initialized()


@pytest.mark.parametrize(
    "mutation", ["type", "id", "workspace", "timestamp", "utf8", "crlf", "duplicate"]
)
def test_inspect_really_parses_envelopes(tmp_path: Path, mutation: str) -> None:
    project, request = workspace(tmp_path)
    task = project.create_task(**request)
    path = Path(task["path"])
    relative = path.relative_to(tmp_path).as_posix()
    assert project.inspect_state(envelope_path=relative)["type"] == "TASK"
    text = path.read_text(encoding="utf-8")
    changed = {
        "type": text.replace("type: TASK", "type: EVAL"),
        "id": text.replace(task["task_id"], "TASK-different"),
        "workspace": text.replace(
            request["workspace_id"], "urn:uuid:22222222-2222-4222-8222-222222222222"
        ),
        "timestamp": text.replace(fields(path)["created_at"], "2026-09-04T12:00:00"),
        "crlf": text.replace("\n", "\r\n"),
        "duplicate": text.replace("protocol: fcop", "protocol: fcop\nprotocol: fcop"),
        "utf8": text,
    }[mutation]
    path.write_bytes(changed.encode() + (b"\xff" if mutation == "utf8" else b""))
    before = snapshot(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.inspect_state(envelope_path=relative)
    assert caught.value.code == (
        "WORKSPACE_ID_MISMATCH" if mutation == "workspace" else "INVALID_ENVELOPE"
    )
    assert snapshot(tmp_path) == before


def test_append_only_all_three_fact_types(tmp_path: Path) -> None:
    project, request = workspace(tmp_path)
    task = project.create_task(**request)
    common = {
        "workspace_id": request["workspace_id"],
        "sender": "ME",
        "recipient": "ME",
        "body": "evidence",
        "subject_ref": task["task_id"],
    }
    report_request = {
        **common,
        "attempt_id": "urn:uuid:aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "report_kind": "final",
        "result": "done",
    }
    report = project.write_report(**report_request)
    issue = project.write_issue(**common, severity="medium")
    review = project.write_review(**common, review_kind="assessment", decision="needs_human")
    before = snapshot(tmp_path)
    replacement = project.write_report(
        **{**report_request, "report_kind": "replacement", "references": [report["report_id"]]}
    )
    second_issue = project.write_issue(**common, severity="medium", references=[issue["issue_id"]])
    approval = project.mark_human_approved(
        review_id=review["review_id"],
        approver="human:test",
        decision="approved",
        profile_ref="profile:test",
    )
    after = snapshot(tmp_path)
    assert all(after[key] == value for key, value in before.items())
    assert len(after) == len(before) + 3
    for old, new, field in [
        (report, replacement, "report_id"),
        (issue, second_issue, "issue_id"),
        (review, approval, "review_id"),
    ]:
        assert old[field] != new[field]
        assert old[field] in fields(new["path"])["references"]
    for value in after.values():
        assert b"\r" not in value
        value.decode("utf-8", errors="strict")


@pytest.mark.parametrize(
    "operation",
    ["transition", "finish_task", "archive_task", "archive_to_history", "archive_review", "init"],
)
def test_deferred_and_legacy_mutators_blocked_including_class_calls(
    tmp_path: Path, operation: str
) -> None:
    project, request = workspace(tmp_path)
    task = project.create_task(**request)
    before = snapshot(tmp_path)
    for method in [
        getattr(project, operation),
        lambda **kw: getattr(Project, operation)(project, **kw),
    ]:
        with pytest.raises(V4ProtocolError):
            method(
                task_id=task["task_id"], from_stage="inbox", to_stage="active", tool="claim_task"
            )
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize(
    "damage", ["missing-fact", "duplicate-fact", "bad-fact", "task-byte-change"]
)
def test_partial_or_damaged_creation_preserved(tmp_path: Path, damage: str) -> None:
    project, request = workspace(tmp_path)
    result = project.create_task(**request)
    fact = next((tmp_path / "fcop/operations").glob("*.json"))
    if damage == "missing-fact":
        fact.rename(tmp_path / "saved-fact.json")
    elif damage == "duplicate-fact":
        (fact.parent / "duplicate.json").write_bytes(fact.read_bytes())
    elif damage == "bad-fact":
        fact.write_bytes(b"{bad")
    else:
        path = Path(result["path"])
        path.write_bytes(path.read_bytes() + b"changed\n")
    before = snapshot(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.create_task(**request)
    assert caught.value.code == "RECOVERY_REQUIRED"
    assert snapshot(tmp_path) == before


def test_no_overwrite_primitive_preserves_evidence(tmp_path: Path) -> None:
    path = tmp_path / "fact.json"
    publish(path, b"original\n")
    with pytest.raises(V4ProtocolError) as caught:
        publish(path, b"different\n")
    assert caught.value.code == "TARGET_ALREADY_EXISTS_DIFFERENT"
    assert path.read_bytes() == b"original\n"
    assert [p.read_bytes() for p in tmp_path.glob(".fcop-create-*.tmp")] == [b"different\n"]


def _lock_holder(path: str, ready: Any, release: Any) -> None:
    with operation_lock(Path(path)):
        ready.set()
        release.wait(timeout=10)


def test_kernel_lock_timeout_and_release(tmp_path: Path) -> None:
    ctx = multiprocessing.get_context("spawn")
    ready, release = ctx.Event(), ctx.Event()
    path = tmp_path / "key.lock"
    child = ctx.Process(target=_lock_holder, args=(str(path), ready, release))
    child.start()
    try:
        assert ready.wait(timeout=10)
        with pytest.raises(V4ProtocolError) as caught, operation_lock(path, timeout=0.1):
            pytest.fail("contending process acquired the held lock")
        assert caught.value.code == "LOCK_RECOVERY_REQUIRED"
    finally:
        release.set()
        child.join(timeout=10)
        if child.is_alive():
            child.terminate()
            child.join(timeout=5)
    assert child.exitcode == 0
    with operation_lock(path, timeout=0.1):
        assert path.stat().st_size == 0
    assert path.read_bytes() == b""


def test_symlink_escape_and_absolute_inspection_rejected(tmp_path: Path) -> None:
    source = tmp_path / "workspace"
    project, request = workspace(source)
    result = project.create_task(**request)
    with pytest.raises(V4ProtocolError):
        project.inspect_state(envelope_path=Path(result["path"]))
    outside = tmp_path / "outside"
    outside.mkdir()
    link = source / "fcop/linked"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("OS account cannot create symlinks")
    with pytest.raises(V4ProtocolError):
        project.inspect_state(envelope_path="fcop/linked/TASK-external.md")
    assert not list(outside.iterdir())


def test_binding_is_manifest_based_and_constructor_read_only(tmp_path: Path) -> None:
    # A lifecycle-shaped empty directory must not imply v4.
    (tmp_path / "fcop/_lifecycle/inbox").mkdir(parents=True)
    before = snapshot(tmp_path)
    project = Project(tmp_path)
    assert snapshot(tmp_path) == before

    with pytest.raises(V4ProtocolError) as caught:
        project.create_task(workspace_id="made-up")
    assert caught.value.code == "UNSUPPORTED_WORKSPACE_VERSION"
    assert "trusted_profiles" in inspect.signature(Project).parameters
    assert snapshot(tmp_path) == before


def test_legacy_layout_not_migrated_by_create_workspace(tmp_path: Path) -> None:
    legacy = tmp_path / "docs/agents"
    legacy.mkdir(parents=True)
    (legacy / "fcop.json").write_bytes(b'{"mode":"solo"}\n')
    before = snapshot(tmp_path)
    with pytest.warns(DeprecationWarning):
        project = Project(tmp_path)
    with pytest.raises(V4ProtocolError):
        project.create_workspace()
    assert snapshot(tmp_path) == before
    assert not (tmp_path / "fcop").exists()
