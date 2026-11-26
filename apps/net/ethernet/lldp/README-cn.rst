.. zephyr:code-sample:: lldp
   :name: 链路层发现协议 (LLDP)
   :relevant-api: lldp net_l2

   启用 LLDP 支持并设置 VLAN。

概述
********

适用于 Zephyr 的链路层发现协议（Link Layer Discovery Protocol，LLDP）示例应用程序将启用 LLDP 支持，并在需要时设置 VLAN。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/ethernet/lldp` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

运行此 LLDP 示例应用程序的一种便捷方式是在 QEMU 中运行（如 :ref:`networking_with_qemu` 所述），或者在 FRDM-K64F 等嵌入式设备上运行。请注意，仅带有以太网端口的开发板支持 LLDP。

按照以下步骤构建 LLDP 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/lldp
   :board: <board to use>
   :conf: prj.conf
   :goals: build
   :compact:

设置 Linux 主机
=====================

如果你的网络需要 VLAN 支持， :zephyr_file:`samples/net/ethernet/vlan/vlan-setup-linux.sh` 提供了一个可在 Linux 主机上执行的脚本。它会在 Linux 主机上创建两个 VLAN，并建立通往 Zephyr 的路由。
