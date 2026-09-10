"""Fail-closed publishing preflight. Verification only: never uploads or tags."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

REPOSITORY = "joinwell52-AI/FCoP"
OWNER = "joinwell52-AI"
TARGET = "4.0.0rc1"
NAMES = {"fcop-4.0.0rc1-py3-none-any.whl", "fcop-4.0.0rc1.tar.gz",
         "fcop_mcp-4.0.0rc1-py3-none-any.whl", "fcop_mcp-4.0.0rc1.tar.gz"}
ENVIRONMENT = "fcop-pypi"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", "repos/" + REPOSITORY + "/" + path]))


def validate_artifacts(directory, expected_sha, head, content):
    raw = (directory / "candidate-manifest.json").read_bytes()
    assert re.fullmatch(r"[0-9a-f]{64}", expected_sha) and sha(raw) == expected_sha
    for value in (head, content):
        assert re.fullmatch(r"[0-9a-f]{40}", value)
    manifest = json.loads(raw)
    assert manifest["repository"] == REPOSITORY and manifest["schema"] == "wp4e-candidates/v1"
    assert manifest["execution_head"] == head and manifest["commit"] == content
    assert manifest["raw_reproducibility"] == "4/4"
    rows = manifest["files"]
    assert len(rows) == 4 and {r["filename"] for r in rows} == NAMES
    assert {p.name for p in directory.iterdir()} == NAMES | {"candidate-manifest.json"}
    for row in rows:
        raw = (directory / row["filename"]).read_bytes()
        assert sha(raw) == row["sha256"] and len(raw) == row["bytes"]
        assert row["version"] == TARGET
    return manifest


def validate_publication(comment, environment, run, manifest, manifest_sha, tag):
    assert comment["user"]["login"] == OWNER and comment["author_association"] == "OWNER"
    assert comment.get("issue_url", "").startswith("https://api.github.com/repos/" + REPOSITORY + "/issues/")
    blocks = re.findall(r"```json\s*(.*?)\s*```", comment["body"], re.S)
    assert len(blocks) == 1, "Exactly one structured ADMIN release authorization required"
    gate = json.loads(blocks[0])
    assert gate["gate"] == "FCOP_4_RC_RELEASE_READY" and gate["status"] == "SIGNED"
    assert gate["repository"] == REPOSITORY
    assert gate["accepted_head"] == manifest["execution_head"]
    assert gate["candidate_content"] == manifest["commit"]
    assert gate["candidate_manifest_sha256"] == manifest_sha
    assert gate["version"] == TARGET and gate["tag"] == tag == "v" + TARGET
    assert gate["artifacts"] == {r["filename"]: r["sha256"] for r in manifest["files"]}
    for key in ("phase_b_authorized", "tag_authorized", "pypi_publish_authorized", "github_release_authorized"):
        assert gate[key] is True, key
    assert gate["stable_release_authorized"] is False
    assert environment["name"] == ENVIRONMENT
    rules = environment["protection_rules"]
    assert any(r["type"] == "required_reviewers" and r.get("reviewers")
               and r.get("prevent_self_review") is True for r in rules), "Protected independent approval required"
    policy = environment.get("deployment_branch_policy")
    assert policy and (policy.get("protected_branches") or policy.get("custom_branch_policies"))
    assert run["head_sha"] == manifest["execution_head"]
    assert run["status"] == "completed" and run["conclusion"] == "success"
    assert run["path"] == ".github/workflows/rc-candidate.yml"
    assert run["repository"]["full_name"] == REPOSITORY
    assert str(run["id"]) == str(manifest["run_id"]) == str(gate["artifact_run_id"])
    return gate


def validate_ci(runs, jobs):
    expected = {".github/workflows/test-fcop.yml", ".github/workflows/test-fcop-mcp.yml",
                ".github/workflows/rc-candidate.yml"}
    latest = {}
    for run in sorted(runs, key=lambda r: r["id"], reverse=True):
        if run["path"] in expected:
            latest.setdefault(run["path"], run)
    assert latest.keys() == expected, "All three final-head CI workflows must actually run"
    names = set()
    for run in latest.values():
        assert run["status"] == "completed" and run["conclusion"] == "success"
        rows = jobs[str(run["id"])]
        assert rows and all(j["status"] == "completed" and j["conclusion"] == "success" for j in rows)
        names.update(j["name"] for j in rows)
    assert {"Stability charter (API surface + CHANGELOG)", "Tool contract (snapshot + CHANGELOG)"} <= names


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifacts", type=Path)
    p.add_argument("--manifest-sha256", required=True)
    p.add_argument("--head", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--tag", default="v4.0.0rc1")
    p.add_argument("--mode", choices=["dry-run", "publish-preflight"], default="dry-run")
    p.add_argument("--gate-comment")
    a = p.parse_args()
    manifest = validate_artifacts(a.artifacts, a.manifest_sha256, a.head, a.content)
    assert a.tag == "v" + TARGET
    authorized = False
    if a.mode == "publish-preflight":
        assert a.gate_comment and a.gate_comment.isdigit()
        assert os.environ.get("GITHUB_REPOSITORY") == REPOSITORY
        comment = api("issues/comments/" + a.gate_comment)
        environment = api("environments/" + ENVIRONMENT)
        run = api("actions/runs/" + str(manifest["run_id"]))
        validate_publication(comment, environment, run, manifest, a.manifest_sha256, a.tag)
        runs = api("actions/runs?head_sha=" + a.head + "&per_page=100")["workflow_runs"]
        selected = [r for r in runs if r["path"] in {
            ".github/workflows/test-fcop.yml", ".github/workflows/test-fcop-mcp.yml",
            ".github/workflows/rc-candidate.yml",
        }]
        jobs = {}
        for r in selected:
            response = api("actions/runs/" + str(r["id"]) + "/jobs?per_page=100")
            assert response["total_count"] == len(response["jobs"])
            jobs[str(r["id"])] = response["jobs"]
        validate_ci(selected, jobs)
        # The tag must already exist at the accepted commit; no implicit tag creation.
        ref = api("git/ref/tags/" + a.tag)["object"]
        while ref["type"] == "tag":
            ref = api("git/tags/" + ref["sha"])["object"]
        assert ref["type"] == "commit" and ref["sha"] == a.head
        authorized = True
    result = dict(mode=a.mode, upload_authorized=authorized, tag=a.tag, version=TARGET,
                  prerelease=True, head=a.head, content=a.content,
                  manifest_sha256=a.manifest_sha256, artifact_run_id=manifest["run_id"],
                  artifacts={r["filename"]: r["sha256"] for r in manifest["files"]},
                  uploads_executed=0, releases_created=0)
    print(json.dumps(result, sort_keys=True))
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as stream:
            stream.write("authorized=" + str(authorized).lower() + "\n")


if __name__ == "__main__":
    main()
