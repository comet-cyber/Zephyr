.. zephyr:code-sample:: packet-socket
   :name: Packet Socket
   :relevant-api: bsd_sockets ethernet

   在以太网上使用原始 Packet Socket。

概述
********

本示例是一个简单的 Packet Socket 应用程序，演示了如何在以太网（Ethernet）上使用 Packet Socket。该示例会打印接收到的每一个数据包，并每隔 5 秒发送一个测试（Dummy）数据包。Zephyr 网络子系统不会修改任何协议头（如 L2、L3 等）。

构建与运行
********************

应用程序运行时，会打开一个 Packet Socket 并打印所接收数据包的长度。随后，它会每隔 5 秒发送一个测试数据包。你可以使用 Wireshark 观察这些发送和接收的数据包。

接收端 Socket 还会加入一个以太网组播组（Multicast group），使网络接口开始监听一个额外的组播 MAC 地址。该操作通过 ``PACKET_ADD_MEMBERSHIP`` Socket 选项完成，并在示例停止运行时通过 ``PACKET_DROP_MEMBERSHIP`` 退出该组播组。可以通过设置 :kconfig:option:`CONFIG_NET_SAMPLE_MCAST_ADDR` 来指定组播地址，或者禁用 :kconfig:option:`CONFIG_NET_SAMPLE_MCAST_MEMBERSHIP` 以完全跳过加入组播组的操作。

加入和离开组播组的操作还会作为网络管理（net_mgmt）事件上报，可通过以下 Shell 命令查看：

.. code-block:: console

   uart:~$ net events on

更多详情请参阅 `net-tools`_ 项目。

本示例可按照 :ref:`networking_with_host` 中的说明在 QEMU 或 native_sim 开发板上构建并运行。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
