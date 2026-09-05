# FCoP 4.0 WP3D Family Model

## 1. 审计身份

```yaml
TASKBOOK_COMMIT: e664fa39592b699637c1f0e6aeee229331b321e3
TASKBOOK_SHA256: c97c82d0cb179aafd2a0a7c2c37e34e4eeea9a0ae33b47a4bdf3b9bb1c2232e5
INPUT_HEAD: 9f72dc0ec9a6c7fcbc781f5bb073eac85d3578ab
ACCEPTED_REVIEW_HEAD: c08d6059b89c599388756db8a5cdbaa4536a8e56
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
AUTHORIZED_SCOPE: WP3D_ONLY
```

本报告在修改生产代码前生成。所有判断来自固定提交中的代码、冻结规范与冻结符合性测试。

## 2. 身份与路径模型

- 普通 TASK：四类文件中的 TASK 信封，且没有 `branch_of`。
- Root TASK：TASK 信封自身没有 `branch_of`，同时至少有一个 TASK 的 `branch_of` 指向它。
- Branch TASK：TASK 信封含 `branch_of`，其值指向唯一 Root TASK。
- TASK 的生命周期状态只由其在 `_lifecycle/{inbox,active,review,done,archive}` 中的唯一物理路径决定；同一 `task_id` 多路径或零路径均应 Fail Closed。

现有 `creation._paths()` 已跨五个生命周期目录扫描 TASK，`creation._resolve()` 已执行唯一性检查。因此 family 枚举不需要索引、数据库或第二权威存储：先唯一解析 Root，再跨五目录扫描所有 TASK 信封，严格筛选 `branch_of == root_task_id`，最后按 `task_id` 排序。

## 3. 当前 attempt 与 REPORT head

当前 attempt 应由 TASK 中最后一次合法进入 `active` 的 transition 决定，现有 `lifecycle.current_attempt()` 可作为唯一解析入口。每个 Branch 的 REPORT 候选必须同时满足：

1. 信封类型为 REPORT；
2. `task_id` 等于 Branch；
3. `attempt_id` 等于当前 attempt；
4. replacement 链无环、无悬空、无分叉；
5. 最终唯一 head 可由 `lifecycle.report_head()` 解析。

历史 REPORT 保持 append-only；replacement 只改变“当前 head”的解析结果，不改写旧文件。

## 4. Canonical family digest

规范要求的 canonical 对象只包含 Root 身份及按 `branch_task_id` Unicode code point 顺序排列的 Branch 项；每项绑定 Branch 当前 attempt、REPORT id 与 REPORT 原始字节 SHA-256。对象键递归按 Unicode code point 排序，以无 BOM、无尾换行、无额外空白的 UTF-8 JSON 序列化，再计算 SHA-256。

因此以下内容不能进入摘要：mtime、目录枚举顺序、Runtime 计数器、进程内 generation，以及 Branch 位于 `done` 还是 `archive` 的路径。Branch 终态是 T7 的独立门，不属于 digest；故 Branch 的 T7 路径移动本身不改变 digest。

## 5. 收敛与线性化

既有 `linearization.family_boundary(root, workspace_id, root_task_id)` 是可复用的跨进程 Root-family 短锁。所有会改变 family 快照的短提交必须遵循同一锁序：

1. 解析 subject 与 family Root；
2. 获取唯一 Root-family lock；
3. 锁内重新读取 Root/Branch 路径、当前 attempts、REPORT heads；
4. 在同一快照上计算 canonical digest；
5. 验证 convergence 或 T7 门；
6. 仅提交短文件操作与 receipt/event；
7. 释放锁。

Branch create/reopen、Branch REPORT 初写或 replacement、convergence REVIEW 写入、Branch T7、Root T7 都必须走这一边界。convergence 写入必须锁内重算摘要并核对完整 references，不能接受调用者提供的 digest 作为事实。旧 convergence REVIEW 保留，但 Root T7 只能选择与锁内当前 family 完全匹配的一份明确 REVIEW。

## 6. 三类 T7

- 普通 TASK：唯一 `done` 路径、当前 attempt 与有效 T7 Authorization；不需要 convergence。
- Branch TASK：普通 T7 门加合法 `branch_of`/Root；路径从 `done` 到 `archive` 不改变 family digest。
- 存在 Branch 的 Root：锁内验证全部 Branch 已在 `done`/`archive`、每个当前 attempt 有唯一有效 REPORT head、明确 convergence references 与当前 family 完全相等、convergence digest 与重算值相等、T7 Authorization 绑定同一 digest。

三者可共用现有 Lifecycle 入口、Authorization gate、single-use consumption、过期复查和三阶段 receipt；差异只在锁内证据门。lost-response exact retry 必须由同一 operation identity 返回 Existing，不得追加第二个 T7 event。

## 7. 复杂度结论

任务书允许的一个新私有生产模块 `src/fcop/v4/convergence.py` 足以集中 family 扫描、head 解析、canonical bytes/digest 和 convergence 验证；唯一新公共读取入口 `Project.family_digest(*, root_task_id)` 足够。无需数据库、后台组件、第二锁实现、第二状态机或新依赖。

```yaml
FAMILY_MODEL_IMPLEMENTABLE: true
NEW_PUBLIC_APIS_REQUIRED: 1
NEW_PRODUCTION_MODULES_REQUIRED: 1
SECOND_AUTHORITATIVE_STORE_REQUIRED: false
FAMILY_LINEARIZATION_GAP: false
```

但实现不能在当前冻结符合性夹具下合法完成，详见 `FCOP-4.0-WP3D-TARGET-NODE-BASELINE.md` 与阻断报告。
