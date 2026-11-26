.. zephyr:code-sample:: servo-motor
   :name: 舵机（Servomotor）
   :relevant-api: pwm_interface

   使用 PWM API 驱动舵机（伺服电机）。

概述
********

本示例应用程序演示如何使用 :ref:`PWM API <pwm_api>` 驱动舵机（Servomotor）。

该示例通过 PWM 控制信号驱动舵机在 180 度范围内往复旋转。

本应用程序针对型号为 ROB-09065 的舵机设计，其 0 到 180 度角度范围对应的 PWM 脉冲宽度分别为 700 到 2300 微秒。不同型号的舵机可能需要不同的 PWM 脉冲宽度，如果你使用的是其他舵机，可能需要相应修改源代码。

环境要求
************

本示例需要将舵机的信号引脚连接到支持 PWM 输出的引脚上。必须在 Devicetree 中使用 ``pwm-servo`` 兼容属性（compatible，由本示例定义）定义该舵机节点，并将其节点标签（node label）设置为 ``servo`` 。配置示例如下：

.. code-block:: devicetree

   / {
       servo: servo {
           compatible = "pwm-servo";
           pwms = <&pwm0 1 PWM_MSEC(20) PWM_POLARITY_NORMAL>;
           min-pulse = <PWM_USEC(700)>;
           max-pulse = <PWM_USEC(2500)>;
       };
   };

请注意，常用的周期值为 20 ms。具体示例可参考 :zephyr_file:`samples/basic/servo_motor/boards/bbc_microbit.overlay` 。

接线说明
************

BBC micro:bit
=============

你需要将舵机的红线连接到外部 5V 电源，黑线接地（GND），白线连接到 SCL 引脚（即金手指边缘连接器上的 P19 引脚）。

构建与运行
********************

本示例提供了适用于 :zephyr:board:`bbc_microbit` 的 Devicetree overlay 文件。

本示例可针对多种开发板进行构建，此处我们以 bbc_microbit 开发板为例进行构建：

.. zephyr-app-commands::
   :zephyr-app: samples/basic/servo_motor
   :board: bbc_microbit
   :goals: build flash
   :compact:
