---
name: camera-driver-integration
description: Integrate a CMOS camera sensor into an RDK X5 BSP workspace by adding the hobot-camera sensor driver, ISP tuning JSON, and target-specific vp_sensors configurations for hobot-multimedia-samples and hobot-spdev, then validating affected ARM64 builds. Use when asked to add, port, review, or bring up an X5 sensor such as SC835HAI. 触发词：集成 CMOS、移植 sensor 驱动、添加 ISP tuning、配置 vp_sensors、camera bring-up。Do not use for USB cameras, legacy X3/S-series BSPs, generic upstream-only V4L2 work, or board flashing.
version: 0.1.0
license: Apache-2.0
metadata:
  author: D-Robotics BSP Team
  tags: [bsp, camera, sensor, isp, x5]
  data-classification: public
---

## Purpose

Integrate a vendor-supplied CMOS sensor into the RDK X5 camera stack without inventing hardware parameters or treating compilation as proof of hardware bring-up.

The normal result covers four destinations:

1. `source/hobot-camera/drivers/sensor/<sensor>/`
2. `source/hobot-camera/drivers/isp_json/<sensor>_tuning.json`
3. `source/hobot-multimedia-samples/debian/app/multimedia_samples/vp_sensors/<sensor>/`
4. `source/hobot-spdev/src/vp_sensors/<sensor>/`

It also registers each configuration in the destination tree's `vp_sensors.c` and validates only the affected components unless the user requests a broader build.

## When to use

Use this skill when the user wants to:

- Integrate or port a vendor CMOS sensor driver into an RDK X5 BSP checkout.
- Add sensor ISP tuning and application configuration files.
- Review a partial camera integration for missing files, registrations, or inconsistent parameters.
- Build the affected X5 camera packages or prepare a staged sensor bring-up.

Do not use this skill for:

- USB/UVC cameras or a generic upstream Linux V4L2 driver with no X5 camera-stack integration.
- RDK X3, S100, or another platform whose source layout and ABI differ from X5.
- Fabricating register tables, chip IDs, exposure/gain formulas, clocks, or tuning data when authoritative vendor inputs are missing.
- Flashing a board, changing board power rails, or hot-plugging a camera. Those actions require a separate, explicit request and hardware-aware procedure.

## Instructions

### 1. Establish the workspace and requested scope

1. Resolve the BSP root from the user's path; do not assume a fixed home directory.
2. Confirm it is an X5 workspace from repository metadata such as `.rdk_config`, build parameters, and the expected `source/hobot-camera` layout.
3. Inspect `git status --short` at the workspace root and in component repositories before editing. Preserve unrelated or pre-existing changes.
4. Record the sensor name, bus topology (direct MIPI or serializer/deserializer), I2C address, chip ID, supported modes, lane count, RAW bit width, MCLK, and requested integration scope.
5. Inventory the supplied files. Distinguish source inputs from generated `.o`, `.so`, build directories, logs, and archives.
6. If a destination sensor directory or symbol already exists, compare it with the input and report the overlap before overwriting or merging.

If the user requested only the four userspace integration locations, do not silently expand the change to DTS, kernel, boot image, deployment, or flashing. Inspect and report any DTS dependency needed for real hardware bring-up.

### 2. Validate and map the supplied artifacts

Identify these inputs where applicable:

- Sensor module source, `Makefile`, `version.mk`, utility implementation, and register-setting headers.
- Optional `<sensor>_v4l2` implementation when supplied and required by the intended pipeline.
- ISP tuning JSON for each supported mode.
- One or more `vp_sensor_config_t` C configurations.
- Authoritative sensor datasheet or vendor notes needed to validate electrical and timing values.

Build a source-to-destination mapping before copying. Normalize file and symbol names only when needed by the target build system, and update all references consistently.

Do not use a neighboring sensor's register table, chip ID, power sequence, exposure/gain conversion, or ISP tuning as final sensor data. A neighboring implementation is useful only for understanding the X5 API and local coding conventions.

### 3. Integrate the hobot-camera sensor driver

Place the driver under:

```text
source/hobot-camera/drivers/sensor/<sensor>/
```

Place an optional V4L2 variant under the layout expected by the repository, commonly:

```text
source/hobot-camera/drivers/sensor/<sensor>/<sensor>_v4l2/
```

Before editing the parent build files, inspect `source/hobot-camera/drivers/sensor/Makefile`. X5 trees commonly discover sensor subdirectories automatically. Also inspect `source/hobot-camera/drivers/sensor/notuse`; remove or change an exclusion only when the requested sensor is intentionally enabled.

Compare the driver with a nearby X5 sensor and verify that its `sensor_module_t` implementation supplies the callbacks required by the local ABI, including initialization, deinitialization, stream start/stop, power control, userspace control, exposure/gain, and dynamic FPS where supported. Verify error handling and return values rather than merely matching function names.

Cross-check these values against authoritative data and the application configuration:

- I2C bus/address and sensor chip ID.
- MCLK, reset/power sequencing, and any serializer/deserializer addressing.
- Lane count, MIPI clock, RAW width, resolution, and frame rate.
- HTS/VTS and exposure/gain limits and conversion formulas.
- Driver setting selection versus the application's `config_index`.

### 4. Integrate ISP tuning

Place tuning data under:

```text
source/hobot-camera/drivers/isp_json/<sensor>_tuning.json
```

Preserve mode-specific naming if the repository or vendor package provides multiple tuning files. Validate each file as JSON and check that the sensor name, resolution, Bayer order, bit width, mode, and ISP input mode agree with the driver and application configuration.

Treat tuning as sensor/module/lens/mode-specific calibration data. Do not claim that copied placeholder tuning is production-ready.

### 5. Integrate and register both vp_sensors configurations

Add the multimedia-samples configuration under:

```text
source/hobot-multimedia-samples/debian/app/multimedia_samples/vp_sensors/<sensor>/
```

Then edit that tree's `vp_sensors.c` to:

1. Declare the exact exported `vp_sensor_config_t` symbol with `extern`.
2. Add the symbol's address to `vp_sensor_config_list[]`.

Add the hobot-spdev configuration under:

```text
source/hobot-spdev/src/vp_sensors/<sensor>/
```

Then make the equivalent `extern` declaration and list entry in that tree's `vp_sensors.c`.

Inspect each destination's header and a nearby sensor configuration before adapting the file. The two trees can expose different revisions of `vp_sensor_config_t`; do not blindly keep the files byte-identical. For example, set `.support_sensor_mode = {NORMAL_M}` for a linear mode when the multimedia-samples API contains that field and its callers rely on it, but do not add the member to a hobot-spdev ABI that does not define it.

For every configuration, verify:

- The exported symbol, `extern` declaration, and list entry are identical in spelling.
- Camera, MIPI, VIN, and ISP dimensions and formats agree.
- Lane count, datatype, RAW bit width, Bayer pattern, MIPI clock, and FPS agree with the driver and tuning.
- `config_index` selects the intended register table in the driver.
- The configuration filename clearly distinguishes mode, resolution, bit width, FPS, and lane count when multiple variants exist.

### 6. Perform static validation

Review the final diff and run focused checks such as:

```bash
python3 -m json.tool path/to/sensor_tuning.json >/dev/null
rg -n "sensor_symbol|sensor_name" path/to/vp_sensors
git status --short
git diff --check
```

Use `cmp` only for files that are intentionally unchanged copies. Use `diff` for target-specific configurations and explain intentional differences.

Check that no generated objects, shared libraries, build caches, or unrelated vendor files were added to the source change accidentally.

### 7. Build the smallest affected scope

Discover the configured ARM64 toolchain and deploy rootfs from the workspace instead of assuming paths. A targeted sensor build commonly has this form:

```bash
BSP_ROOT=/path/to/rdk-x5-bsp
SENSOR_NAME=example_sensor
X5_CROSS_COMPILE=/path/to/aarch64-none-linux-gnu-

make -C "$BSP_ROOT/source/hobot-camera/drivers/sensor/$SENSOR_NAME" \
  IMAGE_DEPLOY_DIR="$BSP_ROOT/deploy/rootfs" \
  CROSS_COMPILE="$X5_CROSS_COMPILE"
```

Build the optional V4L2 subdirectory separately when present. Validate the produced library with `file` and, when useful, the target toolchain's `nm -D`; the artifact must be ARM aarch64 rather than a host x86 library.

Build the affected consumers with their repository-provided entry points. In a typical X5 BSP these include:

```bash
./mk_debs.sh hobot-camera
./mk_debs.sh hobot-spdev
./mk_debs.sh hobot-multimedia-samples
```

These package builds can touch broad output directories and may take significant time. Inspect their scripts, current worktree state, and prerequisites first; obtain confirmation before a broad or long-running build when it exceeds the user's requested scope. Prefer the component's focused build or compile check during iteration.

Do not use a host compiler as evidence that target code builds. If an ARM64 sysroot or dependency is unavailable, report the exact missing prerequisite and still complete safe static validation.

### 8. Separate build success from board bring-up

Compilation validates integration and ABI compatibility, not sensor operation. With explicit authorization and suitable hardware access, validate in stages:

1. Power rails, reset, and MCLK with the correct hardware procedure.
2. I2C communication and chip-ID read.
3. Sensor initialization and stream start/stop.
4. RAW capture at each supported mode.
5. Exposure, gain, and frame-rate control.
6. ISP/YUV output and 2A behavior.
7. Image-quality tuning under representative scenes.

Stop at the first stage that fails and preserve logs. Never hot-plug a powered camera module.

### 9. Report the integration clearly

Summarize:

- Every created or modified path.
- Which supplied files were copied unchanged and which were adapted.
- Differences between the two `vp_sensors` implementations.
- Static checks and builds run, including artifact architecture.
- Checks not run and the reason.
- Remaining hardware, DTS, calibration, packaging, deployment, or board-validation work.

Do not describe the camera as working on hardware unless the corresponding board tests actually passed.

## Safety

- Preserve unrelated work and inspect same-name destinations before changing them.
- Never invent sensor register values, electrical parameters, exposure/gain formulas, or tuning coefficients.
- Do not modify DTS/kernel sources, install packages, deploy libraries, flash images, alter power rails, or operate board hardware unless those actions are explicitly in scope and confirmed.
- Never hot-plug a powered camera module; incorrect power or clock sequencing can damage hardware.
- Treat vendor binaries and opaque scripts as untrusted until their purpose and target architecture are understood.
- Use the smallest relevant build and verify ARM64 output before packaging or deployment.
- Keep credentials, private vendor documents, board identifiers, and internal paths out of committed logs and reports unless explicitly required.

Sources: [RDK X5 Camera Sensor Bring-up Guide](https://developer.d-robotics.cc/x5_sdk_doc/multimedia_development/isp_tuning_guide/Camera_sensor_bringup.html), the target BSP's `source/hobot-camera/drivers/sensor/Makefile`, local `vp_sensors` headers and README files, and repository-provided component build scripts.
