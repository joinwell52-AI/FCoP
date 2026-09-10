"""Copyable installed-library demo. Educational Profile is not issuer security."""
from __future__ import annotations

import argparse
import hashlib
import json
import socket
import sys
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path

PROFILE = "profile:wp4d-offline-demo"
MODULES = ["workspace", "envelopes", "relations", "authorization", "idempotency",
           "recovery", "lifecycle", "compatibility", "convergence"]


def offline(event, args):
    if event not in {"socket.connect", "socket.bind", "socket.getaddrinfo", "socket.sendto"}:
        return
    caller = sys._getframe(1).f_code
    if caller.co_filename == socket.__file__ and caller.co_name == "_fallback_socketpair":
        return
    raise RuntimeError("WP4D application network access forbidden: " + event)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes()) if p.is_file() else None
            for p in sorted(root.rglob("*"))}


def encode_bytes(value):
    if isinstance(value, bytes):
        return {"wp4d_bytes_hex": value.hex()}
    raise TypeError(type(value).__name__)


def decode_bytes(value):
    return bytes.fromhex(value["wp4d_bytes_hex"]) if set(value) == {"wp4d_bytes_hex"} else value


def write_json(path, value):
    path.write_bytes((json.dumps(value, sort_keys=True, ensure_ascii=True, default=encode_bytes) + "\n").encode())


def evaluator(*, profile_ref, issuer, proof):
    return "AUTHORIZED" if (profile_ref, issuer, proof) == (PROFILE, "ME", "demo-only") else "DENIED"


def project(root):
    from fcop import Project
    return Project(root, trusted_profiles={PROFILE: evaluator})


def reject(root, call, code):
    from fcop.errors import FcopError
    before = snapshot(root)
    try:
        call()
    except FcopError as exc:
        assert exc.code == code, (exc.code, code)
    else:
        raise AssertionError("Expected structured rejection: " + code)
    assert snapshot(root) == before


class Application:
    def __init__(self, root, workspace_id):
        self.p, self.workspace_id = project(root), workspace_id

    def create(self, operation_id, branch_of=None):
        request = dict(workspace_id=self.workspace_id, operation_id=operation_id,
                       sender="ME", recipient="ME", subject=operation_id, body="Offline sample")
        if branch_of is not None:
            request["branch_of"] = branch_of
        return request, self.p.create_task(**request)

    def move(self, task, source, target, tool, **evidence):
        return self.p.transition(task_id=task, from_stage=source, to_stage=target,
                                 tool=tool, actor="ME", **evidence)

    def review(self, task, kind, decision, **fields):
        return self.p.write_review(
            workspace_id=self.workspace_id, sender="ME", recipient="ME",
            subject_ref=task, body="Demo evidence", review_kind=kind, decision=decision, **fields,
        )["review_id"]

    def authorize(self, task, source, target, *, report=None, family=None):
        return self.review(
            task, "acceptance" if report else "authorization",
            "approved" if report else "authorize",
            attempt_id=self.p.inspect_state(task_id=task)["current_attempt_id"],
            references=[report] if report else [], transition={"from": source, "to": target},
            profile_ref=PROFILE, issuer_proof="demo-only",
            issued_at=datetime.now(timezone.utc).isoformat(), expires_at=None,
            authorization_scope="single_use", operation_kind="lifecycle_transition",
            family_digest=family,
        )

    def start(self, operation, branch_of=None):
        task = self.create(operation, branch_of)[1]["task_id"]
        self.move(task, "inbox", "active", "claim_task")
        return task

    def complete(self, task):
        report = self.p.write_report(
            workspace_id=self.workspace_id, sender="ME", recipient="ME", subject_ref=task,
            body="Finished", attempt_id=self.p.inspect_state(task_id=task)["current_attempt_id"],
            report_kind="final", result="done",
        )["report_id"]
        self.move(task, "active", "review", "submit_task", report_ref=report)
        auth = self.authorize(task, "review", "done", report=report)
        self.move(task, "review", "done", "approve_task", report_ref=report, review_ref=auth,
                  authorization_ref=auth, profile_ref=PROFILE)
        return report

    def archive(self, task, convergence=None, family=None):
        auth = self.authorize(task, "done", "archive", family=family)
        fields = dict(authorization_ref=auth, profile_ref=PROFILE)
        if convergence is not None:
            fields.update(review_ref=convergence, family_digest=family)
        self.move(task, "done", "archive", "archive_task", **fields)


def prepare_host(root, app):
    package = root.parent / "rules"
    package.mkdir()
    bundled = files("fcop.rules").joinpath("_data", "v4")
    for entry in bundled.iterdir():
        if entry.is_file():
            (package / entry.name).write_bytes(entry.read_bytes())
    assert len(list(package.iterdir())) == 19
    profile = root.parent / "host-profile.json"
    write_json(profile, {
        "host_id": "codex", "profile_version": "1.0-candidate.1",
        "supported_entry_kinds": ["markdown"], "reference_mode": "none",
        "projection_mode": "bounded_embed", "target_paths": ["AGENTS.md"],
        "preserve_regions": [["<!-- fcop:v4:begin -->", "<!-- fcop:v4:end -->"]],
        "max_projection_bytes": 65536, "encoding": "UTF-8-no-BOM",
        "newline": "LF", "languages": ["en"],
    })
    request = dict(manifest_path=str(package / "manifest.json"),
                   host_profile_path=str(profile), workspace_id=app.workspace_id,
                   protocol_version="4.0", assembly_id="parallel",
                   selected_modules=MODULES, selected_languages=["en"])
    def call(action, req=request):
        return app.p.rule_distribution(action=action, request=req)
    before = snapshot(root.parent)
    assert len(call("validate")["artifacts"]) == 18
    selected = call("select")
    assert selected
    call("plan")
    assert snapshot(root.parent) == before
    reject(root.parent, lambda: call("select", {**request, "protocol_version": "3.0"}),
           "UNSUPPORTED_WORKSPACE_VERSION")
    target = package / "workspace.en.md"
    original = target.read_bytes()
    target.unlink()
    reject(root.parent, lambda: call("select"), "toolkit:RULE_ARTIFACT_MISMATCH")
    target.write_bytes(original + b"changed\n")
    reject(root.parent, lambda: call("select"), "toolkit:RULE_ARTIFACT_MISMATCH")
    target.write_bytes(original)
    manifest_path = package / "manifest.json"
    original_manifest = manifest_path.read_bytes()
    oversized = b"X" * 66000 + b"\n"
    target.write_bytes(oversized)
    manifest = json.loads(original_manifest)
    artifact = next(a for a in manifest["artifacts"] if a["source_path"] == target.name)
    artifact.update(size_bytes=len(oversized), sha256=sha(oversized))
    write_json(manifest_path, manifest)
    reject(root.parent, lambda: call("plan"), "toolkit:RULE_PROJECTION_LIMIT")
    target.write_bytes(original)
    manifest_path.write_bytes(original_manifest)
    authority = root.parent / "selection.md"
    authority.write_bytes(b"Explicit educational choice: parallel / codex / en.\n")
    request.update(recorded_at="2026-09-09T00:00:00+00:00",
                   admin_selection_ref={"path": str(authority), "sha256": sha(authority.read_bytes())})
    adoption = call("adopt")["adoption_receipt_ref"]
    request["adoption_receipt_ref"] = adoption
    before = snapshot(root.parent)
    request["plan"] = call("plan")
    assert snapshot(root.parent) == before
    deployment = call("apply")["deployment_receipt_ref"]
    assert (root / "AGENTS.md").is_file()
    return request, deployment


def layers(app, request, deployment):
    return app.p.rule_distribution(action="inspect_layers", request={
        "manifest_path": request["manifest_path"],
        "adoption_receipt_ref": request["adoption_receipt_ref"],
        "deployment_receipt_ref": deployment,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["hold", "inspect"])
    parser.add_argument("directory", type=Path)
    parser.add_argument("--source", action="store_true")
    args = parser.parse_args()
    sys.addaudithook(offline)
    import fcop
    assert fcop.__version__ == "4.0.0rc1"
    if not args.source:
        assert Path(fcop.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    assert not any(n == "fcop_mcp" or n.startswith("fcop_mcp.") for n in sys.modules)
    directory = args.directory.resolve()
    if args.mode == "hold":
        assert not directory.exists(), "A fresh caller-owned directory is required"
        directory.mkdir(parents=True)
    else:
        assert directory.is_dir()
    root = directory / "workspace"
    witness = directory / "witness.json"
    if args.mode == "hold":
        identity = project(root).create_workspace(protocol_version="4.0", profiles=[PROFILE])
        app = Application(root, identity["workspace_id"])
        seq = app.start("sequential")
        app.complete(seq)
        app.archive(seq)
        parent = app.start("family-root")
        branch = app.start("family-branch", parent)
        branch_report = app.complete(branch)
        app.complete(parent)
        family = app.p.family_digest(root_task_id=parent)
        convergence = app.review(parent, "convergence", "approved", family_digest=family,
                                 references=[branch_report])
        app.archive(parent, convergence, family)
        request, result = app.create("response-lost")
        # A transport witness observes completion; the simulated application
        # receives no result before its process is externally terminated.
        reject(directory, lambda: app.p.create_task(**{**request, "body": "different"}),
               "OPERATION_ID_CONFLICT")
        host_request, deployment = prepare_host(root, app)
        tasks = [seq, parent, branch, result["task_id"]]
        observed = [app.p.read_task(task_id=t) for t in tasks]
        context = layers(app, host_request, deployment)
        assert context["runtime_consumption_verified"] is None
        write_json(witness, dict(workspace_id=identity["workspace_id"], request=request,
                   result=result, tasks=tasks, observed=observed, workspace=snapshot(root),
                   family=family, context=context, host_request=host_request, deployment=deployment))
        print("COMMITTED", flush=True)
        sys.stdin.read()  # Test controller kills the real process here.
        raise AssertionError("Controller did not terminate at durable boundary")
    data = json.loads(witness.read_bytes(), object_hook=decode_bytes)
    app = Application(root, data["workspace_id"])
    before = snapshot(directory)
    assert snapshot(root) == data["workspace"]
    assert [app.p.read_task(task_id=t) for t in data["tasks"]] == data["observed"]
    assert app.p.family_digest(root_task_id=data["tasks"][1]) == data["family"]
    assert layers(app, data["host_request"], data["deployment"]) == data["context"]
    again = app.p.create_task(**data["request"])
    assert again["existing"] is True and again["task_id"] == data["result"]["task_id"]
    assert again["digest"] == data["result"]["digest"]
    assert snapshot(directory) == before
    host = app.p.rule_distribution(action="apply", request=data["host_request"])
    assert host["existing"] is True and host["deployment_receipt_ref"] == data["deployment"]
    assert snapshot(directory) == before
    app.p.rule_distribution(action="verify_deployment",
                            request={**data["host_request"], "deployment_receipt_ref": data["deployment"]})
    rollback = {**data["host_request"], "deployment_receipt_ref": data["deployment"],
                "recorded_at": "2026-09-09T00:01:00+00:00"}
    app.p.rule_distribution(action="rollback", request=rollback)
    assert not (root / "AGENTS.md").exists()
    before = snapshot(directory)
    assert app.p.rule_distribution(action="rollback", request=rollback)["existing"] is True
    assert snapshot(directory) == before
    states = [app.p.inspect_state(task_id=t)["stage"] for t in data["tasks"]]
    assert states == ["archive", "archive", "done", "inbox"]
    assert sum(len(v["transitions"]) for v in data["observed"]) == 15
    print(json.dumps(dict(mode="SOURCE_ONLY" if args.source else "INSTALLED",
                          states=states, transitions=15, exact_retry=True,
                          disk_reopen=True, host_rollback=True, rules=19,
                          import_path=fcop.__file__), sort_keys=True))


if __name__ == "__main__":
    main()
