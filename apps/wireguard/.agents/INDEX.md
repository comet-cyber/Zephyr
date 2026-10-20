# Zephyr WireGuard 项目

更新日期：2026-10-20

- phase: active
- home: F:\zephyr\apps\wireguard
- 当前增量：P2 普通 UDP。用户已确认延后首次发送后首包丢失现象消失，普通单向 UDP 应用接收已验证（用户报告）。支持启动时序影响；具体初始化/过滤机制尚未定位。下一步继续普通 UDP 回显，不再重复延时位置实验；正文尚未加入发送序号。

## 当前入口

1. [STATUS](STATUS.md)：当天总结、已验证事实、待办及历史证据。
2. [PLAN](PLAN.md)：增量路线；当前先验收 Titan → Windows UDP 接收，再继续回显，不再安排 ping 收尾。
3. [THEORY](THEORY.md)：原理；[DECISIONS](DECISIONS.md)、[OPEN](OPEN.md)：已有决策和问题，冲突时以当前 STATUS 和实际证据为准。
4. [HARDWARE](HARDWARE.md)、[SAFETY](SAFETY.md)：硬件与固件下载边界。

## 最新事实

- 目标为 Titan 大板 Cortex-M85，board target：ra8p1_titan/r7ka8p1kflcac/cm85；Zephyr 4.4.99，源码 4c6971ba90a。
- 最小 main + printk 已由用户报告运行成功；网络 shell 输出由用户提供。
- 当前对端是 Windows 本机，鲁班猫3不在身边；长期 Linux 对端仍初选鲁班猫3。
- Windows 真实以太网 192.168.50.1/24；Titan eth0（接口1）192.168.50.2/24，carrier ON，千兆全双工，MAC 74:90:50:01:02:03；eth1未用。
- Windows → Titan ping 实测3/3回复，0%丢包，1–2ms；Titan → Windows曾超时；用户随后明确确认 ping 已解决、P1 按完成处理，不再复验。反向 ping 未保存新的原始输出。
- prj.conf 静态地址已持久保存；构建通过已实测。最新源码另含 NET_IF_MAX_IPV4_COUNT=2 和 NET_STATISTICS=y，这两项最新构建/板上生效状态未独立复核。
- WireGuard已编译启用但未配置隧道、peer或密钥；UDP应用向 192.168.50.1:4242 发送 16 字节。2026-10-20 实际抓包证明 Hello 内容和 IPv4/UDP 校验和正确、已经到达电脑网卡，但 Windows 记录 `transport endpoint was not found` 等丢弃事件，尚未送达 Python。shell 手动发送的 probe 已被 Python 实收。证据见 [抓包分析](evidence/udp-startup-20261020-111951/analysis.md)。
- Windows 接收工具为 `tools/udp_receiver.py`，仅使用 Python 标准库，默认监听 192.168.50.1:4242 并持续接收，Ctrl+C 退出；`--once` 收到一个数据报后退出。电脑回环 UDP 测试已通过，该结果不代表开发板数据已到达电脑。
- 最新真实接收：诊断接收器先实收来自 `192.168.50.2:53175` 的完整 16 字节 Hello；之后用户在自己的终端以 `--host 0.0.0.0` 启动接收器，保持板子运行并执行 shell 发送命令，也明确确认出现 `Data: Hello from Titan`。诊断自建接收进程和抓包均已结束；用户自己的接收器由用户控制。未改脚本默认监听地址、板端代码或系统网络设置。
- Zephyr IDE 4.1.0字符串保存问题已通过源码和最小复现定位；未修改插件，配置由用户手动保存至prj.conf。

不重复搭建环境；默认继续辅助学习。无板上证据不标记功能完成，禁止存储密钥；固件下载遵循 SAFETY。此次只保存本地记录，不提交Git或推送。
