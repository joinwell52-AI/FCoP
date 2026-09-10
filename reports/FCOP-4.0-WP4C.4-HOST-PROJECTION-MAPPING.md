# WP4C.4 Host projection and adoption mapping

Status: local implementation and verification complete; final run results are recorded in RESULT. Remote delivery and ADMIN acceptance remain separate.

Authority: [fixed WP4C.4 taskbook](https://github.com/joinwell52-AI/FCoP/blob/01c53355293c08f100b9f6e5aba0caea015d27cd/taskbooks/fcop-4.0/WP4C.4/01-Host-Projection-Adoption-Deployment-and-Rollback-Taskbook-v1.0.zh.md). Frozen RD contract: f6831de12991010f22672fb6e776ce85ef1507ff. This report does not modify it or sign a Gate.

## Single public boundary

`Project.rule_distribution(*, action, request)` retains its accepted signature. Only its private dispatch changes. Existing validate, select and validate_operation_scope retain their original handlers. Eight Toolkit error identities are retained; no Base error is added. The only legacy facade adjustment is the taskbook section 5.1 narrow adopt-version rejection. It does not redeploy legacy rules or rewrite Core errors on other actions.

| Action | Single primary implementation | RD / taskbook | Permitted effects |
| --- | --- | --- | --- |
| inspect_profile | _profiles.inspect_profile via _deployment.dispatch | RD-11/12 | none |
| status | _deployment.dispatch | RD-11 | none; independent facts only |
| adopt | _receipts.adopt | RD-09 / section 5.1 | one immutable adoption identity |
| plan | _projection.plan | RD-13–16 | none, including no coordination file |
| apply | _deployment.apply / _commit_targets | RD-10/16 | explicitly selected Host targets and private evidence |
| verify_deployment | _receipts.verify_deployment | RD-10/14 | none |
| rollback | _deployment.rollback / _commit_targets | RD-10/16 | immediate verified backup restoration, new receipts |
| inspect_failure | _deployment.inspect_failure / _observe | RD-16 | none; never replay |
| rollback_partial | _deployment.rollback_partial | RD-16 | only recorded changed targets, explicit restoration fact |

All paths above are under src/fcop/v4/rule_distribution. Additional private responsibilities: _files supplies safe relative paths and immutable I/O; _profiles owns strict static profiles; _receipts owns immutable evidence validation; _projection owns deterministic framing; _deployment owns physical commit/recovery. These are not new facades, services or registries.

Implementation anchors: [static Profile validation](../src/fcop/v4/rule_distribution/_profiles.py#L20), [adoption](../src/fcop/v4/rule_distribution/_receipts.py#L150), [pure plan](../src/fcop/v4/rule_distribution/_projection.py#L47), [apply](../src/fcop/v4/rule_distribution/_deployment.py#L241), [shared physical commit](../src/fcop/v4/rule_distribution/_deployment.py#L301), [verification](../src/fcop/v4/rule_distribution/_receipts.py#L264), [failure inspection](../src/fcop/v4/rule_distribution/_deployment.py#L368), [partial restoration](../src/fcop/v4/rule_distribution/_deployment.py#L373), [rollback](../src/fcop/v4/rule_distribution/_deployment.py#L404), [independent status](../src/fcop/v4/rule_distribution/_deployment.py#L475). These line anchors refer to the Content Commit bound by the delivery Manifest.

## Static profiles

| Host | Exact target | Initial version / mode | Full target bound | Entry framing |
| --- | --- | --- | --- | --- |
| codex | AGENTS.md | 1.0-candidate.1 / bounded_embed | 65536 bytes | Markdown managed region |
| cursor | .cursor/rules/fcop-v4.mdc | 1.0-candidate.1 / bounded_embed | 65536 bytes | frozen Cursor frontmatter plus managed region |
| claude-code | CLAUDE.md | 1.0-candidate.1 / bounded_embed | 65536 bytes | Markdown managed region |

Profiles are explicit local raw JSON inputs, not discovered or bundled defaults. No optional bundled Profile files were added. Single language is en or zh; unknown fields/identity/mode, duplicate keys, BOM/CRLF, executable logic and probes reject. A reference-fixture.1 profile requires the fixed local RD-14 evidence before adoption, with its 8192-byte bound. Subsequent deployment binds its adopted raw Profile hash; it does not infer real Host consumption from that test evidence.

Support, explicit adoption, generated entry and runtime consumption are separate outputs. `runtime_consumption_verified` remains None even when an entry or caller consumption file exists. Profile selection is not F4.7 authorization and never registers an evaluator.

## Receipt and byte bindings

Adoption uses exactly the 13 RD-09 fields and content-addressed canonical UTF-8/LF bytes at fcop/internal/rule-distribution/adoptions/&lt;sha&gt;.json. It binds explicit workspace/version, complete selection, Manifest/Profile identities, verified local ADMIN selection reference, explicit timezone-aware recorded_at as adopted_at and the entire previous receipt chain. `actor=ADMIN` is insufficient. Adoption writes no Host entry, package snapshot, workspace profiles, task or lifecycle event. Exact retry returns the existing identity.

Deployment uses the eight RD-10 fields and five-field target entries. Targets, backups, package/profile snapshots and receipt references use workspace-relative paths. Snapshots contain the Manifest and all 18 canonical artifacts, even though only selected artifacts are projected. All historical receipts/backups/snapshots are read-only evidence; no mutable latest pointer is introduced. A unique history tail is derived from verified predecessor references, not file times.

The two framing modes preserve source bytes. Bounded embedding uses the exact package/Manifest/Host/assembly/language header and per-module digest markers. Reference output uses ordered POSIX links relative to the target directory into the immutable package snapshot. Verification reconstructs the expected managed bytes from the verified snapshot, so link target, order and artifact digest cannot be substituted. Unresolved source-relative references are rejected, not relocated or downloaded.

Plan checks the complete package, Profile, explicit adoption when supplied, history and target ownership. It returns selected modules/languages, before/after hashes, after_bytes, full size, deterministic unified diff, planned_backups and planned_receipt. It creates no directories, locks, receipts, backups, snapshots or logs. Different machine roots and request times do not change target bytes or hashes.

Owned updates require one complete, non-nested managed block matching previous owned bytes. User prefix/suffix bytes are preserved exactly; verification separately checks the complete deployed target hash. Rollback restores the exact captured before bytes, including legitimate user bytes added between deployments; a previous receipt owns its managed region, not subsequent user edits. Initial absent-target rollback removes only a still-unchanged managed-only entry. Existing unmanaged targets, fake/incomplete markers and active legacy Cursor inputs reject.

## Isolation and evidence limits

All generated AGENTS.md, CLAUDE.md and Cursor files belong to disposable test sandboxes. No real repository Host entry or D:/FCoP dogfood file is a deployment target. No MCP/Relay, Schema, rule body, frozen test, package version, release workflow or CodeFlowMu file is changed. New private Python modules are included by existing packaging rules; no runtime dependency or package-data policy change is needed.

Native verification is Windows/Python 3.12.9. Linux/macOS are NOT_NATIVE_VERIFIED without native runners; local type checks and builds are not substitutes. GitHub CI status is reported from the final review HEAD, not borrowed from a prior taskbook or Gate.
