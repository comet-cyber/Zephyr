# Titan 板载 Wi-Fi 与跨网络 WireGuard 可行性

更新日期：2026-10-24

## 用户目标与边界

Titan 与鲁班猫 3 分别接入两个不同网络，通过 WireGuard 完成应用双向通信。Titan 优先使用板载 Wi-Fi，现有以太网直连保留为联调基线。继续使用当前 Zephyr 工作区，不因厂商示例采用 RT-Thread 而更换系统。

独立上网与接收公网入站是不同条件：Titan 可使用热点分配的私有地址，经网关和 NAT 主动联系公网 peer，不要求 Titan 自己获得公网 IP。两边都能上网仍不保证互为可达的 UDP endpoint。

## 已核对的硬件与源码

| 项目 | 依据与结论 |
| --- | --- |
| 板载模块 | 厂商 Titan_driver_wifi/README_zh.md 明确为 CYWL6208-GS，内部 CYW43438，通过 SDHI1/SDIO 连接 |
| 厂商软件路径 | RA r_sdhi + WHD + RT-Thread/lwIP；可参考硬件与初始化，不能直接视为 Zephyr 适配 |
| Zephyr Wi-Fi 驱动 | drivers/wifi/infineon/Kconfig.airoc 有 CONFIG_CYW43438；AIROC 使用 Zephyr 原生网络栈，可与原生 WireGuard 组合 |
| SDIO 上层需求 | drivers/wifi/infineon/airoc_whd_hal_sdio.c 经 sd_init、sdio_init_func 及 CMD52/53 包装访问模块；SDIO 枚举还需 CMD5 |
| 当前 RA 主机驱动 | drivers/sdhc/sdhc_renesas_ra.c 的 request 命令 switch 未处理 CMD5/52/53，未支持命令返回 -ENOTSUP；不能把 SD 卡读写能力当作 SDIO Wi-Fi 能力 |
| Titan 板级 | ra8p1_titan 的 pinctrl 含 sdhc1_default，但板级 DTS 未创建 Wi-Fi 节点；用户 15:45 新构建已启用 CONFIG_WIFI 与 Wi-Fi shell，但未启用 AIROC/CYW43438 驱动及 SDIO_STACK，sdhc1 仍为 disabled |
| 固件资源 | Zephyr CMake 有 43438A1.bin 的选择逻辑；本轮未验证固件 blob、CLM/NVRAM 与此模块的完整匹配和落盘情况 |

因此硬件方向成立，当前软件存在明确适配工作。尚无 Wi-Fi 构建、下载、扫描、连接或公网可达证据，不承诺只增加 CONFIG_WIFI=y 即可运行。

## 用户扫描失败与直接原因

用户执行 `wifi scan`，截图显示 `Scan request failed`。本地 `wifi_shell.c` 在扫描请求调用返回非零时打印此通用消息，未打印原始错误码；它不表示已成功扫描但找不到热点。

用户新增的两个配置项只打开 Wi-Fi 基础支持与 shell 命令。当前构建没有板载 Wi-Fi 设备节点与对应 AIROC 驱动，SDIO 总线链路也未启用。用户已提供 `net iface`：只有 eth0[1]、eth1[2]、wg0[3]、wg_ctrl[4]，全部 down，没有 Wi-Fi 接口。运行时缺少 Wi-Fi 接口已确认；继续板级和主机驱动适配，不再要求重复列接口。以太网接口 down 的具体原因未由此输出确认，也不作为 Wi-Fi 未注册的根因。

## HAL 与通知能力补充

本地 `modules/hal/renesas/drivers/ra/fsp/src/r_sdhi/r_sdhi.c` 中，`R_SDHI_ReadIo`、`R_SDHI_WriteIo`、`R_SDHI_ReadIoExt`、`R_SDHI_WriteIoExt`、`R_SDHI_IoIntEnable` 只忽略参数并返回 `FSP_ERR_UNSUPPORTED`。API 名称存在不代表已实现 SDIO 功能。

Zephyr RA SDHC 的驱动 API 表也没有 enable_interrupt/disable_interrupt；AIROC 具有 SDIO 带内和 GPIO 带外通知路径，需结合模块接线确定必要实现。当前不是增加设备树节点就能完成的适配，需先让最小 SDIO 枚举收到模块响应，再验证寄存器访问与数据传输。

厂商 rtconfig.h 还提供 REG_ON=1028、HOST_WAKE_IRQ=1294 及下降沿配置；这些是厂商编号，不直接作为 Zephyr GPIO 索引照抄。厂商 pin_data.c 与本地 sdhc1_default 的 SDHI1 引脚一致，控制信号仍须结合编号规则和原理图核对。

## 下一增量

1. 对照厂商 SDHI1/FSP 配置与原理图，核对总线、供电和唤醒信号，确定必要的主机能力。
2. 补齐 RA SDHC 的 SDIO 枚举、寄存器访问与数据传输；评估中断/通知方式，不预先宣布适配完成。
3. 在项目配置中接入 Wi-Fi 设备树、AIROC 驱动及匹配的固件/模块参数。
4. 按模块初始化、扫描 2.4 GHz AP、连接、DHCP 地址/网关、选定公网端点可达逐项验收；使用域名时验证 DNS。
5. 将已有 WireGuard 与 UDP 校验应用复用到该接口，分别验收本地隧道与跨网络通信。

## 跨网拓扑待选

候选接入方式：Titan 连手机热点，手机使用蜂窝网络；鲁班猫连家中宽带。手机若仍通过同一家庭宽带出网，不能用此证明跨运营商网络通信。

- 直接 peer：Titan 与鲁班猫直接互认公钥；通常需要一端具备公网 IPv4 加 UDP 转发入口，或可达公网 IPv6。外层中间路由器只转发加密 UDP。
- VPS 中心：两端分别与有公网 IP 的 VPS 建立 WireGuard，由 VPS 转发内层包；这是两段独立隧道，VPS 会解密并重新加密，可看到内层 IP 流量。应用若另加 TLS，其内容保密性由 TLS 提供。

用户尚未选择公网拓扑，本轮不部署或调整 VPS。

## 公开依据

- [板卡厂商 Wi-Fi 示例](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/README_zh.md)
- [厂商示例配置](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/rtconfig.h)
- 本地 Zephyr：F:\zephyr\zephyr；板目录 boards/ruiside/ra8p1_titan；驱动路径见上表。

本轮仅静态检查及项目文档同步，没有业务源码、目标板固件、网络配置或 VPS 状态变更。
