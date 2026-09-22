# SAFETY

> 更新日期：2026-09-22
>
> 本文件约束所有 `west flash`、J-Link、OpenOCD、RFP 和任何写目标存储器的操作。

## 红线

1. **未经用户在当前消息里明确同意，不下发任何 Zephyr 或实验固件。**
2. **禁止写入 Config Area、Option-setting、OTP、分区、DLM、密钥或生命周期相关区域。**
3. **禁止启动 Device Partition Manager 的 SCI 连接。**
4. 出现 TrustZone mismatch、Option-setting、DLM、OTP、key、分区提示时：停下，保存日志，先审计，不确认。
5. 不升级 J-Link 探针固件；探针身份异常（显示未来编译日期等）时只使用已验证功能，不“顺便升级”。

## 允许写入的范围

第一次以及后续日常 Zephyr 下载，默认只允许：

- Code MRAM：`0x02000000` … `0x02100000`（1 MB 可用 MRAM）

SRAM `0x22000000` 是运行期加载/数据，不是下载器应擦写的持久配置区。

明确排除：

| 区域 | 例子 |
| --- | --- |
| Option-setting / OFS | `0x02C9F000` 一带，含 `OFS1_SEC@0x02C9F0C0` |
| OTP / PBPS | `0x02E17700` 一带 |
| 其它配置/分区窗口 | 任何不在 Code MRAM 窗口内的 PHDR / HEX 记录 |

板上已有配置：`OFS1_SEC@0x02C9F0C0 = 0xFEFFFFFF`（`SWDBG` 已打开）。不要用 Zephyr 默认值覆盖它。

## 当前默认镜像为什么危险

`F:\zephyr\zephyr\soc\renesas\ra\ra8p1\sections.ld` 在独立应用（未走 MCUboot 应用镜像）时会链入 `option_setting_*` 段。

2026-09-04 的 blinky `zephyr.hex` 已确认包含：

```text
0x02C9F040  FFFFFFFF
0x02C9F044  EFFFFFFF
0x02C9F074  FFFFFFFF
0x02C9F0C0  FFFFFFFD    ← OFS1_SEC，会改配置区
0x02C9F0C4  FFFFFFFF
0x02C9F120 / 0x02C9F124 / 0x02C9F200
0x02E17700  FFFF…       ← OTP PBPS 段
```

`zephyr.bin` ≈ 14.1 MB，是被这些高地址撑开的 padded 文件。即使用 J-Link `--dt-flash=y`，也不要把这个 bin 交给下载器。

在守门脚本判定 PASS 之前，这条命令视为危险操作：

```text
west flash
```

## 下载前检查单

1. 用户在**当前消息**里明确说可以下载。
2. 已备份当前 Code MRAM；备份文件不含 Config Area。建议至少覆盖现有固件实际范围，第一次更稳妥备份整段 `0x02000000-0x02100000`。
3. 对将要下载的 `zephyr.hex` 或 ELF 跑守门脚本。
4. 守门结果必须是：所有 load 段物理地址都在 Code MRAM 内；OFS/OTP 段数量为 0。
5. 使用 J-Link、设备名 `R7KA8P1KF_CPU0`。CM33 才是 `R7KA8P1KF_CPU1`，入门阶段不要下到 CPU1。
6. 下载后只核对 Code MRAM / PC / 串口或 LED，不把配置区“顺便校验成和 hex 一致”。

## 守门脚本要求

脚本尚未落地。落地后应做到：

- 解析 ELF program headers 与 Intel HEX 扩展线性地址
- 白名单：`0x02000000-0x02100000`
- 命中 `0x02C9xxxx`、`0x02E1xxxx` 或其它窗口 → `FAIL` 且退出码非 0
- 打印每个越界段的地址和大小
- 不修改目标板，只审计文件

在脚本存在前，人工最低限度：打开 `zephyr.stat` 或 `readelf -l`，确认没有 `0x02c9` / `0x02e1` 的 LOAD；再搜 hex 是否出现 `:0200000402C9` 或 `:0200000402E1`。

## 恢复

裸机可恢复材料在：

`F:\embedded_systems_learning\projects\titan-mini-system-monitor`

已知对照（裸机 Stage 0 原始 Code MRAM，供恢复对照，不是 Zephyr 目标）：

- 范围：`0x02000000-0x020011FF`
- SHA-256：`3F13821669C519682EE74BFAFEEA6676EC079C6FBCC5797537D9927FD4E2CDE4`
- `vector[0]=0x22000408`，`vector[1]=0x0200093D`，`0x02000FFC=0x06040000`

当前板上更可能是 e² studio Stage 2 固件。第一次下 Zephyr 前应重新读回并保存**当前** Code MRAM，不要假设 Stage 0 仍在板上。

## 调试器

- 主链路：J-Link，S/N `601012527`，SWD 1000 kHz，`R7KA8P1KF_CPU0`
- OpenOCD / Horco CMSIS-DAP：仅诊断与恢复
- 不要为了 Zephyr 去点 RA Partition Manager、RFP 的 Initialize/DLM、或 SCI boot 写配置

需要真实波形时，再请用户接 DSLogic U2Pro16。
