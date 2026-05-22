---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260522-006
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: agent-bringup-prompt-20260522
session_id: sess-20260522-me-06
related: [TASK-20260522-005]
---

# TASK-006 · 起草 agent-bringup-prompt 双语防呆 prompt

## 背景 / Background

3.0.2 发版后，ADMIN 在另一台电脑（用了较弱模型的 agent）上做 fresh-install
验证，暴露出"换台机器、换个模型，agent 立刻翻车"的问题：

**现场翻车实录**（2026-05-22T14:30+08:00）：

- agent 直接 `import fcop` 然后调 `fcop.fcop_report()` —— 把 **MCP 工具**当
  Python API 调（fcop_report 是 fcop-mcp 暴露的 MCP 工具，不是 fcop 包里的
  函数）；
- 找不到后开始**瞎猜** API：尝试 `fcop.project.Project.init_project(team="ME")`
  这种不存在的写法（`ME` 是角色码不是 team 名）；
- PowerShell 环境里调 `head` / `grep` 直接 `CommandNotFoundException`；
- 完全没去读仓里已有的 `agent-install-prompt.zh.md` / `LETTER-TO-ADMIN.md`。

**根因**：现有 `agent-install-prompt.zh.md` 只覆盖"装 fcop-mcp"，**没覆盖**：

1. 装 Python 包（`pip install fcop fcop-mcp`）
2. 验证版本（`python -c "import fcop; print(fcop.__version__)"`）
3. 初始化与 _lifecycle 五桶验证（3.0.2 修复重点）
4. 跨抽象层的边界声明（Python API vs MCP 工具，二者不混用）
5. 笨模型常见 anti-pattern（错把角色码当 team 名等）

聪明模型会自己探/读文档；笨模型不会。这次野外失败必须**反向吸收**为一份
**防呆 prompt 档**——下次换电脑、新 release、教别人都能直接复制粘贴。

## 目标 / Goal

落一份 `agent-bringup-prompt` 双语档（zh + en），覆盖**从零到能用**的
完整链路，并按**笨模型可接受**的密度写——每步必须停下报告、不准自由发挥、
明确给出"这是 MCP 工具不是 Python 函数"这类边界声明。

## 范围 / Scope

### 必做 / Required

1. **新建文件**（双语，跟随 wheel 部署）：
   - `src/fcop/rules/_data/agent-bringup-prompt.zh.md`
   - `src/fcop/rules/_data/agent-bringup-prompt.en.md`

2. **内容五段式**（每段都要清楚给笨模型看）：

   **§1 · 环境检查**
   - `python --version`（≥3.10）
   - `pip show fcop fcop-mcp`（看当前版本）
   - 报告结果给 ADMIN 后**停**，等 ADMIN 决定是否升级。

   **§2 · 升级到目标版本**
   - `pip install --upgrade --no-cache-dir "fcop==X.Y.Z" "fcop-mcp==X.Y.Z"`
   - `python -c "import fcop, fcop_mcp; print('fcop:', fcop.__version__, '/ fcop-mcp:', fcop_mcp.__version__)"`
   - 两个版本号必须一致。

   **§3 · 边界声明（最重要，防笨模型）**
   - 显式标出 **MCP 工具 vs Python API** 的区别：
     - `fcop_report()` / `init_solo()` / `init_project()` / `fcop_audit()`
       是 **MCP 工具**，必须先把 fcop-mcp 挂到 Cursor 的 mcp.json 才能用。
     - `import fcop` 后**找不到**这些函数是**正常的**，不要瞎猜其它名字。
     - 如果没装 fcop-mcp，可以走 Python API 兜底：`from fcop import Project; Project('.').init(mode='solo', role_code='ME')`。
   - **anti-pattern 清单**（已知坑，告诉 agent 不要做）：
     - ❌ `init_project(team="ME")` — `ME` 是角色码，不是 team 名
     - ❌ `fcop.fcop_report()` — `fcop_report` 是 MCP 工具不是 Python 函数
     - ❌ 在 PowerShell 用 `head` / `grep` — 用 `Select-Object -First` / `Select-String`
     - ❌ 找不到 API 时自己想象 `fcop.project.Project.init_project(...)`

   **§4 · 初始化（ADMIN 选择题，agent 不准默认）**
   - 调 `fcop_report()` 拿 Phase 1 的初始化汇报。
   - **停下**，等 ADMIN 三选一：solo / 预设团队 / 自定义。
   - ADMIN 选完后再调对应 `init_*`。

   **§5 · 初始化后验证 + 体检**
   - 再调一次 `fcop_report()` 进 Phase 2，确认角色绑定。
   - 验证 `fcop/_lifecycle/` 五桶（intent / plan / execution / verification / archive）
     都已物理存在 —— **这是 3.0.2 修的关键 bug**，3.0.0 / 3.0.1 那两版 init 后
     这五桶是空的。
   - 跑 `fcop_audit(scope="new")`，把 P0 / P1 / P2 计数贴给 ADMIN。

3. **行为约束（每个章节都要重申）**：
   - 每完成一步**必须**报告结果，**不准**自动跳下一步。
   - 碰到不确定，**优先**读 `LETTER-TO-ADMIN.md` / `getting-started.md`，
     **不要**瞎猜。
   - 任何 `init_*` 是 ADMIN 的选择题，agent 不替 ADMIN 默认。

4. **MCP 资源暴露**（与现有 `agent-install-prompt` 一致）：
   - 在 `src/fcop/rules/__init__.py` 或 mcp resources 注册处加上：
     - `fcop://prompt/bringup` 指向 zh.md
     - `fcop://prompt/bringup.en` 指向 en.md
     （视当前架构而定，可能在 mcp/src/fcop_mcp/server.py 注册资源）

5. **README 双语索引**（zh + en 两份 README 都加一行）：
   - 在"agent 安装"段落附近加一句"换电脑/升版本？看 `agent-bringup-prompt`"。

### 不做 / Out of scope

- 不改 `agent-install-prompt.zh.md` 现有内容（它只管"装 mcp"，定位清晰，
  不要混进 bringup 的内容）。
- 不动 `LETTER-TO-ADMIN.md`（3.0.2 已经更新过摘要块，这次不重复改）。
- 不做"工具层 anti-pattern 防呆"（那是 v3.1.x 候选，超出本 task 范围；
  本 task 只解决 prompt 层）。

## 验收标准 / Acceptance Criteria

1. ✅ `src/fcop/rules/_data/agent-bringup-prompt.{zh,en}.md` 存在，五段式齐全。
2. ✅ §3 边界声明显式区分 MCP 工具 vs Python API，含 anti-pattern 清单
   ≥ 4 条。
3. ✅ §5 验证 `_lifecycle` 五桶（明确点名 3.0.2 修复重点）。
4. ✅ MCP 资源 `fcop://prompt/bringup` / `fcop://prompt/bringup.en` 可解析
   （或文档说明留白到下次 release 处理，本次先把文件落进 wheel）。
5. ✅ README.md / README.zh.md 加入索引行。
6. ✅ 跑一次 `python scripts/release_audit.py` 看是否触发文档相关 P0 / P1
   （新增 prompt 不应该触发 drift；如果触发了，把 RULES-release-file-inventory.md
   §2 同步更新）。
7. ✅ 跑一次 `python scripts/inventory_drift.py` 三类警告清零。
8. ✅ 写 REPORT-006，archive TASK-006。

## 不做的事 / Anti-scope

- 不发新版本（这是 3.0.2 后的小幅 docs 增补，攒到下次 minor / patch 再发）。
- 不改协议规则（`fcop-rules.mdc` / `fcop-protocol.mdc` 不动）。
- 不动既有 `agent-install-prompt.zh.md` 的内容定位。

## 时限 / Deadline

无硬截止。建议本次会话内完成草稿+验收，下次会话决定何时发版。

## 备注 / Notes

- 这个 task 是 Rule 4 第二张图（Semantic Evolution Loop）的现场——野外
  观察到笨模型翻车，反向吸收为 prompt 防呆档。
- 真正的工具层防呆（错参数给清晰报错）是更深的协议演化，留给 ADR 起草，
  不在本 task。
