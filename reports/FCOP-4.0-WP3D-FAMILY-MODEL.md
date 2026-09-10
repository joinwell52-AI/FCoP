# FCoP 4.0 WP3D v1.1 Family Model

## 审计身份

```yaml
TASKBOOK_COMMIT: 4e0d8c524020cc3b1b152d3d3a736f84a2f78a4e
TASKBOOK_SHA256: dbe310a116ce2a3b8679ac5f6b85bd551ce810ce554b7857d3e92786a7fa5c26
INPUT_HEAD: dd8c39a2e025cc60f37d443abbe0988cbddf1810
FIXTURE_GATE: WP3D_FIXTURE_ALIGNMENT_ACCEPTED
AUTHORIZED_SCOPE: WP3D_ONLY
```

本报告在修改生产代码前更新。旧任务书 `e664fa3...` 已作废；此前发现的 T7 可信 Profile 夹具冲突已由输入基线中的 WP3D.0 Gate 关闭。

## 身份、路径与 family 枚举

- 普通 TASK 没有 `branch_of`，且没有其他 TASK 指向它。
- Root TASK 自身没有 `branch_of`，且至少一个 Branch 的 `branch_of` 指向它。
- Branch TASK 含唯一、同工作区、深度为一的 `branch_of`，指向 Root。
- TASK 的 NOW 状态仅由 `_lifecycle/{inbox,active,review,done,archive}` 中唯一物理路径决定；重复路径、悬空 Root、Branch 指向 Branch 均 Fail Closed。

Family 枚举不建立第二索引：先唯一解析 Root，再扫描五个生命周期目录中的 TASK 信封，筛选 `branch_of == root_task_id`，按 `branch_task_id` 的 Unicode code point 顺序排序。每次短提交均在既有 `family_boundary(workspace_id, root_task_id)` 锁内重新枚举。

## Attempt、REPORT head 与 canonical digest

每个 Branch 的当前 attempt 由 TASK 最后一次合法进入 `active` 的 transition 决定。REPORT head 必须满足同 `subject_ref`、同当前 attempt、replacement 链无悬空/环/分叉且唯一。摘要项绑定：

```json
{"attempt_id":"...","branch_task_id":"...","report_digest":"...","report_id":"..."}
```

完整对象为 `contract=fcop-family-v1`、`root_task_id` 和排序后的 `branches`。对象键递归排序，使用无 BOM、无尾换行、无额外空白的 UTF-8 JSON，再取小写 SHA-256。REPORT 摘要针对经过 v4 Encoding 验证后的完整文件字节。mtime、目录枚举顺序、运行时计数和 Branch 的 done/archive 路径不得进入摘要；因此 Branch T7 只移动路径，不改变 family digest。

## Convergence REVIEW

只有 `review_kind: convergence`、`decision: approved`、subject 为 Root 的 REVIEW 才可作为收敛证据。写入时必须在 family lock 内重新计算摘要并验证：

1. Root 至少存在一个 Branch；
2. 每个 Branch 当前 attempt 有唯一 REPORT head；
3. references 精确包含全部 Branch 当前 REPORT，可选再含 Root 当前 REPORT；
4. 不允许重复、缺失、额外、旧 attempt 或旧 replacement head；
5. 请求 `family_digest` 与锁内重算值一致。

旧 convergence 文件保持 append-only；Root T7 只接受请求明确引用且与锁内当前快照完全一致的那一份。

## 三类 T7 与错误优先级

- 普通 TASK：唯一 done 路径、强关系有效、T7 Authorization 有效；不要求 convergence。
- Branch TASK：同普通 T7，并在 Root family lock 内提交；done→archive 不改变摘要。
- 带 Branch 的 Root：先验证所有 Branch 均为 done/archive，再验证 convergence 当前性，最后验证绑定同一 digest 的 single-use Authorization。

锁内优先级固定为：`BRANCH_NOT_TERMINAL` → `FAMILY_CONVERGENCE_REQUIRED/MISMATCH` → 已验收的 WP3C Authorization 错误。精确 lost-response retry 复用既有 receipt 返回 Existing；同一授权用于不同迁移仍返回 `AUTHORIZATION_REUSED`。

## 线性化与复杂度结论

Branch create/reopen、Branch REPORT 初写或 replacement、convergence REVIEW、Branch T7、Root T7 均复用现有 family lock。`src/fcop/v4/convergence.py` 作为唯一新私有模块集中纯扫描、canonical digest 和 convergence 校验；唯一新公共 API 为 `Project.family_digest(*, root_task_id)`。无需数据库、后台进程、第二锁、第二状态机或新依赖。

```yaml
FAMILY_MODEL_IMPLEMENTABLE: true
NEW_PUBLIC_APIS_REQUIRED: 1
NEW_PRODUCTION_MODULES_REQUIRED: 1
SECOND_AUTHORITATIVE_STORE_REQUIRED: false
FAMILY_LINEARIZATION_GAP: false
```
