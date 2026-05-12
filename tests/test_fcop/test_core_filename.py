"""Tests for :mod:`fcop.core.filename`.

Covers grammar (regex), parsing, building, round-trip, validators, and
the sequence allocator. All pure — no tmp files.
"""

from __future__ import annotations

import re

import pytest

from fcop.core import filename as fn
from fcop.core import schema
from fcop.models import ValidationIssue

# ── Grammar / regex sanity ───────────────────────────────────────────


class TestRegexSanity:
    def test_task_re_is_anchored(self) -> None:
        assert fn.TASK_FILENAME_RE.pattern.startswith("^")
        assert fn.TASK_FILENAME_RE.pattern.endswith("$")

    def test_report_re_is_anchored(self) -> None:
        assert fn.REPORT_FILENAME_RE.pattern.startswith("^")
        assert fn.REPORT_FILENAME_RE.pattern.endswith("$")

    def test_issue_re_is_anchored(self) -> None:
        assert fn.ISSUE_FILENAME_RE.pattern.startswith("^")
        assert fn.ISSUE_FILENAME_RE.pattern.endswith("$")

    def test_role_subpattern_matches_schema_grammar(self) -> None:
        # If the schema regex changes, this test fails — forcing the
        # filename grammar to be updated in lockstep.
        role_re = re.compile(r"^[A-Z][A-Z0-9_]*(-[A-Z0-9_]+)*$")
        for legal in ("PM", "LEAD-QA", "AUTO-TESTER", "PM_01"):
            assert role_re.fullmatch(legal) is not None
            assert schema.ROLE_CODE_RE.fullmatch(legal) is not None


# ── TASK filename ────────────────────────────────────────────────────


class TestParseTaskFilename:
    @pytest.mark.parametrize(
        "name,expected_sender,expected_recipient,expected_slot",
        [
            ("TASK-20260423-001-PM-to-DEV.md", "PM", "DEV", None),
            ("TASK-20260423-017-ADMIN-to-PM.md", "ADMIN", "PM", None),
            ("TASK-20260423-042-LEAD-QA-to-AUTO-TESTER.md", "LEAD-QA", "AUTO-TESTER", None),
            ("TASK-20260423-100-PM-to-DEV.BACKEND.md", "PM", "DEV", "BACKEND"),
            ("TASK-20260423-999-SYSTEM-to-PM.md", "SYSTEM", "PM", None),
        ],
    )
    def test_valid_names(
        self,
        name: str,
        expected_sender: str,
        expected_recipient: str,
        expected_slot: str | None,
    ) -> None:
        result = fn.parse_task_filename(name)
        assert result is not None
        assert result.sender == expected_sender
        assert result.recipient == expected_recipient
        assert result.slot == expected_slot

    def test_sequence_returned_as_int(self) -> None:
        result = fn.parse_task_filename("TASK-20260423-017-PM-to-DEV.md")
        assert result is not None
        assert result.sequence == 17
        assert isinstance(result.sequence, int)

    def test_date_kept_as_string(self) -> None:
        result = fn.parse_task_filename("TASK-20260423-001-PM-to-DEV.md")
        assert result is not None
        assert result.date == "20260423"

    def test_task_id_property(self) -> None:
        result = fn.parse_task_filename("TASK-20260423-017-PM-to-DEV.md")
        assert result is not None
        assert result.task_id == "TASK-20260423-017"

    @pytest.mark.parametrize(
        "bad",
        [
            "",
            "TASK-20260423-1-PM-to-DEV.md",  # sequence not 3 digits
            "TASK-20260423-0001-PM-to-DEV.md",  # sequence 4 digits
            "task-20260423-001-PM-to-DEV.md",  # lowercase prefix
            "TASK-20260423-001-pm-to-DEV.md",  # lowercase sender
            "TASK-20260423-001-PM-to-dev.md",  # lowercase recipient
            "TASK-2026-04-23-001-PM-to-DEV.md",  # dashed date
            "TASK-20260423-001-PM-to-DEV.txt",  # wrong extension
            "TASK-20260423-001-PM-DEV.md",  # missing -to-
            "TASK-20260423-001-PM-to-DEV.md.bak",  # trailing junk
            "REPORT-20260423-001-PM-to-DEV.md",  # wrong prefix
            "TASK-20260423-001--to-DEV.md",  # empty sender
            "TASK-20260423-001-PM-to-.md",  # empty recipient
        ],
    )
    def test_invalid_names_return_none(self, bad: str) -> None:
        assert fn.parse_task_filename(bad) is None


class TestBuildTaskFilename:
    def test_basic(self) -> None:
        assert (
            fn.build_task_filename(date="20260423", sequence=17, sender="PM", recipient="DEV")
            == "TASK-20260423-017-PM-to-DEV.md"
        )

    def test_with_slot(self) -> None:
        assert (
            fn.build_task_filename(
                date="20260423",
                sequence=1,
                sender="PM",
                recipient="DEV",
                slot="BACKEND",
            )
            == "TASK-20260423-001-PM-to-DEV.BACKEND.md"
        )

    def test_hyphenated_roles(self) -> None:
        assert (
            fn.build_task_filename(
                date="20260423",
                sequence=3,
                sender="LEAD-QA",
                recipient="AUTO-TESTER",
            )
            == "TASK-20260423-003-LEAD-QA-to-AUTO-TESTER.md"
        )

    def test_sequence_zero_rejected(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            fn.build_task_filename(
                date="20260423", sequence=0, sender="PM", recipient="DEV"
            )

    def test_sequence_too_large_rejected(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            fn.build_task_filename(
                date="20260423", sequence=1000, sender="PM", recipient="DEV"
            )

    def test_illegal_date_rejected(self) -> None:
        with pytest.raises(ValueError, match="YYYYMMDD|calendar"):
            fn.build_task_filename(
                date="2026-04-23", sequence=1, sender="PM", recipient="DEV"
            )

    def test_nonexistent_date_rejected(self) -> None:
        with pytest.raises(ValueError, match="calendar"):
            fn.build_task_filename(
                date="20260230", sequence=1, sender="PM", recipient="DEV"
            )

    def test_malformed_sender_rejected(self) -> None:
        with pytest.raises(ValueError, match="sender"):
            fn.build_task_filename(
                date="20260423", sequence=1, sender="pm", recipient="DEV"
            )

    def test_empty_recipient_rejected(self) -> None:
        with pytest.raises(ValueError, match="recipient"):
            fn.build_task_filename(
                date="20260423", sequence=1, sender="PM", recipient=""
            )

    def test_malformed_slot_rejected(self) -> None:
        with pytest.raises(ValueError, match="slot"):
            fn.build_task_filename(
                date="20260423",
                sequence=1,
                sender="PM",
                recipient="DEV",
                slot="back end",
            )


class TestTaskRoundTrip:
    @pytest.mark.parametrize(
        "name",
        [
            "TASK-20260423-001-PM-to-DEV.md",
            "TASK-20260423-017-ADMIN-to-PM.md",
            "TASK-20260423-042-LEAD-QA-to-AUTO-TESTER.md",
            "TASK-20260423-100-PM-to-DEV.BACKEND.md",
        ],
    )
    def test_parse_then_render(self, name: str) -> None:
        parsed = fn.parse_task_filename(name)
        assert parsed is not None
        assert parsed.render() == name


# ── REPORT filename ──────────────────────────────────────────────────


class TestReportFilename:
    def test_parse_valid(self) -> None:
        result = fn.parse_report_filename("REPORT-20260423-003-DEV-to-PM.md")
        assert result is not None
        assert result.reporter == "DEV"
        assert result.recipient == "PM"
        assert result.sequence == 3
        assert result.report_id == "REPORT-20260423-003"

    def test_parse_hyphenated_roles(self) -> None:
        result = fn.parse_report_filename(
            "REPORT-20260423-005-LEAD-QA-to-AUTO-TESTER.md"
        )
        assert result is not None
        assert result.reporter == "LEAD-QA"
        assert result.recipient == "AUTO-TESTER"

    def test_build(self) -> None:
        assert (
            fn.build_report_filename(
                date="20260423", sequence=3, reporter="DEV", recipient="PM"
            )
            == "REPORT-20260423-003-DEV-to-PM.md"
        )

    def test_round_trip(self) -> None:
        name = "REPORT-20260423-003-DEV-to-PM.md"
        parsed = fn.parse_report_filename(name)
        assert parsed is not None
        assert parsed.render() == name

    def test_task_name_not_parsed_as_report(self) -> None:
        assert fn.parse_report_filename("TASK-20260423-001-PM-to-DEV.md") is None

    def test_slot_not_allowed_on_report(self) -> None:
        assert fn.parse_report_filename("REPORT-20260423-003-DEV-to-PM.BACKEND.md") is None


# ── ISSUE filename ───────────────────────────────────────────────────


class TestIssueFilename:
    def test_parse_valid(self) -> None:
        result = fn.parse_issue_filename("ISSUE-20260423-007-QA.md")
        assert result is not None
        assert result.reporter == "QA"
        assert result.sequence == 7
        assert result.issue_id == "ISSUE-20260423-007"

    def test_build(self) -> None:
        assert (
            fn.build_issue_filename(date="20260423", sequence=7, reporter="QA")
            == "ISSUE-20260423-007-QA.md"
        )

    def test_round_trip(self) -> None:
        name = "ISSUE-20260423-007-QA.md"
        parsed = fn.parse_issue_filename(name)
        assert parsed is not None
        assert parsed.render() == name

    def test_recipient_is_illegal(self) -> None:
        # Issues broadcast; any "-to-" segment makes the name invalid.
        assert fn.parse_issue_filename("ISSUE-20260423-007-QA-to-DEV.md") is None

    def test_task_name_not_parsed_as_issue(self) -> None:
        assert fn.parse_issue_filename("TASK-20260423-001-PM-to-DEV.md") is None


# ── Date validator ───────────────────────────────────────────────────


class TestValidateDate:
    @pytest.mark.parametrize(
        "value", ["20260101", "20260423", "20260228", "20261231", "20000101"]
    )
    def test_valid_dates(self, value: str) -> None:
        assert fn.validate_date(value) == []

    def test_leap_year_feb29(self) -> None:
        # 2024 was a leap year
        assert fn.validate_date("20240229") == []

    def test_nonleap_feb29_rejected(self) -> None:
        # 2023 was not
        issues = fn.validate_date("20230229")
        assert len(issues) == 1
        assert issues[0].severity == "error"

    @pytest.mark.parametrize(
        "value",
        ["", "2026", "20260", "2026-04-23", "abcdefgh", "20260230", "20261301"],
    )
    def test_invalid_values(self, value: str) -> None:
        issues = fn.validate_date(value)
        assert len(issues) == 1
        assert issues[0].severity == "error"

    def test_field_label_threaded(self) -> None:
        issues = fn.validate_date("bad", field="created_at")
        assert issues[0].field == "created_at"


# ── Sequence validator ───────────────────────────────────────────────


class TestValidateSequence:
    @pytest.mark.parametrize("value", [1, 17, 500, 999])
    def test_in_range(self, value: int) -> None:
        assert fn.validate_sequence(value) == []

    @pytest.mark.parametrize("value", [0, -1, 1000, 99999])
    def test_out_of_range(self, value: int) -> None:
        issues = fn.validate_sequence(value)
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert "out of range" in issues[0].message

    def test_bool_rejected(self) -> None:
        # Python's bool is an int subclass — protect against accidental True/False.
        issues = fn.validate_sequence(True)  # noqa: FBT003
        assert len(issues) == 1
        assert "int" in issues[0].message

    def test_non_int_rejected(self) -> None:
        issues = fn.validate_sequence("17")  # type: ignore[arg-type]
        assert len(issues) == 1
        assert issues[0].severity == "error"


# ── next_sequence ────────────────────────────────────────────────────


class TestNextSequence:
    def test_empty_returns_one(self) -> None:
        assert fn.next_sequence([], date="20260423", kind="task") == 1

    def test_single_existing_returns_next(self) -> None:
        existing = ["TASK-20260423-001-PM-to-DEV.md"]
        assert fn.next_sequence(existing, date="20260423", kind="task") == 2

    def test_skips_other_dates(self) -> None:
        existing = [
            "TASK-20260422-001-PM-to-DEV.md",
            "TASK-20260422-002-PM-to-DEV.md",
        ]
        assert fn.next_sequence(existing, date="20260423", kind="task") == 1

    def test_fills_gap(self) -> None:
        # If sequences 1, 3, 5 are taken, next should fill in 2.
        existing = [
            "TASK-20260423-001-PM-to-DEV.md",
            "TASK-20260423-003-PM-to-DEV.md",
            "TASK-20260423-005-PM-to-DEV.md",
        ]
        assert fn.next_sequence(existing, date="20260423", kind="task") == 2

    def test_ignores_non_matching(self) -> None:
        existing = [
            "TASK-20260423-001-PM-to-DEV.md",
            "README.md",
            ".gitkeep",
            "REPORT-20260423-001-DEV-to-PM.md",  # wrong kind
            "ISSUE-20260423-001-QA.md",
        ]
        assert fn.next_sequence(existing, date="20260423", kind="task") == 2

    def test_kind_report(self) -> None:
        existing = [
            "REPORT-20260423-001-DEV-to-PM.md",
            "REPORT-20260423-002-DEV-to-PM.md",
            "TASK-20260423-001-PM-to-DEV.md",
        ]
        assert fn.next_sequence(existing, date="20260423", kind="report") == 3

    def test_kind_issue(self) -> None:
        existing = [
            "ISSUE-20260423-001-QA.md",
            "ISSUE-20260423-002-QA.md",
        ]
        assert fn.next_sequence(existing, date="20260423", kind="issue") == 3

    def test_bad_date_raises(self) -> None:
        with pytest.raises(ValueError, match="YYYYMMDD"):
            fn.next_sequence([], date="2026-04-23", kind="task")

    def test_exhausted_raises(self) -> None:
        # Synthesize all 999 slots taken.
        existing = [
            f"TASK-20260423-{i:03d}-PM-to-DEV.md" for i in range(1, fn.MAX_SEQUENCE + 1)
        ]
        with pytest.raises(OverflowError):
            fn.next_sequence(existing, date="20260423", kind="task")


# ── today_iso ────────────────────────────────────────────────────────


class TestTodayIso:
    def test_format_is_yyyymmdd(self) -> None:
        value = fn.today_iso()
        assert fn.DATE_RE.fullmatch(value) is not None
        # And must round-trip through validate_date.
        assert fn.validate_date(value) == []


# ── Module API surface ───────────────────────────────────────────────


class TestModuleApi:
    def test_all_exports_resolve(self) -> None:
        for name in fn.__all__:
            assert hasattr(fn, name), f"fcop.core.filename missing {name!r}"

    def test_dataclasses_are_frozen(self) -> None:
        from dataclasses import FrozenInstanceError

        t = fn.TaskFilename(date="20260423", sequence=1, sender="PM", recipient="DEV")
        with pytest.raises(FrozenInstanceError):
            t.sequence = 2  # type: ignore[misc]

    def test_validate_date_returns_validation_issues(self) -> None:
        issues = fn.validate_date("bad")
        assert all(isinstance(i, ValidationIssue) for i in issues)

    def test_validate_sequence_returns_validation_issues(self) -> None:
        issues = fn.validate_sequence(0)
        assert all(isinstance(i, ValidationIssue) for i in issues)


# ── Trailing slug (ADR-0033) ─────────────────────────────────────────
#
# Field-observed pattern formalised in fcop_protocol_version 2.1.0:
# an optional lowercase ``-{slug}`` segment may follow the routing
# fields of TASK / REPORT / ISSUE filenames, e.g.
# ``TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md``. The slug is a
# human-readable label that does NOT participate in routing.


class TestTaskTrailingSlug:
    """Trailing-slug grammar for TASK filenames (ADR-0033)."""

    @pytest.mark.parametrize(
        "name,sender,recipient,slot,slug",
        [
            # Codeflow field-observed samples (the original motivation).
            (
                "TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md",
                "PM",
                "OPS",
                None,
                "phase-a-fix-naming",
            ),
            (
                "TASK-20260512-022-PM-to-OPS-fcop-mcp-1-5-1-housekeeping-commit.md",
                "PM",
                "OPS",
                None,
                "fcop-mcp-1-5-1-housekeeping-commit",
            ),
            (
                "TASK-20260512-009-PM-to-OPS-codeflow-json-rm.md",
                "PM",
                "OPS",
                None,
                "codeflow-json-rm",
            ),
            # slot + slug combination.
            (
                "TASK-20260423-100-PM-to-DEV.BACKEND-fix-naming.md",
                "PM",
                "DEV",
                "BACKEND",
                "fix-naming",
            ),
            # Hyphenated role + slug.
            (
                "TASK-20260423-042-LEAD-QA-to-AUTO-TESTER-rerun-suite.md",
                "LEAD-QA",
                "AUTO-TESTER",
                None,
                "rerun-suite",
            ),
            # Slug with digits.
            (
                "TASK-20260512-001-PM-to-OPS-release-1-5-1.md",
                "PM",
                "OPS",
                None,
                "release-1-5-1",
            ),
        ],
    )
    def test_parse_with_slug(
        self,
        name: str,
        sender: str,
        recipient: str,
        slot: str | None,
        slug: str,
    ) -> None:
        result = fn.parse_task_filename(name)
        assert result is not None
        assert result.sender == sender
        assert result.recipient == recipient
        assert result.slot == slot
        assert result.slug == slug

    @pytest.mark.parametrize(
        "name",
        [
            "TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md",
            "TASK-20260423-100-PM-to-DEV.BACKEND-fix-naming.md",
            "TASK-20260423-042-LEAD-QA-to-AUTO-TESTER-rerun-suite.md",
        ],
    )
    def test_round_trip_with_slug(self, name: str) -> None:
        parsed = fn.parse_task_filename(name)
        assert parsed is not None
        assert parsed.render() == name

    def test_legacy_no_slug_stays_compatible(self) -> None:
        """Legacy short filenames must keep parsing with ``slug=None``."""
        result = fn.parse_task_filename("TASK-20260423-017-ADMIN-to-PM.md")
        assert result is not None
        assert result.slug is None
        assert result.render() == "TASK-20260423-017-ADMIN-to-PM.md"

    @pytest.mark.parametrize(
        "bad",
        [
            # Slug must start with a lowercase letter.
            "TASK-20260512-007-PM-to-OPS-1foo.md",  # digit start
            "TASK-20260512-007-PM-to-OPS--foo.md",  # empty segment
            "TASK-20260512-007-PM-to-OPS-foo_bar.md",  # underscore in slug
            "TASK-20260512-007-PM-to-OPS-foo.bar.md",  # dot in slug
            "TASK-20260512-007-PM-to-OPS-foo bar.md",  # space in slug
            "TASK-20260512-007-PM-to-OPS-foo-.md",  # trailing hyphen
        ],
    )
    def test_invalid_slug_rejected(self, bad: str) -> None:
        assert fn.parse_task_filename(bad) is None

    def test_uppercase_tail_absorbed_by_role(self) -> None:
        """Disambiguation: an uppercase segment after ``-`` is parsed as
        part of the role code, not as a slug. ``OPS-FOO`` is a legal
        compound role per :data:`ROLE_CODE_RE`, so ``OPS-FOO.md`` parses
        with ``recipient='OPS-FOO'`` and ``slug=None``.

        This is the by-design boundary that makes slug grammar
        unambiguous: lowercase-start forces the slug to never collide
        with role-code segments.
        """
        result = fn.parse_task_filename("TASK-20260512-007-PM-to-OPS-FOO.md")
        assert result is not None
        assert result.recipient == "OPS-FOO"
        assert result.slug is None


class TestBuildTaskFilenameWithSlug:
    def test_build_with_slug(self) -> None:
        assert (
            fn.build_task_filename(
                date="20260512",
                sequence=25,
                sender="PM",
                recipient="OPS",
                slug="phase-a-fix-naming",
            )
            == "TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md"
        )

    def test_build_with_slot_and_slug(self) -> None:
        assert (
            fn.build_task_filename(
                date="20260423",
                sequence=100,
                sender="PM",
                recipient="DEV",
                slot="BACKEND",
                slug="fix-naming",
            )
            == "TASK-20260423-100-PM-to-DEV.BACKEND-fix-naming.md"
        )

    def test_slug_none_omits_segment(self) -> None:
        assert (
            fn.build_task_filename(
                date="20260423",
                sequence=17,
                sender="PM",
                recipient="DEV",
                slug=None,
            )
            == "TASK-20260423-017-PM-to-DEV.md"
        )

    @pytest.mark.parametrize(
        "bad_slug",
        [
            "Foo",  # uppercase
            "foo_bar",  # underscore
            "1foo",  # digit start
            "foo bar",  # space
            "-foo",  # leading hyphen
            "foo-",  # trailing hyphen
            "",  # empty (None means "omit"; "" is explicit illegal)
        ],
    )
    def test_malformed_slug_rejected(self, bad_slug: str) -> None:
        with pytest.raises(ValueError, match="slug"):
            fn.build_task_filename(
                date="20260423",
                sequence=1,
                sender="PM",
                recipient="DEV",
                slug=bad_slug,
            )


class TestReportTrailingSlug:
    def test_parse_with_slug(self) -> None:
        result = fn.parse_report_filename(
            "REPORT-20260512-009-OPS-to-PM-codeflow-json-rm.md"
        )
        assert result is not None
        assert result.reporter == "OPS"
        assert result.recipient == "PM"
        assert result.slug == "codeflow-json-rm"

    def test_round_trip_with_slug(self) -> None:
        name = "REPORT-20260512-009-OPS-to-PM-codeflow-json-rm.md"
        parsed = fn.parse_report_filename(name)
        assert parsed is not None
        assert parsed.render() == name

    def test_legacy_no_slug(self) -> None:
        result = fn.parse_report_filename("REPORT-20260423-003-DEV-to-PM.md")
        assert result is not None
        assert result.slug is None

    def test_build_with_slug(self) -> None:
        assert (
            fn.build_report_filename(
                date="20260512",
                sequence=9,
                reporter="OPS",
                recipient="PM",
                slug="codeflow-json-rm",
            )
            == "REPORT-20260512-009-OPS-to-PM-codeflow-json-rm.md"
        )

    def test_malformed_slug_rejected(self) -> None:
        with pytest.raises(ValueError, match="slug"):
            fn.build_report_filename(
                date="20260423",
                sequence=3,
                reporter="DEV",
                recipient="PM",
                slug="Foo",
            )


class TestIssueTrailingSlug:
    def test_parse_with_slug(self) -> None:
        result = fn.parse_issue_filename(
            "ISSUE-20260512-001-PM-pm50-userhome-pollution.md"
        )
        assert result is not None
        assert result.reporter == "PM"
        assert result.slug == "pm50-userhome-pollution"

    def test_round_trip_with_slug(self) -> None:
        name = "ISSUE-20260512-001-PM-pm50-userhome-pollution.md"
        parsed = fn.parse_issue_filename(name)
        assert parsed is not None
        assert parsed.render() == name

    def test_legacy_no_slug(self) -> None:
        result = fn.parse_issue_filename("ISSUE-20260423-007-QA.md")
        assert result is not None
        assert result.slug is None

    def test_build_with_slug(self) -> None:
        assert (
            fn.build_issue_filename(
                date="20260512",
                sequence=1,
                reporter="PM",
                slug="pm50-userhome-pollution",
            )
            == "ISSUE-20260512-001-PM-pm50-userhome-pollution.md"
        )

    def test_malformed_slug_rejected(self) -> None:
        with pytest.raises(ValueError, match="slug"):
            fn.build_issue_filename(
                date="20260423",
                sequence=7,
                reporter="QA",
                slug="Foo",
            )


class TestSlugRegexExport:
    """``SLUG_RE`` should be exported and shape-pinned."""

    def test_slug_re_in_all(self) -> None:
        assert "SLUG_RE" in fn.__all__

    def test_slug_re_anchored(self) -> None:
        assert fn.SLUG_RE.pattern.startswith("^")
        assert fn.SLUG_RE.pattern.endswith("$")

    @pytest.mark.parametrize(
        "legal",
        ["foo", "foo-bar", "phase-a-fix-naming", "release-1-5-1", "x", "abc123"],
    )
    def test_slug_re_accepts(self, legal: str) -> None:
        assert fn.SLUG_RE.fullmatch(legal) is not None

    @pytest.mark.parametrize(
        "illegal",
        ["", "Foo", "1foo", "-foo", "foo-", "foo_bar", "foo bar", "foo.bar"],
    )
    def test_slug_re_rejects(self, illegal: str) -> None:
        assert fn.SLUG_RE.fullmatch(illegal) is None
