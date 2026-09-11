# FCoP 4.0 CLI Adapter v1：正式规范身份与 PyPI 双页整改修订书

**Amendment ID:** `FCOP-4.0-CLI-ADAPTER-V1-RELEASE-IDENTITY-A1-20260911`  
**Repository:** `joinwell52-AI/FCoP`  
**Execution target:** Codex  
**Base taskbook:** `taskbooks/fcop-4.0/CLI-V1/01-CLI-Adapter-v1-Development-Taskbook-v4.zh.md`  
**Applies to:** Draft PR #40  
**Date:** 2026-09-11

---

## 1. ADMIN 决策

FCoP 4.0 已经实现并正式发布，不再是 Candidate。

本修订书解决两项由旧文档合同造成的发布阻断，并把 GitHub 权威文档与
PyPI 两个公开页面纳入同一次 4.0.2 发布：

1. MCP README 不再内嵌大段旧 Cursor 安装提示词，改为链接权威提示词；
2. FCoP 4.0 中英文规范从候选身份更新为正式稳定规范，并机械同步所有
   全文投影、资源测试及冻结 Conformance 身份检查。

本修订书是基础任务书的定点增补。冲突时以本修订书为准；无冲突条款继续
执行基础任务书。

---

## 2. 固定事实

1. `fcop==4.0.1` 与 `fcop-mcp==4.0.1` 已发布。
2. 当前 MCP 能力面为 49 Tools / 12 Resources / 4 Templates。
3. PR #38 已把以下文件确立为 PyPI 长说明权威源：
   - `fcop-README.pypi.md` → `fcop`；
   - `mcp/README.md` → `fcop-mcp`；
   - `docs/pypi/README.md` → 两份说明源和发布核验记录。
4. 当前 `spec/fcop-4.0-spec.md` 与 `.zh.md` 仍保留 Candidate / Not
   Implemented / Not Released 的历史发布身份文字；这是文档身份漂移，
   不是协议业务语义仍处于候选状态。
5. 历史 WP1/WP1.1 报告、Manifest 和冻结摘要真实记录当时的候选阶段，
   必须作为历史证据保留。

---

## 3. 授权范围 A：旧安装提示词测试

允许：

- 修改 `tests/test_fcop/test_install_prompt.py`，将 MCP README 的“正文逐字
  内嵌”合同改为“明确链接权威 EN/ZH 提示词与 MCP Resource”合同；
- 在 `mcp/README.md` 增加：
  - `src/fcop/rules/_data/agent-install-prompt.en.md`；
  - `src/fcop/rules/_data/agent-install-prompt.zh.md`；
  - `fcop://prompt/install`。

必须保留：

- `get_install_prompt()` 与两份权威提示词文件逐字一致；
- EN/ZH 保留既有 `mcpServers` 的安全条款；
- 首次启动等待时间安全条款；
- 禁止自动初始化安全条款。

禁止：

- 把旧安装提示词正文重新内嵌到 PyPI 首页；
- 修改两份 canonical prompt 的正文；
- 删除或弱化安全测试。

---

## 4. 授权范围 B：FCoP 4.0 正式规范身份

允许修改当前权威规范：

- `spec/fcop-4.0-spec.md`；
- `spec/fcop-4.0-spec.zh.md`。

仅允许修改：

- 标题中的 Candidate / 候选；
- 状态栏中的 Not Implemented / Not Released；
- 前言和自指条款中仅用于说明冻结、实现、发布阶段的历史时态；
- 中英文必须同步表达 FCoP 4.0 Stable / Implemented / Released。

允许机械同步因上述字节变化而必须更新的：

- Core 或包内规范全文引用、投影、索引和 SHA-256；
- MCP Spec Resource 投影及其来源摘要；
- Resource 测试；
- 冻结 Conformance 身份、全文一致性和摘要检查；
- 本轮报告、Manifest 与远端哈希记录。

测试必须继续严格证明：

```text
current spec bytes
== packaged/core projection bytes
== MCP resource source bytes

recorded SHA-256
== SHA-256(current spec bytes)

English clause set
== Chinese clause set
```

不得用删除检查、跳过、模糊匹配或降低断言强度解决摘要变化。

---

## 5. 历史证据边界

以下内容不得回写为“当时已经正式发布”：

- WP1 / WP1.1 / WP2 历史报告；
- 旧 review 目录和旧 Manifest；
- `4.0.0-candidate.2` 冻结输入记录；
- 过去 Gate、候选提交和验收回执。

当前权威规范表达现在的 Stable 身份；历史报告表达当时的 Candidate 身份。
两者用途不同，不构成冲突。

如测试需要历史候选摘要，必须从既有历史证据读取或明确标注为 historical，
不得继续把它当作当前规范身份。

---

## 6. 授权范围 C：GitHub 与 PyPI 两份说明同步

PR #40 必须完成并核验：

- `README.md`；
- `README.zh.md`；
- `docs/cli.md`；
- `docs/cli.zh.md`；
- `docs/mcp-tools.md`；
- `fcop-README.pypi.md`；
- `mcp/README.md`；
- `docs/pypi/README.md`；
- `CHANGELOG.md`；
- CLI `--help` 文本。

两份 PyPI 权威说明必须明确：

- FCoP 4.0 是正式稳定版本，不是候选版本；
- `CLI = Setup + Observe + Diagnose`；
- `MCP = Work`；
- 当前为 49 Tools / 12 Resources / 4 Templates；
- `create_branch`、`inspect_family`、`merge_branches` 属于正式 MCP 工具；
- 4.0.2 的安装、CLI Quick Start、MCP 配置与验证方式；
- 安装不会自动初始化、迁移或修改现有 workspace。

不得出现：

- Candidate / review candidate / pending approval；
- 把 4.0.0 或 4.0.1 写成当前安装版本；
- 45/46 Tools 作为当前工具总数；
- 在首页重新堆入大段 0.x/3.x 历史迁移说明。

---

## 7. 协议与产品边界

本修订不授权修改：

- F4.0.1–F4.13.2 的协议条款编号、规范强度和业务语义；
- TASK / REPORT / ISSUE / REVIEW schema 语义；
- 生命周期 T1–T7；
- Authorization、Branch、Convergence、幂等或恢复行为；
- MCP 工具名称、参数、返回合同或业务行为；
- CodeFlowMu；
- Host-specific 产品逻辑。

规范身份文字改变导致的精确摘要更新不属于协议语义修改。

---

## 8. 版本与发布

本轮发布固定为：

```text
fcop      4.0.2
fcop-mcp  4.0.2
tag       v4.0.2
```

两包都必须发布：

- `fcop 4.0.2` 包含 CLI Adapter v1、Core 只读观察能力及更新后的
  `fcop-README.pypi.md`；
- `fcop-mcp 4.0.2` 包含 49 项 Tool Catalog 单一事实源、公开 Catalog API
  及更新后的 `mcp/README.md`。

不得先从未合并分支发布。顺序固定为：

```text
GitHub 当前文档与代码整改
→ 最终 HEAD 全量验证
→ PR #40 合并 main
→ v4.0.2 tag 精确绑定合并后的发布提交
→ 从该 tag 构建并核验四个制品
→ 发布 fcop 4.0.2 与 fcop-mcp 4.0.2
→ 创建/核对 GitHub Release
→ 从 PyPI 无缓存回装
→ 核对两个公开 PyPI 页面
```

公开页面必须逐一核对：

- `https://pypi.org/project/fcop/4.0.2/` 与 `fcop-README.pypi.md`；
- `https://pypi.org/project/fcop-mcp/4.0.2/` 与 `mcp/README.md`。

---

## 9. 验收

发布前必须全部通过：

1. 本修订书的定点测试；
2. 基础任务书 C01–C20；
3. 最终 HEAD 全量回归；
4. Windows / Ubuntu 适用 CI；
5. MCP 49 项真实 stdio 一致性；
6. Core-without-MCP 安装；
7. 四制品构建与 Twine；
8. 两份构建 Metadata 长说明与 GitHub 权威源逐字一致；
9. 远端文件哈希与 Manifest 一致。

任一失败：

```text
STATUS: BLOCKED
REQUESTED_ADMIN_GATE: NONE
MERGE: FORBIDDEN
PUBLISH: FORBIDDEN
```

全部通过后，无需再次请求 ADMIN Gate，直接按第 8 节完成合并、Tag、
GitHub Release、PyPI 两包发布、公开回装与页面核验。

---

## 10. 最终回执追加字段

```text
SPEC_EN_STATUS:
SPEC_ZH_STATUS:
SPEC_EN_ZH_CLAUSE_PARITY:
PACKAGED_SPEC_EQUALS_SOURCE:
MCP_SPEC_RESOURCE_EQUALS_SOURCE:
CONFORMANCE_ASSERTION_STRENGTH_UNCHANGED:
HISTORICAL_CANDIDATE_EVIDENCE_PRESERVED:

PYPI_FCOP_DESCRIPTION_MATCH:
PYPI_FCOP_MCP_DESCRIPTION_MATCH:
PYPI_FCOP_URL:
PYPI_FCOP_MCP_URL:

MAIN_MERGED:
TAG:
TAG_COMMIT:
GITHUB_RELEASE:
CLI_V1_RELEASE_COMPLETED:
```

执行完成后停止，不进入 CodeFlowMu 或其他 FCoP 工作包。
