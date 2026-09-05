# FCoP 开发任务书 GitHub 交付约定

## 1. 唯一权威

从本约定启用后，FCoP 开发任务书统一保存在仓库：

```text
taskbooks/fcop-4.0/<WP-ID>/
```

正式执行权威由以下三项共同确定：

```text
GitHub repository path
+ immutable Taskbook Commit SHA
+ taskbook file SHA-256
```

聊天中的摘要、复制文本、本地下载文件和旧附件只能帮助阅读，不能单独授权执行。

## 2. 分支命名

任务书发布分支：

```text
task/fcop-4.0-<wp-id>-<short-name>
```

实现审核分支：

```text
review/fcop-4.0-<wp-id>-<short-name>
```

任务书分支只允许写入 `taskbooks/**`。实现分支从 Taskbook Commit 创建，使任务书随提交链保留，但实现阶段不得改写任务书。

## 3. 文件命名

```text
taskbooks/fcop-4.0/<WP-ID>/00-README.zh.md       # 可选阶段入口
taskbooks/fcop-4.0/<WP-ID>/01-<Task>-Taskbook.zh.md
```

一个阶段只能有一份文件声明：

```yaml
document_role: EXECUTION_TASKBOOK
execution_authorized: true
authorized_scope: <WP-ID>_ONLY
```

其他说明、审计输入和历史任务书必须写：

```yaml
document_role: REVIEW_INPUT_ONLY
execution_authorized: false
authorized_scope: NONE
```

## 4. Codex 开始规则

Codex 开始执行前必须：

1. fetch 指定 taskbook 分支；
2. 读取指定 GitHub 路径；
3. 验证 Taskbook Commit 和文件 SHA-256；
4. 验证任务书声明的代码基线、冻结合同和 Gate；
5. 从 Taskbook Commit 创建独立 review 分支/worktree；
6. 若任一身份不匹配，Fail Closed 并停止。

不得根据“最新文件”、文件名相似度、聊天历史或本地旧副本猜测执行任务书。

## 5. 执行交付

实现继续采用两提交结构：

1. Content Commit：代码、测试和报告；
2. Manifest Commit：只写对应 `reviews/fcop-4.0/<wp-id>/MANIFEST.md`。

Manifest 必须记录：

- Taskbook repository path；
- Taskbook Commit；
- Taskbook SHA-256；
- Code Baseline；
- Frozen Contract Commit；
- Content Commit；
- Manifest Commit；
- 远端回读与文件 SHA-256；
- requested Gate；
- 未获授权的下一阶段保持 `false`。

## 6. ADMIN 审核

ADMIN 审核只读取 GitHub 固定提交，不要求人工下载、转发 ZIP 或复制报告。

执行者可以声明完成，但不能自行签署 Gate。只有 ADMIN 审核指定 review HEAD 后，才能签署下一阶段 Gate。

## 7. 禁止事项

- 不把任务书直接提交到 `main`；
- 不 force push；
- 不在实现提交中偷偷修改任务书；
- 不让多个文件同时声称同一阶段执行授权；
- 不用 Manifest 替代任务书；
- 不用本地路径作为唯一审核入口；
- 不因 GitHub 分支存在就自动授权执行。
