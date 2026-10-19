# Skill Card: bsp-ion-memory

| Field | Value |
|---|---|
| name | bsp-ion-memory |
| owner | D-Robotics BSP Team |
| license | Apache-2.0 |
| kind | workflow |
| riskLevel | medium — boot memory reservations and optional ISP disablement |
| platforms | RDK X5 only |

## Use case

Configure ION memory size for BPU and multimedia through srpi-config, boot config or device tree. The device-tree path confirms the project absolute path, edits x5-memory.dtsi, builds hobot-dtb, then confirms board IP, username, and password before scp. Verify saved versus effective sizes and distinguish ISP CMA reclamation.

## Known risks

- Undersized heaps can break BPU or multimedia workloads even when Linux has free memory.
- Bootloader overrides can replace source DT sizes; verify the running system.
- Disabling ISP CMA may affect remaining consumers and is separate from ION sizing.
- Wrong DTB or reservation ranges can prevent boot; retain backups and a recovery path.
- Board password is session-only. Do not write it into the skill, source tree, or config.
- User-tested zero sizes and RDK addresses are version-specific examples, not universal defaults.

## Sources

- https://developer.d-robotics.cc/x5_sdk_doc_v2.0.0/linux_development/system_component_development/39-ION_Debug_Guide.html
- User-provided RDK X5 boot logs, srpi-config screenshots and x5-memory.dtsi diff.
