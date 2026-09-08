# WP4C.6 context measurement

Status: BLOCKED by the later historical ordinary-test absence assertion. Frozen target matrix, full distribution and Core passed; final regression/native verification is incomplete and stopped.

## Exact meaning and reuse

`measure_context` returns the full new-entry projection's UTF-8 byte size, including existing framing, final LF, module headers and Cursor frontmatter. It calls the accepted `_projection.framed` function and the extracted, shared `new_entry` prefix helper. Deployment planning uses the same helper with unchanged semantics. No alternate projection algorithm, token counter, model lookup, Host probe or Runtime exists in this path.

Fixed disclosure is `limit_unit=utf8_bytes`, `estimator={algorithm: exact-utf8-byte-count, version: "1"}`, and `runtime_consumption_verified=null`. This measures an explicit static selection, not actual process injection, context availability or consumption. It does not inspect or modify existing Host files, adoption/deployment receipts or user regions.

## Matrix and trusted scope

The frozen DIST-28 function passed all **18/18** combinations: sequential/parallel × codex/cursor/claude-code × en/zh/en+zh. Its independent expected-byte oracle compares the full projected byte length, selected modules/languages, estimator disclosure and all six historical sizes. The ordinary tests separately compare the public result with the real shared projection.

The explicit bilingual profile version from the fixed task/frozen input is accepted only in this measurement path. Existing profile validation and module selection default to their prior policies for all other callers. Ordinary negative tests confirm the bilingual measurement does not make planning/deployment available. Candidate adoption remains one language; no profile field or deployment/rollback contract changes.

JUnit target evidence: `C:/Users/Administrator/AppData/Local/Temp/fcop-wp4c6-target-01.xml`, SHA-256 `dbbfbb5f3e7a7ca7d630a143b1247f9baaa742a28691b2f9e24062cba87d1529`; 20 total target passes in 109.74 seconds, including the two artifact tests. Target selection deselected eleven unrelated functions in that file; this is not a skip/xfail or a claim of full-suite completion.

## Historical facts and effects

Exactly six ordered, unique explicit path/hash inputs are accepted. Each entry has exactly path and lowercase SHA-256. Regular-file/ancestor checks reject indirect/network paths; repeated byte and identity checks reject observed changes. Historical bytes are counted as supplied (including historical CRLF or non-ASCII), not normalized into canonical rule Encoding. Returns contain only path/hash/byte count, never the bodies.

The ordinary tests exercise missing/duplicate/extra-field/hash/absent/directory/network inputs, in-flight byte drift and native indirect paths. Windows uses an isolated junction; non-Windows uses a real directory symlink. All rejection checks compare before/after sandbox contents. Measurement performs no writes or network calls. Evidence proves these observed calls' effects, not indefinite external-file immutability.

Final native platform matrix and full regression remain required; until then this report does not claim cross-platform acceptance or a signed distribution Gate.
