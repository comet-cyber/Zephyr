.. zephyr:code-sample:: async-sockets-echo-select
   :name: 使用 select() 的异步回显服务器
   :relevant-api: bsd_sockets

   使用 BSD Socket 和 select() 实现异步 IPv4/IPv6 TCP 回显服务器

概述
********

Zephyr 的 sockets/echo_async_select 示例应用程序使用兼容 BSD Sockets 的 API，结合非阻塞 Socket 和 ``select()`` 调用，实现了一个异步 IPv4/IPv6 TCP 回显（echo）服务器。本示例是 :zephyr:code-sample:`async-sockets-echo` 示例的一个变体。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/echo_async_select` 。

环境要求
**************

- :ref:`networking_with_host`
- 或者一块具备硬件网络功能（包括 6LoWPAN）的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 sockets/echo_async 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_async_select
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会在端口 4242 上等待发往 192.0.2.1（IPv4）或 2001:db8::1（IPv6）的连接。最简便的连接方式是：

.. code-block:: console

    $ telnet 192.0.2.1 4242     # use this for IPv4
    $ telnet 2001:db8::1 4242   # or this for IPv6

建立连接后，应用程序会将发送给它的任意一行内容原样回显。与 :zephyr:code-sample:`sockets-echo` 示例不同，本应用程序支持多个并发客户端连接。你可以打开另一个终端窗口，运行与上面相同的 telnet 命令。
本示例最多支持 3 个已连接的客户端，但可以通过修改源代码中定义的 ``NUM_FDS`` 来调整该数量。

在 POSIX 主机上运行应用程序
========================================

同一份应用程序源代码也可以针对 POSIX 系统（例如 Linux）进行构建。（注意：如果查看源代码，你会发现除了 Zephyr 与 POSIX 所用的头文件不同，以及在 Linux 上需要将 Socket 额外设置为仅限 IPv6（IPv6-only）选项外，其余代码完全相同。）

构建：

.. code-block:: console

    $ make -f Makefile.host

运行：

.. code-block:: console

    $ ./socket_echo

测试：

.. code-block:: console

    $ telnet 127.0.0.1 4242   # use this for IPv4
    $ telnet ::1 4242         # or this for IPv6

可以看到，该应用程序的行为与 Zephyr 版本一致。
