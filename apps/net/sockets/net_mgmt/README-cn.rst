.. zephyr:code-sample:: sockets-net-mgmt
   :name: 网络管理 Socket
   :relevant-api: bsd_sockets net_if

   使用网络管理 Socket 监听网络管理事件。

概述
********

适用于 Zephyr 的 net-mgmt-socket 示例应用程序实现了一个监听器，用于接收网络子系统发送的网络管理（network management）事件。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/sockets/net_mgmt` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

使用本应用程序有多种方式。最常见的使用场景之一是在 QEMU 中运行 echo-server 应用程序，具体说明请参阅 :ref:`networking_with_qemu` 。

按如下方式构建 net-mgmt Socket 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/net_mgmt
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

针对 native_sim 开发板构建与运行的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/net_mgmt
   :host-os: unix
   :board: native_sim
   :conf: prj.conf
   :goals: run
   :compact:
