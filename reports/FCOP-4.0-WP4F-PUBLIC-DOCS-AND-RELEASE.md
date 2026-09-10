---
protocol: fcop
version: "3.0"
sender: ME
recipient: ADMIN
subject: WP4F public metadata and release execution boundary
---

# Stable public documentation and release plan

## Candidate descriptions

`fcop-README.pypi.md` is the Core package long description;
`mcp/README.md` is the separate MCP package long description. They explicitly
identify their separate package roles, 4.0.0 install commands, unchanged
protocol semantics and no automatic workspace migration. MCP documents
46 tools / 12 resources / 4 templates, `reopen_task`, trusted startup Profile
registration and the dependency `fcop>=4.0.0,<4.1.0`. Historical 3.x guidance
and the canonical install prompt remain identifiable as historical material,
not a Stable upgrade instruction. Relative links in the PyPI MCP description
are replaced by repository URLs. Root English/Chinese README commands and
links are checked for parity and the Python example is executed.

The new `docs/releases/4.0.0.md` and CHANGELOG record Stable promotion, retain
the published RC history and add no new protocol or runtime functionality.
The package metadata audit verifies both wheel and sdist descriptions against
their corresponding UTF-8 README, exact version, classifiers and dependency.

**Phase A cannot truthfully confirm that public PyPI pages already show
4.0.0:** publishing is gated in Phase B. Phase A verifies the exact payload to
be published. `scripts/wp4f_public_reinstall.py` performs the actual public
check after upload: both version-specific and latest project JSON, README
description, Repository URL, MCP dependency, all four public hashes, fresh
installation and actual stdio MCP execution. This pending public step is not
counted as a Phase A success.

## No-upload dry-run

The Stable build workflow invokes `scripts/wp4f_release_guard.py` against the
real candidate set. Its default `dry-run` returns `upload_authorized=false`,
`uploads_executed=0`, `releases_created=0`. It validates all four filenames,
sizes, hashes, source content, execution HEAD and machine Manifest hash.
The release workflow retains separate `verify` and conditional `publish`
jobs; a dry-run never enters `fcop-pypi` or uploads a package.

## Single readiness Gate, then Phase B

The final review receipt must bind the exact accepted HEAD, candidate content,
successful artifact run, machine Manifest hash and four artifact hashes, and
request only `FCOP_4_STABLE_RELEASE_READY`. This report does not sign that Gate.

After that authorization, the sequence is:

1. Preserve full review history when merging main. Create `v4.0.0` at the
   exact accepted execution HEAD, not an inferred merge commit or moving ref.
2. Preserve the existing RC tag and environment policy. Add an exact Stable
   tag deployment policy if required by `fcop-pypi`; retain same-account human
   ADMIN approval. No independent GitHub account is required, and the executor
   does not approve the deployment on ADMIN's behalf.
3. Dispatch the release workflow with the accepted identities and signed
   comment. After human environment approval, revalidate the binding and upload
   the fixed Core pair and MCP pair without rebuilding or `skip-existing`.
4. Download the public four artifacts and verify SHA-256; verify latest Stable
   pages/metadata and fresh-installed actual MCP behavior.
5. Create the formal GitHub `v4.0.0` Release from those same bytes, retaining
   `v4.0.0rc1` and its artifacts. Upgrade/restart the actual local MCP only as
   described in the separate environment plan, then write the final receipt.

The workflow uses the already accepted Twine 7.0.0 and packaging 26.3 toolchain.
No credentials are embedded in source or reports. MCP Registry, Zenodo,
CodeFlowMu and subsequent development remain outside this task.
