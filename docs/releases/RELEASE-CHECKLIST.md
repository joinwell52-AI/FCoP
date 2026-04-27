# FCoP Release Checklist

> Source of truth for "fcop 一条龙" releases. Born after the 0.7.0 →
> 0.7.1 incident (`fcop-mcp 0.7.0` shipped with the wrong `fcop`
> dependency pin and had to be hot-patched and yanked the next day).
> Every box must be checked before `twine upload`. No exceptions.

The two packages release in lockstep at the **minor level** while we
are pre-1.0 (see ADR-0002 "Lockstep pin rule"). Patches may be
released independently, but the `fcop` dependency pin in
`mcp/pyproject.toml` is always the cross-package contract.

## Phase 0 — Pre-flight

- [ ] Read this file end-to-end. Yes, every release.
- [ ] Confirm scope: list every ISSUE-* / TASK-* this release closes.
      Open changes that aren't in scope wait for the next release.
- [ ] No `.fcop/proposals/role-switch-*.md` from this development
      cycle is unresolved (run `fcop_check()` from a fresh shell to
      verify).

## Phase 1 — Bumps (all four files in one commit)

- [ ] `src/fcop/_version.py` → new version
- [ ] `mcp/src/fcop_mcp/_version.py` → same minor as `fcop`
- [ ] `mcp/pyproject.toml` `dependencies` → `fcop>=X.Y,<X.(Y+1)`
      where `X.Y` matches the new `fcop-mcp` minor
- [ ] `mcp/pyproject.toml` `description` field still names the
      correct `fcop` minor (`...depends on fcop X.Y.x...`)
- [ ] If protocol surface moved: `src/fcop/rules/_data/fcop-rules.mdc`
      `fcop_rules_version` bumped + matching changelog entry at the
      bottom of the rule file
- [ ] If protocol commentary moved:
      `src/fcop/rules/_data/fcop-protocol.mdc` `fcop_protocol_version`
      bumped + new entry under "Protocol Version Log"
- [ ] If letter copy changed: `src/fcop/rules/_data/letter-to-admin.zh.md`
      AND `src/fcop/rules/_data/letter-to-admin.en.md` updated together
      (the two languages drift if you change one without the other)

## Phase 2 — Code & tests

- [ ] New library APIs land in `src/fcop/__init__.py` `__all__` and
      get a corresponding `from fcop.models import ...` entry
- [ ] New MCP tools have docstrings that decompose into "essential
      file ops" (Consequence 1 of `fcop-protocol.mdc`)
- [ ] `pytest tests/test_fcop/test_pyproject_pins.py -q` is **green**
      — this is the lockstep enforcement, do not skip
- [ ] `pytest -q` (all tests) green
- [ ] `ruff check src/ mcp/src/ tests/` green
- [ ] If any tool surface changed: `pytest tests/test_fcop_mcp/test_tool_surface.py
      --snapshot-update` AND `pytest tests/test_fcop/test_public_surface.py
      --snapshot-update`, then commit the snapshot diff with the
      bump

## Phase 3 — Docs

- [ ] `CHANGELOG.md` has a new `[X.Y.Z]` section above prior entries,
      describing the change in user-facing terms
- [ ] `docs/releases/X.Y.Z.md` exists and includes:
      - One-liner of "why this release exists"
      - Bullet list of every closed ISSUE-* / TASK-*
      - Post-mortem section if anything went wrong getting here
- [ ] `mcp/README.md` and root `README.md` mention the new version
      where they reference the latest version explicitly (don't leave
      stale "Latest: 0.6.5" anywhere)

## Phase 4 — Project ledger

- [ ] All TASK-* this release closes have matching REPORT-* in
      `docs/agents/reports/` (or already in `log/reports/`)
- [ ] `archive_task` has been run on every closed TASK-*
- [ ] All ISSUE-* this release closes have `status: closed` in their
      frontmatter (FCoP allows in-place flip per ADR-0004)
- [ ] `redeploy_rules` has been run so `.cursor/rules/`, `AGENTS.md`,
      and `CLAUDE.md` all carry the new rules / protocol versions

## Phase 5 — Build

- [ ] `python -m build --wheel --sdist` from repo root → `fcop` wheel
- [ ] `python -m build --wheel --sdist` from `mcp/` → `fcop-mcp` wheel
- [ ] `twine check dist/*` passes for both packages
- [ ] Local sanity install: `pip install dist/fcop-X.Y.Z-py3-none-any.whl`
      then `python -c "import fcop; print(fcop.__version__)"`
- [ ] Local sanity install of `fcop-mcp`: `pip install
      dist/fcop_mcp-X.Y.Z-py3-none-any.whl` then
      `python -c "from fcop_mcp.server import mcp; print('ok')"`

## Phase 6 — Publish (order is hard-required)

- [ ] `twine upload dist/fcop-X.Y.Z*` — fcop FIRST so fcop-mcp's
      pin can resolve at install time
- [ ] Wait ~30 seconds for PyPI's index to propagate
- [ ] `twine upload dist/fcop_mcp-X.Y.Z*` — fcop-mcp SECOND
- [ ] `uvx --refresh fcop-mcp@X.Y.Z` from a clean machine (or `uv
      cache clean`) and call `fcop_report()` end-to-end. **This step
      catches the 0.7.0 pin-bug class — never skip it.**
- [ ] If a previous version on PyPI has known-broken pins, **yank
      it** so new installs don't pick it up. PyPI yank is web-UI-only
      as of 2026-04: log in to https://pypi.org/manage/project/<name>/
      → "Releases" → ⋮ next to the bad version → "Yank release" →
      enter a one-line reason (shown to users in pip warnings). Yanks
      are reversible from the same menu.

## Phase 7 — Git / GitHub

- [ ] `git status` clean
- [ ] `git tag vX.Y.Z`
- [ ] `git push origin main && git push origin vX.Y.Z`
- [ ] `gh release create vX.Y.Z` with notes from `docs/releases/X.Y.Z.md`

## Phase 8 — Post-release verification

- [ ] On a *different* machine: `uvx --refresh fcop-mcp` and run
      `fcop_report()` — pinned dependency must resolve correctly
- [ ] In the issue tracker / GitHub issues: link this release tag
      to every closed issue
- [ ] If anything failed: file a new ISSUE-*, write a post-mortem
      in `docs/releases/X.Y.(Z+1).md`, and patch-fix
