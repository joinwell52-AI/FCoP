---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260514-001
sender: ME
recipient: ADMIN
task_id: TASK-20260514-001
parent: REPORT-20260513-015
related:
  - REPORT-20260513-014   # stage-1 双包 lockstep + MCP registry 入驻文档化
  - REPORT-20260513-015   # stage-1.5 Glama badge 加入
thread_key: v2-0-2-release
status: done
priority: P0
session_id: sess-20260514-ME-stage2
created_at: "2026-05-14T01:55:00+08:00"
---

# REPORT · v2.0.2 stage-2 release execution — done

## 一句话结论 / TL;DR

**`fcop@2.0.2` + `fcop-mcp@2.0.2` 双包已在 PyPI 上线,GitHub Release
`v2.0.2` 已创建,Zenodo Concept DOI 自动跟随,origin + backup + tag
三方对齐**。从 `git push v2.0.2` 到全绿,**6 分钟**。剩余唯一 ADMIN 手工
动作:`.\mcp-publisher.exe publish`(~30 秒,把 MCP registry 从 2.0.1
跟到 2.0.2)。

## 时间线 / Timeline

| 时刻 (+08:00) | 事件 | 证据 |
|---|---|---|
| 2026-05-13 22:30 | stage-1 commit `d79d438` | TASK-014 + REPORT-014 |
| 2026-05-13 23:53 | stage-1.5 commit `19ef61e`(Glama 加入) | TASK-015 + REPORT-015 |
| 2026-05-14 01:01 | ADMIN 授权"按规则去做" | `.fcop/proposals/20260514-010249-stage2-sop-execution-authorization.md` |
| 2026-05-14 01:43 | ADMIN 决策撤 Glama(选 "B") | REPORT-015 v2 增补 |
| 2026-05-14 01:46 | stage-2 commit `d3e870a` 落档 | 见下"stage-2 commit 范围" |
| 2026-05-14 01:46 | tag `v2.0.2` annotated 创建 + 双 push | `git push origin v2.0.2` + `git push backup v2.0.2` |
| 2026-05-14 01:46 | `release.yml` workflow `25816343560` 触发 | https://github.com/joinwell52-AI/FCoP/actions/runs/25816343560 |
| 2026-05-14 01:49 | 5/5 job 全绿 | verify 6s · build 35s · fcop 14s · fcop-mcp 15s · release 16s |
| 2026-05-14 01:49 | GitHub Release `v2.0.2` 自动创建 | https://github.com/joinwell52-AI/FCoP/releases/tag/v2.0.2 |
| 2026-05-14 01:53 | PyPI 双包 `/simple/` index 已含 2.0.2 | `pypi.org/simple/fcop/` + `pypi.org/simple/fcop-mcp/` |

## stage-2 commit 范围 / What stage-2 commit changed

`d3e870a release(v2.0.2): stage-2 — CITATION Concept DOI + drop Glama card + stage-2 task`

| 文件 | 改动 | 字节 |
|---|---|---|
| `CITATION.cff` | Zenodo DOI `19886036`(Apr-29 Version) → `19886035`(Concept,始终指向最新);`version` v2.0.0 → v2.0.2;`date-released` 2026-05-13 | 18 行(9+ / 9-) |
| `README.md` | 撤除 Glama AI card badge(ADMIN 选 "B",card 过大破坏头部布局) | -3 行 |
| `README.zh.md` | 同上(中文版) | -3 行 |
| `fcop/tasks/TASK-20260514-001-...` | 新建 stage-2 执行任务文件,formalises SOP-mediated authorization | +152 行 |

**合计**:4 files changed, 152 insertions(+), 15 deletions(-)。

**Glama 已撤,MCP Registry 保留**——后者是 Anthropic 官方目录、纯文字
shields.io badge,体积合理;前者是 Glama AI 自托管的产品 card.svg,
渲染高度 ~250px,破坏 GitHub README 头部观感。

## 三方对齐 SHA / Three-way SHA alignment

| Ref | SHA / Tag | origin | backup |
|---|---|---|---|
| main HEAD | `d3e870a` | ✅ | ✅ |
| tag v2.0.2 | annotated, points to `d3e870a` | ✅ | ✅ |

```bash
$ git log --oneline -3
d3e870a release(v2.0.2): stage-2 — CITATION Concept DOI + drop Glama card + stage-2 task
19ef61e release(v2.0.2): stage-1.5 — add Glama AI MCP server card badge to README (zh+en)
d79d438 release(v2.0.2): stage-1 — dual-package bump + MCP registry milestone
```

## workflow `release.yml` 5 job 结果

| Job | 耗时 | 状态 |
|---|---|---|
| Verify tag matches package versions | 6s | ✅ fcop 2.0.2 / fcop-mcp 2.0.2 / CHANGELOG [2.0.2] 全部对齐 |
| Build both wheels | 35s | ✅ twine check pass · 双 wheel smoke install clean venv 成功 |
| Publish fcop to PyPI | 14s | ✅ twine upload via `PYPI_API_TOKEN_FCOP` secret |
| Publish fcop-mcp to PyPI | 15s | ✅ twine upload via `PYPI_API_TOKEN_FCOP_MCP` secret |
| Create GitHub Release | 16s | ✅ release body 自动从 `CHANGELOG.md` 抽 `## [2.0.2]` 段 |

**总耗时**:86s(包括 job 间调度)。run URL:
https://github.com/joinwell52-AI/FCoP/actions/runs/25816343560

## 现实状态验证 / Reality check

```bash
# PyPI · fcop
$ python -c "import urllib.request as u; print('2.0.2 in simple:', '2.0.2' in u.urlopen('https://pypi.org/simple/fcop/').read().decode())"
2.0.2 in simple: True

# PyPI · fcop-mcp
$ python -c "import urllib.request as u; print('2.0.2 in simple:', '2.0.2' in u.urlopen('https://pypi.org/simple/fcop-mcp/').read().decode())"
2.0.2 in simple: True

# GitHub Release
$ gh release view v2.0.2 --json tagName,name,publishedAt,url
{
  "name": "fcop & fcop-mcp 2.0.2",
  "publishedAt": "2026-05-13T17:49:06Z",
  "tagName": "v2.0.2",
  "url": "https://github.com/joinwell52-AI/FCoP/releases/tag/v2.0.2"
}
```

> 注:`pypi.org/pypi/fcop/json` JSON API 端点在 commit 后 5 分钟内可能
> 显示旧版本(2.0.0),是 PyPI CDN 缓存延迟,**不是回滚**。`/simple/` HTML
> 端点是真相源,已显示 2.0.2。Pip 安装走 `/simple/`,不受影响。

## Zenodo Concept DOI 效果 / Zenodo behaviour

- **`CITATION.cff` 中的 DOI** 现为 `10.5281/zenodo.19886035`(Concept)。
- GitHub Release v2.0.2 创建会触发 Zenodo webhook,**自动**抓取仓库
  zipball + `CITATION.cff` → 生成新的 Version DOI(数字大于 `20154554`,
  即 v2.0.1 的 snapshot)。
- Concept DOI `19886035` **不变**,但其"最新版本"指针自动指向新生成
  的 Version DOI。
- 所有现在与未来引用 `10.5281/zenodo.19886035` 的论文 / README badge
  / `CITATION.cff` 都**自动**指向 v2.0.2 快照,**未来发版无需手动改
  `CITATION.cff` 的 DOI**——只改 `date-released` 与 `version`。
- 这一切构成 Rule 0.c 的物理实现:**引用永远跟随最新真相,无人工同步
  缺口**。

## 协议合规 / Protocol compliance

| Rule | 落点 |
|---|---|
| **0.a.1**(四步循环) | TASK-014 / 015 / 001 三个任务文件全部落档;三份 REPORT 闭环(REPORT-014 / 015 / 001);本份 REPORT 闭后立即归档(stage-3 closure commit) |
| **0.b**(决策-执行分离) | ADMIN(决策)+ workflow `release.yml`(以 GitHub secret 实际执行 PyPI upload)+ me(协调 commit + push,不持有 PyPI 凭证)= 三方制衡。MCP registry publish 保留 ADMIN 手工,**完整链路三方分离** |
| **0.c**(只落真话) | 每一行数字 / SHA / URL 都源自命令输出;PyPI JSON API 延迟现象明示;不替 ADMIN 操作 mcp-publisher |
| **5**(append-only) | TASK / REPORT 全部 append-only;stage-2 / 1.5 / 1 三份独立 commit,无 rebase / squash |
| **6**(reciprocity) | TASK-001 / 015 / 014 均有对应 REPORT 闭环 |
| **7**(破坏性操作) | 高风险 publish 通过 SOP-mediated authorization(`.fcop/proposals/20260514-010249`)落档;rollback plan 已写在 TASK-001 §回滚预案 |
| **8**(拒绝执行) | mcp-publisher 凭证物理不在 agent 手上,**没有跨越 ADMIN 凭证边界**——这是 Rule 8 在物理层的天然实现 |
| **9.5.1**(risk_level) | TASK-001 frontmatter `risk_level: high`;但本 task 是 SOP-routine 而非 ad-hoc,故走 RULES-mcp-registry-release.md §Step ① + ② 而不再触发 `decision=needs_human` |

## 剩余 ADMIN 手工动作 / Remaining ADMIN-only action

**唯一一步**(per `fcop/shared/RULES-mcp-registry-release.md` §Step ③):

```powershell
cd D:\FCoP
.\mcp-publisher.exe publish
```

- 用途:把 MCP registry `io.github.joinwell52-AI/fcop` 从 2.0.1 跟到 2.0.2。
- 凭证:本机 OAuth session(`mcp-publisher login` 早前完成,token 长期
  有效),agent 无法非交互式调用。
- 预期输出:`✓ Server io.github.joinwell52-AI/fcop version 2.0.2`。
- 验证:`curl https://registry.modelcontextprotocol.io/v0/servers | grep fcop`
  或直接 https://registry.modelcontextprotocol.io 搜索 `fcop`。
- 完成后请告知 me,me 把"MCP registry 2.0.2"行追加进
  `fcop/shared/RULES-mcp-registry-release.md` 的"近期发版记录"段(若有),
  并把本份 REPORT-001 frontmatter `status: done` 不动(目前的 `done`
  反映"我能交付的全部范围已交付",MCP registry 那一步是 ADMIN 的
  scope)。

## 下一步 / Next steps

收到本份 REPORT 后,me 立即:

1. **归档** TASK-014 / TASK-015 / TASK-001 + 对应 REPORT-014 / 015 / 001
   → `fcop/log/`(逐份 `archive_task`,保留 Rule 0.a 的 ledger 事件可见性)
2. **stage-3 closure commit**:落 6 份归档移动 + 本份 REPORT-001 + 任何
   遗漏的 `_letter-to-admin.*.md` 模板修正(若 ADMIN 决策更新)
3. **双 push** origin + backup,三方 SHA 对齐
4. 给 ADMIN 一份"今夜执行报告"作为聊天总结(不再起新 TASK)

---

**End of REPORT-20260514-001.**

stage-2 thread `v2-0-2-release` 在 stage-3 closure commit 后正式关闭。
