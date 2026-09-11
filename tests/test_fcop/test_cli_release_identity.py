"""ADMIN release-identity amendment: exact bytes, unchanged normative remainder."""

import hashlib
import re
from pathlib import Path

import pytest

from fcop.v4.rule_distribution._read import specification_identity

ROOT = Path(__file__).resolve().parents[2]
REVISION = "81d3229ee602341063879fe9100ab7db92417ffe"
HASHES = {
    "en": "fb10d1b14a678b77874012f88cf35a977d2f8517b1aa4a6fdc5a0e94546ef33d",
    "zh": "0dac91db3e38e0cf06423a0d815beaaad9c9b4d6ec06e732f1012aec0e346f40",
}
# Historical 8bedfd3 source after omitting ONLY the amended identity header
# and four self-reference lines. All tables, code blocks and other clauses remain.
HISTORICAL_REMAINDER = {
    "en": "a0f3ac05e04d269ec84f3d0ad448bb14ebe71135752d4019f9cdd08fed97707c",
    "zh": "6c79052cb6043ee18535cb98d5ec225f10e8d5e9d8794b578f319ac880717a44",
}
IDENTITY_CLAUSES = {"F4.0.2", "F4.11.1", "F4.11.5", "F4.12.4"}


def source(language):
    suffix = "" if language == "en" else ".zh"
    return ROOT / f"spec/fcop-4.0-spec{suffix}.md"


@pytest.mark.parametrize("language", ["en", "zh"])
def test_stable_source_and_unchanged_normative_remainder(language):
    raw = source(language).read_bytes()
    text = raw.decode("utf-8")
    assert not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == HASHES[language]
    assert "Stable · Implemented · Released" in text.splitlines()[2]
    assert "Candidate" not in text.splitlines()[0] and "候选" not in text.splitlines()[0]
    assert "4.0.0-candidate.2" in text.splitlines()[4]  # preserved historical reference
    remainder = "\n".join(
        line for line in text.splitlines()[5:]
        if not any(line.startswith(f"**{key}**") for key in IDENTITY_CLAUSES)
    )
    assert hashlib.sha256(remainder.encode()).hexdigest() == HISTORICAL_REMAINDER[language]
    # These self-reference clauses keep their original requirements, not just IDs.
    clauses = dict(re.findall(r"^\*\*(F4\.\d+\.\d+)\*\* (.*)$", text, re.M))
    if language == "en":
        assert "MUST have the same clause IDs, objects, transitions, errors, and invariants." in clauses["F4.0.2"]
        assert clauses["F4.11.1"].endswith("This specification does not authorize migration.")
        assert clauses["F4.12.4"].endswith("does not authorize Schema, tests, implementation, migration, push, or release.")
    else:
        assert "条款编号、对象、迁移、错误和不变量必须一致" in clauses["F4.0.2"]
        assert clauses["F4.11.1"].endswith("迁移不在本规范中授权。")
        assert clauses["F4.12.4"].endswith("它不授权 Schema、测试、实现、迁移、push 或发布。")


def test_stable_clause_parity_and_core_source_identity():
    ids = [re.findall(r"^\*\*(F4\.\d+\.\d+)\*\*", source(lang).read_text(encoding="utf-8"), re.M)
           for lang in ("en", "zh")]
    assert ids[0] == ids[1] and len(ids[0]) == len(set(ids[0]))
    assert specification_identity("cli-release-proof") == {
        "path": "spec/fcop-4.0-spec.md", "revision": REVISION, "sha256": HASHES["en"],
    }
