.. zephyr:code-sample:: coap-client
   :name: CoAP 客户端
   :relevant-api: coap

   使用 CoAP 库实现一个用于获取资源的客户端。

概述
********

本示例是一个简单的 CoAP 客户端，演示了如何从资源中获取信息。

本演示假定所选平台已支持网络功能，可能需要根据实际情况对配置进行适当调整。

本示例会连接到由 ``CONFIG_NET_SAMPLE_COAP_CLIENT_PEER`` 指定的 CoAP 服务器。对端（Peer）的值可以是 IPv4 字面量地址、IPv6 字面量地址或主机名。如果省略端口号，示例将使用默认的 CoAP 端口 5683。

在默认配置下，目标 URI 可表示为：

.. code-block:: none

    coap://[2001:db8::1]:5683/test

其他有效的对端字符串包括：

.. code-block:: none

    192.0.2.1:5683
    192.0.2.42
    [2001:db8::1]:5683
    [2001:db8::2]
    example.com:5683
    example.com

可选的响应超时时间与分块传输（Block-wise）重试行为可通过 ``CONFIG_NET_SAMPLE_COAP_CLIENT_REPLY_TIMEOUT_MS`` 和 ``CONFIG_NET_SAMPLE_COAP_CLIENT_BLOCKWISE_MAX_RETRIES`` 进行配置。

例如，可通过如下方式设置 IPv4 对端端点：

.. code-block:: none

    CONFIG_NET_SAMPLE_COAP_CLIENT_PEER="192.0.2.1:5683"

若已启用 DNS 并进行基于主机名的测试，可配置为：

.. code-block:: none

    CONFIG_NET_SAMPLE_COAP_CLIENT_PEER="example.com:5683"

有关可用于手动互操作性测试的简易辅助服务器，请参见 ``net-tools\coap-test-server\`` 目录下的 ``coap_sample_server.py`` 。

构建与运行
********************

本工程会将接收到的响应报文的所有字节（Octets）打印出来；如需获取更多上下文信息，可使用 tcpdump 或 Wireshark 等工具进行抓包分析。

更多详情请参见 `net-tools`_ 项目。

有关测试服务器脚本的更多详情，请参见 ``net-tools\coap-test-server\README.md`` 。

本示例可按照 :ref:`networking_with_host` 中的说明，在 QEMU 或 native_sim 开发板上构建并运行。

示例输出
=============

.. code-block:: console

  reply: 60 00 00 00 00 24 11 40 fe 80 00 00 00 00 00 00 5c 25 e2 ff fe
  15 01 01 fe 80 00 00 00 00 00 00 5c 25 e2 ff fe 15 01 01 16 33 16 33
  00 24 3d 86 60 40 00 01 ff 54 79 70 65 3a 20 30 0a 43 6f 64 65 3a 20
  31 0a 4d 49 44 3a 20 31 0a (76 bytes)

.. note::

   上方显示的数值可能会有所不同。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
