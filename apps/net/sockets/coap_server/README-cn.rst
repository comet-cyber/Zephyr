.. zephyr:code-sample:: coap-server
   :name: CoAP 服务
   :relevant-api: coap coap_service

   使用 CoAP 服务器子系统注册 CoAP 资源。

概述
********

本示例展示如何将 CoAP 资源注册到主 CoAP 服务中。该 CoAP 服务器实现要求所有服务和资源在编译期可用，因为它们会被放入专用的链接器段（section）中。

资源会根据所属服务的名称被放置到对应的链接器段中。为此需要提供一个链接器脚本文件，示例请参阅 ``sections-ram.ld`` 。

本演示假定所选平台具备网络支持，实际使用时可能需要对配置做适当调整。

本示例将在专为 CoAP 节点保留的站点本地（site-local）IPv6 组播地址上，监听默认的 CoAP UDP 端口（5683，安全 CoAP 则为 5684）上的请求。

本示例导出以下资源：

.. code-block:: none

   /test
   /seg1/seg2/seg3
   /query
   /separate
   /large
   /location-query
   /large-update

通过这些资源，可以针对 coap-server 运行大部分 ETSI 测试用例。

构建与运行
********************

按如下方式构建 CoAP 服务器示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/coap_server
   :board: <board to use>
   :goals: build
   :compact:

若要改为构建带有安全 CoAP 资源的示例，请使用 :zephyr_file:`overlay-dtls.conf <samples/net/sockets/coap_server/overlay-dtls.conf>` 。

本工程在正常运行时没有控制台输出，可以使用 tcpdump 或 wireshark 等外部工具验证其功能是否正常。

更多详情请参阅 `net-tools`_ 项目。

本示例可按照 :ref:`networking_with_host` 中的说明，在 QEMU 或 native_sim 开发板上构建并运行。

在主机上使用以下命令运行 `libcoap`_ 实现的 ETSI 测试用例：

.. code-block:: console

   sudo ./examples/etsi_coaptest.sh -i tap0 2001:db8::1

若要构建支持 TI CC2520 射频芯片的版本，请使用随附的启用了 IEEE 802.15.4 的 prj_cc2520.conf 配置文件。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

.. _`libcoap`: https://github.com/obgm/libcoap

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。
