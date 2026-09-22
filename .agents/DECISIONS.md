# DECISIONS

> 更新日期：2026-09-22

记录已经选定、后续默认遵守的决定。要改这些决定，先更新本文件和 `STATUS.md`。

## 2026-09-22  工作区与板

- Zephyr 学习根目录固定为 `F:\zephyr`，不用 `C:\Users\comet` 或 `F:\ai_lab` 另起一份 west 树。
- 学习板是 **ra8p1-titan-mini**，Zephyr 名 `ra8p1_titan_mini`，默认 `.../r7ka8p1kflcac/cm85`。
- 这是独立学习轨，不并入 `embedded-systems-learning` 的 Issue/PR 流程，除非用户以后明确要求。
- 包装仓库 `comet-cyber/Zephyr` 只跟踪工作区配置与 `.agents`；上游源码继续 gitignore + west 管理。

## 2026-09-22  下载策略

- 入门阶段 **禁止** 使用带 `option_setting_*` 的默认 RA8P1 镜像直接 `west flash`。
- 日常下载只写 Code MRAM。Config Area / OTP / 分区保持裸机阶段的守门策略。
- 第一次板上实验必须：当前固件备份 → 镜像审计 PASS → 用户当次明确同意。
- 优先 hex/elf，不用 padded `zephyr.bin`。

## 2026-09-22  学习顺序

- 先安全 hello/blinky，再 DT/GPIO，再按键，再树外应用。
- 双核、MCUboot、以太网、NPU 不作为入门前置。
- 长期应用放到 `F:\zephyr\apps\`，不在上游 `samples/` 里长出项目。

## 待决（先不要猜）

- 是否把 west manifest 钉到某个 Zephyr 发布标签，而不是继续跟 `4.4.99` 主线。
- Zephyr 下载是继续用系统 J-Link，还是复用 IAR 自带 DLL `8.74`。
- 树外第一个应用的名字和目标（纯学习 blinky，还是逐步接系统监视器功能）。
