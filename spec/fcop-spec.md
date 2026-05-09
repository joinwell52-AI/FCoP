<p align="center">
  <img src="../assets/fcop-logo-256.png" alt="FCoP Logo" width="200" />
</p>

# FCoP 正式规范入口

> **File-based Coordination Protocol · AI OS Protocol Layer**
> 让 AI 协作像整理文件夹一样简单

## 当前正式版（v1.0）

| 语言 | 规范文件 | 状态 |
|---|---|---|
| **English（权威）** | [fcop-runtime-protocol-v1.0.md](./fcop-runtime-protocol-v1.0.md) | ✅ 正式发布 |
| 简体中文（参考译文） | [fcop-runtime-protocol-v1.0.zh.md](./fcop-runtime-protocol-v1.0.zh.md) | ✅ 正式发布（informative） |

> 两个版本不一致时，**以英文版为准**。

本文件是**稳定入口链接**，始终指向最新正式规范。外部引用、README 跳转请使用本文件。

---

## 版本历史

| 版本 | 日期 | 状态 | 规范文件 |
|---|---|---|---|
| **v1.0** | 2026-05-09 | ✅ **当前正式版** | [fcop-runtime-protocol-v1.0.md](./fcop-runtime-protocol-v1.0.md) |
| v0.7.x（≤1.0.3） | 2026-04-18/19 | 已被 v1.0 取代（保留为遗留参考） | [fcop-spec-v1.0.3.md](./fcop-spec-v1.0.3.md) |

---

## FCoP v1.0 核心要点

- **协议层定位**：AI OS Protocol Layer（POSIX 之于 Unix，CRD 之于 Kubernetes）
- **七大核心概念**：Agent · IPC · Encoding · Event · Failure · Boundary · Audit
- **协调基础**：共享文件系统——无数据库、无消息队列、无专用服务器
- **机器可读契约**：[`spec/schemas/`](./schemas/)（7 个 JSON Schema）

## 配套文档

- [`docs/getting-started.md`](../docs/getting-started.md) — 快速入门
- [`adr/`](../adr/) — 架构决策记录（为什么这样设计）
- [`docs/MIGRATION-1.0.md`](../docs/MIGRATION-1.0.md) — 从 0.7.x 升级指南

## 配套实现（与协议正交）

- **[`fcop`](https://pypi.org/project/fcop/)**（PyPI）：Python 参考实现
- **[`fcop-mcp`](https://pypi.org/project/fcop-mcp/)**（PyPI）：MCP 桥接（Cursor / Claude Desktop 等）
