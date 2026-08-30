# D-Robotics BSP Skills

[![License](https://img.shields.io/badge/license-Apache--2.0%20%2F%20CC--BY--4.0-green.svg)](#license)

> English | [中文](README_cn.md)

BSP (Board Support Package) development skills for D-Robotics RDK boards. Each skill is a portable instruction set that teaches AI coding agents how to build the RDK system on a development host — cross-compilation environment, source sync, full system images, kernel/DTB/driver modules, `hobot-*` deb packages, bootloader/miniboot, and Ubuntu rootfs customization — grounded in the official build repos, not model memory.

Current BSP release: **v1.0.0**.

| Skill | What it does |
|---|---|
| `bsp-env-setup` | Prepare the host cross-compilation environment (Ubuntu, toolchain, repo, SSH key) |
| `bsp-source-sync` | Sync RDK Linux source via repo/manifest (X5: `x5-manifest`, X3: `manifest`) |
| `bsp-image-build` | Build system images with `pack_image.sh` (desktop/server × beta/release) |
| `bsp-kernel-build` | Build kernel, device tree, and driver modules (`mk_kernel.sh`) |
| `bsp-deb-build` | Rebuild `hobot-*` debian packages (`mk_debs.sh`) |
| `bsp-bootloader-build` | Build miniboot (`xbuild.sh lunch`, X5 documented) |
| `bsp-rootfs-custom` | Make and customize the Ubuntu root filesystem (samplefs, debootstrap/chroot) |
| `bsp-s-series` | S100/S600 BSP source acquisition and build entry points |

## Supported platforms

| Series | Source repo / entry | Build repo |
|---|---|---|
| RDK X5 | [`x5-manifest`](https://github.com/D-Robotics/x5-manifest) | [`x5-rdk-gen`](https://github.com/D-Robotics/x5-rdk-gen) (v3.5.0) |
| RDK X3 | [`manifest`](https://github.com/D-Robotics/manifest) | [`rdk-gen`](https://github.com/D-Robotics/rdk-gen) (v3.0.3) |
| RDK S100 / S600 | [developer.d-robotics.cc/resource](https://developer.d-robotics.cc/resource) download center | documented in [rdk_s_doc §7.6](https://developer.d-robotics.cc/rdk_s_doc/Advanced_development/rdk_gen) |

X-series and S-series BSP are strictly isolated: skills 1–7 cover X3/X5 host-side development; S-series lives in `bsp-s-series` only. Flashing built images onto boards is device-side territory — use `rdk-board-knowledge` from the RDK Device Skills pack (S-series xburn DFU/Fastboot) or the official install docs.

## Installation

### From the Hub (recommended)

```bash
npx skills add d-robotics/rdk-skills
```

Pick the `bsp-*` skills you need from the catalog.

### From this repo directly

```bash
git clone https://github.com/D-Robotics/bsp-skills.git
cd bsp-skills
./install.sh                          # default: symlink into ~/.claude/skills etc.
./install.sh --copy                   # copy instead of symlink
./install.sh --targets claude,cursor  # specific agents only
```

## Skill structure

Each skill follows the L2 governance standard:

```
skills/<skill-name>/
├── SKILL.md          # entry point: YAML frontmatter + Purpose/When to use/Instructions/Safety
├── skill-card.md     # governance card: owner, license, use case, known risks
└── evals/tasks.yaml  # five-dimension evaluation tasks
```

Every command and path in these skills is quoted from the official build repos (`x5-rdk-gen` README v3.5.0, `rdk-gen` README v3.0.3) or the official documentation; each SKILL.md carries a `Sources:` line for provenance.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Commits must be DCO signed-off (`git commit -s`).

## Roadmap

- S-series build flow details (pending S-series BSP source package from the download center)
- X3 bootloader/miniboot build steps
- Board flashing workflow skill (pending overlap decision with RDK Device Skills)

## License

Source code is licensed under [Apache-2.0](LICENSE-APACHE). Documentation and skill content is licensed under [CC-BY-4.0](LICENSE-CC-BY-4.0).
