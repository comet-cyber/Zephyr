# PLAN

> 更新日期：2026-09-22

## 学习原则

沿用用户的项目驱动螺旋，不把 Zephyr 手册当课程表：

1. 当前增量 → 最少必要原理 → 代码边界 → 板上测量/日志 → 复盘 → 下一增量。
2. 一次大约引入 3～5 个新概念。
3. 先做出可观察结果，再沿一条路径看 Device Tree、Kconfig 或驱动。
4. 不逐行读 HAL/FSP，不要求记寄存器表。
5. 双核、MCUboot、以太网、NPU 等只在真实需求出现时进入。

验收标准：能复述“这段代码为什么能在这块板上动”，并留下构建命令、镜像审计结果和板上现象。无证据不标 `verified`。

## 默认目标

| 项 | 值 |
| --- | --- |
| 板 | `ra8p1_titan_mini/r7ka8p1kflcac/cm85` |
| 核 | Cortex-M85 / CPU0 |
| 控制台 | UART2，115200，外接 USB-UART |
| 第一个可见结果 | 安全下载后的 `hello_world` 或 `blinky` |
| 应用位置 | 长期代码放 `F:\zephyr\apps\<name>\`，入门阶段可用上游 sample，但不要改上游 sample 当工程 |

## Z0  工作区与下载安全

**增量：** 搞清 west 工作区、board target、构建产物，并堵住 RA8P1 配置区误写。

**概念：** west topdir / manifest；board target 与 SoC qualifier；`west build` ≠ `west flash`；Code MRAM vs Option-setting/OTP；Intel HEX 扩展地址。

**要做：**

- 固定环境：`.venv` + `F:\zephyr\.sdk`
- 写下载守门脚本：拒绝任何落在 `0x02000000-0x02100000` 之外的 load 段
- 用 overlay 关闭 `option_setting_*` DT 节点
- 重编后审计 hex/elf，确认无 `0x02C9xxxx` / `0x02E1xxxx`
- 备份当前板上 Code MRAM（排除 Config Area）

**完成证据：** 守门脚本对“带 OFS 的旧 blinky”失败、对“关掉 OFS 的新镜像”通过。尚未下载也可以结束 Z0 的脚本部分；第一次下载必须另获用户同意。

## Z1  第一张可恢复的 Zephyr 映像

**增量：** 在用户明确同意后，把纯 Code MRAM 镜像下到 CPU0，并看到 hello 或 LED。

**概念：** `west flash --runner jlink`；J-Link 设备名 `R7KA8P1KF_CPU0`；复位后 PC/VTOR；UART2 控制台或 `led0`。

**要做：**

- 优先 `samples/hello_world` 或 `samples/basic/blinky`
- 只下审计通过的 hex/elf，不用 padded `zephyr.bin`
- 记录串口输出或 LED1（P108，低有效）现象
- 保留如何回到裸机 Stage 2 / Stage 0 映像的说明

**完成证据：** 守门 PASS + J-Link 下载 + 板上可观察结果 + 恢复路径写明。

## Z2  GPIO 与 Device Tree

**增量：** 理解 `blinky` 为什么能点 LED1，必要时改 overlay 点 LED2/LED3。

**概念：** `aliases { led0 = &led1; }`；`GPIO_DT_SPEC_GET`；`GPIO_ACTIVE_LOW`；`gpio-leds` 节点；board overlay。

**完成证据：** 能指着 DTS 说出 LED 引脚和极性，并能用 overlay 换灯，而不是改 `main.c` 写死寄存器。

## Z3  按键输入

**增量：** 用板载 SW1（P201）控制 LED，先轮询，需要时再进中断。

**概念：** `gpio-keys`；`DT_ALIAS(sw0)`；输入极性/上拉；轮询 vs GPIO 回调。中断消抖放到本阶段末尾或下一阶段，不要和 DT 入门绑死。

**完成证据：** 按下 SW1 有稳定可观察的 LED/日志变化。

## Z4  树外应用骨架

**增量：** 把可运行的最小应用搬出 `zephyr/samples`，放到 `F:\zephyr\apps\<name>`。

**概念：** 树外应用的 `CMakeLists.txt` / `prj.conf` / `boards/` overlay；west 构建路径；Kconfig 与 DTS 的分工。

**完成证据：** 不修改上游 sample 也能重复构建、审计、下载同一功能。

## 明确暂缓

- CM33 第二核与 `--sysbuild` 双核启动
- MCUboot
- 以太网 PHY / ESWM
- SDHI、USB、SDRAM、OSPI
- Ethos-U55
- 把 Zephyr 接到 HWT101。注意：裸机 Stage 2 用的是 `IIC0 / P409 / P410`，Zephyr 板文件默认 `IIC1 / P512 / P511`，不能假设引脚相同

## 和裸机路线的边界

`F:\embedded_systems_learning` 继续服务系统监视器项目。本仓库只服务 Zephyr。需要对照板级资料时可以读 RT-Thread BSP 和裸机证据，但不要把 FSP 工程改造成 Zephyr，也不要把 Zephyr 应用写回 IAR/e² studio 目录。
