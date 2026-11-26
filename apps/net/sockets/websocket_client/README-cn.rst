.. zephyr:code-sample:: sockets-websocket-client
   :name: WebSocket 客户端
   :relevant-api: bsd_sockets websocket

   实现一个连接到 WebSocket 服务器的 WebSocket 客户端。

概述
********

本示例应用程序实现了一个 WebSocket 客户端：它会先向 HTTP 服务器发起 HTTP 或 HTTPS 握手请求，随后开始发送数据并等待来自 WebSocket 服务器的响应。

本示例应用程序的源代码位于： :zephyr_file:`samples/net/sockets/websocket_client` 。

环境要求
**************

- :ref:`networking_with_host`

构建与运行
********************

你可以在受支持的开发板上运行本应用程序，也可以按照 :ref:`networking_with_qemu` 中的说明在 QEMU 中运行。

按如下方式构建 websocket-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/websocket_client
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

启用 TLS 支持
====================

使用以下命令在构建工程时启用 ``overlay-tls.conf`` overlay 配置文件，即可在本示例中启用 TLS 支持：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/websocket_client
   :board: qemu_x86
   :conf: "prj.conf overlay-tls.conf"
   :goals: build
   :compact:

另一种方法是在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 。

本示例所使用的证书和私钥位于示例的 :zephyr_file:`samples/net/sockets/websocket_client/src/` 目录中。


在 Linux 宿主机上运行 websocket-server
================================================

你可以在 QEMU 中运行此 ``websocket-client`` 示例应用程序，并在 Linux 宿主机上运行 ``zephyr-websocket-server.py`` （来自 net-tools）。另一种替代方案是安装并使用 `websocketd <http://websocketd.com/>`_ 。

如需使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。

在终端窗口中可以执行以下命令之一：

.. code-block:: console

    $ ./zephyr-websocket-server.py

或者

.. code-block:: console

    $ websocketd --port=9001 cat

在 QEMU 中运行 ``websocket-client`` 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/websocket_client
   :host-os: unix
   :board: qemu_x86
   :conf: prj.conf
   :goals: run
   :compact:

请注意，在 QEMU 中启动 ``websocket-client`` 应用程序之前，必须先在 Linux 宿主机终端窗口中运行 ``zephyr-websocket-server.py`` 或 ``websocketd`` 。按 :kbd:`CTRL+A` :kbd:`x` 可退出 QEMU。

目前 `net-tools <https://github.com/zephyrproject-rtos/net-tools>`_ 项目中的 ``zephyr-websocket-server.py`` 版本暂不支持 TLS。
