"""External stdlib-only JSON-RPC client; never imports either FCoP package."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

PROFILE = "profile:wp4d-offline-demo"


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            if p.is_file() else None for p in sorted(root.rglob("*"))}


class Connection:
    def __init__(self, root, source=False, index=0):
        self.root, self.counter, self.incoming = root, 0, queue.Queue()
        env = {k: v for k, v in os.environ.items() if not k.startswith("FCOP_")}
        env["FCOP_PROJECT_DIR"] = str(root)
        if not source:
            env.pop("PYTHONPATH", None)
        flags = ["-B"] if source else ["-I", "-B"]
        self.log = (root.parent / f"server-{index}.log").open("wb")
        self.proc = subprocess.Popen(
            [sys.executable, *flags, str(Path(__file__).with_name("server.py")), str(root)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log,
            text=True, encoding="utf-8", env=env,
        )
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()
        try:
            result = self.rpc("initialize", {
                "protocolVersion": "2025-11-25", "capabilities": {},
                "clientInfo": {"name": "wp4d-external", "version": "1"},
            })
            assert result["protocolVersion"]
            self.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            tools = self.rpc("tools/list", {})["tools"]
            resources = self.rpc("resources/list", {})["resources"]
            templates = self.rpc("resources/templates/list", {})["resourceTemplates"]
            assert (len(tools), len(resources), len(templates)) == (46, 12, 4)
            self.tools = {t["name"]: t["inputSchema"] for t in tools}
        except BaseException:
            self.close()
            raise

    def read(self):
        for line in self.proc.stdout:
            self.incoming.put(line)
        self.incoming.put(None)

    def send(self, message):
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()

    def rpc(self, method, params):
        self.counter += 1
        self.send(dict(jsonrpc="2.0", id=self.counter, method=method, params=params))
        while True:
            line = self.incoming.get(timeout=90)
            assert line is not None, "Server exited; inspect stderr log"
            message = json.loads(line)
            if message.get("id") != self.counter:
                continue
            assert "error" not in message, message
            return message["result"]

    def call(self, name, **arguments):
        assert name in self.tools, name
        schema = self.tools[name]
        assert set(schema.get("required", [])) <= arguments.keys(), (name, schema)
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        assert not result.get("isError"), result
        assert isinstance(result.get("structuredContent"), dict), result
        return result["structuredContent"]

    def close(self):
        if self.proc.poll() is None:
            self.proc.kill()
        self.proc.wait(timeout=30)
        self.reader.join(timeout=10)
        self.log.close()
        assert not self.reader.is_alive()


class Application:
    def __init__(self, connection, workspace_id):
        self.c, self.workspace_id = connection, workspace_id

    def create(self, operation, branch=None):
        request = dict(workspace_id=self.workspace_id, operation_id=operation,
                       sender="ME", recipient="ME", subject=operation, body="Offline MCP sample")
        if branch is not None:
            request["branch_of"] = branch
        return request, self.c.call("create_task", **request)

    def start(self, operation, branch=None):
        task = self.create(operation, branch)[1]["task_id"]
        self.c.call("claim_task", task_id=task, actor="ME")
        return task

    def review(self, task, kind, decision, **fields):
        return self.c.call("write_review", workspace_id=self.workspace_id,
                           reviewer_role="ME", recipient="ME", subject_type="task",
                           subject_ref=task, review_kind=kind, decision=decision,
                           body="Offline MCP evidence", **fields)["review_id"]

    def authorize(self, task, source, target, report=None, family=None):
        return self.review(task, "acceptance" if report else "authorization",
                           "approved" if report else "authorize",
                           attempt_id=self.c.call("inspect_task", filename=task)["current_attempt_id"],
                           references=[report] if report else [],
                           transition={"from": source, "to": target},
                           profile_ref=PROFILE, issuer_proof="demo-only",
                           issued_at=datetime.now(timezone.utc).isoformat(), expires_at=None,
                           authorization_scope="single_use", operation_kind="lifecycle_transition",
                           family_digest=family)

    def complete(self, task):
        report = self.c.call(
            "write_report", task_id=task, reporter="ME", recipient="ME", body="Finished",
            workspace_id=self.workspace_id,
            attempt_id=self.c.call("inspect_task", filename=task)["current_attempt_id"],
            report_kind="final", result="done",
        )["report_id"]
        self.c.call("submit_task", task_id=task, actor="ME", report_ref=report)
        auth = self.authorize(task, "review", "done", report=report)
        self.c.call("approve_task", task_id=task, actor="ME", report_ref=report,
                    review_ref=auth, authorization_ref=auth, profile_ref=PROFILE)
        return report

    def archive(self, task, convergence=None, family=None):
        auth = self.authorize(task, "done", "archive", family=family)
        fields = dict(task_id=task, actor="ME", authorization_ref=auth, profile_ref=PROFILE)
        if convergence:
            fields.update(review_ref=convergence, family_digest=family)
        self.c.call("archive_task", **fields)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--source", action="store_true")
    args = parser.parse_args()
    directory = args.directory.resolve()
    directory.mkdir(parents=True)
    root = directory / "workspace"
    c = Connection(root, args.source, 1)
    try:
        workspace = c.call("init_solo", role_code="ME", protocol_version="4.0", profiles=[PROFILE])
        app = Application(c, workspace["workspace_id"])
        seq = app.start("sequential")
        app.complete(seq)
        app.archive(seq)
        parent = app.start("family-root")
        branch = app.start("family-branch", parent)
        branch_two = app.start("family-branch-two", parent)
        report = app.complete(branch)
        report_two = app.complete(branch_two)
        app.complete(parent)
        family = c.call("inspect_task", filename=parent, include_family_digest=True)["family_digest"]
        convergence = app.review(parent, "convergence", "approved", family_digest=family,
                                 references=[report, report_two])
        app.archive(parent, convergence, family)
        # Two independent stdio servers submit real writes to one workspace.
        # The barrier coordinates request dispatch, never substitutes for the writes.
        competitor = Connection(root, args.source, 3)
        try:
            assert competitor.proc.pid != c.proc.pid
            request = dict(workspace_id=workspace["workspace_id"], operation_id="race-same",
                           sender="ME", recipient="ME", subject="Concurrent task", body="same")
            barrier = threading.Barrier(2)

            def compete(connection):
                barrier.wait(timeout=30)
                return connection.call("create_task", **request)

            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(compete, connection) for connection in (c, competitor)]
                raced = [f.result(timeout=90) for f in futures]
            assert raced[0]["task_id"] == raced[1]["task_id"]
            assert raced[0]["digest"] == raced[1]["digest"]
            assert sorted(r["existing"] for r in raced) == [False, True]
            race_before = snapshot(root)
            replay = competitor.call("create_task", **request)
            assert replay["existing"] and replay["task_id"] == raced[0]["task_id"]
            assert snapshot(root) == race_before
            failed = competitor.rpc("tools/call", {"name": "create_task",
                                     "arguments": {**request, "body": "different"}})
            assert failed["isError"]
            assert failed["structuredContent"]["code"] == "OPERATION_ID_CONFLICT"
            assert snapshot(root) == race_before
        finally:
            competitor.close()
        lost_request, first = app.create("response-lost")
        # Transport observes completion but withholds it from the retrying app.
        # Kill the actual service only after committed filesystem facts exist.
        tasks = [seq, parent, branch, branch_two, first["task_id"]]
        observed = [c.call("read_task", filename=t) for t in tasks]
        before = snapshot(root)
    finally:
        c.close()
    c = Connection(root, args.source, 2)
    try:
        assert snapshot(root) == before
        assert [c.call("read_task", filename=t) for t in tasks] == observed
        current_family = c.call("inspect_task", filename=parent,
                                include_family_digest=True)["family_digest"]
        assert current_family == family
        again = c.call("create_task", **lost_request)
        assert again["existing"] is True
        assert again["task_id"] == first["task_id"]
        assert again["digest"] == first["digest"]
        assert snapshot(root) == before
        rejected = c.rpc("tools/call", {"name": "create_task",
                         "arguments": {**lost_request, "body": "conflict"}})
        assert rejected["isError"]
        assert rejected["structuredContent"]["code"] == "OPERATION_ID_CONFLICT"
        assert snapshot(root) == before
        states = [c.call("inspect_task", filename=t)["stage"] for t in tasks]
        assert states == ["archive", "archive", "done", "done", "inbox"]
        assert sum(len(v["transitions"]) for v in observed) == 19
        race_retry = c.call("create_task", **request)
        assert race_retry["existing"] and race_retry["task_id"] == raced[0]["task_id"]
        assert snapshot(root) == before
        print(json.dumps(dict(mode="SOURCE_ONLY" if args.source else "INSTALLED",
                              transport="stdio-json-rpc", tools=46, resources=12, templates=4,
                              states=states, transitions=19, service_processes=3,
                              branches=2, concurrent_real_writes=2, same_operation_one_result=True,
                              exact_retry=True, convergence=True, zero_conflict_effects=True),
                         sort_keys=True))
    finally:
        c.close()
    assert not any(n in {"fcop", "fcop_mcp"} or n.startswith(("fcop.", "fcop_mcp."))
                   for n in sys.modules)


if __name__ == "__main__":
    main()
