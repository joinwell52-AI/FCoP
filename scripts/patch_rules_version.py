"""Patch fcop_rules_version 2.3.0 -> 2.4.0 in AGENTS.md and CLAUDE.md."""
from pathlib import Path

OLD_VER = "2.3.0"
NEW_VER = "2.4.0"

NEW_ENTRY = (
    f"**2.4.0 changes / 2.4.0 变更**（随 `fcop@1.5.0`）:\n\n"
    "- 新增 **RULE_DOC_DRIFT 违规类型**：已部署角色文档内容落后于已安装 `fcop` 版本\n"
    "  超过 1 个 minor 版本，由 `fcop_audit(scope=upgrade/takeover)` 扫描检出。\n"
    "  整改动作：`deploy_role_templates(force=True)`（per ADR-0032 §4.7）\n"
    "- Rule 0–9.7 主体不变。\n\n"
    "**2.3.0 changes / 2.3.0 变更**（随 `fcop@1.3.1`）:"
)
OLD_ENTRY = "**2.3.0 changes / 2.3.0 变更**（随 `fcop@1.3.1`）:"

for fname in ["AGENTS.md", "CLAUDE.md"]:
    p = Path(fname)
    content = p.read_text(encoding="utf-8")
    content = content.replace(f"fcop_rules_version: {OLD_VER}", f"fcop_rules_version: {NEW_VER}")
    content = content.replace(
        f"**Version**: `fcop_rules_version: {OLD_VER}`",
        f"**Version**: `fcop_rules_version: {NEW_VER}`",
    )
    content = content.replace(OLD_ENTRY, NEW_ENTRY)
    p.write_text(content, encoding="utf-8")
    print(f"Updated {fname}")
