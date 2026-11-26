.. zephyr:code-sample:: dhcpv6-pd
   :name: DHCPv6 前缀委派
   :relevant-api: dhcpv6 dhcpv6_server

   使用 DHCPv6（RFC 8415）获取并委派 IPv6 前缀。

概述
********

本示例演示了 :rfc:`8415` 中规定的 IPv6 前缀委派（Prefix Delegation）。它可以构建为以下两种角色：

* **请求路由器（Requesting router）** （默认）：DHCPv6 客户端在其上游（WAN）接口上请求一个 IPv6 地址（IA_NA）和一个委派前缀（IA_PD）。随后，每个下游（LAN）接口都会分配到一个从该委派前缀中划分出来的独立 ``/64`` 子网，并通过路由器通告（Router Advertisements）进行广播，以便下游链路上的主机能够自动配置地址（SLAAC）。

* **委派路由器 / 服务器（Delegating router / server）** （ ``overlay-server.conf`` ）：DHCPv6 服务器从 ``2001:db8:abcd::/64`` 分配地址，并从 ``2001:db8:beef::/48`` 中委派前缀，为每个客户端分配一个 ``/56`` 前缀。这两个地址池特意保持互不重叠：如果将客户端自身 WAN 地址所在的同一个子网委派给该客户端，它就会在其 LAN 上重新通告该子网，最终导致两条链路使用相同的前缀。

网络接口
******************

前缀委派至少需要两条链路，因此请求路由器（requesting-router）构建版本会启用两个网络接口。在 native_sim 开发板上，它们是两个 TAP 接口：

* ``zeth0`` -- 上游（WAN），运行 DHCPv6 客户端（接口索引 1），
* ``zeth1`` -- 下游（LAN），用于通告委派前缀（接口索引 2）。

下游链路的数量受 :kconfig:option:`CONFIG_NET_DHCPV6_MAX_DOWNSTREAM` 限制；若要委派给更多链路，请调高该选项的值（同时调高 :kconfig:option:`CONFIG_NET_IF_MAX_IPV6_COUNT` 以及 :file:`boards/native_sim.overlay` 中 ``zephyr,native-tap`` 接口的数量）。

服务器构建版本（ ``overlay-server.conf`` ）使用单个名为 ``zeth`` 的接口： :file:`overlay-server.overlay` 会禁用下游接口并将保留的接口重命名，从而使该构建版本绑定到 ``zeth`` 而非 ``zeth0`` 。

为了使 TAP 接口具备主机侧连通性，请在运行前使用 `net-tools <https://github.com/zephyrproject-rtos/net-tools>`_ 项目中的 ``net-setup.sh`` 脚本配置它们，例如将一个实例作为服务器运行，另一个实例作为请求路由器运行。详情请参阅 net-tools 中的 ``README-dhcpv6-pd.md`` 文件。

构建与运行
********************

请求路由器（客户端）：

.. code-block:: console

   west build -b native_sim samples/net/dhcpv6_pd
   west build -t run

委派路由器（服务器）：

.. code-block:: console

   west build -b native_sim samples/net/dhcpv6_pd -- \
       -DEXTRA_CONF_FILE=overlay-server.conf \
       -DEXTRA_DTC_OVERLAY_FILE=overlay-server.overlay
   west build -t run

环境要求
************

请求路由器的下游通告功能需要启用 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX` ，并且若要在 WAN 和 LAN 接口之间进行转发，还需要启用 :kconfig:option:`CONFIG_NET_IPV6_FORWARDING` 。
