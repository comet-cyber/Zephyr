.. zephyr:code-sample:: secure-mqtt-sensor-actuator
   :name: 安全 MQTT 传感器/执行器
   :relevant-api: mqtt_socket sensor_interface json

   实现基于 MQTT 的物联网（IoT）传感器/执行器设备

概述
********

本示例演示了物联网（IoT）传感器/执行器设备的实现。该应用程序使用 MQTT 协议将传感器数据安全地发送到远程 MQTT Broker，同时响应通过 MQTT 接收到的命令。

功能特性：

- 使用 DHCPv4 租约建立网络连接
- 与 MQTT Broker 建立安全 MQTT 连接（使用 TLS 1.2）
- 按用户定义的时间间隔将 JSON 格式的温度传感器数据发布到 MQTT Broker
- 订阅 MQTT Broker 上用户定义的主题（Topic）
- 响应通过网络接收到的命令（LED 控制）
- 处理 MQTT 连接、重连以及保活（Keep-Alive）
- 网络状态 LED 指示

环境要求
************
- 具备网络功能的开发板（已在 adi_eval_adin1110ebz 上测试）
- `Eclipse Mosquitto`_ MQTT Broker
- DHCP 服务器
- 开发板与 Mosquitto Broker 之间的网络连接

构建与运行
********************
本应用程序依赖开发板与 MQTT Broker 之间的网络连接。该 Broker 可以部署在本地（例如主机 PC 上），也可以使用公开可用的 MQTT Broker <https://test.mosquitto.org/> 。为了便于快速体验和测试，本示例还提供了一套使用静态 IP 地址且不启用加密连接本地 MQTT Broker 的配置。

硬件设置
==============
如果使用以太网，请将开发板连接到 MQTT Broker 所在网络。连接目标可以是你的主机 PC（针对本地托管的 Mosquitto Broker）或互联网路由器（用于连接公共 Mosquitto Broker）。如有需要，请将温度传感器连接到开发板。

软件设置
==============
温度传感器应在 Devicetree 中设置别名为 ``ambient-temp0`` 。如果开发板不包含板载温度传感器，可以外接一个传感器，并使用开发板 overlay 文件添加该传感器及其别名：

.. code-block:: devicetree

	/ {
		aliases {
				ambient-temp0 = &adt7420;
			};
		};
	};

也可以通过在 Devicetree 中添加其他类型的传感器，并修改 :file:`device.c` 中的 ``SENSOR_CHAN`` 以匹配所需的传感器类型，从而使用其他传感器。

本应用程序支持以下几种配置方式：

.. list-table::

   * - :file:`prj.conf`
     - 默认配置：安全 MQTT，动态 IP 地址（DHCP）

   * - :file:`overlay-static.conf`
     - 安全 MQTT，静态 IP 地址

   * - :file:`overlay-static-insecure.conf`
     - 非加密 MQTT，静态 IP 地址

**默认配置：**

使用默认配置时，应用程序将通过 DHCP 获取 IP 地址，并尝试使用 TLS 1.2 安全地连接到 MQTT Broker。

- 开发板所要连接的 MQTT Broker 由 ``CONFIG_NET_SAMPLE_MQTT_BROKER_HOSTNAME`` 指定。默认设置为 test.mosquitto.org。
- 使用 TLS 安全连接时，需要将 Broker 的 CA 证书包含到应用程序中。
- 从 https://test.mosquitto.org 下载 DER 或 PEM 格式的 CA 证书。
- 在 :file:`tls_config/cert.h` 中，将 ``ca_certificate[]`` 设置为该证书的内容。
- 将开发板连接到互联网路由器后，它应能通过 DHCP 自动获取 IPv4 地址。
- 随后应用程序将尝试连接到公共 Mosquitto Broker 并开始发布数据。
- 也可以安全地连接到本地托管的 MQTT Broker，这需要预先配置证书。CA 证书应按上述方式包含到构建中。 ``CONFIG_NET_SAMPLE_MQTT_BROKER_HOSTNAME`` 应配置为匹配本地 Broker 的主机名或 IP 地址。根据所使用的 CA 证书，可能还需要启用额外的 MbedTLS 配置选项，这可以通过 Kconfig 或自定义 MbedTLS 配置文件来完成（参见 modules/mbedtls/Kconfig）。有关在本地为 Mosquitto 配置 TLS 支持的更多信息，请参阅 https://mosquitto.org/man/mosquitto-tls-7.html 。
- 可以在主机 PC 上安装 DHCP 服务器来为开发板分配 IP 地址，例如 dnsmasq（Linux）或 DHCP Server for Windows（Windows）。
- 使用默认配置构建示例：

.. zephyr-app-commands::
	 :zephyr-app: samples/net/secure_mqtt_sensor_actuator
	 :board: adi_eval_adin1110ebz
	 :goals: build
	 :compact:

**静态 IP 配置：**

使用 :file:`overlay-static.conf` Kconfig overlay 可禁用 DHCP 并使用静态 IP 地址配置。设备、网关和 DNS 服务器的 IP 地址应根据你的本地网络配置进行设置。

.. zephyr-app-commands::
	 :zephyr-app: samples/net/secure_mqtt_sensor_actuator
	 :board: adi_eval_adin1110ebz
	 :conf: "prj.conf overlay-static.conf"
	 :goals: build
	 :compact:

**静态 IP / 非加密 MQTT 配置：**

使用 :file:`overlay-static-insecure.conf` Kconfig overlay 可禁用 TLS 和 DHCP。此配置需要连接到本地托管的 Mosquitto MQTT Broker。

- 在 :file:`overlay-static-insecure.conf` 中，设置开发板和 Mosquitto Broker 的 IP 地址（即主机 PC 以太网端口的 IP 地址）。这些地址应位于同一子网中，例如 192.0.2.1 和 192.0.2.2。
- 在主机 PC 上安装 Mosquitto。
- 创建一个名为 ``unsecure.conf`` 的文件，内容如下：

.. code-block:: console

		listener 1883 0.0.0.0
		allow_anonymous true


- 使用该配置文件启动 Mosquitto Broker：

.. code-block:: console

		$ sudo mosquitto -v -c unsecure.conf

- 使用快速测试配置构建示例：

.. zephyr-app-commands::
	 :zephyr-app: samples/net/secure_mqtt_sensor_actuator
	 :board: adi_eval_adin1110ebz
	 :conf: "prj.conf overlay-static-insecure.conf"
	 :goals: build
	 :compact:

使用本示例
================
- 一旦开发板与 Mosquitto Broker 建立 MQTT 连接，网络状态 LED 就会点亮，开发板将按 ``CONFIG_NET_SAMPLE_MQTT_PUBLISH_INTERVAL`` 所确定的固定时间间隔以 JSON 格式发布传感器读数。

- 使用 Mosquitto 订阅开发板发送的传感器数据：

.. code-block:: console

		$ mosquitto_sub -d -h <test.mosquitto.org/local broker IP> -t zephyr_sample/sensor

- 应用程序将订阅由 ``CONFIG_NET_SAMPLE_MQTT_SUB_TOPIC_CMD`` 确定的主题。如果开发板在该主题上收到受支持的命令字符串，就会执行相应的命令处理函数。受支持的命令（定义在 :file:`device.c` 中）：

  - ``led_on`` ，点亮开发板 LED
  - ``led_off`` ，熄灭开发板 LED

- 使用 Mosquitto 向 MQTT Broker 发布这些命令：

.. code-block:: console

		$ mosquitto_pub -d -h <test.mosquitto.org/local broker IP> --cafile <path/to/ca.crt> -t zephyr_sample/command -m "led_on"

- 用于 MQTT 发布和订阅的服务质量（QoS）等级可通过 Kconfig 进行配置。

示例输出
=============

.. code-block:: console

	*** Booting Zephyr OS build v3.6.0-2212-g2c9c4f3733e9 ***
	[00:00:00.181,000] <inf> app_device: Device adt7420@48 is ready
	[00:00:00.181,000] <inf> app_device: Device leds is ready
	[00:00:00.181,000] <inf> app_main: MAC Address: 00:E0:FE:FE:DA:C8
	[00:00:00.181,000] <inf> app_main: Bringing up network..
	[00:00:00.801,000] <inf> net_dhcpv4: Received: 192.168.1.17
	[00:00:00.801,000] <inf> app_main: Network connectivity up!
	[00:00:00.818,000] <inf> app_mqtt: Connecting to MQTT broker @ 91.121.93.94
	[00:00:01.154,000] <inf> net_mqtt: Connect completed
	[00:00:01.197,000] <inf> app_mqtt: Connected to MQTT broker!
	[00:00:01.197,000] <inf> app_mqtt: Hostname: test.mosquitto.org
	[00:00:01.198,000] <inf> app_mqtt: Client ID: adi_eval_adin1110ebz_9a
	[00:00:01.198,000] <inf> app_mqtt: Port: 8883
	[00:00:01.198,000] <inf> app_mqtt: TLS: Enabled
	[00:00:01.198,000] <inf> app_mqtt: Subscribing to 1 topic(s)
	[00:00:01.238,000] <inf> app_mqtt: SUBACK packet ID: 5841
	[00:00:04.200,000] <inf> app_mqtt: Published to topic 'zephyr_sample/sensor', QoS 1
	[00:00:04.319,000] <inf> app_mqtt: PUBACK packet ID: 1
	[00:00:07.202,000] <inf> app_mqtt: Published to topic 'zephyr_sample/sensor', QoS 1
	[00:00:07.323,000] <inf> app_mqtt: PUBACK packet ID: 2
	[00:00:10.204,000] <inf> app_mqtt: Published to topic 'zephyr_sample/sensor', QoS 1
	[00:00:10.322,000] <inf> app_mqtt: PUBACK packet ID: 3
	[00:00:12.769,000] <inf> app_mqtt: MQTT payload received!
	[00:00:12.769,000] <inf> app_mqtt: topic: 'zephyr_sample/command', payload: led_on
	[00:00:12.770,000] <inf> app_device: Executing device command: led_on

.. _Eclipse Mosquitto: https://mosquitto.org/download/
