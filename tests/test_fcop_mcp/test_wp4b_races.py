"""Real simultaneous MCP submissions, never parameter/surface race probes."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from importlib import import_module
from pathlib import Path
from threading import Barrier
from typing import Any

import pytest

from .test_wp4b_delivery import app_at, call, facts, trusted


def _simultaneous(root: Path, requests: list[tuple[str, dict[str, Any]]]) -> list[Any]:
    barrier = Barrier(len(requests))
    def worker(item: tuple[str, dict[str, Any]]) -> Any:
        server = trusted(root)
        barrier.wait(timeout=30)
        return call(server, *item)
    with ThreadPoolExecutor(max_workers=len(requests)) as pool:
        return list(pool.map(worker, requests))


def test_branch_reopen_vs_root_archive(tmp_path: Path) -> None:
    example = import_module("examples.v4.application")
    app = app_at(tmp_path)
    root = app.task("Root")
    branch = app.task("Branch", branch_of=root)
    report = app.complete(branch)
    app.complete(root)
    family = app.project.family_digest(root_task_id=root)
    convergence = app.review(root, "convergence", "approved", family_digest=family, references=[report])
    archive_auth = app.authorization(root, "done", "archive", family=family)
    attempt = app.project.inspect_state(task_id=branch)["current_attempt_id"]
    review = app.review(branch, "reopen", "approved", attempt_id=attempt)
    auth = app.authorization(branch, "done", "active", refs=[review])
    results = _simultaneous(tmp_path, [
        ("reopen_task", dict(task_id=branch, review_ref=review, authorization_ref=auth,
                             profile_ref=example.PROFILE, actor="ME")),
        ("archive_task", dict(task_id=root, review_ref=convergence, authorization_ref=archive_auth,
                              profile_ref=example.PROFILE, family_digest=family, actor="ME")),
    ])
    assert sum(not result.is_error for result in results) == 1
    branch_state = app.project.inspect_state(task_id=branch)
    root_state = app.project.inspect_state(task_id=root)
    if not results[0].is_error:
        assert branch_state["stage"] == "active" and root_state["stage"] == "done"
        assert branch_state["current_attempt_id"] != attempt
        assert results[1].structured_content["code"] == "BRANCH_NOT_TERMINAL"
        before = facts(tmp_path)
        rejected = call(trusted(tmp_path), "submit_task", dict(task_id=branch, report_ref=report))
        assert rejected.structured_content["code"] == "ATTEMPT_MISMATCH"
        assert facts(tmp_path) == before
        app.complete(branch)
        assert app.project.family_digest(root_task_id=root) != family
        stale = call(trusted(tmp_path), "archive_task", dict(task_id=root, review_ref=convergence,
                     authorization_ref=archive_auth, profile_ref=example.PROFILE, family_digest=family, actor="ME"))
        assert stale.is_error and stale.structured_content["code"] == "FAMILY_CONVERGENCE_MISMATCH"
    else:
        assert root_state["stage"] == "archive" and branch_state["stage"] == "done"
        assert results[0].structured_content["code"] == "INVALID_TRANSITION"
        assert branch_state["current_attempt_id"] == attempt


def test_root_reopen_vs_branch_create(tmp_path: Path) -> None:
    example = import_module("examples.v4.application")
    app = app_at(tmp_path)
    root = app.task("Root")
    app.complete(root)
    attempt = app.project.inspect_state(task_id=root)["current_attempt_id"]
    review = app.review(root, "reopen", "approved", attempt_id=attempt)
    auth = app.authorization(root, "done", "active", refs=[review])
    results = _simultaneous(tmp_path, [
        ("reopen_task", dict(task_id=root, review_ref=review, authorization_ref=auth,
                             profile_ref=example.PROFILE, actor="ME")),
        ("create_task", dict(workspace_id=app.workspace_id, operation_id="branch-race", sender="ME",
                             recipient="ME", subject="Branch", body="work", branch_of=root)),
    ])
    assert not results[0].is_error
    assert app.project.inspect_state(task_id=root)["stage"] == "active"
    if results[1].is_error:
        assert results[1].structured_content["code"] == "ROOT_NOT_ACTIVE"
    else:
        fields = app.project.read_task(task_id=results[1].structured_content["task_id"])
        assert fields["branch_of"] == root


@pytest.mark.parametrize("different", [False, True])
def test_cross_process_create_idempotency(tmp_path: Path, different: bool) -> None:
    app = app_at(tmp_path)
    request = dict(workspace_id=app.workspace_id, operation_id="same-operation", sender="ME",
                   recipient="ME", subject="Same request", body="work")
    script = """
import asyncio,json,sys,time
from pathlib import Path
from fastmcp import Client
from fcop_mcp.server import create_server
root=Path(sys.argv[1]); start=Path(sys.argv[2]); request=json.loads(sys.argv[3]); ready=Path(sys.argv[4])
async def run():
    async with Client(create_server(root)) as client:
        ready.touch()
        deadline=time.monotonic()+45
        while not start.exists():
            if time.monotonic()>deadline: raise RuntimeError('race start timeout')
            await asyncio.sleep(.01)
        r=await client.call_tool('create_task',request,raise_on_error=False)
        print('RESULT='+json.dumps({'error':r.is_error,'value':r.structured_content}),flush=True)
asyncio.run(run())
"""
    barrier = tmp_path.parent / (tmp_path.name + "-start")
    env = dict(os.environ)
    repo = Path(__file__).resolve().parents[2]
    env["PYTHONPATH"] = os.pathsep.join([str(repo / "src"), str(repo / "mcp/src")])
    requests = [request, {**request, "subject": "Different"} if different else request]
    ready = [tmp_path.parent / (tmp_path.name + f"-ready-{index}") for index in range(2)]
    processes = [subprocess.Popen([sys.executable, "-c", script, str(tmp_path), str(barrier), json.dumps(r), str(marker)],
                                  env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for r, marker in zip(requests, ready, strict=True)]
    results = []
    try:
        import time

        deadline = time.monotonic() + 60
        while not all(marker.exists() for marker in ready):
            assert time.monotonic() < deadline, "Both real MCP clients must initialize before release"
            time.sleep(.01)
        barrier.touch()
        for process in processes:
            out, err = process.communicate(timeout=90)
            assert process.returncode == 0, err
            results.append(json.loads(next(line[7:] for line in out.splitlines() if line.startswith("RESULT="))))
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.communicate()
    assert len(list((tmp_path / "fcop/_lifecycle/inbox").glob("TASK-*.md"))) == 1
    if different:
        assert sum(result["error"] for result in results) == 1
        assert next(result for result in results if result["error"])["value"]["code"] == "OPERATION_ID_CONFLICT"
    else:
        assert not any(result["error"] for result in results)
        assert results[0]["value"]["task_id"] == results[1]["value"]["task_id"]


def test_same_authorization_real_t6_race_and_reuse(tmp_path: Path) -> None:
    example = import_module("examples.v4.application")
    app = app_at(tmp_path)
    root = app.task("T6 race")
    app.complete(root)
    attempt = app.project.inspect_state(task_id=root)["current_attempt_id"]
    review = app.review(root, "reopen", "approved", attempt_id=attempt)
    auth = app.authorization(root, "done", "active", refs=[review])
    request = dict(task_id=root, review_ref=review, authorization_ref=auth, profile_ref=example.PROFILE, actor="ME")
    results = _simultaneous(tmp_path, [("reopen_task", request), ("reopen_task", request)])
    assert not any(result.is_error for result in results)
    assert sum(result.structured_content.get("existing", False) for result in results) == 1
    fields = app.project.read_task(task_id=root)
    assert len([event for event in fields["transitions"] if event.get("authorization_ref") == auth]) == 1
    before = facts(tmp_path)
    reused = call(trusted(tmp_path), "archive_task", dict(task_id=root, authorization_ref=auth,
                  profile_ref=example.PROFILE, actor="ME"))
    assert reused.is_error and reused.structured_content["code"] == "AUTHORIZATION_REUSED"
    assert facts(tmp_path) == before
