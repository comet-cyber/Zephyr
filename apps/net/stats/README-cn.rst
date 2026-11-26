.. zephyr:code-sample:: net-stats
   :name: 网络统计信息
   :relevant-api: net_stats

   在用户应用程序中查询并显示网络统计信息。

概述
********

本示例展示了如何在用户应用程序中查询（并显示）网络统计信息。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/stats` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

运行本示例应用程序的推荐方式是按照 :ref:`networking_with_host` 中的说明使用 QEMU 或 native_sim 开发板。

请按照以下步骤构建网络统计信息示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/stats
   :board: <board to use>
   :conf: prj.conf
   :goals: build
   :compact:

如果所有配置均正确无误，应用程序将定期向控制台打印当前的网络统计信息。

.. code-block:: console

    Global network statistics
    IPv6 recv      27	sent	8	drop	0	forwarded	0
    IPv6 ND recv   2	sent	5	drop	2
    IPv6 MLD recv  0	sent	3	drop	0
    IPv4 recv      20	sent	0	drop	20	forwarded	0
    IP vhlerr      0	hblener	0	lblener	0
    IP fragerr     0	chkerr	0	protoer	0
    ICMP recv      15	sent	3	drop	13
    ICMP typeer    0	chkerr	0
    UDP recv       0	sent	0	drop	30
    UDP chkerr     0
    TCP bytes recv 0	sent	0
    TCP seg recv   0	sent	0	drop	0
    TCP seg resent 0	chkerr	0	ackerr	0
    TCP seg rsterr 0	rst	0	re-xmit	0
    TCP conn drop  0	connrst	0
    Bytes received 7056
    Bytes sent     564
    Processing err 1
