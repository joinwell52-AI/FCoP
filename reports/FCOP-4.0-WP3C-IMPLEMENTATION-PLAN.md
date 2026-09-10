# FCoP 4.0 WP3C Implementation Plan

## 1. 执行现场

```yaml
WORKTREE: D:/FCoP-wp3c-authorization
BRANCH: review/fcop-4.0-wp3c-authorization-transitions
START_HEAD: 46c7d7522f020e85ad658a9e0147578d61fe908a
WORKTREE_BASELINE: CLEAN
ORIGINAL_D_FCOP: DIRTY_PRESERVED
TASKBOOK_SHA256: 9574b070cc9e850004954e9e5b1d3516c4f73bcaa5ea335da6dd226d31ff1340
COLLECT_ONLY: 119 tests collected
```

## 2. WP3C 目标节点

`WP3C_TARGET_NODE_IDS` 共 33 个：

- C3：`C3-N02`、`C3-GATE-01[T4]`、`[T5]`、`[T6]`。
- C6：`C6-N01`；Profile evaluator `DENIED`、`UNKNOWN`；caller-smuggling 四个参数节点；`C6-R02[expired]`、`[reused]`；`C6-PROFILE-01`、`C6-SPOOF-01`、`C6-DIGEST-01`。
- C8：`C8-RETRY-01[T4]`、`[T5]`、`[T6]`。
- WP2.1b Meta：registry 初始化边界 1 个、caller authority 四字段 × 三业务入口 12 个、生产业务签名 1 个。

`C6-R01` 当前五个参数节点全部只构造 T7 `done→archive`，不属于 WP3C，不列为转绿目标。将在新增定向单元测试中覆盖 T4/T5/T6 的 subject、edge、attempt、kind、decision、scope、profile 绑定错误。

## 3. 编码前基线

命令：

```text
python -m pytest -q <上述 C3/C6/C8 精确节点> tests/conformance/v4/test_meta_profile_boundary.py
```

```yaml
BASELINE_PASS: 14
BASELINE_EXPECTED_FAIL: 19
BASELINE_UNEXPECTED_FAIL: 0
```

14 个通过节点全部是 WP2.1b 的静态/Meta 信任边界。19 个预期失败分别为 C3 4 个、C6 12 个、C8 3 个；根因是代码基线只开放 T2/T3、registry 未接入 `_Creation`、现有事务未开放 response-loss 测试边界。

## 4. 最小实现切片

1. `src/fcop/project.py`：只把构造时冻结的 trusted registry 传给 `_Creation.open_if_declared/create`，不改变 v3 签名或行为。
2. `src/fcop/v4/creation.py`：私有上下文持有只读 registry；扩展所有业务请求的调用者裁判拒绝清单；不新增公共 API。
3. `src/fcop/v4/authorization.py`：唯一允许的新生产模块；以纯验证函数解析 REVIEW、检查 evidence、执行 evaluator、扫描 transition 消费事实，并返回不可变验证结果。
4. `src/fcop/v4/lifecycle.py`：把 T4/T5/T6 纳入现有 family lock；在锁内形成 event 与 receipt；T5/T6 分配新 attempt；T7 继续结构化未实现。
5. `src/fcop/v4/receipts.py`：保持既有 T2/T3 receipt 可验证；仅为 T4/T5/T6 增加严格的授权/证据/source-target attempt 字段与请求摘要验证。
6. 测试：新增 `tests/test_fcop/test_v4_authorization.py`，扩展 `test_v4_lifecycle.py`；仅当冻结夹具无法表达规范时才最小修正允许的 conformance fixture/节点。

## 5. 不变量与停止条件

- 每个失败验证发生在任何写入前。
- receipt、目标 TASK、source 删除仍按 WP3B 三阶段顺序；不覆盖目标。
- T2/T3 和 v3 全部既有通过节点不得回退。
- 不改变冻结规范、Schema、31 个错误码、MCP、CodeFlowMu、依赖、main 或发布内容。
- 不实现 T7、family digest、convergence 或 Branch terminal gate。
- 若冻结恢复表不能表示 T4/T5/T6 的真实物理崩溃窗口，则停止并报告 `BLOCKED`；不得改合同。

## 6. 验证顺序

按任务书 §14 顺序执行新增单元、v4 lifecycle/creation、C3/C6/C8 定向、全 v4、`tests/test_fcop`、正确 PYTHONPATH 的 v3、隔离 MCP、type/lint/diff、范围与冻结哈希、smoke、Windows 并发/response-loss。只有全部 WP3C 目标通过且无意外回归，才创建 Content Commit；Manifest 必须作为第二个独立提交。
