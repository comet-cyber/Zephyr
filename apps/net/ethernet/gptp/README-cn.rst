.. zephyr:code-sample:: gptp
   :name: gPTP
   :relevant-api: gptp ptp_time

   启用 gPTP 支持并使用 net-shell 监控其功能。

概述
********

Zephyr 的 gPTP 示例应用程序会启用 gPTP 支持、注册 gPTP 相位不连续回调、启用流量类别（Traffic Class）支持（TX 多队列）并配置 VLAN（若已启用）。同时还会启用 net-shell，以便用户监控 gPTP 功能。

本示例应用程序的源代码位于 :zephyr_file:`samples/net/ethernet/gptp` 目录。

环境要求
************

关于可用于调试目的的通用主机网络连接方式，请参阅 :ref:`networking_with_native_sim` 了解详情。

构建与运行
********************

运行本示例的一种理想方式是按照 :ref:`networking_with_native_sim` 中的说明在 native_sim 开发板环境中运行此 gPTP 应用程序，或者在 NXP FRDM-K64F、Nucleo-H743-ZI、Nucleo-H745ZI-Q、Nucleo-F767ZI 或 Atmel SAM-E70 Xplained 等嵌入式设备上运行。请注意，gPTP 仅支持具备以太网端口且支持采集收发以太网帧时间戳的开发板。

请按照以下步骤构建 gPTP 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/gptp
   :board: <board to use>
   :goals: build
   :compact:

net-shell 命令 **net gptp** 会打印通用的 gPTP 信息。对于端口 1，命令 **net gptp 1** 会打印端口 1 统计数据等详细信息。请注意，执行 Shell 命令可能会影响收发 gPTP 数据包的时序，主时钟（Grandmaster）可能会将该设备标记为不具备 AS 能力（non AS capable）并将其禁用。

配置 Linux 主机
=====================

如果你的网络需要 VLAN 支持，那么 :zephyr_file:`samples/net/ethernet/vlan/vlan-setup-linux.sh` 提供了一个可在 Linux 主机上执行的脚本。它会在 Linux 主机上创建两个 VLAN 并添加通往 Zephyr 的路由。如果你使用的是 native_sim 开发板，则 ``net-setup.sh`` 可通过以下命令自动完成 VLAN 配置：

.. code-block:: console

   ./net-setup.sh -c zeth-vlan.conf

位于 https://github.com/AVnu 的 OpenAVNU 仓库包含可在 Linux 主机上运行的 gPTP 守护进程，可作为 IEEE 802.1AS 网络的主时钟（Grandmaster）。请注意，OpenAVNU 无法配合 native_sim 开发板使用，因为该开发板仅支持软件时间戳，而 OpenAVNU 仅支持硬件时间戳。关于如何配合 native_sim 开发板运行 linuxptp 守护进程，请参阅本章末尾的说明。

获取 OpenAvnu/gPTP 项目源码：

.. code-block:: console

    git clone git@github.com:AVnu/gptp.git

下载源代码后，在 Linux 中按如下方式编译：

.. code-block:: console

    mkdir build
    cd build
    cmake ..
    make
    cp ../gptp_cfg.ini .

编辑 :file:`gptp_cfg.ini` 文件并将 neighborPropDelayThresh 设置为 10000，因为在 FRDM-K64F 上运行 gPTP 时默认值 800 过低。

随后指定正确的网络接口和配置文件启动该守护进程：

.. code-block:: console

    sudo ./gptp enp0s25 -F gptp_cfg.ini

请注意，此处的示例网络接口 **enp0s25** 是连接到你的 Zephyr 设备的网络接口名称。

如果所有配置均正确，你应该会看到来自 gptp 的如下输出信息：

.. code-block:: console

    INFO     : GPTP [13:01:14:837] gPTP starting
    INFO     : GPTP [13:01:14:838] priority1 = 248
    INFO     : GPTP [13:01:14:838] announceReceiptTimeout: 3
    INFO     : GPTP [13:01:14:838] syncReceiptTimeout: 3
    INFO     : GPTP [13:01:14:838] LINKSPEED_100MB - PHY delay
			TX: 1044 | RX: 2133
    INFO     : GPTP [13:01:14:838] LINKSPEED_1G - PHY delay
			TX: 184 | RX: 382
    INFO     : GPTP [13:01:14:838] neighborPropDelayThresh: 10000
    INFO     : GPTP [13:01:14:838] syncReceiptThreshold: 8
    ERROR    : GPTP [13:01:14:838] Using clock device: /dev/ptp0
    STATUS   : GPTP [13:01:14:838] Starting PDelay
    STATUS   : GPTP [13:01:14:838] Link Speed: 1000000 kb/sec
    STATUS   : GPTP [13:01:14:871] AsCapable: Enabled
    STATUS   : GPTP [13:01:16:497] New Grandmaster "3C:97:0E:FF:FE:23:F2:32" (previous "00:00:00:00:00:00:00:00")
    STATUS   : GPTP [13:01:16:497] Switching to Master

如果 Zephyr 与 gptp 守护进程正常同步，则会打印以下信息：

.. code-block:: console

    STATUS   : GPTP [13:01:25:965] AsCapable: Enabled

默认情况下，Zephyr 中的 gPTP 不会向控制台打印任何 gPTP 调试信息。可通过在配置文件中设置 :kconfig:option:`CONFIG_NET_GPTP_LOG_LEVEL_DBG` 来启用调试打印。

对于 native_sim 开发板，请使用支持软件时间戳的 ``linuxptp`` 项目。

获取 linuxptp 项目源码：

.. code-block:: console

    git clone git://git.code.sf.net/p/linuxptp/code

编译 ``ptp4l`` 守护进程并按如下方式启动：

.. code-block:: console

    sudo ./ptp4l -2 -f gPTP-zephyr.cfg -i zeth -m -q -l 6 -S

以 ``default.cfg`` 为基础，将其复制为 ``gPTP-zephyr.cfg`` 文件，并根据需要进行修改。


多端口配置
==================

如果将 :kconfig:option:`CONFIG_NET_GPTP_NUM_PORTS` 设置为大于 1 的值，gPTP 示例将创建多个 TSN 端口。此配置目前仅在 native_sim 开发板上受支持。Devicetree 中定义的 ``zephyr,native-tap`` 接口数量必须与 :kconfig:option:`CONFIG_NET_GPTP_NUM_PORTS` 一致。对于双端口配置，请结合添加第二个 TAP 接口的 :file:`overlay-multiport.conf` 和 :file:`overlay-multiport.overlay` 进行构建：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/gptp
   :board: native_sim
   :gen-args: -DEXTRA_CONF_FILE=overlay-multiport.conf -DEXTRA_DTC_OVERLAY_FILE=overlay-multiport.overlay
   :goals: build
   :compact:


你需要在 net-tools 中启用这些端口。如果端口数量设置为 2，请执行以下命令在主机侧创建网络接口：

.. code-block:: console

    sudo ./net-setup.sh -c zeth0-gptp.conf -i zeth0 start
    sudo ./net-setup.sh -c zeth1-gptp.conf -i zeth1 start

随后即可为这两个接口启动 ptp4l 守护进程。启动 ptp4l 守护进程时请使用两个终端窗口。请注意，此处必须使用 ptp4l，因为 OpenAVNU 不支持 native_sim 中提供的软件时钟。

.. code-block:: console

    cd <ptp4l directory>
    sudo ./ptp4l -2 -f gPTP-zephyr.cfg -m -q -l 6 -S -i zeth0
    sudo ./ptp4l -2 -f gPTP-zephyr.cfg -m -q -l 6 -S -i zeth1

编译 Zephyr 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/gptp
   :board: native_sim
   :goals: build
   :compact:

Zephyr 镜像构建完成后，可按如下方式启动：

.. code-block:: console

    build/zephyr/zephyr.exe -attach_uart

静态 timeReceiver 配置
============================

在遵循 IEEE 802.1AS 车载规范（automotive profile）构建的网络中，网桥会发送 Sync 和 Follow_Up 报文，但不发送 Announce 报文，因此默认协议栈永远不会选出时间接收端（time receiver）端口。请结合 :zephyr_file:`samples/net/ethernet/gptp/overlay-static-time-receiver.conf` overlay 文件构建本示例，将该端口固定为时间接收端角色：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/gptp
   :board: <board to use>
   :conf: "prj.conf overlay-static-time-receiver.conf"
   :goals: build
   :compact:

这可以配合 linuxptp 进行测试：将 ptp4l 作为不发送 Announce 报文的主时钟运行，例如使用基于 linuxptp 自带的 ``automotive-master.cfg`` 文件修改而成的配置。
