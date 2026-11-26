.. zephyr:code-sample:: ocpp
   :name: OCPP 充电桩
   :relevant-api: ocpp_api

   实现一个连接到中央系统（Central System）服务器并模拟电表读数的 OCPP 充电桩。

概述
********

开放充电点协议（Open Charge Point Protocol，OCPP）是一种应用层通信协议，用于充电桩（电动汽车（EV）充电站）与中央管理系统（也称为充电站网络）之间的通信。

本 Zephyr OCPP 示例应用程序实现了 OCPP 库，并通过 WebSocket 与中央系统（Central System）服务器建立连接。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/ocpp` 。

环境要求
************

- Linux 主机
- STM32 Discovery 开发套件（32F769IDISCOVERY）或任何带网络接口的设备
- SteVe 演示服务器 (<https://github.com/steve-community/steve/blob/master/README.md>)
- 用于测试的局域网（以太网）

配置
*************

本示例应用程序支持通过 Kconfig 设置以下多个配置选项：

- ``CONFIG_NET_SAMPLE_OCPP_SERVER`` ：OCPP 中央系统服务器 IP 地址

- ``CONFIG_NET_SAMPLE_OCPP_PORT`` ：OCPP 中央系统服务器端口号

- ``CONFIG_NET_SAMPLE_OCPP_WS_PATH`` ：WebSocket URL 路径

- ``CONFIG_NET_SAMPLE_SNTP_SERVER`` ：用于从网络获取时间的 SNTP 服务器 IP 地址

生成用于 TLS 的密钥与证书（可选）：
*******************************************************

- 使用 OpenSSL 生成 ECDSA 私钥：

   .. code-block:: console

      openssl ecparam -name prime256v1 -genkey -noout -out ec-priv.key

- 使用 OpenSSL 生成自签名证书：

   .. code-block:: console

      openssl req -new -x509 -key ec-priv.key -days 3650 \
      -subj "/CN=localhost" -outform PEM -out ec.crt

构建与运行
********************

按如下方式构建 OCPP 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ocpp
   :board: <board to use>
   :goals: build
   :compact:

可按如下命令在目标板上构建并测试本示例应用程序：

.. code-block:: console

	west build -b stm32f769i_disco
	west flash

示例输出如下：

.. code-block:: console

	*** Booting Zephyr OS build v3.6.0-rc1-37-g8c035d8f24cf ***
	OCPP sample stm32f769i_disco
	[00:00:02.642,000] <inf> net_dhcpv4: Received: 192.168.1.101
	[00:00:02.642,000] <inf> main: net mgr cb
	[00:00:02.642,000] <inf> main: Your address: 192.168.1.101
	[00:00:02.642,000] <inf> main: Lease time: 86400 seconds
	[00:00:02.642,000] <inf> main: Subnet: 255.255.255.0
	[00:00:02.643,000] <inf> main: Router: 192.168.1.1
	[00:00:07.011,000] <inf> main: cs server 122.165.245.213 8180
	[00:00:07.011,000] <inf> main: IPv4 Address 122.165.245.213
	[00:00:07.024,000] <inf> main: sntp succ since Epoch: 1707890823
	[00:00:07.024,000] <inf> ocpp: upstream init
	[00:00:07.025,000] <inf> ocpp: ocpp init success
	[00:00:17.066,000] <inf> main: ocpp auth 0> idcon 1 status 1
	[00:00:17.101,000] <inf> main: ocpp auth 0> idcon 2 status 1
	[00:00:17.197,000] <inf> main: ocpp start charging connector id 1
	[00:00:17.255,000] <inf> main: ocpp start charging connector id 2
	[00:01:07.064,000] <inf> main: ocpp stop charging connector id 1
	[00:01:08.063,000] <inf> main: ocpp stop charging connector id 2
