"""Independent unpublished candidate identity and negative dependency guards."""
from __future__ import annotations

import hashlib
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
    # Preserve the registry identity at accepted RC commit d5e851c3fa628167999a9f8b7b7b89290e7b8f06.
    # The live manifest advances when a stable package is actually published.
    registry = (ROOT / "tests/stable/accepted-rc-registry.json").read_text(encoding="utf-8")
    assert hashlib.sha256(registry.encode("utf-8")).hexdigest() == (
        "2194638d6894dd2bb33aa73ceea1ca58f1ece24f172e700ef66396d6a8003d85"
    )
    assert "4.0.0rc1" not in registry
    assert "3.2.5" in registry
