.. zephyr:code-sample:: wifi-shell
   :name: Wi-Fi Shell
   :relevant-api: net_stats

   使用 Wi-Fi Shell 模块测试 Wi-Fi 功能。

概述
********

本示例通过启用提供扫描（scan）、连接（connect）和断开连接（disconnect）等命令的 Wi-Fi Shell 模块，用于测试各类开发板的 Wi-Fi 驱动程序；同时还启用了 net_shell 模块以验证 net_if 设置。

构建与运行
********************

请确认你所选用的目标开发板和芯片提供 Wi-Fi 支持。

例如，你可以通过选择 nrf7002dk/nrf5340/cpuapp 开发板目标来使用 Nordic 的 nrf7002dk。

若要在无真实硬件的情况下运行，可以结合源码树内置的 wifi_hwsim 驱动针对 native_sim 进行构建（包含两个虚拟射频：一个 AP，一个 STA）。在第一个接口上启动 AP，然后从第二个接口进行扫描并连接：

.. zephyr-app-commands::
   :zephyr-app: samples/net/wifi/shell
   :board: native_sim
   :goals: build
   :compact:

.. zephyr-app-commands::
   :zephyr-app: samples/net/wifi/shell
   :board: nrf7002dk/nrf5340/cpuapp
   :goals: build
   :compact:

控制台交互示例
==========================

如需了解每个 Shell 命令的详细说明，可以在 Shell 中运行 ``wifi --help`` 。

在本 Shell 示例中，我们将扫描可用的接入点（AP）并连接其中之一。
``--key-mgmt`` 用于指定安全类型，其中 0 表示开放网络（Open），1 表示 WPA/WPA2 Personal。

更多信息可通过运行 ``wifi connect --help`` 获取。

.. code-block:: console

   shell> wifi scan
   Scan requested
   shell>
   Num  | SSID                             (len) | Chan | RSSI | Sec
   1    | kapoueh!                         8     | 1    | -93  | WPA/WPA2
   2    | mooooooh                         8     | 6    | -89  | WPA/WPA2
   3    | Ap-foo blob..                    13    | 11   | -73  | WPA/WPA2
   4    | gksu                             4     | 1    | -26  | WPA/WPA2
   ----------
   Scan request done

   shell> wifi connect --ssid "gksu" --key-mgmt 1 --passphrase SecretStuff
   Connection requested
   shell>
   Connected
   shell>
