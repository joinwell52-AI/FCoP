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


@pytest.mark.parametrize("versions", [('"4.0","protocol_version":"3.2"'),
                                      ('"3.2","protocol_version":"4.0"')])
def test_closeout_duplicate_version_no_legacy_fallback(tmp_path: Path, versions: str) -> None:
    (tmp_path / "fcop").mkdir()
    (tmp_path / "fcop/fcop.json").write_bytes(
        ('{"protocol":"fcop","protocol_version":' + versions + '}\n').encode()
    )
    before = snapshot(tmp_path)
    for name in ("write_task", "create_task"):
        with pytest.raises(FcopError) as caught:
            getattr(Project(tmp_path), name)(
                sender="ME", recipient="ME", subject="blocked", body="x", priority="P2"
            )
        assert getattr(caught.value, "code", None) == "INVALID_ENVELOPE"
        assert snapshot(tmp_path) == before


def test_closeout_fact_path_is_relative(tmp_path: Path) -> None:
    project, request = workspace(tmp_path)
    result = project.create_task(**request)
    fact = json.loads(next((tmp_path / "fcop/operations").glob("*.json")).read_bytes())
    assert fact["path"] == Path(result["path"]).relative_to(tmp_path).as_posix()


def test_closeout_class_autospec_signature() -> None:
    from unittest.mock import create_autospec

    mocked = create_autospec(Project, instance=True)
    assert "sender" in inspect.signature(mocked.write_task).parameters
    with pytest.raises(TypeError):
        mocked.write_task(bogus_argument=True)


def tree_snapshot(root: Path) -> dict[str, bytes | None]:
    return {p.relative_to(root).as_posix(): p.read_bytes() if p.is_file() else None
            for p in root.rglob("*")}


@pytest.mark.parametrize("raw", [
    b'{"workspace_id":"a","workspace_id":"b"}',
    b'{"encoding":{},"encoding":{}}',
    b'{"unknown":1,"unknown":2}',
    b'{"encoding":{"version":"4.0","version":"3.2"}}',
    b'\xff', b'\xef\xbb\xbf{}', b'{bad', b'[]', b'{"x":NaN}',
])
def test_closeout_invalid_manifest_all_mutators(tmp_path: Path, raw: bytes) -> None:
    from fcop.v4.boundary import _METHOD_POLICIES

    (tmp_path / "fcop").mkdir()
    (tmp_path / "fcop/fcop.json").write_bytes(raw)
    before = tree_snapshot(tmp_path)
    project = Project(tmp_path)
    assert project.is_initialized()  # diagnosis is not a write authorization
    for name, policy in _METHOD_POLICIES.items():
        if policy in {"COMMON_SAFE", "V4_READ_UNAVAILABLE"} or name == "is_initialized":
            continue
        for class_call in (False, True):
            with pytest.raises(FcopError) as caught:
                if class_call:
                    getattr(Project, name)(project)
                else:
                    getattr(project, name)()
            assert getattr(caught.value, "code", None) == "INVALID_ENVELOPE"
            assert tree_snapshot(tmp_path) == before


def test_closeout_business_version_cannot_rebind(tmp_path: Path) -> None:
    project, request = workspace(tmp_path)
    before = tree_snapshot(tmp_path)
    for name in ("write_task", "create_task"):
        with pytest.raises(FcopError) as caught:
            getattr(project, name)(**request, protocol_version="3.2")
        assert getattr(caught.value, "code", None) == "INVALID_ENVELOPE"
        assert tree_snapshot(tmp_path) == before
    legacy = Project(tmp_path / "empty")
    with pytest.raises(FcopError) as caught:
        legacy.create_task(**request, protocol_version="4.0")
    assert getattr(caught.value, "code", None) == "UNSUPPORTED_WORKSPACE_VERSION"
    assert legacy._v4_creation is None
    assert not legacy.path.exists()


def assert_complete_or_absent(root: Path) -> bool:
    canonical_dir = root / "fcop"
    if not canonical_dir.exists():
        return False
    required = ["_lifecycle/inbox", "_lifecycle/active", "_lifecycle/review",
                "_lifecycle/done", "_lifecycle/archive", "reports", "issues",
                "reviews", "operations", "cold"]
    assert all((canonical_dir / relative).is_dir() for relative in required)
    value = json.loads((canonical_dir / "fcop.json").read_bytes())
    assert value["protocol_version"] == "4.0"
    assert value["workspace_id"].startswith("urn:uuid:")
    return True


@pytest.mark.parametrize("phase", [
    "before-staging", "before-manifest", "partial-directories", "before-publication",
    "publication-fails", "response-lost",
])
def test_closeout_initialization_faults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, phase: str
) -> None:
    from fcop.v4 import creation, encoding

    original_mkdir = Path.mkdir
    real_publish = creation.publish_directory

    def failed(*args: Any, **kwargs: Any) -> Any:
        assert not assert_complete_or_absent(tmp_path)
        raise OSError("injected initialization failure")

    if phase == "before-staging":
        monkeypatch.setattr(creation.tempfile, "mkdtemp", failed)
    elif phase == "before-manifest":
        monkeypatch.setattr(creation, "publish", failed)
    elif phase == "partial-directories":
        def partial(path: Path, *args: Any, **kwargs: Any) -> None:
            if path.name == "reports":
                staging = path.parent
                assert (staging / "fcop.json").is_file()
                assert (staging / "_lifecycle/inbox").is_dir()
                failed()
            original_mkdir(path, *args, **kwargs)
        monkeypatch.setattr(Path, "mkdir", partial)
    elif phase == "before-publication":
        def ready(staging: Path, target: Path) -> None:
            assert (staging / "cold").is_dir()
            assert (staging / "fcop.json").is_file()
            failed()
        monkeypatch.setattr(creation, "publish_directory", ready)
    elif phase == "publication-fails":
        # A real no-replace OS publication to an existing empty destination
        # must not replace it. Keep the canonical path absent in this scenario.
        occupied = tmp_path / "occupied"
        occupied.mkdir()
        def collision(staging: Path, target: Path) -> None:
            encoding.publish_directory(staging, occupied)
        monkeypatch.setattr(creation, "publish_directory", collision)
    else:
        def response_lost(staging: Path, target: Path) -> None:
            real_publish(staging, target)
            assert assert_complete_or_absent(tmp_path)
            raise OSError("response lost after complete commit")
        monkeypatch.setattr(creation, "publish_directory", response_lost)

    with pytest.raises(FcopError) as caught:
        Project(tmp_path).create_workspace()
    assert getattr(caught.value, "code", None) in {
        "RECOVERY_REQUIRED", "TARGET_ALREADY_EXISTS_DIFFERENT"
    }
    assert assert_complete_or_absent(tmp_path) == (phase == "response-lost")
    if phase not in {"before-staging", "response-lost"}:
        assert list(tmp_path.glob(".fcop-init-*"))
    before = tree_snapshot(tmp_path)
    if phase == "response-lost":
        assert Project(tmp_path).is_initialized()
        with pytest.raises(FcopError):
            Project(tmp_path).create_workspace()
        assert tree_snapshot(tmp_path) == before


def test_closeout_existing_canonical_and_staging_preserved(tmp_path: Path) -> None:
    root = tmp_path / "staged"
    staged = root / ".fcop-init-interrupted"
    staged.mkdir(parents=True)
    (staged / "fcop.json").write_bytes(b"evidence")
    before = tree_snapshot(root)
    with pytest.raises(FcopError) as caught:
        Project(root).create_workspace()
    assert getattr(caught.value, "code", None) == "RECOVERY_REQUIRED"
    assert tree_snapshot(root) == before
    assert not assert_complete_or_absent(root)
    other = tmp_path / "existing"
    project, request = workspace(other)
    project.create_task(**request)
    before = tree_snapshot(other)
    with pytest.raises(FcopError):
        Project(other).create_workspace(profiles=["different"])
    assert tree_snapshot(other) == before
    assert assert_complete_or_absent(other)


def _init_worker(root: str, barrier: Any, queue: Any) -> None:
    from unittest.mock import patch

    from fcop.v4 import creation

    original_temp = creation.tempfile.mkdtemp
    original_publish = creation.publish_directory
    def stage(*args: Any, **kwargs: Any) -> str:
        barrier.wait(timeout=15)  # both passed the pre-existing-evidence guard
        return original_temp(*args, **kwargs)
    def commit(staging: Path, target: Path) -> None:
        assert not assert_complete_or_absent(Path(root))
        barrier.wait(timeout=15)  # both complete staging before real OS race
        original_publish(staging, target)
    try:
        with patch.object(creation.tempfile, "mkdtemp", stage), \
                patch.object(creation, "publish_directory", commit):
            result = Project(root).create_workspace()
        queue.put(("ok", result, snapshot(Path(root) / "fcop")))
    except FcopError as exc:
        queue.put(("error", getattr(exc, "code", None), None))


def test_closeout_spawn_initialization_no_overwrite(tmp_path: Path) -> None:
    ctx = multiprocessing.get_context("spawn")
    barrier, queue = ctx.Barrier(2), ctx.Queue()
    children = [ctx.Process(target=_init_worker, args=(str(tmp_path), barrier, queue))
                for _ in range(2)]
    try:
        for child in children:
            child.start()
        results = [queue.get(timeout=30) for _ in children]
        for child in children:
            child.join(timeout=10)
            assert child.exitcode == 0
        successes = [r for r in results if r[0] == "ok"]
        failures = [r for r in results if r[0] == "error"]
        assert len(successes) == len(failures) == 1
        assert failures[0][1] == "TARGET_ALREADY_EXISTS_DIFFERENT"
        assert assert_complete_or_absent(tmp_path)
        assert snapshot(tmp_path / "fcop") == successes[0][2]
        assert json.loads((tmp_path / "fcop/fcop.json").read_bytes()) == successes[0][1]
        assert len(list(tmp_path.glob(".fcop-init-*"))) == 1  # losing evidence retained
    finally:
        for child in children:
            if child.is_alive():
                child.terminate()
                child.join(timeout=5)
        queue.close()


def test_closeout_move_workspace_retry(tmp_path: Path) -> None:
    source, destination = tmp_path / "original", tmp_path / "moved"
    project, request = workspace(source)
    first = project.create_task(**request)
    same = project.create_task(**request)
    for key in ("task_id", "path", "digest"):
        assert same[key] == first[key]
    fact_path = next((source / "fcop/operations").glob("*.json"))
    raw = fact_path.read_bytes()
    fact = json.loads(raw)
    assert str(source).encode() not in raw and source.as_posix().encode() not in raw
    assert "\\" not in fact["path"] and ":" not in fact["path"]
    before = tree_snapshot(source)
    source.rename(destination)  # isolated temporary fixture, not a real workspace
    retried = Project(destination).create_task(**request)
    assert retried["existing"] is True
    assert retried["task_id"] == first["task_id"] and retried["digest"] == first["digest"]
    assert retried["path"] == str(destination / fact["path"])
    assert Path(retried["path"]).is_file()
    assert len(list((destination / "fcop/_lifecycle").glob("*/TASK-*.md"))) == 1
    assert tree_snapshot(destination) == before


@pytest.mark.parametrize("bad", ["../outside", "/absolute/TASK-x.md", "D:/elsewhere/TASK-x.md",
                                "other/fcop/TASK-x.md", "fcop//TASK-x.md", "fcop/./TASK-x.md",
                                "fcop\\_lifecycle\\inbox\\TASK-x.md", None])
def test_closeout_fact_path_tampering(tmp_path: Path, bad: Any) -> None:
    project, request = workspace(tmp_path)
    project.create_task(**request)
    fact_path = next((tmp_path / "fcop/operations").glob("*.json"))
    fact = json.loads(fact_path.read_bytes())
    fact["path"] = bad
    fact_path.write_bytes((json.dumps(fact) + "\n").encode())
    before = tree_snapshot(tmp_path)
    with pytest.raises(FcopError) as caught:
        Project(tmp_path).create_task(**request)
    assert getattr(caught.value, "code", None) == "RECOVERY_REQUIRED"
    assert tree_snapshot(tmp_path) == before


def test_closeout_boundary_reflection_binding_and_subclass(tmp_path: Path) -> None:
    from unittest.mock import create_autospec, patch

    from fcop.v4.boundary import _METHOD_POLICIES, version_boundary

    legacy = Project(tmp_path / "legacy")
    legacy.init_solo(role_code="ME")
    original_names = set(_METHOD_POLICIES) - {
        "create_workspace", "create_task", "derive_workspace", "inspect_state",
        "transition", "finish_task", "family_digest",
    }
    assert len(original_names) == 38
    assert isinstance(vars(Project)["validate_team"], staticmethod)
    assert Project.validate_team(roles=["ME"], leader="ME") == []
    assert legacy.validate_team(roles=["ME"], leader="ME") == []
    discovered = dict(inspect.getmembers(Project, inspect.isfunction))
    for name in original_names - {"validate_team"}:
        method = discovered[name]
        original = inspect.unwrap(method)
        assert method.__name__ == original.__name__
        assert method.__doc__ == original.__doc__
        assert inspect.signature(method) == inspect.signature(original)
        bound = getattr(legacy, name)
        assert bound.__self__ is legacy and bound.__func__ is method
    assert Project.is_initialized(legacy) is True
    request = dict(sender="ADMIN", recipient="ME", subject="real legacy", body="body", priority="P2")
    task = Project.write_task(legacy, **request)
    assert legacy.read_task(task.task_id).task_id == task.task_id
    for target in (Project, legacy):
        mocked = create_autospec(target)
        with pytest.raises(TypeError):
            mocked.write_task(unexpected=True)
    with patch.object(Project, "write_task", autospec=True) as mocked_method:
        legacy.write_task(**request)
        mocked_method.assert_called_once_with(legacy, **request)
        with pytest.raises(TypeError):
            legacy.write_task(unknown=True)

    class Inherited(Project):
        pass
    class Overridden(Project):
        def write_task(self, **kwargs: Any) -> Any:
            return super().write_task(**kwargs)
    for cls in (Inherited, Overridden):
        instance = cls(tmp_path / cls.__name__)
        manifest = instance.create_workspace()
        result = instance.write_task(
            workspace_id=manifest["workspace_id"], operation_id="subclass",
            sender="ME", recipient="ME", subject="subclass", body="x",
        )
        assert Path(result["path"]).is_file()
        legacy_child = cls(legacy.path)
        assert legacy_child.write_task(**request).task_id
    # Class construction rejects an unclassified future public method.
    class Unknown:
        def future_write(self) -> None:
            pass
    with pytest.raises(TypeError, match="classification"):
        version_boundary(Unknown)


def test_closeout_all_unsupported_mutators_rejected(tmp_path: Path) -> None:
    from fcop.v4.boundary import _METHOD_POLICIES

    project, request = workspace(tmp_path)
    project.create_task(**request)
    before = tree_snapshot(tmp_path)
    names = [n for n, p in _METHOD_POLICIES.items()
             if p in {"LEGACY_ONLY", "V4_MUTATION_REJECTED"}]
    for name in names:
        for class_call in (False, True):
            with pytest.raises(FcopError) as caught:
                if class_call:
                    getattr(Project, name)(project)
                else:
                    getattr(project, name)()
            assert getattr(caught.value, "code", None)
            assert tree_snapshot(tmp_path) == before


@pytest.mark.parametrize("version", [None, "1.0", "2.0", "3.2.5"])
def test_closeout_legacy_crlf_keeps_legacy_behavior(tmp_path: Path, version: str | None) -> None:
    project = Project(tmp_path)
    project.init_solo(role_code="ME")
    declaration = json.loads(project.config_path.read_bytes())
    if version is not None:
        declaration["protocol_version"] = version
    raw = (json.dumps(declaration, indent=2) + "\n").replace("\n", "\r\n").encode()
    project.config_path.write_bytes(raw)
    reopened = Project(tmp_path)
    assert reopened._v4_creation is None
    result = reopened.write_review(
        reviewer_role="ME", subject_type="code_change", subject_ref="commit:abc",
        decision="approved",
    )
    assert result.decision.value == "approved"
    assert project.config_path.read_bytes() == raw


def test_closeout_v4_crlf_no_writer_bypass(tmp_path: Path) -> None:
    project, request = workspace(tmp_path)
    manifest = json.loads(project.config_path.read_bytes())
    project.config_path.write_bytes((json.dumps(manifest, indent=2) + "\n")
                                   .replace("\n", "\r\n").encode())
    before = tree_snapshot(tmp_path)
    for name in ("write_task", "create_task"):
        for bound in (project, None):
            with pytest.raises(FcopError) as caught:
                getattr(bound if bound is not None else Project(tmp_path), name)(**request)
            assert getattr(caught.value, "code", None) == "INVALID_ENVELOPE"
            assert tree_snapshot(tmp_path) == before


def test_closeout_actual_version_bound_signatures(tmp_path: Path) -> None:
    from unittest.mock import create_autospec

    from fcop.v4.boundary import _METHOD_POLICIES

    legacy = Project(tmp_path / "legacy")
    legacy.init_solo(role_code="ME")
    project, _ = workspace(tmp_path / "v4")
    for current in (project, Project(project.path)):
        for name, policy in _METHOD_POLICIES.items():
            if policy != "V4_HANDLER":
                continue
            handler = current._v4_creation.handler(name)
            assert inspect.signature(getattr(current, name)) == inspect.signature(handler)
            assert inspect.signature(getattr(Project, name)) == inspect.signature(
                inspect.unwrap(getattr(Project, name))
            )
        for name in ("write_task", "write_report", "write_issue", "write_review"):
            assert inspect.signature(getattr(current, name)) != inspect.signature(
                getattr(legacy, name)
            )
        mocked_report = create_autospec(current.write_report)
        assert "kwargs" in inspect.signature(mocked_report).parameters


@pytest.mark.parametrize("version", ["3.garbage", "", None, 4, "5.0", "4.1"])
def test_closeout_unknown_version_never_legacy(tmp_path: Path, version: Any) -> None:
    (tmp_path / "fcop").mkdir()
    (tmp_path / "fcop/fcop.json").write_bytes(
        (json.dumps({"protocol": "fcop", "protocol_version": version}) + "\n").encode()
    )
    before = tree_snapshot(tmp_path)
    for name in ("write_task", "create_task"):
        with pytest.raises(FcopError) as caught:
            getattr(Project(tmp_path), name)(
                sender="ME", recipient="ME", subject="blocked", body="x", priority="P2"
            )
        assert getattr(caught.value, "code", None) == "UNSUPPORTED_WORKSPACE_VERSION"
        assert tree_snapshot(tmp_path) == before


def test_closeout_crlf_duplicate_does_not_enable_legacy(tmp_path: Path) -> None:
    (tmp_path / "fcop").mkdir()
    (tmp_path / "fcop/fcop.json").write_bytes(
        b'{\r\n"protocol_version":"4.0",\r\n"protocol_version":"3.2"\r\n}\r\n'
    )
    before = tree_snapshot(tmp_path)
    for name in ("write_task", "create_task"):
        with pytest.raises(FcopError) as caught:
            getattr(Project(tmp_path), name)(
                sender="ME", recipient="ME", subject="blocked", body="x", priority="P2"
            )
        assert getattr(caught.value, "code", None) == "INVALID_ENVELOPE"
        assert tree_snapshot(tmp_path) == before
