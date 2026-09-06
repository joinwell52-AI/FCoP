# WP4C.0 Distribution Baseline — BLOCKED

- Repository: `joinwell52-AI/FCoP`
- Gate / audited tree: `aad88ae5f1112881545d30c9938739e83481516d`
- Taskbook commit: `962b67d89e137c26440291d3a48fc7aea1cfebb6`
- Taskbook: [fixed WP4C.0 authority](https://github.com/joinwell52-AI/FCoP/blob/962b67d89e137c26440291d3a48fc7aea1cfebb6/taskbooks/fcop-4.0/WP4C.0/01-Rule-Distribution-Host-Assembly-and-Development-Context-Baseline-Audit-Taskbook-v1.0.zh.md)
- Taskbook SHA-256: `c8c4cb26708a480a6793d88c21511b103f140021c3827c9977b076dfed748e55`
- Scope: `WP4C_0_ONLY`; report state: `BLOCKED`.

## Stop decision

`ENGINEERING_CONSTITUTION_SOURCE_UNRESOLVED` is one confirmed P0 blocker, not an exhaustive count of all possible conflicts. Taskbook sections 3 and 14 require an identifiable authority file, version, digest, license and acquisition method for 《Agent 原生软件工程宪法》. Those cannot be established from the supplied fixed inputs. Section 14 permits factual BLOCKED reports but prohibits requesting the acceptance Gate.

No replacement constitution is authored, downloaded or adopted. The audit stopped at this prerequisite; remaining audit obligations are explicitly incomplete. `REQUESTED_GATE: NONE`; WP4C.1 is not started.

## Reproducible authority evidence

All paths below refer to the fixed Gate tree, not a mutable checkout or the currently deployed user workspace.

| Evidence | Observed fact | Limit |
|---|---|---|
| `taskbooks/fcop-4.0/WP4/00-Public-Contract-Adapters-and-Distribution-Master-Taskbook-v1.0.zh.md:569` | Names 《Agent 原生软件工程宪法》 and limits its audience to FCoP developers. | Does not pin its text, version, digest, license or acquisition location. |
| Same master, lines 112 and 127 | Declares the development-only flag and future phase. | A roadmap flag/title is not an adopted authority artifact. |
| `reviews/fcop-4.0/gates/WP4B-MCP-ADAPTER-ACCEPTED.md:144` | Restricts the development constitution to development Agents. | Does not identify the constitution payload or fixed authority descriptor. |
| Taskbook commit versus its parent | Direct parent is the Gate; the sole changed file is the WP4C.0 taskbook. | No constitution payload is supplied by this commit. |
| Gate-tree `git grep` for the English/Chinese constitution terms | 42 matching lines, including legacy team-constitution mentions and the titles above. | These matches do not identify the requested engineering constitution; match count is not a normative-rule count. |
| Path inventory / named Git-log probes | No named engineering-constitution artifact established. | This is not a claim that no such document exists anywhere outside the supplied fixed inputs. |

The legacy two-file team constitution (`TEAM-ROLES.md` and `TEAM-OPERATING-RULES.md`) and ADR-0015's historical charter wording are not substitutes for the named engineering constitution. No repository-wide license is presumed to license an unidentified external text.

ADMIN resolution needed: supply a fixed authority file/URL, version, exact SHA-256, applicable license and acquisition/adoption instructions, or publish a fixed taskbook clarification. This report does not choose that policy.

## Baseline and protection

The audit worktree is `D:\FCoP-wp4c0-distribution-audit`, on `review/fcop-4.0-wp4c.0-distribution-audit`, initially clean at the Gate. The taskbook commit is verified separately; it is not inserted into the delivery parent chain. Existing `D:\FCoP` changes and dogfood files are preserved. No branch switch, stash, reset, cleanup, migration or rule redeployment was performed there.

## Source identities established before the stop

The fully read `src/fcop/rules/__init__.py` declares `fcop-rules.mdc` and `fcop-protocol.mdc` and loads them with `importlib.resources` from `fcop.rules/_data`, decoding UTF-8. `get_rules()` and `get_protocol_commentary()` return their text. Version readers extract the corresponding frontmatter version keys. This identifies the loader's declared inputs, not completion of the full canonical-authority audit.

The tracked Host header declares four deployment targets: AGENTS.md, CLAUDE.md and the two Cursor rule files. The six raw Git-blob identities are recorded in the Context report. No generation provenance or byte-reproducible regeneration has been proven in this run.

## Required verification accounting

| Requirement | Current evidence / status |
|---|---|
| Input Gate, taskbook parent, path, SHA-256 | Verified before audit. |
| Rule-related tests | NOT_RUN after prerequisite hard stop. |
| Canonical / four Host copies | Six raw-blob byte/line/hash measurements available; structural comparison incomplete. |
| wheel / sdist inventory | NOT_RUN; no fresh artifact built. |
| Project / MCP distribution call graph | NOT_COMPLETED; loader only read, not the complete call graph. |
| Mandatory inputs UTF-8/LF | Only six measured blobs verified; full inventory NOT_COMPLETED. |
| Normative and reverse-rule mapping | NOT_COMPLETED; denominators not established. |
| Report formatting / diff / allowlist | Delivery validation, recorded in Manifest and remote receipt. |
| Remote parent chain / five SHA-256 | To be measured after delivery; final PR receipt is the authority for that result. |

Full v3/v4/MCP regressions, dry-runs and deployment recovery probes were not run. Earlier WP4B results are historical inputs, not new test results. No production, test, Schema, rule, MCP or Host file was changed.

## Read coverage limitation

The WP4C.0 taskbook, WP4B Gate and rules loader were read in full. Searches and metadata extraction do not count as deep reading. The long Host text read was truncated and is not claimed complete. The remaining mandatory source/specification/history/report set, including the full WP4B evidence package, was not fully reviewed before the stop.

This is a preserved partial baseline and blocker delivery, not a completed WP4C.0 baseline.
