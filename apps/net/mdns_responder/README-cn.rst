.. zephyr:code-sample:: mdns-responder
   :name: mDNS 响应器
   :relevant-api: net_core dns_sd bsd_sockets

   监听并响应 mDNS 查询。

概述
********

本应用程序将等待针对预定义主机名的 mDNS 查询并予以响应。默认主机名为 **zephyr** ，在 :file:`prj.conf` 文件中进行设置。

环境要求
**************

- :ref:`networking_with_host`

- avahi 或其他支持发起 mDNS 信息查询的类似应用程序。

构建与运行
********************

按如下方式构建并运行 mdns-responder 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/mdns_responder
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

mdns-responder 示例应用程序启动后，将等待来自网络的查询请求。

在主机上打开终端窗口并输入：

.. code-block:: console

    $ avahi-resolve -4 -n zephyr.local

如果查询成功，则会打印以下信息：

.. code-block:: console

    zephyr.local	192.0.2.1

若要执行 IPv6 查询，请输入：

.. code-block:: console

    $ avahi-resolve -6 -n zephyr.local

如果查询成功，则会打印以下信息：

.. code-block:: console

    zephyr.local	2001:db8::1

最后，使用 DNS 服务发现（DNS Service Discovery）解析服务：

.. code-block:: console

    $ avahi-browse -t -r _zephyr._tcp

如果查询成功，则会打印以下信息：

.. code-block:: console

    +   zeth IPv6 zephyr                                        _zephyr._tcp         local
    =   zeth IPv6 zephyr                                        _zephyr._tcp         local
       hostname = [zephyr.local]
       address = [192.0.2.1]
       port = [4242]
       txt = []

Wi-Fi
=====

可通过 :ref:`Wi-Fi 代码片段 <snippet-wifi-ipv4>` 在本示例中启用 IPv4 Wi-Fi 支持。
