# Titan 上游驱动与 WireGuard 项目需求审查

日期：2026-10-26。

## 结论与范围

本地 Zephyr 为 `v4.5.0-rc3-3-g2a9e8ac155a`，主仓工作树干净。此结论针对该提交及其 manifest 指定依赖，不声称代表尚未拉取的远端新提交。

上游已经提供项目所需的主要协议与驱动接口：RA SDIO、CYW43438/AIROC、Zephyr 原生 IP/socket 和 WireGuard。可以据此继续完成 Titan 的 STA 联网与隧道项目，未发现需要从零移植整个 SDIO/Wi-Fi 协议栈的依据。但现状尚不满足“完整板级支持、构建可用、板上通信与恢复全部验收”：板级接入和资源选择缺失，另有一个初始化错误处理缺陷。

本次只读审查源码、配置、既有构建和厂商公开资料，并保存项目记录；没有同步依赖、下载 blob 到工作区、构建、连接/复位/下载目标板，未修改业务源码、上游驱动或系统网络。

## 已确认的能力

| 需求 | 源码证据 | 判断 |
| --- | --- | --- |
| RA SDIO 枚举与寄存器访问 | `drivers/sdhc/sdhc_renesas_ra.c:251` 处理 CMD52/CMD5 | 已实现主机接口 |
| SDIO 数据读写 | 同文件 `:442` 的 CMD53 分支调用 HAL 传输函数，处理字节/块模式 | 已实现；仍需 Titan 实测 |
| SDIO 带内中断 | 同文件 `:104`、`:535`、`:564` 与 `:792` | ISR、使能/屏蔽和上层回调已接入 |
| CYW43438 芯片选择 | `drivers/wifi/infineon/Kconfig.airoc` | 有芯片选项和 SDIO/native networking 路径 |
| STA 扫描、关联、断开 | `drivers/wifi/infineon/airoc_wifi.c:857`、`:900`、`:1000` | 有实现；不等于本板初始化成功 |
| Wi-Fi 与 WireGuard 共用原生栈 | AIROC 的 TX 调 WHD，RX 在 `airoc_wifi.c:516` 调 `net_recv_data()`；Kconfig 选择 `WIFI_USE_NATIVE_NETWORKING` | 不存在 socket offload 阻断本地虚拟网口的结构性冲突 |
| 隧道密码与随机源 | WireGuard PSA 路径、RA entropy 驱动，旧构建已启用真实 entropy/CSPRNG | 有实现基础；新组合仍需构建和运行验证 |

RA 驱动使用 `r_sdhi_command_send_no_wait`、`r_sdhi_transfer_read/write` 和 `r_sdhi_read_write_common`，不调用 HAL 中返回 UNSUPPORTED 的 ReadIo/WriteIo/IoIntEnable 等入口。HAL 的 `SDIO_MODE = 0` 初始化也不能单独用于否定支持，Zephyr 后续中断使能会设置 INTEN。

## 缺口 1：Titan 尚未接入 SDHI1/Wi-Fi

- SoC 的 `sdhc1`（`dts/arm/renesas/ra/ra8/ra8x2.dtsi:1532`）仍 disabled；Titan CM85 DTS 只启用接 SD 卡的 `sdhc0`，没有 `infineon,airoc-wifi` 子节点。
- 应用 overlay 仅关闭 option-setting 节点，未添加 Wi-Fi。
- `sdhc1_default` 已给出引脚：CLK=P400、CMD=P401、DAT0=P402、DAT1=P403、DAT2=P810、DAT3=P811，与厂商 pin_data.c 的 SDHI1 引脚集合吻合。
- 厂商 `rtconfig.h` 的 REG_ON=1028=`0x0404`，对应 P404；HOST_WAKE=1294=`0x050E`，对应 P514。HAL 的 `bsp_io.h` 枚举已确认端口编码。引脚连接依据为厂商示例，不代替实物/原理图复核。
- P514 的 SoC GPIO 映射为 `port_irq13`（`r7ka8p1xf.dtsi:513`）。Titan 当前只启用外部 IRQ1/20/31，若使用 HOST_WAKE 带外中断，还需启用 IRQ13 并分配不冲突的 NVIC IRQ。仅写 `wifi-host-wake-gpios` 不够。也可评估只用已实现的 SDIO 带内中断，不能预先假定省略 OOB 在本板已验证。
- 新 RA SDHC 每个启用实例必须提供 accs/card/dma-req/sdio-int 四组 IRQ；SDHC1 不能照抄 SDHC0 的 NVIC 编号。
- SCI1 的 I2C 引脚也定义为 P400/P401；当前 SCI1 未启用。后续不要同时启用该 I2C 路径和 SDHI1。

## 缺口 2：芯片选项不等于完整资源配套

`zephyr/modules/hal_infineon/whd-expansion/CMakeLists.txt:120` 的 CYW43438 分支只选择 FW_IMAGE_NAME；全文件没有 CYW43438 的默认 CLM_IMAGE_NAME/NVRAM_IMAGE_NAME 分支。后面 `:343` 和 `:348` 又无条件读取这两个文件的大小。

因此，单独添加 `CONFIG_CYW43438=y`，即使拿到了 bin，也不能认为默认资源链完整。需由项目显式提供完整 FW/CLM/NVRAM 选择，或完整实现 AIROC_WIFI_CUSTOM 的资源接口。CUSTOM 选项本身不会自动生成所需 C 资源/头文件。

本地 manifest 所列 CYW43438 正常固件及 CLM 文件均不存在于 `modules/hal/infineon/zephyr/blobs/img/whd/resources/` 对应路径。

已从厂商公开仓库以内存方式读取并校验：

| 文件 | 字节数 | SHA-256 |
| --- | ---: | --- |
| 43438A1.bin | 419799 | f85e3feed55c429cf2fc88316dba472647da25622bac6c07ab63807fa0ad875e |
| 43438A1.clm_blob | 7222 | e10611ba6721b8639426d4491a06c53587b56a5ea20f3f4b30ccd8866e26695b |

两文件与当前及 manifest 期望版本 hal_infineon/module.yml 的正常固件清单完全一致。

厂商 Wi-Fi 工程使用的 AW-CU427-P NVRAM 与本地同名 txt 归一化比较：厂商 42 个键，本地 43 个键；厂商所有键均存在，共有键中仅 NVRAMRev 元数据不同，本地额外有 macaddr。boardtype、boardrev、xtalfreq 等参数一致。这个结果提供了资源候选依据，不授权直接复用默认 MAC，也不代替本板射频与实际运行验收。

## 缺口 3：SDIO 初始化错误被误报为成功

位置：`drivers/wifi/infineon/airoc_whd_hal_sdio.c:109`。

```c
cy_rslt_t whd_ret = whd_init(...);
if (whd_ret == CY_RSLT_SUCCESS) {
    /* attach / wifi_on，以及内部失败分支 */
}
return 0;
```

上面是保留控制流的节选，省略号不是可编译代码。若 whd_init 本身返回失败，函数跳过整个 if 后仍返回 0。调用者 airoc_init 将继续使用尚未成功创建的 WHD 接口注册事件。已静态确认错误返回丢失；未在板上触发，不断言已发生崩溃。接入时应修复该错误路径，再验证内存不足的报错与清理行为。

WHD 的 whd_mem_malloc/calloc 映射到 k_malloc/calloc。当前旧构建 HEAP_MEM_POOL_SIZE=0，另有 GETADDRINFO 最低堆需求 280 B，不能把前者误说成完全没有堆；也不能据此认为已满足 WHD 的动态分配。Titan 没有对应 Wi-Fi 堆容量默认补充，需要在新配置中预算并测量。

## 限制 4：AP 与 STA 同时运行不受当前管理路径支持

`airoc_wifi.c:923` 在 AP 已启用时拒绝 STA connect；`:1069` 在 STA 已连接时拒绝 AP enable，均返回 -EBUSY。supplicant 的 AP 初始化路径 `:2269` 也有 STA 互斥判断；当前注册代码仅建立单个 Zephyr Wi-Fi 接口。

所以 `samples/net/wifi/apsta_mode` 不能作为 Titan 的直接验收示例。示例 README 的主要板卡为 ESP32。硬件/固件支持 APSTA 并不证明当前 Zephyr 适配支持它。本项目目标是 Titan 作为 STA 连接路由器/手机热点，单 STA 足够；若以后明确要求同时开热点，需要单独适配和验收。

## 缺口 5：依赖、联网配置与容量

- hal_renesas 实际 f2eb9bc7352f4dadae08e9f5f16b05bb26779b87；manifest 期望 0c0beea010e78899c8ffbfd995cbfe50d3e6595e。
- hal_infineon 实际 13e4b3cd70fb2d862a37e55665f03af09fe74201；manifest 期望 eae914ed1ad0b54af28191d13da9b8e98fb5cb2b。两模块本地均无修改；本次未切换。
- prj.conf 仍是有线静态 192.168.50.2/24、空网关，旧构建 NET_DHCPV4 关闭。需要按实际 Wi-Fi 网络配置 DHCP 或匹配的静态地址/网关；使用域名时再配置和验收 DNS。
- 如果同时保留 eth0、Wi-Fi 和 wg0 并配置 IPv4，旧的 NET_IF_MAX_IPV4_COUNT=2 不够，需要按实际用到的接口数量调整；只使用 Wi-Fi+wg0 则不能据此机械要求三个。
- CM85 默认 MRAM 区域为 768 KiB、SRAM0 为 1 MiB。仅 Wi-Fi firmware+CLM 就约 417 KiB；需根据新 ELF/Map 决定资源布置和内存预算，未构建，不能声称必然溢出或必然够用。厂商 RT-Thread 的外部 Flash 分区方案不会自动存在于 Zephyr。
- 既有构建仍是 4.4.99/4c6971ba90a，不能作为新版 Wi-Fi 构建证据。

## 缺口 6：WireGuard 重启恢复尚无默认保证

`subsys/net/lib/wireguard/wg.c:2310` 的弱默认时间实现来自 k_uptime_get；`wg_crypto.c:46` 明确说明握手时间戳参与对端防重放。

Titan 复位后 uptime 回零，使用相同静态密钥且 Linux 对端保留先前时间戳时，新的较小握手时间戳可能被拒绝，直到超过上一次记录值或对端状态改变。首次握手成功不能证明复位恢复要求已满足。应使用可跨重启保持递增的可信时间方案覆盖该弱函数，并实际验收；不关闭防重放、不把重启 Linux 对端当作恢复方案。

WireGuard 仍标记 EXPERIMENTAL。近期握手、隧道内双向校验、至少 100 条统计、Wi-Fi 断连重连和 Titan 复位恢复均需独立证据。互联网入口/NAT/端口转发属于拓扑条件，上游驱动无法自动解决，当前不部署或修改 VPS。

## 下一增量

1. 对齐必要 west 依赖并取得经过校验的正常 FW/CLM/NVRAM 资源。
2. 项目 overlay 接入 SDHI1、P404、选定中断路径和 AIROC 子节点；项目配置选择 CYW43438/SDIO、堆和联网方式。
3. 完成资源选择与上述错误返回修复，先验收纯 STA 的初始化、2.4 GHz 扫描、WPA2 连接、DHCP/网关及普通 UDP。WPA3 等能力不据通用驱动枚举自动保证。
4. 新构建后检查最终 DTS/.config、ELF/Map 与镜像范围，再按既有下载规则由用户验收板上行为。
5. 接入已有 WireGuard 目标，验证本地隧道、重启时间方案，之后验收跨网络与 100 条统计。

## 外部资料

- [厂商 Wi-Fi 说明](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/README_zh.md)
- [厂商配置](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/rtconfig.h)
- [厂商 pin_data.c](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/ra_gen/pin_data.c)
- [厂商固件目录](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/tree/main/project/Titan_driver_wifi/firmware)
- [厂商 NVRAM](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/packages/wifi-host-driver-latest/wifi-host-driver/WiFi_Host_Driver/resources/nvram/COMPONENT_43438/COMPONENT_AW-CU427-P/wifi_nvram_image.h)
- [manifest 指定 Infineon blob 清单](https://github.com/zephyrproject-rtos/hal_infineon/blob/eae914ed1ad0b54af28191d13da9b8e98fb5cb2b/zephyr/module.yml)

当前 src/main.c 的 UDP/VPN 查找代码全部处于注释内，实际 main 只返回 0；历史 UDP 通过结论保留为用户实测历史，不将旧代码描述为当前活动业务。
