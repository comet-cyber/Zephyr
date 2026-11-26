.. zephyr:code-sample:: tsn-switch
   :name: TSN 交换机
   :relevant-api: eth_bridge ptp_clock_interface ethernet_mgmt

   测试与调试 TSN 交换机

概述
********

关于测试与调试 TSN 交换机的示例。

在 Zephyr 中，交换机设备通过 DSA（Distributed Switch Architecture，分布式交换架构）驱动提供支持。
基于 DSA 用户端口的以太网网桥（Ethernet bridge）将用作交换机配置的方式，例如 FDB、VLAN 等（遗憾的是目前尚不支持这些功能）。

对于 TSN 协议，目前可以在 DSA 用户端口上启用 gPTP 协议栈，使交换机充当时间感知中继（Time-Aware Relay）。Qbv 可通过管理 API 进行管理。后续还将支持更多 TSN 协议，并可在本示例中启用。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/ethernet/tsn-switch` 。

环境要求
************

为了验证 TSN 交换机，至少需要两台支持 TSN（至少支持 gPTP）的 Linux 主机连接到该交换机。

构建与运行
********************

1. 构建并运行本示例。

.. zephyr-app-commands::
   :zephyr-app: samples/net/ethernet/tsn-switch
   :board: <board to use>
   :goals: build
   :compact:

2. 将 Linux 主机连接到 TSN 交换机。以 NXP i.MX943 EVK 为例。

.. code-block:: none

                         i.MX943 EVK
                     +-----------------+
                     |     bridge0     | gPTP bridge as Master
                     |  IP: 192.0.2.1  |    priority1 246
                     |                 |
                     | swp0(Qbv)  swp1 |
                     +--+----------+---+
                        |          |
                +-------+          +-------+
                |                          |
   +------------+-----------+  +-----------+------------+
   |          eth0          |  |          eth0          |
   | IP:  192.0.2.2         |  | IP:  192.0.2.3         |
   | MAC: fa:fa:62:fe:a2:11 |  | MAC: a6:10:52:1d:cb:6d |
   +------------------------+  +------------------------+
         Linux Host A                Linux Host B
    gPTP Slave priority1 248    gPTP slave priority1 248

在第一个 DSA 用户端口 swp0 上配置了用于演示的 Qbv。

.. code-block:: none

   time cycle 10ms   gate7 6 5 4 3 2 1 0
   -----------------------------------------
   slot 1 - 2ms:         1 1 1 1 0 1 0 1
   slot 2 - 8ms:         1 1 1 1 1 0 0 1

在 Linux 主机上配置好 IP 地址后，可以使用 ping 验证三台设备之间的基本通信。

3. 在 Linux 主机上运行 gPTP（使用带 gPTP.cfg 的 ptp4l），将时间基准同步到交换机。

.. code-block:: console

   # ptp4l -i eth0 -m -f gPTP-slave.cfg > /tmp/ptp.log &
   # tail -f /tmp/ptp.log
   ptp4l[186.753]: rms   25 max   51 freq  -8579 +/-  32 delay  1311 +/-   0
   ptp4l[187.752]: rms   19 max   39 freq  -8575 +/-  26 delay  1311 +/-   0
   ptp4l[188.752]: rms   30 max   59 freq  -8592 +/-  41 delay  1311 +/-   0
   ptp4l[189.752]: rms   17 max   28 freq  -8570 +/-  22 delay  1311 +/-   0
   ptp4l[190.752]: rms   23 max   37 freq  -8600 +/-  25 delay  1314 +/-   0
   ptp4l[191.752]: rms   24 max   42 freq  -8600 +/-  32 delay  1310 +/-   0
   ptp4l[192.752]: rms   30 max   54 freq  -8574 +/-  38 delay  1310 +/-   0
   ptp4l[193.753]: rms   25 max   35 freq  -8587 +/-  35 delay  1314 +/-   0
   ptp4l[194.752]: rms   27 max   48 freq  -8598 +/-  35 delay  1314 +/-   0
   ptp4l[195.752]: rms   26 max   42 freq  -8602 +/-  35 delay  1314 +/-   0
   ptp4l[196.752]: rms   25 max   42 freq  -8588 +/-  34 delay  1318 +/-   0

4. 在 Linux 主机 B 上使用 pktgen 向主机 A 发送数据包，以验证 Qbv 功能。

在 Linux 主机 B 上，每秒发送 VLAN 100 PCP 0 数据包。

.. code-block:: console

   # modprobe pktgen
   # cd /proc/net/pktgen
   # echo "add_device eth0"           > kpktgend_0
   # echo "count 0"                   > eth0
   # echo "clone_skb 0"               > eth0
   # echo "pkt_size 64"               > eth0
   # echo "dst_mac fa:fa:62:fe:a2:11" > eth0
   # echo "vlan_id 100"               > eth0
   # echo "vlan_p 0"                  > eth0
   # echo "delay 1000000000"          > eth0
   # echo "start" > pgctrl


在 Linux 主机 A 上捕获数据包。由于门控（gate）0 始终开启，因此可以接收到数据包。

.. code-block:: console

   # tcpdump -i eth0 -e vlan
   tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
   listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
   13:56:12.259668 a6:10:52:1d:cb:6d (oui Unknown) > fa:fa:62:fe:a2:11 (oui Unknown), ethertype 802.1Q (0x8100), length 64: vlan 100, p 0, ethertype IPv4, 169.254.153.102.9 > 0.0.0.0.9: UDP, length 18
   13:56:13.259696 a6:10:52:1d:cb:6d (oui Unknown) > fa:fa:62:fe:a2:11 (oui Unknown), ethertype 802.1Q (0x8100), length 64: vlan 100, p 0, ethertype IPv4, 169.254.153.102.9 > 0.0.0.0.9: UDP, length 18
   13:56:14.259714 a6:10:52:1d:cb:6d (oui Unknown) > fa:fa:62:fe:a2:11 (oui Unknown), ethertype 802.1Q (0x8100), length 64: vlan 100, p 0, ethertype IPv4, 169.254.153.102.9 > 0.0.0.0.9: UDP, length 18

在 Linux 主机 B 上，改为每秒发送 VLAN 100 PCP 1 数据包。

.. code-block:: console

   # echo "vlan_p 1" > eth0
   # echo "start" > pgctrl


在 Linux 主机 A 上捕获数据包。由于门控（gate）1 始终关闭，因此无法接收到任何数据包。

.. code-block:: console

   # tcpdump -i eth0 -e vlan
   tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
   listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes

5. 在 Linux 主机 B 上使用 pktgen 向主机 A 发送数据包，以验证 Qbv 性能。

在 Linux 主机 B 上，每 100us 发送一次 VLAN 100 PCP 2 数据包。

.. code-block:: console

   # modprobe pktgen
   # cd /proc/net/pktgen
   # echo "add_device eth0"           > kpktgend_0
   # echo "count 0"                   > eth0
   # echo "clone_skb 0"               > eth0
   # echo "pkt_size 64"               > eth0
   # echo "dst_mac fa:fa:62:fe:a2:11" > eth0
   # echo "vlan_id 100"               > eth0
   # echo "vlan_p 2"                  > eth0
   # echo "delay 100000"              > eth0
   # echo "start" > pgctrl


在 Linux 主机 A 上捕获 100000 个数据包，并检查它们是否落在 2ms 时间窗口内。
由于门控（gate）2 具有 2ms 时隙，因此仅在 2ms 窗口内才能接收到数据包。
结果显示，考虑到某些临界条件，99.98% 的数据包落在 2ms 窗口内。

.. code-block:: none

   # tcpdump -i eth0 -j adapter_unsynced --time-stamp-precision nano -tt -e vlan -c 100000 -w pcp2.pcap
   tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
   100000 packets captured
   101793 packets received by filter
   0 packets dropped by kernel
   #
   #
   # tcpdump -r pcp2.pcap --time-stamp-precision nano -tt -n 2>/dev/null | \
   awk '
   BEGIN{
     period=10000000; win=2000000; off=0;
     win_in=0; win_out=0; total=0;
   }
   $1 ~ /^[0-9]+\.[0-9]+$/ {
     split($1,a,"."); t=a[1]*1000000000 + (a[2]+0);
     phase = ((t - off) % period + period) % period;
     if (phase < win) win_in++; else win_out++;
     total++;
   }
   END{
     pct = (total ? (win_in*100.0/total) : 0);
     printf("period=10ms win=2ms off=%dns\n", off);
     printf("total=%d win_in=%d win_out=%d in_win=%.2f%%\n",
            total, win_in, win_out, pct);
   }'
   period=10ms win=2ms off=0ns
   total=100000 win_in=99977 win_out=23 in_win=99.98%

在 Linux 主机 B 上，改为每 100us 发送一次 VLAN 100 PCP 3 数据包。

.. code-block:: console

   # echo "vlan_p 3" > eth0
   # echo "start" > pgctrl


在 Linux 主机 A 上捕获 100000 个数据包，并检查它们是否落在 8ms 时间窗口内。
由于门控（gate）3 具有 8ms 时隙，因此仅在 8ms 窗口内才能接收到数据包。
结果显示，考虑到某些临界条件，99.98% 的数据包落在 8ms 窗口内。

.. code-block:: none

   # tcpdump -i eth0 -j adapter_unsynced --time-stamp-precision nano -tt -e vlan -c 100000 -w pcp3.pcap
   tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
   100000 packets captured
   101793 packets received by filter
   0 packets dropped by kernel
   #
   #
   # tcpdump -r pcp3.pcap --time-stamp-precision nano -tt -n 2>/dev/null | \
   awk '
   BEGIN{
     period=10000000; win=8000000; off=2000000;
     win_in=0; win_out=0; total=0;
   }
   $1 ~ /^[0-9]+\.[0-9]+$/ {
     split($1,a,"."); t=a[1]*1000000000 + (a[2]+0);
     phase = ((t - off) % period + period) % period;
     if (phase < win) win_in++; else win_out++;
     total++;
   }
   END{
     pct = (total ? (win_in*100.0/total) : 0);
     printf("period=10ms win=8ms off=%dns\n", off);
     printf("total=%d win_in=%d win_out=%d in_win=%.2f%%\n",
            total, win_in, win_out, pct);
   }'
   period=10ms win=8ms off=2000000ns
   total=100000 win_in=99976 win_out=24 in_win=99.98%
