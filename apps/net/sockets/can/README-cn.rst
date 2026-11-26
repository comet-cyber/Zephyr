.. zephyr:code-sample:: socket-can
   :name: SocketCAN
   :relevant-api: bsd_sockets socket_can

   使用 BSD Socket API 发送和接收原始 CAN 帧。

概述
********

SocketCAN 示例是一个使用 BSD Socket API 发送和接收原始 CAN 帧的服务器/客户端应用程序。

本应用程序包含以下功能函数：

* 初始化函数：创建一个 CAN Socket，将其绑定到 CAN 网络接口，然后为该 Socket 安装 CAN 过滤器，以便应用程序接收 CAN 帧。
* 接收函数：开始监听 CAN Socket 并打印有关 CAN 帧的信息。
* 发送函数：开始向总线发送原始 CAN 帧。

此示例应用程序的源代码位于： :zephyr_file:`samples/net/sockets/can` 。

环境要求
************

你需要一块支持 CAN 总线（CANBUS）的开发板，例如 :zephyr:board:`nucleo_l432kc` 或 :zephyr:board:`stm32f072b_disco` 。

构建与运行
********************

按照如下方式构建 SocketCAN 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/can
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

针对 nucleo_l432kc 的构建示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/can
   :host-os: unix
   :board: nucleo_l432kc
   :goals: run
   :compact:
