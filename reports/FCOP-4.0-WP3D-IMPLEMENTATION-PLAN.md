# FCoP 4.0 WP3D v1.1 Implementation Plan

## 状态与边界

```yaml
PLAN_STATUS: READY_AFTER_RED_BASELINE
AUTHORIZED_SCOPE: WP3D_ONLY
FROZEN_CONFORMANCE_MUTATION: FORBIDDEN
PUBLIC_RECOVERY_OR_COLD_EXPORT: OUT_OF_SCOPE
```

## 最小实现切分

1. `src/fcop/v4/convergence.py`：family 扫描、当前 head、canonical object/digest、convergence 请求与存量 REVIEW 校验。
2. `src/fcop/v4/creation.py`：增加 `family_digest` handler；仅对 convergence REVIEW 接入 Root family lock 并在锁内重算验证，其他 REVIEW 行为保持不变。
3. `src/fcop/v4/lifecycle.py`：启用 T7；普通、Branch、带 Branch Root 共享既有 transition/receipt 路径，并按 family 门优先级生成 evidence。
4. `src/fcop/v4/authorization.py`：把 done→archive 纳入可信 Profile、过期、single-use、attempt/edge/subject 与 family-digest 绑定；不引入默认信任。
5. `src/fcop/v4/receipts.py`：在既有 receipt schema 中加入 T7 与可空 `family_digest`，保持三阶段恢复和 exact retry。
6. `src/fcop/project.py`、`src/fcop/v4/boundary.py`：只增加任务书授权的 `Project.family_digest` 公共读取面及显式版本策略。
7. `src/fcop/v4/linearization.py`：只有发现既有 family lock 接线缺口时才改；不新增锁实现。

## 单元测试计划

在任务书允许的四个 `tests/test_fcop/test_v4_*.py` 文件中覆盖：canonical digest 独立 oracle、Unicode 排序、mtime/路径无关、replacement 改变摘要；Root/Branch/普通 T7；T7 Authorization 的绑定、过期与 single-use；response-loss retry、异迁移复用和真实跨进程 race。

不修改 `tests/conformance/v4/**`。

## 验证与交付顺序

1. 15 个固定节点达到 15/15；
2. 运行新增单元测试与 WP3C 回归；
3. 运行 `tests/test_fcop`、v3、MCP、v4 Static/Meta、完整 Behavioral、collect-only；
4. 检查冻结文件 SHA、允许文件集、复杂度预算；
5. Content Commit；
6. Manifest-only Commit；
7. push、重新 fetch、核验远端 HEAD/祖先链/全部 SHA-256；
8. 停止并请求 `WP3D_CONVERGENCE_ACCEPTED`。

若实现需要修改冻结文件、增加错误码/依赖/公共 API、建立第二权威存储，或既有 lock/receipt 无法覆盖真实窗口，则停止为 BLOCKED。
