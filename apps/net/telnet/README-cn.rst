.. zephyr:code-sample:: telnet-console
   :name: Telnet 控制台
   :relevant-api: shell_api net_core net_if net_mgmt

   通过 Telnet 访问 Zephyr Shell。

概述
********

本应用程序会在默认网络接口上配置 IPv4/IPv6 地址。Telnet 控制台服务会随 Shell 以及两个 Shell 模块（net 和 kernel）由内核透明启动。启动并运行后，你可以通过网络使用 Telnet 客户端连接到目标设备。

环境要求
**************

- :ref:`networking_with_qemu`


构建与运行
********************

QEMU x86
========

以下说明介绍了如何在连接到提供 DHCP 服务的网络的 Linux 宿主机上，使用 QEMU 运行本示例应用程序。

如需使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。

在 QEMU 中运行 Zephyr samples/net/telnet 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/telnet
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

启动后，你应该能看到 IP 地址详细信息，例如：

.. code-block:: console

    [Setup] [INF] main: Starting Telnet sample
    [Setup] [INF] setup_ipv4: IPv4 address: 192.0.2.1
    [Setup] [INF] setup_ipv6: IPv6 address: 2001:db8::1

此时，QEMU 客户机已启动并正在运行。按如下方式从 Linux 宿主机连接到 Telnet 控制台：

.. code-block:: console

    $ telnet 192.0.2.1
    Telnet escape character is '^]'.
    Trying 192.0.2.1...
    Connected to 192.0.2.1.
    Escape character is '^]'.

现在按下回车键，Shell 提示符将会出现，你可以输入命令，例如 ``help`` 。


Freedom-K64F 开发板
========================

以下说明介绍了如何在 Freedom-K64F 开发板上运行并使用本示例应用程序。与在 QEMU 上运行不同， :zephyr:board:`Freedom-K64F 开发板 <frdm_k64f>` 的 IPv4 网络配置依赖 DHCPv4。如果确实需要，你可以修改 :file:`prj_frdm_k64f.conf` 来设置静态 IPv4 地址。

有关构建、烧录以及使用串口控制台日志的详细说明，请参阅 :zephyr:board:`Freedom-K64F 开发板 <frdm_k64f>` 文档章节。

使用以太网网线将 :zephyr:board:`Freedom-K64F <frdm_k64f>` 开发板连接到通过 DHCPv4 提供 IPv4 地址配置的局域网。在局域网中自行搭建 DHCP 服务器不在本 README 的讨论范围内。

构建 Zephyr samples/net/telnet 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/telnet
   :board: frdm_k64f
   :goals: build
   :compact:

按照上文提到的 :zephyr:board:`Freedom-K64F <frdm_k64f>` 开发板文档烧录生成的 Zephyr 固件镜像。

在宿主机上打开连接至开发板的串口控制台：

.. code-block:: console

    $ sudo screen /dev/ttyACM0 115200

将以太网网线插入 :zephyr:board:`Freedom-K64F <frdm_k64f>` 开发板。复位开发板后，你首先会在控制台上看到：

.. code-block:: console

    [dev/eth_mcux] [INF] eth_0_init: Enabled 100M full-duplex mode.
    [dev/eth_mcux] [DBG] eth_0_init: MAC 00:04:9f:69:c7:36
    shell> [Setup] [INF] main: Starting Telnet sample
    [Setup] [INF] setup_dhcpv4: Running dhcpv4 client...
    [Setup] [INF] setup_ipv6: IPv6 address: 2001:db8::1

如果 DHCPv4 客户端成功获取地址，很快还会看到类似如下输出：

.. code-block:: console

   [Setup] [INF] ipv4_addr_add_handler: IPv4 address: 192.168.0.21
   [Setup] [INF] ipv4_addr_add_handler: Lease time: 86400 seconds
   [Setup] [INF] ipv4_addr_add_handler: Subnet: 255.255.255.0
   [Setup] [INF] ipv4_addr_add_handler: Router: 192.168.0.1

上述结果取决于你所在的局域网环境。此时，你应该能够通过网络使用 Telnet 进行连接。在 Linux 宿主机上执行：

.. code-block:: console

    $ telnet 192.168.0.21
    Telnet escape character is '^]'.
    Trying 192.168.0.21...
    Connected to 192.168.0.1.
    Escape character is '^]'.

现在你已成功连接，就像使用 UART 控制台一样，你可以通过 Telnet 客户端输入命令并获取输出。

Wi-Fi
=====

本示例可通过 :ref:`Wi-Fi 代码片段（Snippet） <snippet-wifi-ipv4>` 启用 IPv4 Wi-Fi 支持。
