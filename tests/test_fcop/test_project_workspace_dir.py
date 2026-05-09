"""``Project()`` workspace-root resolution and v1.0 layout detect.

Phase 2 of ADR-0022 introduces a ``workspace_dir=`` constructor
parameter and four auto-detect outcomes for the workspace root:

1. ``fcop/`` exists                   → use it (v1.0 default), no warn
2. only ``docs/agents/`` exists       → use it + DeprecationWarning
3. both exist                         → :class:`ConfigError`
4. neither exists                     → default to ``fcop/`` (v1.0)

Plus the explicit override path:

5. ``workspace_dir=`` (relative or absolute) wins unconditionally,
   never warns, and works even when nothing exists on disk yet.

These are the "freshly-init'd v1.0 project", "0.7.x project that
hasn't migrated yet", "half-migrated project that needs human
attention", and "novel layout (e.g. monorepo)" scenarios respectively.
The library MUST distinguish them at construction time so downstream
code (and the CLI's ``migrate-workspace``) never has to guess.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import pytest

from fcop import Project
from fcop.errors import ConfigError


# ── Auto-detect: 4 canonical scenarios ────────────────────────────────


class TestAutoDetect:
    """Auto-detect runs when ``workspace_dir=`` is not provided."""

    def test_v1_root_when_fcop_exists(self, tmp_path: Path) -> None:
        # Scenario 1: a v1.0 project (``fcop/`` already present).
        # Detect must pick it without warning.
        (tmp_path / "fcop").mkdir()
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # promote to error so we
            # actually catch any DeprecationWarning regression.
            project = Project(tmp_path)
        assert project.workspace_dir == (tmp_path / "fcop").resolve()
        assert project.workspace_layout == "v1"

    def test_legacy_root_when_only_docs_agents_exists(
        self, tmp_path: Path
    ) -> None:
        # Scenario 2: 0.7.x project — must still work but warn loudly
        # so users actually run the migrator at some point.
        (tmp_path / "docs" / "agents").mkdir(parents=True)
        with pytest.warns(DeprecationWarning, match="0.7.x-style"):
            project = Project(tmp_path)
        assert project.workspace_dir == (
            tmp_path / "docs" / "agents"
        ).resolve()
        assert project.workspace_layout == "legacy"

    def test_both_exist_raises_config_error(self, tmp_path: Path) -> None:
        # Scenario 3: half-migrated repo. Refuse to guess. The error
        # message must point at the explicit-override escape hatch
        # so the user has a clear next step.
        (tmp_path / "fcop").mkdir()
        (tmp_path / "docs" / "agents").mkdir(parents=True)
        with pytest.raises(ConfigError, match="workspace_dir"):
            Project(tmp_path)

    def test_neither_exists_defaults_to_v1(self, tmp_path: Path) -> None:
        # Scenario 4: empty directory — the v1.0 default wins. No
        # DeprecationWarning (we are not falling back to a legacy
        # layout, we are committing to the new default).
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            project = Project(tmp_path)
        assert project.workspace_dir == (tmp_path / "fcop").resolve()
        assert project.workspace_layout == "v1"


# ── Explicit override ─────────────────────────────────────────────────


class TestExplicitOverride:
    """``workspace_dir=`` always wins."""

    def test_relative_path(self, tmp_path: Path) -> None:
        # Relative paths resolve against the project root, mirroring
        # the rest of the library's path-handling contract.
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            project = Project(tmp_path, workspace_dir="custom-ws")
        assert project.workspace_dir == (tmp_path / "custom-ws").resolve()
        assert project.workspace_layout == "explicit"

    def test_absolute_path(self, tmp_path: Path) -> None:
        # Absolute paths are taken as-is (resolved). This supports
        # monorepo / out-of-tree workspace setups.
        target = tmp_path / "elsewhere" / "ws"
        target.mkdir(parents=True)
        project = Project(tmp_path, workspace_dir=target)
        assert project.workspace_dir == target.resolve()
        assert project.workspace_layout == "explicit"

    def test_explicit_docs_agents_silences_warning(
        self, tmp_path: Path
    ) -> None:
        # Pinning to ``docs/agents`` deliberately is the永久 escape
        # hatch — projects that prefer to stay on the 0.7.x layout
        # can do so without the noise.
        (tmp_path / "docs" / "agents").mkdir(parents=True)
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # any DeprecationWarning fails
            project = Project(tmp_path, workspace_dir="docs/agents")
        assert project.workspace_dir == (
            tmp_path / "docs" / "agents"
        ).resolve()
        assert project.workspace_layout == "explicit"

    def test_explicit_overrides_double_layout_conflict(
        self, tmp_path: Path
    ) -> None:
        # Even when both ``fcop/`` and ``docs/agents/`` exist,
        # explicit ``workspace_dir=`` resolves the ambiguity — that
        # is the documented escape hatch from the ConfigError.
        (tmp_path / "fcop").mkdir()
        (tmp_path / "docs" / "agents").mkdir(parents=True)
        project = Project(tmp_path, workspace_dir="fcop")
        assert project.workspace_dir == (tmp_path / "fcop").resolve()
        assert project.workspace_layout == "explicit"


# ── Path properties follow workspace_dir ──────────────────────────────


class TestPathPropertiesFollowWorkspace:
    """All ``*_dir`` / ``config_path`` properties must derive from
    ``workspace_dir`` so the same Project instance points at exactly
    one workspace, period."""

    @pytest.mark.parametrize(
        "ws_kw, ws_subpath",
        [
            ({}, "fcop"),  # v1.0 default
            ({"workspace_dir": "docs/agents"}, "docs/agents"),
            ({"workspace_dir": "monorepo/agents"}, "monorepo/agents"),
        ],
    )
    def test_subdirectories_derive_from_workspace(
        self, tmp_path: Path, ws_kw: dict[str, str], ws_subpath: str
    ) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            project = Project(tmp_path, **ws_kw)
        ws = (tmp_path / ws_subpath).resolve()
        assert project.workspace_dir == ws
        assert project.tasks_dir == ws / "tasks"
        assert project.reports_dir == ws / "reports"
        assert project.issues_dir == ws / "issues"
        assert project.shared_dir == ws / "shared"
        assert project.log_dir == ws / "log"
        assert project.reviews_dir == ws / "reviews"
        assert project.config_path == ws / "fcop.json"


# ── is_initialized respects workspace_dir ─────────────────────────────


class TestIsInitializedHonoursWorkspace:
    """``is_initialized()`` checks ``workspace_dir/fcop.json`` —
    fcop.json under the *other* layout must not count, otherwise the
    half-migrated case (scenario 3) silently slips through."""

    def test_fresh_v1_with_fcop_json(self, tmp_path: Path) -> None:
        cfg = tmp_path / "fcop" / "fcop.json"
        cfg.parent.mkdir(parents=True)
        cfg.write_text("{}", encoding="utf-8")
        assert Project(tmp_path).is_initialized() is True

    def test_legacy_with_fcop_json(self, tmp_path: Path) -> None:
        cfg = tmp_path / "docs" / "agents" / "fcop.json"
        cfg.parent.mkdir(parents=True)
        cfg.write_text("{}", encoding="utf-8")
        with pytest.warns(DeprecationWarning):
            assert Project(tmp_path).is_initialized() is True

    def test_explicit_workspace_does_not_inherit_fcop_json(
        self, tmp_path: Path
    ) -> None:
        # User explicitly opts into ``custom-ws`` even though
        # ``fcop/fcop.json`` exists. The explicit choice wins; the
        # other layout's fcop.json must not be picked up.
        v1 = tmp_path / "fcop" / "fcop.json"
        v1.parent.mkdir(parents=True)
        v1.write_text("{}", encoding="utf-8")
        project = Project(tmp_path, workspace_dir="custom-ws")
        assert project.is_initialized() is False


# ── init() lands artifacts under the resolved workspace_dir ───────────


class TestInitUnderExplicitWorkspace:
    """End-to-end check that init() honours ``workspace_dir=``.

    This is the regression-prevention test for ADR-0022 Phase 2: any
    future code path that re-introduces a hard-coded ``docs/agents/``
    will fail here because the artifact will land in the wrong
    directory."""

    def test_init_solo_under_custom_workspace(self, tmp_path: Path) -> None:
        project = Project(tmp_path, workspace_dir="custom-ws")
        project.init_solo(role_code="ME", lang="zh")
        assert (tmp_path / "custom-ws" / "fcop.json").is_file()
        assert (tmp_path / "custom-ws" / "tasks").is_dir()
        assert (tmp_path / "custom-ws" / "reports").is_dir()
        assert (tmp_path / "custom-ws" / "log").is_dir()
        # And nothing under the v1.0 default — proving the override
        # actually kept artifacts off the standard path.
        assert not (tmp_path / "fcop").exists()
        assert not (tmp_path / "docs" / "agents").exists()
