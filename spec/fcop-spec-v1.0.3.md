<p align="center">
  <img src="./images/fcop-logo-256.png" alt="FCoP Logo" width="200" />
</p>

# FCoP v1.0.3 正式规范
## File-based Coordination Protocol

> **让 AI 协作像整理文件夹一样简单**
>
> 版本：1.0.3（2026-04-19）
> 简称：**FCoP**
> 口号：Infrastructure-Free · Human-in-the-Loop · IDE-Native
> 维护者：CodeFlow 项目组
> 仓库：https://github.com/joinwell52-AI/codeflow-pwa

---

## 摘要

FCoP 是一套**无数据库、无消息队列、无专用服务器**的多 Agent 协调协议。它将文件系统的原子 `rename` 操作作为唯一同步原语，用文件名编码路由信息，用目录物理位置表达状态机，实现多 Agent 之间的任务分发、状态流转和结果传递。

**两条核心命题（必须同时成立）：**

1. **原子性命题**：文件系统的 `rename` 在同一挂载点内是原子操作。这是 FCoP 避免竞态条件的唯一物理基础，无需任何外部锁机制。
2. **真理性命题**：**文件名（含目录位置）是 FCoP 的唯一真理（Single Source of Truth）。** Frontmatter 中的 `status` 字段仅是冗余元数据，解析器遇到不一致时必须以文件名为准。

---

## 变更记录

| 版本 | 日期 | 核心变更 |
|---|---|---|
| 1.0.3 | 2026-04-19 | ① 新增 §3.4 归档策略（按日期分片防目录膨胀）；② RETRY 明确为规范级保留键；③ 新增 §8.5 Contention Lost 日志规范；④ 路线图新增 fcop-cli 和 FCoP↔MCP 桥 |
| 1.0.2 | 2026-04-19 | ① HASH 升级为幂等键（防任务重复执行）；② 新增 §8.2d 优先级抢占机制；③ 新增 §10.3 DIAG 诊断文件规范；④ CDP 活跃度探测作为僵尸检测第二层；⑤ required_tools 与 Skill Market 关联规范 |
| 1.0.1 | 2026-04-19 | ① 确立"文件名即真理"原则；② 新增僵尸任务检测（PID + 心跳）；③ context_hash 改为 rsync 传输时强制；④ 新增 GATEKEEPER 角色与数字签名；⑤ 新增 inotify 配额与目录分片策略；⑥ Windows `FileExistsError` 处理规范化 |
| 1.0 | 2026-04-18 | 初始版本 |

---

## 目录

1. [设计哲学](#1-设计哲学)
2. [术语定义](#2-术语定义)
3. [工作区结构](#3-工作区结构)
4. [文件命名协议](#4-文件命名协议)
5. [文件内容结构](#5-文件内容结构)
6. [状态机与处理流程](#6-状态机与处理流程)
7. [标准角色体系](#7-标准角色体系)
8. [Patrol Engine 规范](#8-patrol-engine-规范)
9. [互操作性与扩展](#9-互操作性与扩展)
10. [错误处理与自愈](#10-错误处理与自愈)
11. [安全模型](#11-安全模型)
12. [版本兼容性](#12-版本兼容性)
13. [参考实现](#13-参考实现)
14. [附录](#14-附录)

---

## 1. 设计哲学

### 1.1 降维打击

FCoP 用最原始的工具解决最前沿的问题。传统多 Agent 协调需要：Redis（消息队列）+ PostgreSQL（状态存储）+ Docker（隔离）+ 负载均衡 + 鉴权体系。

FCoP 只需要：**一个文件夹**。

### 1.2 三个核心价值

**① 消除基础设施焦虑（Infrastructure-Free）**

| 传统方案 | FCoP 方案 |
|---|---|
| Redis + Postgres + Docker | 普通文件夹 |
| 需要运维工程师 | 任何人都能搭建 |
| 云服务费用 | 零成本 |
| 配置数小时 | 5 分钟启动 |

**② 极致的人类可干预性（Human-in-the-Loop）**

- 老板打开文件夹，看文件名就知道进度
- `PENDING` = 等待接单；`RUNNING` = AI 正在执行；`DONE` = 已完成
- AI 卡住？直接把文件名从 `FAILED` 改回 `PENDING` 强制重试
- 想修改需求？直接编辑 `.fcop` 文件正文，下次 Agent 读取时生效

**③ 成本与安全的完美平衡**

- 零云端费用，所有数据在本地或内网
- 适合涉及敏感业务逻辑的企业场景（车辆数据、财务逻辑、法务文件等）
- 文件系统天然的访问控制（OS 权限体系）

### 1.3 设计约束（不可违反）

```
MUST   仅依赖文件系统的原子 rename 作为同步原语
MUST   文件名包含完整路由信息，无需读取文件内容即可路由
MUST   任何实现都必须支持人类直接读写文件进行干预
MUST   新版本解析器必须能解析旧版本文件（向后兼容）
MUST   文件名/目录位置优先级高于 Frontmatter 元数据（详见 1.4 节）
MUST NOT  使用数据库存储状态
MUST NOT  依赖网络服务作为核心协调机制
MUST NOT  依赖 rename 之后的内容修改作为状态转换的一部分
SHOULD    提供 .fcop 专属后缀以区分协议文件
SHOULD    支持 MCP/A2A 桥接作为可选扩展
```

### 1.4 核心原则：文件名即真理（Filename as Single Source of Truth）

> **这是 FCoP 区别于其他协议的最关键原则。**

#### 为什么这个原则如此重要

考察一个典型崩溃场景：

```
时刻 T1: Agent 执行 os.rename(inbox/xxx-PENDING, active/xxx-RUNNING)
         ↓ 原子成功，文件名已是 RUNNING
时刻 T2: Agent 尝试修改 Frontmatter 中的 status: PENDING → RUNNING
         ↓ 在写入时 OOM 崩溃
时刻 T3: 文件名 = RUNNING，但 Frontmatter 仍是 PENDING ← 不一致！
```

**rename 是原子的，但"rename + 修改内容"不是原子的。** 如果协议允许 Frontmatter 作为状态的权威来源，这个不一致会导致严重后果：

- 重启后 Patrol Engine 扫描，看到 Frontmatter 是 PENDING，误以为任务未认领
- 两个 Agent 可能先后执行同一任务（因为一个看文件名，一个看 Frontmatter）

#### 规范化定义

```
MUST  Patrol Engine 和所有 Agent 以【物理位置 + 文件名】作为状态的唯一权威来源
MUST  Frontmatter 的 status 字段仅用于显示和审计，不用于决策路由
MUST  当文件名 STATUS 与 Frontmatter status 冲突时，以文件名为准
SHOULD  Agent 在 rename 成功后，尝试同步更新 Frontmatter；若失败不阻塞流程
```

#### 工程影响

- **简化 Agent 逻辑**：Agent 认领任务后，不必非得同步更新 Frontmatter 才"合法"
- **天然崩溃恢复**：系统重启后，只需读取目录和文件名即可恢复完整状态
- **审计友好**：Frontmatter 可有滞后，但不影响系统正确性

---

## 2. 术语定义

| 术语 | 定义 |
|---|---|
| **工作区（Workspace）** | 存放所有 FCoP 文件的根目录 |
| **Patrol Engine** | 监控工作区、路由任务、执行自愈的守护进程 |
| **Agent** | 处理特定角色任务的 AI 实例（一个 Cursor session / LLM 调用等）|
| **Task File** | 描述一个待执行任务的 `.fcop` 文件 |
| **认领（Claim）** | Agent 将 `PENDING` 文件原子重命名为 `RUNNING` 的操作 |
| **流水线（Pipeline）** | 一系列 Task File 按角色顺序传递，形成完整业务链路 |
| **thread_key** | 同一业务流水线的所有文件共享的唯一标识符 |

---

## 3. 工作区结构

### 3.1 标准目录布局

```
fcop-workspace/
│
├── inbox/              ← [PENDING] 新任务在此等待认领
│   └── TASK-20260419-120000-001-PM-to-DEV-PENDING.fcop
│
├── active/             ← [RUNNING] 已认领、执行中的任务
│   └── TASK-20260419-120000-001-PM-to-DEV-RUNNING.fcop
│
├── done/               ← [DONE] 成功完成的任务（可选归档）
│   └── RESULT-20260419-123000-002-DEV-to-QA-DONE.fcop
│
├── failed/             ← [FAILED] 失败的任务（便于人工排查）
│   └── TASK-20260419-115000-000-PM-to-DEV-FAILED.fcop
│
├── archive/            ← 长期归档（定期从 done/ failed/ 移入）
│
├── events/             ← 系统广播事件（EVENT 类型文件）
│   └── EVENT-20260419-120500-001-SYSTEM-broadcast-ALL-INFO.fcop
│
├── fcop-logs/          ← Patrol Engine 操作日志
│   └── patrol-20260419.log
│
└── fcop-config.yaml    ← 工作区配置文件
```

### 3.2 目录与状态的对应关系

| 目录 | 对应 STATUS | 说明 |
|---|---|---|
| `inbox/` | `PENDING` | 等待 Agent 认领 |
| `active/` | `RUNNING` | Agent 正在执行，禁止他人修改 |
| `done/` | `DONE` | 正常完成，等待归档 |
| `failed/` | `FAILED` | 失败，等待人工处理或自动重试 |
| `archive/` | 所有终态 | 长期存储，保留完整历史 |
| `events/` | `INFO`/`WARN`/`ERROR` | 系统事件，不进入状态机流程 |

### 3.3 fcop-config.yaml 完整规范

```yaml
# FCoP 工作区配置文件
# 版本：1.0

protocol_version: "1.0"
workspace_name: "my-project"          # 工作区名称，用于多工作区区分

# 团队配置
team:
  name: "dev-team"                    # 团队模板名称
  roles:                              # 注册的角色列表（自定义角色在此声明）
    - PM
    - DEV
    - QA
    - OPS

# 文件配置
files:
  extension: ".fcop"                  # 专属后缀（也可用 .md）
  encoding: "utf-8"
  max_size_kb: 512                    # 单文件最大 512KB，超出用文件引用

# Patrol Engine 配置
patrol:
  mode: "watch"                       # watch（inotify）或 poll（轮询）
  poll_interval_s: 5                  # 轮询间隔（mode=poll 时生效）
  task_timeout_min: 10                # RUNNING 超过此时间视为超时
  max_retries: 3                      # 最大重试次数
  auto_archive_after_days: 7          # DONE/FAILED 多少天后自动归档
  archive_shard_by: "day"             # 归档分片策略：none / day / hour
  active_shard_threshold: 1000        # active/inbox 超过此数量启用分片

# 扩展（可选）
extensions:
  mcp_enabled: false                  # 是否启用 MCP 桥接
  mcp_port: 8765
  a2a_rsync_enabled: false            # 是否启用跨机 rsync 同步
  a2a_rsync_targets: []               # rsync 目标列表
  webhook_enabled: false              # 是否在状态变更时触发 Webhook
  webhook_url: ""

# 日志
logging:
  level: "INFO"                       # DEBUG / INFO / WARN / ERROR
  retention_days: 30
  contention_log: true                # 记录 Contention Lost 事件
```

### 3.4 归档策略（Archiving Strategy）

> **问题场景：** 大规模自动化流水线每天可能产生数千任务文件。`done/` 和 `failed/` 在数周内就会累积到数万个文件，触发文件系统单目录索引性能瓶颈（ext4 hashed directory 约 10K 文件后退化，NTFS 单目录 >50K 时 `FindFirstFile` 显著变慢）。

#### 规范要求

```
MUST    Patrol Engine 必须支持定时归档任务
MUST    归档窗口由 auto_archive_after_days 控制（默认 7 天）
MUST    归档时将文件移入 archive/{YYYY-MM-DD}/ 子目录，按文件原创建日期分片
SHOULD  当 archive/ 某一天文件数超过 10000 时，启用二级分片 archive/{YYYY-MM-DD}/{HH}/
MUST NOT 归档操作中修改文件名的核心字段（仅物理位置变更）
SHOULD  归档前生成当日索引文件 archive/{YYYY-MM-DD}/INDEX.json，加速后续检索
```

#### 目录分片布局

```
archive/
├── 2026-04-12/
│   ├── INDEX.json              # 当日任务元数据索引（Patrol 生成）
│   ├── TASK-20260412-...-DONE.fcop
│   └── ...（当日 <10K 个文件）
├── 2026-04-13/
│   ├── 08/                     # 高吞吐日自动启用二级分片
│   │   └── ...
│   ├── 09/
│   └── INDEX.json
└── 2026-04-19/
    └── ...
```

#### 参考实现

```python
def archive_sweep(workspace: Path, cutoff_days: int = 7):
    """归档超过 cutoff_days 的 DONE/FAILED 文件"""
    cutoff = time.time() - cutoff_days * 86400
    for src_dir in ["done", "failed"]:
        for f in (workspace / src_dir).glob("*.fcop"):
            if f.stat().st_mtime > cutoff:
                continue
            created = datetime.fromtimestamp(f.stat().st_mtime)
            shard = workspace / "archive" / created.strftime("%Y-%m-%d")
            if shard.exists() and len(list(shard.glob("*.fcop"))) > 10000:
                shard = shard / created.strftime("%H")
            shard.mkdir(parents=True, exist_ok=True)
            os.rename(f, shard / f.name)


def rebuild_index(day_dir: Path):
    """为归档子目录生成元数据索引"""
    index = []
    for f in day_dir.rglob("*.fcop"):
        meta = parse_filename(f.name)
        index.append({
            "filename": str(f.relative_to(day_dir)),
            "task_id": meta["task_id"],
            "sender": meta["sender"],
            "recipient": meta["recipient"],
            "status": meta["status"],
            "thread_key": meta.get("thread_key"),
        })
    (day_dir / "INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
```

#### 人类检索路径

```
# 按日期定位
ls archive/2026-04-18/

# 按 thread_key 跨天检索
grep -l "thread_key:ORDER20260418" archive/**/INDEX.json

# 全文检索（归档后仍可用）
rg "VIN码错误" archive/2026-04-18/
```

---

## 4. 文件命名协议

> 文件名是协议的**路由层**和**状态层**。Patrol Engine 无需读取文件内容即可完成路由和状态判断。

### 4.1 格式规范（强制）

```
[TYPE]-[DATE]-[TIME]-[SEQ]-[SENDER]-[DIR]-[RECIPIENT]-[STATUS][EXTRA].[EXT]
```

**字段分隔符：单连字符 `-`（严格）**
**字段内容：禁止包含连字符 `-`，复合词用下划线 `_` 或驼峰**

### 4.2 字段完整定义

| 字段 | 必填 | 格式 | 约束 | 示例 |
|---|---|---|---|---|
| `TYPE` | ✅ | 枚举 | 见 4.3 节 | `TASK` |
| `DATE` | ✅ | `YYYYMMDD` | UTC 或项目内统一时区 | `20260419` |
| `TIME` | ✅ | `HHMMSS` | 24小时制 | `143000` |
| `SEQ` | ✅ | `\d{3,6}` | 全局递增，同秒内防重 | `001` |
| `SENDER` | ✅ | `[A-Z][A-Z0-9_]{0,19}` | 最长 20 字符，无连字符 | `PM` |
| `DIR` | ✅ | `to` / `broadcast` | 小写固定值 | `to` |
| `RECIPIENT` | ✅ | 同 SENDER，或 `ALL` | `ALL` 仅用于 broadcast | `DEV` |
| `STATUS` | ✅ | 枚举 | 见 4.4 节 | `PENDING` |
| `EXTRA` | ❌ | `-KEY=VALUE` 链 | 每段 `-KEY=VALUE`，Key 全大写 | `-PRIO=HIGH` |
| `EXT` | ✅ | `.fcop` / `.md` | 推荐 `.fcop` | `.fcop` |

**完整文件名长度限制：< 200 字符（兼容各操作系统文件名限制）**

### 4.3 TYPE 枚举

| TYPE | 含义 | 方向 | 生成者 |
|---|---|---|---|
| `TASK` | 任务指令 | SENDER → RECIPIENT | 任意 Agent / USER |
| `RESULT` | 执行结果 | Agent → 下一环节 | 执行 Agent |
| `EVENT` | 系统事件/通知 | SYSTEM → ALL | Patrol Engine / SYSTEM |

### 4.4 STATUS 枚举与目录对应

| STATUS | 含义 | 所在目录 | 可转换为 |
|---|---|---|---|
| `PENDING` | 等待认领 | `inbox/` | `RUNNING`（Agent 认领）|
| `RUNNING` | 执行中 | `active/` | `DONE` / `FAILED` / `REVIEW` |
| `DONE` | 正常完成 | `done/` | `ARCHIVE`（定期归档）|
| `FAILED` | 执行失败 | `failed/` | `PENDING`（人工重试）/ `ARCHIVE` |
| `REVIEW` | 等待人工审核 | `active/` | `PENDING`（退回）/ `DONE`（通过）|
| `INFO` | 信息广播 | `events/` | —（只追加，不转换）|
| `WARN` | 警告广播 | `events/` | —（只追加，不转换）|
| `ERROR` | 错误广播 | `events/` | —（只追加，不转换）|

### 4.5 EXTRA 扩展字段规范

| Key | 值格式 | 含义 | 示例 |
|---|---|---|---|
| `PRIO` | `HIGH` / `MEDIUM` / `LOW` | 优先级 | `-PRIO=HIGH` |
| `EXP` | `YYYYMMDD` | 过期日期 | `-EXP=20260420` |
| `PARENT` | `{DATE}{TIME}{SEQ}` | 父任务 ID（无连字符）| `-PARENT=202604191430001` |
| `THREAD` | 字母数字串 | 流水线 thread_key | `-THREAD=ORDER20260419` |
| `RETRY` | 数字 | 当前重试次数 | `-RETRY=2` |
| `HASH` | 前12位 sha256 | 内容哈希 + 幂等键（防重复处理）| `-HASH=a1b2c3d4e5f6` |
| `FORCE` | `1` | 强制重跑，跳过 HASH 去重 | `-FORCE=1` |
| `REASON` | 大写短语 | 状态流转原因 | `-REASON=DEDUP` / `-REASON=MAXRETRY` / `-REASON=COMPLIANCE` |
| `SIGNED_BY` | 角色名 | 签名者（REVIEW 批准）| `-SIGNED_BY=GATEKEEPER` |
| `PREEMPTED_BY` | 任务 ID | 被抢占时指向新任务 | `-PREEMPTED_BY=202604191450005` |

> **规范级保留键（Reserved Keys）**
>
> 以下 EXTRA 键为 FCoP 规范**强制保留**，任何实现**不得重新定义语义**：
> `PRIO`、`HASH`、`RETRY`、`REASON`、`SIGNED_BY`、`PREEMPTED_BY`、`FORCE`、`THREAD`、`EXP`、`PARENT`
>
> 其中 **`RETRY=N` 是规范级重试计数器**：Patrol Engine 在执行 §8.2 自动重试流程时，**必须**使用该键，不得用自定义字段（如 `_retry`、`attempt`）替代。这保证了不同实现之间的任务文件可以无损迁移。
>
> 自定义键必须使用 `X_` 前缀（例如 `-X_CUSTOMER=ABC123`）以避免未来与规范键冲突。

### 4.6 合法文件名示例

```
# 基础：PM 给 DEV 的任务
TASK-20260419-143000-001-PM-to-DEV-PENDING.fcop

# DEV 认领后（Patrol Engine 原子重命名 + 移目录）
TASK-20260419-143000-001-PM-to-DEV-RUNNING.fcop

# DEV 完成，结果给 QA
RESULT-20260419-153000-002-DEV-to-QA-DONE.fcop

# QA 测试失败，打回 DEV
RESULT-20260419-163000-003-QA-to-DEV-FAILED.fcop

# 高优先级广播任务（带 thread_key）
TASK-20260419-143000-004-PM-to-ALL-PENDING-PRIO=HIGH-THREAD=SPRINT42.fcop

# 系统超时警告广播
EVENT-20260419-160000-005-SYSTEM-broadcast-ALL-WARN.fcop

# 带重试标记的任务
TASK-20260419-143000-001-PM-to-DEV-PENDING-RETRY=2.fcop
```

### 4.7 文件名解析正则（权威版）

```python
import re

FCOP_RE = re.compile(
    r'^(?P<type>TASK|RESULT|EVENT)'
    r'-(?P<date>\d{8})'
    r'-(?P<time>\d{6})'
    r'-(?P<seq>\d{3,6})'
    r'-(?P<sender>[A-Z][A-Z0-9_]{0,19})'
    r'-(?P<dir>to|broadcast)'
    r'-(?P<recipient>[A-Z][A-Z0-9_]{0,19})'
    r'-(?P<status>PENDING|RUNNING|DONE|FAILED|REVIEW|INFO|WARN|ERROR)'
    r'(?P<extra>(?:-[A-Z]+=\S+)*)'
    r'\.(?P<ext>fcop|md)$'
)

def parse(name: str) -> dict | None:
    m = FCOP_RE.match(name)
    if not m:
        return None
    d = m.groupdict()
    # 解析 EXTRA 键值对
    d['extra_kv'] = {}
    for part in d['extra'].split('-'):
        if '=' in part:
            k, v = part.split('=', 1)
            d['extra_kv'][k] = v
    return d
```

---

## 5. 文件内容结构

### 5.1 整体结构

```
┌──────────────────────┐
│   YAML Frontmatter   │  ← 机器可读，Patrol Engine 解析
│   (--- 开头 ---)      │
├──────────────────────┤
│   Markdown 正文      │  ← 人类可读，Agent 执行依据
│                      │
│   ## 任务描述         │
│   ### 具体要求        │
│   ### 预期输出        │
│   ### 参考资料        │
└──────────────────────┘
```

### 5.2 Frontmatter 字段规范

```yaml
---
# ── 必填字段 ──────────────────────────────────────────
protocol_version: "1.0"              # FCoP 版本号，固定值
task_id: "20260419-143000-001"       # 唯一 ID（DATE-TIME-SEQ，无连字符）
type: "TASK"                         # TASK / RESULT / EVENT
sender: "PM"
recipient: "DEV"
status: "PENDING"                    # 当前状态（与文件名一致）
created_at: "2026-04-19T14:30:00Z"  # ISO 8601，UTC

# ── 推荐字段 ──────────────────────────────────────────
priority: "HIGH"                     # HIGH / MEDIUM / LOW（默认 MEDIUM）
thread_key: "ORDER20260419"          # 同一流水线的所有文件共享此值

# ── 可选字段 ──────────────────────────────────────────
parent_task: "20260419-140000-000"   # 父任务 ID
expires_at: "2026-04-20T00:00:00Z"  # 过期时间，Patrol Engine 会清理
context_hash: "sha256:a1b2c3d4e5f6" # 正文内容 sha256 前12位，防篡改
required_tools:                      # Agent 执行所需工具声明
  - cursor_edit
  - terminal
retry_count: 0                       # 当前重试次数（Patrol Engine 维护）
error_reason: ""                     # 失败原因（STATUS=FAILED 时必填）
---
```

### 5.3 Markdown 正文模板

```markdown
## 任务描述

清晰描述本次任务的**目标**和**背景**，使用自然语言。

### 具体要求

- [ ] 要求 1（可量化，有明确的验收标准）
- [ ] 要求 2
- [ ] 要求 3

### 预期输出格式

下一个接收方（RECIPIENT）期望收到的数据结构：

```json
{
  "status": "success",
  "files_modified": ["src/api/auth.py"],
  "test_passed": true,
  "notes": "简短说明，供人类阅读"
}
```

### 参考资料

- [相关文档](../docs/xxx.md)
- [相关代码](../src/xxx.py)
- [上一个任务结果](../done/RESULT-xxx-DONE.fcop)
```

### 5.4 正文规范（强制）

```
MUST     每个文件只描述一个任务，禁止合并多个任务
MUST     明确"预期输出格式"，便于下一个 Agent 无歧义解析
MUST     Frontmatter 的 status 字段与文件名 STATUS 保持一致
SHOULD   大上下文用文件引用（相对路径），不直接内联
SHOULD   验收标准用 - [ ] checkbox，Agent 完成后打 - [x]
MUST NOT 文件大小超过 fcop-config.yaml 中 files.max_size_kb 限制
```

---

## 6. 状态机与处理流程

### 6.1 完整状态机

```
                   ┌──────────────────┐
    SENDER 创建 ──>│    PENDING        │ inbox/
                   └────────┬─────────┘
                            │ Agent 原子 rename（成功者获执行权）
                   ┌────────▼─────────┐
                   │    RUNNING        │ active/
                   └────────┬─────────┘
              ┌─────────────┼──────────────┐
              │             │              │
     ┌────────▼───┐  ┌──────▼─────┐  ┌───▼──────┐
     │    DONE    │  │   FAILED   │  │  REVIEW  │
     │   done/    │  │  failed/   │  │  active/ │
     └─────┬──────┘  └──────┬─────┘  └────┬─────┘
           │                │              │
           │         ┌──────▼─────┐   人工处理
           │         │  重试?      │        │
           │         │ retry < max │──────> PENDING
           │         │ retry ≥ max │──────> archive/FAILED-MAXRETRY
           │         └────────────┘
           │
     ┌─────▼──────┐
     │  ARCHIVE   │ archive/（定期移入）
     └────────────┘
```

### 6.2 处理流程（逐步规范）

**步骤 ① — 创建任务**

```python
# SENDER 生成任务文件（原子写入）
import os, hashlib
from datetime import datetime, timezone
from pathlib import Path

def create_task(workspace, sender, recipient, body, priority="MEDIUM", thread_key=None):
    ts = datetime.now(timezone.utc)
    date = ts.strftime("%Y%m%d")
    time_ = ts.strftime("%H%M%S")
    seq = next_seq()  # 全局递增序号
    task_id = f"{date}-{time_}-{seq:03d}"

    frontmatter = f"""---
protocol_version: "1.0"
task_id: "{task_id}"
type: "TASK"
sender: "{sender}"
recipient: "{recipient}"
status: "PENDING"
created_at: "{ts.isoformat()}"
priority: "{priority}"
{"thread_key: \"" + thread_key + "\"" if thread_key else ""}
retry_count: 0
---
"""
    content = frontmatter + body
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

    filename = f"TASK-{date}-{time_}-{seq:03d}-{sender}-to-{recipient}-PENDING.fcop"
    tmp = Path(workspace) / "inbox" / (filename + ".tmp")
    target = Path(workspace) / "inbox" / filename

    tmp.write_text(content, encoding="utf-8")
    os.rename(tmp, target)   # 原子写入
    return task_id, filename
```

**步骤 ② — Patrol Engine 发现**

```python
# 扫描 inbox/，找到匹配 my_role 的 PENDING 文件
def scan_inbox(workspace, my_role):
    inbox = Path(workspace) / "inbox"
    candidates = []
    for f in inbox.glob("*.fcop"):
        meta = parse(f.name)
        if not meta:
            continue
        if meta["status"] != "PENDING":
            continue
        if meta["recipient"] in (my_role, "ALL"):
            candidates.append((f, meta))
    # 按时间戳 + SEQ 排序，优先处理最早的任务
    candidates.sort(key=lambda x: (x[1]["date"], x[1]["time"], x[1]["seq"]))
    return candidates
```

**步骤 ③ — Agent 认领（原子操作）**

```python
# 原子 rename：PENDING(inbox) → RUNNING(active)
# rename 失败 = 已被其他 Agent 抢占，静默跳过
def claim(workspace, pending_path, meta):
    running_name = pending_path.name.replace("-PENDING.", "-RUNNING.")
    target = Path(workspace) / "active" / running_name
    try:
        os.rename(pending_path, target)
        # 成功：更新 Frontmatter 中的 status 字段
        update_frontmatter_status(target, "RUNNING")
        return target
    except (FileNotFoundError, FileExistsError):
        return None   # 已被抢占
```

**步骤 ④ — 执行任务**

Agent 读取 `active/` 中的 `.fcop` 文件，按正文指令执行，执行过程中**不修改文件名**。

**步骤 ⑤ — 完成（生成 RESULT）**

```python
def complete_task(workspace, running_path, meta, result_body, next_recipient):
    # 生成 RESULT 文件给下一个环节
    create_task(workspace, sender=meta["sender"], recipient=next_recipient,
                body=result_body, thread_key=meta.get("extra_kv", {}).get("THREAD"))

    # 原 TASK 文件改名为 DONE，移入 done/
    done_name = running_path.name.replace("-RUNNING.", "-DONE.")
    done_path = Path(workspace) / "done" / done_name
    update_frontmatter_status(running_path, "DONE")
    os.rename(running_path, done_path)
```

**步骤 ⑥ — 失败（写入 error_reason）**

```python
def fail_task(workspace, running_path, meta, error_reason):
    failed_name = running_path.name.replace("-RUNNING.", "-FAILED.")
    failed_path = Path(workspace) / "failed" / failed_name
    update_frontmatter_field(running_path, "error_reason", error_reason)
    update_frontmatter_field(running_path, "status", "FAILED")
    os.rename(running_path, failed_path)
```

---

## 7. 标准角色体系

### 7.1 系统保留角色

| 角色 | 说明 | 可创建文件 |
|---|---|---|
| `SYSTEM` | Patrol Engine，系统事件 | EVENT 类型 |
| `USER` | 人类用户，最高优先级 | TASK 类型 |

### 7.2 dev-team（开发团队）

```
USER → PM → DEV → QA → OPS → PM（回执）
```

| 角色 | 职责 | 接收来源 | 输出去向 |
|---|---|---|---|
| `PM` | 任务拆解，优先级管理 | USER, QA(FAILED), OPS | DEV, QA, OPS |
| `DEV` | 编码，架构实现 | PM, QA(FAILED) | QA |
| `QA` | 测试，结果审计 | DEV | OPS(通过), DEV(失败) |
| `OPS` | 部署，监控 | QA | PM(回执) |

### 7.3 media-team（媒体团队）

```
PM → RESEARCHER → WRITER → EDITOR → PUBLISHER → PM（回执）
```

### 7.4 mvp-team（MVP 团队）

```
USER → BUILDER → DESIGNER → MARKETER → USER（回执）
```

### 7.5 自定义角色规范

在 `fcop-config.yaml` 的 `team.roles` 中声明：

```yaml
team:
  roles:
    - PM
    - DEV
    - QA
    - OPS
    - LEGAL        # 自定义：法务
    - FINANCE      # 自定义：财务
    - SAIGE_DEV    # 自定义：赛格专项开发（下划线分隔）
```

**角色命名规范：**
- 只使用大写字母、数字、下划线
- 最长 20 字符
- 禁止使用连字符（`-`）
- 禁止使用保留名：`SYSTEM`、`USER`、`ALL`

---

## 8. Patrol Engine 规范

### 8.1 功能要求

```
必须实现（MUST）：
  ✅ 文件系统监听（watchdog inotify 或定时轮询）
  ✅ 文件名解析（FCOP_RE 正则，见 4.7 节）
  ✅ 任务路由（根据 RECIPIENT 找到对应 Agent）
  ✅ 原子认领（rename PENDING→RUNNING + 移目录）
  ✅ 完成处理（RUNNING→DONE/FAILED + 移目录）
  ✅ 超时检测（RUNNING 超过 task_timeout_min → FAILED）
  ✅ 自动重试（retry_count < max_retries → 重置 PENDING）
  ✅ 操作日志（写入 fcop-logs/）
  ✅ 过期清理（expires_at 过期的 PENDING 文件 → FAILED）

推荐实现（SHOULD）：
  ⚡ 优先级队列（PRIO=HIGH 的任务优先分发）
  ⚡ thread_key 追踪（同一流水线的任务关联展示）
  ⚡ MCP 桥接接口（见第 9 节）
  ⚡ Webhook 通知（状态变更时触发）
```

### 8.2 超时与重试逻辑

```python
def check_timeouts(workspace, config):
    timeout_min = config["patrol"]["task_timeout_min"]
    max_retries = config["patrol"]["max_retries"]
    now = time.time()

    for f in Path(workspace, "active").glob("*-RUNNING.fcop"):
        mtime = f.stat().st_mtime
        if (now - mtime) / 60 < timeout_min:
            continue

        meta = read_frontmatter(f)
        retry_count = int(meta.get("retry_count", 0))

        if retry_count < max_retries:
            # 重置为 PENDING，放回 inbox/，递增重试次数
            pending_name = f.name.replace("-RUNNING.", "-PENDING.")
            # 追加重试标记到文件名
            pending_name = pending_name.replace(".fcop", f"-RETRY={retry_count+1}.fcop")
            target = Path(workspace, "inbox", pending_name)
            update_frontmatter_field(f, "retry_count", retry_count + 1)
            update_frontmatter_field(f, "status", "PENDING")
            os.rename(f, target)
            emit_event(workspace, "WARN", f"Task timeout, retry {retry_count+1}/{max_retries}: {f.name}")
        else:
            # 超过最大重试次数，标记 FAILED-MAXRETRY
            failed_name = f.name.replace("-RUNNING.", "-FAILED.")
            target = Path(workspace, "failed", failed_name)
            update_frontmatter_field(f, "error_reason", f"MAXRETRY: exceeded {max_retries} retries")
            update_frontmatter_field(f, "status", "FAILED")
            os.rename(f, target)
            emit_event(workspace, "ERROR", f"Task MAXRETRY: {f.name}")
```

### 8.2a 僵尸任务检测（Zombie Task Detection）

> **问题场景：** Agent 通过 `rename` 成功认领任务（文件进入 `active/*-RUNNING.fcop`），但进程随即崩溃（OOM、段错误、机器重启）。此时文件会停留在 RUNNING 状态直到超时，但超时时间通常较长（30 分钟），严重拖慢吞吐。

#### 规范要求

```
MUST   Agent 认领任务后，必须在 Frontmatter 写入 owner_pid 和 owner_host
MUST   Agent 在运行期间，每 heartbeat_interval_sec 更新一次文件 mtime（touch）
SHOULD 心跳间隔建议 30 秒；默认僵尸判定阈值 = 3 × heartbeat_interval_sec
MUST   Patrol Engine 扫描 RUNNING 文件时，必须执行僵尸检测
```

#### 参考实现

```python
import os, time, psutil, socket
from pathlib import Path

HEARTBEAT_SEC = 30
ZOMBIE_THRESHOLD_SEC = 90  # 3 × HEARTBEAT_SEC

def detect_zombie(f: Path) -> bool:
    """返回 True 表示该 RUNNING 文件是僵尸任务"""
    meta = read_frontmatter(f)
    owner_pid = meta.get("owner_pid")
    owner_host = meta.get("owner_host")

    if owner_host and owner_host != socket.gethostname():
        return False

    if owner_pid:
        try:
            proc = psutil.Process(int(owner_pid))
            if proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                return False
        except (psutil.NoSuchProcess, ValueError):
            pass

    mtime_age = time.time() - f.stat().st_mtime
    return mtime_age > ZOMBIE_THRESHOLD_SEC


def revive_zombie(f: Path, workspace: Path):
    """把僵尸任务放回 inbox/ 重置为 PENDING，并打 ZOMBIE 标记"""
    pending_name = f.name.replace("-RUNNING.", "-PENDING.")
    pending_name = pending_name.replace(".fcop", "-ZOMBIE_REVIVED.fcop")
    target = workspace / "inbox" / pending_name
    os.rename(f, target)
    emit_event(workspace, "WARN", f"Zombie task revived: {f.name}")


def heartbeat_loop(claimed_file: Path, stop_flag):
    """Agent 侧：运行期间每 30 秒 touch 一次文件"""
    while not stop_flag.is_set():
        try:
            os.utime(claimed_file, None)
        except FileNotFoundError:
            break
        time.sleep(HEARTBEAT_SEC)
```

#### 第二层检测：对话活跃度（IDE-specific，可选）

> PID 心跳只能证明"Agent 进程还在"，但不能证明"Agent 正在有效工作"。当 Agent 进程卡在网络请求或陷入无限思考循环时，进程看起来是活的，实际任务已经死了。

```
OPTIONAL  针对 Cursor/VSCode 类 IDE-Agent，Patrol Engine 可通过 IDE 的调试协议
          （Cursor 使用 CDP，端口 5253）探测 Agent 对话面板的最新消息时间戳
MUST      若实现此层，必须在 fcop-config.yaml 中声明：
            liveness_probe:
              type: "cdp"            # cdp / lsp / none
              port: 5253
              silence_threshold_sec: 120
SHOULD    检测到对话流静默超过 silence_threshold_sec 时，先尝试 Nudge（发送空 @ 回车催促），
          若再静默一个周期则判定为僵尸并 revive
```

参考实现见 CodeFlow Desktop `nudger.py` 的 `_probe_conversation_activity()` 函数。这是规范的**可选扩展层**，非 IDE 场景（纯脚本 Agent）不需要实现。

#### Agent 认领流程（完整版）

```python
def claim_task(pending: Path, workspace: Path) -> Path | None:
    """原子认领 + 心跳初始化"""
    running_name = pending.name.replace("-PENDING.", "-RUNNING.")
    target = workspace / "active" / running_name
    try:
        os.rename(pending, target)
    except (FileExistsError, FileNotFoundError):
        # Windows FileExistsError / Linux race-loss 都视为认领失败
        return None
    update_frontmatter_field(target, "owner_pid", os.getpid())
    update_frontmatter_field(target, "owner_host", socket.gethostname())
    update_frontmatter_field(target, "claimed_at", utc_now_iso())
    return target
```

> **注意：** Windows 平台上 `os.rename` 在目标已存在时抛 `FileExistsError`，Linux 上则是覆盖。跨平台实现必须捕获 `FileExistsError` + `FileNotFoundError` 两种情况均视为"认领失败"。

### 8.2b 轮询 vs 事件驱动性能策略

#### 规范要求

```
SHOULD  active/ 目录文件数 < 1000 时，使用 watchdog/inotify
SHOULD  active/ 目录文件数 ≥ 1000 时，改用定时轮询（默认 5s）+ 内存索引
MUST    Linux 平台实现必须检查 /proc/sys/fs/inotify/max_user_watches
MUST    inotify 监听数超过配额的 50% 时，必须降级到轮询
```

#### 目录分片（高吞吐场景）

当 `inbox/` 单目录文件数超过 1000 时，强制启用二级分片：

```
inbox/
├── 20260419/
│   ├── 14/                    ← 按小时分片
│   │   ├── TASK-...-PENDING.fcop
│   │   └── ...
│   └── 15/
└── 20260420/
    └── 09/
```

Patrol Engine 必须能自适应识别分片模式（通过 `fcop-config.yaml` 的 `shard_by: hour|day|none` 字段）。

#### 内存索引

Patrol Engine 启动时全量扫描一次，随后仅响应 `IN_MOVED_TO` / `IN_CREATE` 事件增量更新内存索引。索引结构：

```python
{
  "pending": { "TASK-20260419-143000-001-PM-to-DEV": PosixPath(...) },
  "running": { "TASK-20260419-140000-002-PM-to-DEV": PosixPath(...) },
}
```

### 8.2c GATEKEEPER 角色与数字签名（可选）

> **适用场景：** 车辆档案、财务审批、合规流程等需要跨部门签署的场景。

#### 规范要求

```
OPTIONAL  引入 GATEKEEPER 角色，专门处理 REVIEW 状态
MUST      GATEKEEPER 在批准任务时，必须对 Frontmatter + 正文计算 SHA256
MUST      签名结果写入文件名 EXTRA 字段：SIGNED_BY=GATEKEEPER
SHOULD    生产环境可升级为 GPG 签名（v1.2 规划）
```

#### 流程示例

```
DEV 完成 → RESULT-...-DEV-to-GATEKEEPER-REVIEW.fcop   （待审）
GATEKEEPER 批准 → RESULT-...-GATEKEEPER-to-OPS-DONE-SIGNED_BY=GATEKEEPER-HASH=abc123.fcop
GATEKEEPER 驳回 → RESULT-...-GATEKEEPER-to-DEV-FAILED-REASON=COMPLIANCE.fcop
```

### 8.2d 优先级抢占（Preemption）

> **问题场景：** DEV Agent 正在执行 `PRIO=LOW` 的重构任务，此时 PM 下发 `PRIO=HIGH` 的生产事故修复任务。如果没有抢占机制，HIGH 任务必须排队，紧急响应能力完全丧失。

#### 规范要求

```
SHOULD   Patrol Engine 应支持优先级抢占
MUST     仅允许 PRIO=HIGH 抢占 PRIO=LOW（不允许抢占同级或更高级）
MUST     抢占必须"礼貌"：先写入 PREEMPT 信号文件，给 Agent 最多 30s 自行暂存
MUST     被抢占的任务，其 RUNNING 文件必须 rename 回 inbox/ 并标记 PREEMPTED_BY=<新任务 ID>
MUST NOT 抢占已在 REVIEW 或带 SIGNED_BY 标记的任务（合规性任务不得中断）
```

#### 参考实现

```python
def preempt_if_needed(workspace: Path, new_high_task: dict):
    """新来的 HIGH 任务触发时调用"""
    recipient = new_high_task["recipient"]

    for running in (workspace / "active").glob(f"*-to-{recipient}-RUNNING.fcop"):
        meta = read_frontmatter(running)
        if meta.get("priority", "MEDIUM").upper() != "LOW":
            continue
        if "SIGNED_BY" in running.name or meta.get("status") == "REVIEW":
            continue

        signal = workspace / "active" / f"PREEMPT-{running.stem}.signal"
        signal.write_text(f"preempted_by={new_high_task['task_id']}\n", encoding="utf-8")

        deadline = time.time() + 30
        while time.time() < deadline and signal.exists():
            time.sleep(1)

        if signal.exists():
            signal.unlink()

        preempted_name = running.name.replace(
            "-RUNNING.",
            f"-PENDING-PREEMPTED_BY={new_high_task['task_id']}.",
        )
        target = workspace / "inbox" / preempted_name
        update_frontmatter_field(running, "retry_count",
                                 int(meta.get("retry_count", 0)) + 1)
        os.rename(running, target)
        emit_event(workspace, "WARN", f"Preempted {running.name} by HIGH task")
        break
```

#### Agent 侧协作契约

```
MUST   Agent 在执行期间每 heartbeat_interval_sec 检查 active/PREEMPT-<self>.signal
MUST   检测到信号后，必须在 30s 内保存当前进度到 Frontmatter 的 checkpoint 字段，
       然后删除信号文件表示"已同意让路"
SHOULD 被抢占任务重新调度时，Agent 应从 checkpoint 恢复，而非从零开始
```

### 8.3 EVENT 广播规范

```python
def emit_event(workspace, level, message, thread_key=None):
    """发送系统广播事件"""
    ts = datetime.now(timezone.utc)
    filename = (
        f"EVENT-{ts.strftime('%Y%m%d')}-{ts.strftime('%H%M%S')}"
        f"-{next_seq():03d}-SYSTEM-broadcast-ALL-{level}.fcop"
    )
    content = f"""---
protocol_version: "1.0"
task_id: "{ts.strftime('%Y%m%d-%H%M%S')}-{next_seq():03d}"
type: "EVENT"
sender: "SYSTEM"
recipient: "ALL"
status: "{level}"
created_at: "{ts.isoformat()}"
{"thread_key: \"" + thread_key + "\"" if thread_key else ""}
---

## 系统事件

{message}
"""
    path = Path(workspace) / "events" / filename
    path.write_text(content, encoding="utf-8")
```

### 8.4 操作日志（fcop-logs/）规范

```
MUST   Patrol Engine 必须把所有状态转换操作写入 fcop-logs/YYYY-MM-DD.log
MUST   每条日志至少包含：时间戳 / 操作类型 / 源文件名 / 目标文件名 / 执行者
SHOULD 日志使用 JSONL 格式，便于机器解析与增量同步
```

日志条目示例：

```jsonl
{"ts":"2026-04-19T14:30:00Z","op":"CLAIM","src":"TASK-...-PENDING.fcop","dst":"TASK-...-RUNNING.fcop","by":"DEV","pid":12345}
{"ts":"2026-04-19T14:30:00Z","op":"CONTENTION_LOST","src":"TASK-...-PENDING.fcop","by":"DEV2","pid":12346}
{"ts":"2026-04-19T14:35:22Z","op":"COMPLETE","src":"...-RUNNING.fcop","dst":"...-DONE.fcop","by":"DEV","pid":12345}
```

### 8.5 争抢失败日志（Contention Lost）

> **问题场景：** 多 Agent 并行场景下（例如两个 DEV 实例同时监听 `inbox/`），必然会出现"两个 Agent 同时看到同一个 PENDING 文件，一个认领成功，另一个 rename 失败"的情况。**这不是 bug，是 FCoP 并发模型的预期行为**。但如果不记录，事后无法诊断吞吐瓶颈和负载分布。

#### 规范要求

```
MUST    任何 Agent 或 Patrol Engine 在原子认领失败（rename 抛出 FileExistsError 
        或 FileNotFoundError）时，必须在 fcop-logs/ 写入一条 CONTENTION_LOST 日志
MUST    记录字段：时间戳、争抢的文件名、当前 Agent ID、当前 PID
SHOULD  争抢失败不应触发重试或告警；这是正常并发事件
SHOULD  生产环境每 10000 次 CLAIM 操作的 CONTENTION_LOST 比率应 < 5%，
        超过则提示调度粒度过粗，应增加分片或调度随机延迟
```

#### 参考实现

```python
def safe_atomic_claim(src: Path, dst: Path, logger, agent_id: str) -> bool:
    """原子认领，失败时静默记录争抢事件"""
    try:
        os.rename(src, dst)
        logger.log("CLAIM", src=src.name, dst=dst.name, by=agent_id, pid=os.getpid())
        return True
    except (FileExistsError, FileNotFoundError):
        logger.log("CONTENTION_LOST", src=src.name, by=agent_id, pid=os.getpid())
        return False


class FcopLogger:
    """JSONL 日志写入器，线程安全"""
    def __init__(self, workspace: Path):
        self.dir = workspace / "fcop-logs"
        self.dir.mkdir(exist_ok=True)
        self._lock = threading.Lock()

    def log(self, op: str, **fields):
        entry = {"ts": utc_now_iso(), "op": op, **fields}
        today = datetime.utcnow().strftime("%Y-%m-%d")
        with self._lock:
            with open(self.dir / f"{today}.log", "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
```

#### 诊断命令

```bash
# 当日争抢失败总数
grep -c CONTENTION_LOST fcop-logs/2026-04-19.log

# 按 Agent 统计认领成功率
jq -r 'select(.op=="CLAIM" or .op=="CONTENTION_LOST") | .by + "\t" + .op' \
   fcop-logs/2026-04-19.log | sort | uniq -c

# 找出被争抢最激烈的任务
jq -r 'select(.op=="CONTENTION_LOST") | .src' fcop-logs/2026-04-19.log | sort | uniq -c | sort -rn
```

---

## 9. 互操作性与扩展

### 9.1 MCP 桥接（Model Context Protocol）

Patrol Engine 可选暴露 MCP 工具接口，让大模型直接从文件夹里"掏"任务：

**工具定义：**

```json
{
  "name": "fcop_fetch_pending_task",
  "description": "从 FCoP 工作区的 inbox/ 目录获取待处理任务，并原子认领",
  "inputSchema": {
    "type": "object",
    "properties": {
      "role": {
        "type": "string",
        "description": "当前 Agent 的角色名（如 DEV、QA）"
      },
      "workspace": {
        "type": "string",
        "description": "FCoP 工作区路径（可选，默认使用配置值）"
      }
    },
    "required": ["role"]
  }
}
```

```json
{
  "name": "fcop_complete_task",
  "description": "完成当前任务，生成 RESULT 文件，原 TASK 标记 DONE",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": { "type": "string" },
      "result_body": { "type": "string", "description": "Markdown 格式的结果正文" },
      "next_recipient": { "type": "string", "description": "结果发送给谁" },
      "status": { "type": "string", "enum": ["DONE", "FAILED"] }
    },
    "required": ["task_id", "result_body", "next_recipient", "status"]
  }
}
```

**Python MCP Server 骨架（基于 FastMCP）：**

```python
from mcp.server.fastmcp import FastMCP
from fcop import PatrolEngine, parse, create_task

mcp = FastMCP("fcop-patrol")
engine = PatrolEngine(workspace="./fcop-workspace")

@mcp.tool()
def fcop_fetch_pending_task(role: str) -> dict:
    """获取并认领 inbox/ 中最旧的 PENDING 任务"""
    candidates = engine.scan_inbox(role)
    if not candidates:
        return {"found": False}
    path, meta = candidates[0]
    claimed = engine.claim(path, meta)
    if not claimed:
        return {"found": False, "reason": "抢占失败，已有其他 Agent 认领"}
    content = claimed.read_text(encoding="utf-8")
    return {"found": True, "task_id": meta["task_id"], "content": content, "path": str(claimed)}

@mcp.tool()
def fcop_complete_task(task_id: str, result_body: str, next_recipient: str, status: str = "DONE") -> dict:
    """完成任务，生成 RESULT 文件"""
    engine.complete(task_id, result_body, next_recipient, status)
    return {"ok": True, "task_id": task_id, "status": status}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**在 `fcop-config.yaml` 中启用：**

```yaml
extensions:
  mcp_enabled: true
  mcp_port: 8765   # SSE 模式时使用
```

### 9.2 A2A 跨机协作（rsync 桥接）

对于跨物理机器的协作，使用 `rsync` 每分钟同步 `inbox/` 目录：

**单向推送（SENDER 机器 → RECIPIENT 机器）：**

```bash
# crontab 或 systemd timer，每分钟执行
rsync -avz --include="*.fcop" \
  ./fcop-workspace/inbox/ \
  user@remote-host:/path/to/fcop-workspace/inbox/
```

**双向同步（两台机器都有 Agent）：**

```bash
# 使用 --update 只同步更新的文件，避免覆盖正在执行的 RUNNING 文件
rsync -avz --update \
  user@remote-host:/path/to/fcop-workspace/inbox/ \
  ./fcop-workspace/inbox/
```

**注意事项：**
- 只同步 `inbox/`，不同步 `active/`（防止覆盖正在执行的任务）
- `archive/` 和 `done/` 可定期全量同步用于审计
- 网络不稳定时，rsync 的原子性由目标机文件系统的 `rename` 保证

**在 `fcop-config.yaml` 中配置：**

```yaml
extensions:
  a2a_rsync_enabled: true
  a2a_rsync_interval_s: 60
  a2a_rsync_targets:
    - host: "192.168.1.100"
      user: "agent"
      path: "/home/agent/fcop-workspace"
      direction: "push"    # push / pull / both
    - host: "192.168.1.101"
      user: "agent"
      path: "/home/agent/fcop-workspace"
      direction: "pull"
```

### 9.3 Webhook 集成

状态变更时触发 HTTP POST，集成企业微信、钉钉、Slack 等通知：

```yaml
extensions:
  webhook_enabled: true
  webhook_url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
  webhook_events:
    - FAILED          # 任务失败时通知
    - REVIEW          # 需要人工审核时通知
    - DONE            # 任务完成时通知（可选）
```

**Webhook Payload 格式：**

```json
{
  "fcop_version": "1.0",
  "event": "FAILED",
  "task_id": "20260419-143000-001",
  "sender": "PM",
  "recipient": "DEV",
  "thread_key": "ORDER20260419",
  "error_reason": "编译错误：缺少依赖包",
  "file": "TASK-20260419-143000-001-PM-to-DEV-FAILED.fcop",
  "timestamp": "2026-04-19T16:00:00Z"
}
```

### 9.4 Git 集成

FCoP 工作区可直接纳入 Git 版本控制：

```gitignore
# .gitignore（推荐配置）
fcop-workspace/active/        # 执行中的任务不需要版本控制
fcop-workspace/fcop-logs/     # 日志不需要
fcop-workspace/**/*.tmp       # 临时文件
```

```bash
# 每次任务完成后自动 commit（Patrol Engine 可选触发）
git add fcop-workspace/done/ fcop-workspace/failed/
git commit -m "FCoP: task ${TASK_ID} ${STATUS}"
```

**好处：**
- 完整的任务历史 `git log`
- 任务内容变更 `git diff`
- 可回滚任何历史状态

### 9.5 Cursor Rules 集成

在 `.cursor/rules/fcop-global.mdc` 中定义全局 FCoP 规则：

```markdown
# FCoP 全局协议规则

## 文件识别
以 .fcop 后缀的文件遵循 FCoP v1.0 协议。
读取时必须先解析 YAML Frontmatter，确认 recipient 字段匹配当前角色。

## 接单流程
1. 扫描 fcop-workspace/inbox/ 中 recipient 为本角色的 PENDING 文件
2. 原子重命名：xxx-PENDING.fcop → active/xxx-RUNNING.fcop
3. 按正文执行任务
4. 生成 RESULT 文件放入 inbox/
5. 原文件重命名 DONE，移入 done/

## 输出格式
严格按照任务文件"预期输出格式"章节输出，不自行添加字段。

## 禁止行为
- 不修改 active/ 中不属于自己的文件
- 不跳过 Patrol Engine 直接操作 archive/
- 不在一个文件输出多个任务结果
```

---

## 10. 错误处理与自愈

### 10.1 错误分类

| 错误类型 | 触发条件 | 自愈策略 |
|---|---|---|
| **超时（TIMEOUT）** | RUNNING 超过 `task_timeout_min` | 重置 PENDING + 递增 retry_count |
| **最大重试（MAXRETRY）** | retry_count ≥ max_retries | 标记 FAILED-MAXRETRY，发 ERROR 广播 |
| **过期（EXPIRED）** | 当前时间 > expires_at | 直接标记 FAILED-EXPIRED |
| **解析失败（PARSE_ERROR）** | 文件名不符合格式 | 移入 failed/，发 WARN 广播 |
| **内容校验失败（HASH_MISMATCH）** | 实际内容哈希 ≠ HASH 字段 | 标记 FAILED，发 ERROR 广播 |
| **Agent 崩溃** | RUNNING 文件长期无修改 | 同超时处理 |

### 10.2 人工干预手册

```
场景 1：任务卡在 RUNNING
  操作：将 active/xxx-RUNNING.fcop 重命名为 inbox/xxx-PENDING.fcop
  效果：Patrol Engine 下次扫描时重新分发

场景 2：任务失败，想修改需求重试
  操作：
    1. 编辑 failed/xxx-FAILED.fcop 正文，修改需求
    2. 将文件重命名为 inbox/xxx-PENDING.fcop
    3. 清空 Frontmatter 中的 error_reason
  效果：以新需求重新执行

场景 3：紧急插队（高优先级任务）
  操作：创建文件名带 -PRIO=HIGH 的任务放入 inbox/
  效果：Patrol Engine 优先分发高优先级任务

场景 4：暂停整个流水线
  操作：将 inbox/ 中所有 PENDING 文件移到临时目录
  效果：Patrol Engine 扫描到空 inbox/，暂停分发
```

### 10.3 DIAG 诊断文件规范

> **问题场景：** 任务进入 `failed/` 后，人类用户（尤其是移动端）只看到一个失败文件。要判断"原地重试"还是"改需求"，必须翻日志、查对话、看错误栈，非常低效。

FCoP 要求 Patrol Engine 在产生 `FAILED` 文件时，**自动生成配套的诊断文件**，汇总一次失败的所有关键信息。

#### 规范要求

```
MUST   Patrol Engine 在将任务转入 failed/ 时，必须在同目录生成 DIAG- 文件
MUST   DIAG 文件名格式：DIAG-{原任务 SEQ}-{原任务 task_id}.md
MUST   DIAG 文件使用 .md 后缀（不用 .fcop，因为它不参与状态机）
MUST   DIAG 内容必须包含：错误原因、最后 N 行日志、Agent 最后一段输出（如可得）、重试建议
SHOULD 移动端 PWA 应优先展示 DIAG 文件，失败文件次之
```

#### DIAG 文件结构

```markdown
---
diag_version: "1.0"
original_task: "20260419-143000-001"
failed_at: "2026-04-19T14:35:22Z"
error_category: "RETRY_EXCEEDED"   # RETRY_EXCEEDED / HASH_MISMATCH / TIMEOUT / COMPLIANCE / ZOMBIE
retry_count: 3
last_agent: "DEV"
recoverable: true                  # 建议是否可原地重试
---

## 错误摘要

在 3 次重试后仍超时，最后一次心跳停在 14:35:02。

## 最后日志片段（尾 20 行）

```
14:35:01 [DEV] Reading src/app.py ...
14:35:02 [DEV] CDP connection lost
```

## Agent 最后输出（如可得）

> 我正在重构 app.py，但发现依赖链涉及 17 个文件...

## 建议操作

- [ ] 原地重试（mv -RETRY=4）
- [x] 改需求：将任务拆分为更小粒度
- [ ] 转交其他 Agent
```

#### 参考实现

```python
def write_diag(workspace: Path, failed_file: Path, category: str,
               last_logs: list[str], agent_output: str = ""):
    meta = read_frontmatter(failed_file)
    seq = meta.get("task_id", "000").split("-")[-1]
    diag_name = f"DIAG-{seq}-{meta.get('task_id', 'unknown')}.md"
    content = f"""---
diag_version: "1.0"
original_task: "{meta.get('task_id')}"
failed_at: "{utc_now_iso()}"
error_category: "{category}"
retry_count: {meta.get('retry_count', 0)}
last_agent: "{meta.get('sender', 'unknown')}"
recoverable: {str(category != 'COMPLIANCE').lower()}
---

## 错误摘要

{meta.get('error_reason', '(无)')}

## 最后日志片段（尾 {len(last_logs)} 行）

```
{chr(10).join(last_logs)}
```

## Agent 最后输出

{agent_output or '（未采集）'}

## 建议操作

{"- [ ] 原地重试" if category != "COMPLIANCE" else "- [x] 需合规审查"}
"""
    (failed_file.parent / diag_name).write_text(content, encoding="utf-8")
```

### 10.4 required_tools 与 Skill Market 对齐

`required_tools` Frontmatter 字段不仅是声明，更是技能包动态加载的入口。

#### 规范要求

```
MUST    Frontmatter 的 required_tools 列表中每一项必须是全局唯一的技能 ID
SHOULD  技能 ID 格式：{domain}.{skill_name}，例如 cursor.edit / ocr.baidu / vehicle.vin_lookup
MUST    Agent 认领任务后，必须解析 required_tools 并加载对应的 .cursorrules 或等价规则
MUST    若任何一项 required_tools 无法加载，Agent 必须将任务改为 FAILED-REASON=MISSING_SKILL
SHOULD  技能包以目录形式放置：fcop-workspace/skills/{skill_id}/SKILL.md + rules.mdc
```

#### 技能目录结构

```
fcop-workspace/
└── skills/
    ├── cursor.edit/
    │   ├── SKILL.md              # 人类可读说明
    │   └── rules.mdc             # 自动注入 Agent 的 Cursor Rules
    ├── vehicle.vin_lookup/
    │   ├── SKILL.md
    │   ├── rules.mdc
    │   └── api_spec.yaml         # 可选：工具调用规范
    └── ocr.baidu/
        └── ...
```

#### Agent 加载流程

```python
def load_required_skills(task_meta: dict, workspace: Path) -> list[Path]:
    loaded = []
    for skill_id in task_meta.get("required_tools", []):
        skill_dir = workspace / "skills" / skill_id
        rules = skill_dir / "rules.mdc"
        if not rules.exists():
            raise SkillNotFoundError(skill_id)
        loaded.append(rules)
    return loaded
```

---

## 11. 安全模型

### 11.1 文件系统权限

```bash
# 推荐权限配置（Linux/macOS）
chmod 750 fcop-workspace/          # 目录：所有者+组可读写执行
chmod 640 fcop-workspace/**/*.fcop # 文件：所有者可读写，组可读

# Windows：使用 NTFS ACL 限制访问
icacls fcop-workspace /grant "DOMAIN\AgentGroup:(OI)(CI)M"
```

### 11.2 内容完整性

#### 规范要求

```
SHOULD  本地工作区：创建任务时写入 context_hash（SHA-256 前 12 位）
MUST    跨机器传输（rsync/scp/云盘同步）场景：context_hash 必须强制启用
MUST    接收方认领任务前，必须校验 hash；不一致则进入 failed/ 并附 REASON=HASH_MISMATCH
SHOULD  同时记录到 EXTRA 字段：HASH=abc123
```

#### 参考实现

```python
import hashlib

def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]

def create_task_with_hash(body: str, frontmatter: dict) -> str:
    h = compute_hash(body)
    frontmatter["context_hash"] = f"sha256:{h}"
    return h

def verify_on_claim(path: Path, meta: dict) -> bool:
    """认领时校验；跨机器场景下此校验强制，本地可降级为警告"""
    if not meta.get("context_hash"):
        return True
    expected = meta["context_hash"].replace("sha256:", "")
    actual = compute_hash(read_body(path))
    if expected != actual:
        fail_task(path, meta, "HASH_MISMATCH")
        return False
    return True
```

#### 为什么跨机器场景必须强制

rsync 在特殊情况下可能产生截断文件（网络中断、磁盘满），云盘同步可能因冲突而改写内容。context_hash 是协议层防止"内容损坏但元数据仍合法"的唯一手段。

#### context_hash 的第二重语义：幂等键（Idempotency Key）

> **在 AI 协作场景下，重复执行同一个任务的代价极高**（消耗 token、产生重复 PR、污染数据）。HASH 不仅是完整性校验，更是天然的幂等键。

```
MUST   Agent 认领任务前，必须扫描 done/ 目录，查找是否已存在同 context_hash 的已完成任务
MUST   若已存在且状态为 DONE，当前任务必须直接跳过执行，rename 到 done/ 并附 REASON=DEDUP
SHOULD 跳过时应保留指向原任务的引用：Frontmatter 添加 dedup_of: <original_task_id>
```

#### 参考实现

```python
def find_completed_by_hash(workspace: Path, hash_value: str) -> Path | None:
    """在 done/ 中查找同 HASH 的已完成任务"""
    if not hash_value:
        return None
    for done_file in (workspace / "done").glob("*.fcop"):
        meta = read_frontmatter(done_file)
        if (meta.get("context_hash") or "").replace("sha256:", "") == hash_value:
            return done_file
    return None


def claim_with_dedup(pending: Path, workspace: Path) -> Path | None:
    meta = read_frontmatter(pending)
    h = (meta.get("context_hash") or "").replace("sha256:", "")
    if h:
        duplicate = find_completed_by_hash(workspace, h)
        if duplicate:
            dedup_name = pending.name.replace("-PENDING.", "-DONE-REASON=DEDUP.")
            target = workspace / "done" / dedup_name
            update_frontmatter_field(pending, "dedup_of", meta.get("task_id", "unknown"))
            os.rename(pending, target)
            emit_event(workspace, "INFO", f"Deduplicated: {pending.name} == {duplicate.name}")
            return None
    return claim_task(pending, workspace)
```

#### 业务价值

- **车辆注册流水线**：同一辆车的 VIN 被重复提交时自动跳过，避免重复入库
- **代码修复任务**：同一段错误堆栈的修复请求被节流，避免 AI 重复分析
- **成本控制**：直接削减重复任务的 token 开销

> 如果业务语义要求"强制重跑"（例如 A/B 测试），应显式使用 `FORCE=1` EXTRA 字段跳过幂等检查。

### 11.3 并发安全：Windows 与 Linux 的差异

```
MUST  实现必须同时捕获 FileExistsError（Windows）和 FileNotFoundError（Linux race-loss）
MUST  两种异常均视为"认领失败"，必须静默返回 None，不得重试或告警
MUST NOT  使用 shutil.move，它在 Windows 上不是原子的
```

```python
def safe_atomic_claim(src: Path, dst: Path) -> bool:
    try:
        os.rename(src, dst)
        return True
    except (FileExistsError, FileNotFoundError):
        return False
```

### 11.4 敏感数据处理

对于涉及企业敏感逻辑（如车辆数据、财务数据）的任务：

```yaml
# fcop-config.yaml
security:
  encrypt_body: true           # 加密正文（v1.1 计划支持）
  allowed_roles:               # 角色白名单（仅允许指定角色访问特定目录）
    - role: FINANCE
      inbox_filter: "TASK-*-to-FINANCE-*"
  audit_log: true              # 所有读写操作写入审计日志
```

---

## 12. 版本兼容性

### 12.1 版本演进计划

#### 协议规范层

| 版本 | 状态 | 主要内容 |
|---|---|---|
| **v1.0.3** | ✅ 当前 | 归档策略 + RETRY 保留键 + Contention Lost 日志 |
| **v1.0.2** | ✅ 已发 | HASH 幂等键 + 优先级抢占 + DIAG 诊断 + Skill Market |
| **v1.0.1** | ✅ 已发 | 文件名即真理 + 僵尸任务检测 + Windows 并发规范 |
| **v1.0** | ✅ 已发 | 基础文件名协议 + Frontmatter + 三段式目录 + MCP/A2A/Webhook 桥接 |
| **v1.1** | 📋 计划 | 优先级队列实现、Git 自动 commit、文件锁原语标准化 |
| **v1.2** | 📋 计划 | 正文加密（AES-256）、数字签名验证 |
| **v2.0** | 🔮 远期 | 分布式工作区协议、FCoP-over-A2A 标准桥接 |

#### 工具与生态层（标准化工程）

| 项目 | 状态 | 说明 |
|---|---|---|
| **`fcop-cli`** | 📋 v1.1 计划 | 协议校验工具。提供 `fcop lint <workspace>` 检查目录结构与命名合规、`fcop trace <file>` 重建任务流转链、`fcop stats` 输出吞吐/争抢/归档统计 |
| **`fcop-mcp-bridge`** | 📋 v1.1 计划 | 标准 MCP Server，暴露 `fcop_fetch_pending_task` / `fcop_complete_task` / `fcop_emit_event` 三件套。让 Claude / Gemini / Cursor / VSCode Copilot 等任何 MCP 客户端直接读写 `.fcop` 工作区 |
| **`fcop-vscode`** | 📋 v1.2 计划 | VSCode/Cursor 扩展：`.fcop` 语法高亮、Frontmatter schema 校验、右键"认领/归档/重试" |
| **`fcop-py` SDK** | 📋 v1.1 计划 | 参考实现 SDK，PyPI 发布，`pip install fcop` 即可嵌入任意 Python 项目 |

> **fcop-cli 是标准化成败的关键。** 一个协议能否成为事实标准，不取决于规范写得多精致，而取决于"有没有一条命令能告诉你合不合规"。Webhook、Markdown、OpenAPI 全都是靠 lint 工具推起来的。

### 12.2 向后兼容规则

```
解析器 MUST 能解析所有低版本文件
解析器 MUST 对无法识别的 EXTRA 字段（-KEY=VALUE）静默忽略
解析器 MUST 对缺少可选 Frontmatter 字段的文件优雅处理（使用默认值）
解析器 MUST NOT 因为 TIME 字段格式变化而拒绝解析文件
```

### 12.3 与 CodeFlow agent_bridge 的迁移路径

| 阶段 | 内容 | 兼容性 |
|---|---|---|
| **当前（agent_bridge）** | `TASK-YYYYMMDD-SEQ-SENDER-to-RECIPIENT.md` | — |
| **过渡期（v1.0 对齐）** | nudger.py 同时支持旧格式和 FCoP 格式解析 | 双向兼容 |
| **目标（FCoP Native）** | 全面使用 `.fcop` 后缀 + 三段式目录 | 新格式为主 |

---

## 13. 参考实现

### 13.1 CodeFlow Desktop（生产级）

**仓库：** https://github.com/joinwell52-AI/codeflow-pwa
**文件：** `codeflow-desktop/nudger.py`

包含：
- CDP 集成（Cursor DOM 直连，无需截图/OCR）
- WebSocket 中继（手机 PWA 远程控制，端口 5252）
- watchdog 文件系统监听
- OOM 崩溃检测 + CDP 断线自动重连（端口 5253）
- 多角色并发巡检（`_probe_cdp` + 自愈机制）

### 13.2 最小实现参考（Python，约 100 行）

```python
#!/usr/bin/env python3
"""FCoP v1.0 最小 Patrol Engine 参考实现"""
import os, re, time, hashlib
from pathlib import Path
from datetime import datetime, timezone

FCOP_RE = re.compile(
    r'^(?P<type>TASK|RESULT|EVENT)'
    r'-(?P<date>\d{8})-(?P<time>\d{6})-(?P<seq>\d{3,6})'
    r'-(?P<sender>[A-Z][A-Z0-9_]{0,19})'
    r'-(?P<dir>to|broadcast)'
    r'-(?P<recipient>[A-Z][A-Z0-9_]{0,19})'
    r'-(?P<status>PENDING|RUNNING|DONE|FAILED|REVIEW|INFO|WARN|ERROR)'
    r'(?P<extra>(?:-[A-Z]+=\S+)*)\.(?P<ext>fcop|md)$'
)

_seq = 0
def next_seq():
    global _seq; _seq += 1; return _seq

def parse(name):
    m = FCOP_RE.match(name)
    if not m: return None
    d = m.groupdict()
    d['extra_kv'] = dict(p.split('=',1) for p in d['extra'].split('-') if '=' in p)
    return d

class PatrolEngine:
    def __init__(self, workspace, role, timeout_min=10, max_retries=3):
        self.ws = Path(workspace)
        self.role = role
        self.timeout_min = timeout_min
        self.max_retries = max_retries
        for d in ['inbox','active','done','failed','archive','events','fcop-logs']:
            (self.ws/d).mkdir(parents=True, exist_ok=True)

    def run(self, interval=5):
        print(f"[FCoP] Patrol Engine started. Role={self.role}, Workspace={self.ws}")
        while True:
            self.scan(); self.check_timeouts()
            time.sleep(interval)

    def scan(self):
        for f in sorted((self.ws/'inbox').glob('*.fcop')):
            meta = parse(f.name)
            if not meta or meta['status'] != 'PENDING': continue
            if meta['recipient'] not in (self.role, 'ALL'): continue
            claimed = self._claim(f, meta)
            if claimed:
                self.dispatch(claimed, meta)

    def _claim(self, path, meta):
        running = path.name.replace('-PENDING.', '-RUNNING.')
        target = self.ws / 'active' / running
        try:
            os.rename(path, target)
            return target
        except (FileNotFoundError, FileExistsError):
            return None

    def dispatch(self, path, meta):
        # 子类重写此方法实现具体业务逻辑
        print(f"[FCoP] Dispatched: {path.name} to {meta['recipient']}")

    def complete(self, running_path, result_body, next_recipient):
        meta = parse(Path(running_path).name)
        # 生成 RESULT 文件
        ts = datetime.now(timezone.utc)
        seq = next_seq()
        result_name = (f"RESULT-{ts.strftime('%Y%m%d')}-{ts.strftime('%H%M%S')}"
                       f"-{seq:03d}-{meta['recipient']}-to-{next_recipient}-DONE.fcop")
        (self.ws/'inbox'/result_name).write_text(result_body, encoding='utf-8')
        # 原 TASK → DONE
        done_name = Path(running_path).name.replace('-RUNNING.', '-DONE.')
        os.rename(running_path, self.ws/'done'/done_name)

    def check_timeouts(self):
        for f in (self.ws/'active').glob('*-RUNNING.fcop'):
            age_min = (time.time() - f.stat().st_mtime) / 60
            if age_min < self.timeout_min: continue
            content = f.read_text(encoding='utf-8')
            retry = int(re.search(r'retry_count:\s*(\d+)', content or '').group(1)
                        if re.search(r'retry_count:\s*(\d+)', content or '') else 0)
            if retry < self.max_retries:
                pending = f.name.replace('-RUNNING.', '-PENDING.')
                os.rename(f, self.ws/'inbox'/pending)
            else:
                failed = f.name.replace('-RUNNING.', '-FAILED.')
                os.rename(f, self.ws/'failed'/failed)

if __name__ == '__main__':
    import sys
    role = sys.argv[1] if len(sys.argv) > 1 else 'DEV'
    workspace = sys.argv[2] if len(sys.argv) > 2 else './fcop-workspace'
    PatrolEngine(workspace, role).run()
```

---

## 14. 附录

### 附录 A：dev-team 完整流水线示例

```
USER（手机 PWA）
  ↓ TASK-20260419-090000-001-USER-to-PM-PENDING.fcop
PM
  ↓ TASK-20260419-090500-002-PM-to-DEV-PENDING.fcop         (拆解任务)
DEV
  ↓ RESULT-20260419-100000-003-DEV-to-QA-DONE.fcop          (开发完成)
QA
  ↓ RESULT-20260419-103000-004-QA-to-OPS-DONE.fcop          (测试通过)
  ↓ RESULT-20260419-103000-004-QA-to-DEV-FAILED.fcop        (测试失败→打回)
OPS
  ↓ EVENT-20260419-110000-005-OPS-to-PM-DONE.fcop           (部署完成)
PM
  ↓ EVENT-20260419-110100-006-PM-to-USER-DONE.fcop          (最终回执)
```

### 附录 B：文件名字段速查

```
TASK - 20260419 - 143000 - 001 - PM - to - DEV - PENDING - PRIO=HIGH.fcop
│       │          │        │    │    │    │      │          │
│       │          │        │    │    │    │      │          └─ 扩展字段（可选）
│       │          │        │    │    │    │      └─────────── STATUS
│       │          │        │    │    │    └────────────────── RECIPIENT
│       │          │        │    │    └─────────────────────── DIRECTION
│       │          │        │    └──────────────────────────── SENDER
│       │          │        └───────────────────────────────── SEQ
│       │          └────────────────────────────────────────── TIME (HHMMSS)
│       └───────────────────────────────────────────────────── DATE (YYYYMMDD)
└───────────────────────────────────────────────────────────── TYPE
```

### 附录 C：常见问题

**Q: 两个 Agent 同时认领同一任务会怎样？**
A: `os.rename()` 在同一挂载点内是原子操作。只有一个 Agent 的 rename 会成功，另一个会收到 `FileNotFoundError`，静默跳过。这是 FCoP 唯一的同步原语，无需任何外部锁。

**Q: 跨网络驱动器（SMB/NFS）的 rename 是否原子？**
A: SMB/NFS 的原子性依赖服务端实现，不保证。生产环境建议使用本地文件系统或 Git 同步方案，而非直接挂载网络驱动器作为 FCoP 工作区。

**Q: .fcop 文件用什么编辑器打开？**
A: 任何文本编辑器均可。Cursor / VS Code 可安装 YAML 高亮插件改善阅读体验。未来可提供 `.fcop` 专属语法定义。

**Q: 与 MCP 的关系是什么？**
A: FCoP 是本地协调协议（文件系统），MCP 是工具调用协议（函数调用）。两者正交，可以共存：MCP 工具 `fcop_fetch_pending_task` 让大模型通过 MCP 接口拉取 FCoP 任务，本质上是 FCoP 的一种触发方式，不替代 FCoP 的文件系统基础。

---

*FCoP v1.0.3，2026-04-19，CodeFlow 项目组。*
*基于 Blackboard 模式与 Unix "一切皆文件" 哲学。*
*Issues & PR：https://github.com/joinwell52-AI/codeflow-pwa/issues*
