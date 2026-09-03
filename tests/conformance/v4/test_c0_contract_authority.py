"""Static authority and bilingual parity checks for the frozen contract."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC_EN = ROOT / "spec" / "fcop-4.0-spec.md"
SPEC_ZH = ROOT / "spec" / "fcop-4.0-spec.zh.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _clauses(text: str) -> set[str]:
    return set(re.findall(r"\bF4\.\d+\.\d+\b", text))


def _base_errors(text: str) -> set[str]:
    section = text.split("F4.10.1", 1)[1].split("F4.10.2", 1)[0]
    return set(re.findall(r"`([A-Z][A-Z0-9_]+)`", section))


def test_c0_parity_01() -> None:
    """C0-PARITY-01 · F4.0.2."""
    # Arrange: frozen English and Chinese candidate bytes.
    en = _text(SPEC_EN)
    zh = _text(SPEC_ZH)
    # Act: independently extract clause and named contract sets.
    en_clauses, zh_clauses = _clauses(en), _clauses(zh)
    # Assert: exact bilingual authority parity.
    assert en_clauses == zh_clauses
    for token in [*(f"C{i}" for i in range(1, 9)), *(f"T{i}" for i in range(1, 8))]:
        assert token in en and token in zh


def test_c0_auth_01() -> None:
    """C0-AUTH-01 · F4.0.3/F4.12.3."""
    # Arrange: frozen primary authority text.
    en = _text(SPEC_EN)
    # Act: select the three authority/release obligations.
    obligations = [
        "JSON Schema has machine authority only for structure",
        "governs lifecycle, authorization, concurrency, and recovery behavior",
        "Conflict among Schema, specification, and tests blocks release",
    ]
    # Assert: Schema cannot override behavior and conflict blocks release.
    assert all(item in en for item in obligations)


def test_c0_error_registry_01() -> None:
    """C0-ERROR-REGISTRY-01 · F4.10.1-F4.10.3."""
    # Arrange/Act: extract only the normative F4.10.1 registries.
    en_errors = _base_errors(_text(SPEC_EN))
    zh_errors = _base_errors(_text(SPEC_ZH))
    # Assert: exact 31-code parity and no test-only code leakage.
    assert en_errors == zh_errors
    assert len(en_errors) == 31
    assert "V4_NOT_IMPLEMENTED" not in en_errors
