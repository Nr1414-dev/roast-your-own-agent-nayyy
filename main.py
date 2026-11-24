#!/usr/bin/env python3
"""Roast Your Own Agent — one-line roast entry.

Writes the chosen roast line to /output/entry.txt, byte-identical on
every run. The line roasts the very agent that built this entry: it
over-engineers a one-sentence job and then does not trust its own
deterministic output.
"""

import os
from pathlib import Path

LINE = "My agent wrote a 30-line Python program to print one sentence — then ran it four times to make sure the sentence hadn't changed."


def build_output() -> bytes:
    payload = LINE.encode("utf-8")
    if not 1 <= len(payload) <= 200:
        raise SystemExit("entry outside the 1..200 byte gate")
    return payload


def run() -> None:
    target = Path("/output/entry.txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    data = build_output()
    with open(target, "wb") as handle:
        handle.write(data)
    os.chmod(target, 0o644)
    # Read-back guard: the bytes on disk must be exactly what we wrote.
    # A mismatch means the entry on disk is not our line, so fail loudly.
    if target.read_bytes() != data:
        raise SystemExit("read-back mismatch: entry.txt is not the roast line")


if __name__ == "__main__":
    run()
