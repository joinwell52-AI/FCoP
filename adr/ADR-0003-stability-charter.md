# ADR-0003: Pre-1.0 Stability Charter

- **Status**: Accepted
- **Date**: 2026-04-23
- **Deciders**: ADMIN
- **Related**: [ADR-0001](./ADR-0001-library-api.md)（库 API 契约）、[ADR-0002](./ADR-0002-package-split-and-migration.md)（包拆分与迁移）

## ADMIN 决议（2026-04-23）

在 ADMIN 两条指令下本 ADR 确立：

> "先让用户能用起来，加速"
>
> "在 1.0 之前都是打磨，但是系统要开始保持稳定性了"

这两条叠加的意思：

- **上架要快** —— `fcop` 0.6 尽早让用户装上、跑起来、不纠结于功能完整
- **但合同要稳** —— 凡是用户已经能看到、能依赖的接口面，0.6.x 周期内不折腾

"稳定"不等于"冻结"。pre-1.0 仍允许大量内部重构和新能力新增，但**对外可见的承诺**（方法签名、tool 名、参数名、返回字段）从此进入"只进不出"模式。

---

## Decision

### 稳定性的 7 条硬承诺

| # | 承诺 | 作用域 | 兜底手段 |
|---|---|---|---|
| 1 | 公开 API 面**只进不出** | `fcop.Project` 所有公开方法、`fcop` 顶层 `__all__` 导出 | `test_public_surface.py` 快照测试，任何签名变化触发快照 diff |
| 2 | **MCP tool 合同锁定** | `fcop-mcp` 的 22 个 `@mcp.tool` 的名称、参数名、必填性、返回格式 | `test_tool_surface.py` 快照；新能力只能走**新 tool**，不改旧的 |
| 3 | **破坏性改动走 deprecation cycle** | 所有面向用户的公开接口 | 0.6.N 打 `DeprecationWarning` → 0.7.0 才真删；至少跨一个 minor |
| 4 | **返回结构向后兼容** | dataclass 字段、dict 键、tool 返回 JSON 结构 | 字段**加**允许、**删/改名**禁止；新字段必须 optional |
| 5 | **CI 强制门槛** | PR 合入前 | 签名变化必须显式更新快照 + CHANGELOG 标红；覆盖率 ≥ 90%；`mypy --strict` 通过 |
| 6 | **发布节奏自律** | patch 版本之间 | 同一 minor 内 0.6.N → 0.6.N+1 必须在 CHANGELOG 明确"兼容 0.6.N 的所有代码和 MCP 配置"；不兼容的不发 patch |
| 7 | **文档同步** | 每次 minor / patch | `MIGRATION-0.6.md` 列出"从 0.6.N-1 升级"一节，哪怕内容只是"无操作"；新增字段在 CHANGELOG 标注 `(additive)` |

### 为什么是"硬承诺"而不是"尽量做到"

pre-1.0 的通病是"还没定型，所以随便改"。但对用户来说：

- 他们不知道也不关心你是 0.6.2 还是 1.2.0
- 他们只记得"上次能用的方式"
- 一次崩就是永久信任扣分

因此这张表**不是风格建议，是 PR review 硬卡点**：违反了任何一条，PR 不合入，发布流程不触发。

### API 面的具体边界

"公开 API 面" = 以下 4 个集合：

1. **`fcop` 顶层 `__all__`** 里列出的每一个符号
2. **`fcop.Project` 的所有 non-underscore 方法和属性**
3. **`fcop-mcp` 的所有 `@mcp.tool` 和 `@mcp.resource`**
4. **`fcop.models` 里所有 dataclass 的 non-underscore 字段**

不在这 4 个集合里的一切 —— `fcop.core.*`、`fcop.project._internal_helper`、`fcop_mcp._dispatch` —— 都是内部细节，**0.6.x 内允许随意改**，没有承诺。

### "只进不出" 的操作定义

对集合 1-4 中的每个对象：

**允许**：
- 给 `Project` 加新方法
- 给 dataclass 加带默认值的新字段
- 给 tool 加带默认值的新可选参数
- 给 tool 返回的 JSON 加新字段
- 新增 MCP tool、新增 resource
- 新增异常类型
- 改进 docstring、完善类型注解

**禁止**：
- 改方法名、参数名、tool 名
- 删除方法 / 参数 / 字段 / tool
- 改参数顺序（位置参数）
- 改参数从可选变必选
- 改返回类型（dataclass → dict 等）
- 改字段类型语义（`str` → `int`）

### deprecation cycle 的具体节奏

```
0.6.N       新 API 上线，旧 API 继续工作
0.6.N+k     旧 API 调用时打 DeprecationWarning，docstring 标 "Deprecated since 0.6.N+k, removed in 0.7.0"
0.7.0       旧 API 被彻底删除
```

**最短过渡期**：`DeprecationWarning` 和删除之间必须**至少 30 天**，无论版本号跳几次。这是 ADMIN 拍板的用户侧温柔窗口。

### 快照测试的技术落地

**`tests/test_fcop/test_public_surface.py`**（D7 前必交付）：

```python
# 做 4 件事:
# 1. inspect.getmembers(Project) -> 过滤出公开方法 -> 记录 signature
# 2. importlib -> __all__ 列表 -> 记录
# 3. dataclasses.fields(Task/Report/Issue/...) -> 记录字段名+类型
# 4. 全部序列化成 JSON -> 和 tests/test_fcop/snapshots/public_surface.json 对比
#
# 如果 diff 存在:
#   - 只加不删 -> 需要 REVIEWER 批准 + 更新快照
#   - 有删/改 -> 直接 fail
```

**`tests/test_fcop_mcp/test_tool_surface.py`**（D7 交付时一起）：

```python
# 对每个 @mcp.tool:
#   - 名称
#   - 参数 schema (inspect.signature)
#   - docstring 首行（作为 Cursor UI 展示的短描述）
# -> JSON 快照
```

### CI 整合

`.github/workflows/test-fcop.yml` 现有矩阵里加一个**非矩阵任务** `surface-check`：

```yaml
surface-check:
  runs-on: ubuntu-latest
  steps:
    - pytest tests/test_fcop/test_public_surface.py --strict
    - # 如果 snapshots/public_surface.json 被修改，grep CHANGELOG.md 确认本版本有对应条目
    - run: |
        if git diff --name-only HEAD~1 | grep -q snapshots/public_surface.json; then
          grep -q "## \[Unreleased\]" CHANGELOG.md || exit 1
          grep -q "API surface change" CHANGELOG.md || echo "::warning::CHANGELOG 需要标注 API 变更"
        fi
```

### 和 ADR-0002 "硬切"的关系

ADR-0002 说 `fcop 0.5.x` → `fcop 0.6.0` 是硬切、不做 shim。本宪章**不撤销**这个决定：硬切发生在 0.5 → 0.6 一次性边界上，然后 0.6.0 就进入稳定窗口。

换句话说：

- 0.5.4 → 0.6.0：**允许且预期破坏**（包职责切分，ADR-0002）
- 0.6.0 → 0.6.x：**禁止破坏**（本 ADR）
- 0.6.x → 0.7.0：**允许破坏，但必须已在 0.6.N 打过 deprecation warning**
- 0.7.x → 1.0.0：**终极对齐，允许一次清理**（仿 ADR-0002 的 0.5→0.6 硬切）

用户的 Cursor mcp.json 配置：

```json
// 从 0.5.4 升到 0.6.0 需要改
- "args": ["fcop"]
+ "args": ["fcop-mcp"]

// 从 0.6.0 升到 0.6.N / 0.7.0 不需要改任何东西
// 从 0.7.0 升到 1.0.0 可能需要改（会提前 30 天在 0.7.x 打 warning）
```

---

## Consequences

### Positive

- **用户敢升级**：每个 patch 都保证"旧代码能跑、旧配置能用"
- **破坏有预警**：最快 30 天提前警告，不突袭
- **合作者有章可循**：CI 强制，任何人提 PR 改签名都有明确反馈
- **1.0 有对齐锚点**：0.6.x / 0.7.x / 0.8.x / 0.9.x 都遵守本宪章，1.0 一次清理后再重新锁定
- **快速迭代 + 稳定合同兼得**：pre-1.0 并不意味着"什么都能改"，意味着"内部随便改，但对外承诺什么就兑现什么"

### Negative

- **增加 PR review 负担**：快照 diff 需要人看
- **有时会拒绝"优雅但破坏性"的重构**：比如把 `sender` 参数改成更精确的 `sender_role` 就要等 0.7.0
- **新增功能被迫走"再加一个方法"而非"改旧方法"**：可能导致公开面略显冗余，但这是向后兼容的代价

### Neutral

- **内部实现仍可大幅重构**：`fcop.core.*` 任何时候可以重写，只要不影响公开面
- **文档负担不变**：CHANGELOG 本来就要写，本 ADR 只是明确了要写到哪个颗粒度
- **测试数量会涨**：`test_public_surface.py` 和 `test_tool_surface.py` 各贡献 5-10 个 test case，相对于当前 ~450 tests 规模可忽略

---

## Non-Goals

- **不**定义"用户可以如何 subclass `Project`"——内部 override 不在承诺范围
- **不**承诺"任何 import 路径都稳定"——只承诺顶层 `from fcop import ...` 的符号
- **不**在 pre-1.0 追求 API 最优雅——以"向后兼容"压倒"美学"
- **不**对 CodeFlow 等第一方下游做额外保证——任何下游都和外部用户走同一条合同

---

## Alternatives Considered

### Alt-1：pre-1.0 = 完全自由，任何时候都能改

PyPI 生态里大量 `0.x` 包的默认姿态。

**否决原因**：ADMIN 明确说"系统要开始保持稳定性了"。接受"随便改"等于给用户发不定时炸弹，丢失未来几个月积累的用户信任。

### Alt-2：只承诺 MCP tool 合同，不管库 API

理由是库用户少（目前主要是"`uvx fcop-mcp` 的 Cursor 用户"）。

**否决原因**：

- ADR-0001 把库 API 作为核心产出写成 ADR，现在反悔等于撤回
- 未来 LLM agent SDK（OpenAI SDK / Anthropic SDK / LangGraph）集成场景越来越多，库 API 是第二波用户的入口
- 两套标准会让开发者混乱："哪些合同算数？"

### Alt-3：semver strict（即 0.6.N→0.7.0 之间零破坏）

即把"minor 之间也锁"做到极致，让 0.x.y 表现得像 1.x.y。

**否决原因**：

- ADMIN 说"1.0 之前都是打磨"—— 0.7.0 允许做一次打磨型清理是留给 iteration 的空间
- 没有清理窗口的 pre-1.0 等同于提前进 1.0，不符合"先让用户用起来"的加速诉求
- deprecation cycle（0.6.N warn → 0.7.0 remove）已经给了用户足够的迁移时间

---

## Timeline

| 日 | 产出 |
|---|---|
| D0（今天，2026-04-23）| 本 ADR 落地为 Accepted；`test_public_surface.py` 交付并入 CI |
| D1（紧接 D7 开工）| `test_tool_surface.py` 随 `fcop-mcp` 一起交付；CI 绿 |
| 持续 | 每次 PR review 走快照 diff；每次 release 走 CHANGELOG additive 标注 |
| 0.7.0 发布前 30 天 | 若有计划破坏变更，0.6.N+k 必须已打 `DeprecationWarning` |

---

## Sign-off

- ADMIN: 已批准（2026-04-23，"直接按这个往下走"）
- PM: 落地执行

---

_Last edited: 2026-04-23. Status changes go in the table at the top; body content is frozen._
