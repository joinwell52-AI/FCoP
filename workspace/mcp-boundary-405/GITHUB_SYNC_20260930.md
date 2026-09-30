# GitHub synchronization verification — September 30, 2026

The local 4.0.5 upgrade commit `6905b1e` was applied on top of GitHub main
`33b3ea05c693beffb1c981d362ae3223a5de5470`, incorporating the 35 intervening
remote commits. Eight document/test conflicts were resolved while retaining
the practical homepage, installation FAQ, macOS guides, distribution badges,
and Zenodo 4.0.3 archive identity.

Delivery branch: `codex/fcop-4.0.5-github-sync`.
Draft review: https://github.com/joinwell52-AI/FCoP/pull/58.

The PyPI JSON APIs report 4.0.5 for both packages. GitHub's latest Release API
reports v4.0.3; its v4.0.5 tag ref returned 404. Documentation therefore links
current packages separately from the historical GitHub Release and archive.
The MCP CI smoke assertion now expects exactly 25 tools, six resources and
zero resource templates.

## Validation

- `python -m ruff check src tests mcp/src`: passed.
- `python scripts/pages/build.py --check`: passed, 16 generated files and logo.
- `git diff origin/main --check`: passed.
- PM/DEV/QA example: passed, producing 3 TASKs, 3 REPORTs, 1 assessment REVIEW.
- `python -m build` at root and in `mcp/`: both wheel/sdist pairs built.
- Full `python -m pytest -q`: 2336 passed, 2 skipped, 1 failed in 286.14s.
  The sole failure asserted an obsolete README stable-version label. After
  correcting that assertion, the two release/document test files passed:
  **71 passed**. No production code changed after the full run.
- `python -m mypy src/fcop`: 41 errors.
- `python -m mypy --config-file mcp/pyproject.toml mcp/src/fcop_mcp`: 116 errors.
- `python -m mypy --config-file mcp/pyproject.toml tests/test_fcop_mcp`: 27 errors.
  These strict typing failures remain open; the PR is a draft and this record
  does not claim merge or release-candidate readiness.

## Preservation and publication boundary

The original `D:/FCoP` checkout remained at `6905b1e`; its uncommitted and
untracked work was not modified or included in this synchronization.
No `.env`, virtual environment, local scratch directory or unrelated working
change was uploaded. No main update, force push, merge, tag, Release, registry
publication or package upload was performed.
