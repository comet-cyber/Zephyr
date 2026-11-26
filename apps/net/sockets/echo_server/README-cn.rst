.. zephyr:code-sample:: sockets-echo-server
   :name: 回显服务器（高级）
   :relevant-api: bsd_sockets tls_credentials

   实现一个将接收到的数据包原样发回给发送方的 UDP/TCP 服务器。

概述
********

Zephyr 的 echo-server 示例应用程序实现了一个与 echo-client 示例应用程序配套使用的 UDP/TCP 服务器：echo-server 监听传入的 IPv4 或 IPv6 数据包（由 echo 客户端发送），并直接将其原样发回。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/echo_server` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

本应用程序有多种使用方式。最常见的使用场景之一是在 QEMU 中运行 echo-server 应用程序，具体说明请参阅 :ref:`networking_with_qemu` 。

echo-server 目录下提供了适用于不同开发板和配置的配置文件：

- :file:`prj.conf`
  通用配置文件，通常应使用此文件。

- :file:`overlay-ot.conf`
  该 overlay 配置启用对 OpenThread 的支持。

- :file:`overlay-802154.conf`
  该 overlay 配置启用对原生 IEEE 802.15.4 连接的支持。
  注意，默认情况下 IEEE 802.15.4 L2 使用无确认（unacknowledged）通信。为提高连接可靠性，可通过 Shell 命令启用确认机制： ``ieee802154 ack set`` 。

- :file:`overlay-qemu_802154.conf`
  当仿真两个互联的 QEMU 实例组建 IEEE 802.15.4 网络时，该 overlay 配置启用相应支持。

- :file:`overlay-tls.conf`
  该 overlay 配置启用对 TLS 的支持。

- :file:`overlay-tunnel.conf`
  该 overlay 配置启用对 IP 隧道（IP tunneling）的支持。

- :file:`overlay-vlan.conf`
  该 overlay 配置启用对虚拟局域网（VLAN）的支持。
  详情请参阅 :ref:`networking_samples_common` 。

按如下方式构建 echo-server 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

针对 nrf52840dk/nrf52840 并启用 OpenThread 支持的构建示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: nrf52840dk/nrf52840
   :conf: "prj.conf overlay-ot.conf"
   :goals: run
   :compact:

针对 samr21_xpro 并启用 RF2XX 驱动支持的构建示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: [samr21_xpro | sam4e_xpro | sam_v71_xult/samv71q21]
   :gen-args: -DEXTRA_CONF_FILE=overlay-802154.conf
   :goals: build flash
   :compact:

可以在终端窗口中检查通信是否正在进行：

.. code-block:: console

    $ minicom -D /dev/ttyACM0

启用 TLS 支持
====================

在构建工程时启用 ``overlay-tls.conf`` 叠加文件即可在本示例中启用 TLS 支持，例如使用以下命令：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :board: qemu_x86
   :conf: "prj.conf overlay-tls.conf"
   :goals: build
   :compact:

另一种方式是在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 。

本示例所使用的证书位于示例的 ``src`` 目录下。Socket Echo Server 与 :zephyr:code-sample:`sockets-echo-client` 所使用的默认证书支持在这两个示例之间建立安全连接。

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。

在 Linux 主机上运行 echo-client
========================================

与 Linux 主机配合使用时，有一个非常实用的测试场景：在 QEMU 中运行 echo-server，同时在 Linux 主机上运行 echo-client。

要使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。

在 QEMU 中运行 echo-server 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

在终端窗口中执行：

.. code-block:: console

    $ sudo ./echo-client -i tap0 2001:db8::1

注意，必须先在 QEMU 中运行 echo-server，然后再在主机终端窗口中启动 echo-client 应用程序。

你也可以与 Linux 主机验证 TLS 通信。有关如何使用 Linux 主机示例测试 TLS 的信息，请参阅 https://github.com/zephyrproject-rtos/net-tools 文档。

有关在 Linux 主机上运行 echo-server 而在 QEMU 中运行 echo-client 的另一种运行方式，请参阅 :zephyr:code-sample:`sockets-echo-client` 示例文档。
