"""Run a small, verifiable handoff through two independent MCP stdio sessions.

Requires Python 3.10+ and uvx. Packages are resolved in uv's isolated environment.
Only a fresh demo directory is initialized; no IDE configuration is changed.
"""

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

VERSION = "4.0.2"
INPUT = "FCoP handoff example"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


class Session:
    def __init__(self, root, run, label, transcript):
        self.root, self.run, self.label = root, run, label
        self.transcript = transcript
        self.counter = 0
        self.process = None

    async def __aenter__(self):
        uvx = shutil.which("uvx")
        require(uvx, "uvx is missing from PATH. See docs/mcp-handoff.md for setup.")
        self.stderr = (self.run / f"{self.label}-stderr.log").open("wb")
        try:
            self.process = await asyncio.create_subprocess_exec(
                uvx, "--from", f"fcop-mcp=={VERSION}", "--with", f"fcop=={VERSION}",
                "fcop-mcp", env=dict(os.environ, FCOP_PROJECT_DIR=str(self.root)),
                stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                stderr=self.stderr, limit=8 * 1024 * 1024,
            )
            await self.request("initialize", {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "fcop-handoff-example", "version": "1.0"},
            })
            self.process.stdin.write(
                b'{"jsonrpc":"2.0","method":"notifications/initialized"}\n'
            )
            await self.process.stdin.drain()
            return self
        except BaseException:
            await self.close()
            raise

    async def request(self, method, params):
        self.counter += 1
        request = {"jsonrpc": "2.0", "id": self.counter, "method": method, "params": params}
        self.process.stdin.write((json.dumps(request) + "\n").encode())
        await self.process.stdin.drain()
        deadline = asyncio.get_running_loop().time() + 180
        while True:
            remaining = deadline - asyncio.get_running_loop().time()
            require(remaining > 0, f"Timeout: {method}")
            raw = await asyncio.wait_for(self.process.stdout.readline(), timeout=remaining)
            require(raw, f"MCP server exited; check {self.label}-stderr.log")
            response = json.loads(raw)
            if response.get("id") != self.counter:
                continue
            self.transcript.write(json.dumps({
                "session": self.label, "request": request, "response": response,
            }) + "\n")
            self.transcript.flush()
            require("error" not in response, f"MCP error: {response.get('error')}")
            return response["result"]

    async def call(self, name, arguments):
        result = await self.request("tools/call", {"name": name, "arguments": arguments})
        require(not result.get("isError"), f"Tool failed: {name}; see transcript.jsonl")
        return result["structuredContent"]

    async def close(self):
        try:
            if self.process and self.process.returncode is None:
                self.process.stdin.close()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=10)
                except asyncio.TimeoutError:
                    self.process.terminate()
                    try:
                        await asyncio.wait_for(self.process.wait(), timeout=5)
                    except asyncio.TimeoutError:
                        self.process.kill()
                        await self.process.wait()
        finally:
            self.stderr.close()

    async def __aexit__(self, *args):
        await self.close()


async def handoff(root, run, transcript):
    print("1/4 Discover the published MCP adapter (no workspace writes).", flush=True)
    async with Session(root, run, "first", transcript) as first:
        catalog = await first.request("tools/list", {})
        resources = await first.request("resources/list", {})
        templates = await first.request("resources/templates/list", {})
        counts = {
            "tools": len(catalog["tools"]), "resources": len(resources["resources"]),
            "templates": len(templates["resourceTemplates"]),
        }
        require(counts == {"tools": 49, "resources": 12, "templates": 4}, "Catalog mismatch")
        require(not snapshot(root), "Discovery modified the demo workspace")
        print("2/4 Create, claim, compute SHA-256 and submit a report for review.", flush=True)
        manifest = await first.call("init_solo", {
            "role_code": "ME", "lang": "en", "protocol_version": "4.0",
        })
        workspace_id = manifest["workspace_id"]
        created = await first.call("write_task", {
            "workspace_id": workspace_id, "operation_id": uuid.uuid4().urn,
            "sender": "ADMIN", "recipient": "ME",
            "subject": "Compute a digest and leave a handoff report",
            "body": f"Compute SHA-256 of the UTF-8 text {INPUT}. Record input and digest.",
        })
        task_id = created["task_id"]
        await first.call("claim_task", {"task_id": task_id, "actor": "ME"})
        state = await first.call("inspect_task", {"filename": task_id})
        require(state["stage"] == "active", "Task was not claimed")
        attempt_id = state["current_attempt_id"]
        digest = hashlib.sha256(INPUT.encode()).hexdigest()
        report = await first.call("write_report", {
            "workspace_id": workspace_id, "task_id": task_id, "attempt_id": attempt_id,
            "reporter": "ME", "recipient": "ADMIN", "result": "done",
            "body": f"Input (UTF-8): {INPUT}\nSHA-256: {digest}\n"
                    "Computed locally with Python hashlib. Review is still pending.",
        })
        report_id = report["report_id"]
        await first.call("submit_task", {
            "task_id": task_id, "actor": "ME", "report_ref": report_id,
        })
        first_pid = first.process.pid

    print("3/4 First session exited. Open a new session on the same files.", flush=True)
    before = snapshot(root)
    require(before, "No workspace files persisted")
    async with Session(root, run, "second", transcript) as second:
        restored = await second.call("inspect_task", {"filename": task_id})
        read_report = await second.call("read_report", {"filename": report_id})
        require(restored["task_id"] == task_id, "Task identity changed")
        require(restored["stage"] == "review", "Task is no longer pending review")
        require(restored["current_attempt_id"] == attempt_id, "Attempt identity changed")
        require(read_report["report_id"] == report_id, "Report identity changed")
        require(read_report["subject_ref"] == task_id, "Report/task relationship changed")
        require(read_report["attempt_id"] == attempt_id, "Report/attempt relationship changed")
        require(f"Input (UTF-8): {INPUT}" in read_report["content"], "Report input missing")
        require(f"SHA-256: {digest}" in read_report["content"], "Report digest missing")
        second_pid = second.process.pid
    after = snapshot(root)
    require(before == after, "Second-session observation changed workspace files")
    print(f"4/4 PASS: same task, attempt and report; {len(before)} files unchanged; review pending.", flush=True)
    return {
        "status": "pass", "package_pair": VERSION, "workspace": str(root),
        "task_id": task_id, "report_id": report_id, "attempt_id": attempt_id,
        "stage": "review", "digest": digest, "discovery": counts,
        "launcher_pids": [first_pid, second_pid],
        "files_verified_unchanged_on_resume": len(before), "file_hashes": after,
        "scope": "Scripted MCP sessions; no model or external user; review remains pending.",
    }


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Parent for a new run; default: system temp")
    args = parser.parse_args()
    require(shutil.which("uvx"), "uvx is missing from PATH. See docs/mcp-handoff.md for setup.")
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="fcop-handoff-", dir=args.output)).resolve()
    root = run / "workspace"
    root.mkdir()
    print(f"Run directory: {run}", flush=True)
    print("First run may download the pinned 4.0.2 packages from PyPI.", flush=True)
    with (run / "transcript.jsonl").open("w", encoding="utf-8") as transcript:
        try:
            result = await handoff(root, run, transcript)
        except Exception as error:
            result = {"status": "fail", "error": str(error) or type(error).__name__}
            (run / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            raise
    (run / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Evidence: {run / 'result.json'}", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (Exception, KeyboardInterrupt) as exc:
        print(f"FAIL: {str(exc) or type(exc).__name__}", file=sys.stderr)
        sys.exit(1)
