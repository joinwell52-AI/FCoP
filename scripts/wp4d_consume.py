"""Consume the first verified set outside checkout; never rebuild from source."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path

from wp4d_candidate_ref import candidate_ref

NAMES = ["fcop-4.0.0rc1-py3-none-any.whl", "fcop-4.0.0rc1.tar.gz",
         "fcop_mcp-4.0.0rc1-py3-none-any.whl", "fcop_mcp-4.0.0rc1.tar.gz"]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(command, **kwargs):
    subprocess.run(command, check=True, **kwargs)


def execute(command, log, *, cwd, env, timeout=600):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                            text=True, encoding="utf-8", timeout=timeout)
    log.write_text(result.stdout + "\nSTDERR\n" + result.stderr, encoding="utf-8")
    assert result.returncode == 0, (result.returncode, str(log), result.stdout[-4000:], result.stderr[-4000:])
    lines = [line for line in result.stdout.splitlines() if line.startswith("{")]
    return json.loads(lines[-1]) if lines else {}


def python_reopen(python, app, directory, logdir, env, *, source=False):
    command = [str(python), *(["-B"] if source else ["-I", "-B"]), str(app)]
    error_log = (logdir / "python-hold.stderr").open("wb")
    proc = subprocess.Popen([*command, "hold", str(directory), *(["--source"] if source else [])],
                            cwd=app.parent, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=error_log, text=True, encoding="utf-8")
    lines = queue.Queue()
    def read():
        for line in proc.stdout:
            lines.put(line)
        lines.put(None)
    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    try:
        while True:
            line = lines.get(timeout=600)
            assert line is not None, "Preparation exited; inspect python-hold.stderr"
            if line.strip() == "COMMITTED":
                break
        proc.kill()
        proc.wait(timeout=30)
        assert proc.returncode != 0
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=30)
        reader.join(timeout=10)
        error_log.close()
    assert not reader.is_alive()
    return execute([*command, "inspect", str(directory), *(["--source"] if source else [])],
                   logdir / "python-inspect.log", cwd=app.parent, env=env)


def verify_set(directory, manifest_name, manifest_sha):
    path = directory / manifest_name
    assert sha(path.read_bytes()) == manifest_sha
    document = json.loads(path.read_bytes())
    records = document["files"]
    assert len(records) == len({r["filename"] for r in records})
    assert {p.name for p in directory.iterdir()} == {r["filename"] for r in records} | {manifest_name}
    for row in records:
        assert Path(row["filename"]).name == row["filename"]
        raw = (directory / row["filename"]).read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"], row["filename"]
    return document


def mismatch(python, wheel, package, work, logs, env):
    run([str(python), "-m", "pip", "install", "--no-cache-dir", "--no-deps", "--force-reinstall", str(wheel)], env=env)
    root = work / ("mismatch-" + package)
    root.mkdir()
    before = list(root.rglob("*"))
    code = (
        "import sys; from importlib.metadata import version; "
        "print(version('fcop'), version('fcop-mcp')); "
        "from fcop_mcp.server import create_server; create_server(sys.argv[1])"
    )
    result = subprocess.run([str(python), "-I", "-B", "-c", code, str(root)],
                            cwd=work, env={**env, "FCOP_PROJECT_DIR": str(root)},
                            capture_output=True, text=True, encoding="utf-8", timeout=60)
    (logs / (package + "-mismatch.log")).write_text(result.stdout + result.stderr, encoding="utf-8")
    assert result.returncode != 0 and "toolkit:MCP_PACKAGE_INCOMPATIBLE" in result.stderr
    assert list(root.rglob("*")) == before
    assert "3.2.5" in result.stdout and "4.0.0rc1" in result.stdout
    return dict(pair=result.stdout.strip(), zero_workspace_effects=True,
                diagnostic="toolkit:MCP_PACKAGE_INCOMPATIBLE")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", type=Path)
    parser.add_argument("candidate_manifest_sha256")
    parser.add_argument("legacy", type=Path)
    parser.add_argument("historical_manifest_sha256")
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    repo = Path.cwd().resolve()
    artifacts, legacy = args.artifacts.resolve(), args.legacy.resolve()
    manifest = verify_set(artifacts, "candidate-manifest.json", args.candidate_manifest_sha256)
    assert sorted(r["filename"] for r in manifest["files"]) == sorted(NAMES)
    assert manifest["raw_reproducibility"] == "4/4"
    assert manifest["repository"] == "joinwell52-AI/FCoP"
    execution_head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    assert manifest["commit"] == candidate_ref(repo)
    assert manifest["execution_head"] == execution_head
    historical = verify_set(legacy, "historical-manifest.json", args.historical_manifest_sha256)
    assert historical["commit"] == "167c5fd4ca4c9603c392bae3a4a055963e7b7ed6"
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH" and not k.startswith("FCOP_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = datetime.now(timezone.utc).isoformat()
    results = []
    for origin in ("wheel", "sdist"):
        # Keep test work and logs for evidence; directory is never inside checkout.
        work = Path(tempfile.mkdtemp(prefix="wp4d-" + origin + "-"))
        assert not work.is_relative_to(repo)
        venv, applications = work / "venv", work / "applications"
        shutil.copytree(repo / "examples/v4/third-party", applications)
        shutil.copyfile(repo / "tests/rc/installed_identity.py", work / "installed_identity.py")
        shutil.copyfile(repo / "tests/rc/legacy_fixture.py", work / "legacy_fixture.py")
        logs = evidence / origin
        logs.mkdir()
        run([sys.executable, "-m", "venv", str(venv)], env=env)
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run([str(python), "-m", "pip", "install", "--upgrade", "pip", "hatchling==1.32.0"], env=env)
        pair = NAMES[::2] if origin == "wheel" else NAMES[1::2]
        run([str(python), "-m", "pip", "install", "--no-cache-dir", "--no-build-isolation",
             *[str(artifacts / name) for name in pair]], env=env, cwd=work)
        identity = execute([str(python), "-I", "-B", str(work / "installed_identity.py")],
                           logs / "identity.log", cwd=work, env=env)
        adoption = python_reopen(python, applications / "python-only/app.py",
                                work / "python-project", logs, env)
        try:
            mcp = execute([str(python), "-I", "-B", str(applications / "mcp-only/client.py"),
                           str(work / "mcp-project")], logs / "mcp.log", cwd=work, env=env)
        finally:
            for server_log in (work / "mcp-project").glob("server-*.log"):
                shutil.copyfile(server_log, logs / server_log.name)
        legacy_read = execute([str(python), "-I", "-B", str(work / "legacy_fixture.py"), "read",
                               str(work / "legacy-workspace"), str(legacy / "workspace.json")],
                              logs / "legacy.log", cwd=work, env=env)
        negative = []
        for package, old_wheel, restore in (
            ("core", "fcop-3.2.5-py3-none-any.whl", pair[0]),
            ("mcp", "fcop_mcp-3.2.5-py3-none-any.whl", pair[1]),
        ):
            negative.append(mismatch(python, legacy / old_wheel, package, work, logs, env))
            run([str(python), "-m", "pip", "install", "--no-deps", "--force-reinstall",
                 "--no-build-isolation", str(artifacts / restore)], env=env)
        execute([str(python), "-I", "-B", str(work / "installed_identity.py")],
                logs / "restored-identity.log", cwd=work, env=env)
        results.append(dict(origin=origin, identity=identity, python=adoption, mcp=mcp,
                            legacy=legacy_read, mismatches=negative))
    final = dict(schema="wp4d-consumer/v1", os=platform.system(), python=platform.python_version(),
                 candidate_commit=manifest["commit"], execution_head=execution_head, started=started,
                 finished=datetime.now(timezone.utc).isoformat(),
                 candidate_manifest_sha256=args.candidate_manifest_sha256,
                 artifact_sha256={r["filename"]: r["sha256"] for r in manifest["files"]},
                 results=results, status="PASS")
    (evidence / "result.json").write_text(json.dumps(final, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(final, sort_keys=True))


if __name__ == "__main__":
    main()
