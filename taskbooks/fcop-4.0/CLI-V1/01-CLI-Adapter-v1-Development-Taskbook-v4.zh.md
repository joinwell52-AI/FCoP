# FCoP 4.0 CLI Adapter v1 开发任务书（v4 修订版）

**Task ID:** `FCOP-4.0-CLI-ADAPTER-V1-20260911`  
**Repository:** `joinwell52-AI/FCoP`  
**Execution target:** Codex  
**Revision:** v4（对齐 FCoP 4.0.1、49 Tools 与 PR #38 文档基线）  
**Authorized scope:** CLI Adapter v1 + Tool Catalog 单一事实源修正 + 全套公开文档同步  
**Delivery:** GitHub PR + evidence package + 两包 4.0.2 发布  
**Merge:** AUTHORIZED ONLY AFTER ALL RELEASE GATES PASS  
**Tag / GitHub Release:** AUTHORIZED ONLY FOR `v4.0.2` AFTER MERGE  
**PyPI publish:** AUTHORIZED ONLY FROM THE MERGED/TAGGED COMMIT AFTER ALL RELEASE GATES PASS  
**Date:** 2026-09-11

---

## 0. ADMIN 决策

FCoP 4.0 正式定义一个薄的 CLI Adapter。

CLI 的定位固定为：

> **CLI = Setup + Observe + Diagnose**  
> **MCP = Work**

CLI 不是第二套 MCP，不承担 Agent 正常业务协作，不复制 TASK / REPORT / REVIEW / Authorization / Branch / Convergence 等 MCP 工作工具。

目标架构：

```text
                         FCoP Core
                            │
             ┌──────────────┴──────────────┐
             │                             │
        CLI Adapter                   MCP Adapter
             │                             │
     Human / Script / CI              Agent / Host
             │                             │
 Setup / Observe / Diagnose               Work
```

本任务授权实现 CLI Adapter v1。

---

# 1. 事实基线

执行前必须从最新 `origin/main` 重新核验，不得使用缓存结论。

当前已知基线：

1. `fcop` 包已经存在 console entry point：

   ```text
   fcop = "fcop.cli._main:main"
   ```

2. 当前顶层 CLI 仅注册迁移类入口：

   ```text
   fcop migrate-workspace
   fcop migrate --to-v3
   ```

3. `fcop` Core 当前版本为 `4.0.1`。

4. `fcop-mcp` 当前版本为 `4.0.1`。

5. 当前实际 MCP Server 能力面为 **49 Tools / 12 Resources / 4 Templates**。
   其中 `create_branch`、`inspect_family`、`merge_branches` 已由
   `fcop_mcp.branches` 注册并随 4.0.1 发布。

6. 当前 `fcop_mcp.disposition.TOOLS` 仍只有历史 45 个工具加 T6
   `reopen_task`，即 46 项；它尚未包含上述 3 个既有 Branch 工具。
   因此“声明表 46、实际 Server 49”是本任务必须定点修正的事实源缺口，
   不是新增 3 个工具。CLI 不得把 46 或 49 硬编码为自己的清单。

7. FCoP 4.0 Core 已有可复用公共能力，包括但不限于：
   - `Project(...).create_workspace(...)`
   - `Project(...).is_initialized()`
   - `Project(...).inspect_state(...)`
   - Core 的 schema / rules / inspection / validation 能力
   - 既有 migration engine

8. PR #38 已合并到 `main`，其中：
   - `fcop-README.pypi.md` 是 `fcop` 的 PyPI 长说明源；
   - `mcp/README.md` 是 `fcop-mcp` 的 PyPI 长说明源；
   - `docs/pypi/README.md` 记录两份说明源及发布检查规则。

9. 安装 MCP Server 本身不等于初始化 workspace。

若最新 `origin/main` 与以上基线有实质冲突：

- 不要猜；
- 不要覆盖新设计；
- 记录 `BASELINE_CONFLICT`；
- 仅在能保持本任务边界和兼容性的情况下继续；
- 否则停止相关子项并在 Draft PR 中报告。

---

# 2. 设计原则

本实现必须遵守以下规则。

## 2.1 单一事实源

CLI 只投影现有 Core / MCP 的事实。

禁止：

- 在 CLI 中复制 MCP 工具清单；
- 在 CLI 中复制协议版本常量；
- 在 CLI 中重写 Schema；
- 在 CLI 中重新实现生命周期判断；
- 在 CLI 中自行判断 Authorization 的业务语义；
- 用 CLI 输出制造新的业务决定。

## 2.2 薄 Adapter

优先调用现有公共 Core API。

如果 CLI 缺少某个只读聚合能力：

1. 优先在 CLI 内组合已有公共只读 API；
2. 若必须新增 API，只允许新增最小、只读、无新协议语义的公共查询接口；
3. 不得为了 CLI 新增新的生命周期规则、授权规则或业务状态。

## 2.3 默认只读

除以下两类明确操作外，CLI v1 默认不得改变 FCoP 业务状态：

```text
fcop init
fcop migrate ... --apply
```

所有其他 v1 命令必须只读。

特别禁止：

```text
fcop doctor --fix
fcop validate --repair
fcop status --recover
```

不得存在任何隐式修复。

## 2.4 不复制 MCP Work Surface

本任务禁止增加以下类型 CLI：

```text
fcop create-task
fcop claim-task
fcop submit-report
fcop approve
fcop reject
fcop branch
fcop converge
fcop authorize
fcop reopen
fcop archive-task
```

这些继续属于：

```text
Agent -> fcop-mcp -> FCoP Core
```

## 2.5 确定性输出

所有观察 / 诊断命令必须同时提供：

- 人类可读文本输出；
- `--json` 机器可读输出。

`--json` 不得输出装饰字符，不得混入日志，不得依赖终端宽度。

JSON schema 必须稳定、有测试。

---

# 3. CLI v1 冻结命令面

正式一级命令固定为以下 9 个：

```text
fcop init
fcop status
fcop inspect
fcop validate
fcop tools
fcop doctor
fcop version
fcop spec
fcop migrate
```

现有历史命令：

```text
fcop migrate-workspace
```

继续保留兼容，但不计入新的一级能力面，不删除、不改坏。

本任务不得增加第 10 个新的一级命令。

---

# 4. 命令合同

## 4.1 `fcop init`

### 目的

创建新的 FCoP 4.0 protocol workspace。

### 边界

这是 **workspace bootstrap**，不是 Agent 团队业务操作。

不得借此：

- 创建 TASK；
- 自动认领角色；
- 自动创建业务 REVIEW；
- 自动产生 Authorization；
- 自动修改 Host 配置；
- 自动安装 MCP。

### 实现要求

必须调用现有 FCoP Core workspace 创建 API，不得手工拼目录模拟初始化。

建议 UX：

```text
fcop init
fcop init --root <path>
fcop init --protocol 4.0
fcop init --json
```

协议版本来源必须使用现有权威版本定义，不得在多个文件复制。

若 workspace 已存在：

- 必须确定性报告；
- 不得覆盖；
- 不得静默重建；
- 依照现有 Core 幂等 / 已存在合同处理。

---

## 4.2 `fcop status`

### 目的

快速回答：

> “这里是不是一个 FCoP workspace？它当前是什么版本、什么身份、什么基本状态？”

### 至少输出

可用时输出：

- resolved project root；
- workspace path；
- initialized / not initialized；
- protocol version；
- workspace identity / workspace_id；
- topology / layout；
- Core version；
- 基本对象统计或 Core 已提供的状态摘要；
- warning / error summary。

不得生成 REPORT，不得修复文件。

建议：

```text
fcop status
fcop status --root <path>
fcop status --json
```

---

## 4.3 `fcop inspect`

### 目的

检查一个 FCoP 对象的真实协议状态。

v1 至少支持：

```text
fcop inspect <task-id>
fcop inspect --path <envelope-path>
fcop inspect <task-id> --json
```

对于 v4，应优先调用现有 `Project.inspect_state(...)`。

至少输出可获得的：

- subject identity；
- envelope type；
- authoritative path；
- current lifecycle state / NOW；
- attempt / head；
- relation references；
- family information；
- validation warnings；
- 可用时的 family digest。

### 重要边界

如果 Core 返回 `family_digest` 未就绪、`null` 或明确错误：

- CLI 原样保留不确定性；
- 不得自己计算一个“看起来合理”的 digest；
- 不得把缺失解释成 PASS。

本任务不得顺便修复 PR #37 或其他未授权 Core 并发 / convergence 缺口。

---

## 4.4 `fcop validate`

### 目的

验证当前 workspace 或指定 envelope 是否符合当前已安装 FCoP 协议。

建议：

```text
fcop validate
fcop validate --root <path>
fcop validate --path <path>
fcop validate --json
```

### 检查范围

仅使用现有协议事实可验证的项目，包括：

- workspace/config parse；
- protocol declaration；
- envelope frontmatter / schema；
- lifecycle path consistency；
- filename / identity consistency；
- references 可解析性；
- Core 已实现的其他 deterministic validation。

### 禁止

`validate` 只能判断完全可观察事实。

不得：

- 评价任务业务是否“做得好”；
- 代替 PM / ADMIN / QA / EVAL；
- 修改任何业务文件；
- 自动修复；
- 因模型推测给 PASS。

### 退出语义

至少区分：

- valid；
- protocol/data invalid；
- unsupported/unavailable；
- internal execution failure。

具体 exit code 在 WP0 冻结，但必须有自动化测试和文档。

---

## 4.5 `fcop tools`

### 目的

查看当前安装的 `fcop-mcp` 实际声明工具面。

建议：

```text
fcop tools
fcop tools <tool-name>
fcop tools --json
```

### 唯一事实源要求

不得在 `fcop` CLI 中复制工具清单。

本轮固定方案：

- 将 3 个已经发布并实际注册的 Branch 工具纳入 MCP 的权威声明式 Catalog；
- 为 `fcop-mcp` 提供一个最小、只读、稳定的公开 Tool Catalog 查询接口；
- 该接口必须投影完整的 49 项 MCP authoritative registry；
- Server 注册集合、Catalog 返回集合和 stdio `tools/list` 集合必须三方相等；
- `fcop tools` 通过 optional discovery 调用该接口。

允许：

```text
fcop installed
fcop-mcp not installed
```

即 Core 独立安装时，`fcop tools` 必须正常返回明确状态，而不是 import crash。

### 输出

默认至少包含：

- `fcop` version；
- `fcop-mcp` installed / not installed；
- `fcop-mcp` version（若安装）；
- total tool count；
- tool names；
- disposition / policy（若 registry 提供）。

单工具模式应尽量输出：

- name；
- policy/disposition；
- description / signature / schema（仅当 authoritative registry 可可靠提供）。

不得为了丰富显示而维护第二份 metadata。

### 当前基线验收

当前 main 的 Server 实际注册 49 个工具：

```text
fcop tools
```

必须返回完整 49 项，并与 MCP authoritative registry 及真实 stdio
`tools/list` 的工具集合完全一致。

测试必须比较集合来源，不得靠复制或硬编码数字 `49` 维护。

---

## 4.6 `fcop doctor`

### 目的

回答：

> “FCoP 为什么不能正常使用？”

### 至少检查

1. Python runtime 是否满足包声明；
2. `fcop` package/version/import；
3. CLI entry point；
4. `fcop-mcp` installed / not installed；
5. `fcop-mcp` version/import；
6. Core / MCP compatibility check；
7. bundled schema 可读取；
8. bundled rules/spec 可读取；
9. 当前目录 workspace detection；
10. workspace config 是否可解析；
11. MCP Tool Catalog 是否可读取；
12. 关键路径权限 / 基础 filesystem 可读性（只能安全检查）。

### 输出级别

建议：

```text
PASS
WARN
FAIL
```

每一项必须有：

```text
check_id
status
message
evidence
```

JSON 模式应返回结构化 checks array。

### 禁止

- 不启动长期 MCP transport；
- 不写业务对象；
- 不迁移 workspace；
- 不重建配置；
- 不联网下载更新；
- 不自动 pip install；
- 不自动修改 Host；
- 不自动修复。

---

## 4.7 `fcop version`

### 目的

快速查看安装版本关系。

建议输出：

```text
FCoP Core:      4.0.x
FCoP MCP:       4.0.x / not installed
Protocol:       ...
Python:         ...
```

建议：

```text
fcop version
fcop version --json
```

版本来源必须来自 package metadata / authoritative version source。

不得复制版本字符串。

---

## 4.8 `fcop spec`

### 目的

让人、脚本、AI 找到当前安装包携带的协议规范、Schema 和 Rules。

建议：

```text
fcop spec
fcop spec --json
```

至少输出可获得的：

- protocol name；
- supported/current protocol version；
- spec identity/version；
- schema location / bundled schema set；
- rules version；
- rules/spec source location；
- package version。

若需要增加 `--print` / `--path` 等二级 flag，可以在 WP0 评估，但：

- 不得增加新的一级命令；
- 默认输出必须简洁；
- 不得从网络下载“最新规范”覆盖本地安装事实。

---

## 4.9 `fcop migrate`

### 目的

继续承载既有迁移能力。

本任务 **不重新设计 migration engine**。

必须：

- 保持 `fcop migrate --to-v3` 现有行为；
- 保持 dry-run first；
- 只有显式 `--apply` 才写；
- 保留原退出码语义或严格兼容映射；
- 不破坏 `fcop migrate-workspace` 历史入口。

### 本轮不做

不把全部历史迁移路径强行重写成一个新状态机。

如果希望未来统一 `migrate-workspace` 到 `fcop migrate` 下，单独提出 ADR / follow-up，不在本任务扩大。

---

# 5. 通用 CLI 合同

## 5.1 `--root`

适用于 workspace 相关命令：

```text
init
status
inspect
validate
doctor
```

若未提供，默认使用当前工作目录。

必须使用 `pathlib` / 现有 Project path resolution；不得写死 Windows 分隔符。

## 5.2 `--json`

以下命令必须支持：

```text
init
status
inspect
validate
tools
doctor
version
spec
```

`migrate` 保持现有输出合同，本任务不强制为旧 migration 改 JSON surface；如可无破坏增加，可作为可选项，但不得拖大范围。

## 5.3 stdout / stderr

- 业务结果：stdout；
- diagnostics / parser errors：stderr；
- JSON 模式 stdout 必须保持纯 JSON；
- 不允许 JSON 前后出现日志、banner、ANSI 控制符。

## 5.4 Exit Codes

WP0 必须定义统一表。

最低要求：

```text
0 = success / healthy / valid
1 = command execution/internal failure
2 = invalid protocol/data/user input
3 = unavailable/unsupported dependency or environment
```

如保留现有 migration 特殊码，必须文档化，不得为“统一”而破坏兼容。

## 5.5 Bare `fcop`

当前 bare `fcop` 的历史兼容行为属于既有合同。

**本任务不得擅自改变 bare `fcop` 行为。**

CLI discovery 使用：

```text
fcop --help
```

若未来要把 bare `fcop` 改成 help + exit 0，需单独 ADMIN 兼容性裁定。

---

# 6. `fcop` 与 `fcop-mcp` 的依赖边界

FCoP Core 继续保持：

> No MCP dependency in Core.

`fcop` 包的 Core modules 不得 import FastMCP / MCP runtime。

`fcop tools` / `fcop doctor` 可以在 CLI Adapter 层做 **optional package discovery**。

推荐结构之一：

```text
src/fcop/cli/
    _main.py
    _common.py
    init.py
    status.py
    inspect.py
    validate.py
    tools.py
    doctor.py
    version.py
    spec.py
    migrate_v3.py
    migrate_workspace.py

mcp/src/fcop_mcp/
    ...
    catalog.py   # only if needed: minimal public read-only catalog
```

文件名可根据当前代码风格调整，但职责边界不得改变。

如果新增 `fcop_mcp.catalog`：

- 必须从现有 authoritative tool registry 生成；
- 不得复制 `TOOLS`；
- 不得启动 Server 才能读取；
- 不得修改 MCP tool names / signatures / semantics；
- 必须可独立单测。

本任务明确授权修正 `fcop_mcp.disposition.TOOLS` 与实际 49 项 Server
工具面的漂移：只允许补入已经存在的 `create_branch`、`inspect_family`、
`merge_branches` 及其既有 disposition，不得借机新增、删除、重命名工具，
也不得改变任何工具签名或业务语义。

---

# 7. 工作包

## WP0 — Baseline & Contract Freeze

先做，不改业务代码。

1. Fetch latest `origin/main`。
2. 记录：
   - Core version；
   - MCP version；
   - CLI entry point；
   - 现有 subcommands；
   - 当前 Tool Registry；
   - public Project APIs；
   - existing test count；
   - package split/version policy。
3. 冻结：
   - 9 个一级命令；
   - global/common flags；
   - exit code table；
   - JSON envelope conventions；
   - readonly/write classification。
4. 产出：
   - `reports/FCOP-4.0-CLI-V1-BASELINE.md`
   - `reports/FCOP-4.0-CLI-V1-CONTRACT.md`

若发现需要改变协议语义，STOP，该项不授权。

---

## WP1 — CLI Infrastructure

实现共享但保持很薄：

- top-level parser registration；
- common root resolution；
- JSON serializer；
- deterministic result envelope；
- common exit-code mapping；
- stdout/stderr isolation；
- shared error rendering。

不得建立“CLI framework inside FCoP”。

优先 stdlib `argparse`，除非仓库 main 已经采用其他正式依赖。

不得为 CLI 引入 Click/Typer/Rich 等新 runtime dependency，除非有明确不可替代证据并单独报告。

---

## WP2 — Read-only Core Commands

实现：

```text
status
inspect
validate
version
spec
```

要求：

- 优先调用 public Core API；
- 不写 workspace；
- 不写报告；
- 不修复；
- human / JSON 双输出；
- Windows path tests；
- invalid / uninitialized / v3 / v4 边界测试。

---

## WP3 — Init

实现：

```text
fcop init
```

要求：

- 只通过 Core bootstrap；
- 默认不创建业务 TASK；
- 不安装 MCP；
- 不修改 Codex/Cursor/Claude/ChatGPT Host config；
- already-initialized 行为确定；
- crash/partial state 不得被 CLI 隐式猜测修复；
- v4 workspace identity 可在结果中明确返回。

---

## WP4 — MCP Catalog + Tools + Doctor

### 4A. Tool Catalog

实现 `fcop-mcp` 的最小公开只读 catalog surface，并把既有 3 个 Branch
工具纳入同一权威声明源。该变化构成 `fcop-mcp 4.0.2` 的真实公共能力改进，
不是为了版本整齐而空发包。

证明：

```text
catalog tool set == server authoritative registered tool set
catalog tool set == stdio tools/list tool set
```

不得通过复制两份名单让测试“恰好相等”。

### 4B. `fcop tools`

实现 human / JSON / single-tool view。

`fcop-mcp` 未安装必须 graceful degradation。

### 4C. `fcop doctor`

实现 deterministic checks。

`doctor` 不执行 repair。

---

## WP5 — Migration Compatibility

1. 运行所有现有 CLI migration tests。
2. 保证：
   - `migrate-workspace` 不变坏；
   - `migrate --to-v3` 不变坏；
   - bare `fcop` 兼容合同不变坏；
   - new parser registration 不抢旧 flags。
3. 增加 compatibility regression tests。

---

## WP6 — Docs, Packaging, Release Preparation

更新：

- root README / README.zh；
- PyPI-facing `fcop` README：`fcop-README.pypi.md`；
- PyPI-facing `fcop-mcp` README：`mcp/README.md`；
- PyPI 说明源记录：`docs/pypi/README.md`；
- CLI 英文参考：`docs/cli.md`；
- CLI 中文参考：`docs/cli.zh.md`；
- `docs/mcp-tools.md` 中补充 `fcop tools` 与同一 Catalog 的关系；
- CHANGELOG；
- `--help` 文本；
- `fcop-mcp` public catalog API note。

文档必须明确：

```text
CLI = Setup + Observe + Diagnose
MCP = Work
```

提供两段最短 quick start：

```text
pip install fcop
fcop version
fcop doctor
fcop init
fcop status
```

若用户还安装 MCP：

```text
pip install fcop-mcp
fcop tools
```

不得把 CLI 文档写成 MCP 业务操作教程。

两份 PyPI 长说明必须随本轮 4.0.2 制品一起构建并实际更新公开页面：

- `fcop` 页面增加 9 个 CLI 命令、定位、最短 Quick Start、退出码与
  `--json` 入口，但不得弱化 Core/CLI/MCP 的包边界；
- `fcop-mcp` 页面保留 49/12/4 与 3 个 Branch 工具，并增加
  `fcop tools` 作为 Catalog 查看入口；
- 两页不得再次混入候选版、待批准、旧稳定版或大段历史迁移说明；
- 发布后必须逐页与 GitHub 权威源核对。

---

# 8. 测试要求

## 8.1 新命令测试

每个命令至少覆盖：

- `--help`；
- successful human output；
- successful `--json`；
- invalid input；
- missing workspace；
- path with spaces；
- Windows-compatible path handling；
- no unintended writes。

## 8.2 Read-only Proof

对以下命令：

```text
status
inspect
validate
tools
doctor
version
spec
```

测试前后对测试 workspace 做文件树 + content hash 比较。

要求：

```text
before == after
```

除 OS/pytest 自身临时文件外不得有 FCoP workspace mutation。

## 8.3 Tool Catalog Proof

必须有自动测试证明：

```text
CLI catalog names
==
MCP authoritative registry names
==
stdio tools/list names
```

当前 4.0.1 基线应观察到 49 个工具，但测试必须比较三个事实源的集合，
不得靠硬编码 49 维持通过。

## 8.4 Core Independence Proof

必须证明：

```text
pip install fcop
```

在没有 `fcop-mcp` 的环境中：

```text
fcop version
fcop status
fcop validate
fcop spec
fcop doctor
fcop tools
```

不会因 `ImportError: fcop_mcp` 整体崩溃。

其中 `fcop tools` 应明确报告：

```text
fcop-mcp: not installed
```

## 8.5 MCP Non-regression

若修改 `fcop-mcp`：

- 所有现有 MCP tool contract tests 必须通过；
- tool names unchanged；
- tool parameters unchanged；
- tool semantics unchanged；
- resources unchanged；
- no new MCP tool added；
- no MCP tool removed。

## 8.6 Full Regression

运行仓库现有完整测试集。

不允许只跑新测试后宣称完成。

---

# 9. 验收矩阵

| ID | Requirement | Expected |
|---|---|---|
| C01 | `fcop --help` | 显示 v1 命令和兼容 migration |
| C02 | `fcop init` | 通过 Core 创建 workspace |
| C03 | `fcop status` | 只读、确定性状态 |
| C04 | `fcop inspect` | 使用 Core authoritative inspection |
| C05 | `fcop validate` | 只验证可观察协议事实 |
| C06 | `fcop tools` | 无复制清单，投影 MCP registry |
| C07 | MCP absent | `fcop tools/doctor` graceful degradation |
| C08 | `fcop doctor` | PASS/WARN/FAIL structured checks |
| C09 | `fcop version` | authoritative package versions |
| C10 | `fcop spec` | authoritative bundled spec/schema/rules |
| C11 | `fcop migrate --to-v3` | old behavior preserved |
| C12 | `fcop migrate-workspace` | old behavior preserved |
| C13 | bare `fcop` | existing compatibility preserved |
| C14 | observation commands | filesystem no-write proof |
| C15 | JSON | pure stdout JSON |
| C16 | CLI/Core boundary | no MCP runtime dependency in Core |
| C17 | MCP tool contract | no add/remove/rename/signature change |
| C18 | Windows paths | pass |
| C19 | full regression | pass |
| C20 | docs | EN/ZH CLI role clearly documented |

必须 C01–C20 全部 PASS 才能进入合并与发布；任一失败立即停止并报告。

---

# 10. Release / PyPI 规则

当前基线版本为：

```text
fcop      4.0.1
fcop-mcp  4.0.1
```

该基线已于 2026-09-11 从仓库最新 `main` 的两个权威 `_version.py` 文件核验。
执行时 Codex 仍必须重新 fetch 最新 `origin/main`；若任一版本已继续前进，
不得硬编码 `4.0.2`、不得自行改发其他版本，必须记录
`VERSION_BASELINE_ADVANCED` 并停止。

本任务会改变已发布 `fcop` wheel 的 CLI 能力，并修正 `fcop-mcp` 的
公开 Tool Catalog 事实源，因此必须发布新的两包，不能只停留在 GitHub。

## 10.1 版本

当前基线下的目标版本固定为：

```text
fcop      4.0.2
fcop-mcp  4.0.2
```

`fcop-mcp 4.0.2` 不是空发布：它包含 49 项单一事实源修正、公开只读
Catalog API、对应测试及更新后的 PyPI 长说明。

若执行开始时任一包已高于 `4.0.1`，STOP 并报告
`VERSION_BASELINE_ADVANCED`，不得自行推导一组新的发布版本。

必须遵守仓库当前 package version policy，并从权威 version source 修改版本号，不得在多处手工维护。

## 10.2 Codex 本轮发布权限

Codex 被授权在全部 Release Gates 通过后，将 PR 合并到 `main`，创建仅有的
`v4.0.2` tag 与 GitHub Release，并从该精确 tag 发布两包到 PyPI。

发布前必须同时满足：

```text
C01-C20 ALL PASS
+ full regression PASS
+ MCP non-regression PASS
+ read-only proof PASS
+ Core-without-MCP proof PASS
+ package build PASS
+ twine check PASS
+ clean install from built artifacts PASS
+ Draft PR created
+ release evidence + manifest complete
+ PR head has not moved since final verification
+ mergeable without unresolved conflicts
```

任何一项失败：

```text
STOP
PYPI_PUBLISH = FORBIDDEN
```

不得降级验收、不得跳过失败项、不得用“非关键失败”理由继续发布。

## 10.3 发布顺序

授权顺序固定为：

```text
1. Fetch latest origin/main
2. Implement CLI Adapter v1
3. Run C01-C20
4. Run full regression
5. Build wheel/sdist
6. twine check
7. Fresh isolated install from local built artifacts
8. Create/update Draft PR and evidence package
9. Confirm PR exact HEAD, checks, changed files and mergeability
10. Mark PR ready and merge into main
11. Verify merged main contains the exact accepted content
12. Create tag `v4.0.2` on the merged release commit
13. Build/verify final artifacts from that exact tag checkout
14. Publish both packages to PyPI
15. Create/update GitHub Release for `v4.0.2`
16. Fresh isolated install of both packages from PyPI
17. Re-run release smoke tests and inspect both public PyPI descriptions
18. Record versions, links, artifact hashes, tag binding and PyPI page comparison
19. Post final release receipt on the merged PR
20. Stop
```

PyPI 发布完成后必须从 **PyPI 实际安装**，不能只验证本地 wheel。

至少验证：

```text
pip install --no-cache-dir fcop==4.0.2
fcop version
fcop doctor
fcop --help
fcop status
fcop spec
```

必须同时验证：

```text
pip install --no-cache-dir fcop-mcp==4.0.2
fcop tools
```

并证明 PyPI 安装后的 Tool Catalog 与 authoritative MCP registry 一致。

## 10.4 发布后的失败处理

PyPI version 不可覆盖。

如果 PyPI 发布后 smoke test 失败：

- 不得删除或覆盖已发布版本；
- 立即记录 `RELEASE_POST_PUBLISH_FAILURE`；
- 停止继续发布其他 package；
- 不得自行发布下一 patch 版本；
- 在 Draft PR 和 evidence 中完整记录；
- 请求 ADMIN 裁定后续修复版本。

## 10.5 仍然禁止

Codex 仍然不可以：

- 在 Release Gates 未全部通过时 merge PR 或 push main；
- 合并本任务 PR 之外的任何 PR；
- 擅自创建新的 major/minor release；
- 因失败自动再发 `4.0.2`；
- 修改 PyPI 已发布版本内容；
- 跳过 release evidence。

除 `v4.0.2` 外不得创建其他 tag 或 GitHub Release。

---

# 11. GitHub 交付

使用统一 GitHub 审核交付。

必须：

1. 从最新 `origin/main` 建开发分支；
2. 仅修改本任务所需文件；
3. 提交完整测试证据；
4. 创建 Draft PR；
5. 全部 Release Gates 通过前不 merge、不 publish；
6. 全部通过后按第 10.3 节连续完成 merge、tag、GitHub Release 与两包发布。

Draft PR 至少包含：

- Scope；
- Non-scope；
- architecture summary；
- command matrix；
- exact changed files；
- test commands；
- test counts；
- read-only proof；
- tool catalog equality proof；
- package build result；
- version recommendation；
- known limitations；
- unresolved findings。

建议 evidence 目录：

```text
reviews/fcop-4.0/cli-v1/
```

至少包含：

```text
BASELINE.md
CONTRACT.md
TEST-RESULTS.md
READONLY-PROOF.md
MCP-CATALOG-PROOF.md
PACKAGE-PROOF.md
MANIFEST.md
```

如仓库最新 main 已有新的 review 目录规范，服从最新 main。

---

# 12. 明确禁止范围

本任务不得：

- 修改 FCoP 4.0 协议语义；
- 修改 TASK / REPORT / ISSUE / REVIEW schema 语义；
- 修改 Authorization 权限边界；
- 修改 Branch / Convergence 语义；
- 修复 PR #37 中未授权的 Core gap；
- 改变 lifecycle T1–T7 决策；
- 增加/删除 MCP work tools；
- 把 MCP 工具复制成 CLI；
- 把 CodeFlowMu 逻辑加入 FCoP；
- 修改 CodeFlowMu；
- 加 Host-specific Codex/Cursor 业务逻辑；
- 增加自动 repair；
- 增加网络更新器；
- 增加 background daemon；
- 把 CLI 做成新的 workflow engine；
- 因 CLI 开发顺便“清理”无关历史代码。

发现无关缺陷：记录，不扩大修复范围。

---

# 13. Codex 完成回执

完成后必须按以下格式回复 ADMIN：

```text
FCOP-4.0-CLI-ADAPTER-V1

STATUS:
BRANCH:
COMMIT:
DRAFT_PR:

COMMANDS:
- init:
- status:
- inspect:
- validate:
- tools:
- doctor:
- version:
- spec:
- migrate compatibility:

MCP_TOOL_COUNT_OBSERVED:
CATALOG_EQUALS_MCP_REGISTRY:
READONLY_PROOF:
CORE_WITHOUT_MCP_PROOF:
MCP_NON_REGRESSION:

TESTS:
FULL_REGRESSION:

PACKAGES_BUILT:
FCOP_VERSION_PROPOSED:
FCOP_MCP_VERSION_PROPOSED:

PYPI_PUBLISHED:
PYPI_FCOP_VERSION:
PYPI_FCOP_MCP_VERSION:
PYPI_FRESH_INSTALL_PROOF:
PYPI_DESCRIPTION_MATCH:
GITHUB_RELEASE:
TAG:
TAG_COMMIT:
MAIN_MERGED:

KNOWN_LIMITATIONS:
UNRESOLVED_FINDINGS:

REQUESTED_ADMIN_GATE:
CLI_V1_RELEASE_COMPLETED
```

如果 C01–C20 未全部通过，必须停止，`REQUESTED_ADMIN_GATE: NONE`。

---

# 14. 最终完成定义

本任务的“完成”不是：

- 代码写完；
- 命令能启动；
- 新测试通过；
- Codex 说完成。

只有以下事实同时成立才算 implementation-ready：

```text
9-command CLI contract implemented
+ legacy migration preserved
+ observation commands proven read-only
+ tool catalog has one authoritative source
+ fcop works without fcop-mcp installed
+ MCP work surface unchanged
+ full regression passes
+ package build passes
+ documentation complete
+ GitHub English/Chinese, CLI reference and both PyPI descriptions complete
+ PR merged to main from the fully verified HEAD
+ v4.0.2 tag and GitHub Release bound to the merged release commit
+ authorized PyPI release completed
+ fresh install from PyPI passes
+ release smoke tests pass
+ both public PyPI descriptions match their GitHub canonical sources
+ published artifact hashes recorded
```

然后停止，等待 ADMIN 对合并与正式发布结果进行最终审核。

**Release Gates 全部通过前不得合并或发布；全部通过后必须一次完成本任务 PR
合并、`v4.0.2` tag、GitHub Release、PyPI 两包发布及公开回装核验。**
