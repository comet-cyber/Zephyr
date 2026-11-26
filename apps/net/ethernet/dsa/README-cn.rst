.. zephyr:code-sample:: dsa
   :name: DSA（分布式交换机架构）
   :relevant-api: dsa_core

   测试与调试分布式交换机架构（DSA）

概述
********

本示例演示如何测试与调试分布式交换机架构（Distributed Switch Architecture，DSA）。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/ethernet/dsa` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

按照以下步骤构建 DSA 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/dsa
   :board: <board to use>
   :conf: prj.conf
   :goals: build
   :compact:
