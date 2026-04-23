"""Stateless accessors for bundled team templates.

This module exposes read-only metadata and template content for the
preset teams packaged with fcop (``dev-team``, ``media-team``,
``mvp-team``, ``qa-team``). Both metadata and template text are loaded
from ``fcop/teams/_data/`` inside the wheel via
:mod:`importlib.resources`, so the library works from a wheel, an
sdist, or an editable checkout without caring about cwd.

Public contract (stable within 0.6.x):
    * :func:`get_available_teams` — list every bundled preset.
    * :func:`get_team_info` — fetch one preset's metadata by slug.
    * :func:`get_template` — fetch the three-layer doc bundle (team
      README + TEAM-ROLES + TEAM-OPERATING-RULES + per-role bios).

Source of truth for the team list is ``_data/teams/index.json``; the
Python representation is derived at import time. Bumping the bundled
index is therefore a two-step change: edit the JSON, let the import
machinery re-derive. No duplicated hard-coded role lists.

See adr/ADR-0001-library-api.md ("无状态模块：`fcop.teams`") for the
rationale behind keeping this module stateless.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache
from importlib import resources
from importlib.abc import Traversable
from typing import Literal

from fcop.errors import FcopError, TeamNotFoundError

__all__ = [
    "TeamInfo",
    "TeamTemplate",
    "get_available_teams",
    "get_team_info",
    "get_template",
]

# Language codes supported by bundled teams. Each file exists in two
# variants: ``{name}.md`` (zh) and ``{name}.en.md`` (en). Adding a new
# language is a data-only change — drop the translated files in next
# to the existing ones and add the code here.
_SUPPORTED_LANGS: frozenset[str] = frozenset({"zh", "en"})

# Files that make up one team's template bundle. Order matters only
# for deterministic TeamTemplate iteration; on disk they live flat
# under teams/<slug>/.
_TEAM_FILES: tuple[str, ...] = (
    "README",
    "TEAM-ROLES",
    "TEAM-OPERATING-RULES",
)


# ── Public types ─────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TeamInfo:
    """Metadata for one bundled team.

    Derived from ``index.json`` at import time; stable within 0.6.x
    per the semver promise. ``roles`` is a tuple so it can be used as
    a dict key / set member without copying.
    """

    name: str
    display_name: str
    leader: str
    roles: tuple[str, ...]
    description_zh: str
    description_en: str


@dataclass(frozen=True, slots=True)
class TeamTemplate:
    """The three-layer documentation bundle for one team, one language.

    Layer 1: team introduction (``readme``).
    Layer 2: roster + operating rules (``team_roles`` /
             ``operating_rules``).
    Layer 3: per-role bios, keyed by role code (``roles``).

    All fields hold plain strings — ready to write to disk or feed
    into an LLM context without any framework glue.
    """

    name: str
    lang: str
    readme: str
    team_roles: str
    operating_rules: str
    roles: dict[str, str]


# ── Public API ───────────────────────────────────────────────────────


def get_available_teams() -> list[TeamInfo]:
    """Return metadata for every bundled preset team.

    Order is deterministic: sorted by team slug so UIs that render
    these as a picker get a stable presentation.
    """
    bundled = _load_bundled_teams()
    return [bundled[name] for name in sorted(bundled)]


def get_team_info(team: str) -> TeamInfo:
    """Return metadata for one bundled team.

    Raises:
        TeamNotFoundError: ``team`` is not bundled. The error's
            ``.team`` attribute carries the requested slug so callers
            can echo it back without reparsing.
    """
    bundled = _load_bundled_teams()
    try:
        return bundled[team]
    except KeyError as exc:
        available = ", ".join(sorted(bundled))
        raise TeamNotFoundError(
            f"team {team!r} is not bundled; available: {available}",
            team=team,
        ) from exc


def get_template(
    team: str, lang: Literal["zh", "en"] = "zh"
) -> TeamTemplate:
    """Fetch the three-layer documentation bundle for a preset team.

    Args:
        team: Team slug (e.g. ``"dev-team"``). Must be one of the
            presets listed by :func:`get_available_teams`.
        lang: Language of the returned templates. Only ``"zh"`` and
            ``"en"`` are bundled; more can be added by dropping
            translated files next to the existing ones.

    Returns:
        A :class:`TeamTemplate` with every file loaded into memory.
        Each bundled team carries at most a few dozen KB of text, so
        eager loading keeps the API simple without noticeable cost.

    Raises:
        TeamNotFoundError: ``team`` is not bundled.
        ValueError: ``lang`` is not supported.
    """
    if lang not in _SUPPORTED_LANGS:
        raise ValueError(
            f"unsupported lang {lang!r}; "
            f"expected one of {sorted(_SUPPORTED_LANGS)}"
        )

    info = get_team_info(team)
    team_dir = _data_dir().joinpath(team)

    readme = _read_lang_file(team_dir, "README", lang)
    team_roles = _read_lang_file(team_dir, "TEAM-ROLES", lang)
    operating_rules = _read_lang_file(
        team_dir, "TEAM-OPERATING-RULES", lang
    )

    roles_dir = team_dir.joinpath("roles")
    roles: dict[str, str] = {}
    for role in info.roles:
        roles[role] = _read_lang_file(roles_dir, role, lang)

    return TeamTemplate(
        name=team,
        lang=lang,
        readme=readme,
        team_roles=team_roles,
        operating_rules=operating_rules,
        roles=roles,
    )


# ── Internal helpers ─────────────────────────────────────────────────


def _data_dir() -> Traversable:
    """Return the Traversable for ``fcop/teams/_data/``.

    Defined as a function (rather than a module-level constant) so
    testing hooks that patch :mod:`importlib.resources` see each call
    fresh, and so packaging regressions surface on first access
    rather than at import time.
    """
    return resources.files("fcop.teams").joinpath("_data")


@cache
def _load_bundled_teams() -> dict[str, TeamInfo]:
    """Parse ``_data/teams/index.json`` into a mapping of TeamInfo.

    Cached because the shape never changes during a process lifetime
    and re-reading the wheel on every :func:`get_team_info` call
    would be wasteful. Invalidation would require a process restart,
    which is fine: bundled data is, by definition, immutable in a
    given installed version.

    Raises:
        FcopError: the bundled index is missing or malformed. This
            indicates a packaging bug, not a user error — surface it
            loudly so CI catches it.
    """
    try:
        raw = _data_dir().joinpath("index.json").read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FcopError(
            "bundled index.json is missing from fcop.teams._data; "
            "rebuild the wheel or check pyproject.toml force-include"
        ) from exc

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FcopError(
            f"bundled index.json is not valid JSON: {exc}"
        ) from exc

    entries = parsed.get("teams")
    if not isinstance(entries, list) or not entries:
        raise FcopError("bundled index.json has no 'teams' list")

    result: dict[str, TeamInfo] = {}
    for entry in entries:
        info = _team_info_from_entry(entry)
        result[info.name] = info
    return result


def _team_info_from_entry(entry: object) -> TeamInfo:
    """Build a :class:`TeamInfo` from one ``index.json`` list item.

    Defensive about types: the index is hand-authored and a future
    maintainer fat-fingering a value should produce a loud
    :class:`FcopError`, not a mysterious AttributeError three call
    frames deep.
    """
    if not isinstance(entry, dict):
        raise FcopError(
            f"team entry must be a JSON object, got {type(entry).__name__}"
        )

    name = _required_str(entry, "id")
    display_name = _required_str(entry, "name_zh")
    leader = _required_str(entry, "leader")

    raw_roles = entry.get("roles")
    if not isinstance(raw_roles, list) or not raw_roles:
        raise FcopError(f"team {name!r} has no roles list")
    roles: tuple[str, ...] = tuple(str(r) for r in raw_roles)

    description_zh = _required_str(entry, "description_zh")
    description_en = _required_str(entry, "description_en")

    return TeamInfo(
        name=name,
        display_name=display_name,
        leader=leader,
        roles=roles,
        description_zh=description_zh,
        description_en=description_en,
    )


def _required_str(entry: dict[str, object], key: str) -> str:
    """Pull a non-empty string field out of a team entry or raise."""
    value = entry.get(key)
    if not isinstance(value, str) or not value.strip():
        raise FcopError(
            f"team entry is missing required string field {key!r}"
        )
    return value


def _read_lang_file(
    directory: Traversable,
    base: str,
    lang: str,
) -> str:
    """Read ``{base}.md`` (zh) or ``{base}.en.md`` (en) under *directory*.

    The lang-suffix convention is flat across all bundled teams:
    Chinese files have no language suffix, English files carry
    ``.en.md``. Aligns with ``index.json.lang_suffix``.
    """
    filename = f"{base}.md" if lang == "zh" else f"{base}.en.md"
    # Traversable.read_text() is declared to return str but mypy
    # cannot infer that through the abstract base class, so we cast.
    return str(directory.joinpath(filename).read_text(encoding="utf-8"))
