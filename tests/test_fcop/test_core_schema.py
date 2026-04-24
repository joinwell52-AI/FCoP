"""Tests for :mod:`fcop.core.schema` — protocol constants and validators.

These are pure unit tests: no tmp files, no I/O. They pin down the
normative values of the protocol so a future refactor can't silently
re-spell a canonical form or drop a legacy alias.
"""

from __future__ import annotations

import re

import pytest

from fcop.core import schema
from fcop.models import Priority, Severity, ValidationIssue

# ── Protocol identity ────────────────────────────────────────────────


class TestProtocolIdentity:
    def test_canonical_name_is_lowercase_fcop(self) -> None:
        assert schema.PROTOCOL_NAME == "fcop"

    def test_version_is_integer_one(self) -> None:
        assert schema.PROTOCOL_VERSION == 1
        assert isinstance(schema.PROTOCOL_VERSION, int)

    def test_aliases_include_canonical_and_history(self) -> None:
        # Canonical always accepted; historical aliases must never be
        # removed without a major version bump (pre-0.6 files rely on
        # them).
        for alias in (
            "fcop",
            "agent_bridge",
            "agent-bridge",
            "file-coordination",
            "file_coordination",
        ):
            assert alias in schema.PROTOCOL_ALIASES

    def test_aliases_is_frozenset(self) -> None:
        assert isinstance(schema.PROTOCOL_ALIASES, frozenset)


class TestNormalizeProtocolName:
    @pytest.mark.parametrize(
        "raw",
        [
            "fcop",
            "FCoP",
            "FCOP",
            "  fcop  ",
            "agent_bridge",
            "agent-bridge",
            "file-coordination",
            "file_coordination",
        ],
    )
    def test_known_aliases_normalize_to_canonical(self, raw: str) -> None:
        assert schema.normalize_protocol_name(raw) == "fcop"

    @pytest.mark.parametrize("raw", ["", "bridgeflow", "contoso-cms", "mcp", "http"])
    def test_unknown_values_return_none(self, raw: str) -> None:
        assert schema.normalize_protocol_name(raw) is None


# ── Role codes ───────────────────────────────────────────────────────


class TestRoleCodeRegex:
    @pytest.mark.parametrize(
        "code",
        [
            "PM",
            "DEV",
            "QA",
            "PM_01",
            "DEV_02",
            "LEAD-QA",
            "AUTO-TESTER",
            "PERF-TESTER",
            "A",
            "Z9",
            "X-Y-Z",
        ],
    )
    def test_legal_codes_match(self, code: str) -> None:
        assert schema.ROLE_CODE_RE.fullmatch(code) is not None

    @pytest.mark.parametrize(
        "code",
        [
            "",
            "pm",  # lowercase
            "1PM",  # leading digit
            "_PM",  # leading underscore
            "-PM",  # leading hyphen
            "PM-",  # trailing hyphen
            "PM--QA",  # consecutive hyphens
            "PM.QA",  # dot
            "PM QA",  # space
            "程序员",  # non-ASCII
            "PM/QA",  # slash
        ],
    )
    def test_illegal_codes_reject(self, code: str) -> None:
        assert schema.ROLE_CODE_RE.fullmatch(code) is None


class TestIsValidRoleCode:
    def test_legal_code_is_valid(self) -> None:
        assert schema.is_valid_role_code("PM") is True

    def test_reserved_code_is_invalid(self) -> None:
        assert schema.is_valid_role_code("ADMIN") is False
        assert schema.is_valid_role_code("SYSTEM") is False

    def test_empty_string_is_invalid(self) -> None:
        assert schema.is_valid_role_code("") is False

    def test_malformed_is_invalid(self) -> None:
        assert schema.is_valid_role_code("pm") is False


class TestValidateRoleCode:
    def test_legal_code_returns_empty_list(self) -> None:
        assert schema.validate_role_code("PM") == []

    def test_empty_returns_error(self) -> None:
        issues = schema.validate_role_code("")
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert "empty" in issues[0].message.lower()

    def test_malformed_returns_error(self) -> None:
        issues = schema.validate_role_code("pm")
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert "'pm'" in issues[0].message

    def test_reserved_returns_error(self) -> None:
        issues = schema.validate_role_code("ADMIN")
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert "reserved" in issues[0].message.lower()

    def test_system_reserved_returns_error(self) -> None:
        issues = schema.validate_role_code("SYSTEM")
        assert len(issues) == 1
        assert issues[0].severity == "error"

    def test_allow_reserved_accepts_admin(self) -> None:
        # Frontmatter sender/recipient legitimately carries ADMIN
        # (the human) or SYSTEM (the protocol); the allow_reserved
        # switch lets callers opt out of the strict check used for
        # team config.
        assert schema.validate_role_code("ADMIN", allow_reserved=True) == []
        assert schema.validate_role_code("SYSTEM", allow_reserved=True) == []

    def test_allow_reserved_still_rejects_grammar_errors(self) -> None:
        # The switch only relaxes the reserved-word check; bad grammar
        # is still a hard error.
        issues = schema.validate_role_code("admin", allow_reserved=True)
        assert len(issues) == 1
        assert issues[0].severity == "error"

    def test_authority_word_is_warning_not_error(self) -> None:
        issues = schema.validate_role_code("BOSS")
        assert len(issues) == 1
        assert issues[0].severity == "warning"
        assert "authority" in issues[0].message.lower()

    def test_field_label_is_threaded_through(self) -> None:
        issues = schema.validate_role_code("", field="sender")
        assert issues[0].field == "sender"

    def test_returns_validation_issue_instances(self) -> None:
        issues = schema.validate_role_code("pm")
        assert all(isinstance(i, ValidationIssue) for i in issues)


class TestSuggestRoleCode:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("pm", "PM"),
            ("dev", "DEV"),
            ("dev 01", "DEV_01"),
            ("dev.01", "DEV_01"),
            ("lead-qa", "LEAD-QA"),
            ("  pm  ", "PM"),
            ("__pm__", "PM"),
            ("--pm--", "PM"),
            ("pm__qa", "PM_QA"),
            ("pm--qa", "PM-QA"),
            ("1pm", "R1PM"),
        ],
    )
    def test_common_repairs(self, raw: str, expected: str) -> None:
        assert schema.suggest_role_code(raw) == expected

    @pytest.mark.parametrize("raw", ["", "   ", "程序员", "!!!", "。。。"])
    def test_hopeless_inputs_return_empty(self, raw: str) -> None:
        assert schema.suggest_role_code(raw) == ""

    def test_suggestion_always_passes_regex(self) -> None:
        # Property-style check over the hand-picked cases above.
        for raw in ["pm", "dev 01", "lead-qa", "1pm"]:
            out = schema.suggest_role_code(raw)
            assert out, f"unexpectedly empty suggestion for {raw!r}"
            assert schema.ROLE_CODE_RE.fullmatch(out) is not None


class TestReservedAndAuthority:
    def test_reserved_codes_contain_admin_and_system(self) -> None:
        assert "ADMIN" in schema.RESERVED_ROLE_CODES
        assert "SYSTEM" in schema.RESERVED_ROLE_CODES

    def test_reserved_codes_is_frozenset(self) -> None:
        assert isinstance(schema.RESERVED_ROLE_CODES, frozenset)

    def test_authority_words_are_not_in_reserved(self) -> None:
        # Authority words are warnings, not rejections. Mixing them into
        # RESERVED would upgrade them to errors by mistake.
        assert schema.AUTHORITY_WORDS.isdisjoint(schema.RESERVED_ROLE_CODES)

    def test_authority_words_are_frozenset(self) -> None:
        assert isinstance(schema.AUTHORITY_WORDS, frozenset)


# ── Frontmatter sets ─────────────────────────────────────────────────


class TestFrontmatterKeys:
    def test_required_keys_contain_the_four_canonical_fields(self) -> None:
        assert frozenset(
            {"protocol", "version", "sender", "recipient"}
        ) == schema.REQUIRED_TASK_FRONTMATTER_KEYS

    def test_required_and_optional_do_not_overlap(self) -> None:
        assert schema.REQUIRED_TASK_FRONTMATTER_KEYS.isdisjoint(
            schema.OPTIONAL_TASK_FRONTMATTER_KEYS
        )

    def test_priority_is_optional_not_required(self) -> None:
        # Priority has a library-level default (P2); frontmatter doesn't
        # need to carry it.
        assert "priority" in schema.OPTIONAL_TASK_FRONTMATTER_KEYS
        assert "priority" not in schema.REQUIRED_TASK_FRONTMATTER_KEYS


# ── Priority ─────────────────────────────────────────────────────────


class TestNormalizePriority:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("P0", Priority.P0),
            ("p0", Priority.P0),
            ("P1", Priority.P1),
            ("P2", Priority.P2),
            ("P3", Priority.P3),
            (" P2 ", Priority.P2),
        ],
    )
    def test_canonical_strings(self, raw: str, expected: Priority) -> None:
        assert schema.normalize_priority(raw) is expected

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("urgent", Priority.P0),
            ("critical", Priority.P0),
            ("high", Priority.P1),
            ("normal", Priority.P2),
            ("medium", Priority.P2),
            ("low", Priority.P3),
            ("NORMAL", Priority.P2),
        ],
    )
    def test_legacy_aliases(self, raw: str, expected: Priority) -> None:
        assert schema.normalize_priority(raw) is expected

    def test_enum_passthrough(self) -> None:
        assert schema.normalize_priority(Priority.P1) is Priority.P1

    @pytest.mark.parametrize("raw", ["P4", "", "whatever", "p5", "nope"])
    def test_unknown_raises_value_error(self, raw: str) -> None:
        with pytest.raises(ValueError, match="unknown priority"):
            schema.normalize_priority(raw)


class TestNormalizeSeverity:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("low", Severity.LOW),
            ("LOW", Severity.LOW),
            ("medium", Severity.MEDIUM),
            ("med", Severity.MEDIUM),
            ("high", Severity.HIGH),
            ("critical", Severity.CRITICAL),
            ("crit", Severity.CRITICAL),
            (" high ", Severity.HIGH),
        ],
    )
    def test_known_values(self, raw: str, expected: Severity) -> None:
        assert schema.normalize_severity(raw) is expected

    def test_enum_passthrough(self) -> None:
        assert schema.normalize_severity(Severity.HIGH) is Severity.HIGH

    @pytest.mark.parametrize("raw", ["", "whatever", "P1", "blocker"])
    def test_unknown_raises_value_error(self, raw: str) -> None:
        with pytest.raises(ValueError, match="unknown severity"):
            schema.normalize_severity(raw)


# ── Module API surface ───────────────────────────────────────────────


class TestModuleApi:
    def test_all_exports_are_defined(self) -> None:
        for name in schema.__all__:
            assert hasattr(schema, name), f"fcop.core.schema missing {name!r} from __all__"

    def test_role_code_re_is_compiled_pattern(self) -> None:
        assert isinstance(schema.ROLE_CODE_RE, re.Pattern)
