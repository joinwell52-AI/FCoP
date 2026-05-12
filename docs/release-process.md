# FCoP 发布流程 / Release Process

> 面向 **`fcop` / `fcop-mcp` 的维护者**。
> 终端用户不需要读本文;看 [MIGRATION-0.6.md](./MIGRATION-0.6.md) 或
> [README](../README.md) 即可。
>
> 本 SOP 自 **v1.6.0**(2026-05-12)起按"一条龙"流程组织,
> 经历 v1.6.0 完整闭环验证。下次发版**逐节按此 SOP 执行即可**,不需要再凭记忆。
> 历史 0.6.x SOP 见 git history。

---

## 核心约束 / Core Invariants

1. **两个包必须同版本号齐发**(`fcop 1.6.0` 和 `fcop-mcp 1.6.0`,不能只发一个)
   ——见 [ADR-0002](../adr/ADR-0002-package-split-and-migration.md)
2. **稳定性宪章一票否决**([ADR-0003](../adr/ADR-0003-stability-charter.md)):
   snapshot 改了 / CHANGELOG 没标注 / ADR 还是 `Proposed` → CI 挡下
3. **发布即不可逆**:PyPI 禁止同版本号覆盖。`twine upload` 成功即占坑
4. **Rule 0.a.1 闭环是发版的强制交付物**(自 v1.6.0 起):
   发版必须有一份载体 `TASK-*.md` + 一份对应 `REPORT-*.md` + archive 到
   `fcop/log/`。**没落文件 = 没发版过**(Rule 0.a)

---

## 版本号规则 / Versioning

遵循 [Semantic Versioning 2.0](https://semver.org/spec/v2.0.0.html):

```
MAJOR.MINOR.PATCH[rcN|devN]
```

| 场景 / Scenario | 示例 / Example |
|---|---|
| 1.x 稳定版主开发版本 | `1.6.0`, `1.6.1`, `1.7.0` |
| RC(候选发布,允许装但不推) | `1.7.0rc1` |
| 开发快照(仅本地 / CI) | `1.7.0.dev0` |
| 正式版 | `1.7.0` |

**硬规则**(ADR-0003 1.x SemVer 派生):

- `1.MINOR.PATCH` 内:**additive only**。加 tool、加可选字段、加 frontmatter 项
  ——全部 OK,但**不得**破坏既有接口
- MAJOR(`1.x` → `2.0`):才允许破坏性变更,且必须走 deprecation cycle
- `fcop_protocol_version` / `fcop_rules_version` 单独有自己的语义版本号,
  和 wheel 版本**不需要绑定 1:1**,但破坏性变更必须同步 MAJOR bump

---

## 发布前检查清单 / Pre-Release Checklist

> 下面 **6 段(A–F)** 全部 ✅ 才能进入发布步骤。
> 任一项 ⛔ → 修;`⚠️` → 标到任务里走 ADMIN 决策。

### A. 代码层 / Code

- [ ] `src/fcop/_version.py` bump 到目标版本(如 `__version__ = "1.7.0"`)
- [ ] `mcp/src/fcop_mcp/_version.py` **同步** bump,字符串与 `fcop` 一致
- [ ] `mcp/pyproject.toml` 的 `fcop>=1.0,<2.0` 依赖约束保持 **MAJOR 锁**
      (`<MAJOR+1`)。1.x 之间任意 MINOR 都兼容,不需要每发一次就改约束
- [ ] `pyproject.toml` / `mcp/pyproject.toml` 其它元数据正确
      (classifiers, `python_requires`, `[project.urls]`)

### B. 测试 & CI / Tests & CI

明确 release-gate **范围**:`src/` + `tests/` + `mcp/src/` 三处必须全绿。
`scripts/` 是维护者临时工具,**不**进 release-gate。

- [ ] `py -3.10 -m pytest tests/test_fcop` 全绿
- [ ] `py -3.10 -m pytest tests/test_fcop_mcp` 全绿
- [ ] `py -3.10 -m ruff check src tests mcp/src` 全绿
      *(`scripts/` 历史 lint 错误不阻塞)*
- [ ] `py -3.10 -m mypy src` 全绿
      *(`tests/` 历史 mypy 错误不阻塞,只要 `src/` 严格通过即可)*
- [ ] `py -3.10 -m pip_audit` 对 **直接运行时依赖** 无高危
      ——建议用 `importlib.metadata.requires()` 抽出 `fcop` + `fcop-mcp` 的
      运行时 deps 单独喂 `pip_audit --requirement`,避免本机其它包污染结果
- [ ] GitHub Actions 主干最近一次 `test-fcop.yml` / `test-fcop-mcp.yml`
      run 是绿的
- [ ] `public_surface.json` / `tool_surface.json` / 其它 snapshot 与
      `git status` 一致(没有未提交 diff,或 diff 已在 CHANGELOG 标注)

### C. 文档层 / Docs

下面 **6 处文档** + **3 处硬断言** 必查。这是 v1.6.0 实战经验:任何一处漂移
都会让 `test_rules` 红或者让用户读到错版本号:

- [ ] `CHANGELOG.md` 把 `[Unreleased]` → `[1.7.0] - YYYY-MM-DD`
- [ ] CHANGELOG 新版块下至少包含:
   - 新增的每个 public API → `Added`
   - 每个 signature/behavior 变化 → `Changed`(必须 additive 或带 deprecation)
   - 每个 deprecation → `Deprecated` + 移除目标版本
- [ ] `README.md` 顶部 "Current release: `vX.Y.Z`" 一行同步到新版本号 + 一句
      话亮点描述
- [ ] `src/fcop/rules/_data/letter-to-admin.zh.md` 摘要块版本号 / 日期 /
      `fcop-protocol.mdc` 版本号
- [ ] `src/fcop/rules/_data/letter-to-admin.en.md` 同上(必须与 zh 同步)
- [ ] **3 处 hardcoded 字符串测试断言**(若改版本号必同步):
   - `tests/test_fcop/test_rules.py` 里 `assert "vX.Y.Z 摘要" in intro` 一行
   - `tests/test_fcop_mcp/test_server.py` 里若有 `"vX.Y.Z 摘要"` 断言
   - `mcp/src/fcop_mcp/server.py` 里若 `init_*` 工具回执的 prompt 里写死
     了 "尤其是 vX.Y.Z 摘要那一段)"
- [ ] `docs/MIGRATION-*.md` 若本版本影响某段迁移指引,在"版本差异"加一行
- [ ] 每份 ADR `Status: Accepted`(不能带着 `Proposed` 的 ADR 发版)

### D. Git

- [ ] `main` 分支干净:`git status` 无未提交变更
- [ ] 所有发版相关 commit 已 merge 进 `main`
- [ ] `git log origin/main..HEAD` 为空(本地 = 远端)

### E. P=E 同步(协议-环境一致性) / Protocol-Environment Sync

**v1.6.0 新增,发 tag 前最后一步**。`fcop` 包内带的协议规则文件(权威源)和
项目根 / `.cursor/rules/` 下部署的副本(运行时环境)必须 byte-identical。

- [ ] `fcop_report()` 底部对比"项目本地版本"与"包内版本",**无版本漂移警告**
- [ ] **优先**:ADMIN 在 IDE 聊天里调 MCP 工具:

      ```text
      请调 redeploy_rules(force=True, archive=True)
      ```

      工具会覆盖四份目标文件,旧文件归档到 `.fcop/migrations/<时间戳>/rules/`

- [ ] **降级路径**(MCP server 跑旧 wheel 时):若 `fcop_report()` 显示 MCP
      server 在跑旧 `fcop@X.Y.Z`、而本仓库源码已是新版,`redeploy_rules()`
      反而会把规则**回退**到旧版本。这时**绕过 MCP 工具**,直接从本地源码
      调 Python API:

      ```powershell
      py -3.10 -c "from pathlib import Path; from fcop.project import Project; print(Project(Path(r'D:\FCoP')).deploy_protocol_rules(force=True, archive=True))"
      ```

      跑完后再调一次 `fcop_report()` 确认版本数字与包内一致

- [ ] 部署后**四份文件**(`.cursor/rules/fcop-rules.mdc` +
      `.cursor/rules/fcop-protocol.mdc` + `AGENTS.md` + `CLAUDE.md`)
      `git diff` 检查,确认确实更新了(若内容已经一致,deploy 是 no-op,
      `git diff` 为空也 OK)
- [ ] commit 这次 redeploy,作为发版 sprint 的一部分进 `main`

### F. Rule 0.a.1 闭环载体 / Rule 0.a.1 Carrier

发版本身就是一项工作 → 必须落文件(Rule 0.a.1)。**v1.6.0 起强制**。

- [ ] 已在 `fcop/tasks/` 下落 `TASK-<date>-<seq>-ADMIN-to-<role>-release-<x>-<y>-<z>.md`
   - `risk_level: irreversible`(PyPI 发布不可逆)
   - 写明本次发版的范围、ADR 引用、回滚预案
   - 因 `irreversible`,`write_task` MCP 工具会自动生成 `decision=needs_human`
     的 REVIEW,等 ADMIN `mark_human_approved(review_id)` 才放行执行
- [ ] 发版完成后准备好 `REPORT-<同日期>-<同seq>-<role>-to-ADMIN-release-*.md`
      模板,留到第 4 阶段填实际产物链接

---

## 发布步骤 / Release Steps

### 阶段 1:本地验证 / Local Verify (不上传)

```powershell
# 清理旧产物
Remove-Item -Recurse -Force dist, build, mcp\dist, mcp\build -ErrorAction SilentlyContinue

# 构建两个包
py -3.10 -m build
Push-Location mcp; py -3.10 -m build; Pop-Location

# 元数据合法性
py -3.10 -m twine check dist\* mcp\dist\*
# 期望: PASSED PASSED PASSED PASSED  (四份产物)

# 干净 venv 试装验证 — 关键,这一步抓 packaging 错误
$test = "$env:TEMP\fcop-install-test-$(Get-Date -Format yyyyMMddHHmmss)"
py -3.10 -m venv $test
& "$test\Scripts\pip.exe" install (Get-ChildItem dist\fcop-*.whl).FullName
& "$test\Scripts\pip.exe" install (Get-ChildItem mcp\dist\fcop_mcp-*.whl).FullName

# 关键:清空 PYTHONPATH,否则会从 src/ 而不是装好的 wheel 里 import
$env:PYTHONPATH = ""
& "$test\Scripts\python.exe" -c "import fcop, fcop_mcp; print(fcop.__version__, fcop_mcp.__version__)"
& "$test\Scripts\fcop-mcp.exe" --help
```

POSIX 等价:把 `Remove-Item` 换成 `rm -rf`、venv 路径换成 `/tmp/...`、可执行
后缀去掉 `.exe`,逻辑完全一致。

### 阶段 2:TestPyPI(仅 RC 或 dev 版本) / TestPyPI (RC only)

正式版**不**走本阶段。RC 版本时:

```bash
py -3.10 -m twine upload --repository testpypi dist/* mcp/dist/*

pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            fcop-mcp==1.7.0rc1
fcop-mcp --help
```

`extra-index-url` 必加:`fcop-mcp` 依赖 `fastmcp` 和 `pyyaml`,TestPyPI 上
可能没有,得允许 fallback 到真 PyPI。

### 阶段 3:tag push 触发 release.yml / Tag Push Triggers Automation

**这是发版主路径**。本地不再手动 `twine upload`——一切交给
`.github/workflows/release.yml`。

```powershell
# ADMIN 在 IDE 聊天里给出"Rule 7 二次确认 go"之后:

# 1. annotated tag (推荐用 -F 走文件,避免 shell 转义问题)
git tag -a v1.7.0 -F .scratch\_v1_7_0_tag_msg.txt

# 2. 先 push tag (触发自动化),再 push main (commits 跟上)
git push origin v1.7.0
git push origin main
```

`release.yml` 自动跑 **5 个 job**(顺序):

| Job | 内容 | 失败处理 |
|---|---|---|
| 1. verify | tag 版本号 = `_version.py` = CHANGELOG 章节标题 | 修 → bump 到下一版号重试 |
| 2. build | 双包 wheel + sdist + `twine check` + smoke install | 同上 |
| 3. publish-fcop | 用 `PYPI_TOKEN_FCOP` 上传 `fcop` | tag 留着,版号占坑 → bump 重试 |
| 4. publish-fcop-mcp | 上传 `fcop-mcp`(依赖 step 3 成功) | 同上 |
| 5. github-release | 从 CHANGELOG 抽取本版本内容,创建带附件的 Release | 可手工补 |

正常 3–5 分钟全跑完。可在 Actions UI 看实时日志。

**Dry run**:Actions UI 用 `workflow_dispatch` 手动触发,勾 `dry_run=true`,
只 build + twine check,不发 PyPI 也不建 Release。

### 阶段 4:发布后验证 + Rule 0.a.1 闭环 / Post-Release & Closure

```powershell
# 1. PyPI JSON API(比 pip 索引更早可见,通常 release.yml 完成后立即可查)
Invoke-RestMethod https://pypi.org/pypi/fcop/json | Select-Object -ExpandProperty info | Select-Object version
Invoke-RestMethod https://pypi.org/pypi/fcop-mcp/json | Select-Object -ExpandProperty info | Select-Object version

# 2. GitHub Release 检查
gh release view v1.7.0

# 3. 等 CDN 传播(通常 1–5 分钟)后,干净 venv 公网装 — 终极验证
$verify = "$env:TEMP\fcop-pypi-verify-1.7.0"
py -3.10 -m venv $verify
$env:PYTHONPATH = ""
& "$verify\Scripts\pip.exe" install --no-cache-dir fcop==1.7.0 fcop-mcp==1.7.0
& "$verify\Scripts\python.exe" -c "import fcop, fcop_mcp; from fcop.rules import get_rules_version; print(fcop.__version__, fcop_mcp.__version__, get_rules_version())"
```

**已知现象**:`release.yml` 成功后立即跑 `pip install` 可能找不到新版本号
——是 PyPI **CDN 传播延迟**,通常 1–5 分钟。PyPI JSON API 比 pip 索引更早可
见。`fcop@1.6.0` 实战记录显示 ~5 分钟全网可拉。

**Rule 0.a.1 闭环**(必走):

- [ ] 把准备好的 `REPORT-*.md` 填实(发版主刀 / 实际 commit hash / 5 个 job
      结果 / 已知非阻塞项 / CDN 传播时间)落到 `fcop/reports/`
- [ ] `Move-Item` 把 `TASK-*.md` 移到 `fcop/log/tasks/`、`REPORT-*.md` 移到
      `fcop/log/reports/`(`archive_task(task_id)` MCP 工具也可,但 v1.6.0
      实战是手动 `Move-Item` + `git add -A`,因为 git 会自动识别 rename)
- [ ] `git add -A && git commit -F .scratch\_release_*_closure_msg.txt`
- [ ] `git push origin main`
- [ ] 至此 Rule 0.a.1 四步全闭环

---

## 常见故障与回滚 / Common Failures & Rollback

### 问题 1:PyPI 上传后才发现 bug

PyPI **不允许同版本号重新上传**。处置:

1. 立刻 bump 到下一个 patch(`1.7.0` → `1.7.1`)
2. 修 bug → 走完发布前 6 段检查清单
3. 重新 tag push 触发 `release.yml`
4. **如果问题严重**,用 `yank` 把坏版本标红(不是删除,只是警告别装):

   ```bash
   py -3.10 -m twine yank fcop-mcp==1.7.0 --reason "packaging bug, use 1.7.1"
   ```

### 问题 2:CI 全绿但本地 build 失败 / Local build fails

常见原因:

- `pyproject.toml` 的 `[tool.hatch.build.targets.wheel].include` 漏了数据文件
  (`_data/teams/*.json`、`_data/letter-to-admin.*.md`)
- hatchling 的 `dynamic = ["version"]` 与 `_version.py` 路径不一致
- Python 3.10 兼容性(`from __future__ import annotations` 漏了、用了
  Python 3.11+ 的 `tomllib`)

检查 wheel 里实际装了什么:

```bash
py -3.10 -m zipfile -l dist/fcop-1.7.0-py3-none-any.whl
```

### 问题 3:MCP server 跑旧 wheel,`redeploy_rules()` 反而回退规则

**v1.6.0 实战发现**。`fcop-mcp` 的 server 进程是用某个时刻的 `fcop` wheel
启的,中间 `pip install -e .` 升级本地源码并**不会**更新已经在跑的 MCP
server。直接调 `redeploy_rules()` 会用 server 进程内的旧规则覆盖项目里的新
规则。

**应对**:绕过 MCP 工具,直接从本仓库源码调 Python API:

```powershell
py -3.10 -c "from pathlib import Path; from fcop.project import Project; print(Project(Path(r'D:\FCoP')).deploy_protocol_rules(force=True, archive=True))"
```

跑完后 `git diff .cursor/rules/ AGENTS.md CLAUDE.md` 应看到协议规则更新到
最新版本。

### 问题 4:`release.yml` `verify` job 在几十秒内失败

- **现象**:tag 推上去后,`Verify` job 报 `_version.py` 里版本与 tag 不一
  致,**约半分钟内失败**,尚未进入 build。
- **历史原因**(已修):旧脚本用 `grep` 取「文件中**第一个**双引号子串」;
  `src/fcop/_version.py` 注释里含有 `"semver 承诺"`,会先于
  `__version__ = "0.6.x"` 被匹配。
- **现行为**:从 `^__version__` 行解析(与 `mcp/.../_version.py` 一致)。
  若仍失败,先看日志里是 CHANGELOG 缺节还是别的问题。

### 问题 5:GitHub Actions Node.js 20 弃用警告

**遗留项,2026-06-02 前必修**。`release.yml` 里 `actions/checkout@v4` 等
action 内部用 Node.js 20,GitHub 已宣布 Node 20 弃用。升级到 Node 24 兼容版
本(关注 `actions/checkout@v5` 或同等 release)。

### 问题 6:PyPI 上看到版本号、`pip install` 找不到

CDN 传播延迟,通常 1–5 分钟。期间 PyPI JSON API
(`https://pypi.org/pypi/fcop/json`)已能看到新版本,但 `pip install` 走
的索引可能还是旧缓存。等几分钟再试,或加 `--no-cache-dir`。
**不是发版失败**,无需任何操作。

---

## 一次完整发版的命令序列 / End-to-End Command Sequence

(假定下次发 `1.7.0`,所有清单已 ✅,Rule 0.a.1 carrier TASK 已落)

```powershell
cd D:\FCoP

# Phase 1: local verify
Remove-Item -Recurse -Force dist, build, mcp\dist, mcp\build -ErrorAction SilentlyContinue
py -3.10 -m build
Push-Location mcp; py -3.10 -m build; Pop-Location
py -3.10 -m twine check dist\* mcp\dist\*

# Phase 1.5: smoke install
$smoke = "$env:TEMP\fcop-smoke-1.7.0"
py -3.10 -m venv $smoke
& "$smoke\Scripts\pip.exe" install (Get-ChildItem dist\fcop-*.whl).FullName
& "$smoke\Scripts\pip.exe" install (Get-ChildItem mcp\dist\fcop_mcp-*.whl).FullName
$env:PYTHONPATH = ""
& "$smoke\Scripts\python.exe" -c "import fcop, fcop_mcp; print(fcop.__version__, fcop_mcp.__version__)"

# Phase 2: P=E sync (最后一刻)
py -3.10 -c "from pathlib import Path; from fcop.project import Project; print(Project(Path(r'D:\FCoP')).deploy_protocol_rules(force=True, archive=True))"
git add -A
git commit -F .scratch\_release_1_7_0_predeploy_msg.txt

# Phase 3: ADMIN 二次确认(Rule 7) + tag push + release.yml automation
git tag -a v1.7.0 -F .scratch\_v1_7_0_tag_msg.txt
git push origin v1.7.0
git push origin main
# → GitHub Actions release.yml 自动跑 5 job,3–5 分钟

# Phase 4: 公网验证 + Rule 0.a.1 closure
Invoke-RestMethod https://pypi.org/pypi/fcop/json | Select-Object -ExpandProperty info | Select-Object version
gh release view v1.7.0
# 等 5 分钟左右
$verify = "$env:TEMP\fcop-pypi-verify-1.7.0"
py -3.10 -m venv $verify
$env:PYTHONPATH = ""
& "$verify\Scripts\pip.exe" install --no-cache-dir fcop==1.7.0 fcop-mcp==1.7.0

# 写 REPORT + archive + closure commit + push
# (按 Rule 0.a.1 闭环段)
```

---

## 自动化路线图 / Automation Roadmap

### 已实现 / Done

**GitHub Actions `release.yml`**(`.github/workflows/release.yml`):
tag `v*` push 触发,5 个 job 见阶段 3 表格。

### 待办 / TODO

1. **PyPI Trusted Publishing (OIDC)**:取代两个 `PYPI_TOKEN_*` secret,
   用 GitHub Actions 的 OIDC 身份直接发布,进一步降低凭据面
2. **CHANGELOG lint as a PR gate**:PR 里改 `_version.py` 必须伴随 CHANGELOG
   条目
3. **Release checksum/provenance**:在 Release 页面发 SHA-256、sigstore 签名
4. **Pre-release lint extension**:把发布前检查清单 C 段的"3 处 hardcoded
   字符串"做成一个 `tools/check_release_docs.py`,CI 里跑,避免下次人肉漏看
5. **Node 24 升级**(2026-06-02 前)
6. **PEP 621 + 旧 `Home-page` 字段双写**:当前 `pyproject.toml` 用 PEP 621
   `[project.urls] Homepage = ...`,PyPI 网页 / `pip show` 都能解析;但
   **PyCharm "可用软件包" 对话框等老 UI** 只读旧 `Home-page:` core metadata
   字段,所以两个包的列表里看不到主页链接。修法:在 hatchling 配置里
   `[tool.hatch.metadata.hooks.custom]` 显式补一行 `Home-page` 字段;或迁
   到 setuptools(默认就会双写)。**优先级低**——只是 IDE 的 UX 细节,
   PyPI / pip 一切正常

---

## 参考 / References

- [PEP 440 — Version specifiers](https://peps.python.org/pep-0440/)
- [PyPA packaging guide](https://packaging.python.org/en/latest/)
- [twine docs](https://twine.readthedocs.io/en/stable/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [ADR-0002](../adr/ADR-0002-package-split-and-migration.md) — 包拆分策略
- [ADR-0003](../adr/ADR-0003-stability-charter.md) — 稳定性宪章(SemVer 法律基础)
- [ADR-0033](../adr/ADR-0033-filename-trailing-slug.md) — 文件名 trailing-slug 语法
- v1.6.0 实战完整记录:`fcop/log/tasks/TASK-20260512-009-*.md` +
  `fcop/log/reports/REPORT-20260512-009-*.md`

**最终用户**升级两个 PyPI 包,见 [升级说明](./upgrade-fcop-mcp.md)。
