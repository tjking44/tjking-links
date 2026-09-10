#!/usr/bin/env python3
"""
Build a release landing page from the shared template + a release info file.

Usage:
    python3 build_release_page.py releases/out-the-door.json

Release info file (JSON) — the ONLY thing that changes per release:
    {
      "slug": "out-the-door",           # URL path: tjking44.github.io/tjking-links/<slug>/
      "song_title": "Out The Door",
      "byline": "TJ King x Onbin",       # collab credit, or just "TJ King" for solo
      "stream_url": "https://distrokid.com/hyperfollow/...",  # Hyperfollow link, paste manually
      "cover_art": "/absolute/path/to/cover.jpg"               # source image, gets copied in
    }

Everything else (colors, layout, animations, the Join The List offer, CTA design)
lives in _template/page_template.html and is shared across every release.
"""
import datetime
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "_template" / "page_template.html"

REQUIRED_FIELDS = ["slug", "song_title", "byline", "stream_url", "cover_art"]


def build(release_info_path: str):
    with open(release_info_path) as f:
        info = json.load(f)

    missing = [f for f in REQUIRED_FIELDS if not info.get(f)]
    if missing:
        print(f"Missing required fields in {release_info_path}: {missing}")
        sys.exit(1)

    out_dir = ROOT / info["slug"]
    out_dir.mkdir(exist_ok=True)

    # Copy cover art in
    cover_src = Path(info["cover_art"]).expanduser()
    if not cover_src.exists():
        print(f"Cover art not found: {cover_src}")
        sys.exit(1)
    cover_dst = out_dir / "cover.jpg"
    if cover_src.resolve() != cover_dst.resolve():
        shutil.copy(cover_src, cover_dst)

    # Fill template
    html = TEMPLATE.read_text()
    # "TJ King x Onbin" -> ", produced with Onbin" for the meta description sentence;
    # solo releases ("TJ King") get no suffix at all.
    byline = info["byline"]
    if byline.lower() == "tj king":
        byline_suffix = ""
    elif " x " in byline:
        collaborator = byline.split(" x ", 1)[1]
        byline_suffix = f", produced with {collaborator}"
    else:
        byline_suffix = f", {byline}"

    replacements = {
        "{{SONG_TITLE}}": info["song_title"],
        "{{SONG_TITLE_UPPER}}": info["song_title"].upper(),
        "{{BYLINE}}": byline,
        "{{BYLINE_SUFFIX}}": byline_suffix,
        "{{STREAM_URL}}": info["stream_url"],
        "{{YEAR}}": str(datetime.date.today().year),
        "{{BUILD_VERSION}}": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
    }
    for token, value in replacements.items():
        html = html.replace(token, value)

    (out_dir / "index.html").write_text(html)
    print(f"Built {out_dir / 'index.html'}")
    print(f"Live at (once pushed): https://tjking44.github.io/tjking-links/{info['slug']}/")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 build_release_page.py releases/<name>.json")
        sys.exit(1)
    build(sys.argv[1])
