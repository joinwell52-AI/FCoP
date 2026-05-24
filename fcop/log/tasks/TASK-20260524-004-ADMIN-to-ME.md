---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P2
thread_key: ai-must-write-it-down-20260524
subject: 按原始文件名编号修正聊天截图顺序
---

## 背景
ADMIN 指出 `ai-must-write-it-down` 文章附记中的聊天截图顺序不对。原始文件名顺序为 `落地成文聊天1.png` 到 `落地成文聊天6.png`，应按文件名编号排序。

## 要求
- 按系统保存文件名中残留的原始编号 `_1` 到 `_6` 重新覆盖 `essays/ai-must-write-it-down-evidence/screenshot-01..06`。
- 更新中英文文章附记中的说明顺序，使其与截图内容一致。
- 保持题图不变。

## 验收
- `screenshot-01..06` 与原始 `落地成文聊天1..6.png` 顺序一致。
- 中英文文章说明与图片顺序一致。
- Markdown 无诊断错误。