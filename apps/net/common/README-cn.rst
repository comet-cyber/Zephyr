.. _networking_samples_common:

概述
********

各类网络示例均可利用通用代码来启用诸如 VLAN 支持等通用功能。

该通用示例模块的源代码位于： :zephyr_file:`samples/net/common` 。

VLAN
****

如果要为网络示例应用程序启用 VLAN 支持，请在编译示例应用程序时添加 :file:`overlay-vlan.conf` ，例如以下针对 echo-server 示例应用程序的命令：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :conf: "prj.conf overlay-vlan.conf"
   :goals: run
   :compact:

宿主机端的 VLAN 配置可按如下方式完成：

.. code-block:: console

    $ cd tools/net-setup
    $ ./net-setup.sh -c zeth-vlan.conf

该示例配置将创建如下网络结构：

* 在宿主机端：

  * 创建普通的 ``zeth`` 接口，其地址为 ``192.0.2.2/24`` 。所有发往 Zephyr 的网络流量都将经过该接口。

  * VLAN 接口 ``vlan.100`` 用于承载 VLAN tag 100 的网络流量，具有 IPv4 地址 ``198.51.100.2`` 和 IPv6 地址 ``2001:db8:100::2`` 。

  * VLAN 接口 ``vlan.200`` 用于承载 VLAN tag 200 的网络流量，具有 IPv4 地址 ``203.0.113.2`` 和 IPv6 地址 ``2001:db8:200::2`` 。

* Zephyr 端的网络接口与地址：

  * ``eth0`` 是主接口，其地址为 ``192.0.2.1/24`` ，用于与宿主机建立连接。

  * ``VLAN-100`` 是用于 VLAN tag 100 流量的虚拟接口，具有 IPv4 地址 ``198.51.100.1/24`` 和 IPv6 地址 ``2001:db8:100::1/64`` 。

  * ``VLAN-200`` 是用于 VLAN tag 200 流量的虚拟接口，具有 IPv4 地址 ``203.0.113.1/24`` 和 IPv6 地址 ``2001:db8:200::1/64`` 。

.. warning::

   本示例中使用的 IPv4 和 IPv6 地址不得用于任何实际生产网络，仅适用于这些网络示例。
   这些 IPv4 和 IPv6 地址仅供文档说明使用，不可在公网路由。
