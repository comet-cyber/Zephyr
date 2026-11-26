.. zephyr:code-sample:: net-rtp
   :name: RTP
   :relevant-api: rtp

   通过 UDP 组播发送或接收 RTP 音频流。

概述
********

本示例演示了如何使用 Zephyr RTP API 通过 UDP 组播 Socket 发送和接收音频流。设备角色在构建时通过附加配置文件进行选择：发送端使用 ``source.conf`` 配置文件，接收端使用 ``sink.conf`` 配置文件。两个角色共用 ``5004`` 端口上的 ``239.0.1.1`` 组播地址。添加 ``ipv6.conf`` 附加配置文件可将会话切换为同一端口上的 ``ff02::5004`` IPv6 组播地址。

**source** 角色（发送端）使用 Payload 类型 97 将 100 Hz 正弦波（16 位单声道，8000 采样/秒）作为 RTP 数据包发送。数据包每 50 ms 发送一次，每个数据包携带 400 个采样点（该音调的五个完整周期）。

**sink** 角色（接收端）加入组播组，并使用基于回调的 API 接收音频流。它会每 5 秒记录一次包含已接收数据包数量的心跳日志，若在 500 ms 内未收到任何数据包则记录一条警告日志。

环境要求
************

- :ref:`networking_with_host`

在 native_sim 上运行
************************

若要在 :zephyr:board:`native_sim` 开发板上运行本示例，请先按照 :ref:`networking_with_host` 的说明在主机上配置 ``zeth`` TAP 接口。

配合 FFmpeg 进行测试时，Linux 内核需要为该组播地址配置显式路由，以便通过 ``zeth`` 接口而非默认网络接口投递数据包。在 ``zeth`` 接口启动后，运行以下命令：

.. code-block:: console

   sudo ip route add 239.0.1.1 dev zeth

构建
********

构建为发送端（source / transmitter）：

.. zephyr-app-commands::
   :zephyr-app: samples/net/rtp
   :board: <board to use>
   :goals: build
   :conf: source.conf
   :compact:

构建为接收端（sink / receiver）：

.. zephyr-app-commands::
   :zephyr-app: samples/net/rtp
   :board: <board to use>
   :goals: build
   :conf: sink.conf
   :compact:

使用 net_pkt 加速 RTP 协议栈
====================================

附加配置文件 ``net_pkt.conf`` 可调优网络数据包缓冲池以提高吞吐量，可与任一角色组合使用：

.. zephyr-app-commands::
   :zephyr-app: samples/net/rtp
   :board: <board to use>
   :goals: build run
   :conf: "source.conf net_pkt.conf"
   :compact:

.. zephyr-app-commands::
   :zephyr-app: samples/net/rtp
   :board: <board to use>
   :goals: build run
   :conf: "sink.conf net_pkt.conf"
   :compact:

启用 IPv6 构建
====================

附加配置文件 ``ipv6.conf`` 可将 RTP 会话切换至 ``ff02::5004`` IPv6 组播地址，可与任一角色以及 ``net_pkt.conf`` 组合使用：

.. zephyr-app-commands::
   :zephyr-app: samples/net/rtp
   :board: <board to use>
   :goals: build run
   :conf: "source.conf ipv6.conf"
   :compact:

.. zephyr-app-commands::
   :zephyr-app: samples/net/rtp
   :board: <board to use>
   :goals: build run
   :conf: "sink.conf ipv6.conf"
   :compact:

使用 FFmpeg 测试
======================

本示例可在任意一端配合 `FFmpeg <https://ffmpeg.org>`_ 进行测试。

测试发送端（Source）
----------------------------

若要使用 FFmpeg 接收来自 **source** 角色的音频流，请先创建描述该 RTP 会话的 :file:`stream.sdp` 文件：

.. code-block:: none

   v=0
   o=- 0 0 IN IP4 127.0.0.1
   s=No Name
   c=IN IP4 239.0.1.1
   t=0 0
   a=tool:libavformat 58.76.100
   m=audio 5004 RTP/AVP 97
   a=rtpmap:97 L16/8000/1

随后运行 FFmpeg 接收音频流并将其保存为 WAV 文件：

.. code-block:: console

   ffmpeg -protocol_whitelist file,udp,rtp -i stream.sdp \
          -acodec pcm_s16le -ar 8000 -ac 1 \
          -f wav out.wav

测试接收端（Sink）
--------------------------

若要通过 FFmpeg 向 **sink** 角色提供输入音频流，请运行以下命令通过 RTP 组播发送 8 kHz 静音单声道流：

.. code-block:: console

   ffmpeg -re -f lavfi -i anullsrc=r=8000:cl=mono \
          -acodec pcm_s16le \
          -f rtp -rtp_flags latm \
          -pkt_size 1440 \
          rtp://239.0.1.1:5004

示例输出
*************

发送端（Source）
======================

.. code-block:: console

   *** Booting Zephyr OS build v4.4.0-3146-g5ef8f883a77f ***
   [00:00:00.000,000] <inf> net_config: Initializing network
   [00:00:00.000,000] <inf> net_config: IPv4 address: 192.0.2.102
   [00:00:00.000,000] <inf> main: RTP source on native_sim
   [00:00:00.000,000] <dbg> rtp.rtp_session_start_tx: (0x428e60): my_rtp_session started transmitter to 239.0.1.1:5004
   [00:00:00.000,000] <inf> main: Start sending RTP packets

接收端（Sink）
====================

.. code-block:: console

   *** Booting Zephyr OS build v4.4.0-3146-g5ef8f883a77f ***
   [00:00:00.000,000] <inf> net_config: Initializing network
   [00:00:00.000,000] <inf> net_config: IPv4 address: 192.0.2.101
   [00:00:00.000,000] <inf> main: RTP sink on native_sim
   [00:00:00.000,000] <dbg> rtp.rtp_session_start_rx: (0x420fc0): my_rtp_session started receiver on 239.0.1.1:5004

当发送端同时运行时，接收端会输出：

.. code-block:: console

   [00:00:00.120,000] <inf> main: Receiving rtp stream
   [00:00:05.120,000] <inf> main: Received 100 packets
   [00:00:10.120,000] <inf> main: Received 200 packets
   ...

如果发送端停止发送，接收端会在 500 ms 后记录超时警告：

.. code-block:: console

   [00:00:10.620,000] <wrn> main: Timeout occurred
