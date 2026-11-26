.. zephyr:code-sample:: quic-service-echo
   :name: Echo 服务器（QUIC）
   :relevant-api: quic

   使用 QUIC API 与 Socket Service API 实现一个简单的 IPv4/IPv6 Echo 服务器。

概述
********

本 Zephyr quic/echo_service 示例应用程序使用兼容 BSD Sockets 的 API，实现了一个同时支持 IPv4 和 IPv6 的 QUIC 协议 Echo 服务器。

本示例旨在展示如何使用 QUIC API 与 Socket Service API。Socket Service（套接字服务）的设计理念是由单个线程（Thread）监听多个阻塞式 Socket，当该组 Socket 中有活动发生时触发回调函数。由于系统中只需创建一个线程，这种机制能够有效节省内存。

本应用程序同时支持 IPv4 和 IPv6，并使用 QUIC 协议（ :rfc:`9000` ）来实现该服务。本示例应用程序的源代码位于： :zephyr_file:`samples/net/quic/echo_service` 。

环境要求
************

- :ref:`networking_with_host`
- 或者一块支持硬件网络的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 quic/echo_service 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/quic/echo_service
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，将在 192.0.2.1 或 2001:db8::1 的 4422 端口等待连接。最简单的连接方式是使用 net-tools 项目中的辅助 echo-client 脚本：

.. code-block:: console

    $ ./quic-echo-client.py --host 192.0.2.1 --max-size 1280 --packets 1
    $ ./quic-echo-client.py --host 2001:db8::1 --packets 10

建立连接后，该应用程序会将发送给它的任何一行数据原样回显。quic-echo-client.py 应用程序会在运行结束时打印统计信息。
