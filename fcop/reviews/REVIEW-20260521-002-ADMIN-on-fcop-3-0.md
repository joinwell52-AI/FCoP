---
protocol: fcop
version: 1
type: REVIEW
review_id: REVIEW-20260521-002-ADMIN-on-fcop-3-0
subject_type: code_change
subject_ref: adr/ADR-0035 + ADR-0036 + ADR-0038 + NOTE-custody-is-not-a-layer.md
reviewer_role: ADMIN
decision: approved
decided_at: "2026-05-21T17:40:00+08:00"
subject: FCoP 3.0 canonical protocol sign-off (post-RFC semantic collapse)
---

# FCoP 3.0 Canonical Protocol · Formal Sign-Off

## 1. Scope / 评审范围

本 REVIEW **一次性签下整个 FCoP 3.0 协议本体**，覆盖：

| Subject | Status | 角色 |
|---------|--------|------|
| ADR-0035 (State Ontology) | Accepted & Frozen | NOW truth · path = state |
| ADR-0036 (Event Layer) | Accepted | PAST audit-only trace |
| ADR-0038 (Boundary Charter) | Accepted | Meta · 防 OS 化 |
| NOTE-custody-is-not-a-layer | Informative | custody 解释 |
| PROPOSAL `20260521-rfc-semantic-collapse-and-custody-rejection.md` | Archived | RFC 现场归档 |

ADR-0037（Custody Layer）已在 RFC 评审中 **Withdrawn**，不进入 Accepted。

---

## 2. Rationale / 评审理据

### 2.1 协议形态收敛完成

FCoP 3.0 完成"时间维度分治"语义收敛：

```
META       ADR-0038 · Boundary Charter        ← 防 OS 化的元宪章
              ↓
NOW         ADR-0035 · State (path = truth)   ← Frozen · 唯一 NOW 真相
PAST        ADR-0036 · Event (audit trace)    ← write-then-rename atomic
            NOTE   · Custody = interpretation ← 无层级，仅注释
```

NOW 与 PAST 在时间维度上正交，不构成"多真相"。custody 已降级为衍生解释。

### 2.2 三条核心承诺已锁定

- **Rule A**（ADR-0035）：`ls _lifecycle/<stage>/` 即真相，无需 replay
- **Rule G**（ADR-0036）：events 是 audit-only PAST trace，**不得**用于运行时状态判定
- **§5.1**（ADR-0038）：边界宪章带豁免条款，承认协议可演进但门槛清晰

### 2.3 工程可执行性已保证

- ADR-0036 §4.1 锁定 **write-then-rename atomic pattern**，原子性策略不留模糊
- ADR-0036 §4.2 明确 `_lifecycle/` 必须同一挂载点
- ADR-0038 §5.1 给出豁免触发条件（E1/E2/E3）与不可豁免红线

### 2.4 Canonical One-Liner

> **FCoP = file location is truth; everything else is trace.**
> **FCoP is filesystem-sourced with event-based auditability.**

已写入 ADR-0035 底部，作为协议本体的最简表达。

---

## 3. Decision / 评审结论

| ADR | Decision | Action |
|-----|----------|--------|
| ADR-0035 | `approved` | Frozen，不再扩展任何语义 |
| ADR-0036 | `approved` | Accepted，进入 fcop 3.0 实现路线图 |
| ADR-0038 | `approved` | Accepted，所有未来 ADR 必经其 §5 五问过滤 |
| NOTE-custody-is-not-a-layer | `approved` | Informative，作为 0037 思想的永久墓志铭 |
| PROPOSAL RFC archive | `approved` | 归档为协议演进的历史证据 |

**FCoP 3.0 协议本体正式生效。**

---

## 4. Post-Sign-Off Roadmap / 后续路线图

| 优先级 | 动作 | 责任 |
|--------|------|------|
| P0 | 实现 fcop-mcp 3.0：L1 工具按 ADR-0036 §4.1 write-then-rename pattern 重写 | 实现层 |
| P0 | 实现 `fcop migrate --to-v3`：2.x → 3.0 一键迁移脚本 | 实现层 |
| P1 | 更新 `.cursor/rules/fcop-rules.mdc` Rule 2 章节，注入 Canonical One-Liner | 文档层 |
| P1 | 在 `fcop_audit()` 加硬检查：拒绝从 events 推导 NOW state 的代码路径 | 实现层 |
| P2 | PLAN 文件归宿决策（候选：`fcop/plan/` 或 `fcop/_intent/`）| 待新 ADR |
| P2 | 写一篇 essay：`the-day-we-almost-added-custody.md` | 社区层 |

---

## 5. 一句话留存

> **2026-05-21，FCoP 完成了从"文件组织协议"到"文件系统行为流转协议"的协议级跃迁，并在同一天拒绝了一次自己的扩展。**
>
> 这两件事一起发生，标志着 FCoP 进入"协议自治"阶段——它知道自己是什么，也知道自己不是什么。
