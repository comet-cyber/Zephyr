.. zephyr:code-sample:: tftp-client
   :name: TFTP 客户端
   :relevant-api: tftp_client

   使用 TFTP 客户端库从 TFTP 服务器获取（get）文件或向其上传（put）文件。

概述
********

简单文件传输协议（TFTP，Trivial File Transfer Protocol）是一种基于 UDP 的简单锁步（Lockstep）文件传输协议，旨在从远程主机获取文件或将文件上传到远程主机。

本 Zephyr TFTP 客户端示例应用程序实现了 TFTP 客户端库调用，并在标准端口 69 上与 TFTP 服务器建立连接。

本示例应用程序的源代码可在 :zephyr_file:`samples/net/tftp_client` 中找到。

环境要求
**************

- :ref:`networking_with_eth_qemu` 、 :ref:`networking_with_qemu` 或 :ref:`networking_with_native_sim`
- Linux 主机

构建与运行
********************

在 samples/net/tftp_client 目录下提供了适用于不同环境的配置文件：

- :file:`prj.conf`
  这是标准的默认配置文件。

按如下方式构建 tftp-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/tftp_client
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

配置并运行本示例应用程序最简单的方式是使用默认配置文件 :file:`prj.conf` ，将其作为 native_sim 应用程序或 QEMU 目标进行构建和运行。这需要进行少量前期配置，具体请参见 :ref:`networking_with_eth_qemu` 、 :ref:`networking_with_qemu` 和 :ref:`networking_with_native_sim` 。

按如下方式针对 :zephyr:board:`native_sim <native_sim>` 构建并运行 tftp-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/tftp_client
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:

下载并运行一个 TFTP 服务器（例如 TFTPd），然后创建 file1.bin（包含数据）和 newfile.bin。

请注意，默认的服务器 IP 地址为 192.0.2.2，默认端口为 69。若要指定其他服务器 IP 地址和/或端口，请在 ``prj.conf`` 中修改以下配置项：

.. code-block:: cfg

    CONFIG_TFTP_APP_SERVER="10.0.0.10"
    CONFIG_TFTP_APP_PORT="70"

若要使用主机名连接服务器，请在 ``prj.conf`` 中修改以下两项配置以启用 DNS 解析器：

.. code-block:: cfg

    CONFIG_DNS_RESOLVER=y
    CONFIG_TFTP_APP_SERVER="my-tftp-server.org"

示例输出
==================================

在主机上运行 TFTP 服务器的同时，可在 :zephyr:board:`native_sim<native_sim>` 上运行本示例。

启动 net-tools 中的 :command:`net-setup.sh` ：

.. code-block:: bash

   net-setup.sh

.. code-block:: bash

    <inf> net_config: Initializing network
    <inf> net_config: IPv4 address: 192.0.2.1
    <inf> net_tftp_client_app: Run TFTP client
    <inf> net_tftp_client_app: Received data:
            74 65 73 74 74 66 74 70  66 6f 72 7a 65 70 68 79 |testtftp forzephy
            72 0a                                            |r.
    <inf> net_tftp_client_app: TFTP client get done
    <inf> net_tftp_client_app: TFTP client put done
