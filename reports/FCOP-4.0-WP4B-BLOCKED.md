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
