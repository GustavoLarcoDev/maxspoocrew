#!/usr/bin/env python3
"""Render every piece in print/src/ to a press-ready PDF and a preview JPG.

    python build.py            # everything
    python build.py magnet     # only sources whose name contains "magnet"

Each source HTML owns its own trim size through its `@page { size: W in H in }`
rule, and this script reads that rule rather than keeping a separate manifest —
so the sheet size can never drift out of sync with the artwork.

Outputs, matching the convention the existing collateral already uses:
    print/pdf/<name>.pdf        what the printer gets
    print/img/<name>-p1.jpg     preview per page, for print/index.html
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import pymupdf  # used only to turn the finished PDF into previews
except ImportError:  # older releases only expose the `fitz` name
    try:
        import fitz as pymupdf
    except ImportError:
        sys.exit("Missing PyMuPDF. Run: pip install -r print/requirements.txt")

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
PDF_OUT = HERE / "pdf"
IMG_OUT = HERE / "img"

PREVIEW_DPI = 110       # readable in the gallery without bloating the repo
PREVIEW_QUALITY = 82

CHROME_CANDIDATES = [
    Path(p).expanduser()
    for p in [
        r"~\AppData\Local\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
    ]
]

PAGE_SIZE = re.compile(r"@page[^}]*size:\s*([\d.]+)in\s+([\d.]+)in", re.I)
EXPECT_PAGES = re.compile(
    r"""<meta\s+name=["']pages["']\s+content=["'](\d+)["']""", re.I
)
LINKED_CSS = re.compile(
    r"""<link[^>]+rel=["']stylesheet["'][^>]+href=["']([^"':]+\.css)["']""", re.I
)


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if path.exists():
            return str(path)
    sys.exit("Chrome not found. Edit CHROME_CANDIDATES in build.py.")


def styles_of(html: Path) -> str:
    """The piece's own markup plus any local stylesheet it links.

    The @page rule can live in a shared sheet rather than in the piece, which is
    how the ten flyers keep their trim size in one place instead of ten.
    """
    text = html.read_text(encoding="utf-8")
    for href in LINKED_CSS.findall(text):
        sheet = (html.parent / href).resolve()
        if sheet.exists():
            text += "\n" + sheet.read_text(encoding="utf-8")
    return text


def trim_size(html: Path) -> tuple[float, float]:
    """The @page size, in inches, that this piece declares."""
    match = PAGE_SIZE.search(styles_of(html))
    if not match:
        sys.exit(f"{html.name}: no '@page {{ size: Win Hin }}' rule found.")
    return float(match.group(1)), float(match.group(2))


def expected_pages(html: Path) -> int | None:
    """How many sheets this piece says it is, from <meta name="pages">."""
    match = EXPECT_PAGES.search(html.read_text(encoding="utf-8"))
    return int(match.group(1)) if match else None


def render(chrome: str, html: Path, profile: Path) -> Path:
    pdf = PDF_OUT / f"{html.stem}.pdf"
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            # A throwaway profile per run. Sharing the desktop profile lets
            # Chrome serve a cached copy of the CSS, which quietly renders the
            # edit you just made as if you had not made it.
            f"--user-data-dir={profile}",
            "--disable-application-cache",
            "--disk-cache-size=1",
            f"--print-to-pdf={pdf}",
            html.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    if not pdf.exists():
        sys.exit(f"{html.name}: Chrome produced no PDF.")
    return pdf


def preview(pdf: Path) -> list[Path]:
    # Clear previews from an earlier run first. A piece that used to overrun
    # left a stray -p2.jpg behind, and nothing downstream would ever remove it.
    for stale in IMG_OUT.glob(f"{pdf.stem}-p*.jpg"):
        stale.unlink()

    written = []
    with pymupdf.open(pdf) as doc:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=PREVIEW_DPI)
            out = IMG_OUT / f"{pdf.stem}-p{i}.jpg"
            pix.save(out, jpg_quality=PREVIEW_QUALITY)
            written.append(out)
    return written


def main() -> int:
    needle = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    chrome = find_chrome()
    PDF_OUT.mkdir(parents=True, exist_ok=True)
    IMG_OUT.mkdir(parents=True, exist_ok=True)

    sources = sorted(p for p in SRC.glob("*.html") if needle in p.stem.lower())
    if not sources:
        sys.exit(f"No sources in {SRC} matching {needle!r}.")

    profile = Path(tempfile.mkdtemp(prefix="mpc-print-"))
    overruns = []
    for html in sources:
        width, height = trim_size(html)
        want = expected_pages(html)
        pdf = render(chrome, html, profile)
        pages = preview(pdf)

        # An extra page means a sheet overran its own height and Chrome pushed
        # the remainder onto a new one. On screen that looks like a flyer with
        # the footer missing; at the printer it is a wasted box of paper.
        flag = ""
        if want is not None and len(pages) != want:
            flag = f"  <-- OVERRUNS, expected {want}"
            overruns.append(html.stem)

        size_kb = pdf.stat().st_size / 1024
        print(
            f"{html.stem:<34} {width}x{height}in  "
            f"{len(pages)} page(s)  {size_kb:6.0f} KB{flag}"
        )

    shutil.rmtree(profile, ignore_errors=True)

    print(f"\n{len(sources)} piece(s) built into print/pdf and print/img.")
    if overruns:
        print(f"\n{len(overruns)} piece(s) overrun their sheet: {', '.join(overruns)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
