"""Reproduce the unchanged Core initialization boundary in a disposable root.

This deliberately injects a publication failure. PASS means reproduction,
not conformance to the proposed fcop-only ownership boundary.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from fcop import Project
from fcop.errors import FcopError
from fcop.v4 import creation


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        if p.is_file() else "directory"
        for p in root.rglob("*")
    }


def main():
    root = Path(tempfile.mkdtemp(prefix="fcop-403-init-boundary-")).resolve()
    observed = {}

    def before_publication(staging, target):
        assert staging.parent == root and staging.name.startswith(".fcop-init-")
        assert target == root / "fcop" and not target.exists()
        assert (staging / "fcop.json").is_file() and (staging / "cold").is_dir()
        observed.update(staging=staging.name, target=target.name, staged=snapshot(root))
        raise OSError("intentional publication-boundary failure")

    with patch.object(creation, "publish_directory", before_publication):
        try:
            Project(root).create_workspace(protocol_version="4.0")
        except FcopError as exc:
            observed["first_error"] = exc.code
    assert observed["first_error"] == "RECOVERY_REQUIRED"
    before = snapshot(root)
    assert before == observed["staged"] and not (root / "fcop").exists()
    try:
        Project(root).create_workspace(protocol_version="4.0")
    except FcopError as exc:
        observed["retry_error"] = exc.code
    assert observed["retry_error"] == "RECOVERY_REQUIRED"
    assert snapshot(root) == before
    observed.update(
        status="REPRODUCED_NOT_ACCEPTED", temporary_root=str(root),
        initialization_source=str(Path(creation.__file__).resolve()),
        initialization_sha256=hashlib.sha256(Path(creation.__file__).read_bytes()).hexdigest(),
        retry_zero_write=True, host_instruction_files_created=False,
    )
    print(json.dumps(observed, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
