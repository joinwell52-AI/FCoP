# WP4C.6b resumed implementability proof

Scope: WP4C_6B_EXCEPTION_CATCH_CORRECTION_AND_WP4C_6_RESUME_ONLY. Local evidence below does not imply final native CI acceptance. RESULT and the final remote receipt distinguish pending checks from PASS.

## Authority and preserved failures

Original taskbook: dc4bd62d47c3c422c8e758b588369dd3ed089acd, SHA-256 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e.
WP4C.6a ruling: cd0fe4df900c3ff0b34beca957097f87a8d4b150, SHA-256 988738c5f175fd8ed91f4d9f32772282e79ef3caba6675c6b7ebb0facccb4aba.
WP4C.6b erratum: 8162d6ae9a91b8b23a6698bfd292a2cb2a75194c, 5334 bytes, SHA-256 4fbf32c198f4ee624d55bd149c4152e3382894623c638b1001f943849900e306.

PR #29 HEAD 91e64fa0a0ee377335af3226263a1811e1a56c1d stopped on a pre-WP4C.6 absence sentinel. WP4C.6a superseded that sentinel but prescribed the wrong exception catch. PR #30 HEAD 576bad0025038ee085fc53da46c125143d126bd3 preserved the resulting two failures. These real intermediate failures remain in Git history; neither reports-only CI nor older-stage test passes are used as implementation acceptance.

The existing public hierarchy is FcopError with sibling subclasses V4ProtocolError and private _DistributionError. Both actions already returned exact toolkit:RULE_SELECTION_INVALID without effects. ADMIN corrected only the catch, not production inheritance or behavior. See src/fcop/errors.py:84 and src/fcop/v4/rule_distribution/_errors.py:15.

Failed local alignment SHA: b0a77d2b84d51e435a5dd7b171554e83005023ed1d8e7568fbd5d863a832ad3e.
Successful SHA: 1905cc752c455b41d77defb41a4dd7a21d1fba3a1d51850dd74d7390e0b97bc2.
Alignment commit: 22e2f558d3980d5647a1669e9455e4dacb60bc85.

Against the failed local input only the catch changed. Against the Git parent this commit also contains the previously authorized, uncommitted WP4C.6a function-name and code replacements: three line replacements in one file, not a one-line Git diff. Imports, both parameter nodes, fixture/call/snapshot helpers and every zero-effect assertion remain intact. Fresh alignment result: 2/2, zero failure/skip.

The user's explicit clarification identifies the erratum as the current PR #30 HEAD; the older HEAD in erratum section 2 is retained as historical input. Original/recovered eleven candidates matched the PR #29 inventory before resumption and were not changed by this continuation.

## Narrow implementation

| Responsibility | Evidence | Boundary |
| --- | --- | --- |
| Two dispatches | src/fcop/v4/rule_distribution/__init__.py:41 | Existing Project.rule_distribution; no new facade |
| Offline export | src/fcop/v4/rule_distribution/_artifacts.py:120 | Full loader validation, explicit ordinary local output, deterministic archives, exclusive writes and byte verification |
| Measurement | src/fcop/v4/rule_distribution/_measurement.py:30 | Six explicit hash-bound inputs; raw identity recheck; read-only |
| Full projection | src/fcop/v4/rule_distribution/_projection.py:47 | Shared new_entry/framed, including Cursor frontmatter; no duplicate algorithm |
| Bilingual evidence | _profiles.py:20 and _selection.py:81 in the same package | Private measurement_only admission; effectful plan/adoption admission not expanded |

Only two private production modules are new. Export uses standard-library ZIP/TAR/GZIP and static carrier metadata. The content-addressed fcop-rule-data identity is an offline data carrier, not a project-version change, installed FCoP runtime replacement or release. Each archive contains exactly nineteen canonical data members plus carrier metadata. It excludes Host entries, receipts, workspace identity and CodeFlowMu content. No build backend is imported or executed; no shell, network, installer or publisher is called.

Invalid input, changed package and unsafe/occupied output are rejected before output creation. Authorized output I/O failures are surfaced for inspection; no new atomic publication/recovery guarantee is invented.

Measurement counts complete UTF-8 projection bytes, not tokens. runtime_consumption_verified remains null. The reviewed bilingual fixture is accepted only for read-only measurement; the real-projection ordinary tests also reject its effectful plan requests.

## Verification and frozen boundaries

Fresh targets passed 20/20, full distribution 176/176 and Core 119/119. The 62 new ordinary nodes cover actual archives and public operations, repeat determinism, negative input/path/hash cases, zero effects, native indirect paths, eighteen projections, v3 rejection and the existing 46/12/4 MCP snapshot. No success result is mocked.

Frozen distribution tree remains 4f99c7261b63b6db81c500604a231defaca9f14b; frozen Core test tree remains 24ab264c6bca9a3183ee270becb552f22a4c4f9e. Both Conformance directories, frozen specifications/contracts, Schema, MCP source, error classes, versions, dependencies and release workflow are unchanged. No new public API, Base error, Runtime dependency, background component, authoritative store, state machine, Host discovery or automatic migration is introduced.

Workflow candidates add only native target execution and installed artifact/stdio probes. Branch filters, existing checks and failure thresholds are not weakened. Native final-HEAD execution is a separate mandatory requirement; local passes do not satisfy it.

WP4C_RULE_DISTRIBUTION_ACCEPTED: false
