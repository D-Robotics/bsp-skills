# camera-driver-integration

- Owner: D-Robotics BSP Team
- License: Apache-2.0
- Kind: workflow
- Risk level: high
- Platforms: RDK X5

## Use case

Use this skill to integrate a vendor CMOS sensor into the RDK X5 camera stack. It maps and adapts the sensor driver, ISP tuning JSON, and both `vp_sensors` configuration variants, registers their exported symbols, and validates the smallest affected ARM64 build scope.

The skill is designed for both a fresh integration and a review of an existing partial integration. It keeps host-side source/build validation separate from board deployment and physical sensor bring-up.

## Known risks

- Incorrect power sequencing, clocks, voltages, I2C addresses, or register tables can prevent startup or damage hardware.
- The multimedia-samples and hobot-spdev trees may use different `vp_sensor_config_t` revisions; blindly copying one configuration into both can cause compile failures or subtle runtime behavior.
- A mismatched `config_index`, MIPI lane count, RAW width, Bayer order, timing, or tuning mode can produce no image or corrupted output.
- Host compilation, even when successful, does not prove I2C communication, streaming, image quality, or hardware stability.
- Full package builds may modify broad deploy/output directories and expose unrelated dirty-tree changes.
- Vendor tuning and register data may be confidential or redistribution-restricted; confirm its provenance and license before committing it.

Sources: [RDK X5 Camera Sensor Bring-up Guide](https://developer.d-robotics.cc/x5_sdk_doc/multimedia_development/isp_tuning_guide/Camera_sensor_bringup.html) and the build/API definitions in the target RDK X5 BSP checkout.
