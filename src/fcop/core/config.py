"""FCoP project configuration (``docs/agents/fcop.json``) parser.

This module turns the raw JSON on disk into a typed :class:`TeamConfig`.
Writing config back to disk is the responsibility of ``Project.init`` and
friends (see :mod:`fcop.project`) — this module only reads.

Legacy compatibility:
    FCoP 0.5.x wrote ``"mode": "team"`` for preset-team projects and
    ``"roles": [{"code": ..., "label": ...}]`` as a list of dicts. Both
    shapes are accepted here and normalized to the 0.6 shape
    (``"mode": "preset"`` / ``"roles": ["PM", ...]``). The original
    per-role labels, ``created_at``, and any other unknown keys are
    preserved under :attr:`TeamConfig.extra` so no information is lost.
"""

from __future__ import annotations

import json
from pathlib import Path

from fcop.core.schema import (
    PROTOCOL_VERSION,
    is_valid_role_code,
)
from fcop.errors import ConfigError
from fcop.models import TeamConfig

__all__ = [
    "parse_team_config",
    "load_team_config",
]


_VALID_MODES: frozenset[str] = frozenset({"solo", "preset", "custom"})
_LEGACY_MODE_ALIASES: dict[str, str] = {
    "team": "preset",
}


def parse_team_config(raw: object, *, source: Path | None = None) -> TeamConfig:
    """Parse a raw JSON-decoded object into a :class:`TeamConfig`.

    Args:
        raw: The result of ``json.loads`` on the ``fcop.json`` bytes.
             Must be a mapping; anything else raises :class:`ConfigError`.
        source: Optional path for inclusion in the raised error's
                ``.path`` attribute. Pass the actual ``fcop.json`` path
                when available so the caller can surface it in messages.

    Raises:
        ConfigError: ``raw`` is not a mapping, or any required field is
                     missing, wrong type, or invalid (e.g. a role code
                     that doesn't match :data:`ROLE_CODE_RE`).
    """
    err_path = source if source is not None else Path("<memory>")

    if not isinstance(raw, dict):
        raise ConfigError(
            f"fcop.json top-level must be a JSON object, got {type(raw).__name__}",
            path=err_path,
        )

    mode = _extract_mode(raw, err_path)
    leader = _extract_required_str(raw, "leader", err_path)
    team = _extract_required_str(raw, "team", err_path)
    roles, role_extras = _extract_roles(raw, err_path)
    lang = _extract_lang(raw)
    version = _extract_version(raw, err_path)

    if leader not in roles:
        raise ConfigError(
            f"leader {leader!r} is not listed among roles {list(roles)!r}",
            path=err_path,
        )

    extra = _collect_extra(raw, role_extras)

    return TeamConfig(
        mode=mode,  # type: ignore[arg-type]
        team=team,
        leader=leader,
        roles=roles,
        lang=lang,
        version=version,
        extra=extra,
    )


def load_team_config(path: Path) -> TeamConfig:
    """Read and parse ``fcop.json`` at *path*.

    Raises:
        ConfigError: the file is missing, not valid JSON, or fails
                     :func:`parse_team_config`'s structural checks.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ConfigError(f"fcop.json not found at {path}", path=path) from exc
    except OSError as exc:
        raise ConfigError(f"cannot read {path}: {exc}", path=path) from exc

    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"fcop.json is not valid JSON ({exc.msg} at line {exc.lineno})",
            path=path,
        ) from exc

    return parse_team_config(raw, source=path)


# ── internals ─────────────────────────────────────────────────────────


def _extract_mode(raw: dict[str, object], source: Path) -> str:
    value = raw.get("mode")
    if not isinstance(value, str):
        raise ConfigError(
            f"fcop.json 'mode' must be a string, got {type(value).__name__}",
            path=source,
        )
    normalized = _LEGACY_MODE_ALIASES.get(value, value)
    if normalized not in _VALID_MODES:
        raise ConfigError(
            f"fcop.json 'mode' must be one of {sorted(_VALID_MODES)}; got {value!r}",
            path=source,
        )
    return normalized


def _extract_required_str(raw: dict[str, object], key: str, source: Path) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(
            f"fcop.json {key!r} must be a non-empty string",
            path=source,
        )
    return value


def _extract_roles(
    raw: dict[str, object],
    source: Path,
) -> tuple[tuple[str, ...], dict[str, dict[str, object]]]:
    """Return (tuple-of-codes, mapping-of-code-to-legacy-fields).

    The second element preserves per-role labels and any other fields
    that existed on legacy dict-shaped role entries, so the caller can
    stash them in ``TeamConfig.extra``.
    """
    value = raw.get("roles")
    if not isinstance(value, list) or not value:
        raise ConfigError(
            "fcop.json 'roles' must be a non-empty list",
            path=source,
        )

    codes: list[str] = []
    labels: dict[str, dict[str, object]] = {}

    for i, entry in enumerate(value):
        if isinstance(entry, str):
            code = entry
        elif isinstance(entry, dict):
            raw_code = entry.get("code")
            if not isinstance(raw_code, str):
                raise ConfigError(
                    f"fcop.json roles[{i}].code must be a string",
                    path=source,
                )
            code = raw_code
            leftover = {k: v for k, v in entry.items() if k != "code"}
            if leftover:
                labels[code] = leftover
        else:
            raise ConfigError(
                f"fcop.json roles[{i}] must be a string or object with 'code'",
                path=source,
            )

        if not is_valid_role_code(code):
            raise ConfigError(
                f"fcop.json roles[{i}] = {code!r} is not a valid role code "
                "(must be uppercase ASCII, optionally hyphenated)",
                path=source,
            )
        if code in codes:
            raise ConfigError(
                f"fcop.json roles contains duplicate code {code!r}",
                path=source,
            )
        codes.append(code)

    return tuple(codes), labels


def _extract_lang(raw: dict[str, object]) -> str:
    value = raw.get("lang", "zh")
    if not isinstance(value, str) or not value:
        return "zh"
    return value


def _extract_version(raw: dict[str, object], source: Path) -> int:
    value = raw.get("version", PROTOCOL_VERSION)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(
            f"fcop.json 'version' must be an integer, got {type(value).__name__}",
            path=source,
        )
    if value < 1:
        raise ConfigError(
            f"fcop.json 'version' must be >= 1, got {value}",
            path=source,
        )
    return value


def _collect_extra(
    raw: dict[str, object],
    role_extras: dict[str, dict[str, object]],
) -> dict[str, object]:
    known = {"mode", "team", "leader", "roles", "lang", "version"}
    extra: dict[str, object] = {k: v for k, v in raw.items() if k not in known}
    if role_extras:
        extra["_role_labels"] = role_extras
    return extra
