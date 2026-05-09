"""断言 ``src/fcop/_data/schemas/`` 与 ``spec/schemas/`` 字节级一致。

按 TASK-20260509-004 §决议 1 落地。

两份 schema 的存在是 build-time 工程妥协（spec/ 是协议权威，wheel
需要包内可用副本），但**协议唯一真相必须只有一份**。本测试把这条
规则上 CI ——任何 PR 改 schema 但忘 sync，CI 会立即拦下。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop.core.jsonschema_validator import BUNDLED_SCHEMA_DIR, SCHEMA_NAMES

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_SCHEMA_DIR = REPO_ROOT / "spec" / "schemas"


def test_repo_layout_assumption():
    """前置条件：能找到 spec/schemas/ —— 否则本测试无法运行。"""
    assert SPEC_SCHEMA_DIR.is_dir(), (
        f"expected spec/schemas/ at {SPEC_SCHEMA_DIR}; repo layout changed?"
    )


def test_all_schemas_present_in_both_locations():
    """7 份 schema 在 spec/ 和 _data/ 都存在。"""
    spec_files = {p.name for p in SPEC_SCHEMA_DIR.glob("*.schema.json")}
    bundled_files = {p.name for p in BUNDLED_SCHEMA_DIR.glob("*.schema.json")}
    assert set(SCHEMA_NAMES) <= spec_files, (
        f"missing in spec/: {set(SCHEMA_NAMES) - spec_files}"
    )
    assert set(SCHEMA_NAMES) <= bundled_files, (
        f"missing in _data/: {set(SCHEMA_NAMES) - bundled_files}"
    )


@pytest.mark.parametrize("name", SCHEMA_NAMES)
def test_schema_byte_identical(name: str):
    """每份 schema 在两处的字节内容必须完全一致。"""
    spec_bytes = (SPEC_SCHEMA_DIR / name).read_bytes()
    bundled_bytes = (BUNDLED_SCHEMA_DIR / name).read_bytes()
    assert spec_bytes == bundled_bytes, (
        f"{name} drifted: spec/ ≠ src/fcop/_data/schemas/. "
        f"Re-sync via: Copy-Item spec/schemas/*.schema.json "
        f"src/fcop/_data/schemas/ -Force"
    )


def test_no_extra_schemas_in_bundled_dir():
    """src/fcop/_data/schemas/ 里不应有 spec/schemas/ 没有的文件。"""
    bundled = {p.name for p in BUNDLED_SCHEMA_DIR.glob("*.schema.json")}
    spec = {p.name for p in SPEC_SCHEMA_DIR.glob("*.schema.json")}
    extra = bundled - spec
    assert not extra, f"orphan schemas in _data/: {extra}"
