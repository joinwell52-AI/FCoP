# FCoP 4.0 WP3C Conformance Alignment

## 1. 目标结果

```yaml
WP3C_TARGET_NODES: 33/33
BASELINE_PASS: 14
BASELINE_EXPECTED_FAIL: 19
BASELINE_UNEXPECTED_FAIL: 0
FINAL_TARGET_PASS: 33
FROZEN_TEST_IDS: 60/60
V4_COLLECT_ONLY: 119
V4_STATIC_META: 27/27
V4_TOTAL: 81 passed / 38 deferred
UNEXPECTED_FAILURES: 0
SKIP_OR_XFAIL_ADDED: 0
```

目标 33 节点包括 C3 的 T4/T5/T6 生命周期节点 4 个、C6 信任/绑定/消费节点 12 个、C8 retry 节点 3 个，以及 WP2.1b Profile 边界 Meta 节点 14 个。编码前为 14 pass / 19 expected fail；编码后全部通过。

## 2. Conformance 夹具修正

| 文件 | 修正 | 合同理由 |
|---|---|---|
| `fixtures.py` | 新增 `bind_t3()` | review 阶段的 T4/T5 fixture 必须真实存在最近 T3 对当前 REPORT 字节的绑定 |
| `test_c3_lifecycle.py` | C3-N01、C3-N02、T4/T5/T6 Gate 使用可信初始化 registry 和真实授权事实 | 让组合流程越过已实现 T4/T6，仍在未授权 T7 停止 |
| `test_c6_authorization.py` | Profile 三态、smuggling、expiry/retry 和 digest 节点接入可信 driver；精确重试断言 Existing | 冻结 F4.9.11 要求 response-loss 精确重试返回既有结果，不把它误判为 reuse |
| `test_c8_recovery.py` | T4/T5/T6 使用真实 T3/授权；response loss 在生产提交返回后由调用端模拟丢失；异边复用选 WP3C 内合法边 | 不用 `parallel_surface_probe` 或公共 fault stub 冒充实际操作 |

没有更改 60 个 Test ID，没有删除行为断言，没有增加 skip/xfail，也没有让 driver 截获生产错误。

## 3. 38 个 deferred 节点逐项处置

| # | 节点 | 明确原因 |
|---:|---|---|
| 1 | `C3-N01` | T1–T6 已执行成功，最终 T7 `done→archive` 按 WP3C 边界返回未实现 |
| 2 | `C3-X01` | 需要未授权的 cold export 与公共 fault injection |
| 3 | `C3-GATE-01[T7]` | T7 Gate 属于 WP3D |
| 4 | `C4-R01[dangling-gate-reference]` | `references_required_by_gate` 创建面语义为继承失败，WP3C 不改 C4 创建合同 |
| 5 | `C5-N02` | 需要 convergence REVIEW、family digest 与 Root T7 |
| 6 | `C5-R03` | 需要 stale convergence 判定 |
| 7 | `C5-X01` | 需要并发 stale convergence 判定 |
| 8 | `C5-BRANCH-01` | 需要 Branch 终态门 |
| 9 | `C5-ARCHIVED-01` | 需要 T7 后 archive/cold export 行为 |
| 10 | `C5-FAMILY-DIGEST-01` | family_digest 尚未获授权实现 |
| 11 | `C5-REPORT-RACE-01` | 需要 REPORT 变化驱动 convergence/family digest 失效 |
| 12 | `C6-R01[missing]` | 节点构造 T7，WP3C 明确保留 T7 未实现 |
| 13 | `C6-R01[actor-admin-only]` | 节点构造 T7；WP3C 已另以 T4/T5/T6 测试证明 actor 不授权 |
| 14 | `C6-R01[wrong-subject]` | 节点构造 T7；WP3C 新单测已覆盖受控边 subject 绑定 |
| 15 | `C6-R01[wrong-edge]` | 节点构造 T7；WP3C 新单测已覆盖受控边 edge 绑定 |
| 16 | `C6-R01[wrong-attempt]` | 节点构造 T7；WP3C 新单测已覆盖受控边 attempt 绑定 |
| 17 | `C6-X01` | 需要 T7 的授权中断/恢复和公共 fault injection |
| 18 | `C7-CREATE-01` | 继承节点要求第二次 T2 拒绝，而 WP3B durable receipt 返回 Existing；非 WP3C 授权范围且未由本轮引入 |
| 19 | `C8-X01[PREPARED]` | 需要公共 fault injection/recovery API |
| 20 | `C8-X01[TARGET_DURABLE]` | 需要公共 fault injection/recovery API |
| 21 | `C8-X01[COMMITTED]` | 需要公共 fault injection/recovery API |
| 22 | `C8-X01[RESPONSE_LOST]` | 需要公共 fault injection/recovery API |
| 23 | `C8-X03[divergent]` | 需要公共 recover_operation 处理 divergent 双副本 |
| 24 | `C8-X03[corrupt-receipt]` | 需要公共 recover_operation 处理损坏 receipt |
| 25 | `C8-X03[unsupported-filesystem]` | 需要公共 recover_operation 的文件系统分支 |
| 26 | `C8-RETRY-01[T7]` | T7 retry 属于 WP3D |
| 27 | `C8-STATE-01[S1]` | 五状态公共 recovery 表面尚未授权 |
| 28 | `C8-STATE-01[S2]` | 五状态公共 recovery 表面尚未授权 |
| 29 | `C8-STATE-01[S3]` | 五状态公共 recovery 表面尚未授权 |
| 30 | `C8-STATE-01[S4]` | 五状态公共 recovery 表面尚未授权 |
| 31 | `C8-STATE-01[S5]` | 五状态公共 recovery 表面尚未授权 |
| 32 | `C8-INDETERMINATE-01` | 需要公共 recovery 的 indeterminate 分支 |
| 33 | `AT-05[PREPARED]` | 需要公共 fault injection |
| 34 | `AT-05[TARGET_DURABLE]` | 需要公共 fault injection |
| 35 | `AT-05[RESPONSE_LOST]` | 需要公共 fault injection |
| 36 | `AT-06[S2]` | 需要公共 recover_operation |
| 37 | `AT-06[S4]` | 需要公共 recover_operation |
| 38 | `AT-06[S5]` | 需要公共 recover_operation |

## 4. 验证结果

| 检查 | 结果 |
|---|---|
| WP3C 新增单元 | 36 passed |
| WP3B lifecycle 单元 | 47 passed |
| WP3A creation 单元 | 94 passed |
| WP3C 精确目标 | 33 passed |
| 完整 v4 | 81 passed / 38 deferred / 0 unexpected |
| `tests/test_fcop` | 1085 passed |
| 绑定 `PYTHONPATH=mcp/src;src` 非-Conformance | 1402 passed / 2 inherited skips |
| 隔离 MCP | 80 passed |
| v4 static/meta | 27 passed |
| collect-only | 119 collected |

两项 skip 是迁移后不存在 `docs/agents/log` 的既有 legacy fixture 分支；本轮没有新增 skip。
