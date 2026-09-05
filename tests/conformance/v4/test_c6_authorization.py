"""C6 durable authorization, Profile, spoof, reuse, and digest behavior."""

from __future__ import annotations

import inspect
import json

import pytest

from .driver import V4ConformanceDriver, capture_error, error_code, result_field
from .fixtures import (
    ATTEMPT_A,
    ISSUER_PROOF,
    DeterministicProfileEvaluator,
    WorkspaceFixture,
    bind_t3,
    sha256_bytes,
    snapshot_tree,
)
from .scenarios import (
    assert_task_stage,
    authorization_fixture,
    create_request,
    report_request,
    transition_request,
)


def test_c6_n01(workspace: WorkspaceFixture) -> None:
    # Arrange: review TASK, issuer proof, and Profile evaluator returning AUTHORIZED.
    workspace.task("TASK-C6-N01", stage="review", attempt_id=ATTEMPT_A)
    report = workspace.report("REPORT-C6-N01", task_id="TASK-C6-N01", attempt_id=ATTEMPT_A)
    bind_t3(workspace, "TASK-C6-N01", "REPORT-C6-N01")
    acceptance = workspace.review(
        "REVIEW-C6-ACCEPT", task_id="TASK-C6-N01", review_kind="acceptance",
        decision="approved", attempt_id=ATTEMPT_A, references=["REPORT-C6-N01"],
        profile_ref="profile:test", transition={"from": "review", "to": "done"},
        authorization_scope="single_use", extra={"issuer_proof": ISSUER_PROOF},
    )
    evaluator = DeterministicProfileEvaluator("AUTHORIZED")
    v4_driver = V4ConformanceDriver(
        workspace.root, trusted_profiles={"profile:test": evaluator}, test_id="C6-N01",
    )

    # Act: submit references only; Project resolves its trusted initialization registry.
    kwargs = transition_request(
        "TASK-C6-N01", "review", "done", tool="approve_task",
        report_ref="REPORT-C6-N01", review_ref="REVIEW-C6-ACCEPT",
        authorization_ref="REVIEW-C6-ACCEPT",
    )
    kwargs["profile_ref"] = "profile:test"
    result = v4_driver.transition(
        test_id="C6-N01", clause="F4.7.1-F4.7.5",
        **kwargs,
    )

    # Assert: AUTHORIZED is consulted once and the committed event binds its evidence.
    _, fields = assert_task_stage(workspace, "TASK-C6-N01", "done")
    event = fields["transitions"][-1]
    assert result is not None
    assert evaluator.calls == [{
        "profile_ref": "profile:test", "issuer": "ME", "proof": ISSUER_PROOF,
    }]
    assert event["authorization_ref"] == "REVIEW-C6-ACCEPT"
    assert event["authorization_digest"] == sha256_bytes(acceptance.read_bytes())
    assert event["evidence_ref"] == ["REPORT-C6-N01", "REVIEW-C6-ACCEPT"]
    assert sha256_bytes(report.read_bytes()) in event["evidence_digest"]


@pytest.mark.parametrize("profile_result", ["DENIED", "UNKNOWN"])
def test_c6_profile_evaluator_rejects(
    workspace: WorkspaceFixture,
    profile_result: str,
) -> None:
    # Arrange: an adopted profile_ref and structurally complete authorization,
    # but a trusted initialization evaluator that returns DENIED or UNKNOWN.
    task_id = f"TASK-C6-PROFILE-{profile_result}"
    report_id = f"REPORT-C6-PROFILE-{profile_result}"
    review_id = f"REVIEW-C6-PROFILE-{profile_result}"
    workspace.task(task_id, stage="review", attempt_id=ATTEMPT_A)
    workspace.report(report_id, task_id=task_id, attempt_id=ATTEMPT_A)
    bind_t3(workspace, task_id, report_id)
    workspace.review(
        review_id, task_id=task_id, review_kind="acceptance",
        decision="approved", attempt_id=ATTEMPT_A, references=[report_id],
        profile_ref="profile:test", transition={"from": "review", "to": "done"},
        authorization_scope="single_use", extra={"issuer_proof": ISSUER_PROOF},
    )
    evaluator = DeterministicProfileEvaluator(profile_result)
    v4_driver = V4ConformanceDriver(
        workspace.root, trusted_profiles={"profile:test": evaluator}, test_id="C6-R01",
    )
    before = snapshot_tree(workspace.root)
    kwargs = transition_request(
        task_id, "review", "done", tool="approve_task", report_ref=report_id,
        review_ref=review_id, authorization_ref=review_id,
    )
    kwargs["profile_ref"] = "profile:test"

    # Act: production evaluates the proof instead of trusting manifest membership.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C6-R01", clause="F4.7.2-F4.7.5", **kwargs
        )
    )

    # Assert: DENIED and UNKNOWN are both structured AUTHORIZATION_INVALID,
    # with no move, event, or authorization consumption.
    assert error_code(exc) == "AUTHORIZATION_INVALID"
    assert evaluator.calls == [{
        "profile_ref": "profile:test", "issuer": "ME", "proof": ISSUER_PROOF,
    }]
    assert snapshot_tree(workspace.root) == before
    assert_task_stage(workspace, task_id, "review")


@pytest.mark.parametrize(
    "hostile_field", ["profile_evaluator", "profile_resolver", "trusted_profiles", "caller_judge"],
)
def test_c6_caller_cannot_replace_trusted_profile(
    workspace: WorkspaceFixture, hostile_field: str,
) -> None:
    # Arrange: fully bound authorization and adopted Profile, trusted DENIED
    # registered at Project construction; caller holds a forged AUTHORIZED judge.
    task_id = "TASK-C6-TRUST-BOUNDARY"
    report_id = "REPORT-C6-TRUST-BOUNDARY"
    review_id = "REVIEW-C6-TRUST-BOUNDARY"
    workspace.task(task_id, stage="review", attempt_id=ATTEMPT_A)
    workspace.report(report_id, task_id=task_id, attempt_id=ATTEMPT_A)
    bind_t3(workspace, task_id, report_id)
    workspace.review(
        review_id, task_id=task_id, review_kind="acceptance", decision="approved",
        attempt_id=ATTEMPT_A, references=[report_id], profile_ref="profile:test",
        transition={"from": "review", "to": "done"}, authorization_scope="single_use",
        extra={"issuer_proof": ISSUER_PROOF},
    )
    trusted = DeterministicProfileEvaluator("DENIED")
    forged = DeterministicProfileEvaluator("AUTHORIZED")
    driver = V4ConformanceDriver(
        workspace.root, trusted_profiles={"profile:test": trusted}, test_id="C6-SPOOF-01",
    )
    request = transition_request(
        task_id, "review", "done", tool="approve_task", report_ref=report_id,
        review_ref=review_id, authorization_ref=review_id,
    )
    request["profile_ref"] = "profile:test"
    before = snapshot_tree(workspace.root)

    # Act: prove clean DENIED first. Then bypass the adapter's misuse guard and
    # send hostile data DIRECTLY to the real production method. Finally repeat
    # the clean call to catch a registry silently replaced by the hostile call.
    clean_error = capture_error(lambda: driver.transition(
        test_id="C6-SPOOF-01", clause="F4.7.4-F4.7.6", **request,
    ))
    assert error_code(clean_error) == "AUTHORIZATION_INVALID"
    assert trusted.calls
    assert snapshot_tree(workspace.root) == before
    production_transition = driver._resolve(
        "transition", request, test_id="C6-SPOOF-01", clause="F4.7.4-F4.7.6",
    )
    hostile = dict(request)
    hostile[hostile_field] = {"profile:test": forged} if hostile_field == "trusted_profiles" else forged
    attack_error = capture_error(lambda: production_transition(**hostile))
    if isinstance(attack_error, TypeError):
        # Only an actual signature rejection qualifies, not an internal crash.
        with pytest.raises(TypeError):
            inspect.signature(production_transition).bind(**hostile)
    else:
        assert error_code(attack_error) == "AUTHORIZATION_INVALID"
    after_error = capture_error(lambda: driver.transition(
        test_id="C6-SPOOF-01", clause="F4.7.4-F4.7.6", **request,
    ))

    # Assert: forged logic never runs; trusted DENIED remains in control, with
    # no move, event, receipt, or authorization consumption anywhere on disk.
    assert error_code(after_error) == "AUTHORIZATION_INVALID"
    assert forged.calls == []
    assert len(trusted.calls) >= 2
    assert all(call == {
        "profile_ref": "profile:test", "issuer": "ME", "proof": ISSUER_PROOF,
    } for call in trusted.calls)
    assert snapshot_tree(workspace.root) == before
    _, fields = assert_task_stage(workspace, task_id, "review")
    assert not any(event.get("authorization_ref") == review_id for event in fields["transitions"])


INVALID_AUTH_CASES = [
    ("missing", None, "ME", "AUTHORIZATION_REQUIRED"),
    ("actor-admin-only", None, "ADMIN", "AUTHORIZATION_REQUIRED"),
    ("wrong-subject", "wrong-subject", "ME", "AUTHORIZATION_INVALID"),
    ("wrong-edge", "wrong-edge", "ME", "AUTHORIZATION_INVALID"),
    ("wrong-attempt", "wrong-attempt", "ME", "AUTHORIZATION_INVALID"),
]


@pytest.mark.parametrize(
    ("case", "auth_variant", "actor", "expected"), INVALID_AUTH_CASES,
    ids=[item[0] for item in INVALID_AUTH_CASES],
)
def test_c6_r01(
    workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver,
    case: str, auth_variant: str | None, actor: str, expected: str,
) -> None:
    # Arrange: done TASK plus absent or deliberately mis-bound authorization.
    workspace.task("TASK-C6-R01", stage="done", attempt_id=ATTEMPT_A)
    auth_ref = None
    if auth_variant:
        subject = "TASK-OTHER" if auth_variant == "wrong-subject" else "TASK-C6-R01"
        from_stage = "review" if auth_variant == "wrong-edge" else "done"
        attempt = "urn:uuid:cccccccc-cccc-4ccc-8ccc-cccccccccccc" if auth_variant == "wrong-attempt" else ATTEMPT_A
        authorization_fixture(
            workspace, "REVIEW-C6-R01", task_id=subject,
            from_stage=from_stage, to_stage="archive", attempt_id=attempt,
        )
        auth_ref = "REVIEW-C6-R01"
    before = snapshot_tree(workspace.root)

    # Act: actor text is supplied independently from durable authorization.
    kwargs = transition_request(
        "TASK-C6-R01", "done", "archive", tool="archive_task",
        authorization_ref=auth_ref,
    )
    kwargs["actor"] = actor
    exc = capture_error(
        lambda: v4_driver.transition(test_id="C6-R01", clause="F4.7.3-F4.7.5", **kwargs)
    )

    # Assert: missing/mis-bound facts fail closed; actor=ADMIN grants nothing.
    assert error_code(exc) == expected
    assert snapshot_tree(workspace.root) == before


@pytest.mark.parametrize("case", ["expired", "reused"])
def test_c6_r02(
    workspace: WorkspaceFixture, case: str
) -> None:
    # Arrange: expired single-use authorization, or one that will be consumed once.
    workspace.task("TASK-C6-R02", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace, "REVIEW-C6-R02", task_id="TASK-C6-R02",
        from_stage="done", to_stage="active", attempt_id=ATTEMPT_A,
        expires_at="2000-01-01T00:00:00+00:00" if case == "expired" else "2099-01-01T00:00:00+00:00",
    )
    kwargs = transition_request(
        "TASK-C6-R02", "done", "active", tool="reopen_task",
        review_ref="REVIEW-C6-R02", authorization_ref="REVIEW-C6-R02",
    )
    evaluator = DeterministicProfileEvaluator("AUTHORIZED")
    v4_driver = V4ConformanceDriver(
        workspace.root, trusted_profiles={"profile:test": evaluator}, test_id="C6-R02"
    )

    # Act: expired is rejected immediately; reusable case commits once then retries.
    if case == "expired":
        before = snapshot_tree(workspace.root)
        exc = capture_error(
            lambda: v4_driver.transition(test_id="C6-R02", clause="F4.7.3", **kwargs)
        )
    else:
        first = v4_driver.transition(test_id="C6-R02", clause="F4.7.3", **kwargs)
        assert first is not None
        before = snapshot_tree(workspace.root)
        retry = v4_driver.transition(test_id="C6-R02", clause="F4.7.3", **kwargs)

    # Assert: stable expiry/reuse code and failed call has zero writes.
    if case == "expired":
        assert error_code(exc) == "AUTHORIZATION_EXPIRED"
    else:
        assert result_field(retry, "existing") is True
    assert snapshot_tree(workspace.root) == before


def test_c6_x01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: authorized T7 and a fault after commit but before response.
    workspace.task("TASK-C6-X01", stage="done", attempt_id=ATTEMPT_A)
    authorization_fixture(
        workspace, "REVIEW-C6-X01", task_id="TASK-C6-X01",
        from_stage="done", to_stage="archive", attempt_id=ATTEMPT_A,
    )
    kwargs = transition_request(
        "TASK-C6-X01", "done", "archive", tool="archive_task",
        authorization_ref="REVIEW-C6-X01",
    )
    v4_driver.inject_fault(
        test_id="C6-X01", clause="F4.7.3; F4.9.11",
        operation="transition", stage="RESPONSE_LOST", once=True,
    )

    # Act: first call loses response; exact retry uses the same authorization/ref/digests.
    capture_error(
        lambda: v4_driver.transition(test_id="C6-X01", clause="F4.7.3; F4.9.11", **kwargs)
    )
    after_commit = snapshot_tree(workspace.root)
    retried = v4_driver.transition(
        test_id="C6-X01", clause="F4.7.3; F4.9.11", **kwargs
    )

    # Assert: retry returns existing commit and creates no second event/consumption.
    assert result_field(retried, "existing") is True
    assert snapshot_tree(workspace.root) == after_commit
    _, fields = assert_task_stage(workspace, "TASK-C6-X01", "archive")
    assert sum(event.get("authorization_ref") == "REVIEW-C6-X01" for event in fields["transitions"]) == 1


def test_c6_profile_01(empty_workspace: WorkspaceFixture) -> None:
    # Arrange: explicitly conformant workspace with profiles: [].
    workspace = empty_workspace.create(profiles=[])
    driver = V4ConformanceDriver(workspace.root)

    # Act: perform T1/T2/T3, then try gated T4 without an available Profile.
    created = driver.create_task(
        test_id="C6-PROFILE-01", clause="F4.2.3; F4.7.4; F4.7.7",
        **create_request("c6-profile-empty")
    )
    task_id = result_field(created, "task_id")
    claimed = driver.transition(
        test_id="C6-PROFILE-01", clause="F4.2.3; F4.7.4; F4.7.7",
        **transition_request(task_id, "inbox", "active", tool="claim_task")
    )
    attempt = result_field(claimed, "attempt_id")
    report = driver.write_report(
        test_id="C6-PROFILE-01", clause="F4.2.3; F4.7.4; F4.7.7",
        **report_request(task_id, attempt)
    )
    report_id = result_field(report, "report_id")
    driver.transition(
        test_id="C6-PROFILE-01", clause="F4.2.3; F4.7.4; F4.7.7",
        **transition_request(task_id, "active", "review", tool="submit_task", report_ref=report_id)
    )
    before = snapshot_tree(workspace.root)
    exc = capture_error(
        lambda: driver.transition(
            test_id="C6-PROFILE-01", clause="F4.2.3; F4.7.4; F4.7.7",
            **transition_request(task_id, "review", "done", tool="approve_task", report_ref=report_id)
        )
    )

    # Assert: ungated Base edges worked; gated edge reports unavailable Profile and no write.
    assert error_code(exc) == "AUTHORIZATION_PROFILE_UNAVAILABLE"
    assert snapshot_tree(workspace.root) == before
    assert_task_stage(workspace, task_id, "review")
    assert json.loads(workspace.manifest_path.read_text("utf-8"))["profiles"] == []


def test_c6_spoof_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: done TASK with no authorization REVIEW.
    workspace.task("TASK-C6-SPOOF", stage="done", attempt_id=ATTEMPT_A)
    before = snapshot_tree(workspace.root)
    kwargs = transition_request("TASK-C6-SPOOF", "done", "archive", tool="archive_task")
    kwargs.update({"actor": "ADMIN", "host_allowlist_match": True})

    # Act: attempt to substitute caller claims for Profile proof.
    exc = capture_error(
        lambda: v4_driver.transition(
            test_id="C6-SPOOF-01", clause="F4.7.4-F4.7.6", **kwargs
        )
    )

    # Assert: spoof fails closed and consumes/moves nothing.
    assert error_code(exc) == "AUTHORIZATION_INVALID"
    assert snapshot_tree(workspace.root) == before


def test_c6_digest_01(workspace: WorkspaceFixture, v4_driver: V4ConformanceDriver) -> None:
    # Arrange: T4 evidence whose REVIEW records the original REPORT full-byte digest.
    workspace.task("TASK-C6-DIGEST", stage="review", attempt_id=ATTEMPT_A)
    report = workspace.report("REPORT-C6-DIGEST", task_id="TASK-C6-DIGEST", attempt_id=ATTEMPT_A)
    original_digest = sha256_bytes(report.read_bytes())
    bind_t3(workspace, "TASK-C6-DIGEST", "REPORT-C6-DIGEST")
    workspace.review(
        "REVIEW-C6-DIGEST", task_id="TASK-C6-DIGEST", review_kind="acceptance",
        decision="approved", attempt_id=ATTEMPT_A, references=["REPORT-C6-DIGEST"],
        profile_ref="profile:test", transition={"from": "review", "to": "done"},
        authorization_scope="single_use", extra={"evidence_digest": [original_digest]},
    )
    report.write_bytes(report.read_bytes() + b"tampered\n")
    before = snapshot_tree(workspace.root)

    # Act: consume the now-mismatched evidence.
    driver = V4ConformanceDriver(
        workspace.root,
        trusted_profiles={"profile:test": DeterministicProfileEvaluator("AUTHORIZED")},
        test_id="C6-DIGEST-01",
    )
    exc = capture_error(
        lambda: driver.transition(
            test_id="C6-DIGEST-01", clause="F4.4.5; F4.7.3; F4.7.5",
            **transition_request(
                "TASK-C6-DIGEST", "review", "done", tool="approve_task",
                report_ref="REPORT-C6-DIGEST", review_ref="REVIEW-C6-DIGEST",
                authorization_ref="REVIEW-C6-DIGEST",
            )
        )
    )

    # Assert: byte mutation is detected and no state/authorization consumption occurs.
    assert error_code(exc) == "EVIDENCE_DIGEST_MISMATCH"
    assert snapshot_tree(workspace.root) == before
