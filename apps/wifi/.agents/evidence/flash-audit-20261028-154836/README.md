# Titan 外部 Flash 只读验证

日期：2026-10-28T15:48:36.552718+08:00。本轮由用户明确授权助手执行 Flash 可用区域验证。

## 结论与边界

外部 Flash 的 64 MiB 地址空间已完整读回。发现多个连续空白区，后续 Wi-Fi 固件分区优先考虑以下候选：

- 设备内偏移：`0x02000000～0x0207FFFF`，长度 512 KiB。
- CPU 映射地址：`0x92000000～0x9207FFFF`。
- 512 KiB 的每个字节均为 `0xFF`；全片读取一次后，对候选区另外完整读取两次，三次一致。
- CYW43438 固件 419799 B 可放入该大小的分区；本轮没有写入固件。

**空白是读回状态，不能证明厂家逻辑分区未预留该空间。尚未核实原厂逻辑分区，也未执行擦除/写入测试。**

## 容量、页布局和现有数据

从已运行驱动的 RAM 缓存读取 SFDP 和页布局，并用已匹配的构建 ELF 定位结构体：

- SFDP 签名 `SFDP`；密度 DWORD 为 `0x1FFFFFFF`，对应 67108864 B（64 MiB）。
- 驱动当前报告单一区域，16384 个擦除页，每页 4096 B，覆盖整个 64 MiB。
- 当前构建配置的最小写入块为 16 B；当前 SPI 模式下驱动校准扇区大小为 0。
- 偏移 0 的 `MODL` 头和偏移 `0x01000000` 的数据与用户的串口读回一致。
- 全片最后一个非 FF 字节在 `0x03F000FF`。**63 MiB 位置 `0x03F00000` 的页也有原有数据，应保留。**这些数据的用途未确认。
- 保守排除最后 64 KiB：`0x03FF0000～0x03FFFFFF`，供后续可能的 DDR/OPI 校准布局评估。

全片中，按 4 KiB 页边界统计，至少 512 KiB 的连续全 FF 区域如下。它们都是候选空白范围，不是已确认的逻辑空闲分区：

| 起始偏移 | 结束偏移（含） | 长度 |
|---|---|---:|
| `0x0047D000` | `0x00518FFF` | 624 KiB |
| `0x00A89000` | `0x00B84FFF` | 1008 KiB |
| `0x00BBB000` | `0x00FFFFFF` | 4372 KiB |
| `0x01001000` | `0x03EFFFFF` | 48124 KiB |
| `0x03F01000` | `0x03FFFFFF` | 1020 KiB |

最后一个范围包括上述保留尾部；不能直接将整个范围划作分区。完整的逐段分类见 [ranges.csv](ranges.csv)。

## 执行方式与验证

- J-Link/SAM-ICE S/N `24060501`，目标 `R7KA8P1KF_CPU0`，使用 IAR 自带 J-Link DLL 8.74。
- 借助现有应用已经初始化的 OSPI 映射窗口 `0x90000000`，通过 SWD 读取。
- SWD 先以 1000 kHz 读取非空白参考数据，再与 4000 kHz 结果比较一致后执行全片读取。
- COM34 被现有程序占用；未关闭用户的串口程序，未依赖串口执行扫描。
- 全片扫描及复核耗时约 409.1 秒。
- 扫描前后的 768 KiB Code MRAM 读回逐字节一致；23 个已分配的 ELF 文件数据段/节与实际 MRAM 内容一致。ELF 段间 4 字节填充不计入节内容比较。
- CPU 在连接、扫描和结束时均为运行状态；未执行 halt、复位、下载或 Flash 擦写。
- 原 `src/main.c`、`prj.conf`、板级 overlay 和 CMake 未修改。

## 证据文件

- [audit.json](audit.json)：扫描参数、范围、候选区和校验结果。
- [audit.log](audit.log)：完整读取进度和复核日志。
- [driver-geometry.json](driver-geometry.json)：运行中驱动的 SFDP/页布局读回。
- [elf-validation.json](elf-validation.json)：构建 ELF 与扫描前 MRAM 的节内容匹配结果。
- [external-flash.bin](external-flash.bin)：64 MiB 外部 Flash 完整原始备份。
- [mram-before.bin](mram-before.bin)：扫描前 768 KiB Code MRAM 读回。
- [candidate-readback.bin](candidate-readback.bin)：512 KiB 空白候选区读回。
- [checksums.sha256](checksums.sha256)：上述三个二进制文件的 SHA-256。
- 可复用只读工具：[flash_readonly_audit.py](../../tools/flash_readonly_audit.py)。

外部 Flash 备份 SHA-256：`a91aaf1a9feef8ed1cd2b386385349d52975f053e57b4cf1885f8713173ebb95`。

## 2026-10-31 擦除结果

用户确认旧板遗留数据不再需要后，通过 Shell 执行：

```text
flash erase flash-controller@1 0x00000000 0x03FFF000
```

擦除成功。该驱动对以容量末尾为结束地址的擦除请求存在边界检查限制，因此第二条最后 4 KiB 擦除命令被拒绝；擦除前的完整备份显示最后 64 KiB 已经为空白。

随后 J-Link 对完整 64 MiB 映射区进行只读扫描，结果为：

- `non_ff_bytes = 0`
- SHA-256：`dd30d9e07e89c1749cd420e998190ab9e31d4b43d27b5862887320ba2a2b8b0f`
- CPU 扫描前后均为运行状态
- 未执行复位、halt、下载或额外写入

因此当前外部 Flash 全片已确认为 `0xFF`，可以重新写入 Wi-Fi 固件。原始数据备份仍保留，擦除后的扫描证据见 [post-erase-scan.json](post-erase-scan.json)。

## 下一步

保留现有数据与完整备份；确认候选区的逻辑归属后，再定义 Wi-Fi 资源分区并做有备份的局部擦写/读回验证。本轮未实现 WHD 外部资源回调，也未解决此前的 Wi-Fi Usage Fault。
