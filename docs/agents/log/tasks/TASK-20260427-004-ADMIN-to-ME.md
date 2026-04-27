---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260427-004
sender: ADMIN
recipient: ME
priority: P0
related: [ISSUE-20260427-001, ISSUE-20260427-004, ISSUE-20260427-005, ISSUE-20260427-006]
session_id: sess-20260427-me-071
---

# 0.7.1 一条龙发版本（不留残余）

## 背景

0.7.0 刚发就发现 `fcop-mcp 0.7.0` 在 PyPI 上钉死 `fcop<0.7`（ISSUE-006），
等于 release 失败需要立刻补救。同时 dogfood 曝出两个新协议 gap：
ISSUE-004（子 agent 冒充角色）与 ISSUE-005（AMEND-/v2 文件名悬空）；
更早的 ISSUE-001（Rule 0.a.1 tripwire 盲区）也并入一起处理。

ADMIN 指令："**什么乱七八糟的，0.7.1 一起搞完！！！！不要残留，最后又
不对！！！**"——所以本次 0.7.1 是**全包发版**，不准再延后任何条目。

## 要求

### A. 协议文档（rules + protocol + 信件）

1. `fcop-rules.mdc` 1.7.0 → **1.8.0**：
   - Rule 1 加"子 agent 继承呼叫者身份"条款。
   - Rule 5 移除 `AMEND-*` / `*-v2.md` 例子。
   - Rule 0.a.1 澄清"适用所有写入路径，tripwire 仅事后审计"。
2. `fcop-protocol.mdc` 1.5.0 → **1.6.0**：与 1.8.0 同步，附 v1.6 changelog。
3. `letter-to-admin.{zh,en}.md`：在 "一个角色只能给一个 agent" 后补一节
   "子 agent ≠ 多一个角色"。

### B. 库代码（fcop）

4. `Project.audit_drift()` 新方法：扫 `git status --porcelain` 与 FCoP
   账本对照，列出在 ledger 之外的未归账修改。
5. 版本：`src/fcop/_version.py` 0.7.0 → **0.7.1**。

### C. MCP 代码（fcop-mcp）

6. **CRITICAL**: `mcp/pyproject.toml` 把 `fcop>=0.6,<0.7` 改为
   `fcop>=0.7,<0.8`（ISSUE-006）。
7. `mcp/src/fcop_mcp/_version.py` 0.7.0 → **0.7.1**。
8. 新增 MCP 工具 `fcop_check`：调 `audit_drift` + `session_id↔role`
   一致性审计，返回 ADMIN 可读报告。
9. `fcop_report` 在 occupancy 段后追加 `audit_drift` 摘要 + 跨角色冲突
   计数。
10. `write_task` / `write_report` / `write_issue` 加 first-write-wins
    角色锁定：同一 `session_id` 第一次写谁就锁定那个 sender 角色，再用
    别的 sender 调用 → 工具直接拒绝并指向 Rule 1。

### D. 测试

11. `tests/test_pyproject_pins.py`：自动核对 `fcop-mcp` 版本与其
    `fcop` 依赖 pin 的 minor 一致。
12. `tests/test_audit_drift.py`：审计未在 ledger 中的 git 改动。
13. `tests/test_role_lock.py`：first-write-wins + 拒绝跨角色二写。
14. `tests/test_rule5_text.py`：rules 1.8.0 文案不再包含 `AMEND-*` /
    `*-v2.md`。

### E. 发版基建

15. 更新 `adr/ADR-0002-package-split-and-migration.md`：示例段动态化 +
    新增 lockstep 检查表。
16. 新增 `docs/releases/RELEASE-CHECKLIST.md`：一条龙发版必勾项。
17. `CHANGELOG.md` 新增 `[0.7.1]` 段。
18. `docs/releases/0.7.1.md` 含 post-mortem（pin bug 怎么发生的）。

### F. 验证 & 发版

19. `pytest -x` 全绿；`ruff check` 全绿。
20. `redeploy_rules` 把 1.8.0 / 1.6.0 同步到 `.cursor/rules/` +
    `AGENTS.md` + `CLAUDE.md`。
21. 写 done report、archive task、把 ISSUE-001/004/005/006 标 `closed`。
22. `uv build` × 2、`twine check` × 2、`twine upload` × 2。
23. `pip install fcop-mcp 0.7.0` yank 掉。
24. `git tag v0.7.1` + push + `gh release create`。

## 验收

- `uvx --refresh fcop-mcp` 能正常启动 `fcop_report()` 与 `fcop_check()`。
- `pip show fcop fcop-mcp` 显示 0.7.1 / 0.7.1。
- 任何旧脚本调用 `unbound_report()` 仍按 0.7.0 报错（不要回插 alias）。
- ISSUE-001 / 004 / 005 / 006 全部 `status: closed`，对应 REPORT 落盘。
