.. zephyr:code-sample:: sockets-echo-client
   :name: Echo 客户端（高级）
   :relevant-api: bsd_sockets tls_credentials

   实现一个发送 IP 数据包、等待数据回传并校验其一致性的客户端。

概述
********

本 Zephyr echo-client 示例应用程序实现了一个 UDP/TCP 客户端，它会发送 IPv4 或 IPv6 数据包，等待数据回传，然后验证返回的数据是否与发送的数据一致。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/sockets/echo_client` 。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

本应用程序有多种使用方式。最常见的使用场景之一是在 QEMU 中运行 echo-client 应用程序，具体方法请参阅 :ref:`networking_with_qemu` 。

在 echo-client 目录下针对不同开发板和配置场景提供了多个配置文件：

- :file:`prj.conf`
  通用配置文件，通常情况下应使用此文件。

- :file:`overlay-ot.conf`
  该 overlay 配置用于启用 OpenThread 支持。

- :file:`overlay-802154.conf`
  该 overlay 配置用于启用原生 IEEE 802.15.4 连接支持。注意，默认情况下 IEEE 802.15.4 L2 使用无确认（Unacknowledged）通信。为了提高连接可靠性，可以通过 Shell 命令启用确认机制： ``ieee802154 ack set`` 。

- :file:`overlay-qemu_802154.conf`
  该 overlay 配置用于在模拟两个互联的 QEMU 实例组建 IEEE 802.15.4 网络时启用支持。

- :file:`overlay-tls.conf`
  该 overlay 配置用于启用 TLS 支持。

- :file:`overlay-vlan.conf`
  该 overlay 配置用于启用虚拟局域网（VLAN）支持。详情请参阅 :ref:`networking_samples_common` 。

按如下方式构建 echo-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

为启用 OpenThread 支持的 nrf52840dk/nrf52840 构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: nrf52840dk/nrf52840
   :conf: "prj.conf overlay-ot.conf"
   :goals: run
   :compact:

为 IEEE 802.15.4 RF2XX 收发器构建的示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: [samr21_xpro | sam4s_xplained | sam_v71_xult/samv71q21]
   :gen-args: -DEXTRA_CONF_FILE=overlay-802154.conf
   :goals: build flash
   :compact:

可以在终端窗口中检查通信是否正常进行：

.. code-block:: console

    $ minicom -D /dev/ttyACM1



启用 TLS 支持
====================

在构建工程时启用 ``overlay-tls.conf`` overlay 文件即可为本示例启用 TLS 支持，例如使用以下命令：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :board: qemu_x86
   :conf: "prj.conf overlay-tls.conf"
   :goals: build
   :compact:

另一种方式是在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 。

本示例使用的证书和私钥位于示例的 ``src`` 目录中。Socket Echo 客户端与 :zephyr:code-sample:`sockets-echo-server` 使用的默认证书支持在这两个示例之间建立安全连接。

SOCKS5 代理支持
====================

也可以通过 SOCKS5 代理连接到 echo-server。若要启用该功能，请在运行 ``west build`` 或 ``cmake`` 时使用 ``-DEXTRA_CONF_FILE=overlay-socks5.conf`` 。

默认情况下，为了便于测试，代理服务器预期与 echo-server 运行在同一台 Linux 主机上。

若要启动代理服务器，例如可以使用 SSH 内置的 SOCKS 服务器支持（-D 选项）。使用以下命令在主机上以默认端口运行代理服务器：

对于 IPv4 代理服务器：

.. code-block:: console

        $ ssh -N -D 0.0.0.0:1080 localhost

对于 IPv6 代理服务器：

.. code-block:: console

        $ ssh -N -D [::]:1080 localhost

如果同时测试 IPv4 和 IPv6，请同时运行上述两条命令。

如果要连接的代理服务器与 echo-server 不在同一 IP 地址下运行，或者使用了不同的端口号，请修改 echo_client/src/tcp.c 中的以下宏定义：

.. code-block:: c

        #define SOCKS5_PROXY_V4_ADDR IPV4_ADDR
        #define SOCKS5_PROXY_V6_ADDR IPV6_ADDR
        #define SOCKS5_PROXY_PORT    1080

Wi-Fi
=====

可以通过 :ref:`Wi-Fi 代码片段（snippet） <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。

在 Linux 主机上运行 echo-server
========================================

结合 Linux 主机有一种非常实用的测试场景：在 QEMU 中运行 echo-client，同时在 Linux 主机上运行 echo-server。

若要使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。

在终端窗口中运行：

.. code-block:: console

    $ sudo ./echo-server -i tap0

在 QEMU 中运行 echo-client 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :conf: "prj.conf overlay-linux.conf"
   :goals: run
   :compact:

请注意，在 QEMU 中启动 echo-client 应用程序之前，必须先在 Linux 主机终端窗口中运行 echo-server。按下 :kbd:`CTRL+A` :kbd:`x` 可退出 QEMU。

你也可以结合 Linux 主机验证 TLS 通信。有关如何使用 Linux 主机示例测试 TLS 的信息，请参阅 https://github.com/zephyrproject-rtos/net-tools 文档。

有关在 Linux 主机上运行 echo-client 并在 QEMU 中运行 echo-server 的另一种运行方式，请参阅 :zephyr:code-sample:`sockets-echo-server` 文档。

OpenThread RCP + Zephyr 主机（通过 UART 建立 SPINEL 连接）
========================================================================

前置条件：
------------------

- 为主机 PC（x86_64）构建 ``echo-server``
  (https://github.com/zephyrproject-rtos/net-tools) SHA1:1c4fdba

.. code-block:: console

    $ make echo-server

- 从 Nordic nRF SDK（v2.7.0）烧录 nRF RCP：

.. code-block:: console

   (v2.7.0) ~/ncs$ west build -p always -b nrf21540dk/nrf52840 -S logging nrf/samples/openthread/coprocessor


- 构建 mimxrt1020_evk 主机固件（Zephyr）：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :board: mimxrt1020_evk
   :conf: "prj.conf overlay-ot-rcp-host-uart.conf"
   :goals: build
   :compact:

并烧录：

.. code-block:: console

    $ west flash -r pyocd -i 0226000047784e4500439004d9170013e56100009796990


- 通过 UART 连接 nRF RCP 与 IMXRT1020（主机）：

.. code-block:: c

	/*
	 * imxrt1020_evk -> HOST
	 * nRF21540-DK   -> RCP (nrf/samples/openthread/coprocessor)
	 * LPUART2 used for communication:
	 *  nRF21540 (P6) P0.08 RXD -> IMXRT1020-EVK (J17) D1 (GPIO B1 08) (TXD)
	 *  nRF21540 (P6) P0.07 CTS -> IMXRT1020-EVK (J19) D8 (GPIO B1 07) (RTS)
	 *  nRF21540 (P6) P0.06 TXD -> IMXRT1020-EVK (J17) D0 (GPIO B1 09) (RXD)
	 *  nRF21540 (P6) P0.05 RTS -> IMXRT1020-EVK (J17) D7 (GPIO B1 06) (CTS)
	 */


- 在主机 PC（x86_64）上安装 OTBR（OpenThread Border Router）Docker 容器，请遵循 https://docs.nordicsemi.com/bundle/ncs-2.5.1/page/nrf/protocols/thread/tools.html#running_otbr_using_docker 中的步骤。

**关键步骤如下：**

  1. 创建 ``otbr0`` 网桥，以便从 Linux 主机 PC 访问 OT 网络：

  .. code-block:: console

    sudo docker network create --ipv6 --subnet fd11:db8:1::/64 -o com.docker.network.bridge.name=otbr0 otbr


  2. 拉取 OTBR 的 Docker 容器镜像：

  .. code-block:: console

    docker pull nrfconnect/otbr:84c6aff


  3. 启动 Docker 镜像：

  .. code-block:: console

    sudo modprobe ip6table_filter
    sudo docker run -it --rm --privileged --name otbr --network otbr -p 8080:80 --sysctl "net.ipv6.conf.all.disable_ipv6=0 net.ipv4.conf.all.forwarding=1 net.ipv6.conf.all.forwarding=1" --volume /dev/ttyACM5:/dev/radio nrfconnect/otbr:84c6aff --radio-url spinel+hdlc+uart:///dev/radio?uart-baudrate=1000000


  4. 在主机 PC（x86_64）上添加正确的路由（ ``fd11:22::/64`` 是允许访问 OT 设备的网内（On-Mesh）IPv6 地址段）：

  .. code-block:: console

    sudo ip -6 route add fd11:22::/64 dev otbr0 via fd11:db8:1::2


  查询 OT 网络内地址的路由输出示例如下：

  .. code-block:: console

    ip route get fd11:22:0:0:5188:1678:d0c0:6893
    fd11:22::5188:1678:d0c0:6893 from :: via fd11:db8:1::2 dev otbr0 src fd11:db8:1::1 metric 1024 pref medium


  5. 进入 Docker 容器的控制台：

  .. code-block:: console

    sudo docker exec -it otbr /bin/bash


  例如可使用以下命令进行测试：

  .. code-block:: console

    ot-ctl router table
    ot-ctl ipaddr



配置 OTBR
--------------

在主机 PC 的网页浏览器中打开： http://localhost:8080/

进入 ``Form`` 页面并保留默认值，例如：

  * Network Key:	``00112233445566778899aabbccddeeff``
  * On-Mesh Prefix:	``fd11:22::``
  * Channel:	``15``


以组建（"FORM"）OT 网络。

*注意：*
"On-Mesh Prefix" 必须与 ``otbr0`` 路由中设置的前缀保持一致。


配置 RCP（nRF21540-DK）+ OT 主机（mimxrt1020）
--------------------------------------------------------

.. code-block:: console

   ot factoryreset
   ot dataset networkkey 00112233445566778899aabbccddeeff
   ot ifconfig up


在主机 PC 的 Web 网页界面中执行以下操作：
Commission -> 将 Joiner PSKd* 设置为 ``J01NME`` -> START COMMISSION

.. code-block:: console

   ot joiner start J01NME
   ot thread start


执行 ``ot ipaddr`` 应当会显示以 ``fd11:22:0:0:`` 开头的 IPv6 地址。可以从主机 PC 网络访问该地址（例如通过 ``ping -6 fd11:22:0:0:e8bf:266b:63ca:eff4`` ）。

在主机 PC（x86-64）上启动 ``echo-server``
----------------------------------------------------

.. code-block:: console

   ./echo-server -i otbr0
