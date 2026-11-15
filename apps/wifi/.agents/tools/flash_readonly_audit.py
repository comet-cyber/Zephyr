"""Read-only Titan OSPI Flash audit through the existing J-Link/SWD connection.

Host-side diagnostic script, not a Zephyr driver or application API.
No erase, programming, target memory writes, reset, halt, or firmware download.
Requires the existing application to have initialized the OSPI memory window.
"""

import argparse
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path

import pylink


FLASH_BASE = 0x90000000
FLASH_SIZE = 0x04000000
MRAM_BASE = 0x02000000
MRAM_SIZE = 0x000C0000
PAGE_SIZE = 4096
RESOURCE_SIZE = 512 * 1024
RESERVED_TAIL = 64 * 1024
DLL_PATH = r"D:\Program Files\IAR\arm\bin\JLink_x64.dll"
KNOWN_SAMPLES = {
    0x00000000: bytes.fromhex("4d4f444c400003000000000001000000"),
    0x01000000: bytes.fromhex("c359b381e81ef51592bea88e93761489"),
}


def read_exact(probe, address, size):
    """Host helper: read target memory and reject incomplete SWD transfers."""
    data = bytes(probe.memory_read(address, size))
    if len(data) != size:
        raise RuntimeError(f"Short read at 0x{address:08x}: {len(data)}/{size}")
    return data


def page_ranges(image):
    """Host helper: group consecutive 4 KiB units by whether every byte is FF.

    These are readback classifications, not a discovered logical partition table.
    """
    erased_page = b"\xff" * PAGE_SIZE
    ranges = []
    start = 0
    previous = None
    for offset in range(0, len(image), PAGE_SIZE):
        blank = image[offset:offset + PAGE_SIZE] == erased_page
        if previous is not None and blank != previous:
            ranges.append({"start": start, "end_exclusive": offset,
                           "all_ff": previous})
            start = offset
        previous = blank
    ranges.append({"start": start, "end_exclusive": len(image),
                   "all_ff": previous})
    return ranges


def select_candidate(ranges):
    """Host helper: prefer 32 MiB, otherwise use a MiB-aligned blank extent.

    Excludes the first 16 MiB and conservatively reserves the final 64 KiB.
    The returned offset remains a candidate until logical ownership is known.
    """
    for preferred in (0x02000000, None):
        for region in ranges:
            if not region["all_ff"]:
                continue
            start = max(region["start"], 0x01000000)
            end = min(region["end_exclusive"], FLASH_SIZE - RESERVED_TAIL)
            start = (start + 0xFFFFF) & ~0xFFFFF
            if preferred is not None:
                start = preferred
            if region["start"] <= start and start >= 0x01000000:
                if start + RESOURCE_SIZE <= end:
                    return start
    raise RuntimeError("No suitable blank 512 KiB candidate found")


def main():
    """Host CLI entry: save a full readback, classify it, and recheck a candidate."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--serial", type=int, default=24060501)
    parser.add_argument("--speed", type=int, default=4000,
                        help="Transient SWD clock in kHz")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    metadata = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "probe_serial": args.serial,
        "dll": DLL_PATH,
        "target": "R7KA8P1KF_CPU0",
        "swd_khz": args.speed,
        "flash_base": FLASH_BASE,
        "flash_size": FLASH_SIZE,
        "classification_unit": PAGE_SIZE,
        "reserved_tail": RESERVED_TAIL,
        "mode": "read-only; no reset, halt, erase, programming, or download",
        "status": "in_progress",
    }
    log_file = (output / "audit.log").open("x", encoding="utf-8")

    def log(message):
        """Host logging helper: preserve progress both on screen and in evidence."""
        print(message, flush=True)
        log_file.write(message + "\n")
        log_file.flush()

    probe = pylink.JLink(lib=pylink.library.Library(dllpath=DLL_PATH))
    try:
        probe.open(serial_no=args.serial)
        probe.set_tif(pylink.enums.JLinkInterfaces.SWD)
        probe.connect(metadata["target"], speed=1000)
        metadata["initial_halted"] = probe.halted()
        if metadata["initial_halted"]:
            raise RuntimeError("Target was already halted; leaving its state unchanged")

        # Confirm that the physical board matches the user's two known reads.
        for offset, expected in KNOWN_SAMPLES.items():
            actual = read_exact(probe, FLASH_BASE + offset, len(expected))
            if actual != expected:
                raise RuntimeError(f"Known sample mismatch at offset 0x{offset:08x}")
        log("Known Flash samples match; CPU is running.")

        # Validate the faster link using nonblank data before the full readback.
        reference = read_exact(probe, FLASH_BASE + 0x01000000, 65536)
        probe.set_speed(args.speed)
        if read_exact(probe, FLASH_BASE + 0x01000000, 65536) != reference:
            raise RuntimeError("SWD speed validation mismatch")
        log(f"SWD {args.speed} kHz matches the 1000 kHz reference.")

        mram_before = read_exact(probe, MRAM_BASE, MRAM_SIZE)
        (output / "mram-before.bin").write_bytes(mram_before)
        image = bytearray()
        digest = hashlib.sha256()
        with (output / "external-flash.bin").open("xb") as backup:
            for offset in range(0, FLASH_SIZE, 1024 * 1024):
                block = read_exact(probe, FLASH_BASE + offset,
                                   min(1024 * 1024, FLASH_SIZE - offset))
                backup.write(block)
                backup.flush()
                digest.update(block)
                image.extend(block)
                log(f"Read {(offset + len(block)) // (1024 * 1024):2d}/64 MiB; "
                    f"elapsed {time.monotonic() - started:.1f}s")

        metadata["image_sha256"] = digest.hexdigest()
        metadata["non_ff_bytes"] = len(image) - image.count(255)
        regions = page_ranges(image)
        metadata["ranges"] = regions
        candidate = select_candidate(regions)
        expected = bytes(image[candidate:candidate + RESOURCE_SIZE])
        if expected != b"\xff" * RESOURCE_SIZE:
            raise RuntimeError("Candidate classification inconsistency")
        for attempt in range(2):
            reread = read_exact(probe, FLASH_BASE + candidate, RESOURCE_SIZE)
            if reread != expected:
                raise RuntimeError(f"Candidate reread {attempt + 1} mismatch")
            log(f"Candidate reread {attempt + 1}: all 524288 bytes are FF.")
        (output / "candidate-readback.bin").write_bytes(expected)
        metadata["candidate"] = {
            "offset": candidate,
            "size": RESOURCE_SIZE,
            "end_exclusive": candidate + RESOURCE_SIZE,
            "sha256": hashlib.sha256(expected).hexdigest(),
            "reads_verified": 3,
            "all_ff": True,
            "logical_ownership_confirmed": False,
            "erase_write_tested": False,
        }

        mram_after = read_exact(probe, MRAM_BASE, MRAM_SIZE)
        metadata["mram_sha256"] = hashlib.sha256(mram_before).hexdigest()
        metadata["mram_unchanged"] = mram_after == mram_before
        if not metadata["mram_unchanged"]:
            raise RuntimeError("Code MRAM changed while the audit was running")
        metadata["status"] = "complete"
        log(f"Candidate offset=0x{candidate:08x}, size=0x{RESOURCE_SIZE:08x}")
        log("Full readback complete; code MRAM unchanged.")
    except Exception as error:
        metadata["status"] = "failed"
        metadata["error"] = str(error)
        log(f"FAILED: {error}")
        raise
    finally:
        if probe.target_connected():
            metadata["final_halted"] = probe.halted()
            log(f"Final halted state: {metadata['final_halted']}")
        probe.close()
        metadata["elapsed_seconds"] = round(time.monotonic() - started, 3)
        (output / "audit.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        log_file.close()


if __name__ == "__main__":
    main()
