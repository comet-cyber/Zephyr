.. zephyr:code-sample:: mcp-server-hello-world
   :name: MCP Server Hello World
   :relevant-api: mcp_server

   本代码示例展示了两个非常基础的工具定义，向用户介绍 Zephyr MCP Server 库。

概述
********

本示例定义了两个工具：一个是 LED 控制工具，允许 MCP 客户端打开、关闭或翻转板载 LED；另一个是延迟响应工具，用于触发延迟响应机制，向用户展示服务器在此类场景下的行为表现。

一旦服务器连接到网络并获取到 IP 地址，即可通过分配的 IP 地址或 mDNS 地址（例如通过 http://mcp-hello-world.local:8080/mcp ）进行访问。

环境要求
************

- 支持网络功能的开发板
- 连接了 ``led0`` 别名对应 LED 的开发板（可选，用于 LED 控制）

硬件接线
************

无特殊接线要求。

构建与运行
********************

按如下方式构建并烧录本示例：

.. zephyr-app-commands::
   :zephyr-app: samples/net/mcp/mcp_server_hello_world
   :board: <board_name>
   :goals: build flash
   :compact:

请将 ``<board_name>`` 替换为你的目标开发板。

测试
********

服务器运行后，会通过 HTTP 监听 MCP 客户端连接。你可以使用任意兼容 MCP 的客户端进行连接并调用已注册的工具。本示例默认配置为使用 DHCP 和 mDNS，因此可通过 URL ``http://mcp-hello-world.local:8080/mcp`` 访问该 MCP 服务器。

示例输出
*************

.. code-block:: console

   Initializing...
   LED initialized successfully
   Registering Tool #1: Delayed response tool...
   Tool #1 registered.
   Registering Tool #2: LED Control...
   Tool #2 registered.
   Starting...
   MCP Server running...

调用工具时，你将看到类似如下的输出：

.. code-block:: console

   Delayed response tool executed with arguments: {"message":"test"}, token: <uuid>
   LED control tool executed with arguments: {"action":"on"}, token: <uuid>

参考资料
************

- `Model Context Protocol 规范 <https://modelcontextprotocol.io/specification>`_
