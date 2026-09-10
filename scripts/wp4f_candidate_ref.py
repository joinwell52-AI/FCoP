"""Resolve content identity without treating evidence-only commits as content."""
from __future__ import annotations

import subprocess
from pathlib import Path


def candidate_ref(repo: Path, stage: str = "WP4F") -> str:
    """Skip only contiguous, single-parent WP4F evidence/Manifest commits."""
    assert stage in {"WP4F"}
    ref = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    while True:
        parents = subprocess.check_output(
            ["git", "-C", str(repo), "rev-list", "--parents", "-n", "1", ref], text=True,
        ).split()
        assert len(parents) == 2, "Candidate delivery requires an unambiguous parent chain"
        names = subprocess.check_output(
            ["git", "-C", str(repo), "diff", "--name-only", parents[1], ref], text=True,
        ).splitlines()
        evidence = bool(names) and all(
            name.startswith((f"reports/FCOP-4.0-{stage}-", f"tests/rc/evidence/{stage.lower()}/"))
            or name == f"reviews/fcop-4.0/{stage.lower()}/MANIFEST.md"
            for name in names
        )
        if not evidence:
            return ref
        ref = parents[1]
