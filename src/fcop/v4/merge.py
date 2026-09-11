"""Core-only family inspection and recoverable, idempotent convergence append.

Lock order: workspace merge-operation lock, then exactly one existing family
lock. The REVIEW publication is the linearization point. A PREPARED receipt
contains the exact validated bytes; retries reconcile those bytes, never create
another identity. No adapter journal, new lifecycle, or background recovery.
"""

from __future__ import annotations

import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.convergence import SHA256_RE, members, snapshot, validate_convergence_request
from fcop.v4.encoding import (
    OP_RE,
    canonical,
    digest,
    envelope_bytes,
    fail,
    normalize,
    operation_lock,
    parse_envelope,
    publish,
    read_json,
    replace_durable,
    safe_path,
)
from fcop.v4.lifecycle import current_attempt, report_head
from fcop.v4.linearization import family_boundary
from fcop.v4.receipts import RECEIPT_STAGES

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation

CONTRACT = "fcop-convergence-append-v1"


def inspect_family(creation: _Creation, *, root_task_id: str) -> dict[str, Any]:
    creation._check()
    with family_boundary(creation.root, creation.manifest["workspace_id"], root_task_id):
        creation._check()
        return inspect_locked(creation, root_task_id)


def inspect_locked(creation: _Creation, root_task_id: str) -> dict[str, Any]:
    root_path, root_fields, branches = members(creation, root_task_id)
    reasons: list[dict[str, str]] = []
    rows = []
    if root_path.parent.name != "done":
        reasons.append({"code": "ROOT_NOT_DONE", "task_id": root_task_id})
    if not branches:
        reasons.append({"code": "FAMILY_CONVERGENCE_REQUIRED", "task_id": root_task_id})
    complete = True
    for path, fields in branches:
        task_id = fields["task_id"]
        row: dict[str, Any] = {
            "task_id": task_id,
            "stage": path.parent.name,
            "attempt_id": None,
            "report_head": None,
            "reasons": [],
        }
        if path.parent.name not in {"done", "archive"}:
            row["reasons"].append({"code": "BRANCH_NOT_TERMINAL", "task_id": task_id})
        try:
            attempt = current_attempt(fields)
            row["attempt_id"] = attempt
            report_path, report = report_head(creation, task_id, attempt)
            row["report_head"] = {
                "report_id": report["report_id"],
                "sha256": digest(report_path.read_bytes()),
                "attempt_id": attempt,
            }
        except V4ProtocolError as exc:
            complete = False
            row["reasons"].append({"code": exc.code, "task_id": task_id})
        reasons.extend(row["reasons"])
        rows.append(row)
    family_digest = snapshot(creation, root_task_id).digest if complete else None
    reviews = []
    for path in sorted(safe_path(creation.root, "fcop/reviews").glob("REVIEW-*.md")):
        path = safe_path(creation.root, path.relative_to(creation.root).as_posix())
        fields = creation._validate(parse_envelope(path), path)
        if fields.get("subject_ref") == root_task_id and fields.get("review_kind") == "convergence":
            reviews.append(
                {
                    "review_id": fields["review_id"],
                    "path": str(path),
                    "sha256": digest(path.read_bytes()),
                    "family_digest": fields["family_digest"],
                    "current": fields["family_digest"] == family_digest,
                    "references": fields.get("references", []),
                }
            )
    return {
        "root": {
            "task_id": root_task_id,
            "workspace_id": root_fields["workspace_id"],
            "stage": root_path.parent.name,
            "path": str(root_path),
        },
        "branches": rows,
        "family_digest": family_digest,
        "merge_ready": not reasons,
        "reasons": reasons,
        "convergence_reviews": reviews,
    }


def merge_branches(
    creation: _Creation,
    *,
    workspace_id: str,
    root_task_id: str,
    expected_family_digest: str,
    branch_report_heads: Mapping[str, str],
    conclusion: str,
    conflict_resolution: str,
    operation_id: str,
    sender: str,
    recipient: str,
) -> dict[str, Any]:
    from fcop.v4.creation import _request

    _request({"branch_report_heads": branch_report_heads}, {"branch_report_heads"}, set())
    if not isinstance(branch_report_heads, Mapping) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in branch_report_heads.items()
    ):
        raise fail(_V4Code.INVALID_ENVELOPE, "Expected Branch ID to REPORT ID mapping")
    if not normalize(conclusion).strip() or not normalize(conflict_resolution).strip():
        raise fail(_V4Code.INVALID_ENVELOPE, "Explicit conclusion and conflict resolution required")
    body = (
        "## Merge conclusion\n\n"
        + normalize(conclusion).strip()
        + "\n\n## Conflict resolution\n\n"
        + normalize(conflict_resolution).strip()
        + "\n"
    )
    return append(
        creation,
        dict(
            workspace_id=workspace_id,
            subject_ref=root_task_id,
            family_digest=expected_family_digest,
            references=list(branch_report_heads.values()),
            sender=sender,
            recipient=recipient,
            body=body,
            review_kind="convergence",
            decision="approved",
            operation_id=operation_id,
        ),
        branch_report_heads=dict(branch_report_heads),
    )


def _payload(kwargs: dict[str, Any]) -> tuple[dict[str, Any], str]:
    from fcop.v4.creation import _request

    required = {
        "workspace_id",
        "sender",
        "recipient",
        "body",
        "subject_ref",
        "review_kind",
        "decision",
    }
    allowed = required | {
        "references",
        "family_digest",
        "operation_id",
        "attempt_id",
        "authorization_ref",
        "profile_ref",
        "transition",
        "issued_at",
        "expires_at",
        "authorization_scope",
        "operation_kind",
        "issuer_proof",
    }
    request = _request(kwargs, allowed, required)
    if request["review_kind"] != "convergence" or request["decision"] != "approved":
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Convergence must be approved")
    family = request.get("family_digest")
    if not isinstance(family, str) or not SHA256_RE.fullmatch(family):
        raise fail(
            _V4Code.FAMILY_CONVERGENCE_MISMATCH, "A canonical non-null family digest is required"
        )
    references = request.get("references", [])
    if (
        not isinstance(references, (list, tuple))
        or not all(isinstance(ref, str) for ref in references)
        or len(set(references)) != len(references)
    ):
        raise fail(_V4Code.FAMILY_CONVERGENCE_MISMATCH, "Invalid exact REPORT references")
    value = {
        k: normalize(v) if isinstance(v, str) else v
        for k, v in request.items()
        if k != "operation_id" and v is not None
    }
    value["references"] = sorted(references)
    value["body"] = normalize(request["body"]).rstrip("\n") + "\n"
    for key in ("workspace_id", "sender", "recipient", "subject_ref"):
        if not isinstance(value.get(key), str) or not value[key]:
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid convergence identity")
    opid = request.get("operation_id", "merge-" + digest(canonical(value)))
    if not isinstance(opid, str) or not OP_RE.fullmatch(opid):
        raise fail(_V4Code.INVALID_ENVELOPE, "Invalid operation_id")
    return value, opid


def _key(payload: dict[str, Any]) -> str:
    return digest(
        canonical({k: payload[k] for k in ("workspace_id", "subject_ref", "family_digest")})
    )


def _read_receipt(creation: _Creation, path: Path) -> dict[str, Any]:
    """Reject copied, damaged or noncanonical evidence before any write."""
    try:
        value = read_json(safe_path(creation.root, path.relative_to(creation.root).as_posix()))
        required = {
            "contract",
            "payload",
            "request_digest",
            "operations",
            "review_id",
            "data",
            "content_digest",
            "stage",
            "branches",
        }
        if (
            set(value) != required
            or value["contract"] != CONTRACT
            or value["stage"] not in RECEIPT_STAGES
            or not isinstance(value["payload"], dict)
            or not isinstance(value["operations"], list)
            or not value["operations"]
            or len(set(value["operations"])) != len(value["operations"])
            or not all(isinstance(op, str) and OP_RE.fullmatch(op) for op in value["operations"])
            or value["payload"].get("workspace_id") != creation.manifest["workspace_id"]
            or path.name != f"merge-{_key(value['payload'])}.json"
            or value["request_digest"] != digest(canonical(value["payload"]))
        ):
            raise ValueError("receipt identity")
        data = bytes.fromhex(value["data"])
        if digest(data) != value["content_digest"]:
            raise ValueError("receipt content")
        target = safe_path(creation.root, f"fcop/reviews/{value['review_id']}.md")
        # Parse planned bytes without a temporary file or bypassing Schema.
        from fcop.v4.encoding import _parse_envelope_bytes

        fields = creation._validate(_parse_envelope_bytes(data), target)
        if fields["review_id"] != value["review_id"]:
            raise ValueError("review identity")
        comparable: dict[str, Any] = {k: fields.get(k) for k in value["payload"] if k != "body"}
        comparable["references"] = sorted(fields.get("references", []))
        if comparable != {k: v for k, v in value["payload"].items() if k != "body"}:
            raise ValueError("review request")
        if envelope_bytes(fields, value["payload"]["body"]) != data:
            raise ValueError("review body")
        if not isinstance(value["branches"], list):
            raise ValueError("branches")
        canonical_family = {
            "contract": "fcop-family-v1",
            "root_task_id": value["payload"]["subject_ref"],
            "branches": value["branches"],
        }
        from fcop.v4.schema import _validate

        _validate("family-canonical", canonical_family)
        if digest(canonical(canonical_family)) != value["payload"]["family_digest"]:
            raise ValueError("family digest")
        return value
    except (KeyError, TypeError, ValueError, V4ProtocolError) as exc:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid merge receipt", subject=str(path)) from exc


def _finish(
    creation: _Creation, path: Path, receipt: dict[str, Any], *, existing: bool
) -> dict[str, Any]:
    target = safe_path(creation.root, f"fcop/reviews/{receipt['review_id']}.md")
    data = bytes.fromhex(receipt["data"])
    if target.exists():
        if target.read_bytes() != data:
            raise fail(_V4Code.RECOVERY_REQUIRED, "Merge REVIEW differs from receipt")
    else:
        if receipt["stage"] != "PREPARED":
            raise fail(_V4Code.RECOVERY_REQUIRED, "Durable merge REVIEW is missing")
        family = validate_convergence_request(
            creation,
            receipt["payload"]["subject_ref"],
            receipt["payload"]["family_digest"],
            receipt["payload"]["references"],
        )
        if family.root_path.parent.name != "done":
            raise fail(_V4Code.INVALID_TRANSITION, "Root must be done")
        publish(target, data)
    creation._trigger_fault("merge_branches", "TARGET_DURABLE")
    if receipt["stage"] != "COMMITTED":
        receipt = {**receipt, "stage": "COMMITTED"}
        replace_durable(path, canonical(receipt) + b"\n")
    creation._trigger_fault("merge_branches", "COMMITTED")
    creation._trigger_fault("merge_branches", "RESPONSE_LOST")
    family_digest = receipt["payload"]["family_digest"]
    return {
        "review_id": receipt["review_id"],
        "review_ref": receipt["review_id"],
        "path": str(target),
        "root_task_id": receipt["payload"]["subject_ref"],
        "branches": receipt["branches"],
        "old_family_digest": family_digest,
        "new_family_digest": family_digest,
        "family_digest": family_digest,
        "existing": existing,
        "warnings": [],
    }


def append(
    creation: _Creation,
    kwargs: dict[str, Any],
    *,
    branch_report_heads: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload, opid = _payload(kwargs)
    creation._check(payload["workspace_id"])
    request_digest = digest(canonical(payload))
    # Reuse the existing OS operation lock, outside workspace facts so rejected
    # requests have zero fact-tree effects. All Core merge entry points use it.
    lock = Path(tempfile.gettempdir()) / (
        "fcop-merge-" + digest(payload["workspace_id"].encode()) + ".lock"
    )
    with (
        operation_lock(lock),
        family_boundary(creation.root, payload["workspace_id"], payload["subject_ref"]),
    ):
        creation._check(payload["workspace_id"])
        records = [
            (p, _read_receipt(creation, p))
            for p in sorted(safe_path(creation.root, "fcop/operations").glob("merge-*.json"))
        ]
        bound = [(p, r) for p, r in records if opid in r["operations"]]
        if len(bound) > 1:
            raise fail(_V4Code.RECOVERY_REQUIRED, "Duplicate merge operation identity")
        if bound:
            path, receipt = bound[0]
            if receipt["request_digest"] != request_digest:
                raise fail(
                    _V4Code.OPERATION_ID_CONFLICT,
                    "Merge operation has a different request",
                    operation=opid,
                )
            if branch_report_heads is not None and branch_report_heads != {
                row["branch_task_id"]: row["report_id"] for row in receipt["branches"]
            }:
                raise fail(
                    _V4Code.OPERATION_ID_CONFLICT,
                    "Branch mapping differs from original request",
                    operation=opid,
                )
            return _finish(creation, path, receipt, existing=True)
        family = validate_convergence_request(
            creation, payload["subject_ref"], payload["family_digest"], payload["references"]
        )
        if family.root_path.parent.name != "done":
            raise fail(_V4Code.INVALID_TRANSITION, "Convergence requires Root done")
        if branch_report_heads is not None and branch_report_heads != {
            row["branch_task_id"]: row["report_id"] for row in family.entries
        }:
            raise fail(
                _V4Code.FAMILY_CONVERGENCE_MISMATCH, "Exact Branch to REPORT mapping required"
            )
        path = safe_path(creation.root, f"fcop/operations/merge-{_key(payload)}.json")
        matching = [r for p, r in records if p == path]
        if matching:
            receipt = matching[0]
            if receipt["request_digest"] != request_digest:
                raise fail(
                    _V4Code.FAMILY_CONVERGENCE_MISMATCH,
                    "Different merge content already owns this family digest",
                )
            # Validate target BEFORE extending the operation alias set.
            target = safe_path(creation.root, f"fcop/reviews/{receipt['review_id']}.md")
            if target.exists() and target.read_bytes() != bytes.fromhex(receipt["data"]):
                raise fail(_V4Code.RECOVERY_REQUIRED, "Merge target differs")
            if not target.exists() and receipt["stage"] != "PREPARED":
                raise fail(_V4Code.RECOVERY_REQUIRED, "Merge target missing")
            receipt = {**receipt, "operations": sorted([*receipt["operations"], opid])}
            replace_durable(path, canonical(receipt) + b"\n")
            return _finish(creation, path, receipt, existing=True)
        # Never silently add another convergence over historical 4.0.0 facts.
        old = inspect_locked(creation, payload["subject_ref"])["convergence_reviews"]
        historical = [r for r in old if r["family_digest"] == payload["family_digest"]]
        if historical:
            if len(historical) != 1:
                raise fail(
                    _V4Code.FAMILY_CONVERGENCE_MISMATCH,
                    "Multiple historical facts; no automatic winner",
                )
            target = safe_path(creation.root, f"fcop/reviews/{historical[0]['review_id']}.md")
            fields = creation._validate(parse_envelope(target), target)
            comparable: dict[str, Any] = {k: fields.get(k) for k in payload if k != "body"}
            comparable["references"] = sorted(comparable["references"])
            if (
                comparable != {k: v for k, v in payload.items() if k != "body"}
                or envelope_bytes(fields, payload["body"]) != target.read_bytes()
            ):
                raise fail(
                    _V4Code.FAMILY_CONVERGENCE_MISMATCH, "Historical convergence content conflicts"
                )
            data = target.read_bytes()
            receipt = {
                "contract": CONTRACT,
                "payload": payload,
                "request_digest": request_digest,
                "operations": [opid],
                "review_id": fields["review_id"],
                "data": data.hex(),
                "content_digest": digest(data),
                "stage": "COMMITTED",
                "branches": list(family.entries),
            }
            publish(path, canonical(receipt) + b"\n")
            return _finish(creation, path, receipt, existing=True)
        fields = creation._common("REVIEW", payload["sender"], payload["recipient"])
        fields.update({k: v for k, v in payload.items() if k != "body"})
        target = safe_path(creation.root, f"fcop/reviews/{fields['review_id']}.md")
        creation._validate(fields, target)
        creation._relations(fields)
        data = envelope_bytes(fields, payload["body"])
        receipt = {
            "contract": CONTRACT,
            "payload": payload,
            "request_digest": request_digest,
            "operations": [opid],
            "review_id": fields["review_id"],
            "data": data.hex(),
            "content_digest": digest(data),
            "stage": "PREPARED",
            "branches": list(family.entries),
        }
        publish(path, canonical(receipt) + b"\n")
        creation._trigger_fault("merge_branches", "PREPARED")
        return _finish(creation, path, receipt, existing=False)
