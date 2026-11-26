.. zephyr:code-sample:: mqtt-sn-publisher
   :name: MQTT-SN 发布者
   :relevant-api: mqtt_sn_socket

   向 MQTT-SN 网关发送 MQTT-SN PUBLISH 消息。

概述
********

`MQTT <http://mqtt.org/>`_ （MQ Telemetry Transport，消息队列遥测传输）是一种针对小型传感器和移动设备优化的轻量级发布/订阅消息传递协议。

MQTT-SN 可以看作是针对无线通信环境特点进行适配的 MQTT 版本。MQTT 需要可靠的 TCP/IP 传输，而 MQTT-SN 则设计为可在任何基于数据报的传输层上使用，例如 UDP、ZigBee 甚至是普通的 UART（配合额外的成帧协议）。

Zephyr MQTT-SN Publisher 示例应用程序是一个 MQTT-SN v1.2 客户端，用于向 MQTT-SN 网关发送 MQTT-SN PUBLISH 消息，同时也会 SUBSCRIBE（订阅）一个主题。
更多信息请参阅 `MQTT-SN v1.2 spec`_ 。

.. _MQTT-SN v1.2 spec: https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/mqtt_sn_publisher` 。

环境要求
************

- Linux 主机
- MQTT-SN 网关，例如 Eclipse Paho
- Mosquitto 服务器：支持 MQTT v3.1.1 的任意版本。本示例使用 mosquitto 1.6 测试通过。
- Mosquitto 订阅客户端
- 测试用局域网（以太网）

构建与运行
*****************

本示例应用程序同时支持静态 IP 地址和网关发现（Gateway Discovery）流程。
打开 :zephyr_file:`samples/net/mqtt_sn_publisher/prj.conf` 文件，并根据局域网环境设置 IP 地址。可使用 CONFIG_NET_SAMPLE_MQTT_SN_STATIC_GATEWAY 选择静态 IP 或网关发现流程。

你还需要启动一个 MQTT-SN 网关。 :zephyr_file:`samples/net/mqtt_sn_publisher/compose/compose.yaml` 中提供了一个便捷的 Docker Compose 配置文件。
首先，通过以下命令启动来自 `此处 <https://github.com/zephyrproject-rtos/net-tools>`_ 的 net-tools 配置：

.. code-block:: console

	$ ./net-setup.sh --config docker.conf

随后在另一个终端窗口中通过以下命令启动 Docker 环境：

.. code-block:: console

	$ cd ./compose
	$ docker compose up

你也可以手动搭建此环境。对于 Paho，既可以从源码构建（参见 `PAHO MQTT-SN Gateway`_ ），也可以运行非官方 Docker 镜像，例如 `kyberpunk/paho`_ 。

.. _PAHO MQTT-SN Gateway: https://www.eclipse.org/paho/index.php?page=components/mqtt-sn-transparent-gateway/index.php
.. _kyberpunk/paho: https://hub.docker.com/r/kyberpunk/paho

在 Linux 主机上打开 3 个终端窗口。首先启动 mosquitto：

.. code-block:: console

	$ sudo mosquitto -v -p 1883

接着，在另一个窗口中启动网关，例如使用 Docker：

.. code-block:: console

	$ docker run -it -p 10000:10000 -p 10000:10000/udp --name paho -v $PWD/gateway.conf:/etc/paho/gateway.conf:ro kyberpunk/paho

然后进入你的 Zephyr 目录并执行：

.. zephyr-app-commands::
   :zephyr-app: samples/net/mqtt_sn_publisher
   :board: native_sim/native/64
   :goals: run
   :compact:

可选地，你也可以使用任意 MQTT 客户端工具连接到你的 Broker。

Wi-Fi
=====

可通过 :ref:`Wi-Fi snippet <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。

示例输出
=============

以下是应用程序的输出：

.. code-block:: console

	WARNING: Using a test - not safe - entropy source
	*** Booting Zephyr OS build zephyr-v3.2.0-279-gc7fa387cea81  ***
	[00:00:00.000,000] <inf> net_config: Initializing network
	[00:00:00.000,000] <inf> net_config: IPv4 address: 172.18.0.20
	[00:00:00.000,000] <inf> mqtt_sn_publisher_sample: MQTT-SN sample
	[00:00:00.000,000] <inf> mqtt_sn_publisher_sample: Network connected
	[00:00:00.000,000] <inf> mqtt_sn_publisher_sample: Waiting for connection...
	[00:00:00.000,000] <inf> mqtt_sn_publisher_sample: Connecting client
	[00:00:00.510,000] <inf> net_mqtt_sn: Decoding message type: 5
	[00:00:00.510,000] <inf> net_mqtt_sn: Got message of type 5
	[00:00:00.510,000] <inf> net_mqtt_sn: MQTT_SN client connected
	[00:00:00.510,000] <inf> mqtt_sn_publisher_sample: MQTT-SN event EVT_CONNECTED
	[00:00:01.020,000] <inf> net_mqtt_sn: Decoding message type: 19
	[00:00:01.020,000] <inf> net_mqtt_sn: Got message of type 19
	[00:00:10.200,000] <inf> mqtt_sn_publisher_sample: Publishing timestamp
	[00:00:10.200,000] <inf> net_mqtt_sn: Registering topic
										2f 75 70 74 69 6d 65                             |/uptime
	[00:00:10.200,000] <inf> net_mqtt_sn: Can't publish; topic is not ready
	[00:00:10.710,000] <inf> net_mqtt_sn: Decoding message type: 11
	[00:00:10.710,000] <inf> net_mqtt_sn: Got message of type 11
	[00:00:10.710,000] <inf> net_mqtt_sn: Publishing to topic ID 14
	[00:00:20.400,000] <inf> mqtt_sn_publisher_sample: Publishing timestamp
	[00:00:20.400,000] <inf> net_mqtt_sn: Publishing to topic ID 14

以下是 MQTT-SN 网关的输出：

.. code-block:: console

	20221024 140210.191   CONNECT           <---  ZEPHYR                              0C 04 04 01 00 3C 5A 45 50 48 59 52
	20221024 140210.192   CONNECT           ===>  ZEPHYR                              10 12 00 04 4D 51 54 54 04 02 00 3C 00 06 5A 45 50 48 59 52
	20221024 140210.192   CONNACK           <===  ZEPHYR                              20 02 00 00
	20221024 140210.192   CONNACK           --->  ZEPHYR                              03 05 00

	20221024 140210.643   SUBSCRIBE   0001  <---  ZEPHYR                              0C 12 00 00 01 2F 6E 75 6D 62 65 72
	20221024 140210.648   SUBSCRIBE   0001  ===>  ZEPHYR                              82 0C 00 01 00 07 2F 6E 75 6D 62 65 72 00
	20221024 140210.660   SUBACK      0001  <===  ZEPHYR                              90 03 00 01 00
	20221024 140210.661   SUBACK      0001  --->  ZEPHYR                              08 13 00 00 0D 00 01 00

	20221024 140220.338   REGISTER    0002  <---  ZEPHYR                              0D 0A 00 00 00 02 2F 75 70 74 69 6D 65
	20221024 140220.348   REGACK      0002  --->  ZEPHYR                              07 0B 00 0E 00 02 00

	20221024 140220.848   PUBLISH           <---  ZEPHYR                              0C 0C 00 00 0E 00 00 31 30 32 30 30
	20221024 140220.850   PUBLISH           ===>  ZEPHYR                              30 0E 00 07 2F 75 70 74 69 6D 65 31 30 32 30 30

	20221024 140230.539   PUBLISH           <---  ZEPHYR                              0C 0C 00 00 0E 00 00 32 30 34 30 30
	20221024 140230.542   PUBLISH           ===>  ZEPHYR                              30 0E 00 07 2F 75 70 74 69 6D 65 32 30 34 30 30
