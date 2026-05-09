---
protocol: fcop
version: 1
type: TASK
sender: ADMIN
recipient: ME
date: 2026-05-09
priority: P1
status: in_progress
subject: 双语补齐（核心入口文档）—— v1.0 RC 用户体验
ref_charter: adr/ADR-0015-fcop-1.0-ai-os-protocol-charter.md
ref_predecessor: docs/agents/log/tasks/TASK-20260509-008-ADMIN-to-ME.md
acceptance_criteria_count: 6
---

# TASK-20260509-Z01-ADMIN-to-ME

> Solo 模式任务。范围控制：仅核心**入口**文档双语化（不全译 spec 长文 +
> 长 ADR 内文），目标是让中文用户能看到 v1.0 的 framing 与 RC 状态，
> 不被英文挡在门外。

---

## 1 · 为什么需要这个任务

用户多次反馈：「你现在写的都是英文版本了，我都看不懂了哦」 +
「本来就要双语的，也没关系！」+ 「双语后面补就可以了」。

矛盾的诉求 → 范围控制：

1. **核心面向用户的入口必须双语**（README、release notes、CHANGELOG
   首段、spec abstract、ADR 头部 TL;DR）
2. **深度技术文档（spec 全文 + ADR 内文）暂不全译**（工作量太大，
   留 v1.0 final / v1.1）

## 2 · 决议

| # | 决议 | 理由 |
|---|---|---|
| 1 | README × 2（en + zh）badge 同步 v1.0 + RC | 入口最高优先级 |
| 2 | RC release notes 加双语 TL;DR | 链入口必看 |
| 3 | CHANGELOG `[1.0.0-rc.1]` 段加双语 TL;DR | RC 用户读 changelog 必看 |
| 4 | Spec v1.0 abstract 加中文摘要小节 | spec 是英文权威，中文是导读 |
| 5 | ADR-0015..0022 顶部加双语 TL;DR 段（每份 2 段，~3-5 行）| ADR 不可变，TL;DR 是 meta 段允许追加 |
| 6 | ADR-0016 / 0017 / 0021 status: Proposed → Accepted | TASK-003/004 已实施完毕，状态滞后，顺手刷新 |
| 7 | adr/README.md 索引同步 status | 与 #6 联动 |

## 3 · 验收标准

1. ✅ README.md + README.zh.md 顶部 badge 与 nav 链接同步 v1.0 + RC
2. ✅ docs/releases/1.0.0-rc.1.md 顶部含中文 TL;DR + English TL;DR 双段
3. ✅ CHANGELOG.md `[1.0.0-rc.1]` 段顶部含中文 TL;DR + English TL;DR
4. ✅ spec/fcop-runtime-protocol-v1.0.md Abstract 段含 "摘要（简体中文）" 小节
5. ✅ ADR-0015 / 0016 / 0017 / 0018 / 0019 / 0020 / 0021 / 0022 顶部各含 "## TL;DR" 段（中文 + English 两段）
6. ✅ ADR-0016 / 0017 / 0021 status 升 Accepted；adr/README.md 索引同步
7. ✅ 测试无回归（965 passed，与上一 task 持平 + 唯一 fail 仍是已知 pre-existing）

## 4 · 执行计划

| Round | 内容 | commit prefix |
|---|---|---|
| R1 | README × 2 + RC notes + CHANGELOG + spec abstract | `docs(i18n):` |
| R2 | ADR-0015..0022 双语 TL;DR + status 升级 + adr README | `docs(adr):` |
| R3 | TASK-Z01 报告 + 归档 | `docs(workflow):` |

## 5 · self-review

- [x] 范围控制：仅入口文档；spec 全文 + ADR 内文留 v1.0 final
- [x] 不破坏既有英文版（spec 仍为权威 normative）
- [x] ADR 不可变正文；只追加 meta 段（TL;DR + Accepted-on）
- [x] 全回归无新红
- [x] 一次性完成所有验收 → 可考虑 1-2 commit 收口
