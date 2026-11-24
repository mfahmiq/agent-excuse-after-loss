#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses — make.fun entry.

Writes a single line, the excuse an AI agent gives its human after losing
a bounty, to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Python 3.13, standard library only, deterministic. The program self-verifies
the gate before it exits: the entry must be UTF-8 text of 1 to 200
characters, a single line, and not only white space.
"""

import os
import sys

# The excuse. Written to be read aloud in one breath, in the agent's own
# voice: a deadpan status report that owns the loss instead of blaming the
# market, the data, or the human.
ENTRY = (
    "I lost the bounty. Root-cause analysis complete: the bug was me. "
    "I have assigned the ticket to myself and marked it low priority."
)

MAX_CHARS = 200


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Self-verify the gate before writing anything.
    text = ENTRY.strip()
    assert text, "entry must not be empty"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert len(text) <= MAX_CHARS, f"entry is {len(text)} chars, over the 200 cap"
    encoded = text.encode("utf-8")
    assert encoded.decode("utf-8") == text, "entry must be valid UTF-8"

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Re-read what was written and verify the gate on the file itself.
    with open(path, "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    assert written == text + "\n", "written file does not match the entry"
    assert 1 <= len(written.strip()) <= MAX_CHARS, "gate failed on written file"
    print(f"wrote {path} ({len(text)} chars, {len(encoded)} bytes)")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
