# 从空文件夹到 2 人团队的贪吃蛇——FCoP 上手教程

> **预计时长**：约 35 分钟（装 5 分钟 + solo 写贪吃蛇 15 分钟 + 切团队 5 分钟 + 双人模式 10 分钟）
>
> **前置要求**：装好 [Cursor](https://cursor.com/)、网络能连 PyPI；不需要预装 Python 或 `uv`，AI 自己装。
>
> **演示了什么**：自动装 `fcop-mcp` → solo 模式起步 → 一句话切 2 人团队 → 老归档不丢 → 新角色上岗 → 双人协作完成新功能。即把 [Rule 0.a.1（task → do → report → archive）](../../src/fcop/rules/_data/fcop-rules.mdc)、[Rule 1（角色唯一性）](../../src/fcop/rules/_data/fcop-rules.mdc)、[Rule 5（追加不删）](../../src/fcop/rules/_data/fcop-rules.mdc)、[ADR-0006（host-neutral 规则分发）](../../adr/ADR-0006-host-neutral-rule-distribution.md) 在一个具体项目里跑一遍。
>
> **截图缺失**：本教程截图来自一台真实电脑实操；如果你看到的是占位标记 `[截图：...]`，说明本仓还没上传该截图，按文字也能完整跟做。

---

## 第 0 章：5 分钟，让 AI 自己把 fcop-mcp 装到 Cursor

打开 Cursor，新建一个空文件夹（比如 `~/snake-demo` 或 `D:\snake-demo`），在 Cursor 里打开它。Cursor 聊天框粘贴下面这段 prompt 给 AI：

```text
帮我把 fcop-mcp 装到 Cursor，全程你来跑命令。要求：

1. 先识别我的系统：终端跑 `uname -s 2>$null; echo $env:OS` 看一眼是 Windows 还是 macOS。
2. 装 uv（如果还没有）。一行命令：
   - Windows PowerShell: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   装完跑 `uvx --version` 确认。
3. 在全局 mcp.json 里加 fcop entry。**保留**已有的其他 mcp servers，不要覆盖：
   - Windows 路径: `%USERPROFILE%\.cursor\mcp.json`
   - macOS 路径: `~/.cursor/mcp.json`
   - 加到 mcpServers 对象里这一段：
     "fcop": { "command": "uvx", "args": ["fcop-mcp"] }
4. 把最终的 mcp.json 完整内容打印给我看。
5. 提醒我重启 Cursor；首次启动 fcop-mcp 会下载依赖，**等 30 秒到 1 分钟**，不要急着关掉或重连。

每完成一步报告结果再走下一步。
```

AI 会一步步跑命令并展示输出。

`[截图 0-1：AI 跑完后展示的 mcp.json 内容]`

**重启 Cursor**，等首次依赖下载（半分钟），然后在聊天里输入：

```text
fcop_report()
```

如果看到类似下面的报告，说明 fcop-mcp 已经接上：

```
=== FCoP UNBOUND 报告 ===
项目 / project: ~/snake-demo  (来源: cwd fallback ...)
[版本 / Versions]
  fcop-mcp:  0.7.2
  fcop:      0.7.2
  rules:     （项目本地未部署）| 包内 1.8.0
  protocol:  （项目本地未部署）| 包内 1.6.0
状态：未初始化（no docs/agents/fcop.json）
```

`[截图 0-2：fcop_report() 第一次输出，UNBOUND 状态]`

> **如果版本不是 `0.7.2`**：你的 `uvx` 缓存还在旧版本上。让 AI 跑 `uv cache clean fcop fcop-mcp`，然后重启 Cursor 再试。

**这一步 FCoP 在做什么**：还什么都没做。`fcop-mcp` 只是接上了，整台机器不知道你要做什么项目、用哪个团队。它只敢报告 PyPI 包版本和"项目未初始化"。这是 [Rule 1 两阶段启动](../../src/fcop/rules/_data/fcop-rules.mdc)的第 0 阶段——**先识别项目，再分配角色**，绝不假设。

---

## 第 1 章：solo 模式起步，写贪吃蛇 v1

继续在同一个 Cursor 会话里：

```text
1. set_project_dir("D:/snake-demo")    # 改成你刚才打开的文件夹路径
2. init_solo(role_code="ME", lang="zh")
3. fcop_report()
```

AI 会依次调三个工具。第二个工具调完后，你的文件夹会多出这些东西：

```
snake-demo/
├── .cursor/
│   └── rules/
│       ├── fcop-rules.mdc       ← Cursor 自动注入到 LLM 的协议规则
│       └── fcop-protocol.mdc
├── AGENTS.md                    ← Codex/通用 host 读这份
├── CLAUDE.md                    ← Claude Code CLI 读这份
├── docs/
│   └── agents/
│       ├── fcop.json            ← 团队配置：mode=solo, roles=[ME]
│       ├── LETTER-TO-ADMIN.md   ← 给你（ADMIN）的说明书
│       ├── shared/
│       │   ├── TEAM-README.md
│       │   ├── TEAM-ROLES.md
│       │   ├── TEAM-OPERATING-RULES.md
│       │   └── roles/ME.md
│       └── tasks/ reports/ issues/ log/
└── workspace/
    └── README.md                ← AI 写代码的"笼子"，规则 7.5
```

`[截图 1-1：init 完成后的目录树]`

**打开 `docs/agents/LETTER-TO-ADMIN.md` 读一遍**——这封信是 FCoP 给你（管理员）的使用说明书，不是给 AI 看的。它会告诉你怎么分配角色、怎么切团队、注意什么红线。

`[截图 1-2：LETTER-TO-ADMIN.md 头几屏]`

现在告诉 AI 它是谁，并下达任务：

```text
你是 ME。任务：用 HTML5 Canvas 写一个 200 行以内的贪吃蛇，
键盘方向键控制，吃到食物 +1，撞墙或撞自己结束。

按 Rule 0.a.1 四步走：
1. 先 write_task(sender="ADMIN", recipient="ME", priority="P1", title="Snake v1", body="...")
2. 实现到 workspace/snake/ 目录下
3. write_report(sender="ME", recipient="ADMIN", title="Snake v1 done", body="...")
4. archive_task("TASK-...")
```

AI 应该依次调用这些 fcop-mcp 工具：

| 步骤 | 工具 | 落盘文件 |
|---|---|---|
| 1 | `write_task(...)` | `docs/agents/tasks/TASK-YYYYMMDD-001-ADMIN-to-ME.md` |
| 2 | （写代码，不是 fcop 工具） | `workspace/snake/index.html` + `snake.js` |
| 3 | `write_report(...)` | `docs/agents/reports/REPORT-YYYYMMDD-001-ME-to-ADMIN.md` |
| 4 | `archive_task(...)` | TASK 和 REPORT 一起搬到 `docs/agents/log/tasks/` 和 `log/reports/` |

`[截图 1-3：AI 调 write_task 后聊天里返回的 TASK 文件路径]`

`[截图 1-4：贪吃蛇游戏在浏览器里能跑]`

最后跑一次 `fcop_report()`，应该能看到：

```
[角色占用 / Role occupancy]
  ME    OCCUPIED   ← 因为 log/ 下有以 sender=ME 的归档文件
[审计 / drift]
  无漂移
```

**这一步 FCoP 在做什么**：

- `init_solo` 一次性把 4 套东西落盘：协议规则（Cursor + Codex + Claude 三家通吃，[ADR-0006](../../adr/ADR-0006-host-neutral-rule-distribution.md)）、团队三层文档（README + ROLES + OPERATING-RULES）、`fcop.json` 项目配置、`workspace/` 代码笼子。**这是 0.6.4 修过的"init 一次性落齐"承诺**。
- AI 走完四步循环后，TASK 和 REPORT **不被删除**——它们从 `tasks/` 移到 `log/tasks/`，作为永久历史。这是 [Rule 5 追加不删](../../src/fcop/rules/_data/fcop-rules.mdc)。
- "ME OCCUPIED" 不是 AI 自己声称的，是 fcop-mcp **扫 `log/` 下落盘文件**得出的结论：因为有文件以 `sender: ME` 出现过，所以 ME 角色已"被占用"。这是 [Rule 1 角色唯一性 0.7.0 协议升级](../releases/0.7.0.md)的核心。

---

## 第 2 章：一句话切到 2 人团队（戏剧性最强的一章）

贪吃蛇 v1 跑通了。现在你想升级成双人模式（WASD + 方向键），需要拆给"产品经理"和"开发"两个角色协作。下一句 prompt：

```text
ADMIN 切团队。把 solo 升级成 2 人团队（PM + DEV，PM 当 leader）：

create_custom_team(
  team_name="Snake Duo",
  roles="PM,DEV",
  leader="PM",
  lang="zh",
  force=True
)

切完后跑 fcop_report() 和 fcop_check()，告诉我：
1. 老的 ME 角色文件去哪儿了？
2. 新的 PM 和 DEV 现在是 OCCUPIED 还是 UNBOUND？
3. .fcop/migrations/ 下有什么？
```

AI 调完 `create_custom_team` 之后，FCoP 会做这些事：

| 旧文件 | 命运 |
|---|---|
| `docs/agents/fcop.json`（mode=solo） | 归档到 `.fcop/migrations/<时间戳>/fcop.json` |
| `docs/agents/shared/`（solo 团队的三层文档） | 归档到 `.fcop/migrations/<时间戳>/shared/` |
| `docs/agents/LETTER-TO-ADMIN.md` | 归档到 `.fcop/migrations/<时间戳>/LETTER-TO-ADMIN.md` |
| `docs/agents/log/`（贪吃蛇 v1 的 TASK + REPORT） | **不动**——历史就是历史 |
| `workspace/snake/`（贪吃蛇代码） | **不动**——产品就是产品 |

新落盘的：

| 新文件 | 内容 |
|---|---|
| `docs/agents/fcop.json` | mode=custom, roles=[PM, DEV], leader=PM |
| `docs/agents/LETTER-TO-ADMIN.md` | 新团队的说明书 |
| `docs/agents/shared/` | 空目录（自定义团队没有内置三层文档；需要时 ADMIN 自己拷） |
| `.fcop/migrations/<时间戳>/` | 一份完整的"切团队前快照" |

`[截图 2-1：.fcop/migrations/<时间戳>/ 文件夹打开的样子，看到旧 fcop.json 和旧 shared/]`

`fcop_report()` 现在应该这样：

```
[团队 / Team]
  mode:   custom
  roles:  PM, DEV
  leader: PM

[角色占用 / Role occupancy]
  PM    UNBOUND        ← 还没人写过任何以 PM 为 sender 的文件
  DEV   UNBOUND        ← 同上
```

`fcop_check()` 会发现一个有意思的事——历史归档里有以 `sender: ME` 的文件，但 ME 不在当前 roster 里：

```
[历史角色 / historical roles]
  ME    出现于 log/tasks/TASK-...md, log/reports/REPORT-...md
        当前 roster: [PM, DEV]，ME 不再适用
        建议：作为项目历史保留；不需要"恢复"
```

`[截图 2-2：fcop_report() 切完团队后的输出，新角色 + 历史角色对照]`

**这一步 FCoP 在做什么**——这是整个教程最值得记住的一段：

- **无损迁移**：`force=True` 不是"覆盖"，是"归档后写新的"。`.fcop/migrations/` 像是 git 给你做的本地时光胶囊，不需要 git 也能看到"切团队前的样子"。
- **历史不灭**：贪吃蛇 v1 是 ME 写的——ME 这个角色已经从 roster 里下岗了，但 v1 的所有 TASK / REPORT 仍在 `log/` 里完整可查。这就是 [Rule 5 追加不删](../../src/fcop/rules/_data/fcop-rules.mdc)的实际表现。
- **新角色一开始都是 UNBOUND**：`fcop-mcp` 不会偷偷帮你"分配"PM 给 AI。**只有 ADMIN（你）显式说"你是 PM"**，AI 才能以 PM 落盘文件，然后 PM 才会从 UNBOUND 变 OCCUPIED。这是 [Rule 1 两阶段启动 + 角色唯一性](../../src/fcop/rules/_data/fcop-rules.mdc)。
- **ADMIN 不变**：你切团队、归档、新角色上岗，全程 ADMIN 这个身份不动——它是协议层保留的"真人管理员"，跟具体哪个 team 解耦。

---

## 第 3 章：PM + DEV 协作做双人模式

现在告诉 AI 它是 PM，下需求：

```text
你是 PM。新需求：把贪吃蛇升级成双人模式
（WASD 控制蛇 1，方向键控制蛇 2，两条蛇，撞墙/撞自己/撞对方都死，最后存活者胜）。

按 Rule 0.a.1：先用 write_task 把任务拆给 DEV（recipient="DEV", priority="P1"），
等会儿 DEV 完成、写好 REPORT 给你，你 review 后 archive。
```

AI 以 PM 身份调 `write_task(sender="PM", recipient="DEV", ...)`，落盘 `TASK-YYYYMMDD-002-PM-to-DEV.md`。

然后**切角色**——这一步是教程最容易踩坑的地方，也是 0.7.1 加进来的[`session_id ↔ role` 一致性审计 + 软角色锁](../releases/0.7.1.md)派上用场的地方：

```text
ADMIN 切角色。**你现在不再是 PM，你是 DEV。**
读最新的 TASK 文件（recipient=DEV 的那份），按要求实现，
写完后 write_report(sender="DEV", recipient="PM", ...)。
```

如果你只在同一个 Cursor 会话里换身份，0.7.1 的软角色锁会在 `.fcop/proposals/role-switch-<时间戳>.md` 落一份"角色切换证据"——记录这个 session 之前以 PM 落了什么文件、什么时候切到 DEV——不阻断，只留证据。

`[截图 3-1：.fcop/proposals/role-switch-...md 文件内容]`

DEV 实现 + 写 REPORT 后，再切回 PM review + archive：

```text
ADMIN 切角色。你是 PM。读 DEV 刚交的 REPORT，
如果验收通过，archive 对应的 TASK。
```

最终 `fcop_report()`：

```
[角色占用 / Role occupancy]
  PM    OCCUPIED   ← 写过 TASK + 做过 archive
  DEV   OCCUPIED   ← 写过 REPORT
```

`fcop_check()` 会显示这个 session 既以 PM 又以 DEV 落过盘——是预期的"ADMIN 主动切换"模式（不是 sub-agent 偷换身份），有 `.fcop/proposals/role-switch-*.md` 证据兜底。

`[截图 3-2：贪吃蛇 v2 双人模式跑起来的样子]`

**这一步 FCoP 在做什么**：

- **PM 和 DEV 用的是同一份 fcop-mcp 工具**，但落盘文件**因身份不同被强制分流**：以 PM 写的去 `tasks/`（指派给 DEV），以 DEV 写的去 `reports/`（回给 PM）。文件名里的 `-PM-to-DEV` 和 `-DEV-to-PM` 是协议级的可追溯链。
- **同一 session 切角色不被阻断，但有审计**——这是 0.7.1 的设计取舍：硬阻断会让"sub-agent 替工"的合法用法（PM 调一个 sub-agent 帮自己整理资料）也被误伤，所以选了"软锁 + 留证据"。详见 [`docs/releases/0.7.1.md` ISSUE-004 一段](../releases/0.7.1.md)。
- **archive 是协议性动作，不是 git mv**：`archive_task` 同时把 TASK 和它配对的 REPORT 都搬到 `log/`，并且 fcop-mcp 知道哪份 REPORT 配哪份 TASK——因为 REPORT 的 frontmatter 里有 `related_task: TASK-...`。

---

## 结尾：彩蛋——`docs/agents/log/` 是最有说服力的演示

打开你刚才那个 `snake-demo/` 文件夹，浏览：

```
snake-demo/
└── docs/agents/log/
    ├── tasks/
    │   ├── TASK-YYYYMMDD-001-ADMIN-to-ME.md      ← 贪吃蛇 v1 任务
    │   └── TASK-YYYYMMDD-002-PM-to-DEV.md        ← 双人模式任务
    └── reports/
        ├── REPORT-YYYYMMDD-001-ME-to-ADMIN.md    ← v1 完工报告
        └── REPORT-YYYYMMDD-002-DEV-to-PM.md      ← v2 完工报告
```

**这就是项目历史的全部**。没有数据库、没有云端服务、没有 webhook。一个文件夹 + git，能完整复盘"这个项目从 solo 起步、切到 2 人团队、最后双人模式跑起来"的每一步谁说了什么、什么时候做的、改了什么、为什么 archive。

要再戏剧性一点，看看这个仓库自己的 [`docs/agents/log/`](../agents/log/)：[`fcop-mcp` 自己也是用 `fcop-mcp` 开发的](../../README.md)。0.7.0 → 0.7.1 → 0.7.2 三次发版的所有 ISSUE / TASK / REPORT 都在那里——包括 0.7.2 那个让我们多发一次的"frontmatter 写错版本号"bug 的[完整复盘](../releases/0.7.2.md)。

那一刻你会理解，为什么 FCoP 把它的标语写成"**filename is the protocol**"。

---

## 常见问题

**Q：第 0 章重启 Cursor 后 `fcop_report()` 报错或工具列表没有 `fcop_*`？**
A：等 30-60 秒（首次 `uvx` 拉依赖）。还不行，让 AI 跑 `uv cache clean fcop fcop-mcp` 然后再重启。

**Q：`fcop_report()` 显示 `rules: 1.7.0` 而不是 `1.8.0`？**
A：`uvx` 缓存还在 0.7.0 / 0.7.1。`uv cache clean fcop fcop-mcp` 然后 `uvx --refresh fcop-mcp` 重启 Cursor。

**Q：第 2 章 `create_custom_team` 报"项目已初始化"？**
A：你忘了 `force=True` 参数。FCoP 默认不允许覆盖；显式 `force=True` 才会归档旧的 + 写新的。

**Q：第 3 章 PM 调 `write_task(sender="PM", ...)` 报"角色锁冲突"？**
A：这个 session 之前已经以别的角色落过文件。让 AI 看 `.fcop/proposals/role-switch-*.md` 里的提示，确认是 ADMIN 主动切换不是 impersonation，然后照样可以继续——0.7.1 的角色锁是软锁，留证据不阻断。

**Q：教程跑完想清掉一切重来？**
A：删掉 `docs/agents/` `workspace/` `.cursor/rules/` `AGENTS.md` `CLAUDE.md` `.fcop/`。或者更简单，删掉整个 `snake-demo/` 重新建一个。

---

## 下一步

- 想用 FCoP 改造**已有项目**？等 [brownfield 教程](README.md)
- 想用 **Cursor + Claude Code** 同仓协作？等 [host-neutral 教程](README.md)
- 想看协议本身？读 [`docs/fcop-standalone.md`](../fcop-standalone.md) 和 [`adr/`](../../adr/)
- 想反馈 bug / 提建议？[GitHub Issues](https://github.com/joinwell52-AI/FCoP/issues)
