# BOARD  ra8p1_titan_mini

> 更新日期：2026-09-22
>
> 来源：`F:\zephyr\zephyr\boards\ruiside\ra8p1_titan_mini\` 与 2026-09-04 blinky 构建信息。未单独做板上复测的条目不标 verified。

## 标识

| 项 | 值 |
| --- | --- |
| 板名 | `ra8p1_titan_mini` |
| 厂商目录 | `boards/ruiside/ra8p1_titan_mini` |
| SoC | Renesas `R7KA8P1KFLCAC`（文档常用 `R7KA8P1`） |
| 默认 target | `ra8p1_titan_mini/r7ka8p1kflcac/cm85` |
| 第二核 target | `ra8p1_titan_mini/r7ka8p1kflcac/cm33` |
| J-Link CPU0 | `R7KA8P1KF_CPU0` |
| J-Link CPU1 | `R7KA8P1KF_CPU1` |
| 官方板文档 | `boards/ruiside/ra8p1_titan_mini/doc/index.rst` |
| 板仓库（参考，非本工作区） | https://github.com/RT-Thread-Studio/sdk-bsp-ra8p1-titan-mini |

还有一块更大的 `ra8p1_titan`（非 Mini）。本学习轨只用 Mini。

## 核与内存

- CPU0：Cortex-M85，最高约 1 GHz，Zephyr 入门只用它
- CPU1：Cortex-M33，最高约 250 MHz，需要 `--sysbuild` 由 CM85 拉起，暂缓
- Code MRAM 可用窗口：`0x02000000-0x02100000`（1 MB）
- SRAM 可用窗口：`0x22000000-0x221A0000`（1664 KB）
- CM85 默认：`zephyr,flash = &code_mram_cm85`，`zephyr,sram = &sram0`
- CM85 DTS 还划了 MCUboot 分区（boot 64K + slot0/slot1 各 344K + storage 16K）。入门不启用 MCUboot 时，应用仍从 Code MRAM 起点链接；分区节点先当地图，不要当成必须使用的启动链

## 控制台

两边核的 Zephyr console / shell 都是 **UART2（SCI2）**，115200。

| 功能 | 引脚 | pinctrl |
| --- | --- | --- |
| UART2 TX | P801 | `RA_PSEL_SCI_2, 8, 1` |
| UART2 RX | P802 | `RA_PSEL_SCI_2, 8, 2` |

板上没有把 UART2 接到调试 USB 当 CDC。读日志需要外接 USB-UART 到这两根线。这和裸机阶段用过的 USBFS CDC 演示不是同一条路径。

## LED 与按键

均来自 `ra8p1_titan_mini.dtsi`，低有效。

| 节点 | 引脚 | CM85 alias | 备注 |
| --- | --- | --- | --- |
| `led1` | P108 `ioport1 8` | `led0` | 裸机 Stage 1 验证过的绿 LED |
| `led2` | P109 `ioport1 9` | blinky overlay 里的 `led1` | |
| `led3` | P110 `ioport1 10` | blinky overlay 里的 `led2` | |
| `button0` / SW1 | P201 `ioport2 1` | `sw0` | 文档：USER/BOOT，port IRQ4 |
| `button1` / SW2 | P008 `ioport0 8` | CM33 的 `sw0` | CM85 DTS 里默认 disabled |

`samples/basic/blinky/boards/ra8p1_titan_mini.overlay` 只是补了 `led1`/`led2` alias，CM85 的 `led0` 仍是 LED1/P108。

## 和裸机工程不同的引脚

裸机 Stage 2 HWT101：`IIC0 / P409(SDA) / P410(SCL)`。

Zephyr Mini 板文件默认：

- `iic1`：P512 / P511
- 尚未在板文件里启用 `iic0`

以后如果在 Zephyr 里接 HWT101，必须先对原理图和 overlay，不能沿用“板文件已经开了 I2C”的假设。

## 其它已在 DTS 打开、入门先不用的东西

CM85 目标还启用了：IIC1、USBFS gadget、SDHI0、ESWM、ETH1 + RTL8211F、SDRAM、TRNG、ULPT 定时器。

这些会把默认镜像变大、把时钟树变复杂。Z1/Z2 若构建偏慢或外设 init 干扰 hello/blinky，可以用 overlay 关掉无关节点，而不是一上来就学以太网。

## 构建时看到的时钟

blinky `.config` 中 `CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC=1000000000`，与 M85 1 GHz 设定一致。这是 Kconfig 事实，不是示波器实测。
