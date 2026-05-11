# 本机工作区（`D:\FCoP`）与 Bridgeflow 的关系

> 本文件说明 **`D:\FCoP` 独立工程** 与 **`D:\Bridgeflow`（CodeFlow 主仓）** 的分工，避免两套路径混用。

## 1. 本目录从哪里来

- **主来源**：`D:\Bridgeflow\private\fcop-repo` 与 **GitHub `https://github.com/joinwell52-AI/FCoP`** 同构（已含 `.git`、协议正文、`src/fcop`、`mcp` 子包等）。
- **补充同步**：`mcp\src\fcop_mcp\` 下的 Python 源码，已从 `D:\Bridgeflow\fcop-mcp\fcop_mcp\` **按文件覆盖** 到本仓 `mcp\` 的 **`src\fcop_mcp\`** 布局，以便与当前 Bridgeflow 上正在推的 `fcop-mcp` 开发线（如 **0.6.2**）对齐。

**注意**：FCoP 主仓的规范布局是 `mcp/` 为独立包（`mcp\pyproject.toml`，代码在 `mcp\src\fcop_mcp\`），与 Bridgeflow 里顶层 `D:\Bridgeflow\fcop-mcp\fcop_mcp\` 的目录层级不同，但发布内容一致；日常以 **`D:\FCoP\mcp`** 为准发版/开发。

## 2. 与 `Bridgeflow\codeflow-plugin` 的区别

| 项目 | 说明 |
|------|------|
| **`D:\FCoP\src\fcop`** | **0.6+ 拆分后**的协议库：无 `fastmcp`、无 LLM 依赖，纯协议与 `Project` API。 |
| **`D:\Bridgeflow\codeflow-plugin\src\fcop`** | **历史路径**：曾作为 PyPI 包名 `fcop` 的发布目录、含旧式 `_data` 等布局；**不要**与主仓 `FCoP` 的 `src\fcop` 直接当作「同一工作树双写」。 |

新协议、新 API、MCP 工具面请以 **`D:\FCoP`** 或 **GitHub FCoP 仓** 为准；Bridgeflow 内如仍有 `codeflow-plugin` 仅作 **CodeFlow 老文档/联调引用** 时保留，应逐步切到 `pip` / 可编辑安装 或子模块 指向 FCoP。

## 3. 本地可编辑安装（开发）

在 **`D:\FCoP` 根目录**：

```bash
py -3.10 -m pip install -e .
py -3.10 -m pip install -e mcp
```

自测版本：

```bash
py -3.10 -c "import fcop; from fcop_mcp import __version__ as m; print(fcop.__version__, m)"
```

## 4. Git 说明

- `origin` 应指向 `joinwell52-AI/FCoP`；在推送前用 `git status` 确认与远程分支的意图一致。
- 从 `private\fcop-repo` 拷到 `D:\FCoP` 时，**工作区未提交改动**会原样带来；与 Bridgeflow 的 `fcop-mcp` 覆写会体现在 `mcp\` 相关 diff 上，提交前请自行审阅。
