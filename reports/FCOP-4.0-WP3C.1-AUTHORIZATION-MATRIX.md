# FCoP 4.0 WP3C.1 Authorization Carrier Matrix

## 1. 结论

WP3C.1 将 `authorization_ref` 的载体规则实现为显式封闭矩阵。REVIEW 中出现 `profile_ref`、`issuer_proof`、`decision` 或其他授权字段，不会使该 REVIEW 自动获得跨边授权能力。

| REVIEW `review_kind` | 必须的 `decision` | T4 `review → done` | T5 `review → active` | T6 `done → active` |
|---|---|---:|---:|---:|
| `authorization` | `authorize` | 允许 | 允许 | 允许 |
| `acceptance` | `approved` | 允许 | 拒绝 | 拒绝 |
| `rejection` | `rejected` | 拒绝 | 允许 | 拒绝 |
| `reopen` | 任意 | 拒绝 | 拒绝 | 拒绝 |

矩阵外的类型、边或 decision 组合统一返回结构化错误 `AUTHORIZATION_INVALID`，并在 receipt、TASK、REVIEW 或事件写入前失败。

## 2. T6 的证据与授权分离

- `reopen + approved` 可以作为 T6 的 `review_ref` 证据，但不能作为 `authorization_ref`。
- T6 使用 reopen 证据时，必须另外提供 `authorization + authorize` REVIEW。
- `authorization + authorize` 也可以同时作为 T6 的 `review_ref` 与 `authorization_ref`。

因此，业务请求中的“证据引用”和“授权载体”仍是两个独立角色；只有冻结合同明确允许的载体才可兼任。

## 3. 实现位置

- `src/fcop/v4/authorization.py` 中的私有 `_AUTHORIZATION_CARRIERS` 是唯一载体矩阵。
- `validate_gate()` 在解析不可变 REVIEW 后，同时校验 `review_kind`、生命周期边和 `decision`。
- 未新增公共 API、公共参数、错误码或权威存储。

## 4. 定点测试

| ID | 生产入口场景 | 结果 |
|---|---|---|
| WP3C1-KIND-01 | T6 用 reopen 同时作 evidence 与 authorization | `AUTHORIZATION_INVALID`；树快照零变化 |
| WP3C1-KIND-02 | T5 用 acceptance 作 authorization | `AUTHORIZATION_INVALID`；树快照零变化 |
| WP3C1-KIND-03 | T4 用 rejection 作 authorization | `AUTHORIZATION_INVALID`；树快照零变化 |
| WP3C1-KIND-04 | T6 用 reopen evidence 与独立 authorization | 成功，event 分别绑定两个引用 |
| WP3C1-REG-01 | T4 acceptance 兼任 authorization | 成功 |
| WP3C1-REG-02 | T5 rejection 兼任 authorization | 成功 |
| WP3C1-REG-03 | T6 authorization 兼任 evidence | 成功 |

上述测试均直接调用生产 `Project.transition()`，没有通过 driver 或辅助探针代替业务行为。

## 5. 冻结 Conformance 观察

冻结 `C3-GATE-01[T6]` fixture 仍把 `reopen` REVIEW 同时传为 `review_ref` 和 `authorization_ref`。WP3C.1 明确要求该组合拒绝，同时禁止修改冻结 Conformance，因此完整 v4 运行中该节点由原先通过变为预期红灯。合法的两条 T6 路径已由 WP3C1-KIND-04 与 WP3C1-REG-03 证明通过；冻结 Test ID 仍为 60/60，文件未修改。该节点单独列为“任务书修正后的预期红灯”，不是实现回退或意外失败。
