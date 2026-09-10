"""Observable Host bytes, ownership, short commit races and partial failure."""

import re

import pytest

from .conftest import (
    BEGIN,
    END,
    HOSTS,
    SEQUENTIAL,
    Scenario,
    concurrent_apply,
    field,
    json_bytes,
    sha,
    snapshot,
    structured_code,
)


@pytest.mark.parametrize("host", list(HOSTS))
@pytest.mark.parametrize("occupied", [False, True])
def test_dist_13(case, host, occupied):
    """DIST-13; RD-12/13; Owner: WP4C.4. Arrange new/unowned entry; Act apply; Assert exact ownership isolation."""
    c = Scenario(case.sandbox / host, case.node, host)
    adoption = c.adopt()
    target = c.root / HOSTS[host]
    if occupied:
        c.put(target, b"Product-owned legacy instructions.\n")
        if host == "cursor":
            c.put(c.root / ".cursor/rules/fcop-rules.mdc", b"Active legacy FCoP.\n")
        c.reject("apply", "RULE_OWNERSHIP_CONFLICT", c.request(adoption_receipt_ref=adoption))
        assert target.read_bytes() == b"Product-owned legacy instructions.\n"
    else:
        c.deploy(adoption)
        assert target.read_bytes() == c.expected_embed()
        assert all(
            not (c.root / other).exists() for other in HOSTS.values() if other != HOSTS[host]
        )


def test_dist_14(case):
    """DIST-14; RD-13; Owner: WP4C.4. Arrange different roots/times; Act plan; Assert byte identity and zero effects."""
    other = Scenario(case.sandbox / "different-absolute-location", case.node)
    first = case.invoke(
        "plan", case.request(recorded_at="2026-01-01T00:00:00+00:00"), readonly=True
    )
    second = other.invoke(
        "plan", other.request(recorded_at="2030-01-01T00:00:00+00:00"), readonly=True
    )
    a, b = field(first, "targets")[0], field(second, "targets")[0]
    assert field(a, "after_bytes") == field(b, "after_bytes") == case.expected_embed()
    assert field(a, "after_sha256") == field(b, "after_sha256") == sha(case.expected_embed())
    assert str(case.root).encode() not in field(a, "after_bytes")
    assert b"2030-01-01" not in field(b, "after_bytes")


@pytest.mark.parametrize(
    "variant", ["preserve", "nested", "duplicate", "missing", "oversized-user-region"]
)
def test_dist_15(case, variant):
    """DIST-15; RD-13; Owner: WP4C.4. Arrange owned block/user bytes; Act update; Assert precise region effects."""
    ref, receipt = case.deploy()
    target = case.root / "AGENTS.md"
    prefix, suffix = b"USER PREFIX\n", b"USER SUFFIX\n"
    managed = target.read_bytes()
    raw = prefix + managed + suffix
    if variant == "nested":
        raw = prefix + BEGIN + managed + END + suffix
    elif variant == "duplicate":
        raw = prefix + managed + managed + suffix
    elif variant == "missing":
        raw = raw.replace(END, b"")
    elif variant == "oversized-user-region":
        raw = b"U" * 65536 + b"\n" + managed + suffix
    case.put(target, raw)
    request = case.request(
        adoption_receipt_ref=receipt["adoption_receipt_ref"], previous_deployment_ref=ref
    )
    if variant in {"nested", "duplicate", "missing"}:
        case.reject("apply", "RULE_OWNERSHIP_CONFLICT", request)
    elif variant == "oversized-user-region":
        case.reject("apply", "RULE_PROJECTION_LIMIT", request)
    else:
        plan = case.invoke("plan", request, readonly=True)
        t = field(plan, "targets")[0]
        assert field(t, "after_bytes") == raw
        assert field(t, "size_bytes") == len(raw)
        case.invoke("apply", {**request, "plan": plan})
        assert target.read_bytes().startswith(prefix)
        assert target.read_bytes().endswith(suffix)
        assert target.read_bytes() == raw
        assert sha((case.root / ref["path"]).read_bytes()) == ref["sha256"]


@pytest.mark.parametrize(
    "variant", ["reference", "stale-snapshot", "missing-snapshot", "escaping-reference"]
)
def test_dist_16(case, variant):
    """DIST-16; RD-14; Owner: WP4C.4. Arrange proven local references; Act deploy/verify; Assert resolution and no fetch."""
    case.profile.update(
        profile_version="reference-fixture.1",
        projection_mode="reference",
        reference_mode="relative-path",
        max_projection_bytes=8192,
    )
    case.flush()
    support = {
        "host_id": "codex",
        "profile_sha256": sha(json_bytes(case.profile)),
        "resolution": "PASS",
        "order": "PASS",
        "integrity": "PASS",
        "failure": "PASS",
        "evidence_kind": "isolated-static-fixture",
        "runtime_consumption_verified": None,
    }
    case.put(case.sandbox / "inputs/reference-support.json", json_bytes(support))
    adoption = case.invoke(
        "adopt",
        case.request(
            reference_support_ref={
                "path": str(case.sandbox / "inputs/reference-support.json"),
                "sha256": sha(json_bytes(support)),
            }
        ),
    )
    ref = field(adoption, "adoption_receipt_ref")
    deployed, receipt = case.deploy(ref)
    raw = (case.root / "AGENTS.md").read_bytes()
    links = re.findall(rb"- \[([^]]+)\]\(([^)]+)\) sha256=([a-f0-9]{64})\n", raw)
    assert [label.decode() for label, _, _ in links] == [f"{m}:en" for m in SEQUENTIAL]
    package_snapshot = (
        case.root
        / "fcop/internal/rule-distribution/packages"
        / sha((case.package / "manifest.json").read_bytes())
    )
    assert (package_snapshot / "manifest.json").read_bytes() == (
        case.package / "manifest.json"
    ).read_bytes()
    assert len(list(package_snapshot.glob("*.md"))) == 18
    for label, path, digest in links:
        assert b"\\" not in path and b"://" not in path
        resolved = (case.root / path.decode()).resolve()
        assert resolved.is_relative_to(case.root.resolve())
        assert sha(resolved.read_bytes()).encode() == digest
        assert (
            resolved.read_bytes()
            == (case.package / (label.decode().replace(":", ".") + ".md")).read_bytes()
        )
    if variant == "stale-snapshot":
        case.put(package_snapshot / "workspace.en.md", b"stale\n")
    elif variant == "missing-snapshot":
        (package_snapshot / "workspace.en.md").unlink()
    elif variant == "escaping-reference":
        case.put(case.root / "AGENTS.md", raw.replace(links[0][1], b"../../outside.md"))
    request = case.request(deployment_receipt_ref=deployed)
    if variant != "reference":
        case.reject(
            "verify_deployment",
            "RULE_OWNERSHIP_CONFLICT"
            if variant == "escaping-reference"
            else "RULE_ARTIFACT_MISMATCH",
            request,
        )
    else:
        verified = case.invoke("verify_deployment", request, readonly=True)
        assert field(verified, "verified") is True
        assert field(verified, "runtime_consumption_verified") is None
        assert receipt["targets"][0]["after_sha256"] == sha(raw)


@pytest.mark.parametrize(
    "variant", ["exact", "unadopted-multilingual", "overflow", "broken-source-link"]
)
def test_dist_17(case, variant):
    """DIST-17; RD-15; Owner: WP4C.4. Arrange bounded bytes; Act plan; Assert exact framing or zero-write failure."""
    if variant == "unadopted-multilingual":
        case.reject("plan", "RULE_SELECTION_INVALID", case.request(selected_languages=["en", "zh"]))
    elif variant in {"overflow", "broken-source-link"}:
        raw = (
            (b"X" * 66000 + b"\n")
            if variant == "overflow"
            else b"Non-normative [missing](../unresolved.md).\n"
        )
        case.put(case.package / "workspace.en.md", raw)
        case.manifest["artifacts"][0].update(sha256=sha(raw), size_bytes=len(raw))
        case.flush()
        case.reject(
            "plan", "RULE_PROJECTION_LIMIT" if variant == "overflow" else "RULE_ARTIFACT_MISMATCH"
        )
    else:
        plan = case.invoke("plan", readonly=True)
        target = field(plan, "targets")[0]
        assert field(target, "after_bytes") == case.expected_embed()
        assert field(target, "size_bytes") == len(case.expected_embed())
        assert field(target, "after_sha256") == sha(case.expected_embed())
        assert b"language=zh" not in field(target, "after_bytes")


@pytest.mark.parametrize("conflict", [False, True])
def test_dist_18(case, conflict):
    """DIST-18; RD-16; Owner: WP4C.4. Arrange recursive snapshot; Act dry-run; Assert no directories/receipts/backups."""
    if conflict:
        case.put(case.root / "AGENTS.md", b"Unowned target\n")
    before = snapshot(case.sandbox)
    if conflict:
        case.reject("plan", "RULE_OWNERSHIP_CONFLICT")
    else:
        result = case.invoke("plan", readonly=True)
        target = field(result, "targets")[0]
        assert field(result, "selected_modules") == SEQUENTIAL
        assert field(result, "manifest_sha256") == sha(
            (case.package / "manifest.json").read_bytes()
        )
        assert field(result, "host_profile_sha256") == sha(json_bytes(case.profile))
        assert field(target, "before_sha256") is None
        assert field(target, "after_sha256") == sha(case.expected_embed())
        assert field(target, "size_bytes") == len(case.expected_embed())
        assert field(target, "diff")
        assert field(result, "planned_receipt") is not None
        assert field(result, "planned_backups") == []
    assert snapshot(case.sandbox) == before


@pytest.mark.parametrize("variant", ["stale-plan", "two-processes"])
def test_dist_19(case, variant):
    """DIST-19; RD-16; Owner: WP4C.4. Arrange target race; Act real apply; Assert revalidation/no lost writes."""
    if variant == "stale-plan":
        adoption = case.adopt()
        plan = case.invoke("plan", case.request(adoption_receipt_ref=adoption), readonly=True)
        case.put(case.root / "AGENTS.md", b"user edit after plan\n")
        case.reject(
            "apply",
            "RULE_OWNERSHIP_CONFLICT",
            case.request(adoption_receipt_ref=adoption, plan=plan),
        )
        assert (case.root / "AGENTS.md").read_bytes() == b"user edit after plan\n"
    else:
        # A real overlapping apply request contains explicit ADMIN selection
        # and frozen target preconditions; production must validate/adopt before
        # committing. Both processes start apply at the same barrier, including
        # on the absent implementation baseline; this is not a surface probe.
        request = case.request(expected_target_sha256={"AGENTS.md": None}, adopt_if_authorized=True)
        results = concurrent_apply(case, [request, request.copy()])
        successes = [r for r in results if r["code"] is None]
        assert successes
        assert all(r["code"] in {None, "toolkit:RULE_OWNERSHIP_CONFLICT"} for r in results)
        assert (case.root / "AGENTS.md").read_bytes() == case.expected_embed()
        receipt_refs = [field(r["result"], "deployment_receipt_ref") for r in successes]
        receipts = [case.read_receipt(ref, "deployments") for ref in receipt_refs]
        assert all(r["targets"][0]["after_sha256"] == sha(case.expected_embed()) for r in receipts)
        if len(successes) == 2:
            assert receipt_refs[0] == receipt_refs[1], (
                "Contradictory double success for one absent-target precondition"
            )
        assert (
            len(list((case.root / "fcop/internal/rule-distribution/deployments").glob("*.json")))
            == 1
        )


@pytest.mark.parametrize(
    "window", ["before_stage_durable", "between_replacements", "before_success_receipt"]
)
def test_dist_20(case, window):
    """DIST-20; RD-16; Owner: WP4C.4. Arrange public fault window; Act apply/inspect/rollback; Assert partial evidence."""
    # The public test-only seam is explicitly requested, not monkeypatched or
    # implemented here. Its absence remains a structured red. Batch inputs
    # name separately selected static profiles, not an invented fourth Host.
    other = Scenario(case.sandbox / "claude-input", case.node, "claude-code")
    second = other.request()
    second["workspace_id"] = case.request()["workspace_id"]
    request = case.request(
        deployments=[case.request(), second],
        test_fault={"window": window, "raise_after_observation": True},
    )
    before = snapshot(case.sandbox)
    with pytest.raises(Exception) as caught:
        case.invoke("apply", request)
    assert structured_code(caught.value) == "toolkit:RULE_DEPLOYMENT_RECOVERY_REQUIRED"
    details = field(caught.value, "details")
    writes = field(details, "proven_writes")
    assert field(details, "requires_explicit_recovery") is True
    after = snapshot(case.sandbox)
    assert not list((case.root / "fcop/internal/rule-distribution/deployments").glob("*.json"))
    for rel in writes:
        p = case.root / rel
        assert p.resolve().is_relative_to(case.root.resolve())
        assert p.is_file()
    if window == "before_stage_durable":
        assert not (case.root / "AGENTS.md").exists()
        assert not (case.root / "CLAUDE.md").exists()
    elif window == "between_replacements":
        assert 0 < sum((case.root / p).exists() for p in ["AGENTS.md", "CLAUDE.md"]) < 2
        assert writes
    else:
        assert (case.root / "AGENTS.md").exists() and (case.root / "CLAUDE.md").exists()
        assert writes
    for rel, fact in before.items():
        if rel.startswith("package/") or rel.startswith("inputs/"):
            assert after[rel] == fact
    inspection = case.invoke(
        "inspect_failure", case.request(failure_ref=field(details, "failure_ref")), readonly=True
    )
    assert snapshot(case.sandbox) == after, "No background/inspection replay"
    assert set(field(inspection, "proven_writes")) == set(writes)
    result = case.invoke(
        "rollback_partial", case.request(failure_ref=field(details, "failure_ref"))
    )
    assert field(result, "restored") is True
    assert not (case.root / "AGENTS.md").exists() and not (case.root / "CLAUDE.md").exists()
    assert all(snapshot(case.sandbox).get(k) == v for k, v in before.items())
