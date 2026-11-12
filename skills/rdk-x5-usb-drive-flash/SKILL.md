---
name: rdk-x5-usb-drive-flash
description: 为支持 X5 芯片手册 2.0.0 USB 升级流程的 RDK X5 准备 FAT32 升级盘，检查 SD、eMMC 或 SPI NAND 原始整盘镜像，排查板端 U-Boot 未识别镜像、分片不完整与更新后版本不符。用于 U 盘作为镜像来源的升级，不用于 PC 读卡器写盘或 XBurn 下载。
version: 1.0.0
license: Apache-2.0
metadata:
  tags: [rdk, x5, u-boot, usb-drive, fat32]
  data-classification: public
---

# RDK X5 U 盘升级

## Purpose

让使用者能区分三个结果：升级盘文件是否正确、U-Boot 是否写完指定目标、板卡是否从预期介质启动。适用依据是 [X5 芯片用户手册 2.0.0 §4.4.10](https://developer.d-robotics.cc/sdk_doc/versions/2.0.0/en/linux_development/system_component_development/42-Auto_update_system_by_USB_storage.html)；芯片手册列出能力，不代表每块开发板的出厂固件都具备它。

## When to use

- U 盘插在 X5 板上，由 U-Boot 从 U 盘读取镜像并更新板上存储。
- 若板上存储经 USB 映射成 PC 的可移动磁盘，或 SD 卡在 PC 读卡器中，由 PC 写盘，走 [RDK 系统镜像流程](https://developer.d-robotics.cc/rdk_x_doc/Quick_start/system-burn/burn-sd-card)。PC 端正在运行 XBurn 则按 XBurn 排查。

## Instructions

1. **确认板端能力。** 记录板型、U-Boot 构建版本、目标介质及镜像来源。查看 U-Boot 的 `help` 列表是否包含 `usbupdate`，并核对该构建对应的公开手册。不要执行写入命令来测试它是否存在。若手册版本或板端能力不匹配，先解决适用性问题。
2. **确认盘的角色。** U 盘存放源文件，板上的 SD、eMMC 或 SPI NAND 是写入目标。用 `lsblk`、`findmnt` 检查实际挂载点和设备；核对 FAT32 版本与可用容量。盘已经准备好时不重复格式化。
3. **只为一个目标准备原始整盘镜像。** 在 U 盘根目录使用 `update_img/`。按目标选 `sd_disk.img`、`emmc_disk.img` 或 `nand_disk.img`，先确认硬件上确有该介质。不要通过改文件名把另一种格式或另一块板的镜像变成目标镜像。手册还列有稀疏镜像和分区更新，本技能的检查工具只处理以上三种原始整盘镜像。
4. **检查再移动 U 盘。** 按[制盘与核验](references/prepare-and-verify.md)复制整镜像或分片；对照可信原镜像检查内容。检查工具 `scripts/check_media.py` 不写盘。若有混放文件、编号重复或 SHA-256 不同，停止并定位差异。同步、正常卸载后再移动 U 盘。
5. **启动与验证。** 在已确认写入范围后，将准备好的 U 盘插到断电的板上，再上电。此流程由冷启动触发。观察早期串口，区分 USB 枚举、目录扫描、镜像识别、实际写入和完成状态。完成并自动重启后，用正常启动串口、实际根挂载所在介质及预期版本验证结果；更新启动固件时核对固件版本和引导交接。

| 现象 | 下一项检查 |
| --- | --- |
| Linux 能看到 U 盘，启动时没看到升级 | 核对固件能力、启动类型、板端早期 USB 枚举；Linux 挂载不能证明 U-Boot 识别 |
| 能扫描盘，但没有匹配镜像 | 核对目录层级、文件名、是否解压、目标介质和手册版本 |
| 分片写入失败 | 记录最后成功的编号或报错；停写后检查分片总数、顺序、总长度和内容 |
| 写完后仍是旧系统 | 先区分写的是启动固件还是系统盘，再核对实际从哪个介质启动 |

## Safety

制备文件不等于启动写板。格式化、覆盖目标存储前，先核对设备、镜像、备份和已有授权。写入期间不拔盘、断电或更换介质。不要把样例的路径或盘符当作现场设备名。

Sources: [X5 USB Flash Drive Update，2.0.0](https://developer.d-robotics.cc/sdk_doc/versions/2.0.0/en/linux_development/system_component_development/42-Auto_update_system_by_USB_storage.html)；[RDK X5 系统镜像指南](https://developer.d-robotics.cc/rdk_x_doc/Quick_start/system-burn/burn-sd-card)。
