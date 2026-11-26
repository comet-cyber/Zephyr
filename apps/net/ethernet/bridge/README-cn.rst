.. zephyr:code-sample:: bridge
   :name: 以太网网桥
   :relevant-api: ethernet net_if

   测试与调试以太网网桥

概述
********

用于测试和调试以太网网桥（Ethernet Bridge）的示例。

本示例应用程序的源代码位于 :zephyr_file:`samples/net/ethernet/bridge` 目录。

构建与运行
********************

请按照以下步骤构建网桥示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/bridge
   :board: <board to use>
   :conf: prj.conf
   :goals: build
   :compact:

在没有硬件开发板的情况下，可以使用 native_sim 应用程序快速验证网桥功能。
:zephyr_file:`samples/net/ethernet/bridge/bridge-test-setup.sh` 提供了用于主机端配置的脚本。
具体步骤如下：

1. 运行脚本执行前置配置（pre-setup）。这会创建两个 TAP 接口 zeth0 和 zeth1。

.. code-block:: console

    bridge-test-setup.sh pre-setup

2. 运行 native_sim 应用程序。

3. 运行脚本执行后置配置（post-setup）。zeth1 会被移至另一个网络命名空间（network namespace）。（我们无法在运行 native_sim 应用程序之前完成此项后置配置，因为 Zephyr 网络接口似乎无法连接到位于网络命名空间中的接口。）

.. code-block:: console

    bridge-test-setup.sh post-setup

4. 测试 zeth0 与 zeth1 之间的桥接功能。IP 地址配置如下所示，请对位于另一个网络命名空间中的 zeth1 执行 ping 测试：

   - zeth0: IPv4 192.0.2.2, IPv6 2001:db8::2
   - zeth1: IPv4 192.0.2.3, IPv6 2001:db8::3

.. code-block:: console

    ping 192.0.2.3
    ping 2001:db8::3

5. 测试完成后清理环境。

.. code-block:: console

    bridge-test-setup.sh clean
