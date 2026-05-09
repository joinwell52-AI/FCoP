# ADR-0022: Workspace Directory Convention — `docs/agents/` → `fcop/`

- **Status**: Accepted
- **Date**: 2026-05-09
- **Deciders**: ADMIN
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md)（charter，本 ADR 是 §抽象 2 Encoding 的子决议）；[ADR-0021](./ADR-0021-encoding-abstraction.md)（workspace_dir 是 encoding contract 的一部分）；[ADR-0006](./ADR-0006-host-neutral-rule-distribution.md)（rule 分发位置约定）

## Context

ADMIN 在 ADR-0015 charter 落定后约 30 分钟，提出第二轮元批评：

> 「MCP 落盘是建立 docs 文件夹，难道不应该是 fcop 文件夹吗？」

这个问题精准戳到 ADR-0021 Encoding Abstraction 没明示的一个 contract 项：**FCoP 工作区目录命名应该是协议本体的一部分，还是 reference encoding 的可选项？**

### 现状（0.7.x）

```
<project_root>/
└── docs/
    └── agents/                  ← FCoP 全部协议级文件塞这里
        ├── fcop.json            ← 协议配置
        ├── tasks/               ← 4 类 IPC envelope
        ├── reports/
        ├── issues/
        ├── shared/
        └── log/                 ← 归档
```

### 历史选择 `docs/` 的（猜测）原因

- `docs/` 是工业惯例（Sphinx / mkdocs / Docusaurus / GitHub Pages）—— 任何项目几乎都有
- "agents 协作 = 项目文档的一种" 这个隐喻让 FCoP 看起来"无侵入"
- git 默认 track `docs/`，对 review / audit 友好

### 协议层面的批评（ADMIN）

- **`docs/` 暗示"文档"语义** → AI 协作记录被定位成"项目文档的一种"，遮蔽了"这块工作区被 FCoP 占用"的事实
- **`fcop/` 才是"协议命名空间"语义** → 显式占位
- 主流工具都用自己的命名空间：`.git/` / `.cursor/` / `node_modules/` / `.venv/` / `.next/` / `.cache/`
- 把协议占用区放进通用 `docs/` 让用户的"自然 docs"和"FCoP 占用区"混在一起 —— 与 ADR-0015 charter §背景批评的 `fcop-standalone.md` 自相矛盾**同病**

## Decision

`fcop@1.0.0` 起，FCoP 工作区默认目录从 `docs/agents/` 迁移到顶层 `fcop/`：

```
<project_root>/
└── fcop/                          ← v1.0 起的协议命名空间
    ├── fcop.json
    ├── tasks/
    ├── reports/
    ├── issues/
    ├── reviews/                   ← REVIEW-* 目录（ADR-0017 新增）
    ├── shared/
    └── log/
        ├── tasks/
        ├── reports/
        ├── issues/
        ├── reviews/
        └── events/                ← 视 ADR-0018 决议（v1.0 暂不创建）
```

### 关键约束

1. **`fcop/` 是 v1.0 默认；workspace_dir 仍可配置**——`Project(workspace_dir="custom/")` 接口由 ADR-0021 Encoding Abstraction 提供
2. **0.7.x 项目必须迁移**——这是 v1.0 的 breaking change，由 ADR-0003 §0.7→1.0 一次性清理窗口允许
3. **必须配自动迁移工具**——`fcop migrate-workspace` 命令一键迁移；`fcop` lib 启动时如发现旧 `docs/agents/` 布局自动 detect 并提示
4. **过渡期保护**：v1.0 reference impl 在 detect 到 `docs/agents/` 时**不报错**，只 warning + 提示运行 migrate

## Design Details

### 自动迁移工具（v1.0 必须交付）

新增 `fcop` CLI 命令：

```bash
fcop migrate-workspace               # 默认：dry run，列出会发生的改动
fcop migrate-workspace --apply       # 真正执行
fcop migrate-workspace --target=path # 指定目标目录（默认 fcop/）
```

迁移行为：

1. `git mv docs/agents/ → fcop/`（保留 git history）
2. 更新 `fcop/fcop.json` 内任何指向 `docs/agents/` 的内部路径
3. 检查 `.gitignore` / `.cursor/rules/*.mdc` 等是否引用 `docs/agents/`，列出建议手工改的位置（不自动改，避免误伤用户文档）
4. 写一份 `fcop/MIGRATED_FROM_DOCS_AGENTS.md` 留痕，便于回滚

### 启动时 detect 行为

`Project()` 构造时：

- 如果 `fcop/` 存在 → 用 `fcop/`
- 如果 `fcop/` 不存在但 `docs/agents/` 存在 → 用 `docs/agents/` + 打 warning："This is a 0.7.x-style workspace. Run `fcop migrate-workspace` to migrate to the v1.0 default."
- 如果两者都存在 → error："Both `fcop/` and `docs/agents/` exist. Please remove one or pass `workspace_dir=` explicitly."
- 如果两者都不存在 + 用户调 `init()` → 创建 `fcop/`（默认 v1.0 行为）

### encoding contract 项（与 ADR-0021 协同）

`encoding.schema.json` 的 contract 加一项：

```json
{
  "workspace_dir": {
    "description": "Root directory for FCoP protocol files relative to project root",
    "type": "string",
    "default": "fcop"
  }
}
```

ADR-0021 §Decision 表"Encoding Abstraction (协议本体)"加一行 "**workspace_dir** 默认值"。

## Tests Checklist

- [x] `tests/test_fcop/test_migrate_workspace.py`：dry run / --apply / 已迁移幂等 / git history 保留（25 用例，2026-05-09 by ME，commit 见下方 Implementation 段）
- [ ] `tests/test_fcop/test_project_init.py`：新项目 init 默认创建 `fcop/`（**deferred 到 v1.0 final 之前的独立 task**：见下方 v1.0 RC Implementation Notes）
- [ ] `tests/test_fcop/test_project_detect.py`：4 种 detect 场景（仅 fcop/、仅 docs/agents/、两者都有、两者都无）（**deferred**，同上）
- [ ] `tests/test_fcop/test_project_detect.py`：detect 到 docs/agents/ 时打 warning 而不报错（**deferred**，同上）
- [ ] `tests/test_fcop_mcp/test_init_tool.py`：MCP `init_project` tool 创建 `fcop/`（**deferred**，同上）
- [x] CHANGELOG.md `[1.0.0-rc.1]` 段含 workspace 迁移条目（commit 见下）
- [ ] `MIGRATION-1.0.md` 必须有"Workspace 迁移"段（含命令 + 风险说明）（**deferred** 到 v1.0 final）

## v1.0 RC Implementation Notes (2026-05-09)

TASK-008 把 ADR-0022 拆成两阶段交付：

**Phase 1 — v1.0.0-rc.1（本次落地）**

- 完整交付 `fcop migrate-workspace` CLI（dry-run / `--apply` / `--target` /
  `--source` / `--project-root`）
- git-aware：检测到 git 工作区 + path 已 tracked 时自动用 `git mv`，
  否则 fallback `shutil.move`
- 幂等：`apply()` 在已迁移的 tree 上是 no-op
- 安全：both-exist 时 `--apply` 退出码 2 并 ABORT，绝不合并
- 留痕：移动后写 `MIGRATED_FROM_DOCS_AGENTS.md` 含时间戳 + 版本号
- 顾问扫描：检测 `.gitignore` / `.cursor/rules/*.mdc` / `AGENTS.md` /
  `CLAUDE.md` / `README*.md` 中的 `docs/agents` 字符串引用，**列出但不
  自动改写**（per ADR-0022 §"Design Details" item 3 规避误伤用户文档）
- `fcop` console-script entry 从 `_compat_cli:main` 升级为
  `cli._main:main`：subcommand 派发器；`fcop`（无参）仍打印 0.5→0.6
  legacy migration 信息以兼容历史

**Phase 2 — v1.0.0 final 之前（deferred 到独立 task）**

- `Project()` 构造加 `workspace_dir=` 参数 + 4 种 detect 场景
- 把 `Project` 内 30+ 处 hard-coded `docs/agents/` 路径替换为
  `self.workspace_dir / X`
- `Project()` 默认在新 init 时创建 `fcop/`，老项目检测到 `docs/agents/`
  打 DeprecationWarning
- `MIGRATION-1.0.md`（用户向）

理由：Phase 2 改动 `Project` 30+ 处路径会触动 600+ 既有测试；RC 期不
应承担该范围风险。CLI 是 ADR-0022 §"Design Details" §自动迁移工具的
核心交付物，独立可用，不依赖 Phase 2。

## Implementation

- **ME** — 2026-05-09 (commit `<TBD this commit>`):
  - `src/fcop/cli/__init__.py`（新建）
  - `src/fcop/cli/_main.py`（新建，subcommand 派发器 + 0.5→0.6 legacy
    fallback）
  - `src/fcop/cli/migrate_workspace.py`（新建，~340 行：plan/apply/
    render_summary/argparse glue）
  - `pyproject.toml`：entry point bump
  - `tests/test_fcop/test_migrate_workspace.py`（新建，25 用例：
    plan / apply / render / CLI / standalone run）
  - `tests/test_fcop/test_compat_cli.py`：放宽 `test_console_script_
    resolves_to_cli_main` 接受 v1.0 + v0.7 entry value
  - `CHANGELOG.md` `[1.0.0-rc.1]`：新增 "fcop migrate-workspace CLI" 段

## Backwards Compatibility

- **Breaking**：默认 workspace 改变；0.7.x 项目升级 v1.0 后第一次启动会得 warning，必须运行 `fcop migrate-workspace`（或显式传 `workspace_dir="docs/agents/"`）
- **不破坏**：`Project(workspace_dir="docs/agents/")` 显式调用永远合法 —— 即使 v2.x 也保留作 escape hatch
- **不破坏**：所有 0.7.x 文件 frontmatter / filename 100% 兼容；只是住在新地址
- **依据**：ADR-0003 §0.7→1.0 stability charter 留的"一次性清理"窗口允许此 breaking；v1.0 之后不再允许任何 workspace 默认迁移

## Alternatives Considered

### Alt-A：保留 `docs/agents/`

**否决原因**：ADMIN 明确选 B（migrate）；协议命名空间清晰是 1.0 framing 升级的必然要求

### Alt-B（已选）：迁移到 `fcop/` 配自动迁移

ADMIN 拍板。

### Alt-C：双轨过渡（v1.0 同时支持，新项目默认 fcop/，老项目继续 docs/agents/）

**否决原因**：
- 双轨意味着 v1.x 长期维护两套测试矩阵
- 老项目永远没有动力迁移 → v2.x 还得再处理
- 不如 v1.0 一次性 breaking + 配自动迁移，工程上更干净

### Alt-D：用隐藏目录 `.fcop/`

**否决原因**：
- FCoP 的核心哲学之一是"人机同构"——人在文件浏览器里要能看到 agent 在干啥
- 隐藏目录违背这一原则
- 隐藏目录默认不被 git track，与 ADR-0006 host-neutral rule distribution 的 git-friendly 精神冲突

### Alt-E：用顶层 `agents/`

**否决原因**：
- `agents/` 命名通用，可能与项目里其他 agent 概念冲突（如 sales agents、user agents）
- `fcop/` 是协议名占位，无歧义

## Consequences

### Positive

- 协议命名空间清晰；与 .git / .cursor / node_modules 等命名空间惯例同族
- 多 FCoP 项目混合时一眼可识
- 与 ADR-0015 §术语表 "FCoP Protocol Layer" 命名呼应
- 解决 ADMIN 第二轮元批评的协议层级问题
- 为未来 alternative encoding（JSON / SQLite）提供清晰锚点（都住在 `fcop/`）

### Negative

- v1.0 增加一个 breaking change（除已有的 framing 升级 + 7 抽象冻结）
- 必须额外交付 `fcop migrate-workspace` 命令 + 测试 + 文档
- 0.7.x 老用户升级体验：第一次跑会得 warning，需要手工运行迁移命令
- 所有教程文档、essay、forum post 中的 `docs/agents/` 路径示例都要改（约 30+ 份文件，由后续 TASK 排期）
- ADR-0015 §Non-Goals "不动 Python 实现代码" 需要 carve-out（新增 migrate-workspace 命令）

### Neutral

- `docs/agents/` 仍可显式使用（escape hatch 永久保留）
- 迁移工具是一次性使用，未来 minor 不需维护
- 与 `_data/` vs `.cursor/rules/` 关系（ADR-0006 既定）正交，不冲突

## Timeline

| 日期 | 里程碑 |
|---|---|
| 2026-05-09（D0）| 本 ADR Accepted；ADR-0015 / 0021 / 1.0.0 release notes / adr/README.md 联动 patch |
| 2026-05-13 (D+4)| `fcop migrate-workspace` 命令完整稿 + PR |
| 2026-05-15 (D+6) | `Project()` detect 行为完整稿 + PR |
| **2026-06-20 ~ 2026-07-04 (D+42 ~ D+56)** | 随 fcop@1.0.0 上 PyPI |

## Sign-off

- **ADMIN**：已批准（2026-05-09 14:50 CST，AskQuestion 选 B - migrate）
- **ME**：Phase 1 已实施（2026-05-09，TASK-008，commit 见 Implementation 段）；Phase 2 待 v1.0.0 final 前独立 task

---

_Last edited: 2026-05-09. Status changes go in the table at the top; body content is frozen per ADR convention._
