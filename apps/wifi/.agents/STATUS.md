# 当前状态

更新日期：2026-11-09（Asia/Shanghai）。

## 最新状态：Wi-Fi 关联、自动 DHCPv4 与网关连通性已通过

2026-11-09 用户要求启用 IPv4/DHCPv4 并继续执行。应用新增 `NET_IPV4=y`、`NET_UDP=y`、`NET_DHCPV4=y`、`WIFI_STA_AUTO_DHCPV4=y`；AIROC 关联成功后会自动启动 DHCP。

- 构建通过：FLASH 399900 B，RAM 248712 B；最终配置四项均为 y。
- 已备份 Code MRAM、通过 IAR J-Link 下载，并二次独立读回核对全部 34 个实际分配段一致。CPU 结束时运行。
- 当前 BIN SHA-256：`be480a92e28d00d35ced00c43a36128e112cd86b566ffc4fc139383beaf5430b`。
- COM4 释放后，新 IPv4 镜像已通过软件复位、扫描和 34 段读回校验。用户将目标 SSID 更正为 `Redmi_514` 后，板端关联成功：COMPLETED、2.4 GHz、信道 6、WPA2-PSK、RSSI -39 dBm。
- 自动 DHCPv4 一次取得 `192.168.28.198/24`，网关及 DHCP 服务器为 `192.168.28.1`，状态 bound，租期 43200 秒；两次 `net iface` 查询一致。
- 板端 ping 网关 3 发 3 收、0% 丢包，RTT 最小/平均/最大为 23.38/24.43/25.60 ms。`net_mgmt` 栈实测使用 936/4096 B，剩余 3160 B。
- 本次仍可见 KSO 唤醒 CMD52 首次写入 -EIO 日志，但 DHCP 和全部 ping 均成功；不将其描述为已消除。未验收断电冷启动、长期稳定性或互联网访问。
- 测试结束保持 Wi-Fi 连接，COM4 已关闭释放；凭据未写入配置，证据日志中的密码已脱敏。
- [配置、构建与下载证据](evidence/wifi-fix-20261109-ipv4/README.md)。

## 扫描修复基线（2026-11-08）

2026-11-08 用户明确要求助手直接修复并使用已连接开发板；本轮已完成修改、构建、MRAM 备份/下载/读回校验及串口验收。

- 串口为 **COM4（CH340），115200 / 8N1 / 无流控**；COM18 是 J-Link CDC，不是本项目接出的 UART。
- 本次基线已包含之前的 SDHC 回调修正，实际失败点变为 `csr=0x40` 等待 HT 时钟超时。根因是 custom resource 模式直接使用 CRLF NVRAM 文本；已在应用构建阶段转成 NUL 分隔、双 NUL 结尾且按 4 字节补齐的 668 B 数据。
- 只修 NVRAM 后首扫成功、第二次扫描发生 `net_mgmt` 栈溢出；将线程栈从 800 B 提高至 4096 B，并启用栈哨兵。最终测得栈使用 936 B，剩余 3160 B。
- 修复 AIROC HOST_WAKE 回调的逻辑/物理电平混用及忽略 interrupt enable 参数的问题；本次驱动增量保存为 `.agents/patches/airoc-oob-interrupts.patch`。
- 最终正常 UART 镜像在两轮软件复位后 **5/5 次扫描成功**，无 Usage Fault、栈哨兵错误或 HOST_WAKE 误报。维持 4 位 SDIO、最大 25 MHz。
- 最终构建目录为 `build/ra8p1_titan/r7ka8p1kflcac/cm85`，FLASH 375284 B，RAM 247264 B。BIN SHA-256：`4ce6db60b4b1e877fae45b77733aa8209c0134f92eeb0604a620513143703d07`。
- KSO 唤醒初次 CMD52 写入偶尔返回 -EIO，WHD 按既有流程重试后扫描完成；诊断日志保持可见，详见报告。未验收断电冷启动、关联/DHCP 或数据传输。
- 本次保留任务开始前 Zephyr/Infineon 的已有未提交改动；没有修改 Config Area、OFS、OTP 或外部固件分区。
- [完整修复报告、日志、哈希与备份](evidence/wifi-fix-20261108/README.md)。后文均为历史记录，不代表当前仍然没有 STA 接口。

## 历史状态（2026-11-02）：固件下载末尾 SDIO CMD53 回读验证超时

2026-11-02 用户下载镜像后的板端输出已确认：Zephyr Shell 正常启动，但 Wi-Fi 主接口初始化失败，`wifi scan` 因没有默认 STA 接口而失败。

- 关键错误为 `whd_bus_sdio_read_backplane_value()` line 975 返回 `4294967285`，即 32 位无符号显示的 `-11 / -EAGAIN`。
- 这次 backplane read 位于 WHD `whd_bus_sdio_download_resource()` 的固件下载尾部：资源块读取并通过 SDIO 写入后，WHD 写入启动指令，再通过 CMD53 读回校验。当前错误因此指向 SDIO 回读验证，不是 `wifi_firmware_flash_read()` 的 OSPI 资源回调失败；固件数据传输阶段已推进到末尾校验。
- 完整失败日志确认 RA SDHC 在 `00:00:11.519` 打印 `Can not take sem!`；对应 CMD53 路径等待传输完成 semaphore 超时并返回 `-EAGAIN`。当前 `CONFIG_SD_DATA_TIMEOUT=10000`，与启动时序一致。WHD 随后在 `whd_bus_sdio_cmd53()` 返回 `-11`，固件下载中止。
- `airoc_wifi_init_primary` 随后失败，STA net_if 未创建；`wifi scan` 的 `No default interface found for type: STA` 是初始化失败的后果。`whd_deinit` 的 NULL 接口报错也属于失败后的清理路径。
- 用户读取到 SDIO_INFO1=`0x2`、SDIO_INFO1_MASK=`0x6`、SD_ERR_STS1=`0x2000`、SD_ERR_STS2=`0x0`：EXWT bit 15 未屏蔽但采样时未置位；CRCTK=`010b` 是正常 CRC 状态令牌，未见已记录的 CRC/超时错误。
- 后续读取 SD_INFO1=`0x700`、SD_INFO2=`0x2080`。SD_INFO1 的 DAT3 插入/移除标志及 DAT3 状态位置位；应用 overlay 删除了 `card-detect` 属性，这些是 DAT3 状态/历史标志，不能据此判断 Wi-Fi 模块掉线。SD_INFO2 表示 DAT0 当前为高、时钟控制状态就绪，CBSY 与命令/CRC/数据超时错误位均为 0。它们是失败后的快照，不能还原传输期间事件。
- 静态配置核查显示 SDHC1 的 `sdio-int` 使用 ICU 向量 34，驱动将其路由到 RA8P1 的 `SDHIMMC1_SDIO` 事件，并在启动时启用该 IRQ；WHD 的 `sdhc_enable_interrupt(SDHC_INT_SDIO)` 会解除 EXWT 屏蔽。静态设备树/事件映射目前看一致。尚未确定的是 CMD53 线级传输是否完成、EXWT 是否产生，以及 ISR 是否实际进入。
- 下一步需要在 Wi-Fi 启动失败的 CMD53 附近采集 SDIO 总线波形，核对 CLK、CMD、DAT0-DAT3 的命令、响应与数据，再决定修改总线/中断配置或驱动路径。

此前扫描 Shell 与启动日志镜像构建记录如下：

2026-11-01 已在不修改上游 Infineon 模块的前提下完成 WHD 外部固件资源接入：

- `prj.conf` 恢复网络、AIROC、SDIO 依赖，并启用 `CONFIG_AIROC_WIFI_CUSTOM=y`。
- overlay 恢复 SDHI1、P404 REG_ON、P514 HOST_WAKE 和 SDIO 中断节点。
- 应用定义 `wifi_firmware_image` 为外部资源，并通过 `platform_read_external_resource()` 从 `whd-firmware` 分区读取固件。
- CLM/NVRAM 由应用 CMake 生成 `.inc`；没有生成 Wi-Fi 固件 `.inc`。
- pristine 构建成功：`FLASH 375748 / 786432 B`，`RAM 240136 / 1048576 B`。
- Map 中固件句柄仅占 16 B；CLM 为 7222 B，NVRAM 为 710 B，未出现固件数据数组。

当前已完成“主控镜像能够通过 custom resource 访问外部 Flash 固件”的编译验收；尚未下载本次 CM85 镜像并完成板上 SDIO/Wi-Fi 启动验收。

2026-11-02 为扫描结果输出做了应用配置并重新构建：

- `CONFIG_NET_L2_WIFI_SHELL=y` 已包含 Zephyr Shell 命令 `wifi scan`，扫描由 Shell 触发，不需要在 `main()` 中增加扫描调用。
- 扫描结果通过 Zephyr 网络管理事件队列异步交给 Shell。应用将 `CONFIG_NET_MGMT_EVENT_QUEUE_SIZE` 从默认 5 提高到 32，并将队列等待时间从 10 ms 提高到 100 ms，减少串口打印期间的结果丢失。
- 扫描队列配置构建通过：FLASH `375748 / 786432 B`，RAM `242944 / 1048576 B`；该版本哈希见下方最新日志配置构建记录。
- Titan 大板 J-Link 下载器为 S/N `24060501`；已确认 IAR J-Link Commander V8.74 位于 `D:\Program Files\IAR\arm\bin\jlink.exe`。下载命令：`west flash --build-dir F:/zephyr/apps/wifi/build/ra8p1_titan/r7ka8p1kflcac/cm85 --runner jlink --dev-id 24060501 --commander "D:\Program Files\IAR\arm\bin\jlink.exe"`。
- 仍需下载本次镜像并通过串口确认启动。扫描成功标准：Shell 执行 `wifi scan` 后收到 `Scan request done`，并打印可见 AP 的 SSID、信道和 RSSI。此前 SDIO 初始化期间曾出现 Usage Fault，必须以本次启动日志确认是否仍存在。

2026-11-02 根据首次板端串口片段调整了启动日志等级并重新构建：

- 用户日志中每约 10 ms 重复出现的 mutex 行是 Zephyr `LOG_DBG`。通过当前 ELF 的符号和 DWARF 确认：`0x22002868` 是 `z_main_thread`，`0x22006214` 是 `airoc_wifi_data.card.lock`，即 AIROC Wi-Fi 驱动使用的 SDIO 卡互斥锁。该片段表示主线程在反复执行 SDIO 卡访问；锁均正常获取/释放，没有单凭这些行判定死锁的证据。片段没有包含完整启动标记，尚不能判断 Wi-Fi 初始化是否返回。
- `CONFIG_LOG_DEFAULT_LEVEL` 从 4（DEBUG）改为 3（INFO），避免内核 mutex DEBUG 经 UART 立即输出持续刷屏；`CONFIG_FLASH_LOG_LEVEL_DBG=y` 保留。
- 最新构建通过：FLASH `371584 / 786432 B`，RAM `242944 / 1048576 B`；`zephyr.bin` SHA-256 为 `2CF1C2B8F341A4FEBF837AA1813236ABE3E0FFB7BC9D6B20732A6BCCD79E3E48`。
- 需要下载此最新镜像重新观察完整启动日志。若出现 `[boot] reached main` 和 Shell 提示符，再执行 `wifi scan`；若始终没有这些标记，说明初始化仍未走完，应根据新的 INFO/错误日志继续查 SDIO/WHD 初始化。

## 固件存储状态

2026-10-31 已将上游 `43438A1.bin` 写入外部 OSPI Flash 的 `whd-firmware` 分区：

- 分区偏移 `0x02000000`，大小 `512 KiB`；主控映射地址为 `0x92000000`。
- 原始固件大小 `419799 B`，SHA-256 `f85e3feed55c429cf2fc88316dba472647da25622bac6c07ab63807fa0ad875e`。
- 为满足 Flash 的 16 B 写入对齐，末尾补 9 个 `0xFF`，写入大小 `419808 B`；写入镜像 SHA-256 为 `cda3223641e3796ee686a6a7128d0e9545fce250e8a08dc94783a75c0c1c4857`。
- UART 上传期间发现 `CRLF` 的 `LF` 被 Shell bypass 当作第一个固件字节，导致旧写入以 `0x0A` 开头并整体错位。该分区随后重新擦除；[上传工具](tools/upload_whd_firmware.py) 改为只用 `CR` 结束命令，并在上传后自动读回头部 16 B。
- 修正版上传后，头部为 `00 00 00 00 ED 21 00 00 19 21 00 00 19 21 00 00`。随后通过 J-Link/SWD 从 `0x92000000` 只读回 419808 B，SHA-256 与写入镜像一致。读回前后目标均未 halted，没有复位或停核。
- `Read all` 只表示 UART 收够指定长度；整段内容正确是由 J-Link 全量读回 SHA-256 确认的。

此前完成的是“固件文件存入外部 Flash”。本次代码已恢复 Wi-Fi 配置并接入 WHD 外部资源回调；下一步需要下载新的 CM85 镜像，观察板上初始化日志。

## 历史记录：外部 Flash 已清空（2026-10-31）

2026-10-31 用户明确授权通过 Shell 擦除旧板遗留数据。已执行：

```text
flash erase flash-controller@1 0x00000000 0x03FFF000
```

该命令成功，清除了 `0x00000000～0x03FFEFFF`。针对最后 `0x03FFF000～0x03FFFFFF` 的第二条命令被当前驱动以“ending sector 未对齐”拒绝；但擦除前完整备份显示这 64 KiB 已经全为 `FF`。

随后通过 J-Link 对 CPU 映射地址 `0x90000000～0x93FFFFFF` 做 64 MiB 只读扫描：非 `FF` 字节数为 `0`，SHA-256 为 `dd30d9e07e89c1749cd420e998190ab9e31d4b43d27b5862887320ba2a2b8b0f`。CPU 扫描前后均未 halted，未复位、下载或写入。

擦除完成时外部 Flash 全片为空白，原始 64 MiB 备份仍保留在 [flash-audit-20261028-154836](evidence/flash-audit-20261028-154836/)。随后固件已写入上述 `whd-firmware` 分区。

## 历史记录：外部 Flash 只读审计（2026-10-28）

用户已恢复 Flash 迁移，并明确要求助手执行可用区域验证。本轮未改动应用源码、配置、设备树或板上固件。

- 外部 Flash 已由用户接入：W35T51NW、OSPI0/CS1、SPI 模式，CPU 映射基址 `0x90000000`。
- 当前实际配置是 Flash 验证程序：`CONFIG_NETWORKING=n`，Wi-Fi/SDHI 部分已注释；`main()` 输出启动信息后返回，保留 Flash shell。
- 通过 J-Link S/N `24060501`，完整读回并备份 64 MiB；从已运行驱动的 SFDP 与页布局缓存确认容量 64 MiB、16384 个 4 KiB 擦除页。当前配置的写入块为 16 B。
- `0x02000000～0x0207FFFF`（512 KiB）在只读审计期间完整读取三次，全部为 FF；此后由应用规划为 Wi-Fi 固件分区并完成写入校验。
- 擦除前偏移 0、16 MiB 和 63 MiB 等位置存在旧数据，且最后 64 KiB 为空白；随后用户授权擦除全片，原始内容由审计备份保留。
- 扫描前后的 768 KiB Code MRAM 完全一致；CPU 结束时仍运行，未执行复位、halt、烧录或 Flash 擦写。
- [完整报告、区域表与原始备份](evidence/flash-audit-20261028-154836/README.md)；可复用工具为 [flash_readonly_audit.py](tools/flash_readonly_audit.py)。

以下构建占用和排障记录属于此前的 Wi-Fi 固件基线，不代表当前关闭网络后的 Flash 验证程序。

## 当前目标与边界

先打通 Titan 大板的 Wi-Fi STA 路径，作为后续局域网数据传输和 WireGuard 的基础。

当前应用为 `F:\zephyr\apps\wifi`。此前讨论过的 `apps\wireguard` 不是本轮实际构建目录；硬件为 Titan 大板，不是 Titan Mini。

## 已完成的构建排障

1. 启用 `CONFIG_SHELL=y`，解决 Wi-Fi shell 选择 `SHELL_GETOPT` 时的 Kconfig 依赖警告。
2. Wi-Fi 固件与 CLM 已进入当前构建；应用 [CMakeLists.txt](../CMakeLists.txt) 在 `find_package(Zephyr ...)` 前显式指定 CLM/NVRAM 路径。当前上游 CYW43438 分支只自动选择固件，没有自动补齐这两个路径。
3. [应用 overlay](../boards/ra8p1_titan_r7ka8p1kflcac_cm85.overlay) 接入 SDHI1/SDIO、P404 REG_ON、P514 HOST_WAKE 及对应中断；保留了原 OFS/OTP 节点禁用配置。
4. [prj.conf](../prj.conf) 设置 128 KiB 堆，启用日志、Wi-Fi shell 和网络 shell。
5. 曾在链接时超出 FLASH 6516 字节。用户选择在 `prj.conf` 关闭以下有线网口驱动后，当前构建已成功产生 ELF/HEX/BIN：

   ```ini
   CONFIG_ETH_RENESAS_RA_RMAC=n
   CONFIG_MDIO_RENESAS_RA_RMAC=n
   CONFIG_PHY_REALTEK_RTL8211F=n
   ```

   当前采用 Kconfig 裁剪方案，并未追加关闭有线网口的 overlay。AIROC Wi-Fi 仍需要 `NET_L2_ETHERNET`，不能将这个共享网络层一并关闭。

## 此前 Wi-Fi 构建结果

Zephyr 版本为 `4.5.0-rc3`，当前构建标识为 `v4.5.0-rc3-3-g2a9e8ac155a3`；编译使用调试优化 `-Og`。

以下数据来自用户提供的成功构建输出；本次记录时同时核对了生成文件与配置，没有重新构建：

| 区域 | 已用 | 区域大小 | 使用率 |
|---|---:|---:|---:|
| FLASH（当前 CM85 的 MRAM 区域） | 770952 B | 768 KiB | 98.03% |
| RAM | 230264 B | 1 MiB | 21.96% |
| ITCM | 0 B | 128 KiB | 0% |
| DTCM | 0 B | 128 KiB | 0% |
| SDRAM | 0 B | 64 MiB | 0% |

- FLASH 剩余 `15480 B`，约 `15.1 KiB`，后续新增功能余量较小。
- `zephyr.bin` 当前长度为 `770952 B`，与上述 FLASH 使用量一致。
- [最终 Map](../build/ra8p1_titan/r7ka8p1kflcac/cm85/zephyr/zephyr.map) 和 [最终设备树](../build/ra8p1_titan/r7ka8p1kflcac/cm85/zephyr/zephyr.dts) 位于构建目录，重新构建时会更新，不是永久归档证据。

当前构建命令：

```powershell
west build -b ra8p1_titan/r7ka8p1kflcac/cm85 "F:/zephyr/apps/wifi" -p --build-dir "F:/zephyr/apps/wifi/build/ra8p1_titan/r7ka8p1kflcac/cm85" -- -DCONFIG_DEBUG_OPTIMIZATIONS=y -DCONFIG_DEBUG_THREAD_INFO=y
```

## Wi-Fi 路径仍待验收

- 恢复 Wi-Fi 配置后，需要处理此前 SDIO 初始化期间的 Usage Fault；根因尚未证实。
- Wi-Fi 扫描、关联、取址和数据传输尚未验收，Flash 读取成功不代表 Wi-Fi 路径已打通。
- 此前 Wi-Fi 配置为 `NET_IPV6=y`，`NET_IPV4` 未启用。普通 IPv4 局域网方案仍需配置 IPv4/DHCPv4，并验证实际取址流程。
- 128 KiB 堆是初始预算，尚未经 Wi-Fi 运行验证。
- 外部 Flash 迁移的后续步骤见 [PLAN.md](PLAN.md)。
