"""Independent unpublished candidate identity and negative dependency guards."""
from __future__ import annotations

from pathlib import Path

import pytest
from scripts.fcop_rc_candidate_check import check, validate_pin

from tests.stable.historical import identity_tree

ROOT = Path(__file__).resolve().parents[2]


def test_wp4d_rc_candidate_identity(tmp_path):
    assert check(identity_tree(tmp_path)) == {
        "schema": "wp4d-identity/v1", "fcop": "4.0.0rc1", "fcop-mcp": "4.0.0rc1",
        "pin": "fcop>=4.0.0rc1,<4.1.0", "candidate_pair": True,
        "stable_pair": False, "published": False,
    }


@pytest.mark.parametrize("pin", [
    "fcop>=4.0.0rc1,<5.0", "fcop>=4.0.0rc1,<4.2", "fcop>=4.0.0,<4.1.0",
    "fcop>=3.2.5,<4.1.0", "fcop>=4.0.0rc1", "fcop>=4.0.0rc2,<4.1.0",
    "fcop[dev]>=4.0.0rc1,<4.1.0", 'fcop>=4.0.0rc1,<4.1.0; python_version>"3.11"',
])
def test_wp4d_rc_pin_rejects_wide_or_wrong_lower(pin):
    with pytest.raises(ValueError):
        validate_pin(pin, "4.0.0rc1", "4.0.0rc1")


def test_wp4d_rc_pin_accepts_prerelease_lower_and_excludes_next_minor():
    assert validate_pin("fcop>=4.0.0rc1,<4.1.0", "4.0.0rc1", "4.0.0rc1") == {
        "lower": "4.0.0rc1", "upper_exclusive": "4.1.0", "same_major_minor": True,
    }


def test_wp4d_rc_pin_rejects_major_only_alignment():
    with pytest.raises(ValueError, match="MCP_PIN_MAJOR_MINOR_MISMATCH"):
        validate_pin("fcop>=4.0.0rc1,<4.2.0", "4.0.0rc1", "4.1.0rc1")


def test_wp4d_rc_existing_registry_identity_is_not_relabelled():
    registry = (ROOT / "mcp/server.json").read_text(encoding="utf-8")
    assert "4.0.0rc1" not in registry
