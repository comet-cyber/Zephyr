# DECISIONS

更新日期：2026-10-14

## 已锁

- 开发入口：VS Code IDE for Zephyr 插件；Titan 当前使用 jlink runner 和板载探针 UID 24060501，复用用户已打通的 rgb_led 编译/下载链路。

- home：F:\zephyr\apps\wireguard，用户明确指定。
- MCU/核：已有 RA8P1，Cortex-M85/CPU0 单核；首轮锁定 Titan 大板。
- RTOS：Zephyr，学习目标明确；Ubuntu 鲁班猫为 Linux 对端。
- 语言：应用 C，Linux 对端先用简单可观察的回显程序。
- 实现：优先本地 Zephyr 原生 WireGuard API；沿用当前源码提交，不使用另一套 lwIP 移植。
- 工具链：沿用 F:\zephyr\.venv\Scripts\west.exe 与工作区 Zephyr SDK；实际构建前复核，参考 ../../.. 路径不作猜测，工作区文档位于 F:\zephyr\.agents\TOOLCHAIN.md。
- 首版网络：Titan 大板一个物理网口通过网线直连鲁班猫3，使用静态 IPv4；一个 WireGuard peer、隧道应用收发。
- 学习节奏：普通网络 → UDP → WireGuard → 恢复/并发；API 学参数、返回值、上下文与所有权，再追一条实现路径。

## 候选比较

| 轴 | 首选 | 其它候选与理由 |
| --- | --- | --- |
| 板卡 | Titan 大板 | Mini 能沿用已有基线，但存在原固件保护；不采购第三块板 |
| 软件栈 | Zephyr 原生 WireGuard | 裸机/lwIP 不服务本次 Zephyr 学习；只用 Linux WireGuard 无法完成 MCU 目标 |
| 开发工具 | west + 工作区 SDK | IAR 适合现有裸机恢复，不作为 Zephyr 应用主构建链；native_sim Linux 模拟仅作故障隔离备选 |
| 网络 | 建议网线直连静态 IPv4 | 共用交换机/路由器也可；Wi-Fi 引入额外驱动与配网问题 |

## 淘汰与变更

首版不做自研密码算法、不复制官方示例私钥、不直接把 native_sim 的 TAP 配网脚本用在实物网卡上。

- 2026-10-14 superseded：此前按 DAPLink 建议 pyOCD → 本机枚举确认当前接口为 SEGGER J-Link 类，改用 jlink runner；不升级或重刷探针固件。
