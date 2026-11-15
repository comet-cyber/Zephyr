# 后续计划与 Flash 迁移

更新日期：2026-11-09（Asia/Shanghai）。

## 当前验收与下一步

2026-11-08 用户授权助手直接修复；Wi-Fi 初始化及 COM4 Shell 扫描已通过两轮复位、5 次扫描验收，见 [报告](evidence/wifi-fix-20261108/README.md)。本轮目标已完成。

2026-11-09 已按用户要求启用 IPv4/DHCPv4 与自动 DHCP，构建、下载和读回校验完成。用户确认目标为 `Redmi_514` 后，板端关联成功、自动取得 `192.168.28.198/24`，并通过网关 `192.168.28.1` 的 3 次 ping（0% 丢包），见 [记录](evidence/wifi-fix-20261109-ipv4/README.md)。本轮扫描、关联、自动 IPv4 取址与网关连通性目标已完成，结束时保持连接并释放 COM4。

断电冷启动、长期稳定性、应用层数据传输与互联网访问尚未验收；后续按用户需求推进。现有 KSO 唤醒 CMD52 首次写入 -EIO 诊断日志仍保留，本次未阻止 DHCP 或 ICMP 通信。

本次直接执行授权适用于此次修复。下列“用户亲自动手、助手指导”是历史协作方式，本次已由用户新指令覆盖。

## 历史推进方向（2026-11-02）

用户此前暂缓 Flash 迁移，随后因空间不足恢复迁移。只读审计、全片清理、固件上传和全量读回校验均已完成；只读审计的原始备份及过程见 [验证报告](evidence/flash-audit-20261028-154836/README.md)。

2026-10-31 用户确认旧板遗留数据不再需要，外部 Flash 全片擦除并经 J-Link 确认为 `FF`。之后将 `43438A1.bin` 写入应用规划的 `whd-firmware` 分区，UART 传输头部检查通过，并从 CPU 映射地址全量读回 419808 B，SHA-256 与写入镜像一致。

WHD 外部资源读取适配和 Wi-Fi/SDIO 配置已在应用侧完成，且 pristine 构建通过。下一步是下载新的 CM85 镜像并验证初始化。该偏移是本应用规划的分区，不代表已确认厂商原始分区表。保留现有全片审计备份。

后续围绕现有 Wi-Fi 应用逐步验证：

2026-11-02 已确认 Zephyr Shell 提供 `wifi scan`，并在应用侧将网络管理事件队列设为 32 项、等待时间设为 100 ms；当前镜像已构建通过。下一待验收项是下载本次 CM85 镜像，确认启动无 SDIO Usage Fault 后，在串口 Shell 执行扫描。

1. 观察板上启动日志，确认 SDHI1/SDIO 和 AIROC 驱动初始化结果。
2. 通过 Wi-Fi shell 验证扫描与 STA 关联。
3. 按实际局域网补齐 IPv4/DHCPv4，验证取址、路由与连通性。
4. 验证与电脑的数据传输，再推进 WireGuard。

每一步以实际日志和板测结果验收，不将编译成功视为运行验收。涉及代码修改和板上操作时，沿用用户亲自动手、助手指导的协作方式。

## 外部 Flash 迁移：已恢复

### 动机与已确认事实

- 当前 CM85 MRAM 使用 `770952 / 786432 B`，余量约 `15.1 KiB`。
- 当前板级 `chosen` 配置为 `zephyr,flash = &code_mram_cm85`；主程序及只读 Wi-Fi 资源均存放在 MRAM。
- WHD 通过 `RESOURCE_BIN_ADD(".rodata", ...)` 将资源打包进只读数据段；Wi-Fi 芯片启动时，主控读取这些资源并经 SDIO 加载到 CYW43438。

| 当前资源 | 大小 |
|---|---:|
| `43438A1.bin` | 419799 B |
| `43438A1.clm_blob` | 7222 B |
| `cyw943438_aw-cu427.txt` | 710 B |
| 合计 | 427731 B，约 417.7 KiB |

若移出以上资源，仅按大小相减，MRAM 占用约为 `343221 B`（335.2 KiB）。这是粗略估算，未计外部 Flash 驱动、资源适配与链接对齐的变化，不能视为实测迁移结果。

### 外部存储与支持现状

- 厂商工程的目录名为 `hyperflash`，当前代码按 **W35T51NW、64 MB 外部 NOR Flash、OSPI 接口**配置；后续实施前仍需核对实际板卡器件及片选。
- 板载 HyperRAM 是另一种易失性存储器，不作为掉电保存 Wi-Fi 固件的替代品。
- 当前 Zephyr 源码已有 `drivers/flash/flash_renesas_ra_ospi_b.c` 通用 RA OSPI NOR 驱动。
- 用户已在本项目 overlay 接入外部 NOR；实际驱动设备为 `titan_ospi_flash_ctrl` / `flash-controller@1`，子节点 `titan_ospi_flash` 用于描述容量。
- 当前板测确认 64 MiB 可读；2026-10-31 在 `0x02000000～0x0207FFFF` 完成擦除、UART 写入及 J-Link 全量读回 SHA-256 校验。此结果证明该分区的本次写入链路可用，不代表已验证芯片全部擦写边界或其他分区行为。
- 通用驱动存在不等于该板已完整适配；厂商 RT-Thread 的资源分区和烧录方案不会自动应用到 Zephyr。

### 后续实施路线

优先保持 Zephyr、应用和 WHD 主机驱动位于 MRAM，将占用最大的 Wi-Fi 固件移至外部 NOR；CLM/NVRAM 暂留 MRAM，后续再根据启动稳定性和空间预算决定是否迁移。

1. **完成外部 NOR 固件分区写入验证**：已在 `0x02000000～0x0207FFFF` 写入 `43438A1.bin`，并完成 419808 B 全量读回 SHA-256 校验；全片原始备份继续保留。
2. **应用侧 custom resource 接入**：已完成。WHD 通过 `USES_RESOURCES_IN_EXTERNAL_STORAGE` 调用应用回调，固件从该分区读取并送入 CYW43438。
3. **确定剩余资源放置与版本配套**：CLM/NVRAM 暂留 CM85 镜像，已按 7222 B / 710 B 生成并链接；固件、CLM、NVRAM 仍保持同一 CYW43438 组合。
4. **保证初始化顺序**：已在代码层使用 Zephyr Flash 分区设备；板上仍需确认外部 Flash 就绪后 Wi-Fi 初始化顺序。
5. **重新验收**：构建和 Map 已验收；待板上验证 SDIO 初始化、固件下载、扫描和连接。

分区设计时还需检查上游 OSPI 驱动的校准区使用方式：当前实现可能擦写外部 Flash 末尾扇区以保存自动校准数据，资源和已有数据应避开该区域。

### 参考位置

- 本地 Wi-Fi 固件打包方式：`F:\zephyr\modules\hal\infineon\whd-expansion\WHD\COMPONENT_WIFI5\resources\resources.h`。
- 本地 RA OSPI 驱动：`F:\zephyr\zephyr\drivers\flash\flash_renesas_ra_ospi_b.c`。
- [厂商外部 Flash 驱动](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/board/ports/hyperflash/drv_ospi_flash.c)。
- [厂商 Flash 参数与设备 ID](https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-board/blob/main/project/Titan_driver_wifi/board/ports/hyperflash/ospi_b_ep.h)。
