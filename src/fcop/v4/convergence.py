"""Canonical Root-family snapshots and convergence validation."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.encoding import STAGES, canonical, digest, fail, parse_envelope, safe_path

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation

SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class FamilySnapshot:
    root_task_id: str
    root_path: Path
    root_fields: Mapping[str, Any]
    branches: tuple[tuple[Path, Mapping[str, Any]], ...]
    entries: tuple[Mapping[str, str], ...]
    value: Mapping[str, Any]
    digest: str


def snapshot(
    creation: _Creation, root_task_id: str, *, require_terminal: bool = False
) -> FamilySnapshot:
    """Re-read one family from authoritative envelopes; no cache or index."""
    root_path, root_fields = creation._resolve(root_task_id)
    if root_fields.get("type") != "TASK" or root_fields.get("branch_of") is not None:
        raise fail(_V4Code.RELATION_INVALID, "Family subject must be a Root TASK")

    found: dict[str, tuple[Path, Mapping[str, Any]]] = {}
    for stage in STAGES:
        folder = safe_path(creation.root, f"fcop/_lifecycle/{stage}")
        for candidate in sorted(folder.glob("TASK-*.md")):
            fields = creation._validate(parse_envelope(candidate), candidate)
            if fields.get("branch_of") != root_task_id:
                continue
            task_id = fields["task_id"]
            if task_id in found:
                raise fail(_V4Code.STATE_AMBIGUOUS, "Branch has multiple authoritative paths")
            path, resolved = creation._resolve(task_id)
            if path != candidate or resolved.get("branch_of") != root_task_id:
                raise fail(_V4Code.RELATION_INVALID, "Branch family relation is unstable")
            if require_terminal and path.parent.name not in {"done", "archive"}:
                raise fail(_V4Code.BRANCH_NOT_TERMINAL, "Every Branch must be terminal")
            found[task_id] = (path, resolved)

    from fcop.v4.lifecycle import current_attempt, report_head

    entries: list[Mapping[str, str]] = []
    branches = tuple(found[key] for key in sorted(found))
    for _path, branch_fields in branches:
        task_id = branch_fields["task_id"]
        attempt_id = current_attempt(branch_fields)
        report_path, report = report_head(creation, task_id, attempt_id)
        entries.append(
            {
                "branch_task_id": task_id,
                "attempt_id": attempt_id,
                "report_id": report["report_id"],
                "report_digest": digest(report_path.read_bytes()),
            }
        )
    value: Mapping[str, Any] = {
        "contract": "fcop-family-v1",
        "root_task_id": root_task_id,
        "branches": entries,
    }
    return FamilySnapshot(
        root_task_id, root_path, root_fields, branches, tuple(entries), value,
        digest(canonical(value)),
    )


def _root_report(creation: _Creation, family: FamilySnapshot) -> str | None:
    """Return the optional current Root REPORT, rejecting an ambiguous head."""
    from fcop.v4.lifecycle import current_attempt, report_head

    try:
        attempt = current_attempt(family.root_fields)
        _, report = report_head(creation, family.root_task_id, attempt)
    except V4ProtocolError as exc:
        if exc.code in {_V4Code.ATTEMPT_MISMATCH.value, _V4Code.REPORT_REQUIRED.value}:
            return None
        raise
    report_id = report.get("report_id")
    if not isinstance(report_id, str):
        raise fail(_V4Code.INVALID_ENVELOPE, "REPORT identity is invalid")
    return report_id


def validate_references(
    creation: _Creation, family: FamilySnapshot, references: Any
) -> tuple[str, ...]:
    if (
        isinstance(references, (str, bytes))
        or not isinstance(references, Sequence)
        or not all(isinstance(item, str) for item in references)
        or len(set(references)) != len(references)
    ):
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Invalid convergence references")
    branch_refs = {item["report_id"] for item in family.entries}
    supplied = set(references)
    permitted = [branch_refs]
    root_report = _root_report(creation, family)
    if root_report is not None:
        permitted.append(branch_refs | {root_report})
    if supplied not in permitted:
        raise fail(
            _V4Code.FAMILY_CONVERGENCE_MISMATCH,
            "Convergence does not reference the exact current family",
        )
    for reference in references:
        path, fields = creation._resolve(reference)
        if fields.get("type") != "REPORT":
            raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Convergence evidence is not REPORT")
        del path
    return tuple(sorted(supplied))


def validate_convergence_request(
    creation: _Creation, root_task_id: str, family_digest: Any, references: Any
) -> FamilySnapshot:
    family = snapshot(creation, root_task_id, require_terminal=True)
    if not family.branches:
        raise fail(_V4Code.FAMILY_CONVERGENCE_REQUIRED, "Convergence requires a Branch family")
    if not isinstance(family_digest, str) or not SHA256_RE.fullmatch(family_digest):
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Invalid family digest")
    validate_references(creation, family, references)
    if family_digest != family.digest:
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Family digest is stale")
    return family


def validate_stored_convergence(
    creation: _Creation, request: Mapping[str, Any], family: FamilySnapshot
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    reference = request.get("review_ref")
    if reference is None:
        raise fail(_V4Code.FAMILY_CONVERGENCE_REQUIRED, "Root T7 requires convergence")
    try:
        review_path, review = creation._resolve(reference)
    except V4ProtocolError as exc:
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Convergence REVIEW is unresolved") from exc
    if (
        review.get("type") != "REVIEW"
        or review.get("review_kind") != "convergence"
        or review.get("decision") != "approved"
        or review.get("subject_ref") != family.root_task_id
    ):
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Invalid convergence REVIEW")
    validate_references(creation, family, review.get("references"))
    supplied = request.get("family_digest")
    if supplied != family.digest or review.get("family_digest") != family.digest:
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Convergence snapshot is stale")

    refs = [review["review_id"]]
    digests = [digest(review_path.read_bytes())]
    for item in family.entries:
        report_path, report = creation._resolve(item["report_id"])
        refs.append(report["report_id"])
        digests.append(digest(report_path.read_bytes()))
    root_report = _root_report(creation, family)
    if root_report is not None and root_report in review.get("references", []):
        report_path, report = creation._resolve(root_report)
        refs.append(report["report_id"])
        digests.append(digest(report_path.read_bytes()))
    return tuple(refs), tuple(digests)
