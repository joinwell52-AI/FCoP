---
protocol: fcop
version: "3.0"
sender: ADMIN
recipient: ME
subject: WP4F Stable 发布与实际 user-fcop MCP 升级
---

# WP4F — FCoP 4.0.0 Stable 发布与 MCP 工具升级

权威来源：ADMIN 在当前会话直接下发的 WP4F 任务；不设观察期，不增加功能。

## 固定基线与目标

- Repository: joinwell52-AI/FCoP
- 最新 origin/main / 分支起点：5208d8a2b37c969b0b2067c01107966bf705293c
- RC tag: v4.0.0rc1；RC HEAD: d5e851c3fa628167999a9f8b7b7b89290e7b8f06
- Stable: fcop==4.0.0 / fcop-mcp==4.0.0；tag: v4.0.0。
- 独立工作树：D:/FCoP-wp4f-stable；分支：codex/fcop-4.0-wp4f-stable。
- 原 D:/FCoP 的修改、未跟踪资料、dogfood 及旧工作树原样保留。

## Phase A 授权

仅修改 Core/MCP 版本与打包元数据、匹配依赖 fcop>=4.0.0,<4.1.0、CHANGELOG、双语 README 与发布说明、Stable 构建/发布/回装脚本和对应测试、报告、任务书、Manifest。
版本兼容登记只增加精确 Stable 配对，不改版本检查算法、路由或工具业务行为；RC/legacy 历史配对保留。

验证四个 Stable wheel/sdist 的两次独立可复现构建、Twine、Windows/Ubuntu 全量回归、Python 3.10–3.13 三平台安装矩阵、Core/MCP wheel/sdist 外部消费者、真实 stdio MCP 46 Tools / 12 Resources / 4 Templates、reopen_task、Root+双 Branch、显式收敛、跨进程并发、幂等重试/冲突、重启恢复、Stable dry-run、PyPI 描述与依赖的制品元数据预检。

Phase A 尚未发布，不能谎称 PyPI 已显示 Stable；实际项目主页及公开安装在 Phase B 验证。完整报告和 Manifest 固定候选字节及最终 CI HEAD 后，只请求一次 FCOP_4_STABLE_RELEASE_READY。

## Phase B：Gate 后执行

保留完整历史合并 main；固定 v4.0.0；上传已验收的四个制品到两个 PyPI 项目；创建正式 GitHub Release；确认两项目最新 Stable 为 4.0.0；公开下载四制品核对 SHA-256；全新环境安装并执行真实 MCP 验证。

之后才升级实际 user-fcop 的 Python 环境为两个 4.0.0 包。保持 MCP 名称、传输及配置不变，重启准确的服务并核验 46/12/4、Branch、收敛、并发和恢复。测试仅用新临时工作区，不迁移现有工作区。完成最终回执即停止。RC 制品和 tag 保留。

## 禁止与停止条件

不得修改协议语义、Core/MCP 业务行为、Schema、冻结 Conformance、工具合同、CodeFlowMu、MCP Registry、Zenodo，或增加新功能。发布范围内小问题可直接修正并完整回归；需要改变语义/业务行为或缺少发布凭据时停止报告。

Phase A 不发布、不合并 main、不创建 Stable tag、不升级或重启本机服务。Phase B 使用同账号 ADMIN 人工批准，不要求独立 GitHub 账号，不代替 ADMIN 点击审批。

## 执行检查与回退

ME 执行前复读本任务：阶段授权清晰；四制品必须同源固定；版本数字不改变协议；历史测试不是当前版本的永久上限。规则包、Schema、Conformance、工具 snapshot 逐文件/树保持，业务代码仅版本声明常量可变，其余 AST 保持。
候选阶段失败只保留证据，不影响现有服务；发布后不得删除或重用版本号。实际本机升级前记录准确解释器、包版本、配置摘要、服务入口，保留原版本可回装路径；不可擅自终止其他进程或修改配置。
当前工具集合未提供 fcop_report，因此不调用未知工具、不初始化或部署原工作区。此任务书及后续报告承担本轮文件化执行链，验收由 ADMIN 完成。
