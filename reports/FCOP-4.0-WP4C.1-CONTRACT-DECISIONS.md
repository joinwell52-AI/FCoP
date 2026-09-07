# WP4C.1 Contract Decisions — BLOCKED

## Fixed authority and stop

- Taskbook/input: `81d5cd416515d9d712db0250514f7011c346a07c`.
- Taskbook SHA-256: `21c77fa93750c95e1b27dabaab59a938ef9f6f49677c15c069cbbf3e6dc80220`.
- Scope: WP4C_1_ONLY; executor ME, solo. ADMIN taskbook is the decision carrier; this is a factual execution report, not a replacement taskbook.
- Confirmed P0: **TASKBOOK_RELATION_SET_CONFLICT**.
- This is a semantic conflict, NOT INPUT_REF_MISMATCH: GitHub taskbook bytes, local Git blob, required ancestors and frozen EN/ZH spec bytes all matched.
- Under taskbook §12, contract drafting stops. No candidate contract or freeze Gate is requested.

## Evidence

All line numbers are LF-delimited lines in the fixed input, not floating main.

| Source | Exact constraint / finding |
| --- | --- |
| Taskbook §4.1, line 132 | The candidate relations module's stated responsibility is branch_of, blocks, relates_to, supersedes. |
| Frozen EN spec F4.5.1, line 108 | Core relations are exactly parent, branch_of, subject_ref, references. |
| Frozen ZH spec F4.5.1, line 108 | Same four relations; this is not a translation discrepancy. |
| Frozen spec F4.5.2, line 117 | Strong relation validity and weak references used as gate evidence apply beyond Branch work. |
| Taskbook §4.1, line 139 | Every frozen clause must map to exactly one primary module; cross-references must not duplicate normative duties. |
| Taskbook §5.2, line 261 | Adds relations and convergence to the sequential assembly, leaving ordinary relation coverage ambiguous when read with the misdefined module. |
| Taskbook §9, line 337; §12, line 377 | Frozen Specification must not be changed; stop if changing it would be necessary. |

The sets intersect only at branch_of. Missing from the taskbook's table: parent, subject_ref, references. Additional there but not in F4.5.1: blocks, relates_to, supersedes. This report does not guess the provenance of those additional names or promote them to a Profile.

Following the table literally would not be a faithful projection of frozen C4. Quietly replacing three names would alter the fixed taskbook's stated contract responsibility. Treating them as synonyms, introducing another relationship model, moving missing duties into other primary modules, or editing the frozen spec is not an authorized resolution.

Section 4.1 calls the modules candidates and permits evidence-backed merging; it does not explicitly authorize redefining the four Core relations. Section 5.2's loading issue is a consequence of the same unresolved relation boundary, not counted as a second independent P0.

## Requested ADMIN clarification — proposed correction, not applied

1. Confirm relations projects only **parent / branch_of / subject_ref / references** from F4.5.1. Exclude blocks / relates_to / supersedes as v4 Core relation names.
2. Clarify that ordinary sequential work must retain applicable parent/subject_ref/references guidance and gate validation. Branch-specific semantics and convergence are explicitly selected; ordinary relation semantics must not disappear merely because Branch is not selected.
3. Publish the correction in a fixed taskbook or an explicit fixed ADMIN decision, retaining the frozen spec unchanged. Then resume the remaining WP4C.1 contracts and all required mappings.

No recommendation here changes Core, adds a new module implementation or signs any Gate.

## Other scope decisions already clear

- WP4C.0 baseline Gate at 65ed07263de707d327e6e2c358aec2dd7c00a6df remains valid.
- Scope correction abc2dc06db227dbc81afbd554c372271c05e89da excludes the CodeFlowMu v1.0-rc.1 source. Its body was not read, copied, translated, adopted, bundled or projected in this task.
- The current taskbook §5.3 permits absent general constitution authority without substituting CodeFlowMu RC. This is NOT a renewed constitution-license prerequisite blocker.
- Ordinary business guidance and FCoP repository development guidance stay separate. Neither receives any new text here.
- Prior six audit files match the accepted 59a6654dbb5387201056004c06068f8afcafb9ed blobs exactly. Prior counts are accepted audit inputs, not completed WP4C.1 contract decisions.
- Only factual reports and their Manifest are delivered. All remaining contract decisions remain unperformed after the hard stop.
