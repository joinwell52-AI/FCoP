"""Private WP3C authorization verification for T4, T5, and T6."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.encoding import STAGES, digest, fail, parse_envelope, safe_path

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation


_AUTHORIZATION_CARRIERS: dict[
    str, tuple[frozenset[tuple[str, str]], str]
] = {
    "authorization": (
        frozenset({("review", "done"), ("review", "active"), ("done", "active")}),
        "authorize",
    ),
    "acceptance": (frozenset({("review", "done")}), "approved"),
    "rejection": (frozenset({("review", "active")}), "rejected"),
}


@dataclass(frozen=True)
class AuthorizationGate:
    """Validated immutable inputs used to construct one transition event."""

    evidence_ref: tuple[str, ...]
    evidence_digest: tuple[str, ...]
    authorization_ref: str
    authorization_digest: str
    profile_ref: str


def _time(value: Any, *, field: str) -> datetime:
    try:
        stamp = value
        if isinstance(stamp, str):
            stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if not isinstance(stamp, datetime) or stamp.utcoffset() is None:
            raise ValueError(field)
        return stamp
    except (TypeError, ValueError) as exc:
        raise fail(_V4Code.AUTHORIZATION_INVALID, f"Invalid {field}") from exc


def _utc_now() -> datetime:
    """Return the private UTC clock used at authorization linearization points."""
    return datetime.now(timezone.utc)


def _review(
    creation: _Creation, reference: Any
) -> tuple[Path, dict[str, Any], str]:
    if not isinstance(reference, str) or not reference.startswith("REVIEW-"):
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization must reference a REVIEW")
    try:
        path, fields = creation._resolve(reference)
    except V4ProtocolError as exc:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization REVIEW is not resolvable") from exc
    if fields.get("type") != "REVIEW" or fields.get("review_id") != reference:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization object is not a REVIEW")
    return path, fields, digest(path.read_bytes())


def usable_profiles(creation: _Creation) -> tuple[str, ...]:
    adopted = creation.manifest.get("profiles", [])
    return tuple(
        item
        for item in adopted
        if item in creation.trusted_profiles and callable(creation.trusted_profiles[item])
    )


def find_consumptions(
    creation: _Creation, authorization_ref: str
) -> list[tuple[str, Mapping[str, Any]]]:
    """Return durable transition events that consumed one authorization REVIEW."""
    found: list[tuple[str, Mapping[str, Any]]] = []
    for stage in STAGES:
        folder = safe_path(creation.root, f"fcop/_lifecycle/{stage}")
        for path in sorted(folder.glob("TASK-*.md")):
            fields = creation._validate(parse_envelope(path), path)
            for event in fields.get("transitions", []):
                if isinstance(event, Mapping) and event.get("authorization_ref") == authorization_ref:
                    found.append((fields["task_id"], event))
    return found


def _current_t3(
    fields: Mapping[str, Any], report_ref: str, report_digest: str
) -> None:
    transitions = fields.get("transitions", [])
    for event in reversed(transitions if isinstance(transitions, list) else []):
        if not isinstance(event, Mapping):
            continue
        if event.get("to") == "review":
            if (
                event.get("from") != "active"
                or event.get("tool") != "submit_task"
                or event.get("evidence_ref") != [report_ref]
                or event.get("evidence_digest") != [report_digest]
            ):
                raise fail(
                    _V4Code.EVIDENCE_DIGEST_MISMATCH,
                    "Current review round is not bound to the REPORT head",
                )
            return
    raise fail(_V4Code.AUTHORIZATION_INVALID, "Current review round has no T3 evidence")


def _evidence_review(
    creation: _Creation,
    request: Mapping[str, Any],
    *,
    task_id: str,
    attempt_id: str,
    edge: tuple[str, str],
    report_ref: str | None,
    report_digest: str | None,
) -> tuple[Path, dict[str, Any], str]:
    path, review, review_digest = _review(creation, request.get("review_ref"))
    expected = {
        ("review", "done"): ("acceptance", "approved"),
        ("review", "active"): ("rejection", "rejected"),
    }.get(edge)
    if expected is None:
        if review.get("review_kind") not in {"reopen", "authorization"}:
            raise fail(_V4Code.AUTHORIZATION_INVALID, "T6 requires a reopen/authorization REVIEW")
        if review.get("review_kind") == "reopen" and review.get("decision") != "approved":
            raise fail(_V4Code.AUTHORIZATION_INVALID, "Reopen REVIEW is not approved")
        if review.get("review_kind") == "authorization":
            if (
                review.get("decision") != "authorize"
                or review.get("operation_kind") != "lifecycle_transition"
                or review.get("transition") != {"from": edge[0], "to": edge[1]}
                or review.get("authorization_scope") != "single_use"
                or review.get("family_digest") is not None
                or not isinstance(review.get("profile_ref"), str)
                or not review.get("profile_ref")
                or "issuer_proof" not in review
            ):
                raise fail(
                    _V4Code.AUTHORIZATION_INVALID,
                    "T6 authorization evidence is structurally incomplete",
                )
            _time(review.get("issued_at"), field="issued_at")
            if review.get("expires_at") is not None:
                _time(review["expires_at"], field="expires_at")
    elif (review.get("review_kind"), review.get("decision")) != expected:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Evidence REVIEW kind/decision mismatch")
    if review.get("subject_ref") != task_id or review.get("attempt_id") != attempt_id:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Evidence REVIEW binding mismatch")
    if report_ref is not None and report_ref not in review.get("references", []):
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Evidence REVIEW does not reference REPORT head")
    if (
        report_digest is not None
        and "evidence_digest" in review
        and review.get("evidence_digest") != [report_digest]
    ):
        raise fail(_V4Code.EVIDENCE_DIGEST_MISMATCH, "REVIEW binds different REPORT bytes")
    return path, review, review_digest


def validate_gate(
    creation: _Creation,
    request: Mapping[str, Any],
    source_fields: Mapping[str, Any],
    *,
    attempt_id: str,
) -> AuthorizationGate:
    """Validate the complete evidence and trusted authorization gate."""
    available = usable_profiles(creation)
    if not available:
        raise fail(
            _V4Code.AUTHORIZATION_PROFILE_UNAVAILABLE,
            "No adopted Profile has a trusted evaluator",
        )
    auth_ref = request.get("authorization_ref")
    if auth_ref is None:
        raise fail(_V4Code.AUTHORIZATION_REQUIRED, "Transition requires authorization")

    edge = (request["from_stage"], request["to_stage"])
    task_id = request["task_id"]
    report_ref: str | None = None
    report_digest: str | None = None
    evidence_ref: list[str] = []
    evidence_digest: list[str] = []
    if edge[0] == "review":
        from fcop.v4.lifecycle import report_head

        report_path, report = report_head(creation, task_id, attempt_id)
        report_ref = report["report_id"]
        report_digest = digest(report_path.read_bytes())
        if request.get("report_ref") not in {None, report_ref}:
            raise fail(_V4Code.REPORT_HEAD_AMBIGUOUS, "Explicit REPORT is not current head")
        _current_t3(source_fields, report_ref, report_digest)
        evidence_ref.append(report_ref)
        evidence_digest.append(report_digest)
    elif request.get("report_ref") is not None:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "T6 consumes no REPORT")

    _, review, review_digest = _evidence_review(
        creation,
        request,
        task_id=task_id,
        attempt_id=attempt_id,
        edge=edge,
        report_ref=report_ref,
        report_digest=report_digest,
    )
    evidence_ref.append(review["review_id"])
    evidence_digest.append(review_digest)

    auth_path, authorization, authorization_digest = _review(creation, auth_ref)
    del auth_path
    review_kind = authorization.get("review_kind")
    carrier = (
        _AUTHORIZATION_CARRIERS.get(review_kind)
        if isinstance(review_kind, str)
        else None
    )
    if (
        carrier is None
        or edge not in carrier[0]
        or authorization.get("decision") != carrier[1]
    ):
        raise fail(
            _V4Code.AUTHORIZATION_INVALID,
            "REVIEW kind/decision cannot authorize this lifecycle edge",
        )
    if (
        authorization.get("subject_ref") != task_id
        or authorization.get("transition") != {"from": edge[0], "to": edge[1]}
        or authorization.get("attempt_id") != attempt_id
        or authorization.get("operation_kind") != "lifecycle_transition"
        or authorization.get("authorization_scope") != "single_use"
        or authorization.get("family_digest") is not None
    ):
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization binding mismatch")
    issued = _time(authorization.get("issued_at"), field="issued_at")
    expires_value = authorization.get("expires_at")
    expires: datetime | None = None
    if expires_value is not None:
        expires = _time(expires_value, field="expires_at")
        if expires < _utc_now():
            raise fail(_V4Code.AUTHORIZATION_EXPIRED, "Authorization has expired")
        if expires < issued:
            raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization time range is invalid")

    profile_ref = authorization.get("profile_ref")
    if request.get("profile_ref") not in {None, profile_ref}:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Requested Profile differs from REVIEW")
    if not isinstance(profile_ref, str) or not profile_ref:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization Profile is invalid")
    if profile_ref not in creation.manifest["profiles"]:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Profile is not adopted")
    evaluator = creation.trusted_profiles.get(profile_ref)
    if not callable(evaluator):
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Adopted Profile has no trusted evaluator")
    if "issuer_proof" not in authorization:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Authorization lacks issuer proof")
    try:
        decision = evaluator(
            profile_ref=profile_ref,
            issuer=authorization["sender"],
            proof=authorization["issuer_proof"],
        )
    except Exception as exc:
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Profile evaluation failed") from exc
    if decision != "AUTHORIZED":
        raise fail(_V4Code.AUTHORIZATION_INVALID, "Profile did not authorize issuer proof")
    if expires is not None and expires < _utc_now():
        raise fail(
            _V4Code.AUTHORIZATION_EXPIRED,
            "Authorization expired before consumption linearization",
        )

    if authorization.get("evidence_digest") is not None:
        bound = authorization["evidence_digest"]
        if not isinstance(bound, list) or bound != evidence_digest[: len(bound)]:
            raise fail(_V4Code.EVIDENCE_DIGEST_MISMATCH, "Authorization binds changed evidence")

    return AuthorizationGate(
        evidence_ref=tuple(evidence_ref),
        evidence_digest=tuple(evidence_digest),
        authorization_ref=auth_ref,
        authorization_digest=authorization_digest,
        profile_ref=profile_ref,
    )
