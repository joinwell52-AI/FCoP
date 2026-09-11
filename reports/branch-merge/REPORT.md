---
protocol: fcop
version: "3.0"
sender: ME
recipient: ADMIN
status: blocked
---

# MCP 4.0.1 Branch Merge: Core capability evidence

## Result

BLOCKED at the taskbook's explicitly permitted Core capability boundary, not on
taskbook formalities, unrelated workspace files, credentials, or reviewer identity.
The three MCP tools have NOT been implemented or accepted. No package version,
Core source, existing MCP tool, frozen test, or original workspace was changed.

Baseline: `ec7f415f84bfb93534ffccedaad873accd744095`, fetched origin/main.
Independent branch: `codex/fcop-mcp-4.0.1-branch-merge`.

## Reproduction

Run from this checkout with an interpreter containing published `fcop==4.0.0`:

```text
python -I reports/branch-merge/core_capability_probe.py
```

Executed on native Windows with
`C:/Users/Administrator/.cursor/fcop_mcp_venv/Scripts/python.exe`.
The probe asserts the distribution version and site-packages import location; it
does not import the checkout's Core through PYTHONPATH. It uses the existing
public-consumer fixture at `tests/stable/third-party/python-only/app.py` only to
construct valid tasks and authorization evidence. Fixture SHA-256:
`3e169faab05a6f6d75f809af87408b0ac3765e82082d3cbf53042039d5a4327a`.

All TASK/REPORT/REVIEW operations run in a disposable workspace. There are two
real child processes synchronized at READY/GO, followed by a third fresh process.
The trusted evaluator is registered during Project construction, not supplied
by a transition request. The example evaluator is test-only, not issuer security.

Final probe: exit 0. This means the capability observations below reproduced;
it does NOT mean the requested MCP behavior passed.

| Scenario | Observed installed Core 4.0.0 behavior |
| --- | --- |
| Create Branch, then request canonical family digest | `ATTEMPT_MISMATCH` while Branch is inbox |
| Claim Branch, but do not fabricate a REPORT | `REPORT_REQUIRED` while Branch is active |
| Convergence append with durable `operation_id` | `INVALID_ENVELOPE`, no workspace changes |
| Acquire existing Core family lock, call public convergence append | `LOCK_RECOVERY_REQUIRED` after the existing lock timeout; no workspace changes |
| Two processes append identical valid convergence request | Both succeed, two different REVIEW IDs |
| Repeat same append in a fresh process | Third distinct REVIEW ID, not Existing |

Recorded diagnostic-run IDs (before adding explicit expected-code assertions):

- First: `REVIEW-eee527ca1cb6455ab0ed45ba0fb63517`
- Second: `REVIEW-3e15571128d54971afd5f0c1ea09333d`
- Fresh-process retry: `REVIEW-6ef61b7e1b7148fd98d7b94ac9111ba8`
- Family digest after the first two appends:
  `2fc739311bc89eca70fb4f766918eaa65596b1cbdf946301aaafa6e3f196ee2b`;
  the probe verifies it is unchanged from before those appends.

UUIDs, workspace paths, REPORT bytes, and resulting digests vary on rerun.
Rejection/read checks compare the entire temporary workspace's paths and file
SHA-256 values. The retained Core lock inode is outside that fact tree.

## Gap 1: a newly created Branch has no canonical family digest

The requested create_branch success response must contain the latest canonical
family_digest. But Core creates Branches in inbox, before any attempt or REPORT
exists. Core's digest includes each Branch's attempt, precise REPORT ID, and full
REPORT byte digest. Thus creating a Branch and then requesting that digest cannot
produce the mandated success response. Returning the previous digest would be
stale; fabricating an attempt/report, omitting the Branch, or inventing a second
digest algorithm would violate the task's Core reuse boundary.

The same issue affects inspect_family for incomplete families. An explicit
`family_digest: null` plus a structured digest-unavailable reason could preserve
Core semantics, but is a change to the requested return contract that needs ADMIN
resolution. It has not been silently substituted for a canonical digest.

## Gap 2: existing append is not an atomic idempotent merge primitive

Core already validates terminal Branches, exact references, digest, and Root done
under its family lock, then atomically publishes ONE new REVIEW per call. Those
capabilities are reusable. However, public append accepts neither operation_id nor
a caller-selected stable review_id, and does not atomically check for an Existing
merge result. Repeating a valid request intentionally appends another audit fact.
This is not evidence that the original Core append contract is broken; it is
evidence that it alone does not supply the new merge contract.

Wrapping that call in the same private Core family lock is not a solution: the
public call reacquires the non-reentrant kernel lock and times out, as reproduced.
An unlocked precheck followed by append does not atomically reserve a unique
result. A separate MCP lock would coordinate cooperating MCP calls, not all
existing public Core writers under the required family boundary. Writing a second
receipt after append also introduces a response-loss/crash window unless a durable
reconciliation format is defined.

This evidence does not prove every possible adapter algorithm impossible. An
adapter-specific durable marker in REVIEW body, separate serialization, or direct
use of private Core append internals would require carefully defined semantics
and proof. None is an existing public atomic merge service; this change has not
invented such a mechanism or bypassed Core validation to claim completion.

## Source evidence at the fixed baseline

- [Canonical family snapshot](https://github.com/joinwell52-AI/FCoP/blob/ec7f415f84bfb93534ffccedaad873accd744095/src/fcop/v4/convergence.py#L37): every Branch requires current attempt and REPORT head.
- [Public family digest](https://github.com/joinwell52-AI/FCoP/blob/ec7f415f84bfb93534ffccedaad873accd744095/src/fcop/v4/creation.py#L293).
- [Append field whitelist and generated identity](https://github.com/joinwell52-AI/FCoP/blob/ec7f415f84bfb93534ffccedaad873accd744095/src/fcop/v4/creation.py#L836).
- [Locked convergence append](https://github.com/joinwell52-AI/FCoP/blob/ec7f415f84bfb93534ffccedaad873accd744095/src/fcop/v4/creation.py#L941).
- [Kernel lock](https://github.com/joinwell52-AI/FCoP/blob/ec7f415f84bfb93534ffccedaad873accd744095/src/fcop/v4/encoding.py#L447).
- Frozen specification F4.6.1 and F4.6.6 define attempt timing and canonical digest content.

## Verification and next decision

Native Windows executable characterization: reproduced, including real process
concurrency, restart, and zero-write rejection checks. No new-tool stdio validation,
full regression, Ubuntu run, or release acceptance is claimed. Existing tools
remain 46; target 49 and target version 4.0.1 are unfulfilled. Draft PR CI, if
triggered for these evidence files, cannot serve as new-tool acceptance.

ADMIN needs to settle unavailable-digest representation and the allowed durable,
atomic merge boundary before implementation can honestly satisfy all requirements
with Core 4.0.0 unchanged. No extra taskbook SHA or independent reviewer is needed.

```text
FCOP_MCP_BRANCH_MERGE_STATUS: BLOCKED
TARGET_VERSION: fcop-mcp 4.0.1
IMPLEMENTATION_COMPLETE: false
CORE_MODIFIED: false
MCP_BUSINESS_BEHAVIOR_MODIFIED: false
CODEFLOWMU_MODIFIED: false
MERGED: false
PUBLISHED: false
REQUESTED_GATE: NONE
```
