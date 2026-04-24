# ADR-0002: Package Split（`fcop` + `fcop-mcp`）& 0.5 → 0.6 Migration

- **Status**: Accepted
- **Date**: 2026-04-22
- **Deciders**: ADMIN
- **Related**: [ADR-0001](./ADR-0001-library-api.md)（库 API 契约）

> **读者注意**：文内出现的 `codeflow-pwa`、`codeflow-plugin` 等专名是**迁移当时**的仓库与路径记录，用于历史追溯；**不是**当前 FCoP 主仓对外的品牌口径。

## ADMIN 决议（2026-04-22）

ADMIN 针对本 ADR 的关键决策已拍板：

1. **迁移策略 = 方案 A 硬切**，不做 shim、不保留 `fcop` CLI 转发（理由：还
   没真用户，不值得为零个潜在用户维持 shim 维护成本）
2. **`bridgeflow` 不处理**：不发 deprecated 占位版，不改 README，保留 PyPI
   2026-04-03 的最后一版现状不动
3. **独立仓库 `joinwell52-AI/FCoP` 已经创建**（具体初始化步骤见下面
   Decision / New Repository Initialization 一节）
4. **版本独立递增 + 1.0 对齐**：0.6.x / 0.7.x / 0.8.x / 0.9.x 期间
   `fcop` 与 `fcop-mcp` 各走各的 minor / patch；1.0 作为一次性版本对齐锚
   点，`fcop 1.0.0` 与 `fcop-mcp 1.0.0` 同日发布；之后再次允许漂移
5. **PyPI 包归位**：当前 `fcop`（0.5.4，内容是 MCP 服务器）从 0.6.0 起改
   为库，把 MCP 服务器代码迁到 `fcop-mcp`（当前是空占位）里重新发布
6. **责任划分**：ADR-0001 的库 API 文档由 ADMIN 审阅；测试体系 / 用户迁移
   指南（`MIGRATION-0.6.md`）/ 发布流程文档（`docs/release-process.md`）
   由执行 AI 负责

以上决议生效，本 ADR 从 Proposed 升格为 Accepted。

## Context

### PyPI 上的三个名字

截至 2026-04-22，ADMIN 在 PyPI 名下有三个相关的包名：

| PyPI 名 | 最后发布 | 当前内容 | 预期定位 |
|---|---|---|---|
| `fcop` | 2026-04-22（0.5.4）| **MCP 服务器**（误占库名）| 纯协议 SDK（库）|
| `fcop-mcp` | 2026-04-21（占位空包）| — | MCP 服务器壳 |
| `bridgeflow` | 2026-04-03 | 上古遗留（前身名称）| 保持现状，不处理 |

**问题**：`fcop` 这个名字目前装的是错的东西。按 ADR-0001 的定位，
`fcop` 应该是"`import fcop` 就能用的协议库"，但 0.5.4 装上之后给你的是
一个 stdio MCP 服务器和一个 `fcop` 命令——跟"库"相去甚远。

### `bridgeflow` 的来历

`bridgeflow` 是 FCoP 更早的命名。从当前 workspace 路径 `D:\Bridgeflow\` 和
描述"基于文件的多AI代理协作桥接器（移动管理+PC执行+光标代理）"可以看出，
那是"CodeFlow"之前的名字。后来经过一轮命名迭代变成 CodeFlow，再抽出
FCoP 协议本身，`bridgeflow` 就被遗忘在 PyPI。

### 0.5.x 的用户基数

ADMIN 多次确认："还没真用户"。这意味着 0.5 → 0.6 的破坏性迁移可以**硬切**
而不用顾虑兼容 shim。`fcop 0.5.4` 的 PyPI 周下载量应基本为零（除了构建机
和 ADMIN 自己）。

### codeflow 品牌污染

当前 `fcop 0.5.4` 的外部表面多处指向 `codeflow-pwa` 仓库：

- `pyproject.toml` 的 Homepage / Repository / Issues
- `.cursor-plugin/plugin.json` 的 homepage / repository
- `README.md` 的 install script URL（`codeflow-pwa/main/codeflow-plugin/...`）
- `README.md` 的本地开发命令 `pip install -e codeflow-plugin`
- `scripts/install-fcop.{ps1,sh}` 注释

FCoP 是独立协议，CodeFlow 只是"某个使用 FCoP 的应用"。这些外链和路径让
fcop 的品牌和某个下游产品耦合，是错位。独立仓库是治本之举。

### 为什么不直接"改现有 fcop 包的内容，不搞 fcop-mcp"

理论上可以：0.6 把 `fcop` 包里的内容换成库，把 MCP 服务器代码删掉。但这样：

- 原来 `uvx fcop` 的用户装不到 MCP 了，功能下线
- MCP 这层价值不低（三个官方预设团队、自升级、22 个工具）不应该丢
- 既然 `fcop-mcp` 名字已经占好，就顺势用它——两个包职责清晰

## Decision

### 三个包的最终职责

```
┌────────────────────────────────────────────────────────────┐
│  fcop  (PyPI 包, 库)                                        │
│  ─────────────────────────────────                         │
│  • import fcop                                              │
│  • 纯 Python 协议 SDK                                       │
│  • 零 MCP 依赖, 零 LLM 依赖                                 │
│  • 约束见 ADR-0001                                          │
└────────────────────────────────────────────────────────────┘
           ▲
           │ depends on
           │
┌──────────┴─────────────────────────────────────────────────┐
│  fcop-mcp  (PyPI 包, MCP 服务器)                            │
│  ─────────────────────────────────                         │
│  • uvx fcop-mcp  /  python -m fcop_mcp                      │
│  • 薄壳: 把库的能力通过 FastMCP 暴露给 MCP 客户端           │
│  • 22 个 @mcp.tool + 10 个 @mcp.resource                    │
│  • 支持 FCOP_PROJECT_DIR / 中继桥接环境变量                 │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  bridgeflow  (PyPI 包, 保持现状不处理)                       │
│  ─────────────────────────────────                         │
│  • 不发新版本, 不改 README                                  │
│  • 理由: 没真用户, 不值得为 SEO 残影多维护一个包            │
│  • 以后若有人反馈用到它再议                                 │
└────────────────────────────────────────────────────────────┘
```

### 从 0.5 → 0.6 的硬切

**硬切原则**：

1. `fcop 0.5.4` 装的 MCP 服务器功能，0.6.0 起**整体搬到 `fcop-mcp`**，`fcop`
   里不留 MCP 代码，也不留 `fcop` CLI 入口（0.6.0 的 `fcop` 命令——见下）。
2. 不做弃用 shim。用户 `uvx fcop` 会得到库本身，没有 `main()`，执行会报
   `No module named 'fcop.__main__'` 之类的错——这是**刻意的**，引导他
   们读发布说明迁到 `fcop-mcp`。
3. 在 `fcop 0.6.0` README 和 PyPI 项目描述顶部**醒目位置**放"如果你原来
   装的是 0.5.x 的 MCP 服务器，请换成 `pip install fcop-mcp`"。
4. `fcop-mcp 0.6.0` README 顶部同样放一行"This is the MCP server shell.
   For the library, install `fcop`."

**ADMIN 已确认"还没真用户"**，因此不启动 shim 逻辑；否则应考虑方案 B
（`fcop 0.6.0` 保留一个 `main()` entry，打弃用警告然后转发到 `fcop-mcp`，
0.7.0 删除）。

### 仓库迁移：独立新仓库

0.6 的一切改动**全部发生在新仓库** `joinwell52-AI/FCoP`。

```
joinwell52-AI/FCoP/                 ← 新仓库, 仓库根 = Python 包源码根
├── README.md
├── README.zh.md
├── LICENSE                         ← MIT, 迁自 codeflow-plugin
├── CHANGELOG.md
├── pyproject.toml                  ← fcop 库本体
├── src/
│   └── fcop/                       ← 见 ADR-0001
│       ├── __init__.py
│       ├── _version.py
│       ├── core/
│       ├── models.py
│       ├── errors.py
│       ├── teams/
│       └── rules/
├── mcp/                            ← fcop-mcp 子包 (单仓库多包)
│   ├── pyproject.toml              ← fcop-mcp 的独立 pyproject
│   ├── README.md
│   └── src/
│       └── fcop_mcp/
│           ├── __init__.py
│           ├── __main__.py         ← python -m fcop_mcp
│           └── server.py           ← 22 个 tool, 10 个 resource
├── tests/
│   ├── test_fcop/                  ← 库的测试
│   └── test_fcop_mcp/              ← MCP 壳的测试
├── docs/
│   ├── adr/                        ← 迁自 private/fcop-repo/adr/
│   ├── spec/                       ← 迁自 private/fcop-repo/spec/
│   ├── essays/                     ← 迁自 private/fcop-repo/essays/
│   ├── primer/                     ← 迁自 private/fcop-repo/primer/
│   └── library-api.md              ← ADR-0001 的用户向 re-package
├── examples/
│   ├── library/
│   │   ├── hello_project.py
│   │   ├── anthropic_agent.py
│   │   └── openai_agent.py
│   └── mcp/
│       └── cursor-mcp.json
├── integrations/                   ← 迁自 private/fcop-repo/integrations/
├── scripts/
│   ├── install-fcop-mcp.ps1        ← 原 install-fcop.ps1, 改指向 fcop-mcp
│   └── install-fcop-mcp.sh
├── assets/                         ← 迁自 private/fcop-repo/assets/
├── .github/
│   ├── workflows/
│   │   ├── test-fcop.yml           ← 测库, 不装 fastmcp (硬约束)
│   │   ├── test-fcop-mcp.yml       ← 测 MCP 壳
│   │   ├── release-fcop.yml
│   │   └── release-fcop-mcp.yml
│   └── dependabot.yml
└── .gitignore
```

- 仓库根就是 `fcop` 库的 Python 包根
- `mcp/` 子目录是 `fcop-mcp` 包的独立发布源（单仓库多包）
- `docs/` 把 `private/fcop-repo/` 的非代码资产全部吸收
- **不再有 `codeflow` 任何痕迹**

### 老仓库的善后

`joinwell52-AI/codeflow-pwa` 在新仓库稳定之后：

1. **`codeflow-plugin/` 子目录保留，不删也不改**——它是 `fcop 0.5.4` 发布
   的那份代码的 pre-history archive。未来有人好奇 0.5.x 长什么样，来这里看
2. 保留 `web/pwa/`、`server/relay/`、`docs/`、`scripts/` 等真正属于 CodeFlow
   应用的东西
3. 在 `codeflow-pwa` 根 `README.md` 末尾加一行：FCoP 协议本身和它的 MCP
   插件已独立为 `joinwell52-AI/FCoP`，本仓库专注 CodeFlow PWA 和桥接服务
4. 如果 CodeFlow 本身未来需要用 FCoP，就走 `pip install fcop` 正常依赖路径

### 新仓库的初始化顺序（现实版）

**仓库 `joinwell52-AI/FCoP` 已于 2026-04 前建好**，不是空壳：

- 远端分支 `main`，头部 commit `7d2dba6`（"docs(readme): add essay 03"）
- 已有 14 个 commit 的协议文档历史（`spec/`、`essays/`、`primer/`、
  `integrations/`、`assets/`、`README.md`、`README.zh.md`、`LICENSE`、
  `.gitignore`）
- 本地 working copy 位置：`d:\Bridgeflow\private\fcop-repo\`

**因此不走 `git filter-repo`**。理由：

1. FCoP 仓库自己已经有独立的 commit 历史（14 个 commits，围绕协议文档
   演进），强行把 codeflow-plugin 的代码历史插进来会把时间线打乱
2. codeflow-plugin 的历史完整保留在 `joinwell52-AI/codeflow-pwa` 里，
   在 `CHANGELOG.md` 头部加一条 "pre-history reference"，直接链到老
   仓库对应 commit 即可满足可追溯性
3. 代码作为一次"clean import" commit 进来，是**刻意的断代**——强调
   `fcop 0.6.0` 是"首个作为独立项目的发布"

**实际走的步骤**：

```bash
# 0. 进入本地 working copy
cd d:\Bridgeflow\private\fcop-repo

# 1. 先把我已经写好的 adr/ 目录提交推送（当前未跟踪）
git add adr/
git commit -m "docs(adr): add ADR-0001 (library API) and ADR-0002 (package split)"
git push origin main

# 2. 新开分支做 0.6 的代码引入
git checkout -b feat/0.6-library-split

# 3. 在这个分支上:
#    - 新建 pyproject.toml (库)
#    - 从 codeflow-plugin/src/fcop/ 复制需要保留的代码到 src/fcop/
#      (纯粹 cp, 不保留 git blame/log, 在 commit message 里注明来源 commit)
#    - 按 ADR-0001 新写库的 Project/Task/Report 公共 API
#    - 新建 mcp/ 子目录, 放 fcop-mcp 的壳
#    - 新建 tests/
#    - 新建 .github/workflows/

# 4. 开 PR 回 main (这样 14→15→... 的 commit 线能看到"0.6 代码引入"那一跳)
```

**注：老仓库 `codeflow-pwa` 的 `codeflow-plugin/` 子目录不删、不改**。
保留它的 0.5.4 最终态作为"pre-history archive"。新仓库的 `CHANGELOG.md`
顶部链过去即可。

### 双包的依赖关系

`mcp/pyproject.toml`（`fcop-mcp` 的）：

```toml
[project]
name = "fcop-mcp"
dynamic = ["version"]
description = "FastMCP server exposing fcop's Project/Task/Report API to MCP clients."
requires-python = ">=3.10"
dependencies = [
    "fcop >=0.6,<0.7",
    "fastmcp >=3.2.0",
    "websockets >=12.0",
]

[project.scripts]
fcop-mcp = "fcop_mcp.__main__:main"
```

版本策略：**独立递增**。

- `fcop 0.6.0` 与 `fcop-mcp 0.6.0` **首发日对齐**
- 之后 bugfix 各自独立发 patch（`fcop 0.6.1`、`fcop-mcp 0.6.3` 都可能发生）
- `fcop-mcp` 的依赖范围 `>=0.6,<0.7`，兼容 0.6.x 任何版本
- 0.7 到来时，`fcop-mcp 0.7.0` 跟着发，把依赖范围升到 `>=0.7,<0.8`
- **1.0 作为一次"版本对齐锚点"**：届时 `fcop 1.0.0` 与 `fcop-mcp 1.0.0`
  同日发布，之后再次允许独立 minor/patch 漂移。1.0 是协议/API/服务器三方
  stable 宣告点，对齐这次版本号是对外信号。

**发布顺序硬约束**：`fcop` 先发，`fcop-mcp` 后发。理由是 `fcop-mcp` 在
PyPI `twine upload` 时，`fastmcp` 能从 PyPI 先解析 `fcop` 的依赖；否则
`fcop-mcp` 发出去但依赖的 `fcop` 尚未可用，用户装会失败。

CI 用一个 workflow 串联：

```yaml
# .github/workflows/release-all.yml (触发条件: tag v*)
jobs:
  release-fcop:
    # 构建 fcop, twine upload
  release-fcop-mcp:
    needs: release-fcop
    # 等 fcop 发布完再构建 fcop-mcp
```

### `bridgeflow` 的处理

**不处理**。PyPI 上保持 2026-04-03 最后一版的现状不变。

理由：

- ADMIN 确认"还没真用户"；既然没人装 bridgeflow，发 deprecated 占位版的价值
  等于零
- PyPI 的 SEO 上，`bridgeflow` 会自然沉下去；新用户搜"file-based agent
  protocol"找到的是 `fcop` / `fcop-mcp`
- 多维护一个包等于多一份发布流程 / 密钥轮换 / CI 负担，为了"照顾可能存在
  的零个用户"不值得
- 未来若真的有人反馈"我在用 bridgeflow"，再议（届时至少知道有真实用户了）

## Design Details

### 用户侧迁移对照表

#### 原来装的是 `fcop 0.5.x` 做 MCP 服务器

**0.5.x 配置**：

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop"]
    }
  }
}
```

**0.6.0 配置**（唯一变化：`fcop` → `fcop-mcp`）：

```json
{
  "mcpServers": {
    "fcop": {
      "command": "uvx",
      "args": ["fcop-mcp"]
    }
  }
}
```

`mcpServers.fcop` 这个**键名可以保留**——Cursor 不认 key 名，只认
`command` + `args`。保留旧 key 名能避免重开命名混乱。

#### 原来用 `pip install fcop` 然后 `python -m fcop`

```bash
# Before (0.5.x)
pip install fcop
python -m fcop

# After (0.6.0)
pip install fcop-mcp    # ← 改这一行
python -m fcop_mcp      # ← 命令也改
```

#### 原来想"用 fcop 做开发"（0.5.x 时代没有稳妥做法）

```python
# Before (0.5.x) — 脏后门
from fcop.server import write_task  # 返回字符串, 依赖全局 PROJECT_DIR

# After (0.6.0) — 正经库 API
from fcop import Project
project = Project("/my/project")
task = project.write_task(sender="PM", recipient="DEV", priority="P1",
                          subject="...", body="...")
# 返回 Task dataclass, 实例级状态, 线程安全
```

#### install-fcop 脚本

`scripts/install-fcop-mcp.ps1`（原 `install-fcop.ps1` 改名）：

```powershell
# 安装 fcop-mcp (自动合并进 ~/.cursor/mcp.json)
# 脚本里 URL 从 codeflow-pwa/.../codeflow-plugin/scripts/install-fcop.ps1
# 改成 joinwell52-AI/FCoP/main/scripts/install-fcop-mcp.ps1
```

### 环境变量迁移

| 环境变量 | 0.5.x 行为 | 0.6.0 行为 |
|---|---|---|
| `FCOP_PROJECT_DIR` | 读取；未设时自动向上回溯 | **仅在 `fcop-mcp` 生效**；库 API 不读 |
| `CODEFLOW_PROJECT_DIR` | 兼容读取 + 弃用警告（0.4.1 开始）| **直接报错**："此变量已在 0.6 删除，请用 `FCOP_PROJECT_DIR`" |
| `FCOP_ROOM_KEY` | 桥接中继开关 | 仅 `fcop-mcp` 生效 |
| `FCOP_RELAY_WS_URL` | 桥接 WS URL | 仅 `fcop-mcp` 生效 |
| `FCOP_DEVICE_ID` | 本机 MCP 设备 ID | 仅 `fcop-mcp` 生效 |

**库 API 用户通过 `Project(path=...)` 参数注入路径**，不读任何环境变量。
这是 ADR-0001 的硬性约束。

### CI 的硬约束

`test-fcop.yml` 必须**刻意不装 fastmcp**：

```yaml
- name: Install fcop (library only)
  run: |
    pip install -e .
    # 故意不装 fastmcp 和 mcp
    pip show fastmcp && exit 1 || echo "Good: fastmcp not installed"

- name: Run library tests
  run: pytest tests/test_fcop/
```

这个检查保证了"`fcop` 库真的能在无 MCP 环境下独立工作"这个承诺是可验证的。
如果哪天有人不小心 `import fastmcp`，CI 立刻挂。

### 测试组织

```
tests/
├── conftest.py                     ← 共享 fixtures (tmp_path 下起的假项目)
├── test_fcop/
│   ├── test_project.py             ← Project 类的单元测试
│   ├── test_task_lifecycle.py
│   ├── test_report.py
│   ├── test_issue.py
│   ├── test_team_deploy.py
│   ├── test_validation.py          ← ProtocolViolation / ValidationError 路径
│   ├── test_filename_parsing.py
│   ├── test_frontmatter.py
│   ├── test_teams_module.py        ← fcop.teams
│   ├── test_rules_module.py        ← fcop.rules
│   └── test_errors.py              ← 异常体系
└── test_fcop_mcp/
    ├── test_tool_parity.py          ← 每个 MCP tool 的行为 vs 对应的库方法
    ├── test_resources.py
    └── test_env_handling.py         ← FCOP_PROJECT_DIR 等环境变量逻辑
```

覆盖率门槛：库 80%、MCP 壳 60%。（MCP 壳大部分是 FastMCP 装饰器和字符串
格式化，测不了也没必要。核心逻辑的覆盖都在库测试里完成。）

### 发布 checklist（取代现有 `docs/release-process.md`）

**每次 0.6.x 发布**：

1. `fcop`:
   - [ ] 改 `src/fcop/_version.py` 为新版本
   - [ ] `CHANGELOG.md` 写新条目
   - [ ] `git tag v0.6.N` 并 `git push --tags`
   - [ ] CI 自动触发 `release-fcop.yml` → `twine upload`
   - [ ] 验证 PyPI 上能看到新版
2. `fcop-mcp`（通常同日或隔日）：
   - [ ] 改 `mcp/src/fcop_mcp/_version.py` 为新版本
   - [ ] `CHANGELOG.md` 写新条目
   - [ ] `git tag v-mcp-0.6.N` 并 `git push --tags`（用 `v-mcp-` 前缀区分）
   - [ ] CI 自动触发 `release-fcop-mcp.yml` → `twine upload`
   - [ ] 验证 PyPI 上能看到新版，并且依赖的 `fcop` 版本已可用

**重要**：不用同一个 tag 同时发两个包。每个包一个独立的 tag prefix：
`v0.6.0` = fcop，`v-mcp-0.6.0` = fcop-mcp。

## Non-Goals

- **不**在 0.6 做 API/CLI 工具（`fcop` 命令做啥留给未来 ADR）
- **不**做 Rust / Go 绑定
- **不**做 relay server 的重构——0.5.x 的中继代码搬到 `fcop-mcp` 里，保持原样
- **不**在 0.6 改 FCoP 协议本身（`fcop-rules.mdc` 的 Rule 0-8 + 4.5）
- **不**动 `.cursor-plugin` 的 Cursor 插件元数据重大变化（只改 URL 和 version）

## Alternatives Considered

### Alt-1：单包 + extras

`fcop` 仍是一个包，`fcop[mcp]` extras 装 MCP 壳。

**否决原因**：

- `fcop-mcp` 名字已经占了，不用可惜
- extras 在 PyPI 搜索可见性差，很多用户不知道 extras 语法
- `uvx fcop[mcp]` 在 Cursor mcp.json 里的 `args` 写法不友好
- 两个 PyPI 条目搜索可见度各自独立，更容易被新用户找到

### Alt-2：保留 shim（软切）

`fcop 0.6.0` 继续有 `main()` entry，但只是打弃用警告后 `subprocess.run(["fcop-mcp"])` 转发。

**否决原因**：ADMIN 已确认"还没真用户"；软切增加代码复杂度且寿命只到 0.7。

### Alt-3：不拆新仓库

在 `codeflow-pwa/codeflow-plugin/` 内部做 0.6 改造。

**否决原因**：外链、URL、路径里的 `codeflow` 品牌污染是**硬约束**。
不拆仓库，codeflow 字眼根除不掉，PyPI 项目页 Homepage 仍指向 codeflow-pwa。

### Alt-4：monorepo 用 `pyproject.toml` 的 workspace 机制（uv / poetry）

让一个顶层 `pyproject.toml` 描述整个 monorepo，`fcop` 和 `fcop-mcp` 作为
workspace members。

**否决原因**：

- Python monorepo workspace 工具链还不成熟（uv 刚开始支持）
- 发布流程复杂度不降反升
- 用户不会从 workspace 装，只会 `pip install fcop` / `pip install fcop-mcp`
- 本 ADR 的目标是"干净的双包"，不是"高级的构建工具选择"

未来如果 uv workspace 生态成熟，可以在新 ADR 里迁过去。

### Alt-5：把 `private/fcop-repo/` 提升为独立仓库本身 —— **已选中**

**这就是实际状态**：`d:\Bridgeflow\private\fcop-repo\` 就是
`joinwell52-AI/FCoP` 的本地 working copy，已有 14 个协议文档 commit
（`spec/`、`essays/`、`primer/`、`integrations/`、`assets/`、`LICENSE`、
`README.md`、`README.zh.md`、`.gitignore`）。

**选中理由**：

- FCoP 仓库已经以"协议项目主页"姿态存在，spec + essays + primer 先行，
  代码后入场，符合"协议优先、实现服务于协议"的定位
- 无需 `filter-repo` 折腾，commit 历史清爽
- codeflow-plugin 的代码历史完整留在 `codeflow-pwa`，新仓库不背历史债

**本来 Alt-1（filter-repo 抽历史）的代价**：

- 把 3500 行 `server.py` 演进史插进来会让 FCoP 的 commit 时间线错位
  （FCoP 仓库 14 个 commit 的时间比 codeflow-plugin 晚）
- 解决插入冲突需要做 rebase / 手动归并 commit，收益是"能 git blame 看
  旧代码"，但这个价值对一个"马上要 0.6 大改"的项目几乎为零

`fcop 0.6.0` 的代码引入以**一次性 clean import** 的形式加入 FCoP 仓库
的新分支，在 commit message / `CHANGELOG.md` 里注明"based on
codeflow-pwa@e651139（fcop 0.5.4）"即可满足可追溯性。

## Consequences

### Positive

- **品牌干净**：`fcop` 是独立项目，独立仓库、独立 PyPI、独立文档、独立路线图
- **职责分明**：库归库、服务器归服务器；使用者按需装
- **破坏一次，终身受益**：0.6 硬切之后，命名混乱一次性了结
- **未来扩展空间大**：想做 `fcop-cli` 就再加一个包；想换 MCP SDK 就只改 `fcop-mcp`
- **CodeFlow 和 FCoP 解耦**：CodeFlow 未来可以作为 `fcop` 的一个普通下游使用者
- **ADR-0001 的库 API 有正当落地点**：`fcop` 包里就是库，没有 MCP 代码让名字
  实至名归

### Negative

- **一次性工作量大**：新仓库初始化、CI 双轨、文档大搬家、pypi 迁移对照，
  粗估整体 1-2 周（含 ADR-0001 的 5-8 天库拆分）
- **外部已存在的 PyPI URL / GitHub URL 引用全部失效**：当前 README / 文档中
  指向 `codeflow-pwa/.../codeflow-plugin/` 的 URL 都要改
- **Cursor 插件商店可能需要重新申请**：`.cursor-plugin/plugin.json` 的
  `homepage` / `repository` 变了，插件可能需要重新注册
- **SEO / 发现性一次性重置**：`fcop 0.5.x` 在 PyPI 历史页搜索已经建立的
  "打开这个包即可装 MCP" 的认知，0.6 要重新解释
- **`bridgeflow` 这个名字永久留在 PyPI**：不做任何处理，它会维持 2026-04-03
  的最后一版现状。搜索"bridgeflow"还能搜到，但没有迁移引导信息——这是为"没
  真用户"场景刻意选择的低成本方案

### Neutral

- `joinwell52-AI/FCoP` 已建好（14 commits），本地 working copy 在
  `d:\Bridgeflow\private\fcop-repo\`；只需补 branch protection / PyPI
  token secrets / CI workflows
- `codeflow-pwa/codeflow-plugin/` **不清理**，保留 0.5.4 最终态作为
  pre-history archive；只改根 `README.md` 加一句"fcop 已独立到
  joinwell52-AI/FCoP"
- `CHANGELOG.md` 在 FCoP 仓库新建，顶部链到 codeflow-pwa 对应 commit
- `docs/agents/shared/` 的旧 0.5 样板已经被 0.5.4 的 `deploy_role_templates`
  处理过，和本次迁移正交
- `private/fcop-repo/` 不是"预备区"，就是仓库本身的本地 clone；它和
  远端 `joinwell52-AI/FCoP` 永远保持同步

## Timeline

| 日 | 产出 | 所在 |
|---|---|---|
| D0 | 本地 `private/fcop-repo/` 提交 `adr/` 目录并推送 origin/main（ADR-0001/0002/README 三份文档）| FCoP |
| D0 | FCoP 仓库配 branch protection 规则 + PyPI token secrets（`PYPI_TOKEN_FCOP` / `PYPI_TOKEN_FCOP_MCP`）| FCoP |
| D0 | 新开分支 `feat/0.6-library-split` | FCoP |
| D1 | `pyproject.toml` 库本体（`src/fcop/`）骨架 + `_version.py`（单一事实源）| FCoP |
| D1–D6 | 按 ADR-0001 Timeline 开发库公共 API、dataclass 模型、errors、teams、rules | FCoP |
| D3 | `mcp/` 子目录 + `mcp/pyproject.toml` + `src/fcop_mcp/` 壳：把 22 个 tool / 10 个 resource 改成调库 | FCoP |
| D5 | `tests/test_fcop/` + `tests/test_fcop_mcp/`，覆盖率 ≥ 80%；CI 硬约束"测 `fcop` 时不装 `fastmcp`" | FCoP |
| D7 | `.github/workflows/test-fcop.yml` + `test-fcop-mcp.yml` + `release-fcop.yml` + `release-fcop-mcp.yml` | FCoP |
| D7 | 写 `MIGRATION-0.6.md`（用户迁移指南）+ 更新 `docs/release-process.md`（双包发布流程）| FCoP |
| D8 | PR `feat/0.6-library-split` → `main` 合入，打 tag `v0.6.0` | FCoP |
| D8 | `fcop 0.6.0` 先发 PyPI（`py -3.10 -m twine upload dist/fcop-*.whl`）| FCoP |
| D8 | 稍候（等 PyPI 索引更新 1-5 分钟），`fcop-mcp 0.6.0` 发 PyPI | FCoP |
| D8 | `codeflow-pwa` 根 `README.md` 末尾加一行"FCoP protocol + plugin moved to joinwell52-AI/FCoP" | codeflow-pwa |
| D9 | 写发布 blog post（essay 性质：为什么拆成两个包）；可选：申请 `fcop.dev` 域名 | FCoP |

## Sign-off

- ADMIN: _待签字_
- PM: _待指派_

---

_Last edited: 2026-04-22. Status changes go in the table at the top; body content is frozen._
