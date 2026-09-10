"""Candidate identity only ignores a contiguous evidence-only commit suffix."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize(("changed", "evidence_only"), [
    ("reports/FCOP-4.0-WP4D-RESULT.md", True),
    ("tests/rc/evidence/wp4d/result.json", True),
    ("reviews/fcop-4.0/wp4d/MANIFEST.md", True),
    ("src/fcop/example.py", False),
    ("examples/v4/third-party/mcp-only/server.py", False),
    ("tests/test_fcop_mcp/test_wp4d_rc_offline_guard.py", False),
])
def test_wp4d_rc_candidate_ref_preserves_content_identity(
    tmp_path: Path, changed: str, evidence_only: bool,
) -> None:
    script = Path(__file__).resolve().parents[2] / "scripts/wp4d_candidate_ref.py"
    spec = importlib.util.spec_from_file_location("wp4d_candidate_ref_under_test", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def git(*args: str) -> str:
        return subprocess.check_output([
            "git", "-C", str(tmp_path), "-c", "user.name=WP4D test",
            "-c", "user.email=wp4d@example.invalid", "-c", "core.autocrlf=false",
            *args,
        ], text=True).strip()

    git("init", "-q")
    (tmp_path / "initial.txt").write_text("initial\n", encoding="utf-8")
    git("add", "initial.txt")
    git("commit", "-qm", "initial")
    (tmp_path / "content.txt").write_text("candidate\n", encoding="utf-8")
    git("add", "content.txt")
    git("commit", "-qm", "candidate")
    content = git("rev-parse", "HEAD")
    path = tmp_path / changed
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("new\n", encoding="utf-8")
    git("add", changed)
    git("commit", "-qm", "next")
    head = git("rev-parse", "HEAD")
    assert module.candidate_ref(tmp_path) == (content if evidence_only else head)
