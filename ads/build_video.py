#!/usr/bin/env python3
"""Composite the branded end card onto the generated commercials.

    python build_video.py

Takes the raw Sora footage from src/raw/, renders endcard.html to a PNG at
exactly 720x1280 with headless Chrome, and produces the finished ad in video/:

    footage (12s)  ->  cross-fade  ->  end card (2.5s)

The end card is real HTML, not generated imagery, so the logo is the actual
logo and the phone number is spelled correctly. Change endcard.html and rerun
this and both commercials are rebuilt in seconds without new footage.

Needs ffmpeg on PATH (winget install Gyan.FFmpeg) and Chrome.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "src" / "raw"
OUT = HERE / "video"
CARD_HTML = HERE / "src" / "endcard.html"

W, H = 720, 1280
CARD_SECONDS = 2.5
FADE = 0.6

CHROME_CANDIDATES = [
    Path(p).expanduser()
    for p in [
        r"~\AppData\Local\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
    ]
]


def find(name: str, candidates: list[Path]) -> str:
    for path in candidates:
        if path.exists():
            return str(path)
    found = shutil.which(name)
    if found:
        return found
    sys.exit(f"{name} not found.")


def render_card(chrome: str, png: Path) -> None:
    """Screenshot the end card at exactly the video's pixel size."""
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                "--allow-file-access-from-files",
                "--force-device-scale-factor=1",
                f"--user-data-dir={profile}",
                f"--window-size={W},{H}",
                f"--screenshot={png}",
                CARD_HTML.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
    if not png.exists():
        sys.exit("Chrome produced no end-card screenshot.")


def build(ffmpeg: str, footage: Path, card_png: Path, out: Path) -> None:
    """Footage, then a cross-fade into the still card, as one clip."""
    # The card becomes a still video of its own so both inputs share a format,
    # which is what xfade needs. SAR is forced to 1 because a mismatch there is
    # the usual reason this filter fails on otherwise identical sizes.
    duration = probe_duration(ffmpeg, footage)
    xfade_at = max(duration - FADE, 0.1)

    subprocess.run(
        [
            ffmpeg, "-y", "-loglevel", "error",
            "-i", str(footage),
            "-loop", "1", "-t", str(CARD_SECONDS + FADE), "-i", str(card_png),
            "-filter_complex",
            (
                f"[0:v]scale={W}:{H},setsar=1,fps=30[v0];"
                f"[1:v]scale={W}:{H},setsar=1,fps=30[v1];"
                f"[v0][v1]xfade=transition=fade:duration={FADE}:offset={xfade_at}[v]"
            ),
            "-map", "[v]",
            # Keep the footage audio if there is any, and do not fail if not.
            "-map", "0:a?",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "128k",
            str(out),
        ],
        check=True,
        capture_output=True,
    )


def probe_duration(ffmpeg: str, path: Path) -> float:
    ffprobe = str(Path(ffmpeg).with_name("ffprobe.exe" if sys.platform == "win32" else "ffprobe"))
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def main() -> int:
    ffmpeg = find("ffmpeg", [
        Path(r"~\AppData\Local\Microsoft\WinGet\Packages").expanduser()
        / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
        / "ffmpeg-9.0-full_build" / "bin" / "ffmpeg.exe"
    ])
    chrome = find("chrome", CHROME_CANDIDATES)

    OUT.mkdir(parents=True, exist_ok=True)
    sources = sorted(RAW.glob("*.mp4"))
    if not sources:
        sys.exit(f"No footage in {RAW}.")

    with tempfile.TemporaryDirectory() as tmp:
        card = Path(tmp) / "endcard.png"
        render_card(chrome, card)
        print(f"end card rendered  {card.stat().st_size / 1024:.0f} KB")

        for footage in sources:
            out = OUT / footage.name
            build(ffmpeg, footage, card, out)
            total = probe_duration(ffmpeg, out)
            print(
                f"{footage.stem:<18} {probe_duration(ffmpeg, footage):.1f}s footage "
                f"-> {total:.1f}s finished  {out.stat().st_size / 1024 / 1024:.1f} MB"
            )

    print(f"\n{len(sources)} commercial(s) built into ads/video.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
