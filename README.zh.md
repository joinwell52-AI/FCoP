<p align="center"><a href="spec/fcop-4.0-spec.zh.md"><img src="assets/fcop-logo-256.png" alt="FCoP 4.0 协议原文" width="72" /></a></p>

# FCoP — File-based Coordination Protocol

**让多个 Agent 像团队一样工作，任务和交付都留在文件里。**

换个会话，又要从头解释项目？Agent 说“改好了”，却找不到交付记录？FCoP 把分工、结果、问题和审查保存为项目里的 Markdown 文件，让人和接手的 Agent 都能打开查看、继续工作。

**多 Agent 协作 · 文件即协议 · 无需复杂基础设施 · Agent 治理**

[协议原文：中文](spec/fcop-4.0-spec.zh.md) · [Specification: English](spec/fcop-4.0-spec.md) · [English](README.md) · [简体中文](README.zh.md) · [项目主页](https://joinwell52-ai.github.io/FCoP/)

[PyPI · fcop](https://pypi.org/project/fcop/4.0.3/) · [MCP · fcop-mcp](https://pypi.org/project/fcop-mcp/4.0.3/) · [MIT](LICENSE) · [Zenodo 与引用](#research)

**[先跑最小案例](#team-demo) · [接入 Cursor / Codex](#ai-install) · [安装前问答](#before-install)**

<a id="why-fcop"></a>

## 你会得到什么？

| 你关心的问题 | FCoP 留下的工作记录 |
|---|---|
| 谁在做什么？ | **TASK**：任务内容、收发方与当前状态 |
| “做完了”，结果在哪？ | **REPORT**：交付说明与证据引用 |
| 卡在哪里？ | **ISSUE**：问题、阻碍与上下文 |
| 谁检查过？能交接了吗？ | **REVIEW**：审查结果与决定 |

这些文件就在你的项目中，可以用编辑器查看、由工具检查，也可以将适合的记录纳入 Git。协作记录无需另配 Redis、消息队列或数据库，Agent 继续使用你熟悉的 Cursor、Codex 等工具。

**即使 Agent 离开了，工作依然在那里。**

<a id="team-workflow"></a>

## 30 秒看懂：你交目标，PM 带团队

<img src="assets/fcop-team-workflow.zh.svg" alt="ADMIN 向 PM 提需求；PM 拆解并派发任务；成员向 PM 提交报告；PM 汇总后向 ADMIN 汇报。" width="960" />

你是 **ADMIN**，只需与 **PM** 对接。PM 把目标拆成任务，分给 DEV、QA、OPS；成员执行并交付报告；最后 PM 汇总结果，向你汇报。**Agent 之间不聊天，通过文件协作。**

文件名标识任务或报告，文件头写明收发方，目录表达任务状态。Agent 按协议找到属于自己的工作，读任务、做工作、交报告。这里展示的是一套 PM 团队工作流；[文件格式与版本差异](#files-as-protocol)可按需查看。

<a id="team-demo"></a>

## 先跑一个最小案例

PM 派给 DEV 一个文本转换任务，QA 检查实际结果，PM 读取两人的报告后汇总给 ADMIN。这个脚本用独立客户端模拟三个角色，顺序执行，无需模型或 API Key。需要 Python 3.10+ 和 Git。

```bash
git clone https://github.com/joinwell52-AI/FCoP.git
cd FCoP
python -m pip install "fcop==4.0.3"
python examples/team_workflow.py --output ./demo-runs
```

运行后，打开终端打印的工作区路径，你会看到：

| 留下的文件 | 谁交给谁 |
|---|---|
| 3 份 TASK | ADMIN → PM；PM → DEV；PM → QA |
| 3 份 REPORT | DEV → PM；QA → PM；PM → ADMIN |
| 1 份 REVIEW | QA 对实际结果的检查记录 |

**你可以直接打开 PM 的汇总报告，沿着文件找到成员交付和 QA 检查。** 案例完成交付，任务保留在 `review` 等待正式验收。

[完整案例代码](examples/team_workflow.py) · [跨会话交接：English](docs/mcp-handoff.md) · [中文](docs/mcp-handoff.zh.md)

<a id="before-install"></a>

## 安装前的四个问题

### 1. 为什么我要安装 FCoP？

如果你需要多个 Agent 分工，或者经常换会话接手项目，FCoP 能让任务、交付和审查有共同的文件记录。下一位接手者可以据此确认进度，少做一轮人工整理和转述。

### 2. 安装后，是直接在开发代码里引用吗？

通常不需要。普通项目通过 CLI 和 MCP 使用 FCoP；开发自己的集成工具时，才需要 `from fcop import Project`。

### 3. 应该把它安装到 Codex、Cursor 等 Agent 工具里吗？有什么用？

是的，配置 `fcop-mcp` 后，Agent 就可以调用创建任务、领取任务、提交报告、记录问题与审查等工具。当前提供 **49 tools / 12 resources / 4 resource templates**。

### 4. 安装后立刻能看到什么效果？

连接后，客户端显示 FCoP 工具；初始化后，项目中出现 `<project>/fcop/`；执行第一份任务后，就能打开真实的 TASK 和 REPORT。上面的案例还会留下 QA 检查与 PM 汇总。

<a id="ai-install"></a>

## 让 AI 帮你安装 FCoP

把下面这段话交给 **Cursor Agent、Codex，或其他能运行命令、修改文件的编程 AI**。由 AI 完成安装并检查结果。

```text
请为我当前使用的 AI 编程客户端和项目安装 FCoP，按这份说明操作：
https://github.com/joinwell52-AI/FCoP/blob/main/docs/ai-install.md
环境检查、安装、配置和验收都由你执行。保留我现有的配置和项目状态。完成后告诉我实际验证结果；只在缺少客户端/项目选择，或确实需要授权、重连时让我介入。
```

### MCP：让 Agent 使用 FCoP

```bash
python -m pip install "fcop==4.0.3" "fcop-mcp==4.0.3"
fcop tools
```

安装后，在支持本地 stdio MCP 的客户端中配置服务。以下是通用 JSON 示例；Codex 的具体配置见[AI 安装说明](docs/ai-install.md)。

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/absolute/path/to/python",
      "args": ["-m", "fcop_mcp"],
      "env": {
        "FCOP_PROJECT_DIR": "/absolute/path/to/my-project"
      }
    }
  }
}
```

将两个绝对路径换成你的 Python 解释器和项目路径，Windows 可用正斜杠。重连后检查工具列表，再按安装说明初始化项目、采用团队规则并执行一份任务。

[完整安装与客户端配置](docs/ai-install.md)

Cursor 实际连接效果：**49 个工具、12 个资源**。

<img src="assets/fcop-cursor-connected.png" alt="Cursor: fcop connected, 49 tools and 12 resources enabled" width="640" />

<a id="codeflowmu"></a>

## 已有应用：CodeFlowMu

[CodeFlowMu](https://github.com/joinwell52-AI/CodeflowMu-Distribution) 已将 FCoP 用于 PM、DEV、QA、OPS 开发团队，提供客户端接入、运行和进度查看。它以专有软件预览版分发；FCoP 协议与工具按 MIT 开源，可独立使用。

FCoP 是多 Agent 协作的一种选择，适合希望将任务与交付保留在本地文件中的团队。

**想在下一个多 Agent 项目里试试？欢迎 Star 收藏 FCoP。**


## CLI：本地安装、检查与诊断

**CLI = Setup + Observe + Diagnose；MCP = Work。**

| 命令 | 用途 |
| --- | --- |
| `fcop init` | 初始化 FCoP workspace |
| `fcop status` | 查看 workspace 状态 |
| `fcop inspect` | 检查 TASK / REPORT / ISSUE / REVIEW |
| `fcop validate` | 验证协议结构 |
| `fcop tools` | 查看已安装的 MCP 工具目录 |
| `fcop doctor` | 检查安装、环境和兼容性 |
| `fcop version` | 查看已安装版本 |
| `fcop spec` | 查看规范 / 规则身份 |
| `fcop migrate` | 显式迁移旧 workspace；先检查计划，再决定是否 apply |

<details>
<summary>CLI 自检与详细说明</summary>

### 安装后快速自检 / Install & Verify

在已激活的 Python 3.10+ 环境中执行：

```bash
python -m pip install fcop

fcop version
fcop doctor
fcop init --root ./my-project
fcop status --root ./my-project
fcop validate --root ./my-project
```

需要查看 MCP 工具目录时：

```bash
python -m pip install fcop-mcp

fcop tools
fcop tools merge_branches --json
```

安装完成后，CLI 可在本地、离线环境中初始化、查看、校验和诊断；`doctor` 不联网、不修改 Host 配置。安装包本身可能需要访问包索引，离线安装需预备本地包。
CLI 不负责 create_task、approve、Branch、merge、authorization 等工作操作，实际 Agent 工作由 MCP 或 Python API 承担。
安装 `fcop` 不会自动创建 Host 指令文件；FCoP 4.x 正常 workspace 状态写入范围是 `<project>/fcop/`，不是根目录的 `AGENTS.md`、`CLAUDE.md` 或 Cursor 规则。
保留既有原子初始化暂存及失败证据，不自动清理用户文件。
`migrate` 是单独显式执行的旧工作区迁移，不是升级包时的自动步骤。
`tools` 需要可选 MCP 包，但不会自动安装它或启动服务。

[CLI reference](docs/cli.md) · [中文 CLI 参考](docs/cli.zh.md).

</details>


## 按需查阅

<a id="files-as-protocol"></a>

<details>
<summary>文件名、收发方与 v3 / v4 格式差异</summary>

## 文件怎样成为协议？

**文件有约定的类型、身份、收发方和内容；Agent 依据协议识别属于自己的工作。** 文件名、目录和文件头各有职责，不能混为一谈。

| 载体 | 能读出什么 |
|---|---|
| 文件名 | 文件类型与身份；旧版命名还直接包含收发角色 |
| 所在目录 | 任务当前处于 inbox、active、review、done 或 archive |
| 文件头 | 工作区、发送方、接收方、任务关联与证据身份 |
| Markdown 正文 | 要做什么、交付了什么、问题和审查理由 |

**文件名路由的直观例子（Legacy v1–v3）：** `TASK-20260915-001-PM-to-DEV.md` 表示 PM 发给 DEV 的任务，`REPORT-20260915-001-DEV-to-PM.md` 表示 DEV 交给 PM 的报告。角色明确后，Agent 可以从命名约定识别自己的收件文件。

**4.0 当前实现的实际格式：** 新任务保存在 `fcop/_lifecycle/inbox/TASK-<uuid>.md`，文件头使用 `sender: PM`、`recipient: DEV` 标明收发方。Agent 或调用方读取任务字段，按已确定的角色选择自己的任务；不能仅通过文件名中的 `to-DEV` 查找，因为 v4 文件名不再包含这一段。报告保存在 `fcop/reports/REPORT-<uuid>.md`，通过 `subject_ref` 和 `attempt_id` 关联任务及本次执行。

上面的占位符用于解释布局，不是完整可运行的信封。具体字段以4.0 协议原文（[English](spec/fcop-4.0-spec.md) · [简体中文](spec/fcop-4.0-spec.zh.md)）为准；[当前创建实现](src/fcop/v4/creation.py)与[旧版文件名语法](src/fcop/core/filename.py)可直接核对。

</details>

<a id="installation"></a>

<details>
<summary>CLI、Python、源码安装与自行实现</summary>

## 选择你的安装方式

| 使用方式 | 安装什么 | 用来做什么 |
|---|---|---|
| 独立命令行 CLI | `fcop` | 初始化、查看、校验、诊断项目 |
| Python 开发引用 | `fcop` | 在自己的程序中调用 `Project` API |
| Agent 工具中的 MCP | `fcop` + `fcop-mcp` | 让 Codex、Cursor 等客户端中的 Agent 使用协作工具 |
| 从源码开发 | 本仓库及 `mcp/` 子项目 | 修改、调试或贡献参考实现 |

### CLI 与 Python：同一个安装包

```bash
python -m pip install "fcop==4.0.3"
fcop version
fcop doctor
fcop init --root ./my-project
fcop status --root ./my-project
```

Python 开发者安装后可以使用 `from fcop import Project`，完整例子见下方[手动参考](#manual-setup)。普通用户不需要把 FCoP 引入业务代码。

### MCP：让 Agent 使用 FCoP

```bash
python -m pip install "fcop==4.0.3" "fcop-mcp==4.0.3"
fcop tools
```

安装后，在支持本地 stdio MCP 的客户端中配置服务。以下是通用 JSON 示例；Codex 的具体配置见[AI 安装说明](docs/ai-install.md)。

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/absolute/path/to/python",
      "args": ["-m", "fcop_mcp"],
      "env": {
        "FCOP_PROJECT_DIR": "/absolute/path/to/my-project"
      }
    }
  }
}
```

把 `command` 换成安装了两个包的 Python 解释器绝对路径，把项目路径换成你的工作目录；Windows 路径可使用正斜杠。重连客户端后，应看到 FCoP 的 49 个工具与 12 个资源。项目初始化与团队规则采用是后续步骤，连接 MCP 不会自动建立 PM 团队或启动其他 Agent。

### 源码安装

```bash
git clone https://github.com/joinwell52-AI/FCoP.git
cd FCoP
python -m pip install -e .
python -m pip install -e ./mcp
fcop version
```

官方安装入口是上述 Python 包；本指南不提供未经核实的 npm 包或 Node SDK。Node.js 等语言可以通过 MCP 客户端接入，或依据协议开发自己的实现。

### 只采用协议，自行实现

无需使用 Python 参考实现，也可以依据双语正式规范（[English](spec/fcop-4.0-spec.md) · [简体中文](spec/fcop-4.0-spec.zh.md)）开发符合协议的工具。仅创建几个目录还不构成符合性实现：字段、状态迁移、证据、授权、幂等与恢复契约都需要满足。使用官方工具时，由 `fcop init` 创建工作区。

</details>

<details>
<summary>macOS 安装步骤</summary>

## macOS（Intel 与 Apple 芯片）：同时安装 CLI 与 MCP

FCoP 支持 Intel Mac 与 Apple Silicon（M1/M2/M3/M4 等），发布包不依赖特定处理器架构，不需要 Rosetta。需要 Python 3.10–3.13。CLI 可直接在终端使用；MCP 还要求 Codex、Cursor 等客户端支持本地 stdio MCP Server。

创建独立环境，并安装同版本线的 Core 与 MCP：

```bash
python3 --version
python3 -m venv ~/.local/share/fcop/venv
~/.local/share/fcop/venv/bin/python -m pip install --upgrade \
  "fcop>=4.0.3,<4.1.0" \
  "fcop-mcp>=4.0.3,<4.1.0"
```

检查 CLI 与已安装的 MCP 工具目录：

```bash
~/.local/share/fcop/venv/bin/fcop version
~/.local/share/fcop/venv/bin/fcop doctor
~/.local/share/fcop/venv/bin/fcop tools --json
```

安装后即可使用下方列出的九条 CLI 命令：`init`、`status`、`inspect`、`validate`、`tools`、`doctor`、`version`、`spec`、`migrate`。使用 CLI 初始化、查看和诊断时，不要求 AI 客户端支持 MCP。

需要 MCP 时，在客户端配置中使用 macOS 绝对路径；配置文件中不要写 `~`：

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/Users/YOUR_NAME/.local/share/fcop/venv/bin/python",
      "args": ["-m", "fcop_mcp"],
      "env": {
        "FCOP_PROJECT_DIR": "/Users/YOUR_NAME/path/to/your-project"
      }
    }
  }
}
```

替换用户名和项目路径后，重启或重新连接 MCP 客户端。`FCOP_PROJECT_DIR` 应指向实际使用 FCoP 的项目，而不是 FCoP 源码仓库。

</details>

<a id="manual-setup"></a>

<details>
<summary>手动安装、Python/MCP 示例与 CLI 参考（可选）</summary>

4.0.1 已提供 `create_branch`、`inspect_family`、`merge_branches`，
4.0.3 保持 49 个工具及原签名。Core 负责原子合并、持久幂等和恢复。
未就绪家族返回 `family_digest: null`、`merge_ready: false` 及结构化原因；
语义合并结论始终来自调用方。
详见[英文合同与示例](docs/branch-merge.md) / [中文合同](docs/branch-merge.zh.md)。

<a id="try-it"></a>

## 直接试用：创建一次，换个客户端仍能读取

在已激活的 **Python 3.10+ 虚拟环境**中安装公开版本：

```sh
python -m pip install "fcop==4.0.3"
```

保存为 `demo.py`，运行 `python demo.py`。示例写入一份真实 TASK，再通过新的 `Project` 实例读取工作区，并重试原始创建请求。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from fcop import Project

with TemporaryDirectory(prefix="fcop-demo-") as directory:
    root = Path(directory) / "workspace"
    project = Project(root)
    workspace = project.create_workspace(protocol_version="4.0")
    request = dict(
        workspace_id=workspace["workspace_id"],
        operation_id="demo-create-1",
        sender="ME", recipient="ME",
        subject="Inspect this handoff",
        body="Read the task and check the evidence before accepting delivery.",
    )
    first = project.create_task(**request)

    next_client = Project(root)
    state = next_client.inspect_state(task_id=first["task_id"])
    retry = next_client.create_task(**request)

    assert Path(state["path"]).is_file()
    assert retry["existing"] and retry["task_id"] == first["task_id"]
    print("State read from disk:", state["stage"])
    print("Same task after retry:", retry["task_id"] == first["task_id"])
```

```text
State read from disk: inbox
Same task after retry: True
```

示例结束时会清理临时目录；使用自己的项目目录即可保留文件。以相同 `operation_id` 和规范化载荷重试 `create_task`，会返回原有持久结果；修改载荷则构成冲突。这项幂等保证具体适用于任务创建。

**继续查看 [4.0 接入与版本指南](docs/fcop-4.0-progress.md)**，了解长期工作区、生命周期操作，以及完成任务所需的授权配置。

<a id="mcp"></a>

## 通过 MCP，把同一套操作交给 Agent

可选适配器通过 stdio 为支持 MCP 的客户端提供 FCoP 操作。在同一已激活环境中安装：

```sh
python -m pip install "fcop==4.0.3" "fcop-mcp==4.0.3"
```

在客户端的 MCP 配置中加入以下条目，替换两个绝对路径；Windows 的命令路径以 `.venv/Scripts/fcop-mcp.exe` 结尾。

```json
{
  "mcpServers": {
    "fcop": {
      "command": "/absolute/path/to/.venv/bin/fcop-mcp",
      "env": {"FCOP_PROJECT_DIR": "/absolute/path/to/new-workspace"}
    }
  }
}
```

连接后，用 `init_solo(role_code="ME", protocol_version="4.0")` 初始化**新工作区**。调用 `create_task` 时传入工作区身份，再用 `inspect_task(filename=task_id)` 检查 TASK。安装 MCP 服务本身不会初始化工作区，也不会启动一个 Agent 团队。

**49 tools / 12 resources / 4 resource templates**（49 个工具、12 个资源、4 个资源模板）。适配器将调用交给同一 Python Core。默认初始化不含可信授权 Profile：可以创建、领取、提交任务；验收、退回、重开和归档需要显式采纳 Profile，并由可信宿主注册签发者评估器。在请求里填写一个角色名，不能赋予自己这些权限。

[MCP 工具参考](docs/mcp-tools.md) · [稳定版独立 Python 示例](tests/stable/third-party/python-only/app.py) · [稳定版独立 MCP 示例](tests/stable/third-party/mcp-only/client.py)。完整示例包含教学用 Profile，实际部署需要配置自己的信任策略。

</details>

<a id="architecture"></a>

<details>
<summary>团队规则、授权、生命周期与架构原理</summary>

4.0 正式规范将 FCoP 定义为“文件原生的 Agent 行为治理协议”：文件承载协议，路径表达当前状态，事件记录迁移历史。

`dev-team` 中的 PM、DEV、QA、OPS 来自 Team/Profile。团队规则需要由宿主采用；连接 MCP 提供工具，模型运行与调度由宿主负责。正式接受、退回、重开和归档需要已采用的 Profile 与可信宿主授权判断。业务代码的并发修改需要工作区隔离与集成审查。

## 从“提交交付”到“验收通过”

每项 TASK 沿有序生命周期前进。4.0 中，每次进入 `active` 都会生成新的尝试身份，提交时关联该次尝试的 REPORT；验收再把审查与授权绑定到当前证据。

<a href="spec/fcop-4.0-spec.zh.md"><img src="assets/fcop-lifecycle.zh.svg" alt="FCoP 4.0 生命周期：待领取、执行、审查、完成、归档；经授权的退回和重开进入新的执行尝试。" width="960" /></a>

4.0 移除了 `active → done` 的直接跳转。普通任务和 Branch 都可通过 `reopen_task` 重开并生成新尝试；旧 REPORT 不能满足新尝试的提交门槛。完整迁移条件见 [C1–C8 英文规范](spec/fcop-4.0-spec.md) · [中文规范](spec/fcop-4.0-spec.zh.md)。

## 多条有序工作流形成并行，收尾有据可查

多项工作可以同时推进。Branch 是通过 `branch_of` 关联到同一 Root 的普通 TASK；同级 Branch 各自保留尝试、报告和审查。由谁执行、何时调度，交给 Runtime 决定。

<a href="docs/architecture.zh.md#parallel-work"><img src="assets/fcop-parallel-work.zh.svg" alt="两个同级 Branch 分别执行、提交报告并接受审查；Root 收尾检查当前证据、汇合记录和归档授权。" width="960" /></a>

带 Branch 的 Root 归档前，FCoP 会检查分支完成状态、各自当前 REPORT、匹配的 `family_digest`、汇合 REVIEW，以及独立的 Root 归档授权。分支重开或报告变化会使旧汇合失效。相关写入只在短暂提交时协调，Agent 执行工作期间不持有这把锁。这里汇合的是工作证据，代码集成仍由应用负责。

## 协议核心保持小，系统职责分清楚

另一种实现应该能够保留相同的工作语义，而无需照搬某个 Python 库、MCP 工具清单或产品。

| 层次 | 负责什么 |
|---|---|
| **Core** | C1–C8：身份、信封、生命周期、关系、汇合、授权、创建幂等、原子恢复。 |
| **Specification** | 定义字段、状态迁移、错误与外部可观察行为。 |
| **Conformance** | 用样例、测试向量和行为测试检查实现是否遵守契约。 |
| **Toolkit** | 实现并提供协议操作；本仓库提供 Python 和 MCP 适配器。 |
| **Profile** | 提供组织策略与签发者权限；PM/DEV/QA 等固定角色不是通用 Core 规则。 |
| **Runtime** | 运行模型与工具，管理会话，调度工作并提供界面。 |

**深入了解设计：[English](docs/architecture.en.md) · [简体中文](docs/architecture.zh.md)。** 专页展开说明为什么用文件、为什么分开交付与验收、如何组织并行，以及 FCoP、MCP 和 Runtime 各自承担什么。

**FCoP 架构原理系列 · 五篇全文**（2026-09-10 发布，已按 4.0 修订）：

1. [Agent 没有操作系统：为什么把工作行为外化到文件系统](docs/fcop-architecture-series/01-work-beyond-context.zh.md)
2. [FCoP Core 到底是什么：从工具箱中提炼最小工作内核](docs/fcop-architecture-series/02-minimal-core.zh.md)
3. [FCoP 不等于它的工具：Core、Specification、Toolkit、Profile 与 Runtime 如何分层](docs/fcop-architecture-series/03-architecture-layers.zh.md)
4. [单机多 Agent 为什么不追求高并发：多串行形成并行](docs/fcop-architecture-series/04-parallel-work.zh.md)
5. [从单机到联网：FCoP、MCP、A2A 与 CodeFlowMu 各自负责什么](docs/fcop-architecture-series/05-mcp-a2a-runtime.zh.md)

[系列导读](docs/fcop-architecture-series/README.md) · [五篇全文合集](docs/fcop-architecture-series/collected.zh.md)

4.0.3 通过包内和 MCP resources 分发**九个双语规则模块**，保留严格清单、`sequential`、`parallel` 及独立的 `repository-development` 装配。**安装 → 连接 MCP → 初始化工作区 → 使用 FCoP。** FCoP 拥有 `<project>/fcop/`，不拥有项目根 Host 指令文件。Host 投影、采用、部署与回滚已退役；`redeploy_rules` 仅支持 Legacy v1–v3，对 v4 零写入拒绝。已有用户文件保持不变。[Rule resources / 规则资源](docs/rule-resources.md)。

</details>

<a id="research"></a>

<details>
<summary>发布、MCP 收录、论文、Zenodo 与历史版本</summary>

**Stable version: 4.0.3** — [4.0.3 发布页面](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.3)。本仓库提供开放协议、`fcop` Python 实现和可选的 `fcop-mcp` 适配器。需要 Python 3.10+；下面的本地示例无需模型 API Key。

</p>

**发现 FCoP：**[MCPServers 介绍页](https://mcpservers.org/servers/joinwell52-ai/fcop)（[中文版](https://mcpservers.org/zh-CN/servers/joinwell52-ai/fcop)）——第三方目录，帮助用户发现和了解 FCoP。**注册信息：**[官方 MCP Registry](https://registry.modelcontextprotocol.io/v0/servers/io.github.joinwell52-AI%2Ffcop/versions/4.0.3)——查看服务标识、版本与安装包元数据。

## 论文、证据与引用



| 资料 | 阅读或引用 |
|---|---|
| **架构白皮书** | [English](essays/from-coordination-to-governance.en.md) · [中文](essays/from-coordination-to-governance.md) — 历史研究背景 |
| **3.2.5 归档** | [Zenodo DOI 10.5281/zenodo.20457285](https://doi.org/10.5281/zenodo.20457285) · [OSF DOI 10.17605/OSF.IO/92NWM](https://doi.org/10.17605/OSF.IO/92NWM) |
| **2026 年 4 月研究快照** | [Zenodo DOI 10.5281/zenodo.19886036](https://doi.org/10.5281/zenodo.19886036) · [引用元数据](CITATION.cff) |
| **17 篇现场报告与设计文章** | [英文目录](essays/README.md) · [中文目录](essays/README.zh.md)，保留原始发布和证据链接 |

引用时请选择与研究版本相符的归档。以上历史 DOI 不代表 4.0.0；讨论当前行为请同时指向版本化发布与规范。

## 三个仓库，三个入口

| 仓库 | 定位 |
|---|---|
| **[FCoP](https://github.com/joinwell52-AI/FCoP)** | **主推开源旗舰库：** 协议、Python 库与 MCP 服务；使用、实现和贡献协作层从这里开始。 |
| **[joinwell52](https://github.com/joinwell52-AI/joinwell52)** | **研究传播入口：** AI Agent、数字员工与工程研究。 |
| **[CodeflowMu-Distribution](https://github.com/joinwell52-AI/CodeflowMu-Distribution)** | **产品体验入口：** 打包应用与[下载](https://github.com/joinwell52-AI/CodeflowMu-Distribution/releases)；支持的版本以产品发布说明为准。 |

FCoP 可按 [MIT 许可证](LICENSE)独立使用；产品分发有自己的许可和发布节奏。

**如果你想持续使用或研究这套协议，欢迎 Star FCoP 收藏。** 也欢迎通过 [Issues](https://github.com/joinwell52-AI/FCoP/issues) 或 Pull Request 提供可复现的接入问题、宿主集成示例和协议行为测试。

## 版本与已有安装

- **4.0.0：** [发布说明](docs/releases/4.0.0.md) · [变更日志](CHANGELOG.md) · [架构决策](adr/README.md)。本次发布经过已记录的 `FCOP_4_STABLE_RELEASE_READY` 门槛；使用者安装上方稳定版 PyPI 包即可。
- **Release candidate: 4.0.0rc1** — 作为[历史预发布版本](https://github.com/joinwell52-AI/FCoP/releases/tag/v4.0.0rc1)保留。
- **3.x 工作区：** 显式迁移前保持原有语义。[旧版英文规范](spec/fcop-v3-spec.md) · [中文](spec/fcop-v3-spec.zh.md)。`finish_task` 和历史工具仍可被发现，但会拒绝 v4 工作区。
- **旧版安装提示词：** [EN](src/fcop/rules/_data/agent-install-prompt.en.md) · [ZH](src/fcop/rules/_data/agent-install-prompt.zh.md)，也可通过 `fcop://prompt/install` 读取。这些是历史安装材料，当前版本请使用上面的 4.0 指南。

</details>
