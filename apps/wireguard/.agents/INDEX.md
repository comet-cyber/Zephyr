# Zephyr WireGuard 项目

更新日期：2026-10-23

- phase: active
- home: F:\zephyr\apps\wireguard
- 当前增量：P2 普通 UDP。最小回显已由用户确认成功；2026-10-22 下载编程/校验成功，2026-10-23 用户再次确认可以下载程序，下载问题按已恢复处理。保留 Titan profile 的 `--pre-script-cmd=connect` 等现有参数；USB 重新插拔与显式连接均参与了恢复，未隔离具体诱因，不认定板载 J-Link 不适配或原配置错误。当前源码正文为 `Hello from Titan #%d->`；下一步验收实际 `#1->` 至 `#10->` 收发，再做回复校验及至少 100 条统计。

## 当前入口

1. [STATUS](STATUS.md)：当天总结、已验证事实、待办及历史证据。
2. [PLAN](PLAN.md)：增量路线；当前继续报文序号、回复校验及统计，不再重复环境、ping 或最小回显。
3. [THEORY](THEORY.md)：原理；[DECISIONS](DECISIONS.md)、[OPEN](OPEN.md)：已有决策和问题，冲突时以当前 STATUS 和实际证据为准。
4. [HARDWARE](HARDWARE.md)、[SAFETY](SAFETY.md)：硬件与固件下载边界。

## 最新事实

- 2026-10-23：用户确认程序下载已恢复；保留已成功使用的下载配置，不重复搭环境或继续无关的探针排障。下载成功与应用收发分别验收；本轮未提供带序号正文的实际收发输出。
- 2026-10-21：用户贴出十次发送成功、十次接收超时和 socket 关闭日志；只读检查当时 Windows 的 UDP 4242 无监听进程。指导先启动回显脚本再复位后，用户确认“成功了”。最小真实双向回显按用户报告完成；未获得该轮逐包日志，不推定十包全收或无丢包。
- 目标为 Titan 大板 Cortex-M85，board target：ra8p1_titan/r7ka8p1kflcac/cm85；Zephyr 4.4.99，源码 4c6971ba90a。
- 最小 main + printk 已由用户报告运行成功；网络 shell 输出由用户提供。
- 当前对端是 Windows 本机，鲁班猫3不在身边；长期 Linux 对端仍初选鲁班猫3。
- Windows 真实以太网 192.168.50.1/24；Titan eth0（接口1）192.168.50.2/24，carrier ON，千兆全双工，MAC 74:90:50:01:02:03；eth1未用。
- Windows → Titan ping 实测3/3回复，0%丢包，1–2ms；Titan → Windows曾超时；用户随后明确确认 ping 已解决、P1 按完成处理，不再复验。反向 ping 未保存新的原始输出。
- prj.conf 静态地址已持久保存；构建通过已实测。最新源码另含 NET_IF_MAX_IPV4_COUNT=2 和 NET_STATISTICS=y，这两项最新构建/板上生效状态未独立复核。
- WireGuard已编译启用但未配置隧道、peer或密钥；当前 UDP 源码向 192.168.50.1:4242 发送 `Hello from Titan #%d->`，格式化后按实际长度发送。2026-10-20 的旧版 16 字节 Hello 抓包曾记录 Windows 投递异常，后续最小双向回显已由用户确认成功，不再作为当前阻塞。历史证据见 [抓包分析](evidence/udp-startup-20261020-111951/analysis.md)。
- Windows 收发工具为 `tools/udp_receiver.py`，仅使用 Python 标准库，默认监听 192.168.50.1:4242 并持续接收、原样回显到实际源 IP/端口，Ctrl+C 退出；`--once` 处理一个数据报并完成回显后退出，`--no-echo` 仅接收、用于测试板端超时。本机回环已验证连续收发、多源端口、二进制和空数据报及单次退出；不代替 Titan 板上回显验收。
- 最新真实接收：诊断接收器先实收来自 `192.168.50.2:53175` 的完整 16 字节 Hello；之后用户在自己的终端以 `--host 0.0.0.0` 启动接收器，保持板子运行并执行 shell 发送命令，也明确确认出现 `Data: Hello from Titan`。诊断自建接收进程和抓包均已结束；用户自己的接收器由用户控制。未改脚本默认监听地址、板端代码或系统网络设置。
- Zephyr IDE 4.1.0字符串保存问题已通过源码和最小复现定位；未修改插件，配置由用户手动保存至prj.conf。

不重复搭建环境；默认继续辅助学习。无板上证据不标记功能完成，禁止存储密钥；固件下载遵循 SAFETY。此次只保存本地记录，不提交Git或推送。
