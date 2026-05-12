"""Patch fcop_protocol_version 2.2.0 -> 2.3.0 in AGENTS.md and CLAUDE.md,
and also update the Protocol Version Log reference."""
from pathlib import Path

OLD_PROTO_VER = "2.2.0"
NEW_PROTO_VER = "2.3.0"

OLD_PROTO_FRONTMATTER = f"fcop_protocol_version: {OLD_PROTO_VER}"
NEW_PROTO_FRONTMATTER = f"fcop_protocol_version: {NEW_PROTO_VER}"

OLD_PROTO_BODY = f"**Version**: `fcop_protocol_version: {OLD_PROTO_VER}`"
NEW_PROTO_BODY = f"**Version**: `fcop_protocol_version: {NEW_PROTO_VER}`"

OLD_LETTER_ZH = "v1.3.0 摘要"
NEW_LETTER_ZH = "v1.5.0 摘要"

OLD_LETTER_EN = "v1.3.0 summary"
NEW_LETTER_EN = "v1.5.0 summary"

for fname in ["AGENTS.md", "CLAUDE.md"]:
    p = Path(fname)
    content = p.read_text(encoding="utf-8")
    content = content.replace(OLD_PROTO_FRONTMATTER, NEW_PROTO_FRONTMATTER)
    content = content.replace(OLD_PROTO_BODY, NEW_PROTO_BODY)
    # Also update letter-to-admin summary block references
    content = content.replace(OLD_LETTER_ZH, NEW_LETTER_ZH)
    content = content.replace(OLD_LETTER_EN, NEW_LETTER_EN)
    # Update fcop-rules.mdc references to old rules version
    content = content.replace("fcop-protocol.mdc 2.1.0", "fcop-protocol.mdc 2.2.0")
    content = content.replace("fcop-rules.mdc 2.3.0", "fcop-rules.mdc 2.4.0")
    p.write_text(content, encoding="utf-8")
    print(f"Updated {fname}")
