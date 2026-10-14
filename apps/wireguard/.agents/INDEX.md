# Zephyr WireGuard 项目

更新日期：2026-10-14

- phase: active
- home: F:\zephyr\apps\wireguard
- 当前增量：P1 普通以太网 IPv4 已按用户确认完成；下一步 P2 普通 UDP 回显。

## 当前入口

1. [STATUS](STATUS.md)：当天总结、已验证事实、待办及历史证据。
2. [PLAN](PLAN.md)：增量路线；下一次直接做普通 UDP 回显，不再安排 ping 收尾。
3. [THEORY](THEORY.md)：原理；[DECISIONS](DECISIONS.md)、[OPEN](OPEN.md)：已有决策和问题，冲突时以当前 STATUS 和实际证据为准。
4. [HARDWARE](HARDWARE.md)、[SAFETY](SAFETY.md)：硬件与固件下载边界。

## 最新事实

- 目标为 Titan 大板 Cortex-M85，board target：ra8p1_titan/r7ka8p1kflcac/cm85；Zephyr 4.4.99，源码 4c6971ba90a。
- 最小 main + printk 已由用户报告运行成功；网络 shell 输出由用户提供。
- 当前对端是 Windows 本机，鲁班猫3不在身边；长期 Linux 对端仍初选鲁班猫3。
- Windows 真实以太网 192.168.50.1/24；Titan eth0（接口1）192.168.50.2/24，carrier ON，千兆全双工，MAC 74:90:50:01:02:03；eth1未用。
- Windows → Titan ping 实测3/3回复，0%丢包，1–2ms；Titan → Windows曾超时；用户随后明确确认 ping 已解决、P1 按完成处理，不再复验。反向 ping 未保存新的原始输出。
- prj.conf 静态地址已持久保存；构建通过已实测。最新源码另含 NET_IF_MAX_IPV4_COUNT=2 和 NET_STATISTICS=y，这两项最新构建/板上生效状态未独立复核。
- WireGuard已编译启用但未配置隧道、peer或密钥；UDP应用尚未实现。
- Zephyr IDE 4.1.0字符串保存问题已通过源码和最小复现定位；未修改插件，配置由用户手动保存至prj.conf。

不重复搭建环境；默认继续辅助学习。无板上证据不标记功能完成，禁止存储密钥；固件下载遵循 SAFETY。此次只保存本地记录，不提交Git或推送。
