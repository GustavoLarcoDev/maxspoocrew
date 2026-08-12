#!/usr/bin/env python3
"""Decode the QR code out of every built PDF and report what it points at.

    python checkqr.py

A QR that does not scan is invisible until a box of flyers has already been
printed, so this reads the rendered page rather than trusting the source SVG.
Exits non-zero if a code decodes to somewhere other than the website.

Every code is expected to carry a utm_source so scans are attributable by
format in Analytics - a bare link to the site counts as a failure here, because
it means that piece stopped being trackable.

Needs opencv and PyMuPDF:  pip install opencv-python-headless pymupdf
"""

import sys
from pathlib import Path

try:
    import cv2
    import numpy as np
    import pymupdf
except ImportError:
    sys.exit("Run: pip install opencv-python-headless pymupdf")

HERE = Path(__file__).resolve().parent
PDF_DIR = HERE / "pdf"
BASE = "https://maxspoocrew.com/"
DPI = 300


def decode(pdf: Path) -> str | None:
    """The QR payload on any page of this PDF, or None if nothing decoded.

    Tries more than one render size, and the multi-code detector as well as the
    single one. On a busy sheet the single detector will happily lock onto a
    table rule or a photo edge instead of the actual code and then report
    nothing - which reads as "this piece has no QR" when it plainly does.
    """
    detector = cv2.QRCodeDetector()
    with pymupdf.open(pdf) as doc:
        for page in doc:
            for dpi in (DPI, 200, 450):
                pix = page.get_pixmap(dpi=dpi)
                img = np.frombuffer(pix.samples, dtype=np.uint8)
                img = img.reshape(pix.height, pix.width, pix.n)
                gray = (
                    cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    if pix.n >= 3
                    else img[:, :, 0]
                )

                ok, texts, _, _ = detector.detectAndDecodeMulti(gray)
                if ok:
                    for text in texts:
                        if text:
                            return text

                text, _, _ = detector.detectAndDecode(gray)
                if text:
                    return text
    return None


def main() -> int:
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDFs in {PDF_DIR}. Run build.py first.")

    bad = []
    untagged = []
    without = []
    for pdf in pdfs:
        payload = decode(pdf)
        if payload is None:
            # Signs, magnets and bumper stickers carry no QR on purpose - they
            # are read from a moving car, where nobody is scanning anything.
            without.append(pdf.stem)
            print(f"{pdf.stem:<26} no QR")
        elif not payload.startswith(BASE):
            bad.append((pdf.stem, payload))
            print(f"{pdf.stem:<26} {payload}   <-- not the website")
        elif "utm_source=" not in payload:
            untagged.append((pdf.stem, payload))
            print(f"{pdf.stem:<26} {payload}   <-- no utm_source, untrackable")
        else:
            source = payload.split("utm_source=")[1].split("&")[0]
            print(f"{pdf.stem:<26} ok, tagged {source}")

    total = len(pdfs)
    good = total - len(without) - len(bad) - len(untagged)
    print(f"\n{good}/{total} carry a working, tagged QR")
    if without:
        print(f"{len(without)} carry no QR by design: {', '.join(without)}")
    for stem, payload in bad + untagged:
        print(f"  PROBLEM {stem}: {payload}")
    return 1 if (bad or untagged) else 0


if __name__ == "__main__":
    raise SystemExit(main())
