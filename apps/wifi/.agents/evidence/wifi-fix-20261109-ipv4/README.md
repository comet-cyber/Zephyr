# Wi-Fi IPv4 / DHCPv4 启用

日期：2026-11-09。项目：`F:\zephyr\apps\wifi`。

## 修改与行为

应用 `prj.conf` 显式启用以下配置：

```ini
CONFIG_NET_IPV4=y
CONFIG_NET_UDP=y
CONFIG_NET_DHCPV4=y
CONFIG_WIFI_STA_AUTO_DHCPV4=y
```

AIROC 驱动在 STA 关联成功后调用 `net_dhcpv4_restart(iface)`，因此用户执行
`wifi connect -s "SSID" -p "密码" -k 1` 后，DHCP 客户端会自动申请 IPv4 地址。
可以用 `wifi status` 看关联状态、`net iface` 看 IPv4 地址、网关和 DHCPv4 状态。
`Connection requested` 不等于关联成功；关联成功也不等于 DHCP 租约已取得。

## 验证

- 工作区 west 构建通过，FLASH 399900 B，RAM 248712 B。
- [最终配置核对](enabled-config.txt) 中上述四项均为 y。
- [构建日志](../wifi-fix-20261109-ipv4-build.log)。
- 已通过 IAR J-Link Commander 下载到 Titan 大板 CM85；[下载日志](program.log) 显示编程与校验成功。
- [二次独立 SWD 读回](post-download.json) 比较了全部 34 个有文件数据的分配段，完全一致，结束时 CPU 运行。
- 最终 BIN SHA-256：`be480a92e28d00d35ced00c43a36128e112cd86b566ffc4fc139383beaf5430b`。
- Code MRAM 下载前完整备份为 [mram-before.bin](mram-before.bin)，[镜像范围审计](preflight.json) 确认只下载 Code MRAM；未写配置区或外部 Flash。
- COM4 释放后已完成软件复位启动、镜像 34 段校验和扫描复测；[启动/扫描日志](uart-boot-scan/uart.txt)、[结果](uart-boot-scan/result.json) 均通过，无 Fatal Error。
- 最初按用户提供的 `Redmi_5G` 连接，返回 `33555456 / 0x02000400 = WHD_NETWORK_NOT_FOUND`；[该次连接日志](wifi-connect-redmi.txt) 已隐藏密码。[再次扫描](redmi-rescan.txt) 发现 `Redmi_514`，随后用户确认此名称才是目标 SSID。
- 使用正确 SSID 后，[关联与 DHCP 日志](wifi-connect-redmi514.txt) 确认状态 COMPLETED、WPA2-PSK、2.4 GHz、信道 6、RSSI -39 dBm，BSSID 为 `44:DF:65:A3:75:5C`。
- DHCPv4 自动启动，一次取得 `192.168.28.198/255.255.255.0`，网关及 DHCP 服务器为 `192.168.28.1`，状态 bound；租期 43200 秒，续租时间 21600 秒。两次 `net iface` 查询均确认地址与租约。
- [网关 ping 与栈使用日志](gateway-ping-stacks.txt)：`net ping -c 3 192.168.28.1` 共 3 发 3 收、0% 丢包，RTT 最小/平均/最大为 23.38/24.43/25.60 ms。
- `kernel thread stacks` 确认 `net_mgmt` 使用 936/4096 B、剩余 3160 B；WHD 使用 1308/5120 B。本次连接与 ping 日志中无 Fatal Error 或栈溢出。

## 验收范围与结束状态

已完成软件复位启动、扫描、目标热点关联、自动 DHCPv4 取址及本地网关 ICMP 通信。断电冷启动、长期稳定性、应用层数据传输与互联网访问未验收。

连接及 ping 期间仍可见 KSO 唤醒 CMD52 写入 `opcode=52 arg=0x9a003e01 ret=-5` 的诊断日志；WHD 现有重试后本次通信成功，未修改或隐藏这些日志，不宣称底层错误已全部消除。

测试结束保持板子连接 `Redmi_514`，串口 COM4 已关闭释放。密码只用于用户授权的串口连接命令，未写入源码或配置；保存的串口连接日志已脱敏。

构建产物：`build/ra8p1_titan/r7ka8p1kflcac/cm85/zephyr/zephyr.elf`。
