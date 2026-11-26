.. zephyr:code-sample:: sntp-server
   :name: SNTP 服务器
   :relevant-api: bsd_sockets sntp sntp_server

   向网络上的 SNTP 客户端提供当前时间服务。

概述
********

本示例是一个简单的 SNTP 服务器实现。

启动时，本示例会向 :kconfig:option:`CONFIG_NET_SAMPLE_SNTP_UPSTREAM_ADDRESS` 中配置的 SNTP 服务器发起查询，并根据响应设置系统时钟。随后，它会在所有已启用的地址族（address family）上监听默认 SNTP 端口（UDP 端口 123），向客户端提供时间服务。

上游服务器没有默认值，请根据你的网络环境进行设置，例如 ``pool.ntp.org`` 。如果未设置上游服务器，本示例仍会启动服务器，但该服务器会告知客户端其时钟未同步，不得使用所返回的时间戳。

你可以使用 ``ntpdig`` 或 ``sntp`` 等 SNTP 客户端向该服务器发起查询。

本演示假定所选平台具备网络支持，实际使用时可能需要对配置做适当调整。

构建与运行
********************

更多详情请参阅 `net-tools`_ 项目。

本示例可以按照 :ref:`networking_with_qemu` 中的说明，在 QEMU 或 native_sim 开发板上构建并执行。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。
