# Skill Card: rdk-x5-usb-drive-flash

| Field | Value |
| --- | --- |
| name | rdk-x5-usb-drive-flash |
| owner | Dasoncai |
| license | Apache-2.0（代码），文档遵循仓库 CC-BY-4.0 约定 |
| kind | workflow |
| riskLevel | high：启动已准备好的升级盘可能覆盖板上存储 |
| platforms | RDK X5；需板端 U-Boot 支持本技能引用的 2.0.0 流程 |
| data-classification | public |

## Use case

确认固件是否支持从 USB 存储读取更新，制备单一目标的原始整盘镜像或分片，按介质、写入和启动三个阶段验证。

## Known risks

芯片 SDK 文档不保证特定开发板固件支持；分区、稀疏镜像、直接读卡器写卡不在检查脚本范围。脚本仅检查文件，不能替代备份、镜像来源核查或实板启动验证。

## Sources

[公开 X5 芯片手册 2.0.0](https://developer.d-robotics.cc/sdk_doc/versions/2.0.0/en/linux_development/system_component_development/42-Auto_update_system_by_USB_storage.html)、[公开 RDK 镜像指南](https://developer.d-robotics.cc/rdk_x_doc/Quick_start/system-burn/burn-sd-card)、[制盘说明](references/prepare-and-verify.md)、[评估场景](evals/tasks.yaml)。
