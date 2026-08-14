# 贡献指南

本仓库是 D-Robotics **BSP Skill Pack**：面向 RDK X3/X5/S 系列板级支持包开发的 Agent Skills 源头仓库。内容被中央目录 `D-Robotics/rdk-skills` 镜像分发。

## Skill 标准（L2）

每个 skill 必须满足：

1. `SKILL.md` 存在，frontmatter 必填 `name` / `description` / `version` / `license`（`license: Apache-2.0`）；`name` 小写连字符、与目录名一致；`description` ≤1024 字符且携带触发词与负向触发词
2. 四个必备章节：`## Purpose` / `## When to use` / `## Instructions` / `## Safety`
3. `skill-card.md`（owner、license、用例、已知风险）
4. `evals/tasks.yaml`（五维：security / correctness / discoverability / effectiveness / efficiency）
5. 每个 SKILL.md 带 `Sources:` 行，标注官方出处（构建仓库 README 版本或官方文档链接）

## 设计原则

1. **官方仓库是唯一真相源**：命令、路径、参数均出自 `x5-rdk-gen` / `rdk-gen` / `rdk_s_doc`，不编造
2. **平台隔离**：X 系列（X3/X5）与 S 系列（S100/S600）BSP 严格分开，S 系列只在 `bsp-s-series` 中处理
3. **主机侧为主**：本 Pack 覆盖开发主机构建流程；板端烧录/诊断属设备侧 Pack（rdk-device-skills），不越界
4. **观察/行动分离**：读命令、跑构建前向用户确认 `sudo` 与磁盘/网络副作用

## 提交要求

- DCO 签名：`git commit -s -m "..."`
- 新增 skill：一个 PR 一个 skill，按 L2 标准写全
- 修改命令/流程：同步更新 `Sources:` 与 `evals/`

## 本地校验

```bash
make validate          # 或 python3 tools/validate.py --mode advisory
```
