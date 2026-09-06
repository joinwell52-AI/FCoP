"""Two real filesystem-only applications. Demo Profile is NOT identity security.

Run: python application.py sequential (or family). Work is always temporary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fcop import Project

PROFILE = "profile:offline-example"


def evaluator(*, profile_ref, issuer, proof):
    # Deliberately educational, not a production issuer-verification system.
    return "AUTHORIZED" if (profile_ref, issuer, proof) == (PROFILE, "ME", "demo-only") else "DENIED"


def open_project(root):
    return Project(root, trusted_profiles={PROFILE: evaluator})


class Application:
    def __init__(self, root):
        self.root = Path(root)
        self.project = open_project(self.root)
        manifest = self.project.create_workspace(
            protocol_version="4.0", encoding="fcop-filesystem/4.0", profiles=[PROFILE],
        )
        self.workspace_id = manifest["workspace_id"]

    def task(self, subject, branch_of=None):
        request = dict(workspace_id=self.workspace_id, operation_id=uuid4().hex,
                       sender="ME", recipient="ME", subject=subject, body="Example work")
        if branch_of is not None:
            request["branch_of"] = branch_of
        result = self.project.create_task(**request)
        self.move(result["task_id"], "inbox", "active", "claim_task")
        return result["task_id"]

    def move(self, task, source, target, tool, **evidence):
        return self.project.transition(task_id=task, from_stage=source, to_stage=target,
                                       tool=tool, actor="ME", **evidence)

    def review(self, task, kind, decision, **fields):
        return self.project.write_review(
            workspace_id=self.workspace_id, sender="ME", recipient="ME", body="Example evidence",
            subject_ref=task, review_kind=kind, decision=decision, **fields,
        )["review_id"]

    def authorization(self, task, source, target, *, kind="authorization", refs=(), family=None):
        attempt = self.project.inspect_state(task_id=task)["current_attempt_id"]
        decision = "approved" if kind == "acceptance" else "authorize"
        return self.review(
            task, kind, decision, attempt_id=attempt, references=list(refs),
            transition={"from": source, "to": target}, profile_ref=PROFILE,
            issuer_proof="demo-only", issued_at=datetime.now(timezone.utc).isoformat(),
            expires_at=None, authorization_scope="single_use",
            operation_kind="lifecycle_transition", family_digest=family,
        )

    def complete(self, task):
        attempt = self.project.inspect_state(task_id=task)["current_attempt_id"]
        report = self.project.write_report(
            workspace_id=self.workspace_id, sender="ME", recipient="ME", subject_ref=task,
            body="Completed example", attempt_id=attempt, report_kind="final", result="done",
        )["report_id"]
        self.move(task, "active", "review", "submit_task", report_ref=report)
        acceptance = self.authorization(task, "review", "done", kind="acceptance", refs=[report])
        self.move(task, "review", "done", "approve_task", report_ref=report,
                  review_ref=acceptance, authorization_ref=acceptance, profile_ref=PROFILE)
        return report

    def archive(self, task, convergence=None, family=None):
        authorization = self.authorization(task, "done", "archive", family=family)
        request = dict(authorization_ref=authorization, profile_ref=PROFILE)
        if convergence is not None:
            request.update(review_ref=convergence, family_digest=family)
        return self.move(task, "done", "archive", "archive_task", **request)


def run(root, mode):
    app = Application(root)
    task = app.task("Example " + mode)
    if mode == "family":
        branches = [app.task("Branch " + str(index), branch_of=task) for index in range(2)]
        reports = [app.complete(branch) for branch in branches]
        app.complete(task)
        family = app.project.family_digest(root_task_id=task)
        convergence = app.review(task, "convergence", "approved", family_digest=family,
                                 references=reports)
        app.archive(task, convergence, family)
    else:
        app.complete(task)
        app.archive(task)
    # A fresh interpreter, not merely a second object, reads disk authority.
    output = subprocess.check_output(
        [sys.executable, str(Path(__file__).resolve()), "inspect", str(root), task], text=True,
    )
    result = json.loads(output)
    assert result["state"] == "archive", result
    assert result["events"] == 5, result  # T1,T2,T3,T4,T7
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["sequential", "family", "inspect"])
    parser.add_argument("root", nargs="?")
    parser.add_argument("task", nargs="?")
    args = parser.parse_args()
    if args.mode == "inspect":
        fields = open_project(Path(args.root)).read_task(task_id=args.task)
        path = Path(fields["path"])
        print(json.dumps({"state": path.parent.name, "task_id": args.task,
                          "events": len(fields["transitions"]),
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))
        return
    with tempfile.TemporaryDirectory(prefix="fcop-v4-example-") as temporary:
        print(json.dumps(run(Path(temporary), args.mode)))


if __name__ == "__main__":
    main()
