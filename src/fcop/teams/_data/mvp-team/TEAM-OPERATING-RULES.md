---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: mvp-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-04-17
---

# mvp-team 运行规则

## 1. 基本路由

1. `ADMIN ↔ MARKETER` 是唯一对外接口。
2. `RESEARCHER / DESIGNER / BUILDER` 只从 `MARKETER` 接任务、只向 `MARKETER` 回执。
3. 不允许 `RESEARCHER ↔ DESIGNER`、`DESIGNER ↔ BUILDER` 横向直交产物——必经 `MARKETER`。
4. 横向协作需求必须先回 `MARKETER`,由其决定是否拆新任务。

## 2. 任务派发规则

### MARKETER 直接做

- 愿景澄清、市场目标定义、资源约束排序
- 任务拆解、里程碑规划
- 是否进入下一轮、是否 pivot 的决策
- Landing Page、冷启动、增长实验
- 对 `ADMIN` 的阶段回执

### MARKETER 派给 RESEARCHER

- 市场分析、竞品拆解
- 用户访谈、问卷、数据采集
- 机会/风险评估

### MARKETER 派给 DESIGNER

- PRD 撰写(派发时**附上已审核的调研结论**)
- 用户流程、交互设计、关键界面
- 可行性/合规性/可测量性评估

### MARKETER 派给 BUILDER

- 技术选型、架构决策
- MVP 搭建、环境、部署
- 技术债与限制说明

## 3. 产物流转规则

1. 每一轮流转都是"派发任务 + 上一轮产物"的形式,不允许下游直接拉上游的文件。
2. `MARKETER` 把调研结论附在 `MARKETER-to-DESIGNER` 任务里一起派发(或放 `shared/` 并引用)。
3. `BUILDER` 拿到的 PRD 来自 `MARKETER` 回流的 `DESIGNER` 产出,不从 `DESIGNER` 直接拿。
4. 每次流转都要产生可追溯的文件记录。

## 4. 回执规则

1. 每条任务都必须有对应回执。
2. 回执必须说明:状态、产出文件、关键结论、不确定性、下一步建议。
3. `RESEARCHER / DESIGNER / BUILDER` 的正式回执目标都是 `MARKETER`。
4. `MARKETER` 汇总后,统一向 `ADMIN` 输出阶段结论与里程碑。
5. 口头同步不算回执,必须落成文件。

## 5. 线程与节奏

1. 同一 `thread_key`(一个 MVP 假设的完整验证链路)同一时刻只能有一个活跃 driver,默认是 `MARKETER`。
2. 派出子任务后,其他角色只处理自己收到的那一段,不独立驱动整条线程。
3. 子任务完成后及时回给 `MARKETER`,不积压、不沉默。
4. `MARKETER` 负责判断是否进入下一阶段或 pivot。

## 6. 升级给 ADMIN 的条件

出现以下情况时,`MARKETER` 必须升级给 `ADMIN`:

- 关键假设被调研推翻,方向需要 pivot
- 资源(时间/预算/人力)不够完成下一轮
- 合规、法律、市场准入风险
- 需要 `ADMIN` 做"杀掉/继续/改方向"的决策
- 外部合作或付费资源需要批准

## 7. 高风险动作规则

以下动作执行前必须有明确记录并等待确认:

- 正式上线面向真实用户的服务
- 涉及付款、个人数据、账号系统的功能
- 对外品牌发声(Landing Page 正式发布、媒体稿件)
- 花钱:采买服务、跑付费广告、外包

花钱、影响品牌、处理用户数据的动作,**默认都要回 `ADMIN`**。

## 8. 文档与归档

1. 流程文件放在 `tasks/`、`reports/`、`issues/`。
2. 调研结论、PRD、架构决策放在 `shared/`。
3. 一轮迭代闭环后由 `MARKETER` 负责归档,并在 `shared/` 留下"本轮复盘"。
4. `shared/` 文档允许原地更新;任务和报告遵循追加历史原则。

## 9. 执行口径

MVP 阶段的目标不是"做出最完整的东西",而是"用最小代价验证最关键的假设":

- `MARKETER` 负责调度、增长、决策
- `RESEARCHER` 负责把假设变成证据
- `DESIGNER` 负责把证据变成方案
- `BUILDER` 负责把方案变成可用的东西

假设清晰 → 验证可靠 → 决策有据 → 下一轮值得开。
