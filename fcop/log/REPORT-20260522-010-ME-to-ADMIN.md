---
protocol: fcop
version: 1
kind: report
task_id: TASK-20260522-010
sender: ME
recipient: ADMIN
priority: P1
status: done
thread_key: agent-bringup-prompt-fix
---

# REPORT-010 · §1 改成"让 agent 自己查 PyPI"

## 做了什么 / What got done

### 1. `agent-bringup-prompt.zh.md` §1

把原本只查本地的 2 条命令扩展成 4 条：

```
python --version
pip show fcop fcop-mcp
pip index versions fcop
pip index versions fcop-mcp
```

加入"老 pip 退路"：`python -m pip install --dry-run --upgrade fcop fcop-mcp`，
读 `Would install` 行的版本号当 PyPI 最新。

判断规则改成 4 档（local == latest / local < latest / local > latest /
not installed），明令禁止"可能是 X 或更高"、"需要确认墙内同步"这种废话。

### 2. `agent-bringup-prompt.en.md` §1

英文同步，措辞自然，不中英混杂。`pip index versions` 命令同样作为
权威源给出，老 pip 退路写法一致。

## 结果 / Outcome

`grep` 验证：

```
$ rg "pip index versions|3\.0\.2|frozen at|写定时" agent-bringup-prompt.*.md
```

只剩两类 `3.0.2` 引用：

- §1 区域不再有任何硬编码版本号 ✅
- §5 / §10 历史叙述里"v3.0.2 修了什么"保持不变 ✅（TASK-009 改过的
  那部分没动）
- §1 加入 `pip index versions` × 4 处（中英各 2）✅

## 影响 / Impact

agent 在另一台机器跑 §1 时，**手里同时有本地版本号和 PyPI 最新版**，
没有再"凭印象猜"的余地。如果 agent 还是说"可能是 X 或更高"，那是
agent 选择性不读 prompt，不再是 prompt 自己的洞。

prompt 不再随发版漂移——3.0.3 / 3.1.0 / 4.0.0 发版时，prompt 一字不改
仍然给出正确判断。

## 下一步 / Next

双 commit + push（沿用 TASK-009 的两段式策略）：

- commit A · 产品改动：两份 prompt §1
- commit B · 协作账本：TASK-010 + REPORT-010 + archive
