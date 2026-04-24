# 升级 `fcop` / `fcop-mcp`（0.6.x 小版本）

面向**已经**在用 PyPI 上 `fcop` 与/或 `fcop-mcp` 的用户。从 **0.5.x** 跨大版本请先看 [MIGRATION-0.6.md](./MIGRATION-0.6.md)。

## 原则

- 两包**同一大版本线齐发**（如 `0.6.2`），见 [ADR-0002](../adr/ADR-0002-package-split-and-migration.md)。日常升级**建议一起升**，避免只升其一导致依赖不对齐。
- **0.6.x 内** MCP 工具形态**只增不改**（[ADR-0003](../adr/ADR-0003-stability-charter.md)），升级后一般**不必**改 `mcp.json` 结构，除非换启动方式（如 `uvx` ↔ 固定 venv 的 `python -m`）。

## 用 pip（推荐，与 `mcp.json` 里使用的 Python 同一 venv）

在**你运行 MCP 的那个环境**里执行：

```bash
pip install -U "fcop" "fcop-mcp"
```

若需钉到当前小版本，例如 0.6.2（把数字换成你需要的版本）：

```bash
pip install -U "fcop==0.6.2" "fcop-mcp==0.6.2"
```

## 用 uvx 启动的

- `uvx` 会解析并拉取；若首连慢或缓存异常，以 [mcp/README.md](../mcp/README.md) 为准，可考虑改为**独立 venv + `python -m fcop_mcp`**，之后只在 venv 里用 `pip install -U` 升级，行为更稳。

## 升级后

1. **完全重开** Cursor 或 *Developer: Reload Window*，让 MCP 加载新装包。
2. 自检（与 mcp 文档一致）：

```bash
python -c "from fcop import Project; print('fcop OK', Project)"
python -c "from fcop_mcp.server import mcp; print('fcop-mcp OK')"
```

## 发版与 PyPI 说明

- 维护者发版流程、tag 与 CI 见 [release-process.md](./release-process.md)。  
- 各版本变更摘要见 [CHANGELOG.md](../CHANGELOG.md) 与 `docs/releases/*.md`。

## English (short)

- Bump **both** `fcop` and `fcop-mcp` in the same venv: `pip install -U "fcop" "fcop-mcp"`.  
- Full install paths and `mcp.json` templates: [mcp/README.md](../mcp/README.md).
