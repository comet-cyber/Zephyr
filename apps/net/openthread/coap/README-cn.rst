.. zephyr:code-sample:: ot-coap
   :name: OpenThread CoAP 客户端与服务器应用程序
   :relevant-api: openthread

   构建全功能 Thread 设备（Full Thread Device，FTD）CoAP 服务器与客户端。

概述
********

本示例演示了如何使用 OpenThread CoAP API。它可以编译为作为服务器或客户端运行。

通过在两块开发板上分别运行客户端和服务器，即可组建一个本地 Thread 网络。OpenThread 使用通过 Kconfig 提供的网络密钥来创建网络。开发板烧录完成后，网络将自动完成创建与配置。

待网络正常运行后，客户端即可开始与服务器进行交互。用户每次按下按键时，服务器上的 LED 状态都会翻转。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/openthread/coap` 。

.. note::
   尽管 Zephyr 拥有自身的 CoAP API，但本示例使用的是 OpenThread CoAP API。那么为什么要在此使用 OpenThread CoAP API 呢？

   * OpenThread 在内部使用该 API 来实现其众多服务。
   * OpenThread CoAP API 能够更直接地访问无线射频（Radio）。

   因此，使用 OpenThread CoAP API 替代 Zephyr 自带的 CoAP API 可以降低开销，尽管这会降低应用程序的可移植性。

构建与运行
********************

按如下方式构建 OpenThread FTD CoAP 服务器示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coap
   :board: <board to use>
   :west-args: -T sample.net.openthread.ftd.coap.server
   :goals: build
   :compact:

按如下方式构建 OpenThread FTD CoAP 客户端示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coap
   :board: <board to use>
   :west-args: -T sample.net.openthread.ftd.coap.client
   :goals: build
   :compact:

为 cc1352p7 LaunchPad 构建 CoAP 服务器的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coap
   :host-os: unix
   :board: cc1352p7_lp
   :west-args: -T sample.net.openthread.ftd.coap.server
   :goals: build flash
   :compact:

为 cc1352p7 LaunchPad 构建 CoAP 客户端的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coap
   :host-os: unix
   :board: cc1352p7_lp
   :west-args: -T sample.net.openthread.ftd.coap.client
   :goals: build flash
   :compact:

检查 Thread 网络状态
*****************************

在服务器和客户端开发板上分别打开控制台，然后检查状态：

.. code-block:: console

   server:~$ ot state
   router
   Done

有效状态可以是 child、router 或 leader。

当 Thread 网络正常运行后，即可开始使用客户端。

使用客户端开发板上的按键控制服务器开发板的 LED
**********************************************************************

Thread 网络正常运行后无需额外配置。只需按下客户端上的按键 sw0，即可看到服务器上的 led0 状态翻转。

客户端使用广播地址请求 CoAP 服务器翻转 LED。由于客户端并不知道服务器的具体地址，如果网络中存在第二个服务器，那么第二块开发板上的 LED 也会随之翻转。

从计算机控制服务器开发板的 LED
**********************************************

尽管我们使用的是 OpenThread CoAP API，但仍然可以与网络上的任何 CoAP 客户端或服务器交互。在此示例中，我们将从一台不在 Thread 网络内的计算机控制该 LED。这需要在同一网络中部署启用了 NAT64 支持的 `OpenThread Border Router`_ 。

首先，检查服务器（或客户端）是否已连接到 OTBR（otbr）并且可以使用 NAT64：

.. code-block:: console

   server:~$ ot netdata show
   router
   Done
   Prefixes:
   fd6f:cb3a:802:1::/64 paos low dc00
   Routes:
   fc00::/7 sa med dc00
   fd6f:cb3a:802:2:0:0::/96 sn low dc00
   Services:
   44970 01 14000500000e10 s dc00 0
   44970 5d fd78b9ce54779c6eb5484d062c3b5b22d120 s dc00 1
   Contexts:
   fd6f:cb3a:802:1::/64 1 c
   Commissioning:
   11426 - - -
   Done

Prefixes 显示了供 Thread 网络外部设备联系 Thread 网络内部设备所使用的 IPv6 前缀。

设备应当拥有一个使用该前缀的 IPv6 地址：

.. code-block:: console

   server:~$ ot ipaddr
   fd78:b9ce:5477:9c6e:0:ff:fe00:a800
   fd6f:cb3a:802:1:f0ec:c1e2:c1bb:744
   fd78:b9ce:5477:9c6e:75b8:386c:1f79:1013
   fe80:0:0:0:50d1:bed5:6e6e:ad75
   Done

fd6f:cb3a:802:1:f0ec:c1e2:c1bb:744 即为可从 Thread 网络外部联系该 CoAP 服务器的 IPv6 地址。

我们还可以检查是否能够从 Thread 网络访问互联网：

.. code-block:: console

   server:~$ ot ping 8.8.8.8
   Pinging synthesized IPv6 address: fd6f:cb3a:802:2:0:0:808:808
   16 bytes from fd6f:cb3a:802:2:0:0:808:808: icmp_seq=1 hlim=114 time=36ms
   1 packets transmitted, 1 packets received. Packet loss = 0.0%. Round-trip min/avg/max = 36/36.0/36 ms.
   Done

如果一切正常，就可以开始从计算机控制该 LED 了。为此，我们使用 Python 编写的工具 aiocoap-client。首先安装该工具：

.. code-block:: shell

   pip install aiocoap


然后向服务器发送请求以翻转 LED：

.. code-block:: shell

    aiocoap-client -m PUT --payload '{"led_id":0,"state":2}'  coap://[fd6f:cb3a:802:1:f0ec:c1e2:c1bb:744]/led

此时 LED 状态应当已发生改变。


.. _OpenThread Border Router: https://openthread.io/codelabs/openthread-border-router-nat64

使用 Shell 命令控制服务器开发板的 LED
****************************************************

本示例还提供了一条 Shell 命令，用于从客户端控制服务器上的 LED。

翻转 LED：

.. code-block::

   $client:~$ ot_coap led set 0 toggle

此时 LED 状态应当已发生改变。

与按键控制相同，该命令默认使用广播地址。若要控制特定服务器的 LED，可以指定其 IPv6 地址：

.. code-block::

   $client:~$ ot_coap led set 0 toggle fd6f:cb3a:802:1:f0ec:c1e2:c1bb:744
