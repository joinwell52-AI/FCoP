# PyPI description sources / PyPI 项目说明源

This directory records how the two FCoP PyPI project descriptions are maintained.
The descriptions themselves stay beside the package build configuration so the
same files are included in source distributions and rendered by package builds.

## Canonical sources

| PyPI project | Canonical GitHub file | Build binding |
| --- | --- | --- |
| [`fcop`](https://pypi.org/project/fcop/) | [`/fcop-README.pypi.md`](../../fcop-README.pypi.md) | Root `pyproject.toml`: `readme = "fcop-README.pypi.md"` |
| [`fcop-mcp`](https://pypi.org/project/fcop-mcp/) | [`/mcp/README.md`](../../mcp/README.md) | `mcp/pyproject.toml`: `readme = "README.md"` |

These files are the single sources of truth for future PyPI long descriptions.
Do not maintain separate copied descriptions in this directory.

## 4.0.1 documentation correction

Prepared on 2026-09-11 against the published FCoP 4.0.1 package pair.

The correction:

- removes release-candidate and pending-approval wording;
- removes stale 4.0.0 install instructions from the current page;
- moves 0.x and 3.x detail out of the main package descriptions;
- states the `fcop` / `fcop-mcp` package boundary;
- records the current MCP surface as 49 tools, 12 resources, and 4 templates;
- documents `create_branch`, `inspect_family`, and `merge_branches`;
- explains that Branch convergence is explicit and Core owns atomic persistence,
  idempotency, cross-process locking, and recovery;
- uses compatible 4.0.x installation ranges beginning at 4.0.1.

This GitHub documentation change does not modify the already published PyPI
pages. A future package release must build its long descriptions from these
committed sources.

## Release checklist

Before the next PyPI release:

1. Update both canonical source files together.
2. Describe the current stable release only; link to historical migration
   material instead of embedding it in the landing page.
3. Confirm version ranges, supported Python versions, tool/resource/template
   counts, and package boundaries.
4. Build all wheel and sdist artifacts.
5. Render and inspect each artifact's exact long description.
6. Run package metadata validation before upload.
7. After publication, compare both public PyPI pages with these GitHub sources.

A version bump, tag, package upload, GitHub Release, MCP registry update, or
local MCP upgrade is outside this historical documentation record.

## 4.0.2 CLI v1 release binding

The separately authorized CLI v1 release updates both canonical README sources,
adds CLI Setup/Observe/Diagnose guidance, and retains 49 MCP tools. Build metadata
must contain these exact UTF-8 descriptions. The release evidence must compare
both public PyPI JSON descriptions with the tagged sources after publication;
pre-publication metadata checks alone are not public-page verification.
