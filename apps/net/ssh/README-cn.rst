.. zephyr:code-sample:: ssh-server-client
   :name: SSH 服务器与客户端

   实现 SSH 服务器与客户端的 Shell 支持。

概述
********

Zephyr 的 SSH 示例应用程序启用了 SSH 服务器和客户端功能。可以使用网络 Shell 监听传入的 SSH 连接，或使用 SSH 连接到外部主机。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/ssh` 。

环境要求
************

- :ref:`networking_with_host`

构建
********

按如下方式构建 SSH 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/ssh
   :board: <board to use>
   :conf: <config file to use>
   :goals: build
   :compact:

使用你常用的终端模拟器连接到 Zephyr UART Shell（将 ``/dev/pts/12`` 替换为上面 Zephyr 实际打印的路径，例如 ``uart connected to pseudotty: /dev/pts/12`` ）：

.. code-block:: console

   python -m serial.tools.miniterm /dev/pts/12 --raw --eol CRLF

生成密钥
***************

首次运行时，你可以在网络 Shell 中生成并保存主机密钥（host key），本示例中主机密钥索引设为 0。

.. code-block:: console

   net ssh_key gen 0 rsa 2048
   net ssh_key save 0 priv id_rsa

在后续运行时，你可以直接加载该主机密钥。

.. code-block:: console

   net ssh_key load 0 priv id_rsa


SSH 服务器
***************

启动 SSH 服务器（服务器实例 0，主机密钥索引 0）

.. code-block:: console

   net sshd start -i 0 -b 192.0.2.1 -k 0 -p password123

如果省略 ``-b`` 选项或绑定到 ``0.0.0.0`` ，服务器将监听所有地址。绑定本地地址时也可以使用 IPv6 地址。

在宿主机 Shell 中：

.. code-block:: console

   ssh root@192.0.2.1

若要退出，请依次按下 'Enter'、'~' 和 '.'（即回车后输入波浪号加英文句号）。


SSH 客户端
***************

从 Zephyr SSH 客户端（客户端实例 0）连接到你的宿主机。
将 <username> 替换为目标宿主机用户名。

.. code-block:: console

   net ssh start username@192.0.2.2

按下 ``Ctrl+d`` 或输入 ``exit`` 即可退出并返回 Zephyr。

指定目标地址时，也可以使用 IPv6 地址或主机名。

.. code-block:: console

   net ssh start username@2001:db8::2
   net ssh start username@[2001:db8::2]:22
   net ssh start username@example.com
   net ssh start username@example.com:22


客户端公钥认证
======================

导出公钥（主机密钥索引 0）

.. code-block:: console

   net ssh_key pub export 0

在宿主机 Shell 中：

将导出的密钥转换为 RFC4716 格式并添加到 authorized_keys

.. code-block:: console

   ssh-keygen -i -f /dev/stdin -m pkcs8 <<< \
   '-----BEGIN PUBLIC KEY-----
   <your base-64 encoded host key>
   ------END PUBLIC KEY-----' \
   >> ~/.ssh/authorized_keys

附带主机密钥参数重启 SSH 客户端，无需输入密码！
（客户端实例 0，主机密钥索引 0）

.. code-block:: console

   net ssh stop
   net ssh start -k 0 username@192.0.2.2


服务器公钥认证
======================

在宿主机 Shell 中将宿主机公钥转换为 PEM 格式：

.. code-block:: console

   ssh-keygen -e -f ~/.ssh/id_rsa.pub -m PKCS8

在 Zephyr Shell 中将公钥导入到密钥索引 1（索引 0 已保留给前面生成的服务器主机密钥）

.. code-block:: console

   net ssh_key pub import 1

粘贴上面输出的公钥内容，然后按下 Ctrl+C。
接着保存该公钥（密钥索引 1）

.. code-block:: console

   net ssh_key save 1 pub authorized_key_0

在后续运行时，你可以直接加载该公钥

.. code-block:: console

   net ssh_key load 1 pub authorized_key_0

以无密码（禁用密码认证）并指定授权密钥参数的方式重启 SSH 服务器
（服务器实例 0，主机密钥索引 0，授权密钥索引 1）

.. code-block:: console

   net sshd stop -i 0
   net sshd start -i 0 -b 192.0.2.1:22 -k 0 -a 1

在宿主机 Shell 中连接到 Zephyr SSH 服务器，无需输入密码。

.. code-block:: console

   ssh -i ~/.ssh/id_rsa root@192.0.2.1

若要退出，请依次按下 'Enter'、'~' 和 '.'（即回车后输入波浪号加英文句号）。


创建 SSH 通道
*********************

除了内置的 ``net ssh`` 和 ``net sshd`` Shell 命令外，本示例还注册了一组精简的 ``sample`` 命令集，用于演示应用程序如何在现有客户端连接之上创建和移除 SSH 通道（Channel）。
连接管理本身仍交由上文介绍的 SSH 客户端 Shell 命令处理。

首先建立客户端连接，完成认证并打开一个交互式会话通道：

.. code-block:: console

   net ssh start username@192.0.2.2

按下 ``Ctrl+d`` 或输入 ``exit`` 返回 Zephyr Shell，同时保持连接处于打开状态。随后在该连接上创建一个附加通道：

.. code-block:: console

   sample open

可通过以下命令列出已打开的通道以及活动的服务器与客户端连接：

.. code-block:: console

   sample info

最后，按通道编号（由 ``sample info`` 显示）移除通道：

.. code-block:: console

   sample close 1

``sample`` 命令依赖于 SSH 传输层回调：本示例注册了服务器和客户端传输层回调来跟踪连接，并使用 :c:func:`ssh_transport_channel_open` 和 :c:func:`ssh_channel_close` 来创建和移除通道。
