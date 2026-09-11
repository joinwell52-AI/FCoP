"""Characterize installed Core 4.0.0; NOT acceptance tests for new MCP tools.

Run with an installed Core interpreter and -I. All workspace writes are temporary.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import fcop
from fcop import Project
from fcop.errors import FcopError


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            if p.is_file() else None for p in sorted(root.rglob("*"))}


def attempt(call):
    try:
        return {"result": call()}
    except FcopError as exc:
        return {"code": exc.code, "exception": type(exc).__name__}


def worker():
    data = json.loads(sys.stdin.readline())
    project = Project(Path(data["root"]))
    print("READY", flush=True)
    assert sys.stdin.readline().strip() == "GO"
    print(json.dumps(attempt(lambda: project.write_review(**data["request"]))), flush=True)


def main():
    assert importlib.metadata.version("fcop") == "4.0.0"
    assert "site-packages" in str(Path(fcop.__file__)).lower()
    repo = Path(__file__).resolve().parents[2]
    helper_path = repo / "tests/stable/third-party/python-only/app.py"
    spec = importlib.util.spec_from_file_location("consumer_example", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    observations = {"core_version": "4.0.0", "core_module": fcop.__file__,
                    "helper_sha256": hashlib.sha256(helper_path.read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix="fcop-branch-capabilities-") as temp:
        root = Path(temp) / "workspace"
        created = Project(root).create_workspace(protocol_version="4.0", profiles=[helper.PROFILE])
        app = helper.Application(root, created["workspace_id"])
        root_id = app.start("root")
        _, branch = app.create("branch-a", root_id)
        branch_id = branch["task_id"]
        before = snapshot(root)
        observations["inbox_branch_digest"] = attempt(lambda: app.p.family_digest(root_task_id=root_id))
        assert observations["inbox_branch_digest"]["code"] == "ATTEMPT_MISMATCH"
        assert snapshot(root) == before
        app.move(branch_id, "inbox", "active", "claim_task")
        before = snapshot(root)
        observations["active_branch_without_report_digest"] = attempt(
            lambda: app.p.family_digest(root_task_id=root_id))
        assert observations["active_branch_without_report_digest"]["code"] == "REPORT_REQUIRED"
        assert snapshot(root) == before
        report_a = app.complete(branch_id)
        branch_b = app.start("branch-b", root_id)
        report_b = app.complete(branch_b)
        app.complete(root_id)
        digest = app.p.family_digest(root_task_id=root_id)
        request = dict(workspace_id=created["workspace_id"], sender="ME", recipient="ME",
                       subject_ref=root_id, review_kind="convergence", decision="approved",
                       body="Caller conclusion: combine both results; no conflict.",
                       references=[report_a, report_b], family_digest=digest)
        before = snapshot(root)
        observations["convergence_with_operation_id"] = attempt(
            lambda: app.p.write_review(**request, operation_id="same-merge-operation"))
        assert observations["convergence_with_operation_id"]["code"] == "INVALID_ENVELOPE"
        assert snapshot(root) == before
        # Diagnostic only: even borrowing Core's private lock cannot wrap the
        # public append in a single transaction; that append acquires it again.
        from fcop.v4.linearization import family_boundary
        with family_boundary(root, created["workspace_id"], root_id):
            observations["public_append_inside_existing_family_lock"] = attempt(
                lambda: app.p.write_review(**request))
        assert observations["public_append_inside_existing_family_lock"]["code"] == "LOCK_RECOVERY_REQUIRED"
        assert snapshot(root) == before
        processes = [subprocess.Popen([sys.executable, "-I", str(Path(__file__).resolve()), "worker"],
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, text=True) for _ in range(2)]
        try:
            for process in processes:
                process.stdin.write(json.dumps({"root": str(root), "request": request}) + "\n")
                process.stdin.flush()
            for process in processes:
                assert process.stdout.readline().strip() == "READY"
            for process in processes:
                process.stdin.write("GO\n")
                process.stdin.flush()
            results = []
            for process in processes:
                out, err = process.communicate(timeout=30)
                assert process.returncode == 0, err
                results.append(json.loads(out))
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.wait()
        observations["concurrent_convergence_appends"] = results
        assert len({item["result"]["review_id"] for item in results}) == 2
        observations["family_digest_after_two_appends"] = app.p.family_digest(root_task_id=root_id)
        assert observations["family_digest_after_two_appends"] == digest
        # A fresh process submits the identical formal append after both exited.
        p = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve()), "worker"],
                           input=json.dumps({"root": str(root), "request": request}) + "\nGO\n",
                           capture_output=True, text=True, timeout=30)
        assert p.returncode == 0, p.stderr
        retry = json.loads(p.stdout.splitlines()[-1])
        observations["fresh_process_same_append"] = retry
        assert retry["result"]["review_id"] not in {r["result"]["review_id"] for r in results}
        observations["read_rejections_zero_workspace_writes"] = True
    print(json.dumps(observations, indent=2))


if __name__ == "__main__":
    worker() if sys.argv[1:] == ["worker"] else main()
