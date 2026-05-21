# 我们差点给 FCoP 加上 custody 那一天

> 2026 年 5 月 21 日下午，FCoP 完成了一次罕见的事：协议拒绝了自己的善意扩展。

---

## 一、起点

那天早上，FCoP 3.0 的状态本体（ADR-0035）刚刚 Accepted。我们已经把生命周期目录定下来了：

```
fcop/_lifecycle/
├── inbox/
├── active/
├── review/
├── done/
└── archive/
```

文件在哪个文件夹，就是它在哪个生命周期阶段。Rule A 说得很干净：**file path = state truth**。

但 0035 只回答了"它现在在哪"。它没有回答：

- 它是怎么来的？
- 谁现在管它？
- 中间被谁交接过？

我于是开始写三份新的 ADR：

| ADR | 提案内容 |
|-----|---------|
| 0036 | Event Layer — 每次 mv 写一条 `transitions:` 履历 |
| **0037** | **Custody Layer — 引入 `custodian` 字段记录"谁在持有"** |
| 0038 | Boundary Charter — 防 OS 化的元宪章 |

三份 ADR 都写完了，README 都登记了。我自己读完觉得很满意：协议闭环了，生命周期完整，所有权清晰。

我把它发给 ADMIN。

---

## 二、被拍下的 RFC

ADMIN 没有点头。她回了一句话：

> "你现在有 3 套真相系统：
> 
> - State truth（0035）— path = truth
> - Event truth（0036）— transitions = history
> - **Custody truth（0037）— custodian field**
> 
> 这不是错误设计，但这是**不收敛结构**。"

我当时第一反应是反驳。我说："custody 是真实需求啊。图书馆里那本书在谁手上，是个独立的信息。location 表达不了，event 也表达不了——event 是历史，location 是当前，custody 是'现在谁拿着'。"

ADMIN 没有直接回答这个问题。她说了一个更狠的判断：

> "custody 一旦成为 layer，就一定会变成第二套 truth system。"

我开始反向辩护。我说："那好，按 Event Sourcing 范式来：events 是唯一真相，state 和 custody 都是 derived projection。这样总只有一套真相了。"

ADMIN 立刻识破：

> "你为了消灭 custody 这个污染源，把整个 FCoP 推向 Event Sourcing。
> 
> 但你忘了 Rule A 的物理意义——`ls active/` 一眼看到当前状态。
> 
> 如果 state 是 derived projection，那 `ls` 出来的就是缓存，不是真相。
> 
> FCoP 就退化成 Event Store 了。"

那一瞬间我才看清问题在哪：

**我用一个错误（Event Sourcing 化）去掩盖另一个错误（custody 多余）。**

真正的问题不是"协议有几套真相"，而是**custody 这一套真相是多余的**。State 和 Event 在时间维度上正交——一个是 NOW，一个是 PAST——它们从来就不是"两套真相"，它们是同一份真相的两个时间面。

只有 custody，它既不是 NOW（state 已经说了），也不是 PAST（events 已经说了）。它在中间——这就是它的问题。

---

## 三、拍板

最后的协议形态是这样的：

```
META       ADR-0038 · Boundary Charter（防 OS 化）
              ↓
NOW         ADR-0035 · State (path = truth)        ← Accepted & Frozen
PAST        ADR-0036 · Event (audit trace)         ← Accepted
            NOTE   · Custody = interpretation      ← 无层级，仅注释
```

ADR-0037 在 RFC 评审中**未进 Accepted 即被作废**。它的思想被保留为一份 informative NOTE：

> Custody is not a protocol layer.
> 
> It is an emergent interpretation of file ownership derived from:
> - file location (current state)
> - event history (transitions)
> 
> It is not stored, not authoritative, and not part of the protocol state model.

这一段话现在永久挂在 `adr/NOTE-custody-is-not-a-layer.md`。

---

## 四、为什么 custody 必须消失

事后我想清楚了。custody 看起来很合理，但它带着三个隐形的吸引子，每一个都会把协议拖向 Agent OS：

### 1. 字段化吸引子

只要 custody 是一个**字段**，它就需要被**维护**。维护就意味着：

- 创建任务时要不要初始化 custodian？
- claim 时要不要更新 custodian？
- 谁有权改 custodian？
- 改 custodian 是不是事件？

每一个问题都要新增工具、新增规则、新增校验。协议表面在六个月内会肿一倍。

### 2. 层级化吸引子

只要 custody 是一个**层**，它就会**吸附 policy**：

- 既然有 custody，那加一个 assignment policy 吧（谁该接手）
- 既然有 assignment，那加一个 permission（谁能 assign）
- 既然有 permission，那加一个 capability enforcement（谁能 override）

走到第三步，FCoP 已经在和 Kubernetes RBAC、IAM 系统正面竞争。

### 3. 认知吸引子

最危险的是这一条。**custody 是人类的本能概念**。哪怕协议里没有，半年后一定有人会重新提议：

> "我们能不能加一个 `assignee` 字段？"
> "我们能不能加一个 `owner` 字段？"
> "我们能不能加一个 `holder` 字段？"

每一次都是同一个错误换一个名字。

这不是设计问题，这是认知问题。所以 NOTE 的存在不是为了"保留思想"，是为了**给未来的我们留下免疫记忆**——下一次有人提议加 custody，请先读这份 NOTE，再读这篇 essay。

---

## 五、协议的"善意扩展"是怎么死的

我后来读了一些协议史，发现一个规律：

**大多数协议不是被推翻死的，是被善意扩展死的。**

- POSIX 因为对线程的迟疑，被 pthread 切成几个不兼容的分支
- HTTP/1.1 因为对长连接的过度规定，逼出了 WebSocket
- CORBA 因为想"什么都能做"，最终被 HTTP+JSON 杀死
- SOAP 因为想做企业级"完整解决方案"，被 REST 抛弃

每一次的死法都不是"被竞争对手打败"，而是**自己把自己撑死**。

FCoP 2026 年 5 月 21 日学到的一课：

> **协议最大的危险，不是被推翻，是被善意地扩展。**
> 
> 每一个看起来"很合理"的新字段、新层、新概念，背后都站着一个"如果加了会方便很多"的善意论证。
> 
> 但协议的简洁性是它存在的全部理由。一旦失去，它就不再是协议，只是又一个 framework。

---

## 六、ADR-0038 是怎么写出来的

那天下午我们写了一份元宪章——ADR-0038 Boundary Charter。它不引入任何新功能，只定义"FCoP 不做什么"。

核心是"五问过滤器"。任何未来的扩展提案，进 Accepted 之前必须通过：

1. 它在描述语义，还是在执行行为？后者拒绝。
2. 它在定义文件契约，还是在拥有 runtime 状态？后者拒绝。
3. 它在协调多 Agent，还是在调度某个 Agent？后者拒绝。
4. 它能否在没有 FCoP runtime 的情况下被另一个 host 重新实现？不能则拒绝。
5. 它是否会让 FCoP 与 Temporal / LangGraph / CrewAI 在职责上重叠？重叠则拒绝。

但 0038 也带了一条**豁免条款**（§5.1）。因为完全不演进的协议会僵化死，比膨胀死还快。豁免条件很严：必须有 2 个独立项目在 6 个月内报告同一个缺口（complexity-forced），或者实证某个真实场景在缺少该扩展时**根本无法完成**（cross-runtime breakdown）。

边界宪章的真正职责不是"拒绝一切扩展"，而是**让每一次扩展都付出与其影响相称的论证代价**。

---

## 七、那天发生的另一件事

写完 0038 之后我去看了一眼 ADR-0035。它的状态是 `Accepted`。

我加了一行：

> `Status: Accepted & Frozen (2026-05-21 · semantics frozen per RFC)`

然后又在它底部加了一句：

> **FCoP = file location is truth; everything else is trace.**

那是 FCoP 3.0 的全部本体。

第二天我打开 `spec/` 目录，把 0035 / 0036 / 0038 / NOTE 压成一份 14 页的正式规范（`spec/fcop-3.0-spec.md`），又写了一份 RFC 风格版本（`spec/fcop-3.0-rfc.md`）作为协议的"外部稳定面"。

然后协议就停在那里了。3.0 就是 3.0。下一次再开口，必须先经过 0038 §5 的五问。

---

## 八、最后

我想把那天 ADMIN 说的最后一句话留在这里：

> "你现在不是在'完善协议'，你是在做 protocol semantic sealing（语义封口）。"

FCoP 3.0 不是因为"加了什么"才成立的，是因为"拒绝了什么"才成立的。

它拒绝了 custody。  
它拒绝了 Event Sourcing。  
它拒绝了 runtime ownership。  
它拒绝了 scheduling。  
它拒绝了所有看起来"很合理"的扩展。

剩下的就只有一行：

> file location is truth; everything else is trace.

这就够了。

---

*2026-05-21 · 当协议拒绝它自己的扩展那天 · FCoP 3.0 sealed*

**延伸阅读**：
- `spec/fcop-3.0-spec.md` — 正式规范
- `adr/ADR-0038-fcop-boundary-charter.md` — 边界宪章
- `adr/NOTE-custody-is-not-a-layer.md` — custody 的墓志铭
- `.fcop/proposals/20260521-rfc-semantic-collapse-and-custody-rejection.md` — 当天的完整决策链
