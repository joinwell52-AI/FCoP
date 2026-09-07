"""Failure taxonomy, artifact/context facts and the distinct control plane."""

import json
import sys
import tarfile
import zipfile

import pytest
import yaml

from .conftest import (
    ALLOWLIST,
    ERRORS,
    EXCLUDED_RC,
    HOSTS,
    INPUT_HEAD,
    MODULES,
    SEQUENTIAL,
    WP4C_2_ACCEPTED_HEAD,
    WP4C_2_INPUT_HEAD,
    Scenario,
    field,
    git,
    historical_delivery_paths,
    input_blob,
    sha,
    snapshot,
)
from .driver import RuleDistributionConformanceDriver


@pytest.mark.parametrize("code", ERRORS)
def test_dist_25(case, code):
    """DIST-25; RD-22; Owner: WP4C.3. Arrange eight distinct faults; Act real operations; Assert structured namespace/effects."""
    action, request = "validate", case.request()
    if code == "RULE_MANIFEST_INVALID":
        case.manifest["manifest_schema"] = "invalid"
        case.flush()
    elif code == "RULE_ARTIFACT_MISMATCH":
        case.put(case.package / "workspace.en.md", b"not the pinned artifact\n")
    elif code == "RULE_SELECTION_INVALID":
        action, request = "select", case.request(selected_modules=["missing"])
    elif code == "RULE_HOST_UNAVAILABLE":
        case.profile["host_id"] = "unknown"
        case.flush()
        action = "inspect_profile"
    elif code == "RULE_PROJECTION_LIMIT":
        raw = b"non-normative oversized fixture " * 3000 + b"\n"
        case.put(case.package / "workspace.en.md", raw)
        case.manifest["artifacts"][0].update(sha256=sha(raw), size_bytes=len(raw))
        case.flush()
        action = "plan"
    elif code == "RULE_OWNERSHIP_CONFLICT":
        case.put(case.root / "AGENTS.md", b"secret-fixture-token: user owned\n")
        action = "plan"
    elif code == "RULE_ADOPTION_REQUIRED":
        action, request = "apply", case.request(adoption_receipt_ref=None, admin_selection_ref=None)
    else:
        action, request = (
            "rollback",
            case.request(
                deployment_receipt_ref={
                    "path": "fcop/internal/rule-distribution/deployments/missing.json",
                    "sha256": "0" * 64,
                }
            ),
        )
    case.reject(action, code, request)
    assert code not in {"AUTHORIZATION_INVALID", "RECOVERY_REQUIRED", "INVALID_ENVELOPE"}


def test_dist_26(case):
    """DIST-26; RD-23; Owner: WP4C.5. Arrange cached/deployed old bytes; Act disk upgrade/query; Assert layer separation."""
    deployment, receipt = case.deploy()
    old_host = (case.root / "AGENTS.md").read_bytes()
    old_hash = sha((case.package / "manifest.json").read_bytes())
    first = case.invoke(
        "inspect_layers", case.request(deployment_receipt_ref=deployment), readonly=True
    )
    assert field(first, "disk_manifest_sha256") == old_hash
    assert field(first, "index_manifest_sha256") == old_hash
    case.manifest["package_version"] = "4.0.0-fixture.2"
    case.flush()
    new_hash = sha((case.package / "manifest.json").read_bytes())
    second = case.invoke(
        "inspect_layers", case.request(deployment_receipt_ref=deployment), readonly=True
    )
    assert field(second, "disk_manifest_sha256") == new_hash != old_hash
    assert field(second, "index_manifest_sha256") in {old_hash, new_hash}
    assert field(second, "index_invalidation_evidence") is not None
    assert field(second, "adopted_manifest_sha256") == receipt["manifest_sha256"] == old_hash
    assert field(second, "host_entry_sha256") == sha(old_host)
    assert field(second, "runtime_consumption_verified") is None
    assert (case.root / "AGENTS.md").read_bytes() == old_host
    restarted = RuleDistributionConformanceDriver(case.root).invoke(
        "inspect_layers", case.request(deployment_receipt_ref=deployment)
    )
    assert field(restarted, "disk_manifest_sha256") == new_hash
    assert field(restarted, "host_entry_sha256") == sha(old_host)
    assert field(restarted, "runtime_consumption_verified") is None


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
def test_dist_27(case, kind):
    """DIST-27; RD-23; Owner: WP4C.6. Arrange offline artifact request; Act build; Assert actual archive raw-byte parity."""
    result = case.invoke(
        "build_artifacts",
        case.request(
            output_directory=str(case.sandbox / "build-output"),
            formats=[kind],
            offline=True,
            build_isolation=False,
        ),
    )
    archive = field(result, "artifacts")[kind]
    from pathlib import Path

    archive = Path(archive)
    assert archive.resolve().is_relative_to(case.sandbox.resolve())
    assert archive.is_file()
    if kind == "wheel":
        with zipfile.ZipFile(archive) as package:
            members = {n: package.read(n) for n in package.namelist() if not n.endswith("/")}
    else:
        with tarfile.open(archive) as package:
            members = {
                m.name: package.extractfile(m).read() for m in package.getmembers() if m.isfile()
            }
    prefix = "fcop/rules/_data/v4/"
    entries = {name.split(prefix, 1)[1]: raw for name, raw in members.items() if prefix in name}
    expected = {p.name: p.read_bytes() for p in case.package.iterdir() if p.is_file()}
    assert set(entries) == set(expected)
    assert len(entries) == 19
    for name, raw in expected.items():
        assert entries[name] == raw
        assert sha(entries[name]) == sha(raw)
        assert b"\r" not in entries[name]
    assert all(sha(raw) != EXCLUDED_RC for raw in members.values())
    assert not any(n.endswith(("/AGENTS.md", "/CLAUDE.md", "/fcop-v4.mdc")) for n in members)
    assert not any(
        "rule-distribution/adoptions/" in n or "rule-distribution/deployments/" in n
        for n in members
    )


@pytest.mark.parametrize("assembly", ["sequential", "parallel"])
@pytest.mark.parametrize("host", list(HOSTS))
@pytest.mark.parametrize("languages", [["en"], ["zh"], ["en", "zh"]])
def test_dist_28(case, assembly, host, languages):
    """DIST-28; RD-23; Owner: WP4C.6. Arrange byte/context inputs; Act measure; Assert exact bytes/disclosed estimates."""
    c = Scenario(case.sandbox / "measurement", case.node, host)
    c.profile["languages"] = languages
    if len(languages) == 2:
        c.profile["profile_version"] = "explicit-bilingual-fixture.1"
    c.flush()
    modules = MODULES if assembly == "parallel" else SEQUENTIAL
    historical = []
    for n in range(6):
        raw = (f"Historical surface {n}.\n" * (n + 1)).encode()
        path = c.sandbox / f"inputs/historical-{n}.md"
        c.put(path, raw)
        historical.append({"path": str(path), "sha256": sha(raw)})
    result = c.invoke(
        "measure_context",
        c.request(
            assembly_id=assembly,
            selected_modules=modules,
            selected_languages=languages,
            historical_surfaces=historical,
        ),
        readonly=True,
    )
    expected = c.expected_embed(modules, languages)
    assert field(result, "projection_size_bytes") == len(expected)
    assert field(result, "selected_modules") == modules
    assert field(result, "selected_languages") == languages
    estimator = field(result, "estimator")
    assert field(estimator, "algorithm") and field(estimator, "version")
    assert field(result, "limit_unit") == "utf8_bytes"
    assert field(result, "runtime_consumption_verified") is None
    measures = field(result, "historical_surfaces")
    assert len(measures) == 6
    from pathlib import Path

    assert [field(m, "size_bytes") for m in measures] == [
        len(Path(h["path"]).read_bytes()) for h in historical
    ]


def test_dist_29(case):
    """DIST-29; RD-23; Owner: WP4C.5. Arrange synthetic downstream; Act unauthorized shadow; Assert zero access/write/upgrade."""
    sentinel = case.sandbox / "synthetic-downstream-never-real-product"
    case.put(sentinel / "pin.txt", b"product-owned-version-pin\n")
    events = []
    active = [False]

    def audit(event, args):
        if (
            active[0]
            and any(str(sentinel) in str(a) for a in args)
            and event
            in {
                "open",
                "os.listdir",
                "os.scandir",
                "os.remove",
                "os.rename",
                "os.mkdir",
            }
        ):
            events.append((event, str(args)))

    sys.addaudithook(audit)
    before = snapshot(case.sandbox)
    active[0] = True
    try:
        with pytest.raises(Exception) as caught:
            RuleDistributionConformanceDriver(case.root).invoke(
                "shadow",
                case.request(
                    downstream_path=str(sentinel), shadow_authorization_ref=None, deploy=False
                ),
            )
    finally:
        active[0] = False
        after = snapshot(case.sandbox)
        assert after == before
        assert events == [], "Even a read of downstream requires separate authorization"
        case.node.user_properties.append(
            (
                "operation_evidence",
                json.dumps(
                    {
                        "action": "shadow",
                        "public_entry": "fcop.Project.rule_distribution",
                        "changed_paths": [],
                        "zero_write_verified": after == before,
                        "downstream_accesses": events,
                    }
                ),
            )
        )
    from .conftest import structured_code

    assert structured_code(caught.value) == "toolkit:RULE_ADOPTION_REQUIRED"
    assert (sentinel / "pin.txt").read_bytes() == b"product-owned-version-pin\n"


def test_dist_30(request):
    """DIST-30; RD-24; Owner: WP4C.2. Arrange fixed repository facts; Act control audit; Assert zero stage advance."""
    gate_path = "reviews/fcop-4.0/gates/WP4C-1-RULE-DISTRIBUTION-CONTRACT-FROZEN.md"
    book_path = "taskbooks/fcop-4.0/WP4C.2a/01-DIST-30-Control-Plane-Boundary-Correction-Taskbook-v1.0.zh.md"
    old_path = "taskbooks/fcop-4.0/WP4C.2/01-Distribution-Conformance-First-and-Red-Baseline-Taskbook-v1.0.zh.md"
    manifest_path = "reviews/fcop-4.0/wp4c.1/MANIFEST.md"
    before = {p: input_blob(p) for p in [gate_path, book_path, old_path, manifest_path]}
    gate = yaml.safe_load(before[gate_path].decode().split("---", 2)[1])
    book = yaml.safe_load(before[book_path].decode().split("---", 2)[1])
    old = yaml.safe_load(before[old_path].decode().split("---", 2)[1])
    assert gate["status"] == "SIGNED" and gate["authority"] == "ADMIN"
    assert gate["gate"] == "WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN"
    assert gate["accepted_review_head"] == "f6831de12991010f22672fb6e776ce85ef1507ff"
    assert book["authorized_scope"] == "WP4C_2A_ONLY" and book["resumes_stage"] == "WP4C.2"
    assert book["requested_gate"] == "WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED"
    assert gate["wp4c_2_authorized"] is False
    for facts in [gate, book, old]:
        assert facts["implementation_authorized"] is False
        assert facts["main_merge_authorized"] is False
        assert facts["release_authorized"] is False
    assert old["authorized_scope"] == "WP4C_2_ONLY"
    assert "WP4C_3_STARTED: false" in before[book_path].decode()
    assert "完成后强制停止" in before[book_path].decode()
    paths = (
        git(
            "ls-tree",
            "-r",
            "--name-only",
            INPUT_HEAD,
            "reviews/fcop-4.0/gates",
            "taskbooks/fcop-4.0",
        )
        .decode()
        .splitlines()
    )
    for path in paths:
        data = input_blob(path).decode("utf-8")
        if data.startswith("---"):
            facts = yaml.safe_load(data.split("---", 2)[1])
            assert not (
                facts.get("gate") == "WP4C_2_DISTRIBUTION_CONFORMANCE_ACCEPTED"
                and facts.get("status") == "SIGNED"
            )
            assert not (
                facts.get("authorized_scope") == "WP4C_3_ONLY"
                and facts.get("execution_authorized") is True
            )
    assert historical_delivery_paths() == ALLOWLIST
    assert not git(
        "rev-list", "--merges", f"{WP4C_2_INPUT_HEAD}..{WP4C_2_ACCEPTED_HEAD}"
    ).strip()
    # Signed/frozen, test authorization, implementation, merge and release are
    # independently observed fields, not inferred from one signed Gate.
    assert book["conformance_implementation_authorized"] is True
    assert before == {p: input_blob(p) for p in before}
    request.node.user_properties.append(
        (
            "operation_evidence",
            json.dumps(
                {
                    "action": "repository-control-audit",
                    "classification": "CONTROL_PLANE_PASS",
                    "public_entry": "NOT_APPLICABLE_CONTROL_PLANE",
                    "structured_error": "NOT_APPLICABLE",
                    "changed_paths": [],
                    "zero_write_verified": True,
                    "effects_observed": "ZERO_STAGE_ADVANCE",
                    "future_owner": "NONE_CLOSED_BY_WP4C_2",
                }
            ),
        )
    )
