---
protocol: fcop
version: 1
kind: spec
spec_id: SPEC-codeflow-token-tracking
sender: ME
recipient: BRIDGEFLOW-PM
related: [TASK-20260514-003]
thread_key: codeflow-token-tracking
status: draft-v1.1
date: "2026-05-14"
target_project: Bridgeflow / CodeFlow
target_role: PM-01
---

# SPEC · CodeFlow Token 消耗记录

> **送达方式**:本文件由 FCoP 总部 ME 起草,ADMIN 转交 Bridgeflow PM-01。
> **协议位置**:本文件是 Bridgeflow 项目的**需求规格**,不是 FCoP 协议规则。本期不升级 FCoP 协议本身。
>
> **v1.1 校准说明**(2026-05-14):v1.0 误以为需要 hook LLM 调用 + 自己用 pricing.json 算 cost。**实测 SDK 后发现:Claude Agent SDK 在每次 run 结束时自带 `SDKResultMessage`,包含 `total_cost_usd` + `usage` + `modelUsage`,根本不用自己算**。CodeFlow 实际改动 = 在已有 SDK hook 旁加一个事件 type 监听,把现成数据落盘即可。工作量从 1 dev-day 砍到 ~2 hours。

---

## 0 · 实测发现(写 SPEC 前先跑的考察)

### 0.1 CodeFlow 当前 SDK hook 现状

实测 `D:\Bridgeflow\fcop\logs\thinking\thinking-20260514.jsonl`(34421 行 / 16 MB / Python 解析零失败):

| sdk event_type | 行数 | 状态 |
|---|---|---|
| `thinking` | 21,466 | ✅ 已 hook |
| `assistant` | 9,863 | ✅ 已 hook |
| `tool_call` | 3,092 | ✅ 已 hook |
| **`result`**(含 usage) | **0** | ❌ **未 hook(本 SPEC 要补的就是这个)** |
| `system` / `user` / `tool_result` / `stream_event` | 0 | ❌ 全未 hook(本期不要求,P2 再说) |

> 含 `"usage"` / `"input_tokens"` / `"output_tokens"` 子串的行:**全文 0 命中**。SDK 一定发了,CodeFlow 一定丢了。

### 0.2 SDK 真实 schema(从 Anthropic Claude Agent SDK 官方 TypeScript reference 抄录)

来源:<https://code.claude.com/docs/en/sdk/sdk-typescript> → `SDKResultMessage`

```typescript
type SDKResultMessage =
  | {
      type: "result";
      subtype: "success";              // or "error_max_turns" | "error_during_execution"
      duration_ms: number;             // 整个 agent loop 耗时
      duration_api_ms: number;         // 实际 LLM API 耗时
      is_error: boolean;
      num_turns: number;               // 几轮 tool round-trip
      result: string;                  // 最终输出
      stop_reason: string | null;
      total_cost_usd: number;          // ← SDK 已算好,直接用!
      usage: NonNullableUsage;         // ← input_tokens / output_tokens / cache_*
      modelUsage: { [modelName: string]: ModelUsage };  // ← 按模型拆分
      permission_denials: SDKPermissionDenial[];
    }
  | { ... error 变体,字段类似但无 result 文本 ... };

type Usage = {
  input_tokens: number | null;
  output_tokens: number | null;
  cache_creation_input_tokens: number | null;
  cache_read_input_tokens: number | null;
  server_tool_use: { web_search_requests, web_fetch_requests } | null;
  service_tier: "standard" | "priority" | "batch" | null;
  cache_creation: { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens } | null;
};
```

### 0.3 这意味着什么

- ✅ **不用** pricing.json(SDK 自己有 `total_cost_usd`)
- ✅ **不用** 写 cost 计算逻辑
- ✅ **不用** hook LLM 原始 HTTP 调用
- ✅ **多模型自动分摊**(SDK 给 `modelUsage` 字典)
- ✅ **附带** `num_turns` / `duration_ms` 等富指标

CodeFlow 的活儿就一件:**在已有的 SDK 事件 hook 旁,多 hook 一个 `result` 事件 type,把内容原样写到新文件**。

---

## 1 · 目标

让 CodeFlow 的每一次 agent run **结束时**留下一条 token 消耗记录,使 ADMIN 在 dashboard 看见**实测**(而不是估算):

- 今日总 token / 总 $
- 按 agent_id 排行(PM-01 / DEV-01 / QA-01 / OPS-01 / EVAL-01 谁最贵)
- 按 thread_key 排行 Top-5
- 按 model 排行
- 平均每次 run 的 num_turns / duration_ms

---

## 2 · 数据 Schema(JSONL 单行)

**落位**:`fcop/logs/usage/usage-YYYYMMDD.jsonl`
**写入策略**:append-only,每次 agent run 结束时(即收到 `result` 事件时)追加 1 行,按日切分

```json
{
  "ts": 1778733799999,
  "at": "2026-05-14T16:23:19.999Z",
  "event_type": "sdk.result",
  "agent_id": "PM-01",
  "session_id": "session-1-mp505m2d",
  "payload": {
    "sdk_type": "result",
    "raw": {
      "type": "result",
      "subtype": "success",
      "duration_ms": 18432,
      "duration_api_ms": 12876,
      "is_error": false,
      "num_turns": 5,
      "result": "Sprint-7 后端 4 个 endpoint 已...",
      "stop_reason": "end_turn",
      "total_cost_usd": 0.1432,
      "usage": {
        "input_tokens": 48391,
        "output_tokens": 2841,
        "cache_creation_input_tokens": 5000,
        "cache_read_input_tokens": 12000,
        "service_tier": "standard"
      },
      "modelUsage": {
        "claude-sonnet-4-5-20251022": {
          "inputTokens": 48391,
          "outputTokens": 2841,
          "costUSD": 0.1432
        }
      },
      "agent_id": "agent-6f48aa87-76b0-41e0-abf2-ebbf1e5abc57",
      "run_id": "run-34ce8c85-a169-480f-bab6-a3c680873fa6",
      "task_id": "TASK-20260514-455-PM-to-DEV",
      "thread_key": "sprint-pipeline"
    }
  }
}
```

外层 schema **与 CodeFlow 现有 thinking-*.jsonl 完全一致**(`ts` / `at` / `event_type` / `agent_id` / `session_id` / `payload.sdk_type` / `payload.raw`),只是 `event_type` 改成 `sdk.result` + payload.raw 是 SDK 原样 `SDKResultMessage`。

**额外字段(CodeFlow 注入,非 SDK 原生)**:在 `payload.raw` 里追加:
- `task_id`:agent execution context 里如果有 task,就填(用于 §4 P2 聚合)
- `thread_key`:同上

---

## 3 · 字段必填 / 可选清单

外层字段(CodeFlow envelope,与 thinking 流字段对齐):

| 字段 | 必填? | 备注 |
|---|---|---|
| `ts` / `at` | ✅ | 时间戳,毫秒 + ISO 8601 |
| `event_type` | ✅ | 固定 `sdk.result` |
| `agent_id` | ✅ | CodeFlow agent 名(PM-01 / DEV-01 / ...) |
| `session_id` | ✅ | CodeFlow session(同 thinking) |
| `payload.sdk_type` | ✅ | 固定 `result` |

`payload.raw` 字段(SDK 原样 + CodeFlow 注入):

| 字段 | 必填? | 来源 |
|---|---|---|
| `type` | ✅ | SDK `result` |
| `subtype` | ✅ | SDK `success` / `error_max_turns` / `error_during_execution` |
| `duration_ms` | ✅ | SDK |
| `duration_api_ms` | ✅ | SDK |
| `is_error` | ✅ | SDK |
| `num_turns` | ✅ | SDK |
| `total_cost_usd` | ✅ | SDK |
| `usage.input_tokens` | ✅ | SDK |
| `usage.output_tokens` | ✅ | SDK |
| `usage.cache_creation_input_tokens` | ✅(可为 null) | SDK |
| `usage.cache_read_input_tokens` | ✅(可为 null) | SDK |
| `modelUsage` | ✅ | SDK 整对象原样落盘 |
| `result` | ⏺ | SDK,error 情况下 SDK 自己缺,留空即可 |
| `stop_reason` | ⏺ | SDK |
| `agent_id`(SDK 给的 UUID) | ⏺ | 不是 CodeFlow agent 名,是 SDK 的内部 agent UUID |
| `run_id` | ✅ | SDK,用于和上游 Anthropic Console 对账 |
| **`task_id`** | ⏺ | **CodeFlow 注入**:当前 agent context 里若有 task 就填,**没有就留空,绝不编造**(Rule 0.c) |
| **`thread_key`** | ⏺ | **CodeFlow 注入**:同上 |

---

## 4 · 验收标准

Bridgeflow QA-01 验收逐项核对:

| # | 验收项 | 通过定义 |
|---|---|---|
| **a** | 日切文件存在 | `fcop/logs/usage/usage-20260514.jsonl` 当日所有 agent run 都有 1 条记录 |
| **b** | 落盘性能 | 单条记录写盘 P99 < 50ms(不阻塞 agent 关闭 run) |
| **c** | Schema 完整 | 用 Python 跑 §3 全清单断言,100 条抽检全过 |
| **d** | 对账一致(关键) | 一日总 `total_cost_usd` vs Anthropic Console 当日 spend,误差 < 5% |
| **e** | Dashboard 新增卡片 | "Token 消耗" 卡片显示:今日总 $ / 今日总 input+output tokens / 按 agent 排行 / 按 thread_key Top-5 / 按 model 排行 |
| **f** | 单元测试 | mock 一次 agent run,assert 文件多 1 行 + §3 字段齐全 |
| **g** | 错误路径覆盖 | 当 SDK 返回 `subtype: error_max_turns`,记录依然落盘且 `is_error: true` |

---

## 5 · 与 FCoP 协议的边界

⚠️ usage 数据**不是** FCoP 协议数据。

| 类型 | 位置 | 性质 |
|---|---|---|
| FCoP 协议归档 | `fcop/log/` | append-only,审计链 |
| FCoP 协议工作中 | `fcop/{tasks,reports,issues,reviews}/` | 协议 IPC |
| **运行时事件流(本规格)** | **`fcop/logs/usage/`** | **运行时遥测,非协议数据** |
| 思考流(已存在) | `fcop/logs/thinking/` | 同上 |

具体禁止:

- ❌ **不要**把 result 事件混进 `thinking-*.jsonl`(thinking 是"agent 在想什么",result 是"run 完了花了多少",两件事分开落盘可读性高)
- ❌ **不要**把 usage 写进 `fcop/tasks/` 或 `fcop/reports/`(那是协议数据,运行时遥测不该污染)
- ❌ **不要**每条记录就 git commit(`fcop/logs/` 应在 `.gitignore` 或定期归档)

具体允许:

- ✅ Dashboard 可以读 `fcop/logs/usage/*.jsonl` 做实时聚合显示
- ✅ Bridgeflow 自有的归档脚本可以定期把旧 usage 压缩归档
- ✅ Bridgeflow 可以扩展字段(只要不破坏 §3 必填项)

---

## 6 · 优先级与排期建议

| 优先级 | 范围 | 工时(校准后) |
|---|---|---|
| **P1**(本 sprint) | §2 + §3 落盘 + §4 a/b/c/f/g + §4 e dashboard 基础卡片 | **~2 小时**(SDK 已给数据,只是补 hook) |
| **P2**(下 sprint) | 按 `task_id` 聚合:每个 task 闭合时,自动在 REPORT 末尾加一节 `## Token cost / 本任务 LLM 消耗` | ~1 小时(扫 jsonl 按 task_id group by) |
| **P3**(后续,等 FCoP v1.1+) | 超阈值预警:单 task > 100K tokens 或单 thread_key > $1 时,触发 Rule 9.3 `DRIFT` failure → 自动写 ISSUE 给 ADMIN | ~3 小时(等 fcop 包暴露 `report_failure` Python API 到 TypeScript 桥) |

---

## 7 · 反模式(不要做的)

| 反模式 | 为什么不行 | 正确做法 |
|---|---|---|
| 自己 hook LLM 原始 HTTP 调用 | SDK 已经聚合好了 | hook `result` 事件 |
| 自己用 pricing.json 算 cost | SDK 自带 `total_cost_usd`,价格变化跟随 SDK | 直接读 SDK 字段 |
| 用 SQLite/Postgres | JSONL 已够,运维负担更轻 | JSONL append |
| 不记 `run_id` | 无法和 Anthropic Console 对账 | 必填 |
| 一次 run 拆成多条 | 难做求和,审计困难 | 一次 run = 一条 JSONL |
| 把 prompt 内容也写进 usage 流 | usage 应当瘦 | 只记 metric,正文留 thinking 流 |
| 跨日聚合后**删原始 JSONL** | 失去对账能力 | 归档但不删 |

---

## 8 · 给 PM 的执行提示

### Hook 点(就在现有 SDK hook 旁加一个 type)

CodeFlow 当前 hook 看 thinking-*.jsonl 的 schema,实现里大概是这样的逻辑:

```typescript
// 现有(伪代码,从 jsonl schema 反推)
for await (const msg of agentSDK.query(...)) {
  switch (msg.type) {
    case 'thinking': appendToFile('thinking', { ...envelope, payload: { sdk_type: 'thinking', raw: msg } }); break;
    case 'assistant': appendToFile('thinking', { ...envelope, payload: { sdk_type: 'assistant', raw: msg } }); break;
    case 'tool_call': appendToFile('thinking', { ...envelope, payload: { sdk_type: 'tool_call', raw: msg } }); break;
    // ← 这里漏了:
  }
}
```

要加的就是:

```typescript
    case 'result':
      appendToFile('usage', {  // ← 注意:写到 usage-*.jsonl,不是 thinking-*.jsonl
        ...envelope,
        event_type: 'sdk.result',
        payload: {
          sdk_type: 'result',
          raw: {
            ...msg,
            task_id: currentContext.taskId ?? null,
            thread_key: currentContext.threadKey ?? null,
          },
        },
      });
      break;
```

### Dashboard 聚合(SQL-like JS,跑在前端或后端皆可)

```javascript
const lines = readAllLines('fcop/logs/usage/usage-20260514.jsonl');
const events = lines.map(l => JSON.parse(l));

// 今日总消耗
const total_cost = events.reduce((s, e) => s + e.payload.raw.total_cost_usd, 0);
const total_input = events.reduce((s, e) => s + (e.payload.raw.usage.input_tokens ?? 0), 0);
const total_output = events.reduce((s, e) => s + (e.payload.raw.usage.output_tokens ?? 0), 0);

// 按 agent 排行
const byAgent = groupBy(events, e => e.agent_id);
// 按 thread_key 排行(可能为空,需 fallback)
const byThread = groupBy(events, e => e.payload.raw.thread_key ?? '(no thread)');
// 按 model 排行(用 modelUsage)
const byModel = {};
for (const e of events) {
  for (const [m, u] of Object.entries(e.payload.raw.modelUsage ?? {})) {
    byModel[m] ??= { input: 0, output: 0, cost: 0 };
    byModel[m].cost += u.costUSD ?? 0;
  }
}
```

### 注意 `task_id` / `thread_key` 怎么拿到

CodeFlow agent 在执行 task 时,上下文里已经有 task_id(否则它没法写 report)。把这两个字段从 agent runtime context 透传给 SDK hook 即可。**拿不到就留 `null`,绝不编造**(Rule 0.c)。

### Anthropic Console 对账方法

每条记录有 `run_id`(SDK 给的)和 `usage.input_tokens` / `output_tokens`。Anthropic Console 的 Usage 页面也按 day 聚合 token,**两边 sum 起来应该对得上(误差 < 5%,因为时区/聚合窗口可能差)**。

> 实测建议:跑通 hook 后,**先空跑半天**(只落盘,不暴露 dashboard),拿当晚 Anthropic Console 数字对账一次,确认 schema 没漏字段后再 ship。

---

## 9 · 工时一览(供 PM 报 sprint)

| 改动 | 文件 | 工时 |
|---|---|---|
| 1. SDK hook 多 case 'result' | 现有 hook 文件 +1 case | 20 min |
| 2. 新写 usage-writer(`fcop/logs/usage/` 日切) | 1 个新文件,~30 行 | 20 min |
| 3. 透传 task_id / thread_key 到 SDK hook context | 1-2 处插桩 | 30 min |
| 4. Dashboard "Token 消耗" 卡片 | 1 个新组件 + 1 个聚合接口 | 30 min |
| 5. 单元测试(mock SDK + 文件断言) | 1 个 test 文件 | 20 min |
| 6. QA 全清单验收 + Anthropic Console 对账 | QA-01 | 30 min |
| **P1 小计** | | **≈ 2.5 小时** |

---

## 10 · 反馈通道

Bridgeflow PM-01 / DEV-01 实施中发现本 SPEC 有空白、矛盾、不可实施处:

- **不要**自行偏离 SPEC(那会让 Bridgeflow 与未来其他 CodeFlow 实例不一致)
- 用 FCoP `inbox/outbox` 机制反馈回 `D:\FCoP`,或 ADMIN 转告
- ME 在 FCoP 总部一侧追加 SPEC v1.2,Bridgeflow 再按新版改

---

## Changelog

- **v1.0**(初稿,已废弃):误以为要自己 hook LLM + 用 pricing.json 算 cost,估 1 dev-day
- **v1.1**(2026-05-14):实测 thinking-20260514.jsonl + 抄录 Anthropic Claude Agent SDK 官方 schema 后**重写**——确认 SDK 已自带 `SDKResultMessage` 含 `total_cost_usd` + `usage` + `modelUsage`,**改动核心是补 hook,工时砍到 ~2.5 小时**

---

**Spec status**: draft v1.1(已用实测数据校准)
**Author**: FCoP HQ / ME
**Date**: 2026-05-14
**Signed off by**: ADMIN(在 chat 转给 PM-01 时即视为签字)
