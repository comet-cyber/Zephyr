.. zephyr:code-sample:: latmon-client
   :name: Latmon 客户端
   :relevant-api: latmon

   测量 GPIO 事件之间的时间差（Delta Time），并通过 latmon 将延迟指标上报给运行在被测系统（SUT）上的 latmus 服务。

概述
********

本项目提供了一套通过以下组件测量被测系统（SUT，System Under Test）对 GPIO 事件最坏响应时间的工具：

- **Latmon** ：

  运行在基于 Zephyr 的开发板上，用于生成和监控 GPIO 事件并收集指标数据。

- **Latmus** ：

  运行在 SUT 上，用于响应输入 GPIO 事件的下降沿，显示延迟指标并生成直方图数据。

本项目是开源项目 `EVL Project - Latmus GPIO 响应时间 <https://v4.xenomai.org/core/benchmarks/#latmus-gpio-response-time>`_ 的一部分。

主程序旨在利用基于 Zephyr 的系统上的 GPIO 引脚来监控延迟。它会在某个 GPIO 引脚上生成脉冲信号，并测量 SUT（运行 Latmus）响应该信号所需的时间。

SUT 必须运行 Latmus，才能捕获通过网络上报的延迟指标和直方图信息。该程序使用 LED 指示不同的运行状态，例如 DHCP 绑定中（红色）、等待 Latmus 连接（蓝色）以及采样中（绿色）。

为什么不只使用定时器？
====================================

仅依靠定时器测试会遗漏 GPIO 信号、硬件通路和中断处理等外部因素。Latmon 和 Latmus 模拟真实应用场景，能够捕获端到端（End-to-End）延迟指标，从而确保对整个系统的实时响应能力进行准确评估。

- **实时线程测试** ：

  评估用户态线程（Thread）如何处理外部中断。

- **端到端延迟测量** ：

  捕获来自硬件、驱动程序以及用户态线程的整体延迟。

- **广泛的平台支持** ：

  适用于 EVL、PREEMPT_RT 及其他平台。

代码结构
==============

Latmon 示例应用程序分为两个主要组件：

- **应用程序逻辑** (:zephyr_file:`samples/net/latmon/src/main.c`) ：

   该文件包含 Latmon 的应用程序逻辑，负责初始化网络、提供测量插桩机制，并处理不同状态下的 LED 指示灯。

- **库实现** (:zephyr_file:`subsys/net/lib/latmon/latmon.c`) ：

   该文件提供通过 Latmus 进行延迟监控的可复用函数与抽象接口，包含上报延迟指标和直方图数据的核心逻辑。

环境要求
**************

- **兼容 Zephyr 的开发板** ：

  具备外部 GPIO 支持和 IPv4 网络接口的开发板（例如 FRDM-K64F）。

- **被测系统（SUT）** ：

  具备外部 GPIO 引脚、IPv4 网络接口且运行 Latmus 服务的系统。

- **网络连接** ：

  用于分配 IP 地址的 DHCP 服务器。

- **物理连接** ：

  使用导线连接 Zephyr 开发板与 SUT 的 GPIO 引脚，并将两个系统均接入网络。

配置与使用
******************

- **将 Latmon 烧录到 Zephyr 开发板** ：

  应用程序将连接到网络并等待来自 SUT 的连接，同时通过 DHCP 获取 IPv4 地址。

- **连接用于发送（Zephyr 到 SUT）和接收（SUT 到 Zephyr）的 GPIO 引脚** ：

  在 **FRDM-K64F** 上，示例代码使用 **Arduino 排针 J2** 的 ``pin 20`` 向 SUT 发送脉冲，并使用 ``pin 18`` 接收来自 SUT 的应答（ACK）信号。

- **在 SUT 上运行 Latmus** ：

  配合适当的参数运行 `Latmus <https://v4.xenomai.org/core/testing/#latmus-program>`_ 。例如，用户可以使用 ``-p`` 选项修改采样周期，或使用 ``-g`` 选项生成用于后处理的直方图数据。

- **在 SUT 上监控测试结果** ：

  Latmus 将输出延迟统计数据，并在指定相应选项时生成直方图数据文件。

- **校准 Latmus 延迟：CONFIG_LATMON_LOOPBACK_CALIBRATION** ：

  用户可以将 GPIO 引脚连接为 Loopback（回环）模式（即将发送引脚直连到应答接收引脚），并在启用 CONFIG_LATMON_LOOPBACK_CALIBRATION 的情况下构建 Latmon 示例应用程序。在此配置下连接到 Latmus 时，Latmus 会提供一个可用于修正最终延迟结果的校准值。

示例
========

在主机上为 Zephyr FRDM-K64F 开发板构建并烧录 Latmon 示例：

.. code-block:: console

   user@host:~$ west build -b frdm_k64f samples/net/latmon
   user@host:~$ west flash

在运行 Linux 的 SUT 上，latmus **必须** 跟踪信号的下降沿：

.. code-block:: console

   root@target:~$ latmus -I gpiochip2,23,falling-edge -O gpiochip2,21 -z -g"histogram" "broadcast"

同时监控两个控制台，你应该会看到如下输出：

.. code-block:: console

  [00:00:03.311,000] <inf> phy_mc_ksz8081: PHY 0 is up
  [00:00:03.311,000] <inf> phy_mc_ksz8081: PHY (0) Link speed 100 Mb, full duplex
  [00:00:03.312,000] <inf> eth_nxp_enet_mac: Link is up
  *** Booting Zephyr OS build v4.1.0-3337-g886443a190b1 ***
  [00:00:03.313,000] <inf> sample_latmon: DHCPv4: binding...
  [00:00:03.313,000] <inf> latmon: Latmon server thread priority: 14
  [00:00:10.964,000] <inf> net_dhcpv4: Received: 192.168.1.58
  [00:00:10.964,000] <inf> sample_latmon: Listening on 192.168.1.58
  [00:00:30.966,000] <inf> latmon: Waiting for Latmus ...
  [00:00:31.356,000] <inf> latmon: Monitor thread priority: -16
  [00:00:31.356,000] <inf> latmon:        monitoring started:
  [00:00:31.356,000] <inf> latmon:         - samples per period: 1000
  [00:00:31.356,000] <inf> latmon:         - period: 1000 usecs
  [00:00:31.356,000] <inf> latmon:         - histogram cells: 200
  [00:00:31.393,000] <inf> latmon: Transfer thread priority: 14

.. code-block:: console

  root@target:~$ latmus -I gpiochip2,23,falling-edge -O gpiochip2,21 -Z -g"histogram" broadcast
  Received broadcast message: 192.168.1.58
  warming up on CPU0 (not isolated)...
  connecting to latmon at 192.168.1.58:2306...
  RTT|  00:00:16  (oob-gpio, 1000 us period, priority 98, CPU0-noisol)
  RTH|----lat min|----lat avg|----lat max|-overrun|---msw|---lat best|--lat worst
  RTD|     26.375|     30.839|     33.508|       0|     0|     26.375|     33.508
  RTD|     26.333|     30.801|     37.633|       0|     0|     26.333|     37.633
  RTD|     26.375|     30.801|     31.966|       0|     0|     26.333|     37.633
  RTD|     26.375|     30.911|     49.675|       0|     0|     26.333|     49.675
  RTD|     26.333|     30.830|     41.658|       0|     0|     26.333|     49.675
  RTD|     26.375|     31.107|     59.216|       0|     0|     26.333|     59.216
  RTD|     26.333|     30.767|     30.925|       0|     0|     26.333|     59.216
  RTD|     26.333|     30.781|     41.616|       0|     0|     26.333|     59.216
  RTD|     26.375|     30.768|     32.925|       0|     0|     26.333|     59.216
  RTD|     26.375|     30.768|     37.633|       0|     0|     26.333|     59.216

测试完成后，在主机上从 SUT 获取直方图文件，并使用 gnuplot 生成图表（PNG 文件）：

.. code-block:: console

   user@host:~$ gnuplot plot_data.gp

针对名为 ``histogram`` 的文件， ``plot_data.gp`` 脚本内容应如下所示：

.. code-block:: gnuplot

   set terminal pngcairo size 800,600
   set output 'plot.png'
   set title "Data Plot"
   set xlabel "Latency (usec)"
   set ylabel "Sample Count"
   set grid
   set style data linespoints
   plot 'histogram' using 1:2 with linespoints title "Data Points"
