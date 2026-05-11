---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260427-008
sender: ADMIN
recipient: ME
priority: P1
session_id: sess-20260427-me-072
---

# 写中文版教程：从 solo 到 2 人团队的贪吃蛇

## 背景

0.7.2 发版收尾，ADMIN 准备在另一台干净电脑上 dogfood + 写一份
"在 Cursor 里用 fcop-mcp 写贪吃蛇"的图文教程，向新用户展示 FCoP
最有戏剧性的能力——**solo 模式起步 → 一句话切到 2 人团队 → 老
归档不丢 → 新角色上岗**。

英文版稍后由 ADMIN 实操英文 session + AI 翻译正文 + 校读交付。
当前任务：先把**中文版骨架**写出来，新电脑实操时按骨架填截图、
贴真实输出即可。

## 要求

### A. 文件位置

1. `docs/tutorials/snake-solo-to-duo.zh.md`：主教程，章节齐全、
   prompt 可复制即用、截图占位符明显、每段解说"这一步 FCoP 在做
   什么"。
2. `docs/tutorials/README.md`：教程目录索引（首份，未来扩展）。

### B. 教程内容骨架

第 0 章：5 分钟把 fcop-mcp 装到 Cursor（一句话让 AI 自装）
第 1 章：solo 模式起步 + 贪吃蛇 v1（演示 Rule 0.a.1 四步循环）
第 2 章：`create_custom_team(force=True)` 切到 PM+DEV 2 人团队
        （演示 Rule 1 角色占用 + Rule 5 追加不删 +
        `.fcop/migrations/` 无损归档）
第 3 章：PM 拆 task + DEV 实现 v2 双人模式（演示
        `session_id ↔ role` 一致性 + 软角色锁）
结尾：彩蛋——指给读者看 FCoP 自己仓的 `docs/agents/log/`，
      "filesystem is the protocol" 自证

### C. 每章必含元素

- 一句话目标
- 一段可直接复制粘贴到 Cursor 的 prompt
- 期望的 fcop-mcp 工具调用清单（让读者对照检查 AI 没漏步）
- 截图占位符（统一前缀 `tutorial-assets/snake/<step>.png`）
- "这一步 FCoP 在做什么"3-5 行解说，挂相关协议条款链接
  （Rule 0.a.1 / Rule 1 / Rule 5 / ADR-0002 / ADR-0006 等）
- "如果出错怎么办" mini-FAQ（如 0.7.2 propagation lag / uvx
  cache stale）

### D. 协议账本

- 写完即 `REPORT-20260427-008` done report
- archive task
- 由于这是文档新增、无代码变更，不需要发版

### E. 不在本任务范围

- 真实截图（要新机器跑了才有，先留占位符）
- 英文版（下一任务）
- 视频/GIF（远期）

## 验收

- 两个文件落盘且通过 `markdownlint`（如果配置）
- 中文教程 ≥ 800 字、≤ 2500 字（保持轻量；过长读者会跑）
- 所有 prompt 可复制粘贴（不含中文全角符号干扰）
- 所有协议条款引用都有相对路径链接（`../../adr/...` /
  `../../src/fcop/rules/_data/fcop-rules.mdc`）
- README index 包含本教程 + 至少 1 行"未来教程"占位
