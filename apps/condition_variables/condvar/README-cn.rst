.. zephyr:code-sample:: kernel-condvar
   :name: 条件变量
   :relevant-api: condvar_apis

   在多线程应用程序中操作条件变量。

概述
********

本示例演示了在多线程（Thread）应用程序中使用 :ref:`条件变量（Condition Variables） <condvar>` 的方法。条件变量通常与互斥锁（Mutex）配合使用，用于从一个线程向另一个线程通知状态（条件）的变化。线程使用条件变量来等待某个条件变为真。不同线程会根据向挂起在条件变量上的其他线程发送信号的时机，交替执行各自的入口函数。本示例可在任意 :ref:`受支持的开发板 <boards>` 上运行，并将如下所示的示例输出打印到控制台。

构建与运行
********************

可按如下方式在 :zephyr:board:`native_sim <native_sim>` 上构建并运行本应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/kernel/condition_variables/condvar
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:

若要针对其他开发板进行构建，请将上方的 ``native_sim`` 替换为目标开发板的名称。

示例输出
=============

.. code-block:: console

    Starting watch_count: thread 1
    watch_count: thread 1 Count= 0. Going into wait...
    inc_count: thread 2, count = 1, unlocking mutex
    inc_count: thread 3, count = 2, unlocking mutex
    inc_count: thread 2, count = 3, unlocking mutex
    inc_count: thread 3, count = 4, unlocking mutex
    inc_count: thread 2, count = 5, unlocking mutex
    inc_count: thread 3, count = 6, unlocking mutex
    inc_count: thread 2, count = 7, unlocking mutex
    inc_count: thread 3, count = 8, unlocking mutex
    inc_count: thread 2, count = 9, unlocking mutex
    inc_count: thread 3, count = 10, unlocking mutex
    inc_count: thread 2, count = 11, unlocking mutex
    inc_count: thread 3, count = 12  Threshold reached.Just sent signal.
    inc_count: thread 3, count = 12, unlocking mutex
    watch_count: thread 1 Condition signal received. Count= 12
    watch_count: thread 1 Updating the value of count...
    watch_count: thread 1 count now = 137.
    watch_count: thread 1 Unlocking mutex.
    inc_count: thread 2, count = 138, unlocking mutex
    inc_count: thread 3, count = 139, unlocking mutex
    inc_count: thread 2, count = 140, unlocking mutex
    inc_count: thread 3, count = 141, unlocking mutex
    inc_count: thread 2, count = 142, unlocking mutex
    inc_count: thread 3, count = 143, unlocking mutex
    inc_count: thread 2, count = 144, unlocking mutex
    inc_count: thread 3, count = 145, unlocking mutex
    Main(): Waited and joined with 3 threads. Final value of count = 145. Done.
