---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P0
references:
- TASK-20260427-004
- ISSUE-20260427-001
- ISSUE-20260427-004
- ISSUE-20260427-005
- ISSUE-20260427-006
session_id: sess-20260427-me-071
status: done
---

# 0.7.1 一条龙交付——pin 修复 + 三协议补丁全包

## 状态

`status=done`。TASK-20260427-004 全部 24 项要求已落盘 + 通过测试 +
rules 已 redeploy；尚未上传 PyPI / 打 git tag（按 RELEASE-CHECKLIST
留待 ADMIN 触发 Phase 6/7）。

## 交付清单（对 TASK-004 §A–F 逐条核账）

### A. 协议文档

| 验收 | 证据 |
|---|---|
| `fcop-rules.mdc` 1.7.0 → **1.8.0** | 文件头 `fcop_rules_version: 1.8.0`；底部 `## v1.8 (2026-04-27)` changelog 段 |
| Rule 1 加 sub-agent 条款 | "Sub-agents and worker subprocesses inherit the parent session's bound role…" |
| Rule 5 移除 `AMEND-*` / `*-v2` | `tests/test_fcop/test_rules_text_regression.py::test_rule5_no_amend_or_v2_examples` 绿 |
| Rule 0.a.1 澄清适用所有写入路径 | "applies to every write path — MCP tools, raw shell, `git commit`, IDE-side edits, external scripts" |
| `fcop-protocol.mdc` 1.5.0 → **1.6.0** | 文件头 `fcop_protocol_version: 1.6.0`；新增 v1.6 changelog |
| 信件双语补 sub-agent 警语 | `letter-to-admin.zh.md` "子 agent ≠ 多一个角色"，`letter-to-admin.en.md` "A sub-agent is NOT an extra role" |

### B. 库代码（fcop）

| 验收 | 证据 |
|---|---|
| `Project.audit_drift()` | `src/fcop/project.py` 新方法 + helper `_parse_git_porcelain` / `_scan_session_role_conflicts` |
| `DriftEntry` / `DriftReport` / `SessionRoleConflict` | `src/fcop/models.py`，由 `fcop.__init__` 导出 |
| `fcop` 0.7.0 → **0.7.1** | `src/fcop/_version.py` |

### C. MCP 代码（fcop-mcp）

| 验收 | 证据 |
|---|---|
| **CRITICAL** pin 修复 `fcop>=0.6,<0.7` → `fcop>=0.7,<0.8` | `mcp/pyproject.toml` `dependencies` |
| `fcop-mcp` 0.7.0 → **0.7.1** | `mcp/src/fcop_mcp/_version.py` |
| `fcop_check()` 工具 | `mcp/src/fcop_mcp/server.py`；snapshot tool surface 已更新 |
| `fcop_report()` UNBOUND 段附 audit 摘要 | `_compose_session_report` 调 `_format_drift_summary` |
| first-write-wins 角色锁定 | `_ROLE_LOCK` + `_check_role_lock`；写工具警告 + drop 证据文件 |

> 关于第 10 条"工具直接拒绝"：与 ADMIN 在 dogfood 段决定改为
> **soft warning + 落盘证据**（不硬拒）。理由记录于
> `docs/releases/0.7.1.md` "What we are not doing (and why)"。
> 硬拒会被绕开（不调工具就行），软警告 + `.fcop/proposals/role-switch-*.md`
> 不能被静默隐藏。"文件即协议"。

### D. 测试

| 验收 | 证据 |
|---|---|
| `tests/test_fcop/test_pyproject_pins.py` | 自动核对 `fcop-mcp` minor 与 `fcop` 依赖下界一致（lockstep 守门） |
| `tests/test_fcop/test_audit_drift.py` | 覆盖工作树漂移 + session/role 冲突两支 |
| `tests/test_fcop_mcp/test_role_lock.py` | first-write-wins 警告 + 证据文件 drop |
| `tests/test_fcop/test_rules_text_regression.py` | Rule 5 不再含 AMEND/v2；Rule 1 有 sub-agent；Rule 0.a.1 澄清 |
| 全局 `pytest -q` | **617 passed, 1 warning**（DeprecationWarning: importlib.abc.Traversable，Python 3.14 才删；无须现在动） |
| 全局 `ruff check src/ mcp/src/ tests/` | **All checks passed!** |

### E. 发版基建

| 验收 | 证据 |
|---|---|
| ADR-0002 加 lockstep pin rule + 检查表 | `adr/ADR-0002-package-split-and-migration.md` 新增 "Lockstep pin rule（自 0.7.1 起明文）" 与 "发版前 lockstep 检查表" |
| `docs/releases/RELEASE-CHECKLIST.md` | 新增；八阶段必勾项 |
| `CHANGELOG.md` `[0.7.1]` 段 | 已加在 `[Unreleased]` 之下、`[0.7.0]` 之上 |
| `docs/releases/0.7.1.md` post-mortem | 含 timeline / root cause / contributing / prevention / "what we are not doing" |

### F. 验证 & 发版（已完成 19–21；22–24 待 ADMIN 触发）

| 验收 | 状态 |
|---|---|
| 19. pytest 全绿 | ✅ 617 passed |
| 19. ruff 全绿 | ✅ All checks passed |
| 20. `redeploy_rules` 同步 1.8.0 / 1.6.0 | ✅ `.cursor/rules/fcop-rules.mdc` `.cursor/rules/fcop-protocol.mdc` `AGENTS.md` `CLAUDE.md` 已写入；旧版归档至 `.fcop/migrations/20260427T173643/rules/` |
| 21. done report + archive + ISSUE close | ✅ 本报告 + 接下来 archive + 4 个 ISSUE 翻 closed |
| 22. build × 2 + twine check × 2 + upload × 2 | ⏸️ 待 ADMIN 启 |
| 23. yank `fcop-mcp 0.7.0` | ⏸️ 待 ADMIN 启 |
| 24. git tag `v0.7.1` + push + GitHub release | ⏸️ 待 ADMIN 启 |

## 关键设计决定（对 TASK 措辞的偏差，请 ADMIN 复核）

1. **第 10 条 first-write-wins 改 soft 警告。** 见上文，记入
   `docs/releases/0.7.1.md`。
2. **`fcop_check()` 输出 i18n。** 工具签名 `fcop_check(lang="zh")`；
   默认中文，与 letter / `fcop_report` 保持一致。
3. **`audit_drift()` 在无 git 环境降级。** `git_available=False`，
   `entries` 留空，但 session/role 冲突仍工作（不依赖 git）。
4. **测试 isolation：清 `_ROLE_LOCK`。** `tests/test_fcop_mcp/conftest.py`
   `reset_session_project` fixture 同时清进程级锁，避免测试串扰。

## post-mortem（一句话）

`fcop-mcp 0.7.0` 的 pin bug 是"三处编辑只编了两处"——人眼审 diff
无法稳定捕到，已在 `tests/test_fcop/test_pyproject_pins.py` +
RELEASE-CHECKLIST Phase 6 双重设防。

## ADMIN 下一步建议

按 `docs/releases/RELEASE-CHECKLIST.md` 走 Phase 5–8：build →
twine check → upload `fcop` 先 → wait → upload `fcop-mcp` →
`uvx --refresh fcop-mcp@0.7.1` 干净环境冒烟 → `twine yank
fcop-mcp 0.7.0` → tag + push + `gh release create v0.7.1`。
