.. zephyr:code-sample:: t1s
   :name: 10BASE-T1S 测试 (OA_TC6)

   设置测试以检验 10BASE-T1S 通信的长期稳定性


10BASE-T1S 网络 (OA_TC6) 测试
#####################################

概述
********

本测试设置用于检验 T1S 通信能否保持长期稳定运行。

前置条件
*************

硬件前置条件：
========================

* 安装了 Debian 11.9（v.6.1 内核）的 `Raspberry PI4 <rpi4-spec_>`_ 以及配置为 10 BASE T1S 主站（HOST）的 `LAN8670-USB 适配器 <evb-lan8670_>`_
* 连接到一个或多个 `来自 microe.com 的 LAN8651 "micro BUS" 模块 <microe-lan8651_>`_ 的 Nucleo（ :zephyr:board:`nucleo_g474re` ）开发板（作为被测设备 DUT）

.. note::

    lan867x-linux-driver-2v2/linux-v6.1.21-support 的 IPv6 功能在 PC 端的 Debian 12 上无法正常工作。因此，建议迁移到 RPI4 上进行测试。

连接与 IO
===================

+--------------------------------+----------------------+
| :zephyr:board:`nucleo_g474re`  | `microe-lan8651`_    |
+================================+======================+
| 3V3 (CN 6)                     | 3V3                  |
+--------------------------------+----------------------+
| GND (CN 6)                     | GND                  |
+--------------------------------+----------------------+
| SCK/D13 (CN 5)                 | SCK                  |
+--------------------------------+----------------------+
| MISO/D12 (CN 5)                | SDO                  |
+--------------------------------+----------------------+
| PWM/MOSI/D11 (CN 5)            | SDI                  |
+--------------------------------+----------------------+
| PWM/CS/D10 (CN 5)              | CS                   |
+--------------------------------+----------------------+
| D8 (CN 5)                      | RST                  |
+--------------------------------+----------------------+
| D7 (CN 9)                      | IRQ                  |
+--------------------------------+----------------------+


软件前置条件：
========================

* 编译 `udp-perf`_ 程序（同时针对 HOST 和 DUT）

* 应将 `udp-perf Zephyr 源码 <udp-perf-zephyr_>`_ 克隆到： ``modules/udp-perf/zephyr``

* 扩展 ``west.yml`` ：

.. code-block:: shell

   - name: udp-perf
     path: modules/udp-perf

* 在 :code:`echo_server` 或 :code:`zperf` 的配置文件中启用配置项 :code:`UDPPERF`

* 扩展 ``boards/nucleo_g474re.conf`` 以按实际环境配置 IP 地址：

.. code-block:: shell

  CONFIG_NET_CONFIG_MY_IPV4_ADDR="192.0.2.1"
  CONFIG_NET_CONFIG_PEER_IPV4_ADDR="192.0.2.3"
  CONFIG_NET_CONFIG_MY_IPV6_ADDR="2001:db8::1"
  CONFIG_NET_CONFIG_PEER_IPV6_ADDR="2001:db8::3"


测试与验证：
***********************

结合 `udp-perf`_ 的 :zephyr:code-sample:`sockets-echo-server`:
====================================================================

* 针对 :zephyr:board:`nucleo_g474re` 开发板进行构建

.. code-block:: shell

   west build -p always -b nucleo_g474re samples/net/sockets/echo_server/

默认配置：

.. code-block:: console

   Nucleo ip:  192.0.2.1      RPI4: 192.0.2.3
   Nucleo ipv6 2001:db8::1      RPI4: 2001:db8::3


* 使用 RPI4 连接 USB <-> T1S 适配器（连接到 USB 2.0 端口）：

.. code-block:: shell

   uname -a # Linux raspberrypi 6.1.21
   cd ~/work/Zephyr/lan867x-linux-driver-2v2/linux-v6.1.21-support
   ./load.sh

添加通往 Nucleo 的默认路由（在 RPI4 上）：

.. code-block:: shell

   ip -6 route add 2001:db8::1 dev eth0

* 运行测试程序（在 RPI4 上）——通过 SSH 登录以便为每个 ``while`` 循环打开独立的控制台：

.. code-block:: shell

   cd ~/work/Zephyr/net-tools $
   while :; do ./echo-client -r -i eth1 192.0.2.1; sleep 1; ping -c 3 192.0.2.1; done
   while :; do ./echo-client -r -i eth1 2001:db8::1; sleep 1; ping -6 -c 3 2001:db8::1; done
   cd ~/work/Zephyr/udp-perf $
   while :; do ./target/armv7-unknown-linux-gnueabihf/release/udp-perf client --ip 192.0.2.1 --packets 100 --mode reduced --runs 5; [ $? -ne 0 ] && echo "Error!"; done


:zephyr:code-sample:`zperf`:
============================

* 针对 :zephyr:board:`nucleo_g474re` 开发板进行构建

.. code-block:: shell

   west build -p always -b nucleo_g474re samples/net/zperf/

* Zephyr 模块（Nucleo 开发板）作为客户端（CLIENT）

.. code-block:: shell

   zperf udp upload 192.0.2.3 5001 10 1460 10M # -> nucleo shell
   iperf -s -l 1460 -u -B 192.0.2.3 -i 1 # -> RPI4

* Zephyr 模块（Nucleo 开发板）作为服务器（SERVER）

.. code-block:: shell

   zperf udp download 5001 # -> nucleo shell
   iperf -l 1460 -u -c 192.0.2.1 -i 1 -b 10M -p 5001 # -> RPI4


运行多个设备实例：
******************************

可以运行多个被测设备（DUT）实例：

* 在 ``nucleo_g474re.conf`` 中调整 IP 地址

* 在 ``boards/nucleo_g474re.overlay`` 中调整 :code:`local-mac-address` 和 :code:`plca-node-id` 属性。


.. _microe-lan8651:
   https://www.mikroe.com/two-wire-eth-click?srsltid=AfmBOoouUPjUzmLu19iA8wRez6GyJp5Mf_mMjckgRcvtqrBA9INjaKQe

.. _evb-lan8670:
   https://www.microchip.com/en-us/development-tool/ev08l38a

.. _rpi4-spec:
   https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/

.. _udp-perf:
   https://gitlab.com/network851614/udp-perf/-/tree/main/zephyr?ref_type=heads

.. _udp-perf-zephyr:
   https://gitlab.com/network851614/udp-perf/-/tree/main/zephyr?ref_type=heads
