---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: dev-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-05-12
---

# dev-team 运行规则

本文定义 `dev-team` 的工作方式,用来回答"什么时候派、怎么回、什么时候升级"。

## 1. 基本路由

1. `ADMIN ↔ PM` 是唯一对外接口。
2. `DEV / QA / OPS` 只从 `PM` 接任务、只向 `PM` 回执。
3. 不允许 `DEV ↔ QA`、`DEV ↔ OPS`、`QA ↔ OPS` 横向私自派单。
4. 横向协作需求必须先回给 `PM`,由 `PM` 决定是否拆新任务。

## 2. 任务派发规则

### PM 直接做

以下事项默认由 `PM` 直接处理,不必拆发:

- 需求澄清
- 优先级排序
- 任务拆解
- 进展汇总
- 对 `ADMIN` 的阶段回执
- 共享文档维护

### PM 派给 DEV

出现以下事项时派给 `DEV`:

- 功能开发
- Bug 修复
- 代码重构
- 技术验证或原型实现

### PM 派给 QA

出现以下事项时派给 `QA`:

- 功能验证
- 回归验证
- 验收检查
- 缺陷复测

### PM 派给 OPS

出现以下事项时派给 `OPS`:

- 环境准备
- 部署发布
- 服务重启
- 配置变更
- 运行状态检查
- 回滚执行

## 3. 回执规则

1. 每条任务都必须有对应回执。
2. 回执必须说明:状态、已完成内容、阻塞项、下一步建议。
3. `DEV / QA / OPS` 的正式回执目标都是 `PM`。
4. `PM` 汇总后,统一向 `ADMIN` 输出阶段结论或最终结果。
5. 口头同步不算回执,必须落成文件。

## 4. issue 处理规则

1. 发现问题时,应先落 `ISSUE-*` 或在回执中明确写出阻塞。
2. 涉及跨角色影响的问题,由 `PM` 统一协调。
3. 缺陷是否进入返工、是否调整优先级,由 `PM` 决定。
4. 质量问题由 `QA` 提出,技术修复由 `DEV` 执行,环境问题由 `OPS` 执行。

## 5. 线程与节奏

1. 同一 `thread_key` 同一时刻只能有一个活跃 driver,默认是 `PM`。
2. `PM` 未明确交接前,其他角色只处理自己收到的子任务,不独立驱动整条线程。
3. 子任务完成后及时回给 `PM`,不积压、不沉默。
4. `PM` 负责判断线程是否闭环、是否继续拆单、是否归档。

## 6. 升级给 ADMIN 的条件

出现以下情况时,`PM` 必须升级给 `ADMIN`:

- 需求范围明显变化
- 优先级冲突需要裁决
- 高危操作需要二次确认
- 外部依赖阻塞导致计划无法继续
- 发布风险超出原预期
- 需要资源取舍或时间取舍

## 7. 高危动作规则

以下动作执行前必须有明确记录并等待确认:

- 重启生产服务
- 修改网络、防火墙、网关、Nginx、CI/CD
- 删除数据、日志或缓存
- 发布到主干或公网制品仓库

没有回滚方案,不得执行。

## 8. 文档与归档

1. 流程文件放在 `tasks/`、`reports/`、`issues/`。
2. 共享知识放在 `shared/`。
3. 完成闭环后由 `PM` 负责归档。
4. `shared/` 文档允许原地更新;任务和报告遵循追加历史原则。

## 9. 执行口径

`dev-team` 的目标不是让每个角色都很忙,而是让每个角色都在清晰边界内工作:

- `PM` 负责调度和统一出口
- `DEV` 负责实现
- `QA` 负责验证
- `OPS` 负责环境和发布

边界清楚,线程才稳定;线程稳定,团队才可接力。

---

## 协议演进补记（v1.0 ~ v1.4）

本节补记协议演进带来的运行规则变化：

### 高风险任务审批（v1.0 引入）

- `PM`（leader）派单时标注 `risk_level: high`，系统自动生成 `REVIEW-*.md`
- 带 `needs_human: true` 的任务：执行角色**停手**，等 ADMIN 调 `mark_human_approved()`
- 未批准不得执行 → 此约束优先级高于任何"进度压力"

### fcop_audit 整改任务处理（v1.3 引入）

- ADMIN 或 leader 运行 `fcop_audit()` 后，`INSPECTION-*.md` 报告会记录协议缺口
- 对应整改任务（`TASK-*-ADMIN-to-PM.md`）可批量授权（`scope: batch-remediation`）
- 处理整改任务时同样走"四步流程"，并在回执中引用 INSPECTION ID

### 发布绑定规则（v1.4 引入）

- MCP Server 层：write-side 工具必须显式绑定项目路径
- 配置方式：在 MCP config 中设置 `FCOP_PROJECT_DIR`，或会话开始时调 `set_project_dir()`
- 未绑定时调用任何写入工具，将抛出 `WriteRefused` 错误


---

## §internal-only 声明语法（v3.0+，per Rule 4.6）

> 自 fcop@2.0.0 / `fcop_rules_version: 3.0.0` 起，团队若需要"内部档案
> 桶"，可由 ADMIN 调 `Project.init(deploy_internal_template=True)`
> 部署 `fcop/internal/` 子层（Rule 4.6 non-mandatory soft convention）。

- 任何 `fcop/internal/` 下 `.md` 文件**应当**在 frontmatter 之后立即
  携带双语声明块：

```markdown
---
protocol: fcop
version: 1
kind: internal-archive
sender: PM
recipient: PM
internal_only: true
---

> ⚠️ **INTERNAL ONLY · 内部档案 · DO NOT EXTERNALIZE WITHOUT REVIEW**
>
> （本文件用途说明）

# 正文标题
...
```

- 完整模板与背景见 `fcop/internal/README.md`（部署后自动落盘）、
  `fcop-rules.mdc` Rule 4.6、`fcop-protocol.mdc` §How Rule 4.6 Applies。
- `fcop_audit()` 对本桶只做 P3 (suggestion) 提示，不阻塞任何写入。
