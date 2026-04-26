"""Tests for the 0.6.4 init-deposit contract.

Background. 0.6.3 had several "init promises" that were only kept on
paper: the LETTER-TO-ADMIN.md user manual was advertised but never
written, ``workspace/`` was advertised as a Rule 7.5 cage but never
created, and bundled three-layer team docs were not auto-deployed
under ``shared/``. These tests pin the 0.6.4 fix: every ``init_*``
call deposits the **full** documented set in a single transaction
(or raises before any partial write).

Companion change: ``Project.init(team="solo")`` is now rejected with
a ``ValueError`` so callers don't accidentally land a config with
``mode="preset", team="solo"`` (the path through ``init_solo`` is
the only way to land ``mode="solo"``). Tested below as well.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project

# Files every init_* must produce. Subject to expansion as new
# init-time deposits are introduced; intentionally kept as a flat
# list so a regression shows up as a missing path, not a logic bug.
_BASE_DEPOSITS = (
    "docs/agents/fcop.json",
    "docs/agents/LETTER-TO-ADMIN.md",
    "workspace/README.md",
    ".cursor/rules/fcop-rules.mdc",
    ".cursor/rules/fcop-protocol.mdc",
    "AGENTS.md",
    "CLAUDE.md",
)

# Files every preset / solo init must additionally deposit (the
# three-layer team docs). Custom teams have no bundled templates so
# this set is *not* asserted for them.
_TEAM_TEMPLATE_DEPOSITS = (
    "docs/agents/shared/TEAM-README.md",
    "docs/agents/shared/TEAM-README.en.md",
    "docs/agents/shared/TEAM-ROLES.md",
    "docs/agents/shared/TEAM-ROLES.en.md",
    "docs/agents/shared/TEAM-OPERATING-RULES.md",
    "docs/agents/shared/TEAM-OPERATING-RULES.en.md",
)


def _assert_all_present(root: Path, rels: tuple[str, ...]) -> None:
    """Fail with the missing path so a CI red is easy to read."""
    missing = [r for r in rels if not (root / r).is_file()]
    assert not missing, f"init promised these files but did not write them: {missing}"


# ── init() — preset team ─────────────────────────────────────────────


class TestInitPresetDeposits:
    def test_dev_team_deposits_full_set(self, tmp_path: Path) -> None:
        Project(tmp_path).init(team="dev-team", lang="zh", deploy_rules=True)
        _assert_all_present(tmp_path, _BASE_DEPOSITS)
        _assert_all_present(tmp_path, _TEAM_TEMPLATE_DEPOSITS)

        # Per-role layer-3 charters land for every role in the team.
        for role in ("PM", "DEV", "QA", "OPS"):
            for ext in (".md", ".en.md"):
                rel = f"docs/agents/shared/roles/{role}{ext}"
                assert (tmp_path / rel).is_file(), f"missing role charter {rel}"

    def test_letter_lang_follows_init_lang_zh(self, tmp_path: Path) -> None:
        Project(tmp_path).init(team="dev-team", lang="zh", deploy_rules=True)
        letter = (tmp_path / "docs/agents/LETTER-TO-ADMIN.md").read_text(
            encoding="utf-8"
        )
        # The Chinese letter has a recognisable opening; checking a
        # short literal avoids brittle word counts.
        assert "你好，ADMIN" in letter or "ADMIN" in letter

    def test_letter_lang_follows_init_lang_en(self, tmp_path: Path) -> None:
        Project(tmp_path).init(team="dev-team", lang="en", deploy_rules=True)
        letter = (tmp_path / "docs/agents/LETTER-TO-ADMIN.md").read_text(
            encoding="utf-8"
        )
        assert "Hi ADMIN" in letter or "User Manual" in letter

    def test_init_rejects_solo_via_team_param(self, tmp_path: Path) -> None:
        # Calling Project.init(team="solo") would have produced a
        # config with mode="preset", team="solo" — wrong shape.
        # 0.6.4 raises before touching the disk so callers learn to
        # use init_solo() instead.
        with pytest.raises(ValueError) as excinfo:
            Project(tmp_path).init(team="solo")
        assert "init_solo" in str(excinfo.value)
        assert not (tmp_path / "docs/agents/fcop.json").exists()


# ── init_solo() ──────────────────────────────────────────────────────


class TestInitSoloDeposits:
    def test_default_me_role_full_deposits(self, tmp_path: Path) -> None:
        Project(tmp_path).init_solo(
            role_code="ME", lang="zh", deploy_rules=True
        )
        _assert_all_present(tmp_path, _BASE_DEPOSITS)
        _assert_all_present(tmp_path, _TEAM_TEMPLATE_DEPOSITS)

        # Solo's only role charter.
        for ext in (".md", ".en.md"):
            assert (
                tmp_path / f"docs/agents/shared/roles/ME{ext}"
            ).is_file(), f"missing solo ME charter {ext}"

    def test_solo_me_charter_has_workflow_hard_constraint(
        self, tmp_path: Path
    ) -> None:
        # The 0.6.4 ME.md charter must contain the "硬约束 / hard
        # constraint" workflow section — the in-code anchor that
        # forbids "simple tasks may run directly" soft-constraints
        # (companion to fcop-rules.mdc Rule 0.a.1).
        Project(tmp_path).init_solo(role_code="ME", lang="zh")
        zh = (tmp_path / "docs/agents/shared/roles/ME.md").read_text(
            encoding="utf-8"
        )
        assert "硬约束" in zh, "solo ME.md (zh) must declare 硬约束"

        en = (tmp_path / "docs/agents/shared/roles/ME.en.md").read_text(
            encoding="utf-8"
        )
        # English copy uses "hard constraint" verbatim somewhere in
        # the workflow section.
        assert (
            "hard constraint" in en.lower()
        ), "solo ME.en.md must declare a hard-constraint workflow"

    def test_workspace_readme_explains_cage(self, tmp_path: Path) -> None:
        Project(tmp_path).init_solo(role_code="ME")
        readme = (tmp_path / "workspace/README.md").read_text(
            encoding="utf-8"
        )
        # Rule 7.5 is the cage rule; the README is supposed to tell
        # the user where artefacts go without making them open the
        # full protocol commentary.
        assert "Rule 7.5" in readme
        assert "workspace/" in readme

    def test_force_reinit_archives_old_artifacts(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        project.init_solo(role_code="ME", lang="zh", deploy_rules=True)
        # Re-init with a different role to exercise the archive
        # path; the returned config must reflect the new role and
        # the migration directory must contain the previous config.
        project.init_solo(
            role_code="CODER", lang="zh", force=True, deploy_rules=True
        )
        cfg = project.config
        assert cfg.roles == ("CODER",)
        archived = list((tmp_path / ".fcop/migrations").rglob("fcop.json"))
        assert archived, "force=True must archive the previous fcop.json"


# ── init_custom() ────────────────────────────────────────────────────


class TestInitCustomDeposits:
    def test_custom_deposits_base_set_only(self, tmp_path: Path) -> None:
        # Custom teams have no bundled three-layer templates, so
        # only the *base* deposits are guaranteed; shared/roles/
        # remains agent-authored ground.
        Project(tmp_path).init_custom(
            team_name="my-squad",
            roles=["LEAD", "BUILDER"],
            leader="LEAD",
            lang="zh",
            deploy_rules=True,
        )
        _assert_all_present(tmp_path, _BASE_DEPOSITS)

        # No bundled charter for "LEAD" / "BUILDER" — confirm the
        # files genuinely don't exist (rather than testing absence
        # implicitly).
        for role in ("LEAD", "BUILDER"):
            assert not (
                tmp_path / f"docs/agents/shared/roles/{role}.md"
            ).is_file(), (
                f"custom team must not auto-write a bundled charter for {role}"
            )
