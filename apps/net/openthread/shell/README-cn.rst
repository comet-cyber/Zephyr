.. zephyr:code-sample:: openthread-shell
   :name: OpenThread Shell
   :relevant-api: net_stats

   使用 OpenThread Shell 测试 Thread 协议与 IEEE 802.15.4。

概述
********

本示例支持通过 OpenThread Shell 测试各类开发板的 Thread 协议及底层 IEEE 802.15.4 驱动。

构建与运行
********************

请确认你所使用的目标开发板及芯片支持 IEEE 802.15.4。

在 shell 目录下针对不同开发板和配置场景提供了多个配置文件：

- :file:`prj.conf`
  通用配置文件。

- :file:`overlay-ot-rcp-host-nxp.conf`
  该 overlay 配置用于启用通过 IMU 接口在 NXP 芯片上运行的 OpenThread RCP 主机支持。

按如下方式构建 Shell 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/shell
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

为 Nordic nRF52840 DK 构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/shell
   :board: nrf52840dk/nrf52840
   :conf: "prj.conf"
   :goals: build
   :compact:

为 NXP RW612 FRDM（RCP 主机）构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/shell
   :board: frdm_rw612
   :gen-args: -DEXTRA_CONF_FILE="prj-ot-host.conf"
   :goals: build
   :compact:

为 NXP MCXW72 FRDM（主机）构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/shell
   :board: frdm_mcxw72/mcxw727c
   :gen-args: -DEXTRA_CONF_FILE="prj-ot-host.conf"
   :goals: build
   :compact:

为采用厂商特定无线射频实现的 NXP MCXW72 FRDM（主机）构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/shell
   :board: frdm_mcxw72/mcxw727c
   :gen-args: -DEXTRA_CONF_FILE="prj-ot-host.conf;prj-ot-host-no-l2-nxp-mcxw.conf"
   :goals: build
   :compact:

为 Silicon Labs EFR32MG24 4187c 射频板构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/shell
   :board: xg24_rb4187c
   :conf: "prj.conf"
   :goals: build
   :compact:


控制台交互示例
==========================

.. code-block:: console

   uart:~$ ot scan
   | PAN  | MAC Address      | Ch | dBm | LQI |
   +------+------------------+----+-----+-----+
   | fe09 | abcdef1234567890 | 15 | -78 |  60 |
   Done
