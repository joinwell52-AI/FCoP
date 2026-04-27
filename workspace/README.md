# workspace/

按 FCoP Rule 7.5 / Rule 7.5 per FCoP protocol.

**项目根只放协作元数据；具体产物（代码、脚本、数据）进
`workspace/<slug>/`，一个目的一个 slug。**

**Project root holds coordination metadata only; actual artefacts
(code, scripts, data) live under `workspace/<slug>/` — one slug per
piece of work.**

- 推荐用 MCP 工具 `new_workspace(slug=..., title=..., description=...)`
  创建 slug 子目录（会落 `.workspace.json` 元数据）。
- 也可以手动 `mkdir workspace/<slug>`，`list_workspaces()` 同样能识别。
- 跨 slug 共享的资产放 `workspace/shared/`（保留 slug）。

- Recommended: MCP tool
  `new_workspace(slug=..., title=..., description=...)`
  (drops a `.workspace.json` marker).
- Or manually `mkdir workspace/<slug>` — `list_workspaces()` will
  pick it up either way.
- Cross-slug shared assets go under `workspace/shared/`
  (reserved slug).

详见 `docs/agents/LETTER-TO-ADMIN.md` § "产物放哪：workspace/<slug>/ 约定".
See `docs/agents/LETTER-TO-ADMIN.md` § "Where artefacts go" for the
full convention.
