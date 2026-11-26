.. zephyr:code-sample:: socket-dumb-http-server
   :name: 极简 HTTP 服务器 (Dumb HTTP server)
   :relevant-api: bsd_sockets net_pkt

   使用 BSD Sockets 实现简单、可移植的 HTTP 服务器。

概述
********

适用于 Zephyr 的 sockets/dumb_http_server 示例应用程序使用兼容 BSD Sockets 的 API 实现了一个框架级极简 HTTP 服务器。本示例旨在展示如何开发一个同时可移植到 POSIX 和 Zephyr 的 Socket 应用程序。因此，该 HTTP 服务器示例保持了极简设计，并不会真正解析收到的 HTTP 请求，而只是读取并丢弃请求内容，并始终返回同一个静态页面。尽管做了如此简化，它作为一个可通过常规 Web 浏览器访问的 Socket 应用程序示例，或者用于配合现有 HTTP 诊断工具执行性能/回归测试，依然非常实用。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/sockets/dumb_http_server` 。

环境要求
**************

- :ref:`networking_with_host`
- 或者带有硬件网络接口的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 sockets/echo 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/dumb_http_server
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会在 192.0.2.1 的 8080 端口等待连接。最简单的连接方式是在 Web 浏览器中打开以下 URL： http://192.0.2.1:8080/ 。你应该会看到一个包含 Zephyr 示例内容的页面（该页面抓取自某一特定时间点的 Zephyr 官方网站，请注意其内容可能与当前在线的 Zephyr 网站有所不同）。此外，也可以使用 ``curl`` 等工具进行访问：

.. code-block:: console

    $ curl http://192.0.2.1:8080/

最后，你还可以针对该服务器运行 Apache Bench（ ``ab`` ）等 HTTP 性能分析/压测工具： ::

    $ ab -n10 http://192.0.2.1:8080/

``-n`` 参数用于指定向服务器发起的 HTTP 请求数量。

在 POSIX 主机上运行应用程序
========================================

同一份应用程序源代码也可以针对 POSIX 系统（如 Linux）进行构建。（注：查看源代码即可发现，除了 Zephyr 与 POSIX 所包含的头文件不同之外，其余代码完全一致。）

构建方法：

.. code-block:: console

    $ make -f Makefile.host

运行方法：

.. code-block:: console

    $ ./socket_dumb_http

测试时，请连接到 http://127.0.0.1:8080/ ，并按照上一节中的步骤进行操作。

可以看到，该应用程序的行为与 Zephyr 版本完全一致。
