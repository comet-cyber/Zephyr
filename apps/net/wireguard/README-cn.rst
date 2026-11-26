.. zephyr:code-sample:: wireguard-vpn
   :name: WireGuard VPN
   :relevant-api: bsd_sockets

   实现一个通过 WireGuard VPN 连接将收到的数据包回传给发送方的 echo-server 应用程序。

WireGuard VPN
*************

可按如下方式针对 ``native_sim`` 目标板编译并运行 WireGuard VPN 演示应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/wireguard
   :board: native_sim
   :conf: <config file to use>
   :goals: build
   :compact:

对于 Linux GNOME 桌面环境，在命令行编译时添加 ``-DCONFIG_NATIVE_UART_AUTOATTACH_DEFAULT_CMD="\"gnome-terminal -- screen %s\""`` 会非常实用。

可按如下方式完成主机端的 WireGuard VPN 配置：

.. code-block:: console

    $ cd tools/net-setup
    $ ./net-setup.sh -c wireguard-vpn.conf

该示例配置将创建如下网络拓扑配置：

* 主机端：

  * 创建常规的 ``zeth`` 接口，其地址为 ``192.0.2.2/24`` 。所有发往 Zephyr 的网络流量都将经过此接口。

  * VPN 接口 ``zwg0`` 是 WireGuard 隧道端点，拥有 ``198.51.100.2`` IPv4 地址和 ``2001:db8:100::2`` IPv6 地址。所有 VPN 流量都将经过此接口。

* Zephyr 端的网络接口与地址（使用 ``native_sim`` 开发板时）：

  * ``eth0`` 是主接口，拥有 ``192.0.2.1/24`` 地址，并与主机相连。

  * ``wg0`` 是虚拟接口。应用程序应当通过该接口发送数据，以便让网络流量通过 WireGuard VPN 隧道传输。它拥有 ``198.51.100.1/24`` IPv4 地址和 ``2001:db8:100::1/64`` IPv6 地址。

  * ``wg_ctrl`` 是 VPN 控制接口。所有 VPN 虚拟接口均挂载到该接口上，它本身没有 IP 地址。

主机端网络接口示例：

.. code-block:: console

  zeth: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.0.2.2  netmask 255.255.255.0  broadcast 0.0.0.0
        inet6 2001:db8::2  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::200:5eff:fe00:53ff  prefixlen 64  scopeid 0x20<link>
        ether 00:00:5e:00:53:ff  txqueuelen 1000  (Ethernet)
        RX packets 16  bytes 2356 (2.3 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 27  bytes 2688 (2.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

  zwg0: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1420
        inet 198.51.100.2  netmask 255.255.255.255  destination 198.51.100.1
        inet6 2001:db8:100::2  prefixlen 128  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 3  bytes 364 (364.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4  bytes 452 (452.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

主机端设置的路由如下：

.. code-block:: console

  192.0.2.0/24 dev zeth proto kernel scope link src 192.0.2.2 linkdown
  198.51.100.1 dev zwg0 proto kernel scope link src 198.51.100.2
  2001:db8::/64 dev zeth proto kernel metric 256 linkdown pref medium
  2001:db8::/64 dev zeth metric 1024 linkdown pref medium
  2001:db8:100::2 dev zwg0 proto kernel metric 256 pref medium
  2001:db8:100::/64 dev zwg0 metric 1024 pref medium

本示例会自动完成 Zephyr 网络配置，但也可以手动进行 WireGuard 配置。

若要手动配置，需要先清空以下 Kconfig 选项：

.. code-block:: console

  CONFIG_NET_SAMPLE_COMMON_VPN_PEER_IP_ADDR=""
  CONFIG_NET_SAMPLE_COMMON_VPN_MY_ADDR=""
  CONFIG_NET_SAMPLE_COMMON_VPN_ALLOWED_PEER_ADDR=""
  CONFIG_NET_SAMPLE_COMMON_VPN_MY_PRIVATE_KEY=""
  CONFIG_NET_SAMPLE_COMMON_VPN_PEER_PUBLIC_KEY=""

执行以下命令以手动配置本示例：

.. code-block:: console

  # Add IPv4 and IPv6 address to the VPN interface
  net ipv4 add 2 198.51.100.1 255.255.255.0
  net ipv6 add 2 2001:db8:100::1

  # Setup our private key
  net wg setup -k lmAIbJR8PQOpgJxmfOydBiDbexTMEKsjglZ1sj3kIjs= -i 2

  # Setup peers
  net wg add -k v/xiHtIDhnnMJV3SbqI+cChcSqfrU4zlhLUUbL1J8x4= -a 2001:db8:100::/64,198.51.100.0/24 -e 192.0.2.2:51820

如果 Zephyr 主机配置正确，VPN 接口 2 应当会自动启动，并且能够连接到对端（Peer）。

.. warning::
   本演示中使用的 IPv4 和 IPv6 地址不得用于任何生产网络，仅适用于这些网络示例。这些 IPv4 和 IPv6 地址仅供文档演示使用，不可路由。切勿在任何真实网络设备中使用示例 WireGuard VPN 配置文件里的私钥；在实际需要时，务必重新生成新的私钥。有关如何生成密钥，请参阅 `WireGuard 快速入门 <https://www.wireguard.com/quickstart/>`_ 。
