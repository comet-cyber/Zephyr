"""Windows 端 UDP 接收工具：默认监听 192.168.50.1:4242。

仅使用 Python 标准库，无需安装依赖。先运行本脚本，再复位 Titan，
即可查看板端发来的数据报。默认持续接收，按 Ctrl+C 退出；
添加 --once 可在收到一个数据报后退出。
"""

import argparse
import errno
import socket
import sys


def parse_args() -> argparse.Namespace:
    """本脚本内部辅助函数：解析电脑监听地址、端口和单次接收选项。

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
        help="收到一个数据报后退出；默认持续接收",
    )
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port 必须在 1 到 65535 之间")
    return args


def main() -> int:
    """命令行入口：创建、绑定并接收 UDP 数据，退出时释放 socket。

    这是电脑端应用工具，不是板端驱动。每次显示发送方 IP/端口、
    实收字节数、原始 bytes 和按 UTF-8 解码的文本；非法 UTF-8
    以替换字符显示，原始数据仍可在 Bytes 行查看。
    正常结束或 Ctrl+C 返回 0，socket 操作失败返回 1。
    """
    args = parse_args()
    received_count = 0

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as receiver:
            receiver.bind((args.host, args.port))
            # 定期结束等待，使 Windows 上的 Ctrl+C 也能及时被处理。
            # 超时仅用于检查退出请求，不代表网络故障，也不会结束脚本。
            receiver.settimeout(0.5)
            print(
                f"监听 UDP {args.host}:{args.port}，按 Ctrl+C 退出。\n"
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

                if args.once:
                    break

    except KeyboardInterrupt:
        print(f"\n接收已停止，共收到 {received_count} 个数据报。", flush=True)
    except OSError as exc:
        print(f"UDP 接收失败：{exc}", file=sys.stderr)
        if exc.errno == errno.EADDRNOTAVAIL:
            print("请确认电脑以太网已配置监听 IP，或用 --host 指定电脑实际地址。",
                  file=sys.stderr)
        elif exc.errno == errno.EADDRINUSE:
            print("该端口已被占用，请关闭已有接收程序后重试。", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
