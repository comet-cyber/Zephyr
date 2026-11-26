.. zephyr:code-sample:: openthread-coprocessor
   :name: OpenThread 协处理器
   :relevant-api: openthread

   使用 OpenThread 的协处理器架构构建 Thread Border Router。

概述
********

OpenThread 协处理器（Co-Processor）可用于构建 Thread 边界路由器（Thread Border Router）。本示例中的代码仅包含完整 Thread Border Router 的目标 MCU 部分。协处理器支持两种工作模式：网络协处理器（Network Co-Processor，NCP）和射频协处理器（Radio Co-Processor，RCP），详情请参阅 https://openthread.io/platforms/co-processor 。

构建 Thread Border Router 所需的其他宿主机端工具（例如 otbr-agent）可参考以下指南获取： https://openthread.io/guides/border-router/build#set-up-the-border-router 。

目前 OpenThread 推荐首选的协处理器配置为 RCP 模式。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/openthread/coprocessor` 。

构建与运行
********************

按如下方式构建 OpenThread NCP 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coprocessor
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

构建使用 CDC ACM UART 设备的 OpenThread NCP 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coprocessor
   :board: nrf52840dk/nrf52840
   :goals: build flash
   :gen-args: -DDTC_OVERLAY_FILE=usb.overlay -DEXTRA_CONF_FILE=overlay-usb-nrf-br.conf
   :compact:

针对 nrf52840dk/nrf52840 构建 RCP 模式的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/openthread/coprocessor
   :board: nrf52840dk/nrf52840
   :goals: build flash
   :gen-args: -DEXTRA_CONF_FILE=overlay-rcp.conf
   :compact:

在 coprocessor 目录下提供了适用于不同开发板和配置方案的配置文件：

:file:`prj.conf`
   通用 NCP 配置文件。如果需要 NCP 配置，请使用此文件。

:file:`overlay-rcp.conf`
   RCP overlay 配置文件。如果需要 RCP 配置，请将此文件与 prj.conf 配合使用。

:file:`overlay-tri-n4m-br.conf`
   专用于特定 Thread Border Router 硬件（ https://www.tridonic.com/com/en/download/data_sheets/net4more_Borderrouter_PoE-Thread_en.pdf ）的 overlay 配置文件。
   该硬件的板级支持未包含在 Zephyr 仓库中，但该产品基于 NXP K64 和 AT86RF233 设计。此文件可作为基于开发板搭建开发环境时的配置参考示例。
