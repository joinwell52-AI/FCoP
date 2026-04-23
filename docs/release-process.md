# FCoP 发布流程

> 面向 **fcop / fcop-mcp 的维护者**。  
> 终端用户不需要读本文；看 [MIGRATION-0.6.md](./MIGRATION-0.6.md) 或 [README](../README.md) 即可。

---

## 核心约束

1. **两个包必须同版本号齐发**（`fcop 0.6.2` 和 `fcop-mcp 0.6.2`，不能只发一个）——见 [ADR-0002](../adr/ADR-0002-package-split-and-migration.md)
2. **稳定性宪章一票否决**（[ADR-0003](../adr/ADR-0003-stability-charter.md)）：如果 snapshot 改了、CHANGELOG 没标注，发布要被 CI 挡下
3. **发布即不可逆**（PyPI 禁止同版本号覆盖）：一旦 `twine upload` 成功，该版本号永久占坑

---

## 版本号规则

遵循 [Semantic Versioning 2.0](https://semver.org/spec/v2.0.0.html)：

```
MAJOR.MINOR.PATCH[rcN|devN]
```

| 场景 | 示例 |
|---|---|
| pre-1.0 的主开发版本 | `0.6.0`, `0.6.1` |
| RC（候选发布，允许装但不推） | `0.6.0rc1` |
| 开发快照（仅本地 / CI） | `0.6.0.dev0` |
| 正式版 | `0.6.0` |

**硬规则**（ADR-0003 派生）：

- `0.6.N` 之间**任意向后兼容**（patch 或 minor 内加 tool / 加字段都 OK）
- `0.6.N` → `0.7.0` 才允许破坏性变更，且必须走 deprecation cycle

---

## 发布前检查清单

### A. 代码层

- [ ] `src/fcop/_version.py` 版本号 bump 到目标（如 `__version__ = "0.6.0rc1"`）
- [ ] `mcp/src/fcop_mcp/_version.py` 同步 bump
- [ ] `mcp/pyproject.toml` 的 `fcop>=A.B,<A.(B+1)` 依赖约束对得上
- [ ] `pyproject.toml` / `mcp/pyproject.toml` 其它元数据正确（classifiers, python_requires）

### B. 测试 & CI

- [ ] `py -3.10 -m pytest tests/test_fcop` 全绿
- [ ] `py -3.10 -m pytest tests/test_fcop_mcp` 全绿
- [ ] `py -3.10 -m ruff check .` 全绿
- [ ] `py -3.10 -m mypy src tests` 全绿
- [ ] `py -3.10 -m pip_audit` 无高危
- [ ] GitHub Actions workflow `test-fcop.yml` 和 `test-fcop-mcp.yml` 最近一次主干 run 是绿的
- [ ] `public_surface.json` / `tool_surface.json` 两份 snapshot 与 `git status` 一致（没有未提交 diff）

### C. 文档层

- [ ] `CHANGELOG.md` 里把 `[Unreleased]` 标题改成 `[0.6.0rc1] - YYYY-MM-DD`
- [ ] CHANGELOG 新版块下必须至少包含：
   - 新增的每个 public API → 对应 `Added`
   - 每个 signature/behavior 变化 → 对应 `Changed`（必须 additive / 或已有 deprecation cycle）
   - 每个 deprecation → 对应 `Deprecated` + 计划移除版本
- [ ] `docs/MIGRATION-0.6.md` 如果有本版本影响的条目，在"版本差异"小节加一行
- [ ] 每份 ADR 都已 `Status: Accepted`（不能带着 Proposed 的 ADR 发版）
- [ ] README.md 的 Quick Start 和 Install 段落与新版本号一致

### D. Git

- [ ] `main` 分支干净：`git status` 无未提交变更
- [ ] 所有要发布的 commit 已 merge 进 `main`
- [ ] `git log origin/main..HEAD` 为空（本地和远端一致）

---

## 发布步骤

### 阶段 1：本地验证（不上传）

```bash
# 清理旧产物
rm -rf dist/ build/ mcp/dist/ mcp/build/

# 构建 fcop
py -3.10 -m build
# 构建 fcop-mcp
cd mcp && py -3.10 -m build && cd ..

# 查看产物
ls dist/ mcp/dist/
# 应该各自有:
#   dist/fcop-0.6.0rc1.tar.gz
#   dist/fcop-0.6.0rc1-py3-none-any.whl
#   mcp/dist/fcop_mcp-0.6.0rc1.tar.gz
#   mcp/dist/fcop_mcp-0.6.0rc1-py3-none-any.whl

# 干净 venv 试装验证（关键 — 这一步抓 packaging 错误）
py -3.10 -m venv /tmp/fcop-install-test
/tmp/fcop-install-test/bin/pip install dist/fcop-0.6.0rc1-py3-none-any.whl
/tmp/fcop-install-test/bin/pip install mcp/dist/fcop_mcp-0.6.0rc1-py3-none-any.whl
/tmp/fcop-install-test/bin/python -c "import fcop; print(fcop.__version__)"
/tmp/fcop-install-test/bin/python -c "import fcop_mcp; print(fcop_mcp.__version__)"
/tmp/fcop-install-test/bin/fcop-mcp --help
```

Windows 等价（PowerShell）：

```powershell
Remove-Item -Recurse -Force dist, build, mcp/dist, mcp/build -ErrorAction SilentlyContinue
py -3.10 -m build
Push-Location mcp; py -3.10 -m build; Pop-Location
py -3.10 -m venv $env:TEMP\fcop-install-test
& "$env:TEMP\fcop-install-test\Scripts\pip.exe" install (Get-ChildItem dist\fcop-*.whl).FullName
& "$env:TEMP\fcop-install-test\Scripts\pip.exe" install (Get-ChildItem mcp\dist\fcop_mcp-*.whl).FullName
& "$env:TEMP\fcop-install-test\Scripts\python.exe" -c "import fcop, fcop_mcp; print(fcop.__version__, fcop_mcp.__version__)"
```

### 阶段 2：上传到 TestPyPI（RC 或 dev 版本必做）

```bash
py -3.10 -m twine upload --repository testpypi dist/* mcp/dist/*
```

然后从 TestPyPI 装一遍，再跑一遍冒烟：

```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            fcop-mcp==0.6.0rc1
fcop-mcp --help
```

**为什么需要 extra-index-url**：`fcop-mcp` 依赖 `fastmcp` 和 `pyyaml`，这些在 TestPyPI 上可能没有，得允许 fallback 到真 PyPI。

### 阶段 3：上传到 PyPI（仅正式版或允许对外公布的 RC）

```bash
py -3.10 -m twine upload dist/* mcp/dist/*
```

**上传顺序**：先 `fcop` 再 `fcop-mcp`。因为 `fcop-mcp` 依赖 `fcop>=0.6,<0.7`，`fcop` 不在 PyPI 上的话 `pip install fcop-mcp` 会失败。

### 阶段 4：打 Git 标签

```bash
git tag -a v0.6.0rc1 -m "Release 0.6.0rc1"
git push origin v0.6.0rc1
```

**标签命名约定**：`vMAJOR.MINOR.PATCH[preN]`，RC 用 `v0.6.0rc1`（没有点号连接 `rc1`，和 Python 版本号对齐）。

### 阶段 5：GitHub Release（仅正式版）

在 GitHub 仓库页面打开 Releases → Draft a new release：

- Tag: 选择刚推的 `v0.6.0rc1`
- Release title: `fcop & fcop-mcp 0.6.0rc1`
- Description: 直接贴 CHANGELOG 对应版本的内容
- Pre-release: **RC 版本勾选**，正式版不勾

---

## 发布后验证

```bash
# 从真 PyPI 装一个全新环境
py -3.10 -m venv /tmp/verify-release
/tmp/verify-release/bin/pip install fcop-mcp==0.6.0rc1

# 验证二者版本号都对
/tmp/verify-release/bin/python -c "import fcop, fcop_mcp; print(fcop.__version__, fcop_mcp.__version__)"

# 启动 MCP 服务器（不会真连 transport，但会 import 所有 tool）
/tmp/verify-release/bin/fcop-mcp --help
```

---

## 常见故障与回滚

### 问题：PyPI 上传后才发现 bug

PyPI **不允许同版本号重新上传**。只能：

1. 立刻 bump 到下一个 patch 版本（`0.6.0rc1` → `0.6.0rc2` 或 `0.6.0`）
2. 修 bug
3. 重新走发布流程
4. 如果问题严重，用 `pip install` 的 `yank` 能力把坏版本标红（不是删除，只是警告用户别装）：
   ```bash
   pip install twine
   py -3.10 -m twine yank fcop-mcp==0.6.0rc1 --reason "packaging bug, use 0.6.0rc2"
   ```

### 问题：CI 全绿但本地 build 失败

常见原因：

- `MANIFEST.in` 或 `pyproject.toml.include` 漏了数据文件（`_data/teams/*.json`）
- hatchling 的 `dynamic = ["version"]` 与 `_version.py` 路径不一致
- Python 3.10 兼容性（`from __future__ import annotations` 漏了）

检查 wheel 里实际装了什么：
```bash
py -3.10 -m zipfile -l dist/fcop-0.6.0rc1-py3-none-any.whl
```

---

## 自动化路线图

### 已实现（0.6.0 之后）

**GitHub Actions `release.yml`**（`.github/workflows/release.yml`）：tag `v*` push 触发，自动完成：

1. **verify**：校验 tag 版本号 = `_version.py` 版本号 = CHANGELOG 章节标题
2. **build**：构建两个包的 wheel + sdist，`twine check`，干净 venv smoke install
3. **publish-fcop**：用 `secrets.PYPI_TOKEN_FCOP`（project-scoped）上传 fcop
4. **publish-fcop-mcp**：上传 fcop-mcp（依赖前一步成功，保证 PyPI 上 fcop 先就位）
5. **github-release**：从 CHANGELOG 自动抽取本版本内容，创建带附件的 Release

**触发方式**：

```bash
# 本地 bump 版本号、CHANGELOG、commit
git tag -a v0.6.1 -m "Release 0.6.1"
git push origin v0.6.1
# → Actions 自动接管，通常 3–5 分钟完成全流程
```

**Dry run**：在 Actions UI 用 `workflow_dispatch` 手动触发，勾 `dry_run=true`，只 build + twine check，不发 PyPI 也不建 Release。

**如果失败**：tag 留着但 PyPI 版本号没占用，修好再 tag `v0.6.N+1` 重试即可（PyPI 不允许重用版本号，所以同版本号重试没戏）。

### 待办

1. **PyPI Trusted Publishing (OIDC)**：取代两个 `PYPI_TOKEN_*` secret，用 GitHub Actions 的 OIDC 身份直接发布。进一步降低凭据面。
2. **CHANGELOG lint as a PR gate**：PR 里改 `_version.py` 必须伴随 CHANGELOG 条目。
3. **Release checksum/provenance**：在 Release 页面发 SHA-256、sigstore 签名。

---

## 参考

- [PEP 440 — Version specifiers](https://peps.python.org/pep-0440/)
- [PyPA packaging guide](https://packaging.python.org/en/latest/)
- [twine docs](https://twine.readthedocs.io/en/stable/)
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [ADR-0002](../adr/ADR-0002-package-split-and-migration.md) — 本仓库的包拆分策略
- [ADR-0003](../adr/ADR-0003-stability-charter.md) — 稳定性宪章（版本号承诺的法律基础）
