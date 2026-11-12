---
name: rdk-xburn-troubleshoot
description: 排查 RDK S100、S600、X5 使用 XBurn 时的设备识别、DFU 或 XModem 引导、Fastboot 连接、写入失败及烧录后启动问题。按板型、介质和实际链路分析主机与串口日志。适用于烧录故障或成功日志核对，不用于 BSP 编译或使用读卡器写卡。
version: 1.0.0
license: Apache-2.0
metadata:
  tags: [rdk, xburn, s100, s600, x5, troubleshooting]
---

# RDK XBurn 烧录排查

## Purpose

从失败日志给出三个可核对的结果：哪块板的哪个步骤失败、此前哪些步骤已完成、下一项检查能区分哪些原因。工具完成写入和操作系统正常启动分别取证。

## When to use

- RDK S100 / S600 使用 XBurn 更新、恢复或核对烧录结果；RDK X5 使用 XBurn 更新 NAND 启动固件或写系统镜像。
- 如果只说“X5 烧卡失败”，先确认是 PC 读卡器写卡、在板映射磁盘，还是 XBurn 在板下载。前两类按对应写卡工具处理。
- S 系列源码与构建交给 `bsp-s-series`；X5 编译 miniboot 交给 `bsp-bootloader-build`。构建成功不能证明板端已经写入。

## Instructions

### 1. 先确定板型、目标和链路

从现有日志提取型号和硬件修订、XBurn/主机版本、镜像来源与目标介质、连接/下载模式、全量或指定区域、板卡是否还能进入 U-Boot。只追问会改变下一步判断的缺项。对照[板型与介质](references/board-routes.md)选择一个分支：

- **S100**：系统盘是 eMMC；全量烧录也可能写 NOR 启动区。USB 恢复流程可能先 DFU 再 Fastboot；非空板能进 U-Boot 时，直接 Fastboot 不需要先有 DFU 日志。
- **S600**：先区分板载 UFS 与扩展 NVMe，核对镜像针对的介质、工具所选介质及 SW8 启动盘选择；另行确认当前硬件版本进入 DFU 的方法。不要用 S100 的 eMMC 区域清单解释 S600。
- **X5**：确认标准开发板还是 Module，再区分 NAND miniboot 与操作系统镜像。串口引导超时先查 XModem 侧；引导通过、Fastboot 找不到设备则转查 USB 侧。U-Boot 可用且实际使用 USB Fastboot 时不要求 XModem。NAND 更新成功不能证明 SD 卡或 Module 的 eMMC 系统可用。

### 2. 找到第一个未完成的阶段

按同一设备、同一次尝试整理“最后成功事件 → 首个有效错误 → 重试或最终状态”。配置、预定执行链和进度条不等于实际执行。日志时间基准不同，用下载项、模式切换、板端启动标记对应三路日志，别按绝对时间硬拼。

| 最后观察到什么 | 下一项检查 | 如何区分结果 |
| --- | --- | --- |
| 加载镜像或参数校验失败，还没开始传输 | 比对本板产品、解压目录、映像类型、目标介质及实际缺失文件 | 缺文件或选错目录先解决输入；配置失败不能直接判存储坏 |
| 等待 DFU 或部分下载后设备消失 | 对照该板修订的下载模式指示和阶段前后主机 USB 枚举 | 从未枚举先查模式、线缆、供电；切换后已枚举但工具打不开，再查对应驱动或权限 |
| 等待 UART 或 XModem 应答 | 仅对实际串口引导：查主机是否有此端口、是否被串口终端占用、该板串口参数和上电握手顺序 | 没有端口和有端口却收不到正确应答是两个阶段；记录实际收到的字节 |
| 引导结束但等不到 Fastboot | 对照板端 U-Boot/Fastboot 状态与主机的 `fastboot devices` 输出 | 板端没进入模式先查引导；板端已进入而主机不可见，再查 USB 数据口、驱动、权限。单次空列表不等于最终超时 |
| 某项发送、写入、校验或返回状态失败 | 记录具体镜像、介质、区域、命令返回与是否重枚举；按时间找首次失败 | 区分发送失败、写入失败和状态读取失败；`Too many links` 不能独自证明线坏。Hash 错误先核对可信校验值、板型和包类型 |
| 工具成功但黑屏或仍是旧系统 | 确认写了什么、实际从哪里启动，采集本次正常启动串口至内核/登录 | 按 U-Boot、内核、根文件系统、用户空间或显示分别定位。尤其留意 S600 启动盘和 X5 是否只更新 NAND |

### 3. 给出结论与下一步

- 最终板卡状态优先于外层进程退出码。若失败后重试成功，分开报告；若日志被截断，标记“最终结果未知”。
- 每个推断附上一条证据、一项最小检查及预期分支。警告后仍正常完成的项不应判失败；同一关键词伴随终止、没有后续成功事件时也不能忽略。
- 分别报告“工具是否报告成功”和“启动是否已验证”。发送/写入应答不是独立读回；启动确认注明来自上电后的日志、登录验证还是用户反馈。X5 仅更新启动程序时，验证的是预期启动程序及其交接，不能据此宣称系统镜像已更新。
- 同类 S100 现象按需阅读 [XBurn 1.2.1 成功基准](references/s100-success.md)。其中的 PID、耗时和分片数不是 S600、X5 或新版工具的通过条件。

## Safety

只读诊断不写板。实际擦除、重分区、重刷前，确认目标板、介质、镜像、范围、备份/恢复路径及对应授权。写入中不拔线、断电或切换拨码；仅在匹配板型流程的握手提示或安全停止后操作。不跨型号套用拨码、波特率、安全类型或降级启动固件。对外整理案例时只保留必要日志标志，移除机器路径、设备标识和凭据。

Sources: [XBurn 手册](https://developer.d-robotics.cc/xburn_doc/overview)、[S100 烧录](https://d-robotics.github.io/rdk_s_doc/Quick_start/install_os/rdk_s100/burn/)、[S600 烧录](https://d-robotics.github.io/rdk_s_doc/Quick_start/install_os/rdk_s600/burn/)、[X5 系统镜像](https://developer.d-robotics.cc/rdk_x_doc/Quick_start/system-burn/burn-sd-card)、[X5 miniboot](https://developer.d-robotics.cc/rdk_x_doc/en/Quick_start/system-burn/upgrade-miniboot)。
