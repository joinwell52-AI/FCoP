# 让 Agent 把 FCoP 项目跑起来（防呆 prompt / zh）

把下面整段话发给一个**新会话的 agent**——升级 fcop / 新建 FCoP 项目 /
换电脑接手项目，都走这一份。

本 prompt 是为**笨模型**写的：每步都讲死、不准自由发挥、必须停下报告。
聪明模型也照样按这套来——多走几步比翻车强。

> 这份提示词来源是 fcop 官方仓库
> `src/fcop/rules/_data/agent-bringup-prompt.zh.md`，也作为 MCP 资源
> `fcop://prompt/bringup` 暴露。同时与 `agent-install-prompt.zh.md`
> 配套——那一份管"装 fcop-mcp 到 Cursor"，本份管"装好之后让项目跑起来"。

---

## 先认清自己在哪条路上

| 场景 | 含义 | 走哪份 prompt |
|---|---|---|
| **A · 装 fcop-mcp** | 这台电脑从来没装过 fcop-mcp / Cursor 没挂过 fcop | `agent-install-prompt.zh.md`（先走那份） |
| **B · 新建 / 升级 FCoP 项目** | fcop-mcp 已挂好，新建空目录、或在已有目录跑最新版 | **本 prompt** |

**只有 B 场景适用本 prompt**。如果 fcop-mcp 还没装，先去看 install
prompt。

---

## 复制下面这段，发给 Agent

```
帮我把 FCoP 项目跑起来。严格按下面六步，每步做完先报告再走下一步——
不准跳步、不准默认、不准瞎猜 API。

═══════════════════════════════════════════════════════════════════
§1 · 环境检查
═══════════════════════════════════════════════════════════════════

跑这两条：

  python --version
  pip show fcop fcop-mcp

要求：
- Python ≥ 3.10
- 如果 fcop / fcop-mcp 任一没装，告诉我"未安装"
- 如果两个都已安装，把版本号贴给我看

把输出原样给我。**停下等我决定要不要升级**——我没说升级你不准 pip
install。

═══════════════════════════════════════════════════════════════════
§2 · 升级到最新版（不锁版本号）
═══════════════════════════════════════════════════════════════════

我说升级了，再跑：

  pip install --upgrade --no-cache-dir fcop fcop-mcp

注意：
- **不**写 ==X.Y.Z 这种锁版本号——拉 PyPI 上最新版
- 全新装也用同一条命令，不区分场景
- --no-cache-dir 是为了避免拿到本地缓存的旧 wheel

装完跑这条确认版本：

  python -c "import fcop, fcop_mcp; print('fcop:', fcop.__version__, '/ fcop-mcp:', fcop_mcp.__version__)"

把版本号贴给我，**停下**等我判断够不够新。

═══════════════════════════════════════════════════════════════════
§3 · 边界声明（最重要，记不住别动手）
═══════════════════════════════════════════════════════════════════

FCoP 有两套接口，**不要混**：

| 类型 | 名字 | 怎么用 |
|---|---|---|
| **MCP 工具** | fcop_report / init_solo / init_project / create_custom_team / fcop_audit / write_task / write_report / archive_task / ... | fcop-mcp 挂到 Cursor 的 mcp.json 里，**重启 Cursor 后**在新会话直接调，不通过 Python import |
| **Python API** | from fcop import Project; Project('.').init(...) | 走 Python 库，是兜底——没装 mcp 也能用 |

**关键事实**：
- import fcop 之后**找不到** fcop_report / init_solo 这些函数是**正常的**
- 它们是 MCP 工具，不在 Python 包里
- 没装 fcop-mcp 时**唯一**合法的 Python 兜底是 Project('.').init(...)
- **不要瞎猜**像 fcop.project.Project.init_project(...) 这种不存在的函数名

**已知 anti-pattern（千万别犯）**：
- ❌ init_project(team="ME") —— ME 是角色码不是 team 名；solo 模式应调
   init_solo(role_code="ME")
- ❌ fcop.fcop_report() —— fcop_report 是 MCP 工具，不是 Python 函数
- ❌ PowerShell 里调 head / grep —— Windows 没这俩；用
   Select-Object -First / Select-String
- ❌ 找不到 API 时自己脑补 fcop.project.Project.init_project(...)
- ❌ ADMIN 没明确选择前自己 init_solo() 起步——init 是 ADMIN 选择题
- ❌ 看到工具返回 "ok" 就当成功——必须**物理 ls 验证**目录是否真生成

**碰到不确定怎么办**：
- 优先读项目里 fcop/LETTER-TO-ADMIN.md
- 或 docs/getting-started.md
- **不要瞎猜 API**，搞不清就停下问我

不需要执行什么，确认你看懂了再走 §4。

═══════════════════════════════════════════════════════════════════
§4 · 初始化（ADMIN 选择题，agent 不准默认）
═══════════════════════════════════════════════════════════════════

调这个 MCP 工具：

  fcop_report()

如果项目还没初始化（fcop/fcop.json 不存在），它会返回 Phase 1 初始化
汇报，里面列**三选一**：

  1) solo —— 单 AI 角色
  2) 预设团队（dev-team / media-team / mvp-team / qa-team）
  3) 自定义团队

把汇报贴给我，**停下**等我选。我选完再调对应工具：

- solo → init_solo(role_code="ME"  或我给的名字)
- 预设团队 → init_project(team="dev-team")  之类
- 自定义 → create_custom_team(team_name="...", roles=[...], leader="...")

**不要替我选**。"我先用 dev-team 起个步" = Rule 1 违规。

═══════════════════════════════════════════════════════════════════
§5 · 物理验证（关键，光信工具返回不够）
═══════════════════════════════════════════════════════════════════

init_* 工具返回 "ok" **不等于** 文件真的生成了。3.0.0 / 3.0.1 那两版
就翻过这种车——工具说成功但 _lifecycle 五桶是空的，3.0.2 才修。所以
你必须 ls 验证。

> ⚠️ **3.0.2 fresh init 不再创建 `fcop/tasks/` 与 `fcop/log/`**——
> spec §6 钦定退场，已搬到 `_lifecycle/inbox/` 和 `_lifecycle/archive/`。
> 看到这两个目录不存在是**正常的**，不是 init 失败。
> 老 v2 项目要升 v3 走 `python -m fcop migrate --to-v3`，不是这份 prompt 的事。

跑这几条（PowerShell）：

  ls fcop/_lifecycle/
  ls fcop/
  ls workspace/
  ls .cursor/rules/

应该能看到（v3 拓扑）：

  fcop/
  ├── fcop.json
  ├── LETTER-TO-ADMIN.md
  ├── _lifecycle/                    ← v3 五桶（必查）
  │   ├── inbox/
  │   ├── active/
  │   ├── review/
  │   ├── done/
  │   └── archive/
  ├── shared/
  │   ├── TEAM-README.md
  │   ├── TEAM-ROLES.md
  │   ├── TEAM-OPERATING-RULES.md
  │   └── roles/{ROLE}.md
  ├── reports/                       ← 报告（v3 仍保留）
  ├── issues/                        ← 问题单（v3 仍保留）
  └── reviews/                       ← 审查（v3 仍保留）

  workspace/
  └── README.md

  .cursor/rules/
  ├── fcop-rules.mdc
  └── fcop-protocol.mdc

  AGENTS.md
  CLAUDE.md

**特别检查**：
- fcop/_lifecycle/ 下五个子目录**必须**全部存在
- 缺任何一个 = init 没成功，**停下**报告我，**不要**自己手动 mkdir
  补齐，那是 fcop 库的 bug，要走 Rule 8 上报

把 ls 输出原样贴给我。

═══════════════════════════════════════════════════════════════════
§6 · 体检（最后一步）
═══════════════════════════════════════════════════════════════════

调这个 MCP 工具：

  fcop_audit(scope="new")

(如果是接手已有项目而不是新建，scope 改 "takeover"。)

工具会写出一份 fcop/shared/INSPECTION-YYYYMMDD-NNN-new.md。打开它，把
里面的 **P0 / P1 / P2 计数**贴给我。

判断规则：
- **P0 ≠ 0** → 项目不合规，**停下**让我决策，不准自决整改
- P1 / P2 是建议级，可以先放着等我看

体检通过 → bringup 完成，等我下一步指令。
```

---

## 行为约束总览（每段都重申过，再总结一次）

- 每完成一步**必须**报告结果，**不准**自动跳下一步。
- 碰到不确定优先读仓里文档（`LETTER-TO-ADMIN.md` / `getting-started.md`），
  **不要瞎猜**。
- 任何 `init_*` 是 ADMIN 选择题，agent 不替 ADMIN 默认。
- 工具返回 ok 不等于成功——必须物理 `ls` 验证。
- 体检 P0 不为零 → 停下报告 ADMIN，不自决整改。

---

## 为什么单写一份 bringup prompt

3.0.2 发版后，ADMIN 在另一台电脑（用了较弱模型）做 fresh-install 验证时，
agent 把 `fcop_report()`（MCP 工具）当成 Python API 调，找不到后开始瞎猜
`fcop.project.Project.init_project(team="ME")` 这种不存在的写法，PowerShell
里还调了 `head` / `grep`——一系列翻车。

根因：原来的 `agent-install-prompt.zh.md` 只覆盖"装 fcop-mcp 到 Cursor"。
**装好之后怎么把项目跑起来**这条链路从来没在协议文档里固化过。聪明模型
能自己补，笨模型不行。

本 prompt 把"环境检查 → 升级 → 边界声明 → 初始化 → 物理验证 → 体检"
六步写死，密度按笨模型可接受写。这是 FCoP Rule 4（Semantic Evolution
Loop）的现场——野外观察到翻车，反向吸收为协议防呆档。

更细的协议背景看 `fcop/LETTER-TO-ADMIN.md`，那是 fcop 给 ADMIN 的完整
说明书。
