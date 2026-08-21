#!/usr/bin/env python3
"""Generate the QR codes the pieces point at.

    python make_qr.py

WHERE THEY GO

All of them land on **https://maxspoocrew.com/quote/** - the page that asks for
the address and the number of dogs. They used to point at the homepage, which
made a scan one more click away from the only thing a scan is for.

Each format still tags itself: `?utm_source=card`, `hanger`, `flyer`, `rack`.
The destination is identical, so a tag costs nothing, and without it Analytics
can only say that print works - not which piece is working. The names match the
ones the original collateral used so old and new scans land in the same bucket.

The separately supplied Vistaprint cards in cards/ carry a bare
https://maxspoocrew.com/quote/ with no tag. Both go to the same page; scans off
those simply arrive untagged.

THREE THINGS HERE THAT ARE NOT COSMETIC

* border=4 - the quiet zone the spec requires. Without it a reader has nothing
  to lock onto, and scanning gets unreliable in a way that only shows up on
  paper.
* light="#ffffff" - an explicit white field, so the code carries its own
  contrast instead of inheriting whatever art sits behind it.
* error="h" - the highest correction level, so a code survives being scuffed or
  rained on. The supplied cards use Q; H is the stricter of the two.

Needs segno:  pip install segno
"""

import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.exit("Run: pip install segno")

SRC = Path(__file__).resolve().parent / "src"
QUOTE = "https://maxspoocrew.com/quote/"
DARK = "#331411"

SOURCES = ["card", "hanger", "flyer", "rack"]


def main() -> int:
    SRC.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        url = f"{QUOTE}?utm_source={source}&utm_medium=print"
        out = SRC / f"qr-{source}.svg"
        code = segno.make(url, error="h")
        code.save(str(out), scale=10, border=4, dark=DARK, light="#ffffff")
        print(f"{out.name:<16} v{code.version:<3} {url}")
    print(f"\n{len(SOURCES)} codes written to marketing/src.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
