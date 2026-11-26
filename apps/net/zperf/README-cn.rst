.. zephyr:code-sample:: zperf
   :name: zperf：网络流量生成器 (Network Traffic Generator)
   :relevant-api: net_config

   使用 zperf Shell 工具评估网络带宽。

功能说明
**************

``zperf`` 示例演示了如何使用 :ref:`zperf Shell 工具 <zperf>` 来评估网络带宽。

特性
*********

- 兼容 iPerf v2.0.10 及更高版本。如需兼容更早版本，请启用 :kconfig:option:`CONFIG_NET_ZPERF_LEGACY_HEADER_COMPAT` 。

- 使用 ``overlay-iperf3.conf`` 构建时改为兼容 iperf3（该配置会启用 :kconfig:option:`CONFIG_NET_ZPERF_IPERF3` ）。

- 无需修改源代码即可使用客户端模式或服务器模式。

支持的开发板
********************

zperf 本身与具体板卡无关。不过，要运行 zperf 示例应用程序，目标平台必须提供受 Zephyr 支持的网络接口。

本示例应用程序已在以下平台上完成测试：

- Freedom Board (FRDM K64F)
- QEMU x86
- Arm FVP BaseR AEMv8-R
- ARM BASE RevC AEMv8A Fixed Virtual Platforms

为了获得最佳性能，本示例配置了大量的网络数据包（packet）和缓冲区（buffer）。因此，本示例对 RAM 的需求较大。如果目标平台的 RAM 无法容纳本示例，请调小以下配置项：

.. code-block:: cfg

   CONFIG_NET_PKT_RX_COUNT=40
   CONFIG_NET_PKT_TX_COUNT=40
   CONFIG_NET_BUF_RX_COUNT=160
   CONFIG_NET_BUF_TX_COUNT=160

环境要求
**************

- 主机上已安装 iPerf 2.0.10 或更高版本；若使用 ``overlay-iperf3.conf`` 构建，则需安装 iperf3
- 受支持的开发板

根据所选网络技术的不同，可能还需要执行额外步骤来配置网络环境。

使用方法
**************

有关该库的使用详情，请参阅 :ref:`zperf 库文档 <zperf>` 。

iperf3
======

若要配合 iperf3（而非 iperf2）进行带宽测量，请附带 iperf3 overlay 进行构建。zperf 命令保持不变，默认端口将变为 5201：

.. zephyr-app-commands::
   :zephyr-app: samples/net/zperf
   :board: <board>
   :gen-args: -DEXTRA_CONF_FILE=overlay-iperf3.conf
   :goals: build flash

构建并运行后，设备端的 ``zperf tcp download`` 和 ``zperf udp download`` 可响应主机端发起的 ``iperf3 -c <device address>`` ，而 ``zperf tcp upload <host address>`` 则可针对主机端的 ``iperf3 -s`` 运行上传测试。

确定性吞吐量回归测试
============================================

如需采用一种与硬件无关、不受主机运行速度影响的方式来检测网络吞吐量性能回退（在 ``qemu_x86`` 上结合 QEMU icount 模式通过客户机内部 Loopback 接口测试），请参阅 :ref:`zperf-loopback-icount` 。

Wi-Fi
=====

在本示例中，可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 启用 IPv4 Wi-Fi 支持。
