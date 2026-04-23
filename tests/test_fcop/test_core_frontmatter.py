"""Tests for :mod:`fcop.core.frontmatter`.

Covers split, raw parse, typed parse with all validation paths,
serialization, round-trip, and legacy-alias normalization.
"""

from __future__ import annotations

import pytest
import yaml

from fcop.core import frontmatter as fm
from fcop.errors import ProtocolViolation, ValidationError
from fcop.models import Priority, TaskFrontmatter

# ── split_frontmatter ────────────────────────────────────────────────


class TestSplitFrontmatter:
    def test_standard_document(self) -> None:
        text = "---\nprotocol: fcop\nversion: 1\n---\n\n# hello\n"
        block, body = fm.split_frontmatter(text)
        assert block == "protocol: fcop\nversion: 1\n"
        assert body == "\n# hello\n"

    def test_no_frontmatter(self) -> None:
        text = "# just body\n"
        block, body = fm.split_frontmatter(text)
        assert block == ""
        assert body == text

    def test_crlf_line_endings(self) -> None:
        text = "---\r\nprotocol: fcop\r\nversion: 1\r\n---\r\n\r\n# body\r\n"
        block, body = fm.split_frontmatter(text)
        assert "protocol: fcop" in block
        assert body.lstrip().startswith("# body")

    def test_empty_body(self) -> None:
        text = "---\nprotocol: fcop\nversion: 1\n---\n"
        block, body = fm.split_frontmatter(text)
        assert block == "protocol: fcop\nversion: 1\n"
        assert body == ""

    def test_unterminated_frontmatter(self) -> None:
        # Opening --- but no closing one ⇒ not recognized as frontmatter
        text = "---\nprotocol: fcop\n"
        block, body = fm.split_frontmatter(text)
        assert block == ""
        assert body == text

    def test_opening_not_on_first_line(self) -> None:
        text = "# title\n---\nprotocol: fcop\n---\n"
        block, body = fm.split_frontmatter(text)
        assert block == ""
        assert body == text

    def test_dashes_with_trailing_whitespace_still_frontmatter(self) -> None:
        # "---   \n" should still count as a fence line
        text = "---   \nprotocol: fcop\nversion: 1\n---\n\nbody"
        block, body = fm.split_frontmatter(text)
        assert "protocol: fcop" in block


# ── parse_frontmatter_raw ────────────────────────────────────────────


class TestParseFrontmatterRaw:
    def test_standard_mapping(self) -> None:
        text = "---\nprotocol: fcop\nversion: 1\nsender: PM\n---\n\nbody"
        raw = fm.parse_frontmatter_raw(text)
        assert raw == {"protocol": "fcop", "version": 1, "sender": "PM"}

    def test_no_frontmatter_returns_empty(self) -> None:
        assert fm.parse_frontmatter_raw("# body\n") == {}

    def test_empty_frontmatter_returns_empty(self) -> None:
        assert fm.parse_frontmatter_raw("---\n---\n\nbody") == {}

    def test_malformed_yaml_raises_validation_error(self) -> None:
        text = "---\nprotocol: fcop\nversion: : bad\n---\n\nbody"
        with pytest.raises(ValidationError):
            fm.parse_frontmatter_raw(text)

    def test_non_mapping_raises_validation_error(self) -> None:
        # A bare scalar isn't a mapping
        text = "---\njust-a-string\n---\n\nbody"
        with pytest.raises(ValidationError, match="mapping"):
            fm.parse_frontmatter_raw(text)

    def test_list_top_level_raises(self) -> None:
        text = "---\n- a\n- b\n---\n"
        with pytest.raises(ValidationError, match="mapping"):
            fm.parse_frontmatter_raw(text)

    def test_comment_only_returns_empty(self) -> None:
        text = "---\n# just a comment\n---\n\nbody"
        assert fm.parse_frontmatter_raw(text) == {}


# ── parse_task_frontmatter — happy paths ─────────────────────────────


class TestParseTaskFrontmatter:
    STANDARD = (
        "---\n"
        "protocol: fcop\n"
        "version: 1\n"
        "sender: ADMIN\n"
        "recipient: PM\n"
        "priority: P1\n"
        "---\n"
        "\n"
        "body text\n"
    )

    def test_standard(self) -> None:
        parsed, body = fm.parse_task_frontmatter(self.STANDARD)
        assert parsed.protocol == "fcop"
        assert parsed.version == 1
        assert parsed.sender == "ADMIN"
        assert parsed.recipient == "PM"
        assert parsed.priority is Priority.P1
        assert body == "\nbody text\n"

    def test_priority_defaults_to_p2_when_absent(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n---\n\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.priority is Priority.P2

    def test_legacy_priority_word_normalizes(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n"
            "priority: urgent\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.priority is Priority.P0

    def test_protocol_alias_normalizes(self) -> None:
        text = (
            "---\nprotocol: agent_bridge\nversion: 1\nsender: PM\nrecipient: DEV\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.protocol == "fcop"

    def test_version_as_string_accepted(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: \"1.0\"\nsender: PM\nrecipient: DEV\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.version == 1

    def test_version_as_float_accepted(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1.0\nsender: PM\nrecipient: DEV\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.version == 1

    def test_optional_fields_populated(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n"
            "thread_key: release-0.6\nsubject: ship the library\n"
            "references:\n  - TASK-20260422-001\n  - REPORT-20260422-001\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.thread_key == "release-0.6"
        assert parsed.subject == "ship the library"
        assert parsed.references == ("TASK-20260422-001", "REPORT-20260422-001")

    def test_references_as_single_string(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n"
            "references: TASK-20260422-001\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.references == ("TASK-20260422-001",)

    def test_unknown_keys_go_to_extra(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n"
            "custom_field: hello\nanother: 42\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.extra == {"custom_field": "hello", "another": 42}


# ── parse_task_frontmatter — error paths ─────────────────────────────


class TestParseTaskFrontmatterErrors:
    def test_missing_protocol_raises_protocol_violation(self) -> None:
        text = "---\nversion: 1\nsender: PM\nrecipient: DEV\n---\n"
        with pytest.raises(ProtocolViolation) as exc_info:
            fm.parse_task_frontmatter(text)
        assert "protocol" in str(exc_info.value)
        assert exc_info.value.rule == "frontmatter.required"

    def test_missing_version_raises_protocol_violation(self) -> None:
        text = "---\nprotocol: fcop\nsender: PM\nrecipient: DEV\n---\n"
        with pytest.raises(ProtocolViolation, match="version"):
            fm.parse_task_frontmatter(text)

    def test_missing_sender_raises_protocol_violation(self) -> None:
        text = "---\nprotocol: fcop\nversion: 1\nrecipient: DEV\n---\n"
        with pytest.raises(ProtocolViolation, match="sender"):
            fm.parse_task_frontmatter(text)

    def test_missing_recipient_raises_protocol_violation(self) -> None:
        text = "---\nprotocol: fcop\nversion: 1\nsender: PM\n---\n"
        with pytest.raises(ProtocolViolation, match="recipient"):
            fm.parse_task_frontmatter(text)

    def test_unknown_protocol_raises_protocol_violation(self) -> None:
        text = (
            "---\nprotocol: bridgeflow\nversion: 1\nsender: PM\nrecipient: DEV\n---\n"
        )
        with pytest.raises(ProtocolViolation, match="unknown protocol"):
            fm.parse_task_frontmatter(text)

    def test_unsupported_version_raises_protocol_violation(self) -> None:
        text = "---\nprotocol: fcop\nversion: 2\nsender: PM\nrecipient: DEV\n---\n"
        with pytest.raises(ProtocolViolation, match="unsupported"):
            fm.parse_task_frontmatter(text)

    def test_non_integer_version_raises_validation_error(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: abc\nsender: PM\nrecipient: DEV\n---\n"
        )
        with pytest.raises(ValidationError):
            fm.parse_task_frontmatter(text)

    def test_bad_role_code_raises_validation_error(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: pm\nrecipient: DEV\n---\n"
        )
        with pytest.raises(ValidationError) as exc:
            fm.parse_task_frontmatter(text)
        assert any(i.field == "sender" for i in exc.value.issues)

    def test_admin_and_system_are_accepted_in_frontmatter(self) -> None:
        # ADMIN = human operator, SYSTEM = internal protocol sender.
        # Both legitimately appear in task headers; reserved-word rules
        # only apply to team-config role assignment.
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: ADMIN\nrecipient: SYSTEM\n---\n"
        )
        parsed, _ = fm.parse_task_frontmatter(text)
        assert parsed.sender == "ADMIN"
        assert parsed.recipient == "SYSTEM"

    def test_bad_priority_raises_validation_error(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n"
            "priority: blocker\n---\n"
        )
        with pytest.raises(ValidationError, match="priority"):
            fm.parse_task_frontmatter(text)

    def test_references_as_mapping_raises_validation_error(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: PM\nrecipient: DEV\n"
            "references:\n  key: value\n---\n"
        )
        with pytest.raises(ValidationError, match="references"):
            fm.parse_task_frontmatter(text)

    def test_no_frontmatter_raises_protocol_violation(self) -> None:
        with pytest.raises(ProtocolViolation, match="protocol"):
            fm.parse_task_frontmatter("# just body, no frontmatter\n")


# ── serialize_task_frontmatter ───────────────────────────────────────


class TestSerializeTaskFrontmatter:
    def test_minimal_serialization(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
        )
        out = fm.serialize_task_frontmatter(frontmatter)
        assert out.startswith("---\n")
        assert out.endswith("---\n")
        parsed = yaml.safe_load(out.split("---")[1])
        assert parsed == {
            "protocol": "fcop",
            "version": 1,
            "sender": "PM",
            "recipient": "DEV",
            "priority": "P1",
        }

    def test_field_order_is_deterministic(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            thread_key="t1",
            subject="s",
        )
        out = fm.serialize_task_frontmatter(frontmatter)
        lines = [line for line in out.splitlines() if ":" in line]
        keys_in_order = [line.split(":", 1)[0] for line in lines]
        assert keys_in_order == [
            "protocol",
            "version",
            "sender",
            "recipient",
            "priority",
            "thread_key",
            "subject",
        ]

    def test_optional_fields_omitted_when_blank(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P2,
        )
        out = fm.serialize_task_frontmatter(frontmatter)
        assert "thread_key" not in out
        assert "subject" not in out
        assert "references" not in out

    def test_extra_keys_appear_sorted(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P2,
            extra={"zebra": 1, "alpha": 2, "mango": 3},
        )
        out = fm.serialize_task_frontmatter(frontmatter)
        alpha_idx = out.index("alpha:")
        mango_idx = out.index("mango:")
        zebra_idx = out.index("zebra:")
        assert alpha_idx < mango_idx < zebra_idx

    def test_unicode_survives(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P1,
            subject="发布码流 0.6.0",
        )
        out = fm.serialize_task_frontmatter(frontmatter)
        # allow_unicode=True should keep the CJK characters, not escape them
        assert "发布码流 0.6.0" in out


# ── Round-trip ───────────────────────────────────────────────────────


class TestRoundTrip:
    def test_parse_serialize_parse_is_stable(self) -> None:
        text = (
            "---\nprotocol: fcop\nversion: 1\nsender: ADMIN\nrecipient: PM\n"
            "priority: P1\nthread_key: release\nsubject: ship it\n"
            "references:\n- TASK-20260422-001\n---\n\nbody paragraph\n"
        )
        first, body1 = fm.parse_task_frontmatter(text)
        assembled = fm.assemble_task_file(first, body1)
        second, body2 = fm.parse_task_frontmatter(assembled)
        assert first == second
        # Body should match after one normalization pass; we don't
        # claim byte-for-byte identity across the first pass (blank
        # line handling), but the second round-trip must be stable.
        assembled2 = fm.assemble_task_file(second, body2)
        assert assembled == assembled2

    def test_assemble_inserts_blank_line(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P2,
        )
        out = fm.assemble_task_file(frontmatter, "content\n")
        assert "\n\ncontent" in out

    def test_assemble_strips_extra_leading_newlines(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P2,
        )
        out = fm.assemble_task_file(frontmatter, "\n\n\ncontent\n")
        # exactly one blank line between --- and content
        assert "---\n\ncontent" in out

    def test_assemble_empty_body(self) -> None:
        frontmatter = TaskFrontmatter(
            protocol="fcop",
            version=1,
            sender="PM",
            recipient="DEV",
            priority=Priority.P2,
        )
        out = fm.assemble_task_file(frontmatter, "")
        assert out.endswith("---\n")


# ── Module API surface ───────────────────────────────────────────────


class TestModuleApi:
    def test_all_exports_resolve(self) -> None:
        for name in fm.__all__:
            assert hasattr(fm, name), f"fcop.core.frontmatter missing {name!r}"

    def test_default_priority_matches_library_contract(self) -> None:
        assert fm.DEFAULT_PRIORITY is Priority.P2
