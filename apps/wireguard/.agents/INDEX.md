# Zephyr WireGuard 项目

更新日期：2026-10-14

- phase: planning
- home: F:\zephyr\apps\wireguard

在 RA8P1 Titan 大板 Cortex-M85 上用 Zephyr 与 Ubuntu 鲁班猫3建立 WireGuard 隧道，伴随每个工程增量学习实际用到的 API 与内核机制。立项资料已落盘，主板和网络拓扑已锁定；未启动实现。

## 阅读入口

1. [STATUS](STATUS.md)：Titan 编译/下载链路已由用户确认打通；网络尚未验证。
2. [DECISIONS](DECISIONS.md)、[OPEN](OPEN.md)、[PLAN](PLAN.md)：下一步先准备板端最小网络配置，复用已有环境基线。
3. [THEORY](THEORY.md)：数据路径与学习切入点。
4. [HARDWARE](HARDWARE.md)、[SAFETY](SAFETY.md)：接线和下载边界。
5. [BRIEF](BRIEF.md)：目标、范围、成功标准。

## 已检查的事实

- 当前应用 CMakeLists.txt、prj.conf、Mini overlay 均为空，src/build 目录没有可用应用证据。
- 本地 Zephyr VERSION 为 4.4.99，源码 HEAD 为 4c6971ba90a；WireGuard 标为 EXPERIMENTAL。
- 本地具备 include/zephyr/net/wireguard.h、subsys/net/lib/wireguard 和 samples/net/wireguard。
- Titan、Titan Mini CM85 DTS 均包含以太网 PHY 配置与 zephyr,entropy = &trng，但尚未验证实物网络。
- 包装仓库仅观察到 apps/wireguard/ 未跟踪；本次不提交、不创建 Issue/PR。

本项目与工作区原 rgb_led 进度独立；工作区 ../.. 下的 .agents 仅作为工具链和安全参考。无构建/板上证据，不写 verified。禁止存储密钥。
