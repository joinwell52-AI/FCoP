# WP4C.5B Legacy and Five-Layer Isolation

## Boundaries

This implementation is confined to the existing Project distribution entry,
two private read helpers and MCP resource representation/registration. Core,
Schema, canonical rule bytes, Host adoption/apply/rollback semantics and the
public method set are unchanged. No automatic consumer update is implemented.

Legacy calls revalidate the workspace with existing strict classification:
duplicate JSON keys and invalid UTF-8 do not reach a writer. Explicit known
legacy declarations keep their compatibility, including CRLF classification.
Unversioned legacy redeploy delegates `Project.deploy_protocol_rules(force=False)`
after preflighting the existing four targets. There is no new legacy writer,
no v4 internal receipt tree and no overwrite of existing Host files. An explicit
v4 request on v3 returns RULE_ADOPTION_REQUIRED before any writer. Invalid or
contradictory versions fail closed; resource requests cannot install evaluators.

For v3 rules/protocol, Project content and MCP content are the original getter
strings, including their complete UTF-8 bytes, with text/markdown MIME. No
banner, pseudo-string, JSON object or trailing metadata is added. v4 returns
the separately defined typed results and never falls back to legacy rules.

## Five independently measured facts

| Layer | Source | Returned fact / no inference |
|---|---|---|
| disk | current validated Manifest bytes | disk_manifest_sha256 |
| process/index | a new uncached read on each action | index_manifest_sha256, uncached_current_read |
| adoption | verified Adoption Receipt chain | adopted_manifest_sha256; no automatic adoption |
| Host entry | verified deployment history plus present full target bytes | actual sha256, recorded_sha256, drifted |
| Runtime | no separately authorized consumer proof exists | runtime_consumption_verified=None |

`inspect_layers` uses the existing adoption/deployment/immutable-history
validators. It does not apply, roll back, repair, rewrite or create a cache.
An updated valid package changes disk/index hashes while the old adoption and
Host bytes stay bound to old receipts. Recreating Project does not imply new
adoption. Modified Host bytes are explicitly reported as drift; a corrupt
receipt is rejected rather than accepted as evidence of deployment.

## Negative and positive evidence

The ordinary `test_v4_rule_distribution_reads.py` covers both version shapes,
all four language/assembly combinations, exact source order and hashes,
noncanonical URIs, forbidden request fields, changing Manifest/spec/module
bytes, disk updates, retained adoption, Host drift and corrupt receipt history.
Before/after snapshots include the caller workspace and external test inputs.
The immutable Conformance targets DIST-23/24/26/29 exercise the same production
entry. Full-suite results are in RESULT; no assertion or Test ID is renamed.

The older unit expectation that `shadow` is an unimplemented future action is
retired only for that newly implemented action. Its negative security contract
now has real authorized and rejected Shadow tests; `measure_context` and
`build_artifacts` remain unavailable and their original unit checks remain.
This is an ordinary non-frozen test update, not a modification of future-stage
behavior expectations or an early WP4C.6 implementation.

No runtime-consumption claim is made for local Host files, MCP resource reads,
installed wheels or CodeFlowMu. The actual downstream product has separate
startup behaviors; those are source evidence only, not adoption authority for
FCoP and not permission to modify CodeFlowMu.
