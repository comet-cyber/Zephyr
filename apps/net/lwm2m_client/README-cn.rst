.. zephyr:code-sample:: lwm2m-client
   :name: LwM2M 客户端
   :relevant-api: lwm2m_api

   实现连接到 LwM2M 服务器的 LwM2M 客户端。

概述
********

轻量级机器对机器（Lightweight Machine to Machine，LwM2M）是一种基于 CoAP/UDP 的应用层协议，旨在极度轻量级的环境中通过 LwM2M 服务器对外暴露各类资源，以供读取、写入和执行。

本 Zephyr LwM2M 客户端示例应用程序实现了 LwM2M 库，并遵循 `Open Mobile Alliance Lightweight Machine to Machine Technical Specification`_ （开放移动联盟轻量级机器对机器技术规范，第 5.3 节：客户端注册接口）与 LwM2M 服务器建立连接。

.. _Open Mobile Alliance Lightweight Machine to Machine Technical Specification:
    http://www.openmobilealliance.org/release/LightweightM2M/V1_0-20170208-A/OMA-TS-LightweightM2M-V1_0-20170208-A.pdf

本示例应用程序的源代码位于： :zephyr_file:`samples/net/lwm2m_client` 。

环境要求
**************

- :ref:`networking_with_eth_qemu` 、 :ref:`networking_with_qemu` 或 :ref:`networking_with_native_sim`
- Linux 主机
- Leshan Demo Server (https://eclipse.org/leshan/)

构建与运行
********************

在 samples/net/lwm2m_client 目录下提供了适用于不同配置场景的配置文件：

.. list-table::

    * - :file:`prj.conf`
      - 标准默认配置文件。

    * - :file:`overlay-bootstrap.conf`
      - 添加此 overlay 配置可启用 LwM2M Bootstrap（引导）支持。

    * - :file:`overlay-ot.conf`
      - 添加此 overlay 配置可启用 OpenThread 支持。

    * - :file:`overlay-dtls.conf`
      - 添加此 overlay 配置可通过 MBEDTLS 启用 DTLS 支持。

    * - :file:`overlay-dtls-cert.conf`
      - 添加此 overlay 配置可通过 MBEDTLS 启用基于证书的 DTLS 支持。

    * - :file:`overlay-queue.conf`
      - 添加此 overlay 配置可启用 LwM2M Queue Mode（队列模式）支持。

    * - :file:`overlay-send-scheduler.conf`
      - 此 overlay 配置用于启用 LwM2M 发送调度器（send scheduler）支持，并为温度和湿度 IPSO 对象启用缓存。

    * - :file:`overlay-tickless.conf`
      - 此 overlay 配置可用于防止 LwM2M 引擎周期性打断 Socket 轮询（poll），在某些设备上能够显著降低功耗。

按如下方式构建 lwm2m-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

搭建本示例应用程序最简便的方式是使用默认配置 :file:`prj.conf` 将其作为 native_sim 应用程序或 QEMU 目标进行构建和运行。这需要完成少量环境配置，具体步骤请参阅 :ref:`networking_with_eth_qemu` 、 :ref:`networking_with_qemu` 和 :ref:`networking_with_native_sim` 。

下载并运行最新构建版本的 Leshan Demo Server：

.. code-block:: console

    $ wget https://ci.eclipse.org/leshan/job/leshan/lastSuccessfulBuild/artifact/leshan-server-demo.jar
    $ java -jar ./leshan-server-demo.jar -wp 8080

现在可以在 Web 浏览器中打开 http://localhost:8080 ，在此页面中查看和管理已连接的 LwM2M 设备。

按如下方式针对 QEMU 构建并运行 lwm2m-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

示例启动后，将使用 IPv6 客户端端点（endpoint）"qemu_x86" 自动连接到 Leshan Demo Server。

若要将示例改为使用 IPv4，请在 ``prj.conf`` 中修改以下两项配置以禁用 IPv6： ::

    CONFIG_NET_IPV6=n
    CONFIG_NET_CONFIG_NEED_IPV6=n

DTLS 支持
==============

若要针对 QEMU 构建启用 DTLS 支持的 lwm2m-client 示例，请执行以下操作：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :host-os: unix
   :board: qemu_x86
   :conf: "prj.conf overlay-dtls.conf"
   :goals: run
   :compact:

在 Leshan Demo Server 中配置 DTLS 安全参数：

1. 打开 Leshan Demo Server 的 Web UI
#. 点击 "Security"
#. 点击 "Add new client security configuration"
#. 输入以下信息：

    * Client endpoint: qemu_x86
    * Security mode: Pre-Shared Key
    * Identity: Client_identity
    * Key: 000102030405060708090a0b0c0d0e0f

#. 启动 Zephyr 示例

Bootstrap（引导）支持
==============================

若要配合本示例运行 Bootstrap 流程，需要下载并运行 Leshan Demo Bootstrap Server：

.. code-block:: console

    $ wget https://ci.eclipse.org/leshan/job/leshan/lastSuccessfulBuild/artifact/leshan-bsserver-demo.jar
    $ java -jar ./leshan-bsserver-demo.jar -wp 8888 -lp 5783 -slp 5784


现在可以在 Web 浏览器中打开 http://localhost:8888 ，此时将打开 Demo Bootstrap Server 的 Web UI，你可以在其中为设备配置 Bootstrap 引导信息。

在 Demo Bootstrap Server 中配置 lwm2m-client 示例：

1. 点击 "Add new client bootstrap configuration"
#. 输入以下信息：

    * Client endpoint: qemu_x86

#. 在 ``LwM2M Server`` 选项卡中，输入以下信息：

    * LwM2M Server URL: coap://[2001:db8::2]:5683 (若使用 IPv4 则为 coap://192.0.2.2:5683)
    * Security mode: No Security

#. ``LwM2M Bootstrap Server`` 选项卡可保持默认配置不变（No Security）。

若要针对 QEMU 构建启用 Bootstrap 的 lwm2m-client 示例，请执行以下操作：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :host-os: unix
   :board: qemu_x86
   :conf: "prj.conf overlay-bootstrap.conf"
   :goals: run
   :compact:

示例启动后，将自动连接到 Leshan Demo Bootstrap Server 以获取 LwM2M 服务器信息。随后，示例将按照 Bootstrap Server 配置中所指示的地址自动连接到 Leshan Demo Server。

也可以组合使用多个 overlay 文件，例如同时启用 DTLS 和 Bootstrap。在这种情况下，用户应确保更新 overlay 文件中用于 Bootstrap over DTLS 的端口号（对于 Leshan Demo Bootstrap Server 为 5784），并在 Web UI 的 ``LwM2M Bootstrap Server`` 选项卡中配置正确的安全模式（Pre-shared Key）。

OpenThread 支持
====================

若要针对需要通过 OpenThread 联网的硬件构建 lwm2m-client 示例，请执行以下操作：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :host-os: unix
   :board: <board to use>
   :conf: "prj.conf overlay-ot.conf"
   :goals: build
   :compact:

注意：如果设备尚未配网（烧录前已完全擦除），设备将组建一个新的 OpenThread 网络并将自身提升为 Leader（当前角色：leader）。若要加入现有的 OT 网络，可以启用 CONFIG_OPENTHREAD_JOINER=y 和 CONFIG_OPENTHREAD_JOINER_AUTOSTART=y，将 CONFIG_OPENTHREAD_JOINER_PSKD 设置为你自行选择的凭据（无默认值），并在现有网络的 Commissioner 上注册相同的 PSKd；或者通过控制台手动配网：

.. code-block:: console

   ot thread stop
   ot channel <channel>
   ot networkname <network name>
   ot masterkey <key>
   ot panid <panid>
   ot extpanid <extpanid>
   ot thread start

你可以在 OTBR 上使用以下命令获取现有 OT 网络的所有参数：

.. code-block:: console

    wpanctl get Thread:ActiveDataset

Queue Mode（队列模式）支持
====================================

若要构建启用 LwM2M Queue Mode 支持的 lwm2m-client 示例，请执行以下操作：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :host-os: unix
   :board: <board to use>
   :conf: "prj.conf overlay-queue.conf"
   :goals: build
   :compact:

启用 Queue Mode 后，LwM2M 客户端将以 "UDP with Queue Mode" 绑定方式进行注册。当接收（RX）窗口关闭时，LwM2M 引擎会向应用程序发送 ``LWM2M_RD_CLIENT_EVENT_QUEUE_MODE_RX_OFF`` 事件通知，以便应用程序执行关闭射频（radio）等省电操作。下一个 RX 窗口将在随后的 ``LWM2M_RD_CLIENT_EVENT_REG_UPDATE_COMPLETE`` 事件触发时开启。

WNC-M14A2A LTE-M 调制解调器支持
========================================

若要构建配合 WNC-M14A2A LTE-M 调制解调器扩展板（shield）使用的 lwm2m-client 示例，请执行以下操作：

.. zephyr-app-commands::
   :zephyr-app: samples/net/lwm2m_client
   :host-os: unix
   :board: <board to use>
   :conf: "prj.conf overlay-wncm14a2a.conf"
   :goals: build
   :compact:

未启用 DTLS 时的示例输出
====================================

以下是来自 QEMU 控制台的示例输出。首先，LwM2M 引擎完成初始化；接着，多个 LwM2M 智能对象（Smart Objects）向引擎注册自身；随后，示例应用程序设置若干客户端属性值，以便在 Leshan Demo Server 界面中查看；最后，向服务器发送注册请求并完成端点的初始化。

.. code-block:: console

    To exit from QEMU enter: 'CTRL+a, x'
    [QEMU] CPU: qemu32,+nx,+pae
    qemu-system-i386: warning: Unknown firmware file in legacy mode: genroms/multiboot.bin

    shell> [lib/lwm2m_engine] [DBG] lwm2m_engine_init: LwM2M engine thread started
    [lwm2m_obj_security] [DBG] security_create: Create LwM2M security instance: 0
    [lwm2m_obj_server] [DBG] server_create: Create LwM2M server instance: 0
    [lwm2m_obj_device] [DBG] device_create: Create LwM2M device instance: 0
    [lwm2m_obj_firmware] [DBG] firmware_create: Create LwM2M firmware instance: 0
    [lwm2m-client] [INF] main: Run LwM2M client
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/0, value:0x0001c99e, len:6
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/1, value:0x0001c9ab, len:23
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/2, value:0x0001c9c9, len:9
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/3, value:0x0001c9d9, len:3
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/9, value:0x0041a3a4, len:1
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/10, value:0x0041a3b4, len:4
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/17, value:0x0001c9fc, len:16
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/18, value:0x0001ca14, len:5
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/20, value:0x0041a3a4, len:1
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3/0/21, value:0x0041a3b4, len:4
    [lib/lwm2m_engine] [DBG] lwm2m_engine_create_obj_inst: path:3303/0
    [ipso_temp_sensor] [DBG] temp_sensor_create: Create IPSO Temperature Sensor instance: 0
    [lib/lwm2m_engine] [DBG] lwm2m_engine_set: path:3303/0/5700, value:0x0041a3b8, len:8
    [lib/lwm2m_rd_client] [INF] lwm2m_rd_client_start: LwM2M Client: qemu_x86
    [lib/lwm2m_rd_client] [INF] sm_do_init: RD Client started with endpoint 'qemu_x86' and client lifetime 0
    [lib/lwm2m_rd_client] [DBG] sm_send_registration: registration sent [2001:db8::2]
    [lib/lwm2m_engine] [DBG] lwm2m_udp_receive: checking for reply from [2001:db8::2]
    [lib/lwm2m_rd_client] [DBG] do_registration_reply_cb: Registration callback (code:2.1)
    [lwm2m-client] [DBG] rd_client_event: Registration complete
    [lib/lwm2m_rd_client] [INF] do_registration_reply_cb: Registration Done (EP='EZd501ZF26')
    [lib/lwm2m_engine] [DBG] lwm2m_udp_receive: reply 0x004001ec handled and removed
