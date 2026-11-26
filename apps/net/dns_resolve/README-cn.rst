.. zephyr:code-sample:: dns-resolve
   :name: DNS 解析
   :relevant-api: dns_resolve net_mgmt

   解析给定主机名的 IP 地址。

概述
********

本应用程序将为设备设置 IP 地址，然后根据用户对系统的配置尝试解析各种主机名。

- 如果启用了 IPv4，则会解析 ``www.zephyrproject.org`` 的 A 记录。
- 如果启用了 IPv6，则会解析 ``www.zephyrproject.org`` 的 AAAA 记录。
- 如果启用了 mDNS，则会解析 ``zephyr.local`` 名称。

环境要求
**************

- :ref:`networking_with_host`

- screen 终端仿真器或同类工具。

- 对于大多数没有以太网接口的开发板，需要使用 ENC28J60 以太网模块。

- dnsmasq 应用程序。本示例中使用的 dnsmasq 版本为：

.. code-block:: console

    dnsmasq -v
    Dnsmasq version 2.76  Copyright (c) 2000-2016 Simon Kelley

构建与运行
********************

网络配置
=====================

打开适用于目标平台的工程配置文件，例如： :file:`prj_frdm_k64f.conf` 是适用于 :zephyr:board:`frdm_k64f` 开发板的配置文件。

在本示例应用程序中，同时支持静态 IP 地址和 DHCPv4 IP 地址。静态 IP 地址在工程配置文件中指定，例如：

.. code-block:: cfg

	CONFIG_NET_CONFIG_MY_IPV6_ADDR="2001:db8::1"
	CONFIG_NET_CONFIG_PEER_IPV6_ADDR="2001:db8::2"

它们分别是运行 Zephyr 的 DNS 客户端和 DNS 服务器的 IPv6 地址。

DNS 服务器
================

可以使用 dnsmasq 工具进行测试。在默认安装的 Zephyr 工程环境中，可以在 `net-tools`_ 项目中找到示例 dnsmasq 启动脚本，也可以从 https://github.com/zephyrproject-rtos/net-tools 下载。

打开终端窗口并输入：

.. code-block:: console

    $ cd net-tools
    $ sudo ./dnsmasq.sh

本示例的默认工程配置使用的是公共 Google DNS 服务器。若要使用本地 dnsmasq 服务器，请编辑相应的 'prj.conf' 文件并更新 DNS 服务器地址。例如，如果使用测试常用的 IP 地址，请将其更新为以下值：

.. code-block:: cfg

    CONFIG_DNS_SERVER1="192.0.2.2:5353"
    CONFIG_DNS_SERVER2="[2001:db8::2]:5353"

.. note::
    DNS 默认使用端口 53，但 net-tools 提供的 dnsmasq.conf 文件使用端口 5353，以便无需超级用户权限即可运行该守护进程。

如果 dnsmasq 启动失败并出现类似如下错误：

.. code-block:: console

    dnsmasq: failed to create listening socket for port 5353: Address already in use

打开终端窗口并输入：

.. code-block:: console

    $ killall -s KILL dnsmasq

然后再次尝试启动 dnsmasq 应用程序。

若要测试 mDNS，请使用 net-tools 项目中的 Avahi 脚本：

.. code-block:: console

    $ cd net-tools
    $ ./avahi-daemon.sh

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

LLMNR 响应器
==================

如果希望 Zephyr 响应 Windows 主机发送的 LLMNR DNS 请求，可以设置以下配置选项：

.. code-block:: cfg

    CONFIG_NET_HOSTNAME_ENABLE=y
    CONFIG_NET_HOSTNAME="zephyr-device"
    CONFIG_DNS_RESOLVER=y
    CONFIG_LLMNR_RESPONDER=y

需要为 Zephyr 主机分配一个主机名，以便它能够响应 DNS 查询。请注意，主机名中不应包含任何点号。


QEMU x86
========

若要使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。


FRDM K64F
=========

打开终端窗口并输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/dns_resolve
   :board: frdm_k64f
   :goals: build flash
   :compact:

有关该开发板的更多信息，请参阅 :zephyr:board:`Freedom-K64F 开发板文档 <frdm_k64f>` 。

打开终端窗口并输入：

.. code-block:: console

    $ screen /dev/ttyACM0 115200


使用 'dmesg' 查找正确的 USB 设备。

将固件加载到 FRDM 开发板后，按下 RESET 按钮。

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。
