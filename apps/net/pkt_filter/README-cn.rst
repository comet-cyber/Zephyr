.. zephyr:code-sample:: net-pkt-filter
   :name: 网络数据包过滤器
   :relevant-api: net_pkt_filter

   安装网络数据包过滤钩子（Hook）。

概述
********

本示例演示如何从用户应用程序设置网络数据包过滤器。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/pkt_filter` 。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

运行本示例应用程序的一种推荐方式是按照 :ref:`networking_with_host` 中的说明，使用 QEMU 或
native_sim 开发板。

出于演示目的，需要在宿主机端按如下方式启用 VLAN 支持。请在终端窗口中执行以下命令：

.. code-block:: console

   $ cd tools/net-tools
   $ ./net-setup.sh  -c zeth-vlan.conf

随后按照以下步骤为 ``qemu_x86`` 或 ``native_sim`` 开发板构建网络数据包过滤器示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/pkt_filter
   :board: <board to use>
   :conf: "prj.conf overlay-vlan.conf"
   :goals: build
   :compact:

在本示例中，我们通过以下设置启用 VLAN 支持：

VLAN overlay 配置文件 :zephyr_file:`samples/net/pkt_filter/overlay-vlan.conf`
使用以下参数创建两个虚拟局域网（VLAN）：

- VLAN tag 100：IPv4 198.51.100.1 与 IPv6 2001:db8:100::1
- VLAN tag 200：IPv4 203.0.113.1 与 IPv6 2001:db8:200::1

在网络 Shell 中，你可以监控网络数据包过滤器：

.. code-block:: console

   uart:~$ net filter
   Rule  Type        Verdict   Pkt-Prio  Queue  Thread-Prio  Tests
   [ 1]  recv        OK             N/A    N/A          N/A  3    iface[2],eth vlan type[0x0800],size max[200]
   [ 2]  recv        OK             N/A    N/A          N/A  3    iface[3],eth vlan type[0x0800],size min[100]
   [ 3]  recv        OK             N/A    N/A          N/A  1    iface[1]
   [ 4]  recv        OK             N/A    N/A          N/A  2    iface[2],eth vlan type[0x0806]
   [ 5]  recv        OK             N/A    N/A          N/A  2    iface[3],eth vlan type[0x0806]
   [ 6]  recv        DROP           N/A    N/A          N/A  0
   [ 7]  IPv4 recv   OK             N/A    N/A          N/A  1    ip src block[192.0.2.2,198.51.100.2]
   [ 8]  IPv6 recv   OK             N/A    N/A          N/A  1    ip src block[2001:db8::2,2001:db8::100:2]

上述示例应用程序的网络数据包过滤规则含义如下：

* 规则 1：允许最大长度为 200 字节的 IPv4（Ethernet 类型 0x0800）数据包进入网络接口 2（即第一个 VLAN 接口）。

* 规则 2：允许最小长度为 100 字节的 IPv4 数据包进入网络接口 3（即第二个 VLAN 接口）。

* 规则 3：允许所有入站流量进入以太网接口 1。

* 规则 4：允许 ARP 数据包（Ethernet 类型 0x0806）进入 VLAN 接口 2。

* 规则 5：允许 ARP 数据包（Ethernet 类型 0x0806）进入 VLAN 接口 3。

* 规则 6：丢弃所有其他数据包。这也意味着 IPv6 数据包会被丢弃。

* 规则 7：丢弃源地址为 ``192.0.2.2`` 或 ``198.51.100.2`` 的 IPv4 数据包。

* 规则 8：丢弃源地址为 ``2001:db8::2`` 或 ``2001:db8::100:2`` 的 IPv6 数据包。

如果启用了网络数据包优先级选项 :kconfig:option:`CONFIG_NET_SAMPLE_USE_PACKET_PRIORITIES` ，
该示例将安装用于设置优先级的额外规则。

   uart:~$ net filter
   Rule  Type        Verdict   Pkt-Prio  Queue  Thread-Prio  Tests
   [ 1]  recv        CONTINUE         1      0            1  1    iface[1]
   [ 2]  recv        CONTINUE         7      2         SKIP  2    iface[1],eth type[0x88f7]
   [ 3]  recv        CONTINUE         2      0            1  2    iface[1],eth type[0x8100]
   [ 4]  recv        CONTINUE         1      0            1  2    iface[2],eth vlan type[0x0806]
   [ 5]  recv        CONTINUE         1      0            1  2    iface[3],eth vlan type[0x0806]
   [ 6]  recv        OK             N/A    N/A          N/A  3    iface[2],eth vlan type[0x0800],size max[200]
   [ 7]  recv        OK             N/A    N/A          N/A  3    iface[3],eth vlan type[0x0800],size min[100]
   [ 8]  recv        OK             N/A    N/A          N/A  1    iface[1]
   [ 9]  recv        OK             N/A    N/A          N/A  2    iface[2],eth vlan type[0x0806]
   [10]  recv        OK             N/A    N/A          N/A  2    iface[3],eth vlan type[0x0806]
   [11]  recv        DROP           N/A    N/A          N/A  0
   [12]  IPv4 recv   OK             N/A    N/A          N/A  1    ip src block[192.0.2.2,198.51.100.2]
   [13]  IPv6 recv   OK             N/A    N/A          N/A  1    ip src block[2001:db8::2,2001:db8::100:2]

上述示例应用程序的网络数据包过滤规则含义如下：

* 规则 1 - 5：添加规则，为特定类型的数据包设置网络数据包优先级。

* 规则 6 - 13：与前一个规则列表中的规则相同。

可以通过网络统计信息查看数据包被丢弃的情况。使用 ``net stats`` 命令监控统计数据。

你可以在网络 Shell 中验证这些规则：

.. code-block:: console

   uart:~$ net ping 2001:db8:100::2 -c 2
   PING 2001:db8:100::2
   Ping timeout
   uart:~$ net stats 2
   Interface 0x8089c6c (Virtual) [2]
   ==================================
   IPv6 recv      0        sent    3       drop    0       forwarded       0
   IPv6 ND recv   0        sent    7       drop    1
   IPv6 MLD recv  0        sent    0       drop    0
   ICMP recv      0        sent    3       drop    0
   ...
   Filter drop rx 10       tx      0
   Bytes received 320
   Bytes sent     660
   Processing err 10

   uart:~$ net ping 198.51.100.2 -c 1
   PING 198.51.100.2
   28 bytes from 198.51.100.2 to 198.51.100.1: icmp_seq=1 ttl=64 time=100 ms

   uart:~$ net ping 198.51.100.2 -c 1 -s 201
   PING 198.51.100.2
   Ping timeout

   uart:~$ net ping 203.0.113.2 -c 1
   PING 203.0.113.2
   Ping timeout

   uart:~$ net ping 203.0.113.2 -c 1 -s 101
   PING 203.0.113.2
   125 bytes from 203.0.113.2 to 203.0.113.1: icmp_seq=1 ttl=64 time=20 ms
