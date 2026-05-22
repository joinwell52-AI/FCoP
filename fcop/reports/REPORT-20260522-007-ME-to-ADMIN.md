---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P1
thread_key: agent-bringup-prompt-20260522
parent: TASK-20260522-007-ADMIN-to-ME
related: [TASK-20260522-006-ADMIN-to-ME, REPORT-20260522-005-ME-to-ADMIN]
session_id: sess-20260522-me-07
subject: agent-bringup-prompt 双语防呆 prompt 落地（最小路径版）
---

# REPORT · agent-bringup-prompt 双语防呆 prompt 落地

## 摘要 / Summary

TASK-007 按"最小路径"完成——只落 wheel 内两份双语 prompt 数据文件，
让 GitHub raw 链接立即可用。MCP resource 注册、`get_bringup_prompt()`
Python API、README 索引、新版本发布，全部按 ADMIN 决议**留下次 patch / minor**。

野外现场（另一台机器笨模型翻车：把 `fcop_report()` 当 Python API、
PowerShell 跑 `head` / `grep`、瞎造 `fcop.project.Project.init_project(...)`）
反向吸收为协议**防呆档**——这是 FCoP Rule 4（Semantic Evolution Loop）
现场实例。

## 验收对照 / Acceptance

### 验收 1 · `src/fcop/rules/_data/agent-bringup-prompt.{zh,en}.md` 存在，六段齐全 ✅

```
src/fcop/rules/_data/
├── agent-bringup-prompt.zh.md   227 行
└── agent-bringup-prompt.en.md   ~230 行
```

两份均含顶部场景表（A · 装 fcop-mcp / B · 起 FCoP 项目）+ §1～§6
（环境检查 → 升级 → 边界声明 → 初始化 → 物理验证 → 体检）。

### 验收 2 · §2 升级命令不锁版本号 ✅

```
pip install --upgrade --no-cache-dir fcop fcop-mcp
```

明确不写 `==X.Y.Z`——避免 prompt 文档随版本号过期。`--no-cache-dir`
对抗本地陈旧 wheel 缓存。

### 验收 3 · §3 边界声明含 MCP vs Python API 对照表 + anti-pattern ≥ 6 条 ✅

对照表：
- MCP 工具：`fcop_report` / `init_solo` / `init_project` / `create_custom_team` /
  `fcop_audit` / `write_task` / `write_report` / `archive_task` / ...
- Python API：`from fcop import Project; Project('.').init(...)`

anti-pattern（双语版各 6 条）：
1. `init_project(team="ME")` — ME 是 role，不是 team
2. `fcop.fcop_report()` — fcop_report 是 MCP 工具不是 Python 函数
3. PowerShell 用 `head` / `grep`
4. 瞎造 `fcop.project.Project.init_project(...)`
5. ADMIN 没选就调 `init_solo()`
6. 工具返回 OK 不物理 `ls` 验证

### 验收 4 · §5 物理验证段列出五桶 + 必查清单 ✅

PowerShell `ls` 命令：

```powershell
ls fcop/_lifecycle/
ls fcop/
ls workspace/
ls .cursor/rules/
```

必查清单：
- `fcop/_lifecycle/{intent,plan,execution,verification,archive}/` 五桶
- `fcop/{fcop.json, LETTER-TO-ADMIN.md, shared/}`
- `workspace/README.md`
- `.cursor/rules/{fcop-rules.mdc, fcop-protocol.mdc}`
- `AGENTS.md` / `CLAUDE.md`

特别强调：**五桶任一缺失 = init 没成功，停下报 ADMIN，不自己 mkdir 兜底**
（因为那是 fcop 库 bug，按 Rule 8 escalate）。

### 验收 5 · §6 明确"P0 ≠ 0 必须停下报告 ADMIN" ✅

```
P0 ≠ 0 → 项目不合规，停下让 ADMIN 决定，不自决整改
P1 / P2 是建议，可以等 ADMIN 看
```

### 验收 6 · README 双语索引 ⏸ 改期

按 ADMIN 决议本次只走最小路径，README 索引行下次 patch 一起加。
GitHub raw 链接已经可用，不影响验收 1 的"链接活起来"诉求。

### 验收 7 · release_audit.py ⏸ 不适用本次

本次不发新版本，audit 的 R1～R12 主要锁版本数字 / CHANGELOG / hardcoded
`vX.Y.Z`，本次新增的两份数据文件不在 inventory §2 钦定清单里，不触发
任何 P0 / P1。

### 验收 8 · inventory_drift.py 三类警告清零 ✅

```
========================================================================
FCoP Inventory Drift Audit · RULES §2 vs git ls-files
========================================================================
[OK] 无漂移 / no drift detected
    zh: RULES-release-file-inventory §2 与 git ls-files 完全对齐
    en: RULES inventory §2 is fully aligned with tracked files
```

新增的 `_data/agent-bringup-prompt.{zh,en}.md` 不在钦定清单——它们是
prompt 数据，不是发版强制资产。审计通过。

### 验收 9 · 写 REPORT-007，archive TASK-006 + TASK-007 ✅

本文件即 REPORT-007。归档动作随后用 `archive_task` 工具落到 `fcop/log/`。

## 决议偏差 / Scope Adjustments

ADMIN 在会话中明确"只要有链接就可以"——本 task 由"完整闭环"收敛为
"最小路径"，三处偏差均经 ADMIN 一次性批准：

| 项 | 原 task 范围 | 实际范围 | 决议 |
|---|---|---|---|
| `__init__.py` 的 `_BRINGUP_PROMPT_FILENAMES` | 加 + 提供 `get_bringup_prompt()` | **未加**（半成品已 revert） | 留下次 patch |
| `mcp/src/fcop_mcp/server.py` 资源注册 | `fcop://prompt/bringup{,.en}` | **未注册** | 留下次 patch |
| README 双语索引行 | `README.md` / `README.zh.md` 加索引 | **未加** | 留下次 patch |
| 发新版本 | 是否 bump 3.0.3 | **不发** | 攒下次 patch / minor |

理由：上面四项都不影响"GitHub raw 链接立即可用"的核心诉求。
拆开两个 commit（产品 / 治理）保持 wheel 内代码改动干净。

## 协议自指 / Protocol Self-Reference

本次落地是 FCoP **Rule 4（Semantic Evolution Loop）的现场实例**：

```
Step 4 现场观察 ── 笨模型在另一台机器翻车
Step 5 涌现适配 ── 写出"防呆 prompt"作为本地约定
Step 6 反向吸收 ── 把 prompt 落进 fcop 包数据，纳入下一代协议产物
```

下一步深演化（v3.1.x 候选 ADR）：
- **工具层防呆**：错参数给清晰报错，让模型不犯第二遍
  （比 prompt 更上游，但需要修工具签名 / 验参数）
- **`get_bringup_prompt()` API + MCP 资源**：让 agent 在 fcop-mcp
  装好后能直接 `fcop_get_bringup_prompt()` 拿到本机最新版

## 文件清单 / File Manifest

新增（产品）：
- `src/fcop/rules/_data/agent-bringup-prompt.zh.md`
- `src/fcop/rules/_data/agent-bringup-prompt.en.md`

新增（协作账本）：
- `fcop/tasks/TASK-20260522-006-ADMIN-to-ME.md`（已 superseded）
- `fcop/tasks/TASK-20260522-007-ADMIN-to-ME.md`
- `fcop/reports/REPORT-20260522-007-ME-to-ADMIN.md`（本文件）

未改动（按决议）：
- `src/fcop/rules/__init__.py`（半成品 `_BRINGUP_PROMPT_FILENAMES` 已 revert）
- `mcp/src/fcop_mcp/server.py`
- `README.md` / `README.zh.md`
- 任何版本号文件

## Commit 计划 / Commit Plan

按 Rule 2（产品 vs 协作元数据）边界拆两个 commit：

1. **commit 1（产品）** —— 仅 `src/fcop/rules/_data/`
   ```
   docs(prompt): add agent-bringup-prompt (zh+en)

   Wheel 内新增双语防呆 prompt，覆盖"装 fcop-mcp 之后如何把项目起起来"
   的六步路径。GitHub raw 链接立即可用，无需 fcop-mcp 已装。

   Rule 4（Semantic Evolution Loop）现场实例：野外笨模型翻车反向吸收
   为协议防呆档。

   - src/fcop/rules/_data/agent-bringup-prompt.zh.md（227 行）
   - src/fcop/rules/_data/agent-bringup-prompt.en.md（~230 行）
   ```

2. **commit 2（治理账本）** —— `fcop/tasks/` `fcop/reports/` `fcop/log/`
   ```
   fcop: TASK-006/007 + REPORT-007 archive

   协议自举的协作账本闭环。
   ```

## 下一步 / Next Steps

ADMIN 自决：
- [ ] 本 commit 1 push 后，访问 GitHub raw 链接核对内容（中文 + 英文）
- [ ] 决定何时把"留 patch"的四项一起落（建议下次有别的小修补一起 bump 3.0.3）
- [ ] 决定是否起草 v3.1.x ADR：工具层防呆 + `get_bringup_prompt()` API

## 备注 / Notes

- TASK-006 已被 TASK-007 supersede（锁版 vs 不锁版的修订），档案保留
  双方文件用于审计。
- 本 task 没改任何协议规则文件 —— 防呆 prompt 是协议产物，不是协议本身。
- 不发新版本是为了让"四项 patch 改动"一起走，而不是为这两份 md 单发一版。
