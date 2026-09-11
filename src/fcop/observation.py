"""Public read-only aggregation of existing Core facts for local adapters.

No repair, transport, authority evaluator or lifecycle decision is performed.
Multi-file observations are not an atomic snapshot of an active writer.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from importlib.resources import files
from pathlib import Path
from typing import Any

from fcop import Project, __version__
from fcop.errors import FcopError

__all__ = ["workspace_status", "inspect_object", "validate_workspace", "bundled_inventory"]


def _context(root: Path | str) -> tuple[Project, Any]:
    from fcop.v4.creation import _Creation
    from fcop.v4.encoding import parse_json

    project = Project(root)
    creation = _Creation.open_if_declared(project.path)
    if project.config_path.exists():
        # Classification must not silently fall through malformed/duplicate JSON.
        parse_json(project.config_path.read_bytes(), classification=True)
        if creation is not None:
            if creation.invalid:
                raise ValueError("Cannot classify workspace declaration")
            creation._check()
        else:
            _ = project.config
    elif project.workspace_dir.exists():
        raise ValueError("Workspace directory exists without a complete manifest")
    return project, creation


def workspace_status(root: Path | str) -> dict[str, Any]:
    """Read workspace declaration/layout and available Core status, never initialize."""
    project, creation = _context(root)
    result: dict[str, Any] = {
        "project_root": str(project.path), "workspace_path": str(project.workspace_dir),
        "initialized": project.is_initialized(), "core_version": __version__,
        "protocol_version": None, "workspace_id": None, "warnings": [],
        "topology": project.topology, "layout": project.workspace_layout,
    }
    if creation is not None:
        from fcop.v4.encoding import BUCKETS, STAGES, safe_path

        result.update(protocol_version=creation.manifest["protocol_version"],
                      workspace_id=creation.manifest["workspace_id"],
                      encoding=creation.manifest["encoding"])
        result["counts"] = {
            part: len(list(safe_path(project.path, f"fcop/{part}").glob("*.md")))
            for part in [*(f"_lifecycle/{s}" for s in STAGES), *BUCKETS.values()]
        }
    elif result["initialized"]:
        result["protocol_version"] = project.config.version
        result["summary"] = asdict(project.status())
    return result


def _contained(project: Project, value: Path | str) -> Path:
    from fcop.v4.encoding import safe_path

    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project.path / candidate
    # Preserve lexical path so safe_path can reject links before resolution.
    relative = candidate.relative_to(project.path)
    path = safe_path(project.path, relative.as_posix())
    if not path.is_relative_to(project.workspace_dir):
        raise ValueError("Envelope path must be within the selected workspace")
    return path


def inspect_object(
    root: Path | str, *, task_id: str | None = None, path: Path | str | None = None,
) -> dict[str, Any]:
    """Read one object via version-selected Core readers and canonical inspection."""
    project, creation = _context(root)
    if not project.is_initialized():
        raise FileNotFoundError("Workspace is not initialized")
    if (task_id is None) == (path is None):
        raise ValueError("Choose exactly one TASK ID or envelope path")
    if creation is not None:
        if path is None:
            state = project.inspect_state(task_id=task_id)
            selected = Path(state["path"])
        else:
            selected = _contained(project, path)
        envelope = project.inspect_state(envelope_path=selected.relative_to(project.path))
        identity = envelope[envelope["type"].lower() + "_id"]
        canonical, _ = creation._resolve(identity)
        if canonical != selected:
            raise ValueError("Envelope is not at its canonical authoritative path")
        result = dict(envelope)
        if envelope["type"] == "TASK":
            state = project.inspect_state(task_id=identity)
            result.update(state)
            from fcop.errors import _V4Code
            from fcop.v4.encoding import digest
            from fcop.v4.lifecycle import report_head

            result["report_head"] = None
            if state["current_attempt_id"] is not None:
                try:
                    head_path, head = report_head(creation, identity, state["current_attempt_id"])
                    result["report_head"] = {"report_id": head["report_id"], "path": str(head_path),
                                             "sha256": digest(head_path.read_bytes())}
                except FcopError as exc:
                    error_code = getattr(exc, "code", None)
                    if error_code != _V4Code.REPORT_REQUIRED.value:
                        raise
                    result.setdefault("warnings", []).append({"code": error_code, "message": str(exc)})
            root_id = envelope.get("branch_of") or identity
            result["family"] = project.inspect_family(root_task_id=root_id)
        return result
    if task_id is not None:
        task = project.read_task(task_id)
        return {"object": asdict(task), "warnings": project.inspect_task(task_id)}
    assert path is not None
    selected = _contained(project, path)
    from fcop.core import filename
    from fcop.core.frontmatter import parse_frontmatter_raw
    from fcop.core.jsonschema_validator import validate_envelope_frontmatter

    kind = selected.name.split("-", 1)[0]
    parsers = {"TASK": filename.parse_task_filename, "REPORT": filename.parse_report_filename,
               "ISSUE": filename.parse_issue_filename, "REVIEW": filename.parse_review_filename}
    if kind not in parsers or parsers[kind](selected.name) is None:
        raise ValueError("Invalid legacy envelope filename")
    fields = parse_frontmatter_raw(selected.read_text(encoding="utf-8"))
    issues = validate_envelope_frontmatter(fields, kind)
    if issues:
        raise ValueError(str(issues))
    if kind == "TASK":
        extra = project.inspect_task(selected.name)
        if extra:
            raise ValueError(str(extra))
    return {"path": str(selected), "type": kind, "fields": fields, "warnings": []}


def validate_workspace(root: Path | str, *, path: Path | str | None = None) -> dict[str, Any]:
    """Validate observable envelopes with installed Core checks, not business quality."""
    project, creation = _context(root)
    if not project.is_initialized():
        raise FileNotFoundError("Workspace is not initialized")
    candidates = [_contained(project, path)] if path is not None else sorted(
        p for p in project.workspace_dir.rglob("*.md")
        if p.name.startswith(("TASK-", "REPORT-", "ISSUE-", "REVIEW-"))
    )
    errors: list[dict[str, str]] = []
    warnings: list[Any] = []
    for candidate in candidates:
        try:
            observed = inspect_object(root, path=candidate)
            warnings.extend(observed.get("warnings", []))
            if creation is not None and observed["type"] == "TASK":
                last = observed["last_transition"]
                if last and last["to"] != observed["stage"]:
                    raise ValueError("Directory state and last transition disagree")
        except (FcopError, ValueError, OSError) as exc:
            errors.append({"path": str(candidate), "code": str(getattr(exc, "code", "INVALID_DATA")),
                           "message": str(exc)})
    return {"valid": not errors, "checked": len(candidates), "errors": errors,
            "warnings": warnings, "scope": "observable Core envelope facts; no business judgment"}


def bundled_inventory() -> dict[str, Any]:
    """Return installed Schema/rule identities and the frozen spec citation offline."""
    from fcop.rules import get_rules_version
    from fcop.v4.rule_distribution._loader import load
    from fcop.v4.rule_distribution._read import specification_identity
    from fcop.v4.schema import _validators

    package = files("fcop")
    directory = package.joinpath("_data/schemas/v4")
    workspace = json.loads(directory.joinpath("workspace.schema.json").read_bytes())
    props = workspace["properties"]
    _validators()  # validates all bundled schema definitions/references without a network
    rules = load(None, "cli_inventory")
    return {"protocol": props["protocol"]["const"],
            "protocol_version": props["protocol_version"]["const"], "core_version": __version__,
            "specification": {**specification_identity("cli_inventory"), "bundled_text": False},
            "schema_path": str(directory),
            "schemas": sorted(p.name for p in directory.iterdir() if p.name.endswith(".schema.json")),
            "rules_path": str(package.joinpath("rules/_data/v4")),
            "rules_version": rules.manifest["package_version"],
            "rules_manifest_sha256": rules.manifest_sha256,
            "legacy_rules_version": get_rules_version()}
