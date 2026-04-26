---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: solo
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-04-26
---

# solo 运行规则

本文定义 solo 模式的工作方式，回答"什么时候写 task、回执怎么写、什么时候
升级、怎么自审"。

## 1. 基本路由

1. `ADMIN ↔ ME` 是唯一通道——直接对接，没有中转。
2. 不允许"聊天直答"代替任务文件——`ADMIN` 在聊天里说什么，`ME` 必须把
   它**先**写成 `TASK-*-ADMIN-to-ME.md`（在 `tasks/` 下），再动手。
3. `ME` 不允许"先做后补 task"——这是 0.6.3 实战中最常见的违规，0.6.4 起
   通过 `roles/ME.md` 的硬约束段予以纠正。
4. solo 没有横向角色，所以没有"私自派单"风险，但**有"自审越权"风险**：
   `ME` 必须用文件而不是脑内推理来分隔"提案"和"审查"。

## 2. 任务派发规则

### ADMIN 直接落给 ME

solo 下所有任务都是 `ADMIN -> ME`，**没有例外**。

| `ADMIN` 在聊天里说 | `ME` 应该做 |
|---|---|
| "做个 XX 工具" | 写 `TASK-*-ADMIN-to-ME.md`，再决定 slug |
| "改一下 YY" | 写 task，再改 |
| "修一下 ZZ 的 bug" | 写 task，再修 |
| "你看看我这段代码"（纯咨询） | 不强制写 task；但若 `ME` 给出建议，建议落 `ISSUE-*` 或 `.fcop/proposals/`，不仅停在聊天 |
| "升级 fcop" | `ME` 调 `upgrade_fcop()` 工具——这是 ADMIN 的直接执行授权，不要先写 task |

> 边界判定：**会产生项目内文件改动的指令 → 必走 task**；纯问答 / 纯查询
> → 不强制 task。模糊地带优先落 task。

### ME 不要直接派给 ADMIN

solo 下 `ME` 不能"派任务给 ADMIN"。如果 `ME` 需要 `ADMIN` 做决定（比如
选方案、确认风险、批准高危动作），用 **`REPORT-*-ME-to-ADMIN.md` 加
"待 ADMIN 确认"段落**，不要伪造一个 `TASK-*-ME-to-ADMIN.md`——后者会
违反"`ADMIN` 永远是真人输入端"的协议约定。

## 3. 回执规则

1. 每条 `TASK-*-ADMIN-to-ME.md` 都必须有对应的 `REPORT-*-ME-to-ADMIN.md`。
2. 回执必须说明：
   - 状态（`done` / `in_progress` / `blocked`）
   - 已完成内容 + 产物路径（指向 `workspace/<slug>/`）
   - 阻塞项 / 待 ADMIN 决策项
   - 验证证据（跑了什么命令、命中什么 HTTP 码、看到什么输出）
3. **口头同步不算回执**——`ADMIN` 在聊天框里看到的"做完了"那段话，
   如果没落成 `REPORT-*` 文件，对协议而言**没发生**（Rule 0.a）。
4. ADMIN 验收回执后，由 ADMIN 决定调用 `archive_task()` 把 task + report
   一起搬到 `log/`。

## 4. issue 处理规则

1. `ME` 发现以下情况时**主动**落 `ISSUE-*-ME.md`：
   - FCoP 协议级冲突（"你这条规则似乎说不通"）
   - fcop / fcop-mcp 工具 bug（"`init_solo` 没暴露 force"）
   - 工作流自身的违规（"我刚才跳过了 task 直接做产物"）
2. issue 不替代 task / report——它是**额外**的备忘记录。
3. `ME` **不修改** issue 的关闭状态——`ADMIN` 决定何时 close。

## 5. 自审规则（Rule 0.b 在 solo 下的具体化）

solo 只有一个 AI，但 Rule 0.b "不允许一个 AI 独自完成决策到执行" 仍然适用。
具体落地：

1. 接到任务后，**先写 task 落盘**——这一步把"提案者 ME"凝固到文件里。
2. 动手前，**重读自己刚才写的 task**——这一步是"审查者 ME"对"提案者 ME"
   的复核（看目标对不对、范围有没有越界、验收标准清不清楚）。
3. 复杂任务再写一份 `计划草稿.md` 落到 `workspace/<slug>/_plan.md`，
   动手前重读。
4. 完成后写 report 时**再读一遍 task**——确保 report 真的回应了 task 的所有点。

文件就是"第二个角色"。solo 的纪律靠这个保证。

## 6. 升级给 ADMIN 的条件

`ME` 出现以下情况时**必须**在 report 里明确"待 ADMIN 决策"，不要自行执行：

- 任务范围超出 ADMIN 原话（有解读分歧）
- 高危操作（删数据、`git push --force`、改 `.cursor/rules/*.mdc`、
  改 `fcop.json`、改 `shared/` 下协议文件）
- 外部依赖不可用 / 阻塞 / 收费 / 触发安全策略
- 多种方案有取舍（性能 vs 简洁 vs 兼容）
- ADMIN 的指令和 FCoP 协议有冲突——绝不闷头执行，落 `ISSUE-*` 或
  `.fcop/proposals/`，让 ADMIN 仲裁

## 7. 高危动作规则

solo 下没有"二次确认人"——所以 `ME` 在执行前必须**在 task / report 里
明确写出**：

- 这个动作是高危的（理由）
- 我打算这样做（具体命令 / 步骤）
- 回滚方案是什么

写下来再执行；如果连回滚方案都写不出，就不要执行——落 issue 等 ADMIN
拍板。

## 8. 文档与归档

1. 流程文件放在 `tasks/` / `reports/` / `issues/`，**只追加不修改**（issue
   的 close 是协议允许的例外）。
2. 共享知识 / 长期约定放在 `shared/`，可原地更新。
3. 业务产物（代码、数据、脚本）**全部**放在 `workspace/<slug>/`，**绝不**
   倾倒到项目根。
4. 闭环后由 **ADMIN** 调 `archive_task()` 归档——`ME` 不主动归档（除非
   ADMIN 在 task 里授权"做完直接 archive"）。

## 9. 执行口径

solo 的目标不是"AI 一个人快速搞定"——是"哪怕只有一个 AI，纪律不打折"。

- 慢一点没关系，不能跳过 task / report。
- 简单任务也不能跳过 task / report——**一旦给"简单"开口子，所有任务都会
  自称"简单"**。这是 0.6.3 实战教训。
- 不确定的事，写到 task / report 里给 ADMIN 看，不闷头猜。

文件协议是 solo 唯一不会变形的纪律。
