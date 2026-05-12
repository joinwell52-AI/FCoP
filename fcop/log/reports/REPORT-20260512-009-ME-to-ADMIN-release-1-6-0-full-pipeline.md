---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-009
task_ref: TASK-20260512-009
sender: ME
recipient: ADMIN
priority: P0
thread_key: release-1-6-0
status: done
risk_level: irreversible
completed_at: "2026-05-13T00:35:00+08:00"
---

# REPORT · v1.6.0 一条龙发版完成

## TL;DR

**`fcop@1.6.0` + `fcop-mcp@1.6.0` 已成功发布到 PyPI 与 GitHub Release。**
release.yml 5 个 job 全部 `success`,本地 wheel smoke install 通,
ADR-0033 trailing-slug 文法可通过 PyPI JSON API 实测到位。

唯一**未完结**的尾巴:PyPI Simple index 的 CDN 传播延迟(典型 5-15min),
外部 `pip install fcop==1.6.0` 暂时还拿不到——这不是发版失败,只是
PyPI Fastly CDN 的标准行为。详见末尾"未完待续"。

---

## 一条龙执行轨迹

| Phase | 动作 | 结果 |
|---|---|---|
| 0 · 立单 | `TASK-20260512-009` 落盘(`risk_level=irreversible`) | ✅ |
| 1 · 代码层检查 | `_version.py × 2 = 1.6.0`、`CHANGELOG [1.6.0]` 段对、`pyproject.toml` 元数据 OK | ✅ |
| 2 · 测试 + lint + audit | `pytest tests/ = 1061 passed`、`ruff check src tests mcp/src = 0`、`mypy src = no issues`、`pip_audit = 0 vulns` | ✅ |
| 3 · 文档版本对齐(发版前体检发现的 ⛔) | README v1.3→v1.6 · letter zh+en v1.5.1→v1.6.0 · protocol 2.3.0→2.4.0 · server.py "0.6.4 summary" → "v1.6.0 summary" · test_rules/test_server 硬断言同步 | ✅ |
| 4 · P=E redeploy | `Project(D:\FCoP).deploy_protocol_rules(force=True, archive=True)` (走**本地 1.6.0 源码**,**不走** MCP 端 1.5.1 wheel 以免反向覆盖) | ✅ 4 个目标文件全部刷到 commentary 2.4.0,旧文件归档到 `.fcop/migrations/20260513T001716/rules/` |
| 5 · 第三个 commit | `ffb41e4 chore(release): pre-1.6.0 docs alignment + redeploy host-neutral rules` (11 files, +617/-36) | ✅ |
| 6 · 本地 build + smoke | `py -3.10 -m build × 2` → 4 个产物全过 `twine check`;干净 venv 装 wheel `fcop=1.6.0 / fcop_mcp=1.6.0 / rules=2.4.0` 全 import 通 | ✅ |
| 7 · ADMIN 二次拍板(Rule 7) | "GO,三步全做" | ✅ |
| 8 · push main | `0250fac..ffb41e4 main -> main` | ✅ |
| 9 · tag v1.6.0 | annotated tag,消息含 ADR-0033 摘要 | ✅ |
| 10 · push tag | `[new tag] v1.6.0 -> v1.6.0`,触发 GitHub Actions release.yml run **25747612150** | ✅ |
| 11 · release.yml | 5 job 全 `success`: Verify tag / Build wheels / Publish fcop PyPI / Publish fcop-mcp PyPI / Create GitHub Release | ✅ |
| 12 · 发布后验证 | PyPI JSON API `/pypi/fcop/1.6.0/json` + `/pypi/fcop-mcp/1.6.0/json` 都返回完整 metadata;GitHub Release `v1.6.0` 含 4 个 assets | ✅ |

## 量化交付

- **PyPI 上架制品**:`fcop-1.6.0-py3-none-any.whl` + `fcop-1.6.0.tar.gz` + `fcop_mcp-1.6.0-py3-none-any.whl` + `fcop_mcp-1.6.0.tar.gz`
- **GitHub Release**:`fcop & fcop-mcp 1.6.0`,publishedAt `2026-05-12T16:25:26Z`,4 assets
- **HEAD**:`ffb41e4` on `main`(连同 `a8ff07c` + `a669ea3`,本次冲刺共 3 个 commits)
- **Tag**:`v1.6.0`,annotated,指向 `ffb41e4`
- **协议版本**:`fcop_protocol_version 2.3.0 → 2.4.0`(commentary 新增 trailing-slug 节)
- **规则版本**:`fcop_rules_version 2.4.0`(不变,trailing-slug 是 commentary-layer additive)
- **新增测试**:31 个 trailing-slug 测试(ADR-0033 sprint)
- **回归**:1061 passed / 2 skipped(legacy 兼容跳过)

## 检查清单 ✅(release-process.md §A-D)

- A · 代码层:`_version.py × 2 = 1.6.0` · `pyproject.toml` 元数据 · CHANGELOG `[1.6.0]` 段对 · `mcp/pyproject.toml` 对 `fcop` 锁注释 vs MAJOR 锁约束的注释矛盾**记账**(non-blocking,与 1.x SemVer 一致)
- B · 测试与质量门:`pytest src+tests+mcp/src` 1061 passed · `ruff check src tests mcp/src` 0 errors · `mypy src` no issues · `pip_audit` 0 vulns · `twine check` 4 通过
- C · 文档对齐:README + letter zh/en + server.py + test_rules + test_server 全部刷到 1.6.0 · `.cursor/rules/*.mdc` + AGENTS.md + CLAUDE.md 全部刷到 commentary 2.4.0
- D · Git:HEAD = `ffb41e4`(干净)· `origin/main` 同步 · `v1.6.0` tag 创建并推送

## ⚠️ 已记账的 non-blocking 项(下个 patch 或独立 task 处理)

1. **`mcp/pyproject.toml` 注释 vs 约束**:注释暗示 MINOR 锁,实际是 MAJOR 锁 `fcop>=1.0,<2.0`(与 ADR-0003 §1.x SemVer 一致,非 bug,只是注释口径漂移)
2. **`ruff check .`(全仓)21 errors 在 `scripts/`**:开发期一次性脚本,不在 wheel 里,`release.yml` 不跑 ruff,不影响发布
3. **`mypy tests/` 110 errors**:pre-existing,`release.yml` 不跑 mypy
4. **`ADR-0028` 状态 `Proposed`**:pre-existing,历史发版未拦,`release.yml` 不检 ADR 状态
5. **Untracked 历史噪音 11 个文件**(`.scratch/` / `scripts/_*` / `*_events.jsonl`):ADR-0033 sprint 已显式排除,建议起独立 task 决定每条 add 或 .gitignore
6. **GitHub Actions runner Node.js 20 deprecation 警告**:6/2/2026 前需把 `release.yml` 里 `actions/checkout@v4` 等升级到 Node.js 24 兼容版本(非阻塞,但要安排)

## 未完待续 · CDN 传播延迟

PyPI Simple index 的 CDN 缓存还在传播,外部 `pip install fcop==1.6.0` 此刻
报 `Could not find a version that satisfies the requirement` —— 这是
PyPI Fastly CDN 的标准延迟(typically 5–15min,有时更长)。验证现状:

- ✅ PyPI JSON API:`https://pypi.org/pypi/fcop/1.6.0/json` 返回 200 + 完整 metadata
- ✅ PyPI JSON API:`https://pypi.org/pypi/fcop-mcp/1.6.0/json` 返回 200 + 完整 metadata
- ✅ GitHub Release v1.6.0 已创建,4 assets 全部可下载
- ⏳ PyPI Simple index(`/simple/fcop/`):缓存未刷新,`pip install` 暂时拿不到

**这不是发版失败**;ADMIN 在 5-30 分钟后跑一次 `pip install --upgrade fcop fcop-mcp`
即可拿到 1.6.0 wheel。我会在下一轮我被唤起时补做一次外部 pip 真验证。

## Rule 0.a.1 闭环

- ✅ Step 1: TASK-20260512-009 落盘(本任务载体)
- ✅ Step 2: 做了(本 REPORT 总结的 12 个 phase)
- ✅ Step 3: REPORT-20260512-009 落盘(本文件)
- ⏳ Step 4: archive_task(TASK-20260512-009) → 待执行(本 REPORT 落盘后立刻 archive)

## Refs

- `TASK-20260512-009-ADMIN-to-ME-release-1-6-0-full-pipeline.md`(本任务载体)
- `ffb41e4` · `a8ff07c` · `a669ea3`(本次 sprint 3 commits)
- `v1.6.0` annotated tag
- GitHub Actions run `25747612150`(release.yml)
- ADR-0033 `Accepted`
- `docs/release-process.md` Phase 1+2+3
- `.fcop/migrations/20260513T001716/rules/`(P=E redeploy 旧版本归档)

---

**Status**: `done`
**Next**: archive TASK-009 + 监控 CDN 传播 + 等 codeflow 上游 PM 早会汇报 I-16/I-17/I-18
