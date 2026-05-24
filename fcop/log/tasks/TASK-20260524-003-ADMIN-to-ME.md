---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P2
thread_key: ai-must-write-it-down-20260524
subject: 在中英文文章末尾直接展示聊天截图附记
---

## 背景
ADMIN 希望 `essays/ai-must-write-it-down.md` 与 `essays/ai-must-write-it-down.en.md` 不只链接证据目录，而是在文章后面直接展示聊天截图。

## 要求
- 中文文章末尾加入“附记：聊天截图”并直接嵌入 6 张截图。
- 英文文章末尾加入英文版 appendix/note，说明文字与截图标题需翻译为英文。
- 保留现有题图、正文与证据索引链接。

## 验收
- 两篇文章底部能直接看到聊天截图。
- 英文版附记为英文。
- Markdown 无诊断错误。