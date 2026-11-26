.. zephyr:code-sample:: sntp-client
   :name: SNTP 客户端
   :relevant-api: bsd_sockets sntp

   使用 SNTP 从宿主机获取当前时间。

概述
********

本示例是一个简单的 SNTP 客户端，演示如何获取自 1970 年 1 月 1 日以来经过的秒数（即当前时间）。

本演示假设所选平台具备网络支持，可能需要对配置做适当调整；同时假设宿主机上正在运行 SNTP 服务器。

构建与运行
********************

应用程序运行时，会向宿主机发送 SNTP 请求并等待响应。收到响应后，程序将打印当前的纪元时间（Epoch time，以秒为单位）以及响应状态码（成功时为 0）。

更多详情请参阅 `net-tools`_ 项目。

本示例可按照 :ref:`networking_with_qemu` 中的说明在 QEMU 或 native_sim 开发板上构建并运行。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

Wi-Fi
=====

在本示例中，可以通过 :ref:`Wi-Fi snippet <snippet-wifi-ipv4>` 启用 IPv4 Wi-Fi 支持。
