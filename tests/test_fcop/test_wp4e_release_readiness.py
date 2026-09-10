"""WP4E documentation and fail-closed release verification, never publication."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_wp4e_readme_commands_parameters_and_links_match():
    en, zh = [(ROOT / n).read_text(encoding="utf-8") for n in ("README.md", "README.zh.md")]
    assert re.findall(r"```.*?```", en, re.S) == re.findall(r"```.*?```", zh, re.S)
    assert re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", en) == re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", zh)
    for text in (en, zh):
        for token in ("Latest stable: 3.2.5", "Release candidate: 4.0.0rc1",
                      "46 tools / 12 resources / 4 resource templates", "reopen_task", "family_digest",
                      "operation_id", "bounded_embed", "FCOP_4_RC_RELEASE_READY"):
            assert token in text
        for link in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
            if not link.startswith("https://"):
                assert (ROOT / link.split("#", 1)[0]).exists(), link


def test_wp4e_readme_python_example_executes():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    code, = re.findall(r"```python\n(.*?)```", text, re.S)
    exec(compile(code, "README.md Python example", "exec"), {})


def fixtures(tmp_path):
    guard = load_script("wp4e_release_guard")
    head, content = "a" * 40, "b" * 40
    rows = []
    for name in sorted(guard.NAMES):
        raw = ("unit-test-only-not-a-release:" + name).encode()
        (tmp_path / name).write_bytes(raw)
        rows.append(dict(filename=name, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                         version="4.0.0rc1"))
    manifest = dict(repository=guard.REPOSITORY, schema="wp4e-candidates/v1", execution_head=head,
                    commit=content, raw_reproducibility="4/4", files=rows, run_id="123")
    raw = json.dumps(manifest).encode()
    (tmp_path / "candidate-manifest.json").write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    gate = dict(gate="FCOP_4_RC_RELEASE_READY", status="SIGNED", repository=guard.REPOSITORY,
                accepted_head=head, candidate_content=content, candidate_manifest_sha256=digest,
                version=guard.TARGET, tag="v4.0.0rc1", artifacts={r["filename"]: r["sha256"] for r in rows},
                phase_b_authorized=True, tag_authorized=True, pypi_publish_authorized=True,
                github_release_authorized=True, stable_release_authorized=False, artifact_run_id="123",
                independent_reviewer_required=False, environment_prevent_self_review=False,
                environment_self_approval_authorized=True)
    comment = dict(user=dict(login=guard.OWNER), author_association="OWNER",
                   issue_url="https://api.github.com/repos/" + guard.REPOSITORY + "/issues/1",
                   body="TEST FIXTURE ONLY\n```json\n" + json.dumps(gate) + "\n```")
    environment = dict(name="fcop-pypi", protection_rules=[dict(type="required_reviewers",
        reviewers=[{"type": "User", "reviewer": {"login": guard.OWNER}}], prevent_self_review=False)],
        deployment_branch_policy=dict(protected_branches=False, custom_branch_policies=True))
    run = dict(head_sha=head, status="completed", conclusion="success", id=123,
               path=".github/workflows/rc-candidate.yml", repository=dict(full_name=guard.REPOSITORY))
    return guard, manifest, digest, gate, comment, environment, run


def test_wp4e_real_hash_validation_and_explicit_gate_fixture(tmp_path):
    guard, manifest, digest, _, comment, environment, run = fixtures(tmp_path)
    assert guard.validate_artifacts(tmp_path, digest, "a" * 40, "b" * 40) == manifest
    assert guard.validate_publication(comment, environment, run, manifest, digest, "v4.0.0rc1")


@pytest.mark.parametrize("field", ["phase_b_authorized", "tag_authorized", "pypi_publish_authorized",
                                  "github_release_authorized", "accepted_head", "candidate_content",
                                  "candidate_manifest_sha256", "version", "artifacts", "artifact_run_id",
                                  "gate", "status", "repository", "tag", "stable_release_authorized"])
def test_wp4e_gate_rejects_incomplete_or_wrong_authority(tmp_path, field):
    guard, manifest, digest, gate, comment, environment, run = fixtures(tmp_path)
    gate[field] = "NOT_AUTHORIZED_OR_WRONG_IDENTITY"
    comment["body"] = "```json\n" + json.dumps(gate) + "\n```"
    with pytest.raises(AssertionError):
        guard.validate_publication(comment, environment, run, manifest, digest, "v4.0.0rc1")


@pytest.mark.parametrize("case", ["actor", "association", "no-reviewer", "self-review", "branch-policy",
                                 "run-head", "run-failed", "run-path", "extra-block", "rc-gate-only"])
def test_wp4e_rejects_untrusted_context(tmp_path, case):
    guard, manifest, digest, _, comment, environment, run = fixtures(tmp_path)
    if case == "actor":
        comment["user"]["login"] = "caller"
    elif case == "association":
        comment["author_association"] = "CONTRIBUTOR"
    elif case == "no-reviewer":
        environment["protection_rules"] = []
    elif case == "self-review":
        environment["protection_rules"][0]["prevent_self_review"] = True
    elif case == "branch-policy":
        environment["deployment_branch_policy"] = None
    elif case == "run-head":
        run["head_sha"] = "c" * 40
    elif case == "run-failed":
        run["conclusion"] = "failure"
    elif case == "run-path":
        run["path"] = "some-other-workflow.yml"
    elif case == "extra-block":
        comment["body"] += '\n```json\n{}\n```'
    else:
        comment["body"] = comment["body"].replace("FCOP_4_RC_RELEASE_READY", "FCOP_4_RC_ACCEPTED")
    with pytest.raises(AssertionError):
        guard.validate_publication(comment, environment, run, manifest, digest, "v4.0.0rc1")


def test_wp4e_explicit_same_account_admin_review_is_accepted(tmp_path):
    guard, manifest, digest, gate, comment, environment, run = fixtures(tmp_path)
    reviewer = environment["protection_rules"][0]["reviewers"][0]
    assert reviewer["reviewer"]["login"] == comment["user"]["login"] == "joinwell52-AI"
    assert environment["protection_rules"][0]["prevent_self_review"] is False
    assert guard.validate_publication(comment, environment, run, manifest, digest, "v4.0.0rc1") == gate


@pytest.mark.parametrize("field", ["independent_reviewer_required", "environment_prevent_self_review",
                                  "environment_self_approval_authorized"])
@pytest.mark.parametrize("case", ["missing", "opposite", "string", "integer"])
def test_wp4e_same_account_policy_requires_explicit_gate(tmp_path, field, case):
    guard, manifest, digest, gate, comment, environment, run = fixtures(tmp_path)
    if case == "missing":
        del gate[field]
    elif case == "opposite":
        gate[field] = not gate[field]
    elif case == "string":
        gate[field] = str(gate[field]).lower()
    else:
        gate[field] = int(gate[field])
    comment["body"] = "```json\n" + json.dumps(gate) + "\n```"
    with pytest.raises(AssertionError):
        guard.validate_publication(comment, environment, run, manifest, digest, "v4.0.0rc1")


@pytest.mark.parametrize("case", ["wrong-reviewer", "team", "empty-reviewers", "missing-reviewers",
                                 "missing-policy", "string-policy", "integer-policy", "split-rules"])
def test_wp4e_environment_requires_admin_and_exact_same_account_policy(tmp_path, case):
    guard, manifest, digest, _, comment, environment, run = fixtures(tmp_path)
    rule = environment["protection_rules"][0]
    if case == "wrong-reviewer":
        rule["reviewers"][0]["reviewer"]["login"] = "another-user"
    elif case == "team":
        rule["reviewers"][0]["type"] = "Team"
    elif case == "empty-reviewers":
        rule["reviewers"] = []
    elif case == "missing-reviewers":
        del rule["reviewers"]
    elif case == "missing-policy":
        del rule["prevent_self_review"]
    elif case == "string-policy":
        rule["prevent_self_review"] = "false"
    elif case == "integer-policy":
        rule["prevent_self_review"] = 0
    else:
        other_rule = copy.deepcopy(rule)
        other_rule["reviewers"][0]["reviewer"]["login"] = "another-user"
        rule["prevent_self_review"] = True
        environment["protection_rules"].append(other_rule)
    with pytest.raises(AssertionError):
        guard.validate_publication(comment, environment, run, manifest, digest, "v4.0.0rc1")


def test_wp4e_modified_artifact_and_extra_file_rejected(tmp_path):
    guard, _, digest, *_ = fixtures(tmp_path)
    extra = tmp_path / "extra.whl"
    extra.write_bytes(b"unexpected")
    with pytest.raises(AssertionError):
        guard.validate_artifacts(tmp_path, digest, "a" * 40, "b" * 40)
    extra.unlink()
    (tmp_path / sorted(guard.NAMES)[0]).write_bytes(b"tampered")
    with pytest.raises(AssertionError):
        guard.validate_artifacts(tmp_path, digest, "a" * 40, "b" * 40)


def test_wp4e_artifact_member_attribution_rejects_production_change():
    delta = load_script("wp4e_artifact_delta")
    old = {"README.md": b"old", "src/fcop/project.py": b"real implementation"}
    new = {**old, "README.md": b"authorized docs"}
    assert delta.compare(old, new) == ["README.md"]
    changed = copy.deepcopy(new)
    changed["src/fcop/project.py"] = b"modified implementation"
    with pytest.raises(AssertionError):
        delta.compare(old, changed)


def test_wp4e_metadata_description_retains_utf8_bytes():
    delta = load_script("wp4e_artifact_delta")
    header = b"Metadata-Version: 2.5\nName: fcop-mcp\nVersion: 4.0.0rc1\n\n"
    expected = (ROOT / "mcp/README.md").read_text(encoding="utf-8").encode("utf-8")
    name = "fcop_mcp-4.0.0rc1.dist-info/METADATA"
    assert delta.compare({name: header + b"old"}, {name: header + expected}) == [name]
    with pytest.raises(AssertionError):
        delta.compare({name: header + b"old"}, {name: header + b"wrong description"})


@pytest.mark.parametrize("case", ["complete", "missing-workflow", "pending", "failed", "skipped", "missing-pr-only"])
def test_wp4e_final_head_ci_must_include_pr_only_checks(case):
    guard = load_script("wp4e_release_guard")
    paths = ["test-fcop.yml", "test-fcop-mcp.yml", "rc-candidate.yml"]
    names = ["Stability charter (API surface + CHANGELOG)", "Tool contract (snapshot + CHANGELOG)", "consumer"]
    runs = [dict(id=i, path=".github/workflows/" + path, status="completed", conclusion="success")
            for i, path in enumerate(paths)]
    jobs = {str(i): [dict(name=names[i], status="completed", conclusion="success")] for i in range(3)}
    if case == "complete":
        guard.validate_ci(runs, jobs)
        return
    if case == "missing-workflow":
        runs.pop()
    elif case == "pending":
        runs[0]["status"] = "in_progress"
    elif case == "failed":
        runs[0]["conclusion"] = "failure"
    elif case == "skipped":
        jobs["0"][0]["conclusion"] = "skipped"
    else:
        jobs["0"][0]["name"] = "not-the-required-pr-gate"
    with pytest.raises(AssertionError):
        guard.validate_ci(runs, jobs)


@pytest.mark.parametrize(("changed", "evidence"), [
    ("reports/FCOP-4.0-WP4E-RESULT.md", True), ("reviews/fcop-4.0/wp4e/MANIFEST.md", True),
    ("README.md", False), ("scripts/wp4e_release_guard.py", False),
    ("reports/FCOP-4.0-WP4D-RESULT.md", False),
])
def test_wp4e_content_identity_cannot_hide_docs_or_old_stage(tmp_path, changed, evidence):
    module = load_script("wp4d_candidate_ref")

    def git(*args):
        return subprocess.check_output(["git", "-C", str(tmp_path), "-c", "user.name=WP4E test",
            "-c", "user.email=wp4e@example.invalid", "-c", "core.autocrlf=false", *args], text=True).strip()

    git("init", "-q")
    for name in ("initial", "content"):
        (tmp_path / name).write_text(name, encoding="utf-8")
        git("add", name)
        git("commit", "-qm", name)
    content = git("rev-parse", "HEAD")
    path = tmp_path / changed
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("next", encoding="utf-8")
    git("add", changed)
    git("commit", "-qm", "next")
    assert module.candidate_ref(tmp_path, stage="WP4E") == (content if evidence else git("rev-parse", "HEAD"))
