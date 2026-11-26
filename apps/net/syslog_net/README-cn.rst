.. zephyr:code-sample:: syslog-net
   :name: 远程 Syslog (Remote syslog)
   :relevant-api: log_backend log_ctrl

   启用远程 Syslog 服务，将 Syslog 消息发送至远程服务器。

概述
********

本示例应用程序用于启用远程 Syslog 服务，按照 ``prj.conf`` 中的配置将 Syslog 消息发送到远程服务器。有关基于 UDP 的 Syslog 协议的更多详情，请参阅 :rfc:`5424` 和 :rfc:`5426` 。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/syslog_net` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

若要配置远程 IPv6 Syslog 服务器，请在 ``prj.conf`` 文件中设置以下变量：

.. code-block:: cfg

	CONFIG_LOG_BACKEND_NET=y
	CONFIG_LOG_BACKEND_NET_SERVER="[2001:db8::2]:514"

如果用户未显式指定，默认端口号为 514，默认协议为 UDP。服务器地址和端口支持以下语法格式：

.. code-block:: console

	192.0.2.1:514
	192.0.2.42
	[2001:db8::1]:514
	[2001:db8::2]
	2001:db::42

若要将协议更改为 TCP，请在服务器地址前加上 ``tcp://`` 前缀：

.. code-block:: console

   tcp://192.0.2.1:514
   tcp://192.0.2.42
   tcp://[2001:db8::1]:514


按如下方式构建 ``syslog_net`` 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/syslog_net
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

Wi-Fi
=====

在本示例中，可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 启用 IPv4 Wi-Fi 支持。
