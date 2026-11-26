.. zephyr:code-sample:: mqtt-azure
   :name: Microsoft Azure IoT Hub MQTT
   :relevant-api: bsd_sockets mqtt_socket tls_credentials random_api

   使用 MQTT 连接到 Azure IoT Hub 并发布消息。

概述
********

本示例应用程序演示了 MQTT 客户端如何基于 MQTT 协议向 Azure Cloud IoT Hub 发布消息。

- 获取 DHCPv4 租约
- 与 Azure Cloud IoT Hub 建立 TLS 连接
- 向 Azure 云端发布数据
- 支持 SOCKS5
- 支持 DNS

本示例应用程序的源代码可在 :zephyr_file:`samples/net/cloud/mqtt_azure` 中找到。

环境要求
**************

- Azure Cloud 账户
- Azure IoT Cloud 凭据及相关必要信息
- Freedom 开发板（FRDM-K64F）
- 网络连接

构建与运行
********************

本应用程序已在 NXP FRDMK64F 上完成构建与测试。向 Azure Cloud IoT Hub 进行身份认证需要证书。当前 :zephyr_file:`samples/net/cloud/mqtt_azure/src/digicert.cer` 中的证书复制自 `<https://github.com/Azure/azure-iot-sdk-c/blob/master/certs/certs.c>`_ 。

请在自定义的 overlay 配置文件中，根据你的 Azure Cloud IoT Hub 配置以下 Kconfig 选项：

- ``SAMPLE_CLOUD_AZURE_USERNAME`` - 用户名字段请使用： ::

    {iothubhostname}/{device_id}/?api-version=2018-06-30,

  其中 ``{iothubhostname}`` 是该 IoT Hub 的完整 CName。

- ``SAMPLE_CLOUD_AZURE_PASSWORD``    - 密码字段，请使用 SAS Token。
- ``SAMPLE_CLOUD_AZURE_CLIENT_ID``   - ClientId 字段，请使用 deviceId。
- ``SAMPLE_CLOUD_AZURE_HOSTNAME``    - IoT Hub 主机名
- ``SAMPLE_CLOUD_AZURE_SERVER_ADDR`` - Azure MQTT Broker 的 IP 地址
- ``SAMPLE_CLOUD_AZURE_SERVER_PORT`` - Azure MQTT Broker 的端口号

如果在代理服务器后运行本示例，还需要设置以下 Kconfig 选项：

- ``SAMPLE_SOCKS_ADDR`` - SOCKS5 代理服务器的 IP 地址
- ``SAMPLE_SOCKS_PORT`` - SOCKS5 代理服务器的端口号

在 Linux 主机上打开终端窗口，定位到本示例应用程序的源代码目录（即 :zephyr_file:`samples/net/cloud/mqtt_azure` ），然后输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/cloud/mqtt_azure
   :board: frdm_k64f
   :conf: "prj.conf <overlay.conf>"
   :goals: build flash
   :compact:

此外，本应用程序也可以使用 QEMU 进行测试，具体方法请参见 :ref:`networking_with_qemu` 。请在主机上配置好 Zephyr 以及 NAT/地址伪装（Masquerading）以访问互联网，并使用 :file:`overlay-qemu_x86.conf` 配置文件。QEMU 下未启用 DHCP 支持，而是使用静态 IP 地址。

示例 overlay 文件
========================

以下是用于配置 Azure IoT Hub 及其他详细信息的 overlay 模板：

.. code-block:: cfg

	CONFIG_SAMPLE_CLOUD_AZURE_USERNAME="<username>"
	CONFIG_SAMPLE_CLOUD_AZURE_PASSWORD="<SAS token>"
	CONFIG_SAMPLE_CLOUD_AZURE_CLIENT_ID="<device id>"
	CONFIG_SAMPLE_CLOUD_AZURE_HOSTNAME="<IoT hub hostname>"
	CONFIG_SAMPLE_SOCKS_ADDR="<proxy addr>"
	CONFIG_SAMPLE_SOCKS_PORT=<proxy port>
	CONFIG_SAMPLE_CLOUD_AZURE_SERVER_ADDR="<server ip addr, if DNS disabled set this>"
	CONFIG_SAMPLE_CLOUD_AZURE_SERVER_PORT=<server port, if DNS disabled set this>

示例输出
=============

以下是来自 FRDM UART 控制台的输出内容：

.. code-block:: console

	[00:00:03.001,000] <inf> eth_mcux: Enabled 100M full-duplex mode.
	[00:00:03.010,000] <dbg> mqtt_azure.main: Waiting for network to setup...
	[00:00:03.115,000] <inf> net_dhcpv4: Received: 10.0.0.2
	[00:00:03.124,000] <inf> net_config: IPv4 address: 10.0.0.2
	[00:00:03.132,000] <inf> net_config: Lease time: 43200 seconds
	[00:00:03.140,000] <inf> net_config: Subnet: 255.255.255.0
	[00:00:03.149,000] <inf> net_config: Router: 10.0.0.10
	[00:00:06.157,000] <dbg> mqtt_azure.try_to_connect: attempting to connect...
	[00:00:06.167,000] <dbg> net_sock_tls.tls_alloc: (0x200024f8): Allocated TLS context, 0x20001110
	[00:00:19.412,000] <dbg> mqtt_azure.mqtt_event_handler: MQTT client connected!
	[00:00:19.424,000] <dbg> mqtt_azure.publish_message: mqtt_publish OK
	[00:00:19.830,000] <dbg> mqtt_azure.mqtt_event_handler: PUBACK packet id: 63387
	[00:00:31.842,000] <dbg> mqtt_azure.publish_message: mqtt_publish OK
	[00:00:51.852,000] <dbg> mqtt_azure.publish_message: mqtt_publish OK
	[00:00:51.861,000] <dbg> mqtt_azure.mqtt_event_handler: PUBACK packet id: 38106

你还可以在 Azure Portal 上查看事件或消息信息。

云到设备通信
=============================

前往 Azure Portal 中的 IoT 设备（IoT devices）部分，从设备列表中点击目标设备。如果配置了多个设备，请选择正确的设备。进入“向设备发送消息”（Message to Device）界面，在“消息正文”（Message Body）中输入文本，然后点击“发送消息”（Send Message）。

详情请参见 `Azure Cloud MQTT 文档 <https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support>`_ 。
