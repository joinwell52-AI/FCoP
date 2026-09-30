"""Protocol audit reuses the sole workspace validator."""
from pathlib import Path
from typing import Any

from fcop.workspace import validate_workspace


def audit(root: Path | str) -> dict[str, Any]:
    return validate_workspace(root)
