---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: qa-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-05-12
---

# qa-team 运行规则

## 1. 基本路由

1. `ADMIN ↔ LEAD-QA` 是唯一对外接口。
2. `TESTER / AUTO-TESTER / PERF-TESTER` 只从 `LEAD-QA` 接任务、只向 `LEAD-QA` 回执。
3. 不允许三条战线横向直接协作——必经 `LEAD-QA`。
4. 跨团队协作(例如与 `dev-team` 的 `PM` 对接缺陷)统一由 `LEAD-QA` 负责。

## 2. 任务派发规则

### LEAD-QA 直接做

- 测试目标澄清、质量门槛定义
- 测试策略、风险矩阵、优先级
- 跨战线任务拆解
- 最终发布/打回建议
- 对 `ADMIN` 的阶段回执

### LEAD-QA 派给 TESTER

- 手工功能测试
- 主流程回归测试
- 边界/异常测试
- 验收测试

### LEAD-QA 派给 AUTO-TESTER

- 自动化脚本编写/维护
- 自动化套件执行与报告
- 回归自动化覆盖扩展

### LEAD-QA 派给 PERF-TESTER

- 压测场景设计
- 负载模型与指标定义
- 压测执行与瓶颈分析

## 3. 并行推进规则

1. 三条战线可以在同一轮测试中并行推进(功能+自动化+性能可以同时跑)。
2. 并行期间,各角色只处理自己的子任务,不互相调度。
3. 每条战线的中间产物必经 `LEAD-QA` 汇总,其他战线才能参考。
4. 例如:功能测试发现的缺陷,不直接要求自动化补用例,而是回 `LEAD-QA` 决定是否派发。

## 4. 回执规则

1. 每条任务都必须有对应回执。
2. 回执必须说明:状态、已跑用例数、通过/失败数、关键缺陷、下一步建议。
3. `TESTER / AUTO-TESTER / PERF-TESTER` 的正式回执目标都是 `LEAD-QA`。
4. `LEAD-QA` 汇总三条战线后,统一向 `ADMIN` 输出发布建议与风险评估。
5. 口头同步不算回执,必须落成文件。

## 5. 缺陷处理规则

1. 发现缺陷时,在 `issues/` 下立案(`ISSUE-*`),写清楚复现步骤与影响。
2. 缺陷的修复派发由 `LEAD-QA` 决定(跨团队时由 `LEAD-QA` 对接开发方)。
3. 不允许 `TESTER` 直接找开发方报 bug,全部走 `LEAD-QA`。
4. 修复后的复测任务由 `LEAD-QA` 重新派发给原测试战线。

## 6. 线程与节奏

1. 同一 `thread_key`(一个测试对象的完整验证链路)同一时刻只能有一个活跃 driver,默认是 `LEAD-QA`。
2. 各战线角色只处理自己收到的子任务,不独立驱动整条线程。
3. 子任务完成后及时回给 `LEAD-QA`,不积压、不沉默。
4. `LEAD-QA` 负责判断是否已达发布门槛。

## 7. 升级给 ADMIN 的条件

出现以下情况时,`LEAD-QA` 必须升级给 `ADMIN`:

- 关键缺陷严重到建议打回发布
- 质量门槛需要调整
- 性能指标不达标但业务希望硬上
- 测试环境/数据不具备
- 跨团队缺陷修复被阻塞

## 8. 高风险动作规则

以下动作执行前必须有明确记录并等待确认:

- 线上性能压测(生产或准生产)
- 涉及真实用户数据的测试
- 清理测试环境中的数据或实例
- 发布建议为"打回"但业务要求带风险上线

## 9. 文档与归档

1. 流程文件放在 `tasks/`、`reports/`、`issues/`。
2. 测试计划、风险矩阵、自动化套件说明、性能基线放在 `shared/`。
3. 测试闭环后由 `LEAD-QA` 负责归档,并在 `shared/` 留下"本轮测试复盘"。
4. `shared/` 文档允许原地更新;任务和报告遵循追加历史原则。

## 10. 执行口径

`qa-team` 的目标不是把所有东西都测一遍,而是用有限资源让关键风险被发现、被记录、被决策:

- `LEAD-QA` 负责调度、决策、对外
- `TESTER` 负责手工验证主流程和边界
- `AUTO-TESTER` 负责把已验证的东西固化成自动回归
- `PERF-TESTER` 负责让性能问题在上线前浮出水面

三条战线独立高效、统一汇总,才能在发布前给出有说服力的质量结论。

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
