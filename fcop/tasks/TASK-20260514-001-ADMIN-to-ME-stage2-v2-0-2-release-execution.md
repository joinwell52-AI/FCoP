---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260514-001
sender: ADMIN
recipient: ME
priority: P0
parent: TASK-20260513-014
related: [TASK-20260513-014, TASK-20260513-015]
thread_key: v2-0-2-release
session_id: sess-20260514-ME-stage2
risk_level: high
created_at: "2026-05-14T01:06:00+08:00"
---

# TASK · v2.0.2 stage-2 release execution (SOP-mediated authorization)

## Background / 背景

`TASK-20260513-014`(stage-1)已经把 v2.0.2 所有**文件层面**的改动
落档(版本号同步 / README / CHANGELOG / docs/index.html /
mcp/README.md / 12 类清单 / mcp-registry release rules)并 commit
为 `d79d438`,双 push 三方对齐完成。

`TASK-20260513-015`(stage-1.5)把 Glama AI badge 加进
`README.md` / `README.zh.md`,commit 为 `19ef61e`,同样双 push
三方对齐完成。

stage-2 是把这一切**变成线上事实**:打 v2.0.2 tag 触发
`.github/workflows/release.yml` 自动跑 PyPI 双包上传 + GitHub
Release 创建,然后切 CITATION.cff 到 Zenodo Concept DOI,落收尾
commit。

## ADMIN 授权依据 / Authorization basis

2026-05-14 01:01 (+08:00) ADMIN 两条消息明示授权:

> "那你尽快去做!"
> "发版的规则都确定了,你只要按规则去做,就可以了;"

授权的 SOP 边界:
- `docs/release-process.md` § 阶段 3 / § 阶段 4 / § 阶段 4.5
- `fcop/shared/RULES-mcp-registry-release.md`(Step ① / ② / ③ 分工)
- `.github/workflows/release.yml`(5-job 自动化)
- `RULES-release-sync-checklist.md`(release 红线)

Rule 8 留证文档:
`.fcop/proposals/20260514-010249-stage2-sop-execution-authorization.md`

## Requirements / 要求

按以下顺序执行,**不跑 SOP 外的命令**,每一阶段全绿才进下一阶段:

### A · Pre-flight(纯本地,不触公网)

1. 跑 `docs/release-process.md` § G 全套 6 条扫描审计
2. 准备 `.scratch/_v2_0_2_tag_msg.txt` annotated tag message
3. 准备 `.scratch/_stage2_commit_msg.txt`(CITATION 切换 commit msg)
4. 准备 `.scratch/_stage3_closure_msg.txt`(release closure commit msg)

### B · Stage-2 commit(CITATION → Concept DOI)

5. 改 `CITATION.cff` 4 处(基于 `.scratch/_stage2_citation_draft.cff`):
   - `identifiers[0].value` → `10.5281/zenodo.19886035`(Concept DOI)
   - `identifiers[0].description` → `"Concept DOI — always resolves to the latest version on Zenodo"`
   - `date-released` → `"2026-05-13"`
   - `version` → `"v2.0.2"`
   - `preferred-citation.{year=2026, month=5, doi, url, type}` 同步
6. 落 REPORT-001 草稿(标 status=in-progress,等 workflow 后补完)
7. 显式 `git add` 列文件,**严禁 `git add -A`**
8. `git commit -F .scratch/_stage2_commit_msg.txt`
9. `git push origin main`
10. `git push backup main`
11. main SHA 三方对齐验证(origin / backup / 本地 HEAD)

### C · Tag push 触发 workflow

12. `git tag -a v2.0.2 -F .scratch/_v2_0_2_tag_msg.txt`
13. `git push origin v2.0.2`
14. `git push backup v2.0.2`
15. tag SHA 三方对齐(annotated tag 比较 object SHA + dereferenced commit SHA)

### D · workflow 监控 + 阶段 4 验证

16. `gh run list --workflow=release --limit 1` 取 run-id
17. `gh run watch <run-id>` 等 5 job 全绿(verify / build / publish-fcop / publish-fcop-mcp / github-release)
18. PyPI JSON API × 2:`fcop` + `fcop-mcp` 都返回 `2.0.2`
19. `gh release view v2.0.2`:状态 `published`,带 4 个 wheel + tar.gz 附件
20. 任一失败 → 落 ISSUE 记录原因 + 停止;不"自我重试",交回 ADMIN 决定 bump v2.0.3

### E · Stage-3 closure(workflow 全绿后)

21. REPORT-001 补完(填入 workflow run url / 各 job 结果 / PyPI 验证截图等价物 / 已知非阻塞项)
22. `git mv` 归档:
    - TASK-014 / REPORT-014 → `fcop/log/{tasks,reports}/`
    - TASK-015 / REPORT-015 → 同
    - TASK-001 / REPORT-001(本任务自己)→ 同
23. 显式 `git add` 列文件
24. `git commit -F .scratch/_stage3_closure_msg.txt`
25. `git push origin main + git push backup main`
26. SHA 三方对齐

### F · 移交 ADMIN

27. 写"今夜执行报告"摘要发给 ADMIN
28. 待办指针:`RULES-mcp-registry-release.md` Step ③(`.\mcp-publisher.exe publish`)
    — 需要 OAuth session,ADMIN 手工执行;agent 物理边界做不了

## Acceptance Criteria / 验收标准

- [ ] `.fcop/proposals/20260514-010249-*.md` 已落档
- [ ] §G 6 条扫描全绿(或显式登记例外)
- [ ] `CITATION.cff` 指 Concept DOI(`19886035`),version=`v2.0.2`
- [ ] stage-2 commit 落档,三方 SHA(origin/backup/local)一致
- [ ] tag `v2.0.2` 三方一致(annotated)
- [ ] `release.yml` 5 job 全绿
- [ ] PyPI JSON:`fcop` 和 `fcop-mcp` 都是 `2.0.2`
- [ ] `gh release view v2.0.2` 状态 `published`
- [ ] stage-3 closure commit + 双 push + SHA 三方对齐
- [ ] REPORT-001 收尾完整
- [ ] TASK-014/015/001 已归档
- [ ] (ADMIN 后续手工)`mcp-publisher publish` + Zenodo 自动抓取确认

## Rollback / 回滚

| 失败点 | 应对 |
|---|---|
| stage-2 commit 内容错(未 push) | `git reset --soft HEAD~1` + 改 + 重 commit |
| stage-2 push 后发现错 | append-only 修复 commit;**禁止** `git push --force` |
| tag push 后 workflow verify 失败 | tag 留着占坑 → bump v2.0.3 重来;在 CHANGELOG 加注脚 |
| workflow build/publish 失败 | 同上,bump v2.0.3 |
| MCP registry publish 出错(ADMIN 阶段) | 不阻塞 PyPI 已发版;按 RULES-mcp-registry-release.md § Failure recovery |

## See also

- `.fcop/proposals/20260514-010249-stage2-sop-execution-authorization.md`(Rule 8 留证)
- `docs/release-process.md` § 阶段 3 / 4 / 4.5
- `fcop/shared/RULES-mcp-registry-release.md`
- `fcop/log/tasks/TASK-20260513-014-*.md`(parent)
- `fcop/log/tasks/TASK-20260513-015-*.md`(related)
- `.scratch/_stage2_citation_draft.cff`(CITATION 改动草稿)
- `.scratch/_stage2_verify_checklist.md`(验证清单草稿)
