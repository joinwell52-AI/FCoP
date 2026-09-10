---
protocol: fcop
version: '4.0'
sender: ADMIN
recipient: ME
subject: WP4E Phase A RC integration and release readiness
status: authorized
scope: WP4E_PHASE_A_ONLY
---

# FCoP 4.0 WP4E · RC 集成、公共文档与发布准备

下面这份任务已把 README、MCP 4.0 能力说明和制品重新锁定纳入 WP4E。由于 README 可能进入 sdist，允许因此产生新制品哈希，但必须证明 Core、MCP 生产语义、规范和 Conformance 均未改变。

执行 FCoP 4.0 **WP4E：RC 集成、公共文档与发布准备**。

本消息是 ADMIN 对 WP4E Phase A 的正式授权。仅操作：

```text
joinwell52-AI/FCoP
```

目标是把已经通过 WP4D 的 `4.0.0rc1` 候选整理成可以进入 `main` 并公开发布的最终候选，但本阶段不得实际合并或发布。

## 1. 固定起点

```text
WP4D_GATE: FCOP_4_RC_ACCEPTED
WP4D_ACCEPTED_HEAD: 64a24295d6c1fa53a182a819d39b295c2b1ba8d2d0
WP4D_CANDIDATE_CONTENT: d1a86f32d87f000fe0aec444563decdc892dc142
WP4D_MANIFEST_SHA256: 21728890f757189cbc47e3ac131efcfb37d5ea0935de2b7467575de95f95314d
TARGET_VERSION:
  fcop: 4.0.0rc1
  fcop-mcp: 4.0.0rc1
```

ADMIN Gate：

[https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5610960987](https://github.com/joinwell52-AI/FCoP/pull/31#issuecomment-5610960987)

WP4D Manifest：

[https://github.com/joinwell52-AI/FCoP/blob/64a24295d6c1fa53a182a819d39b295c2ba8d2d0/reviews/fcop-4.0/wp4d/MANIFEST.md](https://github.com/joinwell52-AI/FCoP/blob/64a24295d6c1fa53a182a819d39b295c2ba8d2d0/reviews/fcop-4.0/wp4d/MANIFEST.md)

WP4D 基线制品 SHA-256：

```text
fcop-4.0.0rc1-py3-none-any.whl
b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9

fcop-4.0.0rc1.tar.gz
43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4

fcop_mcp-4.0.0rc1-py3-none-any.whl
20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a

fcop_mcp-4.0.0rc1.tar.gz
eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b
```

这些哈希是 WP4D 基线，不自动等于 WP4E 最终发布哈希。

## 2. 任务书与分支

1. 从 `64a24295d6c1fa53a182a819d39b295c2ba8d2d0` 创建 WP4E 工作分支。
2. 创建并提交：

```text
taskbooks/fcop-4.0/WP4E/01-RC-Integration-Public-Docs-and-Release-Readiness-Taskbook-v1.0.zh.md
```

3. 记录任务书提交、字节数和 SHA-256。
4. 本消息已授权任务书编制及 Phase A 执行；完成任务书固定后直接继续，不需要再次等待授权。
5. 创建一份以 `main` 为目标的独立 Draft PR。
6. 保留 WP0–WP4D 的祖先关系，不 squash、不重写历史、不 force-push。

## 3. 根 README 和公共入口收口

必须更新并核验：

```text
README.md
README.zh.md
docs/mcp-tools.md
docs/index.html
```

如这些页面直接引用其他安装、升级、规范或快速上手文档，应同步修正相应入口。

README 中必须明确区分：

```text
Latest stable: 3.2.5
Release candidate: 4.0.0rc1
```

不得在公开发布前把 `4.0.0rc1` 写成 stable。

README 必须清楚说明：

1. FCoP 4.0 是协议级 Major 升级。
2. Core 与 MCP Adapter 已分层。
3. 4.0 Core 增加 Workspace 身份、四类信封、Branch、显式收敛、授权绑定、持久幂等、并发线性化、崩溃恢复和版本化规则分发。
4. MCP 公开面为：

```text
46 tools / 12 resources / 4 resource templates
```

5. 正确表述不是“4.0 只新增一个能力”，而是：

```text
原有45个MCP工具获得4.0版本路由及新协议语义；
新增T6 reopen_task；
工具名称总数为46。
```

6. `reopen_task` 是生命周期 T6，不是 Branch 专用工具。
7. Branch 通过以下通用 MCP 能力形成闭环：

```text
create_task(branch_of=...)
inspect_task(include_family_digest=true)
write_report(attempt_id=...)
write_review(
  review_kind="convergence",
  family_digest=...,
  references=...
)
archive_task(
  review_ref=...,
  family_digest=...
)
```

8. 并发不是独立工具，而是相关写工具共同遵守的执行语义，包括：

   * 原子写入；
   * 线性化；
   * `operation_id` 持久幂等；
   * 相同请求精确重试；
   * 冲突拒绝；
   * 零副作用失败；
   * 崩溃恢复；
   * family digest 一致性。
9. 给普通开发者提供最小 Python 和 MCP 使用入口。
10. 英文与中文的版本、数字、链接、安装命令、参数和能力说明完全一致。

## 4. MCP 4.0 能力审计

建立一份完整的 MCP 能力映射，不只统计工具名称。

至少覆盖：

| 能力               | 必须验证的 MCP 入口                                                                         |
| ---------------- | ------------------------------------------------------------------------------------ |
| 4.0 Workspace 创建 | `init_solo`、`init_project`                                                           |
| 普通 TASK 创建       | `create_task`                                                                        |
| Branch 创建        | `create_task(branch_of)`                                                             |
| 持久幂等             | `create_task(operation_id)`                                                          |
| 生命周期 T2–T7       | `claim_task`、`submit_task`、`approve_task`、`reject_task`、`reopen_task`、`archive_task` |
| REPORT head      | `write_report`、读取与检查入口                                                               |
| Authorization    | `write_review`、`mark_human_approved`                                                 |
| Family 查询        | `inspect_task(include_family_digest)`                                                |
| Convergence      | `write_review(review_kind=convergence)`                                              |
| Root 归档          | `archive_task(family_digest, review_ref)`                                            |
| 规则发现与分发          | 版本化 resources/templates 及既定部署入口                                                      |
| 冲突与恢复            | 结构化错误码、精确重试和零副作用                                                                     |

必须使用独立 MCP-only 客户端完成至少以下真实场景：

* 普通顺序 TASK；
* Root 加两个 Branch；
* 两个 Branch 分别完成；
* family digest 计算；
* convergence REVIEW；
* Root T7 归档；
* 相同 `operation_id` 精确重试；
* 不同内容复用 `operation_id` 冲突；
* 并发写竞争；
* 进程关闭后重新打开；
* 错误路径零副作用。

客户端不得直接 import `fcop` 或 `fcop_mcp`，只能通过 MCP stdio JSON-RPC 使用公开工具。

## 5. 发布工作流加固

审计并修改 `.github/workflows/release.yml`：

* 精确区分 RC 与 stable；
* `4.0.0rc1` 必须创建为 GitHub Pre-release；
* 校验版本、tag、候选提交、ADMIN Gate 和四个最终制品 SHA-256；
* 使用受保护发布 environment；
* 权限最小化；
* 未获得发布 Gate 时不得上传；
* 构建工具和可复现参数固定；
* 发布时使用经过最终验收的同一组制品；
* 不得在上传阶段重新构建另一组未知字节；
* 发布后必须从公开 PyPI 全新回装并核验；
* 发布事件、提交、Gate、制品和结果必须可追踪。

在不使用真实发布凭据、不创建 tag、不上传 PyPI、不创建 GitHub Release 的条件下完成 dry-run。

## 6. WP4E 最终制品

完成 README、公共文档和发布工作流修改后，重新构建四个最终 RC 制品。

如果授权修改进入 wheel 或 sdist，导致 WP4D 基线哈希变化：

* 不得把它误报成 WP4D 原制品；
* 记录每个变化的归因；
* 证明变化只来自本任务授权的 README、文档、发布元数据或工作流收口；
* Core、MCP 生产逻辑、冻结规范、Schema 语义和 Conformance 不得变化；
* 两次全新构建必须 `4/4` 逐字节一致；
* WP4E Manifest 必须锁定新的四个最终 SHA-256；
* 后续发布只能使用 WP4E Gate 接受的新制品。

不得为了维持旧哈希而放弃 README 更新，也不得在未记录的情况下接受新哈希。

## 7. 回归与验收

最终 WP4E HEAD 至少必须满足：

* Windows 全量回归全部通过；
* Ubuntu 全量回归全部通过；
* 所有适用 CI 通过；
* 两个 PR-only 检查实际运行并通过；
* WP4E 新增测试全部通过；
* MCP 工具、资源、模板精确为 `46/12/4`；
* 两个包版本均为 `4.0.0rc1`；
* 双包依赖关系准确；
* 12 个 consumer 全部通过；
* wheel/sdist 24 个安装来源全部通过；
* 四制品可复现 `4/4`；
* 权威文件 `19/19`；
* 冻结文件 `21/21`；
* 根 README 中英文一致；
* 链接、安装命令和示例可执行；
* 远端所有交付文件逐一 SHA-256 回读一致。

## 8. 连续修正授权

以下问题属于 WP4E 范围，可直接修正、提交、重跑并继续：

* README、公共文档、链接和示例；
* 测试前置条件及旧验证断言；
* Windows/Linux 路径、编码、换行和 socket 守卫；
* 构建、Twine、packaging、wheel 和 Actions 工具版本；
* 测试夹具和验证脚本；
* RC/release workflow；
* 发布 dry-run；
* 报告、证据和 Manifest；
* 不改变协议及生产行为的发布元数据。

必须保留失败历史、修正原因、前后结果和提交记录。不得删除测试、弱化断言、增加非必要 skip，或把未运行项写成通过。

只有以下情况才停止：

* 必须修改冻结的 4.0 规范、Conformance 合同或协议语义；
* 必须改变 Core 或 MCP 生产行为；
* 候选版本或双包依赖不唯一；
* 最终制品不可复现；
* 即将执行不可逆动作：合并 main、创建或推送 tag、上传 PyPI、创建 GitHub Release、更新 MCP Registry 或 Zenodo。

## 9. 必交报告

```text
reports/FCOP-4.0-WP4E-INTEGRATION-AND-HISTORY.md
reports/FCOP-4.0-WP4E-README-AND-PUBLIC-SURFACE.md
reports/FCOP-4.0-WP4E-MCP-CAPABILITY-MAPPING.md
reports/FCOP-4.0-WP4E-RELEASE-WORKFLOW-HARDENING.md
reports/FCOP-4.0-WP4E-ARTIFACT-AND-DRY-RUN.md
reports/FCOP-4.0-WP4E-CI-AND-RELEASE-READINESS.md
reports/FCOP-4.0-WP4E-RESULT.md
reviews/fcop-4.0/wp4e/MANIFEST.md
```

报告必须记录命令、平台、起止时间、退出码、测试数、失败数、skip 数、Actions URL、提交、制品哈希和远端回读结果。

## 10. Phase A 停止点

完成全部可逆工作后停止，不得自行合并或发布，并请求：

```text
WP4E_PHASE_A_STATUS: COMPLETE
REQUESTED_GATE: FCOP_4_RC_RELEASE_READY
MAIN_MERGE_AUTHORIZED: FALSE
TAG_AUTHORIZED: FALSE
PYPI_PUBLISH_AUTHORIZED: FALSE
GITHUB_RELEASE_AUTHORIZED: FALSE
MCP_REGISTRY_UPDATE_AUTHORIZED: FALSE
ZENODO_UPDATE_AUTHORIZED: FALSE
STABLE_RELEASE_AUTHORIZED: FALSE
NEXT_STAGE_AUTHORIZED: FALSE
```

最终回执必须提供：

* 固定 WP4E HEAD；
* 面向 main 的 Draft PR；
* 任务书提交、字节数和 SHA-256；
* WP4E 最终四制品 SHA-256；
* README 中英文收口结果；
* MCP Branch、并发和收敛能力证明；
* Windows、Ubuntu 全量测试；
* 全部 CI 与 PR-only 检查；
* 发布 dry-run；
* 远端交付哈希；
* Phase B 拟执行的不可逆动作。

取得 ADMIN `FCOP_4_RC_RELEASE_READY` 后，才允许恢复 Phase B。

## 执行记录补充：已核实的基线勘误与隔离边界

原始授权第 1 节的 `64a24295d6c1fa53a182a819d39b295c2b1ba8d2d0` 为 41 字符误写。执行采用同一授权第 2 节、Manifest URL 以及 GitHub OWNER 的 ADMIN Gate 回执一致指定的 `64a24295d6c1fa53a182a819d39b295c2ba8d2d0`。2026-09-10 通过 GitHub API 回读回执及 Manifest 原始字节：34249 bytes，SHA-256 为 `21728890f757189cbc47e3ac131efcfb37d5ea0935de2b7467575de95f95314d`。

执行工作树：`D:/FCoP-wp4e-release-readiness`。分支：`codex/fcop-4.0-wp4e-release-readiness`。Draft PR 的 base 为 `main`；不得合并。旧工作树、dogfood 和未提交文件均保留。CodeFlowMu 不在本轮读写或协调范围内，不做现场快照，不请求停写窗口。

本任务书是 ADMIN 原始任务的落盘及执行细化，不构成新的 Gate。ME 自审仅核验执行范围，不代替 ADMIN 验收。执行前回读本文件；完成后七份报告及 Manifest 承接本任务书提交，历史任务书保留而不删除。

公开文档、验证脚本/测试、第三方样例与 RC/release workflow 可修改；`src/**`、`mcp/src/**`、`spec/**`、冻结 `tests/conformance/**` 的 Git blob 必须保持。已有历史审计固定其历史区间，不扩大历史白名单。受保护发布 environment 的配置须只读核验；缺失保护则发布流程 fail closed，不在 Phase A 改远端权限。发布 Gate 与 RC 接受 Gate 不可互换。

交付先固定任务书，再提交内容和必要修正，最后单独提交 Manifest。所有最终 CI 均绑定最后 HEAD；后补远端验证回执不得冒充写 Manifest 时尚未完成的验证。可复现性比较的是去掉纯证据提交后的同一内容提交，两次新构建；不使用 WP4D 旧内容作为 WP4E 制品来源。

