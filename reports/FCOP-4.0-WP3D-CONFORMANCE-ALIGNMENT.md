# FCoP 4.0 WP3D v1.1 Conformance Alignment

## 冻结目标

```yaml
COLLECTED_V4_NODES: 119
FROZEN_TEST_IDS: 60/60
WP3D_TARGET_NODES_BEFORE: 0/15
WP3D_TARGET_NODES_AFTER: 15/15
V4_STATIC_META: 27/27
V4_BEHAVIORAL: 69 passed / 23 deferred / 0 unexpected
V4_TOTAL: 96 passed / 23 deferred
FROZEN_CONFORMANCE_FILES_MODIFIED: 0
```

15 个节点逐项覆盖 C3 完整生命周期与 T7 Gate、C5 canonical digest/收敛/终态/陈旧证据/真实 REPORT 竞态、C6 五类授权拒绝，以及 C8 T7 丢响应重试。另行复核 `C5-FAMILY-RACE-01`、`C8-X02`、`AT-02`、`C6-SPOOF-01` 为 4/4。

## Deferred 精确映射

23 项仍红是任务书明示的后续能力，不是本轮回归：

- C3-X01 cold export：1；
- C4-R01 dangling gate reference：1；
- C6-X01 公共 fault injection：1；
- C7-CREATE-01 非 create 外部幂等边界：1；
- C8-X01 公共 fault stages：4；
- C8-X03 公共 recovery：3；
- C8-STATE-01：5；
- C8-INDETERMINATE-01：1；
- AT-05 公共 fault stages：3；
- AT-06 公共 recovery：3。

合计 23。没有实现或伪造 `inject_fault`、`recover_operation`、cold export 或 WP3E 行为。

## 回归与质量

| 检查 | 结果 |
|---|---|
| WP3D 新增测试 `test_v4_convergence.py` | 23 passed |
| 全部 v4 单元（`tests/test_fcop -k v4`） | 210 passed（最终组成：此前 209 + 新增竞态 1） |
| v3/非 v4 行为（排除 public snapshot） | 907 passed |
| MCP，绑定 `PYTHONPATH=mcp/src;src` | 80 passed |
| MyPy（10 个生产模块） | PASS |
| Ruff（授权源码/测试） | PASS |
| `git diff --check` | PASS |
| UTF-8/LF/BOM | PASS |

`tests/test_fcop` 的 public-surface snapshot 会准确报告一个新增的 `Project.family_digest(*, root_task_id) -> str` 条目。该变化正是任务书唯一授权的新公共 API，但 `tests/test_fcop/snapshots/public_surface.json` 不在允许写集，故未越权改写 snapshot；除这一预期、可解释的冻结快照差异外，测试组成全部通过。

冻结中英文规范与提交 `aec4c2b...` 的 Git blob 完全一致；Schema、MCP 实现、Conformance、依赖和 CodeFlowMu 均无变更。
