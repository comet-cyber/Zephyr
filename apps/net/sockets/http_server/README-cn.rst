.. zephyr:code-sample:: sockets-http-server
   :name: HTTP 服务器
   :relevant-api: http_service http_server tls_credentials json

   实现一个演示多种资源类型的 HTTP(S) 服务器。

概述
--------

本示例应用程序演示了 :ref:`http_server_interface` 库的使用方法。
该库提供了高层级函数，用于简化和抽象服务器的实现。
该服务器支持 HTTP/1.1 协议，既可以从 HTTP/1.1 升级到 HTTP/2，也支持无需升级的原生 HTTP/2 协议。
如果启用了 :kconfig:option:`CONFIG_QUIC` 配置选项，该服务器还将支持 HTTP/3 协议。默认情况下，
HTTP/1.1 会话可以升级到 HTTP/3，也可以无需升级直接使用原生 HTTP/3。
通过 ``net http services`` 网络 Shell 命令，可以查看每个已配置的 HTTP 服务所支持的 HTTP 协议。

环境要求
------------

`QEMU 网络配置 <https://docs.zephyrproject.org/latest/connectivity/networking/qemu_setup.html#networking-with-qemu>`_

构建与运行服务器
-------------------------------

:zephyr_file:`samples/net/sockets/http_server` 目录下包含适用于不同场景的配置文件：

.. list-table::

    * - :zephyr_file:`prj.conf <samples/net/sockets/http_server/prj.conf>`
      - 标准默认配置文件。

    * - :zephyr_file:`ieee802154-overlay.conf <samples/net/sockets/http_server/ieee802154-overlay.conf>`
      - 可叠加此 overlay 配置以添加 IEEE 802.15.4 支持。

    * - :zephyr_file:`overlay-usbd.conf <samples/net/sockets/http_server/overlay-usbd.conf>`
      - 可叠加此 overlay 配置以通过 USB 网络进行连接。

    * - :zephyr_file:`overlay-tls.conf <samples/net/sockets/http_server/overlay-tls.conf>`
      - 可叠加此 overlay 配置以构建 HTTPS 版本。

    * - :zephyr_file:`overlay-dhcpv4.conf <samples/net/sockets/http_server/overlay-dhcpv4.conf>`
      - 此 overlay 配置用于启用 DHCPv4 客户端功能。

构建并运行 HTTP 服务器应用程序：

.. code-block:: bash

   $ west build -p auto -b <board_to_use> -t run samples/net/sockets/http_server

对于 HTTPS 版本：

.. code-block:: bash

   $ west build -p auto -b <board_to_use> -t run --test samples/net/sockets/http_server/sample.net.sockets.https.server

服务器启动后，我们可以从宿主机使用 HTTP/1.1 或 HTTP/2 协议向服务器发起请求。

**使用 HTTP/1.1：**

- 使用浏览器： ``http://192.0.2.1/``
- 使用 curl： ``curl -v --compressed http://192.0.2.1/``
- 使用 ab（Apache Bench）： ``ab -n10 http://192.0.2.1/``

**使用 HTTP/2：**

- 使用 nghttp 客户端： ``nghttp -v --no-dep http://192.0.2.1/``
- 使用 curl： ``curl --http2 -v --compressed http://192.0.2.1/``
- 使用 h2load： ``h2load -n10 http://192.0.2.1/``

Web 浏览器对 HTTP/2 协议采用了更严格的安全策略。因此，若要在 Web 浏览器中使用 HTTP/2，
必须在上述 HTTPS 构建的基础上启用 ALPN（在 west build 命令中添加
``-DCONFIG_NET_SAMPLE_HTTPS_USE_ALPN`` ）。
此外，服务器证书必须由浏览器信任的 CA 证书签发。

最佳做法是生成你自己的 CA 证书：

.. code-block:: bash

   $ west build -b <board_to_use> -t sample_ca_cert samples/net/sockets/http_server

生成由该 CA 证书签发的服务器证书：

.. code-block:: bash

   $ west build -t sample_server_cert samples/net/sockets/http_server

随后使用新生成的服务器证书和私钥构建应用程序：

.. code-block:: bash

   $ west build samples/net/sockets/http_server

需要将 CA 证书添加到浏览器的受信任证书颁发机构列表中，才能启用 HTTP/2。如果使用 Firefox，
可能还需要将 ``network.http.http2.enforce-tls-profile`` 设置修改为 false，因为在 Firefox 中，
使用未知颁发机构签发的 CA 证书在启用 HTTP/2 时似乎会被视为安全错误。

服务器自定义配置
------------------------

本服务器示例包含多个可根据需求自定义的参数。可配置参数如下：

- ``CONFIG_NET_SAMPLE_HTTP_SERVER_SERVICE_PORT`` ：配置服务端口。

- ``CONFIG_HTTP_SERVER_MAX_CLIENTS`` ：定义服务器可同时处理的 HTTP/2 客户端最大数量。

- ``CONFIG_HTTP_SERVER_MAX_STREAMS`` ：指定每个客户端可建立的 HTTP/2 流（Stream）最大数量。

- ``CONFIG_HTTP_SERVER_CLIENT_BUFFER_SIZE`` ：定义为每个客户端分配的缓冲区大小。该值限制了所支持的单个 HTTP 请求头的最大长度。

- ``CONFIG_HTTP_SERVER_MAX_URL_LENGTH`` ：指定服务器可处理的 HTTP URL 最大长度。

- ``CONFIG_NET_SAMPLE_WEBSOCKET_SERVICE`` ：启用 WebSocket 服务端点。启用后允许 WebSocket 客户端连接到 ``/`` 端点，客户端发送的所有数据都会被原样回显（Echo）。

若要自定义这些选项，可以运行 ``west build -t menuconfig`` 打开交互式配置界面，然后从顶层菜单依次进入： ``-> Subsystems and OS Services -> Networking -> Network Protocols`` 。

WebSocket 连接测试
----------------------

你可以使用如下简单的 WebSocket 客户端应用程序来测试 WebSocket 连接。

.. code-block:: python

   import websocket

   websocket.enableTrace(True)
   ws = websocket.WebSocket()
   ws.connect("ws://192.0.2.1/ws_echo")
   ws.send("Hello, Server")
   print(ws.recv())
   while True:
     line = input("> ")
     if line == "quit":
       break
     ws.send(line)
     print(ws.recv())
   ws.close()


通过 USB 进行测试
------------------------

下面通过一个真实示例，演示如何使用 USB 连接将真实设备连接到 Linux 宿主机 PC 来测试 HTTP(S) 服务器。
这里我们以 NRF52840 开发板为例。

首先构建启用了 HTTPS 服务的示例并烧录到开发板：

.. zephyr-app-commands::
         :zephyr-app: samples/net/sockets/http_server/
         :board: nrf52840dk/nrf52840
         :goals: build
         :gen-args: -DCONFIG_NET_SAMPLE_HTTPS_SERVICE=y -DEXTRA_CONF_FILE=overlay-netusb.conf

然后将 USB 数据线连接到宿主机 PC 并执行：

.. code-block:: bash

   $ ip link show

以获取 Linux 分配给 USB 以太网接口的设备名称。在下文中，我们假设该名称为 ``eth-device`` 。

现在需要为该接口配置 IP 地址和路由：

.. code-block:: bash

   $ sudo ip addr add 192.0.2.2/24 dev eth-device
   $ sudo ip route add 192.0.2.0/24 dev eth-device

此处说明：

* 我们为该接口选择了一个 IP 地址（即 ``192.0.2.2/24`` ），它与服务器的 IP 地址（即
  :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR` ）不同，但处于 ``/24`` 子网掩码所定义的有效 IP 网段内。
* 我们假设 192.168.0.x 网段不会与宿主系统中的其他地址和路由发生冲突。如果发生冲突，则需要统一修改所有相关 IP 地址（包括示例配置、宿主机 IP 接口以及证书）。

完成上述配置后，即可使用 ``curl`` 测试 HTTP 和 HTTPS：

.. code-block:: bash

   $ curl -v --compressed http://192.0.2.1
   $ curl -v --compressed https://192.0.2.1

.. note::

   为确保 HTTPS 连接成功，请更新宿主机 Linux 系统的 CA 证书列表，将
   :zephyr_file:`samples/net/sockets/http_server/src/certs/ca_cert.pem` 添加到已知 CA 列表中。

性能分析
--------------------

CPU 使用率分析
********************

我们可以使用 ``perf`` 的 ``stat`` 命令来收集运行在 native_sim 开发板上的服务器的 CPU 使用率统计信息：

.. code-block:: console

   $ sudo perf stat -p <pid_of_server>

``perf stat`` 随后将开始监控服务器。我们可以在向服务器发送请求的同时让其持续运行。收集到足够的数据后，停止 ``perf stat`` ，它将打印性能统计摘要。

热点分析
****************

可以结合使用 ``perf record`` 和 ``perf report`` 来定位代码中消耗 CPU 时间最多的函数：

.. code-block:: console

   $ sudo perf record -g -p <pid_of_server> -o perf.data

在服务器高负载运行一段时间后（例如使用 ApacheBench 工具施压），停止录制并使用以下命令分析数据：

.. code-block:: console

   $ sudo perf report -i perf.data

生成包含性能分析数据的 ``perf.data`` 文件后，我们可以使用 ``FlameGraph`` （火焰图）工具对其进行可视化。这对于识别开销最大的代码路径以及排查应用程序耗时最多的位置非常有用。

为此，我们需要先将 ``perf.data`` 转换为 ``FlameGraph`` 可识别的格式：

.. code-block:: console

   $ sudo perf script | ~/FlameGraph/stackcollapse-perf.pl > out.perf-folded

然后生成 ``FlameGraph`` ：

.. code-block:: console

   $ ~/FlameGraph/flamegraph.pl out.perf-folded > flamegraph.svg

最后可以使用 Web 浏览器查看 flamegraph.svg。
