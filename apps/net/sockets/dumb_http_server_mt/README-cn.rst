.. zephyr:code-sample:: socket-dumb-http-server-mt
   :name: 简易多线程 HTTP 服务器 (Dumb HTTP server multi-threaded)
   :relevant-api: bsd_sockets net_pkt thread_apis tls_credentials

   使用 BSD Sockets 实现支持并发连接的简易 HTTP 服务器。

概述
********

Zephyr 的 ``sockets/dumb_http_server_mt`` 示例应用程序使用兼容 BSD Sockets 的 API 实现了一个框架级 HTTP 服务器。本示例的功能与 :zephyr:code-sample:`socket-dumb-http-server` 类似，不同之处在于它支持多个并发连接、TLS 以及 IPv6。此外，本示例应用程序不兼容 POSIX。该 HTTP 服务器示例非常精简，并不会真正解析收到的 HTTP 请求，而是直接读取并丢弃请求内容，并始终返回同一个静态页面。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/dumb_http_server_mt` 。

环境要求
**************

- :ref:`networking_with_host`
- 或者一块具备硬件网络功能的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 ``sockets/dumb_http_server_mt`` 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/dumb_http_server_mt
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会在 192.0.2.1 或 2001:db8::1 的 8080 端口上等待连接。最简单的连接方式是在 Web 浏览器中打开以下 URL： http://192.0.2.1:8080/ 或 http://[2001:db8::1]:8080/ 。你应该会看到一个包含 Zephyr 示例介绍内容的页面（抓取自特定时间点的 Zephyr 官方网站，请注意其内容可能与当前在线的 Zephyr 网站有所不同）。或者，也可以使用 ``curl`` 等工具进行访问：

.. code-block:: console

    $ curl http://192.0.2.1:8080/

最后，你还可以针对该服务器运行 Apache Bench（ ``ab`` ）等 HTTP 性能分析/负载测试工具::

    $ ab -n10 http://192.0.2.1:8080/

其中 ``-n`` 参数用于指定向服务器发起的 HTTP 请求数量。
