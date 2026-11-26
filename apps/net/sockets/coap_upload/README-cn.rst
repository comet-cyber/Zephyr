.. zephyr:code-sample:: coap-upload
   :name: CoAP 上传
   :relevant-api: coap

   使用 CoAP 客户端 API 通过 PUT 请求上传数据

概述
********

本示例演示如何使用 CoAP 客户端 API 通过 PUT 请求向 CoAP 服务器上传内容。本示例展示了多种内容上传方式：

  * 使用 Payload 指针进行短数据上传，
  * 使用 Payload 回调函数进行短数据上传，
  * 使用 Payload 指针进行分块传输（Block transfer）上传，
  * 使用 Payload 回调函数进行分块传输上传。

本示例兼容 :zephyr:code-sample:`coap-server` 示例，也可配合独立的 CoAP 服务器（例如 `aiocoap`_ ）运行。

环境要求
************

- :ref:`networking_with_host` 、 :ref:`networking_with_native_sim`
- 或者，一块支持硬件网络的开发板（已在搭配 ``wifi-ipv4`` snippet 的 nrf7002dk 开发板上测试通过）
- 开发板与运行 CoAP 服务器的宿主机之间具备网络连接

构建与运行
*****************

按如下方式构建 CoAP 上传示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/coap_upload
   :board: <board to use>
   :goals: build
   :compact:

运行本示例应用程序最简便的方式是将其作为 native_sim 应用程序构建并运行。这需要按照
:ref:`networking_with_native_sim` 中的说明进行一些环境配置。

下载一个 CoAP 服务器应用程序，例如 `aiocoap`_ （Python）。

使用 ``aiocoap`` ：

.. code-block:: bash

    python -m pip install "aiocoap[all]"
    mkdir file_root
    aiocoap-fileserver --write file_root

启动 net-tools 中的 :command:`net-setup.sh` ：

.. code-block:: bash

    ./net-setup.sh

按如下方式针对 native_sim 构建并运行 CoAP 上传示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/coap_upload
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
    [00:00:00.110,000] <inf> net_samples_common: Network connectivity established and IP address assigned
    [00:00:00.110,000] <inf> net_samples_common: Waiting for network...
    [00:00:00.110,000] <inf> coap_upload:
    [00:00:00.110,000] <inf> coap_upload: * Starting CoAP upload using IPv4
    [00:00:00.110,000] <inf> coap_upload:
    [00:00:00.110,000] <inf> coap_upload: ** CoAP upload short
    [00:00:00.180,000] <inf> coap_upload: CoAP upload short done in 70 ms
    [00:00:00.180,000] <inf> coap_upload:
    [00:00:00.180,000] <inf> coap_upload: ** CoAP upload short with callback
    [00:00:00.240,000] <inf> coap_upload: CoAP upload short with callback done in 60 ms
    [00:00:00.240,000] <inf> coap_upload:
    [00:00:00.240,000] <inf> coap_upload: ** CoAP upload blockwise
    [00:00:00.300,000] <inf> coap_upload: CoAP upload blockwise ongoing, sent 128 bytes so far
    [00:00:00.360,000] <inf> coap_upload: CoAP upload blockwise ongoing, sent 256 bytes so far
    [00:00:00.420,000] <inf> coap_upload: CoAP upload blockwise ongoing, sent 384 bytes so far
    [00:00:00.480,000] <inf> coap_upload: CoAP upload blockwise done in 240 ms
    [00:00:00.480,000] <inf> coap_upload:
    [00:00:00.480,000] <inf> coap_upload: ** CoAP upload blockwise with callback
    [00:00:00.540,000] <inf> coap_upload: CoAP upload blockwise with callback ongoing, sent 128 bytes so far
    [00:00:00.600,000] <inf> coap_upload: CoAP upload blockwise with callback ongoing, sent 256 bytes so far
    [00:00:00.660,000] <inf> coap_upload: CoAP upload blockwise with callback ongoing, sent 384 bytes so far
    [00:00:00.720,000] <inf> coap_upload: CoAP upload blockwise with callback done in 240 ms
    [00:00:01.230,000] <inf> coap_upload:
    [00:00:01.230,000] <inf> coap_upload: * Starting CoAP upload using IPv6
    [00:00:01.230,000] <inf> coap_upload:
    [00:00:01.230,000] <inf> coap_upload: ** CoAP upload short
    [00:00:01.320,000] <inf> coap_upload: CoAP upload short done in 90 ms
    [00:00:01.320,000] <inf> coap_upload:
    [00:00:01.320,000] <inf> coap_upload: ** CoAP upload short with callback
    [00:00:01.380,000] <inf> coap_upload: CoAP upload short with callback done in 60 ms
    [00:00:01.380,000] <inf> coap_upload:
    [00:00:01.380,000] <inf> coap_upload: ** CoAP upload blockwise
    [00:00:01.440,000] <inf> coap_upload: CoAP upload blockwise ongoing, sent 128 bytes so far
    [00:00:01.500,000] <inf> coap_upload: CoAP upload blockwise ongoing, sent 256 bytes so far
    [00:00:01.560,000] <inf> coap_upload: CoAP upload blockwise ongoing, sent 384 bytes so far
    [00:00:01.620,000] <inf> coap_upload: CoAP upload blockwise done in 240 ms
    [00:00:01.620,000] <inf> coap_upload:
    [00:00:01.620,000] <inf> coap_upload: ** CoAP upload blockwise with callback
    [00:00:01.680,000] <inf> coap_upload: CoAP upload blockwise with callback ongoing, sent 128 bytes so far
    [00:00:01.740,000] <inf> coap_upload: CoAP upload blockwise with callback ongoing, sent 256 bytes so far
    [00:00:01.800,000] <inf> coap_upload: CoAP upload blockwise with callback ongoing, sent 384 bytes so far
    [00:00:01.860,000] <inf> coap_upload: CoAP upload blockwise with callback done in 240 ms

.. _aiocoap: https://github.com/chrysn/aiocoap
