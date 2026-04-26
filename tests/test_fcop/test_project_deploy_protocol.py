"""Tests for :meth:`fcop.Project.deploy_protocol_rules` — D5-c4 (ADR-0006).

The deployment writes the bundled FCoP protocol rules host-neutrally to
**four** locations so any agent host can pick them up:

    .cursor/rules/fcop-rules.mdc       # Cursor IDE
    .cursor/rules/fcop-protocol.mdc    # Cursor IDE
    AGENTS.md                          # Codex / Devin / generic
    CLAUDE.md                          # Claude Code CLI

These tests pin:

    * Layout — exactly those 4 paths, with the right content shape.
    * Byte-exactness of the `.mdc` files (Cursor needs the YAML
      frontmatter intact).
    * Host-neutral copies (`AGENTS.md` / `CLAUDE.md`) are byte-identical
      to each other, frontmatter-stripped, and carry both rules + protocol
      version markers.
    * Works on an *uninitialized* directory — per docstring this method
      doesn't require ``fcop.json``, so it stays usable as a recovery tool.
    * Force/archive/skip semantics match the role-template deploy: default
      ``force=True archive=True`` archives prior content under
      ``.fcop/migrations/<ts>/rules/``; ``force=False`` records pre-existing
      files in ``report.skipped``.
    * Idempotence — repeated default deploys leave on-disk content stable.
    * ``init(deploy_rules=True)`` integration — the kwarg actually fans
      out the protocol-rule deploy as part of project init.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fcop import Project
from fcop.rules import (
    get_protocol_commentary,
    get_protocol_version,
    get_rules,
    get_rules_version,
)

# ── Expected layout constants ────────────────────────────────────────

_EXPECTED_RELS = (
    ".cursor/rules/fcop-rules.mdc",
    ".cursor/rules/fcop-protocol.mdc",
    "AGENTS.md",
    "CLAUDE.md",
)


# ── Layout + content ─────────────────────────────────────────────────


class TestDeploymentLayout:
    def test_four_expected_targets(self, tmp_path: Path) -> None:
        project = Project(tmp_path)
        report = project.deploy_protocol_rules()

        # Exactly the four canonical paths, in the documented order.
        deployed_rels = tuple(
            p.relative_to(tmp_path).as_posix() for p in report.deployed
        )
        assert deployed_rels == _EXPECTED_RELS

        # Every deployed path is absolute, exists, and is non-empty.
        for path in report.deployed:
            assert path.is_absolute()
            assert path.is_file()
            assert path.stat().st_size > 0

    def test_mdc_files_byte_for_byte(self, tmp_path: Path) -> None:
        # Cursor relies on the YAML frontmatter (alwaysApply: true).
        # If we ever silently rewrite it we silently break Cursor — so
        # the .mdc deploys must be byte-identical to the bundled wheel.
        project = Project(tmp_path)
        project.deploy_protocol_rules()

        on_disk_rules = (
            tmp_path / ".cursor" / "rules" / "fcop-rules.mdc"
        ).read_text(encoding="utf-8")
        on_disk_protocol = (
            tmp_path / ".cursor" / "rules" / "fcop-protocol.mdc"
        ).read_text(encoding="utf-8")

        assert on_disk_rules == get_rules()
        assert on_disk_protocol == get_protocol_commentary()

    def test_agents_and_claude_are_byte_identical(
        self, tmp_path: Path
    ) -> None:
        # Per ADR-0006 we duplicate the host-neutral payload between
        # AGENTS.md and CLAUDE.md because Codex reads one and Claude
        # Code reads the other and neither falls back. They must stay
        # bit-equal.
        project = Project(tmp_path)
        project.deploy_protocol_rules()

        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
        claude = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert agents == claude

    def test_host_neutral_content_shape(self, tmp_path: Path) -> None:
        # AGENTS.md / CLAUDE.md must:
        #   * NOT start with the Cursor YAML frontmatter (Codex / Claude
        #     Code don't parse it and would render `alwaysApply: true`
        #     as visible noise),
        #   * include both the rules-version and protocol-version
        #     markers in a small banner so agents on those hosts can
        #     still see what shipped,
        #   * include a chunk of the rules body and the protocol body.
        project = Project(tmp_path)
        project.deploy_protocol_rules()

        agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

        # No raw Cursor frontmatter leaked through.
        assert not agents.startswith("---\nalwaysApply:")
        assert "alwaysApply: true" not in agents.splitlines()[:5]

        # The host-neutral preamble lands first (sentinel from
        # _HOST_NEUTRAL_PREAMBLE in project.py).
        assert agents.startswith(
            "# FCoP Protocol Rules · agent-host-neutral copy"
        )

        # Both versions appear in the banner.
        rules_v = get_rules_version()
        protocol_v = get_protocol_version()
        assert rules_v in agents
        assert protocol_v in agents

        # Rules body and protocol body are both folded in. We can't
        # assert the *exact* concatenation because frontmatter
        # stripping varies, but the H1s of both source documents
        # should still appear.
        assert "# FCoP Rules" in agents  # from fcop-rules.mdc body

    def test_report_tuple_types(self, tmp_path: Path) -> None:
        # Frozen-dataclass contract: deployed/skipped/archived are
        # tuples (hashable, immutable). Same as deploy_role_templates.
        project = Project(tmp_path)
        report = project.deploy_protocol_rules()
        assert isinstance(report.deployed, tuple)
        assert isinstance(report.skipped, tuple)
        assert isinstance(report.archived, tuple)


# ── No-init + recovery-tool semantics ────────────────────────────────


class TestUninitializedProject:
    def test_works_without_fcop_json(self, tmp_path: Path) -> None:
        # Per docstring: deploy_protocol_rules does not read or
        # require fcop.json. This is the explicit recovery-tool
        # contract from ADR-0006. We verify by deploying onto a bare
        # directory and confirming nothing about init() was needed.
        project = Project(tmp_path)
        assert project.is_initialized() is False

        report = project.deploy_protocol_rules()

        assert len(report.deployed) == 4
        # We did NOT magically initialize the project as a side-effect.
        assert project.is_initialized() is False
        assert not (tmp_path / "docs" / "agents" / "fcop.json").exists()


# ── Force / archive / skip ───────────────────────────────────────────


class TestForceAndSkip:
    def test_default_archives_existing_rules_file(
        self, tmp_path: Path
    ) -> None:
        # First plant a stale .cursor/rules/fcop-rules.mdc.
        cursor_dir = tmp_path / ".cursor" / "rules"
        cursor_dir.mkdir(parents=True)
        stale_path = cursor_dir / "fcop-rules.mdc"
        stale_path.write_text("# stale rules\n", encoding="utf-8")

        # Default deploy = force=True, archive=True.
        report = Project(tmp_path).deploy_protocol_rules()

        # The fresh file overwrote the stale one.
        assert stale_path.read_text(encoding="utf-8") == get_rules()

        # The stale content was preserved under .fcop/migrations/<ts>/rules/.
        assert report.migration_dir is not None
        archived = (
            report.migration_dir / ".cursor" / "rules" / "fcop-rules.mdc"
        )
        assert archived.is_file()
        assert archived.read_text(encoding="utf-8") == "# stale rules\n"
        assert archived in report.archived

    def test_force_no_archive_overwrites_silently(
        self, tmp_path: Path
    ) -> None:
        # archive=False + force=True: stale file is *destroyed*, not
        # archived. Useful for callers (CI / one-shot bootstraps) that
        # know there are no local edits worth preserving.
        agents_path = tmp_path / "AGENTS.md"
        agents_path.write_text("# stale agents\n", encoding="utf-8")

        report = Project(tmp_path).deploy_protocol_rules(
            force=True, archive=False
        )

        # New content on disk; stale gone without trace.
        assert agents_path.read_text(encoding="utf-8").startswith(
            "# FCoP Protocol Rules"
        )
        assert report.migration_dir is None
        assert report.archived == ()

    def test_no_force_skips_existing(self, tmp_path: Path) -> None:
        # Plant a custom AGENTS.md that the user has hand-edited.
        agents_path = tmp_path / "AGENTS.md"
        agents_path.write_text("# user-authored\n", encoding="utf-8")

        report = Project(tmp_path).deploy_protocol_rules(force=False)

        # Custom file is untouched.
        assert agents_path.read_text(encoding="utf-8") == "# user-authored\n"
        # And it's recorded as skipped, not deployed.
        assert agents_path in report.skipped
        assert agents_path not in report.deployed
        # No migration dir since nothing was archived.
        assert report.migration_dir is None
        # The other three targets *did* deploy normally — partial
        # protection of one file shouldn't block the rest.
        assert len(report.deployed) == 3

    def test_idempotent_repeated_default_deploys(
        self, tmp_path: Path
    ) -> None:
        # Two back-to-back default deploys (force=True, archive=True):
        # the second deploy archives the first deploy's content; final
        # on-disk state matches the bundle.
        project = Project(tmp_path)
        project.deploy_protocol_rules()
        project.deploy_protocol_rules()

        # Final state matches the bundle.
        on_disk = (
            tmp_path / ".cursor" / "rules" / "fcop-rules.mdc"
        ).read_text(encoding="utf-8")
        assert on_disk == get_rules()

        # Two migration directories now exist under .fcop/migrations/.
        migrations_root = tmp_path / ".fcop" / "migrations"
        assert migrations_root.is_dir()
        stamps = [p for p in migrations_root.iterdir() if p.is_dir()]
        assert len(stamps) >= 1  # at least one (timestamps may collide)


# ── init(deploy_rules=True) integration ──────────────────────────────


class TestInitDeployRulesKwarg:
    """:meth:`Project.init` accepts ``deploy_rules=True`` (added in
    0.6.3) which folds the protocol-rule deploy into project init.
    """

    def test_init_with_deploy_rules_writes_all_four(
        self, tmp_path: Path
    ) -> None:
        project = Project(tmp_path)
        project.init(team="dev-team", deploy_rules=True)

        # Standard init artifacts.
        assert project.is_initialized() is True

        # Plus all four protocol-rule targets.
        for rel in _EXPECTED_RELS:
            assert (tmp_path / rel).is_file(), (
                f"init(deploy_rules=True) did not write {rel!r}"
            )

    def test_init_default_does_not_deploy_rules(
        self, tmp_path: Path
    ) -> None:
        # Default init (deploy_rules=False) leaves the four targets
        # absent — the kwarg has to be opt-in or we'd surprise users
        # who already manage .cursor/rules / AGENTS.md by hand.
        project = Project(tmp_path)
        project.init(team="dev-team")
        for rel in _EXPECTED_RELS:
            assert not (tmp_path / rel).exists(), (
                f"default init unexpectedly wrote {rel!r}"
            )


# ── Error paths ──────────────────────────────────────────────────────


class TestErrors:
    def test_no_lang_kwarg(self, tmp_path: Path) -> None:
        # Unlike deploy_role_templates, deploy_protocol_rules has no
        # team/lang knobs — the protocol is single-language by design.
        # If anyone tries to pass them, that's a TypeError, surfaced
        # by Python's keyword-arg machinery.
        project = Project(tmp_path)
        with pytest.raises(TypeError):
            project.deploy_protocol_rules(lang="zh")  # type: ignore[call-arg]
