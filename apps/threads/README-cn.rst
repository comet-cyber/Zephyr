.. zephyr:code-sample:: multi-thread-blinky
   :name: 基本线程操作
   :relevant-api: gpio_interface thread_apis

   创建多个线程来闪烁 LED 并将信息打印到控制台。

概述
********

本示例演示了如何使用 :c:func:`K_THREAD_DEFINE` 创建多个线程（Thread）。示例共创建了三个线程，每个线程均在编译期通过 K_THREAD_DEFINE 进行定义。

前两个线程各自控制一个 LED。这两个 LED（ ``led0`` 和 ``led1`` ）的循环控制与定时逻辑由独立的函数分别控制：

- ``blink0()`` 控制 ``led0`` ，休眠周期为 100ms
- ``blink1()`` 控制 ``led1`` ，休眠周期为 1000ms

每当这两个线程中的任意一个翻转其控制的 LED 状态时，它还会将标识该线程/LED 以及翻转次数的信息推入 :ref:`FIFO <fifos_v2>` 中。

第三个线程使用 :c:func:`printk` 将添加到 FIFO 中的信息打印到设备控制台。

环境要求
************

开发板必须具有两个通过 GPIO 引脚连接的 LED。在许多 Zephyr :ref:`开发板 <boards>` 上，它们被称为“用户 LED（User LEDs）”。这些 LED 必须使用 ``led0`` 和 ``led1`` :ref:`Devicetree <dt-guide>` 别名进行配置，通常定义在 :ref:`BOARD.dts 文件 <devicetree-in-out-files>` 中。

如果尝试针对不受支持的开发板构建本示例，将会看到以下错误之一：

.. code-block:: none

   Unsupported board: led0 devicetree alias is not defined
   Unsupported board: led1 devicetree alias is not defined

构建
********

例如，针对 :ref:`96b_carbon_board` 构建本示例：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/threads
   :board: 96b_carbon/stm32f401xe
   :goals: build flash
   :compact:

对于其他受支持的开发板，请相应替换 ``96b_carbon/stm32f401xe`` 。
