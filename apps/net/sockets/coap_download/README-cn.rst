.. zephyr:code-sample:: coap-download
   :name: CoAP 下载
   :relevant-api: coap

   使用 CoAP 客户端 API 通过 GET 请求下载数据

概述
********

本示例演示如何使用 CoAP 客户端 API 向 CoAP 服务器发起 GET 请求。如果待获取的数据大于单个 CoAP 数据包，程序将使用分块传输（blockwise transfer）来接收数据。

传输完成后，示例会打印接收到的数据量以及所耗费的时间。

环境要求
**************

- :ref:`networking_with_host` 、 :ref:`networking_with_native_sim`
- 或者一块具备硬件网络功能的开发板（已在 nucleo_h753zi 上测试）
- 开发板与运行 CoAP 服务器的主机之间具备网络连接

构建与运行
*****************

按如下方式构建 CoAP 下载示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/coap_download
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

运行本示例应用程序最简便的方式是将其作为 native_sim 应用程序进行构建和运行。这需要按照 :ref:`networking_with_native_sim` 中的说明完成一些前置设置。

下载一个 CoAP 服务器应用程序，例如 `aiocoap`_ （Python），或者使用 `Eclipse Californium`_ （Java）提供的 `Simple File Server`_ 演示应用程序。

使用 ``aiocoap`` ：

.. code-block:: bash

    python -m pip install "aiocoap[all]"
    mkdir file_root
    echo "some test data" > file_root/test.txt
    aiocoap-fileserver file_root

你也可以通过 Kconfig 修改要请求的 CoAP 资源名称：

.. code-block:: cfg

    CONFIG_NET_SAMPLE_COAP_RESOURCE_PATH="resource_name_to_request"

启动 net-tools 中的 :command:`net-setup.sh` ：

.. code-block:: bash

   ./net-setup.sh

按如下方式针对 native_sim 构建并运行 coap_download 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/coap_download
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:

示例输出
=============

.. code-block:: console

    [00:00:00.000,000] <inf> net_config: Initializing network
    [00:00:00.000,000] <inf> net_config: IPv4 address: 192.0.2.1
    [00:00:00.110,000] <inf> net_config: IPv6 address: 2001:db8::1
    [00:00:00.110,000] <inf> net_config: IPv6 address: 2001:db8::1
    [00:00:00.110,000] <inf> coap_download: Network L4 is connected
    [00:00:00.110,000] <inf> coap_download: Starting CoAP download using IPv4
    [00:00:00.180,000] <inf> coap_download: CoAP response, result_code=69, offset=0, len=100
    [00:00:00.180,000] <inf> coap_download: CoAP download done, got 100 bytes in 70 ms
    [00:00:00.180,000] <inf> coap_download: Starting CoAP download using IPv6
    [00:00:00.300,000] <inf> coap_download: CoAP response, result_code=69, offset=0, len=100
    [00:00:00.300,000] <inf> coap_download: CoAP download done, got 100 bytes in 120 ms

.. _aiocoap: https://github.com/chrysn/aiocoap
.. _Eclipse Californium: https://github.com/eclipse-californium/californium
.. _Simple File Server: https://github.com/eclipse-californium/californium/tree/main/demo-apps/cf-simplefile-server
