.. zephyr:code-sample:: synchronization
   :name: 基础同步机制
   :relevant-api: thread_apis semaphore_apis

   操作基本的内核同步原语。

概述
********

这是一个用于演示内核基本运行正常性的简单应用程序。两个线程（Thread A 和 B）轮流向控制台打印问候消息，并使用休眠请求和信号量（Semaphore）来控制消息生成的速率。这表明内核的调度、通信和定时功能均正常工作。

构建与运行
********************

本工程向控制台输出信息，可按如下方式在 QEMU 上构建并运行：

.. zephyr-app-commands::
   :zephyr-app: samples/synchronization
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

示例输出
=============

.. code-block:: console

   thread_a: Hello World from cpu 0 on qemu_x86!
   thread_b: Hello World from cpu 0 on qemu_x86!
   thread_a: Hello World from cpu 0 on qemu_x86!
   thread_b: Hello World from cpu 0 on qemu_x86!
   thread_a: Hello World from cpu 0 on qemu_x86!
   thread_b: Hello World from cpu 0 on qemu_x86!
   thread_a: Hello World from cpu 0 on qemu_x86!
   thread_b: Hello World from cpu 0 on qemu_x86!
   thread_a: Hello World from cpu 0 on qemu_x86!
   thread_b: Hello World from cpu 0 on qemu_x86!

   <repeats endlessly>

按下 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。
