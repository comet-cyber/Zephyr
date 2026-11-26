.. zephyr:code-sample:: net-capture
   :name: 网络数据包捕获
   :relevant-api: net_capture

   捕获网络数据包并通过 IPIP 隧道将其发送到远程主机。

概述
********

本应用程序将对设备进行配置，以便通过 net-shell 启用网络数据包捕获功能。

捕获到的数据包会通过 IPIP 隧道发送到远程主机。该隧道既可以配置在与被捕获数据包相同的连接上，也可以使用独立的承载链路（Bearer）。例如，如果你正在捕获接口 1 的网络流量，那么当设备连接了多个网络接口时，接收捕获数据包的远程主机既可以通过接口 1 访问，也可以通过其他网络接口访问。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

按如下方式构建本示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/capture
   :board: <board to use>
   :goals: build
   :compact:

针对 :zephyr:board:`native_sim` 构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/capture
   :board: native_sim
   :gen-args: -DEXTRA_CONF_FILE=overlay-tunnel.conf
   :goals: build
   :compact:

网络配置
*********************

``net-tools`` 项目包含可用于配置隧道的 ``net-setup.sh`` 脚本。

在终端 #1 中输入：

.. code-block:: console

   ./net-setup.sh -c zeth-tunnel.conf

该脚本将创建以下网络接口：

.. code-block:: console

   zeth: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.0.2.2  netmask 255.255.255.255  broadcast 0.0.0.0
        inet6 2001:db8::2  prefixlen 128  scopeid 0x0<global>
        ether 00:00:5e:00:53:ff  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   zeth-ip6ip: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1480
        inet6 2001:db8:200::2  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::c000:202  prefixlen 64  scopeid 0x20<link>
        sit  txqueuelen 1000  (IPv6-in-IPv4)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   zeth-ip6ip6: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1452
        inet6 fe80::486c:eeff:fead:5d11  prefixlen 64  scopeid 0x20<link>
        inet6 2001:db8:100::2  prefixlen 64  scopeid 0x0<global>
        unspec 20-01-0D-B8-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 8  dropped 8 overruns 0  carrier 8  collisions 0

   zeth-ipip: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1480
        inet 198.51.100.2  netmask 255.255.255.0  destination 198.51.100.2
        inet6 fe80::5efe:c000:202  prefixlen 64  scopeid 0x20<link>
        tunnel   txqueuelen 1000  (IPIP Tunnel)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 7  dropped 0 overruns 0  carrier 0  collisions 0

   zeth-ipip6: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1452
        inet 203.0.113.2  netmask 255.255.255.0  destination 203.0.113.2
        inet6 fe80::387b:a6ff:fe56:6cac  prefixlen 64  scopeid 0x20<link>
        unspec 20-01-0D-B8-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 7  dropped 7 overruns 0  carrier 0  collisions 0

``zeth`` 是外层隧道接口，所有数据包均经由该接口传输。其他接口则会根据你在 Zephyr 侧的配置接收相应的数据包。

网络捕获配置
=============================

在 Zephyr 控制台中输入：

.. code-block:: console

   uart:~$ net iface

   Interface 0x807df74 (Virtual) [1]
   =================================
   Interface is down.

   Interface 0x807e040 (Ethernet) [2]
   ==================================
   Link addr : 02:00:5E:00:53:3B
   MTU       : 1452
   Flags     : AUTO_START,IPv4,IPv6
   Ethernet capabilities supported:
   IPv6 unicast addresses (max 4):
        fe80::5eff:fe00:533b autoconf preferred infinite
        2001:db8::1 manual preferred infinite
   IPv6 multicast addresses (max 4):
        ff02::1
        ff02::1:ff00:533b
        ff02::1:ff00:1
   IPv6 prefixes (max 2):
        <none>
   IPv6 hop limit           : 64
   IPv6 base reachable time : 30000
   IPv6 reachable time      : 43300
   IPv6 retransmit timer    : 0
   IPv4 unicast addresses (max 2):
        192.0.2.1 manual preferred infinite
   IPv4 multicast addresses (max 1):
        <none>
   IPv4 gateway : 0.0.0.0
   IPv4 netmask : 255.255.255.0

接下来配置监控功能，使捕获到的数据包作为 IPv6/UDP 数据包的 Payload 发送。

.. code-block:: console

   uart:~$ net capture setup 192.0.2.2 2001:db8:200::1 2001:db8:200::2
   Capture setup done, next enable it by "net capture enable <idx>"

``net capture`` 命令将显示当前配置。由于尚未启用捕获功能，此时尚未设置捕获接口。

.. code-block:: console

   uart:~$ net capture
   Network packet capture disabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    -        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

接下来为接口 2 启用网络数据包捕获功能。

.. code-block:: console

   uart:~$ net capture enable 2

此时隧道接口将处于 UP 状态，捕获到的数据包将被发送到对端主机。

.. code-block:: console

   uart:~$ net iface 1

   Interface 0x807df74 (Virtual) [1]
   =================================
   Name      : IPv4 tunnel
   Attached  : 2 (Ethernet / 0x807e040)
   Link addr : 8E:F9:94:6D:B9:E6
   MTU       : 1452
   Flags     : POINTOPOINT,NO_AUTO_START,IPv6
   IPv6 unicast addresses (max 4):
        fe80::aee6:fbff:fe50:28c0 autoconf preferred infinite
        2001:db8:200::1 manual preferred infinite
   IPv6 multicast addresses (max 4):
        <none>
   IPv6 prefixes (max 2):
        <none>
   IPv6 hop limit           : 64
   IPv6 base reachable time : 30000
   IPv6 reachable time      : 22624
   IPv6 retransmit timer    : 0
   IPv4 not enabled for this interface.

如果现在执行以下命令：

.. code-block:: console

   uart:~$ net ping -c 1 192.0.2.2

你应该会看到一条发送到 ``192.0.2.2`` 的 ICMPv4 报文，同时捕获到的数据包也会通过发往 ``192.0.2.2`` 的隧道被发送到 ``2001:db8:200::2`` 地址。UDP 端口默认为 ``4242`` ，但可以在设置隧道端点地址时进行更改。

在隧道末端实际接收到的捕获网络数据包如下所示：

.. code-block:: console

   No.     Time           Source                Destination           Protocol Length Info
        34 106.078538049  192.0.2.1             192.0.2.2             ICMP     94     Echo (ping) request  id=0xdc36, seq=0/0, ttl=64 (reply in 35)

   Frame 34: 94 bytes on wire (752 bits), 94 bytes captured (752 bits) on interface zeth-ip6ip, id 0
   Raw packet data
   Internet Protocol Version 6, Src: 2001:db8:200::1, Dst: 2001:db8:200::2
   User Datagram Protocol, Src Port: 4242, Dst Port: 4242
   Ethernet II, Src: 02:00:5e:00:53:3b (02:00:5e:00:53:3b), Dst: ICANNIAN_00:53:ff (00:00:5e:00:53:ff)
   Internet Protocol Version 4, Src: 192.0.2.1, Dst: 192.0.2.2
   Internet Control Message Protocol

   No.     Time           Source                Destination           Protocol Length Info
        35 106.098850599  192.0.2.2             192.0.2.1             ICMP     94     Echo (ping) reply    id=0xdc36, seq=0/0, ttl=64 (request in 34)

   Frame 35: 94 bytes on wire (752 bits), 94 bytes captured (752 bits) on interface zeth-ip6ip, id 0
   Raw packet data
   Internet Protocol Version 6, Src: 2001:db8:200::1, Dst: 2001:db8:200::2
   User Datagram Protocol, Src Port: 4242, Dst Port: 4242
   Ethernet II, Src: ICANNIAN_00:53:ff (00:00:5e:00:53:ff), Dst: 02:00:5e:00:53:3b (02:00:5e:00:53:3b)
   Internet Protocol Version 4, Src: 192.0.2.2, Dst: 192.0.2.1
   Internet Control Message Protocol
