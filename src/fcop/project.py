"""The :class:`Project` facade — the main entry point of the fcop library.

A :class:`Project` represents one FCoP-managed directory on disk. It is
the only public class that performs side effects; every method that
creates, modifies, archives, or reads files goes through a ``Project``
instance.

See adr/ADR-0001-library-api.md for the full API contract and invariants.

Implementation status: D3 in progress. Identity / path properties,
``is_initialized``, ``config``, and ``status`` are implemented. Task /
report / issue CRUD, ``init*``, and deployment still raise
:class:`NotImplementedError` — they land in D3-c2 and D4.
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import os
import pathlib
import warnings
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, cast

if TYPE_CHECKING:
    from fcop.inspection import InspectionReport, Violation

import yaml

from fcop.core.boundary import (
    lookup_capability,
    validate_action,
)
from fcop.core.config import load_team_config, save_team_config
from fcop.core.events import (
    WATCHER_ID,
    WatcherState,
    compute_diff,
    make_event,
    scan_workspace,
)
from fcop.core.filename import (
    ISSUE_FILENAME_RE,
    REPORT_FILENAME_RE,
    REVIEW_FILENAME_RE,
    REVIEW_SUBJECT_SHORT_RE,
    TASK_FILENAME_RE,
    ReviewFilename,
    build_issue_filename,
    build_report_filename,
    build_review_filename,
    build_task_filename,
    next_sequence,
    parse_issue_filename,
    parse_report_filename,
    parse_review_filename,
    parse_task_filename,
    today_iso,
)
from fcop.core.frontmatter import (
    FRONTMATTER_DELIMITER,
    assemble_review_file,
    assemble_task_file,
    parse_frontmatter_raw,
    parse_review_frontmatter,
    parse_task_frontmatter,
    split_frontmatter,
)
from fcop.core.jsonschema_validator import (
    validate_envelope_frontmatter,
)
from fcop.core.recovery import (
    build_recovery_record,
    make_abort_artifact,
    make_escalate_artifact,
    make_resume_payload,
    make_retry_plan,
    make_rollback_plan,
    parse_session_id,
)
from fcop.core.schema import (
    PROTOCOL_NAME,
    PROTOCOL_VERSION,
    is_valid_role_code,
    normalize_priority,
    normalize_risk_level,
    normalize_severity,
    validate_role_code,
)
from fcop.errors import (
    BoundaryViolationError,
    ProjectAlreadyInitializedError,
    ProtocolViolation,
    TaskNotFoundError,
    TeamNotFoundError,
    ValidationError,
)
from fcop.models import (
    BoundaryViolation,
    DeploymentReport,
    DriftEntry,
    DriftReport,
    Event,
    EventSource,
    EventSourceKind,
    EventType,
    Failure,
    FailureReceipt,
    HumanApproval,
    HumanApprovalChannel,
    HumanApprovalDecision,
    HumanApprovalEvidence,
    Issue,
    Priority,
    ProjectStatus,
    RecentActivityEntry,
    Recovery,
    RecoveryAction,
    RecoveryOutcome,
    Report,
    Review,
    ReviewDecision,
    ReviewSubjectType,
    RiskLevel,
    RoleOccupancy,
    SessionRecoveryAction,
    SessionRecoveryResult,
    SessionRoleConflict,
    Severity,
    Task,
    TaskFrontmatter,
    TeamConfig,
    ValidationIssue,
)
from fcop.rules import (
    get_internal_readme,
    get_letter,
    get_protocol_commentary,
    get_protocol_version,
    get_rules,
    get_rules_version,
)
from fcop.teams import TeamTemplate, get_team_info, get_template

__all__ = ["Project", "EventSubscription"]


@dataclass(slots=True)
class EventSubscription:
    """A handle returned by :meth:`Project.subscribe_events`（v1.0）。

    Attributes:
        project: 反向引用，便于 :meth:`unsubscribe` 操作 registry。
        types: 关心的事件类型元组；``None`` = 所有 12 类。
        callback: 事件回调；``None`` 表示静默订阅。
    """

    project: Project
    types: tuple[EventType, ...] | None
    callback: Callable[[Event], None] | None
    _active: bool = True

    def unsubscribe(self) -> None:
        """Stop receiving further events. Idempotent."""
        if not self._active:
            return
        self._active = False
        with contextlib.suppress(ValueError):
            self.project._subscriptions.remove(self)

    @property
    def active(self) -> bool:
        return self._active


class Project:
    """Represents an FCoP-managed project rooted at a filesystem path.

    Constructing a :class:`Project` does **not** touch the filesystem.
    Use :meth:`is_initialized` to check whether the project has been set
    up, and :meth:`init` (or :meth:`init_solo` / :meth:`init_custom`) to
    create the directory structure and configuration.

    Args:
        path: Absolute or relative path to the project root. When the
              project is initialized, this directory will contain
              ``docs/agents/`` with the FCoP layout inside.
        strict: If ``True`` (the default), every operation validates
                against FCoP rules and raises
                :class:`~fcop.errors.ProtocolViolation` on any breach.
                If ``False``, best-effort mode — useful for migration
                tools that need to read malformed legacy files.

    Thread safety:
        A :class:`Project` instance maintains no mutable state other
        than a per-call config cache. Multiple instances for different
        paths are independent and safe to use concurrently. Concurrent
        writers to the *same* path rely on filesystem ``rename()``
        atomicity; the :meth:`write_task` method retries on sequence
        number collisions.
    """

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        strict: bool = True,
        workspace_dir: str | os.PathLike[str] | None = None,
    ) -> None:
        """Bind a :class:`Project` instance to ``path``.

        Args:
            path: Project root.
            strict: Validation toggle (see class docstring).
            workspace_dir: Override the workspace root location. Either
                a relative path (resolved against ``path``) or an
                absolute path. ``None`` triggers v1.0 auto-detect:
                  - if ``<path>/fcop/`` exists  → use it (v1.0 default)
                  - if only ``<path>/docs/agents/`` exists → use it
                    + emit ``DeprecationWarning`` (per ADR-0022)
                  - if both exist                → raise
                    :class:`ConfigError`
                  - if neither exists            → default to
                    ``<path>/fcop/`` (v1.0 fresh-init layout)
                Passing the string ``"docs/agents"`` (or
                ``"docs/agents/"``) explicitly is the永久 escape
                hatch — it is legal even in v2.x — and never emits
                the DeprecationWarning since the choice is intentional.
        """
        self._path = pathlib.Path(path).resolve()
        self._strict = strict
        self._workspace_root, self._workspace_layout = (
            self._resolve_workspace_root(workspace_dir)
        )
        # FCoP 3.0 dual-topology detection (per ADR-0035 + ADR-0039
        # Freeze Discipline). The detector is pure inspection and
        # never raises; the result is cached as a lightweight
        # TopologyReport instance for the lifetime of the Project.
        # All v3-aware properties (lifecycle_root, inbox_dir,
        # active_dir, …) and the v3 mode toggle in core write
        # methods read from this cache.
        from fcop.lifecycle.detect import detect_topology as _detect

        self._topology = _detect(
            self._path, workspace_root=self._workspace_root
        )

    def _resolve_workspace_root(
        self,
        explicit: str | os.PathLike[str] | None,
    ) -> tuple[pathlib.Path, str]:
        """Decide the workspace root and tag the layout.

        Returns ``(absolute_path, layout)`` where ``layout`` is one of:
          - ``"v1"``      — ``<root>/fcop/`` (v1.0 default)
          - ``"legacy"``  — ``<root>/docs/agents/`` (0.7.x layout,
                            auto-detected; emits DeprecationWarning)
          - ``"explicit"``— caller-supplied path (no warning, no
                            assumption about layout shape)

        Per ADR-0022 §"启动时 detect 行为".
        """
        if explicit is not None:
            ws = pathlib.Path(explicit)
            ws = (self._path / ws).resolve() if not ws.is_absolute() else ws.resolve()
            return ws, "explicit"

        v1_root = self._path / "fcop"
        legacy_root = self._path / "docs" / "agents"
        v1_exists = v1_root.exists()
        legacy_exists = legacy_root.exists()

        if v1_exists and legacy_exists:
            from fcop.errors import ConfigError as _ConfigError

            raise _ConfigError(
                f"both {v1_root.relative_to(self._path).as_posix()!r} and "
                f"{legacy_root.relative_to(self._path).as_posix()!r} "
                "exist under the project root. FCoP refuses to guess. "
                "Either remove one, or pass `workspace_dir=` "
                "explicitly to disambiguate. See ADR-0022 §'启动时 "
                "detect 行为'.",
                path=self._path,
            )

        if v1_exists:
            return v1_root.resolve(), "v1"

        if legacy_exists:
            warnings.warn(
                f"{legacy_root.relative_to(self._path).as_posix()!r} is "
                "the 0.7.x-style FCoP workspace. v1.0 default is "
                f"{v1_root.relative_to(self._path).as_posix()!r}. Run "
                "`fcop migrate-workspace --apply` to migrate, or "
                "pass `workspace_dir=\"docs/agents\"` to silence "
                "this warning. See ADR-0022.",
                DeprecationWarning,
                stacklevel=3,
            )
            return legacy_root.resolve(), "legacy"

        # Neither exists — assume fresh v1.0 init.
        return v1_root.resolve(), "v1"

    # ── Identity ──────────────────────────────────────────────────────

    @property
    def path(self) -> pathlib.Path:
        """Absolute, resolved path to the project root."""
        return self._path

    @property
    def tasks_dir(self) -> pathlib.Path:
        """Directory holding open (created-but-not-yet-claimed) tasks.

        * v2 projects: ``<workspace>/tasks/``
        * v3 projects: ``<workspace>/_lifecycle/inbox/`` (the v3
          equivalent of "open inbox of tasks"; per FCoP 3.0 spec
          §1.2, ``inbox`` is the canonical name for *created* tasks
          that have not yet been claimed)

        This property is the v2→v3 compatibility shim. CodeFlow and
        any other v2-era caller continues to read ``project.tasks_dir``
        and the right physical directory is returned. New code SHOULD
        prefer :attr:`inbox_dir` for v3-explicit clarity; a future
        release will mark ``tasks_dir`` as ``DeprecationWarning``
        once that switch is mechanical.
        """
        if self.is_v3:
            return self._workspace_root / "_lifecycle" / "inbox"
        return self._workspace_root / "tasks"

    @property
    def reports_dir(self) -> pathlib.Path:
        """``<workspace>/reports/`` (same path in v2 and v3 — per spec §1.1)."""
        return self._workspace_root / "reports"

    @property
    def issues_dir(self) -> pathlib.Path:
        """``<workspace>/issues/`` (same path in v2 and v3 — per spec §1.1)."""
        return self._workspace_root / "issues"

    @property
    def shared_dir(self) -> pathlib.Path:
        """``<workspace>/shared/`` (same path in v2 and v3)."""
        return self._workspace_root / "shared"

    @property
    def log_dir(self) -> pathlib.Path:
        """``<workspace>/log/`` (archive root; v2 only).

        In v3 projects this directory does not exist by protocol —
        the v3 equivalent of archived tasks is :attr:`archive_dir`
        (``_lifecycle/archive/``), and archived reports/issues live
        directly under :attr:`reports_dir` / :attr:`issues_dir`.
        The property still returns a path so v2-era code that
        constructs paths under ``log_dir`` (without touching disk)
        continues to type-check; callers that actually read from
        the directory will get an empty / missing result on v3
        projects, which is the correct v3 behaviour.
        """
        return self._workspace_root / "log"

    # ── FCoP 3.0 lifecycle properties ─────────────────────────────────
    #
    # These are present on every Project but only meaningful when
    # is_v3 is True. They are computed lazily from the workspace
    # root so they remain valid even before _lifecycle/ is created
    # by ensure_lifecycle_dirs() — callers can resolve paths first
    # and create directories second.

    @property
    def topology(self) -> str:
        """The detected protocol topology: ``"v2"``, ``"v3"``,
        ``"empty"``, or ``"mixed"``.

        Computed once at construction time via
        :func:`fcop.lifecycle.detect.detect_topology`. The cached
        :class:`fcop.lifecycle.detect.TopologyReport` is available
        as :attr:`topology_report` for callers that need the
        structured detail (notes, v2_dirs_present, etc.).
        """
        return self._topology.topology.value

    @property
    def topology_report(self):  # type: ignore[no-untyped-def]
        """The full :class:`fcop.lifecycle.detect.TopologyReport`.

        Untyped here to avoid leaking the lifecycle type into the
        public Project signature in environments that import Project
        without fcop.lifecycle (which is permitted but unusual).
        Real callers can ``isinstance``-check or pull the attribute
        names they need.
        """
        return self._topology

    @property
    def is_v3(self) -> bool:
        """``True`` if this project's workspace is in the v3
        (``_lifecycle/``) topology — *and* not in the half-migrated
        MIXED state. MIXED returns ``False`` because v3 semantics
        cannot be safely enforced over an ambiguous tree; callers
        get v2 behaviour and a topology-level diagnostic via
        :attr:`topology_report`.
        """
        return self.topology == "v3"

    @property
    def lifecycle_root(self) -> pathlib.Path:
        """``<workspace>/_lifecycle/`` — the FCoP 3.0 state root.

        Per spec §1.1, this is the directory whose 5 immediate
        children (``inbox``/``active``/``review``/``done``/``archive``)
        ARE the protocol's NOW truth. Returns the path unconditionally
        — even on v2 projects — so v3-aware tooling can compute the
        target of a future migration without re-deriving it.
        """
        return self._workspace_root / "_lifecycle"

    @property
    def inbox_dir(self) -> pathlib.Path:
        """``<workspace>/_lifecycle/inbox/`` — v3 created tasks (spec §1.2)."""
        return self.lifecycle_root / "inbox"

    @property
    def active_dir(self) -> pathlib.Path:
        """``<workspace>/_lifecycle/active/`` — v3 claimed tasks (spec §1.2)."""
        return self.lifecycle_root / "active"

    @property
    def review_dir(self) -> pathlib.Path:
        """``<workspace>/_lifecycle/review/`` — v3 pending confirmation (spec §1.2)."""
        return self.lifecycle_root / "review"

    @property
    def done_dir(self) -> pathlib.Path:
        """``<workspace>/_lifecycle/done/`` — v3 completed tasks (spec §1.2)."""
        return self.lifecycle_root / "done"

    @property
    def archive_dir(self) -> pathlib.Path:
        """``<workspace>/_lifecycle/archive/`` — v3 closed tasks (spec §1.2).

        In v3 this replaces v2's ``log/tasks/`` for closed-task
        archival. Reports and issues are *not* archived in v3 — they
        live directly under :attr:`reports_dir` / :attr:`issues_dir`
        (per FCoP 3.0 spec §1.1 + ADR-0039 Freeze Discipline).
        """
        return self.lifecycle_root / "archive"

    @property
    def workspace_dir(self) -> pathlib.Path:
        """FCoP workspace root.

        v1.0 default is ``<project>/fcop/``; 0.7.x legacy projects keep
        ``<project>/docs/agents/`` (with a DeprecationWarning at
        construction time). Caller can override via the
        ``workspace_dir=`` constructor arg.
        """
        return self._workspace_root

    @property
    def workspace_layout(self) -> str:
        """``"v1"`` / ``"legacy"`` / ``"explicit"`` — see
        :meth:`_resolve_workspace_root`."""
        return self._workspace_layout

    @property
    def reviews_dir(self) -> pathlib.Path:
        """``<workspace>/reviews/`` —— REVIEW envelopes (v1.0,
        per ADR-0017)."""
        return self._workspace_root / "reviews"

    @property
    def config_path(self) -> pathlib.Path:
        """``<workspace>/fcop.json``.

        The presence of this file is the canonical signal that a project
        has been initialized — see :meth:`is_initialized`.
        """
        return self._workspace_root / "fcop.json"

    @property
    def _migrations_dir(self) -> pathlib.Path:
        """``<project>/.fcop/migrations/`` — destination for archived
        conflicts during ``init(force=True)`` and template redeploys.

        Private because the exact ``.fcop/`` layout is an internal
        implementation detail that may change between minor releases.
        """
        return self._path / ".fcop" / "migrations"

    @property
    def _proposals_dir(self) -> pathlib.Path:
        """``<project>/.fcop/proposals/`` — inbox for out-of-band
        notes AI roles drop for ADMIN (typically protocol-level
        disagreements that don't fit the task/report/issue flow).

        Private for the same reason as :attr:`_migrations_dir`: the
        exact ``.fcop/`` layout is an implementation detail.
        """
        return self._path / ".fcop" / "proposals"

    # ── Lifecycle ─────────────────────────────────────────────────────

    def is_initialized(self) -> bool:
        """``True`` if ``docs/agents/fcop.json`` exists under the root.

        This is a pure filesystem probe — it does not validate the
        contents of ``fcop.json``. Use :attr:`config` to actually parse
        the configuration (which will raise :class:`ConfigError` if the
        file is present but malformed).
        """
        return self.config_path.is_file()

    def init(
        self,
        *,
        team: str = "dev-team",
        lang: str = "zh",
        force: bool = False,
        deploy_rules: bool = False,
        deploy_role_templates: bool = True,
        deploy_internal_template: bool = False,
    ) -> ProjectStatus:
        """Initialize this directory as an FCoP project with a preset team.

        Creates the ``docs/agents/{tasks,reports,issues,shared,log}/``
        tree and writes ``fcop.json``. Role template deployment, Cursor
        rule installation, and the welcome task are intentionally
        decoupled — call :meth:`deploy_role_templates` and
        :meth:`deploy_protocol_rules` after init, or pass
        ``deploy_rules=True`` here to fold the second one in.

        Args:
            team: Name of a bundled preset team. See
                  :func:`fcop.teams.get_available_teams` for the list.
            lang: ``"zh"`` or ``"en"`` — informational only at this
                  point; influences nothing that ``init`` writes
                  today, but is persisted into ``fcop.json`` so later
                  template deployment picks it up.
            force: If ``True``, allow overwriting an existing
                   ``fcop.json``; the old file is archived to
                   ``.fcop/migrations/<timestamp>/`` before the new
                   one lands. Destructive — defaults to ``False``.
            deploy_rules: If ``True``, also drop the bundled protocol
                rules into the project root via
                :meth:`deploy_protocol_rules` (writes
                ``.cursor/rules/*.mdc``, ``AGENTS.md``, and
                ``CLAUDE.md``). **Defaults to ``False``** to keep
                pure-library users' behaviour identical to 0.6.2 —
                they may not want the project root touched. The
                ``fcop-mcp`` ``init_project`` tool overrides this to
                ``True`` so MCP-driven inits get rules on disk
                automatically. See ADR-0006 for the rationale.
            deploy_role_templates: If ``True`` (the default since
                0.6.4), automatically materialise the team's
                three-layer documentation under
                ``docs/agents/shared/`` via
                :meth:`deploy_role_templates`. This used to be a
                separate post-init step in 0.6.3, which led to the
                "team switched but `shared/roles/` is empty" pitfall
                — agents on the new team had no role charter to
                read. Solo and the four bundled multi-role teams all
                have templates; ``init_custom`` users with no
                bundled templates pass ``False``.
            deploy_internal_template: If ``True``, also create the
                ``fcop/internal/`` bucket (Rule 4.6 / ADR-0034 §4.3,
                introduced in fcop@2.0.0) with a ``README.md`` carrying
                the ``internal-only`` declaration block v1. **Defaults
                to ``False``** because Rule 4.6 is a non-mandatory
                soft convention — projects that don't need a
                team-internal archive bucket stay clean. Existing
                projects on fcop ≥2.0.0 can opt in retroactively by
                running ``Project.init(force=True,
                deploy_internal_template=True)`` or invoking the new
                ``deploy_internal_template()`` MCP tool (when shipped).

        Returns:
            A :class:`ProjectStatus` snapshot of the freshly initialized
            project.

        Raises:
            ProjectAlreadyInitializedError: ``fcop.json`` exists and
                ``force=False``.
            TeamNotFoundError: ``team`` is not in the bundled registry.
            ValueError: ``team == "solo"`` — Solo has its own
                dedicated entry point (:meth:`init_solo`) that pins
                ``mode="solo"`` rather than ``"preset"``. Using
                ``init`` for solo would silently mislabel the project.
        """
        if team == "solo":
            raise ValueError(
                "init() is for preset multi-role teams; "
                "use init_solo(role_code=...) for solo mode so the "
                "config carries mode='solo' not mode='preset'."
            )
        info = get_team_info(team)
        cfg = TeamConfig(
            mode="preset",
            team=info.name,
            leader=info.leader,
            roles=info.roles,
            lang=lang,
            version=PROTOCOL_VERSION,
            extra={
                "display_name": info.display_name,
                "created_at": _now_iso(),
            },
        )
        self._apply_init(cfg, force=force)
        if deploy_rules:
            # Use force=force so an init(force=True, deploy_rules=True)
            # is internally consistent; archive defaults to True so
            # any pre-existing local rule edits survive in
            # .fcop/migrations/.
            self.deploy_protocol_rules(force=force, archive=True)
        if deploy_role_templates:
            # force=True so that an init(force=True) overwrite re-deploys
            # the team's three-layer docs (any stale per-role files from
            # the previous team get archived under .fcop/migrations/).
            # Graceful fallback when the team has no bundled templates
            # (shouldn't happen for a preset team, but defence in depth).
            # ``lang=None`` lets ``deploy_role_templates`` re-read the
            # canonical lang from the just-written ``fcop.json`` —
            # avoids re-validating a free-form ``str`` against the
            # ``Literal["zh", "en"]`` parameter at the boundary.
            with contextlib.suppress(TeamNotFoundError, ValueError):
                self.deploy_role_templates(
                    team=info.name, lang=None, force=True
                )
        if deploy_internal_template:
            self._deposit_internal_template(cfg.lang, force=force)
        return self.status()

    def init_solo(
        self,
        *,
        role_code: str = "ME",
        lang: str = "zh",
        force: bool = False,
        deploy_rules: bool = False,
        deploy_role_templates: bool = True,
        deploy_internal_template: bool = False,
    ) -> ProjectStatus:
        """Initialize in Solo mode (single role interfacing with ADMIN).

        Solo mode is for individual users who want FCoP's file
        discipline without a multi-agent team. Exactly one role is
        registered (default ``"ME"``); it doubles as the leader.

        Args:
            role_code: The one role that writes in this project.
                Must match the role grammar (uppercase, ASCII,
                optionally hyphenated). ``ADMIN`` / ``SYSTEM`` are
                rejected because solo mode is about AI authorship —
                ADMIN is already implied as the human counterpart.
            lang: Persisted into ``fcop.json`` for later template
                deployment; ignored by ``init_solo`` itself.
            force: Same semantics as :meth:`init`.
            deploy_rules: Same semantics as :meth:`init` —
                defaults to ``False`` to preserve pure-library
                behaviour; the MCP layer flips this to ``True``.
            deploy_role_templates: Same semantics as :meth:`init` —
                defaults to ``True`` since 0.6.4. The bundled
                ``solo`` team carries its own three-layer docs
                (``README`` / ``TEAM-ROLES`` /
                ``TEAM-OPERATING-RULES`` / ``roles/{role_code}.md``),
                deployed under ``docs/agents/shared/``. The bundled
                role file is named ``ME.md`` (matching the default
                role code); when ``role_code`` differs, the file is
                still deployed as ``roles/ME.md`` and the agent
                reads it as a role-charter template even though the
                runtime role code is different. (A future release
                may rename on deploy; for 0.6.4 we keep the simpler
                "exact bundled filename" path.)
            deploy_internal_template: Same semantics as :meth:`init` —
                defaults to ``False``. Rule 4.6's ``fcop/internal/``
                bucket is non-mandatory soft convention; opt in only
                if your solo workflow needs a team-internal archive
                (per ADR-0034 §4.3, fcop@2.0.0+).

        Raises:
            ValidationError: ``role_code`` fails
                :func:`fcop.core.schema.validate_role_code`
                (strict — reserved roles rejected).
            ProjectAlreadyInitializedError: see :meth:`init`.
        """
        issues = validate_role_code(role_code, field="role_code")
        errors = [i for i in issues if i.severity == "error"]
        if errors:
            raise ValidationError(
                f"invalid role_code {role_code!r} for solo mode",
                issues=errors,
            )

        cfg = TeamConfig(
            mode="solo",
            team="solo",
            leader=role_code,
            roles=(role_code,),
            lang=lang,
            version=PROTOCOL_VERSION,
            extra={"created_at": _now_iso()},
        )
        self._apply_init(cfg, force=force)
        if deploy_rules:
            self.deploy_protocol_rules(force=force, archive=True)
        if deploy_role_templates:
            # The bundled `solo` team has roles=("ME",); when the user
            # picks a different role_code we still deploy ME.md so the
            # agent has a role charter to read. Graceful fallback for
            # any future team-data drift. ``lang=None`` defers to the
            # config we just wrote (avoids re-narrowing ``str`` →
            # ``Literal["zh", "en"]`` at the call site).
            with contextlib.suppress(TeamNotFoundError, ValueError):
                self.deploy_role_templates(
                    team="solo", lang=None, force=True
                )
        if deploy_internal_template:
            self._deposit_internal_template(cfg.lang, force=force)
        return self.status()

    def init_custom(
        self,
        *,
        team_name: str,
        roles: Sequence[str],
        leader: str,
        lang: str = "zh",
        force: bool = False,
        deploy_rules: bool = False,
        deploy_role_templates: bool = False,
        deploy_internal_template: bool = False,
    ) -> ProjectStatus:
        """Initialize with a user-defined role set.

        Equivalent to the legacy ``create_custom_team()`` tool. Call
        :meth:`validate_team` first to surface any naming or
        structural issues without writing files — the checks here are
        identical, they just raise :class:`ValidationError` on failure
        instead of returning a list.

        Args:
            team_name: Human-readable team slug written into
                ``fcop.json`` (``"my-custom-squad"``). Free-form
                string; only non-emptiness is enforced.
            roles: Ordered sequence of role codes registered on this
                team. Must include ``leader``.
            leader: Role code of the team's leader — the one recipient
                ``ADMIN``-addressed tasks default to.
            lang: Persisted for later template deployment.
            force: Same semantics as :meth:`init`.
            deploy_rules: Same semantics as :meth:`init` —
                defaults to ``False`` to preserve pure-library
                behaviour; the MCP layer flips this to ``True``.
            deploy_role_templates: Defaults to ``False`` because a
                custom team has no bundled three-layer documents to
                deploy. The agent is expected to read
                ``fcop://teams/<bundled-team>`` as a sample and
                hand-author the project's own ``shared/{TEAM-README,
                TEAM-ROLES, TEAM-OPERATING-RULES}.md`` plus
                ``shared/roles/{ROLE}.md`` per the protocol. Setting
                this to ``True`` would raise
                :class:`TeamNotFoundError` since ``team_name`` is
                user-defined — kept as an option for symmetry only.
            deploy_internal_template: Same semantics as :meth:`init` —
                defaults to ``False``. Custom teams may opt in if
                they want Rule 4.6's ``fcop/internal/`` bucket
                (per ADR-0034 §4.3, fcop@2.0.0+).

        Raises:
            ValidationError: the team config is invalid. The raised
                exception's ``.issues`` list mirrors what
                :meth:`validate_team` returns.
        """
        issues = Project.validate_team(roles=roles, leader=leader)
        errors = [i for i in issues if i.severity == "error"]
        if errors:
            raise ValidationError(
                "invalid custom team config",
                issues=errors,
            )
        if not team_name.strip():
            raise ValidationError(
                "team_name must not be empty",
                issues=[
                    ValidationIssue(
                        severity="error",
                        field="team_name",
                        message="team_name must be a non-empty string",
                    )
                ],
            )

        cfg = TeamConfig(
            mode="custom",
            team=team_name,
            leader=leader,
            roles=tuple(roles),
            lang=lang,
            version=PROTOCOL_VERSION,
            extra={"created_at": _now_iso()},
        )
        self._apply_init(cfg, force=force)
        if deploy_rules:
            self.deploy_protocol_rules(force=force, archive=True)
        if deploy_internal_template:
            self._deposit_internal_template(cfg.lang, force=force)
        return self.status()

    @staticmethod
    def validate_team(
        *,
        roles: Sequence[str],
        leader: str,
    ) -> list[ValidationIssue]:
        """Dry-run validation of a custom team config.

        Does not touch the filesystem. Checks:

        * ``roles`` is non-empty.
        * Each role code matches
          :data:`fcop.core.schema.ROLE_CODE_RE` and is not reserved
          (``ADMIN`` / ``SYSTEM`` cannot be assigned to AI roles).
        * Authority words like ``BOSS`` produce a stylistic
          ``warning`` issue (non-fatal — callers can elect to proceed).
        * ``roles`` has no duplicates.
        * ``leader`` appears in ``roles``.

        Returns:
            A list of :class:`ValidationIssue` — empty when the config
            is clean. Callers render the list to the user; callers
            that prefer exceptions can filter to ``severity=="error"``
            and raise themselves.
        """
        issues: list[ValidationIssue] = []

        if not roles:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="roles",
                    message="roles must be a non-empty sequence",
                )
            )
            return issues

        seen: set[str] = set()
        for i, code in enumerate(roles):
            field = f"roles[{i}]"
            issues.extend(validate_role_code(code, field=field))
            if code in seen:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        field=field,
                        message=f"duplicate role code {code!r}",
                    )
                )
            else:
                seen.add(code)

        if not is_valid_role_code(leader):
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="leader",
                    message=(
                        f"leader {leader!r} is not a valid role code "
                        "(must be uppercase ASCII, optionally hyphenated)"
                    ),
                )
            )
        elif leader not in seen:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="leader",
                    message=(
                        f"leader {leader!r} must appear in the roles list"
                    ),
                )
            )

        return issues

    def _apply_init(self, cfg: TeamConfig, *, force: bool) -> None:
        """Shared I/O for ``init`` / ``init_solo`` / ``init_custom``.

        Order of operations:

        1. Check for pre-existing ``fcop.json``. If present and
           ``force=False``, refuse.
        2. Create the canonical directory tree even in the force path;
           this is idempotent (``mkdir(parents=True, exist_ok=True)``).
        3. If forcing, archive the old ``fcop.json`` into
           ``.fcop/migrations/<timestamp>/`` *before* the atomic swap —
           losing the old config silently would be a data hazard.
        4. Atomic write of the new config (``save_team_config``
           uses tmp-then-replace internally).
        5. Deposit the protocol's promised on-disk artifacts:
           ``LETTER-TO-ADMIN.md`` (the user manual) and the
           ``workspace/`` cage with its README. These are baked into
           ``fcop-rules.mdc`` Rule 1 Phase 1 / Rule 7.5 — every
           ``init_*`` call promises them to ADMIN, so the lifecycle
           method materializes them rather than leaving the promise
           unredeemed (the 0.6.3 bug we fixed in 0.6.4).

        Private because the exact sequencing is an implementation
        detail; callers use the high-level ``init*`` methods.
        """
        config_path = self.config_path
        already = config_path.is_file()
        if already and not force:
            raise ProjectAlreadyInitializedError(
                f"fcop.json already exists at {config_path}; "
                "pass force=True to overwrite (the old file will be "
                "archived under .fcop/migrations/)."
            )

        # FCoP 3.0 default topology (per spec §1.1 / §6):
        #   _lifecycle/{inbox,active,review,done,archive}/  ← state buckets
        #   reports/  issues/  shared/                      ← retained from v2
        # v2's tasks/ is superseded by _lifecycle/inbox/.
        # v2's log/   is removed; archive/ + report-in-place takes over.
        from fcop.lifecycle.state import ensure_lifecycle_dirs as _ensure_lifecycle_dirs

        _ensure_lifecycle_dirs(self._workspace_root)
        # Refresh the cached topology now that _lifecycle/ exists, so
        # that property accessors (is_v3, tasks_dir, log_dir, …) see
        # the freshly-initialised v3 layout instead of the pre-init
        # "empty" snapshot taken in __init__.
        from fcop.lifecycle.detect import detect_topology as _detect

        self._topology = _detect(
            self._path, workspace_root=self._workspace_root
        )
        for directory in (
            self.reports_dir,
            self.issues_dir,
            self.shared_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

        if already and force:
            timestamp = _now_iso().replace(":", "").replace("-", "")
            migration_dir = self._migrations_dir / timestamp
            migration_dir.mkdir(parents=True, exist_ok=True)
            archive_path = migration_dir / "fcop.json"
            config_path.replace(archive_path)

        save_team_config(cfg, config_path)

        self._deposit_letter(cfg.lang, force=force)
        self._deposit_workspace_cage(force=force)

    def _deposit_letter(self, lang: str, *, force: bool) -> None:
        """Write ``docs/agents/LETTER-TO-ADMIN.md`` from the bundled
        manual.

        Falls back to ``zh`` if the configured ``lang`` isn't a
        bundled letter language — :func:`fcop.rules.get_letter` is
        the source of truth for which languages exist, but a custom
        ``lang`` (say a future ``ja``) shouldn't crash init.
        """
        try:
            content = get_letter(lang)  # type: ignore[arg-type]
        except ValueError:
            content = get_letter("zh")

        target = self._workspace_root / "LETTER-TO-ADMIN.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            return
        if target.exists() and force:
            self._archive_one_file(target, sub="letter")
        target.write_text(content, encoding="utf-8", newline="\n")

    def _deposit_workspace_cage(self, *, force: bool) -> None:
        """Create ``workspace/`` + ``workspace/README.md`` per Rule 7.5.

        The ``workspace/`` directory is the protocol's "cage for
        actual work products" — keeping it created up-front matches
        the user-facing promise in ``LETTER-TO-ADMIN.md`` ("起完之后
        会落下这些东西") and gives agents a directory they can write
        into without an extra ``new_workspace`` round-trip.
        """
        workspace_dir = self._path / "workspace"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        readme = workspace_dir / "README.md"
        if readme.exists() and not force:
            return
        if readme.exists() and force:
            self._archive_one_file(readme, sub="workspace")
        readme.write_text(_WORKSPACE_README_TEXT, encoding="utf-8", newline="\n")

    def _deposit_internal_template(self, lang: str, *, force: bool) -> None:
        """Create ``fcop/internal/`` + ``README.md`` per Rule 4.6 (opt-in).

        Rule 4.6 (per ADR-0034 §4.3, fcop@2.0.0+) introduces the
        ``fcop/internal/`` bucket as a **non-mandatory soft convention**
        for team-internal archive material (emergence-log,
        self-disclosure, decision-trail, upstream-issue drafts).

        Only deposited when the caller explicitly opts in via
        ``deploy_internal_template=True`` on any of the ``init_*``
        methods — the default is ``False`` so existing projects remain
        untouched.

        The README template carries the ``internal-only`` declaration
        block v1 (per ADR-0034 §4.3) and substitutes ``{fcop_version}``
        / ``{deployed_at}`` placeholders so the deposit is dated and
        tied to a fcop version.

        Falls back to ``zh`` if the configured ``lang`` isn't a
        bundled language — mirrors :meth:`_deposit_letter`.
        """
        try:
            template = get_internal_readme(lang)  # type: ignore[arg-type]
        except ValueError:
            template = get_internal_readme("zh")

        from fcop import __version__ as _fcop_version

        content = template.format(
            fcop_version=_fcop_version,
            deployed_at=_now_iso(),
        )

        internal_dir = self._workspace_root / "internal"
        internal_dir.mkdir(parents=True, exist_ok=True)
        readme = internal_dir / "README.md"
        if readme.exists() and not force:
            return
        if readme.exists() and force:
            self._archive_one_file(readme, sub="internal")
        readme.write_text(content, encoding="utf-8", newline="\n")

    def _archive_one_file(
        self, path: pathlib.Path, *, sub: str
    ) -> pathlib.Path:
        """Move *path* into ``.fcop/migrations/<timestamp>/<sub>/``.

        Used by ``_deposit_letter`` and ``_deposit_workspace_cage`` to
        preserve hand-edited copies before overwriting on
        ``init(force=True)``. Mirrors the archival pattern in
        :meth:`deploy_protocol_rules` / :meth:`deploy_role_templates`.
        """
        stamp = _now_iso().replace(":", "").replace("-", "")
        target_dir = self._migrations_dir / stamp / sub
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / path.name
        path.replace(target)
        return target

    # ── Template deployment ───────────────────────────────────────────

    def deploy_role_templates(
        self,
        *,
        team: str | None = None,
        lang: Literal["zh", "en"] | None = None,
        force: bool = True,
    ) -> DeploymentReport:
        """Deploy the three-layer team documentation under ``docs/agents/shared/``.

        Writes the bundled :class:`TeamTemplate` content to disk so
        every assigned agent can read its own role charter *inside the
        repo* without pulling anything from the network:

        .. code-block:: text

            docs/agents/shared/
            ├── TEAM-README.md              # layer 0 — team positioning
            ├── TEAM-README.en.md
            ├── TEAM-ROLES.md               # layer 1 — role boundaries
            ├── TEAM-ROLES.en.md
            ├── TEAM-OPERATING-RULES.md     # layer 2 — ops rules
            ├── TEAM-OPERATING-RULES.en.md
            └── roles/
                ├── {ROLE}.md               # layer 3 — role charter
                └── {ROLE}.en.md

        Both ``zh`` and ``en`` variants are always deployed so agents
        switching language mid-project never hit a missing file; the
        ``lang`` argument only decides which copy is *primary* (today
        that's recorded in :attr:`TeamConfig.lang` rather than
        influencing layout).

        Args:
            team: Team slug. If ``None``, reads from :attr:`config`.
                The project must be initialized in that case.
            lang: Language tag. If ``None``, reads from :attr:`config`.
                Only ``"zh"`` / ``"en"`` are bundled.
            force: When ``True`` (the default, matching 0.5.x
                behavior), any existing file that would be overwritten
                is first archived to
                ``.fcop/migrations/<timestamp>/shared/<rel>`` so
                ADMIN can diff or restore manually. When ``False``,
                existing files are skipped and recorded in
                :attr:`DeploymentReport.skipped`; this is the
                conservative mode suitable for partial redeploys.

        Returns:
            :class:`DeploymentReport` listing every path written,
            skipped, and archived. ``migration_dir`` is set only when
            at least one file was archived.

        Raises:
            ConfigError: team/lang not provided and the project is
                not initialized (so they can't be read from config).
            TeamNotFoundError: resolved team is not a bundled preset.
            ValueError: resolved lang is not supported.
        """
        resolved_team, resolved_lang = self._resolve_team_and_lang(team, lang)

        deployed: list[pathlib.Path] = []
        skipped: list[pathlib.Path] = []
        archived: list[pathlib.Path] = []
        migration_dir: pathlib.Path | None = None

        shared = self.shared_dir
        shared.mkdir(parents=True, exist_ok=True)
        (shared / "roles").mkdir(parents=True, exist_ok=True)

        # Load *both* language variants — see the docstring: mixed-lang
        # projects shouldn't hit a missing file when an agent opens
        # the "other" file by hand. `lang` parameter still matters for
        # which one is authoritative per config but both land on disk.
        bundles: dict[str, TeamTemplate] = {
            "zh": get_template(resolved_team, "zh"),
            "en": get_template(resolved_team, "en"),
        }

        plan = _plan_template_deployment(bundles)

        for rel_path, content in plan:
            target = shared / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)

            if target.exists():
                if not force:
                    skipped.append(target)
                    continue
                # force=True: archive before overwrite so the author
                # of the old file can get it back.
                if migration_dir is None:
                    stamp = _now_iso().replace(":", "").replace("-", "")
                    migration_dir = self._migrations_dir / stamp / "shared"
                    migration_dir.mkdir(parents=True, exist_ok=True)
                archive_target = migration_dir / rel_path
                archive_target.parent.mkdir(parents=True, exist_ok=True)
                target.replace(archive_target)
                archived.append(archive_target)

            target.write_text(content, encoding="utf-8", newline="\n")
            deployed.append(target)

        # `lang` is threaded through to the return value by recording
        # it (indirectly) in the files deployed; the report itself
        # carries only paths, which is enough for callers to decide
        # what to log/display.
        _ = resolved_lang
        return DeploymentReport(
            deployed=tuple(deployed),
            skipped=tuple(skipped),
            archived=tuple(archived),
            migration_dir=migration_dir,
        )

    def _resolve_team_and_lang(
        self,
        team: str | None,
        lang: Literal["zh", "en"] | None,
    ) -> tuple[str, Literal["zh", "en"]]:
        """Fill in ``team`` / ``lang`` from :attr:`config` when missing.

        Extracted so :meth:`deploy_role_templates` reads linearly and
        the "default from config" policy is easy to test in isolation
        later. :attr:`config` is only read when at least one argument
        is ``None`` — explicit calls with both supplied never touch
        the filesystem here.
        """
        if team is not None and lang is not None:
            _ensure_lang_supported(lang)
            return team, lang

        cfg = self.config  # raises ConfigError if not initialized
        resolved_team = team if team is not None else cfg.team
        # cfg.lang is a plain str on TeamConfig; narrow it to the
        # Literal only after _ensure_lang_supported has vouched for it.
        raw_lang: str = lang if lang is not None else cfg.lang
        _ensure_lang_supported(raw_lang)
        # Safe cast: _ensure_lang_supported guarantees raw_lang ∈ _DEPLOY_LANGS.
        return resolved_team, raw_lang  # type: ignore[return-value]

    # ── Protocol rule distribution (host-neutral) ─────────────────────

    def deploy_protocol_rules(
        self,
        *,
        force: bool = True,
        archive: bool = True,
    ) -> DeploymentReport:
        """Deploy the FCoP protocol rules to the project root, host-neutrally.

        Writes the bundled :file:`fcop-rules.mdc` and
        :file:`fcop-protocol.mdc` to **four** locations so any agent
        host that the project runs under can pick them up:

        .. code-block:: text

            <root>/.cursor/rules/fcop-rules.mdc       # Cursor IDE auto-injects
            <root>/.cursor/rules/fcop-protocol.mdc    # Cursor IDE auto-injects
            <root>/AGENTS.md                          # Codex / Cursor / Devin / generic
            <root>/CLAUDE.md                          # Claude Code CLI

        The two ``.mdc`` files keep their original content byte-for-byte
        (including the YAML frontmatter ``alwaysApply: true`` Cursor
        relies on). ``AGENTS.md`` and ``CLAUDE.md`` carry the same
        normative content as a single concatenated markdown file with
        the YAML frontmatter stripped — Codex and Claude Code don't
        understand the Cursor frontmatter and would otherwise render it
        as visible noise. ``AGENTS.md`` and ``CLAUDE.md`` are
        byte-identical; we duplicate because Claude Code reads
        ``CLAUDE.md`` and most everyone else reads ``AGENTS.md``.

        Per ADR-0006 (host-neutral rule distribution) this is the
        canonical path for getting protocol rules into a project. Use
        it in two situations:

        * On project creation, if the user wants protocol rules on
          disk immediately. The :meth:`init` family takes a
          ``deploy_rules=True`` kwarg that delegates here.
        * On package upgrade, after ``pip install -U fcop`` (or
          ``-U fcop-mcp``), to refresh on-disk copies to the newly
          packaged versions. The MCP layer exposes this as
          ``redeploy_rules``.

        Per ADR-0001 §"Rule 8" agents must NOT call this method
        themselves — only ADMIN does, explicitly. The fcop-mcp tool
        gates this with an explicit redeploy contract.

        Args:
            force: ``True`` (the default) overwrites any existing copy.
                ``False`` skips files that already exist and records
                them in :attr:`DeploymentReport.skipped`.
            archive: When ``True`` (the default) and ``force=True``,
                any file that would be overwritten is first moved to
                :file:`.fcop/migrations/<timestamp>/rules/<rel>` so
                ADMIN can diff or roll back. ``False`` skips archiving
                — destructive, only sensible when callers are sure
                the project has no local edits.

        Returns:
            :class:`DeploymentReport` listing every path written,
            skipped, and archived. ``migration_dir`` points to the
            archive root iff at least one file was archived.

        Notes:
            This method does **not** read or require ``fcop.json`` —
            it works on any directory, initialized or not. That keeps
            it usable as a manual recovery tool.
        """
        deployed: list[pathlib.Path] = []
        skipped: list[pathlib.Path] = []
        archived: list[pathlib.Path] = []
        migration_dir: pathlib.Path | None = None

        plan = _plan_protocol_rules_deployment()

        for rel_path, content in plan:
            target = self._path / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)

            if target.exists():
                if not force:
                    skipped.append(target)
                    continue
                if archive:
                    if migration_dir is None:
                        stamp = _now_iso().replace(":", "").replace("-", "")
                        migration_dir = self._migrations_dir / stamp / "rules"
                        migration_dir.mkdir(parents=True, exist_ok=True)
                    archive_target = migration_dir / rel_path
                    archive_target.parent.mkdir(parents=True, exist_ok=True)
                    target.replace(archive_target)
                    archived.append(archive_target)
                # archive=False + force=True: just overwrite without
                # archiving. The atomic-write below replaces in place.

            target.write_text(content, encoding="utf-8", newline="\n")
            deployed.append(target)

        return DeploymentReport(
            deployed=tuple(deployed),
            skipped=tuple(skipped),
            archived=tuple(archived),
            migration_dir=migration_dir,
        )

    # ── Config ────────────────────────────────────────────────────────

    @property
    def config(self) -> TeamConfig:
        """Read-only snapshot of ``docs/agents/fcop.json``.

        Re-read from disk on each access so external mutations are
        visible. This property has no caching guarantees; if you need
        to repeatedly inspect the config, capture it into a local.

        Raises:
            ConfigError: ``fcop.json`` is missing, unreadable, not valid
                JSON, or fails structural validation. The raised error's
                ``.path`` attribute points at ``config_path``.
        """
        return load_team_config(self.config_path)

    # ── Status ────────────────────────────────────────────────────────

    def status(self) -> ProjectStatus:
        """Return counts and recent activity for this project.

        Safe to call on an uninitialized project: in that case every
        count is ``0``, ``config`` is ``None``, and ``recent_activity``
        is empty. Never raises for a missing directory — only for
        invalid ``fcop.json`` contents (via :attr:`config`).
        """
        initialized = self.is_initialized()
        cfg: TeamConfig | None = self.config if initialized else None

        tasks_open = _count_matching(self.tasks_dir, TASK_FILENAME_RE)
        reports_count = _count_matching(self.reports_dir, REPORT_FILENAME_RE)
        issues_count = _count_matching(self.issues_dir, ISSUE_FILENAME_RE)
        tasks_archived = _count_matching(
            self.log_dir / "tasks", TASK_FILENAME_RE
        )

        recent = _collect_recent_activity(
            tasks_dir=self.tasks_dir,
            reports_dir=self.reports_dir,
            issues_dir=self.issues_dir,
            limit=_RECENT_ACTIVITY_LIMIT,
        )

        return ProjectStatus(
            path=self._path,
            is_initialized=initialized,
            config=cfg,
            tasks_open=tasks_open,
            tasks_archived=tasks_archived,
            reports_count=reports_count,
            issues_count=issues_count,
            recent_activity=recent,
        )

    def role_occupancy(self) -> tuple[RoleOccupancy, ...]:
        """Per-role occupancy snapshot derived from the on-disk ledger.

        Returns one :class:`RoleOccupancy` per role declared in
        ``fcop.json``, plus an entry per role that appears in the
        ledger but is not declared (so ADMIN can spot stale role
        codes from a previous team layout).

        Counts are computed by parsing **filenames only** —
        frontmatter is read solely to recover the optional
        ``session_id`` field of the most recent file. Bodies are never
        read, which makes this method safe to call from an UNBOUND
        session where Rule 1 forbids reading task bodies.

        On an uninitialized project an empty tuple is returned.

        Backs the "Role occupancy" section of `fcop_report()`'s
        UNBOUND output (since ``fcop_protocol_version: 1.5.0``,
        fcop-mcp 0.7.0). Agents consult this section to detect the
        double-bind scenario described in
        ``ISSUE-20260427-002-ME.md`` before transitioning to BOUND.
        """
        if not self.is_initialized():
            return ()

        cfg = self.config
        assert cfg is not None

        # Parse all filenames once — cheap and avoids repeated regex
        # compilations across every role.
        # v2 → v3 archive location:
        #   v2: log/tasks/  log/reports/
        #   v3: _lifecycle/archive/  (single bucket; tasks + reports
        #       co-located, classifier handles split)
        if self.is_v3:
            archive_root = self._workspace_root / "_lifecycle" / "archive"
            active_tasks = _parse_dir_files(self.tasks_dir, parse_task_filename)
            archived_tasks = _parse_dir_files(archive_root, parse_task_filename)
            active_reports = _parse_dir_files(
                self.reports_dir, parse_report_filename
            )
            archived_reports = _parse_dir_files(archive_root, parse_report_filename)
        else:
            active_tasks = _parse_dir_files(self.tasks_dir, parse_task_filename)
            archived_tasks = _parse_dir_files(
                self.log_dir / "tasks", parse_task_filename
            )
            active_reports = _parse_dir_files(
                self.reports_dir, parse_report_filename
            )
            archived_reports = _parse_dir_files(
                self.log_dir / "reports", parse_report_filename
            )
        active_issues = _parse_dir_files(
            self.issues_dir, parse_issue_filename
        )

        seen_roles: set[str] = set()
        occupancies: list[RoleOccupancy] = []

        # Honor the order from fcop.json so output is deterministic
        # and ADMIN sees teammates in the documented order.
        for role in cfg.roles:
            seen_roles.add(role)
            occupancies.append(
                _build_role_occupancy(
                    role,
                    active_tasks,
                    archived_tasks,
                    active_reports,
                    archived_reports,
                    active_issues,
                )
            )

        # Surface any "ghost" roles that show up in files but not in
        # fcop.json — those are exactly the situations Rule 1's role
        # uniqueness clause helps ADMIN catch (e.g., team layout was
        # changed but stale tasks remained on disk).
        ledger_roles: set[str] = set()
        for parsed_list in (
            active_tasks,
            archived_tasks,
            active_reports,
            archived_reports,
            active_issues,
        ):
            for _path, parsed in parsed_list:
                ledger_roles |= _roles_in_parsed(parsed)
        for role in sorted(ledger_roles - seen_roles - _RESERVED_ROLES):
            occupancies.append(
                _build_role_occupancy(
                    role,
                    active_tasks,
                    archived_tasks,
                    active_reports,
                    archived_reports,
                    active_issues,
                )
            )

        return tuple(occupancies)

    def audit_drift(self) -> DriftReport:
        """Cross-reference ``git status`` and frontmatter against the FCoP ledger.

        Two independent post-hoc audits surface here:

        1. **Working-tree drift** (Rule 0.a.1, since 1.8.0). Calls
           ``git status --porcelain`` from the project root and removes
           every entry whose path lives under the FCoP ledger
           directories (``docs/agents/{tasks,reports,issues,log}``).
           Whatever remains is — by definition — work that landed
           without going through the four-step task→do→report→archive
           cycle, e.g. raw ``echo > foo.md``, IDE-side edits, `git
           commit -am` from a peer process, or files dropped by
           sub-agents that bypassed the toolchain entirely.

        2. **Session/role conflicts** (Rule 1, since 1.8.0). Walks
           every ``TASK-*.md`` / ``REPORT-*.md`` / ``ISSUE-*.md`` under
           both active and archive directories, parses frontmatter
           for ``session_id``, and groups files by session. Any
           ``session_id`` that signed files under more than one role
           code is direct evidence of sub-agent role impersonation —
           one session = one role binding, period.

        This is **detection, not prevention**. The protocol itself
        cannot prevent an agent from spawning a sub-process and
        writing whatever it wants; what FCoP can do is make the
        evidence loud and unmissable by the next ``fcop_report()`` /
        ``fcop_check()`` call. Prevention still depends on the agent
        honouring Rule 0.a.1 + Rule 1.

        Returns:
            A :class:`DriftReport`. ``git_available`` is ``False``
            when ``git`` is not installed or this is not a git repo;
            in that case ``entries`` is empty and the caller should
            note the limitation, but ``session_role_conflicts`` still
            works since it does not depend on git.
        """
        entries: list[DriftEntry] = []
        git_available = True

        try:
            import subprocess

            result = subprocess.run(
                ["git", "status", "--porcelain", "-z"],
                cwd=str(self._path),
                capture_output=True,
                text=False,
                check=False,
                timeout=15,
            )
        except (FileNotFoundError, OSError, subprocess.SubprocessError):
            git_available = False
            result = None

        if result is not None and result.returncode == 0:
            entries = list(
                _parse_git_porcelain(
                    result.stdout, self._path, _ledger_prefixes_for(self),
                )
            )
        elif result is not None:
            # ``git status`` ran but failed — most often because this
            # path is not a git repository. Treat the same as "git
            # unavailable" so callers see ``git_available=False`` and
            # know to surface the limitation.
            git_available = False

        # Filter to only the drift entries (outside ledger).
        drift_only = tuple(e for e in entries if not e.in_ledger)

        # ── Session ↔ role consistency audit ──────────────────────
        conflicts = _scan_session_role_conflicts(self)

        return DriftReport(
            entries=drift_only,
            session_role_conflicts=conflicts,
            git_available=git_available,
        )

    # ── Protocol audit (ADR-0032) ─────────────────────────────────────

    def audit(
        self,
        scope: Literal["new", "upgrade", "takeover", "auto"] = "auto",
        output: Literal["file", "stdout", "both"] = "file",
    ) -> InspectionReport:
        """Three-scenario protocol compliance audit (ADR-0032).

        Scans the project for protocol violations and generates an
        **INSPECTION report** that is both a compliance finding *and* a
        remediation plan (L3 format with Execution Block).

        Args:
            scope:  ``"new"`` — new project validation;
                    ``"upgrade"`` — post-version-upgrade validation;
                    ``"takeover"`` — legacy non-fcop project onboarding;
                    ``"auto"`` — infer from project state (recommended).
            output: ``"file"`` writes ``fcop/shared/INSPECTION-*.md``;
                    ``"stdout"`` returns Markdown only;
                    ``"both"`` writes file *and* returns Markdown.

        Returns:
            :class:`~fcop.inspection.InspectionReport` — call
            ``.to_markdown()`` or ``.to_dict()`` for the rendered output.

        Note:
            ``audit()`` is a **read-only deep scan**; the only side-effect
            is writing the INSPECTION file when ``output`` includes ``"file"``.
            It does *not* execute any remediation — that is for the human
            ADMIN/PM to do after reviewing the report.
        """
        from fcop.inspection import InspectionReport, OverallStatus

        resolved_scope = self._infer_audit_scope() if scope == "auto" else scope

        # Run all relevant scan_* methods, collect violations
        all_violations = []
        if resolved_scope in ("new", "upgrade", "takeover"):
            all_violations.extend(self._scan_cursor_rules())
            all_violations.extend(self._scan_shared_deployment())
            # FCoP 3.0 topology compliance — runs in every scope so a
            # fresh ``init_*`` self-check (``new``) catches missing
            # ``_lifecycle/`` immediately, before any work lands.
            all_violations.extend(
                self._scan_lifecycle_topology_compliance()
            )
        if resolved_scope in ("upgrade", "takeover"):
            all_violations.extend(self._scan_ghost_prefixes())
            all_violations.extend(self._scan_outdated_role_docs())
        if resolved_scope == "takeover":
            all_violations.extend(self._scan_misplaced_envelopes())
            all_violations.extend(self._scan_legacy_role_docs())
            all_violations.extend(self._scan_legacy_manifests())
        # Rule 4.6 (ADR-0034) — opt-in internal-only declaration audit.
        # Runs in every scope: the scan returns [] when the bucket is absent,
        # so it's effectively no-op for projects that haven't opted in.
        # P3 only, never blocks (see overall_status logic below).
        all_violations.extend(self._scan_internal_only_declarations())

        # Re-number violation IDs sequentially per severity
        all_violations = _renumber_violations(all_violations)

        # Determine overall status.
        # P3 (suggestion) violations *never* move the status off ``green`` —
        # they are non-blocking soft-convention nudges (Rule 4.6 + ADR-0034).
        has_p0 = any(v.severity == "P0" for v in all_violations)
        has_p1_or_p2 = any(
            v.severity in ("P1", "P2") for v in all_violations
        )
        overall: OverallStatus
        if has_p0:
            overall = "blocked"
        elif has_p1_or_p2:
            overall = "needs_remediation"
        else:
            overall = "green"

        import fcop as _fcop
        from fcop.rules import get_rules_version

        try:
            local_rules_version: str | None = _read_local_rules_version(self._path)
        except Exception:
            local_rules_version = None

        try:
            pkg_rules_version = get_rules_version()
        except Exception:
            pkg_rules_version = "unknown"

        inspection_id = self._allocate_inspection_id(resolved_scope)

        report = InspectionReport(
            inspection_id=inspection_id,
            scope=resolved_scope,  # type: ignore[arg-type]
            project_path=self._path,
            inspected_at=_dt.datetime.now(tz=_dt.timezone.utc),
            fcop_version=_fcop.__version__,
            fcop_rules_version_local=local_rules_version,
            fcop_rules_version_package=pkg_rules_version,
            overall_status=overall,
            violations=all_violations,
        )

        if output in ("file", "both"):
            shared = self.shared_dir
            shared.mkdir(parents=True, exist_ok=True)
            fname = f"{inspection_id}-{resolved_scope}.md"
            (shared / fname).write_text(
                report.to_markdown(), encoding="utf-8"
            )

        return report

    def _infer_audit_scope(self) -> str:
        """Infer scope from project state (conservative: prefer takeover)."""
        cfg_path = self.config_path
        if not cfg_path.exists():
            # If fcop/ directory already exists → legacy project → takeover
            if (self._path / "fcop").is_dir():
                return "takeover"
            # Truly empty or minimal dir → new
            file_count = sum(1 for _ in self._path.rglob("*") if _.is_file())
            return "new" if file_count < 5 else "takeover"
        # fcop.json exists — check for version lag
        try:
            import json as _json
            data = _json.loads(cfg_path.read_text(encoding="utf-8"))
            proto_ver = data.get("protocol_version", "")
            import fcop as _fcop
            if proto_ver and proto_ver < _fcop.__version__:
                return "upgrade"
        except Exception:
            pass
        return "takeover"

    def _allocate_inspection_id(self, scope: str) -> str:
        """Return next INSPECTION-YYYYMMDD-NNN id (sequential, no collision)."""
        shared = self.shared_dir
        today = _dt.date.today().strftime("%Y%m%d")
        prefix = f"INSPECTION-{today}-"
        existing = sorted(
            p.stem for p in shared.glob(f"{prefix}*.md")
            if p.stem.startswith(prefix)
        ) if shared.exists() else []
        if existing:
            try:
                last_n = int(existing[-1].split("-")[2])
            except (IndexError, ValueError):
                last_n = 0
        else:
            last_n = 0
        return f"{prefix}{last_n + 1:03d}"

    # ── scan_* methods ────────────────────────────────────────────────

    def _scan_cursor_rules(self) -> list[Violation]:
        """Detect missing protocol rules + stray non-protocol rules in .cursor/rules/."""
        from fcop.inspection import RemediationStep, Violation

        violations: list[Violation] = []
        rules_dir = self._path / ".cursor" / "rules"

        # SubCheck A: required protocol files
        required = {
            ".cursor/rules/fcop-rules.mdc",
            ".cursor/rules/fcop-protocol.mdc",
            "AGENTS.md",
            "CLAUDE.md",
        }
        missing = [
            r for r in sorted(required)
            if not (self._path / r).exists()
        ]
        if missing:
            violations.append(Violation(
                violation_id="P0-000",
                severity="P0",
                rule_violated="Rule 0 (协议规则缺失)",
                summary=f"{len(missing)} 件协议规则文件未部署",
                evidence=missing,
                impact="Agent 无法读取 fcop 协议规则，所有写盘行为均不受协议约束",
                scan_source="_scan_cursor_rules",
                remediation=[RemediationStep(
                    action="部署协议规则文件",
                    command="redeploy_rules()",
                    executor="ADMIN",
                    estimated_minutes=1,
                    tier=1,
                    rollback="旧规则已归档到 .fcop/migrations/<ts>/rules/，可手工恢复",
                )],
            ))

        # SubCheck B: stray non-protocol .mdc files
        if rules_dir.exists():
            protocol_mdc = {"fcop-rules.mdc", "fcop-protocol.mdc"}
            stray = [
                f.name for f in rules_dir.glob("*.mdc")
                if f.name not in protocol_mdc
            ]
            if stray:
                violations.append(Violation(
                    violation_id="P2-000",
                    severity="P2",
                    rule_violated="Rule 0 (草根规则混入)",
                    summary=f".cursor/rules/ 下有 {len(stray)} 件非协议 .mdc 文件",
                    evidence=[f".cursor/rules/{f}" for f in sorted(stray)],
                    impact="草根规则可能与 fcop 协议规则冲突，建议清理",
                    scan_source="_scan_cursor_rules",
                    remediation=[RemediationStep(
                        action="审查并归档草根 mdc 规则",
                        command="# 手工审查后移动到项目文档区或删除",
                        executor="ADMIN",
                        estimated_minutes=15,
                        tier=3,
                        rollback="git checkout -- .cursor/rules/",
                    )],
                ))

        return violations

    def _scan_shared_deployment(self) -> list[Violation]:
        """Check fcop/shared/ three-layer team document deployment completeness."""
        from fcop.errors import ConfigError
        from fcop.inspection import RemediationStep, Violation

        # 尝试读取 config；没有 fcop.json 的接管场景（takeover）也要检查基础文档
        cfg = None
        team_name = "dev-team"
        project_roles: tuple[str, ...] = ()
        try:
            cfg = self.config
            # solo 模式不要求三层团队文档（Rule 4.5 仅约束 team 模式）
            if cfg.mode == "solo":
                return []
            team_name = cfg.team
            project_roles = cfg.roles
        except ConfigError:
            # fcop.json 不存在（takeover 场景）：只检查 6 份基础文档，
            # 不检查角色文件（未知项目角色集）
            pass

        shared = self.shared_dir
        # 六份基础文档（双语）
        expected_base = [
            "TEAM-README.md", "TEAM-README.en.md",
            "TEAM-ROLES.md", "TEAM-ROLES.en.md",
            "TEAM-OPERATING-RULES.md", "TEAM-OPERATING-RULES.en.md",
        ]
        # 从 fcop.json 读取实际角色列表，支持两种命名约定（role.md / role-01.md）
        expected_roles = []
        for role in project_roles:
            if not (shared / f"roles/{role}-01.md").exists() and not (shared / f"roles/{role}.md").exists():
                expected_roles.append(f"roles/{role}.md")
        all_expected_count = len(expected_base) + len(project_roles)
        missing_base = [f for f in expected_base if not (shared / f).exists()]
        missing = missing_base + expected_roles  # expected_roles 已过滤，只含缺失项
        if not missing:
            return []

        ratio = len(missing) / all_expected_count
        from fcop.inspection import ViolationSeverity
        severity: ViolationSeverity = "P0" if ratio >= 0.5 else "P1"
        return [Violation(
            violation_id="P0-000" if severity == "P0" else "P1-000",
            severity=severity,
            rule_violated="Rule 4.5 (三层团队文档缺失)",
            summary=f"fcop/shared/ 缺少 {len(missing)}/{all_expected_count} 件团队文档",
            evidence=[f"fcop/shared/{f}" for f in missing],
            impact="团队职责边界、协作流程、升级路径缺失，agent 无法查阅角色定义",
            scan_source="_scan_shared_deployment",
            remediation=[RemediationStep(
                action="部署团队宪法文件",
                command=f'deploy_role_templates(team="{team_name}", force=True)',
                executor="ADMIN",
                estimated_minutes=1,
                tier=1,
                rollback="shared/ 原文件已备份（若 force=True 覆盖则需从包重新提取）",
            )],
        )]

    def _scan_misplaced_envelopes(self) -> list[Violation]:
        """Detect envelope files whose physical path contradicts their kind: frontmatter.

        **Exempt paths** (per ISSUE-20260513-008, fcop 2.0.0):

        - ``fcop/log/**``                    — archived envelopes (legitimate)
        - ``fcop/**/_archive/**``            — team-local archives (Rule 2 soft layout)
        - ``fcop/**/legacy-non-protocol/**`` — pre-FCoP imports (kept for forensics)
        - ``fcop/.git/**`` / ``fcop/.tmp/**`` — VCS / scratch (always skipped)

        Files under these paths are skipped because their kind: frontmatter
        is a *historical* claim, not a *current* routing key — they shouldn't
        be physically in tasks/reports/issues/reviews dirs.
        """
        from fcop.inspection import RemediationStep, Violation

        bucket_map = {
            "task": self.tasks_dir,
            "report": self.reports_dir,
            "issue": self.issues_dir,
            "review": self.reviews_dir,
        }
        fcop_root = self._path / "fcop"
        if not fcop_root.exists():
            return []

        misplaced: list[str] = []
        for md in fcop_root.rglob("*.md"):
            if _is_audit_exempt_path(md, fcop_root):
                continue
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")
                fm = _extract_frontmatter_kind(text)
                if fm not in bucket_map:
                    continue
                expected_dir = bucket_map[fm]
                if md.parent.resolve() != expected_dir.resolve():
                    misplaced.append(str(md.relative_to(self._path)))
            except Exception:
                continue

        if not misplaced:
            return []

        # Group by kind for a cleaner remediation command
        ps_lines = "\n".join(
            f"git mv '{f}' 'fcop/reports/{pathlib.Path(f).name}'"
            for f in misplaced[:5]
        ) + ("\n# ... 更多文件" if len(misplaced) > 5 else "")

        return [Violation(
            violation_id="P1-000",
            severity="P1",
            rule_violated="Rule 2 (桶错位)",
            summary=f"{len(misplaced)} 个 envelope 文件物理路径与 kind: 不符",
            evidence=misplaced[:20],
            impact=(
                "list_tasks/list_reports 输出错误；leader 无法归档线程；"
                "fcop_check 计数失真"
            ),
            scan_source="_scan_misplaced_envelopes",
            remediation=[RemediationStep(
                action="将错位文件移到正确桶目录",
                command=ps_lines,
                command_unix=ps_lines.replace("'", '"'),
                executor="PM",
                estimated_minutes=max(5, len(misplaced) // 10 + 5),
                tier=1,
                rollback="git revert HEAD",
                precondition="git status 确认无未提交变更",
            )],
        )]

    def _scan_legacy_role_docs(self) -> list[Violation]:
        """Detect grass-roots role files in fcop/ root (not protocol-standard)."""
        from fcop.inspection import RemediationStep, Violation

        fcop_root = self._path / "fcop"
        if not fcop_root.exists():
            return []

        # Only scan the top level (not recursive) for *.md files without kind:
        legacy: list[str] = []
        skip_prefixes = (
            "INSPECTION-", "SOP-", "TEAM-", "TASK-",
            "REPORT-", "ISSUE-", "REVIEW-",
        )
        for md in fcop_root.glob("*.md"):
            if any(md.name.startswith(p) for p in skip_prefixes):
                continue
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")
                fm = _extract_frontmatter_kind(text)
                if fm is None:
                    legacy.append(str(md.relative_to(self._path)))
            except Exception:
                continue

        if not legacy:
            return []

        return [Violation(
            violation_id="P1-000",
            severity="P1",
            rule_violated="Rule 1 (草根角色书)",
            summary=f"fcop/ 根目录有 {len(legacy)} 份非协议 Markdown 文件",
            evidence=legacy,
            impact="可能导致角色混淆；不在 fcop 任何审计路径；积累技术债",
            scan_source="_scan_legacy_role_docs",
            remediation=[RemediationStep(
                action="将草根角色书归档到 fcop/shared/roles/ 或 fcop/log/",
                command="# 逐文件确认内容后手工归档：\n"
                        "# git mv fcop/<file>.md fcop/shared/roles/<file>.md",
                executor="PM",
                estimated_minutes=30,
                tier=2,
                rollback="git revert HEAD",
            )],
        )]

    def _scan_legacy_manifests(self) -> list[Violation]:
        """Detect non-standard JSON files in fcop/ (e.g. custom manifests)."""
        from fcop.inspection import RemediationStep, Violation

        fcop_root = self._path / "fcop"
        if not fcop_root.exists():
            return []

        stray = [
            str(f.relative_to(self._path))
            for f in fcop_root.glob("*.json")
            if f.name != "fcop.json"
        ]
        if not stray:
            return []

        return [Violation(
            violation_id="P1-000",
            severity="P1",
            rule_violated="Rule 0 (双 manifest)",
            summary=f"fcop/ 下有 {len(stray)} 个非标准 JSON 文件（双 manifest 风险）",
            evidence=stray,
            impact="自创 manifest 与 fcop.json 并存会导致工具行为不一致",
            scan_source="_scan_legacy_manifests",
            remediation=[RemediationStep(
                action="确认内容后删除或迁移非标准 JSON",
                command="# 逐文件确认后：\n# git rm fcop/<file>.json",
                executor="ADMIN",
                estimated_minutes=10,
                tier=2,
                rollback="git revert HEAD",
            )],
        )]

    def _scan_lifecycle_topology_compliance(self) -> list[Violation]:
        """Audit FCoP 3.0 ``_lifecycle/`` topology compliance.

        Two checks (per spec §1.1 / §6 + TASK-20260522-004):

        - **P0**: ``fcop.json.protocol_version`` is v3+ but the project
          has no ``_lifecycle/`` directory at all. Project is broken on
          its own terms — every v3 tool path will refuse to run.
        - **P1**: project is in v3 topology yet retains the superseded
          ``tasks/`` or ``log/`` v2 buckets. Hygiene only — both
          locations parse correctly, but having two task homes invites
          drift.

        Pure-v2 projects (``protocol_version`` < 3 *and* no
        ``_lifecycle/``) are silently skipped: they are not v3, so v3
        compliance does not apply.
        """
        from fcop.errors import ConfigError
        from fcop.inspection import RemediationStep, Violation

        # Skip uninitialized projects entirely — they have no opinion
        # about which topology version they should be in yet.
        try:
            _ = self.config
        except ConfigError:
            return []
        if not self._workspace_root.is_dir():
            return []

        lifecycle_root = self._workspace_root / "_lifecycle"
        has_lifecycle = lifecycle_root.is_dir()

        # A bucket counts as "v2 residual" only if it actually contains
        # files. Empty ``tasks/`` / ``log/`` directories left behind by
        # tooling do not constitute a v2 project.
        residual: list[str] = []
        v2_has_content = False
        for legacy in ("tasks", "log"):
            legacy_path = self._workspace_root / legacy
            if not legacy_path.is_dir():
                continue
            try:
                content = [p for p in legacy_path.rglob("*") if p.is_file()]
            except OSError:
                content = []
            if content:
                v2_has_content = True
                residual.append(
                    str(legacy_path.relative_to(self._path)) + "/"
                )

        violations: list[Violation] = []

        # P0: initialized project with no _lifecycle/ AND no v2 task
        # content — the topology layer is simply missing. Pure v2
        # projects (have v2 content, no _lifecycle/) are skipped here;
        # the migration path covers them.
        if not has_lifecycle and not v2_has_content:
            violations.append(Violation(
                violation_id="P0-000",
                severity="P0",
                rule_violated="FCoP 3.0 spec §1.1 (_lifecycle/ MUST exist)",
                summary=(
                    "项目已初始化但 _lifecycle/ 与 v2 桶都不存在 —— "
                    "拓扑层缺失，task/report/review 写入会失败"
                ),
                evidence=[
                    f"missing: {lifecycle_root.relative_to(self._path)}/",
                ],
                impact=(
                    "v3 工具路径全部依赖 _lifecycle/{inbox,active,review,done,"
                    "archive}/；缺这层目录 task/report/review 写入会失败"
                ),
                scan_source="_scan_lifecycle_topology_compliance",
                remediation=[RemediationStep(
                    action="重新部署初始化产物以补齐 _lifecycle/",
                    command=(
                        "python -c \"from fcop import Project; "
                        "Project('.').deploy_role_templates(force=True)\"\n"
                        "# 或者完全重新初始化（会丢已有协作历史）：\n"
                        "# rm -rf fcop/ && fcop init ..."
                    ),
                    executor="ADMIN",
                    estimated_minutes=5,
                    tier=1,
                    rollback="git checkout fcop/",
                )],
            ))

        # P1: v3 lifecycle present AND v2 buckets retain content —
        # both topologies parse correctly, but two task homes invite
        # drift. Trigger the migration path.
        if has_lifecycle and residual:
            violations.append(Violation(
                violation_id="P1-000",
                severity="P1",
                rule_violated="FCoP 3.0 spec §6 (v2 buckets superseded)",
                summary=(
                    f"v3 项目残留 {len(residual)} 个 v2 桶（tasks/ / log/）"
                ),
                evidence=residual,
                impact=(
                    "v2 与 v3 拓扑并存会导致同一份 task 出现在两处，"
                    "list/archive 操作行为不一致"
                ),
                scan_source="_scan_lifecycle_topology_compliance",
                remediation=[RemediationStep(
                    action="把残留 v2 桶迁移到 _lifecycle/",
                    command="python -m fcop migrate --to-v3",
                    executor="ADMIN",
                    estimated_minutes=3,
                    tier=2,
                    rollback="git checkout fcop/",
                )],
            ))

        return violations

    def _scan_ghost_prefixes(self) -> list[Violation]:
        """Detect stale ghost-prefix files (DRAFT-/HANDOFF-/AMEND-/*-v2.md).

        Honours the same exempt-path list as :meth:`_scan_misplaced_envelopes`
        (per ISSUE-20260513-008): an ``AMEND-*.md`` that lives under
        ``fcop/log/`` or ``_archive/`` was already legitimately archived
        and shouldn't re-trigger as a ghost.
        """
        from fcop.inspection import RemediationStep, Violation

        fcop_root = self._path / "fcop"
        if not fcop_root.exists():
            return []

        ghost_patterns = ["DRAFT-*.md", "HANDOFF-*.md", "AMEND-*.md"]
        version_pattern = "*-v[0-9]*.md"
        found_paths: list[pathlib.Path] = []
        for pat in ghost_patterns:
            found_paths.extend(fcop_root.rglob(pat))
        found_paths.extend(fcop_root.rglob(version_pattern))
        found = sorted({
            str(p.relative_to(self._path))
            for p in found_paths
            if not _is_audit_exempt_path(p, fcop_root)
        })
        if not found:
            return []

        return [Violation(
            violation_id="P2-000",
            severity="P2",
            rule_violated="Rule 5 (幽灵前缀文件)",
            summary=f"发现 {len(found)} 个幽灵前缀文件",
            evidence=found[:20],
            impact="草稿/交接/修订文件未清理，积累协议外文件，干扰审计",
            scan_source="_scan_ghost_prefixes",
            remediation=[RemediationStep(
                action="确认内容后重命名或删除幽灵文件",
                command="# DRAFT- → 确认后 git mv 为 TASK- 或删除\n"
                        "# HANDOFF- → 确认交接完成后 git mv 到 fcop/log/archive/\n"
                        "# *-v2.md → 确认合并后 git rm 旧版",
                executor="PM",
                estimated_minutes=15,
                tier=3,
                rollback="git revert HEAD",
            )],
        )]

    def _scan_outdated_role_docs(self) -> list[Violation]:
        """Detect deployed role docs whose content lags the installed fcop version.

        Inspects every ``*.md`` in ``fcop/shared/roles/`` and checks whether
        the highest protocol version referenced (e.g. "v1.4") is more than one
        minor version behind the installed ``fcop`` package.  A gap of > 1 minor
        version is reported as a P1 violation (RULE_DOC_DRIFT).

        Background: role docs are authored once and deployed via
        ``deploy_role_templates()``.  Without an explicit re-deployment they do
        not automatically pick up new protocol sections (REVIEW, risk_level,
        supersedes: etc.), leaving agents unaware of current FCoP capabilities.
        """
        import re

        from fcop.inspection import RemediationStep, Violation

        shared_roles = self._path / "fcop" / "shared" / "roles"
        if not shared_roles.exists() or not any(shared_roles.glob("*.md")):
            return []

        # Installed package minor version
        try:
            from fcop._version import __version__ as pkg_ver

            parts = pkg_ver.split(".")
            pkg_major, pkg_minor = int(parts[0]), int(parts[1])
        except Exception:
            return []

        # Matches version tags like "v1.3", "v1.4.0", "v1.0 ~ v1.4" etc.
        ver_re = re.compile(r"v(\d+)\.(\d+)")

        outdated: list[str] = []
        for md in sorted(shared_roles.glob("*.md")):
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            found = ver_re.findall(text)
            if not found:
                # No version reference at all → definitely outdated
                outdated.append(str(md.relative_to(self._path)))
                continue

            # Highest (major, minor) mentioned in the file
            max_major = max(int(m) for m, _ in found)
            max_minor = max(
                int(n) for m, n in found if int(m) == max_major
            )

            # Report if gap > 1 minor version (proposal: "差距 > 1 个 minor 版本")
            minor_gap = (pkg_major - max_major) * 100 + (pkg_minor - max_minor)
            if minor_gap > 1:
                outdated.append(str(md.relative_to(self._path)))

        if not outdated:
            return []

        return [
            Violation(
                violation_id="P1-000",
                severity="P1",
                rule_violated="RULE_DOC_DRIFT (角色文档协议漂移)",
                summary=(
                    f"{len(outdated)} 份已部署角色文档内容"
                    f"滞后已安装的 fcop {pkg_major}.{pkg_minor}.x 超过 1 个 minor 版本"
                ),
                evidence=outdated[:20],
                impact=(
                    "Agent 读取的角色说明书缺少协议新功能描述"
                    "（REVIEW envelope / risk_level / supersedes: 等），"
                    "可能导致 Agent 不了解当前 FCoP 能力边界"
                ),
                scan_source="_scan_outdated_role_docs",
                remediation=[
                    RemediationStep(
                        action="重新部署角色模板，将本地角色文档同步到最新协议版本",
                        command="deploy_role_templates(force=True)",
                        command_unix="deploy_role_templates(force=True)",
                        executor="PM",
                        estimated_minutes=5,
                        tier=2,
                        rollback="git revert HEAD  # 如部署结果有问题",
                    )
                ],
            )
        ]

    def _scan_internal_only_declarations(self) -> list[Violation]:
        """Detect ``fcop/internal/*.md`` files missing the ``internal-only`` declaration.

        Per Rule 4.6 (FCoP rules 3.0.0+) every ``.md`` file under the
        opt-in internal-archive bucket ``fcop/internal/`` *should* carry
        a bilingual declaration block right after the YAML frontmatter,
        plus an ``internal_only: true`` flag in the frontmatter itself.

        This is a **soft convention** (Rule 4.6 is non-mandatory): any
        finding here is reported as :pyattr:`Violation.severity == "P3"`
        and never moves :pyattr:`InspectionReport.overall_status` off
        ``green``. The remediation is a manual edit suggestion only.

        Detection rule (per ADR-0034 §4.3):

        - File MUST contain ``internal_only: true`` in the YAML
          frontmatter, *or* the literal string ``INTERNAL ONLY`` in the
          first 30 non-blank lines after the frontmatter (case-sensitive
          banner).
        - Files matching neither are flagged P3.

        Returns an empty list when the bucket does not exist (the
        bucket is opt-in, deployed only via
        ``Project.init(deploy_internal_template=True)``).
        """
        from fcop.inspection import RemediationStep, Violation

        internal_dir = self._path / "fcop" / "internal"
        if not internal_dir.exists() or not internal_dir.is_dir():
            return []

        offenders: list[str] = []
        for md in sorted(internal_dir.rglob("*.md")):
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            # Quick frontmatter check: look for `internal_only: true` (any case-insensitive variant)
            head = text[:4096]
            has_flag = (
                "internal_only: true" in head
                or "internal_only: True" in head
                or "internal_only: TRUE" in head
            )
            has_banner = "INTERNAL ONLY" in head
            if has_flag or has_banner:
                continue
            offenders.append(str(md.relative_to(self._path)).replace("\\", "/"))

        if not offenders:
            return []

        return [
            Violation(
                violation_id="P3-000",
                severity="P3",
                rule_violated="Rule 4.6 (internal-only 声明缺失，soft convention)",
                summary=(
                    f"{len(offenders)} 份 fcop/internal/ 下的 .md 文件未携带 "
                    "internal-only 声明（frontmatter `internal_only: true` "
                    "或正文 `INTERNAL ONLY` 警告块）"
                ),
                evidence=offenders[:20],
                impact=(
                    "建议而非强制：缺失声明不会阻塞写入，但人工读盘 / "
                    "外发审阅时容易把内部档案当外发文档误传。"
                    "推荐补齐以让 Rule 4.6 内外档案体系生效。"
                ),
                scan_source="_scan_internal_only_declarations",
                remediation=[
                    RemediationStep(
                        action=(
                            "为每份 fcop/internal/ 下的 .md 文件补齐双语 "
                            "internal-only 声明（参考 fcop/internal/README.md）"
                        ),
                        command=(
                            "# 在每份文件的 frontmatter 末尾加 internal_only: true，"
                            "并在 frontmatter 之后插入 INTERNAL ONLY 警告块"
                        ),
                        command_unix=(
                            "# 模板见 fcop/internal/README.md（"
                            "Project.init(deploy_internal_template=True) 自动落盘）"
                        ),
                        executor="PM",
                        estimated_minutes=2,
                        tier=3,
                        rollback="git revert HEAD",
                    )
                ],
            )
        ]

    # ── Tasks ─────────────────────────────────────────────────────────

    def write_task(
        self,
        *,
        sender: str,
        recipient: str,
        priority: Priority | str,
        subject: str,
        body: str,
        references: Sequence[str] = (),
        thread_key: str | None = None,
        slot: str | None = None,
        risk_level: RiskLevel | str | None = None,
    ) -> Task:
        """Create a new task file.

        Filename is auto-generated as
        ``TASK-YYYYMMDD-NNN-{sender}-to-{recipient}.md``. ``NNN`` is
        today's existing task count + 1. On concurrent-write
        collisions the sequence is retried up to :data:`_MAX_WRITE_RETRIES`
        times before giving up with a :class:`RuntimeError`.

        Args:
            sender: Role code of the sending agent (uppercase, ASCII,
                hyphen-friendly). ``ADMIN`` and ``SYSTEM`` are accepted.
            recipient: Role code of the receiving agent.
            priority: Either a :class:`Priority` enum or a string alias
                accepted by :func:`normalize_priority` (``"P0".."P3"``
                or legacy words like ``"urgent"`` / ``"normal"``).
            subject: Short one-line summary written into the ``subject:``
                frontmatter field. Required by the 0.6 grammar.
            body: Markdown body of the task; any leading blank lines
                are normalized away so the output stays idempotent.
            references: Zero or more task/report IDs this task depends
                on. Written as ``references: [...]`` in the frontmatter.
            thread_key: Optional thread grouping key — ties a sequence
                of back-and-forth tasks together.
            slot: Optional recipient qualifier (``.BACKEND`` → recipient
                becomes ``DEV.BACKEND`` in the filename). Role grammar
                applies to the slot too.
            risk_level: Optional risk level of this task operation
                (``low``, ``medium``, ``high``, ``irreversible``).
                Defaults to ``medium`` when omitted. ``high`` and
                ``irreversible`` automatically require a ``needs_human``
                review gate (ADR-0024/0025).

        Raises:
            ValueError: filename components don't match the grammar
                (e.g. sender contains lowercase letters), or ``priority``
                is an unrecognized alias.
            OverflowError: today's 999-sequence space is exhausted.
            RuntimeError: failed to reserve a sequence after
                :data:`_MAX_WRITE_RETRIES` collisions with concurrent
                writers. Practical only under pathological races.
        """
        tasks_dir = self.tasks_dir
        tasks_dir.mkdir(parents=True, exist_ok=True)

        priority_enum = normalize_priority(priority)
        date = today_iso()
        risk_level_enum = normalize_risk_level(risk_level)

        fm = TaskFrontmatter(
            protocol=PROTOCOL_NAME,
            version=PROTOCOL_VERSION,
            sender=sender,
            recipient=recipient,
            priority=priority_enum,
            thread_key=thread_key,
            subject=subject or None,
            references=tuple(references),
            risk_level=risk_level_enum,
        )
        text = assemble_task_file(fm, body)
        payload = text.encode("utf-8")

        for _ in range(_MAX_WRITE_RETRIES):
            existing = _existing_filenames_for_seq(
                tasks_dir, self.log_dir / "tasks"
            )
            sequence = next_sequence(existing, date=date, kind="task")
            filename = build_task_filename(
                date=date,
                sequence=sequence,
                sender=sender,
                recipient=recipient,
                slot=slot,
            )
            target = tasks_dir / filename

            try:
                # O_EXCL makes the reservation atomic: if a concurrent
                # writer won the same sequence we fail here and retry.
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    # FCoP 3.0 (per spec §2.4 + ADR-0036 Rule E):
                    # every file under _lifecycle/ MUST carry a
                    # creation transition event. We stamp it here,
                    # inside the O_EXCL atomic reservation, so the
                    # file appears on disk in its already-witnessed
                    # state — no observable intermediate "v3 file
                    # without an event" window exists.
                    final_payload = payload
                    if self.is_v3:
                        final_payload = _stamp_v3_creation_event(
                            payload, sender=sender,
                        )
                    handle.write(final_payload)
            except BaseException:
                # Writer crashed after reserving — clean up the empty
                # placeholder so we don't poison the sequence slot.
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            parsed = parse_task_filename(filename)
            assert parsed is not None, (
                f"built filename {filename!r} failed to round-trip through "
                "parse_task_filename — this is a bug in core.filename."
            )
            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            return Task(
                path=target,
                filename=filename,
                task_id=parsed.task_id,
                date=parsed.date,
                sequence=parsed.sequence,
                frontmatter=fm,
                body=body,
                is_archived=False,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve a task sequence after {_MAX_WRITE_RETRIES} "
            "retries — concurrent writers are colliding faster than we can "
            "pick an unused slot"
        )

    def list_tasks(
        self,
        *,
        sender: str | None = None,
        recipient: str | None = None,
        status: Literal["open", "archived", "all"] = "open",
        date: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Task]:
        """List tasks, optionally filtered by sender / recipient / date.

        Args:
            sender: Exact-match role code filter. ``None`` means any.
            recipient: Exact-match role code filter. ``None`` means any.
            status: ``"open"`` scans :attr:`tasks_dir`, ``"archived"``
                scans ``log/tasks/``, ``"all"`` scans both.
            date: ``YYYYMMDD`` filter. ``None`` means any date.
            limit: Max results; ``None`` means unlimited.
            offset: Skip this many results from the front (applied
                after sorting). Combine with ``limit`` for pagination.

        Returns:
            Tasks sorted by ``(date, sequence)`` descending — newest
            first. Unreadable files (malformed frontmatter, corrupt
            YAML) are silently skipped; use :meth:`inspect_task` if
            you need to surface their problems.
        """
        directories: list[tuple[pathlib.Path, bool]] = []
        if status in ("open", "all"):
            directories.append((self.tasks_dir, False))
        if status in ("archived", "all"):
            directories.append((self.log_dir / "tasks", True))

        tasks: list[Task] = []
        for directory, archived in directories:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                task = _try_load_task(entry, is_archived=archived)
                if task is None:
                    continue
                if date is not None and task.date != date:
                    continue
                if sender is not None and task.sender != sender:
                    continue
                if recipient is not None and task.recipient != recipient:
                    continue
                tasks.append(task)

        tasks.sort(key=lambda t: (t.date, t.sequence), reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return tasks[offset:end]

    def read_task(self, filename_or_id: str) -> Task:
        """Load one task by full filename or by task id (``TASK-YYYYMMDD-NNN``).

        Args:
            filename_or_id: Either a full filename (``TASK-...md``) or a
                task id prefix (``TASK-20260423-001``). Ids are resolved
                by scanning :attr:`tasks_dir` first, then ``log/tasks/``
                so open tasks win over archived ones.

        Raises:
            TaskNotFoundError: nothing matches.
            ValidationError | ProtocolViolation: file exists but its
                frontmatter is malformed. Use :meth:`inspect_task` for a
                non-raising variant.
        """
        target, archived = self._resolve_task_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no task matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_task_strict(target, is_archived=archived)

    def _resolve_task_file(
        self, filename_or_id: str
    ) -> tuple[pathlib.Path | None, bool]:
        """Resolve a user-supplied task handle to an on-disk path.

        Accepts three shapes:

        * A full filename matching :data:`TASK_FILENAME_RE`
          (``TASK-20260423-001-ADMIN-to-PM.md``). Direct lookup.
        * A task id (``TASK-20260423-001``). Scan both dirs for the
          first file whose filename starts with that id.
        * Anything else — returns ``(None, False)``.

        The open :attr:`tasks_dir` is scanned before ``log/tasks/`` so
        a live task takes precedence over a same-id archived one; that
        matches how ADMIN thinks about it ("the task I'm working on").

        Returns:
            ``(path, is_archived)``. ``path`` is ``None`` when no
            match is found; ``is_archived`` is meaningless in that case.
        """
        # Build the search order. v2 projects scan tasks/ then
        # log/tasks/. v3 projects scan the 5 lifecycle buckets in
        # protocol order (inbox → active → review → done → archive)
        # so a "live" hit beats an archived same-id duplicate, matching
        # how ADMIN thinks about it ("the task I'm working on").
        if self.is_v3:
            search_order: tuple[tuple[pathlib.Path, bool], ...] = (
                (self.inbox_dir, False),
                (self.active_dir, False),
                (self.review_dir, False),
                (self.done_dir, False),
                (self.archive_dir, True),
            )
        else:
            search_order = (
                (self.tasks_dir, False),
                (self.log_dir / "tasks", True),
            )

        if TASK_FILENAME_RE.fullmatch(filename_or_id):
            for directory, archived in search_order:
                candidate = directory / filename_or_id
                if candidate.is_file():
                    return candidate, archived
            return None, False

        prefix = filename_or_id
        for directory, archived in search_order:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                if not entry.is_file():
                    continue
                parsed = parse_task_filename(entry.name)
                if parsed is None:
                    continue
                if parsed.task_id == prefix or entry.name.startswith(
                    prefix + "-"
                ):
                    return entry, archived
        return None, False

    def archive_task(self, filename_or_id: str) -> Task:
        """Archive a task (move it to the archive bucket).

        On v2 projects: physically moves the task from
        ``tasks/`` to ``log/tasks/`` and brings any matching reports
        along to ``log/reports/``. The legacy "this conversation is
        closed" marker.

        On v3 projects: walks the file through the legal lifecycle
        chain to ``_lifecycle/archive/``. Concretely, depending on
        where the file currently is:

          * ``inbox`` → active → done → archive   (3 transitions)
          * ``active`` → done → archive           (2 transitions)
          * ``review`` → done → archive           (2 transitions; uses approve_task)
          * ``done`` → archive                    (1 transition)
          * ``archive`` → no-op (idempotent)

        Each step appends one ``transitions:`` event using the
        canonical L1 tool for that edge (claim_task / finish_task /
        approve_task / archive_task) so the audit trace records the
        full path. The fast-track exists so v2-era callers
        (CodeFlowMu) that treat archive_task as the single
        "wrap this up" verb continue to work without modification —
        per the Q1=a + ADR-0039 §2.5 "permitted without an ADR:
        reference-implementation behaviour aligning to the protocol"
        directive.

        Matching report movement (v2 only). On v3 projects reports
        live under ``reports/`` regardless of task status, so this
        method does not touch them.

        Idempotent — archiving an already-archived task returns the
        same :class:`Task` without touching the filesystem. That makes
        the method safe to call from cleanup scripts without
        pre-checking.

        Args:
            filename_or_id: Full filename or task id, same shapes
                accepted by :meth:`read_task`.

        Returns:
            The archived :class:`Task` with ``is_archived == True`` and
            an updated ``path``.

        Raises:
            TaskNotFoundError: no matching file in either the open or
                archived directories.
            ValidationError | ProtocolViolation: file exists but its
                frontmatter is malformed; archiving a corrupt file
                would hide the problem, so we surface it up-front.
        """
        source, archived = self._resolve_task_file(filename_or_id)
        if source is None:
            raise TaskNotFoundError(
                f"cannot archive: no task matches {filename_or_id!r}",
                query=filename_or_id,
            )

        if archived:
            return _load_task_strict(source, is_archived=True)

        if self.is_v3:
            destination = _v3_archive_chain(self, source)
            # Reports under reports/ are not archived in v3 (spec §1.1)
            # — they stay where they are.
            return _load_task_strict(destination, is_archived=True)

        log_tasks_dir = self.log_dir / "tasks"
        log_tasks_dir.mkdir(parents=True, exist_ok=True)
        destination = log_tasks_dir / source.name
        # os.replace is atomic on same-filesystem moves, which is the
        # only case we can reach here — tasks_dir and log_dir are both
        # under self._path.
        source.replace(destination)

        # Move matching reports alongside. A report is "matching" when
        # its filename starts with the task id that precedes the
        # sender/recipient segment of the task filename.
        parsed = parse_task_filename(source.name)
        if parsed is not None:
            self._archive_related_reports(task_id=parsed.task_id)

        return _load_task_strict(destination, is_archived=True)

    def _archive_related_reports(self, *, task_id: str) -> None:
        """Move every report whose filename embeds *task_id* to the log.

        Report filenames don't include the task id as a prefix — they
        carry their own ``REPORT-YYYYMMDD-NNN-`` slug — so matching is
        done on the ``references`` frontmatter field instead. We load
        each report, check whether it cites *task_id*, and move the
        ones that do.

        Silent if there's nothing to move; reports are optional.
        """
        open_reports = self.reports_dir
        if not open_reports.is_dir():
            return
        log_reports = self.log_dir / "reports"

        for entry in open_reports.iterdir():
            if not entry.is_file():
                continue
            if entry.suffix.lower() not in _FCOP_SUFFIXES:
                continue
            if not REPORT_FILENAME_RE.match(entry.name):
                continue

            try:
                text = entry.read_text(encoding="utf-8")
            except OSError:
                continue
            # Reports share the YAML-frontmatter shape with tasks, so
            # we reuse the task parser to read references / extras.
            # A malformed report here just gets skipped; surfacing its
            # breakage is inspect_report's job, not archive_task's.
            try:
                fm, _ = parse_task_frontmatter(text)
            except Exception:
                continue

            references = fm.references
            if task_id not in references:
                continue

            log_reports.mkdir(parents=True, exist_ok=True)
            entry.replace(log_reports / entry.name)

    def inspect_task(self, filename_or_id: str) -> list[ValidationIssue]:
        """Validate a task file against the FCoP schema.

        Unlike :meth:`read_task`, this method never raises on parser
        errors — every problem is converted into a
        :class:`ValidationIssue` and returned in the list. An empty
        list means the file is schema-valid.

        Useful for UIs that want to display warnings and errors side-
        by-side, or for migration tooling that needs to tolerate a
        batch of broken files.

        Args:
            filename_or_id: Same resolution rules as :meth:`read_task`.
                If nothing matches, a single ``"error"`` issue is
                returned with ``field == "filename"`` — we do not
                raise :class:`TaskNotFoundError` here because that
                would defeat the "non-raising" contract.

        Returns:
            Possibly empty list of issues, ordered: filesystem / I/O
            issues first, then frontmatter issues.
        """
        source, _ = self._resolve_task_file(filename_or_id)
        if source is None:
            return [
                ValidationIssue(
                    severity="error",
                    field="filename",
                    message=f"no task matches {filename_or_id!r}",
                )
            ]

        issues: list[ValidationIssue] = []
        try:
            text = source.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="filename",
                    message=f"cannot read {source.name}: {exc}",
                    path=source,
                )
            )
            return issues

        try:
            parse_task_frontmatter(text)
        except ValidationError as exc:
            # ValidationError carries a .issues list already — annotate
            # each with the file path so agents can jump to it.
            issues.extend(
                ValidationIssue(
                    severity=i.severity,
                    field=i.field,
                    message=i.message,
                    path=source,
                )
                for i in exc.issues
            )
        except Exception as exc:
            # ProtocolViolation and unexpected YAML errors both land
            # here; flatten to a single issue so callers get something
            # actionable. We deliberately catch broad to honor the
            # "never raises" docstring contract.
            issues.append(
                ValidationIssue(
                    severity="error",
                    field="frontmatter",
                    message=str(exc),
                    path=source,
                )
            )

        return issues

    # ── Reports ───────────────────────────────────────────────────────

    def write_report(
        self,
        *,
        task_id: str,
        reporter: str,
        recipient: str,
        body: str,
        status: Literal["done", "blocked", "in_progress", "aborted"] = "done",
        priority: Priority | str = "P2",
    ) -> Report:
        """Create a report responding to an existing task.

        Reports live in ``docs/agents/reports/`` and cite their parent
        task via the ``references:`` frontmatter field. A custom
        top-level ``status:`` field captures the report outcome
        (``done`` / ``blocked`` / ``in_progress``).

        Args:
            task_id: Id of the task this report answers. The task must
                exist — open or archived — and its recipient must match
                ``reporter`` (Rule 5: only the addressee can report).
            reporter: Role code of the reporting agent.
            recipient: Role code receiving the report. Typically the
                original task's sender, so the thread loops back.
            body: Markdown body of the report.
            status: ``done`` / ``blocked`` / ``in_progress`` /
                ``aborted``. Written as a top-level YAML field and
                echoed in :attr:`Report.status`. ``aborted`` was
                added in v1.0 per ADR-0019 §abort recovery action.
            priority: Report priority, same normalization rules as
                :meth:`write_task`. Defaults to ``P2``.

        Raises:
            TaskNotFoundError: ``task_id`` has no matching task file.
            ProtocolViolation: ``reporter`` is not the original task's
                recipient (Rule 5), or ``status`` is not a valid
                report status.
            ValueError: ``priority`` is an unrecognized alias.
        """
        if status not in _VALID_REPORT_STATUSES:
            raise ProtocolViolation(
                f"status must be one of {sorted(_VALID_REPORT_STATUSES)}; "
                f"got {status!r}",
                rule="report.status",
            )

        task_path, task_archived = self._resolve_task_file(task_id)
        if task_path is None:
            raise TaskNotFoundError(
                f"cannot write report: no task matches {task_id!r}",
                query=task_id,
            )
        # Strict load — we need the frontmatter to enforce Rule 5.
        task = _load_task_strict(task_path, is_archived=task_archived)
        if task.recipient != reporter:
            raise ProtocolViolation(
                f"reporter {reporter!r} is not the recipient of task "
                f"{task_id!r} (its recipient is {task.recipient!r}); "
                "only the task's addressee may report on it",
                rule="Rule 5",
            )

        reports_dir = self.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)

        priority_enum = normalize_priority(priority)
        date = today_iso()

        fm = TaskFrontmatter(
            protocol=PROTOCOL_NAME,
            version=PROTOCOL_VERSION,
            sender=reporter,
            recipient=recipient,
            priority=priority_enum,
            references=(task.task_id,),
            extra={"status": status},
        )
        text = assemble_task_file(fm, body)
        payload = text.encode("utf-8")

        for _ in range(_MAX_WRITE_RETRIES):
            existing = _existing_filenames_for_seq(
                reports_dir, self.log_dir / "reports"
            )
            sequence = next_sequence(existing, date=date, kind="report")
            filename = build_report_filename(
                date=date,
                sequence=sequence,
                reporter=reporter,
                recipient=recipient,
            )
            target = reports_dir / filename

            try:
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(payload)
            except BaseException:
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            return Report(
                path=target,
                filename=filename,
                task_id=task.task_id,
                reporter=reporter,
                recipient=recipient,
                status=status,
                body=body,
                is_archived=False,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve a report sequence after "
            f"{_MAX_WRITE_RETRIES} retries"
        )

    def list_reports(
        self,
        *,
        reporter: str | None = None,
        task_id: str | None = None,
        status: Literal["open", "archived", "all"] = "open",
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Report]:
        """List reports, optionally filtered by reporter or parent task.

        Args:
            reporter: Exact-match filter on the report's sender.
            task_id: If provided, only reports that cite this task in
                their ``references:`` list are returned.
            status: ``"open"`` (default, scans ``reports_dir``),
                ``"archived"`` (scans ``log/reports/``), or ``"all"``.
            limit / offset: Pagination window, applied after sorting.

        Returns:
            Reports sorted by filename (which embeds date + sequence)
            descending — newest first. Malformed files are silently
            skipped, matching :meth:`list_tasks`'s contract.
        """
        directories: list[tuple[pathlib.Path, bool]] = []
        if status in ("open", "all"):
            directories.append((self.reports_dir, False))
        if status in ("archived", "all"):
            directories.append((self.log_dir / "reports", True))

        reports: list[Report] = []
        for directory, archived in directories:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                report = _try_load_report(entry, is_archived=archived)
                if report is None:
                    continue
                if reporter is not None and report.reporter != reporter:
                    continue
                if task_id is not None and report.task_id != task_id:
                    continue
                reports.append(report)

        # Date+sequence ordering matches list_tasks; parse once for
        # the sort key so we don't re-parse filenames per comparison.
        def _sort_key(r: Report) -> tuple[str, int]:
            parsed = parse_report_filename(r.filename)
            if parsed is None:  # defense in depth; shouldn't happen
                return ("", 0)
            return (parsed.date, parsed.sequence)

        reports.sort(key=_sort_key, reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return reports[offset:end]

    def read_report(self, filename_or_id: str) -> Report:
        """Load one report by filename or report id (``REPORT-YYYYMMDD-NNN``).

        Resolution is parallel to :meth:`read_task`: full filename or
        id prefix, open directory first then archive.

        Raises:
            TaskNotFoundError: no match. (We reuse this error type
                because there isn't a dedicated ``ReportNotFoundError``
                in the 0.6 exception hierarchy — the search space and
                user intent are analogous.)
            ValidationError | ProtocolViolation: file exists but is
                malformed. Use inspect for a non-raising variant.
        """
        target, archived = self._resolve_report_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no report matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_report_strict(target, is_archived=archived)

    def _resolve_report_file(
        self, filename_or_id: str
    ) -> tuple[pathlib.Path | None, bool]:
        """Resolve a user handle to a report path, parallel to
        :meth:`_resolve_task_file`.

        Accepts a full filename, or a ``REPORT-YYYYMMDD-NNN`` id prefix.
        Live reports in ``reports_dir`` take precedence over archived
        duplicates with the same id.
        """
        if REPORT_FILENAME_RE.fullmatch(filename_or_id):
            for directory, archived in (
                (self.reports_dir, False),
                (self.log_dir / "reports", True),
            ):
                candidate = directory / filename_or_id
                if candidate.is_file():
                    return candidate, archived
            return None, False

        prefix = filename_or_id
        for directory, archived in (
            (self.reports_dir, False),
            (self.log_dir / "reports", True),
        ):
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                if not entry.is_file():
                    continue
                parsed = parse_report_filename(entry.name)
                if parsed is None:
                    continue
                if parsed.report_id == prefix or entry.name.startswith(
                    prefix + "-"
                ):
                    return entry, archived
        return None, False

    # ── Issues ────────────────────────────────────────────────────────

    def write_issue(
        self,
        *,
        reporter: str,
        summary: str,
        body: str,
        severity: Severity | str = "medium",
    ) -> Issue:
        """Create an issue broadcast.

        Issues don't follow the sender → recipient pattern; any
        registered role can write one, and they are addressed to
        *whoever can fix them*. The filename therefore carries only
        the reporter; frontmatter carries ``summary`` and
        ``severity`` as top-level fields.

        Args:
            reporter: Role code of the agent raising the issue. Must
                pass :func:`validate_role_code` (reserved codes like
                ``ADMIN`` / ``SYSTEM`` are permitted — a human or the
                protocol itself can raise an issue).
            summary: Short one-line description. Becomes the ``summary:``
                frontmatter field; must be non-empty after stripping.
            body: Markdown body describing the issue in detail.
            severity: ``low`` / ``medium`` / ``high`` / ``critical``
                (plus the aliases :func:`normalize_severity` accepts).
                Defaults to ``medium``.

        Raises:
            ValidationError: ``reporter`` fails role-code grammar.
            ValueError: ``summary`` is empty or ``severity`` is not a
                recognized value.
        """
        cleaned_summary = summary.strip()
        if not cleaned_summary:
            raise ValueError(
                "issue summary must be non-empty after stripping whitespace"
            )

        role_issues = validate_role_code(
            reporter, field="reporter", allow_reserved=True
        )
        role_errors = [i for i in role_issues if i.severity == "error"]
        if role_errors:
            raise ValidationError(
                f"invalid reporter role code {reporter!r}",
                issues=role_errors,
            )

        severity_enum = normalize_severity(severity)

        issues_dir = self.issues_dir
        issues_dir.mkdir(parents=True, exist_ok=True)

        date = today_iso()
        # Issue files are the one FCoP file type that can be legally
        # edited post-creation (status open→closed is an allowed
        # monotonic append, see ADR-0004 §"Issue 是例外"). That means
        # filesystem mtime no longer equals creation time, so we must
        # persist ``created_at`` in the frontmatter. Tasks and reports
        # don't need this: they are strictly immutable, mtime = created.
        frontmatter_data: dict[str, object] = {
            "protocol": PROTOCOL_NAME,
            "version": PROTOCOL_VERSION,
            "reporter": reporter,
            "severity": severity_enum.value,
            "status": "open",
            "summary": cleaned_summary,
            "created_at": _now_iso(),
        }
        text = _assemble_issue_file(frontmatter_data, body)
        payload = text.encode("utf-8")

        for _ in range(_MAX_WRITE_RETRIES):
            existing = _existing_filenames_for_seq(
                issues_dir, self.log_dir / "issues"
            )
            sequence = next_sequence(existing, date=date, kind="issue")
            filename = build_issue_filename(
                date=date, sequence=sequence, reporter=reporter
            )
            target = issues_dir / filename

            try:
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(payload)
            except BaseException:
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            return Issue(
                path=target,
                filename=filename,
                issue_id=f"ISSUE-{date}-{sequence:03d}",
                summary=cleaned_summary,
                severity=severity_enum,
                reporter=reporter,
                body=body,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve an issue sequence after "
            f"{_MAX_WRITE_RETRIES} retries"
        )

    def list_issues(
        self,
        *,
        reporter: str | None = None,
        severity: Severity | str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Issue]:
        """List issues, optionally filtered.

        Args:
            reporter: Exact-match filter on the issue's ``reporter``.
            severity: Exact-match filter; string aliases are normalized
                via :func:`normalize_severity`.
            limit / offset: Pagination window, applied after sorting.

        Returns:
            Issues sorted by date + sequence descending (newest first).
            Malformed files are silently skipped — matches the
            :meth:`list_tasks` / :meth:`list_reports` contract.
        """
        severity_enum: Severity | None = None
        if severity is not None:
            severity_enum = normalize_severity(severity)

        issues: list[Issue] = []
        directory = self.issues_dir
        if directory.is_dir():
            for entry in directory.iterdir():
                issue = _try_load_issue(entry)
                if issue is None:
                    continue
                if reporter is not None and issue.reporter != reporter:
                    continue
                if (
                    severity_enum is not None
                    and issue.severity is not severity_enum
                ):
                    continue
                issues.append(issue)

        def _sort_key(i: Issue) -> tuple[str, int]:
            parsed = parse_issue_filename(i.filename)
            if parsed is None:
                return ("", 0)
            return (parsed.date, parsed.sequence)

        issues.sort(key=_sort_key, reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return issues[offset:end]

    def read_issue(self, filename_or_id: str) -> Issue:
        """Load one issue by filename or issue id.

        Accepts a full filename (``ISSUE-YYYYMMDD-NNN-REPORTER.md``) or
        an id prefix (``ISSUE-YYYYMMDD-NNN``). Unlike tasks and reports,
        issues are never archived, so there is only one location to
        search.

        Raises:
            TaskNotFoundError: no match. The ``Task`` prefix is
                retained here because the 0.6 exception hierarchy does
                not include a dedicated ``IssueNotFoundError`` — the
                semantic meaning is the same.
            ValidationError | ProtocolViolation: malformed frontmatter.
        """
        target = self._resolve_issue_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no issue matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_issue_strict(target)

    def _resolve_issue_file(
        self, filename_or_id: str
    ) -> pathlib.Path | None:
        """Resolve a user handle to an on-disk issue path, or ``None``.

        Accepts full filename or ``ISSUE-YYYYMMDD-NNN`` prefix. Issues
        live only in ``issues_dir`` — there is no archive equivalent,
        so resolution is a single-directory scan.
        """
        directory = self.issues_dir
        if not directory.is_dir():
            return None

        if ISSUE_FILENAME_RE.fullmatch(filename_or_id):
            candidate = directory / filename_or_id
            return candidate if candidate.is_file() else None

        prefix = filename_or_id
        for entry in directory.iterdir():
            if not entry.is_file():
                continue
            parsed = parse_issue_filename(entry.name)
            if parsed is None:
                continue
            if parsed.issue_id == prefix or entry.name.startswith(
                prefix + "-"
            ):
                return entry
        return None

    # ── Reviews (v1.0 / Audit) ────────────────────────────────────────
    #
    # REVIEW envelope 端到端，per ADR-0017 + review.schema.json。是 v1.0
    # 唯一**新增**的 envelope 类型——其他 6 个抽象（Agent / IPC / Encoding
    # / Event / Failure / Boundary）的 reference impl 由 TASK-005..008
    # 各自落地。
    #
    # 设计要点：
    # - decision 与 subject_type 都用闭枚举，需要绕开必须改 ADR + 升 MINOR。
    # - decision == NEEDS_CHANGES 必配非空 required_changes（schema if/then
    #   也守门，本层先拒以给更友好的错误）。
    # - decision == NEEDS_HUMAN → Review 处于 pending 状态，须配合
    #   mark_human_approved() 完成闭环（per ADR-0025/0026）。

    def write_review(
        self,
        *,
        reviewer_role: str,
        subject_type: str | ReviewSubjectType,
        subject_ref: str,
        decision: str | ReviewDecision,
        rationale: str | None = None,
        required_changes: Sequence[str] = (),
        reviewer_agent: str | None = None,
        body: str = "",
        date: str | None = None,
        subject_short: str | None = None,
    ) -> Review:
        """Write a REVIEW envelope to ``reviews_dir``（v1.1，per ADR-0017/0025）。

        Args:
            reviewer_role: 评审者角色 code（允许 reserved 如 ADMIN）。
            subject_type: ``ReviewSubjectType`` 枚举或同名字符串
                （``"task"`` / ``"report"`` / ``"role_switch"`` / ``"code_change"``）。
            subject_ref: 被评对象引用。
            decision: ``ReviewDecision`` 枚举或字符串
                （``"approved"`` / ``"rejected"`` / ``"needs_changes"`` /
                ``"abstained"`` / ``"needs_human"``）。
                ``"needs_human"`` 表示主动升级人工审批（ADR-0025）；
                返回的 Review 处于 pending 状态，须调用
                ``mark_human_approved()`` 完成闭环。
            rationale: 可选自由文本理由。
            required_changes: 当 ``decision == NEEDS_CHANGES`` 时必须非空。
            reviewer_agent: 可选；标识具体 session / agent 实例。
            body: REVIEW Markdown body。
            date: 强制日期覆盖（``YYYYMMDD``）；默认 = 今天。便于测试。
            subject_short: 可选；显式覆盖文件名 ``-on-{slug}`` 段。

        Returns:
            新写入的 :class:`Review` 实例。

        Raises:
            ValidationError: reviewer_role 不合 role-code grammar；
                decision/subject_type 不在枚举内；needs_changes 但
                required_changes 空；schema 校验失败。
        """
        decision_enum = self._coerce_review_decision(decision)
        subject_type_enum = self._coerce_review_subject_type(subject_type)

        cleaned_required = tuple(
            s.strip() for s in required_changes if s and str(s).strip()
        )

        if decision_enum is ReviewDecision.NEEDS_CHANGES and not cleaned_required:
            raise ValidationError(
                "decision='needs_changes' requires non-empty required_changes",
                issues=[
                    ValidationIssue(
                        severity="error",
                        field="required_changes",
                        message=(
                            "needs_changes decision must list at least one "
                            "non-blank item; use 'rejected' if there is nothing "
                            "actionable"
                        ),
                    )
                ],
            )

        role_issues = validate_role_code(
            reviewer_role, field="reviewer_role", allow_reserved=True
        )
        role_errors = [i for i in role_issues if i.severity == "error"]
        if role_errors:
            raise ValidationError(
                f"invalid reviewer_role {reviewer_role!r}",
                issues=role_errors,
            )

        if not subject_ref or not str(subject_ref).strip():
            raise ValueError("subject_ref must be a non-empty string")
        subject_ref = str(subject_ref).strip()

        # v1.0 boundary 强制（per ADR-0020 + TASK-005 §决议 3）：
        # 在写盘之前调 assert_boundary。target 角色仅当 subject 是
        # TASK / REPORT 文件且能解析出 recipient 时才传——code_change
        # / role_switch / 不存在的文件路径都跳过 target 检查（target
        # 为 None 时 NO_WORKER_REVIEWS_GOVERNANCE 永不触发，是 conservative
        # default）。assert_boundary 失败立即 raise，文件不会被创建。
        target_role: str | None = None
        if subject_type_enum in (ReviewSubjectType.TASK, ReviewSubjectType.REPORT):
            target_role = self._infer_review_target_role(
                subject_type_enum, subject_ref
            )
        with contextlib.suppress(TaskNotFoundError, FileNotFoundError):
            # project 未 initialized 时 self.config 抛 → 跳过 boundary
            # （test 场景常出）。production 中 init 是 write_review 的
            # 前置条件，此分支事实上不会命中。
            self.assert_boundary(
                reviewer_role,
                "review_decision",
                target_role=target_role,
            )

        date_str = date if date is not None else today_iso()
        slug = subject_short or _derive_review_subject_short(subject_ref)
        if not REVIEW_SUBJECT_SHORT_RE.fullmatch(slug):
            raise ValidationError(
                f"derived subject_short {slug!r} from subject_ref "
                f"{subject_ref!r} is not a legal slug; pass subject_short= explicitly",
                issues=[
                    ValidationIssue(
                        severity="error",
                        field="subject_short",
                        message=(
                            f"slug must match {REVIEW_SUBJECT_SHORT_RE.pattern}"
                        ),
                    )
                ],
            )

        reviews_dir = self.reviews_dir
        reviews_dir.mkdir(parents=True, exist_ok=True)
        archive_dir = self.log_dir / "reviews"

        decided_at_iso = _now_iso()

        for _ in range(_MAX_WRITE_RETRIES):
            existing = _existing_filenames_for_seq(reviews_dir, archive_dir)
            sequence = next_sequence(existing, date=date_str, kind="review")
            filename = build_review_filename(
                date=date_str,
                sequence=sequence,
                reviewer=reviewer_role,
                subject_short=slug,
            )
            review_id = filename[: -len(".md")]

            fm: dict[str, object] = {
                "protocol": PROTOCOL_NAME,
                "version": PROTOCOL_VERSION,
                "type": "REVIEW",
                "sender": reviewer_role,
                "review_id": review_id,
                "subject_type": subject_type_enum.value,
                "subject_ref": subject_ref,
                "reviewer_role": reviewer_role,
                "decision": decision_enum.value,
                "decided_at": decided_at_iso,
            }
            if reviewer_agent:
                fm["reviewer_agent"] = reviewer_agent
            if rationale:
                fm["rationale"] = rationale
            if cleaned_required:
                fm["required_changes"] = list(cleaned_required)

            schema_issues = validate_envelope_frontmatter(fm, "REVIEW")
            if schema_issues:
                # Validator 还报错 = 上层 logic 有遗漏；不应继续写盘。
                raise ValidationError(
                    "REVIEW frontmatter failed JSON Schema validation",
                    issues=schema_issues,
                )

            text = assemble_review_file(fm, body)
            payload = text.encode("utf-8")

            target = reviews_dir / filename
            try:
                fd = os.open(
                    os.fspath(target),
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                )
            except FileExistsError:
                continue

            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(payload)
            except BaseException:
                with contextlib.suppress(OSError):
                    target.unlink()
                raise

            mtime = _dt.datetime.fromtimestamp(target.stat().st_mtime)
            decided_at_dt = _dt.datetime.fromisoformat(decided_at_iso)
            return Review(
                path=target,
                filename=filename,
                review_id=review_id,
                date=date_str,
                sequence=sequence,
                subject_type=subject_type_enum,
                subject_ref=subject_ref,
                reviewer_role=reviewer_role,
                reviewer_agent=reviewer_agent,
                decision=decision_enum,
                rationale=rationale,
                required_changes=cleaned_required,
                decided_at=decided_at_dt,
                body=body,
                is_archived=False,
                mtime=mtime,
            )

        raise RuntimeError(
            f"failed to reserve a review sequence after "
            f"{_MAX_WRITE_RETRIES} retries"
        )

    def mark_human_approved(
        self,
        review_id: str,
        *,
        approver: str,
        decision: str | HumanApprovalDecision,
        channel: str | HumanApprovalChannel,
        comment: str | None = None,
        device_id: str | None = None,
        ip: str | None = None,
        auth_method: str | None = None,
    ) -> Review:
        """Record a human approval decision on a ``needs_human`` REVIEW file.

        Reads the existing REVIEW file, appends ``human_approval`` to its
        frontmatter, writes it back in-place, and returns the updated
        :class:`Review` object.

        Args:
            review_id: The stable review id (filename stem without ``.md``).
            approver: Agent code of the human approver; MUST be layer=admin.
            decision: ``HumanApprovalDecision`` or string ``"approve"`` / ``"reject"``.
            channel: Channel of the approval (``"mobile"`` / ``"cli"`` / ``"web"`` /
                ``"manual_file_edit"``).
            comment: Optional free-text comment.
            device_id: Optional device identifier for audit evidence.
            ip: Optional IP address for audit evidence.
            auth_method: Optional auth method (``"session"`` / ``"biometric"`` /
                ``"password"``).

        Raises:
            TaskNotFoundError: The REVIEW file does not exist.
            ValidationError: The existing REVIEW's decision is not ``needs_human``,
                or approver grammar is invalid.
        """
        if isinstance(decision, str):
            try:
                decision_enum = HumanApprovalDecision(decision.strip().lower())
            except ValueError:
                raise ValidationError(
                    f"unknown human_approval decision {decision!r}",
                    issues=[
                        ValidationIssue(
                            severity="error",
                            field="human_approval.decision",
                            message=f"must be 'approve' or 'reject'; got {decision!r}",
                        )
                    ],
                ) from None
        else:
            decision_enum = decision

        if isinstance(channel, str):
            try:
                channel_enum = HumanApprovalChannel(channel.strip().lower())
            except ValueError:
                raise ValidationError(
                    f"unknown channel {channel!r}",
                    issues=[
                        ValidationIssue(
                            severity="error",
                            field="human_approval.channel",
                            message=(
                                f"must be one of {[c.value for c in HumanApprovalChannel]}; "
                                f"got {channel!r}"
                            ),
                        )
                    ],
                ) from None
        else:
            channel_enum = channel

        role_issues = validate_role_code(approver, field="approver", allow_reserved=True)
        role_errors = [i for i in role_issues if i.severity == "error"]
        if role_errors:
            raise ValidationError(
                f"invalid approver role code {approver!r}",
                issues=role_errors,
            )

        # Find the review file (active or archived)
        review_path: pathlib.Path | None = None
        for candidate_dir in (self.reviews_dir, self.log_dir / "reviews"):
            candidate = candidate_dir / f"{review_id}.md"
            if candidate.exists():
                review_path = candidate
                break
        if review_path is None:
            raise TaskNotFoundError(f"review {review_id!r} not found", query=review_id)

        raw_text = review_path.read_text(encoding="utf-8")
        fm_text, body = split_frontmatter(raw_text)
        fm_dict = parse_frontmatter_raw(raw_text)

        existing_decision = fm_dict.get("decision", "")
        if existing_decision != ReviewDecision.NEEDS_HUMAN.value:
            raise ValidationError(
                f"review {review_id!r} has decision={existing_decision!r}; "
                f"mark_human_approved only applies to needs_human reviews",
                issues=[
                    ValidationIssue(
                        severity="error",
                        field="decision",
                        message=(
                            "mark_human_approved requires decision='needs_human'; "
                            f"got {existing_decision!r}"
                        ),
                    )
                ],
            )

        approved_at_iso = _now_iso()
        ha_dict: dict[str, object] = {
            "approver": approver,
            "decision": decision_enum.value,
            "approved_at": approved_at_iso,
            "channel": channel_enum.value,
        }
        if comment:
            ha_dict["comment"] = comment
        evidence: dict[str, object] = {}
        if device_id:
            evidence["device_id"] = device_id
        if ip:
            evidence["ip"] = ip
        if auth_method:
            evidence["auth_method"] = auth_method
        if evidence:
            ha_dict["evidence"] = evidence

        fm_dict["human_approval"] = ha_dict

        import yaml as _yaml
        new_fm_text = _yaml.dump(
            fm_dict,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        ).rstrip()
        new_text = (
            FRONTMATTER_DELIMITER
            + "\n"
            + new_fm_text
            + "\n"
            + FRONTMATTER_DELIMITER
            + "\n"
            + body
        )
        review_path.write_text(new_text, encoding="utf-8")

        evidence_obj = (
            HumanApprovalEvidence(
                device_id=str(evidence.get("device_id")) if "device_id" in evidence else None,
                ip=str(evidence.get("ip")) if "ip" in evidence else None,
                auth_method=str(evidence.get("auth_method")) if "auth_method" in evidence else None,  # type: ignore[arg-type]
            )
            if evidence
            else None
        )
        human_approval_obj = HumanApproval(
            approver=approver,
            decision=decision_enum,
            approved_at=_dt.datetime.fromisoformat(approved_at_iso),
            channel=channel_enum,
            comment=comment or None,
            evidence=evidence_obj,
        )

        # Re-hydrate the review from the updated file
        new_text = review_path.read_text(encoding="utf-8")
        new_fm = parse_frontmatter_raw(new_text)
        _, new_body = split_frontmatter(new_text)
        new_parsed = parse_review_filename(review_path.name)
        assert new_parsed is not None
        is_archived = (review_path.parent == (self.log_dir / "reviews"))
        review_obj = _hydrate_review(review_path, new_fm, new_body, new_parsed, is_archived=is_archived)
        # review_obj is now a full Review; patch in the parsed HumanApproval object
        return Review(
            path=review_obj.path,
            filename=review_obj.filename,
            review_id=review_obj.review_id,
            date=review_obj.date,
            sequence=review_obj.sequence,
            subject_type=review_obj.subject_type,
            subject_ref=review_obj.subject_ref,
            reviewer_role=review_obj.reviewer_role,
            reviewer_agent=review_obj.reviewer_agent,
            decision=review_obj.decision,
            rationale=review_obj.rationale,
            required_changes=review_obj.required_changes,
            decided_at=review_obj.decided_at,
            body=review_obj.body,
            is_archived=review_obj.is_archived,
            mtime=review_obj.mtime,
            human_approval=human_approval_obj,
        )

    def list_reviews(
        self,
        *,
        reviewer_role: str | None = None,
        decision: str | ReviewDecision | None = None,
        subject_type: str | ReviewSubjectType | None = None,
        status: Literal["open", "archived", "all"] = "open",
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Review]:
        """List REVIEWs, optionally filtered.

        Args:
            reviewer_role: 仅匹配指定评审者角色的 REVIEW。
            decision: 仅匹配指定决议的 REVIEW（接受字符串别名）。
            subject_type: 仅匹配指定 subject_type 的 REVIEW。
            status: ``"open"`` 扫 ``reviews_dir``；``"archived"`` 扫
                ``log/reviews/``；``"all"`` 两者都扫。
            limit / offset: 分页窗口（先排序后切片）。

        Returns:
            按 (date, sequence) 倒序——最新在前。畸形 / 不可解析的
            REVIEW 文件被静默跳过，与 list_tasks/reports 行为一致。
        """
        decision_filter = (
            self._coerce_review_decision(decision) if decision is not None else None
        )
        subject_filter = (
            self._coerce_review_subject_type(subject_type)
            if subject_type is not None
            else None
        )

        directories: list[tuple[pathlib.Path, bool]] = []
        if status in ("open", "all"):
            directories.append((self.reviews_dir, False))
        if status in ("archived", "all"):
            directories.append((self.log_dir / "reviews", True))

        reviews: list[Review] = []
        for directory, archived in directories:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                review = _try_load_review(entry, is_archived=archived)
                if review is None:
                    continue
                if reviewer_role is not None and review.reviewer_role != reviewer_role:
                    continue
                if decision_filter is not None and review.decision is not decision_filter:
                    continue
                if subject_filter is not None and review.subject_type is not subject_filter:
                    continue
                reviews.append(review)

        def _sort_key(r: Review) -> tuple[str, int]:
            parsed = parse_review_filename(r.filename)
            if parsed is None:
                return ("", 0)
            return (parsed.date, parsed.sequence)

        reviews.sort(key=_sort_key, reverse=True)

        end = None if limit is None else offset + max(0, limit)
        return reviews[offset:end]

    def read_review(self, filename_or_id: str) -> Review:
        """Load one REVIEW by filename or review id.

        Resolution: 先扫 ``reviews_dir``，再扫 ``log/reviews/``。

        Raises:
            TaskNotFoundError: 没有匹配（复用 TaskNotFoundError，与
                read_report / read_issue 一致；v1.x 不新建专属异常）。
            ProtocolViolation / ValidationError: 文件存在但畸形。
        """
        target, archived = self._resolve_review_file(filename_or_id)
        if target is None:
            raise TaskNotFoundError(
                f"no review matches {filename_or_id!r}",
                query=filename_or_id,
            )
        return _load_review_strict(target, is_archived=archived)

    def archive_review(self, filename_or_id: str) -> Review:
        """Move a REVIEW to ``log/reviews/``.

        与 :meth:`archive_task` 不同，REVIEW 没有"关联文件"要顺带移动
        ——它是终点。Idempotent：归档已归档的 REVIEW 直接返回当前状态。

        Raises:
            TaskNotFoundError: 没有匹配文件。
            ProtocolViolation / ValidationError: 文件畸形（不归档，
                先暴露问题）。
        """
        source, archived = self._resolve_review_file(filename_or_id)
        if source is None:
            raise TaskNotFoundError(
                f"cannot archive: no review matches {filename_or_id!r}",
                query=filename_or_id,
            )
        if archived:
            return _load_review_strict(source, is_archived=True)

        log_reviews_dir = self.log_dir / "reviews"
        log_reviews_dir.mkdir(parents=True, exist_ok=True)
        destination = log_reviews_dir / source.name
        source.replace(destination)
        return _load_review_strict(destination, is_archived=True)

    def _resolve_review_file(
        self, filename_or_id: str
    ) -> tuple[pathlib.Path | None, bool]:
        """Resolve a user handle to a REVIEW path. Open dir wins over archive."""
        if REVIEW_FILENAME_RE.fullmatch(filename_or_id):
            for directory, archived in (
                (self.reviews_dir, False),
                (self.log_dir / "reviews", True),
            ):
                candidate = directory / filename_or_id
                if candidate.is_file():
                    return candidate, archived
            return None, False

        # 允许传 stem（无 .md）作为完整 review_id
        if REVIEW_FILENAME_RE.fullmatch(f"{filename_or_id}.md"):
            return self._resolve_review_file(f"{filename_or_id}.md")

        prefix = filename_or_id
        for directory, archived in (
            (self.reviews_dir, False),
            (self.log_dir / "reviews", True),
        ):
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                if not entry.is_file():
                    continue
                parsed = parse_review_filename(entry.name)
                if parsed is None:
                    continue
                if entry.name.startswith(prefix + "-") or entry.stem == prefix:
                    return entry, archived
        return None, False

    # ── Failure & Recovery (v1.0, per ADR-0019 + TASK-006) ──────────

    def report_failure(self, failure: Failure) -> FailureReceipt:
        """Acknowledge a runtime failure（v1.0，per ADR-0019）。

        v1.0 reference impl 不写盘——本方法只做 3 件事：

        1. 触发 stub 事件 ``FAILURE_DETECTED``（见 :meth:`_emit_event_stub`；
           TASK-007 接事件后会换成真实 watcher 推送）；
        2. 返回 :class:`FailureReceipt` 给 caller，包含 accepted_at
           时间戳；
        3. 不调用 :meth:`apply_recovery` ——是否触发 recovery 由 caller
           决定（per ADR-0019 §design-details "Failure 与 Recovery 解
           耦"）。

        Args:
            failure: :class:`Failure` 内存记录。caller 自己构造（含
                detected_at / evidence / suggested_recovery 等）。

        Returns:
            :class:`FailureReceipt`，``accepted_at = datetime.now(UTC)``。

        Raises:
            TypeError: ``failure`` 不是 :class:`Failure` 实例。
        """
        if not isinstance(failure, Failure):
            raise TypeError(
                f"failure must be a Failure instance, got {type(failure).__name__}"
            )
        emitted = self._emit_event_stub(
            "FAILURE_DETECTED", subject=failure
        )
        return FailureReceipt(
            failure=failure,
            accepted_at=_dt.datetime.now(_dt.timezone.utc),
            event_emitted=emitted,
        )

    def apply_recovery(
        self,
        failure: Failure,
        action: RecoveryAction | str | None = None,
        *,
        task_path: pathlib.Path | str | None = None,
        last_report_path: pathlib.Path | str | None = None,
        leader_recipient: str | None = None,
        rollback_target_commit: str | None = None,
        rollback_affected_files: Sequence[str] | None = None,
    ) -> RecoveryOutcome:
        """Run a single recovery action against a failure.

        v1.0 把 5 类 RecoveryAction 映射到 :mod:`fcop.core.recovery`
        reference-impl 函数（per TASK-006 §决议 3）：

        ============  ====================================================
        Action        v1.0 行为
        ============  ====================================================
        ``RETRY``     返回 :class:`RetryPlan`（不实际重试）
        ``RESUME``    返回 :class:`ResumePayload`（只读 metadata）
        ``ROLLBACK``  返回 :class:`RollbackPlan` with ``executed=False``
        ``ABORT``     写一份 ``status=aborted`` REPORT（实际写盘）
        ``ESCALATE`` 写一份 ISSUE 给 leader（实际写盘）
        ============  ====================================================

        Args:
            failure: :class:`Failure` 实例。
            action: 显式 RecoveryAction；``None`` 时取
                ``failure.suggested_recovery``。两者都 ``None`` 时
                raise ``ValueError``。
            task_path: RETRY / RESUME 必填——指向 TASK 文件。可以是
                绝对路径或相对 project root 的字符串。
            last_report_path: RESUME 可选——上一份 REPORT 路径。
            leader_recipient: ESCALATE 必填——leader 角色 code。
            rollback_target_commit: ROLLBACK 可选——commit hash。
            rollback_affected_files: ROLLBACK 可选——受影响文件清单。

        Returns:
            :class:`RecoveryOutcome`，``recovery`` 是构造好的
            :class:`Recovery` 记录，``plan`` 字段类型与 action 对应。

        Raises:
            ValueError: action 和 failure.suggested_recovery 都为 None；
                必填路径缺失。
        """
        chosen_action = self._coerce_recovery_action(action, failure)
        recovery = build_recovery_record(failure, chosen_action)
        # Emit RECOVERY_INITIATED before doing the work; subscribers see
        # the attempt even if the recovery itself fails partway.
        self._emit_event_stub("RECOVERY_INITIATED", subject=recovery)

        if chosen_action == RecoveryAction.RETRY:
            tp = self._coerce_required_path(task_path, "task_path")
            plan = make_retry_plan(failure, task_path=tp)
            outcome = RecoveryOutcome(
                recovery=recovery, plan=plan, artifact_path=None
            )
            self._emit_event_stub("RECOVERY_COMPLETED", subject=recovery)
            return outcome

        if chosen_action == RecoveryAction.RESUME:
            tp = self._coerce_required_path(task_path, "task_path")
            rp = self._coerce_optional_path(last_report_path)
            session_id = self._build_session_id_from_failure(failure)
            payload = make_resume_payload(
                session_id=session_id,
                task_path=tp,
                last_report_path=rp,
            )
            outcome = RecoveryOutcome(
                recovery=recovery, plan=payload, artifact_path=None
            )
            self._emit_event_stub("RECOVERY_COMPLETED", subject=recovery)
            return outcome

        if chosen_action == RecoveryAction.ROLLBACK:
            rollback_plan = make_rollback_plan(
                target_commit_hash=rollback_target_commit,
                affected_files=tuple(rollback_affected_files or ()),
            )
            outcome = RecoveryOutcome(
                recovery=recovery, plan=rollback_plan, artifact_path=None
            )
            self._emit_event_stub("RECOVERY_COMPLETED", subject=recovery)
            return outcome

        if chosen_action == RecoveryAction.ABORT:
            if failure.subject_task_id is None:
                raise ValueError(
                    "ABORT recovery requires failure.subject_task_id "
                    "(no task to abort otherwise)"
                )

            def _write_report_adapter(
                *, sender: str, recipient: str, ref_task: str,
                body: str, status: str
            ) -> Report:
                return self.write_report(
                    task_id=failure.subject_task_id or "",
                    reporter=sender,
                    recipient=recipient,
                    body=body,
                    status=status,  # type: ignore[arg-type]
                )

            recipient = self._infer_task_sender(failure.subject_task_id) or "ADMIN"
            artifact = make_abort_artifact(
                failure,
                write_report_fn=_write_report_adapter,
                ref_task=failure.subject_task_id,
                sender=failure.subject_agent_code,
                recipient=recipient,
            )
            outcome = RecoveryOutcome(
                recovery=recovery,
                plan=artifact,
                artifact_path=artifact,
            )
            self._emit_event_stub("RECOVERY_COMPLETED", subject=recovery)
            return outcome

        if chosen_action == RecoveryAction.ESCALATE:
            if not leader_recipient:
                raise ValueError(
                    "ESCALATE recovery requires leader_recipient= "
                    "(role code of the escalation target)"
                )

            def _write_issue_adapter(
                *, sender: str, recipient: str, title: str,
                severity: str, body: str
            ) -> Issue:
                annotated_body = (
                    f"> Auto-escalated to: `{recipient}`\n\n{body}"
                )
                return self.write_issue(
                    reporter=sender,
                    summary=title,
                    body=annotated_body,
                    severity=severity,
                )

            artifact = make_escalate_artifact(
                failure,
                write_issue_fn=_write_issue_adapter,
                sender=failure.subject_agent_code,
                leader_recipient=leader_recipient,
            )
            outcome = RecoveryOutcome(
                recovery=recovery,
                plan=artifact,
                artifact_path=artifact,
            )
            self._emit_event_stub("RECOVERY_COMPLETED", subject=recovery)
            return outcome

        # Unreachable (enum exhausts), but keeps type checker happy.
        raise ValueError(f"unsupported recovery action: {chosen_action!r}")

    def recover_session(
        self,
        session_id: str,
        action: SessionRecoveryAction | str,
        *,
        task_path: pathlib.Path | str | None = None,
        last_report_path: pathlib.Path | str | None = None,
        rollback_target_commit: str | None = None,
        rollback_affected_files: Sequence[str] | None = None,
        ref_task: str | None = None,
        recipient: str | None = None,
    ) -> SessionRecoveryResult:
        """Resume / rollback / abort a session（v1.0，per ADR-0019）。

        action 仅接受 3 个值——RETRY / ESCALATE 不是 session 级动作
        （前者是 task 级，后者跨 session）；想要它们走
        :meth:`apply_recovery`。

        Args:
            session_id: 接受两种形状（per TASK-006 §决议 5）——
                ``TASK-...:agent``（per ADR-0019）或
                ``sess-YYYYMMDD-agent-NNN``（0.7.x 历史）。
            action: ``"resume"`` / ``"rollback"`` / ``"abort"`` 字符串
                或 :class:`SessionRecoveryAction` 枚举；任何其他值会被
                ``ValueError`` 拒。
            task_path: ``resume`` 必填。
            last_report_path: ``resume`` 可选。
            rollback_target_commit: ``rollback`` 可选。
            rollback_affected_files: ``rollback`` 可选。
            ref_task: ``abort`` 必填——TASK 文件路径或 task_id。
            recipient: ``abort`` 必填——REPORT 的 recipient 角色。

        Returns:
            :class:`SessionRecoveryResult`，``outcome`` 字段是
            ``"succeeded"`` / ``"session_not_found"`` / ``"failed"``。
            session_id 解析失败时返回 outcome=session_not_found
            （**不**抛异常）；其他错误（如 abort 缺 ref_task）抛
            ``ValueError`` 由 caller 处理。

        Raises:
            ValueError: action 不在 3 值内、必填参数缺失。
        """
        action_enum = self._coerce_session_action(action)

        try:
            parsed = parse_session_id(session_id)
        except ValueError as exc:
            self._emit_event_stub(
                "SESSION_LOST",
                subject={"session_id": session_id, "reason": str(exc)},
            )
            return SessionRecoveryResult(
                session_id=session_id,
                action=action_enum,
                outcome="session_not_found",
                payload=None,
                error=str(exc),
            )

        if action_enum == SessionRecoveryAction.RESUME:
            tp = self._coerce_required_path(task_path, "task_path")
            rp = self._coerce_optional_path(last_report_path)
            payload = make_resume_payload(
                session_id=parsed.raw,
                task_path=tp,
                last_report_path=rp,
            )
            return SessionRecoveryResult(
                session_id=parsed.raw,
                action=action_enum,
                outcome="succeeded",
                payload=payload,
            )

        if action_enum == SessionRecoveryAction.ROLLBACK:
            plan = make_rollback_plan(
                target_commit_hash=rollback_target_commit,
                affected_files=tuple(rollback_affected_files or ()),
            )
            return SessionRecoveryResult(
                session_id=parsed.raw,
                action=action_enum,
                outcome="succeeded",
                payload=plan,
            )

        # abort
        if not ref_task:
            raise ValueError("abort action requires ref_task=")
        if not recipient:
            raise ValueError("abort action requires recipient=")
        report = self.write_report(
            task_id=ref_task,
            reporter=parsed.agent_code,
            recipient=recipient,
            body=(
                f"# Aborted via recover_session\n\n"
                f"- session_id: `{parsed.raw}`\n"
                f"- agent_code: `{parsed.agent_code}`\n"
            ),
            status="aborted",
        )
        return SessionRecoveryResult(
            session_id=parsed.raw,
            action=action_enum,
            outcome="succeeded",
            payload=report.path,
        )

    # ── Event subscription & polling (v1.0, per ADR-0018 + TASK-007) ──

    def subscribe_events(
        self,
        types: Sequence[EventType | str] | None = None,
        callback: Callable[[Event], None] | None = None,
    ) -> EventSubscription:
        """Subscribe to runtime events（v1.0，per ADR-0018）。

        本方法**不**启动后台线程 —— caller 必须显式调
        :meth:`poll_once` 才会触发文件类事件（per TASK-007 §决议 3）。
        同步类事件（FAILURE_DETECTED / BOUNDARY_VIOLATED 等）在被
        :meth:`report_failure` / :meth:`write_review` 等触发时立即
        发到所有订阅者。

        Args:
            types: 关心的事件类型；``None`` 表示订阅所有 12 类。
                可传 :class:`EventType` 枚举或字符串（自动 coerce）。
                未知字符串会立即 raise ``ValueError``。
            callback: 接收 :class:`Event` 的同步回调；``None`` 时只是
                注册一个静默订阅（事件仍会进 ``Project`` 内部 log，
                便于 caller 之后通过 :attr:`_emitted_events` 取）。

        Returns:
            :class:`EventSubscription` —— 调它的 ``unsubscribe()`` 可
            取消。Subscription 不持有 Project 强引用之外的资源，可
            安全丢弃。

        Raises:
            ValueError: types 含未知字符串。
        """

        if types is None:
            normalized: tuple[EventType, ...] | None = None
        else:
            buf: list[EventType] = []
            for t in types:
                if isinstance(t, EventType):
                    buf.append(t)
                elif isinstance(t, str):
                    try:
                        buf.append(EventType(t.upper()))
                    except ValueError as exc:
                        raise ValueError(
                            f"unknown EventType {t!r}; valid: "
                            f"{[e.value for e in EventType]}"
                        ) from exc
                else:
                    raise ValueError(
                        f"types items must be EventType / str; got "
                        f"{type(t).__name__}"
                    )
            normalized = tuple(buf)

        sub = EventSubscription(
            project=self, types=normalized, callback=callback
        )
        self._subscriptions.append(sub)
        return sub

    def poll_once(self) -> list[Event]:
        """Run one polling cycle and emit all derived events.

        v1.0 reference impl 行为（per TASK-007 §决议 3）：

        1. 调 :func:`fcop.core.events.scan_workspace` 拍当前快照
        2. 与上次快照（首次为 ``None``）调 :func:`compute_diff` 派生事件
        3. 把派生事件按顺序发到所有订阅者（含静默订阅）
        4. 把当前快照存到 ``self._last_watcher_state`` 以备下次

        Returns:
            按 :func:`compute_diff` 排序的事件列表。Caller 可用此返
            回值直接遍历事件，无需注册 callback。
        """

        curr = scan_workspace(
            workspace_dir=self.workspace_dir, project_root=self._path
        )
        events = compute_diff(prev=self._last_watcher_state, curr=curr)
        self._last_watcher_state = curr
        for ev in events:
            self._dispatch_event(ev)
        return events

    @property
    def _subscriptions(self) -> list[EventSubscription]:
        """Lazy per-instance subscription registry."""
        try:
            return cast(list[EventSubscription], self.__dict__["_subscriptions_list"])
        except KeyError:
            buf: list[EventSubscription] = []
            self.__dict__["_subscriptions_list"] = buf
            return buf

    @property
    def _last_watcher_state(self) -> WatcherState | None:
        return self.__dict__.get("_last_watcher_state_cache")

    @_last_watcher_state.setter
    def _last_watcher_state(self, value: WatcherState | None) -> None:
        self.__dict__["_last_watcher_state_cache"] = value

    @property
    def _emitted_events(self) -> list[Event]:
        """Per-instance log of every event the project has dispatched.

        Useful for tests and post-hoc debugging. Production callers
        should use :meth:`subscribe_events` instead of polling this list.
        """
        try:
            return cast(list[Event], self.__dict__["_emitted_events_list"])
        except KeyError:
            buf: list[Event] = []
            self.__dict__["_emitted_events_list"] = buf
            return buf

    def _dispatch_event(self, event: Event) -> None:
        """Send ``event`` to every matching subscription + record it."""
        self._emitted_events.append(event)
        for sub in list(self._subscriptions):
            if sub.types is not None and event.event_type not in sub.types:
                continue
            if sub.callback is not None:
                with contextlib.suppress(Exception):
                    # subscriber 抛错不应影响其他 subscriber 或主路径；
                    # v1.0 静默吞，由 caller 自己加 logging
                    sub.callback(event)

    # ── Failure / Recovery internal helpers ──────────────────────────

    @property
    def _emit_event_stub_calls(self) -> list[tuple[str, object]]:
        """Backward-compat shim for TASK-006 tests.

        TASK-007 把真实 emitter 接进来后，此 property 仍返回每次
        :meth:`_emit_event_stub` 调用的 (event_type_str, subject)
        元组列表。新代码应订阅 :meth:`subscribe_events` 而不是直接
        读这个 list。
        """
        try:
            return cast(list[tuple[str, object]], self.__dict__["_emit_event_stub_calls_list"])
        except KeyError:
            buf: list[tuple[str, object]] = []
            self.__dict__["_emit_event_stub_calls_list"] = buf
            return buf

    def _emit_event_stub(self, event_type: str, *, subject: object) -> bool:
        """Bridge legacy stub call sites to the v1.0 event bus.

        TASK-006 wrote ``self._emit_event_stub("FAILURE_DETECTED",
        subject=...)`` from ``report_failure`` / ``apply_recovery``.
        This shim now (1) appends to the legacy log so
        ``test_project_failure`` keeps observing the same surface and
        (2) translates the call into a real :class:`Event` and
        dispatches it through the new bus.
        """

        # 1) preserve legacy log shape for TASK-006 tests
        self._emit_event_stub_calls.append((event_type, subject))

        # 2) translate to a real Event when the type is in v1.0 vocab
        try:
            etype = EventType(event_type)
        except ValueError:
            return True  # unknown type → legacy log only

        subject_dict: dict[str, object] = {}
        if isinstance(subject, Failure):
            subject_dict["failure_type"] = subject.failure_type.value
            subject_dict["actor"] = subject.subject_agent_code
            if subject.subject_task_id:
                subject_dict["task_id"] = subject.subject_task_id
        elif isinstance(subject, Recovery):
            subject_dict["recovery_action"] = subject.recovery_action.value
            subject_dict["actor"] = subject.trigger_failure.subject_agent_code
            if subject.trigger_failure.subject_task_id:
                subject_dict["task_id"] = subject.trigger_failure.subject_task_id
        elif isinstance(subject, dict):
            subject_dict.update(subject)
        elif subject is not None:
            subject_dict["payload"] = repr(subject)

        ev = make_event(
            etype,
            subject=subject_dict,
            source=EventSource(
                kind=EventSourceKind.CALLBACK, watcher=WATCHER_ID
            ),
        )
        self._dispatch_event(ev)
        return True

    def _coerce_recovery_action(
        self,
        action: RecoveryAction | str | None,
        failure: Failure,
    ) -> RecoveryAction:
        if action is None:
            if failure.suggested_recovery is None:
                raise ValueError(
                    "apply_recovery: action= is required when failure has "
                    "no suggested_recovery"
                )
            return failure.suggested_recovery
        if isinstance(action, RecoveryAction):
            return action
        if isinstance(action, str):
            try:
                return RecoveryAction(action.upper())
            except ValueError as exc:
                raise ValueError(
                    f"unknown RecoveryAction string {action!r}; "
                    f"valid: {[a.value for a in RecoveryAction]}"
                ) from exc
        raise ValueError(
            f"action must be RecoveryAction / str / None; got {type(action).__name__}"
        )

    @staticmethod
    def _coerce_session_action(
        action: SessionRecoveryAction | str,
    ) -> SessionRecoveryAction:
        if isinstance(action, SessionRecoveryAction):
            return action
        if isinstance(action, str):
            try:
                return SessionRecoveryAction(action.lower())
            except ValueError as exc:
                raise ValueError(
                    f"unknown SessionRecoveryAction {action!r}; "
                    f"valid: {[a.value for a in SessionRecoveryAction]} "
                    "(RETRY / ESCALATE are not session-level; use "
                    "apply_recovery)"
                ) from exc
        raise ValueError(
            f"action must be SessionRecoveryAction / str; "
            f"got {type(action).__name__}"
        )

    def _coerce_required_path(
        self,
        path: pathlib.Path | str | None,
        field_name: str,
    ) -> pathlib.Path:
        if path is None:
            raise ValueError(f"{field_name}= is required for this recovery action")
        p = pathlib.Path(path)
        if not p.is_absolute():
            p = self._path / p
        return p

    def _coerce_optional_path(
        self,
        path: pathlib.Path | str | None,
    ) -> pathlib.Path | None:
        if path is None:
            return None
        return self._coerce_required_path(path, "_optional")

    def _build_session_id_from_failure(self, failure: Failure) -> str:
        """Best-effort session_id 构造 from Failure（per TASK-006 §决议 5 形状 A）。"""
        if failure.subject_task_id:
            return f"{failure.subject_task_id}:{failure.subject_agent_code}"
        # 退到形状 B 大致：sess-{detected_date}-{agent_lower}-000
        date = failure.detected_at.strftime("%Y%m%d")
        return f"sess-{date}-{failure.subject_agent_code.lower()}-000"

    def _infer_task_sender(self, task_id_or_path: str) -> str | None:
        """查 TASK 文件的 sender；用于 ABORT recovery 写 REPORT 时确定 recipient。"""
        try:
            path, _ = self._resolve_task_file(task_id_or_path)
        except Exception:
            return None
        if path is None:
            return None
        try:
            text = path.read_text(encoding="utf-8")
            raw_fm = parse_frontmatter_raw(text)
        except Exception:
            return None
        sender = raw_fm.get("sender") or raw_fm.get("from")
        return str(sender).strip() if sender else None

    def _infer_review_target_role(
        self,
        subject_type: ReviewSubjectType,
        subject_ref: str,
    ) -> str | None:
        """从 REVIEW 的 subject_ref 推断被评对象的 role code（boundary 用）。

        语义：subject 是某个 envelope 文件，它的 ``sender`` 字段标识
        了"谁产出了它"——boundary 检查时这就是 review 的 target role。

        - TASK：sender = 派任务的人 → target_role = sender
        - REPORT：sender = 写报告的人 → target_role = sender
        - role_switch / code_change / 不存在的路径 → ``None``

        无法解析时返回 ``None``（不抛错；review 仍会被写入，只是不
        触发 NO_WORKER_REVIEWS_GOVERNANCE 检查——这是 conservative
        default：信息不足时不挡）。
        """
        if subject_type not in (ReviewSubjectType.TASK, ReviewSubjectType.REPORT):
            return None
        if not subject_ref:
            return None
        # subject_ref 可能是绝对路径、相对项目根的相对路径、或 task_id
        # 短手；只有"能落到一个真实文件"时才查 frontmatter。
        candidate = pathlib.Path(subject_ref)
        if not candidate.is_absolute():
            candidate = self._path / candidate
        if not candidate.is_file():
            return None
        try:
            text = candidate.read_text(encoding="utf-8")
            raw_fm = parse_frontmatter_raw(text)
        except Exception:
            return None
        sender = raw_fm.get("sender") or raw_fm.get("from")
        return str(sender).strip() if sender else None

    @staticmethod
    def _coerce_review_decision(value: str | ReviewDecision) -> ReviewDecision:
        """Strict coerce —— 拒绝任何未知值（v1.1 已包含 needs_human）。"""
        if isinstance(value, ReviewDecision):
            return value
        if isinstance(value, str):
            try:
                return ReviewDecision(value)
            except ValueError as exc:
                raise ValidationError(
                    f"unknown decision {value!r}",
                    issues=[
                        ValidationIssue(
                            severity="error",
                            field="decision",
                            message=(
                                f"decision must be one of "
                                f"{[d.value for d in ReviewDecision]}; "
                                f"got {value!r}."
                            ),
                        )
                    ],
                ) from exc
        raise TypeError(f"decision must be str or ReviewDecision, got {type(value).__name__}")

    @staticmethod
    def _coerce_review_subject_type(value: str | ReviewSubjectType) -> ReviewSubjectType:
        if isinstance(value, ReviewSubjectType):
            return value
        if isinstance(value, str):
            try:
                return ReviewSubjectType(value)
            except ValueError as exc:
                raise ValidationError(
                    f"unknown subject_type {value!r}",
                    issues=[
                        ValidationIssue(
                            severity="error",
                            field="subject_type",
                            message=(
                                f"subject_type must be one of "
                                f"{[s.value for s in ReviewSubjectType]}; "
                                f"got {value!r}"
                            ),
                        )
                    ],
                ) from exc
        raise TypeError(
            f"subject_type must be str or ReviewSubjectType, got {type(value).__name__}"
        )

    # ── Boundary (v1.0 / Capability) ──────────────────────────────────
    #
    # ADR-0020 4 条规则的 user-facing 入口。判定逻辑在
    # :mod:`fcop.core.boundary`；本层只把 fcop.json 角色查 →
    # validate_action 调 → 整合违规列表 / raise 包好。
    #
    # 设计原则（per TASK-005 §决议 3）：
    # - opt-in 显式查询：boundary_violations 永不 raise，返回列表
    # - opt-in 守门 wrapper：assert_boundary 违规即 raise
    # - v1.0 仅 write_review 主动接 assert_boundary（reviewer →
    #   review_decision → subject 角色）；write_task / write_report /
    #   write_issue 维持 0.7.x 行为不变（v1.1 通过 enforce_boundary 参数
    #   逐步引入）。

    def boundary_violations(
        self,
        actor_role: str,
        action: str,
        *,
        target_role: str | None = None,
    ) -> list[BoundaryViolation]:
        """查询 actor 执行 action（可选 target）的 boundary 违规。

        永不 raise（除非 fcop.json 本身畸形）。空列表 ≡ 该操作允许。

        Args:
            actor_role: 主语角色 code。必须已通过 role-code 校验
                （allow_reserved=True，即 ADMIN / SYSTEM 也可）。
            action: capability token（如 ``"review_decision"`` /
                ``"spawn_agent"`` / ``"modify_code"``）。词表外 token
                会得到一条 severity="warning" 的 UNKNOWN_CAPABILITY 记录。
            target_role: 可选；review_decision 等需要受影响方的动作传。

        Returns:
            :class:`BoundaryViolation` 列表（可能是 error / warning 混合）。

        Raises:
            ConfigError: project 未 initialized 或 fcop.json 缺失。
            BoundaryViolationError: 仅在 fcop.json 把某 role 显式声明
                为 ``layer: "admin"`` 时（NO_ADMIN_PROGRAMMATIC_CREATE
                由 ``lookup_capability`` 直接 raise，不进列表）。
        """
        cfg = self.config
        actor = lookup_capability(actor_role, cfg)
        target = (
            lookup_capability(target_role, cfg)
            if target_role is not None
            else None
        )
        return validate_action(actor, action, target=target)

    def assert_boundary(
        self,
        actor_role: str,
        action: str,
        *,
        target_role: str | None = None,
    ) -> None:
        """守门 wrapper：违规（severity=error）即 raise。

        Warning 级别（如 UNKNOWN_CAPABILITY）不 raise，只在
        :meth:`boundary_violations` 返回里可见。

        Raises:
            BoundaryViolationError: 违规列表包含至少一条 severity="error"。
        """
        violations = self.boundary_violations(
            actor_role, action, target_role=target_role
        )
        errors = [v for v in violations if v.severity == "error"]
        if errors:
            details = "; ".join(f"{v.rule_id}: {v.message[:200]}" for v in errors)
            # Emit BOUNDARY_VIOLATED event before raising, so subscribers
            # see the violation even if the caller swallows the exception.
            try:
                ev = make_event(
                    EventType.BOUNDARY_VIOLATED,
                    subject={
                        "actor": actor_role,
                        "attempted_action": action,
                        **({"target": target_role} if target_role else {}),
                        "rule_id": errors[0].rule_id,
                    },
                    source=EventSource(
                        kind=EventSourceKind.CALLBACK, watcher=WATCHER_ID
                    ),
                )
                self._dispatch_event(ev)
            except Exception:
                # event dispatch must never break the raise path
                pass
            raise BoundaryViolationError(
                f"boundary check failed for {actor_role!r} → {action!r}"
                + (f" → {target_role!r}" if target_role else "")
                + f": {details}",
                violations=errors,
            )

    # ── Suggestions ───────────────────────────────────────────────────

    def drop_suggestion(
        self,
        *,
        content: str,
        context: str = "",
    ) -> pathlib.Path:
        """Drop a proposal file under ``.fcop/proposals/``.

        This is the **pressure valve** for agents who disagree with
        the current FCoP protocol (or want to suggest a change to
        the project's conventions). Rather than editing
        ``fcop-rules.mdc`` / ``fcop-protocol.mdc`` directly — which
        agents MUST NOT do per Rule 2 — they drop a timestamped
        markdown file here and move on. ADMIN reviews async.

        The written file looks like::

            # Suggestion @ 20260423-180512

            **Context**: optional pointer string

            <body verbatim from `content`>

        Args:
            content: The suggestion itself, in the agent's own words.
                Must be non-empty after stripping whitespace; empty
                suggestions carry no information and are almost
                certainly a programming error on the caller side.
            context: Optional free-form reference to whatever
                triggered the suggestion — a task id, a filename, a
                short quote. Not validated; anything goes.

        Returns:
            Absolute :class:`pathlib.Path` of the written file, so
            the caller can echo a clickable link back to ADMIN.

        Raises:
            ValueError: ``content`` is empty or whitespace-only.

        Note:
            Filenames use second-resolution timestamps
            (``YYYYMMDD-HHMMSS.md``). If two suggestions land in the
            same second on the same project a numeric suffix is
            appended so neither call silently loses data — verified
            via an ``O_CREAT | O_EXCL`` open rather than a pre-check.
        """
        body = content.strip()
        if not body:
            raise ValueError(
                "drop_suggestion requires non-empty content; "
                "got an empty / whitespace-only string"
            )

        proposals = self._proposals_dir
        proposals.mkdir(parents=True, exist_ok=True)

        timestamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        header = f"# Suggestion @ {timestamp}\n\n"
        if context.strip():
            # Keep `context` verbatim after stripping; if the caller
            # bothered to pass non-whitespace, preserve their wording.
            header += f"**Context**: {context.strip()}\n\n"
        file_bytes = (header + body + "\n").encode("utf-8")

        # Resolve the final path. The bare timestamp is used first;
        # if someone else beats us to it in the same second we fall
        # back to numeric suffixes. The retry is tiny — sub-second
        # collisions on proposals are vanishingly rare outside of
        # tight test loops.
        path = _write_atomic_unique(
            proposals, stem=timestamp, suffix=".md", data=file_bytes
        )
        return path


# ── module-level helpers ──────────────────────────────────────────────

# Cap for :meth:`Project.status` recent-activity output. Intentionally
# small so callers don't pay for a full directory scan on every status
# call; tweak via a future kwarg when a real use case shows up.
_RECENT_ACTIVITY_LIMIT = 10

# How many times :meth:`Project.write_task` retries on sequence-number
# collisions before bailing out. Ten is generous: the lock window is a
# single ``os.open(O_EXCL)``, so collisions are extremely unlikely
# outside of intentional stress tests.
_MAX_WRITE_RETRIES = 10

# File suffixes that the FCoP grammar allows. ``.md`` is canonical;
# legacy 0.5.x projects sometimes carry ``.fcop``. Anything else is
# ignored entirely when counting.
_FCOP_SUFFIXES = frozenset({".md", ".fcop"})

# Report status values. Kept here instead of in :mod:`fcop.core.schema`
# because reports don't yet have a dedicated ReportFrontmatter model —
# the status rides in ``TaskFrontmatter.extra["status"]`` for 0.6 and
# will migrate when we split report parsing into its own module.
_VALID_REPORT_STATUSES: frozenset[str] = frozenset(
    {"done", "blocked", "in_progress", "aborted"}
)

# Boilerplate for ``workspace/README.md`` written on every init. Kept
# minimal on purpose — the canonical Rule 7.5 explanation lives in
# the bundled ``fcop-rules.mdc`` and ``LETTER-TO-ADMIN.md``; this
# README is just the at-the-spot "you found me, here's what goes here".
_WORKSPACE_README_TEXT = """\
# workspace/

按 FCoP Rule 7.5 / Rule 7.5 per FCoP protocol.

**项目根只放协作元数据；具体产物（代码、脚本、数据）进
`workspace/<slug>/`，一个目的一个 slug。**

**Project root holds coordination metadata only; actual artefacts
(code, scripts, data) live under `workspace/<slug>/` — one slug per
piece of work.**

- 推荐用 MCP 工具 `new_workspace(slug=..., title=..., description=...)`
  创建 slug 子目录（会落 `.workspace.json` 元数据）。
- 也可以手动 `mkdir workspace/<slug>`，`list_workspaces()` 同样能识别。
- 跨 slug 共享的资产放 `workspace/shared/`（保留 slug）。

- Recommended: MCP tool
  `new_workspace(slug=..., title=..., description=...)`
  (drops a `.workspace.json` marker).
- Or manually `mkdir workspace/<slug>` — `list_workspaces()` will
  pick it up either way.
- Cross-slug shared assets go under `workspace/shared/`
  (reserved slug).

详见 `docs/agents/LETTER-TO-ADMIN.md` § "产物放哪：workspace/<slug>/ 约定".
See `docs/agents/LETTER-TO-ADMIN.md` § "Where artefacts go" for the
full convention.
"""


def _now_iso() -> str:
    """Return the current local time as an ISO-8601 string.

    Local time (not UTC) matches the operator's wall clock — FCoP
    files are authored interactively and a human reading
    ``created_at`` cares about "when did I create this on my laptop",
    not a UTC offset. Seconds-level precision is sufficient; we don't
    include microseconds because the value is informational only.
    """
    return _dt.datetime.now().replace(microsecond=0).isoformat()


# ── FCoP 3.0 lifecycle helpers ────────────────────────────────────────
#
# These are used only by v3-mode code paths in Project.write_task and
# Project.archive_task. They live at module scope (not on Project)
# because they have no dependency on Project state — pure functions
# from (bytes, sender) to (bytes) and from (Project, path) to (path).


def _stamp_v3_creation_event(payload: bytes, *, sender: str) -> bytes:
    """Append a creation transition event to a freshly-built v3 task file.

    Per FCoP 3.0 spec §2 + Rule E (every mv produces one event), a
    file landing in _lifecycle/inbox/ MUST carry a creation event.
    write_task constructs the file's full text first; this helper
    decodes it, appends ``{from: null, to: inbox, by: <sender>,
    tool: create_task}`` to the ``transitions:`` array via
    fcop.lifecycle.events.append_event_to_frontmatter, and re-encodes.

    The whole thing happens inside write_task's O_EXCL atomic
    reservation, so the file appears on disk in its already-witnessed
    state — no observable "v3 file without an event" window exists.
    """
    from fcop.lifecycle.events import (
        TransitionEvent,
        append_event_to_frontmatter,
    )
    from fcop.lifecycle.state import Stage

    text = payload.decode("utf-8")
    event = TransitionEvent(
        at=_dt.datetime.now(_dt.timezone.utc),
        from_stage=None,
        to_stage=Stage.INBOX,
        by=sender,
        tool="create_task",
    )
    return append_event_to_frontmatter(text, event).encode("utf-8")


def _v3_archive_chain(project: Project, source: pathlib.Path) -> pathlib.Path:
    """Walk ``source`` through legal lifecycle transitions to archive/.

    Returns the final archived path. The chain is computed from
    ``source``'s current stage (per Rule A: file path is truth) and
    walks through the protocol's allowed-transitions table — never
    skipping a stage, always appending an event for each hop.

    For the v2-era caller (CodeFlowMu) that treats ``archive_task``
    as the single "wrap this up" verb, this preserves the simple
    one-call ergonomics while emitting a fully-compliant v3 audit
    trace. The `by` field on each event is the calling agent — we
    use a synthesised "archiver" identity because the caller has
    not declared one (archive_task takes only filename_or_id, no
    actor argument). When a future API exposes an explicit actor,
    this helper should accept it as a parameter.

    Args:
        project: The Project whose ``_lifecycle/`` we walk.
        source: The current path of the task file.

    Returns:
        Absolute path to the file in ``_lifecycle/archive/``.

    Raises:
        IllegalTransitionError: source is not under any recognised
            lifecycle bucket (Rule A cannot identify a from-stage).
    """
    import datetime as _dt2

    from fcop.lifecycle.atomic import commit as _commit
    from fcop.lifecycle.events import TransitionEvent
    from fcop.lifecycle.state import Stage as _Stage
    from fcop.lifecycle.state import stage_of_path as _stage_of_path
    from fcop.lifecycle.transitions import (
        IllegalTransitionError as _IllegalTransitionError,
    )

    # Stage chain from each possible source to archive. Each tuple
    # encodes (from_stage, to_stage, canonical L1 tool).
    chains: dict[_Stage, tuple[tuple[_Stage, _Stage, str], ...]] = {
        _Stage.INBOX: (
            (_Stage.INBOX, _Stage.ACTIVE, "claim_task"),
            (_Stage.ACTIVE, _Stage.DONE, "finish_task"),
            (_Stage.DONE, _Stage.ARCHIVE, "archive_task"),
        ),
        _Stage.ACTIVE: (
            (_Stage.ACTIVE, _Stage.DONE, "finish_task"),
            (_Stage.DONE, _Stage.ARCHIVE, "archive_task"),
        ),
        _Stage.REVIEW: (
            (_Stage.REVIEW, _Stage.DONE, "approve_task"),
            (_Stage.DONE, _Stage.ARCHIVE, "archive_task"),
        ),
        _Stage.DONE: (
            (_Stage.DONE, _Stage.ARCHIVE, "archive_task"),
        ),
        _Stage.ARCHIVE: (),
    }

    current_path = source
    current_stage = _stage_of_path(current_path, project_root=project.workspace_dir)
    if current_stage is None:
        raise _IllegalTransitionError(
            None, _Stage.ARCHIVE, tool="archive_task",
        )

    chain = chains[current_stage]
    actor = "archiver"  # placeholder — see helper docstring

    for from_stage, to_stage, tool in chain:
        event = TransitionEvent(
            at=_dt2.datetime.now(_dt2.timezone.utc),
            from_stage=from_stage,
            to_stage=to_stage,
            by=actor,
            tool=tool,
        )
        result = _commit(
            current_path,
            to_stage,
            event,
            project_root=project.workspace_dir,
        )
        current_path = result.destination_path

    return current_path


_RESERVED_ROLES: frozenset[str] = frozenset({"ADMIN", "SYSTEM"})


def _parse_dir_files(
    directory: pathlib.Path,
    parser: Callable[..., object],
) -> list[tuple[pathlib.Path, object]]:
    """Return ``[(path, parsed_filename)]`` for every parseable file in ``directory``.

    Missing directories yield an empty list. Files whose names don't
    match the kind's grammar are silently skipped — those are stray
    documents (a README, a backup) that don't carry routing info.
    """
    if not directory.is_dir():
        return []
    results: list[tuple[pathlib.Path, object]] = []
    for entry in directory.iterdir():
        if not entry.is_file():
            continue
        parsed = parser(entry.name)
        if parsed is not None:
            results.append((entry, parsed))
    return results


def _roles_in_parsed(parsed: object) -> set[str]:
    """Return the set of role codes that a parsed filename involves.

    The shape depends on the filename kind: tasks have sender +
    recipient (slot is dropped — slot is a recipient *qualifier*, not
    a separate role), reports have reporter + recipient, issues have
    just the reporter.
    """
    roles: set[str] = set()
    sender = getattr(parsed, "sender", None)
    if sender:
        roles.add(sender)
    recipient = getattr(parsed, "recipient", None)
    if recipient:
        roles.add(recipient)
    reporter = getattr(parsed, "reporter", None)
    if reporter:
        roles.add(reporter)
    return roles


def _build_role_occupancy(
    role: str,
    active_tasks: list[tuple[pathlib.Path, object]],
    archived_tasks: list[tuple[pathlib.Path, object]],
    active_reports: list[tuple[pathlib.Path, object]],
    archived_reports: list[tuple[pathlib.Path, object]],
    active_issues: list[tuple[pathlib.Path, object]],
) -> RoleOccupancy:
    """Compute one role's occupancy from the pre-parsed ledger snapshots."""
    open_tasks = sum(
        1 for _p, parsed in active_tasks if role in _roles_in_parsed(parsed)
    )
    archived_tasks_count = sum(
        1 for _p, parsed in archived_tasks if role in _roles_in_parsed(parsed)
    )
    open_reports = sum(
        1 for _p, parsed in active_reports if role in _roles_in_parsed(parsed)
    )
    open_issues = sum(
        1 for _p, parsed in active_issues if role in _roles_in_parsed(parsed)
    )

    # Pick the most recently modified file involving this role across
    # all five buckets — its frontmatter session_id (if any) is what
    # the protocol's UNBOUND step 4 compares against.
    candidates: list[pathlib.Path] = []
    for parsed_list in (
        active_tasks,
        archived_tasks,
        active_reports,
        archived_reports,
        active_issues,
    ):
        for path, parsed in parsed_list:
            if role in _roles_in_parsed(parsed):
                candidates.append(path)

    last_seen_at: _dt.datetime | None = None
    last_session_id: str | None = None
    if candidates:
        latest = max(candidates, key=lambda p: p.stat().st_mtime)
        last_seen_at = _dt.datetime.fromtimestamp(latest.stat().st_mtime)
        last_session_id = _try_read_session_id(latest)

    if open_tasks or open_reports or open_issues:
        status: Literal["UNUSED", "ARCHIVED", "ACTIVE"] = "ACTIVE"
    elif archived_tasks_count or candidates:
        status = "ARCHIVED"
    else:
        status = "UNUSED"

    return RoleOccupancy(
        role=role,
        open_tasks=open_tasks,
        open_reports=open_reports,
        open_issues=open_issues,
        archived_tasks=archived_tasks_count,
        last_session_id=last_session_id,
        last_seen_at=last_seen_at,
        status=status,
    )


def _try_read_session_id(path: pathlib.Path) -> str | None:
    """Best-effort frontmatter read for the optional ``session_id`` field.

    Returns ``None`` on any error (file gone, malformed YAML, missing
    field). This is metadata-only — the caller is reading frontmatter
    to attribute occupancy, which the protocol explicitly permits even
    for UNBOUND sessions.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        raw = parse_frontmatter_raw(text)
    except Exception:
        return None
    value = raw.get("session_id")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


# 0.7.x layout prefixes — kept as fallback for projects that have not
# yet migrated to the v1.0 ``fcop/`` layout. The dynamic per-project
# prefix list is built in :func:`_ledger_prefixes_for` from
# ``Project.workspace_dir`` so it works for both ``fcop/`` and
# ``docs/agents/`` (and explicit overrides) without code duplication.
_LEDGER_RELATIVE_PREFIXES = (
    "docs/agents/tasks/",
    "docs/agents/reports/",
    "docs/agents/issues/",
    "docs/agents/log/",
)


def _ledger_prefixes_for(project: Project) -> tuple[str, ...]:
    """Return the per-project workspace prefixes the drift parser uses.

    Always derived from ``project.workspace_dir`` relative to
    ``project.path`` so that a v1.0 ``fcop/`` project, a 0.7.x
    ``docs/agents/`` project, and an explicit ``custom-ws/`` project
    all behave identically. We additionally union in the historical
    ``docs/agents/...`` prefixes so half-migrated repos (those still
    holding stray legacy files) keep getting ``in_ledger=True`` and
    are surfaced rather than hidden.
    """
    try:
        rel = project.workspace_dir.relative_to(project.path).as_posix().rstrip("/")
    except ValueError:
        # Workspace lives outside project root (rare; explicit override
        # case). The ledger probe needs project-root-relative prefixes,
        # so we fall back to the historical pair for that case.
        rel = ""
    if not rel:
        return _LEDGER_RELATIVE_PREFIXES
    own = tuple(f"{rel}/{sub}/" for sub in ("tasks", "reports", "issues", "log"))
    if rel == "docs/agents":
        return own
    return own + _LEDGER_RELATIVE_PREFIXES


def _parse_git_porcelain(
    raw: bytes,
    project_root: pathlib.Path,
    ledger_prefixes: tuple[str, ...] = _LEDGER_RELATIVE_PREFIXES,
) -> Iterator[DriftEntry]:
    """Parse the NUL-separated output of ``git status --porcelain -z``.

    The ``-z`` form is necessary because plain ``--porcelain`` is
    ambiguous on filenames containing spaces / quotes / newlines —
    edge cases which absolutely show up in real codebases. Each entry
    in ``-z`` output is ``XY <space> path <NUL>``, with renames using
    a follow-up ``<NUL> oldpath`` segment which we drop because we
    only care about the destination.
    """
    text = raw.decode("utf-8", errors="replace")
    chunks = text.split("\x00")

    skip_next = False
    for chunk in chunks:
        if not chunk:
            continue
        if skip_next:
            # This chunk is the rename source path; we already
            # captured the destination on the previous iteration.
            skip_next = False
            continue
        if len(chunk) < 4:
            continue
        status = chunk[:2]
        # Format is ``XY path``; the separator is a single space at
        # index 2.
        path_str = chunk[3:]
        # Rename markers (``R `` / ``RM`` / ``RD`` / ``C `` etc.) are
        # followed by a ``-z`` segment carrying the source path; skip
        # it on the next iteration.
        if status[0] in ("R", "C"):
            skip_next = True
        normalized = path_str.replace("\\", "/")
        in_ledger = any(
            normalized.startswith(prefix)
            for prefix in ledger_prefixes
        )
        yield DriftEntry(path=normalized, status=status, in_ledger=in_ledger)


def _scan_session_role_conflicts(
    project: Project,
) -> tuple[SessionRoleConflict, ...]:
    """Scan every TASK / REPORT / ISSUE for ``session_id ↔ role`` conflicts.

    A "conflict" here means: a single ``session_id`` signed files
    under more than one role code. Per Rule 1 (since 1.8.0) one
    session = one role binding for life, so this is direct evidence
    of sub-agent role impersonation.

    Reads frontmatter only — this is the same contract
    :meth:`Project.role_occupancy` honours: never read task bodies.
    """
    from collections import defaultdict

    if not project.is_initialized():
        return ()

    # session_id → role → set of paths
    sessions: dict[str, dict[str, set[pathlib.Path]]] = defaultdict(
        lambda: defaultdict(set)
    )

    bundles: list[tuple[pathlib.Path, object]] = []
    bundles += _parse_dir_files(project.tasks_dir, parse_task_filename)
    bundles += _parse_dir_files(
        project.log_dir / "tasks", parse_task_filename
    )
    bundles += _parse_dir_files(project.reports_dir, parse_report_filename)
    bundles += _parse_dir_files(
        project.log_dir / "reports", parse_report_filename
    )
    bundles += _parse_dir_files(project.issues_dir, parse_issue_filename)
    bundles += _parse_dir_files(
        project.log_dir / "issues", parse_issue_filename
    )

    for path, parsed in bundles:
        session_id = _try_read_session_id(path)
        if not session_id:
            continue
        # The "role" we attribute to this file depends on the kind:
        # tasks → sender, reports → reporter, issues → reporter.
        role = (
            getattr(parsed, "sender", None)
            or getattr(parsed, "reporter", None)
        )
        if not role:
            continue
        sessions[session_id][role].add(path)

    conflicts: list[SessionRoleConflict] = []
    for session_id in sorted(sessions.keys()):
        roles_map = sessions[session_id]
        if len(roles_map) <= 1:
            continue
        all_files: set[pathlib.Path] = set()
        for paths in roles_map.values():
            all_files |= paths
        conflicts.append(
            SessionRoleConflict(
                session_id=session_id,
                roles=tuple(sorted(roles_map.keys())),
                files=tuple(sorted(all_files, key=lambda p: str(p))),
            )
        )

    return tuple(conflicts)


def _existing_filenames_for_seq(*dirs: pathlib.Path) -> Iterator[str]:
    """Yield basenames of files across *every* given directory.

    Used by :meth:`Project.write_task` / :meth:`write_report` /
    :meth:`write_issue` to compute the next sequence number.

    The ledger of "what basenames are already in use" lives in *both*
    the active directory (e.g. ``docs/agents/tasks/``) **and** the
    archive directory (e.g. ``docs/agents/log/tasks/``). Considering
    only the active directory would let :func:`next_sequence` reuse a
    basename that already exists in the archive — which is exactly the
    bug ISSUE-20260427-003 documents: after ``archive_task`` moves
    ``TASK-{date}-001-...`` to ``log/``, a subsequent ``write_task`` on
    the same date would receive sequence ``001`` again and produce a
    file that collides with its archived ancestor in any history grep.

    Missing directories are tolerated silently; non-file entries are
    skipped. Order between directories is unspecified — this is fine
    because :func:`next_sequence` deduplicates via a ``set``.
    """
    for directory in dirs:
        if not directory.is_dir():
            continue
        for entry in directory.iterdir():
            if entry.is_file():
                yield entry.name


def _try_load_task(
    path: pathlib.Path, *, is_archived: bool
) -> Task | None:
    """Best-effort load of one task file; return ``None`` on any problem.

    Used by :meth:`Project.list_tasks` where a single corrupt file must
    not break the enumeration. Strict loading lives in
    :func:`_load_task_strict`.
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_task_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        fm, body = parse_task_frontmatter(text)
    except Exception:
        # Covers ValidationError, ProtocolViolation, and any unexpected
        # parser bug — list_tasks is advertised as lenient.
        return None
    try:
        mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None
    return Task(
        path=path,
        filename=path.name,
        task_id=parsed.task_id,
        date=parsed.date,
        sequence=parsed.sequence,
        frontmatter=fm,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _load_task_strict(
    path: pathlib.Path, *, is_archived: bool
) -> Task:
    """Strict load for :meth:`Project.read_task` — propagates errors.

    Callers who want a boolean-ish result should use
    :func:`_try_load_task` instead.
    """
    text = path.read_text(encoding="utf-8")
    fm, body = parse_task_frontmatter(text)
    parsed = parse_task_filename(path.name)
    assert parsed is not None, (
        f"_resolve_task_file returned {path.name!r} but it does not match "
        "TASK_FILENAME_RE — this is a bug in the resolver."
    )
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Task(
        path=path,
        filename=path.name,
        task_id=parsed.task_id,
        date=parsed.date,
        sequence=parsed.sequence,
        frontmatter=fm,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _extract_report_status(
    fm: TaskFrontmatter,
) -> Literal["done", "blocked", "in_progress"]:
    """Pull and validate the ``status`` field from a report's frontmatter.

    Reports store their status as a top-level YAML key that ends up in
    :attr:`TaskFrontmatter.extra` (since 0.6 reuses ``TaskFrontmatter``
    for both tasks and reports). A missing status is treated as
    ``"done"`` so older reports that predate the field still load.

    Raises:
        ProtocolViolation: the field exists but its value is not one
            of ``done`` / ``blocked`` / ``in_progress``. We intentionally
            accept a missing field but reject a malformed one — the
            former is a version-skew story, the latter is a bug.
    """
    raw = fm.extra.get("status", "done")
    if not isinstance(raw, str) or raw not in _VALID_REPORT_STATUSES:
        raise ProtocolViolation(
            f"report status must be one of {sorted(_VALID_REPORT_STATUSES)}; "
            f"got {raw!r}",
            rule="report.status",
        )
    return raw  # type: ignore[return-value]


def _try_load_report(
    path: pathlib.Path, *, is_archived: bool
) -> Report | None:
    """Best-effort report load; return ``None`` on any problem.

    Mirrors :func:`_try_load_task` — used by
    :meth:`Project.list_reports` where one bad file must not break
    the enumeration.
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_report_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        fm, body = parse_task_frontmatter(text)
    except Exception:
        return None
    # A report without a `references:` entry is protocol-ambiguous:
    # we don't know which task it replies to. Skip rather than guess.
    if not fm.references:
        return None
    try:
        status = _extract_report_status(fm)
    except ProtocolViolation:
        return None
    try:
        mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None
    return Report(
        path=path,
        filename=path.name,
        task_id=fm.references[0],
        reporter=fm.sender,
        recipient=fm.recipient,
        status=status,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _load_report_strict(
    path: pathlib.Path, *, is_archived: bool
) -> Report:
    """Strict report load for :meth:`Project.read_report`.

    Unlike :func:`_try_load_report`, missing/invalid pieces raise.
    Used where the caller asked for a specific file and silent
    skipping would hide the problem.
    """
    text = path.read_text(encoding="utf-8")
    fm, body = parse_task_frontmatter(text)
    parsed = parse_report_filename(path.name)
    assert parsed is not None, (
        f"_resolve_report_file returned {path.name!r} but it does not match "
        "REPORT_FILENAME_RE — this is a bug in the resolver."
    )
    if not fm.references:
        raise ProtocolViolation(
            f"report {path.name} has no `references:` — cannot identify "
            "the task it responds to",
            rule="report.references",
        )
    status = _extract_report_status(fm)
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Report(
        path=path,
        filename=path.name,
        task_id=fm.references[0],
        reporter=fm.sender,
        recipient=fm.recipient,
        status=status,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _assemble_issue_file(
    frontmatter_data: dict[str, object], body: str
) -> str:
    """Serialize an issue frontmatter + body into a complete file text.

    Issues don't use :class:`TaskFrontmatter` — they have no recipient
    and carry ``summary`` / ``severity`` instead of ``priority``. We
    write the YAML directly rather than shoe-horning issue fields into
    the task dataclass. Field order is deterministic (identity fields
    first, then reporter, severity, summary) so round-tripping produces
    minimal diffs.
    """
    ordered: dict[str, object] = {}
    # Keep a canonical order — mirrors serialize_task_frontmatter's
    # "protocol/version first" discipline. ``status`` / ``created_at``
    # are pinned next to the core identity fields so round-trips
    # produce clean diffs; see ADR-0004 §"Issue 是例外".
    for key in (
        "protocol",
        "version",
        "reporter",
        "severity",
        "status",
        "summary",
        "created_at",
        "closed_at",
        "closed_by",
        "resolution",
    ):
        if key in frontmatter_data:
            ordered[key] = frontmatter_data[key]
    for key in sorted(frontmatter_data):
        if key not in ordered:
            ordered[key] = frontmatter_data[key]

    yaml_text = yaml.safe_dump(
        ordered,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    fm_text = (
        f"{FRONTMATTER_DELIMITER}\n{yaml_text}{FRONTMATTER_DELIMITER}\n"
    )
    if not body:
        return fm_text
    return f"{fm_text}\n{body.lstrip(chr(10))}"


def _parse_issue_frontmatter(
    text: str,
) -> tuple[str, Severity, str, str]:
    """Parse issue frontmatter, returning ``(reporter, severity, summary, body)``.

    Unlike :func:`parse_task_frontmatter`, this accepts a much smaller
    schema: no sender / recipient / priority, but ``reporter``,
    ``severity``, and ``summary`` are mandatory. Historical
    ``protocol`` / ``version`` are still validated.

    Raises:
        ProtocolViolation: required field missing or wrong protocol.
        ValidationError: malformed YAML or bad role code / severity.
    """
    raw = parse_frontmatter_raw(text)
    _, body = split_frontmatter(text)

    for required in ("protocol", "version", "reporter", "severity", "summary"):
        if required not in raw or raw[required] in (None, ""):
            raise ProtocolViolation(
                f"missing required issue frontmatter field: {required}",
                rule="issue.frontmatter.required",
            )

    reporter = str(raw["reporter"]).strip()
    role_issues = validate_role_code(
        reporter, field="reporter", allow_reserved=True
    )
    role_errors = [i for i in role_issues if i.severity == "error"]
    if role_errors:
        raise ValidationError(
            f"invalid reporter role code {reporter!r}",
            issues=role_errors,
        )

    severity_enum = normalize_severity(str(raw["severity"]))
    summary = str(raw["summary"]).strip()
    if not summary:
        raise ProtocolViolation(
            "issue summary must be non-empty",
            rule="issue.frontmatter.required",
        )

    return reporter, severity_enum, summary, body


def _try_load_issue(path: pathlib.Path) -> Issue | None:
    """Best-effort issue load; ``None`` on any problem.

    Companion to :func:`_try_load_task` / :func:`_try_load_report` for
    the :meth:`Project.list_issues` enumeration.
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_issue_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        reporter, severity_enum, summary, body = _parse_issue_frontmatter(text)
    except Exception:
        return None
    try:
        mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None
    return Issue(
        path=path,
        filename=path.name,
        issue_id=parsed.issue_id,
        summary=summary,
        severity=severity_enum,
        reporter=reporter,
        body=body,
        mtime=mtime,
    )


def _load_issue_strict(path: pathlib.Path) -> Issue:
    """Strict issue load for :meth:`Project.read_issue`."""
    text = path.read_text(encoding="utf-8")
    reporter, severity_enum, summary, body = _parse_issue_frontmatter(text)
    parsed = parse_issue_filename(path.name)
    assert parsed is not None, (
        f"_resolve_issue_file returned {path.name!r} but it does not match "
        "ISSUE_FILENAME_RE — this is a bug in the resolver."
    )
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Issue(
        path=path,
        filename=path.name,
        issue_id=parsed.issue_id,
        summary=summary,
        severity=severity_enum,
        reporter=reporter,
        body=body,
        mtime=mtime,
    )


def _derive_review_subject_short(subject_ref: str) -> str:
    """Derive a filename-safe ``subject_short`` slug from ``subject_ref``。

    规则：
    1. 若 ``subject_ref`` 看起来是路径，取 basename 去 ``.md`` 后缀
    2. 全部小写
    3. 非 [a-z0-9-] 字符替换为 ``-``
    4. 折叠连续 ``-``，去首尾 ``-``
    5. 截断到 64 字符（slug 太长会让文件名超过常见 Windows MAX_PATH 边界）

    例：
    - ``fcop/tasks/TASK-20260601-001-PM-to-DEV.md`` → ``task-20260601-001-pm-to-dev``
    - ``adr/ADR-0017-review-file-type-minimal.md`` → ``adr-0017-review-file-type-minimal``
    - ``commit:3c35e0e``                            → ``commit-3c35e0e``

    若 derive 结果不合 :data:`fcop.core.filename.REVIEW_SUBJECT_SHORT_RE`，
    caller 应该显式传 ``subject_short=`` 覆盖。
    """
    import re as _re

    raw = str(subject_ref).strip()
    if "/" in raw or "\\" in raw:
        raw = pathlib.PurePath(raw).name
    if raw.lower().endswith(".md"):
        raw = raw[: -len(".md")]
    raw = raw.lower()
    raw = _re.sub(r"[^a-z0-9-]+", "-", raw)
    raw = _re.sub(r"-+", "-", raw).strip("-")
    if len(raw) > 64:
        raw = raw[:64].rstrip("-")
    return raw


def _try_load_review(
    path: pathlib.Path, *, is_archived: bool
) -> Review | None:
    """Best-effort review load; return ``None`` on any problem.

    Mirrors :func:`_try_load_report` —— 用于 :meth:`Project.list_reviews`
    的扫描场景，单个畸形文件不应中断列表。
    """
    if not path.is_file():
        return None
    if path.suffix.lower() not in _FCOP_SUFFIXES:
        return None
    parsed = parse_review_filename(path.name)
    if parsed is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        fm, body = parse_review_frontmatter(text)
    except Exception:
        return None
    try:
        return _hydrate_review(path, fm, body, parsed, is_archived=is_archived)
    except Exception:
        return None


def _load_review_strict(
    path: pathlib.Path, *, is_archived: bool
) -> Review:
    """Strict REVIEW load for :meth:`Project.read_review` / archive_review."""
    text = path.read_text(encoding="utf-8")
    fm, body = parse_review_frontmatter(text)
    parsed = parse_review_filename(path.name)
    assert parsed is not None, (
        f"_resolve_review_file returned {path.name!r} but it does not match "
        "REVIEW_FILENAME_RE — this is a bug in the resolver."
    )
    return _hydrate_review(path, fm, body, parsed, is_archived=is_archived)


def _hydrate_review(
    path: pathlib.Path,
    fm: dict[str, object],
    body: str,
    parsed: ReviewFilename,
    *,
    is_archived: bool,
) -> Review:
    """Build a Review dataclass from parsed frontmatter + filename + body."""
    # Required fields —— 缺任何一个都拒；schema validator 会给同样判决，
    # 这里手动检 1 次以给出清晰错误（schema 错误聚合在 oneOf 下不直观）。
    for required in ("subject_type", "subject_ref", "reviewer_role", "decision", "decided_at"):
        if required not in fm:
            raise ProtocolViolation(
                f"REVIEW {path.name} missing required frontmatter field: {required}",
                rule="frontmatter.required",
            )

    decision = Project._coerce_review_decision(str(fm["decision"]))
    subject_type = Project._coerce_review_subject_type(str(fm["subject_type"]))
    subject_ref = str(fm["subject_ref"]).strip()
    reviewer_role = str(fm["reviewer_role"]).strip()
    rationale_raw = fm.get("rationale")
    rationale = str(rationale_raw).strip() if rationale_raw else None
    reviewer_agent_raw = fm.get("reviewer_agent")
    reviewer_agent = (
        str(reviewer_agent_raw).strip() if reviewer_agent_raw else None
    )
    raw_required = fm.get("required_changes") or ()
    required_changes: tuple[str, ...]
    if isinstance(raw_required, str):
        required_changes = (raw_required.strip(),) if raw_required.strip() else ()
    elif isinstance(raw_required, (list, tuple)):
        required_changes = tuple(
            str(s).strip() for s in raw_required if s and str(s).strip()
        )
    else:
        required_changes = ()

    # decided_at 接受 datetime / date / str（YAML 自动 parse 时机不定）
    decided_raw = fm["decided_at"]
    if isinstance(decided_raw, _dt.datetime):
        decided_at = decided_raw
    elif isinstance(decided_raw, _dt.date):
        decided_at = _dt.datetime.combine(decided_raw, _dt.time())
    else:
        decided_at = _dt.datetime.fromisoformat(str(decided_raw))

    review_id = str(fm.get("review_id") or path.name[: -len(".md")]).strip()
    mtime = _dt.datetime.fromtimestamp(path.stat().st_mtime)
    return Review(
        path=path,
        filename=path.name,
        review_id=review_id,
        date=parsed.date,
        sequence=parsed.sequence,
        subject_type=subject_type,
        subject_ref=subject_ref,
        reviewer_role=reviewer_role,
        reviewer_agent=reviewer_agent,
        decision=decision,
        rationale=rationale,
        required_changes=required_changes,
        decided_at=decided_at,
        body=body,
        is_archived=is_archived,
        mtime=mtime,
    )


def _count_matching(directory: pathlib.Path, pattern) -> int:  # type: ignore[no-untyped-def]
    """Count files in *directory* whose name matches *pattern*.

    Missing directories are treated as empty — ``status()`` must be
    safe to call on uninitialized projects. We do a shallow scan only;
    archives live under a separate ``log/`` path, not nested.
    """
    if not directory.is_dir():
        return 0
    total = 0
    for entry in directory.iterdir():
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in _FCOP_SUFFIXES:
            continue
        if pattern.match(entry.name):
            total += 1
    return total


def _collect_recent_activity(
    *,
    tasks_dir: pathlib.Path,
    reports_dir: pathlib.Path,
    issues_dir: pathlib.Path,
    limit: int,
) -> tuple[RecentActivityEntry, ...]:
    """Return the newest *limit* entries across tasks/reports/issues.

    Entries are ordered by filesystem mtime, descending. "Newest" is a
    UX hint, not a correctness claim — an external tool that rewrites
    files can perturb the order harmlessly.
    """
    candidates: list[RecentActivityEntry] = []
    for kind, directory, pattern in (
        ("task", tasks_dir, TASK_FILENAME_RE),
        ("report", reports_dir, REPORT_FILENAME_RE),
        ("issue", issues_dir, ISSUE_FILENAME_RE),
    ):
        if not directory.is_dir():
            continue
        for entry in directory.iterdir():
            if not entry.is_file():
                continue
            if entry.suffix.lower() not in _FCOP_SUFFIXES:
                continue
            if not pattern.match(entry.name):
                continue
            try:
                mtime = _dt.datetime.fromtimestamp(entry.stat().st_mtime)
            except OSError:
                continue
            candidates.append(
                RecentActivityEntry(
                    kind=kind,  # type: ignore[arg-type]
                    filename=entry.name,
                    mtime=mtime,
                    summary="",
                )
            )

    candidates.sort(key=lambda e: e.mtime, reverse=True)
    return tuple(candidates[:limit])


# ── Suggestion helpers ────────────────────────────────────────────────


def _write_atomic_unique(
    directory: pathlib.Path,
    *,
    stem: str,
    suffix: str,
    data: bytes,
) -> pathlib.Path:
    """Write *data* to ``directory/stem<suffix>`` atomically & uniquely.

    Tries ``stem+suffix`` first; if that file already exists, falls
    back to ``stem-2+suffix``, ``stem-3+suffix``, etc., until it
    finds an unused name. Uses ``os.open`` with
    ``O_CREAT | O_EXCL | O_WRONLY`` so the existence check and the
    create are atomic — no TOCTOU window between them.

    Shared with :meth:`Project.drop_suggestion` today; extracted to
    module level so the next "append a unique timestamped file"
    feature can reuse it without further refactoring.
    """
    for attempt in range(_MAX_WRITE_RETRIES):
        candidate_name = stem + suffix if attempt == 0 else f"{stem}-{attempt + 1}{suffix}"
        candidate = directory / candidate_name
        try:
            fd = os.open(
                candidate,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o644,
            )
        except FileExistsError:
            continue
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
        except BaseException:
            # On any write failure, clean up the empty file we just
            # created so a partial / zero-byte drop doesn't linger.
            with contextlib.suppress(OSError):
                candidate.unlink()
            raise
        return candidate

    # Exhausted retries — something is seriously wrong (clock frozen,
    # filesystem read-only midway through, etc.). Raise rather than
    # silently overwriting.
    raise OSError(
        f"failed to allocate a unique filename under {directory} "
        f"after {_MAX_WRITE_RETRIES} attempts"
    )


# ── Template deployment helpers ───────────────────────────────────────

# Language codes that get bundled into every deployment. Kept in sync
# with fcop.teams._SUPPORTED_LANGS — duplicated here rather than
# imported because the former is a private constant and we don't want
# an API leak.
_DEPLOY_LANGS: tuple[Literal["zh", "en"], ...] = ("zh", "en")


def _ensure_lang_supported(lang: str) -> None:
    """Raise ValueError if *lang* is not a bundled language code.

    Kept separate from the deploy routine so the check is
    unit-testable in isolation and uses the same error message that
    :func:`fcop.teams.get_template` emits — a different message here
    would be confusing to users who hit one or the other first.
    """
    if lang not in _DEPLOY_LANGS:
        raise ValueError(
            f"unsupported lang {lang!r}; "
            f"expected one of {list(_DEPLOY_LANGS)}"
        )


def _plan_template_deployment(
    bundles: dict[str, TeamTemplate],
) -> list[tuple[str, str]]:
    """Compute ``[(relative_path, content), ...]`` for a deploy run.

    The layout rules (matching 0.5.x plugin behavior so migrating
    projects get the same shape):

    * team-level ``README`` is renamed to ``TEAM-README`` when written
      under ``shared/`` so it does not collide with the prefix-guide
      ``shared/README.md`` that lives in every project.
    * ``TEAM-ROLES`` and ``TEAM-OPERATING-RULES`` keep their names.
    * Per-role bios go into ``roles/{CODE}.md``.
    * The ``zh`` variant has no language suffix; the ``en`` variant
      uses ``.en.md`` — same convention as the bundled source files.

    Returned as a list (not a dict) so the caller can iterate in a
    stable order and emit deterministic :class:`DeploymentReport`
    contents.
    """
    # Use the zh bundle as the source of truth for "which roles
    # exist"; any en-only role would indicate bundled-data drift
    # which get_template() would already have surfaced.
    zh = bundles["zh"]

    def suffix(lang: str) -> str:
        # Mirror the bundled source file convention. Expressed as a
        # closure so the rules above stay close to the data.
        return ".md" if lang == "zh" else ".en.md"

    plan: list[tuple[str, str]] = []
    for lang in _DEPLOY_LANGS:
        bundle = bundles[lang]
        plan.append((f"TEAM-README{suffix(lang)}", bundle.readme))
        plan.append((f"TEAM-ROLES{suffix(lang)}", bundle.team_roles))
        plan.append(
            (f"TEAM-OPERATING-RULES{suffix(lang)}", bundle.operating_rules)
        )
        for role in zh.roles:
            plan.append((f"roles/{role}{suffix(lang)}", bundle.roles[role]))
    return plan


# ── Protocol-rule deployment helpers (ADR-0006) ──────────────────────


def _strip_yaml_frontmatter(text: str) -> str:
    """Remove a leading ``---\\n…\\n---\\n`` YAML frontmatter block.

    Used when materializing host-neutral copies (``AGENTS.md`` /
    ``CLAUDE.md``): the Cursor-specific frontmatter
    (``alwaysApply: true`` etc.) would render as visible noise in
    Codex / Claude Code which don't parse it. The frontmatter
    *content* is still recoverable by reading
    :func:`fcop.rules.get_rules_version` /
    :func:`fcop.rules.get_protocol_version` from the package.

    No-op when the text doesn't start with a frontmatter block, so
    it's safe to apply unconditionally.
    """
    delim = "---\n"
    if not text.startswith(delim):
        return text
    closing = text.find("\n" + delim, len(delim))
    if closing == -1:
        return text
    return text[closing + len("\n" + delim):]


_HOST_NEUTRAL_PREAMBLE = """\
# FCoP Protocol Rules · agent-host-neutral copy

> This file is deployed by `fcop` for agent hosts that read
> `AGENTS.md` / `CLAUDE.md` as their system-prompt source
> (Codex, Claude Code, Devin, Cursor, etc.). Cursor IDE users get
> the same content via `.cursor/rules/fcop-rules.mdc` and
> `.cursor/rules/fcop-protocol.mdc`.
>
> The source of truth is the `fcop` Python package. To upgrade
> this file after `pip install -U fcop[-mcp]`, ADMIN runs the MCP
> tool `redeploy_rules()` (or calls
> `Project.deploy_protocol_rules(force=True)` directly).

"""


def _plan_protocol_rules_deployment() -> list[tuple[str, str]]:
    """Compute ``[(relative_path, content), ...]`` for a host-neutral deploy.

    Four targets, two payload variants:

    * ``.cursor/rules/fcop-rules.mdc`` and
      ``.cursor/rules/fcop-protocol.mdc`` get the bundled ``.mdc``
      content **byte-for-byte** (frontmatter intact — Cursor needs
      ``alwaysApply: true``).
    * ``AGENTS.md`` and ``CLAUDE.md`` get a single concatenated
      file: a small explanatory preamble + rules body
      (frontmatter-stripped) + protocol-commentary body
      (frontmatter-stripped). Content is byte-identical between the
      two — duplicated because Codex reads ``AGENTS.md`` and Claude
      Code reads ``CLAUDE.md`` and neither falls back to the other.

    Cached at the module level via :func:`_load_text` (inherited
    through ``fcop.rules.get_rules`` etc.), so repeated deploys
    don't re-read the wheel.
    """
    rules_mdc = get_rules()
    protocol_mdc = get_protocol_commentary()

    rules_body = _strip_yaml_frontmatter(rules_mdc)
    protocol_body = _strip_yaml_frontmatter(protocol_mdc)

    version_block = (
        f"> Rules version: `{get_rules_version()}` · "
        f"Protocol commentary version: `{get_protocol_version()}`\n\n"
    )
    combined = (
        _HOST_NEUTRAL_PREAMBLE
        + version_block
        + "---\n\n"
        + rules_body.lstrip("\n")
        + "\n\n---\n\n"
        + protocol_body.lstrip("\n")
    )

    return [
        (".cursor/rules/fcop-rules.mdc", rules_mdc),
        (".cursor/rules/fcop-protocol.mdc", protocol_mdc),
        ("AGENTS.md", combined),
        ("CLAUDE.md", combined),
    ]


# ── Inspection helpers ─────────────────────────────────────────────────────


def _extract_frontmatter_kind(text: str) -> str | None:
    """Parse the ``kind:`` field from YAML frontmatter, return None if absent."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm_block = text[3:end]
    for line in fm_block.splitlines():
        if line.startswith("kind:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


_AUDIT_EXEMPT_DIR_NAMES: frozenset[str] = frozenset({
    "log",
    "_archive",
    "legacy-non-protocol",
    ".git",
    ".tmp",
})
"""Directory names that, anywhere under ``fcop/``, exempt their contents
from envelope/ghost-prefix scans.

Rationale (ISSUE-20260513-008, fcop 2.0.0): files under these directories
are archived / VCS metadata / pre-FCoP imports; their physical location
shouldn't be judged by their historical ``kind:`` frontmatter.
"""


def _is_audit_exempt_path(p: pathlib.Path, fcop_root: pathlib.Path) -> bool:
    """Return True if *p* lies under any audit-exempt directory inside ``fcop/``.

    Walks the relative path components from ``fcop/`` downward. A single match
    of any name in :data:`_AUDIT_EXEMPT_DIR_NAMES` exempts the file (e.g.
    ``fcop/log/tasks/TASK-old.md`` and ``fcop/dev-team/_archive/REPORT-1.md``
    both match).
    """
    try:
        rel = p.relative_to(fcop_root)
    except ValueError:
        return False
    return any(part in _AUDIT_EXEMPT_DIR_NAMES for part in rel.parts)


def _read_local_rules_version(project_root: pathlib.Path) -> str | None:
    """Read the rules version from the deployed ``.cursor/rules/fcop-rules.mdc``.

    Resolution order (per ISSUE-20260513-009 / fcop 2.0.0):

    1. **Primary** — YAML frontmatter field ``fcop_rules_version:`` at the
       top of the file. This is the canonical machine-readable channel
       deployed by ``deploy_protocol_rules()`` since fcop 2.0.0.
    2. **Fallback** — legacy in-body sentinel ``> Rules version: `X.Y.Z```
       used in pre-2.0.0 deployments. Retained for backward compatibility
       with projects that have not yet redeployed rules.

    Returns ``None`` only when both channels are missing (rare; would mean
    a hand-edited or truncated rules file).
    """
    import re

    rules_path = project_root / ".cursor" / "rules" / "fcop-rules.mdc"
    if not rules_path.exists():
        return None
    text = rules_path.read_text(encoding="utf-8", errors="ignore")

    # Primary: frontmatter field (canonical since fcop 2.0.0).
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_block = text[3:end]
            for raw in fm_block.splitlines():
                line = raw.strip()
                if line.startswith("fcop_rules_version:"):
                    value = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if value:
                        return value

    # Fallback: legacy in-body sentinel.
    for line in text.splitlines():
        if "Rules version:" in line:
            m = re.search(r"`([^`]+)`", line)
            if m:
                return m.group(1)
    return None


def _renumber_violations(violations: list[Violation]) -> list[Violation]:
    """Assign sequential violation_ids like P0-001, P1-001, P2-001, P3-001."""
    from fcop.inspection import Violation

    counters: dict[str, int] = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    renumbered: list[Violation] = []
    for v in violations:
        counters[v.severity] += 1
        new_id = f"{v.severity}-{counters[v.severity]:03d}"
        # Update remediation violation references if needed (violation_id unchanged in steps)
        renumbered.append(Violation(
            violation_id=new_id,
            severity=v.severity,
            rule_violated=v.rule_violated,
            summary=v.summary,
            evidence=v.evidence,
            impact=v.impact,
            remediation=v.remediation,
            scan_source=v.scan_source,
        ))
    return renumbered
