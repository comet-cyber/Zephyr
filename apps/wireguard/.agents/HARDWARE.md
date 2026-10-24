# HARDWARE

更新日期：2026-10-24

## 已有与候选

| 硬件 | 角色与接口 | 当前判断 |
| --- | --- | --- |
| RA8P1 Titan | 首轮主实验板；CM85，RJ45，以太网 PHY，UART5 控制台；板载调试器 | 本地有板定义；实物端口/板上固件待核对 |
| RA8P1 Titan Mini | 备选；CM85，RJ45，UART2 控制台 | 本地有板定义；与原学习固件共用实物，不能直接覆盖 |
| 鲁班猫 3 Debian 12 | Linux WireGuard 对端与回显接收端；以太网、Wi-Fi/SSH | 内核 6.1.99-rk3576-wg；物理 ping 3/3、临时 wg0/peer 已配置，握手未验收 |
| Titan 板载 CYWL6208-GS / CYW43438 | 目标为 Titan 独立 Wi-Fi 联网，SDHI1/SDIO | 厂商示例确认硬件路径；当前 Zephyr 板级未接入，RA SDHC 有 SDIO 命令缺口，板上未验证 |
| J-Link S/N 601012527 | SWD 下载/调试 | 历史 Mini 主链路可用，不等于已验证 Titan 接线 |
| DSLogic U2Pro16 | 必要时测 UART/PHY 控制信号 | 已有；默认不要求接入 |

## 接口矩阵

| 路径 | 接法/注意点 | 待核对 |
| --- | --- | --- |
| 普通 IP 与加密外层 UDP | Titan 与鲁班猫3一条网线直连，双方静态 IPv4 | 实际网口名称、物理 RJ45 到 DTS eth0/eth1 的对应 |
| 日志 | Mini UART2 / Titan UART5，DTS 为 115200；串口 TX/RX/GND | 引脚位置及 USB-UART 可用性；按原理图确认电平，不接 5V 信号 |
| 调试 | Titan 板载接口当前枚举为 SEGGER J-Link 类，UID 24060501；jlink runner | 用户确认下载打通；板载芯片型号未确认 |

本机枚举的附带串口为 JLink CDC UART Port (COM18)，尚未记录其实际运行日志。外置探针 601012527 与当前板载探针 24060501 必须区分。
| 随机数 | CM85 DTS chosen 指向 trng | Kconfig 实际选项、初始化和密码学随机源可用性 |

Titan Mini CM85 DTS 含 RTL8211F phy@1；Titan 含 eth0/phy@2 和 eth1/phy@1。源码定义不是实测能力证明。首轮只用一个物理网口，第二块 RA8P1 不同时加入网络，避免默认 MAC 地址等因素干扰。

## 采购

当前不建议采购；先核对网线、串口观察和 SWD 接线，缺失时再列清单。

## Wi-Fi 核对入口

详见 [WIFI_FEASIBILITY](WIFI_FEASIBILITY.md)。厂商 RT-Thread 示例是硬件与初始化参考，不作为当前 Zephyr 已适配证据。
