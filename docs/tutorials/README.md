# FCoP 教程索引

> **MCP 工具帮你管理 agent，从单 agent 模式向多 agent 模式转变。** 整个教程合集围绕同一个公式：
>
> 1. **痛点**：单 agent 什么都做，容易陷入**记忆爆炸**。
> 2. **立场**：agent 让我们学会做 ADMIN；**我们不是码农，我们是指挥者、领导者，而 agent 是我们的数字员工**。
> 3. **机制**：每一次记录、每一个文件的落盘，都是为了**管理、追溯、审计、有序、有规则**。
>
> 协议规范去 [`docs/fcop-standalone.md`](../fcop-standalone.md) 与 [`adr/`](../../adr/)；本目录只放**实战教材**——读者画像 + prompt + 真实截图 + 踩坑事故 + 可复用的方法论。
>
> **不知道自己适不适合用？** 直接跳教程末尾的 [附录 A：FCoP 适用边界](snake-solo-to-duo.zh.md#附录-a-fcop-适用边界)——用 3 句话告诉你"该不该用"、"1 人公司怎么用"、"大型项目怎么用"。

## 当前可用

> **两个并列案例，同一个协议**：中文版用**贪吃蛇**做单 agent → 双 agent 切换 + PLANNER 越界冒充 CODER 的彩蛋；英文版用**俄罗斯方块**做同一条路径 + 一个真实的"v1 被 ADMIN 试玩驳回 → PLANNER 写 TASK-006 加 `Verification Requirements` → v2 通过"评审-重做循环 + 在 dogfood 末尾问 agent "你怎么看 FCoP" 收到的诚实自评。任选一篇先读都行。

| 教程 | 时长 | 演示了什么 | 链接 |
|---|---|---|---|
| 【免费开源】【多 agent 实战】【教你怎么指挥 agent】：FCOP-MCP 让 AI 团队有纪律（**中文母语原创 · 贪吃蛇案例**） | ~45 min | 自动装 `fcop-mcp` → solo 写一只能跑的贪吃蛇 → `create_custom_team(force=True)` 一句话切 PLANNER + CODER 两人团队 → ADMIN 提原创主题需求做成《星轨织者 NEON ORBIT》→ **真实复现一次 PLANNER 越界冒充 CODER 的彩蛋并按协议归档** → CODER 接手草稿、修复护盾 bug → 总章「指挥 agent 的 6 条铁律」抽象出可复用方法论 | [snake-solo-to-duo.zh.md](snake-solo-to-duo.zh.md) · [CSDN](https://blog.csdn.net/m0_51507544/article/details/160603953) |
| [Free & Open Source] [Multi-Agent Hands-On] [How to Command Agents]: FCoP-MCP Brings Discipline to AI Teams (**English · Tetris case**) | ~45 min | Auto-install `fcop-mcp` → ship `Nebula Stack` (Tetris) in solo mode → switch to PLANNER + CODER team in one sentence → PLANNER designs `Comet Loom` → CODER ships v1 → **ADMIN plays it, finds 3 blocking defects, bounces it back** → PLANNER writes TASK-006 with new `Verification Requirements` → CODER ships v2 → `fcop_check()` reveals 8 silent role-switch evidence files → **agents get interviewed on the record about what they think of FCoP** → six iron rules of commanding agents | [tetris-solo-to-duo.en.md](tetris-solo-to-duo.en.md) |
| 上一行英文教程的**中文译本** · 俄罗斯方块案例 | ~45 min | 同上一行英文版的内容，俄罗斯方块案例的中文翻译版（非中文母语原创；权威版以英文版为准）。供中文读者阅读两个并列案例的"另一边"用 | [tetris-solo-to-duo.zh.md](tetris-solo-to-duo.zh.md) |

## 计划中

| 主题 | 状态 | 说明 |
|---|---|---|
| 把已有项目改造成 FCoP 项目（**brownfield**） | 占位 | `init_project(force=True)` 在已有 git 仓里如何安全归档老结构 |
| 多 AI 主机协作（Cursor + Claude Code 同仓） | 占位 | ADR-0006 host-neutral rule distribution 实战 |
| 从 0.6.x 升级到 0.7.x | 占位 | 角色唯一性、Rule 0.a.1、`fcop_check()` 的迁移路径 |

## 写教程的原则

1. **可复制粘贴**——所有 prompt 用反引号代码块，不掺中文全角符号，让读者一秒贴到 Cursor 就能跑
2. **真实截图**——所有截图来自一台**真实干净的电脑**走完一遍流程，不是合成或事后补的
3. **挂协议链接**——每个关键步骤都连到对应的 Rule / ADR / Issue / Report，让读者随时跳到原始证据
4. **指向账本**——结尾让读者看仓里的 `docs/agents/log/`，"filesystem is the protocol" 比任何说理都有力
5. **双语对齐**——中文版 `*.zh.md`、英文版 `*.en.md`，结构 1:1，章节锚点同名（方便互相对照阅读）
