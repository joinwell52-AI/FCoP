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

| 教程 | 时长 | 演示了什么 | 中文 | English |
|---|---|---|---|---|
| 【免费开源】【多 agent 实战】【教你怎么指挥 agent】：FCOP-MCP 让 AI 团队有纪律 | ~45 min | 自动装 `fcop-mcp` → solo 写一只能跑的贪吃蛇 → `create_custom_team(force=True)` 一句话切 PLANNER + CODER 两人团队 → ADMIN 提原创主题需求做成《星轨织者 NEON ORBIT》→ **真实复现一次 PLANNER 越界冒充 CODER 的事故并按协议归档** → CODER 接手草稿、修复护盾 bug → 总章「指挥 agent 的 6 条铁律」抽象出可复用方法论 | [snake-solo-to-duo.zh.md](snake-solo-to-duo.zh.md) | _即将上线_ |

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
