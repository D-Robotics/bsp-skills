# D-Robotics BSP Skills

[![License](https://img.shields.io/badge/license-Apache--2.0%20%2F%20CC--BY--4.0-green.svg)](#license)

> 中文 | [English](README.md)

面向 D-Robotics RDK 板卡的 BSP（板级支持包）开发 Skills。每个 Skill 是一组可移植的指令文件，教 AI 编程助手在开发主机上完成 RDK 系统构建——交叉编译环境、源码同步、整机镜像、内核/设备树/驱动模块、`hobot-*` deb 包、bootloader/miniboot、Ubuntu 根文件系统定制——全部基于官方构建仓库，而非模型记忆。

| Skill | 做什么 |
|---|---|
| `bsp-env-setup` | 搭建主机交叉编译环境（Ubuntu、工具链、repo、SSH key） |
| `bsp-source-sync` | repo/manifest 同步 RDK Linux 源码（X5: `x5-manifest`，X3: `manifest`） |
| `bsp-image-build` | `pack_image.sh` 构建系统镜像（desktop/server × beta/release） |
| `bsp-kernel-build` | 编译内核、设备树、驱动模块（`mk_kernel.sh`） |
| `bsp-deb-build` | 重编 `hobot-*` debian 包（`mk_debs.sh`） |
| `bsp-bootloader-build` | 编译 miniboot（`xbuild.sh lunch`，X5 已文档化） |
| `bsp-rootfs-custom` | 制作与定制 Ubuntu 根文件系统（samplefs、debootstrap/chroot） |
| `bsp-s-series` | S100/S600 BSP 源码获取与构建入口 |

## 支持的平台

| 系列 | 源码入口 | 构建仓库 |
|---|---|---|
| RDK X5 | [`x5-manifest`](https://github.com/D-Robotics/x5-manifest) | [`x5-rdk-gen`](https://github.com/D-Robotics/x5-rdk-gen)（v3.5.0） |
| RDK X3 | [`manifest`](https://github.com/D-Robotics/manifest) | [`rdk-gen`](https://github.com/D-Robotics/rdk-gen)（v3.0.3） |
| RDK S100 / S600 | [developer.d-robotics.cc/resource](https://developer.d-robotics.cc/resource) 下载中心 | 官方文档 [rdk_s_doc §7.6](https://developer.d-robotics.cc/rdk_s_doc/Advanced_development/rdk_gen) |

X 系列与 S 系列 BSP 严格隔离：skill 1–7 覆盖 X3/X5 主机侧开发，S 系列仅由 `bsp-s-series` 负责。镜像烧录属于设备侧——请使用设备技能包中的 `rdk-board-knowledge`（S 系列 xburn DFU/Fastboot）或官方安装文档。

## 安装

### 从 Hub 安装（推荐）

```bash
npx skills add d-robotics/rdk-skills
```

在目录中选择需要的 `bsp-*` skill。

### 直接克隆本仓库

```bash
git clone https://github.com/D-Robotics/bsp-skills.git
cd bsp-skills
./install.sh                          # 默认 symlink 到 ~/.claude/skills 等
./install.sh --copy                   # 复制而非 symlink
./install.sh --targets claude,cursor  # 只装到指定 Agent
```

## Skill 结构

每个 skill 遵循 L2 治理标准：

```
skills/<skill-name>/
├── SKILL.md          # 入口：YAML frontmatter + Purpose/When to use/Instructions/Safety
├── skill-card.md     # 治理卡片：owner、license、用例、已知风险
└── evals/tasks.yaml  # 五维评测任务
```

所有命令与路径均出自官方构建仓库（`x5-rdk-gen` README v3.5.0、`rdk-gen` README v3.0.3）或官方文档；每个 SKILL.md 带 `Sources:` 行标注出处。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交需 DCO 签名（`git commit -s`）。

## 路线图

- S 系列构建流程细节（待下载中心 S 系列 BSP 源码包就位）
- X3 bootloader/miniboot 构建步骤
- 板卡烧录工作流 skill（待与设备技能包裁定重叠边界）

## 许可证

源码采用 [Apache-2.0](LICENSE-APACHE)，文档与 Skill 内容采用 [CC-BY-4.0](LICENSE-CC-BY-4.0)。
