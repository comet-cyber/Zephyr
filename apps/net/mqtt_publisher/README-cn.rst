.. zephyr:code-sample:: mqtt-publisher
   :name: MQTT 发布者
   :relevant-api: mqtt_socket

   向 MQTT 服务器发送 MQTT PUBLISH 消息。

概述
********

`MQTT <http://mqtt.org/>`_ （MQ Telemetry Transport，消息队列遥测传输）是一种针对小型传感器和移动设备优化的轻量级发布/订阅（publish/subscribe）消息传输协议。

Zephyr MQTT Publisher 示例应用程序是一个向 MQTT Broker 发送 MQTT PUBLISH 消息的 MQTT 客户端。本示例支持 v3.1.1（默认）和 v5.0 版本的 MQTT 客户端。

有关 MQTT v3.1.1 和 v5.0 的更多信息，请分别参阅 `MQTT v3.1.1 规范 <MQTT v3.1.1 spec_>`_ 和 `MQTT v5.0 规范 <MQTT v5.0 spec_>`_ 。

.. _MQTT v3.1.1 spec: https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html
.. _MQTT v5.0 spec: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/mqtt_publisher` 。

环境要求
**************

- Linux 主机
- Freedom 开发板（FRDM-K64F）
- Mosquitto 服务器：任何支持 MQTT v3.1.1 的版本。本示例已在 mosquitto 1.3.4 上完成测试。
- Mosquitto 订阅客户端（subscriber）
- 测试用局域网（LAN，以太网）

构建与运行
*****************

目前，本示例应用程序仅支持静态 IP 地址。请打开 :file:`src/config.h` 文件，并根据局域网环境设置 IP 地址。
或者，也可以在 :file:`prj.conf` 文件中设置 IP 地址。

:file:`src/config.h` 文件中还包含一些可供修改的配置项：

MQTT Broker 的 TCP 端口：

.. code-block:: c

	#define SERVER_PORT		1883

应用程序休眠时间：

.. code-block:: c

	#define APP_SLEEP_MSECS		500

最大连接尝试次数：

.. code-block:: c

	#define APP_CONNECT_TRIES	10

MQTT 客户端标识符（Client Identifier）：

.. code-block:: c

	#define MQTT_CLIENTID		"zephyr_publisher"

本示例应用程序支持 IBM Bluemix Watson 主题（Topic）格式，可通过将 APP_BLUEMIX_TOPIC 的默认值从 0 修改为 1 来启用：

.. code-block:: c

	#define APP_BLUEMIX_TOPIC	1

Bluemix 主题可包含设备类型、设备标识符、事件类型和消息格式等参数。本应用程序使用以下宏来指定这些值：

.. code-block:: c

	#define BLUEMIX_DEVTYPE		"sensor"
	#define BLUEMIX_DEVID		"carbon"
	#define BLUEMIX_EVENT		"status"
	#define BLUEMIX_FORMAT		"json"

MQTT PUBLISH 的最大循环发送次数在 Kconfig 中定义：

.. code-block:: cfg

	CONFIG_NET_SAMPLE_APP_MAX_ITERATIONS=5

在 Linux 主机上打开终端窗口，进入本示例应用程序的源代码目录（即 :zephyr_file:`samples/net/mqtt_publisher` ），然后输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/mqtt_publisher
   :board: frdm_k64f
   :goals: build flash
   :compact:

如果开发板通过局域网网线直接连接到 Linux 主机，请配置网络接口：

.. code-block:: console

	$ IFACE=eth0 # Change this to the interface to which the LAN cable is connected

	$ IPV4_ADDR_1="192.0.2.2/24"
	$ IPV4_ROUTE_1="192.0.2.0/24"

	$ sudo ip address add $IPV4_ADDR_1 dev $IFACE
	$ sudo ip route add $IPV4_ROUTE_1 dev $IFACE
	$ sudo ip link set dev $IFACE up

你可以运行 ``sudo ip addr flush dev $IFACE`` 来撤销上述步骤。

.. note::
	对于 mosquitto 2.0 及更高版本，请确保在 mosquitto 配置文件 ``mosquitto.conf`` 中添加以下内容以允许匿名（未认证）访问：

	.. code-block:: none

		listener 1883
		allow_anonymous true
		bind_interface eth0

打开另一个终端窗口并输入：

.. code-block:: console

	$ sudo mosquitto -v -p 1883		# For mosquitto < 2.0
	$ sudo mosquitto -v -c mosquitto.conf	# For mosquitto >= 2.0

再打开一个终端窗口并输入：

.. code-block:: console

	$ mosquitto_sub -t sensors

MQTT v5.0 支持
==================

本示例可配置为使用 MQTT v5.0 而非 MQTT v3.1.1。要在示例中启用 MQTT v5.0，请在构建时传入 ``-DEXTRA_CONF_FILE=overlay-mqtt-5.conf`` 参数。本示例应可与任何支持 MQTT v5.0 的 Broker 配合工作，并已在 mosquitto 2.0.21 版本上专门做过测试。在此场景下，服务器端的配置与 MQTT v3.1.1 相同。

当示例配置为 MQTT v5.0 模式时，它会利用主题别名（Topic Alias）特性：即如果 Broker 声明支持主题别名，客户端将为默认的 ``sensors`` 主题注册一个主题别名，并在后续的 MQTT Publish 消息中使用该别名。通过抓包工具（例如 Wireshark）可以观察到，完整主题名称仅出现在第一条 Publish 消息中，而后续所有 Publish 消息由于仅包含主题别名属性，报文体积更小。

使用 TLS 进行安全连接
================================

虽然可以搭建本地安全 MQTT 服务器并修改本示例以连接到该服务器，但这需要用户自行生成证书并在服务器端完成配置。

另一种更简便的方式是使用 `公开可用的 Mosquitto MQTT 服务器/Broker <https://test.mosquitto.org/>`_ 来快速体验启用 TLS 的本示例，具体步骤如下：

- 从 https://test.mosquitto.org 下载 DER 格式的服务器 CA 证书文件
- 在 :file:`src/test_certs.h` 中，使用证书内容设置 ``ca_certificate[]`` （如果目标平台启用了 Socket Offload 特性且 :kconfig:option:`CONFIG_TLS_CREDENTIAL_FILENAMES` 设为 ``y`` ，则将其设置为证书文件名）。
- 在 :file:`src/config.h` 中，将 SERVER_ADDR 设置为要连接的目标 IP 地址，即 test.mosquitto.org 的 IP 地址 ``"37.187.106.16"``
- 在 :file:`src/main.c` 中，将 TLS_SNI_HOSTNAME 设置为 ``"test.mosquitto.org"`` ，以匹配所下载证书中的通用名称（Common Name，CN）。
- 在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 构建本示例（如果目标平台使用 Offload 特性，请参阅下方的 TLS Offload 章节）。
- 将生成的固件烧录到设备中以运行本示例：

.. code-block:: console

        $ west flash

TLS Offload
==============

对于支持该特性的开发板，可在运行 ``west build`` 或 ``cmake`` 时通过指定 ``-DEXTRA_CONF_FILE=overlay-tls-offload.conf`` 来启用 TLS Offload。

使用此 overlay 配置可在不引入 mbedtls 的情况下启用 TLS。

SOCKS5 代理支持
====================

本示例还支持通过 SOCKS5 代理连接到 MQTT Broker。
若要启用该功能，请在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-socks5.conf`` 。

默认情况下，为简化测试，假定代理服务器与 MQTT Broker 运行在同一台主机上。

可以使用 ``ssh`` 启动代理服务器。
在主机上执行以下命令即可在默认端口运行代理：

.. code-block:: console

	$ ssh -N -D 0.0.0.0:1080 localhost

如果要连接的代理服务器与 MQTT Broker 不在同一 IP 地址下运行，或者使用了不同的端口号，请修改以下宏定义：

.. code-block:: c

	#define SOCKS5_PROXY_ADDR    SERVER_ADDR
	#define SOCKS5_PROXY_PORT    1080

MQTT 日志后端
====================

本示例可配置为使用 MQTT 日志后端（logging backend），从而将应用程序的日志消息发布到 MQTT Broker。该特性与主示例应用程序共用同一个 MQTT 客户端实例。

MQTT 日志后端使用 :c:func:`log_backend_mqtt_client_set` API 注册用于发布日志消息的 MQTT 客户端。该后端仅使用客户端的 :c:func:`mqtt_publish` 函数，而不管理客户端的连接生命周期——连接生命周期仍由应用程序负责维护。

要在示例中启用 MQTT 日志后端，请在构建时传入 ``-DEXTRA_CONF_FILE=overlay-log-backend-mqtt.conf`` 参数。

主要可用的配置选项如下：

- :kconfig:option:`CONFIG_LOG_BACKEND_MQTT_TOPIC_DEFAULT` ：发布日志所使用的主题（默认："zephyr/logs"）
- :kconfig:option:`CONFIG_LOG_BACKEND_MQTT_QOS` ：日志消息的 QoS 等级（默认：0）
- :kconfig:option:`CONFIG_LOG_BACKEND_MQTT_RETAIN` ：是否保留（retain）日志消息（默认：禁用）
- :kconfig:option:`CONFIG_LOG_BACKEND_MQTT_MAX_MSG_SIZE` ：最大日志消息大小（默认：256 字节）

在 cc3220sf_launchxl 上运行
================================

cc3220sf_launchxl 上的 Offload 功能同时提供 DHCP 服务，因此本示例在该开发板上使用动态 IP 地址。

默认情况下，本示例配置为连接到 config.h 中 SERVER_ADDR 所指定的 Broker 地址。如果 Broker 使用 TLS 加密，用户应启用 TLS Offload，使用 TI Uniflash 将 DER 格式的服务器 CA 证书文件上传到设备文件系统中，并将其命名为 "ca_cert.der"。

此外，main.c 中的 TLS_SNI_HOSTNAME 应定义为与证书文件中的通用名称（Common Name，CN）一致，以便通过 TLS 域名验证。

请参阅 :zephyr:board:`cc3220sf_launchxl` 文档中关于 Provisioning 和 Fast Connect 的说明。

其中的 Secure Socket Offload 章节介绍了如何将证书烧录到 Flash 中。

随后按上文步骤进行测试即可。

示例输出
=============

以下是配置为如下参数时 FRDM UART 控制台的输出：

.. code-block:: cfg

	CONFIG_NET_SAMPLE_APP_MAX_ITERATIONS=5

.. code-block:: console

	[dev/eth_mcux] [INF] eth_0_init: Enabled 100M full-duplex mode.
	[dev/eth_mcux] [DBG] eth_0_init: MAC 00:04:9f:3e:1a:0a
	[publisher:233] network_setup: 0 <OK>
	[publisher:258] mqtt_init: 0 <OK>
	[connect_cb:81] user_data: CONNECTED
	[try_to_connect:212] mqtt_tx_connect: 0 <OK>
	[publisher:276] try_to_connect: 0 <OK>
	[publisher:285] mqtt_tx_pingreq: 0 <OK>
	[publisher:290] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBACK> packet id: 1888, user_data: PUBLISH
	[publisher:295] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBREC> packet id: 16356, user_data: PUBLISH
	[publish_cb:149] <MQTT_PUBCOMP> packet id: 16356, user_data: PUBLISH
	[publisher:300] mqtt_tx_publish: 0 <OK>
	[publisher:285] mqtt_tx_pingreq: 0 <OK>
	[publisher:290] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBACK> packet id: 45861, user_data: PUBLISH
	[publisher:295] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBREC> packet id: 53870, user_data: PUBLISH
	[publish_cb:149] <MQTT_PUBCOMP> packet id: 53870, user_data: PUBLISH
	[publisher:300] mqtt_tx_publish: 0 <OK>
	[publisher:285] mqtt_tx_pingreq: 0 <OK>
	[publisher:290] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBACK> packet id: 60144, user_data: PUBLISH
	[publisher:295] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBREC> packet id: 6561, user_data: PUBLISH
	[publish_cb:149] <MQTT_PUBCOMP> packet id: 6561, user_data: PUBLISH
	[publisher:300] mqtt_tx_publish: 0 <OK>
	[publisher:285] mqtt_tx_pingreq: 0 <OK>
	[publisher:290] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBACK> packet id: 38355, user_data: PUBLISH
	[publisher:295] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBREC> packet id: 60656, user_data: PUBLISH
	[publish_cb:149] <MQTT_PUBCOMP> packet id: 60656, user_data: PUBLISH
	[publisher:300] mqtt_tx_publish: 0 <OK>
	[publisher:285] mqtt_tx_pingreq: 0 <OK>
	[publisher:290] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBACK> packet id: 28420, user_data: PUBLISH
	[publisher:295] mqtt_tx_publish: 0 <OK>
	[publish_cb:149] <MQTT_PUBREC> packet id: 49829, user_data: PUBLISH
	[publish_cb:149] <MQTT_PUBCOMP> packet id: 49829, user_data: PUBLISH
	[publisher:300] mqtt_tx_publish: 0 <OK>
	[disconnect_cb:101] user_data: DISCONNECTED
	[publisher:304] mqtt_tx_disconnect: 0 <OK>

	Bye!

如下这行输出：

.. code-block:: console

	[try_to_connect:220] mqtt_connect: -5 <ERROR>

表示检测到错误，程序将发送一条新的连接消息。

由于 MQTT API 是异步的，消息会在回调函数执行时打印显示。

以下是订阅端（subscriber）收到的信息：

.. code-block:: console

	$ mosquitto_sub -t sensors
	DOORS:OPEN_QoS0
	DOORS:OPEN_QoS1
	DOORS:OPEN_QoS2
	DOORS:OPEN_QoS0
	DOORS:OPEN_QoS1
	DOORS:OPEN_QoS2
	DOORS:OPEN_QoS0
	DOORS:OPEN_QoS1
	DOORS:OPEN_QoS2
	DOORS:OPEN_QoS0
	DOORS:OPEN_QoS1
	DOORS:OPEN_QoS2
	DOORS:OPEN_QoS0
	DOORS:OPEN_QoS1
	DOORS:OPEN_QoS2

以下是 MQTT Broker 的输出：

.. code-block:: console

	$ sudo mosquitto -v
	1485663791: mosquitto version 1.3.4 (build date 2014-08-17 00:14:52-0300) starting
	1485663791: Using default config.
	1485663791: Opening ipv4 listen socket on port 1883.
	1485663791: Opening ipv6 listen socket on port 1883.
	1485663797: New connection from 192.168.1.101 on port 1883.
	1485663797: New client connected from 192.168.1.101 as zephyr_publisher (c1, k0).
	1485663797: Sending CONNACK to zephyr_publisher (0)
	1485663798: Received PINGREQ from zephyr_publisher
	1485663798: Sending PINGRESP to zephyr_publisher
	1485663798: Received PUBLISH from zephyr_publisher (d0, q0, r0, m0, 'sensors', ... (15 bytes))
	1485663799: Received PUBLISH from zephyr_publisher (d0, q1, r0, m1888, 'sensors', ... (15 bytes))
	1485663799: Sending PUBACK to zephyr_publisher (Mid: 1888)
	1485663799: Received PUBLISH from zephyr_publisher (d0, q2, r0, m16356, 'sensors', ... (15 bytes))
	1485663799: Sending PUBREC to zephyr_publisher (Mid: 16356)
	1485663799: Received PUBREL from zephyr_publisher (Mid: 16356)
	1485663799: Sending PUBCOMP to zephyr_publisher (Mid: 16356)
	1485663800: Received PINGREQ from zephyr_publisher
	1485663800: Sending PINGRESP to zephyr_publisher
	1485663800: Received PUBLISH from zephyr_publisher (d0, q0, r0, m0, 'sensors', ... (15 bytes))
	1485663801: Received PUBLISH from zephyr_publisher (d0, q1, r0, m45861, 'sensors', ... (15 bytes))
	1485663801: Sending PUBACK to zephyr_publisher (Mid: 45861)
	1485663801: Received PUBLISH from zephyr_publisher (d0, q2, r0, m53870, 'sensors', ... (15 bytes))
	1485663801: Sending PUBREC to zephyr_publisher (Mid: 53870)
	1485663801: Received PUBREL from zephyr_publisher (Mid: 53870)
	1485663801: Sending PUBCOMP to zephyr_publisher (Mid: 53870)
	1485663802: Received PINGREQ from zephyr_publisher
	1485663802: Sending PINGRESP to zephyr_publisher
	1485663802: Received PUBLISH from zephyr_publisher (d0, q0, r0, m0, 'sensors', ... (15 bytes))
	1485663803: Received PUBLISH from zephyr_publisher (d0, q1, r0, m60144, 'sensors', ... (15 bytes))
	1485663803: Sending PUBACK to zephyr_publisher (Mid: 60144)
	1485663803: Received PUBLISH from zephyr_publisher (d0, q2, r0, m6561, 'sensors', ... (15 bytes))
	1485663803: Sending PUBREC to zephyr_publisher (Mid: 6561)
	1485663803: Received PUBREL from zephyr_publisher (Mid: 6561)
	1485663803: Sending PUBCOMP to zephyr_publisher (Mid: 6561)
	1485663804: Received PINGREQ from zephyr_publisher
	1485663804: Sending PINGRESP to zephyr_publisher
	1485663804: Received PUBLISH from zephyr_publisher (d0, q0, r0, m0, 'sensors', ... (15 bytes))
	1485663805: Received PUBLISH from zephyr_publisher (d0, q1, r0, m38355, 'sensors', ... (15 bytes))
	1485663805: Sending PUBACK to zephyr_publisher (Mid: 38355)
	1485663805: Received PUBLISH from zephyr_publisher (d0, q2, r0, m60656, 'sensors', ... (15 bytes))
	1485663805: Sending PUBREC to zephyr_publisher (Mid: 60656)
	1485663805: Received PUBREL from zephyr_publisher (Mid: 60656)
	1485663805: Sending PUBCOMP to zephyr_publisher (Mid: 60656)
	1485663806: Received PINGREQ from zephyr_publisher
	1485663806: Sending PINGRESP to zephyr_publisher
	1485663806: Received PUBLISH from zephyr_publisher (d0, q0, r0, m0, 'sensors', ... (15 bytes))
	1485663807: Received PUBLISH from zephyr_publisher (d0, q1, r0, m28420, 'sensors', ... (15 bytes))
	1485663807: Sending PUBACK to zephyr_publisher (Mid: 28420)
	1485663807: Received PUBLISH from zephyr_publisher (d0, q2, r0, m49829, 'sensors', ... (15 bytes))
	1485663807: Sending PUBREC to zephyr_publisher (Mid: 49829)
	1485663807: Received PUBREL from zephyr_publisher (Mid: 49829)
	1485663807: Sending PUBCOMP to zephyr_publisher (Mid: 49829)
	1485663808: Received DISCONNECT from zephyr_publisher

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 配置片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。
