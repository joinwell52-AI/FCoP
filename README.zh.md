# FCoP — File-based Coordination Protocol

[English](README.md) · [简体中文](README.zh.md) · [Homepage](https://joinwell52-ai.github.io/FCoP/)

FCoP 通过 TASK / REPORT / ISSUE / REVIEW 文件治理协作。它是协议，不是调度器、Agent Runtime、消息中间件或数据库。

- **Stable version: 4.0.0** — 稳定发布制品，公开发布须经 WP4F Gate。
- **Release candidate: 4.0.0rc1** — 已公开发布的历史预发布版，保持不变。
- **4.0 MCP: 46 tools / 12 resources / 4 resource templates**。

## 协议级 Major 升级

Python Core（`fcop`）负责校验和文件系统行为。可选 MCP Adapter（`fcop-mcp`）将公共调用路由到 Core，不独立解释或实现协议。

4.0 提供 Workspace 身份、四类强类型信封、Branch、显式收敛、授权绑定、持久幂等、并发线性化、崩溃恢复和版本化规则分发。八项可测试合同为 C1 工作区身份、C2 信封、C3 生命周期、C4 关系、C5 收敛、C6 授权、C7 幂等、C8 原子恢复。历史七个架构概念不能代替 C1–C8。

原有 **45 个 MCP 工具名称获得 4.0 版本路由及协议语义**；新增名称为 **T6 `reopen_task`**，合计 **46**。T6 是 `done → active`，**不是 Branch 专用工具**。可发现不代表所有历史动作都支持 v4：`finish_task` 与 history 工具拒绝 v4；不新增 `close_issue`。

并发是共同写入合同，不是独立工具：原子写入、线性化、持久 `operation_id`、精确重试、冲突拒绝、零副作用失败、恢复以及一致的 `family_digest`。锁和收据是必要机制；actor 字段或一次 rename 都不产生授权。

## 稳定版安装

使用新的虚拟环境；在当前 shell 激活后安装：

```bash
python -m venv .venv
python -m pip install fcop==4.0.0 fcop-mcp==4.0.0
```

## 候选版安装

Stable 公开发布前，取得 WP4F Manifest 锁定的制品及 SHA-256，核验后安装到**另一个全新的虚拟环境**。历史 RC 继续单独保留：

```bash
python -m pip install ./candidate/fcop-4.0.0-py3-none-any.whl ./candidate/fcop_mcp-4.0.0-py3-none-any.whl
python -c "from importlib.metadata import version; print(version('fcop'), version('fcop-mcp'))"
```

Stable 精确组合为 `fcop==4.0.0 / fcop-mcp==4.0.0`；适配器依赖声明为 `fcop>=4.0.0,<4.1.0`。不得混装不同发布线。现有 3.x 工作区保持原语义；安装不授权迁移、重新部署规则或升级下游。

## 最小 Python 入口（已核验 4.0）

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from fcop import Project

with TemporaryDirectory(prefix="fcop-demo-") as directory:
    project = Project(Path(directory) / "workspace")
    workspace = project.create_workspace(protocol_version="4.0")
    request = dict(
        workspace_id=workspace["workspace_id"], operation_id="demo-create-1",
        sender="ME", recipient="ME", subject="First task", body="Read-only research",
    )
    first = project.create_task(**request)
    again = project.create_task(**request)
    assert again["existing"] and again["task_id"] == first["task_id"]
    print(first["task_id"])
```

## 最小 MCP 入口（已核验 4.0）

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

替换两个路径。Windows 使用绝对 `.venv/Scripts/fcop-mcp.exe` 路径。禁止将演示指向现有工作区。调用 `init_solo(role_code="ME", protocol_version="4.0")`，再使用返回的 `workspace_id` 和明确的 `operation_id` 调用 `create_task`。

默认可信 Profile 注册表为空。T4–T7 需要在**可信服务端初始化**注册已采用的 evaluator。调用者代码、YAML、`actor` 和单独的 `profile_ref` 不产生授权。[独立 MCP 样例](examples/v4/third-party/mcp-only/client.py) 只调用公共 stdio JSON-RPC，客户端不导入两个包。其服务端 evaluator **仅用于教学，不是生产安全策略**。

## Branch 与显式收敛

以下是参数映射，不是省略必需证据后仍可运行的代码：

```text
create_task(branch_of=...)
inspect_task(include_family_digest=true)
write_report(attempt_id=...)
write_review(review_kind="convergence", family_digest=..., references=...)
archive_task(review_ref=..., family_digest=...)
```

创建 Root 和两个 Branch。每个 Branch 使用当前 `attempt_id` 的 REPORT 及 acceptance 授权完成，再完成 Root。查询 canonical family digest，追加引用 Branch REPORT heads 的 convergence REVIEW，携带收敛证据及独立的 digest 绑定 T7 授权归档 Root。Core 在 family lock 内重新核验；digest 变化或授权复用被拒绝。REPORT/REVIEW 保持不可变。

## 版本化规则与兼容

九个双语模块形成 18 份 canonical 规则和一个 Manifest。装配为 `sequential`、`parallel`、`repository-development`。普通业务 Agent 规则与仓库开发规则分开。静态 Host profile 选择确定性 `reference` / `bounded_embed` 投影。采用、零写入计划、部署收据和回滚均显式执行。无 Host 探测、自动迁移或后台服务。disk、index、adoption、Host entry 与 Runtime consumption 是不同层次事实。

## 文档与历史

- [4.0 EN](spec/fcop-4.0-spec.md) / [4.0 ZH](spec/fcop-4.0-spec.zh.md)
- [3.x EN](spec/fcop-v3-spec.md) / [3.x ZH](spec/fcop-v3-spec.zh.md)
- [MCP tools](docs/mcp-tools.md) / [MCP Adapter](mcp/README.md)
- [RC guide](docs/fcop-4.0/rc-candidate-guide.md) / [Python example](tests/stable/third-party/python-only/app.py)
- [CHANGELOG](CHANGELOG.md) / [ADR index](adr/README.md)
- [Research EN](essays/when-ai-organizes-its-own-work.en.md) / [研究 ZH](essays/when-ai-organizes-its-own-work.md)
- [License](LICENSE) / [Citation](CITATION.cff)
- 仅限历史版本的安装提示词：[EN](src/fcop/rules/_data/agent-install-prompt.en.md) / [ZH](src/fcop/rules/_data/agent-install-prompt.zh.md)，也可通过 `fcop://prompt/install` 发现。这些历史提示词不授权 RC 安装或迁移。

历史教程仅描述标明的版本，不是自动升级到 4.0 的指令。历史 3.2.5 归档为 [DOI 10.5281/zenodo.20457285](https://doi.org/10.5281/zenodo.20457285)，注册记录为 [OSF 92nwm](https://osf.io/92nwm/)。二者不代表 4.0.0；本轮不创建新 DOI 或 Registry 记录。

## 发布边界

WP4F 将已验收 RC 提升为 Stable，不增加协议或业务行为。Phase A 验证可复现 Stable 制品和真实客户端。发布及指定本机 MCP 升级需要 ADMIN 的 `FCOP_4_STABLE_RELEASE_READY` Gate。保留 RC，不设观察期，不引入自动工作区迁移、Registry 或 Zenodo 更新。参见 [4.0.0 release notes](docs/releases/4.0.0.md)。
