.. zephyr:code-sample:: vlan
   :name: 虚拟局域网 (VLAN)
   :relevant-api: vlan_api net_l2 net_if

   设置两个虚拟局域网（VLAN）并使用 net-shell 查看网络配置。

概述
********

Zephyr 的 VLAN 示例应用程序将设置两个虚拟局域网（Virtual LAN）。该示例启用了 net-shell，允许用户查看 VLAN 配置。

此示例应用程序的源代码位于： :zephyr_file:`samples/net/ethernet/vlan` 。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

运行此 VLAN 应用程序的一种便捷方式是按照 :ref:`networking_with_eth_qemu` 中的说明使用 QEMU。在 Linux 中运行 :file:`net-setup.sh` 脚本时，可以像下面这样使用 :file:`zeth-vlan.conf` 配置文件：

.. code-block:: console

    ./net-setup.sh -c zeth-vlan.conf

请注意，VLAN 仅支持具有以太网端口或支持 USB 网络的开发板。

按照以下步骤构建 VLAN 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/vlan
   :board: <board to use>
   :conf: prj.conf
   :goals: build
   :compact:

默认配置文件 :zephyr_file:`samples/net/ethernet/vlan/prj.conf` 会创建两个具有以下配置的虚拟局域网：

- VLAN tag 100：IPv4 198.51.100.1 和 IPv6 2001:db8:100::1
- VLAN tag 200：IPv4 203.0.113.1 和 IPv6 2001:db8:200::1

配置 Linux 主机
=====================

:zephyr_file:`samples/net/ethernet/vlan/vlan-setup-linux.sh` 提供了一个可在 Linux 主机上执行的脚本。它会在 Linux 主机上创建两个 VLAN 接口 ``vlan.100`` 和 ``vlan.200`` ，并创建通往 Zephyr 的路由。

如果一切配置正确，你将能够在 Linux 主机上成功执行以下命令。

.. code-block:: console

    ping -c 1 2001:db8:100::1
    ping -c 1 198.51.100.1
    ping -c 1 2001:db8:200::1
    ping -c 1 203.0.113.1

发往 ``2001:db8:100::1`` 或 ``198.51.100.1`` 的网络数据包将带有 VLAN tag 100。发往 ``2001:db8:200::1`` 或 ``203.0.113.1`` 的网络数据包将带有 VLAN tag 200。
