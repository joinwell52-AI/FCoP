"""tests/test_fcop/test_core_filename_review.py —— REVIEW filename 单元测试。

按 TASK-20260509-004 §A6。
"""

from __future__ import annotations

import pytest

from fcop.core.filename import (
    REVIEW_FILENAME_PREFIX,
    REVIEW_FILENAME_RE,
    REVIEW_SUBJECT_SHORT_RE,
    ReviewFilename,
    build_review_filename,
    parse_review_filename,
)


class TestParseReviewFilename:
    def test_simple(self):
        f = parse_review_filename("REVIEW-20260601-001-ADMIN-on-task-001.md")
        assert f == ReviewFilename(
            date="20260601",
            sequence=1,
            reviewer="ADMIN",
            subject_short="task-001",
        )

    def test_compound_reviewer_role(self):
        f = parse_review_filename("REVIEW-20260601-007-LEAD-QA-on-adr-0017.md")
        assert f is not None
        assert f.reviewer == "LEAD-QA"
        assert f.subject_short == "adr-0017"

    def test_review_id_concat(self):
        f = parse_review_filename("REVIEW-20260601-042-PM-on-commit-3c35e0e.md")
        assert f is not None
        assert f.review_id == "REVIEW-20260601-042-PM-on-commit-3c35e0e"

    def test_render_round_trip(self):
        original = "REVIEW-20260601-001-ADMIN-on-task-001.md"
        f = parse_review_filename(original)
        assert f is not None
        assert f.render() == original

    @pytest.mark.parametrize(
        "bad",
        [
            "REVIEW-20260601-001-ADMIN.md",  # 缺 -on-{subject}
            "REVIEW-20260601-1-ADMIN-on-task-001.md",  # 序号非 3 位
            "REVIEW-2026601-001-ADMIN-on-task-001.md",  # 日期 7 位
            "REVIEW-20260601-001-admin-on-task-001.md",  # reviewer 小写
            "REVIEW-20260601-001-ADMIN-on-Task-001.md",  # subject 大写非法
            "review-20260601-001-ADMIN-on-task-001.md",  # PREFIX 小写
        ],
    )
    def test_rejects_bad(self, bad):
        assert parse_review_filename(bad) is None


class TestBuildReviewFilename:
    def test_basic(self):
        out = build_review_filename(
            date="20260601",
            sequence=1,
            reviewer="ADMIN",
            subject_short="task-001",
        )
        assert out == "REVIEW-20260601-001-ADMIN-on-task-001.md"

    def test_round_trip(self):
        kwargs = dict(
            date="20260601",
            sequence=42,
            reviewer="LEAD-QA",
            subject_short="adr-0017",
        )
        name = build_review_filename(**kwargs)
        parsed = parse_review_filename(name)
        assert parsed is not None
        assert (parsed.date, parsed.sequence, parsed.reviewer, parsed.subject_short) == (
            "20260601",
            42,
            "LEAD-QA",
            "adr-0017",
        )

    def test_rejects_empty_subject(self):
        with pytest.raises(ValueError, match="subject_short"):
            build_review_filename(
                date="20260601", sequence=1, reviewer="ADMIN", subject_short=""
            )

    def test_rejects_uppercase_subject(self):
        with pytest.raises(ValueError, match="subject_short"):
            build_review_filename(
                date="20260601",
                sequence=1,
                reviewer="ADMIN",
                subject_short="Task-001",
            )


def test_constants_align_with_re():
    assert REVIEW_FILENAME_PREFIX == "REVIEW"
    assert REVIEW_FILENAME_RE.pattern.startswith("^REVIEW-")
    assert REVIEW_SUBJECT_SHORT_RE.fullmatch("task-001")
    assert REVIEW_SUBJECT_SHORT_RE.fullmatch("adr-0017")
    assert REVIEW_SUBJECT_SHORT_RE.fullmatch("3c35e0e")
    assert REVIEW_SUBJECT_SHORT_RE.fullmatch("Task-001") is None
    assert REVIEW_SUBJECT_SHORT_RE.fullmatch("-leading-dash") is None
