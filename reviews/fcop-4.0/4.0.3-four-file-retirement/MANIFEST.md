# 4.0.3 scope-clarification checkpoint Manifest

STATUS: BLOCKED_ON_SCOPE_CLARIFICATION — not an implementation/release acceptance Manifest.

- Base: `157acaeb0cbd11bbf0ce54fba18c2a7d0d980efb`.
- Taskbook: `8ec8658c15f2aa148bd42e3d6e6bb916921e4b0b`; SHA-256 `1fccdeca2e7332cc5e5e397847409e9a4f86d32c81ada64dcce4d88bc7a1f70d`; 16,312 Git blob bytes.
- Evidence content commit: `a6ac744fd64f4434687d4ea6d4efaef59e81789f`.
- Delivery branch: `review/fcop-4.0.3-four-file-retirement`; Draft PR #48.
- Delivery HEAD: the commit containing this Manifest; exact SHA is recorded in the PR checkpoint receipt to avoid a circular self-hash.
- Scope: three evidence files below plus this Manifest only. Production candidates and new tests are preserved locally, NOT part of this commit chain.

## Git blob identities

| Path | SHA-256 |
| --- | --- |
| reviews/fcop-4.0/4.0.3-four-file-retirement/BASELINE.md | bdef6b330380e1db28239105637c78b6f076cb604abc80c45132f2b334af0ed6 |
| reviews/fcop-4.0/4.0.3-four-file-retirement/BLOCKED-INITIALIZATION-BOUNDARY.md | ddec2a6fd0f3a370fb7e1b06093e3754b10366f050da2672fc2d3c110f0bf361 |
| reviews/fcop-4.0/4.0.3-four-file-retirement/initialization-boundary-repro.py | 404ebc67b031a205e2a9446cfed76a2a9ba213908eae16f2b92fe64bacb08a99 |

The Manifest's own hash and remote readback are recorded externally in the PR receipt. Read raw GitHub blobs; do not confuse CRLF checkout hashes with canonical Git blob hashes.

## Validation scope and exclusions

- Directed local candidate run: 130 passed, 3 existing warnings. Not the complete suite and not tests of a final committed implementation.
- Unchanged initialization failure/race checks: 8 passed, 90 deselected, 3 existing warnings.
- Real local stdio catalog: 49 tools / 12 resources / 4 templates.
- Initialization staging boundary: REPRODUCED; clarification required.
- Full regression, package wheel/sdist/long-description checks, 4.0.3 website preview, final implementation CI: NOT_RUN / NOT_COMPLETE.
- Wheel/sdist hashes: NONE, no 4.0.3 artifacts built.
- README/PyPI/homepage sources: unchanged from base; no 4.0.3 publication claim.
- Public release/Registry checks: NOT_APPLICABLE_BEFORE_AUTHORIZATION.
- main, original workspace, CodeFlowMu, tags and public packages: not modified.

Requested ADMIN decision: whether section 3 permits retaining the existing `.fcop-init-*` atomic initialization staging and failed-initialization evidence as a narrow exception. No acceptance or release Gate is requested.
