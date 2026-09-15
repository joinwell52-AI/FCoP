"""FCoP 4.0.3: scripted PM/DEV/QA work handoffs, with persistent evidence.

No model or API key is used. Roles are assigned by this demo application.
This sequential example does not benchmark concurrency or grant acceptance.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from fcop import Project

INPUT = "Hello, FCoP!"


def claim(project, task_id, actor):
    project.transition(task_id=task_id, from_stage="inbox", to_stage="active",
                       tool="claim_task", actor=actor)


def deliver(project, workspace_id, task_id, sender, recipient, body):
    state = project.inspect_state(task_id=task_id)
    report = project.write_report(
        workspace_id=workspace_id, sender=sender, recipient=recipient,
        subject_ref=task_id, attempt_id=state["current_attempt_id"],
        report_kind="final", result="done", body=body,
    )
    project.transition(task_id=task_id, from_stage="active", to_stage="review",
                       tool="submit_task", actor=sender, report_ref=report["report_id"])
    return report["report_id"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.cwd(),
                        help="Parent directory; each run creates a fresh child.")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="fcop-team-", dir=args.output)).resolve()
    pm = Project(root)
    workspace_id = pm.create_workspace(protocol_version="4.0")["workspace_id"]

    def task(operation, sender, recipient, subject, body, parent=None):
        request = dict(workspace_id=workspace_id, operation_id=operation,
                       sender=sender, recipient=recipient, subject=subject, body=body)
        if parent:
            request["parent"] = parent
        return pm.create_task(**request)["task_id"]

    goal = task("admin-goal", "ADMIN", "PM", "Deliver a checked uppercase result",
                "Organize the work and return a summary with the team evidence.")
    claim(pm, goal, "PM")
    dev_task = task("pm-dev", "PM", "DEV", "Uppercase the supplied text",
                    json.dumps({"input": INPUT}), goal)
    print("1/4 ADMIN -> PM: goal recorded; PM -> DEV: TASK assigned.")

    # A separate client reads the assignment from disk, including its recipient.
    dev = Project(root)
    assignment = dev.read_task(task_id=dev_task)
    if assignment["recipient"] != "DEV":
        raise RuntimeError("This TASK is not addressed to DEV")
    claim(dev, dev_task, "DEV")
    assignment = dev.read_task(task_id=dev_task)
    payload = json.loads(Path(assignment["path"]).read_text(encoding="utf-8").split("\n---\n", 1)[1])
    dev_report = deliver(dev, workspace_id, dev_task, "DEV", "PM",
                                    json.dumps({"input": payload["input"],
                                                "output": payload["input"].upper()}))
    print("2/4 DEV -> PM: REPORT submitted; task is pending review.")

    qa_task = task("pm-qa", "PM", "QA", "Check DEV's result",
                   json.dumps({"report_id": dev_report, "expected": INPUT.upper()}), goal)
    qa = Project(root)
    assignment = qa.read_task(task_id=qa_task)
    if assignment["recipient"] != "QA":
        raise RuntimeError("This TASK is not addressed to QA")
    claim(qa, qa_task, "QA")
    assignment = qa.read_task(task_id=qa_task)
    request = json.loads(Path(assignment["path"]).read_text(encoding="utf-8").split("\n---\n", 1)[1])
    delivered = json.loads(qa.read_report(request["report_id"])["content"].split("\n---\n", 1)[1])
    if delivered["output"] != request["expected"]:
        raise RuntimeError("QA found a mismatched result")
    assessment = qa.write_review(
        workspace_id=workspace_id, sender="QA", recipient="PM",
        subject_ref=dev_task, review_kind="assessment", decision="pass",
        references=[dev_report], body="Checked the actual output against the expected uppercase text.",
    )
    qa_report = deliver(
        qa, workspace_id, qa_task, "QA", "PM",
        json.dumps({"checked_report": dev_report, "review_id": assessment["review_id"],
                    "check": "pass"}),
    )
    print("3/4 PM -> QA: TASK assigned; QA -> PM: assessment and REPORT recorded.")

    # PM reads both reports before writing its summary for ADMIN.
    pm = Project(root)
    reports = [pm.read_report(report_id) for report_id in (dev_report, qa_report)]
    for report in reports:
        if report["recipient"] != "PM":
            raise RuntimeError("Expected a report addressed to PM")
    dev_result, qa_result = [
        json.loads(report["content"].split("\n---\n", 1)[1]) for report in reports
    ]
    if qa_result["checked_report"] != dev_report or qa_result["check"] != "pass":
        raise RuntimeError("QA evidence does not support this delivery")
    summary = deliver(pm, workspace_id, goal, "PM", "ADMIN",
                      json.dumps({"output": dev_result["output"], "team_reports": [dev_report, qa_report],
                                  "assessment": qa_result["review_id"],
                                  "acceptance": "pending"}))
    stages = [Project(root).inspect_state(task_id=t)["stage"] for t in (goal, dev_task, qa_task)]
    if stages != ["review", "review", "review"]:
        raise RuntimeError(f"Unexpected final stages: {stages}")
    print("4/4 PM -> ADMIN: summary REPORT recorded; formal acceptance remains pending.")
    print("Workspace:", root)
    print("Summary:", root / "fcop" / "reports" / (summary + ".md"))
    print("Evidence: 3 TASKs, 3 REPORTs, 1 assessment REVIEW. No task was deleted.")


if __name__ == "__main__":
    main()
