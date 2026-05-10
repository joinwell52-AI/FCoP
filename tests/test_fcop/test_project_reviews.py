"""tests/test_fcop/test_project_reviews.py —— Project.write_review /
read_review / list_reviews / archive_review 端到端测试。

按 TASK-20260509-004 §A7 + §A8。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import (
    Project,
    Review,
    ReviewDecision,
    ReviewSubjectType,
    ValidationError,
)


@pytest.fixture()
def project(tmp_project: Path) -> Project:
    proj = Project(tmp_project)
    proj.init_solo(role_code="ME")
    return proj


def _write_minimal(project: Project, **overrides) -> Review:
    """缩短 boilerplate：default 一个合法 approved review，被 overrides 覆盖。"""
    kwargs = dict(
        reviewer_role="ADMIN",
        subject_type="task",
        subject_ref="fcop/tasks/TASK-20260601-001-PM-to-DEV.md",
        decision="approved",
    )
    kwargs.update(overrides)
    return project.write_review(**kwargs)


class TestWriteReview:
    def test_creates_reviews_dir_lazy(self, project):
        assert not project.reviews_dir.exists()
        _write_minimal(project)
        assert project.reviews_dir.is_dir()

    def test_returns_review_with_correct_fields(self, project):
        r = _write_minimal(
            project,
            reviewer_role="ADMIN",
            decision="approved",
            rationale="looks good",
        )
        assert isinstance(r, Review)
        assert r.is_archived is False
        assert r.reviewer_role == "ADMIN"
        assert r.decision is ReviewDecision.APPROVED
        assert r.subject_type is ReviewSubjectType.TASK
        assert r.rationale == "looks good"
        assert r.required_changes == ()
        assert r.path.is_file()
        assert r.path.parent == project.reviews_dir

    def test_filename_grammar(self, project):
        r = _write_minimal(project, date="20260601")
        assert r.filename.startswith("REVIEW-20260601-001-ADMIN-on-")
        assert r.filename.endswith(".md")

    def test_subject_short_derived(self, project):
        r = _write_minimal(
            project,
            subject_ref="fcop/tasks/TASK-20260601-001-PM-to-DEV.md",
            date="20260601",
        )
        # 应 derive 出 task-20260601-001-pm-to-dev
        assert "task-20260601-001-pm-to-dev" in r.filename

    def test_explicit_subject_short_overrides(self, project):
        r = _write_minimal(
            project,
            subject_ref="some/long/path.md",
            subject_short="my-slug",
            date="20260601",
        )
        assert r.filename == "REVIEW-20260601-001-ADMIN-on-my-slug.md"

    def test_sequence_increments(self, project):
        r1 = _write_minimal(project, date="20260601", subject_short="task-1")
        r2 = _write_minimal(project, date="20260601", subject_short="task-2")
        assert r1.sequence == 1
        assert r2.sequence == 2

    def test_accepts_enum_or_string(self, project):
        r1 = _write_minimal(
            project, decision=ReviewDecision.APPROVED, subject_short="t-1"
        )
        r2 = _write_minimal(project, decision="approved", subject_short="t-2")
        assert r1.decision is r2.decision is ReviewDecision.APPROVED

    def test_needs_changes_with_items_ok(self, project):
        r = _write_minimal(
            project,
            decision="needs_changes",
            required_changes=("加测试", "改 README"),
        )
        assert r.decision is ReviewDecision.NEEDS_CHANGES
        assert r.required_changes == ("加测试", "改 README")


class TestWriteReviewValidation:
    """A8：v1.0 enforcement guards。"""

    def test_needs_changes_empty_list_rejected(self, project):
        with pytest.raises(ValidationError, match="required_changes"):
            _write_minimal(
                project, decision="needs_changes", required_changes=()
            )

    def test_needs_changes_blank_strings_rejected(self, project):
        """全空白字符串清洗后等同于空列表，仍拒。"""
        with pytest.raises(ValidationError, match="required_changes"):
            _write_minimal(
                project,
                decision="needs_changes",
                required_changes=("   ", "", "\t"),
            )

    def test_needs_human_accepted(self, project):
        """v1.1 新增：needs_human 现在是合法的 decision 值（per ADR-0025）。"""
        r = _write_minimal(project, decision="needs_human")
        from fcop import ReviewDecision
        assert r.decision == ReviewDecision.NEEDS_HUMAN

    def test_unknown_decision_rejected(self, project):
        with pytest.raises(ValidationError, match="decision"):
            _write_minimal(project, decision="maybe")

    def test_unknown_subject_type_rejected(self, project):
        with pytest.raises(ValidationError, match="subject_type"):
            _write_minimal(project, subject_type="vibes")

    def test_invalid_reviewer_role_rejected(self, project):
        with pytest.raises(ValidationError, match="reviewer_role"):
            _write_minimal(project, reviewer_role="lower-case")

    def test_empty_subject_ref_rejected(self, project):
        with pytest.raises(ValueError, match="subject_ref"):
            _write_minimal(project, subject_ref="")


class TestReadReview:
    def test_by_filename(self, project):
        r = _write_minimal(project)
        loaded = project.read_review(r.filename)
        assert loaded.review_id == r.review_id
        assert loaded.decision is r.decision

    def test_by_review_id_stem(self, project):
        r = _write_minimal(project)
        loaded = project.read_review(r.review_id)
        assert loaded.path == r.path

    def test_not_found(self, project):
        from fcop.errors import TaskNotFoundError

        with pytest.raises(TaskNotFoundError):
            project.read_review("REVIEW-20990101-999-NOPE-on-nope.md")


class TestListReviews:
    def test_empty(self, project):
        assert project.list_reviews() == []

    def test_open_only_default(self, project):
        r1 = _write_minimal(project, subject_short="t-1")
        r2 = _write_minimal(project, subject_short="t-2")
        all_open = project.list_reviews()
        ids = {r.review_id for r in all_open}
        assert ids == {r1.review_id, r2.review_id}

    def test_filter_by_decision(self, project):
        _write_minimal(project, decision="approved", subject_short="a")
        _write_minimal(
            project,
            decision="needs_changes",
            required_changes=("x",),
            subject_short="b",
        )
        approved = project.list_reviews(decision="approved")
        assert len(approved) == 1
        assert approved[0].decision is ReviewDecision.APPROVED

    def test_filter_by_reviewer(self, project):
        _write_minimal(project, reviewer_role="ADMIN", subject_short="a")
        _write_minimal(project, reviewer_role="ME", subject_short="b")
        admin_only = project.list_reviews(reviewer_role="ADMIN")
        assert len(admin_only) == 1
        assert admin_only[0].reviewer_role == "ADMIN"

    def test_sort_newest_first(self, project):
        _write_minimal(project, date="20260601", subject_short="a")
        _write_minimal(project, date="20260603", subject_short="b")
        _write_minimal(project, date="20260602", subject_short="c")
        rs = project.list_reviews()
        dates = [r.date for r in rs]
        assert dates == sorted(dates, reverse=True)


class TestArchiveReview:
    def test_moves_to_log(self, project):
        r = _write_minimal(project)
        archived = project.archive_review(r.filename)
        assert archived.is_archived is True
        assert archived.path.parent == project.log_dir / "reviews"
        assert not r.path.exists(), "原文件应已被 move 走"

    def test_idempotent(self, project):
        r = _write_minimal(project)
        a1 = project.archive_review(r.filename)
        a2 = project.archive_review(a1.filename)
        assert a1.path == a2.path

    def test_list_archived(self, project):
        r = _write_minimal(project)
        project.archive_review(r.filename)
        assert project.list_reviews(status="open") == []
        archived = project.list_reviews(status="archived")
        assert len(archived) == 1
        assert archived[0].review_id == r.review_id
        all_ = project.list_reviews(status="all")
        assert len(all_) == 1
