# FCoP 4.0 WP3D Implementation Plan

## 1. 计划状态

```yaml
PLAN_STATUS: SUSPENDED_BEFORE_PRODUCTION_EDIT
STOP_CODE: FROZEN_CONFORMANCE_CONTRACT_CONFLICT
PRODUCTION_FILES_MODIFIED: 0
CONFORMANCE_FILES_MODIFIED: 0
```

本计划证明任务书给定的文件范围和复杂度预算原则上足够，但在进入编码前发现冻结测试夹具与冻结授权合同冲突，因此没有执行以下生产改动。

## 2. 原定最小实现切分

1. `src/fcop/v4/convergence.py`
   - 唯一实现 family 扫描、current REPORT head、canonical object/bytes/digest；
   - 验证 convergence REVIEW 的 references 与 digest；
   - 输出纯结果，不拥有锁、数据库或后台状态。
2. `src/fcop/v4/creation.py`
   - convergence REVIEW 写入接入既有 Root-family lock；
   - 锁内调用同一 canonical 实现，拒绝陈旧或混合快照。
3. `src/fcop/v4/lifecycle.py`
   - 在现有 transition 状态机中启用 T7；
   - 三类 subject 共享入口，在同一 family lock 内应用不同证据门；
   - 继续复用三阶段提交、event 与恢复路径。
4. `src/fcop/v4/authorization.py`
   - 将 T7 纳入现有可信 Profile、single-use、expiry 和 family-digest 绑定验证；
   - 不建立默认 Profile，不允许请求或 manifest 产生信任。
5. `src/fcop/v4/receipts.py`
   - 将 T7 加入既有 receipt identity；Root-with-Branches 额外绑定 family/convergence evidence digest；
   - exact retry 返回 Existing，异操作复用保持 `AUTHORIZATION_REUSED`。
6. `src/fcop/v4/linearization.py`
   - 只在必要时修正既有 family lock 的接线，不新增锁目录或锁实现。
7. `src/fcop/project.py` 与 `src/fcop/v4/boundary.py`
   - 仅公开任务书唯一授权的 `Project.family_digest(*, root_task_id)`，维持版本闭集和实例签名。

## 3. 原定验证顺序

1. 保留 15 个冻结目标节点的真实红灯基线；
2. 添加任务书允许的 v4 单元测试，覆盖 digest oracle、replacement、convergence、三类 T7、Authorization、receipt/recovery 和真实跨进程 race；
3. 先跑目标 15 节点，再跑 WP3C 回归；
4. 跑 `tests/test_fcop`、v3、MCP、v4 Static/Meta、完整 Behavioral 与 collect-only；
5. 仅在全部合同同时成立时创建 Content Commit 和只含 Manifest 的第二提交。

## 4. 编码前阻断

冻结规范 F4.7.4 规定：T4/T5/T6/T7 没有可用且已采用的可信授权 Profile 时，必须返回 `AUTHORIZATION_PROFILE_UNAVAILABLE`；只有可信初始化边界注册的 evaluator 返回 `AUTHORIZED` 才能通过。

默认冻结夹具 `tests/conformance/v4/conftest.py:23-25` 构造 `V4ConformanceDriver(workspace.root)`。driver 在没有 `trusted_profiles` 时于 `tests/conformance/v4/driver.py:171-172` 构造 `Project(root)`；生产构造函数在 `src/fcop/project.py:237` 将其归一为空注册表。

然而 3 个成功节点使用该默认 driver 执行 T7：

- `C3-GATE-01[T7]`：`tests/conformance/v4/test_c3_lifecycle.py:279-288` 只为 T4/T5/T6 构造可信 driver，T7 走默认 driver；
- `C5-N02`：`tests/conformance/v4/test_c5_convergence.py:64-88` 直接用默认 driver 成功归档 Root；
- `C5-ARCHIVED-01`：`tests/conformance/v4/test_c5_convergence.py:213-231` 直接用默认 driver 成功归档 Branch。

如果生产实现为了让这些节点通过而跳过 T7 evaluator，或因 manifest 中出现 `profile:test` 就自动授权，将违反 F4.7.4，并破坏已验收的 WP3C/WP2.1b 信任边界。任务书第 11.1 节又冻结 `tests/conformance/v4/**`，要求证明冲突后停止并请求单独授权。

## 5. 继续实施所需的最小外部裁定

需要一个独立、明确授权的冻结夹具修订，使所有预期成功的 T7 节点通过可信 `Project/Toolkit` 初始化边界注册确定性 Profile evaluator；业务请求仍只携带 `profile_ref`/`authorization_ref`，不得携带 evaluator。还应同时明确 C6 T7 rejection 节点在“无可信 Profile”与“缺失/错误 authorization”并存时的错误优先级。

在该裁定前，生产实施保持未开始。
