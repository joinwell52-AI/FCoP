"""WP4A/WP4A.1 machine-contract and actual application evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from examples.v4.application import PROFILE, Application, open_project, run
from jsonschema import Draft202012Validator

from fcop import Project
from fcop.errors import V4ProtocolError
from fcop.v4.encoding import _parse_envelope_bytes, parse_envelope, parse_json
from fcop.v4.schema import _validate, _validators

REPO = Path(__file__).resolve().parents[2]


def rewrite(path, **updates):
    fields = parse_envelope(path)
    fields.update(updates)
    path.write_bytes(("---\n" + yaml.safe_dump(fields) + "---\n\nEvidence\n").encode())


@pytest.fixture
def artifacts(tmp_path):
    app = Application(tmp_path)
    task = app.task("schema artifacts")
    app.complete(task)
    app.project.write_issue(workspace_id=app.workspace_id, sender="ME", recipient="ME",
                            subject_ref=task, severity="low", body="Issue")
    app.archive(task)
    result = {"workspace": parse_json((tmp_path / "fcop/fcop.json").read_bytes())}
    for kind, folder in {"task": "_lifecycle/archive", "report": "reports",
                         "issue": "issues", "review": "reviews"}.items():
        result[kind] = parse_envelope(next((tmp_path / "fcop" / folder).glob("*.md")))
    result["transition"] = result["task"]["transitions"][-1]
    result["authorization-binding"] = {"from": "done", "to": "archive"}
    for path in (tmp_path / "fcop/operations").glob("*.json"):
        value = parse_json(path.read_bytes())
        name = "create-operation" if value["contract"] == "fcop-create-task-v1" else "lifecycle-receipt"
        _validate(name, value)
        result[name] = value
    result["recovery-observation"] = {
        "operation_id": "observe", "source": "fcop/_lifecycle/done/TASK-A.md",
        "target": "fcop/_lifecycle/archive/TASK-A.md", "stage": "COMMITTED",
        "content_digest": hashlib.sha256(b"observed").hexdigest(),
    }
    result["family-canonical"] = {"contract": "fcop-family-v1", "root_task_id": task,
                                   "branches": []}
    result["create-request-canonical"] = {
        "contract": "fcop-create-task-v1", "workspace_id": app.workspace_id,
        "operation_kind": "create_task", "operation_id": "normalized", "sender": "ME",
        "recipient": "ME", "subject": "normalized", "body": "body\n", "priority": "P2",
        "parent": None, "branch_of": None, "references": [],
    }
    return result


ROOTS = ["workspace", "task", "report", "issue", "review"]


@pytest.mark.parametrize("name", ROOTS)
def test_sb01_root_extensions(artifacts, name):
    value = artifacts[name]
    value["unknown_profile_field"] = {"local": ["opaque", 7]}
    _validate(name, value)


@pytest.mark.parametrize("name", ROOTS)
def test_sb02_required_not_substituted(artifacts, name):
    value = artifacts[name]
    value["Protocol"] = value.pop("protocol")
    with pytest.raises(V4ProtocolError):
        _validate(name, value)


@pytest.mark.parametrize("name", ROOTS)
def test_sb03_core_type_not_overridden(artifacts, name):
    value = artifacts[name]
    value.update(workspace_id=42, alternate_workspace_id="pretend")
    with pytest.raises(V4ProtocolError):
        _validate(name, value)


@pytest.mark.parametrize("name", ["workspace", "transition", "authorization-binding",
                                  "lifecycle-receipt", "family-canonical"])
def test_sb04_closed_core(artifacts, name):
    value = artifacts[name]
    nested = value["encoding"] if name == "workspace" else value
    nested["unknown_profile_field"] = "not allowed here"
    with pytest.raises(V4ProtocolError):
        _validate(name, value)


@pytest.mark.parametrize("data,parser", [
    (b'{"protocol":"fcop","protocol":"fcop"}\n', parse_json),
    (b'---\nprotocol: fcop\nprotocol: fcop\n---\nbody\n', _parse_envelope_bytes),
])
def test_sb05_duplicates_before_schema(data, parser, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Schema must not run before duplicate-key rejection")
    monkeypatch.setattr("fcop.v4.schema._validate", forbidden)
    with pytest.raises(V4ProtocolError):
        parser(data)


@pytest.mark.parametrize("mode", ["sequential", "family"])
def test_minimal_public_application(tmp_path, mode, monkeypatch):
    monkeypatch.setenv("PYTHONPATH", str(REPO / "src"))
    assert run(tmp_path, mode)["state"] == "archive"


@pytest.mark.parametrize("decision", ["AUTHORIZED", "DENIED", "UNKNOWN"])
def test_sb06_profile_decision_not_overridden(tmp_path, decision):
    app = Application(tmp_path)
    task = app.task("gate")
    app.complete(task)
    auth = app.authorization(task, "done", "archive")
    review_path = tmp_path / "fcop/reviews" / (auth + ".md")
    rewrite(review_path, caller_authorized=True, profile_result="AUTHORIZED",
            approval={"bypass": True})
    project = Project(tmp_path, trusted_profiles={PROFILE: lambda **kwargs: decision})
    request = dict(task_id=task, from_stage="done", to_stage="archive", tool="archive_task",
                   actor="ADMIN", authorization_ref=auth, profile_ref=PROFILE)
    if decision == "AUTHORIZED":
        project.transition(**request)
        assert Path(project.read_task(task_id=task)["path"]).parent.name == "archive"
    else:
        before = project.read_task(task_id=task)
        with pytest.raises(V4ProtocolError) as error:
            project.transition(**request)
        assert error.value.code == "AUTHORIZATION_INVALID"
        assert project.read_task(task_id=task) == before


@pytest.mark.parametrize("source,target,tool", [("inbox", "active", "claim_task"),
    ("active", "review", "submit_task"), ("review", "done", "approve_task"),
    ("review", "active", "reject_task"), ("done", "active", "reopen_task"),
    ("done", "archive", "archive_task")])
def test_sb06_unknown_fields_cannot_grant_evidence_gate(tmp_path, source, target, tool):
    app = Application(tmp_path)
    created = app.project.create_task(workspace_id=app.workspace_id, operation_id="sb06-t1",
        sender="ME", recipient="ME", subject="gate", body="work")
    task = created["task_id"]
    if source != "inbox":
        app.move(task, "inbox", "active", "claim_task")
    if source in {"review", "done"}:
        report = app.project.write_report(workspace_id=app.workspace_id, sender="ME",
            recipient="ME", subject_ref=task, body="done", report_kind="final", result="done",
            attempt_id=app.project.inspect_state(task_id=task)["current_attempt_id"])["report_id"]
        app.move(task, "active", "review", "submit_task", report_ref=report)
        if source == "done":
            auth = app.authorization(task, "review", "done", kind="acceptance", refs=[report])
            app.move(task, "review", "done", "approve_task", review_ref=auth, authorization_ref=auth)
    path = Path(app.project.read_task(task_id=task)["path"])
    rewrite(path, pretend_report="approved", pretend_authorization=True,
            pretend_transition={"from": source, "to": target})
    before = path.read_bytes()
    if source == "inbox":
        app.move(task, source, target, tool)
        fields = app.project.read_task(task_id=task)
        assert fields["pretend_authorization"] is True  # semantic preservation only
        assert len(fields["transitions"]) == 2
    else:
        with pytest.raises(V4ProtocolError) as error:
            app.move(task, source, target, tool)
        assert error.value.code in {"REPORT_REQUIRED", "AUTHORIZATION_REQUIRED"}
        assert path.read_bytes() == before
        assert Path(app.project.read_task(task_id=task)["path"]).parent.name == source


def test_sb06_unknown_fields_do_not_fill_family_coverage(tmp_path):
    app = Application(tmp_path)
    root = app.task("root")
    branches = [app.task(str(i), branch_of=root) for i in range(2)]
    reports = [app.complete(branch) for branch in branches]
    app.complete(root)
    path = Path(app.project.read_task(task_id=root)["path"])
    rewrite(path, pretend_family_coverage=reports, pretend_convergence="approved")
    family = app.project.family_digest(root_task_id=root)
    with pytest.raises(V4ProtocolError) as error:
        app.review(root, "convergence", "approved", family_digest=family, references=reports[:1])
    assert error.value.code == "FAMILY_CONVERGENCE_MISMATCH"


def test_sb07_request_digest_ignores_reachable_profile_context(tmp_path):
    app = Application(tmp_path)
    request = dict(workspace_id=app.workspace_id, operation_id="stable", sender="ME",
                   recipient="ME", subject="fixed", body="fixed")
    first = app.project.create_task(**request, thread_key="one", risk_level="low")
    manifest_path = tmp_path / "fcop/fcop.json"
    manifest = parse_json(manifest_path.read_bytes())
    manifest["opaque_profile_context"] = "different"
    manifest_path.write_bytes((json.dumps(manifest) + "\n").encode())
    second = open_project(tmp_path).create_task(**request, thread_key="two", risk_level="high")
    assert second["existing"] is True
    assert first["task_id"] == second["task_id"] and first["digest"] == second["digest"]


def test_sb08_evidence_digest_includes_extension_bytes(tmp_path):
    app = Application(tmp_path)
    task = app.task("evidence")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    result = app.project.write_report(workspace_id=app.workspace_id, sender="ME", recipient="ME",
        subject_ref=task, body="done", attempt_id=attempt, report_kind="final", result="done")
    report = result["report_id"]
    app.move(task, "active", "review", "submit_task", report_ref=report)
    auth = app.authorization(task, "review", "done", kind="acceptance", refs=[report])
    path = Path(result["path"])
    old = hashlib.sha256(path.read_bytes()).hexdigest()
    # Corruption/adversarial simulation, never a supported append-only edit API.
    rewrite(path, opaque_profile_field="changed after binding")
    _validate("report", parse_envelope(path))
    assert hashlib.sha256(path.read_bytes()).hexdigest() != old
    before = app.project.read_task(task_id=task)
    with pytest.raises(V4ProtocolError) as error:
        app.move(task, "review", "done", "approve_task", review_ref=auth, authorization_ref=auth)
    assert error.value.code == "EVIDENCE_DIGEST_MISMATCH"
    assert app.project.read_task(task_id=task) == before


def test_sb09_local_profile_tightens_not_weakens(artifacts):
    def layered(value):
        _validate("workspace", value)
        return Draft202012Validator({"properties": {"team_label": {"const": "demo"}},
                                     "required": ["team_label"]}).is_valid(value)
    value = artifacts["workspace"]
    value["team_label"] = "invalid"
    assert not layered(value)
    value["team_label"] = "demo"
    assert layered(value)
    del value["protocol"]
    with pytest.raises(V4ProtocolError):
        layered(value)


def test_sb10_legacy_schemas_unchanged():
    # Git-blob SHA-256 captured and verified at the fixed taskbook commit.
    # This oracle is independent of clone depth and never fetches in a test.
    expected = {
        "spec/schemas/agent.schema.json": "82d2c5ffeb6b6c9a8bec4cfa7e9090f74facff17d0eb8b017e28a905846ff4b0",
        "spec/schemas/boundary.schema.json": "87e415a19d0c25b385d8c06136aa9de4968d310b9f75cfc0bc7b4b2e8e829c1a",
        "spec/schemas/encoding.schema.json": "a37f7be31e37c8c40f9afa02dc49c60b876e1bb270ba1fd7a1e64e55504c8024",
        "spec/schemas/event.schema.json": "e0e4561ac172a4e0438e81dd4d0957588c18fa76ae81fc5a2432a5acdd884f57",
        "spec/schemas/failure.schema.json": "0913a0784fc1bd24478717fbbaf264633006832a5e1a8b314bff50454cb61271",
        "spec/schemas/ipc-envelope.schema.json": "e42270d653da5243c18ce550be932cc9657e2f687271c205532ac413ee948829",
        "spec/schemas/review.schema.json": "f682dfc2e982b79f2459908c2844e7138bc1d86aeb82f8ebd3735b23f0bf0134",
        "spec/schemas/skill.schema.json": "157655560e755aef44f540d1e87b0d3abf95d9ae878dc6a34e90e9a7adce4992",
        "src/fcop/_data/schemas/agent.schema.json": "82d2c5ffeb6b6c9a8bec4cfa7e9090f74facff17d0eb8b017e28a905846ff4b0",
        "src/fcop/_data/schemas/boundary.schema.json": "87e415a19d0c25b385d8c06136aa9de4968d310b9f75cfc0bc7b4b2e8e829c1a",
        "src/fcop/_data/schemas/encoding.schema.json": "a37f7be31e37c8c40f9afa02dc49c60b876e1bb270ba1fd7a1e64e55504c8024",
        "src/fcop/_data/schemas/event.schema.json": "e0e4561ac172a4e0438e81dd4d0957588c18fa76ae81fc5a2432a5acdd884f57",
        "src/fcop/_data/schemas/failure.schema.json": "0913a0784fc1bd24478717fbbaf264633006832a5e1a8b314bff50454cb61271",
        "src/fcop/_data/schemas/ipc-envelope.schema.json": "e42270d653da5243c18ce550be932cc9657e2f687271c205532ac413ee948829",
        "src/fcop/_data/schemas/review.schema.json": "f682dfc2e982b79f2459908c2844e7138bc1d86aeb82f8ebd3735b23f0bf0134",
        "src/fcop/_data/schemas/skill.schema.json": "157655560e755aef44f540d1e87b0d3abf95d9ae878dc6a34e90e9a7adce4992",
    }
    for folder in ("spec/schemas", "src/fcop/_data/schemas"):
        paths = sorted((REPO / folder).glob("*.schema.json"))
        assert len(paths) == 8
        for path in paths:
            # Git's Windows checkout filter can use CRLF for historical files.
            normalized = path.read_bytes().replace(b"\r\n", b"\n")
            assert hashlib.sha256(normalized).hexdigest() == expected[path.relative_to(REPO).as_posix()]


def test_schema_parity_ids_offline_and_required_negative_matrix(artifacts, monkeypatch):
    import socket
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network"))
    subprocess.run([sys.executable, str(REPO / "spec/schemas/v4/generate.py"), "--check"], check=True)
    validators = _validators()
    assert len(validators) == 12
    ids = [validator.schema["$id"] for validator in validators.values()]
    assert len(set(ids)) == 12
    for name, value in artifacts.items():
        _validate(name, value)
        schema = validators[name].schema
        if "oneOf" in schema:
            schema = next(item for item in schema["oneOf"]
                          if value["from_stage"] in item["properties"]["from_stage"]["enum"])
        for key in schema["required"]:
            broken = copy.deepcopy(value)
            del broken[key]
            with pytest.raises(V4ProtocolError):
                _validate(name, broken)
            broken = copy.deepcopy(value)
            broken[key] = 7.5
            with pytest.raises(V4ProtocolError):
                _validate(name, broken)
        for key, prop in schema["properties"].items():
            if "const" in prop or "enum" in prop:
                broken = copy.deepcopy(value)
                broken[key] = "invalid-enum"
                with pytest.raises(V4ProtocolError):
                    _validate(name, broken)


@pytest.mark.parametrize("prefix,suffix", [(b"\xef\xbb\xbf", b""), (b"", b"\xff"), (b"", b"\r\n")])
@pytest.mark.parametrize("data,parser", [(b'{}\n', parse_json),
    (b'---\nprotocol: fcop\n---\nbody\n', _parse_envelope_bytes)])
def test_strict_byte_boundary(prefix, suffix, data, parser):
    with pytest.raises(V4ProtocolError):
        parser(prefix + data + suffix)


def test_real_write_and_read_use_same_validator(tmp_path, monkeypatch):
    app = Application(tmp_path)
    task = app.task("shared validator")
    import fcop.v4.schema as schema
    calls = []
    real = schema._validate
    def spy(name, value, **kwargs):
        calls.append((name, value.get("type")))
        return real(name, value, **kwargs)
    monkeypatch.setattr(schema, "_validate", spy)
    app.project.read_task(task_id=task)
    assert ("task", "TASK") in calls
    calls.clear()
    app.project.write_issue(workspace_id=app.workspace_id, sender="ME", recipient="ME",
                            subject_ref=task, severity="low", body="issue")
    assert calls.count(("issue", "ISSUE")) == 2  # fields then strict parsed publication bytes


def test_examples_launch_outside_repository(tmp_path):
    environment = dict(os.environ, PYTHONPATH=str(REPO / "src"))
    for mode in ("sequential", "family"):
        output = subprocess.check_output([sys.executable, str(REPO / "examples/v4/application.py"),
                                           mode], cwd=tmp_path, env=environment, text=True)
        assert json.loads(output)["state"] == "archive"
