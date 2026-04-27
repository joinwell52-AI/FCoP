# FCoP 教程索引

> 面向**初次接触 FCoP 的 Cursor 用户**。每篇教程都是"一台干净电脑 + 一段 prompt → 看到一个能跑的项目"的可复制路径，不是抽象介绍。
>
> 协议规范请看 [`docs/fcop-standalone.md`](../fcop-standalone.md) 与 [`adr/`](../../adr/)；本目录只放**教程**——脚本、prompt、截图、踩坑记录。

## 当前可用

| 教程 | 时长 | 演示了什么 | 中文 | English |
|---|---|---|---|---|
| 从空文件夹到 2 人团队的贪吃蛇 | ~35 min | 自动装 `fcop-mcp` → solo 模式 → `create_custom_team(force=True)` 一句话切 2 人团队 → Rule 0.a.1 四步循环 + Rule 1 角色占用 + Rule 5 追加不删 | [snake-solo-to-duo.zh.md](snake-solo-to-duo.zh.md) | _即将上线_ |

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
