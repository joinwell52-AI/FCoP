"""WP4B.3: validated fact publication is distinct from authorization consumption."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest

from fcop import Project
from fcop.errors import V4ProtocolError


def files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def fixture(root: Path, edge: str = "T6") -> tuple[Any, dict[str, Any], dict[str, Any]]:
    example = import_module("examples.v4.application")
    app = example.Application(root)
    task = app.task("Validated append")
    report = app.complete(task) if edge in {"T6", "T7"} else None
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    if edge in {"T4", "T5"}:
        report = app.project.write_report(
            workspace_id=app.workspace_id, sender="ME", recipient="ME", body="done",
            subject_ref=task, attempt_id=attempt, report_kind="final", result="done",
        )["report_id"]
        app.move(task, "active", "review", "submit_task", report_ref=report)
    source, target, tool, kind, decision = {
        "T4": ("review", "done", "approve_task", "acceptance", "approved"),
        "T5": ("review", "active", "reject_task", "rejection", "rejected"),
        "T6": ("done", "active", "reopen_task", "reopen", "approved"),
        "T7": ("done", "archive", "archive_task", "assessment", "approved"),
    }[edge]
    old = app.review(task, kind, decision, attempt_id=attempt,
                     references=[report] if edge in {"T4", "T5"} else [])
    request = dict(review_id=old, approver="ME", decision="approved", profile_ref=example.PROFILE,
                   from_stage=source, to_stage=target, attempt_id=attempt, family_digest=None,
                   issued_at=datetime.now(timezone.utc).isoformat(), expires_at=None,
                   issuer_proof="demo-only", comment="Human confirmation")
    move = dict(task_id=task, from_stage=source, to_stage=target, tool=tool, actor="ME",
                profile_ref=example.PROFILE)
    if edge != "T7":
        move["review_ref"] = old
    return app, request, move


@pytest.mark.parametrize("edge", ["T4", "T5", "T6", "T7"])
def test_append_once_then_real_consumption(tmp_path: Path, edge: str) -> None:
    app, request, move = fixture(tmp_path, edge)
    calls: list[Any] = []
    def evaluator(**fields: Any) -> str:
        calls.append(fields)
        return "AUTHORIZED"
    project: Any = Project(tmp_path, trusted_profiles={request["profile_ref"]: evaluator})
    before = files(tmp_path)
    result = project.mark_human_approved(**request)
    after = files(tmp_path)
    assert len(calls) == 1
    assert calls[0] == dict(profile_ref=request["profile_ref"], issuer="ME", proof="demo-only")
    assert all(after[k] == v for k, v in before.items())
    assert len(after) == len(before) + 1
    stored = project.inspect_state(envelope_path=Path(result["path"]).relative_to(tmp_path).as_posix())
    assert stored["review_kind"] == "authorization"
    assert stored["decision"] == "authorize"
    assert stored["references"] == [request["review_id"]]
    assert stored["subject_ref"] == move["task_id"]
    assert stored["transition"] == {"from": move["from_stage"], "to": move["to_stage"]}
    for key in ("attempt_id", "family_digest", "issued_at", "expires_at", "profile_ref", "issuer_proof"):
        assert stored.get(key) == request[key]
    assert stored["authorization_scope"] == "single_use"
    assert stored["operation_kind"] == "lifecycle_transition"
    assert project.inspect_state(task_id=move["task_id"])["stage"] == move["from_stage"]
    move["authorization_ref"] = result["review_id"]
    project.transition(**move)
    assert len(calls) == 2
    assert project.inspect_state(task_id=move["task_id"])["stage"] == move["to_stage"]
    committed = files(tmp_path)
    assert project.transition(**move)["existing"] is True
    assert files(tmp_path) == committed


@pytest.mark.parametrize("verdict", ["EMPTY", "UNREGISTERED", "UNADOPTED", "DENIED", "UNKNOWN", "other", "RAISE"])
def test_append_trusted_denials(tmp_path: Path, verdict: str) -> None:
    _, request, _ = fixture(tmp_path)
    calls: list[Any] = []
    def evaluator(**fields: Any) -> str:
        calls.append(fields)
        if verdict == "RAISE":
            raise RuntimeError("not an authority decision")
        return verdict
    registry = {} if verdict in {"EMPTY", "UNREGISTERED"} else {request["profile_ref"]: evaluator}
    if verdict == "UNADOPTED":
        request["profile_ref"] = "profile:not-adopted"
    project: Any = Project(tmp_path, trusted_profiles=registry)
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.mark_human_approved(**request)
    assert caught.value.code == (
        "AUTHORIZATION_PROFILE_UNAVAILABLE" if not registry else "AUTHORIZATION_INVALID"
    )
    assert len(calls) == (0 if verdict in {"EMPTY", "UNREGISTERED", "UNADOPTED"} else 1)
    assert files(tmp_path) == before


@pytest.mark.parametrize("change", [
    {"decision": "reject"}, {"decision": "denied"}, {"decision": "other"},
    {"from_stage": "active"}, {"to_stage": "inbox"}, {"attempt_id": None},
    {"attempt_id": "urn:uuid:aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
    {"family_digest": "0" * 64}, {"issued_at": "not-a-date"},
    {"expires_at": "2000-01-01T00:00:00+00:00"}, {"issuer_proof": None},
    {"review_id": "REVIEW-does-not-exist"}, {"operation_kind": "create"},
    {"authorization_scope": "multiple"}, {"subject_ref": "TASK-fake"},
    {"workspace_id": "fake"}, {"references": []}, {"stored_decision": "authorize"},
    {"profile_evaluator": "AUTHORIZED"}, {"issuer_proof": {"registry": {"result": "AUTHORIZED"}}},
    {"issuer_proof": {"policy": "AUTHORIZED"}},
])
def test_invalid_append_is_zero_write(tmp_path: Path, change: dict[str, Any]) -> None:
    _, request, _ = fixture(tmp_path)
    calls: list[Any] = []
    def evaluator(**fields: Any) -> str:
        calls.append(fields)
        return "AUTHORIZED"
    project: Any = Project(tmp_path, trusted_profiles={request["profile_ref"]: evaluator})
    request.update(change)
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError):
        project.mark_human_approved(**request)
    assert calls == []
    assert files(tmp_path) == before


@pytest.mark.parametrize("verdict", ["DENIED", "UNKNOWN"])
def test_consumption_rechecks_profile(tmp_path: Path, verdict: str) -> None:
    _, request, move = fixture(tmp_path)
    decisions = iter(["AUTHORIZED", verdict])
    project: Any = Project(tmp_path, trusted_profiles={request["profile_ref"]: lambda **_: next(decisions)})
    authorization = project.mark_human_approved(**request)
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.transition(**move, authorization_ref=authorization["review_id"])
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert files(tmp_path) == before


@pytest.mark.parametrize("missing", ["expires_at", "issuer_proof", "issued_at", "attempt_id"])
def test_missing_binding_is_structured(tmp_path: Path, missing: str) -> None:
    app, request, _ = fixture(tmp_path)
    del request[missing]
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        app.project.mark_human_approved(**request)
    assert caught.value.code == "AUTHORIZATION_INVALID"
    assert files(tmp_path) == before


def test_expiry_is_rechecked_after_evaluator(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _, request, _ = fixture(tmp_path)
    clock = import_module("fcop.v4.authorization")
    now = datetime.now(timezone.utc)
    request.update(issued_at=now.isoformat(), expires_at=(now + timedelta(seconds=1)).isoformat())
    monkeypatch.setattr(clock, "_utc_now", lambda: now)
    def evaluator(**_: Any) -> str:
        monkeypatch.setattr(clock, "_utc_now", lambda: now + timedelta(seconds=2))
        return "AUTHORIZED"
    project: Any = Project(tmp_path, trusted_profiles={request["profile_ref"]: evaluator})
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        project.mark_human_approved(**request)
    assert caught.value.code == "AUTHORIZATION_EXPIRED"
    assert files(tmp_path) == before


@pytest.mark.parametrize("family_value", ["VALID", "MISSING", "STALE"])
def test_root_family_authorization(tmp_path: Path, family_value: str) -> None:
    example = import_module("examples.v4.application")
    app = example.Application(tmp_path)
    root = app.task("Root")
    branch = app.task("Branch", branch_of=root)
    report = app.complete(branch)
    app.complete(root)
    family = app.project.family_digest(root_task_id=root)
    old = app.review(root, "convergence", "approved", family_digest=family, references=[report])
    request = dict(review_id=old, approver="ME", decision="authorize", profile_ref=example.PROFILE,
                   from_stage="done", to_stage="archive", attempt_id=None,
                   family_digest=family if family_value == "VALID" else (None if family_value == "MISSING" else "0" * 64),
                   issued_at=datetime.now(timezone.utc).isoformat(), expires_at=None, issuer_proof="demo-only")
    before = files(tmp_path)
    if family_value != "VALID":
        with pytest.raises(V4ProtocolError) as caught:
            app.project.mark_human_approved(**request)
        assert caught.value.code == "FAMILY_CONVERGENCE_MISMATCH"
        assert files(tmp_path) == before
    else:
        authorization = app.project.mark_human_approved(**request)
        assert app.project.inspect_state(task_id=root)["stage"] == "done"
        app.move(root, "done", "archive", "archive_task", review_ref=old,
                 authorization_ref=authorization["review_id"], profile_ref=example.PROFILE, family_digest=family)
        assert app.project.inspect_state(task_id=root)["stage"] == "archive"


@pytest.mark.parametrize("mutation", ["proof", "expired", "other_edge", "other_task"])
def test_consume_does_not_trust_append(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str) -> None:
    app, request, move = fixture(tmp_path)
    clock = import_module("fcop.v4.authorization")
    now = datetime.now(timezone.utc)
    request.update(issued_at=now.isoformat(), expires_at=(now + timedelta(seconds=5)).isoformat())
    monkeypatch.setattr(clock, "_utc_now", lambda: now)
    auth = app.project.mark_human_approved(**request)
    if mutation == "proof":
        path = Path(auth["path"])
        # Deliberate fixture corruption: no production writer rewrites an old fact.
        path.write_bytes(path.read_bytes().replace(b"demo-only", b"fake-proof"))
    elif mutation == "expired":
        monkeypatch.setattr(clock, "_utc_now", lambda: now + timedelta(seconds=10))
    elif mutation == "other_edge":
        move.update(to_stage="archive", tool="archive_task")
        move.pop("review_ref")
    else:
        another = app.task("Another")
        app.complete(another)
        move["task_id"] = another
    before = files(tmp_path)
    with pytest.raises(V4ProtocolError) as caught:
        app.project.transition(**move, authorization_ref=auth["review_id"])
    assert caught.value.code == ("AUTHORIZATION_EXPIRED" if mutation == "expired" else "AUTHORIZATION_INVALID")
    assert files(tmp_path) == before
