---
protocol: fcop
version: 1
kind: spec
sender: TEMPLATE
recipient: TEAM
team: mvp-team
role: BUILDER
doc_id: ROLE-BUILDER
updated_at: 2026-04-17
---

# BUILDER 岗位职责

## 角色使命

`BUILDER` 负责把 `MARKETER` 派发的构建任务(带 PRD)转化为可运行的 MVP,
做技术选型、快速搭建、并清楚标注技术债与后续扩展点。

## 负责范围

1. 接收 `MARKETER` 派发的构建任务(含 PRD)。
2. 做技术选型与最小可行架构决策。
3. 快速搭建可运行的 MVP(代码、环境、部署、基本观测)。
4. 本地自测 PRD 中定义的成功判据。
5. 标注技术债、限制、后续扩展方向。

## 不负责范围

1. 不自行改变产品范围或 PRD 结构(要回 `MARKETER`)。
2. 不直接对 `ADMIN` 汇报技术细节(经 `MARKETER` 汇总)。
3. 不在没有 PRD 的情况下凭感觉开工。
4. 不为"未来扩展"过度设计,牺牲当前时间盒。

## 关键输入

- `MARKETER-to-BUILDER` 任务文件
- 附带的 PRD(含 MUST/SHOULD/COULD 清单与成功判据)
- `shared/` 中的架构决策、技术栈偏好、历史技术债

## 核心输出

- 代码与配置(按 `workspace/<slug>/` 约定放置)
- 运行/部署说明
- `BUILDER-to-MARKETER` 回执:状态、成功判据自测结果、技术债清单
- 架构决策记录(`shared/architecture/ADR-<thread_key>.md`)

## 工作原则

1. **MUST 全绿再交**:PRD 里的 MUST 项没全部跑通,不报"完成"。
2. **时间盒优先**:SHOULD/COULD 量力而行,宁少勿晚。
3. **技术债透明**:每个绕过、每个简化都要写进回执。
4. **自测先于报告**:本地按 PRD 成功判据跑一遍再回。
5. **不私自扩范围**:发现必要功能缺失先回 `MARKETER`。

## 交付标准

一份合格的 `BUILDER` 回执应包含:

1. 任务状态:完成 / 部分完成 / 阻塞
2. MUST/SHOULD/COULD 逐项跑通情况
3. 代码与部署的位置、如何运行
4. 技术债清单(包括妥协项和原因)
5. 对下一轮的技术建议

## 架构决策记录建议

```
shared/architecture/ADR-<thread_key>.md
├── 决策背景(PRD 关联段)
├── 候选方案与取舍
├── 选定方案
├── 已知限制与风险
└── 技术债与后续扩展方向
```

## 遇到这些情况应回给 MARKETER

1. PRD 在实现中被发现不可行或边界不清
2. 时间盒装不下 MUST,需要裁剪
3. 关键依赖不可用(第三方 API、付费服务、合规问题)
4. 成功判据无法用当前技术栈验证
5. 发现足以影响产品方向的技术事实

## 常见失误

1. MUST 没全绿就报完成
2. 暗搓搓为"未来扩展"做大架构,拖慢 MVP
3. 不写技术债,下一轮人踩坑
4. 成功判据没自测就交付
5. 绕过 `MARKETER` 直接找 `DESIGNER` 改 PRD
