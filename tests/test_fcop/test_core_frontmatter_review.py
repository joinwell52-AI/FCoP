"""tests/test_fcop/test_core_frontmatter_review.py —— REVIEW frontmatter
parser/serializer 单元测试。

按 TASK-20260509-004 §A6。
"""

from __future__ import annotations

import pytest

from fcop.core.frontmatter import (
    assemble_review_file,
    parse_review_frontmatter,
    serialize_review_frontmatter,
)
from fcop.errors import ProtocolViolation

_LEGAL = """---
protocol: fcop
version: 1
type: REVIEW
review_id: REVIEW-20260601-001-ADMIN-on-task-001
subject_type: task
subject_ref: fcop/tasks/TASK-20260601-001-PM-to-DEV.md
reviewer_role: ADMIN
decision: approved
decided_at: 2026-06-01T10:00:00
---

REVIEW body markdown 在这里。
"""


def test_parse_legal():
    fm, body = parse_review_frontmatter(_LEGAL)
    assert fm["type"] == "REVIEW"
    assert fm["decision"] == "approved"
    assert fm["reviewer_role"] == "ADMIN"
    assert "REVIEW body" in body


def test_parse_injects_type_when_missing():
    txt = _LEGAL.replace("type: REVIEW\n", "")
    fm, _ = parse_review_frontmatter(txt)
    assert fm["type"] == "REVIEW"


def test_parse_protocol_alias_normalized():
    """0.7.x 别名（agent_bridge）应被 normalize_protocol_name 接受。"""
    txt = _LEGAL.replace("protocol: fcop", "protocol: agent_bridge")
    fm, _ = parse_review_frontmatter(txt)
    assert fm["protocol"] == "fcop"


def test_parse_missing_protocol_rejected():
    txt = _LEGAL.replace("protocol: fcop\n", "")
    with pytest.raises(ProtocolViolation, match="protocol"):
        parse_review_frontmatter(txt)


def test_parse_missing_version_rejected():
    txt = _LEGAL.replace("version: 1\n", "")
    with pytest.raises(ProtocolViolation, match="version"):
        parse_review_frontmatter(txt)


def test_parse_unknown_protocol_rejected():
    txt = _LEGAL.replace("protocol: fcop", "protocol: not_fcop")
    with pytest.raises(ProtocolViolation, match="protocol"):
        parse_review_frontmatter(txt)


class TestSerialize:
    def test_field_order_deterministic(self):
        fm = {
            "decided_at": "2026-06-01T10:00:00",
            "reviewer_role": "ADMIN",
            "subject_type": "task",
            "decision": "approved",
            "subject_ref": "x",
            "review_id": "REVIEW-20260601-001-ADMIN-on-x",
            "type": "REVIEW",
            "version": 1,
            "protocol": "fcop",
        }
        out = serialize_review_frontmatter(fm)
        # protocol 必须在第一行
        first_line = out.splitlines()[1]
        assert first_line.startswith("protocol:")
        # decision 必须在 decided_at 之前
        assert out.index("decision:") < out.index("decided_at:")

    def test_unknown_keys_appended_alphabetically(self):
        fm = {
            "protocol": "fcop",
            "version": 1,
            "type": "REVIEW",
            "review_id": "REVIEW-20260601-001-ADMIN-on-x",
            "subject_type": "task",
            "subject_ref": "x",
            "reviewer_role": "ADMIN",
            "decision": "approved",
            "decided_at": "2026-06-01T10:00:00",
            "z_extra": "z",
            "a_extra": "a",
        }
        out = serialize_review_frontmatter(fm)
        assert out.index("a_extra:") < out.index("z_extra:")

    def test_skips_none_values(self):
        fm = {
            "protocol": "fcop",
            "version": 1,
            "type": "REVIEW",
            "review_id": "x",
            "subject_type": "task",
            "subject_ref": "y",
            "reviewer_role": "ADMIN",
            "decision": "approved",
            "decided_at": "2026-06-01T10:00:00",
            "rationale": None,
        }
        out = serialize_review_frontmatter(fm)
        assert "rationale:" not in out


def test_assemble_round_trip():
    fm, body = parse_review_frontmatter(_LEGAL)
    text = assemble_review_file(fm, body)
    fm2, body2 = parse_review_frontmatter(text)
    assert fm2["decision"] == fm["decision"]
    assert fm2["reviewer_role"] == fm["reviewer_role"]
    assert body2.strip() == body.strip()


def test_assemble_empty_body():
    fm = {
        "protocol": "fcop",
        "version": 1,
        "type": "REVIEW",
        "review_id": "REVIEW-20260601-001-ADMIN-on-x",
        "subject_type": "task",
        "subject_ref": "x",
        "reviewer_role": "ADMIN",
        "decision": "approved",
        "decided_at": "2026-06-01T10:00:00",
    }
    text = assemble_review_file(fm, "")
    assert text.endswith("---\n")
