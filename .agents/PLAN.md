# PLAN

> 更新日期：2026-10-06

## 学习原则

沿用项目驱动螺旋，不把 Zephyr 手册当课程表：

1. 当前增量 → 最少必要原理 → 代码边界 → 板上测量/日志 → 复盘 → 下一增量。
2. 一次大约引入 3～5 个新概念。
3. 先做出可观察结果，再沿一条路径看 Device Tree、Kconfig 或驱动。
4. 不逐行读 HAL/FSP，不要求记寄存器表。
5. 双核、MCUboot、以太网、NPU 只在真实需求出现时进入。
6. 代码已经写了 ≠ 这个阶段完成。没板上证据、说不清“为什么这块板会这样动”，就不标 `verified`。

## 学习载体

长期只养一个树外应用：`F:\zephyr\apps\rgb_led`。

它现在已经能编、能关 OFS、会循环 RGB、`prj.conf` 里已经打开 shell，但 **从未上板**。后续阶段都是给这个应用加能力，不新开一堆 sample 工程，也不改 `zephyr/samples/`。

比赛固件继续放 `F:\ECSDC\firmware`。本轨练会的 overlay / 守门 / UART2 / GPIO / shell，以后搬过去；不要把比赛功能写进 `apps/rgb_led`。

| 项 | 值 |
| --- | --- |
| 板 | `ra8p1_titan_mini/r7ka8p1kflcac/cm85` |
| 核 | Cortex-M85 / CPU0 |
| 控制台 | UART2，115200，外接 USB-UART（P801 TX / P802 RX） |
| 可见结果 | RGB（P108 绿 / P109 红 / P110 蓝，低有效）+ 串口 |
| 构建目录 | `F:\zephyr\build\rgb_led`，不要再写进 `apps/rgb_led/build` 或上游 `zephyr/build` |

当前会话要做什么，看 [`CURRENT.md`](CURRENT.md)。

## Z0  工作区与下载安全

**增量：** 搞清 west 工作区、board target、构建产物，并堵住 RA8P1 配置区误写。

**概念：** west topdir / manifest；board target 与 SoC qualifier；`west build` ≠ `west flash`；Code MRAM vs Option-setting/OTP；Intel HEX 扩展地址。

**任务：**

1. 落地守门脚本 `F:\zephyr\scripts\audit_image.py`：解析 ELF PHDR 与 Intel HEX 扩展线性地址；白名单 `0x02000000-0x02100000`；命中 `0x02C9xxxx` / `0x02E1xxxx` 或其它窗口则 FAIL。
2. 对 2026-09-04 旧 blinky（若还在）必须 FAIL；对 `apps/rgb_led` 现有 hex 必须 PASS。人工抽查 hex 无 `:0200000402C9` / `:0200000402E1`。
3. 把 `app.overlay` 里关闭 `option_setting_*` 的片段抽成可复用 overlay，rgb_led 继续引用，避免每个应用复制十行。
4. 只读备份当前板上 Code MRAM `0x02000000-0x02100000`，排除 Config Area，放到 `F:\zephyr\backups\`。

**完成证据：** 守门脚本对脏镜像失败、对 rgb_led 通过。脚本部分可以在不下板的情况下结束；第一次下载必须另获用户当次同意。

**状态：** 工作区可用；脚本、共用 overlay、MRAM 备份都还没做。

## Z1  第一张可恢复的 Zephyr 映像

**增量：** 用户明确同意后，把纯 Code MRAM 镜像下到 CPU0，看到灯或串口。

**概念：** `west flash --runner jlink`；J-Link 设备名 `R7KA8P1KF_CPU0`；复位后 PC/VTOR；UART2 不是板上调试 USB CDC。

**任务：**

1. 用约定目录重编：`west build -p always -b ra8p1_titan_mini/r7ka8p1kflcac/cm85 -d F:\zephyr\build\rgb_led F:\zephyr\apps\rgb_led`
2. 守门 PASS 后请求当次下载批准。只下 hex/elf，不用 padded `zephyr.bin`。
3. 外接 USB-UART 到 P801/P802，115200。预期：RGB 按调色板循环；串口有启动横幅，可能已经出现 `uart:~$`（shell 已在 `prj.conf` 打开，本阶段只观察，不深挖）。
4. 写明如何回到裸机 Stage 2 / Stage 0。第一次 Zephyr 会覆盖 Code MRAM。

**完成证据：** 守门 PASS + J-Link 下载 + 板上灯或串口现象 + 恢复路径写明。

## Z2  GPIO 与 Device Tree

**增量：** 讲清 rgb_led 为什么点得亮，并且只用 overlay 换行为，不改 `main.c` 写死引脚。

**概念：** `aliases { led0 = &led1; }`；应用别名 `red-led` / `green-led` / `blue-led`；`GPIO_DT_SPEC_GET`；`GPIO_ACTIVE_LOW` 与共阳灯；overlay 合并顺序。

**任务：**

1. 从 `main.c` 的 `DT_ALIAS(green_led)` 追到 `app.overlay` → 板 dtsi `led1` → `ioport1 8`（P108）。红/蓝同样走一遍。
2. 只改 overlay：把 `green-led` 指到另一颗灯，重编、审计、上板，确认循环颜色对不上原先顺序。再改回来。
3. 对照 `gpio_pin_set_dt(..., 1)`：逻辑亮，驱动已经按 `GPIO_ACTIVE_LOW` 拉低引脚。不要在应用里再手动反相。

**完成证据：** 能指着 DTS 说出三色引脚和极性，并能用 overlay 换灯。

## Z3  按键输入

**增量：** SW1（P201，`sw0` / `button0`）接管 RGB，先轮询，稳定后再 GPIO 回调。

**概念：** `gpio-keys`；`DT_ALIAS(sw0)`；CM85 dts 已 `&button0 { status = "okay"; }`；输入极性；轮询 vs `gpio_add_callback`。消抖放本阶段末尾，不和 DT 入门绑死。

**任务：**

1. overlay 确认 `sw0` 能用，不要去改上游板文件。
2. 先轮询：按下 SW1 冻结当前颜色或切到下一色，串口打一行。
3. 再改成中断回调；主循环继续跑灯，按键只发事件。这里开始出现真实并发，作为 Z5 的触发条件，而不是提前讲 RTOS。

**完成证据：** 按下 SW1 有稳定可观察的灯/日志变化。

## Z4  树外应用骨架（收口，不是从零再建）

**增量：** 把已经能跑的 rgb_led 收成以后每个应用都该长这样的骨架。

**概念：** 树外 `CMakeLists.txt` / `prj.conf` / overlay 分工；west `-d` 构建目录；Kconfig 开功能、DTS 描述板；包装仓库跟踪应用，不跟踪上游 `zephyr/`。

**任务：**

1. 固定构建到 `F:\zephyr\build\rgb_led`，清掉 `apps/rgb_led/build` 这类混在源码旁的产物。
2. 核对每个文件的职责：`prj.conf` 只留应用策略（shell/log），板默认不要重复开；OFS 关闭走共用 overlay。
3. 不修改上游 sample 也能重复：构建 → 审计 →（同意后）下载 → 同样现象。

**完成证据：** 能复述四个文件各自干什么，并且换一台机器按 `TOOLCHAIN.md` 能复现。

## Z5  线程：灯和键同时活着

**增量：** 自动循环和按键不能再挤在一个 `while (1)` 里时，才引入线程。

**概念：** `K_THREAD_DEFINE` 或 `k_thread_create`；`k_msleep` vs 忙等；线程优先级只讲到“谁该让出 CPU”；共享颜色状态用 `k_mutex` 或原子变量，先不要消息队列全家桶。

**任务：**

1. LED 调色板放到独立线程。
2. 主线程或按键回调只改“当前模式 / 目标颜色”。
3. 串口仍可打印，但不在灯线程里做重活。

**完成证据：** 按键响应时灯循环不停；能说出两个线程各自让出 CPU 的点。

## Z6  把已经编进去的 shell 用起来

**增量：** `CONFIG_SHELL` 现在只是“碰巧开了”。本阶段要能用命令改板子，而不是只会看 `uart:~$`。

**概念：** `zephyr,shell-uart = &uart2`；应用自定义 `SHELL_CMD_REGISTER`；shell 线程和你的 LED 线程的关系；`help` / `kernel stacks` / `device list` 是观察工具，不是课程。

**任务：**

1. 加 `rgb <color>` 或 `rgb r g b` 命令，调用已有 `rgb_set()`。
2. 加 `rgb cycle on|off`。按键和 shell 改同一份状态。
3. 用 `device list` 确认 GPIO / UART2 在设备模型里，对上 DTS 节点名。

**完成证据：** 不重编、只打命令就能改灯；按键和命令不打架。

## Z7  日志替换 printk

**增量：** 启动信息和错误改走 logging，按级别过滤。

**概念：** `LOG_MODULE_REGISTER`；`CONFIG_LOG` / 级别；printk 仍给极早期失败；日志后端走同一条 UART2，注意和 shell 抢串口时的观感。

**任务：**

1. `main.c` 的日常输出改 `LOG_INF` / `LOG_ERR`。
2. 用 Kconfig 把默认级别收到 INF，调试 DT 问题时临时开 DBG。
3. 对照一次启动日志，标出哪些是内核横幅、哪些是应用、哪些是 shell 提示符。

**完成证据：** 关闭 DBG 后串口仍然干净可读；打开 DBG 能看到你埋的那几条。

## Z8  I2C 对原理图（有外设需求再开）

**增量：** 只有当你要把 HWT101 或其它 I2C 设备接到 Mini 上时才进入。禁止“先学一遍 I2C 子系统”。

**概念：** 板文件默认 `iic1` = P512/P511，裸机 Stage 2 的 HWT101 是 `IIC0 / P409 / P410`；overlay 使能正确控制器和 pinctrl；`zephyr,i2c` API vs 自己写寄存器。

**任务：** 对照原理图写 overlay，扫总线或读谁在线上的设备；驱动逻辑不要写进 `main()` 一锅粥。

**完成证据：** 示波器/逻辑分析仪或成功的设备应答，证明走的是你以为的那组引脚。

## 明确暂缓

- CM33 第二核与 `--sysbuild`
- MCUboot
- 以太网 PHY / ESWM / MQTT / WireGuard（去 ECSDC 轨）
- SDHI、USB、SDRAM、OSPI、Ethos-U55
- 把比赛功能写进 `apps/rgb_led`

## 和其它路线的边界

| 路线 | 根目录 | 关系 |
| --- | --- | --- |
| 本轨 | `F:\zephyr` | Titan Mini 上把 Zephyr 用熟 |
| 裸机系统监视器 | `F:\embedded_systems_learning` | 同一块物理板，固件会互相覆盖 |
| ECSDC | `F:\ECSDC` | 比赛应用；west/SDK 仍用本工作区 |

需要对照板级资料时可以读 RT-Thread BSP 和裸机证据，但不要把 FSP 工程改造成 Zephyr，也不要把 Zephyr 应用写回 IAR/e² studio 目录。
