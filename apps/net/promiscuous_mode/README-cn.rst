.. zephyr:code-sample:: net-promiscuous-mode
   :name: 混杂模式
   :relevant-api: promiscuous

   在所有网络接口上启用混杂模式并打印传入数据包的信息。

概述
********

本应用程序将为系统中的每个网络接口启用混杂模式（Promiscuous mode），随后开始监听传入的网络数据包并显示其相关信息。

该应用程序还提供了一个 Shell，以便用户在运行时启用或禁用混杂模式。相关命令为 ``promisc on`` 和 ``promisc off`` 。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

有多种方式可以使用此应用程序。在本示例中使用 QEMU：

.. zephyr-app-commands::
   :zephyr-app: samples/net/promiscuous_mode
   :board: qemu_x86
   :conf: <config file to use>
   :goals: build
   :compact:
