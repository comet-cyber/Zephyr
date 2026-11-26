.. zephyr:code-sample:: aws-iot-mqtt
   :name: AWS IoT Core MQTT
   :relevant-api: bsd_sockets mqtt_socket dns_resolve tls_credentials json sntp random_api

   连接至 AWS IoT Core 并使用 MQTT 发布消息。

概述
********

本示例应用程序演示了如何使用 MQTT 协议实现一个向 AWS IoT Core 发布消息的 MQTT 客户端。主要特性包括：

- 获取 DHCPv4 租约
- 连接至 SNTP 服务器以获取当前时间
- 与 AWS IoT Core 服务器建立 TLS 1.2 连接
- 在 AWS IoT Core 上订阅主题（Topic）
- 向 AWS IoT Core 发布数据
- 通过 AWS 设备认证计划（DQP）测试套件： `Device Qualification Program (DQP) <https://aws.amazon.com/partners/programs/dqp/>`_
- 发送和接收保活（Keep-alive）Ping 消息
- 使用指数退避算法重试连接

环境要求
**************

- 熵源（Entropy source）
- 具有 AWS IoT Core 访问权限的 AWS 账户
- AWS 凭据及相关必要信息
- 网络连接

构建与运行
********************

本应用程序已在 ST NUCLEO-F429ZI 开发板和 QEMU x86 目标平台上完成构建与测试。向 AWS IoT Core 进行身份验证需要有效的证书和私钥。本示例包含一个转换脚本，用于将证书和私钥转换为可嵌入应用程序的格式。

在 AWS IoT Core 中注册一个 *thing* （事物）并下载证书与私钥。将这些文件复制到 :zephyr_file:`samples/net/cloud/aws_iot_mqtt/src/creds` 目录中。运行 :zephyr_file:`samples/net/cloud/aws_iot_mqtt/src/creds/convert_keys.py` 脚本，该脚本将生成 ``ca.c`` 、 ``cert.c`` 和 ``key.c`` 文件。

要配置本示例，请根据你的 AWS IoT Core 区域（Region）、事物（Thing）以及 Device Advisor 配置设置以下 Kconfig 选项：

- :kconfig:option:`CONFIG_AWS_ENDPOINT`: AWS IoT Core Broker 端点，可在 AWS IoT Core 控制台中查看。如果使用 Device Advisor 运行测试套件，此处需填写对应的专用端点。
- :kconfig:option:`CONFIG_AWS_MQTT_PORT`: AWS IoT Core MQTT Broker 的端口号。
- :kconfig:option:`CONFIG_AWS_THING_NAME`: 在 AWS IoT Core 中创建的事物（Thing）名称。它与证书关联，并将用作客户端 ID（Client ID）。本示例中使用 ``zephyr_sample`` 。
- :kconfig:option:`CONFIG_AWS_SUBSCRIBE_TOPIC`: 要订阅的主题。
- :kconfig:option:`CONFIG_AWS_PUBLISH_TOPIC`: 要发布到的主题。
- :kconfig:option:`CONFIG_AWS_QOS`: 订阅与发布的 QoS 等级。
- :kconfig:option:`CONFIG_AWS_EXPONENTIAL_BACKOFF`: 启用指数退避算法。

更多信息请参阅 `AWS IoT Core 文档 <https://docs.aws.amazon.com/iot/index.html>`_ 。

此外，还可以调整固件以通过 AWS DQP 测试套件，只需将 Kconfig 选项 :kconfig:option:`CONFIG_AWS_TEST_SUITE_DQP` 设置为 ``y`` 即可。

有关 AWS Device Advisor 的更多信息，请参阅： `AWS IoT Core Device Advisor <https://aws.amazon.com/iot-core/device-advisor/>`_ 。

MQTT 测试客户端
======================

在 AWS IoT Core 控制台中打开 MQTT 测试客户端，订阅 ``zephyr_sample/data`` 主题，并向 ``zephyr_sample/downlink`` 主题发布 Payload。设备控制台将显示设备接收到的 Payload，同时 AWS 控制台将在 ``zephyr_sample/data`` 主题下显示设备发送的 JSON 消息。

示例输出
==============

以下是 NUCLEO-F429ZI 开发板上 ST-Link UART 的输出内容：

.. code-block:: console

  *** Booting Zephyr OS build zephyr-v3.3.0 ***
  [00:00:01.626,000] <inf> aws: starting DHCPv4
  [00:00:01.969,000] <dbg> aws: sntp_sync_time: Acquired time from NTP server: 1683472436
  [00:00:01.977,000] <inf> aws: Resolved: 52.212.60.110:8883
  [00:00:03.327,000] <dbg> aws: mqtt_event_cb: MQTT event: CONNACK [0] result: 0
  [00:00:03.327,000] <inf> aws: Subscribing to 1 topic(s)
  [00:00:03.390,000] <dbg> aws: mqtt_event_cb: MQTT event: SUBACK [7] result: 0
  [00:00:03.390,000] <inf> aws: PUBLISHED on topic "zephyr_sample/data" [ id: 1 qos: 0 ], payload: 13 B
  [00:00:03.390,000] <dbg> aws: publish_message: Published payload:
                                7b 22 63 6f 75 6e 74 65  72 22 3a 30 7d          |{"counte r":0}
  [00:00:11.856,000] <dbg> aws: mqtt_event_cb: MQTT event: PUBLISH [2] result: 0
  [00:00:11.856,000] <inf> aws: RECEIVED on topic "zephyr_sample/downlink" [ id: 13 qos: 0 ] payload: 45 / 4096 B
  [00:00:11.856,000] <dbg> aws: handle_published_message: Received payload:
                                7b 0a 20 20 22 6d 65 73  73 61 67 65 22 3a 20 22 |{.  "mes sage": "
                                48 65 6c 6c 6f 20 66 72  6f 6d 20 41 57 53 20 49 |Hello fr om AWS I
                                6f 54 20 63 6f 6e 73 6f  6c 65 22 0a 7d          |oT conso le".}
  [00:00:11.857,000] <inf> aws: PUBLISHED on topic "zephyr_sample/data" [ id: 2 qos: 0 ], payload: 13 B
  [00:00:11.857,000] <dbg> aws: publish_message: Published payload:
                                7b 22 63 6f 75 6e 74 65  72 22 3a 31 7d          |{"counte r":1}
  [00:01:11.755,000] <dbg> aws: mqtt_event_cb: MQTT event: 9 result: 0
  [00:02:11.755,000] <dbg> aws: mqtt_event_cb: MQTT event: 9 result: 0

在 QEMU x86 中运行
========================

本示例可在 QEMU x86 中运行。为此，你需要在宿主机上配置 NAT/MASQUERADE。更多信息请参阅 Zephyr 文档 :ref:`networking_with_qemu` 。
