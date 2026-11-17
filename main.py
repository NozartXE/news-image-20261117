#!/usr/bin/env python3
"""make.fun entry for news-image-20261117: "Sum up 17 November's world news in one image".

The picture itself is entry.png beside this file, drawn by build_image.py from
the verified record of Tuesday 17 November 2026 (Kerch Bridge struck again,
tankers mined in the Strait of Hormuz, the Xi-Trump-Putin Shenzhen summit,
Nvidia after Huang's exit, plus the day's wire briefs).

This program is the delivery step the grader runs: it validates the baked
image against the competition gate (a whole PNG, at most 1 MiB, at most
1024 by 1024 pixels) and copies it, byte for byte, to the output directory —
/output in the sandbox, or $MAKEFUN_OUTPUT_DIR when set. It uses no network
and no clock, so two runs always write identical bytes.
"""
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576  # 1 MiB gate
MAX_SIDE = 1024        # pixel gate, width and height
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Width and height from the IHDR chunk of a PNG byte string."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png does not start with the PNG signature")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate(data: bytes) -> None:
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} gate")
    width, height = png_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the {MAX_SIDE} pixel gate")
    if not data.endswith(b"IEND\xaeB`\x82"):
        raise ValueError("entry.png is truncated: it does not end with an IEND chunk")


def main() -> int:
    data = SOURCE.read_bytes()
    validate(data)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    width, height = png_dimensions(data)
    print(f"wrote {target}: {len(data)} bytes, {width}x{height}, validated against the gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
