# FCoP 4.x rule resources / 规则资源

**Install → connect MCP → initialize workspace → use FCoP.**

FCoP owns the protocol workspace and package-owned rule resources. It does not own project-root Host instruction files. Installing, initializing, upgrading or normally using v4 must not create, overwrite, merge, delete or require `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*` or another Host's instructions.

**安装 → 连接 MCP → 初始化工作区 → 使用 FCoP。** FCoP 仅拥有协议工作区与包内规则资源，不拥有项目根 Host 指令文件。v4 安装、初始化、升级与正常运行不创建、覆盖、合并、删除或依赖这些 Host 文件。

## Read, validate and select / 读取、校验与选择

The installed package carries nine modules in English and Chinese, plus one strict Manifest. All 18 artifacts retain explicit hashes, clause ownership, dependencies and stable load order. `sequential` selects the eight common modules; `parallel` additionally selects `convergence`. `repository-development` remains a separate assembly requiring four explicit pinned repository references, never an implicit business-agent constitution.

包内包含九模块双语共 18 份制品及一个严格 Manifest，保留摘要、条款归属、依赖与稳定顺序。`sequential` 选取八个公共模块，`parallel` 增加 `convergence`；`repository-development` 是独立装配，要求四份显式固定仓库引用，不自动混入普通业务 Agent 指引。

| MCP resource | Result / 内容 |
| --- | --- |
| `fcop://rules` | Validated v4 Manifest / 已校验的 v4 清单 |
| `fcop://protocol` | Fixed Stable specification identity / 固定 Stable 规范身份 |
| `fcop://guidance/sequential/en` | Sequential guidance in English |
| `fcop://guidance/sequential/zh` | 顺序任务中文指引 |
| `fcop://guidance/parallel/en` | Parallel Branch guidance in English |
| `fcop://guidance/parallel/zh` | 并行 Branch 中文指引 |

Resources work without any Host rule files. MCP is a thin adapter over `Project.rule_distribution`; reading guidance is neither authority nor evidence that a Runtime consumed it. Core authorization Profiles are independent of the retired Host projection profiles.

资源无需 Host 规则文件即可工作；MCP 薄适配调用 `Project.rule_distribution`。读取指引不产生权限，也不证明 Runtime 已消费指引。Core 授权 Profile 与已退役的 Host 投影 profile 是不同概念。

## Workspace boundary / 工作区边界

Normal durable v4 business state lives in `<project>/fcop/`. Existing same-volume `.fcop-init-*` initialization staging and failed/losing-initializer evidence remain part of the unchanged atomic Encoding mechanism; they are not Host instructions. Existing customer files and historical deployment receipts are never automatically cleaned up.

v4 正常持久业务状态位于 `<project>/fcop/`。既有同卷 `.fcop-init-*` 初始化暂存及失败/并发落败证据保持不变，属于原子 Encoding 机制，不是 Host 指令。不得自动清理用户已有文件或历史部署回执。

## Retired operations / 退役操作

In v4, `redeploy`, `inspect_profile`, `status` (the rule-distribution Host status action, not CLI workspace status), `adopt`, `plan`, `apply`, `verify_deployment`, `rollback`, `inspect_failure`, `rollback_partial` and projection-only `measure_context` return structured `toolkit:OPERATION_NOT_IMPLEMENTED` with zero writes. No Host target/profile, projection byte limit, backup or deployment receipt is created.

上述 rule-distribution Host 操作在 v4 结构化拒绝且零写入；其中 `status` 指旧 Host 分发状态动作，不是 `fcop status`。规则包 `read_resource`、`validate`、`select`、`validate_operation_scope`、显式包制品导出仍保留；`inspect_layers` 只报告规则包身份，Host 相关事实为空，不检查或信任旧部署回执。

MCP `redeploy_rules` keeps its name and parameters for supported Legacy v1–v3 only. V4 rejects regardless of `force` or `archive`; it is not a v4 install or upgrade step. Retain your own Host files unchanged. Legacy history and prior Host contracts remain auditable in [the historical distribution contract](fcop-4.0/rule-distribution-contract.md), not current v4 installation instructions.

MCP 保持 **49 tools / 12 resources / 4 templates**。`redeploy_rules` 的名称与参数保留，仅支持 Legacy v1–v3；v4 不论 `force`、`archive` 均拒绝。若用户需要清理旧四件套，须由用户单独决定，升级不会代做。

See [CLI](cli.md) / [中文 CLI](cli.zh.md) and [MCP tools](mcp-tools.md).
