# THEORY

更新日期：2026-10-13

## 系统边界与完整路径

```text
RA8P1 应用消息
 → socket（目的地址为 Ubuntu 隧道 IP）
 → Zephyr IP 路由/虚拟网口
 → WireGuard peer 与加密封装
 → 外层 UDP（目的为 Ubuntu 物理 IP:监听端口）
 → Zephyr 物理以太网驱动 → PHY → 网线
 → Ubuntu 物理网卡 → UDP → Linux WireGuard 解密
 → Ubuntu 隧道 IP → 回显 socket/应用
```

返回走反向路径。两层 IP 必须分开：endpoint 是实际可达的物理 IP；隧道 IP 标识加密网络里的节点。AllowedIPs 参与 peer 对应及接收源地址限制，不能代替物理连通与正确路由。不要让外层 endpoint 的路由进入隧道自身。

## 路径 1：设备初始化与普通网络

- 来源：复位、设备初始化及 PHY link 变化。
- 处理：设备树提供硬件描述，Kconfig 选驱动/协议栈，驱动管理 DMA/描述符，net_if 表示网络接口，net_mgmt 发布事件。
- 时限：中断路径短；初始化/链路等待在线程中完成。事件回调的实际上下文需查实现，不能假定允许阻塞。
- 观察：设备就绪状态、串口日志、接口 link/address、ARP/ICMP 抓包。
- 当前学习：device API、net_if、事件、初始化顺序；不追全部寄存器。

## 路径 2：普通 UDP 与线程阻塞

- 来源：应用构造带序号消息，经 socket/sendto 发到 Ubuntu；recvfrom 等待返回。
- 所有权：应用持有自己的收发数组；网络栈内部管理 net_pkt/net_buf，不把 socket 数组和内部包缓存混为一谈。异步接口需另查生命周期。
- 时限：接收设超时，阻塞的是调用线程，其它可运行线程仍可调度；不能在 ISR 或会阻塞其它工作项的系统工作队列里长期等待网络。
- 观察：返回值/errno、收发计数、超时与抓包。
- 当前学习：socket、线程/优先级/栈、阻塞与唤醒；仅在真实并发需求出现时增加应用线程。

## 路径 3：WireGuard 控制与数据

- 来源：配置本端私钥、peer 公钥、endpoint、AllowedIPs、虚拟接口地址和路由，发送隧道流量触发握手/数据传输。
- 处理：应用用公开 API，WireGuard 内部拥有 peer、会话密钥和协议缓冲；虚拟接口把内层包变成外层 UDP，Linux 解密交给隧道应用。
- 时限：握手有重试、keepalive/密钥更新由延期工作维护，不是硬实时任务；加密与缓冲不足可能影响吞吐。
- 观察：Zephyr WireGuard 日志/统计、Ubuntu wg show 与双层抓包；握手成功不等于应用路由已经正确。
- 入口：include/zephyr/net/wireguard.h；samples/net/wireguard/src/wg.c；subsys/net/lib/wireguard/wg.c。

## 路径 4：延期工作、互斥与重启

- 本地 wg.c 使用 k_work_delayable、k_work_schedule/reschedule 维护周期任务，k_mutex_lock/unlock 保护共享 peer 状态。
- 应用先理解回调何时执行、延期不等于精确执行时刻、锁保护哪个状态；不照抄内部锁到所有应用函数。
- 互斥锁通常只在线程上下文使用；系统工作队列里长时间阻塞会拖延其它 work，需按实际调用链诊断。
- 本地 wireguard_get_current_time 默认取 k_uptime_get，开机时间重置后可能违反对端已记录的握手时间戳递增要求。首次连通后必须验证重启重新握手，必要时利用可信 RTC/时间同步或其它可审计的跨重启单调方案；不关闭防重放来绕过。
- 观察：重启前后握手、peer 计数、时间来源日志、恢复耗时；随机数来源也需实测，不用固定值替代密码学随机数。

## 原代码切入点

本地官方示例 samples/net/wireguard/src/wg.c 的配置入口：

```c
peer_config.keepalive_interval = keepalive_interval;
ret = wireguard_peer_add(&peer_config, &peer_iface);
if (ret < 0) {
    LOG_ERR("Cannot add peer (%d)", ret);
}
```

peer_config 是已填写的对端配置，peer_iface 是用于接收接口指针的变量；其返回值与接口生命周期按当前 wireguard.h 的契约学习。该片段省略了密钥、地址、路由等前置配置，不能独立建立隧道。

## 推迟项

完整调度器源码、全部同步原语、密码学推导、双核、TSN、NPU、Wi-Fi、MCUboot、网关转发、性能优化和生产密钥存储，等实际需求触发。每次讲代码贴关键原代码并解释，不只给地址。
