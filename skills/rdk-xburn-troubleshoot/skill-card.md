# Skill Card: rdk-xburn-troubleshoot

| Field | Value |
| --- | --- |
| name | rdk-xburn-troubleshoot |
| owner | xingshun_cai |
| license | Apache-2.0（代码）；文档按仓库 CC-BY-4.0 约定 |
| kind | troubleshooting workflow |
| riskLevel | medium：只读分析；恢复操作可能改写启动固件或系统盘 |
| platforms | RDK S100、S600、X5；X5 Module 按其专用设置区分 |

## Use case

从板型、介质和链路选择检查顺序，解释 DFU/XModem、Fastboot、写入结果及启动验证。X5 普通读卡器写卡与 BSP 编译另行处理。

## Known risks

相同的进度、分区名和通信错误在不同板上含义不同。S100 的单次成功不能证明 S600/X5 通过测试；后两者的指引来自产品手册。写入前明确目标和恢复路径。

## Sources

[板型分支与官方手册](references/board-routes.md)；[S100 实测摘要](references/s100-success.md)；[五维评估场景](evals/tasks.yaml)。
