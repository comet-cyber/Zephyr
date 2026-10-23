#include <string.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/net/socket.h>
#include <zephyr/net/net_if.h>
#include <zephyr/net/virtual.h>
#include <errno.h>

#define TARGET_ADDRESS "192.168.50.1"


/* 应用层查找结果：只保存接口指针，接口对象由 Zephyr 管理。 */
struct app_wg_lookup {
    struct net_if *iface;
};

/*
 * 应用内部回调：由 net_if_foreach() 对每个接口调用一次。
 * iface 是当前检查的接口；user_data 指向调用者提供的查找结果。
 * 当前单 peer 配置下，只记录第一个具有 VPN 能力的虚拟接口。
 */
static void app_wg_find_iface(struct net_if *iface, void *user_data)
{
    struct app_wg_lookup *result = user_data;

    if (result->iface != NULL) {
        return;
    }

    /* 先确认接口使用 Virtual L2，才能查询它的虚拟接口能力。 */
    if (net_if_l2(iface) != &NET_L2_GET_NAME(VIRTUAL)) {
        return;
    }

    /* 能力是位标志；按位与结果非零，表示支持 VPN。 */
    if (!(net_virtual_get_iface_capabilities(iface) &
          VIRTUAL_INTERFACE_VPN)) {
        return;
    }

    result->iface = iface;
}

/*
 * 应用初始化入口：供本文件的 main() 在创建业务 socket 前调用。
 * 当前仅完成 VPN 接口定位；后续继续在这里配置地址、密钥和 peer。
 * 返回 0 表示找到接口，-ENODEV 表示未找到。
 */
static int app_wireguard_init(void)
{
    struct app_wg_lookup result = {0};

    net_if_foreach(app_wg_find_iface, &result);

    if (result.iface == NULL) {
        return -ENODEV;
    }

    printk("WireGuard interface found: %d\n",
           net_if_get_by_iface(result.iface));

    return 0;
}


/* 接收等待上限：2 秒，额外的微秒部分为 0。 */
struct zsock_timeval timeout = {
    .tv_sec = 2,
    .tv_usec = 0,
};



int main()
{
    int sock;
    printk("UDP example started\n");
    
    /* 应用初始化：先确认后续配置所需的 VPN 接口存在。 */
    int wg_ret = app_wireguard_init();

    if (wg_ret < 0) {
        printk("WireGuard init failed: %d\n", wg_ret);
        return 0;
    }


    sock = zsock_socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    if (sock < 0) {
        printk("socket create failed, errno=%d\n", errno);
        return 0;
    }

    printk("socket created, fd=%d\n", sock);


    /* Zephyr 公共 socket API：为这个 socket 设置接收超时。 */
    if (zsock_setsockopt(sock, ZSOCK_SOL_SOCKET, ZSOCK_SO_RCVTIMEO,
                         &timeout, sizeof(timeout)) < 0) {
        printk("set receive timeout failed, errno=%d\n", errno);
        zsock_close(sock);
        return 0;
    }


    struct net_sockaddr_in peer_addr = {0};
    char message[64];
    ssize_t sent;
    int ret;

    /* 填写对端的地址类型和 UDP 端口。 */
    peer_addr.sin_family = NET_AF_INET;
    peer_addr.sin_port = net_htons(4242);

    /* 将对端 IP 字符串转换成网络地址的二进制表示。 */
    ret = zsock_inet_pton(NET_AF_INET, TARGET_ADDRESS,
                          &peer_addr.sin_addr);
    if (ret != 1) {
        printk("invalid peer address, ret=%d\n", ret);
        zsock_close(sock);
        return 0;
    }

    /* 应用层发送循环：每秒发送一次，共发送 10 次。 */
    for (int i = 1; i <= 10; i++) {

        /* Zephyr 格式化 API：将本轮序号写入消息缓冲区。 */
        int message_len = snprintk(
            message, sizeof(message), "Hello from Titan #%d->", i);

        /* 返回值达到缓冲区容量，表示内容被截断，不能按该长度发送。 */
        if (message_len < 0 || (size_t)message_len >= sizeof(message)) {
            printk("message formatting failed\n");
            break;
        }

        /* Zephyr 公共 API：暂停当前线程 1 秒，网络线程仍可运行。 */
        k_sleep(K_SECONDS(1));

        sent = zsock_sendto(
            sock,
            message,
            (size_t)message_len,
            0,
            (const struct net_sockaddr *)&peer_addr,
            sizeof(peer_addr));

        if (sent < 0) {
            printk("UDP #%d failed, errno=%d\n", i, errno);
            continue;
        }

        printk("UDP #%d sent %d bytes\n", i, (int)sent);

        /* 应用接收缓冲区：预留最后一个字节放字符串结束符。 */
        char rx_buf[64];

        /* Zephyr 公共 socket API：从同一个 socket 接收一个 UDP 数据报。 */
        ssize_t received = zsock_recvfrom(
            sock,
            rx_buf,
            sizeof(rx_buf) - 1,
            0,
            NULL,
            NULL);

        if (received < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                printk("UDP #%d receive timeout\n", i);
            } else {
                printk("UDP #%d receive failed, errno=%d\n", i, errno);
            }
            continue;
        }

        /* 接收到的是字节；手动补上结束符后，才能按 C 字符串打印。 */
        rx_buf[received] = '\0';


        /* 应用层长度校验：回显的数据长度必须与本轮发送长度一致。 */
        if (received != message_len) {
            printk("UDP #%d length mismatch: expected=%d, received=%d\n",
                i, message_len, (int)received);
            continue;
        }

        /* C 标准库函数：比较两个缓冲区中的有效数据，不比较字符串结束符。 */
        if (memcmp(rx_buf, message, (size_t)message_len) != 0) {
            printk("UDP #%d content mismatch: %s\n", i, rx_buf);
            continue;
        }

        /* 应用层验收：长度和内容均匹配，才认定本轮回显校验通过。 */
        printk("UDP #%d verified %d bytes: %s\n",
            i, (int)received, rx_buf);

    }

        /* 本次实验结束，释放已经创建的 socket。 */
    if (zsock_close(sock) < 0) {
        printk("socket close failed, errno=%d\n", errno);
        return 0;
    }

    printk("socket closed\n");

    return 0;
}

