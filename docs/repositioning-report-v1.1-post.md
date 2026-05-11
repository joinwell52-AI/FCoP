# FCoP 哲学重定位工作报告

- **日期**：2026-05-11
- **轮次**：v1.1.0 发布后 · 架构哲学收敛
- **性质**：文档 + 规则文件全局更新（无代码变更）
- **关联 ADR**：ADR-0029, ADR-0030

---

## 一句话结论

FCoP 完成从 **"AI OS 协议层"** 到 **"AI Agent 行为治理协议层"** 的哲学收敛。

---

## 核心定位

```
FCoP 是一个约束 Agent 行为的
"可观测 + 可审计 + 可治理协议层"
它不调度任务，只规定行为如何被记录与评估。
```

**三支柱：**

| 支柱 | 原语 | 本质 |
|------|------|------|
| Report | `fcop_report()` | 语义行为声明，让行为成为事实而非黑箱 |
| Review | `fcop_review()` | Code as Law 判例库，将人类意志织入行为流 |
| Capability | `capability governance` | 物理护栏，高风险行为在批准前无法物理发生 |

**边界一句话：**
> CodeFlow 负责"让事情发生"，FCoP 负责"让事情合法地发生"。

---

## 本轮变更范围

### ADR（架构决策记录）

| 文件 | 状态 | 内容 |
|------|------|------|
| `adr/ADR-0029-fcop-behavior-governance-charter.md` | ✅ 新建 + 精化 | FCoP 核心哲学宪章：三支柱定义、Non-Goals、Minimalism Principle、write_task() 降级、CodeFlow 边界 |
| `adr/ADR-0030-capability-governance-boundary.md` | ✅ 新建 | Capability Governance 三层分类（Safe / Sensitive / Critical）的边界定义 |
| `adr/ADR-0028-auto-risk-assessment.md` | ⚠️ 标记待修订 | 原方案含过多 write_task() 治理逻辑，需与新哲学对齐 |

### 规则文件（面向 Agent）

| 文件 | 变更内容 |
|------|----------|
| `src/fcop/rules/_data/fcop-rules.mdc` | 协议层定位章节重写；5 层技术栈图替换 3 层旧图；Rule 9 头部去 "AI OS" |
| `src/fcop/rules/_data/fcop-protocol.mdc` | frontmatter description 更新 |
| `.cursor/rules/fcop-rules.mdc` | 由 `deploy_protocol_rules(force=True)` 同步（v2.2.0） |
| `.cursor/rules/fcop-protocol.mdc` | 同步 |
| `AGENTS.md` | 同步 |
| `CLAUDE.md` | 同步 |

### 主 README

| 文件 | 变更内容 |
|------|----------|
| `README.md`（英文） | 移除 "AI OS" 定语；更新技术栈图为 5 层模型；核心定位段重写 |
| `README.zh.md`（中文） | 同上 |

### 用户文档

| 文件 | 变更内容 |
|------|----------|
| `docs/getting-started.md` | 标题定语；技术栈图；新增 CodeFlow/FCoP 边界说明；非目标重写；FAQ 稳定性承诺 |
| `docs/getting-started.en.md` | 同上（英文） |

### 规范文件

| 文件 | 变更内容 |
|------|----------|
| `spec/fcop-runtime-protocol-v1.0.zh.md` | "技术栈中的位置"一节替换为 5 层模型，移除 POSIX 强类比 |

---

## 技术栈对比（新旧）

**旧（AI OS 类比）：**

```
┌─────────────────────────────────┐
│     Business / Application      │
├─────────────────────────────────┤
│  FCoP · AI OS Protocol Layer    │
├─────────────────────────────────┤
│    Host IDE / LLM Inference     │
└─────────────────────────────────┘
```

**新（行为治理协议层）：**

```
┌─────────────────────────────────────────────┐
│  应用层   CodeFlow / Cursor / Claude Desktop │
├─────────────────────────────────────────────┤
│  宿主适配  fcop-mcp / fcop-cli / @fcop/claude│
├─────────────────────────────────────────────┤
│★ FCoP 协议层  行为报告 / Review /            │
│               Capability Governance / Audit │
├─────────────────────────────────────────────┤
│  参考实现  fcop（Python Library）            │
├─────────────────────────────────────────────┤
│  执行基底  LLM API / MCP Tools / 文件系统    │
└─────────────────────────────────────────────┘
```

---

## 哲学收敛总结

| 维度 | 旧定位（已废止） | 新定位（本轮确立） |
|------|----------------|------------------|
| 类比对象 | POSIX / OCI / CRD | Git + Code Review |
| 核心职责 | 协调 agent 之间的工作流 | 约束 agent 行为的合法性 |
| write_task() | Core runtime abstraction | Optional coordination primitive |
| 非目标 | 未明确 | Workflow engine / BPM / Orchestrator（明确列出） |
| 与 CodeFlow 关系 | 竞争 / 重叠 | 清晰分工：CodeFlow 执行，FCoP 治理 |

---

## fcop-mcp 1.1.1 补丁发布（2026-05-11）

| 项目 | 状态 |
|------|------|
| PyPI `fcop-mcp 1.1.1` 发布 | ✅ 已发布 |
| 4 个 Review 工具补入（write_review / list_reviews / read_review / mark_human_approved） | ✅ 已验证 |
| Cursor MCP 面板显示 30 工具（截图确认） | ✅ |
| letter-to-admin 工具数量 26 → 30 | ✅ 已修正 |

---

## 后续待办（P2）

| 编号 | 内容 | 状态 |
|------|------|------|
| P2-1 | 修订 ADR-0028（自动风险评估与新哲学对齐） | 待开始 |
| P2-2 | 实现 Capability Taxonomy 三层代码支撑（ADR-0030） | 待开始 |
| P2-3 | 更新 `spec/fcop-runtime-protocol-v1.1.md` 技术栈图 | 待开始 |
