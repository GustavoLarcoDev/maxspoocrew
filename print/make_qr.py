#!/usr/bin/env python3
"""Generate the QR codes the print sources point at.

    python make_qr.py

One SVG per campaign source, matching the convention the original 41 pieces
already use: the destination is the same, but each format tags itself so a scan
shows up in Analytics as having come from a trifold rather than a door hanger.

Two things here are not cosmetic:

* border=4 - the quiet zone the QR spec requires. Without it a reader has
  nothing to lock onto and scanning becomes unreliable in a way that only shows
  up on paper, never on screen.
* light="#ffffff" - an explicit white field, so the code carries its own
  contrast instead of inheriting whatever the artwork puts behind it.

Needs segno:  pip install segno
"""

import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.exit("Run: pip install segno")

SRC = Path(__file__).resolve().parent / "src"
BASE = "https://maxspoocrew.com/"
DARK = "#331411"

# Campaign source per format. The five names the original collateral already
# uses are kept spelled exactly as they were so historic Analytics data and new
# scans land in the same buckets.
SOURCES = [
    "trifold",
    "flyer",
    "hanger",
    "menu",
    "rack",
    "card",
    "eddm",
    "ratecard",
]


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        url = f"{BASE}?utm_source={source}&utm_medium=print"
        out = SRC / f"qr-{source}.svg"
        code = segno.make(url, error="h")
        code.save(str(out), scale=10, border=4, dark=DARK, light="#ffffff")
        print(f"{out.name:<18} v{code.version:<3} {url}")
    print(f"\n{len(SOURCES)} codes written to print/src.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
