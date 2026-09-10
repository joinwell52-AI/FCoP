# FCoP 4.0 WP3E · Cold Export Proof

`Project.export_archive(*, task_id)` 只从唯一
`fcop/_lifecycle/archive/{TASK}.md` 读取字节，并通过既有 durable `publish()` 写入
`fcop/cold/{TASK}.md`。archive 原路径、字节和 transition 永不移动或改写。

目标同字节时返回 Existing；目标不同字节时返回
`TARGET_ALREADY_EXISTS_DIFFERENT` 且不覆盖。`TARGET_DURABLE` fault 发生在 cold
副本持久化之后，但 archive 仍是唯一 NOW。`_resolve()`、`inspect_state()`、关系
解析与 family snapshot 都只扫描既有 lifecycle/bucket 权威目录，cold 不成为
第六生命周期桶，也不参与 Authorization 或 digest。

```yaml
COLD_EXPORT_NON_AUTHORITATIVE: PASS
ARCHIVE_PATH_PRESERVED: PASS
ARCHIVE_BYTES_PRESERVED: PASS
COLD_DESCENDANT_CONTAINS_LIFECYCLE: false
SAME_BYTES_EXISTING: PASS
DIFFERENT_BYTES_FAIL_CLOSED: PASS
TARGET_DURABLE_FAULT_NOW_UNCHANGED: PASS
NEW_BACKGROUND_COMPONENTS: 0
```
