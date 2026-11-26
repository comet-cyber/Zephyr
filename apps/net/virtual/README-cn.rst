.. zephyr:code-sample:: virtual-network-interface
   :name: 虚拟网络接口
   :relevant-api: virtual virtual_mgmt

   创建一个示例虚拟网络接口。

概述
********

本示例应用程序出于演示目的创建了一个示例虚拟网络接口，在此并不执行任何实际业务功能。
示例中共有 4 个网络接口。

以太网网络接口提供真实的物理网络接口，所有虚拟接口均运行在其之上。

在以太网接口之上运行着两个虚拟网络接口，其中一个仅提供 IPv6 隧道（tunnel），另一个仅提供 IPv4 隧道。这两个隧道均由 IPIP 隧道提供。

本示例还提供了一个运行在 IPv6 隧道之上的隧道接口。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/virtual` 。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

`net-tools`_ 项目提供了一份配置文件，可用于在宿主机侧创建示例隧道。

.. code-block:: console

	net-setup.sh -c zeth-tunnel.conf

请注意，本示例应用程序要求开发板提供以太网网络接口。按如下方式构建本示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/virtual
   :board: <board to use>
   :goals: build
   :compact:

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
