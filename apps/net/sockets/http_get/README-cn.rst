.. zephyr:code-sample:: sockets-http-get
   :name: 使用普通 Socket 实现 HTTP GET
   :relevant-api: bsd_sockets tls_credentials secure_sockets_options

   使用普通 BSD Socket 实现 HTTP(S) 客户端。

概述
********

Zephyr 的 sockets/http_get 示例应用程序使用兼容 BSD Socket 的 API 实现了一个简单的 HTTP GET 客户端。本示例旨在展示如何开发可在 POSIX 系统与 Zephyr 之间移植的 Socket 应用程序。因此，本示例保持精简设计，仅支持 IPv4。

本示例应用程序的源代码位于 :zephyr_file:`samples/net/sockets/http_get` 目录。

环境要求
************

- :ref:`networking_with_host`
- 或者具备硬件网络功能的开发板
- 需配置好 NAT/路由以允许连接到互联网
- 主机端需有可用的 DNS 服务器以解析域名

构建与运行
********************

按如下方式构建 Zephyr 版本的应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/http_get
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会向 "google.com:80" 发送 HTTP GET 请求并打印响应内容。你可以修改源代码，向互联网上的其他任意站点（或局域网内的站点，此时无需配置 NAT/路由）发送请求。
按 :kbd:`CTRL+A` :kbd:`x` 组合键可退出 QEMU。

启用 TLS 支持
=================================

通过启用 ``overlay-tls.conf`` overlay 文件构建工程即可在本示例中启用 TLS 支持，例如使用以下命令：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/http_get
   :board: qemu_x86
   :conf: "prj.conf overlay-tls.conf"
   :goals: build
   :compact:

另一种方法是在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 参数。

对于支持 TLS Offload 的开发板（例如 TI 的 cc3220sf_launchxl），请使用 ``overlay-tls-offload.conf`` 替代 ``overlay-tls.conf`` 文件。

本示例所使用的证书位于示例工程的 ``src`` 目录下。该证书专为访问示例中配置的默认网站（ https://google.com ）而选取。若要通过 TLS 访问其他网页，请提供相应的证书以对该 Web 服务器进行身份验证。

请注意，本示例中的 TLS 支持依赖于非 POSIX 标准的 TLS Socket 功能。因此，本示例的 TLS 模式只能在 Zephyr 上运行。

启用 TLS 会话缓存
==========================

若要启用持久化 TLS 会话缓存，请在 TLS overlay 的基础上叠加使用 ``overlay-tls-session-cache.conf`` overlay 文件：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/http_get
   :board: <board_to_use>
   :conf: "prj.conf overlay-tls.conf overlay-tls-session-cache.conf"
   :goals: build
   :compact:

该 overlay 通过 settings 子系统启用了持久化会话缓存。每次成功完成 TLS 握手后都会保存会话，并在设备启动时恢复，从而支持设备重启后无需完整握手即可恢复会话。

Wi-Fi
=====

可通过 :ref:`Wi-Fi 代码片段（snippet） <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。

在 POSIX 主机上运行应用程序
======================================

同一份应用程序源代码也可针对 POSIX 系统（例如 Linux）进行构建。（注：查看源代码即可发现，除 Zephyr 与 POSIX 所包含的头文件不同外，其余代码完全一致。）

构建方法：

.. code-block:: console

    $ make -f Makefile.host

运行方法：

.. code-block:: console

    $ ./http_get

可以看到，该应用程序的行为与 Zephyr 版本完全相同。
