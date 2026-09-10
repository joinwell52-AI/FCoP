# FCoP 4.0 WP3E · Implementability 与红灯基线

## 固定输入

```yaml
AUTHORIZED_SCOPE: WP3E_0_ONLY
TASKBOOK_COMMIT: c36995057b038592e51e5769ffb9e54c858ad666
TASKBOOK_SHA256: 0a3f82195ae1a5d9702095c9cf59e5ce1709ce498b44ac4e0a95752c216e0381
ORIGINAL_WP3E_TASKBOOK_COMMIT: 19285e5a22142c3e0331803f85b1776b533d9339
WP3D_GATE_COMMIT: 99d0ab14a8e4e3b5d8580230a9df1d6dbec50b41
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
WORKTREE: D:\FCoP-wp3e0-c6-alignment-resume
BRANCH: review/fcop-4.0-wp3e.0-core-closeout
```

Git blob SHA-256 通过 Git Bash 原生字节管道复核；任务书提交的直接父提交为原
WP3E Taskbook Commit，WP3D Gate 与冻结合同均为祖先。原 `D:\FCoP` 的修改与
未跟踪文件完整保留，没有切分支、stash、reset、clean 或覆盖。

## 编码前事实

```yaml
V4_COLLECT_ONLY: 119
V4_STATIC_META: 27 passed
V4_BASELINE: 96 passed / 23 expected failed
FROZEN_TEST_IDS: 60/60
UNEXPECTED_BASELINE_FAILURES: 0
```

23 个节点严格对应原 WP3E 十组：`C3-X01` 1、C4 dangling Gate reference 1、
`C6-X01` 1、`C7-CREATE-01` 1、`C8-X01` 4、`C8-X03` 3、
`C8-STATE-01` 5、`C8-INDETERMINATE-01` 1、`AT-05` 3、`AT-06` 3。

WP3E.0 已将 `C6-X01` 的可信 Profile 夹具冲突局部关闭。现有
`src/fcop/v4/receipts.py` 已提供唯一 lifecycle receipt validator、唯一
`classify()` 五状态分类器和三阶段 durable receipt；因此公共恢复只需一个薄
机械适配模块，不需要第二 journal、状态机、NOW truth、锁或持久目录。

```yaml
IMPLEMENTABLE_WITHIN_TASKBOOK: true
RECOVERY_RECEIPT_IMPLEMENTATIONS: 1
NEW_PUBLIC_APIS_REQUIRED: 3
NEW_PRODUCTION_MODULES_REQUIRED: 1
NEW_RUNTIME_DEPENDENCIES: 0
NEW_BACKGROUND_COMPONENTS: 0
NEW_AUTHORITATIVE_STORES: 0
NEW_STATE_MACHINES: 0
NEW_LOCK_SYSTEMS: 0
NEW_BASE_ERROR_CODES: 0
```
