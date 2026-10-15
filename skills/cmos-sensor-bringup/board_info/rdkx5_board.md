# RDK X5 板端硬件映射

> RDK X5（X5 MD：RDK X5 Module + IO 载板）两路 22pin MIPI CSI。来源：X5 芯片用户手册 2.0.0《X5 MD 开发板使用指南》摄像头接口表；`x5-rdk.dtsi` 的 `mipi_host` / `lpwm1` 节点。手册未给出单独的 power/pwd GPIO，本表不填。

| 座子 | mipi_host | lane | i2c bus | reset 引脚 (gpio_oth / sensor reset-gpios) | lpwm trigger | MCLK |
|------|-----------|------|---------|--------------------------------------------|--------------|------|
| CAM1（接口 10） | mipi_host0、mipi_host1 共用 | 4 lane（CSI0&1） | i2c6 | LSIO_GPIO1_06 = GPIO 353 | LSIO_LPWM1_0（lpwm1_ch0，lpwm_chn=4）→ LSIO_SPI3_SCLK | LSIO_SENSOR0_MCLK |
| CAM2（接口 9） | mipi_host2、mipi_host3 共用 | 4 lane（CSI2&3） | i2c4 | LSIO_GPIO1_04 = GPIO 351 | LSIO_LPWM1_1（lpwm1_ch1，lpwm_chn=5）→ LSIO_SPI3_SSN | LSIO_SENSOR1_MCLK |

## 约束

- `x5-rdk.dtsi`：`&lpwm1` 使能 `pinctrl_lpwm1_0`、`pinctrl_lpwm1_1`。mipi_host0 与 mipi_host1 共用一组 MCLK 和 GPIO；mipi_host2 与 mipi_host3 共用另一组。
- MCLK 不由 SoC snrclk 输出。`mipi_host0` / `mipi_host2` 注释为外部有源晶振，节点未配置 `snrclk-idx`。22pin 模组（IMX219、IMX477、OV5647）IO 电平选 3.3V，MCLK 在座子上。22pin 转 24pin 转接板自带 24M 有源晶振，IO 电平选 1.8V，用于对接 SC230AI、SC132gs、IMX415 等 EVB 模组。
- lpwm 物理脚与 `lpwm_chn` 来自 X5 LPWM 映射：LPWM1 ch0 = `pinctrl_lpwm1_0` = LSIO_SPI3_SCLK = lpwm_chn 4；LPWM1 ch1 = `pinctrl_lpwm1_1` = LSIO_SPI3_SSN = lpwm_chn 5。
