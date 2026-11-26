.. zephyr:code-sample:: dhcpv4-client
   :name: DHCPv4 客户端
   :relevant-api: dhcpv4 net_mgmt

   启动 DHCPv4 客户端以从 DHCPv4 服务器获取 IPv4 地址。

概述
********

本应用程序会启动一个 DHCPv4 客户端，从 DHCPv4 服务器获取 IPv4 地址，并将地址、租期（lease time）、子网掩码和路由器信息打印到串口控制台。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

在 Linux 主机上运行 DHCPv4 客户端
========================================

以下说明介绍如何在 Linux 主机上使用 QEMU 运行此示例应用程序，以与运行在 Linux 主机上的 DHCPv4 服务器（kea）协商 IP 地址。

若要使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。

以下是用于配置 DHCPv4 服务器的示例服务器配置文件 '/etc/kea/kea-dhcp4.conf'：

.. code-block:: console

    {
        "Dhcp4": {
            "interfaces-config": {
                "interfaces": [ "tap0" ],
                "dhcp-socket-type": "raw"
            },

            "valid-lifetime": 7200,

            "subnet4": [
                {
                    "id": 1,
                    "subnet": "192.0.2.0/24",
                    "pools": [ { "pool": "192.0.2.10 - 192.0.2.100" } ],
                    "option-data": [
                        {
                            "name": "routers",
                            "data": "192.0.2.2"
                        },
                        {
                            "name": "domain-name-servers",
                            "data": "8.8.8.8"
                        }
                    ]
                }
            ]
        }
    }

打开另一个终端窗口，使用此配置文件在 Linux 主机上启动 DHCPv4 服务器：

.. code-block:: console

    $ sudo kea-dhcp4 -c /etc/kea/kea-dhcp4.conf

在 QEMU 中运行 Zephyr samples/net/dhcpv4_client 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/dhcpv4_client
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

当 DHCPv4 客户端与服务器完成地址协商后，将显示如下详细信息：

.. code-block:: console

    [00:00:00.000,000] <inf> net_dhcpv4_client_sample: Run dhcpv4 client
    [00:00:00.000,000] <inf> net_dhcpv4_client_sample: Start on slip: index=1
    [00:00:07.080,000] <inf> net_dhcpv4: Received: 192.0.2.10
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample:    Address[1]: 192.0.2.10
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample:     Subnet[1]: 255.255.255.0
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample:     Router[1]: 192.0.2.2
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample: Lease time[1]: 7200 seconds

若要验证 Zephyr 应用程序客户端正在运行且已收到 IP 地址，请输入：

.. code-block:: console

    $ ping -I tap0 192.0.2.10


FRDM_K64F
=========

以下说明介绍如何在 :zephyr:board:`frdm_k64f` 开发板上运行此示例应用程序，以与运行在 Linux 主机上的 DHCPv4 服务器（kea）协商 IP 地址。

使用以太网网线将 :zephyr:board:`Freedom-K64F 开发板 <frdm_k64f>` 连接到 Linux 主机，并检查新增的网络接口：

.. code-block:: console

    $ ifconfig

为接口添加 IP 地址和路由信息：

.. code-block:: console

    $ sudo ip addr add 192.0.2.2 dev eth1
    $ sudo ip route add 192.0.2.0/24 dev eth1

以下是用于配置 DHCPv4 服务器的示例服务器配置文件 '/etc/kea/kea-dhcp4.conf'：

.. code-block:: console

    {
        "Dhcp4": {
            "interfaces-config": {
                "interfaces": [ "eth1" ],
                "dhcp-socket-type": "raw"
            },

            "valid-lifetime": 7200,

            "subnet4": [
                {
                    "id": 1,
                    "subnet": "192.0.2.0/24",
                    "pools": [ { "pool": "192.0.2.10 - 192.0.2.100" } ],
                    "option-data": [
                        {
                            "name": "routers",
                            "data": "192.0.2.2"
                        },
                        {
                            "name": "domain-name-servers",
                            "data": "8.8.8.8"
                        }
                    ]
                }
            ]
        }
    }

打开另一个终端窗口，使用此配置文件在 Linux 主机上启动 DHCPv4 服务器：

.. code-block:: console

    $ sudo kea-dhcp4 -c /etc/kea/kea-dhcp4.conf

构建 Zephyr samples/net/dhcpv4_client 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/dhcpv4_client
   :host-os: unix
   :board: frdm_k64f
   :goals: build flash
   :compact:

当 DHCPv4 客户端与服务器完成地址协商后，将显示如下详细信息：

.. code-block:: console

    $ sudo screen /dev/ttyACM0 115200
    [00:00:00.000,000] <inf> net_dhcpv4_client_sample: Run dhcpv4 client
    [00:00:00.000,000] <inf> net_dhcpv4_client_sample: Start on ethernet: index=1
    [00:00:07.080,000] <inf> net_dhcpv4: Received: 192.0.2.10
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample:    Address[1]: 192.0.2.10
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample:     Subnet[1]: 255.255.255.0
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample:     Router[1]: 192.0.2.2
    [00:00:07.080,000] <inf> net_dhcpv4_client_sample: Lease time[1]: 7200 seconds

若要验证 Zephyr 应用程序客户端正在运行且已收到 IP 地址，请输入：

.. code-block:: console

    $ ping -I eth1 192.0.2.10


Arm FVP
========

* :zephyr:board:`fvp_baser_aemv8r`
* :zephyr:board:`fvp_base_revc_2xaem`

运行在 Arm FVP 开发板上的此示例应用程序可以与运行在 Arm FVP 上的 DHCPv4 服务器协商 IP 地址，因此无需进行额外配置，可直接构建并运行。

构建 Zephyr samples/net/dhcpv4_client 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/dhcpv4_client
   :host-os: unix
   :board: fvp_baser_aemv8r
   :goals: build run
   :compact:

当 DHCPv4 客户端与服务器完成地址协商后，将显示如下详细信息：

.. code-block:: console

    uart:~$
    [00:00:00.060,000] <inf> phy_mii: PHY (0) ID 16F840

    [00:00:00.170,000] <inf> phy_mii: PHY (0) Link speed 10 Mb, half duplex

    [00:00:00.170,000] <inf> eth_smsc91x: MAC 00:02:f7:ef:37:16
    *** Booting Zephyr OS build zephyr-v3.2.0-4300-g3e6505dba29e ***
    [00:00:00.170,000] <inf> net_dhcpv4_client_sample: Run dhcpv4 client
    [00:00:00.180,000] <inf> net_dhcpv4_client_sample: Start on ethernet@9a000000: index=1
    [00:00:07.180,000] <inf> net_dhcpv4: Received: 172.20.51.1
    [00:00:07.180,000] <inf> net_dhcpv4_client_sample:    Address[1]: 172.20.51.1
    [00:00:07.180,000] <inf> net_dhcpv4_client_sample:     Subnet[1]: 255.255.255.0
    [00:00:07.180,000] <inf> net_dhcpv4_client_sample:     Router[1]: 172.20.51.254
    [00:00:07.180,000] <inf> net_dhcpv4_client_sample: Lease time[1]: 86400 seconds
