#!/usr/bin/env python3
"""Turn each SVG/CSS scene into an MP4 you can post, plus a poster frame.

    python build_video.py                 # every scene
    python build_video.py morning         # only scenes matching "morning"
    python build_video.py --fps 30        # default is 25
    python build_video.py --contact       # also write a contact sheet per scene

How it works, and why this way:

Chrome is launched once per frame with `--virtual-time-budget=N`, which runs the
page's clock forward N milliseconds and screenshots the result. Virtual time is
deterministic - the same N always renders the same frame, whatever the machine
is doing - so the export is reproducible rather than a recording of however the
browser happened to perform.

That costs one browser launch per frame, so the frames are rendered in parallel
across CPU cores. An 11 second scene at 25fps is 275 launches; on eight cores
that is a couple of minutes rather than ten.

The alternative, screen-recording a live page, drops frames under load and would
make the phone number's legibility depend on the machine's mood.

Needs ffmpeg on PATH and Chrome.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENES = HERE / "scenes"
OUT = HERE / "video"
POSTER = HERE / "img"

W, H = 720, 1280
LOOP_SECONDS = 11.0          # must match the animation duration in _scene.css
POSTER_AT = 8.9              # end card fully assembled - the frame worth showing

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
FFMPEG_CANDIDATES = [
    Path(r"~\AppData\Local\Microsoft\WinGet\Packages").expanduser()
    / "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    / "ffmpeg-9.0-full_build" / "bin" / "ffmpeg.exe"
]


def find(name, candidates):
    for path in candidates:
        if path.exists():
            return str(path)
    found = shutil.which(name)
    if found:
        return found
    sys.exit(f"{name} not found on PATH.")


def grab(chrome, page_uri, ms, png, profile_root):
    """One frame, at exactly `ms` into the scene's own clock.

    The scene is asked to seek itself through ?t=, rather than relying on
    Chrome's virtual clock: transform and opacity animations run on the
    compositor, which the headless virtual clock does not advance, so every
    frame would come back identical.
    """
    with tempfile.TemporaryDirectory(dir=profile_root) as profile:
        subprocess.run(
            [
                chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--allow-file-access-from-files",
                "--force-device-scale-factor=1",
                "--run-all-compositor-stages-before-draw",
                f"--user-data-dir={profile}",
                f"--window-size={W},{H}",
                        # enough budget to settle fonts, images and the seek
                "--virtual-time-budget=6000",
                f"--screenshot={png}",
                f"{page_uri}?t={ms / 1000:.4f}",
            ],
            # A heavier scene under many parallel launches can sit well past
            # the default; the two-dog one tripped a 120s cap.
            check=True, capture_output=True, timeout=300,
        )
    return png


def render_frames(chrome, scene, frames_dir, fps, workers):
    n = int(round(LOOP_SECONDS * fps))
    uri = scene.as_uri()
    with tempfile.TemporaryDirectory() as profile_root:
        def one(i):
            png = frames_dir / f"f{i:05d}.png"
            grab(chrome, uri, int(round(i * 1000 / fps)), png, profile_root)
            return png
        with ThreadPoolExecutor(max_workers=workers) as pool:
            done = 0
            for _ in pool.map(one, range(n)):
                done += 1
                if done % 25 == 0 or done == n:
                    print(f"    {done}/{n} frames", end="\r", flush=True)
    print(" " * 30, end="\r")
    return n


def encode(ffmpeg, frames_dir, fps, out):
    subprocess.run(
        [
            ffmpeg, "-y", "-loglevel", "error",
            "-framerate", str(fps), "-i", str(frames_dir / "f%05d.png"),
            "-c:v", "libx264", "-preset", "slow", "-crf", "20",
            # yuv420p and even dimensions are what make this play everywhere,
            # including the phone previews people actually check it on.
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(out),
        ],
        check=True, capture_output=True,
    )


def contact_sheet(frames_dir, fps, out):
    """Nine moments across the loop, for reviewing without scrubbing a video."""
    from PIL import Image
    picks = [int(round(t * fps)) for t in (0.4, 1.6, 2.6, 3.2, 4.6, 5.5, 6.2, 7.7, 9.2)]
    thumbs = []
    for i in picks:
        p = frames_dir / f"f{i:05d}.png"
        if p.exists():
            thumbs.append(Image.open(p).convert("RGB").resize((W // 4, H // 4)))
    if not thumbs:
        return
    tw, th = thumbs[0].size
    sheet = Image.new("RGB", (tw * 3 + 40, th * 3 + 40), (26, 26, 28))
    for k, im in enumerate(thumbs[:9]):
        sheet.paste(im, (10 + (k % 3) * (tw + 10), 10 + (k // 3) * (th + 10)))
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("match", nargs="?", default="")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--contact", action="store_true")
    args = ap.parse_args()

    chrome = find("chrome", CHROME_CANDIDATES)
    ffmpeg = find("ffmpeg", FFMPEG_CANDIDATES)
    OUT.mkdir(parents=True, exist_ok=True)
    POSTER.mkdir(parents=True, exist_ok=True)

    scenes = sorted(p for p in SCENES.glob("scene-*.html")
                    if args.match.lower() in p.stem.lower())
    if not scenes:
        sys.exit(f"No scenes in {SCENES} matching {args.match!r}.")

    for scene in scenes:
        print(f"{scene.stem}")
        with tempfile.TemporaryDirectory() as tmp:
            frames = Path(tmp)
            render_frames(chrome, scene, frames, args.fps, args.workers)
            mp4 = OUT / f"{scene.stem}.mp4"
            encode(ffmpeg, frames, args.fps, mp4)
            grab(chrome, scene.as_uri(), int(POSTER_AT * 1000),
                 POSTER / f"{scene.stem}-p1.png", tmp)
            if args.contact:
                contact_sheet(frames, args.fps, HERE / f"_contact-{scene.stem}.png")
        print(f"    {mp4.name}  {mp4.stat().st_size / 1024 / 1024:.1f} MB  "
              f"{LOOP_SECONDS:.0f}s @ {args.fps}fps")

    print(f"\n{len(scenes)} scene(s) built into animation/video.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
