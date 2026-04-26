"""Tests for the role-template hard-constraint anchor (0.6.4).

Every bundled role charter under
``src/fcop/teams/_data/<team>/roles/<ROLE>{.,.en.}md`` must declare
the canonical "workflow hard constraint" section — the role-side
translation of ``fcop-rules.mdc`` Rule 0.a.1. This file is the
guardrail: a future contributor who copy-pastes a new role from a
sibling charter without porting the constraint will fail this test
and be forced to either keep the constraint or motivate its removal
in CHANGELOG.

The anchor strings are deliberately distinct from the section title
so renaming the section heading still satisfies the test as long as
the canonical phrase ("硬约束" / "hard constraint") survives. Solo's
``ME.md`` uses its own bespoke section ("核心工作流（硬约束 / 不允许
例外）" / "Core workflow (hard constraint / no exceptions)"), which
also contains the anchor — so the same rule applies uniformly.
"""

from __future__ import annotations

from importlib import resources
from typing import Literal

import pytest

from fcop.teams import get_available_teams, get_template

ZH_ANCHOR = "硬约束"
EN_ANCHOR = "hard constraint"

Lang = Literal["zh", "en"]


def _team_role_lang_cases() -> list[tuple[str, str, Lang]]:
    """Return ``(team, role, lang)`` triples for every bundled role
    charter, in both Chinese and English."""
    cases: list[tuple[str, str, Lang]] = []
    langs: tuple[Lang, ...] = ("zh", "en")
    for team_info in get_available_teams():
        for role in team_info.roles:
            for lang in langs:
                cases.append((team_info.name, role, lang))
    return cases


_CASES = _team_role_lang_cases()


@pytest.mark.parametrize(
    "team, role, lang",
    _CASES,
    ids=[f"{team}-{role}-{lang}" for team, role, lang in _CASES],
)
def test_role_charter_declares_hard_constraint(
    team: str, role: str, lang: Lang
) -> None:
    template = get_template(team, lang=lang)
    body = template.roles[role]
    anchor = ZH_ANCHOR if lang == "zh" else EN_ANCHOR
    haystack = body.lower() if lang == "en" else body
    assert anchor in haystack, (
        f"{team}/{role} ({lang}) charter is missing the canonical "
        f"hard-constraint anchor {anchor!r} — Rule 0.a.1 says role "
        "templates must NOT soften the four-step workflow into "
        "'simple tasks may run directly'. Add the workflow hard "
        "constraint section back."
    )


def test_every_team_contributes_role_cases() -> None:
    """Smoke test: each registered team contributes role cases.
    Catches a future bug where a team is added without role docs at
    all (which the per-role test would silently skip)."""
    seen_teams = {team for team, _r, _l in _CASES}
    expected = {t.name for t in get_available_teams()}
    assert seen_teams == expected, (
        "every bundled team must contribute role-charter cases — "
        f"missing: {expected - seen_teams}"
    )


def test_data_files_contain_anchor_on_disk() -> None:
    """Belt-and-braces sweep over the packaged ``_data`` directory.

    If a future contributor adds a charter file directly on disk
    without registering its role in ``index.json``, the
    parametrised test above would miss it; this test would not.
    """
    data_root = resources.files("fcop.teams._data")
    missing: list[str] = []
    for team_dir in data_root.iterdir():
        if not team_dir.is_dir():
            continue
        roles_dir = team_dir / "roles"
        if not roles_dir.is_dir():
            continue
        for role_file in roles_dir.iterdir():
            if not role_file.name.endswith(".md"):
                continue
            text = role_file.read_text(encoding="utf-8")
            is_en = role_file.name.endswith(".en.md")
            anchor = EN_ANCHOR if is_en else ZH_ANCHOR
            haystack = text.lower() if is_en else text
            if anchor not in haystack:
                missing.append(f"{team_dir.name}/roles/{role_file.name}")

    assert not missing, (
        "These bundled role charters are missing the workflow "
        f"hard-constraint anchor: {missing}"
    )
