.. zephyr:code-sample:: wpan-serial
   :name: IEEE 802.15.4 "serial-radio"
   :relevant-api: ieee802154 uart_interface

   为基于 Contiki 的 Border Router 实现 slip-radio 设备。

概述
********

``wpan_serial`` 示例展示了如何将具备 IEEE 802.15.4 射频与 USB 控制器的硬件用作基于 Contiki 的 Border Router（边界路由器）的 "serial-radio"（串口射频）设备。

环境要求
**************

本示例要求开发板支持 IEEE 802.15.4 射频与 USB 控制器。例如，你可以通过 overlay 选用 CC2520 或 RF2xx 等收发器，或者直接使用内置射频的 SoC（如 kw41z、nrf5 或 samr21）。

构建与运行
********************

#. 在构建和运行本示例之前，请确保已禁用 Linux 系统的 ModemManager，否则它可能会干扰串口通信：

   .. code-block:: console

     $ sudo systemctl disable ModemManager.service

#. 针对具备 IEEE 802.15.4 射频和 USB 控制器的开发板构建该 Zephyr 示例应用程序。 ``samples/net/wpan_serial`` 目录下提供了适用于多种硬件组合的配置文件：

   - :file:`prj.conf`
     这是标准的默认配置文件，可直接用于原生支持 IEEE 802.15.4 的硬件。

   构建 ``wpan_serial`` 示例的方法如下：

   .. zephyr-app-commands::
     :zephyr-app: samples/net/wpan_serial
     :board: <board name>
     :conf: "prj.conf [overlay-<RADIO>.conf]"
     :goals: build
     :compact:

   以下是针对 Atmel SAM R21 Xplained Pro 开发套件构建并烧录本示例的方法：

   .. zephyr-app-commands::
     :zephyr-app: samples/net/wpan_serial
     :board: samr21_xpro
     :goals: build flash
     :compact:

#. 将开发板连接到 Linux PC，系统中应出现 ``/dev/ttyACM[number]`` 设备节点。
#. 运行基于 Contiki 的原生 Border Router（如 6lbr、native-router 等）。
   Contiki 运行示例：

   .. code-block:: console

     $ cd examples/ipv6/native-border-router
     $ make
     $ sudo ./border-router.native -v5 -s ttyACM0 fd01::1/64

现在你就拥有了一个 Contiki 原生 Border Router。你可以使用浏览器访问 ``border-router`` 输出中打印的服务器地址，打开其基于 Web 的管理界面。

.. code-block:: console

  ...
  Server IPv6 addresses:
   0x62c5c0: =>fd01::212:4b00:531f:113a
  ...

使用浏览器访问 ``http://[fd01::212:4b00:531f:113a]/`` ，即可查看可用的邻居节点与路由信息。
