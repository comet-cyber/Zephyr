.. zephyr:code-sample:: sys-heap
   :name: 系统堆（System heap）

   将系统堆（System heap）使用情况打印到控制台。

概述
********

这是一个简单的示例，可在任意 :ref:`受支持的开发板 <boards>` 上运行，并将系统堆的使用情况打印到控制台。

构建
********

可按如下方式针对 :zephyr:board:`native_sim <native_sim>` 构建本应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/sys_heap
   :host-os: unix
   :board: native_sim
   :goals: build
   :compact:

如需针对其他开发板进行构建，请将上方的 "native_sim" 替换为目标开发板的名称。

运行
*******

运行 build/zephyr/zephyr.exe

示例输出
*************

.. code-block:: console

   System heap sample

   allocated 0, free 196, max allocated 0, heap size 256
   allocated 156, free 36, max allocated 156, heap size 256
   allocated 100, free 92, max allocated 156, heap size 256
   allocated 0, free 196, max allocated 156, heap size 256
   1 static heap(s) allocated:
         0 - address 0x80552a8 allocated 12, free 180, max allocated 12, heap size 256
   2 heap(s) allocated (including static):
         0 - address 0x80552a8 allocated 12, free 180, max allocated 12, heap size 256
         1 - address 0x805530c allocated 0, free 196, max allocated 156, heap size 256
