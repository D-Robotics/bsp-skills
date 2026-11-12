# 按板型选择排查入口

先看 XBurn 实际执行的是哪一项，再选下列分支。硬件修订、下载包和工具版本有差异时，以该板对应版本的产品手册为准。以下为官方手册流程，核对日期 2026-11-12；只有单独记录的 S100 案例有本次实板结果。

## S100：区分 USB 引导、NOR 启动区与 eMMC

用 [S100 烧录准备](https://d-robotics.github.io/rdk_s_doc/Quick_start/install_os/rdk_s100/preparation/) 核对主机驱动、数据口及镜像包，再看[烧录步骤](https://d-robotics.github.io/rdk_s_doc/Quick_start/install_os/rdk_s100/burn/)。空板恢复时确认下载模式，再等 DFU 下载与设备重新枚举。非空板直接 Fastboot 则检查 U-Boot 和主机识别；USB 下载没有配置串口不等于失败。

核对失败项：`miniboot_flash` 对应 NOR；`miniboot_emmc` 和系统镜像针对 eMMC。若前者完成而后者失败，报告具体未写完的项。一次写入过程可见[成功基准](s100-success.md)，不要照搬它的时间阈值。

## S600：分清下载模式和启动盘选择

[准备](https://d-robotics.github.io/rdk_s_doc/Quick_start/install_os/rdk_s600/preparation/)与[烧录步骤](https://d-robotics.github.io/rdk_s_doc/Quick_start/install_os/rdk_s600/burn/)分别说明镜像目录、USB 数据连接和板上开关。恢复空板时先按硬件版本观察 DFU 指示：V0P1 的 SW2 使用跳线帽，V0P2/V1P0 看对应拨码图。D61 亮是进入下载模式的线索，还要看主机实际枚举。能进入 U-Boot 并直接更新时按 Fastboot 分支分析。

对于“烧录成功、重启还是旧版本”：先对照工具记录的写入介质、镜像是给 UFS 还是 NVMe，以及 SW8 选择的启动盘。默认 UFS 镜像不能因为工具选择了 NVMe 就当作 NVMe 镜像。再从串口启动日志或已启动系统的根挂载来源确认实际介质。NOR 中的 `miniboot_flash` 和目标盘中的系统区域要分别核对；只写共享启动区不能证明目标系统盘更新。

## X5：先问写的是启动固件还是系统

- **NAND 启动固件**：按[升级 miniboot](https://developer.d-robotics.cc/rdk_x_doc/en/Quick_start/system-burn/upgrade-miniboot)核对固件包和连接。Serial+USB 的 XModem 恢复先过调试串口握手，再经 USB 传输。标准 X5 文档的串口设置是 115200，Module 的设置是 921600；先识别型号再判断。若 XModem 已完成却未发现 Fastboot，不应优先反复调整串口参数。能进入 U-Boot 并选择 USB Fastboot 时，确认板端已进入 Fastboot，再检查主机枚举。
- **Ubuntu 系统镜像**：按[X5 系统镜像指南](https://developer.d-robotics.cc/rdk_x_doc/Quick_start/system-burn/burn-sd-card)区分标准板的 Micro SD、Module 的 Micro SD 或 eMMC，以及用 XBurn 在板下载还是读卡器写盘。XBurn 检查解压后的系统镜像和实际目标；Module 写 eMMC 时还要核对 SD 卡是否已取出。若只是 Rufus/RDK Studio 读卡器写盘，查卡、读卡器和选中的磁盘，不去排查板上 DFU。
- **验证对象**：启动固件升级核对 U-Boot 版本与引导交接；系统镜像更新再核对启动介质、登录和系统版本。不要把某个芯片 SDK 或定制载板支持的模式直接推广到标准开发板。

连接或主机枚举有疑问时，参见 [XBurn 连接方式](https://developer.d-robotics.cc/xburn_doc/basics/download-modes)和[驱动排查](https://developer.d-robotics.cc/xburn_doc/troubleshooting/serial-driver)。
