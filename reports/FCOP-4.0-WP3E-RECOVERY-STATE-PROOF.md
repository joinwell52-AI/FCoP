# FCoP 4.0 WP3E · Recovery State Proof

## 单一分类链

公共 `Project.recover_operation(...)` 由 Project version boundary 路由到唯一新增
薄模块 `src/fcop/v4/recovery.py`。该模块只完成：

1. 将 source、target、receipt 规范化到当前 workspace；
2. 验证相同 TASK ID、合法 Base lifecycle edge 与可见 v4 TASK；
3. 将 compact observation receipt 或完整 lifecycle receipt 归一为同一内存证据；
4. 调用既有 `src/fcop/v4/receipts.py::classify()`；
5. 只对 S2/S3 执行既有 durable receipt/source 原语。

没有第二分类器、第二 receipt、第二 operations 目录或业务裁决器。恢复不创建
REVIEW、不追加 transition/event，不依据 mtime、目录顺序或“较新副本”猜测 NOW。

## 五状态结果

| 状态 | 分类 | 机械动作 | 结果 |
|---|---|---|---|
| S1 | `NOT_COMMITTED` | 保留 source，不创建 target | PASS |
| S2 | `RECOVERABLE_DUPLICATE` | 字节/摘要验证后删除 source，receipt→COMMITTED | PASS |
| S3 | `COMMITTED` | 保留唯一 target，只补全 receipt | PASS |
| S4 | `DIVERGENT_DUPLICATE` | 保留两份证据，返回 `RECOVERY_REQUIRED` | PASS |
| S5 | `INDETERMINATE` | 不猜测、不重建，返回 `RECOVERY_REQUIRED` | PASS |

compact 与完整 receipt 均通过同一 `classify()`。单元测试覆盖五行正例、重复
S4/S5、完整 receipt、不同 TASK、非法边、receipt 越界、operation mismatch、
path traversal、symlink escape、network filesystem 零写入，以及 S2/S3 不追加
event。冻结 C8/AT 节点全部通过。

```yaml
RECOVERY_STATE_TABLE: 5/5
RECOVERY_RECEIPT_IMPLEMENTATIONS: 1
UNSUPPORTED_FILESYSTEM_ZERO_WRITE: PASS
PATH_BOUNDARY: PASS
LINUX_NATIVE: NOT_NATIVE_VERIFIED
MACOS_NATIVE: NOT_NATIVE_VERIFIED
```
