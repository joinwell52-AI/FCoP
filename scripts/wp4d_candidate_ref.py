"""Resolve content identity without treating evidence-only commits as content."""
from __future__ import annotations

import subprocess
from pathlib import Path


def candidate_ref(repo: Path) -> str:
    """Skip only contiguous, single-parent WP4D evidence/Manifest commits."""
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
            name.startswith(("reports/FCOP-4.0-WP4D-", "tests/rc/evidence/wp4d/"))
            or name == "reviews/fcop-4.0/wp4d/MANIFEST.md"
            for name in names
        )
        if not evidence:
            return ref
        ref = parents[1]
