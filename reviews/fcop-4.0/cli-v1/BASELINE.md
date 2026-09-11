# CLI v1 baseline

Task: FCOP-4.0-CLI-ADAPTER-V1-20260911. ADMIN decision; ME solo execution.
Authority: [fixed v4 taskbook](https://github.com/joinwell52-AI/FCoP/blob/8bedfd3e132b7cca38e017ca518807332abb4bc2/taskbooks/fcop-4.0/CLI-V1/01-CLI-Adapter-v1-Development-Taskbook-v4.zh.md).
SHA-256: 923480c9a6c4ffa7211cb0032f5497ba4089bb97339fe203978359cd97254e3f.
Baseline/main: 8bedfd3e132b7cca38e017ca518807332abb4bc2; Core/MCP 4.0.1.
Initial 2332-node collection was collection only, not baseline test acceptance.

See reports/FCOP-4.0-CLI-V1-BASELINE.md for the pre-code record.
Worktree: D:/FCoP-4.0.2-cli-v1; branch: codex/fcop-4.0.2-cli-v1.
D:/FCoP was not switched, cleaned or redeployed. CodeFlowMu was not changed.

## Pre-existing full-suite blocker

Test: tests/test_fcop/test_install_prompt.py::TestPromptIsStandardized::test_mcp_readme_inlines_canonical_en_prompt.
It compares the first MCP README text fence with the bundled legacy Cursor
installation prompt. At the fixed baseline that fence is already:
"create_branch → agents write REPORTs → inspect_family → merge_branches".

Original Git blobs:
- mcp/README.md SHA-256: 0f1626393bfba1bad01f0f04be15908060b1e8308185fd5c877c1a709d044ad6
- src/fcop/rules/_data/agent-install-prompt.en.md SHA-256: e71c0eaa084bd75cf9ce7947eae25c0c4d126affe2e52fb069fafae70abdc496

Reproduced with git show at the fixed commit and the exact two regex extraction
patterns from the test: BASELINE_ASSERTION_EQUAL=False. Current targeted run:
1 failed, 10 passed. No changes to that test or either canonical prompt.

Taskbook section 7 prohibits reintroducing large historical installation text
to the current PyPI landing pages; sections 9/12 require all tests to pass and
unrelated defects to be recorded without scope expansion. Release is BLOCKED.
ADMIN must settle the old inline-prompt test versus the current-page contract.
