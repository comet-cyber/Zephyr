#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/net/socket.h>
#include <errno.h>

#define TARGET_ADDRESS "192.168.50.1"

int main()
{
    int sock;
    printk("UDP example started\n");
    
    sock = zsock_socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    if (sock < 0) {
        printk("socket create failed, errno=%d\n", errno);
        return 0;
    }

    printk("socket created, fd=%d\n", sock);




    struct net_sockaddr_in peer_addr = {0};
    const char message[] = "Hello from Titan";
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

        /* Zephyr 公共 API：暂停当前线程 1 秒，网络线程仍可运行。 */
        k_sleep(K_SECONDS(10));
        
        sent = zsock_sendto(
            sock,
            message,
            sizeof(message) - 1,
            0,
            (const struct net_sockaddr *)&peer_addr,
            sizeof(peer_addr));

        if (sent < 0) {
            printk("UDP #%d failed, errno=%d\n", i, errno);
        } else {
            printk("UDP #%d sent %d bytes\n", i, (int)sent);
        }


}




        /* 本次实验结束，释放已经创建的 socket。 */
    if (zsock_close(sock) < 0) {
        printk("socket close failed, errno=%d\n", errno);
        return 0;
    }

    printk("socket closed\n");

    return 0;
}

