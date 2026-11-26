.. zephyr:code-sample:: sockets-big-http-download
   :name: 大文件 HTTP 下载 (Large HTTP download)
   :relevant-api: bsd_sockets tls_credentials

   使用 BSD Sockets 从 Web 服务器下载大文件。

概述
********

Zephyr 的 ``sockets/big_http_download`` 示例应用程序使用兼容 BSD Sockets 的 API 实现了一个简单的 HTTP GET 客户端。与 :zephyr:code-sample:`sockets-http-get` 示例应用程序不同，它会下载数兆字节（MB）大小的文件，并通过哈希计算校验文件完整性。此外，它还会重复执行下载并统计已传输的总字节数。因此，它可以作为 Zephyr IP 协议栈的“负载测试”应用程序。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/big_http_download` 。

环境要求
**************

- :ref:`networking_with_host`
- 或者一块具备硬件网络功能的开发板
- 需配置好 NAT/路由，以允许连接至互联网
- 主机端需提供可用的 DNS 服务器以解析域名

构建与运行
********************

按如下方式构建 Zephyr 版本的应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/big_http_download
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会向 http://archive.ubuntu.com/ubuntu/dists/xenial/main/installer-amd64/current/images/hd-media/vmlinuz 发起 HTTP GET 请求。选择该站点是因为它提供了多种不同大小的文件以及对应的多种哈希值，便于外部选择和校验。此处选定的文件大小为 6.7MB，既能展示 Zephyr 可靠地流式传输较大规模数据的能力，又能在合理的时间内完成下载。在下载文件的同时会计算其哈希值（源代码中使用 SHA-256），如果计算结果与源代码中指定的参考值不一致，则会打印错误消息。短暂暂停后，该过程会在无限循环中重复执行，同时持续累加已接收的总字节数计数器。因此，该应用程序可用于测试在更长时间内传输更大规模流量的稳定性。

你可以修改源代码，向互联网上的任何其他站点（或本地网络中的站点，此时无需配置 NAT/路由）发起请求。

.. warning::

   如果你要使用本示例进行大规模测试，请改用本地服务器或你在互联网上自行搭建的专用测试服务器上的文件。不建议使用 archive.ubuntu.com 上的文件进行大规模测试。

启用 TLS 支持
=================================

通过启用 ``overlay-tls.conf`` overlay 配置文件来构建项目，即可在本示例中启用 TLS 支持，例如使用以下命令：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/big_http_download
   :board: qemu_x86
   :conf: "prj.conf overlay-tls.conf"
   :goals: build
   :compact:

另一种方式是在运行 ``west build`` 或 ``cmake`` 时指定 ``-DEXTRA_CONF_FILE=overlay-tls.conf`` 。

本示例的 TLS 版本会从 https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/git/1:2.34.1-1ubuntu1/git_2.34.1.orig.tar.xz 下载文件（6.6MB）。示例所使用的证书位于示例的 ``src`` 目录下，用于访问示例中默认配置的 TLS 通信站点（ https://launchpad.net ）及可能的重定向站点。若要通过 TLS 访问其他网页，你需要提供相应的证书以对该服务器进行身份验证。

请注意，本示例中的 TLS 支持依赖于非 POSIX 的 TLS Socket 功能。因此，本示例中的 TLS 模式仅能在 Zephyr 上运行。

在 POSIX 主机上运行应用程序
========================================

同一份应用程序源代码也可以针对 POSIX 系统（例如 Linux）进行构建。

构建方法：

.. code-block:: console

    $ make -f Makefile.host

运行方法：

.. code-block:: console

    $ ./big_http_download

该应用程序的行为与 Zephyr 版本一致。
