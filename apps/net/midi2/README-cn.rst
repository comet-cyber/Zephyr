.. zephyr:code-sample:: netmidi2
   :name: MIDI2 网络传输
   :relevant-api: midi_ump net_midi2

   通过 Network MIDI 2.0 协议交换通用 MIDI 数据包（UMP）。

概述
********

本示例演示了 Network MIDI 2.0 协议栈的用法：

* 启动一个可在网络上访问的 UMP Endpoint 主机
* 响应 UMP Stream 发现消息，以便客户端能够发现 Devicetree 中描述的拓扑结构
* 如果在 Devicetree 中定义了 ``midi_serial`` 端口，则将来自 UMP 组 9 的 MIDI1 数据发送到该端口
* 如果在 Devicetree 中定义了 ``midi_green_led`` 节点，则在串口发送数据时点亮该 LED（ :kconfig:option:`CONFIG_NET_SAMPLE_MIDI2_ACTIVITY_LED` ）

环境要求
************

本示例需要一块支持 IP 网络的开发板。若要对运行中的示例执行有意义的操作，还需要一个 Network MIDI 2.0 客户端来连接目标设备，例如 `pymidi2`_ 。

构建与运行
********************

在没有任何硬件的情况下体验本示例最简单的方法是使用 ``native_sim`` 。请参阅 :ref:`native_sim 以太网驱动 <nsim_per_ethe>` 在计算机上相应地配置网络。

.. zephyr-app-commands::
   :zephyr-app: samples/net/midi2/
   :board: native_sim
   :goals: run

此时应该可以在网络上访问该 Network MIDI 2.0 端点：

.. code-block:: console

  $ pymidi2 find
  Zephyr-UDP-MIDI2 (udp://192.0.2.1:45486)
  - Block #0 [io : Recv/Send] 'Synthesizer' UMP groups {0, 1, 2, 3} [MIDI1 + MIDI2]
  - Block #1 [i- : Recv     ] 'Keyboard' UMP groups {8} [MIDI1 only]
  - Block #2 [-o :      Send] 'External output (MIDI DIN-5)' UMP groups {9} [MIDI1 31.25kb/s]


此外，本示例非常适合搭配 :ref:`olimex_shield_midi` 使用，该扩展板已方便地定义了外部 MIDI OUT 及其 LED 的 Devicetree 节点。例如，在 ST Nucleo F429zi 上使用该扩展板：

.. zephyr-app-commands::
   :zephyr-app: samples/net/midi2
   :board: nucleo_f429zi
   :shield: olimex_shield_midi
   :goals: build flash

使用身份认证
********************

若要启用共享密钥（Shared Secret）身份认证以连接到 UMP Endpoint 主机，请启用 :kconfig:option:`CONFIG_NET_SAMPLE_MIDI2_AUTH_SHARED_SECRET` ，然后在 :kconfig:option:`CONFIG_NET_SAMPLE_MIDI2_SHARED_SECRET` 中配置所需的共享密钥。

若要改用用户名/密码身份认证，请启用 :kconfig:option:`CONFIG_NET_SAMPLE_MIDI2_AUTH_USER_PASSWORD` ，然后在 :kconfig:option:`CONFIG_NET_SAMPLE_MIDI2_USERNAME` 和 :kconfig:option:`CONFIG_NET_SAMPLE_MIDI2_PASSWORD` 中配置所需的用户名和密码。

.. _pymidi2:
   https://github.com/titouanc/pymidi2
