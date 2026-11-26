.. zephyr:code-sample:: quic-client-echo
   :name: Echo 客户端 (QUIC)
   :relevant-api: quic

   使用 QUIC API 和 Socket 服务 API 实现简单的 IPv4/IPv6 Echo 客户端。

概述
********

适用于 Zephyr 的 quic/echo_client 示例应用程序使用兼容 BSD Sockets 的 API 实现了一个支持 IPv4 和 IPv6 的 QUIC 协议 Echo 客户端。

本示例旨在展示如何使用 QUIC API 和 Socket 服务（socket service）API。Socket 服务的设计理念是由单个线程监听多个阻塞式 Socket，并在这组 Socket 中出现活动时触发回调函数。由于系统中只需创建一个线程，这种方式能够有效节省内存。

该应用程序支持 IPv4 和 IPv6，并使用 QUIC 协议（ :rfc:`9000` ）实现该服务。本示例应用程序的源代码位于： :zephyr_file:`samples/net/quic/echo_client` 。

环境要求
**************

- :ref:`networking_with_host`
- 或者带有硬件网络接口的开发板

构建与运行
********************

按如下方式构建 Zephyr 版本的 quic/echo_client 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/quic/echo_client
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会尝试连接到 192.0.2.2 或 2001:db8::2 的 4422 端口。监听这些连接最简便的方式是使用 net-tools 项目中的辅助 echo-server 脚本：

.. code-block:: console

    $ ./quic-echo-server.py --host 192.0.2.2 --certificate quic-ca-cert.pem --private-key quic-private-key.pem --max-stream-data 8192
    $ ./quic-echo-server.py --host 2001:db8::1 --certificate quic-ca-cert.pem --private-key quic-private-key.pem

连接建立后，echo-client 应用程序会校验从 echo-server 应用程序接收回来的数据是否与之前发送的数据一致。quic-echo-server.py 应用程序会在最后打印统计信息。
