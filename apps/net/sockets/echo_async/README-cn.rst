.. zephyr:code-sample:: async-sockets-echo
   :name: 使用 poll() 的异步 Echo 服务器
   :relevant-api: bsd_sockets

   使用 BSD Socket 和 poll() 实现异步 IPv4/IPv6 TCP Echo 服务器

概述
********

Zephyr 的 sockets/echo-async 示例应用程序使用兼容 BSD Sockets 的 API、非阻塞 Socket 以及 ``poll()`` 调用，实现了一个异步 IPv4/IPv6 TCP Echo（回显）服务器。它是 :zephyr:code-sample:`sockets-echo` 示例的扩展版本。该应用程序功能更为完整，支持 IPv4 和 IPv6 并发连接、限制最大同时连接数以及基本的错误处理。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/echo_async` 。

环境要求
************

- :ref:`networking_with_host`
- 或者一块具备硬件网络功能（包括 6LoWPAN）的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 sockets/echo_async 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_async
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，将在 192.0.2.1（IPv4）或 2001:db8::1（IPv6）的 4242 端口等待连接。最简单的连接方式是：

.. code-block:: console

    $ telnet 192.0.2.1 4242     # use this for IPv4
    $ telnet 2001:db8::1 4242   # or this for IPv6

建立连接后，应用程序会将发送给它的每一行内容原样回显。与上述 :zephyr:code-sample:`sockets-echo` 示例不同，本应用程序支持多个并发客户端连接。你可以打开另一个终端窗口并运行上面相同的 telnet 命令。
本示例默认最多支持 3 个已连接客户端，但可以通过修改源代码中定义的 ``NUM_FDS`` 来调整该数量。

Wi-Fi
=====

可通过 :ref:`Wi-Fi snippet <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。

在 POSIX 主机上运行应用程序
========================================

同一份应用程序源代码也可以针对 POSIX 系统（例如 Linux）进行构建。（注：查看源码可以发现，除了 Zephyr 与 POSIX 包含的头文件不同，以及 Linux 下需要额外设置一个选项以将 Socket 设为仅限 IPv6 之外，其余代码完全一致。）

构建方法：

.. code-block:: console

    $ make -f Makefile.host

运行方法：

.. code-block:: console

    $ ./socket_echo

测试方法：

.. code-block:: console

    $ telnet 127.0.0.1 4242   # use this for IPv4
    $ telnet ::1 4242         # or this for IPv6

可以看到，该应用程序的行为与 Zephyr 版本完全一致。
