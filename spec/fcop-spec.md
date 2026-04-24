<p align="center">
  <img src="../assets/fcop-logo-256.png" alt="FCoP Logo" width="200" />
</p>

# FCoP 正式规范入口

> **File-based Coordination Protocol**
> 让 AI 协作像整理文件夹一样简单

## 最新版本

**当前正式版：[FCoP v1.0.3](./fcop-spec-v1.0.3.md)**（2026-04-19）

本文件是**稳定入口链接**，始终指向最新的正式规范。外部引用、README 跳转请使用本文件，以避免版本升级时链接失效。

---

## 版本历史

| 版本 | 日期 | 状态 | 规范文件 |
|---|---|---|---|
| **v1.0.3** | 2026-04-19 | ✅ **当前** | [fcop-spec-v1.0.3.md](./fcop-spec-v1.0.3.md) |
| v1.0.2 | 2026-04-19 | 已被 v1.0.3 取代 | （合并在 v1.0.3 变更记录中）|
| v1.0.1 | 2026-04-19 | 已被 v1.0.3 取代 | （合并在 v1.0.3 变更记录中）|
| v1.0 | 2026-04-18 | 已被 v1.0.3 取代 | （合并在 v1.0.3 变更记录中）|

详细变更历史见 v1.0.3 文档开头的"变更记录"章节。

---

## 快速导览

- **核心原则**：文件名 = 唯一真理（Single Source of Truth）
- **唯一同步原语**：`os.rename()` 的原子性
- **零基础设施**：不依赖数据库、消息队列、专用服务器
- **独立说明（无产品绑定）**：[FCoP 纯协议单页 · `docs/fcop-standalone.md`](../docs/fcop-standalone.md)

## 协议扩展名

`.fcop`（推荐）或 `.md`（兼容模式）

## 本仓配套（与协议正交、可选）

- **[`fcop`](https://pypi.org/project/fcop/)**（PyPI）：Python 参考实现，读写 task/report/issue 等，**不依赖 MCP**。  
- **[`fcop-mcp`](https://pypi.org/project/fcop-mcp/)**（PyPI）：把 `fcop` 通过 MCP 接到 Cursor / Claude Desktop 等；与「纯文件协议」正交，可不用。

## 路线图中仍待补全的能力

- `fcop-cli`：独立命令行做合规校验 + 追溯（规划中）
- 更宽的编辑器 / 非 Python 生态封装（随需求演进）

> 与 FCoP **协议层**无绑定关系的第三方桌面/自动化产品，不放在本「正式规范入口」的导览里；需要时自行检索生态，不在此列名。
