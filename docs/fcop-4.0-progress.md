# FCoP 4.0 development notes / 开发记录（草稿）

[README](../README.md) · [中文 README](../README.zh.md)

**FCoP 4.0 is unfinished.** This page is a design and candidate-review snapshot. Contract descriptions and document coverage do not establish completed functionality, engineering acceptance or release readiness.

**FCoP 4.0 尚未完成。** 本页保存设计与候选审查记录；契约描述、文档覆盖度或 README 分支的检查通过，都不能作为 4.0 功能完成、工程验收或发布就绪的证明。

Checked 2026-09-09. This page separates the public installation path from the ongoing 4.0 work. The pinned sources below describe a review candidate; they are not a release announcement.

## Public version

**Use the published `fcop==3.2.5` and `fcop-mcp==3.2.5` packages for the README examples.** See [GitHub Releases](https://github.com/joinwell52-AI/FCoP/releases), [PyPI library](https://pypi.org/project/fcop/3.2.5/) and [PyPI MCP server](https://pypi.org/project/fcop-mcp/3.2.5/).

The 4.0 work includes a `4.0.0rc1` candidate identity. It has not been published as an installable public release. The [candidate boundary](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/docs/fcop-4.0/rc-candidate-boundary.md) explicitly distinguishes candidate verification from release readiness and publication.

## Work persists outside model context

FCoP externalizes formal work into durable, attributable and inspectable records. TASK, REPORT, ISSUE and REVIEW retain assignments, deliveries, problems and review decisions across session boundaries. References and lifecycle history let another person, agent or tool examine the same work. A REPORT records a delivery claim; accepting that delivery requires a separate decision and evidence.

The filesystem is the current reference carrier. The Core contract defines what compatible implementations must preserve; this does not imply that alternative storage adapters have been implemented or certified. Continuing agent execution requires a Runtime.

## Core, Specification, Toolkit, Profile and Runtime

| Layer | Responsibility |
|---|---|
| Core | Eight invariants shared by conforming implementations: workspace identity; four envelopes; lifecycle; four relations; evidence/convergence; durable authorization; create idempotency; recoverable atomic semantics. |
| Specification | The authoritative definition of those fields, states, errors and observable behaviors. |
| Toolkit | Validation, query, migration, recovery and convenience APIs; `fcop` is the reference Toolkit. |
| Profile | Roles, issuer authority, organizational rules and product policy. |
| Runtime | Host, model/tool calls, sessions, scheduling, UI, networking and process management. |

**Conformance is the verification layer:** test vectors, fixtures and observable outcomes check whether an implementation follows the Specification. The Python implementation and MCP tool names do not define Core compatibility by themselves.

Fixed PM/DEV/QA roles are not Core requirements. A Branch is an ordinary TASK related through `branch_of`; Git branch/merge and automatic agent scheduling remain outside Core. In 4.0, `active → done` is removed, authorized `done → active` creates a new attempt, and `archive` is terminal.

## Parallel work and integration boundaries

Independent TASK and Branch workflows can progress concurrently, with ordered transitions inside each workflow. Related changes use a short family commit boundary; it does not lock the duration of agent execution or unrelated tasks. Root archival then checks the current completed Branch evidence, its convergence record and separate archive authorization. This is work-evidence convergence, not automatic Git merging.

MCP is an optional way for an agent to access FCoP operations. Model calls, sessions, scheduling and execution recovery belong to the host Runtime. Cross-system networking belongs to an integration outside Core; an architectural mapping to A2A is not a claim that this release provides an A2A adapter. CodeFlowMu is a separate product Runtime; use the [CodeflowMu-Distribution release notes](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases) to check actual product capabilities and version support.

## Contract history: WP1 to WP1.1

The original [WP1 contract package](https://github.com/joinwell52-AI/FCoP/blob/1b50f9e1fd4d2d21002bb1b98e14fd903a050f07/reports/FCOP-4.0-WP1-RESULT.md) contains six documents: English/Chinese specification, 30 conflict decisions, a future conformance matrix, compatibility/MCP mapping and the result report. Its contract identity is `4.0.0-candidate.1`. Its reported `COMPLETE` means the contract package was delivered; its test matrix describes expected checks and is not a test execution result.

The later specification pinned on this page is `4.0.0-candidate.2`. It clarifies that Profile array order conveys no priority; issuer evaluation is `AUTHORIZED / DENIED / UNKNOWN`; evidence and authorization are bound to file-byte digests; Root convergence and Root archive authorization are distinct; and create idempotency, internal crash recovery and authorized lost-response retry have different scopes. Do not copy WP1-only wording over those revisions.

## What the upgrade covers

| Area | Contract being developed | Source |
|---|---|---|
| Workspace and evidence identity | Stable workspace IDs, four formal envelopes, explicit relations and evidence references | [Core specification, C1–C5](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/spec/fcop-4.0-spec.md) |
| Durable authorization | Persisted authorization tied to evidence digests and an explicitly adopted Profile | [Core specification, C6](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/spec/fcop-4.0-spec.md) |
| Retry and recovery | Operation identity, conflicting retry rejection and observable recovery states | [Core specification, C7–C8](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/spec/fcop-4.0-spec.md) |
| Task families | Branch relationships, evidence coverage and explicit Root convergence; Branch is a task relationship | [Core specification, C4–C5](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/spec/fcop-4.0-spec.md) |
| Rule delivery | Versioned bilingual modules, selection, explicit adoption, deployment planning and rollback | [Rule distribution contract](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/docs/fcop-4.0/rule-distribution-contract.md) |
| Python and MCP consumption | Machine-readable contracts and examples that consume candidate artifacts outside the source checkout | [Python example](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/examples/v4/third-party/python-only/README.md) · [MCP example](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/examples/v4/third-party/mcp-only/README.md) |

These are descriptions of the upgrade's scope. Check the [candidate PR #31](https://github.com/joinwell52-AI/FCoP/pull/31), its [Manifest](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/reviews/fcop-4.0/wp4d/MANIFEST.md) and [verification report](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/reports/FCOP-4.0-WP4D-RESULT.md) for the completed checks, limitations and subsequent review.

A source demo or passing CI job alone does not establish a published release, production credential verification or adoption by an agent host. Existing 3.x workspaces retain 3.x semantics until explicit migration. Current citation identifiers and downstream product versions are not changed by this README.

## 中文说明

**现在可安装的是公开的 3.2.5；4.0 属于正在验证的升级候选。** 候选版本号为 `4.0.0rc1`，不能据此宣称它已经发布到 PyPI，或要求新用户直接从公开包目录安装该候选。

WP1 契约包共六份文件，版本为 `4.0.0-candidate.1`；它的 COMPLETE 指候选材料完成。上方审查来源中的后续规范为 `candidate.2`，已补充 Profile 权限、证据字节摘要、完整迁移条件、汇合与归档授权的区别，以及三类不同的幂等/恢复保证。

Core 的八项契约是：工作区身份、四类信封、生命周期、四种关系、证据与汇合、持久授权、创建幂等、可恢复原子语义。固定角色属于 Profile，Python 实现属于 Toolkit，MCP 属于适配器，模型调用与调度属于 Runtime。

这些契约服务于同一个目的：让 Agent 的正式工作站到模型上下文之外。任务、交付、问题和审查保留为可持续检查与交接的工作记录。文件系统是当前参考载体；工作记录可以保留，Agent 持续执行则需要 Runtime。Specification 规定公开行为，Conformance 用测试向量、样例与可观察结果验证实现是否符合规范。

并行方式是多条有序工作流共同推进：每个 TASK 或 Branch 保持自己的生命周期，相关状态变更只在短暂提交期间协调。任务分支集合收尾要核对当前证据、汇合记录和独立归档授权；这不等于自动合并 Git 代码。MCP 接入、宿主持续执行与跨系统联网各有边界，架构中的 A2A 映射也不能直接当作已交付的适配器。

这次升级重点是：

1. 明确工作区身份、文件之间的关系，以及交付和审查对应的证据。
2. 将授权与具体证据、已采纳的 Profile 绑定并持久保存。
3. 为重试保留操作身份，拒绝冲突，区分可观察的恢复状态。
4. 明确任务分支的关系、完成证据与汇合条件。
5. 按版本分发中英文规则，通过显式采纳、部署计划和回滚处理宿主文件。
6. 验证 Python 与 MCP 使用方如何消费候选安装包。

对应[中文 Core 规范](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/spec/fcop-4.0-spec.zh.md)与[中文规则分发契约](https://github.com/joinwell52-AI/FCoP/blob/700e9e1ecb3eb02e5860094175ba7f8099141695/docs/fcop-4.0/rule-distribution-contract.zh.md)。上表说明的是升级范围；实际完成了哪些验证，应查看 PR、Manifest 和报告。新版本发布、既有工作区迁移、产品接入、宿主实际消费规则，各自需要相应证据。

## Updating the landing page after release

Once a public release exists, update the README package versions and commands from the actual published artifacts, rerun the local demo and MCP connection check, link the version-specific migration instructions, and update citation links only if corresponding records exist. Keep the 3.x documentation accessible to existing users.
