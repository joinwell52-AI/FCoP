# ADR-0006: 协议规则的宿主中立分发与升级（Host-Neutral Rule Distribution & Upgrade）

- **Status**: Accepted
- **Date**: 2026-04-25
- **Deciders**: ADMIN
- **Related**: [ADR-0001](./ADR-0001-library-api.md)（库 API）、[ADR-0002](./ADR-0002-package-split-and-migration.md)（包拆分）、[ADR-0003](./ADR-0003-stability-charter.md)（稳定性宪章）

## ADMIN 决议（2026-04-25）

ADMIN 在远程机器升级 `fcop-mcp` 后发现两个并列的根问题：

> "这个是大 BUG；现在的问题：
>
> 1）是 mdc 就只能支持 cursor；其他的怎么办？
> 2）协议两份文件应该怎么升级？"

并在改名讨论中给出语义校准：

> "因为版本升级，需要 report；unbound 限制是没有配角色。"

本 ADR 把这两件事一次性钉死：
1. 协议规则文件**必须**以宿主中立的形式分发到项目里
2. 升级路径必须存在、显式、由 ADMIN 控制
3. `unbound_report` 改名 `fcop_report` 以匹配通用语义，走 deprecation cycle

---

## Context

### 现状（截至 0.6.2）

`fcop-mcp` 安装时，`fcop.rules._data/` 包内携带：

- `fcop-rules.mdc`（`fcop_rules_version: 1.4.0`）
- `fcop-protocol.mdc`（`fcop_protocol_version: 1.3.0`）
- `letter-to-admin.{zh,en}.md`

但 `Project.init()` / `init_solo()` / `init_custom()` / `deploy_role_templates()`
**没有任何方法**会把这两份 `.mdc` 写到项目根的 `.cursor/rules/` 目录。MCP 工具
`init_project` 的 docstring 还写着 "drops the bundled protocol rules into
`.cursor/rules/`"——**docstring 撒谎了**，代码没干。

### 两个症状

#### 症状 1 ｜ `.mdc` 只对 Cursor 生效

`.mdc` 是 Cursor IDE 的私有规则文件格式。Cursor 自动读 `.cursor/rules/*.mdc`
注入每个 agent 会话的 system prompt。其它 host 的待遇：

| Host | 是否读 `.cursor/rules/*.mdc` | 是否自动看到 FCoP 规则 |
|---|---|---|
| Cursor | 是 | **是** |
| Claude Desktop | 否 | **否**（除非用户手动 attach `fcop://rules` resource） |
| Claude Code CLI | 否（读 `CLAUDE.md`） | **否** |
| Codex CLI | 否（读 `AGENTS.md`） | **否** |
| 直接调 OpenAI / Anthropic API 的脚本 | 否（用户自己拼 system prompt） | **否** |
| 任何未来新 MCP host | 否 | **否** |

`fcop-protocol.mdc` 文档里自称 "host-neutral reminder"——**实际并不**。
非 Cursor host 拿不到这份规则。

#### 症状 2 ｜ 那两份文件升不了

ADMIN 远程机器上看到的版本：

```
fcop-mcp:           0.6.2  ✓
fcop:               0.6.2  ✓
fcop_rules_version: 1.3.0   ← 包内已是 1.4.0
fcop_protocol_version: 1.2.0 ← 包内已是 1.3.0
```

原因是：

- `pip install -U fcop-mcp` 升级了 wheel 里的 `_data/*.mdc`
- 但项目的 `.cursor/rules/*.mdc` 是当年 init 时手工拷过去的旧副本
- `Rule 8` 明令禁止 agent 修改 `.cursor/rules/*.mdc`
- ADMIN 没有任何工具可以安全升级它们

### 第三个相关问题：`unbound_report` 名字过窄

`unbound_report` 字面只对"无角色"状态有意义。但 Rule 0 真正的语义是：
**会话开门 + 任何状态变化（包括包升级）后，都需要 report**。绑定后调用
仍然有意义（查版本告警、查最近活动），但名字不像。

---

## Decision

### 决策 1：库层加 `Project.deploy_protocol_rules`，宿主中立

`fcop` 库新增一个方法，把协议规则文件**同时**部署到三个位置：

```python
class Project:
    def deploy_protocol_rules(
        self,
        *,
        force: bool = True,
        archive: bool = True,
    ) -> DeploymentReport:
        """Deploy fcop-rules.mdc + fcop-protocol.mdc to:

            <root>/.cursor/rules/fcop-rules.mdc        (Cursor)
            <root>/.cursor/rules/fcop-protocol.mdc     (Cursor)
            <root>/AGENTS.md                           (Codex / Cursor / Devin / 通用)
            <root>/CLAUDE.md                           (Claude Code)

        Three packaging formats, identical normative content.
        """
```

**为什么三处都写**：

- `.cursor/rules/*.mdc`：Cursor 自动注入；保留 `.mdc` 因为带 `alwaysApply: true` frontmatter，是 Cursor 的标准约定，删了 Cursor 用户体验倒退
- `AGENTS.md`：业界事实标准——OpenAI Codex、Cursor、Devin、多家 agent SDK 都读这个名字。**这是真正的"host-neutral 出口"**
- `CLAUDE.md`：Anthropic Claude Code 命令行约定。和 `AGENTS.md` 内容完全一样，但 Claude Code 不读 `AGENTS.md`，只读 `CLAUDE.md`，所以并行两份

**为什么不能只留 `AGENTS.md` 一份**：Cursor 不读 `AGENTS.md` 作为 rules 注入；
Claude Code 不读 `AGENTS.md`。这是上游产品的事实，不是 FCoP 的设计选择。

### 决策 2：库层 `init` 默认**不**自动部署

`Project.init / init_solo / init_custom` 的默认行为**与 0.6.2 字节相同**——
只创建 `docs/agents/...` 树。新加可选 kwarg：

```python
def init(self, *, ..., deploy_rules: bool = False) -> ProjectStatus:
    ...
    if deploy_rules:
        self.deploy_protocol_rules(force=force, archive=True)
```

**为什么默认 False**：

1. **保持纯库 import 用户行为不变**——他们 `from fcop import Project; project.init(...)` 用来跑调度脚本，不希望 init 自动给项目根写 `.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md`
2. ADR-0003 「只进不出」要求新参数必须 optional，加默认值；选择 `False` 保证默认行为是 0.6.2 行为
3. MCP 层 `init_project` 工具显式传 `deploy_rules=True`，MCP 用户拿到自动部署体验
4. 想自己控制的库用户：`project.deploy_protocol_rules(force=True)` 任何时候手动调

### 决策 3：MCP 层加 `redeploy_rules` 工具

```python
@mcp.tool
def redeploy_rules(force: bool = True, archive: bool = True) -> str:
    """ADMIN-only: re-deploy bundled protocol rules to the project.

    Run after `pip install -U fcop-mcp` to upgrade the project's
    .cursor/rules/*.mdc, AGENTS.md, and CLAUDE.md to the package's
    bundled versions. Old files are archived to
    .fcop/migrations/<timestamp>/rules/ before being overwritten.
    """
```

**为什么要这个工具**：

- ADMIN 升级了 fcop-mcp 包后必须有**显式**升级路径
- agent 不能自己跑（Rule 8 + ADR-0001-c1：agent 不修改 `.cursor/rules/*.mdc`）
- 对应 `deploy_role_templates` 的工具（那个管 `docs/agents/shared/` 模板，这个管协议规则），命名上对仗

**默认 force=True**：与 `deploy_role_templates` 默认 `force=True` 一致——这个工具的**唯一目的**就是覆盖。`force=False` 时退化成 dry-run 报告。

### 决策 4：`unbound_report` → `fcop_report`，走 deprecation cycle

新增 `fcop_report` 工具，提供与 `unbound_report` 行为字节相同的会话报告。
**额外**加版本告警一节：

```
[Versions]
  fcop-mcp:  0.6.3  (PyPI: 0.6.3 ✓)
  fcop:      0.6.3  (PyPI: 0.6.3 ✓)
  rules:     项目本地 1.4.0 ｜ 包内 1.5.0
  protocol:  项目本地 1.3.0 ｜ 包内 1.4.0

  ⚠ 项目里的 fcop-rules.mdc 比包内旧（1.4.0 vs 1.5.0）
  ADMIN 请显式调 `redeploy_rules()` 升级（agent 不会自行执行）
```

`unbound_report` 保留为 thin wrapper：

```python
@mcp.tool
def unbound_report(lang: str = "zh") -> str:
    """Deprecated alias for fcop_report. Removed in 0.7.0."""
    warnings.warn(
        "unbound_report is deprecated; use fcop_report. "
        "This alias will be removed in fcop-mcp 0.7.0.",
        DeprecationWarning,
        stacklevel=2,
    )
    return fcop_report(lang=lang)
```

**为什么改名**：

- `unbound_report` 字面只匹配 "无角色" 状态，但 Rule 0 真正语义是"会话开始/版本变化都要 report"
- `fcop_report` 通用：未绑定调它看 UNBOUND 限制；绑定调它查版本/状态/告警
- "UNBOUND 限制"不再是工具的目的，只是工具输出的一节（仅当无角色时显示）

**为什么走 deprecation 而不是直接改名**：ADR-0003 「MCP tool 合同锁定」禁止
0.6.x 内删 tool。走 deprecation：0.6.3 加新工具 + 旧工具加 warn → ≥30 天 →
0.7.0 删旧工具。

### 决策 5：协议规则文件随之 minor bump

| 文件 | 0.6.2 | 0.6.3 | 原因 |
|---|---|---|---|
| `fcop-rules.mdc` | `1.4.0` | `1.5.0` | 文档里 `unbound_report` 改成 `fcop_report`；加入 `redeploy_rules` 工具提示；加入"项目本地 vs 包内"版本概念 |
| `fcop-protocol.mdc` | `1.3.0` | `1.4.0` | 命名同步；加入三处分发说明（.cursor/rules + AGENTS.md + CLAUDE.md）；加入升级路径要走 `redeploy_rules` 的章节 |

minor bump（y+1）的依据（沿用既有 semver 习惯）：

- patch（z+1）= 措辞调整 / 错别字
- **minor（y+1）= 加章节 / 加规则提示 / 改工具名（向下兼容）** ← 本次属于这一档
- major（x+1）= 删规则 / 改语义 / 让旧 agent 无法工作

注意：包版本是 `0.6.2 → 0.6.3` patch（按 ADR-0003 这次只加新工具不删旧的），
**包版本与规则版本各自独立 semver**——这是 0.6 的"5 个独立版本号"设计的两个流。

### 决策 6：`fcop_report` 输出布局

```
=== FCoP 报告 ===

[Session]
  项目: <abs path>   (source: <how-resolved>)
  角色: UNBOUND ｜ 或 PM @ dev-team

[Versions]
  fcop-mcp:  0.6.3  (PyPI: 0.6.3 ✓)
  fcop:      0.6.3  (PyPI: 0.6.3 ✓)
  rules:     项目本地 1.5.0 ｜ 包内 1.5.0 ✓
  protocol:  项目本地 1.4.0 ｜ 包内 1.4.0 ✓

[Team]    （仅已初始化才显示）
  team / leader / lang / roles

[Status]  （仅已初始化才显示）
  tasks / reports / issues 计数 + 最近 3 条活动

[UNBOUND 限制]   （仅当无角色才显示）
  ADMIN 请用「你是 <ROLE>...」分配角色
  在此之前禁止：读任务正文 / 写文件 / 自认角色 / 派发任务

[绑定状态]   （仅当已绑定才显示）
  当前可执行 / 受限清单
```

`版本告警段`仅当本地 < 包内 时插入。

---

## Consequences

### Positive

- **真·宿主中立**：Cursor、Claude Code、Codex、任何 LLM SDK 都能拿到同一份 FCoP 规则
- **大 bug 修复**：协议规则文件有了显式升级路径，不再是"装过一次就锁死"
- **库 import 体验保持纯净**：纯 Python 库用户行为零变化，只多两个可选方法
- **agent 体验整体提升**：`fcop_report` 名字与语义对齐；版本不一致时主动告警 ADMIN
- **0.7.0 清理路径明确**：`unbound_report` 走标准 deprecation；其他改动都是 additive 不需要清理

### Negative

- **rules.mdc 内容变多**：要解释 `redeploy_rules`、要解释三处分发约定、要解释项目本地 vs 包内版本——文档更长
- **MCP tool 数量从 24 增到 26**：`fcop_report` + `redeploy_rules` 两个新工具；旧 `unbound_report` 仍计 1 个直到 0.7.0
- **测试矩阵扩大**：要测 .cursor/rules + AGENTS.md + CLAUDE.md 三处都正确写入；要测 force/archive；要测版本告警拼接
- **`AGENTS.md` / `CLAUDE.md` 与项目原有约定可能冲突**：少数项目本来就有 `AGENTS.md` 写自己的 agent 配置——本工具会覆盖（force=True 时归档原文件）。这是接受的代价；ADMIN 显式调用，知情同意

### Neutral

- 包版本是 patch（0.6.2 → 0.6.3）；规则版本是 minor（1.4.0 → 1.5.0）——这是 0.6
  设计的"5 个独立版本号"流的正常工作方式，不需要新约定
- `Rule 8` 仍然有效：agent 不能改 `.cursor/rules/*.mdc`；`redeploy_rules` 是 ADMIN
  显式调用的工具，**MCP host 可以让 ADMIN 在聊天里用一句话触发**，仍属 ADMIN 意图

---

## Non-Goals

- **不**自动检测 host 类型并只部署对应文件——三处一起写比"猜对 host"更简单可靠
- **不**做"规则文件双向同步"（项目本地改 → 反向写回包）——规则源头永远是包，项目本地是只读副本，要改就改源头然后 redeploy
- **不**给 `redeploy_rules` 加 `--diff-only` 模式——那等于把 git diff 抄进工具；ADMIN 真要 diff 用 git
- **不**在 0.6.3 里删除 `unbound_report`——deprecation 至少跨 30 天，删除留给 0.7.0

---

## Alternatives Considered

### Alt-1：只在 MCP 层面加 `redeploy_rules`，库层不动

理由是"反正 MCP 用户最多，库用户少，不必改库"。

**否决原因**：

- 库用户也能从"协议规则可分发"中受益，把方法只放在 MCP 层等于把这能力锁在 Cursor 用户手里——和决策 1 的初衷（host-neutral）矛盾
- ADR-0001 把 fcop 库定位为"零 MCP 耦合"——MCP 工具应该只是库方法的薄封装

### Alt-2：让 `init` 默认 `deploy_rules=True`

理由是 MCP 用户体验更直接。

**否决原因**：

- 破坏纯库用户预期。`from fcop import Project; project.init()` 在 0.6.2 不写 `.cursor/rules/`，0.6.3 突然写了，是无声破坏
- 哪怕 ADR-0003 允许"加默认参数"，破坏的是默认**行为**而非默认**签名**——这是更隐蔽的违约
- MCP 层一行代码 `project.init(..., deploy_rules=True)` 就解决了 MCP 的体验需求，没必要改默认

### Alt-3：把 `unbound_report` 直接改名，不留 alias

理由是 0.6 还没多少用户，alias 是净负担。

**否决原因**：

- 直接违反 ADR-0003 「MCP tool 合同锁定」
- ADMIN 自己定的稳定性宪章不能自己破——一旦破例，宪章对所有未来 case 失效
- 一个 alias + 一行 DeprecationWarning 的代价远小于宪章信用受损

### Alt-4：保留 `.mdc` 不出 `AGENTS.md` / `CLAUDE.md`

理由是少 2 份文件，少污染项目根。

**否决原因**：

- 这就把症状 1 留着没修——Claude Desktop / Codex 用户仍然拿不到规则
- ADMIN 明确指出"是 mdc 就只能支持 cursor；其他的怎么办？"，必须给出答案

### Alt-5：把规则规范化成 JSON / YAML，让每个 host 自己渲染

理由是更"工程"。

**否决原因**：

- 协议规则的**形式**就是给 LLM 读的 markdown——再加一层结构化抽象等于让用户多写一个适配器
- LLM 直接读 markdown 比读 JSON 表现好
- FCoP 设计哲学（"人机同构、文件即协议"）排斥这种额外间接层

---

## Timeline

| 日 | 产出 |
|---|---|
| D0（2026-04-25）| 本 ADR 落地；0.6.3 改动开始 |
| D0 | 库层 `deploy_protocol_rules` + `get_protocol_version` + init kwarg |
| D0 | MCP 层 `fcop_report` + `redeploy_rules` + `unbound_report` deprecation |
| D0 | 规则 mdc 改名 + minor bump（rules→1.5.0、protocol→1.4.0）|
| D0 | 测试 + tool_surface 快照更新 + 文档同步 |
| D0 | 0.6.3 发版 |
| D0 + ≥30 天 | 0.7.0 删除 `unbound_report`，发 minor 版 |

---

## Sign-off

- ADMIN: 已批准（2026-04-25，"开干"）
- PM: 落地执行

---

_Last edited: 2026-04-25. Status changes go in the table at the top; body content is frozen._
