.. zephyr:code-sample:: coap-client-tcp
   :name: CoAP TCP 客户端
   :relevant-api: coap coap_client_tcp

   使用基于 TCP 的 CoAP 客户端与 CoAP 服务器进行通信。

概述
********

本示例演示了如何使用基于 TCP 的 CoAP（CoAP over TCP）客户端 API，按照 RFC 8323 规范通过可靠传输协议与 CoAP 服务器进行通信。

本演示假定所选硬件平台支持网络功能，实际使用时可能需要对配置进行适当调整。

本示例展示了以下功能：

- 连接到 CoAP TCP 服务器
- 使用事件回调等待 CSM（Capabilities and Settings Message）交互完成
- 通过 TCP 发送 GET 请求
- 结合基于事件的等待机制使用 Ping/Pong 信号
- 优雅释放会话（Session Release）
- 处理服务器信号（Release、Abort）的事件回调

环境要求
************

- :ref:`networking_with_host` 、 :ref:`networking_with_native_sim`
- 开发板与运行 CoAP 服务器的主机之间的网络连接
- 支持 TCP 的 CoAP 服务器，例如 `aiocoap`_

构建与运行
********************

运行本示例应用程序最简便的方法是将其作为 native_sim 应用程序进行构建和运行，具体需要按照 :ref:`networking_with_native_sim` 中的说明完成相关配置。

主机上必须运行支持 TCP 的 CoAP 服务器。使用 ``aiocoap`` 启动服务器的示例如下：

.. code-block:: bash

    python -m pip install "aiocoap[all]"
    mkdir file_root
    echo "Hello from CoAP TCP!" > file_root/test
    aiocoap-fileserver --bind "coap+tcp://[::]:5683" file_root

运行 net-tools 中的 :command:`net-setup.sh` 脚本：

.. code-block:: bash

   ./net-setup.sh

构建并运行本示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/coap_client_tcp
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:

配置
*************

可通过 Kconfig 以及 ``src/main.c`` 文件修改服务器地址和端口：

- :kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV4_ADDR` ：服务器 IP 地址
- ``PEER_PORT`` ：服务器端口（默认值：5683）
- ``RESOURCE_PATH`` ：要请求的资源路径（默认值："test"）

相关的 Kconfig 选项如下：

- :kconfig:option:`CONFIG_COAP_OVER_RELIABLE_TRANSPORT` ：启用基于 TCP 的 CoAP 支持
- :kconfig:option:`CONFIG_COAP_CLIENT_TCP` ：启用 CoAP TCP 客户端
- :kconfig:option:`CONFIG_COAP_CLIENT_MESSAGE_SIZE` ：最大消息大小

相关参考
************

- :zephyr:code-sample:`coap-client`
- :zephyr:code-sample:`coap-server`
- `RFC 8323 - CoAP over TCP, TLS, and WebSockets <https://tools.ietf.org/html/rfc8323>`_
- `aiocoap`_

.. _aiocoap: https://github.com/chrysn/aiocoap
