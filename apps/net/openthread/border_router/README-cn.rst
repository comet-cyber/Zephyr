.. zephyr:code-sample:: openthread-border-router
   :name: OpenThread BorderRouter
   :relevant-api:

   使用 OpenThread Border Router 测试 Wi-Fi 和 IEEE 802.15.4。

概述
********

本示例支持通过 OpenThread 和 Wi-Fi Shell 在多种开发板上测试 Thread 协议以及 Thread Border Router（边界路由器）功能。

构建与运行
********************

请确认目标开发板和芯片提供 IEEE 802.15.4 和 Wi-Fi 支持。

在 shell 目录下提供了适用于不同开发板和配置的配置文件：

- :file:`prj.conf`
  通用配置文件。

- :file:`overlay-ot-rcp-host-wifi-nxp.conf`
  该 overlay 配置启用了在 NXP 芯片上通过 IMU 接口运行 OpenThread RCP 主机（Host）的支持，同时也启用了 Wi-Fi 支持。

- :file:`overlay-webserver.conf`
  该 overlay 配置启用了 HTTP Web 服务器（REST API）。

按如下方式构建 OpenThread Border Router 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/border_router
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

针对 NXP RW612 FRDM（RCP 主机）的构建示例。

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/border_router
   :board: frdm_rw612
   :conf: "prj.conf overlay-ot-rcp-host-wifi-nxp.conf"
   :goals: build
   :compact:

针对 NXP RW612 FRDM（RCP 主机）并启用 Web 服务器的构建示例。

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/border_router
   :board: frdm_rw612
   :conf: "prj.conf overlay-ot-rcp-host-wifi-nxp.conf overlay-webserver.conf"
   :goals: build
   :compact:

Web 服务器
**************

使用 ``overlay-webserver.conf`` 构建时，应用程序会包含一个提供以下功能的 HTTP Web 服务器：

- **Web 界面** ：可通过 ``http://<device-ip>:8080`` 或 ``http://zephyr-otbr:8080`` （通过 mDNS）访问
- **REST API** ：用于 Thread 网络管理的基于 JSON 的接口端点
