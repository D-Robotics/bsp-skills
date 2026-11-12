# 准备并核对升级盘

以下针对 [X5 芯片手册 2.0.0 的 U 盘升级格式](https://developer.d-robotics.cc/sdk_doc/versions/2.0.0/en/linux_development/system_component_development/42-Auto_update_system_by_USB_storage.html)。先确认板端固件与该格式相符。目录和文件命名相符不能证明镜像适配硬件。

1. 在 Linux 制盘机上用 `lsblk -o NAME,PATH,TRAN,MODEL,SIZE,FSTYPE,MOUNTPOINT` 识别可移除介质，`findmnt -M <实际挂载点>` 检查挂载状态。不能只根据 `vfat` 这个名称推断 FAT32；可用 `blkid -p <已确认的分区>` 核对 FAT 版本。
2. U 盘根目录创建一个空的 `update_img` 目录。如果已存在，先列出文件，不把新镜像和旧升级包混放。为一个目标准备一份原始整盘镜像；源盘容量要足以容纳全部数据。
3. 单文件不得超过 FAT32 的 4 GiB 减 1 字节。原始整镜像太大时，在有空间的主机上新建空的临时目录，进入后再分片。下面是 eMMC 示例（源文件绝对路径需替换）：

   ```sh
   split -b 3500M -d -a 2 -- /path/to/emmc_disk.img emmc_disk.img.
   ```

   将生成的分片复制到 U 盘的 `update_img/`，不要同时复制整镜像。公开手册限制为最多 32 个分片，编号从零开始、连续且唯一；仅原始文件能用这条分片路径，不切分 sparse 镜像。
4. 从技能目录运行示例检查命令，替换挂载点和原镜像路径。源镜像应独立于 U 盘副本：

   ```sh
   python3 scripts/check_media.py --root /mnt/usb --target emmc --source-image /path/to/emmc_disk.img
   ```

   工具按数字顺序流式比对分片，无需在本机拼出第二份大镜像。省略原镜像时仅检查布局；连续编号不能排除最后一个分片丢失。原镜像有发布方校验值时，应另外核对来源校验值。
5. 关闭仍占用文件的程序，同步并卸载已确认的 U 盘。板端运行中观察串口提供的写入结果；固件更新后查版本，系统更新后再查实际启动介质。检查脚本不接触板端，也不验证真实升级效果。
