# FCoP 4.0.3 — 旧“四件套”规则分发退出与正式发布任务书 v1.0

- Repository: `joinwell52-AI/FCoP`
- Target release: `fcop==4.0.3` + `fcop-mcp==4.0.3`
- Task type: implementation + documentation + packaging + release
- Delivery: GitHub review branch + Draft PR + evidence package
- Merge authority: ADMIN only; Codex MUST NOT merge `main` without explicit ADMIN authorization
- Release authority: 仅在本任务全部 Gate 通过、ADMIN 明确授权发布后，才允许发布 PyPI/GitHub Release/MCP Registry

---

## 1. 任务目标

FCoP 4.x 正式退出 3.x 时代的“Host 规则四件套”模型：

```text
.cursor/rules/fcop-rules.mdc
.cursor/rules/fcop-protocol.mdc
AGENTS.md
CLAUDE.md
```

这些文件不再属于 FCoP 4.x 的正常安装、初始化、升级或协议运行范围。

FCoP 4.x 的正常用户模型必须收敛为：

```text
pip install fcop / fcop-mcp
        ↓
Host 连接 fcop-mcp
        ↓
初始化 FCoP 4.0 workspace
        ↓
<project>/fcop/
        ↓
Agent 通过 MCP tools/resources 使用 FCoP
```

不得再要求用户维护、同步、重部署任何项目根 Host 指令文件。

---

## 2. 必须新增/冻结的协议所有权边界

在 FCoP 4.0 正式规范的 ownership / layer / boundary 位置加入下述正式不变量，并保持中英文条款一致：

> **FCoP MUST NOT create, replace, modify, merge into, or require project-root Host/Agent instruction files as part of protocol installation, workspace initialization, upgrade, or normal protocol operation. Project-root Host instruction files are outside FCoP ownership.**

中文：

> **FCoP 在协议安装、工作区初始化、升级及正常协议运行过程中，不得创建、替换、修改、合并写入或依赖宿主项目根目录的 Host/Agent 指令文件。宿主项目根目录的 Host/Agent 指令文件不属于 FCoP 的所有权范围。**

并补充：

> **FCoP owns only the protocol workspace and package-owned rule resources. Application and Host configuration remain application-owned.**

中文：

> **FCoP 仅拥有协议工作区及包内规则资源；应用配置与 Host 配置始终由宿主应用拥有。**

该条款不是安装建议，而是 FCoP 4.x 的协议所有权边界。

---

## 3. 正常 FCoP 4.x 初始化的唯一允许写入范围

`create_workspace()`、CLI `fcop init`、MCP v4 初始化路由及所有正常 4.x 协议操作，必须保证：

```text
<project>/fcop/
├── fcop.json
├── _lifecycle/
│   ├── inbox/
│   ├── active/
│   ├── review/
│   ├── done/
│   └── archive/
├── reports/
├── issues/
├── reviews/
├── operations/
└── cold/
```

后续协议事实仍按现有 4.0 Core 创建 TASK / REPORT / ISSUE / REVIEW、operation/recovery facts。

不得因 4.x 正常安装、初始化、升级或运行而创建、修改、覆盖、合并、删除：

```text
<project>/AGENTS.md
<project>/CLAUDE.md
<project>/.cursor/**
<project>/GEMINI.md
或任何未来 Host 专属指令文件
```

现有用户文件必须视为 application-owned bytes。

---

## 4. FCoP 4.x 规则与 Agent guidance 的唯一现行分发模型

保留并强化当前包内模块化规则：

```text
src/fcop/rules/_data/v4/
├── manifest.json
├── workspace.{en,zh}.md
├── envelopes.{en,zh}.md
├── relations.{en,zh}.md
├── authorization.{en,zh}.md
├── idempotency.{en,zh}.md
├── recovery.{en,zh}.md
├── lifecycle.{en,zh}.md
├── compatibility.{en,zh}.md
└── convergence.{en,zh}.md
```

保留：manifest、hash、normative clause refs、depends_on、load_order、language selection、sequential/parallel assembly、read/validate/select。

FCoP 4.x Agent guidance 通过 MCP resources 暴露：

```text
fcop://rules
fcop://protocol
fcop://guidance/sequential/en
fcop://guidance/sequential/zh
fcop://guidance/parallel/en
fcop://guidance/parallel/zh
```

不得再把这些规则复制/投影到项目根 Host 文件。

---

## 5. 退出 v4 Host 文件投影

审计并移除/关闭 FCoP 4.x 当前 rule-distribution 中的 Host 文件投影能力，包括但不限于：

```text
codex       -> AGENTS.md
cursor      -> .cursor/rules/fcop-v4.mdc
claude-code -> CLAUDE.md
```

对于 v4，删除或退役以下仅服务于项目根 Host 文件投影的语义/实现：

- Host target mapping；
- Host-specific output path；
- bounded_embed/reference Host projection；
- project-root projection planning/apply；
- Host-file backup/replace/rollback；
- Host projection adoption/deployment receipts；
- projection byte-limit contract；
- 仅证明 AGENTS/CLAUDE/Cursor target 的 conformance tests；
- 仅为上述写盘能力存在的 `fcop/internal/rule-distribution/` 状态。

不得误删 rule package 的读取、选择、校验、assembly 或 MCP resource 能力。

若内部模块命名 `rule_distribution` 已不再准确，允许在不破坏公开 4.0 API 的前提下内部重构；禁止为“目录好看”修改 Core 语义。

---

## 6. 3.x 历史兼容与旧“四件套”

历史事实必须保留：ADR、旧 release notes、CHANGELOG、migration 文档可继续记录 3.x 曾采用“四件套”。

但所有“当前 4.x 用户入口”必须停止把四件套描述为现行安装组成、健康指标或升级步骤。

禁止改写历史文件来伪装从未存在过四件套；只允许在必要位置增加 `Legacy 3.x / Historical` 标识或从当前入口移除引用。

升级到 4.0.3 时，不得自动删除用户项目中已经存在的 `AGENTS.md`、`CLAUDE.md` 或 `.cursor/*`。即使其内容看起来来自旧 FCoP，也只能提示迁移；删除/修改权属于用户。

---

## 7. MCP 工具合同：49 / 12 / 4 保持不变

本任务不得通过删除公开 MCP 工具来完成整改。

目标发布仍必须保持：

```text
49 tools
12 resources
4 templates
```

### 7.1 `redeploy_rules`

`redeploy_rules` 继续保留公开工具名与参数合同，以保持 4.0.x patch 兼容。

但必须明确为 **Legacy v1-v3 only**：

- 对声明为 FCoP 4.0 的 workspace：零写入；不得生成/修改 `AGENTS.md`、`CLAUDE.md`、`.cursor/*`；返回现有兼容的 typed no-op / rejection 结果，优先复用当前 v4 `OPERATION_NOT_IMPLEMENTED` / version-boundary 行为，不为本任务随意新增协议错误码；
- 对仍受支持的 legacy v1-v3 workspace：保持既有兼容行为，除非现有 4.x 兼容合同已经明确禁止；
- 更新 tool description、disposition、MCP docs，明确它不是 FCoP 4.x 正常工作流的一部分。

### 7.2 `init_project` / `init_solo`

完整追踪 MCP adapter/router/server 路由。

对于明确的 v4 初始化：

- 必须最终走 4.0 `create_workspace()`；
- 不得调用 legacy `deploy_rules=True` 路径；
- 不得写项目根 Host 文件；
- 返回 workspace identity / v4 结构化结果保持当前合同。

对于 legacy workspace 初始化，仅保留已冻结的兼容行为，不得让 legacy convenience 反向成为 4.x 默认行为。

### 7.3 MCP resources

验证 4.0 rules/protocol/guidance resources 可以在完全不存在 `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/` 的客户目录中独立工作。

---

## 8. FCoP 仓库自身的旧四件套清理

FCoP GitHub 仓库根目录及 `.cursor/rules/` 中当前由旧机制生成/镜像的协议大文件，不再作为 FCoP 4.x 协议制品。

要求：

1. `AGENTS.md` 不得继续作为 `fcop-rules + fcop-protocol` 的 100KB+ 协议镜像；
2. `CLAUDE.md` 不得继续作为同内容的 FCoP 协议镜像；
3. `.cursor/rules/fcop-rules.mdc` / `fcop-protocol.mdc` 不得继续被定义为 4.x 标准分发制品；
4. 若仓库维护本身仍需要 `AGENTS.md` 作为 Codex repository instruction，可保留/重建为**短小、repository-owned、非协议制品**的开发入口，必须明确：它不属于 FCoP 协议、不随包发布、不向客户部署、不激活 FCoP workspace；
5. 不得为了兼容 Claude/Cursor 再复制同一份协议正文。

最终是否保留短 `AGENTS.md`，以当前仓库实际维护需要和现有自动化为准；但“协议镜像”身份必须彻底消失。

---

## 9. README、文档、FCoP 主页

必须同步更新至少：

- `README.md`
- `README.zh.md`
- 当前 FCoP 4.x getting-started / upgrade / MCP tool 文档
- `docs/mcp-tools.md`
- FCoP GitHub Pages 主页及其真正源文件/生成流程（当前公开主页 `https://joinwell52-ai.github.io/FCoP/`）
- 任何当前状态页/介绍页中“四件套已同步/待升级/redeploy 四件套”的现行表述

首页和 README 必须用同一用户心智：

```text
Install -> connect MCP -> initialize workspace -> use FCoP
```

并明确：

```text
FCoP owns <project>/fcop/
FCoP does not own project-root Host instruction files.
```

不要在主入口继续讲 0.x/1.x/2.x/3.x 的历史细节；历史链接到 release/migration/ADR。

---

## 10. PyPI 两个项目说明必须更新

两个 PyPI 页面都必须随 4.0.3 发布更新。

唯一说明源：

```text
fcop      -> /fcop-README.pypi.md
fcop-mcp  -> /mcp/README.md
```

同时维护 `docs/pypi/README.md` 的说明/发布检查信息。

PyPI 当前说明必须：

- 标明 stable 4.0.3；
- 正确说明 `fcop` 与 `fcop-mcp` 边界；
- 保持 CLI = Setup + Observe + Diagnose；MCP = Work 的当前定位（除非主线已经正式改变）；
- 保持 MCP `49 tools / 12 resources / 4 templates`；
- 移除任何把四件套、`AGENTS.md`、`CLAUDE.md`、Cursor rule deployment 或 `redeploy_rules()` 当作 4.x 标准安装/升级步骤的表述；
- 明确规则由包内 v4 rule resources + MCP resources 提供；
- 明确正常 v4 workspace 写入范围为 `fcop/`。

构建 wheel/sdist 后必须检查实际 METADATA long description；发布后必须从公网 PyPI 再核验两个页面与 tag 源文件一致。

---

## 11. 版本、发布与 Registry

将两个包同步升级：

```text
fcop       4.0.2 -> 4.0.3
fcop-mcp   4.0.2 -> 4.0.3
```

同步所有版本绑定、compatibility pins、build metadata、release notes、CHANGELOG。

发布 Gate 通过并获得 ADMIN 明确授权后：

1. 发布 `fcop==4.0.3` 到 PyPI；
2. 发布 `fcop-mcp==4.0.3` 到 PyPI；
3. 创建 Git tag / GitHub Release `v4.0.3`，附上两包制品 hash；
4. 更新 FCoP GitHub Pages；
5. 若官方 MCP Registry 当前登记含版本/README/description，更新到 4.0.3 并核验公网 Registry 结果；
6. 公网回装两个包，验证版本与行为；
7. 公网核验 GitHub、PyPI 两页面、主页、Registry（如适用）一致。

没有 ADMIN 发布授权，不得上传 PyPI、不得发布 GitHub Release、不得更新 Registry 的正式版本记录。

---

## 12. 强制回归测试

必须新增“项目根所有权”回归测试。

### 12.1 Existing-root-files byte preservation

准备一个客户目录，预先放入任意非 FCoP 内容：

```text
AGENTS.md
CLAUDE.md
.cursor/rules/customer.mdc
GEMINI.md
README.md
任意其他用户文件
```

记录完整 byte hash。

执行：

- v4 workspace initialization；
- CLI setup/observe/diagnose 代表性路径；
- MCP v4 init；
- 代表性 TASK/REPORT/REVIEW/lifecycle；
- MCP rules/protocol/guidance resource reads；
- 4.0.3 upgrade/reopen；
- `redeploy_rules` against declared v4 workspace。

断言：

- 所有预存项目根文件 byte-for-byte 不变；
- 不新增 `AGENTS.md` / `CLAUDE.md` / `.cursor/rules/fcop-*`；
- `redeploy_rules` 对 v4 零写入；
- FCoP 的正常新状态只位于 `fcop/`；
- MCP resources 在没有 Host rule files 时仍正常工作。

### 12.2 Package artifact boundary

wheel/sdist 不得包含作为消费者部署目标的：

```text
AGENTS.md
CLAUDE.md
fcop-v4.mdc
```

但必须包含完整 `src/fcop/rules/_data/v4/` 模块与 manifest。

保留/扩展现有相应 closeout tests。

### 12.3 MCP public surface

断言：

```text
49 tools
12 resources
4 templates
```

工具名及既有参数合同不得因本整改意外变化。

---

## 13. 不得修改的 Core 语义

本任务不是 FCoP Core 重构。除新增 ownership boundary 条款外，不得改变：

- 四 Envelope：TASK / REPORT / ISSUE / REVIEW；
- lifecycle T1-T7；
- relations；
- authorization；
- idempotency；
- recoverable atomic semantics；
- Branch/convergence；
- family digest；
- 现有 4.0 workspace encoding；
- CLI/MCP 对业务 Core 的既有行为合同。

发现 unrelated defect 时记录 ISSUE，不得顺手扩大任务。

---

## 14. 交付证据

使用 GitHub review delivery。建议证据目录：

```text
reviews/fcop-4.0/4.0.3-four-file-retirement/
├── BASELINE.md
├── OWNERSHIP-BOUNDARY.md
├── MCP-SURFACE.md
├── ROOT-BYTE-PRESERVATION.md
├── PACKAGE-PROOF.md
├── PYPI-DESCRIPTION-PROOF.md
├── WEBSITE-PROOF.md
├── TEST-RESULTS.md
├── RELEASE-PLAN.md
└── MANIFEST.md
```

若 `main` 已存在更新的统一 review 目录规范，以最新规范为准，但必须保证上述证据语义全部覆盖。

`MANIFEST.md` 必须至少记录：

- base commit；
- final branch HEAD；
- changed files；
- SHA-256；
- test counts；
- MCP 49/12/4 proof；
- wheel/sdist hashes；
- README/PyPI/homepage source identity；
- public release checks（仅发布后）；
- unresolved items；
- requested ADMIN gate。

---

## 15. Codex 执行流程

1. `fetch origin`，以执行时最新 `origin/main` 为唯一开发基线；
2. 阅读本任务书和当前 4.0 Stable spec、现有 4.0 rule package、MCP disposition、release SOP；
3. 做 baseline inventory：列出所有四件套/Host projection/redeploy_rules/current-doc references；
4. 先写回 baseline 证据，再实施；
5. 完成 ownership boundary + implementation + MCP + docs + PyPI source + homepage source；
6. 跑定向测试；
7. 跑全量测试与现有 release verification；
8. build 两个 wheel + sdist，检查内容与 METADATA；
9. 创建/更新 review evidence；
10. push review branch；
11. 创建 Draft PR，禁止自动 merge；
12. 在 PR 中给出完整完成回执并请求 ADMIN Gate；
13. 仅在 ADMIN 明确授权 release 后执行 PyPI/GitHub Release/MCP Registry/Pages 的正式发布步骤；
14. 发布后执行公网核验并把证据回写 PR/review 目录。

---

## 16. 完成判定

只有同时满足以下条件，实施阶段才可报告 READY_FOR_ADMIN_REVIEW：

- [ ] 协议 ownership boundary 中英文一致且通过规范校验；
- [ ] v4 正常路径不创建/修改/依赖项目根 Host instruction files；
- [ ] v4 Host file projection 已退出当前产品路径；
- [ ] `redeploy_rules` 对 v4 零写入且明确 Legacy-only；
- [ ] MCP 仍为 49 tools / 12 resources / 4 templates；
- [ ] v4 rules/protocol/guidance resources 独立工作；
- [ ] 客户根目录 byte-preservation 回归通过；
- [ ] `fcop` / `fcop-mcp` 均为 4.0.3 release candidate bytes；
- [ ] README EN/ZH 更新；
- [ ] FCoP 主页源更新并验证；
- [ ] 两个 PyPI canonical description source 更新；
- [ ] wheel/sdist/metadata 校验通过；
- [ ] 全量测试通过；
- [ ] review evidence + MANIFEST 完整；
- [ ] Draft PR 已创建；
- [ ] 未未经授权 merge main；
- [ ] 未未经授权发布 PyPI/GitHub Release/Registry。

发布完成后追加：

- [ ] PyPI `fcop==4.0.3` 公网可安装；
- [ ] PyPI `fcop-mcp==4.0.3` 公网可安装；
- [ ] GitHub Release `v4.0.3` 与制品 hash 一致；
- [ ] FCoP 主页公开内容一致；
- [ ] MCP Registry（如适用）公开记录一致；
- [ ] 公网 fresh install 验证无四件套写盘。

---

## 17. 最终回执格式

Codex 最终必须给 ADMIN：

```text
STATUS:
BASE_COMMIT:
BRANCH:
FINAL_COMMIT:
DRAFT_PR:
FCOP_VERSION:
FCOP_MCP_VERSION:
MCP_SURFACE: <tools>/<resources>/<templates>
ROOT_OWNERSHIP_TEST:
FULL_TESTS:
PACKAGE_HASHES:
PYPI_DESCRIPTION_STATUS:
HOMEPAGE_STATUS:
PUBLIC_RELEASE_STATUS:
MCP_REGISTRY_STATUS:
UNRESOLVED:
REQUESTED_ADMIN_GATE:
```

实施完成但尚未获得发布授权时：

```text
REQUESTED_ADMIN_GATE: FCOP_4_0_3_FOUR_FILE_RETIREMENT_ACCEPTED
```

发布完成后再请求最终 release closeout gate，不得把“代码完成”等同于“发布完成”。
