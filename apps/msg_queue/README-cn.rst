.. zephyr:code-sample:: msg_queue
   :name: 消息队列 (Message Queue)
   :relevant-api: msgq_apis

   实现一对基础的消息队列（Message Queue）生产者/消费者线程（Thread）。

概述
********

本示例演示 Zephyr 消息队列的基本用法。一个生产者线程同时发送普通消息和紧急消息，供消费者线程读取。

构建与运行
********************

可按如下方式在 QEMU 上构建并运行本应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/kernel/msg_queue
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

若要针对其他目标开发板进行构建，请将上方的 "qemu_x86" 替换为对应的板卡名称。

示例输出
==============

每条普通消息都会被放入队列尾部，并按 FIFO（先进先出）顺序投递。每条“紧急”（urgent）消息都会被放入队列头部，只要在其之后没有新的“紧急”消息到达，它就会被最先投递。

在本示例中，一个生产者线程每发送 2 条普通消息就会发送 1 条紧急消息。请注意，消息 C 会被最先取出，因为它是最后一条作为“紧急”消息发送的消息。

.. code-block:: console

   [producer] sending: 0
   [producer] sending: 1
   [producer] sending: A (urgent)
   [producer] sending: 2
   [producer] sending: 3
   [producer] sending: B (urgent)
   [producer] sending: 4
   [producer] sending: 5
   [producer] sending: C (urgent)
   [consumer] got sequence: CBA012345

按下 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。
