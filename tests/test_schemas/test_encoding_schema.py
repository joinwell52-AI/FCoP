"""encoding.schema.json —— 抽象 2（Encoding）回归。

ADR-0021 + ADR-0022 / TASK-004 R1 §A3。
"""

from __future__ import annotations


def _legal_doc():
    return {
        "encoding_name": "MarkdownEncoding",
        "encoding_version": "1.0.0",
        "ipc_surface": {
            "envelope_types": ["TASK", "REPORT", "ISSUE", "REVIEW"],
            "filename_grammar": {
                "TASK": "^TASK-(\\d{8})-(\\d{3})-(\\w+)-to-(\\w+)\\.md$",
                "REPORT": "^REPORT-(\\d{8})-(\\d{3})-(\\w+)-to-(\\w+)\\.md$",
                "ISSUE": "^ISSUE-(\\d{8})-(\\d{3})-(\\w+)\\.md$",
                "REVIEW": "^REVIEW-(\\d{8})-(\\d{3})-(\\w+)-on-(\\w+)\\.md$",
            },
            "required_frontmatter_base": ["protocol", "version", "sender"],
        },
        "open_knowledge_surface": {
            "default_dir": "shared",
            "filename_grammar": "^[A-Z][A-Z0-9-]*-[a-z0-9-]+(\\.[a-z]{2,5})?\\.md$",
            "frontmatter_required": [],
        },
        "workspace_dir": {
            "default": "fcop",
            "legacy_paths": ["docs/agents"],
            "subdirs_ipc": ["tasks", "reports", "issues", "reviews"],
            "subdirs_open_knowledge": ["shared"],
            "subdirs_archive": ["log/tasks", "log/reports", "log/issues", "log/reviews"],
        },
    }


def test_legal_full_encoding(validator_for):
    """完整 encoding 抽象描述文档。"""
    v = validator_for("encoding.schema.json")
    assert list(v.iter_errors(_legal_doc())) == []


def test_envelope_types_must_be_exactly_four(validator_for):
    """ipc_surface.envelope_types 长度被锁在 4。"""
    v = validator_for("encoding.schema.json")
    doc = _legal_doc()
    doc["ipc_surface"]["envelope_types"] = ["TASK", "REPORT", "ISSUE"]  # 只 3 个
    errs = list(v.iter_errors(doc))
    assert errs, "envelope_types length != 4 must be rejected"


def test_workspace_default_must_be_fcop(validator_for):
    """workspace_dir.default const = 'fcop'（ADR-0022）。"""
    v = validator_for("encoding.schema.json")
    doc = _legal_doc()
    doc["workspace_dir"]["default"] = "docs/agents"  # 老路径不允许做新默认
    errs = list(v.iter_errors(doc))
    assert errs, "workspace_dir.default must be the literal 'fcop'"


def test_open_knowledge_default_dir_must_be_shared(validator_for):
    """open_knowledge_surface.default_dir const = 'shared'。"""
    v = validator_for("encoding.schema.json")
    doc = _legal_doc()
    doc["open_knowledge_surface"]["default_dir"] = "knowledge"
    errs = list(v.iter_errors(doc))
    assert errs, "open_knowledge_surface.default_dir must be 'shared'"


def test_missing_workspace_dir_block_rejected(validator_for):
    """workspace_dir 是必填。"""
    v = validator_for("encoding.schema.json")
    doc = _legal_doc()
    del doc["workspace_dir"]
    errs = list(v.iter_errors(doc))
    assert errs, "missing workspace_dir block must be rejected"
