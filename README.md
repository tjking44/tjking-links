# TJ King — Release Landing Pages

One folder per release, hosted via GitHub Pages, built from a shared template so
design/copy/animation only ever gets written once.

**Live pattern:** `tjking44.github.io/tjking-links/<slug>/`

## What's templated (never changes per release)

Colors, layout, hover/tap animations, entrance motion, the "Join The List" offer
copy, the subscribe button. Lives in `_template/page_template.html`.

## What you provide per release

One small JSON file in `releases/<slug>.json`:

```json
{
  "slug": "out-the-door",
  "song_title": "Out The Door",
  "byline": "TJ King x Onbin",
  "stream_url": "https://distrokid.com/hyperfollow/...",
  "cover_art": "/path/to/cover.jpg"
}
```

- **slug** — becomes the URL path
- **song_title** — plain text, gets uppercased for the display heading
- **byline** — "TJ King" for solo, "TJ King x [collaborator]" for features
- **stream_url** — the Hyperfollow link. **Manual, every time** — no automation
  exists to pull this from DistroKid. Upload the release there first, grab the
  Hyperfollow URL from `distrokid.com/hyperfollow`, paste it here.
- **cover_art** — path to the release's cover image (or a placeholder if art
  isn't ready yet — swap it later by re-running the build)

## Build it

```
python3 build_release_page.py releases/<slug>.json
git add -A && git commit -m "Add <slug> landing page" && git push
```

Live in under a minute.

## Changing the shared design

Edit `_template/page_template.html` once — affects every future page built
from it. Existing pages already built need to be regenerated (re-run the build
command for each `releases/*.json` file) to pick up the change; it doesn't
retroactively update pages already committed.
