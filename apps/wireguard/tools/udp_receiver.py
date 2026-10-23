"""Windows 端 UDP 收发工具：默认监听 192.168.50.1:4242。

仅使用 Python 标准库，无需安装依赖。先运行本脚本，再复位 Titan，
即可查看板端发来的数据报，并将原始字节回显给发送方。
默认持续收发，按 Ctrl+C 退出；--once 处理一个数据报后退出，
--no-echo 仅接收，可用于测试板端的接收超时。
"""

import argparse
import errno
import socket
import sys


def parse_args() -> argparse.Namespace:
    """本脚本内部辅助函数：解析监听地址、端口、单次处理及回显选项。

    --host 是电脑自身的 IPv4 地址，不是开发板地址；
    --port 必须与板端 zsock_sendto() 使用的目标端口一致。
    参数不合法时由 argparse 打印提示并退出。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host", default="192.168.50.1",
        help="电脑监听的 IPv4 地址，默认 192.168.50.1",
    )
    parser.add_argument(
        "--port", type=int, default=4242,
        help="电脑监听的 UDP 端口，默认 4242",
    )
    parser.add_argument(
        "--once", action="store_true",
        help="处理一个数据报后退出；默认完成回显再退出",
    )
    parser.add_argument(
        "--no-echo", action="store_true",
        help="仅接收，不回显；可用于测试板端接收超时",
    )
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port 必须在 1 到 65535 之间")
    return args


def main() -> int:
    """命令行入口：创建、绑定、接收并回显 UDP 数据，退出时释放 socket。

    这是电脑端应用工具，不是板端驱动。每次显示发送方 IP/端口、
    实收字节数、原始 bytes 和按 UTF-8 解码的文本；非法 UTF-8
    以替换字符显示，原始数据仍可在 Bytes 行查看。默认通过同一个
    socket 把原始 bytes 发回 sender 的 IP 和端口，不重新编码文本。
    回显计数表示本机 sendto 成功次数，不表示板端已经确认收到。
    正常结束或 Ctrl+C 返回 0，socket 操作失败返回 1。
    """
    args = parse_args()
    received_count = 0
    echoed_count = 0

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as receiver:
            receiver.bind((args.host, args.port))
            # 定期结束等待，使 Windows 上的 Ctrl+C 也能及时被处理。
            # 超时仅用于检查退出请求，不代表网络故障，也不会结束脚本。
            receiver.settimeout(0.5)
            print(
                f"监听 UDP {args.host}:{args.port}，按 Ctrl+C 退出。\n"
                f"模式：{'仅接收' if args.no_echo else '接收并原样回显'}。\n"
                "现在可以复位 Titan，等待板端发送数据……",
                flush=True,
            )

            while True:
                try:
                    # 缓冲区可容纳一个最大长度的普通 IPv4 UDP 数据报。
                    data, sender = receiver.recvfrom(65535)
                except socket.timeout:
                    continue

                received_count += 1
                print(f"\n收到第 {received_count} 个数据报，共 {len(data)} 字节")
                print(f"From: {sender[0]}:{sender[1]}")
                print(f"Bytes: {data!r}")
                print(f"Data: {data.decode('utf-8', errors='replace')}", flush=True)

                if not args.no_echo:
                    # 应用层回显：回复实际源端口，不能假定板端也使用 4242。
                    # 直接发送原始 bytes，保留二进制、空数据报及非 UTF-8 内容。
                    sent = receiver.sendto(data, sender)
                    echoed_count += 1
                    print(
                        f"Echo: 已向 {sender[0]}:{sender[1]} 回发 {sent} 字节",
                        flush=True,
                    )

                if args.once:
                    break

    except KeyboardInterrupt:
        print(
            f"\n收发已停止，共收到 {received_count} 个数据报，回显 {echoed_count} 个。",
            flush=True,
        )
    except OSError as exc:
        print(f"UDP 收发失败：{exc}", file=sys.stderr)
        if exc.errno == errno.EADDRNOTAVAIL:
            print("请确认电脑以太网已配置监听 IP，或用 --host 指定电脑实际地址。",
                  file=sys.stderr)
        elif exc.errno == errno.EADDRINUSE:
            print("该端口已被占用，请关闭已有接收程序后重试。", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
