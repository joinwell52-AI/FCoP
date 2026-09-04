"""Private Root-family short-lock identities for FCoP 4.0."""

from __future__ import annotations

import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from fcop.v4.encoding import canonical, digest, operation_lock


def family_key(workspace_id: str, root_task_id: str) -> str:
    return digest(
        canonical(
            {
                "contract": "fcop-family-lock-v1",
                "root_task_id": root_task_id,
                "workspace_id": workspace_id,
            }
        )
    )


@contextmanager
def family_boundary(root: Path, workspace_id: str, root_task_id: str) -> Iterator[None]:
    """Hold exactly one deterministic family lock for a short file commit."""
    # Kernel coordination is deliberately outside the workspace fact tree:
    # failed validation must not mutate protocol evidence, and operation receipt
    # counts must not include locks. The full workspace/family digest is the
    # cross-process identity; the retained inode is never removed by age.
    directory = Path(tempfile.gettempdir()) / "fcop-v4-family-locks"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock = directory / f"family-{family_key(workspace_id, root_task_id)}.lock"
    with operation_lock(lock):
        yield
