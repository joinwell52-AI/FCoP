---
protocol: fcop
version: 1
type: REPORT
sender: ME
recipient: ADMIN
date: 2026-05-09
status: done
ref_task: docs/agents/log/tasks/TASK-20260509-Z01-ADMIN-to-ME.md
subject: TASK-Z01 完成 —— v1.0 入口文档双语化
---

# REPORT-20260509-Z01-ME-to-ADMIN

> TASK-Z01 完成报告。3 commits 收口；7 项验收 100% pass。范围严格控制
> 在"入口文档"，spec 全文 + ADR 内文留 v1.0 final / v1.1。

---

## 1 · TL;DR

- **3 commits**：R1 = 入口文档；R2 = ADR TL;DR；R3 = 报告归档
- **+224 / -16** 行；15 文件（1 新建 / 14 修改）
- **测试**：未动；上游回归 965 passed（与 TASK-008 持平）
- **顺手收益**：ADR-0016 / 0017 / 0021 status 升 Accepted（之前
  状态滞后于已实施事实）

## 2 · 7 项验收

| # | 标准 | 状态 |
|---|---|---|
| 1 | README × 2 顶部 badge + nav 同步 v1.0 + RC | ✅ |
| 2 | docs/releases/1.0.0-rc.1.md 顶部双语 TL;DR | ✅ |
| 3 | CHANGELOG `[1.0.0-rc.1]` 段顶部双语 TL;DR | ✅ |
| 4 | spec/fcop-runtime-protocol-v1.0.md Abstract 加中文摘要小节 | ✅ |
| 5 | ADR-0015..0022 顶部双语 TL;DR（8 份） | ✅ |
| 6 | ADR-0016 / 0017 / 0021 status: Proposed → Accepted；adr/README 同步 | ✅ |
| 7 | 测试无回归（965 passed） | ✅ |

## 3 · 双语策略（明确范围）

| 文档类型 | 双语策略 |
|---|---|
| 用户入口（README × 2、release notes、CHANGELOG TL;DR） | **完整双语** |
| 协议规范长文（`spec/fcop-runtime-protocol-v1.0.md`） | **英文为权威**（normative）；中文限于 abstract 摘要小节 |
| ADR | 头部 TL;DR 双语；内文允许中文 / 中英混合（既有 ~30-45% 中文密度） |
| 教程文档（`docs/getting-started.md` + `.en.md`） | 已是分文件双语（之前 task 落地） |
| 任务/报告/issue（`docs/agents/`）| 中文优先（英文括注关键术语）—— 内部 |
| 长文 essay (`essays/`)、forum post | 已是分文件双语（之前 task 落地） |

> 这份策略来自用户反馈："本来就要双语的，也没关系！" + "双语后面补
> 就可以了；" —— 不强求一次完整双语 + 不破坏已有英文权威性。

## 4 · 顺手收益：ADR status 校准

发现 ADR-0016 / 0017 / 0021 status = Proposed 但实际已实施完毕：

| ADR | 实际实施 task | 落地产物 |
|---|---|---|
| ADR-0016 | TASK-003 R1（schema 物化）+ TASK-004 R1（jsonschema 校验器）| `spec/schemas/*.schema.json` × 7 + `src/fcop/core/jsonschema_validator.py` |
| ADR-0017 | TASK-004 R2（REVIEW envelope + Project.write_review）| `Project.write_review` + `review.schema.json` + 4 值 decision |
| ADR-0021 | TASK-003 R1（encoding.schema.json 物化）+ ADR-0022 子决议 sign-off | `encoding.schema.json` + IPC/Open Knowledge 两面切分 |

3 份 ADR 各加 Accepted-on 字段说明实施 task；status 升 Accepted。
adr/README.md 索引同步。这下 v1.0 8 份 ADR（0015-0022）全部 Accepted，
为 v1.0.0 final tag 解除"ADR Proposed 残留"路障。

## 5 · 设计决策

| 决策 | 理由 |
|---|---|
| Spec 长文不全译，仅 abstract 双语 | 工作量太大；spec 是 normative，需要双向同步质量保证；abstract 已能让中文用户判断"要不要往下读" |
| ADR TL;DR 段而非完整双语 | ADR 不可变正文；TL;DR 是 meta 段允许追加；既有内文 ~30-45% 中文密度已可读 |
| ADR-0016/0017/0021 顺手升 Accepted | 状态滞后于事实；不升级 v1.0 final 时还得再清；既有 ADR-0018/0019/0020 模板可套 |
| README spec badge 改 v1.0 RC（不直接 v1.0） | 准确反映当前状态；final tag 后再 bump |

## 6 · self-review

- [x] 7 项验收 100% pass
- [x] 3 commits 收口；R1 / R2 / R3 模板
- [x] 范围控制（不全译 spec / ADR 长文）显式记入决策
- [x] 顺手收益（ADR status 校准）显式标注
- [x] 全回归无新红
