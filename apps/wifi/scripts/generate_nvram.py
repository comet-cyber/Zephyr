"""Build helper: encode a WHD text NVRAM file as NUL-separated C array bytes."""

import argparse
from pathlib import Path


def encode_nvram(text):
    """Convert LF/CRLF key=value lines to a double-NUL-terminated, aligned image.

    RESOURCE_READ_FROM_C_FILE sends these bytes directly to the Wi-Fi chip.
    Ignore comments and empty lines, preserve values, and reject malformed or
    duplicate keys so a broken configuration fails during the build.
    """
    entries = []
    keys = set()
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\0" in line or "=" not in line:
            raise ValueError(f"Invalid NVRAM entry on line {number}")
        key, _ = line.split("=", 1)
        if not key or key.strip() != key or key in keys:
            raise ValueError(f"Invalid or duplicate NVRAM key on line {number}")
        keys.add(key)
        entries.append(line.encode("ascii"))
    if not entries:
        raise ValueError("NVRAM contains no entries")
    image = b"\0".join(entries) + b"\0\0"
    return image + b"\0" * (-len(image) % 4)


def main():
    """Build CLI: validate the input and emit an include for a C byte array."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    image = encode_nvram(args.input.read_text(encoding="ascii"))
    rows = [", ".join(f"0x{value:02x}" for value in image[i:i + 12]) + ","
            for i in range(0, len(image), 12)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(rows) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
