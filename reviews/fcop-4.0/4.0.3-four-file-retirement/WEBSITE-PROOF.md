# Website and CLI entry proof

Actual source: scripts/pages/index.template.html; generator: scripts/pages/build.py; output: docs/index.html. Existing public baseline was already 4.0.2, not 4.0.0.

`python scripts/pages/build.py --check`: 14 generated text files and local logo match sources. No production Pages deployment was invoked.

ADMIN CLI supplement implemented in README.md, README.zh.md, fcop-README.pypi.md, mcp/README.md and the homepage. All nine commands have purposes. Core and optional MCP install examples are directly visible. CLI = Setup + Observe + Diagnose; MCP = Work. doctor is local/offline/no Host mutation; work operations stay in MCP/Python.

Automated supplement checks: **8/8** including structural visibility before/without details, nine-command inventory, exact self-check examples, offline doctor effects and actual installed console execution. The test uses the public fcop console entry, not unsupported python -m fcop.

Browser preview: local generated page at http://127.0.0.1:18403/?lang=zh#cli, inspected in Chinese and English. The command table and Install & Verify blocks are visible while the separate technical-reference details remain collapsed; screenshots were visually inspected in the app at its default narrow viewport. No clipping observed in the inspected sections. This is local preview evidence, not public deployment or a claim of an exhaustive device matrix.

Registry badge retains the last checked 4.0.2 record and explicitly marks its update pending release authorization. The existing Zenodo DOI remains labeled 4.0.2 rather than falsely acquiring the new package version. No Registry or Zenodo operation was performed.

Upstream PR #49 merged while this implementation was being verified. The review branch incorporates main aa970936f19b875720c4b17608bb3c17b7fb195c with a history-preserving merge b767e8f46ede33d405a96ba568dc38b4e733b3ec. Its handoff documentation, example and README links remain intact. The only conflict was the generated homepage: the upstream bilingual handoff paragraph was added to the real template and output regenerated, preserving both the new example and visible CLI section. Upstream's explicitly published 4.0.2 demo pins were not falsely upgraded to an unpublished version. No merge into main was performed.
