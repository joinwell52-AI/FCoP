"""I5（v1.x 内向后兼容）见证测试。

按 TASK-20260509-004 §A4。

扫 ``docs/agents/log/`` 下所有真实 agent 产出的 0.7.x 文件，逐一过新
schema。任何一份挂掉，说明 schema 写错了 —— 因为 ADR-0003 + ADR-0015
明确禁止 v1.0 break 0.7.x。

field-mapping 规则（与 spec/schemas/README.md §validating-by-hand 一致）：
- 缺 ``type`` 字段 → 按文件名 PREFIX 注入
- 缺 ``sender`` 但有 ``from`` → mapping
- 缺 ``recipient`` 但有 ``to`` → mapping
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from fcop.core.jsonschema_validator import validate_envelope_frontmatter

REPO_ROOT = Path(__file__).resolve().parents[2]
# The legacy docs/agents/ layout was used in 0.7.x; the repo itself has been
# migrated to fcop/ (ADR-0022). When the log dir is absent we skip gracefully
# rather than scanning fcop/log/ which contains newer files, not 0.7.x ones.
LOG_DIR = REPO_ROOT / "docs" / "agents" / "log"

PREFIX_TO_TYPE = {
    "TASK": "TASK",
    "REPORT": "REPORT",
    "ISSUE": "ISSUE",
    "REVIEW": "REVIEW",
}


def _legacy_envelope_files() -> list[Path]:
    """收集 docs/agents/log/{tasks,reports,issues,reviews}/ 下所有
    符合 envelope 文件名 PREFIX 的 .md 文件。"""
    if not LOG_DIR.is_dir():
        return []
    out: list[Path] = []
    for sub in ("tasks", "reports", "issues", "reviews"):
        d = LOG_DIR / sub
        if d.is_dir():
            out.extend(p for p in d.glob("*.md") if p.is_file())
    return sorted(out)


def _split_frontmatter(text: str) -> dict | None:
    """返回 frontmatter dict 或 None（文件没有 frontmatter）。"""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def _detect_envelope_type(path: Path) -> str | None:
    prefix = path.name.split("-", 1)[0].upper()
    return PREFIX_TO_TYPE.get(prefix)


LEGACY_FILES = _legacy_envelope_files()


def test_we_actually_found_some_legacy_files():
    """前置条件：至少有几份历史文件 —— 否则本测试白跑。

    docs/agents/log/ 是 0.7.x 时代的 workspace 路径；v1.0 起迁移至 fcop/
    （ADR-0022）。迁移后该目录不再存在，本检查相应跳过。
    """
    if not LOG_DIR.is_dir():
        pytest.skip(
            f"{LOG_DIR} does not exist — project has been migrated to fcop/ layout "
            "(ADR-0022). No 0.7.x legacy files to validate."
        )
    assert len(LEGACY_FILES) >= 5, (
        f"expected ≥5 legacy envelope files under {LOG_DIR}, found {len(LEGACY_FILES)}"
    )


@pytest.mark.parametrize("path", LEGACY_FILES, ids=lambda p: p.name)
def test_legacy_envelope_validates(path: Path):
    text = path.read_text(encoding="utf-8")
    fm = _split_frontmatter(text)
    assert fm is not None, f"no frontmatter in {path}"

    envelope_type = _detect_envelope_type(path)
    assert envelope_type is not None, f"unknown PREFIX in {path.name}"

    # legacy field-mapping
    if "sender" not in fm and "from" in fm:
        fm["sender"] = fm["from"]
    if "recipient" not in fm and "to" in fm:
        fm["recipient"] = fm["to"]
    # 0.7.x / rc-era files use fcop_version instead of protocol+version
    if "protocol" not in fm and "fcop_version" in fm:
        fm["protocol"] = "fcop"
    if "version" not in fm and "fcop_version" in fm:
        fm["version"] = "1.0.0"

    issues = validate_envelope_frontmatter(fm, envelope_type)
    assert issues == [], (
        f"{path.name} fails new v1.0 schema (this is an I5 violation):\n  "
        + "\n  ".join(f"- {i.field}: {i.message[:160]}" for i in issues)
    )
