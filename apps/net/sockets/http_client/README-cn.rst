.. zephyr:code-sample:: sockets-http-client
   :name: HTTP 客户端
   :relevant-api: bsd_sockets http_client tls_credentials secure_sockets_options

   实现一个可发起多种 HTTP 请求的 HTTP(S) 客户端。

概述
********

本示例应用程序实现了一个 HTTP(S) 客户端，它会发起 HTTP 或 HTTPS 请求并等待来自 HTTP 服务器的响应。

此示例应用程序的源代码位于： :zephyr_file:`samples/net/sockets/http_client` 。

环境要求
************

- :ref:`networking_with_host`

构建与运行
********************

你可以在受支持的开发板上使用此应用程序，包括按照 :ref:`networking_with_qemu` 中的说明在 QEMU 中运行它。

按照如下方式构建 http-client 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/http_client
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

启用 TLS 支持
====================

使用以下命令在启用 ``overlay-tls.conf`` overlay 文件的情况下构建工程，即可在本示例中启用 TLS 支持：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/http_client
   :board: qemu_x86
   :conf: "prj.conf overlay-tls.conf"
   :goals: build
   :compact:

另一种方式是在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 。

本示例所使用的证书和私钥位于示例的 :zephyr_file:`samples/net/sockets/http_client/src/` 目录中。Socket HTTP 客户端以及 `net-tools`_ 项目中的 ``https-server.py`` 程序所使用的默认证书，支持在这些示例之间建立安全连接。


在 Linux 主机上运行 http-server
====================================

你可以在 QEMU 中运行此 ``http-client`` 示例应用程序，并在 Linux 主机上运行 ``http-server.py`` （来自 net-tools）。

若要使用 QEMU 进行测试，请遵循 :ref:`networking_with_qemu` 指南。

在终端窗口中执行：

.. code-block:: console

    $ ./http-server.py

在 QEMU 中运行 ``http-client`` 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/http_client
   :host-os: unix
   :board: qemu_x86
   :conf: prj.conf
   :goals: run
   :compact:

请注意，在 QEMU 中启动 http-client 应用程序之前，必须先在 Linux 主机终端窗口中运行 ``http-server.py`` 。按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

你也可以与 Linux 主机验证 TLS 通信，只需使用 net-tools 项目中的 ``https-server.py`` 程序即可。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
