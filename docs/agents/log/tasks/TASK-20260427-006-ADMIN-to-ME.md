---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260427-006
sender: ADMIN
recipient: ME
priority: P0
related: [ISSUE-20260427-007]
session_id: sess-20260427-me-072
---

# 0.7.2 元数据一致性 hotfix——同类 bug 第三次，必须刹车

## 背景

0.7.1 发版当天 dogfood `fcop_report()` 发现：

- `src/fcop/rules/_data/fcop-rules.mdc` frontmatter `fcop_rules_version`
  仍是 **1.7.0**，但同一文件 body 末尾的 changelog 写的是 **1.8.0**，
  规则正文也是 1.8.0 内容（sub-agent 条款 / Rule 5 删 AMEND /
  Rule 0.a.1 澄清）。
- 即"frontmatter 没跟着 body 一起 bump"。

这是 **0.7.x 周期内第三次"多处编辑只编了 N-1 处"同类 bug**：

1. ISSUE-006（0.7.0）：`mcp/pyproject.toml` 多处编辑漏 dep pin。
2. REPORT-005 写"Phase 23 待 ADMIN 启 yank"——改决策时漏改文档（已被 REPORT-006 修正）。
3. **本次（0.7.1）**：rules.mdc 多处编辑漏 frontmatter 版本号。

ADMIN 指令："走 0.7.2，真的不要有 BUG 了！！"——0.7.2 必须做到
**全表面对齐 + 自动化守门**，杜绝同类。

## 要求

### A. 全表面元数据扫描 + 修复

把以下字段全部对齐到 **正确目标**（不是 0.7.1，而是真值），任何
不一致都要修：

1. `src/fcop/_version.py` → 0.7.2
2. `mcp/src/fcop_mcp/_version.py` → 0.7.2
3. 根 `pyproject.toml` version → 0.7.2（如果是静态字段）
4. `mcp/pyproject.toml` version → 0.7.2
5. `mcp/pyproject.toml` description → 提到的 fcop minor 仍为 0.7.x
6. `mcp/pyproject.toml` dependencies → `fcop>=0.7,<0.8`（lockstep）
7. **`fcop-rules.mdc` frontmatter `fcop_rules_version` → 1.8.0**（核心 bug）
8. `fcop-protocol.mdc` frontmatter `fcop_protocol_version` → 1.6.0
9. `.cursor/rules/*.mdc` → redeploy 后自动同步
10. `AGENTS.md` / `CLAUDE.md` → redeploy 后自动同步
11. README / mcp/README / docs/releases/ 等任何提到"latest"或显式 0.7.0 / 1.7.0 / 1.5.0 的地方 → 检查 + 更新

### B. 自动化守门（防同类）

新增/补强测试：

12. `tests/test_fcop/test_rules_metadata_consistency.py`：
    - assert `fcop-rules.mdc` frontmatter `fcop_rules_version` 等于
      文件 body 中最高的 `## v1.X` / `## 1.X.0 changes` 标题。
    - 同样核 `fcop-protocol.mdc` 与其 protocol_version。
13. `tests/test_fcop/test_package_version_consistency.py`：
    - assert `fcop._version.__version__` 等于根 `pyproject.toml` 的
      version 字段（如果是静态）。
    - assert `fcop_mcp._version.__version__` 等于 `mcp/pyproject.toml`
      version 字段。
14. `tests/test_fcop/test_pyproject_pins.py` 已有，复查覆盖。
15. 运行 `pytest -q` + `ruff check src/ mcp/src/ tests/` 全绿。

### C. 协议账本

16. 立 `ISSUE-20260427-007`：rules.mdc frontmatter 版本号未跟随 body
    bump，根因 = 多行编辑只编了 N-1 处，同 ISSUE-006 一类。
17. `redeploy_rules` 同步本地 `.cursor/rules/` + `AGENTS.md` +
    `CLAUDE.md`，把 rules 字段也对齐到 1.8.0。
18. 写 `REPORT-20260427-007` done report，archive task；ISSUE-007
    `status: closed`。

### D. 发版

19. `CHANGELOG.md` `[0.7.2]` 段：同类 bug post-mortem + 新增的
    consistency 测试守门。
20. `docs/releases/0.7.2.md` 含简短 post-mortem（"third time
    same-class bug; consistency tests now block this class"）。
21. build × 2、twine check × 2、upload PyPI（fcop 先、wait、fcop-mcp 后）。
22. `uvx --refresh fcop-mcp@0.7.2` 干净缓存冒烟。
23. git tag v0.7.2 + push + `gh release create`。
24. 0.7.1 不 yank（同 0.7.0 决策；版本号自动覆盖）。

## 验收

- `pytest -q` 全绿，新增的两道 consistency 测试也绿。
- `fcop_report()` 显示 `fcop-mcp 0.7.2 / fcop 0.7.2 / rules 1.8.0 /
  protocol 1.6.0`，且**包内**与"项目本地"两栏数值一致。
- `grep -rn "fcop_rules_version: 1\.7\.0\|fcop_protocol_version: 1\.5\.0"`
  整仓零命中（本机部署 + src/_data/ 双保险）。
- 任何"X.Y.0 changes"标题数字 ≤ frontmatter 版本号——回归测试自动核。
- ISSUE-007 closed；REPORT-007 入档；TASK-006 archived。

## 红线

不允许"实质对、元数据错"二度发生；这就是 0.7.2 守门的全部意义。
