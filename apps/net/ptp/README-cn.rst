.. zephyr:code-sample:: ptp
   :name: PTP
   :relevant-api: ptp

   启用 PTP 支持并通过日志监控消息与事件。

概述
********

Zephyr 的 PTP 示例应用程序用于启用 PTP（IEEE 1588-2019）支持。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/ptp` 。

环境要求
**************

如需用于调试目的的通用主机连接，请参阅 :ref:`networking_with_native_sim` 了解详情。

在使用嵌入式设备进行测试时，必须使用支持时间戳功能的 Ethernet PHY。本示例应用程序已在搭载 Ethernet PHY 的 :zephyr:board:`nucleo_h563zi` 上完成了测试，测试场景包括配合 ptp4l 守护进程、GPS 时钟（直连）、支持 PTP 的交换机，以及 GPS 时钟 + 支持 PTP 的交换机组合。

构建与运行
********************

运行本示例的一种理想方式是按照 :ref:`networking_with_native_sim` 中的说明在 :zephyr:board:`native_sim` 板卡环境中运行该 PTP 应用程序，或者在 :zephyr:board:`nucleo_h563zi` 、 :zephyr:board:`nucleo_h743zi` 、 :zephyr:board:`nucleo_h745zi_q` 、 :zephyr:board:`nucleo_f767zi` 或 :zephyr:board:`frdm_mcxn947` 等嵌入式设备上运行。

请注意，PTP 仅支持具备 Ethernet 端口且支持采集收发 Ethernet 帧时间戳的开发板。

请按以下步骤构建 PTP 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ptp
   :board: <board to use>
   :goals: build
   :compact:

PPS 输出
============

部分 Ethernet 控制器可以输出由 PTP 硬件时钟分频派生的秒脉冲（PPS，pulse-per-second）信号。在受支持的开发板上，板级 Devicetree 或 overlay 会根据 PTP 时钟节点的 pinctrl 配置将该输出路由到指定引脚。可以使用示波器或逻辑分析仪观测该 1 Hz 信号。通过对比两块开发板的 PPS 输出，或者对比开发板与主时钟（Grandmaster）的 PPS 输出，即可直观评估时钟同步精度。

解析 net ptp 输出
===========================

Shell 提供了两种互补的视图：

- ``net ptp`` ：实例级摘要（时钟标识、当前/父级数据集、最佳外部时间发送端，以及按端口列出的状态表）。
- ``net ptp <port>`` （例如 ``net ptp 1`` ）：单个端口的详细视图，包括配置信息以及运行时计数器/定时器。

作为主时钟（Grandmaster）时的 ``net ptp`` 输出示例：

.. code-block:: console

    uart:~$ net ptp
    PTP Instance:
    Clock ID      : 02:00:00:FF:FE:00:00:01
    Clock Type    : ORDINARY
    Protocol      : UDP/IPv4
    Domain        : 0
    Priorities    : 128 / 128
    Time source   : INTERNAL_OSCILLATOR (0xa0)
    Ports         : 1
    TR only       : no
    PHC now       : 95.703698720

    Current dataset:
    steps_rm      : 0
    offset_from_tt: 0 ns
    mean_delay    : 0 ns
    sync status   : stable

    Parent/GM dataset:
    grandmaster   : 02:00:00:FF:FE:00:00:01 (p1=128 p2=128 class=248 acc=0xfe)
    parent port   : 02:00:00:FF:FE:00:00:01-0
    UTC offset    : 37

    Best foreign transmitter : none

    Port  Interface  State
       1          1  GRAND_MASTER

作为主时钟（Grandmaster）时的 ``net ptp 1`` 输出示例：

.. code-block:: console

    uart:~$ net ptp 1
    PTP Port 1:
    interface            : 1
    port identity        : 02:00:00:FF:FE:00:00:01-1

    Configuration:
    state                : GRAND_MASTER
    enabled              : yes
    protocol             : UDP/IPv4
    time transmitter only: no
    announce log itv     : 1
    announce timeout     : 5
    sync log itv         : 0
    min delay_req log itv: 0
    delay mechanism      : E2E
    delay asymmetry      : 0 ns
    mean link delay      : 0 ns

    Runtime:
    seq announce/delay/signaling/sync: 66 / 0 / 0 / 132
    timeouts bits      : announce=0 delay=0 sync=0 qualification=0
    timer remaining ms : announce=1677 delay=0 sync=677 qualification=0
    PHC now            : 145.138244620
    best foreign       : none

作为时间接收端（Time Receiver）时的 ``net ptp`` 输出示例：

.. code-block:: console

      uart:~$ net ptp
      PTP Instance:
      Clock ID      : 02:00:00:FF:FE:00:00:01
      Clock Type    : ORDINARY
      Protocol      : UDP/IPv4
      Domain        : 0
      Priorities    : 128 / 128
      Time source   : INTERNAL_OSCILLATOR (0xa0)
      Ports         : 1
      TR only       : no
      PHC now       : 1774472701.341945363

      Current dataset:
      steps_rm      : 2
      offset_from_tt: 22 ns
      mean_delay    : 639 ns
      sync status   : stable

      Parent/GM dataset:
      grandmaster   : 02:00:00:FF:FE:00:00:10 (p1=128 p2=128 class=6 acc=0x21)
      parent port   : 02:00:00:FF:FE:00:00:20-2
      UTC offset    : 37

      Best foreign transmitter : 02:00:00:FF:FE:00:00:20-2 (records=2)
      Dataset                : p1=128 p2=128 steps_rm=1 receiver=02:00:00:FF:FE:00:00:01-1

      Port  Interface  State
         1          1  TIME_RECEIVER

作为时间接收端（Time Receiver）时的 ``net ptp 1`` 输出示例：

.. code-block:: console

    uart:~$ net ptp 1
    PTP Port 1:
    interface            : 1
    port identity        : 02:00:00:FF:FE:00:00:01-1

    Configuration:
    state                : TIME_RECEIVER
    enabled              : yes
    protocol             : UDP/IPv4
    time transmitter only: no
    announce log itv     : 1
    announce timeout     : 5
    sync log itv         : 0
    min delay_req log itv: 0
    delay mechanism      : E2E
    delay asymmetry      : 0 ns
    mean link delay      : 0 ns

    Runtime:
    seq announce/delay/signaling/sync: 0 / 1268 / 0 / 0
    timeouts bits      : announce=0 delay=0 sync=0 qualification=0
    timer remaining ms : announce=9459 delay=539 sync=4408 qualification=0
    PHC now            : 1774472701.764088663
    best foreign       : 02:00:00:FF:FE:00:00:20-2 (p1=128 p2=128 steps_rm=1)


这些视图中的常用字段说明：

- ``TR only`` ：是否启用了 :kconfig:option:`CONFIG_PTP_TIME_RECEIVER_ONLY` 。
- ``PHC now`` ：从 Ethernet PHC 读取的当前硬件 PTP 时钟时间。
- ``steps_rm`` ：到所选主时钟（Grandmaster）的网络跳数。
- ``offset_from_tt`` 与 ``mean_delay`` ：当前的同步时间偏差与路径延迟估计值。
- ``Best foreign transmitter`` ：在网络上观测到的用于 BMCA/状态决策的最佳 Announce 候选时钟。

角色/状态说明：

- ``GRAND_MASTER`` 且 ``best foreign : none`` 表示尚未选出符合条件的外部时间发送端，因此本地时钟当前充当主时钟（Grandmaster）。
- 一旦接收到有效的 Announce 消息并完成优选，端口状态通常会根据 BMCA 决策结果切换为 ``TIME_RECEIVER`` 或 ``PASSIVE`` 。

配置 Linux 主机
=====================

默认情况下，Zephyr 中的 PTP 不会向控制台打印任何 PTP 调试消息。可以在配置文件中设置 :kconfig:option:`CONFIG_PTP_LOG_LEVEL_DBG` 来启用调试打印。

首先，获取 linuxptp 项目源码并完成编译：

.. code-block:: console

    git clone http://git.code.sf.net/p/linuxptp/code linuxptp
    cd linuxptp
    make

配合嵌入式设备使用 Linux 主机
--------------------------------------------

为 ptp4l 创建一个配置文件（例如 :file:`e2e.cfg` ），内容如下：

.. code-block:: ini

    [global]
    # Delay mechanism must match your configuration
    delay_mechanism        E2E

    # Use hardware timestamping if your NIC supports it
    time_stamping          hardware

    # Choose the transport that matches your network:
    # - L2 = EtherType 0x88f7 (typical in TSN/industrial, needs L2 reachability)
    # - UDPv4 = common in IT networks / routed segments
    network_transport      UDPv4

    # Must match switch domain
    domainNumber           0

    # Message rates (adjust as needed)
    logSyncInterval        -3
    logMinDelayReqInterval -3

    # Quality-of-life
    tx_timestamp_timeout   20
    summary_interval       1

按如下方式启动该 E2E 配置：

.. code-block:: console

    sudo ./ptp4l -i zeth -f /path/to/config/e2e.cfg -m

对于启用了 :kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_P2P` 的 Zephyr 构建版本，请另行创建一个配置文件（例如 :file:`p2p.cfg` ），并在 Linux 主机端同样使用 ``P2P`` 模式：

.. code-block:: ini

    [global]
    delay_mechanism         P2P
    time_stamping           hardware
    network_transport       UDPv4
    domainNumber            0
    logSyncInterval         -3
    logMinPdelayReqInterval -3
    tx_timestamp_timeout    20
    summary_interval        1

Zephyr 目前支持两步法（two-step）P2P 延迟测量。单步法（one-step） ``Pdelay_Resp`` 数据包会被拒绝并记录日志。

按如下方式启动该 P2P 配置：

.. code-block:: console

    sudo ./ptp4l -i zeth -f /path/to/config/p2p.cfg -m

配合 native_sim 使用 Linux 主机
----------------------------------------

该工作流需要使用三到四个终端：

- 终端 #1：主机网络配置（ ``tools/net-tools`` ）
- 终端 #2： ``ptp4l``
- 终端 #3：Zephyr ``native_sim`` 进程
- 终端 #4（可选）：连接到 Zephyr Shell UART PTY

步骤 1 - 构建 Zephyr 应用程序
----------------------------------------

.. zephyr-app-commands::
   :zephyr-app: samples/net/ptp
   :board: native_sim/native/64
   :goals: build
   :compact:

步骤 2 - 创建主机 TAP 接口
--------------------------------------

在 ``tools/net-tools`` 目录下执行：

.. code-block:: console

    sudo ./net-setup.sh start

在示例运行期间请保持该接口处于开启状态。测试完成后，可通过以下命令将其移除：

.. code-block:: console

    sudo ./net-setup.sh stop

步骤 3 - 启动 ptp4l
--------------------------

.. code-block:: console

    sudo ./ptp4l -4 -i zeth -m -q -l 6 -S

如果 ``ptp4l`` 在 Zephyr 之前启动，短暂出现 ``link down`` 和 ``FAULTY`` 等提示信息属于正常现象。当 Zephyr 创建并拉起 ``zeth`` 接口后， ``ptp4l`` 会重新回到 ``LISTENING`` 状态并继续正常的 BMCA 运行流程。

步骤 4 - 启动 Zephyr native_sim 镜像
---------------------------------------------

.. code-block:: console

    build/zephyr/zephyr.exe

预期的启动输出包含：

.. code-block:: console

    uart connected to pseudotty: /dev/pts/<N>
    *** Booting Zephyr OS build ... ***
    <inf> net_ptp_sample: Runs forever

出现 ``Runs forever`` 是正常现象，因为示例配置中设置了 ``CONFIG_NET_SAMPLE_RUN_DURATION=0`` 。

若要自动将终端连接到 Zephyr Shell UART PTY，请改用 ``-attach_uart`` 参数启动可执行文件：

.. code-block:: console

    build/zephyr/zephyr.exe -attach_uart

连接命令由 :kconfig:option:`CONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD` 指定，可以是任何包含单个 ``%s`` 占位符（代表 PTY 路径）的 Shell 命令。例如，若要在 ``gnome-terminal`` 中打开 ``screen`` ，可设置为：

.. code-block:: cfg

    CONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD="gnome-terminal -- screen %s"

步骤 5 - 连接到 Zephyr Shell
------------------------------------

如果启动可执行文件时未指定 ``-attach_uart`` ，请使用启动时打印的 ``/dev/pts/<N>`` 路径手动连接。

如果已安装 ``screen`` ：

.. code-block:: console

    screen /dev/pts/<N>

如果未安装 ``screen`` ，可以使用 ``socat`` ：

.. code-block:: console

    socat -,rawer,echo=0,escape=0x1d /dev/pts/<N>,rawer,echo=0

按下 ``Ctrl-]`` 可退出 ``socat`` 。

步骤 6 - 在 Zephyr Shell 中检查 PTP 状态
--------------------------------------------------

.. code-block:: console

    uart:~$ net ptp
    uart:~$ net ptp 1

在 ``native_sim`` 上，同时看到主机和 Zephyr 发送 Announce/Sync 流量属于正常现象。根据 BMCA 数据，即使存在 ``best foreign`` ，Zephyr 也可能继续保持 ``GRAND_MASTER`` 状态。

本示例还启用了 ``ptp_clock`` Shell，便于独立于协议状态机直接检查硬件 PTP 时钟。可以使用 ``ptp_clock get <device>`` 读取 PHC 时间，使用 ``ptp_clock set <device> <seconds>`` 或 ``ptp_clock adj <device> <seconds>`` 修改时间，使用 ``ptp_clock freq <device> <ppb>`` 进行频率微调，以及使用 ``ptp_clock selftest <device> <time> <freq> <delay> <adj>`` 快速执行驱动级自检。
