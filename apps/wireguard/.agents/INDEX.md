# Zephyr WireGuard 项目

更新日期：2026-10-24

- phase: active
- home: F:\zephyr\apps\wireguard
- 最终目标：Titan 与鲁班猫 3 在两个不同网络中，通过 WireGuard 完成应用双向通信；Titan 优先使用板载 CYW43438 独立联网。当前增量为 Wi-Fi/SDIO 适配可行性核对，已确认本地 RA SDHC 驱动存在 SDIO 命令缺口。有线链路保留为本地隧道联调基线。

## 当前入口

1. [STATUS](STATUS.md)：当天总结、已验证事实、待办及历史证据。
2. [PLAN](PLAN.md)：增量路线；普通 UDP 按用户反馈已通过，100 条统计移至隧道内应用阶段。
3. [THEORY](THEORY.md)：原理；[DECISIONS](DECISIONS.md)、[OPEN](OPEN.md)：已有决策和问题，冲突时以当前 STATUS 和实际证据为准。
4. [HARDWARE](HARDWARE.md)、[SAFETY](SAFETY.md)：硬件与固件下载边界。

5. [WIFI_FEASIBILITY](WIFI_FEASIBILITY.md)：板载 Wi-Fi 的硬件依据、本地驱动缺口与跨网拓扑边界。

## 最新事实

- 2026-10-24 扫描排查：用户新增 CONFIG_WIFI=y 与 CONFIG_NET_L2_WIFI_SHELL=y，15:45 配置/15:46 构建已包含命令支持；用户截图 wifi scan 返回 Scan request failed。当前构建没有启用 AIROC/CYW43438 驱动，SDIO_STACK 未启用，sdhc1 仍 disabled、没有 Wi-Fi 设备节点；用户随后提供 net iface：仅 eth0、eth1、wg0、wg_ctrl，全部 down，没有 Wi-Fi 接口，运行时缺少 Wi-Fi 接口已确认。下一步处理板级与 SDIO 适配，不再重复要求列接口。

- 2026-10-24：用户明确最终目标为两个不同网络下的 Titan ↔ 鲁班猫 WireGuard 项目。有线直连是联调手段；Wi-Fi 已纳入项目范围。公网入口与是否接受 VPS 中心转发仍待选择。
- 普通 UDP 的编号、回复长度与内容校验已由用户反馈成功；已进入 WireGuard 学习。当前源码包含 VPN 接口定位、长度比较与 memcmp；没有握手成功证据。

- 2026-10-23：用户确认程序下载已恢复；保留已成功使用的下载配置，不重复搭环境或继续无关的探针排障。下载成功与应用收发分别验收；本轮未提供带序号正文的实际收发输出。
- 2026-10-21：用户贴出十次发送成功、十次接收超时和 socket 关闭日志；只读检查当时 Windows 的 UDP 4242 无监听进程。指导先启动回显脚本再复位后，用户确认“成功了”。最小真实双向回显按用户报告完成；未获得该轮逐包日志，不推定十包全收或无丢包。
- 目标为 Titan 大板 Cortex-M85，board target：ra8p1_titan/r7ka8p1kflcac/cm85；Zephyr 4.4.99，源码 4c6971ba90a。
- 最小 main + printk 已由用户报告运行成功；网络 shell 输出由用户提供。
- 当前对端已切换为鲁班猫 3（实测 Debian 12，内核 6.1.99-rk3576-wg）；eth0 临时 192.168.50.1/24，Wi-Fi 192.168.28.172 保留管理用途。鲁班猫 ping Titan 3/3 成功，临时 wg0 与 peer 已配置，尚无隧道握手验收。
- 首轮 Windows 真实以太网 192.168.50.1/24；Titan eth0（接口1）192.168.50.2/24，carrier ON，千兆全双工，MAC 74:90:50:01:02:03；eth1未用。
- Windows → Titan ping 实测3/3回复，0%丢包，1–2ms；Titan → Windows曾超时；用户随后明确确认 ping 已解决、P1 按完成处理，不再复验。反向 ping 未保存新的原始输出。
- prj.conf 静态地址已持久保存；构建通过已实测。最新源码另含 NET_IF_MAX_IPV4_COUNT=2 和 NET_STATISTICS=y，这两项最新构建/板上生效状态未独立复核。
- Titan 的 WireGuard 已编译启用，C 初始化目前只定位 VPN 接口，尚未完成地址/密钥/peer 配置及握手验收；当前 UDP 源码向 192.168.50.1:4242 发送 `Hello from Titan #%d->`，格式化后按实际长度发送。2026-10-20 的旧版 16 字节 Hello 抓包曾记录 Windows 投递异常，后续最小双向回显已由用户确认成功，不再作为当前阻塞。历史证据见 [抓包分析](evidence/udp-startup-20261020-111951/analysis.md)。
- Windows 收发工具为 `tools/udp_receiver.py`，仅使用 Python 标准库，默认监听 192.168.50.1:4242 并持续接收、原样回显到实际源 IP/端口，Ctrl+C 退出；`--once` 处理一个数据报并完成回显后退出，`--no-echo` 仅接收、用于测试板端超时。本机回环已验证连续收发、多源端口、二进制和空数据报及单次退出；不代替 Titan 板上回显验收。
- 首轮历史实收：诊断接收器先实收来自 `192.168.50.2:53175` 的完整 16 字节 Hello；之后用户在自己的终端以 `--host 0.0.0.0` 启动接收器，保持板子运行并执行 shell 发送命令，也明确确认出现 `Data: Hello from Titan`。诊断自建接收进程和抓包均已结束；用户自己的接收器由用户控制。未改脚本默认监听地址、板端代码或系统网络设置。
- Zephyr IDE 4.1.0字符串保存问题已通过源码和最小复现定位；未修改插件，配置由用户手动保存至prj.conf。

不重复搭建环境；默认继续辅助学习。无板上证据不标记功能完成，禁止存储密钥；固件下载遵循 SAFETY。此次只保存本地记录，不提交Git或推送。
