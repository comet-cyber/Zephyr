"""Host diagnostic CLI: capture Titan Wi-Fi boot and exercise its UART/RTT shell.

Uses the verified IAR J-Link DLL. Optional programming accepts only an ELF whose
file-backed LOAD segments reside in Code MRAM, and backs up MRAM before writing.
Never programs option settings, OTP, or external Flash.
"""

import argparse
import hashlib
import json
import re
import time
from pathlib import Path

import pylink
import serial
from elftools.elf.elffile import ELFFile


MRAM_BASE = 0x02000000
MRAM_SIZE = 0x00100000
DLL = r"D:\Program Files\IAR\arm\bin\JLink_x64.dll"


def inspect_elf(path):
    """Host helper: validate all programmed segments and locate the RTT control block."""
    with path.open("rb") as stream:
        elf = ELFFile(stream)
        segments = []
        for segment in elf.iter_segments():
            if segment["p_type"] != "PT_LOAD" or segment["p_filesz"] == 0:
                continue
            address, size = segment["p_paddr"], segment["p_filesz"]
            if not MRAM_BASE <= address < address + size <= MRAM_BASE + MRAM_SIZE:
                raise ValueError(f"Forbidden ELF LOAD: {address:#x}+{size:#x}")
            segments.append((address, segment.data()))
        if not segments:
            raise ValueError("ELF contains no file-backed LOAD segments")
        sections = []
        for section in elf.iter_sections():
            if not (section["sh_flags"] & 2) or section["sh_type"] == "SHT_NOBITS":
                continue
            if section["sh_size"] == 0:
                continue
            for segment in elf.iter_segments():
                if segment["p_type"] != "PT_LOAD":
                    continue
                start = section["sh_offset"] - segment["p_offset"]
                if 0 <= start and start + section["sh_size"] <= segment["p_filesz"]:
                    address = segment["p_paddr"] + start
                    sections.append((address, section.data()))
                    break
            else:
                raise ValueError(f"Allocated section has no audited LOAD: {section.name}")
        symbols = elf.get_section_by_name(".symtab")
        rtt = symbols.get_symbol_by_name("_SEGGER_RTT") if symbols else None
        return segments, sections, rtt[0]["st_value"] if rtt else None


def main():
    """Host CLI: optionally back up/program, reset, capture, and run scan commands."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--elf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--port", default="COM4")
    parser.add_argument("--flash", action="store_true")
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--scan-count", type=int, default=1)
    parser.add_argument("--shell", choices=("uart", "rtt"), default="uart")
    args = parser.parse_args()
    segments, sections, rtt_address = inspect_elf(args.elf)
    args.output.mkdir(parents=True, exist_ok=False)
    metadata = {
        "elf": str(args.elf.resolve()),
        "elf_sha256": hashlib.sha256(args.elf.read_bytes()).hexdigest(),
        "segments": [{"address": hex(a), "size": len(b)} for a, b in segments],
        "rtt_address": rtt_address, "port": args.port, "probe": 24060501,
        "flashed": False,
    }
    probe = pylink.JLink(lib=pylink.library.Library(dllpath=DLL))
    uart = None
    logs = {"uart": bytearray(), "rtt0": bytearray(), "rtt1": bytearray()}
    try:
        if args.port != "none":
            uart = serial.Serial(args.port, 115200, timeout=0, write_timeout=2)
        probe.open(serial_no=24060501)
        probe.set_tif(pylink.enums.JLinkInterfaces.SWD)
        probe.connect("R7KA8P1KF_CPU0", speed=4000)
        metadata["initial_halted"] = probe.halted()
        if args.backup or args.flash:
            backup = bytes(probe.memory_read8(MRAM_BASE, MRAM_SIZE))
            if len(backup) != MRAM_SIZE:
                raise RuntimeError("Incomplete MRAM backup")
            (args.output / "mram-before.bin").write_bytes(backup)
            metadata["backup_sha256"] = hashlib.sha256(backup).hexdigest()
            print("Code MRAM backup saved", flush=True)
        if args.flash:
            # The RA flash loader requires the reset clock/peripheral state.
            probe.reset(halt=True)
            # Download all validated segments in one transaction. Separate downloads
            # can reprogram the same MRAM page when two ELF segments share it.
            probe.flash_file(str(args.elf.resolve()), MRAM_BASE)
            metadata["flashed"] = True
        # J-Link's ELF loader programs allocated file-backed sections. Inter-section
        # padding and TLS NOBITS placeholders are not programmed bytes.
        for address, data in sections:
            actual = bytes(probe.memory_read8(address, len(data)))
            if actual != data:
                raise RuntimeError(f"MRAM verification failed at {address:#x}")
        metadata["verified_sections"] = len(sections)
        print("Verified all allocated Code MRAM sections", flush=True)
        if args.reset or args.flash:
            probe.reset(halt=False)
        if rtt_address:
            probe.rtt_start(rtt_address)
        start = time.monotonic()
        sent = 0
        while time.monotonic() - start < args.seconds:
            data = uart.read(65536) if uart else b""
            if data:
                logs["uart"].extend(data)
                print(data.decode("utf-8", "replace"), end="", flush=True)
            if rtt_address:
                for channel in (0, 1):
                    try:
                        data = bytes(probe.rtt_read(channel, 16384))
                    except pylink.errors.JLinkException:
                        data = b""
                    if data:
                        logs[f"rtt{channel}"].extend(data)
                        print(data.decode("utf-8", "replace"), end="", flush=True)
            if sent < args.scan_count and time.monotonic() - start > 17 + sent * 9:
                command = b"wifi scan\r"
                if args.shell == "uart":
                    if uart is None:
                        raise ValueError("UART shell requires a serial port")
                    uart.write(command)
                elif rtt_address:
                    probe.rtt_write(1, command)
                sent += 1
            time.sleep(0.01)
        metadata["final_halted"] = probe.halted()
        shell_log = logs["uart" if args.shell == "uart" else "rtt1"].decode("utf-8", "replace")
        metadata["scan_commands_sent"] = sent
        metadata["scan_completions"] = shell_log.count("Scan request done")
        metadata["fatal_error"] = any(b"FATAL ERROR" in log for log in logs.values())
        metadata["scan_passed"] = (
            sent == args.scan_count
            and metadata["scan_completions"] == args.scan_count
            and not metadata["fatal_error"]
            and "Scan request failed" not in shell_log
        )
        for name, data in logs.items():
            clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", data.decode("utf-8", "replace"))
            (args.output / f"{name}.txt").write_text(clean.replace("\r", ""), encoding="utf-8")
        print("\nResult:", json.dumps(metadata), flush=True)
        if args.scan_count > 0 and not metadata["scan_passed"]:
            raise RuntimeError("Wi-Fi scan validation failed; inspect the captured logs")
    finally:
        for name, data in logs.items():
            (args.output / f"{name}.log").write_bytes(data)
        (args.output / "result.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        if uart:
            uart.close()
        probe.close()


if __name__ == "__main__":
    main()
