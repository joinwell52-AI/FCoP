# WP4B resumed implementation plan

WP4B.3a fixture authority: `74f0150eee88bcef754fbd5182d2eba9836a04ec`,
SHA-256 `0b0aeb030b3879157b14353e5ee259d2f0ed7dd036c4561edd24c4cbade68cb3`.
Its frontmatter input_head/amends_taskbook_commit repeat the mistyped
`8a9312999788dd13c8c393ee403c8837130a0960`; the actual fixed Git parent
is `8a93129997883aa2013e4d2c412e568fe4d44e8a`. This discrepancy is preserved,
not silently edited. Section 7 explicitly resumes the current dirty review
worktree and requires this taskbook in the delivery parent chain. The real
parent, taskbook-only delta and all 28 dirty file bytes were verified before
fast-forward. No invalid metadata SHA was substituted for a Git object.
Only C2-R02's local Arrange/Act and additional assertions are changed;
global driver/fixtures and all existing assertions remain unchanged.

Current authority: WP4B.3 at `8a93129997883aa2013e4d2c412e568fe4d44e8a`, SHA-256
`df3f979eadc4e72469e3d658502b270c06215a4a060f18002963e218d78aa7d3`.
The fixed GitHub bytes and parent f98027d were verified; all 24 dirty files
were hashed and preserved byte-for-byte across the taskbook-only fast-forward.
First add real authorization-append boundary tests, extract one trusted Profile
validator shared with transition consumption, complete only the existing v4
mark_human_approved method, and route MCP directly to it. Keep generic
write_review unchanged. Re-run REPORT and all full regression suites.
The old C2-R02 fixture's unbound approval request will be checked explicitly;
no default authority or assessment fallback may be introduced to keep it green.

Continuing authority: WP4B.2a at `ed8212cefeccf2e0d2a49b8802386758fd17475a`, SHA-256
`97a1ffe5def18d90199255adce718e00ffa22f74653ea575eb060ec4c9a33b0e`.
WP4B.2 enables only the two existing public REPORT readers; WP4B.2a permits
only the zero-head error-code correction in their shared lifecycle resolver.
WP4B.1 at `e885135f4b074845944a7b8b799de879549fbc33` retains its exact T6 mapping.
WP4B.0 and original WP4B remain applicable except their explicitly superseded
template, Relay dependency and tool-count clauses. Scope: `WP4B_RESUME_ONLY`.

The accepted blockers remain preserved in Git history. ADMIN supplies the
decision; ME implements and reports without signing the acceptance Gate.

## Sequence and boundaries

1. Add executable Profile/template, explicit Relay and T6 surface tests first.
2. Use one server-owned workspace router and immutable trusted Profile registry.
   Classify only declared workspace identity; initialization is an explicitly
   separate bootstrap action. Never fall back from v4 to a legacy writer.
3. Preserve all 45 legacy names and add only the fixed `reopen_task` mapping.
   Optional v4 inputs may extend legacy tools without tightening legacy inputs.
4. Delegate business validation and writes to the accepted Project API. Preserve
   structured Core errors and separate authorization creation from consumption.
5. Keep three Profile resource templates read-only; route current specifications
   by workspace version; mark undelivered v4 rules unavailable.
6. Record transitive dependencies honestly. Base stdio must not activate Relay;
   Relay must have an explicit entry, configuration and lazy dependency loading.
7. Keep historical 45-item snapshot unchanged. Add a v4 46-item snapshot and
   prove the exact additive difference, six reopen parameters and no close_issue.
8. Run the full authorized local regression, package and isolated installation
   checks, then deliver Content + Manifest commits to Draft PR #15 and verify
   remote bytes and all final-HEAD GitHub CI before requesting the Gate.

The WP4B.3 validated authorization append/shared Profile helper,
WP4B.2 public-query allowlist and WP4B.2a zero-head Core correction
extend the original MCP-only write set. Frozen specification, Schema,
Conformance except the WP4B.3a local C2-R02 correction, rules package,
CodeFlowMu, main and releases remain out of scope. A demonstrated
hard-stop condition takes precedence over completing the above sequence.

This file is a plan, not a completion or test-pass claim.

## Executed resumption checkpoints

- Fixed GitHub taskbook bytes matched their published SHA-256 before fast-forward.
- Public query tests first produced 9 failures / 7 passes on the unmodified input.
- The implementation then passed 16/16 directed cases, and 68/68 with additional
  real concurrent writer cases plus existing T3 lifecycle regression.
- The 14-file ZIP was checked against its fixed SHA-256, exact entry allowlist,
  paths, symlink mode and CRC. Every entry was decoded and hashed; restoration
  used UTF-8 text with LF checkout normalization. No Core file exists in that ZIP.
- MCP reads now call public Project queries; no private resolver is imported
  by the adapter. Earlier read-only file scanning was removed for REPORTs.
- Further full-suite, artifact and GitHub results belong to final reports;
  the checkpoints above do not claim whole-WP4B completion.

## Final local checkpoint

- Core full suite: 1256 passed; frozen Conformance: 119 passed; MCP: 134 passed.
- Authorization/REPORT/lifecycle directed suite: 114 passed.
- AST audit: C2-R02 keeps all 6 old assertions and adds 14; outside-function
  syntax trees and global driver are unchanged.
- Ruff and strict mypy passed. Final clean wheel stdio/Relay probes passed;
  source/wheel/sdist payload parity and 24 unchanged Schema JSON files verified.
- SDK startup banner disabled to prevent its optional PyPI update query in
  offline stdio. Only the Windows stdlib self-pipe is exempted from the probe's
  socket audit; no arbitrary endpoint is exempted.
- TASK/REVIEW relation and binding filters remain plain public-reader projections.
  An initial extra thread_key filter test failed because this Profile/Legacy
  field is not a Core relation; the unneeded new filter was removed, not added
  to Core. The corrected complete MCP suite passed 134/134.
- Next: explicit allowlist Content Commit; Manifest-only child; push the
  existing Draft PR; read back every remote blob and await all final-HEAD CI.
  No local test result signs the requested Gate.
