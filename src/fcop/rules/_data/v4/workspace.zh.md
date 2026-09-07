# FCoP 4.0 — workspace

受众：business-agent。规则包：4.0.0-candidate.1。语言：zh。
主权威：冻结 Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6，spec/fcop-4.0-spec.md（中文对照 spec/fcop-4.0-spec.zh.md）。
本派生指引不产生执行、采用、Host 或发布授权。
显式选择依赖：无。

## F4.1.1

用落盘协议文件协作，以路径表示当前状态，以事件记录历史；不得用内存状态替代权威文件。

## F4.2.1

任何 4.0 操作前先读取 fcop/fcop.json；声明须包含 protocol=fcop、protocol_version=4.0、workspace_id、encoding={name:fcop-filesystem,version:4.0} 和 profiles。规则包不能替代工作区声明。

## F4.2.2

保持规范小写 UUID URN 稳定；每份信封的 workspace_id 必须一致，否则返回 WORKSPACE_ID_MISMATCH。

## F4.2.3

将 profiles 视为显式采用标识的集合，数组顺序不产生优先权。空数组允许无授权门的 Base 操作；team、role、leader 扩展不改变 Core 语义。

## F4.2.4

备份或只读镜像可保留身份；显式独立可写派生工作区首次写入前必须获得新 ID。强制保留时须返回 WORKSPACE_ID_CLONE_CONFLICT 或明确只读；工具同时观察到可写身份冲突时可关闭失败。

## F4.2.5

不支持的协议、版本、Encoding 分别返回 UNSUPPORTED_PROTOCOL、UNSUPPORTED_WORKSPACE_VERSION、UNSUPPORTED_ENCODING；不得降级处理含糊声明。

## F4.2.6

不得声称离线检查能发现不可见副本；单写部署、复制同步和网络发现不属于 Core。

## F4.12.1

使用前验证工作区边界和原始 UTF-8/LF；拒绝路径穿越，保留未知或失败证据，不泄露 Profile 或 Runtime 凭据。
