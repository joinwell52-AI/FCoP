# FCoP 4.0 WP3E.0 · C6-X01 可信 Profile 夹具对齐

## 裁定

`C6-X01` 已按任务书唯一例外改为测试内局部可信初始化。修改仅位于
`tests/conformance/v4/test_c6_authorization.py::test_c6_x01`：构造
`V4ConformanceDriver(workspace.root, trusted_profiles={"profile:test":
DeterministicProfileEvaluator("AUTHORIZED")}, test_id="C6-X01")`，并让该测试的
fault 注册、首次 T7 和精确重试使用此局部 driver。

业务请求仍只携带 `authorization_ref` 等数据引用，没有 evaluator、resolver、
registry 或裁定结果。默认 `v4_driver` fixture、全局 driver、Authorization
生产实现、Test ID、clause、请求、故障阶段和所有断言均未修改。

## 验证

修改前，`C6-X01` 的最早红灯是 `inject_fault=absent`。静态读取同时证明默认
fixture 通过 `V4ConformanceDriver(workspace.root)` 构造，可信 registry 为空。

夹具对齐后、阶段 B 实现前，整个 `test_c6_authorization.py` 为
`17 passed / 1 failed`；唯一失败仍是 `C6-X01` 的
`V4_NOT_IMPLEMENTED(inject_fault)`，不再是 Profile unavailable。阶段 B 完成后
该文件 18 项全部通过，且完整 v4 Behavioral 为 92/92。

```yaml
C6_X01_TRUSTED_PROJECT_INITIALIZATION: PASS
CALLER_AUTHORITY_FIELDS_ADDED: 0
GLOBAL_V4_DRIVER_MODIFIED: false
TEST_ID_RENAMED: 0
ASSERTIONS_REMOVED: 0
SKIP_XFAIL_ADDED: 0
OTHER_CONFORMANCE_FILES_MODIFIED: 0
```
