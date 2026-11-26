.. zephyr:code-sample:: so_txtime
   :name: 使用 SO_TXTIME 的 UDP 发送端
   :relevant-api: bsd_sockets ethernet

   使用 SO_TXTIME Socket 选项控制数据包的发送时间。

概述
********

本示例是一个简单的 UDP 收发程序，它会设置 SO_TXTIME Socket 选项，并由以太网驱动在到达预期发送时间（TX time）时将数据发出。本应用程序要求开发板支持 PTP 时钟。qemu_x86 开发板提供了模拟 PTP 时钟，此外还支持 frdm_k64f 和 sam_e70_xplained/same70q21 开发板。其他基于 mcux 或 gmac 以太网驱动的开发板通常也能正常工作。
用户可以通过设置 :kconfig:option:`CONFIG_NET_SAMPLE_PACKET_INTERVAL` 选项来控制应用程序在两次发送数据包之间的等待时间。此外，还可以通过在配置文件中设置 :kconfig:option:`CONFIG_NET_SAMPLE_PACKET_TXTIME` 选项来指定 TXTIME 值；在此情况下，该值将作为相对于当前时间的偏移量使用。

构建与运行
********************

本应用程序运行后会开始发送 UDP 数据包。你可以启动 `net-tools`_ 项目中的 ``echo-server`` 应用程序来接收这些数据包并将其回传给本应用程序。你也可以选择设置 :kconfig:option:`CONFIG_NET_SAMPLE_PACKET_SOCKET` 选项，这会使应用程序创建一个 ``AF_PACKET`` 类型的 Socket；在此情况下，不能使用 ``echo-server`` 应用程序作为对端（peer）。

可按照 :ref:`networking_with_host` 中的说明在 qemu_x86 开发板上构建并运行本示例。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
