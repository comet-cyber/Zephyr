.. zephyr:code-sample:: wifi-ble-provisioning
   :name: 基于 BLE 的 Wi-Fi 配网 (Wi-Fi provisioning over BLE)
   :relevant-api: bluetooth wifi_mgmt wifi_credentials

   通过 BLE GATT 服务接收 Wi-Fi 凭据并连接至 AP。

概述
********

首次启动时，设备会广播一个自定义 GATT 服务，允许 BLE 中心设备（Central）写入 Wi-Fi SSID 和预共享密钥（PSK）。收到控制命令后，设备会通过 :ref:`lib_wifi_credentials` 库保存凭据，并使用 :c:macro:`NET_REQUEST_WIFI_CONNECT_STORED` 加入 Wi-Fi 网络。在后续启动时，设备会自动使用已保存的凭据重新连接。

状态机
=============

.. code-block:: none

   IDLE --(SSID + PSK + CONNECT)--> CONNECTING --> CONNECTED
                                         \
                                          --> FAILED

控制命令 ``ERASE`` 会清除已保存的凭据并返回到 ``IDLE`` 状态。

GATT 服务
=============

所有特征（Characteristic）共享同一个自定义 128 位基础 UUID ``8b84xxxx-f6fa-4e33-9a0c-e14d9f35f201`` ，其中短标识符替换 ``xxxx`` 部分：

.. list-table::
   :header-rows: 1

   * - 特征 (Char)
     - UUID
     - 属性 (Properties)
     - Payload
   * - SSID
     - 0002
     - write
     - UTF-8，最长 32 字节
   * - Password
     - 0003
     - write
     - UTF-8，最长 64 字节
   * - Security
     - 0004
     - write
     - 1 字节（可选，见下表）
   * - Control
     - 0005
     - write
     - 1 字节：0x01 = CONNECT，0x02 = ERASE
   * - Status
     - 0006
     - read, notify
     - 1 字节枚举值（见 ``gatt_svc.h`` ）

安全类型取值与 :c:enum:`wifi_security_type` 一致：

.. list-table::
   :header-rows: 1

   * - 字节值
     - 含义
   * - 0
     - 开放网络（Open，无密码）
   * - 1
     - WPA2-PSK
   * - 2
     - WPA2-PSK-SHA256
   * - 3
     - WPA3-SAE
   * - 6
     - WPA-Auto-Personal（WPA2/WPA3 过渡模式）
   * - 0xFF
     - 自动检测：若 PSK 为空则为开放网络，否则为 WPA2-PSK（默认）

如果未写入 Security 特征，设备将回退使用 ``0xFF`` （自动检测）。

环境要求
**************

一块同时支持 Wi-Fi 和 Bluetooth LE（BLE）的开发板。

构建与运行
********************

.. zephyr-app-commands::
   :zephyr-app: samples/net/wifi/ble_provisioning
   :board: esp32c6_devkitc/esp32c6/hpcore
   :goals: build flash
   :compact:

烧录完成后，设备开始以 ``Zephyr Wi-Fi Provisioning`` 名称进行广播（可通过 :kconfig:option:`CONFIG_BT_DEVICE_NAME` 配置）。

使用 nRF Connect Mobile 进行测试
========================================

#. 在 Android 或 iOS 设备上安装 `nRF Connect for Mobile`_ 。
#. 打开应用，点击 **Scan** ，并连接到广播中的设备。
#. 展开自定义服务（基础 UUID 为 ``8b840001-f6fa-4e33-9a0c-e14d9f35f201`` ）。
#. 将 UTF-8 字节格式的 SSID 写入 ``0002`` 特征。
#. 将密码写入 ``0003`` 特征。
#. （可选）将安全类型字节写入 ``0004`` 特征。
#. （可选）开启 Status ``0006`` 特征的通知（Notification）。
#. 向 Control ``0005`` 特征写入 ``0x01`` 以请求连接 Wi-Fi。
#. 观察串口控制台以及依次经历 ``CONNECTING`` (2) 和 ``CONNECTED`` (3) 的 Status 通知变化。

若要擦除已保存的凭据，请向 Control 特征写入 ``0x02`` 。

.. _nRF Connect for Mobile:
   https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile

安全性
************

可通过 Kconfig 选项选择三种 BLE 安全模式：

**无安全保护 (None)** （ :kconfig:option:`CONFIG_WIFI_BLE_PROV_SECURITY_NONE` ，默认）
   不进行配对。凭据以明文形式传输。仅供评估测试使用。

**加密链路 (Encrypted link)** （ :kconfig:option:`CONFIG_WIFI_BLE_PROV_SECURITY_ENCRYPT` ）
   写入操作需要建立加密链路。配对过程无需用户交互；被动窃听者无法还原凭据。

**认证配对 (Authenticated pairing)** （ :kconfig:option:`CONFIG_WIFI_BLE_PROV_SECURITY_AUTH` ）
   写入操作需要经过认证的 LESC 加密配对。设备会在控制台打印一个 6 位数字配对码（passkey），中心设备必须输入该配对码。

已保存的凭据在 NVS 中仍以明文形式存储。如需对静态存储的凭据进行保护，请将后端切换为 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_PSA` 或使用厂商提供的 NVS 加密功能。

.. note::

   切换安全模式时会复用同一个 NVS 分区。上一次构建遗留的 BLE 绑定信息可能会在启动时打印 ``set-value failure`` 警告；切换安全模式时请先擦除 Flash（ ``west flash --erase`` ）。

示例 Kconfig 选项
******************************

* :kconfig:option:`CONFIG_BT_DEVICE_NAME` -- 广播设备名称。
* :kconfig:option:`CONFIG_WIFI_BLE_PROV_KEEP_BLE_AFTER_CONNECT` --
  Wi-Fi 连接成功后继续保持 BLE 广播。
* :kconfig:option:`CONFIG_WIFI_BLE_PROV_SECURITY_NONE` /
  :kconfig:option:`CONFIG_WIFI_BLE_PROV_SECURITY_ENCRYPT` /
  :kconfig:option:`CONFIG_WIFI_BLE_PROV_SECURITY_AUTH` --
  配网写入操作的 BLE 安全模式。

示例输出
**************

.. code-block:: console

   *** Booting Zephyr OS build v4.4.0 ***
   <inf> wifi_ble_prov: Wi-Fi BLE provisioning starting
   <inf> wifi_ble_prov: security: none (plaintext)
   <inf> gatt_svc: status -> 0
   <inf> wifi_ble_prov: no stored credentials; waiting for provisioning over BLE
   <inf> gatt_svc: advertising as 'Zephyr Wi-Fi Provisioning'
   <inf> wifi_ble_prov: connected: R:4F:0D:14:E8:76:98
   <inf> wifi_prov: connecting using stored credentials
   <inf> gatt_svc: status -> 2
   <inf> wifi_prov: Wi-Fi connected
   <inf> gatt_svc: status -> 3
