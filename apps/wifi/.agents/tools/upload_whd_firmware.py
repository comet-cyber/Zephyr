#!/usr/bin/env python3
"""通过 Zephyr UART Shell 将 CYW43438 固件写入 Titan 外部 OSPI Flash。

默认只写入 0x02000000 开始的 512 KiB whd-firmware 分区，不负责启动
Wi-Fi，也不校验写入后的整段 Flash 内容。若目标区已有数据，可显式使用
--erase-first 擦除整个固件分区后再上传。
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = APP_ROOT.parent.parent
DEFAULT_FIRMWARE = (
    WORKSPACE_ROOT
    / "modules"
    / "hal"
    / "infineon"
    / "zephyr"
    / "blobs"
    / "img"
    / "whd"
    / "resources"
    / "firmware"
    / "COMPONENT_43438"
    / "43438A1.bin"
)

EXPECTED_SOURCE_SHA256 = "f85e3feed55c429cf2fc88316dba472647da25622bac6c07ab63807fa0ad875e"
FLASH_DEVICE = "flash-controller@1"
FLASH_OFFSET = 0x02000000
PARTITION_SIZE = 512 * 1024
WRITE_BLOCK_SIZE = 16
UART_PACKET_SIZE = 64
FLASH_LOAD_BUFFER_SIZE = 256
UART_PROMPT = b"uart:~$ "
UART_PACKET_DELAY_S = 0.002


class ShellReader:
    """缓存并搜索 Zephyr Shell 的串口输出，同时保留已读文本供诊断。"""

    def __init__(self, serial_port: Any) -> None:
        """绑定已打开的 pyserial 端口并初始化输出缓存。"""
        self.serial_port = serial_port
        self.data = bytearray()
        self.search_from = 0

    def wait_for(self, marker: bytes, timeout_s: float, description: str) -> None:
        """等待指定 Shell 回执；超时会附上最近收到的文本帮助定位。"""
        deadline = time.monotonic() + timeout_s
        while True:
            marker_at = self.data.find(marker, self.search_from)
            if marker_at >= 0:
                self.search_from = marker_at + len(marker)
                return

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                tail = bytes(self.data[-1200:]).decode("utf-8", errors="replace")
                raise TimeoutError(
                    f"等待 {description} 超时；最近的 Shell 输出为：\n{tail}"
                )

            received = self.serial_port.read(64)
            if received:
                self.data.extend(received)


def configure_console_encoding() -> None:
    """将 Windows 控制台输出设为 UTF-8，避免中文提示显示为乱码。"""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def sha256_hex(data: bytes) -> str:
    """计算字节内容的 SHA-256 十六进制摘要。"""
    return hashlib.sha256(data).hexdigest()


def prepare_payload(firmware_path: Path) -> tuple[bytes, bytes]:
    """读取并校验上游固件，再补 FF 到 16 字节写入边界。"""
    if not firmware_path.is_file():
        raise FileNotFoundError(f"固件文件不存在：{firmware_path}")

    source = firmware_path.read_bytes()
    source_hash = sha256_hex(source)
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise ValueError(
            "固件 SHA-256 与已审核的 CYW43438 文件不一致："
            f"期望 {EXPECTED_SOURCE_SHA256}，实际 {source_hash}。"
        )

    padding_size = (-len(source)) % WRITE_BLOCK_SIZE
    payload = source + (b"\xff" * padding_size)
    if len(payload) > PARTITION_SIZE:
        raise ValueError(
            f"补齐后的固件为 {len(payload)} 字节，超过分区容量 {PARTITION_SIZE} 字节。"
        )

    return source, payload


def make_parser() -> argparse.ArgumentParser:
    """定义固件路径、串口参数、检查模式和可选分区擦除开关。"""
    parser = argparse.ArgumentParser(
        description="通过 UART Shell 将 CYW43438 固件上传到外部 OSPI Flash。"
    )
    parser.add_argument(
        "--firmware",
        type=Path,
        default=DEFAULT_FIRMWARE,
        help=f"原始固件路径（默认：{DEFAULT_FIRMWARE}）",
    )
    parser.add_argument(
        "--port",
        help="Zephyr Shell 串口，例如 COM34；上传时必填。",
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=115200,
        help="串口波特率（默认 115200，与当前板级 DTS 一致）。",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="等待每条 Shell 回执的超时秒数（默认 15 秒）。",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="只校验固件和对齐长度，不打开串口、不写 Flash。",
    )
    parser.add_argument(
        "--erase-first",
        action="store_true",
        help="先擦除整个 512 KiB whd-firmware 分区；执行前会要求输入确认词。",
    )
    return parser


def open_serial(port_name: str, baud_rate: int) -> Any:
    """打开 UART；关闭软硬件流控并保持 DTR/RTS 为非有效状态。"""
    try:
        import serial
    except ImportError as exc:
        raise RuntimeError(
            "缺少 pyserial。请使用 F:\\zephyr\\.venv\\Scripts\\python.exe 运行，"
            "或在对应 Python 环境安装 pyserial。"
        ) from exc

    serial_port = serial.Serial()
    serial_port.port = port_name
    serial_port.baudrate = baud_rate
    serial_port.timeout = 0.1
    serial_port.write_timeout = 10
    serial_port.xonxoff = False
    serial_port.rtscts = False
    serial_port.dsrdtr = False
    serial_port.dtr = False
    serial_port.rts = False
    serial_port.open()
    return serial_port


def write_shell_command(serial_port: Any, command: str) -> None:
    """用单独的 CR 结束命令，避免 LF 泄漏到随后启动的二进制接收模式。"""
    command_bytes = command.encode("ascii") + b"\r"
    written = serial_port.write(command_bytes)
    if written != len(command_bytes):
        raise OSError(f"Shell 命令只发送了 {written}/{len(command_bytes)} 字节。")
    serial_port.flush()


def confirm_partition_erase() -> bool:
    """要求用户明确确认擦除范围固定为 512 KiB 固件分区。"""
    print(
        "即将擦除外部 Flash 分区："
        f"0x{FLASH_OFFSET:08X} 至 0x{FLASH_OFFSET + PARTITION_SIZE - 1:08X}"
    )
    return input('输入 ERASE WHD PARTITION 才继续：').strip() == "ERASE WHD PARTITION"


def erase_firmware_partition(
    serial_port: Any, shell: ShellReader, timeout_s: float
) -> None:
    """通过 Zephyr Shell 擦除固件分区，并等待成功消息和命令提示符。"""
    command = (
        f"flash erase {FLASH_DEVICE} 0x{FLASH_OFFSET:08X} "
        f"0x{PARTITION_SIZE:X}"
    )
    write_shell_command(serial_port, command)
    shell.wait_for(b"Erase success.", timeout_s, "Flash 分区擦除完成")
    shell.wait_for(UART_PROMPT, timeout_s, "擦除后的 Shell 提示符")
    print("已擦除 whd-firmware 分区。")


def upload_payload(
    serial_port: Any, shell: ShellReader, payload: bytes, timeout_s: float
) -> None:
    """启动 flash load，并以 64 字节 UART 包等待每个 256 字节写入回执。"""
    command = f"flash load {FLASH_DEVICE} 0x{FLASH_OFFSET:08X} {len(payload)}"
    write_shell_command(serial_port, command)
    shell.wait_for(
        f"Send {len(payload)} bytes to complete flash load command".encode("ascii"),
        timeout_s,
        "flash load 接收提示",
    )
    shell.wait_for(b"Loading...", timeout_s, "Shell 原始数据接收模式")

    transfer_started = False
    transfer_output_start = len(shell.data)
    sent = 0
    try:
        for start in range(0, len(payload), UART_PACKET_SIZE):
            packet = payload[start : start + UART_PACKET_SIZE]
            written = serial_port.write(packet)
            if written != len(packet):
                raise OSError(f"UART 数据只发送了 {written}/{len(packet)} 字节。")
            serial_port.flush()
            transfer_started = True
            sent += len(packet)
            time.sleep(UART_PACKET_DELAY_S)

            if sent % FLASH_LOAD_BUFFER_SIZE == 0 or sent == len(payload):
                ack_index = (sent - 1) // FLASH_LOAD_BUFFER_SIZE
                shell.wait_for(
                    f"Written chunk {ack_index}".encode("ascii"),
                    timeout_s,
                    f"Flash 第 {ack_index} 个 256 字节写入回执",
                )
                if b"ERROR!" in shell.data[transfer_output_start:]:
                    raise OSError("Zephyr Flash Shell 报告 flash_write() 失败。")

                if (ack_index + 1) % 64 == 0 or sent == len(payload):
                    print(f"已发送 {sent}/{len(payload)} 字节。")

        shell.wait_for(b"Read all", timeout_s, "全部固件字节接收完成")
    except Exception as exc:
        if transfer_started:
            raise RuntimeError(
                "UART 上传中断；目标分区可能已部分写入。不要直接续传，"
                "先重新启动 Shell，再用 --erase-first 擦除分区后重试。"
            ) from exc
        raise


def verify_flash_header(
    serial_port: Any,
    shell: ShellReader,
    expected_header: bytes,
    timeout_s: float,
) -> None:
    """读回分区开头 16 字节，检测串口命令换行造成的数据偏移。"""
    output_start = len(shell.data)
    command = f"flash read {FLASH_DEVICE} 0x{FLASH_OFFSET:08X} 16"
    write_shell_command(serial_port, command)
    shell.wait_for(UART_PROMPT, timeout_s, "Flash 头部读回后的 Shell 提示符")

    response = bytes(shell.data[output_start:])
    match = re.search(
        rb"(?im)^02000000:\s*((?:[0-9a-f]{2}\s+){15}[0-9a-f]{2})",
        response,
    )
    if match is None:
        tail = response[-1200:].decode("utf-8", errors="replace")
        raise RuntimeError(f"未能解析 Flash 头部读回结果：\n{tail}")

    actual_header = bytes(
        int(token, 16) for token in re.findall(rb"[0-9a-f]{2}", match.group(1), re.I)
    )
    if actual_header != expected_header:
        raise RuntimeError(
            "Flash 前 16 字节与固件不匹配："
            f"期望 {expected_header.hex(' ')}，实际 {actual_header.hex(' ')}。"
            "请勿启动 Wi-Fi；先擦除 whd-firmware 分区，再重新上传。"
        )

    print("Flash 头部 16 字节回读匹配；整段 SHA-256 尚未验证。")


def print_image_summary(firmware_path: Path, source: bytes, payload: bytes) -> None:
    """显示原始固件、补齐后数据、目标分区和地址映射信息。"""
    print(f"固件文件：{firmware_path}")
    print(f"原始大小：{len(source)} 字节")
    print(f"原始 SHA-256：{sha256_hex(source)}")
    print(f"UART/Flash 写入大小：{len(payload)} 字节")
    print(f"补齐后 SHA-256：{sha256_hex(payload)}")
    print(
        "外部 Flash 偏移范围："
        f"0x{FLASH_OFFSET:08X}..0x{FLASH_OFFSET + len(payload) - 1:08X}"
    )
    print(f"主控映射地址：0x{0x90000000 + FLASH_OFFSET:08X}")


def main(argv: list[str] | None = None) -> int:
    """校验固件，并按命令行选择只检查或通过 UART 上传。"""
    configure_console_encoding()
    parser = make_parser()
    args = parser.parse_args(argv)

    if args.check_only and args.erase_first:
        parser.error("--check-only 不能与 --erase-first 同时使用。")
    if not args.check_only and not args.port:
        parser.error("上传时必须指定 --port，例如 --port COM34。")
    if args.baud <= 0 or args.timeout <= 0:
        parser.error("--baud 和 --timeout 必须为正数。")

    try:
        source, payload = prepare_payload(args.firmware.resolve())
        print_image_summary(args.firmware.resolve(), source, payload)
        if args.check_only:
            print("检查完成：未打开串口，也未写入 Flash。")
            return 0

        if args.erase_first and not confirm_partition_erase():
            print("用户未输入确认词，取消操作。")
            return 2

        print(f"正在打开 {args.port} @ {args.baud} baud。请先关闭占用该串口的终端程序。")
        serial_port = open_serial(args.port, args.baud)
        try:
            serial_port.reset_input_buffer()
            shell = ShellReader(serial_port)
            write_shell_command(serial_port, "")
            shell.wait_for(UART_PROMPT, args.timeout, "Zephyr UART Shell 提示符")

            if args.erase_first:
                erase_firmware_partition(serial_port, shell, max(args.timeout, 60.0))
            else:
                print("不会自动擦除；仅在目标固件区域已擦空时继续写入。")

            upload_payload(serial_port, shell, payload, args.timeout)
            shell.wait_for(UART_PROMPT, args.timeout, "上传后的 Shell 提示符")
            verify_flash_header(serial_port, shell, source[:16], args.timeout)
        finally:
            serial_port.close()

        print("设备报告 Read all：指定字节数已接收。")
        print("注意：这不是整段读回校验；仍需从 0x92000000 读回并比对 SHA-256。")
        return 0
    except (OSError, RuntimeError, TimeoutError, ValueError, FileNotFoundError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
