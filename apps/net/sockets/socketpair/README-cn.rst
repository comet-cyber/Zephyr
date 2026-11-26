.. zephyr:code-sample:: sockets-socketpair
   :name: Socketpair
   :relevant-api: bsd_sockets

   使用 Socket 对（socketpair）实现线程间通信。

概述
********

Zephyr 的 sockets/socketpair 示例应用程序演示了一个多线程（Multi-threaded）应用程序如何通过成对的未命名、已连接的 UNIX 域 Socket 进行通信。正如你所料，这些成对的 Socket 是通过 socketpair(2) 创建的。此类 Socket 兼容 BSD Sockets API，因此本示例的另一目的在于表明：开发者完全可以编写出同时可移植于 POSIX 系统和 Zephyr 的 Socket 应用程序。

本示例应用程序的源代码位于：
:zephyr_file:`samples/net/sockets/socketpair` 。

环境要求
************

无

构建与运行
********************

按如下方式构建 Zephyr 版本的 sockets/echo 应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/socketpair
   :board: <board_to_use>
   :goals: build
   :compact:

示例启动后，会创建多个客户端线程。每个客户端线程向服务端（main）发送固定数量的消息。

.. code-block:: console

    *** Booting Zephyr OS build v3.3.0-rc1-97-g432ff20a72e1 ***
    setting-up
    Alpha: socketpair: 4 <=> 3
    Bravo: socketpair: 6 <=> 5
    Charlie: socketpair: 8 <=> 7
    main: read 'Alpha' on fd 4
    main: read 'Bravo' on fd 6
    main: read 'Charlie' on fd 8
    main: read 'Alpha' on fd 4
    main: read 'Bravo' on fd 6
    main: read 'Charlie' on fd 8
    main: read 'Alpha' on fd 4
    main: read 'Bravo' on fd 6
    main: read 'Charlie' on fd 8
    tearing-down
    SUCCESS

在 POSIX 宿主机上运行应用程序
========================================

同一份应用程序源代码也可以针对 POSIX 系统（例如 Linux）进行构建。

构建方法：

.. code-block:: console

    $ make -f Makefile.host

运行方法：

.. code-block:: console

    ./socketpair_example
    setting-up
    Alpha: socketpair: 3 <=> 4
    Bravo: socketpair: 5 <=> 6
    Charlie: socketpair: 7 <=> 8
    main: read 'Alpha' on fd 3
    main: read 'Bravo' on fd 5
    main: read 'Charlie' on fd 7
    main: read 'Alpha' on fd 3
    main: read 'Alpha' on fd 3
    main: read 'Bravo' on fd 5
    main: read 'Charlie' on fd 7
    main: read 'Bravo' on fd 5
    main: read 'Charlie' on fd 7
    tearing-down
    SUCCESS

由此可见，该应用程序的运行行为与 Zephyr 版本基本一致。
