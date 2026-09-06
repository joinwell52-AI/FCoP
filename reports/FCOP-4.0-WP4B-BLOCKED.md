# Current WP4B.2 directed baseline check — BLOCKED

```yaml
WP4B_STATUS: BLOCKED
STOP_CODE: REPORT_ZERO_HEAD_ERROR_CONTRACT_CONFLICT
AUTHORIZED_SCOPE: WP4B_RESUME_ONLY
REPORTER: ME
TASKBOOK_COMMIT: 9359de1f9268dd13c8c393ee403c8837130a0960
TASKBOOK_SHA256: a7dc53f17d676e787ffb6b89c8305bb59e3e9b54f06f28bc75d8d737a554b060
INPUT_HEAD: 1434d409925bec233d6b246ebb081bdf5bc12f08
PARENT_GATE_COMMIT: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WP4B_2_PUBLIC_QUERY_DESIGN_ACCEPTED: true
PUBLIC_QUERY_IMPLEMENTED: false
BACKUP_RESTORED: false
REQUESTED_GATE: NONE
```

## U1. The previous capability decision is resolved

WP4B.2 explicitly authorizes enabling the two existing public Project readers
and a shared internal head resolver. The previous public-query authorization
gap is resolved. This report does not request those permissions again.

The new taskbook was retrieved from the fixed GitHub contents API. Its decoded
bytes equal `git show 9359de1:<taskbook-path>` and have the exact published
SHA-256 above. The independent, clean WP4B worktree was fast-forwarded to
`9359de1f9268dd13c8c393ee403c8837130a0960`; the intervening change was solely
the new taskbook. The original `D:/FCoP` workspace was not touched.

Before restoring the unfinished adapter, the taskbook's directed zero-head
case was exercised against the unchanged accepted Core. It exposes a narrow
contradiction between preserving the baseline T3 error and the required
cycle result. There is no production edit or restored ZIP content in this
delivery; only this report changes.

## U2. Exact conflict

| Fixed source | Requirement or actual behavior |
|---|---|
| WP4B.2 section 2.1 | Extracting the shared resolver must preserve **all** T3 success/failure behavior and error codes. |
| WP4B.2 section 7.2 | A replacement cycle producing zero heads must return `REPORT_REQUIRED`. |
| WP4B.2 section 7.3 | Public queries and T3 must return the same `REPORT_REQUIRED` for the same zero-head fixture. |
| WP4B.2 section 11 | Stop if the frozen head algorithm must change to provide queries. |
| Frozen `spec/fcop-4.0-spec.md`, F4.3.4 | Zero heads returns `REPORT_REQUIRED`; multiple heads returns `REPORT_HEAD_AMBIGUOUS`. No specification edit is requested. |
| `src/fcop/v4/lifecycle.py:109–126` at `9359de1` | No candidate REPORTs return `REPORT_REQUIRED`, but after traversal **every** `len(heads) != 1`, including a nonempty cycle with zero heads, returns `REPORT_HEAD_AMBIGUOUS`. |

This is not a theoretical guess based on code text. Both cycle envelopes pass
public `inspect_state` Encoding/Schema/relation validation; public T3 then
returns the baseline `REPORT_HEAD_AMBIGUOUS`. The complete workspace file-byte
map remains unchanged by validation and the failed transition.

```text
SCHEMA_VALID_REPLACEMENT_CYCLE 2/2
BASELINE_T3_CODE REPORT_HEAD_AMBIGUOUS
TASKBOOK_7_2_AND_7_3_EXPECT REPORT_REQUIRED
ZERO_FILE_CHANGES True
```

The absent-REPORT case and the cyclic nonempty graph are different baseline
branches. Testing only an empty directory would conceal this conflict.

## U3. Reproduction on the fixed commit

Environment: Windows, CPython 3.12, repository `src` on `sys.path`. The program
uses only a fresh temporary fixture. It creates a legitimate final/replacement
chain with public writers, then introduces a cycle by corrupting the fixture's
first REPORT. It does not modify a real workspace or a production source file.

```python
import tempfile
from pathlib import Path

import yaml
from examples.v4.application import Application
from fcop.errors import V4ProtocolError

with tempfile.TemporaryDirectory(prefix="fcop-wp4b2-cycle-") as temporary:
    root = Path(temporary).resolve()
    app = Application(root)
    task = app.task("Cycle error-code baseline")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    request = dict(workspace_id=app.workspace_id, sender="ME", recipient="ME",
                   subject_ref=task, body="Test evidence", attempt_id=attempt,
                   result="done")
    first = app.project.write_report(**request, report_kind="final")
    second = app.project.write_report(**request, report_kind="replacement",
                                      references=[first["report_id"]])
    path = Path(first["path"])
    _, front, body = path.read_text(encoding="utf-8").split("---", 2)
    fields = yaml.safe_load(front)
    fields["report_kind"] = "replacement"
    fields["references"] = [second["report_id"]]
    path.write_bytes(("---\n" + yaml.safe_dump(fields, sort_keys=False,
                     allow_unicode=True) + "---" + body).encode("utf-8"))
    def files():
        return {p.relative_to(root).as_posix(): p.read_bytes()
                for p in root.rglob("*") if p.is_file()}
    before = files()
    for item in (first, second):
        checked = app.project.inspect_state(
            envelope_path=Path(item["path"]).relative_to(root).as_posix())
        assert checked["report_kind"] == "replacement"
    try:
        app.move(task, "active", "review", "submit_task",
                 report_ref=second["report_id"])
    except V4ProtocolError as error:
        assert error.code == "REPORT_HEAD_AMBIGUOUS", error.code
    else:
        raise AssertionError("Baseline unexpectedly accepted a cycle")
    assert before == files()
```

## U4. Narrow clarification needed; no second algorithm

The implementation choices cannot simultaneously satisfy all three explicit
requirements:

- Keeping the existing shared resolver unchanged preserves T3, but fails the
  mandated cycle result in sections 7.2 and 7.3.
- Mapping the code only in readers creates query-versus-T3 disagreement and a
  second interpretation; it is prohibited.
- Correcting the shared resolver's zero-head branch to `REPORT_REQUIRED`
  aligns the explicit test and frozen F4.3.4, but changes a demonstrated T3
  error code, contrary to section 2.1's unconditional preservation clause.

The narrow recommended ADMIN clarification is to explicitly authorize this
**shared implementation error-code correction** as an exception to section
2.1, retaining `REPORT_HEAD_AMBIGUOUS` for multiple heads and keeping the
frozen specification unchanged. This recommendation is not self-authorization
and has not been implemented. No new method name, error code, lock system or
algorithm copy is needed merely to resolve this discrepancy.

## U5. Delivery status

WP4B.2 section 11 requires report-only delivery upon this conflict. The old
14-file backup remains untouched and recoverable at its previously recorded
path/hash. Its restoration is intentionally not claimed; directed query tests
have not yet passed, which is the taskbook's prerequisite for restoration.

No full regression/build or implementation CI result is claimed for this
attempt. The earlier 102 passing MCP tests were measured before the prior
withdrawal and do not describe this clean baseline. The report commit and
remote SHA-256 are returned after GitHub readback. Historical reports below
are preserved verbatim under historical headings.

```yaml
DELIVERY_KIND: BLOCKED_REPORT_ONLY
FILES_CHANGED: 1
PRODUCTION_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WP4C_STARTED: false
WP4D_STARTED: false
MANIFEST_COMMIT: NOT_CREATED_WP4B_2_SECTION_11
REQUESTED_GATE: NONE
```

---

# Historical report accepted at 1434d409 — public query scope resolved by WP4B.2

# Current WP4B.1 implementation audit — BLOCKED

```yaml
WP4B_STATUS: BLOCKED
STOP_CODE: MCP_PUBLIC_REPORT_HEAD_QUERY_UNAVAILABLE
AUTHORIZED_SCOPE: WP4B_RESUME_ONLY
REPORTER: ME
WP4B_0_DECISION_APPLIED: true
WP4B_1_DECISION_APPLIED: true
TASKBOOK_COMMIT: e885135f4b074845944a7b8b799de879549fbc33
TASKBOOK_SHA256: 0695cd68237a5a13eb438935d8741512476f977878938afd8864165345b694df
INPUT_HEAD: 72e26fd214849922369e9135c8be0cb1fd260da8
IMPLEMENTATION_BASE: e885135f4b074845944a7b8b799de879549fbc33
PARENT_GATE_COMMIT: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
BRANCH: review/fcop-4.0-wp4b-mcp-adapter
DRAFT_PR: 15
IMPLEMENTATION_STARTED: true
UNFINISHED_IMPLEMENTATION_WITHDRAWN: true
REQUESTED_GATE: NONE
```

## S1. Decision: a missing public read capability, not missing execution permission

WP4B.1 resolved the T6 mapping. The accepted Profile-template and Relay
clarifications also remain resolved. No repeat authorization is requested for
that work. The implementation was resumed, not merely researched.

During completion of the required per-tool behavioral disposition, a separate
public-library capability gap was demonstrated: v4 `list_reports` and
`read_report` must report ambiguous REPORT heads, but neither accepted public
Project method is available on v4. The public single-envelope reader does not
validate the subject/attempt replacement graph. The actual Core T3 gate does
detect the same ambiguity correctly.

Original WP4B sections 2.1, 3, 5.2 and 13 require the WP1 dispositions while
restricting the adapter to public Project operations, prohibiting duplicated
Core judgments, and requiring unfinished production changes to be withdrawn
when that boundary cannot be satisfied. WP4B.1 sections 8–10 retain these
restrictions. Returning a successful unvalidated list, calling private Core
helpers, or adding a second head resolver would not constitute completion.

This is not evidence that Core's lifecycle gate is broken, nor a request to
change the frozen head rule. It is evidence that the accepted **public read
surface** does not expose the required judgment. The implementation and full
delivery matrix are incomplete; the passing MCP subset is not acceptance.

## S2. Fixed-source evidence

All source line numbers below refer to `e885135f4b074845944a7b8b799de879549fbc33`.
No production, frozen specification, Schema or Conformance file was changed in
the report-only delivery.

| Source | Evidence |
|---|---|
| `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md:48` | `list_reports` must support subject/attempt/head queries, not decide validity itself, and return `REPORT_HEAD_AMBIGUOUS` for multiple heads. |
| Same file, line 55 | `read_report` must expose attempt/head metadata and explicitly reject invalid or ambiguous heads. |
| `spec/fcop-4.0-spec.md:72` (F4.3.4) | The valid REPORT is the unique unreferenced head of the subject/attempt replacement graph. Multiple heads return `REPORT_HEAD_AMBIGUOUS`. |
| `src/fcop/v4/boundary.py`, `_METHOD_POLICIES` | `list_reports` and `read_report` are `V4_READ_UNAVAILABLE`; dispatch raises `toolkit:OPERATION_NOT_IMPLEMENTED`. |
| `src/fcop/v4/lifecycle.py:651`, `inspect_state` | `envelope_path` validates one envelope and its relations; TASK mode returns stage, digest, last transition and current attempt. Neither path calls the head resolver. |
| `src/fcop/v4/lifecycle.py:104`, `report_head` | The existing resolver validates the replacement graph and rejects multiple heads, but takes private `_Creation`, not a public Project request. |
| `src/fcop/v4/convergence.py`, `snapshot` | Public `family_digest` computes Branch report-head entries; an ordinary Root with no Branches does not cause its own REPORT heads to be validated. |
| `src/fcop/project.py:313`, `inspect_state` | The public API promises envelope inspection without lifecycle recovery; it has no head-query selector. |

The fixed WP4B.1 taskbook was retrieved again using GitHub's contents API.
Base64-decoded API bytes equal `git show <commit>:<path>` bytes, with SHA-256
`0695cd68237a5a13eb438935d8741512476f977878938afd8864165345b694df`.
The remote review branch was still at the fixed taskbook commit before this
report was prepared; `main` remained `68dbeb15f4e7f84e1d03f907be9fa66c2265843e`.

## S3. Executed reproduction and observed results

Environment: Windows, CPython 3.12, FastMCP 3.2.4. The probe prepended the
independent worktree's `src` and `mcp/src` to `sys.path`. It used a fresh
temporary workspace, not `D:/FCoP` or a dogfood workspace.

Arrange: create and claim an ordinary Root TASK through public Project calls;
write a valid final REPORT. Simulate external filesystem corruption **only in
the temporary test fixture** by copying that REPORT with a new valid REPORT
ID and matching filename. This produces two individually Schema-valid final
heads for the same subject and attempt. This is not a second writer API.

Act: call public envelope inspection, the public query methods, public family
digest, the unfinished real MCP query handlers via `fastmcp.Client`, then the
actual public T3 transition. Assert the complete file-byte map is unchanged
after fixture construction.

Observed output (random REPORT IDs abbreviated only here):

```text
PUBLIC_INSPECT_ACCEPTED REPORT-<first-id> final
PUBLIC_INSPECT_ACCEPTED REPORT-<second-id> final
PUBLIC_QUERY list_reports toolkit:OPERATION_NOT_IMPLEMENTED
PUBLIC_QUERY read_report toolkit:OPERATION_NOT_IMPLEMENTED
PUBLIC_FAMILY_DIGEST_SUCCEEDED True
LOCAL_ADAPTER_QUERY list_reports is_error False code None items 2
LOCAL_ADAPTER_QUERY read_report is_error False code None items 0
CORE_GATE REPORT_HEAD_AMBIGUOUS
ZERO_FILE_CHANGES_AFTER_FIXTURE True
```

`items 0` for `read_report` means its structured object had no `items` array;
it returned a successful single envelope. It does not mean the file was absent.
Both local adapter results violate the retained head-query disposition; they
are recorded as failures, not accepted behavior. Those handlers are withdrawn.

The Core-only part is reproducible directly on the fixed input commit without
the withdrawn MCP implementation. Run this from that checkout using Python
with the repository `src` on its import path:

```python
import tempfile
from pathlib import Path
from uuid import uuid4

from examples.v4.application import Application
from fcop.errors import V4ProtocolError

with tempfile.TemporaryDirectory(prefix="fcop-wp4b-query-proof-") as temporary:
    root = Path(temporary).resolve()
    app = Application(root)
    task = app.task("Two individually valid REPORT heads")
    attempt = app.project.inspect_state(task_id=task)["current_attempt_id"]
    first = app.project.write_report(
        workspace_id=app.workspace_id, sender="ME", recipient="ME",
        subject_ref=task, body="Evidence", attempt_id=attempt,
        report_kind="final", result="done",
    )
    first_path = Path(first["path"])
    second_id = "REPORT-" + uuid4().hex
    second_path = first_path.with_name(second_id + ".md")
    second_path.write_bytes(first_path.read_bytes().replace(
        first["report_id"].encode(), second_id.encode(),
    ))  # Test-only damaged-state fixture, not production mutation.
    def files():
        return {p.relative_to(root).as_posix(): p.read_bytes()
                for p in root.rglob("*") if p.is_file()}
    before = files()
    for path in (first_path, second_path):
        assert app.project.inspect_state(
            envelope_path=path.relative_to(root).as_posix(),
        )["report_kind"] == "final"
    for method, kwargs in (
        ("list_reports", {}),
        ("read_report", {"filename_or_id": first["report_id"]}),
    ):
        try:
            getattr(app.project, method)(**kwargs)
        except V4ProtocolError as error:
            assert error.code == "toolkit:OPERATION_NOT_IMPLEMENTED"
        else:
            raise AssertionError("Expected unavailable public query")
    assert app.project.family_digest(root_task_id=task)
    try:
        app.move(task, "active", "review", "submit_task",
                 report_ref=first["report_id"])
    except V4ProtocolError as error:
        assert error.code == "REPORT_HEAD_AMBIGUOUS"
    else:
        raise AssertionError("Expected Core ambiguity rejection")
    assert files() == before
```

## S4. Alternatives checked, not silently adopted

1. **Public `list_reports` / `read_report`:** demonstrated unavailable on v4.
2. **Public `inspect_state(envelope_path=...)`:** demonstrated successful on
   each conflicting head; individual Schema validity is not head uniqueness.
3. **Public `inspect_state(task_id=...)` / `read_task`:** exposes TASK facts,
   not a head query or replacement-graph verdict.
4. **Public `family_digest`:** demonstrated successful on the ordinary Root
   despite the conflicting Root REPORTs; its Branch-family scope is different.
5. **Private `report_head` plus `project._v4_creation`:** would reuse the
   algorithm but violate the taskbook's public-Project-only boundary. It was
   not imported by the adapter.
6. **Compute heads in MCP from inspected envelopes:** would duplicate the
   Core head-validity judgment; counting files would also wrongly reject
   legitimate final/replacement chains. Not implemented.
7. **Invoke transition/write-report/convergence as a query probe:** these are
   business writers, not read-only validation. Success can mutate the task or
   append facts. Deliberately malformed writer requests are not a public
   read contract and may fail before the desired validation. Not adopted.
8. **Change the accepted Project or weaken the disposition:** outside the
   current authorized write set. Not performed.

A narrow continuation needs an ADMIN decision for a public, read-only Toolkit
REPORT-head query boundary (implemented under an explicit permitted write
scope), or an explicit revision of the MCP query disposition. The frozen
head algorithm itself already exists and need not be duplicated or changed.
This report does not choose a new public API or a relaxed query contract.

## S5. Work performed and preserved; no false completion counters

- T6 was implemented locally using the exact public transition mapping.
  Actual MCP transport tests covered new attempt, exact retry, old REPORT
  rejection, empty/DENIED/UNKNOWN trusted registries and forbidden inputs.
- A separate v4 46-tool snapshot was added locally; historical 45-tool snapshot
  was left untouched. Resource routing and explicit Relay transport were in
  progress, not fully verified.
- Latest local MCP command before withdrawal:
  `python -m pytest tests/test_fcop_mcp -q`, with `PYTHONPATH` set to this
  worktree's `src;mcp/src`: **102 passed, 3 warnings in 68.82 seconds**.
  This included 22 new tests. It did not cover every WP4B obligation; the
  later two-head probe demonstrated a missing required behavioral assertion.
- Earlier resource-registration collection errors were fixed before that
  successful run. They are not the stop code.
- Ruff and mypy were also run; implementation lint/type work remained. A
  corrected-source-path mypy run reported 15 errors in two new modules.
  These are unfinished implementation checks, not a claim of a Core defect.
- Full FCoP/v4 regression, build, clean base/Relay install, remaining race
  tests and final implementation CI were **not completed** before the
  hard stop. Their results are not inferred from prior phases.

Before withdrawal, all 14 modified/new implementation, test, snapshot and plan
files were preserved in an external local ZIP. Every ZIP entry was read back
and its SHA-256 compared to its source file: **14/14 matched**.

```text
D:/FCoP-wp4b-evidence/wp4b1-unfinished-e246ecc148534c73a1eae34b3ae3b628.zip
SHA256: 27d636ec70dc675bf90e533b2951e679e9adb62abbf892b5efb1fc40271e1d87
```

This is recoverable, unfinished local evidence, **not an approved package or
GitHub implementation delivery**. The temporary probe and the code above
provide the remote reviewer with the independently reproducible reason for
the stop; the ZIP is not required to reproduce the missing Core read surface.
Only this report is committed. The accepted historical blocker reports below
are retained verbatim, with their former current-status headings explicitly
placed under a historical section.

## S6. Report-only delivery and stop

Original WP4B section 13 mandates report-only delivery on a hard stop. Thus
no success Content/Manifest pair is fabricated and no implementation Gate is
requested. Draft PR #15 is updated to distinguish this new stop from the
resolved T6 mapping. Report commit SHA and remote byte hash are returned in
the execution receipt after push/refetch verification.

```yaml
DELIVERY_KIND: BLOCKED_REPORT_ONLY
FILES_CHANGED: 1
PRODUCTION_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WORKSPACE_MIGRATION: false
WP4C_STARTED: false
WP4D_STARTED: false
LOCAL_MCP_BEFORE_WITHDRAWAL: 102_PASSED_NOT_FULL_ACCEPTANCE
FINAL_IMPLEMENTATION_CI: NOT_APPLICABLE_NO_IMPLEMENTATION_DELIVERED
MANIFEST_COMMIT: NOT_CREATED_HARD_STOP_SECTION_13
REQUESTED_GATE: NONE
```

---

# Historical report accepted at 72e26fd2 — T6 mapping resolved by WP4B.1

# Current WP4B.0 resume audit — BLOCKED

```yaml
WP4B_STATUS: BLOCKED
STOP_CODE: MCP_T6_TOOL_MAPPING_UNDERDETERMINED
AUTHORIZED_SCOPE: WP4B_RESUME_ONLY
WP4B_0_DECISION_APPLIED: true
TASKBOOK_COMMIT: b2453202686d08bd6584302072e0be814a059be4
TASKBOOK_SHA256: 10118bcc63df3b8334c9eca4137493164f1c0d329f86dd572b0c9ee9af758c59
BLOCKED_INPUT_HEAD: 9558a267333f245e5d4aa8c32aee4d1a90210639
PARENT_GATE_COMMIT: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
BRANCH: review/fcop-4.0-wp4b-mcp-adapter
WORKTREE: D:/FCoP-wp4b-mcp-adapter
IMPLEMENTATION_STARTED: false
REQUESTED_GATE: NONE
```

## R1. Previous blockers resolved; fixed input verified

The complete WP4B.0 taskbook was fetched at its fixed commit, read, and
independently retrieved using the GitHub contents API. Base64-decoded remote
bytes match `git show` bytes, and their SHA-256 is exactly
`10118bcc63df3b8334c9eca4137493164f1c0d329f86dd572b0c9ee9af758c59`.
The clean, independent WP4B worktree was fast-forwarded from `9558a267...` to
`b2453202...`; the only intervening file is the correction taskbook.

The ADMIN decisions are accepted without qualification:

- All three resource templates remain read-only Profile documents, not business
  envelope generators. Their document `version: 1` does not classify a workspace.
- FastMCP's transitive websockets dependency is allowed. Relay optionality is
  an activation and direct-dependency boundary, not environment purity.

Neither point remains a blocker. The earlier report is retained verbatim in
the historical section below and remains independently accessible at its
accepted commit. Its former stop code is **not** the current decision.

## R2. Remaining decision: which canonical tool requests T6?

Original WP4B section 5.2 requires reopening operations, section 8.3 requires
real T1–T7 delegation, and the canonical name set must remain exactly 45.
WP4B.0 keeps these obligations and the WP1 disposition in force. However,
the retained tool mapping does not assign a request entry to T6, and it
explicitly rules out the natural but unsafe `claim_task` shortcut.

| Fixed source | Constraint |
|---|---|
| `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md:28` | `claim_task` is T2; explicitly not expanded to T6; non-inbox state is `INVALID_TRANSITION`. |
| Same file, section 2 rows 1/2/37/39 | `approve_task`, `archive_task`, `reject_task`, `submit_task` respectively map to T4/T7/T5/T3. |
| Same file, row 16; frozen F4.4.4 | `finish_task` rejects v4 with `LEGACY_TRANSITION_NOT_ALLOWED`. |
| Same file, row 30; frozen F4.3.3–F4.3.5 | `mark_human_approved` appends an authorization REVIEW; writing authorization is not consuming it by moving a TASK. |
| Same file, row 44 | `write_review` creates an append-only typed REVIEW, not an implicit lifecycle transition. |
| Same file, section 6, line 115 | T6 has no dedicated name in the 45; do not reinterpret `claim_task`; future authorized Adapter exposure must preserve the reopen/authorization/Profile/new-attempt contract. |
| Original WP4B lines 148–154 | Preserve the exact 45 names and disposition; necessary new v4 input fields are backward-compatible optional extensions. |
| Original WP4B lines 162–163, section 8.3 | Reopen and real T1–T7 paths must be delivered. |

The later-exposure clause permits a future compliant T6 Adapter, but neither
taskbook identifies **which retained tool and explicit operation selector**
should request that new side effect while retaining the above meanings.
An optional input may transport a reference, but adding an input that changes
which operation a tool performs also defines public behavioral semantics.

This is not a claim that T6 is missing from Core: `Project.transition` exists
and is the correct owner. It is a missing MCP operation-to-tool contract.
The following alternatives were considered and not silently adopted:

1. A new `reopen_task`/`transition` tool would violate the exact canonical set.
2. Allowing `claim_task` on done explicitly conflicts with the WP1 prohibition.
3. Having `reject_task` choose T5 or T6 from current state changes its defined
   rejection behavior; an explicit `operation=reopen` variant still needs an
   approved mapping and documentation of the T5/T6 distinction.
4. Moving a TASK as part of `write_review` or `mark_human_approved` conflates
   creation of authorization evidence with its consumption.
5. Hiding the transition under a read/inspect/audit tool changes its side-effect
   boundary; WP1 row 11 specifically says audit must not repair for the user.
6. Calling Project directly only from a test would prove Core behavior, not
   delivery through a production MCP entry point.

Family digest and recovery routing were also inspected. Their public Python
methods exist, but the absence of equally named MCP tools alone is **not**
reported as another blocker: derived read projection and internal recovery
may cover parts of that requirement. This stop is specifically the mandatory
T6 write entry and its unresolved public tool meaning.

## R3. Reproducible read-only audit

At `b2453202686d08bd6584302072e0be814a059be4`, a Python audit decoded
`tests/test_fcop_mcp/snapshots/tool_surface.json` and inspected the Project AST:

```text
CANONICAL_TOOLS 45
DIRECT_V4_OPERATION_NAMES_PRESENT []
  (checked names: transition, reopen_task, recover_operation, family_digest)
approve_task ['actor', 'note', 'task_id']
archive_task ['lang', 'task_id']
claim_task ['actor', 'task_id']
finish_task ['actor', 'task_id']
reject_task ['actor', 'note', 'task_id']
submit_task ['actor', 'task_id']
inspect_task ['filename']
fcop_audit ['output', 'project_path', 'scope']
PROJECT_PUBLIC_OPERATIONS ['family_digest', 'recover_operation', 'transition']
```

Reproduce the inventory with `json.loads(Path(snapshot).read_text())`, selecting
`tools[*].name` and `tools[*].params[*].name`. Inspect
`src/fcop/project.py` with `ast.parse` and select public `FunctionDef` nodes
under `ClassDef(name='Project')`. Read the cited WP1 rows to distinguish the
missing name observation from the actual behavioral-contract conflict.

This audit did not call a business writer or modify a test. It is not a new
conformance pass claim. Once this contract issue was confirmed, original
WP4B section 13 and WP4B.0 section 9 required stopping; the planned new
contract tests, implementation and full regression matrix were not started.

## R4. Narrow ADMIN clarification requested

Specify one explicit MCP mapping for T6: retained tool name, optional selector
and input fields, its default behavior, and the distinction from the tool's
existing operation. Alternatively, explicitly revise the surface policy.
In either case retain the frozen Core T6 evidence, trusted Profile,
single-use authorization, new-attempt and retry contracts. No Core or Schema
change is requested or needed merely to define the Adapter entry.

No mapping has been adopted here. No extra tool, fourth template, hidden
transition or special test-only route has been created.

## R5. Current delivery status

Only this blocked report is updated, as permitted by WP4B.0 section 8 and
required by the hard-stop clauses. The accepted historical report is preserved
below. The same review branch and Draft PR #15 carry this report-only update;
commit and remote SHA-256 verification are returned in the execution receipt.
No success Manifest or implementation acceptance request is made.

```yaml
RESOURCE_TEMPLATE_CLASSIFICATION: PROFILE_RESOURCE_3_OF_3_ACCEPTED_CONTRACT
RESOURCE_TEMPLATE_AUTHORIZATION_EFFECT: NONE_BY_CONTRACT_NOT_NEWLY_TESTED
BUSINESS_ENVELOPE_GENERATION_BY_TEMPLATES: false
BUSINESS_ENVELOPE_TOOLS: NOT_IMPLEMENTED
FCOP_DIRECT_BASE_RELAY_DEPENDENCY: PRESENT_BASELINE_UNCHANGED
FASTMCP_TRANSITIVE_WEBSOCKETS: RECORDED_IF_PRESENT_ALLOWED
BASE_STDIO_NO_RELAY_ACTIVATION: NOT_NEWLY_TESTED
BASE_STDIO_NO_NETWORK_CONNECT: NOT_NEWLY_TESTED
RELAY_REQUIRES_EXPLICIT_ENABLEMENT: ACCEPTED_CONTRACT_NOT_IMPLEMENTED
RELAY_OPTIONAL_EXTRA_METADATA: NOT_IMPLEMENTED
FULL_REGRESSION_BUILD_CLEAN_INSTALL: NOT_RUN
GITHUB_CI: NOT_AN_IMPLEMENTATION_ACCEPTANCE_CLAIM
PRODUCTION_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WORKSPACE_MIGRATION: false
WP4C_STARTED: false
WP4D_STARTED: false
REQUESTED_GATE: NONE
```

---

# Historical report accepted at 9558a267 — former blockers resolved by WP4B.0

# WP4B pre-implementation contract audit — BLOCKED

```yaml
WP4B_STATUS: BLOCKED
STOP_CODE: MCP_TEMPLATE_CONTRACT_UNDERDETERMINED
AUTHORIZED_SCOPE: WP4B_ONLY
REPORTER: ME
TASKBOOK_COMMIT: 245d914e1f0aff48a19d8f0ba8432e6b4f008b68
TASKBOOK_SHA256: 0a7605efba198799c3f859b68c9d225be568a57e8c591ac1097cbc2eaebebbe9
INPUT_HEAD: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:/FCoP-wp4b-mcp-adapter
BRANCH: review/fcop-4.0-wp4b-mcp-adapter
IMPLEMENTATION_STARTED: false
REQUESTED_GATE: NONE
```

## 1. Decision and authority

Stop before implementation under the taskbook's sections 3 and 13. The three
canonical MCP **resource templates are read-only team/role Profile documents**;
WP4B sections 5.3 and 8.4 instead require them to generate version-compatible
business envelopes. These are different output contracts. The higher-priority
WP1 disposition does not specify such a conversion, and the frozen Core does
not choose an envelope type or request mapping for these Profile resources.

This report does not declare a Core defect, reject the accepted WP4A Gate, or
claim that MCP adaptation is generally impossible. It identifies a decision
needed before writing implementation or tests that would lock in one of the
incompatible interpretations.

Section 13 specifically requires **only this blocked report** to be committed
and forbids requesting a Gate. Consequently there is no implementation Content
Commit / Manifest Commit pair or success Manifest in this blocked delivery.
The authorized review branch and Draft PR provide the remote review entry;
delivery commit and remote-readback hash are reported in the execution receipt.

## 2. Inputs independently verified

The taskbook was fetched from GitHub at the fixed commit, read in full, and
independently read back with the GitHub contents API:

```text
gh api repos/joinwell52-AI/FCoP/contents/taskbooks/fcop-4.0/WP4B/01-MCP-Thin-Adapter-and-Version-Routing-Taskbook-v1.0.zh.md?ref=245d914e1f0aff48a19d8f0ba8432e6b4f008b68
Git blob: 1e13ed42869daae8bacd1f76eb9d090dd2eeb1a7
Decoded API bytes SHA-256:
0a7605efba198799c3f859b68c9d225be568a57e8c591ac1097cbc2eaebebbe9
Decoded API bytes == git show <taskbook-commit>:<taskbook-path>: true
```

The independent worktree starts at the taskbook commit, directly after its
signed parent Gate:

```text
245d914e1f0aff48a19d8f0ba8432e6b4f008b68 docs(fcop4): authorize WP4B MCP thin adapter
982fcb24d9093e01c5ba4fdb87e710acd57e6d54 docs(fcop4): accept WP4A machine contract
d663e9dc05ca4f8db135b87f04f5dee4c3543e55 WP4A.3: seal Windows checkout policy manifest
```

`git merge-base --is-ancestor 982fcb24d9093e01c5ba4fdb87e710acd57e6d54 HEAD`
and `git diff --quiet aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6 HEAD --
spec/fcop-4.0-spec.md spec/fcop-4.0-spec.zh.md` succeeded before this report.
The worktree was clean. The two frozen specification files have not drifted.

The section 3 reading set was reviewed: both frozen specifications, both WP0
MCP disposition reports, WP1 compatibility/MCP disposition, WP4 master
taskbook, and `reviews/fcop-4.0/gates/WP4A-MACHINE-CONTRACT-ACCEPTED.md`.
The fixed taskbook is the ADMIN decision record; this ME execution report
records the resulting evidence and returns the unresolved decision to ADMIN.

## 3. Exact contract mismatch

All repository references below refer to the fixed taskbook commit unless a
different commit is explicitly stated.

| Source | Actual requirement or fact |
|---|---|
| WP4B taskbook section 3 | Frozen contract, accepted Core/WP4A and WP0/WP1 disposition take priority over this taskbook. |
| `reports/FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md:89–95` | The three resource templates remain registered team Profile / Chinese role Profile / English role Profile. |
| `reports/MCP-RESOURCE-DISPOSITION-4.0.md` section 3 | Parameters are only `team`, or `team` and `role`; outputs come from `get_template(...).readme` or `.roles[...]`, classified `PROFILE_RESOURCE`. |
| `mcp/src/fcop_mcp/server.py:3856–3899` | The three registered handlers actually return those read-only Profile documents. |
| WP4B taskbook lines 195–196, section 5.3 | Templates must generate compatible envelopes by workspace version; a v4 template must not produce old relation/version, missing operation_id, or mutable REVIEW shape. |
| WP4B taskbook line 298, section 8.4 | Each of the three templates must generate valid v3/v4 shapes. |
| Frozen specification F4.3.1–F4.3.2, F4.8.1–F4.8.4, F4.11.3 | Four business envelope types have distinct mandatory fields; create TASK has caller operation identity. MCP resource templates themselves are not Core. |

Returning a Profile README is not creating or rendering a TASK, REPORT, ISSUE
or REVIEW. A `team`/`role` URI supplies neither an envelope type nor the subject,
operation, attempt, evidence, recipient and other type-specific inputs needed
to select a real envelope. Nor does the taskbook specify that the new wording
means merely illustrative snippets inside an otherwise unchanged Profile
document. Such snippets are not themselves proof of a valid business request.

It would therefore be an unapproved choice to:

- replace the Profile document contract with an envelope generator;
- invent envelope inputs, defaults or additional canonical URI parameters;
- reinterpret the requirement as embedded examples and count those as the
  three templates' required behavioral coverage;
- ignore sections 5.3/8.4 and claim a version-labelled README satisfies them;
- author v4 team/role policy or Host guidance that belongs to deferred WP4C.

No such choice has been made. The version 1 metadata seen in the existing
Profile documents is reported as baseline evidence, **not** as proof that
these documents should be converted into v4 business envelopes.

## 4. Read-only executable evidence

Environment: Windows, Python 3.12, FastMCP 3.2.4. The probe explicitly prepended
this worktree's `src` and `mcp/src` to `sys.path`, cleared the four project/relay
environment overrides in the probe process, and called the actual registered
server. It did not invoke any business write or bind a user workspace.

Equivalent probe (no repository file is needed):

```python
import asyncio
import hashlib
import os
import sys
from pathlib import Path

import yaml

root = Path.cwd()
for key in ("FCOP_PROJECT_DIR", "CODEFLOW_PROJECT_DIR", "FCOP_ROOM_KEY", "FCOP_RELAY_WS_URL"):
    os.environ.pop(key, None)
sys.path[:0] = [str(root / "src"), str(root / "mcp/src")]
from fcop_mcp.server import mcp

async def probe():
    print(len(await mcp.list_tools()), len(await mcp.list_resources()),
          len(await mcp.list_resource_templates()))
    for uri in ("fcop://teams/dev-team", "fcop://teams/dev-team/PM",
                "fcop://teams/dev-team/PM/en"):
        result = await mcp.read_resource(uri)
        text = result.contents[0].content
        data = yaml.safe_load(text.lstrip("\ufeff").split("---", 2)[1])
        print(uri, data.get("version"), data.get("kind"), data.get("type"),
              data.get("operation_id"), hashlib.sha256(text.encode()).hexdigest())

asyncio.run(probe())
```

Observed inventory: **45 tools / 11 static resources / 3 resource templates**.
All three registered templates have MIME type `text/markdown`.

| Invoked URI | version | kind | type | operation_id | Returned text SHA-256 |
|---|---:|---|---|---|---|
| `fcop://teams/dev-team` | 1 | spec | absent | absent | `2ec172c249b88d20bf399e0f4897221e66efb5d8bdacb2328686f978864a6b36` |
| `fcop://teams/dev-team/PM` | 1 | spec | absent | absent | `348978298f1a7e005126fcbcee54ea6a744ccf0ef95f2de16312f011180fab51` |
| `fcop://teams/dev-team/PM/en` | 1 | spec | absent | absent | `040e20a26e438630ffa970060f2f9e37e47a80175a6832c58fa378a496fd6d6a` |

These are baseline inventory and Profile-read probes, **not WP4B disposition
or v4 conformance pass counts**. No test ID, assertion, snapshot or production
handler was changed. The full implementation regression/build/clean-install
matrix was not run after the pre-implementation hard stop.

## 5. Additional dependency observation (not a second stop code)

The initial read-only audit also found that removing FCoP's direct
`websockets>=12.0` requirement alone will not establish the required clean base
installation without websockets:

- `mcp/pyproject.toml:65` requires `fastmcp>=3.2.0`.
- Installed FastMCP 3.2.4 distribution metadata contains the unconditional
  requirement `websockets>=15.0.1`.
- The official PyPI JSON metadata independently confirms this for both the
  minimum 3.2.0 and installed 3.2.4 versions:
  [3.2.0 metadata](https://pypi.org/pypi/fastmcp/3.2.0/json),
  [3.2.4 metadata](https://pypi.org/pypi/fastmcp/3.2.4/json).

An isolated import-hook probe that denied imports named `websockets` or its
submodules still allowed `from fastmcp import FastMCP` to finish. Therefore the
observed problem is **declared installation dependencies**, not a demonstrated
failure of that import. No clean-install or complete stdio success is claimed.
This observation does not prove that every SDK/version alternative is
impossible. It means a resumed plan must account for the transitive dependency,
not use `--no-deps`, uninstall a required dependency, patch upstream metadata or
claim that moving the direct requirement to an extra has already solved it.
No dependency or transport changes were attempted.

## 6. Decision requested before resumption

ADMIN should clarify the three resource templates' expected v4 output contract
in a fixed correction taskbook. The narrow option consistent with WP1 is to
retain **read-only Profile resources**, specify their version labeling and
WP4C-unavailable behavior, and scope business-envelope input/output validation
to the appropriate tool calls. This is a recommendation, not an adopted policy
or permission to weaken the present tests-to-be-written requirements.

If actual envelope generation was intended, the taskbook needs an explicit
mapping and inputs, with its relationship to the three retained Profile URI
contracts and WP4C exclusion resolved by ADMIN. The transitive dependency
observation above should also be addressed before making a clean-install
acceptance claim.

Only ADMIN can choose. This report requests clarification, **not**
`WP4B_MCP_ADAPTER_ACCEPTED` and not authorization for WP4C/WP4D.

## 7. Scope and verification status

```yaml
TASKBOOK_REMOTE_BYTES: VERIFIED
PARENT_GATE_ANCESTRY: VERIFIED
FROZEN_SPEC_DRIFT: 0
BASELINE_LIVE_TOOLS: 45
BASELINE_LIVE_STATIC_RESOURCES: 11
BASELINE_LIVE_RESOURCE_TEMPLATES: 3
BASELINE_PROFILE_READ_PROBES: 3/3
WP4B_TOOL_DISPOSITION: NOT_IMPLEMENTED
WP4B_RESOURCE_DISPOSITION: NOT_IMPLEMENTED
WP4B_TEMPLATE_DISPOSITION: BLOCKED
WORKSPACE_ROUTING: NOT_IMPLEMENTED
V3_COMPATIBILITY: NOT_RETESTED
V4_PROJECT_DELEGATION: NOT_IMPLEMENTED
TRUSTED_PROFILE_INITIALIZATION: NOT_IMPLEMENTED
CALLER_AUTHORITY_SMUGGLING: NOT_TESTED
BASE_STDIO_WITHOUT_WEBSOCKETS: NOT_VERIFIED
RELAY_OPTIONAL_EXTRA: NOT_IMPLEMENTED
PACKAGE_COMPATIBILITY_FAIL_CLOSED: NOT_IMPLEMENTED
V4_CONFORMANCE: NOT_RUN
TEST_FCOP: NOT_RUN
MCP_REGRESSION: NOT_RUN_FULL_SUITE
RUFF: NOT_RUN
MYPY: NOT_RUN
GITHUB_CI_AT_FINAL_HEAD: NOT_A_GATE_CLAIM
UNEXPECTED_FAILURES: NOT_MEASURED_FULL_MATRIX
NEW_PUBLIC_APIS: 0
NEW_PRODUCTION_MODULES: 0
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
PRODUCTION_FILES_MODIFIED: 0
TEST_FILES_MODIFIED: 0
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
SCHEMA_FILES_MODIFIED: 0
CODEFLOWMU_FILES_MODIFIED: 0
MAIN_MODIFIED: false
RELEASE_CREATED: false
WORKSPACE_MIGRATION: false
WP4C_STARTED: false
WP4D_STARTED: false
MANIFEST_COMMIT: NOT_CREATED_HARD_STOP_SECTION_13
REQUESTED_GATE: NONE
```

The original `D:/FCoP` worktree and all existing workspaces were left untouched.
There were no unfinished production changes to withdraw. Only this report is
eligible for this blocked review-branch commit.
