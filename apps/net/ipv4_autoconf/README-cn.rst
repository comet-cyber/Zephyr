.. zephyr:code-sample:: ipv4-autoconf
   :name: IPv4 自动配置客户端
   :relevant-api: networking net_if net_context net_mgmt

   执行 IPv4 自动配置并自行分配一个随机 IPv4 地址

概述
********

本示例应用程序会启动 IPv4 自动配置（autoconf），在 169.254.0.0/16 范围内自行分配一个随机 IPv4 地址，并维护该 IPv4 地址，在多方尝试分配相同地址时解决 IPv4 地址冲突。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

以下说明介绍如何在 :zephyr:board:`frdm_k64f` 开发板上运行此示例应用程序，以配置链路本地（Link-Local）IPv4 地址并连接到 Linux 主机。

使用以太网网线将 :zephyr:board:`Freedom-K64F 开发板 <frdm_k64f>` 连接到 Linux 主机，并检查新增的网络接口。

在 Linux 主机上运行 Avahi 客户端
====================================

在 Linux 系统中为网络接口分配一个 IPv4 链路本地地址：

.. code-block:: console

   $ avahi-autoipd --force-bind -D eth0


FRDM_K64F
=========

按照以下步骤构建 Zephyr ``samples/net/ipv4_autoconf`` 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ipv4_autoconf
   :host-os: unix
   :board: frdm_k64f
   :goals: build flash
   :compact:

当 IPv4 LL（链路本地）完成探测和通告后，将显示如下详细信息：

.. code-block:: console

   $ sudo screen /dev/ttyACM0 115200

.. code-block:: console

   [ipv4ll] [INF] main: Run ipv4 autoconf client
   [ipv4ll] [INF] handler: Your address: 169.254.218.128

请注意，每次自行分配时 IP 地址可能会发生变化。

若要验证 Zephyr 应用程序正在运行且已配置 IP 地址，请输入：

.. code-block:: console

   $ ping -I eth1 169.254.218.128

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 代码片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。
