"""Optional explicit Profile metadata. Never installs authority or changes Base semantics."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def list_profiles() -> list[dict[str, str]]:
    """Installed bundled team presets are discoverable only on explicit request."""
    from fcop.teams import get_available_teams
    return [{"id": t.name, "source": "bundled-team-profile"} for t in get_available_teams()]


def load_profile(reference: str) -> dict[str, Any]:
    path = Path(reference)
    if path.is_file():
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or not isinstance(value.get("id"), str) or not value["id"].strip():
            raise ValueError("Profile requires a nonempty string id")
        if set(value) - {"id", "description", "roles"}:
            raise ValueError("Unsupported profile metadata field")
        if "roles" in value and (not isinstance(value["roles"], list) or not all(isinstance(r, str) and r for r in value["roles"])):
            raise ValueError("Profile roles must be nonempty strings")
        return value
    for value in list_profiles():
        if value["id"] == reference:
            return value
    raise ValueError(f"Profile not found: {reference}")
