# Titan Wi-Fi 扫描修复与板上验收

日期：2026-11-08。项目：`F:\zephyr\apps\wifi`。

## 验收结果

Titan 大板、J-Link S/N `24060501`、CM85，串口 **COM4 / CH340 / 115200 / 8N1 / 无流控**。
最终正常 UART 镜像在两轮软件复位后共执行 5 次 `wifi scan`，全部输出热点条目和
`Scan request done`，没有 Usage Fault、栈哨兵错误或 `Unexpected interrupt event`。
SDIO 配置保持 4 位、最大 25 MHz。未进行断电冷启动、Wi-Fi 关联、DHCP 或数据传输验收。

- [连续 3 次扫描](uart-final-verified/uart.txt)、[机器可读结果](uart-final-verified/result.json)
- [复位后 2 次扫描](uart-final-reboot/uart.txt)、[机器可读结果](uart-final-reboot/result.json)
- [线程栈测量](thread-stacks.txt)：`net_mgmt` 使用 936 / 4096 B，剩余 3160 B。
- [最终构建日志](final-build.log)：FLASH 375284 B，RAM 247264 B。
- [源码与镜像哈希](final-files.json)

## 根因与修复

1. **当前启动失败：NVRAM 编码错误。** 应用启用了 `RESOURCE_READ_FROM_C_FILE`，
   WHD 会原样读取 `wifi_nvram_image[]`，不会执行普通资源路径里的换行转换。
   原生成文件包含 CRLF 文本，共 710 B，没有正确的 NUL 条目分隔。
   基线启动在 `csr=0x40` 等待 HT 时钟 2500 次后失败；历史 CMD53 超时在本次基线中未复现。
   `scripts/generate_nvram.py` 现在生成 43 个 NUL 分隔条目，双 NUL 结束，按 4 B 补齐，共 668 B。
   CMake 显式跟踪源 NVRAM 与脚本依赖。LF/CRLF、终止符、对齐和非法输入的 3 组回归测试通过。

2. **连续扫描崩溃：事件线程栈不足。** 只修 NVRAM 后，第一次扫描成功，第二次在
   `net_mgmt` 线程发生 Usage Fault；[故障栈快照](fault-mgmt-stack.json) 显示原 800 B 栈已无余量。
   最终实测高水位 936 B，超过旧预算。应用设置 `CONFIG_NET_MGMT_EVENT_STACK_SIZE=4096`，
   并启用 `CONFIG_STACK_SENTINEL=y`。

3. **HOST_WAKE 误报：物理/逻辑电平混用。** `wifi-host-wake-gpios` 为 ACTIVE_LOW，
   `gpio_pin_get_dt()` 会把低电平转换成逻辑 1，而 WHD 的 falling-edge 检查期待物理 0。
   `airoc_whd_hal_sdio.c` 改用 `gpio_pin_get_raw()`；同时修复
   `whd_bus_sdio_enable_oob_intr()` 忽略 `enable` 参数的问题，使屏蔽请求真正关闭中断。

## 既有改动与依赖边界

进入本次任务时 Zephyr 与 Infineon 模块已有未提交改动：RA SDHC 诊断、FSP 回调事件位判断、
AIROC bus width/初始化错误返回，以及 WHD 信息日志。本次保留这些改动，没有声称 NVRAM 修复
能够单独替代历史 SDHC 修复。本次没有修改 `sdhc_renesas_ra.c` 或 Infineon 模块。

- Zephyr HEAD：`2a9e8ac155a3f2fd85d4559753be86a47b44ccf0`
- hal_infineon HEAD：`eae914ed1ad0b54af28191d13da9b8e98fb5cb2b`
- hal_renesas HEAD：`0c0beea010e78899c8ffbfd995cbfe50d3e6595e`
- [本次 OOB 补丁](../../patches/airoc-oob-interrupts.patch) 相对于任务开始时驱动版本；反向检查通过。
- [Zephyr 全部本地差异](zephyr-local.patch)、[Infineon 全部本地差异](infineon-local.patch)
  用于重现当前工作树，包含历史改动；不要不加检查地重复应用。

## 剩余日志的含义

扫描前偶尔有 CMD52 `arg=0x9a003e01 ret=-5`，对应 Function 1 的 `SDIO_SLEEP_CSR@0x1001F`
唤醒写入。WHD `whd_chip.c:whd_kso_enable()` 明确允许初始 KSO 写入失败并重试，
`airoc_whd_hal_sdio.c` 也对该地址保留特殊错误返回。最终 5 次扫描均在随后完成。
当前保留 RA SDHC 历史诊断输出，未通过隐藏日志或禁止芯片休眠来规避它；不能把这些日志说成
没有任何底层重试，也不能据此把已完成的扫描误判为失败。

## 下载与备份

[任务开始前完整 Code MRAM 备份](baseline/mram-before.bin) 覆盖
`0x02000000..0x020FFFFF`，SHA-256：
`2f715f1f0fbd110fda47fd1110125f258a60f37e1ac0af77bef07c663f0fe95c`。
没有下载 Config Area、OFS、OTP 或外部 Flash。

早期直接 halt 后调用 DLL 下载出现编程失败；使用 IAR J-Link Commander 的复位/停核流程后成功，
日志在 [program.log](program.log)。诊断工具已改为下载前 reset/halt。
最终下载成功后曾因 ELF 段内 TLS NOBITS 空洞的 4 B 未写入而触发过严的逐段校验；
工具现在仍审计所有文件型 LOAD 地址，但逐一读回比较实际有文件数据的 34 个分配段，全部通过。
该调整只排除未编程的 NOBITS/段间填充，不排除任何代码或数据段。

最终镜像：`build/ra8p1_titan/r7ka8p1kflcac/cm85/zephyr/zephyr.elf`。
最终 BIN SHA-256：`4ce6db60b4b1e877fae45b77733aa8209c0134f92eeb0604a620513143703d07`。

## 复测入口

关闭占用 COM4 的串口程序。使用工作区的 Python/SDK 环境重新构建：

```powershell
& 'F:\zephyr\.venv\Scripts\west.exe' build -d 'F:\zephyr\apps\wifi\build\ra8p1_titan\r7ka8p1kflcac\cm85'
& 'F:\zephyr\.venv\Scripts\python.exe' 'F:\zephyr\apps\wifi\scripts\test_generate_nvram.py'
```

用户日常操作只需打开 COM4，115200、8N1、无流控，发送 `wifi scan`（CR 结束）。
维护者可用 `.agents/tools/check_wifi_board.py --elf <当前ELF> --output <新证据目录>`
审计/校验当前镜像并执行一次扫描；`--reset` 会复位，`--flash` 会备份、下载并复位。
工具会在退出时关闭串口与 J-Link；日志中的扫描成功数不匹配时返回失败。
