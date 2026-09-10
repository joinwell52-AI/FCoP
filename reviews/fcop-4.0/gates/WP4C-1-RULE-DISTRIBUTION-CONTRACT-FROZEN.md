---
gate: "WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN"
status: "SIGNED"
authority: "ADMIN"
date: "2026-09-07"
accepted_review_head: "f6831de12991010f22672fb6e776ce85ef1507ff"
accepted_content_commit: "6122dca08e3eb093fc015a1b6e884bf2de0bd388"
taskbook_commit: "7f973dc5f32bc6b9e1076184d1247c55a1349bd5"
frozen_fcop_contract_commit: "aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6"
implementation_authorized: false
wp4c_2_authorized: false
main_merge_authorized: false
release_authorized: false
---

# WP4C.1 Rule Distribution Contract Frozen

## ADMIN decision

```yaml
WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN: true
DECISION: ACCEPTED
ACCEPTED_REVIEW_HEAD: f6831de12991010f22672fb6e776ce85ef1507ff
ACCEPTED_CONTENT_COMMIT: 6122dca08e3eb093fc015a1b6e884bf2de0bd388
P0_OPEN: 0
WP4C_2_AUTHORIZED_BY_THIS_GATE: false
MAIN_MERGE_AUTHORIZED: false
RELEASE_AUTHORIZED: false
```

ADMIN accepts the WP4C.1a contract package delivered in Draft PR #19.

This Gate freezes the rule-distribution contract at the exact review HEAD above. It does not merge any branch, implement the contract, authorize WP4C.2 by itself, adopt any Host profile, deploy any Host entry, migrate any workspace, modify CodeFlowMu, or authorize a release.

## Accepted contract decisions

1. FCoP 4.0 Base Core relations are exactly `parent`, `branch_of`, `subject_ref`, and `references`.
2. `blocks`, `relates_to`, and `supersedes` are not v4 Base Core aliases or implicit gate encodings.
3. `relations` is part of the sequential and parallel common base.
4. `convergence` is the sole parallel increment over the sequential assembly.
5. Nine canonical rule modules, a package Manifest, a separate workspace adoption receipt, static Host profiles, and deterministic `reference` / `bounded_embed` projections are contractually separated.
6. FCoP repository-development guidance is separate from ordinary business guidance.
7. CodeFlowMu's `Agent原生软件工程宪法-v1.0-rc.1` remains CodeFlowMu-transition-only and is not an FCoP Rule Package source or authority.
8. Host adapter support, ADMIN adoption, entry generation, and verified Runtime consumption remain four separate facts.
9. Rule distribution adds no lifecycle authority, database, daemon, watcher, scheduler, session manager, remote rule center, or automatic latest-version adoption.
10. Legacy 3.x and v4 selection remain explicitly isolated.

## Review evidence

The accepted GitHub delivery contains exactly six paths. The Content commit is exactly one commit after the fixed taskbook; the Manifest commit is exactly one commit after Content.

| File | SHA-256 |
|---|---|
| docs/fcop-4.0/rule-distribution-contract.md | eab5bbae87a2da73bb4f3f11b7e742f3805e81d06e6c186682cbf5ac9b46e757 |
| docs/fcop-4.0/rule-distribution-contract.zh.md | 30fd7ad62b77acd887ce578a695890f84cdf2b961b1a525177f3243ccc27613f |
| reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md | 4c76d63c011532022d979d5cbca5b00600fffd887f679e8fd34d3b9c886bfbc4 |
| reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md | cad785cfc87c91007df1f8bb831e5c620a2eae3f328bd1b9d491d208e1ba4844 |
| reports/FCOP-4.0-WP4C.1-RESULT.md | 1fefd94f9f6052f9e507ec3238a64c798d0e9e28497445cd4d239a9040c867cd |
| reviews/fcop-4.0/wp4c.1/MANIFEST.md | cf209e49c13aa3aa3e7e7cc8b32b6ab7fbc83a76ef6056288dad20a2932bfe00 |

Independent ADMIN review confirmed:

- bilingual contract IDs: 24/24;
- frozen-clause primary mapping: 73/73;
- legacy rule disposition: 147/147;
- path ownership: 86/86;
- Host/consumer mapping: 12/12;
- Core relation set: 4/4;
- assembly profiles: 3/3;
- exact six-file hash agreement: 6/6;
- delivery scope and two-commit ordering: PASS;
- frozen specifications, implementation, tests, Host output, CodeFlowMu and main: unchanged.

## Preserved limits

The 30 DIST rows are future behavioral-test obligations, not executed tests. Candidate Host profiles and byte caps are contract choices, not proof of Host Runtime support. Runtime consumption remains unverified. No rule generator, package build, deployment, rollback, downstream shadow test, main merge, or release was authorized or performed by WP4C.1a.

A separate fixed taskbook and explicit `WP4C_2_ONLY` authorization are required before writing Conformance tests.
