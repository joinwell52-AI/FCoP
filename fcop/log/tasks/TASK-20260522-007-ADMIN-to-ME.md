---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260522-007
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: agent-bringup-prompt-20260522
session_id: sess-20260522-me-07
related: [TASK-20260522-005, TASK-20260522-006]
supersedes: TASK-20260522-006
---

# TASK-007 · agent-bringup-prompt 双语防呆 prompt（修订版，supersedes TASK-006）

## 修订说明 / Amendment Note

本 task 修订自 TASK-20260522-006（详见 `fcop/tasks/TASK-20260522-006-ADMIN-to-ME.md`）。
ADMIN 二次澄清后补三点：

1. **不锁版本号** — `pip install` 拉最新版，prompt 永不过期。
2. **物理验证文件清单** — agent 必须 `ls` 实际目录而不是只信工具返回。
3. **P0 不为零必须停** — 体检报告有 P0 时 agent 不准自决整改，停下报告 ADMIN。

原 TASK-006 已被本 TASK-007 supersede（不删，append-only 保留）。

## 背景 / Background

3.0.2 发版后，ADMIN 在另一台电脑（用了较弱模型的 agent）做 fresh-install
验证，暴露出"换台机器、换个模型，agent 立刻翻车"的问题：

**现场翻车实录**（2026-05-22T14:30+08:00）：

- agent 直接 `import fcop` 然后调 `fcop.fcop_report()` —— 把 **MCP 工具**当
  Python API 调（`fcop_report` 是 fcop-mcp 暴露的 MCP 工具，不是 fcop 包里的
  函数）；
- 找不到后开始**瞎猜** API：`fcop.project.Project.init_project(team="ME")`
  这种不存在的写法（`ME` 是角色码不是 team 名）；
- PowerShell 环境里调 `head` / `grep` 直接 `CommandNotFoundException`；
- 完全没去读仓里已有的 `agent-install-prompt.zh.md` / `LETTER-TO-ADMIN.md`。

**根因**：现有 `agent-install-prompt.zh.md` 只覆盖"装 fcop-mcp"。bringup 这条
路（**升级 → 验证 → 初始化 → 物理验证 → 体检**）从来没在协议文档里固化过。

聪明模型自己能补上；笨模型必须把每步写死。

## 目标 / Goal

落一份 `agent-bringup-prompt` 双语档（zh + en），覆盖**从零到能用**的
完整链路，按**笨模型可接受**的密度写——每步必须停下报告、不准自由发挥、
明确"这是 MCP 工具不是 Python 函数"这类边界声明，且**永不过期**（不锁
版本号）。

## 范围 / Scope

### 必做 / Required

#### 1. 新建文件（双语，跟随 wheel 部署）

- `src/fcop/rules/_data/agent-bringup-prompt.zh.md`
- `src/fcop/rules/_data/agent-bringup-prompt.en.md`

#### 2. 顶部"两种新建场景"小表

让 agent 先认清自己在哪条路上：

| 场景 | 含义 | 走哪份 prompt |
|---|---|---|
| **A · 装 fcop-mcp** | 这台电脑从来没装过 fcop-mcp / Cursor 没挂过 fcop | `agent-install-prompt.zh.md` |
| **B · 新建 / 升级 FCoP 项目** | fcop-mcp 已挂好，新建空目录或在已有目录跑最新版 | **本 prompt** |

#### 3. 五段式正文（每段都要清楚给笨模型看）

**§1 · 环境检查**

```powershell
python --version          # ≥3.10
pip show fcop fcop-mcp    # 看现状
```

- 报告结果给 ADMIN 后**停**。
- **如果已经是最新版**（ADMIN 告诉你 PyPI 上是什么），不要重复装。
- ADMIN 没说升级前不要 `pip install`。

**§2 · 升级到最新版（不锁版本号）**

```powershell
pip install --upgrade --no-cache-dir fcop fcop-mcp
python -c "import fcop, fcop_mcp; print('fcop:', fcop.__version__, '/ fcop-mcp:', fcop_mcp.__version__)"
```

- **不**写 `==3.0.2` 这种锁版本号 —— 拉最新版让 prompt 永不过期。
- `--upgrade --no-cache-dir` 全新装也照用，不区分场景。
- 把版本号贴给 ADMIN，ADMIN 自己判断够不够新。

**§3 · 边界声明（最重要，防笨模型）**

显式标出 **MCP 工具 vs Python API**：

| 类型 | 名字 | 怎么用 |
|---|---|---|
| **MCP 工具** | `fcop_report()` / `init_solo()` / `init_project()` / `create_custom_team()` / `fcop_audit()` / `write_task()` / ... | 必须先把 fcop-mcp 挂到 Cursor 的 mcp.json（重启 Cursor 后生效），在**新会话里**直接调，**不**通过 Python `import` |
| **Python API** | `from fcop import Project; Project('.').init(...)` | 走 Python 库，是兜底，没装 mcp 也能用 |

**关键事实**：
- `import fcop` 后**找不到** `fcop_report` / `init_solo` 等函数是**正常的**——
  它们是 MCP 工具，不在 Python 包里。
- 没装 fcop-mcp 时**唯一**合法的 Python 兜底是 `Project('.').init(...)`。
- **不要**在 Python 里瞎猜 `fcop.project.Project.init_project(...)` 这类函数名。

**Anti-pattern 清单（已知坑，不要做）**：

- ❌ `init_project(team="ME")` — `ME` 是角色码不是 team 名；solo 模式应调 `init_solo(role_code="ME")`
- ❌ `fcop.fcop_report()` — `fcop_report` 是 MCP 工具不是 Python 函数
- ❌ PowerShell 调 `head` / `grep` — Windows 没这些；用 `Select-Object -First` / `Select-String`
- ❌ 找不到 API 时自己想象 `fcop.project.Project.init_project(...)`
- ❌ ADMIN 没明确选择前自己 `init_solo()` 起步——init 是 ADMIN 选择题
- ❌ 看到工具返回 OK 就当成功——必须**物理验证**目录是否真的生成了

**碰到不确定怎么办**：
- 优先读 `fcop/LETTER-TO-ADMIN.md`（仓里）
- 或 `docs/getting-started.md`
- **不要瞎猜 API**

#### §4 · 初始化（ADMIN 选择题，agent 不准默认）

```
调 fcop_report() 拿 Phase 1 的初始化汇报。
```

- 报告会列出**三选一**：solo / 预设团队（dev-team / media-team / mvp-team / qa-team）/ 自定义。
- **停下**等 ADMIN 选。
- ADMIN 选完后再调对应工具：
  - solo → `init_solo(role_code="...")`
  - 预设团队 → `init_project(team="dev-team")` 等
  - 自定义 → `create_custom_team(team_name="...", roles=[...], leader="...")`

#### §5 · 初始化后**物理验证**（关键）

工具返回 OK **不等于** 文件真的生成了——3.0.0 / 3.0.1 那两版就是工具说 OK
但 `_lifecycle` 五桶是空的，3.0.2 才修。所以必须 `ls` 验证。

**应该看到的物理文件清单**（agent 把实际 `ls` 输出贴给 ADMIN）：

```
fcop/
├── fcop.json
├── LETTER-TO-ADMIN.md
├── _lifecycle/
│   ├── intent/
│   ├── plan/
│   ├── execution/
│   ├── verification/
│   └── archive/
├── shared/
│   ├── TEAM-README.md
│   ├── TEAM-ROLES.md
│   ├── TEAM-OPERATING-RULES.md
│   └── roles/{ROLE}.md         # 团队模式 / solo 模式都有
└── (兼容五桶: tasks/ reports/ issues/ shared/ log/ —— v3 仍保留)

workspace/
└── README.md

.cursor/rules/
├── fcop-rules.mdc
└── fcop-protocol.mdc

AGENTS.md
CLAUDE.md
```

**特别检查项**：
- `fcop/_lifecycle/` 下五个子目录**必须**全部存在（这是 3.0.2 修复重点）。
- 缺任何一个就是 init 没成功，**停下报告 ADMIN**。

PowerShell 验证命令：
```powershell
ls fcop/_lifecycle/
ls fcop/
ls workspace/
ls .cursor/rules/
```

#### §6 · 体检（最后一步）

```
调 fcop_audit(scope="new")
```

- 工具会写出 `fcop/shared/INSPECTION-YYYYMMDD-NNN-new.md`。
- agent 把报告里的 **P0 / P1 / P2 计数**贴给 ADMIN。
- **P0 ≠ 0** → 项目不合规，agent **必须停下**让 ADMIN 决策，**不准**自决整改。
- P1 / P2 是建议级，ADMIN 可以决定先放着。

(如果接手老项目而不是新建，把 `scope="new"` 换成 `scope="takeover"`。)

#### 4. 行为约束（每段都重申一次，笨模型才记得住）

- 每完成一步**必须**报告结果，**不准**自动跳下一步。
- 碰到不确定优先读仓里文档（`LETTER-TO-ADMIN.md` / `getting-started.md`），
  **不要**瞎猜。
- 任何 `init_*` 是 ADMIN 选择题，agent 不替 ADMIN 默认。
- 工具返回 OK 不等于成功——必须物理 `ls` 验证。
- 体检 P0 不为零 → 停下报告 ADMIN，不自决整改。

#### 5. README 双语索引

`README.md` / `README.zh.md` 在"agent 安装"段落附近加一行：

> 换电脑/新项目/升版本？看 `agent-bringup-prompt.zh.md`（双语）。

#### 6. MCP 资源暴露（本次先落文件，资源注册可选）

如果架构允许（看 `mcp/src/fcop_mcp/server.py` 的 resources 注册段）：
- `fcop://prompt/bringup` → zh.md
- `fcop://prompt/bringup.en` → en.md

如果发现注册需要改 mcp 包结构，**本次只落 wheel 内文件**，资源注册留下次发版。

### 不做 / Out of scope

- 不改 `agent-install-prompt.zh.md` 现有内容（它管"装 mcp"，定位清晰）。
- 不动 `LETTER-TO-ADMIN.md`（3.0.2 已经更新过摘要块）。
- 不做"工具层 anti-pattern 防呆"（v3.1.x 候选 ADR，超出本 task）。
- 不发新版本（攒到下次 patch / minor）。
- 不改协议规则文件（`fcop-rules.mdc` / `fcop-protocol.mdc`）。

## 验收标准 / Acceptance Criteria

1. ✅ `src/fcop/rules/_data/agent-bringup-prompt.{zh,en}.md` 存在，六段齐全
   （顶部场景表 + §1～§6）。
2. ✅ §2 升级命令**不锁版本号**（只 `fcop fcop-mcp`，不写 `==X.Y.Z`）。
3. ✅ §3 边界声明含 MCP 工具 vs Python API 对照表 + anti-pattern ≥ 6 条。
4. ✅ §5 物理验证段列出五桶 + 必查清单，含 PowerShell `ls` 命令。
5. ✅ §6 明确"P0 ≠ 0 必须停下报告 ADMIN"。
6. ✅ README.md / README.zh.md 加入索引行。
7. ✅ 跑一次 `python scripts/release_audit.py` 看是否触发文档相关 P0 / P1。
   触发了就同步 `RULES-release-file-inventory.md` §2。
8. ✅ 跑一次 `python scripts/inventory_drift.py` 三类警告清零。
9. ✅ 写 REPORT-007，archive TASK-006 + TASK-007。

## 时限 / Deadline

无硬截止。本次会话内完成草稿+验收。

## 备注 / Notes

- 本 task 是 Rule 4 第二张图（Semantic Evolution Loop）的现场——野外观察
  到笨模型翻车，反向吸收为 prompt 防呆档。
- 真正的工具层防呆（错参数给清晰报错）是更深的协议演化，留给 ADR 起草。
- supersedes TASK-006：TASK-006 锁了 `==3.0.2`，本 task 改为"保持最新版"，
  避免 prompt 过期。
