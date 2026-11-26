.. zephyr:code-sample:: sockets-echo
   :name: Echo 服务器（简单版）
   :relevant-api: bsd_sockets

   使用 BSD Socket 实现一个简单的 IPv4/IPv6 TCP Echo 服务器。

概述
********

Zephyr 的 sockets/echo 示例应用程序使用兼容 BSD Sockets 的 API 实现了一个同时支持 IPv4 和 IPv6 的 TCP Echo（回显）服务器。
本示例旨在展示如何开发一个可同时移植到 POSIX 和 Zephyr 的 Socket 应用程序。因此，代码保持精简，仅支持 IPv4、IPv6 和 TCP。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/echo` 。

环境要求
************

- :ref:`networking_with_host`
- 或者一块具备硬件网络功能的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 sockets/echo 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，将在 192.0.2.1 的 4242 端口等待连接。
最简单的连接方式是：

.. code-block:: console

    $ telnet 192.0.2.1 4242

建立连接后，应用程序会将发送给它的每一行内容原样回显。该应用程序使用阻塞式 Socket 实现单线程服务器，因此同一时间只能服务一个客户端连接。当前客户端断开连接后，下一个连接才能继续进行。

在 POSIX 主机上运行应用程序
========================================

同一份应用程序源代码也可以针对 POSIX 系统（例如 Linux）进行构建。（注：查看源码可以发现，除了 Zephyr 与 POSIX 包含的头文件不同之外，其余代码完全一致。）

构建方法：

.. code-block:: console

    $ make -f Makefile.host

运行方法：

.. code-block:: console

    $ ./socket_echo

测试方法：

.. code-block:: console

    $ telnet 127.0.0.1 4242

可以看到，该应用程序的行为与 Zephyr 版本完全一致。

在 cc3220sf_launchxl 上运行
================================

请参阅 :zephyr:board:`cc3220sf_launchxl` 中关于配网（Provisioning）和快速连接（Fast Connect）的说明。

使用示例中的 Wi-Fi Shell 连接到 AP（Access Point）后，运行此 Echo 应用程序时控制台会打印出 IP 地址。

随后按上述相同步骤进行测试即可。
