# Wi-Fi 应用持久上下文

更新日期：2026-11-09（Asia/Shanghai）。

- 项目：`F:\zephyr\apps\wifi`
- 硬件：Titan 大板，`ra8p1_titan/r7ka8p1kflcac/cm85`，板载 CYW43438 Wi-Fi。
- [当前状态与构建基线](STATUS.md)
- [IPv4 / DHCPv4 配置与下载验证](evidence/wifi-fix-20261109-ipv4/README.md)
- [后续计划与 Flash 迁移](PLAN.md)
- [外部 Flash 全片只读验证与候选分区](evidence/flash-audit-20261028-154836/README.md)
- [外部 Flash 擦除后全片验证](evidence/flash-audit-20261028-154836/post-erase-scan.json)
- [CYW43438 固件 UART 上传工具](tools/upload_whd_firmware.py)

- [Wi-Fi 扫描修复与 COM4 验收](evidence/wifi-fix-20261108/README.md)
- [板上校验/串口扫描工具](tools/check_wifi_board.py)

## 工作约定

- 历史上由用户亲自动手、助手指导；2026-11-08 用户明确授权助手直接修复本应用，已完成代码修改、构建、板上下载与扫描验收。后续遵循用户当前指令。
- 用户随后恢复外部 Flash 迁移，并明确授权助手执行 Flash 可用区域验证；本轮已完成全片读取、备份和空白候选区复核。
- 2026-10-28 的 J-Link/SWD 全片审计是只读操作，未复位、下载或擦写；详见历史审计报告。
- 应用 overlay 将外部 Flash 偏移 `0x02000000～0x0207FFFF`（512 KiB）定义为 `whd-firmware`；2026-10-31 已写入 CYW43438 固件并完成整段读回校验。
- 2026-10-31 用户授权清空旧数据后，通过 Shell 擦除外部 Flash，并用 J-Link 确认全片为空白；随后仅在上述固件分区写入 Wi-Fi 固件。
