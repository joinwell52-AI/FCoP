"""Public API surface snapshot tests.

See adr/ADR-0003-stability-charter.md for the governing policy.

This test freezes the public surface of the :mod:`fcop` library so that
unintended breaking changes cannot slip into 0.6.x releases unnoticed.

The public surface consists of four sets:

1. The :mod:`fcop` top-level ``__all__`` exports.
2. Every non-underscore method and property on :class:`fcop.Project`.
3. Every non-underscore field on every dataclass listed in
   :data:`PUBLIC_DATACLASSES`.
4. Every non-underscore callable in :mod:`fcop.teams` and
   :mod:`fcop.rules`.

When a change is **intentional and additive** (new method, new optional
parameter with default, new dataclass field with default), update the
snapshot:

    pytest tests/test_fcop/test_public_surface.py --snapshot-update

When a change is **breaking** (rename / delete / type change), the pull
request is *not* allowed to land unless ADR-0003's deprecation cycle has
been followed.

The snapshot file :file:`snapshots/public_surface.json` is tracked in
git; CI grep's the diff to ensure CHANGELOG.md records the change.
"""

from __future__ import annotations

import dataclasses
import inspect
import json
from pathlib import Path

import pytest

import fcop
from fcop import Project

SNAPSHOT_PATH = Path(__file__).parent / "snapshots" / "public_surface.json"

PUBLIC_DATACLASSES = [
    "Task",
    "TaskFrontmatter",
    "Report",
    "Issue",
    "TeamConfig",
    "ProjectStatus",
    "RecentActivityEntry",
    "ValidationIssue",
    "DeploymentReport",
]


def _describe_signature(obj: object) -> dict[str, object]:
    """Return a stable description of a callable's signature."""
    sig = inspect.signature(obj)  # type: ignore[arg-type]
    params = []
    for name, p in sig.parameters.items():
        params.append(
            {
                "name": name,
                "kind": p.kind.name,
                "has_default": p.default is not inspect.Parameter.empty,
                "annotation": (
                    str(p.annotation)
                    if p.annotation is not inspect.Parameter.empty
                    else None
                ),
            }
        )
    return {
        "params": params,
        "return": (
            str(sig.return_annotation)
            if sig.return_annotation is not inspect.Signature.empty
            else None
        ),
    }


def _collect_project_surface() -> dict[str, object]:
    result: dict[str, object] = {"methods": {}, "properties": {}}
    for name in sorted(dir(Project)):
        if name.startswith("_"):
            continue
        attr = inspect.getattr_static(Project, name)
        if isinstance(attr, property):
            assert attr.fget is not None
            result["properties"][name] = _describe_signature(  # type: ignore[index]
                attr.fget
            )
        elif callable(attr):
            result["methods"][name] = _describe_signature(attr)  # type: ignore[index]
    return result


def _collect_dataclass_surface() -> dict[str, object]:
    from fcop import models

    result: dict[str, object] = {}
    for cls_name in PUBLIC_DATACLASSES:
        cls = getattr(models, cls_name)
        fields_desc = []
        for f in dataclasses.fields(cls):
            fields_desc.append(
                {
                    "name": f.name,
                    "type": str(f.type),
                    "has_default": (
                        f.default is not dataclasses.MISSING
                        or f.default_factory is not dataclasses.MISSING
                    ),
                }
            )
        result[cls_name] = {"fields": fields_desc}
    return result


def _collect_submodule_surface(module_name: str) -> dict[str, object]:
    import importlib

    mod = importlib.import_module(f"fcop.{module_name}")
    exported = getattr(mod, "__all__", None)
    if exported is None:
        exported = [n for n in dir(mod) if not n.startswith("_")]
    result: dict[str, object] = {"exports": sorted(exported)}
    callables: dict[str, object] = {}
    for name in sorted(exported):
        obj = getattr(mod, name, None)
        if obj is None:
            continue
        if inspect.isfunction(obj) or inspect.isbuiltin(obj):
            callables[name] = _describe_signature(obj)
    result["callables"] = callables
    return result


def _collect_errors_surface() -> list[str]:
    from fcop import errors

    exported = [
        name
        for name in dir(errors)
        if not name.startswith("_") and isinstance(getattr(errors, name), type)
    ]
    return sorted(exported)


def _collect_surface() -> dict[str, object]:
    return {
        "version": "1",
        "top_level_all": sorted(fcop.__all__),
        "project": _collect_project_surface(),
        "dataclasses": _collect_dataclass_surface(),
        "teams": _collect_submodule_surface("teams"),
        "rules": _collect_submodule_surface("rules"),
        "errors": _collect_errors_surface(),
    }


def test_public_surface_matches_snapshot(pytestconfig: pytest.Config) -> None:
    """Fail if the observed public surface drifts from the snapshot.

    Update with ``pytest --snapshot-update`` when the change is
    intentional and ADR-0003 compliant.
    """
    observed = _collect_surface()

    if pytestconfig.getoption("--snapshot-update", default=False):
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_PATH.write_text(
            json.dumps(observed, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        pytest.skip("Snapshot updated; rerun without --snapshot-update to verify.")

    assert SNAPSHOT_PATH.exists(), (
        f"Snapshot missing: {SNAPSHOT_PATH}. "
        "Run `pytest --snapshot-update` to create it."
    )
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))

    if observed != expected:
        # Provide a readable diff instead of a raw dict dump.
        import difflib

        observed_text = json.dumps(observed, indent=2, sort_keys=True)
        expected_text = json.dumps(expected, indent=2, sort_keys=True)
        diff = "\n".join(
            difflib.unified_diff(
                expected_text.splitlines(),
                observed_text.splitlines(),
                fromfile="snapshot (expected)",
                tofile="observed (current)",
                lineterm="",
            )
        )
        pytest.fail(
            "Public API surface drifted from snapshot.\n\n"
            "Per ADR-0003 (Pre-1.0 Stability Charter):\n"
            "  * Additive changes: update snapshot with `pytest --snapshot-update`\n"
            "    and note the addition in CHANGELOG.md.\n"
            "  * Breaking changes (rename / delete / type change): NOT ALLOWED\n"
            "    in 0.6.x. See ADR-0003 for deprecation cycle.\n\n"
            f"Diff:\n{diff}"
        )


def test_top_level_all_is_a_subset_of_snapshot() -> None:
    """Catch accidental removal from ``fcop.__all__`` with a targeted message.

    This is the most common regression and has a clearer error than the
    big unified diff above.
    """
    if not SNAPSHOT_PATH.exists():
        pytest.skip("Snapshot not yet initialized")
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    missing = sorted(set(expected["top_level_all"]) - set(fcop.__all__))
    assert not missing, (
        f"The following symbols were removed from fcop.__all__: {missing}. "
        "Removal is forbidden in 0.6.x per ADR-0003."
    )


def test_project_methods_are_a_superset_of_snapshot() -> None:
    """Catch accidental method deletion on :class:`Project`."""
    if not SNAPSHOT_PATH.exists():
        pytest.skip("Snapshot not yet initialized")
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    expected_methods = set(expected["project"]["methods"].keys())
    observed_methods = {
        name
        for name in dir(Project)
        if not name.startswith("_") and callable(inspect.getattr_static(Project, name))
    }
    missing = expected_methods - observed_methods
    assert not missing, (
        f"The following Project methods disappeared: {sorted(missing)}. "
        "Method removal is forbidden in 0.6.x per ADR-0003."
    )


def test_dataclass_fields_are_not_removed() -> None:
    """Catch dataclass field deletion or rename."""
    if not SNAPSHOT_PATH.exists():
        pytest.skip("Snapshot not yet initialized")
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    from fcop import models

    for cls_name, snap in expected["dataclasses"].items():
        cls = getattr(models, cls_name)
        observed_names = {f.name for f in dataclasses.fields(cls)}
        expected_names = {f["name"] for f in snap["fields"]}
        missing = expected_names - observed_names
        assert not missing, (
            f"{cls_name}: fields disappeared: {sorted(missing)}. "
            "Dataclass field removal/rename is forbidden in 0.6.x per ADR-0003."
        )
