# Titan 板载 Wi-Fi 与跨网络 WireGuard 可行性

更新日期：2026-10-26（驱动与完整需求审查）

## 当前结论

2026-10-26 进一步审查见 [UPSTREAM_REVIEW](UPSTREAM_REVIEW.md)：主要单 STA 原生网络链路可复用，但当前不属于完整可用的 Titan Wi-Fi 支持。除了板级/依赖接入，CYW43438 CMake 缺 CLM/NVRAM 默认选择，本地 blob 未取得，SDIO 初始化存在 whd_init 失败仍返回成功的问题。APSTA 在当前 AIROC 管理路径中被明确互斥，单 STA 仍符合本项目目标。厂商正常 FW/CLM 的 SHA-256 已与上游清单核对一致，NVRAM 主要参数相符；资源来源已有依据，接入及板上验证仍未完成。另需核算堆/镜像容量，并处理 WireGuard 复位时间戳。

用户已将本地 Zephyr 从 4.4.99 / 4c6971ba90a 更新到 4.5.0-rc3 / 2a9e8ac155a。新版已包含 RA SDIO 命令、数据传输和中断支持，之前“当前缺少 SDIO 驱动，需先移植”的结论已被新版本取代。

当前应复用上游驱动，完成依赖版本对齐、Titan 的 SDHI1/Wi-Fi 板级描述、驱动选择和固件/模块参数接入，再进行构建与板上验证。源码已具备支持不等于 Titan 无线联网已经验收。

## 目标与硬件

Titan 与鲁班猫 3 分别接入两个不同网络，通过 WireGuard 完成应用双向通信。Titan 优先使用板载 Wi-Fi；以太网直连保留为联调基线，继续使用当前 Zephyr 工作区。

厂商 Titan_driver_wifi/README_zh.md 确认板载模块为 CYWL6208-GS，内部 CYW43438，通过 SDHI1/SDIO 连接。厂商 RT-Thread/WHD 示例可作为硬件、GPIO、固件与初始化参考，不直接替代 Zephyr 的板级适配。

## 新版已具备的能力

关键提交：[37ff7a7f1b1](https://github.com/zephyrproject-rtos/zephyr/commit/37ff7a7f1b1b4598b4e8c7066b5fe41f4b44a8da)，标题为 drivers: sdhc: Add support for SDIO command for Renesas RA。

| 部分 | 本轮核对结果 |
| --- | --- |
| CYW43438 | drivers/wifi/infineon/Kconfig.airoc 已有芯片选择与 AIROC 原生网络驱动 |
| CMD5、CMD52 | sdhc_renesas_ra.c 的 request switch 已处理 SDIO_SEND_OP_COND 与 SDIO_RW_DIRECT |
| CMD53 | 已实现 SDIO_RW_EXTENDED 的字节/块传输、读写与完成等待 |
| 中断 | 已有 ra_sdio_int_isr、带内 SDIO 中断、enable_interrupt/disable_interrupt 驱动回调 |
| HAL 调用路径 | 使用底层命令/传输辅助函数与寄存器，不调用 ReadIo/WriteIo 等返回 UNSUPPORTED 的 HAL 占位接口 |
| Titan 默认 DTS | 现有 sdhc0 增加 sdio-int 中断，但仍未接入 SDHI1 的 Wi-Fi 节点 |

HAL 高层 SDIO 函数仍为占位实现，本身不再构成上述新版 Zephyr 路径的阻塞。不要继续据旧版函数截图推断当前 RA SDIO 不支持。

## 仍需完成的板级与构建工作

1. 对齐依赖：主仓已更新，但两 HAL 尚未与新 west.yml 对齐。hal_renesas 当前 f2eb9bc7352f4dadae08e9f5f16b05bb26779b87，期望 0c0beea010e78899c8ffbfd995cbfe50d3e6595e；hal_infineon 当前 13e4b3cd70fb2d862a37e55665f03af09fe74201，期望 eae914ed1ad0b54af28191d13da9b8e98fb5cb2b。本轮仅检查，未切换这些模块。
2. 项目 overlay 启用 SDHI1，选择 sdhc1_default，引入 AIROC Wi-Fi 子节点并核对供电/唤醒 GPIO。新驱动需要 accs/card/dma-req/sdio-int 的中断配置，不能照抄 SDHC0 的 IRQ 编号。
3. Kconfig 选择 CYW43438 与必要网络配置；AIROC 驱动依赖有效设备树节点，单独 CONFIG_WIFI=y 与 Wi-Fi shell 不会自动创建设备。
4. 核对固件、CLM/NVRAM 与模块型号及内存布置；Zephyr CMake 已有 43438A1.bin 选择逻辑，本轮未验证 blob 的存在性与模块匹配。
5. 完成依赖、最终 DTS/.config 和编译检查后，按模块初始化、2.4 GHz AP 扫描、连接、DHCP 地址/网关、公网端点可达逐项验收。仅在具体故障证据出现后修改上游驱动。

厂商 rtconfig.h 有 REG_ON=1028、HOST_WAKE_IRQ=1294 与下降沿配置；这些是厂商编号，须按其编号规则与原理图转换，不能直接当 Zephyr GPIO 索引。SDHI1 引脚已在本地 pinctrl 提供。

## 更新前的运行证据

用户在旧固件上执行 wifi scan，返回 Scan request failed。随后 net iface 只列 eth0[1]、eth1[2]、wg0[3]、wg_ctrl[4]，全部 down，没有 Wi-Fi 接口。旧构建缺 AIROC/CYW43438、SDIO_STACK、Wi-Fi 设备节点，sdhc1 disabled。

这证明旧固件未注册无线接口；未重新构建/下载的新源码不会自动改变板上状态。扫描错误原文未显示 errno，也不能用于判断周围是否存在热点。

## 跨网拓扑边界

Titan 可用私有地址经网关和 NAT 主动联系公网 peer，不要求自身获得公网 IP；双方能上网仍不保证互相可接收外层 UDP。候选接入为 Titan 连手机热点（手机使用蜂窝网络）、鲁班猫连家中宽带。

- 直接 peer：两端互认公钥，需可达公网入口，例如公网 IPv4 加 UDP 端口转发，或可达公网 IPv6。
- VPS 中心：两端各与 VPS 建 WireGuard，由 VPS 转发内层包；这是两段隧道，VPS 会解密并重新加密，可见内层 IP 流量。应用 TLS 的内容保密性另由 TLS 提供。

公网拓扑尚未选择，本轮未部署或调整 VPS。

## 参考

- [厂商 Wi-Fi 示例](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/README_zh.md)
- [厂商配置](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/rtconfig.h)
- 本地 Zephyr：F:\zephyr\zephyr；驱动 drivers/sdhc/sdhc_renesas_ra.c；板目录 boards/ruiside/ra8p1_titan。

本轮完成静态复核与项目文档更新，没有修改应用/驱动源码、同步依赖、构建、下载或网络设置变更。
