.. zephyr:code-sample:: cellular-modem
   :name: 蜂窝调制解调器

   使用蜂窝调制解调器与 UDP 服务器进行通信。

概述
********

本示例包含一个简单的应用程序：它会为调制解调器上电，启动网络接口，然后向端点 test-endpoint.com 发送一个包含伪随机数据的数据包；该端点是一台公开托管的服务器，运行着 server 目录下的 Python 脚本。程序使用 DNS 查询 test-endpoint.com 的 IP 地址。

说明
********

本示例使用 Devicetree 别名 ``modem`` 来指定所使用的调制解调器实例。同时，本示例假定调制解调器驱动创建了系统中唯一的 PPP 网络接口。

设置
********

首先在 Devicetree 中配置所需的设备树节点：

.. code-block:: devicetree

   /dts-v1/;

   / {
           aliases {
                   modem = &modem;
           };
   };

   &usart2 {
           pinctrl-0 = <&usart2_tx_pa2 &usart2_rx_pa3 &usart2_rts_pa1 &usart2_cts_pa0>;
           pinctrl-names = "default";
           current-speed = <115200>;
           hw-flow-control;
           status = "okay";

           modem: modem {
                   compatible = "quectel,bg9x";
                   mdm-power-gpios = <&gpioe 2 GPIO_ACTIVE_HIGH>;
                   mdm-reset-gpios = <&gpioe 3 GPIO_ACTIVE_HIGH>;
                   status = "okay";
           };
   };

接下来，必须通过 ``CONFIG_UART_INTERRUPT_DRIVEN=y`` 或 ``CONFIG_UART_ASYNC_API=y`` 指定所使用的 UART API。该驱动不支持 UART 轮询（Polling）模式。

最后，必须使用 ``CONFIG_MODEM_CELLULAR_APN=""`` 配置 APN。

Shell 命令
**************

本示例启用了 :kconfig:option:`CONFIG_MODEM_CELLULAR_SHELL` ，它会添加一个 ``modem_cellular`` Shell 命令，用于在运行时控制 cellular_modem 驱动的周期性会话脚本（chat script）：

.. code-block:: shell

   modem_cellular pause <device>
   modem_cellular resume <device>

在命令通道上执行耗时的 AT 操作（如固件更新、eSIM 配置、产线测试）期间，可使用 ``modem_cellular pause`` 暂停周期性的 CSQ/CREG 轮询。执行 ``modem_cellular resume`` 可重新启用轮询；如果在暂停期间跳过了原定的周期性执行，恢复后会立即触发下一次调用。在已暂停状态下再次暂停，或在未暂停状态下执行恢复，均会返回 ``-EINVAL`` 。

服务器设置
****************

将服务器部署在公网可访问的主机上，然后将 ``prj.conf`` 中的 :kconfig:option:`CONFIG_SAMPLE_CELLULAR_MODEM_ENDPOINT_HOSTNAME` 配置项设置为该服务器的主机名。

.. code-block:: shell

   git clone --depth=1 https://github.com/zephyrproject-rtos/zephyr.git
   cd zephyr/samples/net/cellular_modem/server
   python te.py
