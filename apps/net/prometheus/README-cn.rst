.. zephyr:code-sample:: prometheus
   :name: Prometheus 示例
   :relevant-api: http_service http_server tls_credentials prometheus

   实现一个演示多种指标类型的 Prometheus 指标服务器。

概述
--------

本示例应用程序演示了 ``prometheus`` 库的使用方法。
该库提供了 Prometheus 客户端库（拉取模式，pull method）的实现。
通过将该库集成到代码中，你可以通过应用程序实例上的 HTTP 端点暴露内部指标，使 Prometheus 能够抓取（scrape）并收集这些指标。

环境要求
------------

`QEMU 网络配置 <https://docs.zephyrproject.org/latest/connectivity/networking/qemu_setup.html#networking-with-qemu>`_

构建与运行服务器
-------------------------------

构建并运行该应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/prometheus
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

服务器启动后，我们可以使用 HTTP/1.1 向服务器发送请求。

**使用 HTTP/1.1：**

- 使用浏览器访问： ``http://192.0.2.1/metrics``

请参阅 `Prometheus 客户端库文档
<https://prometheus.io/docs/instrumenting/clientlibs/>`_ 。

指标服务器自定义配置
------------------------------

本服务器示例包含多个可根据需求自定义的参数。可配置参数如下：

- ``CONFIG_NET_SAMPLE_HTTP_SERVER_SERVICE_PORT`` ：配置服务端口。

- ``CONFIG_HTTP_SERVER_MAX_CLIENTS`` ：定义服务器可同时处理的最大 HTTP/2
  客户端数量。

- ``CONFIG_HTTP_SERVER_MAX_STREAMS`` ：指定每个客户端可建立的最大 HTTP/2
  流（stream）数量。

- ``CONFIG_HTTP_SERVER_CLIENT_BUFFER_SIZE`` ：定义为每个客户端分配的缓冲区大小。
  该值限制了所支持的单个 HTTP 标头的最大长度。

- ``CONFIG_HTTP_SERVER_MAX_URL_LENGTH`` ：指定服务器可处理的 HTTP URL 最大长度。

如需自定义这些选项，可以运行 ``west build -t menuconfig`` 打开交互式配置界面，然后从顶层菜单依次进入： ``-> Subsystems and OS Services -> Networking -> Network Protocols`` 。


Prometheus 配置
------------------------

.. code-block:: yaml

    scrape_configs:
      - job_name: 'your_server_metrics'
        static_configs:
          - targets: ['your_server_ip:your_server_port']
        # Optional: Configure scrape interval
        # scrape_interval: 15s

请将 ``'your_server_metrics'`` 替换为描述该任务的名称，将 ``'your_server_ip'`` 替换为服务器的 IP 地址或主机名，并将 ``'your_server_port'`` 替换为服务器暴露 Prometheus 指标的端口号。

请确保根据服务器的实际环境与需求调整配置。

更新配置后，保存文件并重启 Prometheus 服务器。
重启完成后，Prometheus 将按照定义的抓取配置开始从你的服务器抓取指标。你可以通过检查 Prometheus 的 targets 页面，或在 Prometheus 中查询来自该服务器的指标，来验证服务器指标是否已被正常抓取。

请参阅 `Prometheus 配置文档
<https://prometheus.io/docs/prometheus/latest/configuration/configuration>`_ 。
