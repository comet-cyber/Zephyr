.. zephyr:code-sample:: wifi-ap-sta-mode
   :name: Wi-Fi AP-STA 模式
   :relevant-api: wifi_mgmt dhcpv4_server

   将 Wi-Fi 开发板配置为同时作为接入点（AP）和站点（STA）运行。

概述
********

Wi-Fi 开发板的 Wi-Fi AP-STA 模式允许其同时作为接入点（Access Point，AP）和站点（Station，STA）工作。本示例演示如何配置和使用 AP-STA 模式。

本示例展示了以下接口模式的配置与使用方法：

1. ``AP mode`` ：配置并启用 AP 模式，同时配置 DHCPv4 服务器以为接入的 STA 分配 IP 地址。
2. ``STA mode`` ：提供路由器的 SSID 和 PSK。

在示例代码中，首先启用 AP 模式，随后启用 STA 模式。驱动程序会检查此前是否已启用 AP 模式；如果已启用，则将开发板切换至 AP-STA 模式以同时支持两种模式，并尝试连接到所提供的 SSID 和 PSK 指定的 AP。

环境要求
**************

本示例可在任何常见的 :zephyr:board:`esp32_devkitc` 开发板上直接运行，无需任何额外硬件。

若要启用或禁用 ``AP-STA`` 模式，请修改本示例 ``prj.conf`` 文件中的 :kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA_AP` 参数。

默认情况下，AP-STA 模式处于禁用状态。

构建、烧录与运行
******************************

.. zephyr-app-commands::
   :zephyr-app: samples/net/wifi/apsta_mode
   :board: esp32_devkitc/esp32/procpu
   :goals: build flash
   :compact:

示例输出
=================

.. code-block:: console

   *** Booting Zephyr OS build v3.7.0-rc3-104-gd1e5c5b3f9b7 ***
   [00:00:05.171,000] <inf> MAIN: Turning on AP Mode
   [00:00:05.172,000] <dbg> net_dhcpv4_server: net_dhcpv4_server_start: Started DHCPv4 server, address pool:
   [00:00:05.172,000] <dbg> net_dhcpv4_server: net_dhcpv4_server_start:     0: 192.168.4.11
   [00:00:05.172,000] <dbg> net_dhcpv4_server: net_dhcpv4_server_start:     1: 192.168.4.12
   [00:00:05.172,000] <dbg> net_dhcpv4_server: net_dhcpv4_server_start:     2: 192.168.4.13
   [00:00:05.172,000] <dbg> net_dhcpv4_server: net_dhcpv4_server_start:     3: 192.168.4.14
   [00:00:05.172,000] <inf> MAIN: DHCPv4 server started...

   [00:00:05.350,000] <inf> MAIN: AP Mode is enabled. Waiting for sta to connect ESP32-AP
   [00:00:05.350,000] <inf> MAIN: Connecting to SSID: ZIN-Dummy

   [00:00:09.498,000] <inf> net_dhcpv4: Received: 192.168.43.44
   [00:00:09.499,000] <inf> MAIN: Connected to ZIN-Dummy
   [00:00:32.739,000] <inf> MAIN: station: 7C:50:79:17:89:19 joined
   [00:00:32.832,000] <dbg> net_dhcpv4_server: dhcpv4_handle_discover: DHCPv4 processing Discover - reserved 192.168.4.11
   [00:00:33.839,000] <dbg> net_dhcpv4_server: dhcpv4_handle_request: DHCPv4 processing Request - allocated 192.168.4.11
