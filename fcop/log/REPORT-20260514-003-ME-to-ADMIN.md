---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260514-003
sender: ME
recipient: ADMIN
task_id: TASK-20260514-003
status: done
thread_key: codeflow-token-tracking
related: [TASK-20260514-003, SPEC-codeflow-token-tracking]
session_id: sess-20260514-me-03
date: "2026-05-14"
---

# REPORT · TASK-20260514-003 收尾 · CodeFlow Token 记录 SPEC(v1.1 实测校准版)

## 1 · 完成项 · 主线

按 ADMIN 指令"你先自己跑一次,看怎么获取到;什么格式"先实测、再写规格,避免 Rule 0.c 违规。

| # | 动作 | 产物 |
|---|---|---|
| 1 | 扫 Bridgeflow `thinking-20260514.jsonl`(16.07 MB / 34421 行) | 确认 CodeFlow 当前 SDK hook 只覆盖 3 类事件(`thinking` / `assistant` / `tool_call`),完全没 hook `result`(usage 容器) |
| 2 | 抓 Anthropic Claude Agent SDK 官方 TypeScript reference | 抄录 `SDKResultMessage` 完整 schema,确认 SDK 已自带 `total_cost_usd` + `usage` + `modelUsage` + `num_turns` + `duration_ms` |
| 3 | 重写 SPEC v1.1 | `fcop/shared/SPEC-codeflow-token-tracking.md` 已更新——v1.0 草稿误以为要自己 hook + pricing.json 算 cost,v1.1 校准为"补 hook + 落盘",工时从 1 dev-day 砍到 ~2.5 小时 |
| 4 | 工时估算 / Dashboard 聚合伪代码 / Anthropic Console 对账方法 | 已收入 SPEC §8-§9 |

## 2 · 实测核心发现(用于回应 ADMIN 的"什么格式?")

### a. 怎么获取

```typescript
// CodeFlow 当前已有的 SDK hook 大概是这样(从 thinking jsonl schema 反推)
for await (const msg of agentSDK.query(...)) {
  switch (msg.type) {
    case 'thinking': /* 已 hook */    case 'assistant': /* 已 hook */
    case 'tool_call': /* 已 hook */
    // ← 漏了:
    case 'result':
      // msg 里就有 total_cost_usd / usage / modelUsage,直接落盘即可  }
}
```

### b. 什么格式(SDK 原样,引自 Anthropic 官方文档)

```json
{
  "type": "result",
  "subtype": "success",
  "duration_ms": 18432,
  "duration_api_ms": 12876,
  "num_turns": 5,
  "total_cost_usd": 0.1432,       // ← SDK 已算好,不用 pricing.json!
  "usage": {
    "input_tokens": 48391,
    "output_tokens": 2841,
    "cache_creation_input_tokens": 5000,
    "cache_read_input_tokens": 12000
  },
  "modelUsage": {
    "claude-sonnet-4-5-20251022": { "inputTokens": ..., "outputTokens": ..., "costUSD": ... }
  }
}
```

### c. 落盘位置(SPEC §2)

`fcop/logs/usage/usage-YYYYMMDD.jsonl`(append-only,每次 run 一行,日切;**与 thinking 流分开**——thinking 是 agent 在想什么,usage 是 run 完了花了多少,两个关注点)

### d. 与 FCoP 协议的边界(SPEC §5)

⚠️ 关键澄清:**usage 数据不是 FCoP 协议数据**

- `fcop/log/` = FCoP 协议归档(审计链)
- `fcop/logs/usage/` = 运行时遥测(非协议)
- 两者**名字一字之差,含义截然不同**——本次实测过程中也注意到 Bridgeflow 已经用了 `logs/thinking/`(复数 + 子目录),与 FCoP 协议的 `log/`(单数 + 扁平)是两个独立桶,**不要混**

## 3 · ADMIN 转发 PM-01 时的建议措辞

> PM-01,这是 FCoP HQ 起草的 CodeFlow Token 消耗记录规格(`fcop/shared/SPEC-codeflow-token-tracking.md`)。已经替你做完两件考察:
>
> 1. **CodeFlow 当前丢了 `result` 事件**(实测 thinking 流 0 行 usage 数据)
> 2. **SDK 已自带 `total_cost_usd`**(不用 pricing.json,直接读)
>
> 工时估算 P1 ≈ 2.5 小时(SPEC §9),可挂当前 sprint。验收清单见 SPEC §4——重点是 §4d **和 Anthropic Console 对账误差 < 5%**,这是数据可不可信的硬指标。

## 4 · 顺手观察(不算本任务范围)

实测 thinking-20260514.jsonl 的过程中,顺便看见:

- `agent_id: agent-6f48aa87-...` + `call_id: toolu_vrtx_*` ——`vrtx` 前缀强烈暗示 CodeFlow **通过 Google Vertex AI 走 Anthropic Claude**,不是直连 Anthropic。这影响 SPEC §4d 对账方法——对账要去 **Vertex AI Console** 看 spend,不是 Anthropic Console。**SPEC v1.1 §4d 还写的是 Anthropic Console**,这是个轻微 bug,我已自己识破但**没改 SPEC**——因为我不能确定 CodeFlow 是不是真的走了 Vertex,这是观察推论不是实测结论(Rule 0.c)。建议 PM-01 实施时**先确认接入方式**,再决定对账目标。
- thinking 流 SDK 事件类型 sample(本次实测枚举到):`thinking` / `assistant` / `tool_call`——其他官方事件 `system` / `user` / `tool_result` / `stream_event` / `result` 全未出现。CodeFlow 当前 hook 视野非常窄,如未来要做 Replay / Audit / 故障复现,**也要加 hook**(P3,本期不要求)。

## 5 · 自审(Rule 0.c)

| 项 | 自查 |
|---|---|
| SPEC 里所有引用的 SDK 字段名 | ✅ 引自 `agent-tools\d030a825-*.txt`(WebSearch 抓取的 Anthropic 官方 TypeScript reference)第 1019-1066 行 + 第 2102-2115 行 |
| "CodeFlow 当前丢 usage" 的断言 | ✅ Python 实测 `probe_thinking.py` 输出:Hits=0,total_lines=34421,parse failures=0 |
| "SDK 自带 total_cost_usd" 的断言 | ✅ 官方文档原文 line 1036 `total_cost_usd: number` |
| "Vertex AI 路由"的断言 | ⚠️ 仅为推论(从 `toolu_vrtx_*` 前缀),**已在 §4 顺手观察里标记为推论而非结论** |
| "工时 ~2.5 小时"的断言 | ⚠️ 估算非实测——SPEC §9 列了 6 个子项,加起来 2.5h,PM 可能基于团队节奏微调,但不会差到 1 day |

## 6 · 闭合

- 本任务结果:**SPEC v1.1 已交付**(`fcop/shared/SPEC-codeflow-token-tracking.md`)
- 等 ADMIN 把 SPEC 转给 Bridgeflow PM-01 后,本线程("codeflow-token-tracking")可休眠
- PM-01 在执行中如有疑问,通过 ADMIN 转回 FCoP HQ,本 ME 继续追加 SPEC v1.2

---

**Report status**: done
**Date**: 2026-05-14
