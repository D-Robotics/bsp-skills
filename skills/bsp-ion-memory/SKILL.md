---
name: bsp-ion-memory
description: Configure RDK X5 ION memory size for BPU and multimedia through srpi-config, /boot/config.txt, or device tree; verify reservations and allocation usage. Use for ION 内存、ion_reserved_size、ion_carveout_size、ion_cma_size and reclaiming unused ISP memory. The device-tree path confirms the project absolute path, edits x5-memory.dtsi, builds hobot-dtb, then confirms board IP, username, and password before scp deployment. Do not apply X5 settings to X3 or S-series boards.
version: 1.1.0
license: Apache-2.0
metadata:
  author: D-Robotics BSP Team
  tags: [bsp, x5, ion, memory, bpu, multimedia]
  data-classification: public
---

# ION memory

## Purpose

Configure ION memory size for BPU and multimedia on RDK X5. Prepare configuration changes and verify effective reservations without confusing ION capacity with Linux available memory.

## When to use

Use for X5 ION sizing, srpi-config ION presets, boot config overrides, device-tree reservations, or a request to reclaim unused ISP memory. Trigger terms include ION 内存、BPU 内存、多媒体预留内存 and ion_cma_size. Do not apply this workflow to X3 or S-series boards; route kernel compilation to bsp-kernel-build and whole-image assembly to bsp-image-build. Board-side commands here support this memory configuration workflow only, not general flashing or diagnostics.

## Instructions

### Establish the target

Use Chinese unless the user prefers another language. Determine the X5 board, DDR capacity, BSP version, board connection, desired sizes, and whether VIN/ISP, BPU and other multimedia workloads remain in use. Reuse information already supplied. Inspect before changing; if the board is unavailable, produce a concrete configuration or patch without claiming deployment.

Read the board's `/boot/config.txt`, boot log and current heap usage:

```bash
cat /boot/config.txt
dmesg | grep "Reserved ion"
free -m
cat /sys/kernel/debug/ion/heaps/cma_reserved
cat /sys/kernel/debug/ion/heaps/carveout
cat /sys/kernel/debug/ion/heaps/ion_cma
```

If debug nodes are absent, check whether debugfs is mounted and supported before interpreting absence as zero usage. Inspect `/sys/kernel/debug/ion/heaps/all_heap_info` for client/module allocations.

### Interpret sizes correctly

- `ion_reserved_size` → boot log `ion-pool` → heap `cma_reserved`, mainly multimedia.
- `ion_carveout_size` → boot log `ion-carveout` → heap `carveout`, mainly BPU.
- `ion_cma_size` → boot log `ion-cma` → heap `ion_cma`, fallback region.
- The observed srpi-config menu orders sizes as **CMA + reserved + carveout**. Boot log order differs. Check resulting keys rather than relying only on positional labels.
- Hex sizes are bytes; 1 MiB = 0x100000. `0x08000000` = 128 MiB; `0x14000000` = 320 MiB; `0x17E00000` = 382 MiB.
- Heap `heap total size` and heap `total` are decimal bytes, respectively reserved capacity and allocated amount. Client debug output may use hexadecimal; inspect its format.
- Reserved capacity is not actual usage. `free -m` describes Linux-managed memory, not free ION capacity. Do not subtract all ION sizes from an already reported MemTotal or attribute all missing DDR to ION.
- For the documented X5 setup, ION regions are separate reservations unavailable to ordinary malloc/kmalloc/vmalloc. Do not infer generic Linux CMA behavior from the name `ion_cma`; inspect the actual BSP implementation when accounting differs.
- Allocation may fall back between heaps. Not using VIN/ISP alone does not prove carveout or ion_cma can be removed; account for BPU, codec, GPU, display and remaining consumers.

### Choose and perform the change

Prefer the user's chosen method. Preserve unrelated configuration and create a recoverable backup before modifying boot files or deployed DTBs. Present the exact proposed sizes and expected effect. A request to configure memory authorizes configuration edits; obtain reboot or boot-artifact replacement authorization if it is not already provided. Do not reboot merely because a menu prompts for it.

#### Board configuration without rebuilding

On versions offering the menu, run `sudo srpi-config` and choose:

`4 Performance Options` → `P2 ION memory` → desired preset → finish.

Observed presets, in CMA + reserved + carveout order:

```text
128MB+320MB+320MB
192MB+384MB+384MB
256MB+512MB+512MB
320MB+640MB+640MB
512MB+1024MB+1024MB
```

Availability depends on version and board memory. Inspect the installed tool if its choices differ.

For custom sizes, edit the existing matching entries in `/boot/config.txt`, preserving other keys and avoiding duplicate conflicting entries. This known configuration reserves 768 MiB total:

```ini
ion=ion_cma_size=0x08000000
ion=ion_reserved_size=0x14000000
ion=ion_carveout_size=0x14000000
```

The user's tested reduction retains only reserved 320 MiB:

```ini
ion=ion_reserved_size=0x14000000
ion=ion_carveout_size=0x0
ion=ion_cma_size=0x0
```

It reduces ION reservation by 448 MiB relative to the 768 MiB example. Use it only when remaining workloads fit the surviving heap; do not describe it as a universal setting for systems without cameras. Changes take effect after reboot, not immediately after saving.

#### Device tree / BSP integration

Use this path when the user chooses a device-tree change. It does not replace the `/boot/config.txt` method.

Ask in plain text and wait. Do not infer these from the workspace, another skill, or an earlier board:

1. 工程绝对路径. Missing this stops the path. Reuse a path the user already gave in this request.
2. After `hobot-dtb` is built, and before any copy: 开发板 IP、用户名、密码. All three are required. Reuse values the user already gave in this request.

Resolve `arch/arm64/boot/dts/hobot/x5-memory.dtsi` only under the confirmed project. The usual X5 layout is `<project>/source/kernel/arch/arm64/boot/dts/hobot/x5-memory.dtsi`. If that exact file is absent, search only inside the confirmed project. Stop on zero matches or more than one match. Edit that file only.

Inspect the board DTS includes, DDR variant selection and bootloader fixups. Determine the effective nodes before editing: variants may use `_rdk`, `_1g`, `_2g`, or `_ge4g`. Do not blindly modify every variant or assume `status = "disabled"` in source proves a region is unused at runtime. Check whether `/boot/config.txt` or bootloader code overwrites DT settings.

For the user's supplied RDK layout, size is the final cell of the four-cell `reg` value:

```dts
/* ion_carveout_rdk@B8100000: 0 MiB */
reg = <0x0 0xB8100000 0x0 0x0>;

/* ion_cma_rdk@CC100000: 0 MiB */
reg = <0x0 0xCC100000 0x0 0x0>;
```

These are fragments for the appropriate existing nodes, not complete replacement nodes. Keep size comments consistent. Check range overlap, address-cell format, DDR boundaries and bootloader alignment requirements when changing bases or enlarging regions. Zero-size support is version-dependent; use the tested boot configuration and runtime verification rather than assuming any reserved-memory driver accepts it.

Compile `hobot-dtb` from the confirmed project root, the directory that contains `mk_debs.sh`:

```bash
./mk_debs.sh hobot-dtb
```

The package lands in `deploy/deb_pkgs/hobot-dtb_*_arm64.deb`. Kernel artifacts must already exist. If they do not, stop and use `bsp-kernel-build` for that prerequisite, then return here and run `./mk_debs.sh hobot-dtb`. Do not invent another package name or build flag. Identify the single deb from this build before copying.

Back up the board's current DTB or installed `hobot-dtb` and keep a recovery path. Ping the confirmed IP. If it is unreachable, ask for a corrected IP and do not copy.

After the user authorizes boot-artifact replacement, copy that exact deb and install it:

```bash
scp <exact-deb> <user>@<ip>:/tmp/hobot-dtb_arm64.deb
ssh <user>@<ip> 'sudo dpkg -i /tmp/hobot-dtb_arm64.deb'
```

Use the confirmed username and password only for this session. Do not write the password into this skill, the BSP tree, or a config file. Reboot only with separate authorization, then continue at Verify and report. A successful copy or package install shows the package was delivered, not that the new DTB is the one loaded.

#### Release unused ISP-specific memory separately

ION settings do not directly disable ISP or its separate CMA reservation. The user's patch additionally disables `isp_cma` and `&isp`:

```dts
/* Add within the existing isp_cma node; retain other properties. */
status = "disabled";

/* Merge into the existing &isp override. */
&isp {
    memory-region = <&isp_cma>;
    status = "disabled";
};
```

The supplied isp_cma region starts at `0x88000000` and has size `0x17E00000` (382 MiB). Inspect the current tree before using those values. Check consumers of `isp_cma` and camera services before disabling it. The supplied patch does not explicitly disable VIN; do not claim that it does.

Only if all original reservations were active could removing 448 MiB of ION plus 382 MiB of ISP CMA nominally reclaim 830 MiB. Treat this as a conditional estimate; determine actual Linux memory gain after reboot.

### Verify and report

After an authorized reboot, repeat the baseline reads and compare each requested size to the boot log and heap capacity. A zero-sized region may be logged as size 0 or absent depending on version; investigate errors and effective DT before concluding success. A config file alone proves the setting was saved, not applied.

Run the remaining representative BPU/multimedia workload and check allocation failures, fallback pressure, and peak heap usage. Do not claim sufficient memory solely from idle measurements. If boot or workloads fail, restore the backed-up config/DTB through the established recovery path.

Report requested versus actual reservations, Linux MemTotal/available changes, workload verification, and any pending reboot/deployment. Keep theoretical reclamation distinct from measured gain.

## Safety

- Preserve unrelated boot settings and back up the exact configuration or DTB before mutation.
- On the device-tree path, confirm the project absolute path before editing `x5-memory.dtsi`, build `hobot-dtb`, then confirm board IP, username, and password before `scp`.
- Use the board password only to authenticate that session. Never store it in the skill, source tree, or config.
- Use existing authorization; obtain missing authorization for board reboot or boot artifact replacement immediately before that action.
- Do not infer that unused VIN/ISP means BPU, codec, GPU or display heaps can be zeroed.
- Keep ISP CMA release separate from the three ION settings, and retain a recovery path.
- Never claim deployment or successful reboot verification from a configuration edit alone.

## References

- User-provided X5 guide: http://10.64.66.11:8090/linux_development/system_component_development/39-ION_Debug_Guide.html
- Public X5 guide: https://developer.d-robotics.cc/x5_sdk_doc_v2.0.0/linux_development/system_component_development/39-ION_Debug_Guide.html

Use the matching BSP source as authority for bootloader overrides and version-specific behavior. The example sizes and zero-size configuration above come from the user's board logs and screenshots; they are not defaults for every X5 product.

> Sources: Official X5 Chip User Manual 2.0.0, §4.4.6 ION System Debugging Guide (public URL above). The /boot/config.txt keys, srpi-config presets, RDK node fragments and zero-size behavior are additional user-provided board evidence; verify them against the selected checkout before reuse.
