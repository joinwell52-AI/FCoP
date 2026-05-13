---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-007
sender: ADMIN
recipient: ME
priority: P1
parent: TASK-20260513-006
related: [TASK-20260513-005, TASK-20260513-006]
thread_key: essay-13-evolution-reverse-absorption-publication
session_id: sess-20260513-me-01
---

# 翻译 essay #13 至英文版 / Translate essay #13 to English

## 背景 / Background

ADMIN 在 12:06 给出指令:

> Evolution, Reverse Absorption / 演化，反向吸收 ；英文版本也要的；

中文版 `essays/evolution-reverse-absorption.md`(401 行)已在 commit `523d81e` 发表,
但所有三处索引(README.md / README.zh.md / essays/README.md)在 row #13 都标了
"English translation pending"。本任务交付英文版 + 移除"pending"标注。

参照先例:essay 11(`looking-without-touching.md` 231 行)与 `looking-without-touching.en.md`(238 行)
是完整翻译,而非摘要——本任务沿用同样标准。

## 范围 / Scope

### 必须交付 / Must deliver

1. **`essays/evolution-reverse-absorption.en.md`** —— 完整英文翻译,体量与中文版接近(~400 行)。
   - frontmatter 字段完整翻译(`audience` / `length` 等)
   - 所有章节标题保留双语对照(`## 先看两张图 / The Two Diagrams at a Glance` 风格)
   - 两张 ASCII 图本身保留原样不翻译(图内文字已经是双语)
   - ADMIN 引语段落保留原中文 + 加英文译注
   - 所有协议术语(Reverse Absorption / Evolution / Emergence / Boundary 等)与既有
     `looking-without-touching.en.md` / `fcop-rules.mdc` 中的英文术语保持一致

2. **3 处索引更新**(把 "English translation pending" 注释删除并加链接):
   - `README.md` row 13
   - `README.zh.md` row 13(添加 `[GitHub English]` 链接)
   - `essays/README.md` row 13(添加 `[English]` 链接)

### 不动 / Out of scope

- ADR-0034 不翻译(那是协议内部文档,沿用 ADR 默认中文为主、英文为辅风格)
- ASCII 图不翻译(图本身已经是双语)
- 题图(`evolution-reverse-absorption-cover.png`)文字已经是英文,不需要重做

## 交付时间 / Delivery

ADMIN 没给死期,但语气催促("英文版本也要的")——按"快速但不牺牲质量"标准执行。
预估单一 session 内完成。

## 验收标准 / Acceptance Criteria

1. `essays/evolution-reverse-absorption.en.md` 文件存在,完整翻译,frontmatter 合法。
2. 三处索引已更新到带英文链接的形式,与 essay 11 row 在各索引的呈现方式一致。
3. 翻译保持协议术语一致性(查 essay 11 英文版 + fcop-rules.mdc 词汇表,不创造新术语)。
4. 所有内容准确传达原文意思——"反向吸收"作为核心术语,首次出现时给出英文锚定
   `Reverse Absorption (反向吸收)`,后续可单用英文。
5. commit 信息描述清楚交付物 + push 到 origin/main。

## 风险等级 / Risk level

`low` —— 翻译工作,append-only(只新增 .en.md 文件 + 索引行修订),不改动既有产物的语义。

## 闭环 / Loop closure

完成后 `archive_task(TASK-20260513-007)` + `archive_task(TASK-20260513-006)`(如 ADMIN 同意),
并写 `REPORT-20260513-007-ME-to-ADMIN.md` 落账本。
