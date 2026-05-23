---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: media-team
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-05-12
---

# media-team 运行规则

## 1. 基本路由

1. `ADMIN ↔ PUBLISHER` 是唯一对外接口。
2. `COLLECTOR / WRITER / EDITOR` 只从 `PUBLISHER` 接任务、只向 `PUBLISHER` 回执。
3. 不允许 `COLLECTOR ↔ WRITER`、`WRITER ↔ EDITOR` 横向直交稿件——**所有稿件流转必经 `PUBLISHER`**。
4. 横向协作需求必须先回 `PUBLISHER`,由其决定是否拆新任务。

## 2. 任务派发规则

### PUBLISHER 直接做

- 选题澄清、品牌口径定义
- 任务拆解、优先级排序
- 终审(事实、口径、合规)
- 发布排期
- 对 `ADMIN` 的阶段回执

### PUBLISHER 派给 COLLECTOR

- 素材搜集、事实核查、数据收集
- 引用源定位
- 竞品/热点调研

### PUBLISHER 派给 WRITER

- 初稿撰写(派发时**附上已审核的素材包**)
- 标题/导语/结构调整
- 专栏化重写

### PUBLISHER 派给 EDITOR

- 语言润色、排版规范
- 事实核对、引用核查
- 发布前格式清洗

## 3. 稿件流转规则

1. 每一轮流转都是"派发任务 + 上一轮产物"的形式,不允许 `WRITER` 直接拉 `COLLECTOR` 的文件。
2. `PUBLISHER` 把素材包附在 `PM-to-WRITER` 任务里一起派发(或放在 `shared/` 并在任务中引用)。
3. `EDITOR` 拿到的稿件来自 `PUBLISHER` 回流的 `WRITER` 初稿,不从 `WRITER` 直接拿。
4. 每次流转都要产生可追溯的文件记录。

## 4. 回执规则

1. 每条任务都必须有对应回执。
2. 回执必须说明:状态、产出文件、遗留问题、下一步建议。
3. `COLLECTOR / WRITER / EDITOR` 的正式回执目标都是 `PUBLISHER`。
4. `PUBLISHER` 汇总后,统一向 `ADMIN` 输出稿件状态与最终成品。
5. 口头同步不算回执,必须落成文件。

## 5. 线程与节奏

1. 同一 `thread_key`(一篇稿件的完整链路)同一时刻只能有一个活跃 driver,默认是 `PUBLISHER`。
2. 派出子任务后,其他角色只处理自己收到的那一段,不独立驱动整条线程。
3. 子任务完成后及时回给 `PUBLISHER`,不积压、不沉默。
4. `PUBLISHER` 负责判断稿件是否进入下一阶段或归档。

## 6. 升级给 ADMIN 的条件

出现以下情况时,`PUBLISHER` 必须升级给 `ADMIN`:

- 选题方向需要调整
- 出现合规/法律/事实争议,需要裁决
- 素材缺失导致原计划无法继续
- 发布渠道或时间需要改动
- 品牌口径冲突

## 7. 高风险动作规则

以下动作执行前必须有明确记录并等待确认:

- 正式发布到公开渠道(公众号/博客/社交平台)
- 涉及第三方账号、品牌合作、授权引用的内容
- 删除已发布稿件或公开撤稿
- 涉及敏感话题/人物的内容

已发布内容不得静默修改,必须留下修订说明。

## 8. 文档与归档

1. 流程文件走 `_lifecycle/` 生命周期目录（inbox → active → review → done → archive）；问题备忘录放 `issues/`。
2. 素材包、稿件历史、品牌规范放在 `shared/`。
3. 发布完成后由 `PUBLISHER` 负责归档。
4. `shared/` 文档允许原地更新;任务和报告遵循追加历史原则。

## 9. 执行口径

`media-team` 的目标不是让每个角色都在同时写稿,而是让每一篇稿件的每一步都有归属:

- `PUBLISHER` 负责调度、终审、对外
- `COLLECTOR` 负责事实与素材
- `WRITER` 负责结构与文字
- `EDITOR` 负责品质与合规

每一步都可追溯,稿件才可靠;稿件可靠,品牌才可信。

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
