# WP4C.6 context measurement evidence

Scope: WP4C.6 resumed by ADMIN erratum 8162d6ae9a91b8b23a6698bfd292a2cb2a75194c. This is local measured evidence, not native CI or Runtime consumption acceptance.

## Actual public behavior

Existing Project.rule_distribution(action="measure_context") verifies the complete canonical package, explicit static Host profile, selection and exactly six local hash-bound historical files. It reuses the accepted pure projection framing; it does not render a second algorithm or inspect a live Host.

Returned disclosure is fixed:

```yaml
limit_unit: utf8_bytes
estimator:
  algorithm: exact-utf8-byte-count
  version: "1"
runtime_consumption_verified: null
```

Source: src/fcop/v4/rule_distribution/_measurement.py:30 and _projection.py:47. Rejection covers absent/extra/duplicate inputs, mismatched raw hashes, changing identity, directories, network paths and indirect/reparse paths. Source/package/profile/history are rechecked before returning. Neither measurement nor rejected inputs create a workspace/Host entry, receipt, cache or output.

## Eighteen real canonical-package measurements

These numbers use the ordinary test's actual canonical nineteen-file package, not the smaller synthetic module bodies of frozen DIST-28. Fixture source: tests/test_fcop/test_v4_rule_distribution.py:25; direct public calls and full-byte oracle follow test_measure_18_real_projection_bytes in tests/test_fcop/test_v4_rule_distribution_closeout.py. Additional report probe: C:/Users/Administrator/AppData/Local/Temp/fcop_wp4c6b_context_probe.py. Its first and repeated executions both completed successfully.

The exact inputs are bounded_embed, candidate profile 1.0-candidate.1 for a single language, and explicit-bilingual-fixture.1 for read-only bilingual measurement. Sequential selects the eight business modules; parallel additionally selects convergence. All use the canonical Manifest SHA-256 7efb1ba14df4d1ffbe164b8ec85dbf4316e7da4c0f367f3a506c78e4e29862d4. Six explicit CRLF historical fixtures have sizes 18, 36, 54, 72, 90 and 108 bytes. Historical CRLF bytes are measured as supplied, not rewritten into canonical module encoding.

| Assembly | Static Host | Languages | Complete UTF-8 bytes | Zero effect |
| --- | --- | --- | ---: | --- |
| sequential | codex | en | 19867 | PASS |
| sequential | codex | zh | 18140 | PASS |
| sequential | codex | en+zh | 37806 | PASS |
| sequential | cursor | en | 19935 | PASS |
| sequential | cursor | zh | 18208 | PASS |
| sequential | cursor | en+zh | 37874 | PASS |
| sequential | claude-code | en | 19873 | PASS |
| sequential | claude-code | zh | 18146 | PASS |
| sequential | claude-code | en+zh | 37812 | PASS |
| parallel | codex | en | 22266 | PASS |
| parallel | codex | zh | 20370 | PASS |
| parallel | codex | en+zh | 42437 | PASS |
| parallel | cursor | en | 22334 | PASS |
| parallel | cursor | zh | 20438 | PASS |
| parallel | cursor | en+zh | 42505 | PASS |
| parallel | claude-code | en | 22272 | PASS |
| parallel | claude-code | zh | 20376 | PASS |
| parallel | claude-code | en+zh | 42443 | PASS |

Each row compares the real public result with complete new_entry(framed(...)) bytes and compares the entire fixture tree before/after the read. The values include begin/end markers, module markers, header, blank lines, final LF and (for Cursor) frontmatter. They are not source-body-only totals or token estimates. Bilingual measurement does not authorize deployment or plan: ordinary regression explicitly rejects the same measurement-only profile on an effectful path.

## Independent frozen and negative tests

Fresh DIST-28 passed 18/18 against its independent literal expected_embed oracle. DIST-27/28 together passed 20/20 and full Rule Distribution passed 176/176, without changing any frozen assertion, fixture, driver or ID. JUnit target SHA-256: f4a8796f1e587e71a4042d7704f734eff1cb84352b9a3697873627d3e86310d7. Full distribution SHA-256: 3e5434fe42f79c365a56b797933b53f666774662b5176c72c683beff706ba904. File locations and exact commands are recorded in RESULT.

The new ordinary eighteen-node matrix, duplicate/missing/hash/path mutation cases, changed-history identity probe, native Windows junction test, shell/network prohibition and legacy CRLF fail-closed cases passed within the fresh FCoP regression. Host names are static input identifiers, not detected apps. No claim is made that a model loaded or consumed these bytes.

## Preserved history and remaining gate

PR #29's sentinel blocker and PR #30's sibling-exception blocker remain preserved at 91e64fa0a0ee377335af3226263a1811e1a56c1d and 576bad0025038ee085fc53da46c125143d126bd3. Their NOT_RUN continuation states were accurate then; this report records the new 6b runs after the authorized catch alignment.

Local native evidence is Windows/Python 3.12. Cross-platform equality and final native matrix acceptance require the final Manifest HEAD CI; pending/failed/untriggered jobs are not PASS. No exact whole-archive cross-platform digest or Runtime consumption claim is inferred from these local measurements.

CONTEXT_MATRIX: 18/18
CONTEXT_ESTIMATOR: exact-utf8-byte-count/v1
RUNTIME_CONSUMPTION_VERIFIED: null
WP4C_RULE_DISTRIBUTION_ACCEPTED: false
