# RDK X5：hobot-spdev、显示与浏览器预览

## 适用范围与完成条件

仅 project conf 的 board=rdkx5 时使用。沿用已确认的 sensor 参数、项目根目录、接入位置和板端 IP，不重复索取入口信息。RAW 与 ISP 通过后，继续 spdev 适配、编译安装、vio2display、浏览器预览。用户仅要求 RAW/ISP 时按其范围停止。

分别记录 RAW、ISP、spdev 安装、HDMI 显示、浏览器实时画面的通过/失败/未验证状态。缺显示器、依赖或浏览器访问条件时，报告阻塞项并保留已通过结论，不把尚未验证的阶段宣称通过。

## 1. 适配独立的 sensor 配置表

读取 conf 的 hobot-spdev 仓库下 src/vp_sensors/README.md、vp_sensors.h、vp_sensors.c、src/CMakeLists.txt，以及当前 sensor 在 multimedia samples 中已通过 RAW/ISP 的配置。这里只读取当前 sensor 配置和公共框架，不以兄弟 sensor 配置作为参数来源。此阶段允许复用本次已经验证的配置，不重新提取或猜测 sensor 参数。

hobot-spdev 的 src/vp_sensors 与 multimedia samples 的 sensor 表独立。将已验证的当前 sensor 配置适配到 src/vp_sensors/<sensor>/，依据本仓库结构体字段处理差异；保持 sensor 名、I2C/芯片识别、分辨率、fps、lane、格式、emode、VIN/ISP、calib_lname 与通过版本一致。列出复用来源和差异；不覆盖已存在的同模式、不重复注册。

在 vp_sensors.c 补充 extern 和列表项；核对 CMake 是否收集新增文件。已核实当前版本用 vp_sensors/*/*.c 通配收集，不能无依据另加编译规则。不要将 multimedia samples 的 camera_index 当成 spdev 的索引。

回查 vp_get_sensor_config_by_mipi_host 的芯片探测、候选 I2C 地址、宽高/fps 匹配和 vpp_camera.cpp/sp_vio.cpp 的调用方式，确认目标接入位置会选中本 sensor 的目标模式。若同芯片同宽高有多个模式或当前 API 无法指定目标，先报告实际冲突并决定适配方式，不声称自动探测一定正确。SerDes 还须核实封装层的解串器/link 支持，不能因为底层 RAW 已通过就宣称上层支持。

## 2. 编译、部署、安装

从用户工程根目录依次执行 conf 中的 build_hobot-spdev、build_hobot-sp-samples；按 conf 部署、安装。沿用入口已有授权，不逐步重复确认。此阶段处理源码和板端库，不运行全系统镜像构建。

构建前核对当前 mk_debs.sh 的包分支。已核实 hobot-spdev 会调用 build.sh clean 和 build.sh，打包 output/*.so、头文件和 Python wheels；hobot-sp-samples 在当前版本主要打包样例，vio2display 仍需在板端 make。

推送前对 deploy/deb_pkgs 中候选包读取 dpkg-deb 元数据，选中本次构建的确切版本/架构；多个候选不得通过通配符覆盖成同一个目标名。检查安装退出码、dpkg-query 状态和 ldconfig -p，确认 libspcdev/libhbspdev 实际加载路径。浏览器还要检查当前 python3 的 hobot_vio/libsrcampy 导入，不能仅凭 dpkg 成功认定 Python 环境正常。安装脚本可能调用 pip，依赖失败时报告具体错误。

用 dpkg -L hobot-sp-samples 确认板端路径；conf 路径是当前布局，若不一致先查明版本差异，不猜替代路径。

## 3. vio2display 验证

先检查显示器连接和可用显示模式，确认没有仍占用同一 camera 的 RAW/ISP/Web 进程。仅结束本次启动的进程；已有业务占用则向用户说明冲突。

进入 spdev_display_dir，顺序执行 spdev_display_clean、spdev_display_build、spdev_display_cmd，仅替换已确定的 width/height。当前样例仅支持 -w/-h，通过 sp_open_camera_v2 自动探测，不支持 -s camera_index 或 -m/-l；禁止添加这些参数。

检查 ldd ./vio2display 的依赖，运行时核对目标 sensor/mode、sp_open_camera success、非零显示分辨率、显示启动与绑定返回值及持续日志。程序持续运行等待 q 属正常行为，不能套用 RAW 的 10 秒超时规则。保持运行供观察，用户确认显示器上出现持续更新的目标摄像头画面后输入 q 正常退出。具备可观察显示面的工具时可直接观察；否则明确报告“程序链路通过，屏幕画面待用户确认”。退出码为 0 不能替代图像验收，样例部分失败路径仍可能返回 0。

## 4. 浏览器预览

当前工程提供 hobot-sp-samples/debian/app/pydev_demo/09_web_display_camera_sample。它是 YOLOv5X + WebSocket JPEG 预览，不是无模型的纯视频服务。读取当前样例 README、Python、webservice/conf/nginx.conf 和前端 WebSocket 地址后再运行。

当前 README 限制只接一颗 MIPI camera；不将此结论扩展到已支持任意 SerDes/多路输入。核对实际接入满足限制，否则报告需扩展的接口。依赖包括当前 Python 的 hobot_vio、README requirements、websockets==15.0.1、protobuf==3.20.3、实际模型与类别文件。模型缺失时报告缺失，不能谎称预览完成或擅自下载替代模型。

当前脚本 CameraManager.open_cam 使用 FPS 和两个输出通道 [512,1920] / [512,1072]；这些是模型/编码输出尺寸，不是新 sensor 的原始分辨率。确认其自动探测选中目标 sensor 和模式；已核实 src/python/vpp_python.cpp 的 open_cam 支持 raw_height/raw_width 关键字；按当前签名传入已验证原始宽高，并将 FPS 与已验证模式对齐，保留模型所需输出通道尺寸。部署版本仍须核对该签名，不向不支持的旧绑定强传参数。修改输出尺寸时须同步 NV12/JPEG 编码、16 对齐要求、protobuf 宽高和前处理，不得把全部宽高机械替换为 sensor 原始宽高。若用户只要无推理预览，说明现有依赖并按用户要求另行适配，不能把 YOLO 检测当成 sensor 验收条件。

在板端 web_preview_dir 检查 HTTP/WebSocket 端口占用、nginx 配置和所需依赖。当前配置 HTTP=80，Python WebSocket=8080；复用既有兼容服务，冲突时报告，不停止无关服务。依次在 webservice 内执行 sudo ./sbin/nginx -t -p "$PWD/"，检查通过后按 conf 的 web_start_cmd 启动，再回到样例目录执行 web_preview_cmd。跟踪本次启动的进程和日志；测试结束只清理本次启动的服务，不更改开机启动。

提供 http://<本次板端IP>/。能访问板端网络的浏览器中检查页面、WebSocket 连接和连续 JPEG 帧解码，确认图像持续更新且来自目标 camera。HTTP 200、监听端口或模型加载成功都不等于画面通过。无法打开浏览器时报告服务状态和访问链接，将浏览器画面记为未验证，请用户打开确认。

## 故障边界

RAW/ISP 仍按入口原流程排查；spdev/显示/Web 失败先检查新增表项、运行时选中模式、动态库/Python 路径、显示连接、模型依赖、端口与浏览器连接。修复依据须标注本文件对应阶段及实测证据，不把应用层失败直接归因于 sensor 寄存器，不修改 BLS/AWB/LSC/AEC。编译/安装报错暂停汇报；缺少依据时报告未覆盖，不盲目循环。

> Sources: 已检查服务器 /home/xingshun_cai/rdk-x5-bsp 中 source/hobot-spdev/src/vp_sensors/{README.md,vp_sensors.h,vp_sensors.c}、src/CMakeLists.txt、src/vpp_interface/vpp_camera.cpp、src/clang/sp_vio.cpp、src/python/vpp_python.cpp；mk_debs.sh 的 hobot-spdev/hobot-sp-samples 分支；source/hobot-spdev/debian/DEBIAN/postinst；source/hobot-sp-samples/debian/app/cdev_demo/vio2display/{Makefile,vio2display.c}；debian/app/pydev_demo/09_web_display_camera_sample/{README.md,mipi_camera_web_yolov5x.py,webservice/conf/nginx.conf}。执行时以用户选择的 checkout 核实接口，不能将此核对路径当成固定项目根目录。
