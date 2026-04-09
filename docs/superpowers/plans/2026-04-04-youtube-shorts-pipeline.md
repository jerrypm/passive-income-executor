# YouTube Shorts Auto-Generation Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Single-command pipeline that generates a YouTube Shorts MP4 from a topic string — Ollama script generation → edge-tts narration → Pillow code image → ffmpeg video assembly.

**Architecture:** One main Python script (`make_short.py`) with helper functions for each pipeline stage. A JSON file tracks topics. Output goes to `videos/ready/` with a companion `.txt` metadata file for easy YouTube upload.

**Tech Stack:** Python 3.9, edge-tts (Microsoft TTS), Pillow (image gen), ffmpeg (video), Ollama API (llama3.2), requests

---

## File Structure

```
scripts/youtube/
├── make_short.py          # Main pipeline — all 5 stages in one file
└── topics.json            # Topic queue with done/not-done tracking

videos/
├── ready/                 # Output: MP4 + .txt metadata files
└── archive/               # Manually move uploaded videos here
```

## Dependencies (all pre-installed)

- `edge-tts` → `/Users/avika/Library/Python/3.9/bin/edge-tts`
- `ffmpeg` → `/opt/homebrew/bin/ffmpeg`
- `Pillow` → installed via pip3
- `requests` → installed via pip3
- Ollama → `http://localhost:11434` (must be running, llama3.2 model)
- Font: `/System/Library/Fonts/Menlo.ttc` (monospace for code)
- Font: `/System/Library/Fonts/Monaco.ttf` (fallback)

---

## Task 1: Directory setup + topics.json

**Files:**
- Create: `scripts/youtube/topics.json`
- Create: `videos/ready/.gitkeep`
- Create: `videos/archive/.gitkeep`

- [ ] **Step 1: Create directories**

```bash
mkdir -p scripts/youtube videos/ready videos/archive
```

- [ ] **Step 2: Create topics.json with initial 15 topics**

Create `scripts/youtube/topics.json`:

```json
[
  {"topic": "SwiftUI gradient backgrounds in 3 lines", "type": "swiftui", "cta": "Follow for daily SwiftUI tips", "done": false},
  {"topic": "Custom ViewModifier in SwiftUI", "type": "swiftui", "cta": "Follow for daily SwiftUI tips", "done": false},
  {"topic": "SwiftUI animation with matchedGeometryEffect", "type": "swiftui", "cta": "Follow for daily SwiftUI tips", "done": false},
  {"topic": "NavigationStack vs NavigationView", "type": "swiftui", "cta": "Follow for daily SwiftUI tips", "done": false},
  {"topic": "SwiftUI AsyncImage with placeholder", "type": "swiftui", "cta": "Follow for daily SwiftUI tips", "done": false},
  {"topic": "Xcode breakpoint tricks you should know", "type": "ios", "cta": "More iOS tips: link in bio", "done": false},
  {"topic": "Instruments memory leak detection", "type": "ios", "cta": "More iOS tips: link in bio", "done": false},
  {"topic": "Swift Result type error handling", "type": "ios", "cta": "More iOS tips: link in bio", "done": false},
  {"topic": "Core Data vs SwiftData comparison", "type": "ios", "cta": "More iOS tips: link in bio", "done": false},
  {"topic": "iOS app launch time optimization", "type": "ios", "cta": "More iOS tips: link in bio", "done": false},
  {"topic": "Automate your dev workflow from terminal", "type": "promo", "cta": "Terminal Income Starter: link in bio", "done": false},
  {"topic": "Build an AI API and monetize it", "type": "promo", "cta": "Ollama API Monetizer: link in bio", "done": false},
  {"topic": "Free developer tools you need", "type": "promo", "cta": "DevToolKit: devtoolkit-sigma.vercel.app", "done": false},
  {"topic": "Nostr AI bot in 50 lines of Python", "type": "promo", "cta": "Nostr AI Toolkit: link in bio", "done": false},
  {"topic": "SwiftUI @Observable macro explained", "type": "swiftui", "cta": "Follow for daily SwiftUI tips", "done": false}
]
```

- [ ] **Step 3: Create .gitkeep files**

```bash
touch videos/ready/.gitkeep videos/archive/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add scripts/youtube/topics.json videos/ready/.gitkeep videos/archive/.gitkeep
git commit -m "feat(youtube): add topic queue and output directories"
```

---

## Task 2: Ollama script generation (Stage 1)

**Files:**
- Create: `scripts/youtube/make_short.py` (partial — stage 1 only)

- [ ] **Step 1: Create make_short.py with Ollama script generation**

Create `scripts/youtube/make_short.py`:

```python
#!/usr/bin/env python3
"""
YouTube Shorts auto-generation pipeline.
Usage: python3 make_short.py "topic here"
       python3 make_short.py --next
       python3 make_short.py --list
"""

import sys
import os
import json
import re
import subprocess
import requests
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
TOPICS_FILE = SCRIPT_DIR / "topics.json"
OUTPUT_DIR = PROJECT_DIR / "videos" / "ready"
TEMP_DIR = Path("/tmp/youtube_shorts")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
TTS_VOICE = "en-US-AndrewNeural"
EDGE_TTS_BIN = "/Users/avika/Library/Python/3.9/bin/edge-tts"
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
FONT_FALLBACK = "/System/Library/Fonts/Monaco.ttf"


def load_topics():
    with open(TOPICS_FILE) as f:
        return json.load(f)


def save_topics(topics):
    with open(TOPICS_FILE, "w") as f:
        json.dump(topics, f, indent=2)


def get_next_topic(topics):
    for t in topics:
        if not t["done"]:
            return t
    return None


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


def generate_script(topic, cta):
    """Stage 1: Ollama generates narration + code snippet."""
    prompt = f"""You are a YouTube Shorts script writer for iOS/SwiftUI developers.
Write a script for a 30-45 second short about: {topic}

Return ONLY valid JSON with these exact keys:
{{
  "title": "catchy title, max 50 chars",
  "narration": "spoken script, 80-120 words, conversational and energetic",
  "code_snippet": "working Swift/SwiftUI code example, 5-15 lines",
  "description": "YouTube description, 2-3 sentences with hashtags",
  "tags": "comma-separated tags for YouTube"
}}

Rules:
- narration should explain the code step by step
- code_snippet must be valid Swift/SwiftUI code
- End narration with: {cta}
- Keep it beginner-friendly but impressive"""

    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }, timeout=120)
        resp.raise_for_status()
        raw = resp.json()["response"]
        return json.loads(raw)
    except requests.ConnectionError:
        print("ERROR: Ollama not running. Start with: ollama serve")
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"ERROR: Ollama returned invalid JSON: {e}")
        print(f"Raw response: {raw[:500]}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Shorts generator")
    parser.add_argument("topic", nargs="?", help="Topic string")
    parser.add_argument("--next", action="store_true", help="Pick next unprocessed topic")
    parser.add_argument("--list", action="store_true", help="List all topics")
    parser.add_argument("--voice", default=TTS_VOICE, help=f"TTS voice (default: {TTS_VOICE})")
    parser.add_argument("--no-cta", action="store_true", help="Skip CTA overlay on image")
    args = parser.parse_args()

    topics = load_topics()

    if args.list:
        for i, t in enumerate(topics):
            status = "DONE" if t["done"] else "TODO"
            print(f"  [{status}] {i+1}. {t['topic']} ({t['type']})")
        sys.exit(0)

    if not args.next and not args.topic:
        parser.print_help()
        sys.exit(1)

    # Override TTS voice if specified
    voice = args.voice

    if args.next:
        topic_entry = get_next_topic(topics)
        if not topic_entry:
            print("All topics done! Add more to topics.json")
            sys.exit(0)
        topic = topic_entry["topic"]
        cta = "" if args.no_cta else topic_entry["cta"]
        print(f"Next topic: {topic}")
    else:
        topic = args.topic
        cta = "" if args.no_cta else "Follow for more dev tips"
        topic_entry = None

    # Stage 1: Generate script
    print(f"\n[1/5] Generating script for: {topic}")
    script = generate_script(topic, cta)
    print(f"  Title: {script['title']}")
    print(f"  Narration: {len(script['narration'].split())} words")
    print(f"  Code: {len(script['code_snippet'].splitlines())} lines")

    # Placeholder for stages 2-5 (added in next tasks)
    print("\n[DEBUG] Script generation complete. Stages 2-5 not yet implemented.")
    print(json.dumps(script, indent=2))
```

- [ ] **Step 2: Test script generation (requires Ollama running)**

```bash
# Start Ollama first if not running:
# ollama serve &

cd /Users/avika/Documents/passive-income-executor
python3 scripts/youtube/make_short.py --list
```

Expected: list of 15 topics with TODO status.

```bash
python3 scripts/youtube/make_short.py "SwiftUI gradient backgrounds in 3 lines"
```

Expected: JSON output with title, narration, code_snippet, description, tags. If Ollama not running, shows error message.

- [ ] **Step 3: Commit**

```bash
git add scripts/youtube/make_short.py
git commit -m "feat(youtube): add make_short.py with Ollama script generation (stage 1)"
```

---

## Task 3: TTS audio generation (Stage 2)

**Files:**
- Modify: `scripts/youtube/make_short.py` — add `generate_audio()` function and wire into main

- [ ] **Step 1: Add generate_audio function**

Add after `generate_script()` in `make_short.py`:

```python
def generate_audio(narration, output_path, voice=TTS_VOICE):
    """Stage 2: edge-tts converts narration to MP3."""
    result = subprocess.run([
        EDGE_TTS_BIN,
        "--voice", voice,
        "--text", narration,
        "--write-media", str(output_path)
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: edge-tts failed: {result.stderr}")
        sys.exit(1)

    # Get duration
    probe = subprocess.run([
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(output_path)
    ], capture_output=True, text=True)
    duration = float(probe.stdout.strip())
    return duration
```

- [ ] **Step 2: Wire stage 2 into main block**

Replace the placeholder comment block at the end of `__main__` (the lines starting with `# Placeholder for stages 2-5`) with:

```python
    # Stage 2: Generate audio
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = TEMP_DIR / "audio.mp3"
    print(f"\n[2/5] Generating audio with {voice}...")
    duration = generate_audio(script["narration"], audio_path, voice)
    print(f"  Duration: {duration:.1f}s")
    print(f"  File: {audio_path}")

    # Placeholder for stages 3-5 (added in next tasks)
    print("\n[DEBUG] Audio done. Stages 3-5 not yet implemented.")
```

- [ ] **Step 3: Test audio generation**

```bash
cd /Users/avika/Documents/passive-income-executor
python3 scripts/youtube/make_short.py "SwiftUI gradient backgrounds in 3 lines"
```

Expected: `[2/5] Generating audio...` with duration printed, MP3 file at `/tmp/youtube_shorts/audio.mp3`.

```bash
afplay /tmp/youtube_shorts/audio.mp3
```

Expected: hear the narration spoken.

- [ ] **Step 4: Commit**

```bash
git add scripts/youtube/make_short.py
git commit -m "feat(youtube): add edge-tts audio generation (stage 2)"
```

---

## Task 4: Code image generation (Stage 3)

**Files:**
- Modify: `scripts/youtube/make_short.py` — add `generate_image()` function and wire into main

- [ ] **Step 1: Add generate_image function**

Add after `generate_audio()` in `make_short.py`:

```python
def generate_image(title, code_snippet, cta, output_path):
    """Stage 3: Pillow generates dark-themed code image (1080x1920)."""
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1080, 1920
    BG_COLOR = (30, 30, 46)        # Catppuccin Mocha base
    TITLE_COLOR = (205, 214, 244)  # Catppuccin text
    CODE_COLOR = (166, 227, 161)   # Catppuccin green
    CTA_COLOR = (137, 180, 250)    # Catppuccin blue
    ACCENT = (245, 194, 231)       # Catppuccin pink

    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_path = FONT_PATH if os.path.exists(FONT_PATH) else FONT_FALLBACK
    try:
        font_title = ImageFont.truetype(font_path, 52)
        font_code = ImageFont.truetype(font_path, 28)
        font_cta = ImageFont.truetype(font_path, 38)
    except OSError:
        font_title = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_cta = ImageFont.load_default()

    # Draw decorative top bar
    draw.rectangle([(0, 0), (W, 8)], fill=ACCENT)

    # Title area (top 18%)
    title_y = 80
    # Word-wrap title
    title_lines = []
    words = title.split()
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font_title)
        if bbox[2] > W - 120:
            title_lines.append(line)
            line = word
        else:
            line = test
    if line:
        title_lines.append(line)

    for i, tl in enumerate(title_lines):
        bbox = draw.textbbox((0, 0), tl, font=font_title)
        x = (W - bbox[2]) // 2
        draw.text((x, title_y + i * 70), tl, fill=TITLE_COLOR, font=font_title)

    # Code area (middle 55%)
    code_y = 400
    # Draw code background box
    draw.rounded_rectangle(
        [(60, code_y - 20), (W - 60, code_y + 750)],
        radius=20,
        fill=(24, 24, 37)  # slightly darker
    )
    # Fake window dots
    for i, color in enumerate([(243, 139, 168), (249, 226, 175), (166, 227, 161)]):
        draw.ellipse([(90 + i * 30, code_y - 5), (105 + i * 30, code_y + 10)], fill=color)

    # Draw code lines
    code_lines = code_snippet.strip().splitlines()
    for i, cl in enumerate(code_lines[:20]):  # max 20 lines
        # Truncate long lines
        if len(cl) > 45:
            cl = cl[:42] + "..."
        draw.text((90, code_y + 30 + i * 36), cl, fill=CODE_COLOR, font=font_code)

    # CTA area (bottom 15%)
    cta_y = H - 250
    bbox = draw.textbbox((0, 0), cta, font=font_cta)
    x = (W - bbox[2]) // 2
    draw.text((x, cta_y), cta, fill=CTA_COLOR, font=font_cta)

    # Bottom accent bar
    draw.rectangle([(0, H - 8), (W, H)], fill=ACCENT)

    img.save(output_path, quality=95)
```

- [ ] **Step 2: Wire stage 3 into main block**

Replace the placeholder `# Placeholder for stages 3-5` with:

```python
    # Stage 3: Generate code image
    frame_path = TEMP_DIR / "frame.png"
    print(f"\n[3/5] Generating code image...")
    generate_image(script["title"], script["code_snippet"], cta, frame_path)
    print(f"  File: {frame_path}")

    # Placeholder for stages 4-5 (added in next tasks)
    print("\n[DEBUG] Image done. Stages 4-5 not yet implemented.")
```

- [ ] **Step 3: Test image generation**

```bash
cd /Users/avika/Documents/passive-income-executor
python3 scripts/youtube/make_short.py "SwiftUI gradient backgrounds in 3 lines"
```

Expected: PNG at `/tmp/youtube_shorts/frame.png`. Open it:

```bash
open /tmp/youtube_shorts/frame.png
```

Expected: dark-themed 1080x1920 image with title at top, code in middle, CTA at bottom.

- [ ] **Step 4: Commit**

```bash
git add scripts/youtube/make_short.py
git commit -m "feat(youtube): add Pillow code image generation (stage 3)"
```

---

## Task 5: Video assembly + metadata (Stages 4-5) + finish main flow

**Files:**
- Modify: `scripts/youtube/make_short.py` — add `assemble_video()`, `write_metadata()`, and complete main flow

- [ ] **Step 1: Add assemble_video and write_metadata functions**

Add after `generate_image()` in `make_short.py`:

```python
def assemble_video(image_path, audio_path, output_path, duration):
    """Stage 4: ffmpeg combines image + audio into MP4."""
    result = subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-t", str(duration),
        str(output_path)
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: ffmpeg failed: {result.stderr[:500]}")
        sys.exit(1)


def write_metadata(title, description, tags, cta, output_path):
    """Stage 5: Write companion metadata .txt for YouTube upload."""
    content = f"""TITLE:
{title}

DESCRIPTION:
{description}

{cta}

TAGS:
{tags}

#Shorts #SwiftUI #iOSDev #Programming #CodingTips
"""
    with open(output_path, "w") as f:
        f.write(content)
```

- [ ] **Step 2: Replace placeholder with stages 4-5 in main block**

Replace `# Placeholder for stages 4-5 (added in next tasks)` and the debug print below it with:

```python
    # Stage 4: Assemble video
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(topic)
    video_filename = f"{date_str}-{slug}.mp4"
    video_path = OUTPUT_DIR / video_filename
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n[4/5] Assembling video ({duration:.1f}s)...")
    assemble_video(frame_path, audio_path, video_path, duration)
    print(f"  File: {video_path}")

    # Stage 5: Write metadata
    meta_path = OUTPUT_DIR / f"{date_str}-{slug}.txt"
    print(f"\n[5/5] Writing metadata...")
    write_metadata(
        script["title"],
        script.get("description", ""),
        script.get("tags", ""),
        cta,
        meta_path
    )
    print(f"  File: {meta_path}")

    # Mark topic as done
    if topic_entry:
        topic_entry["done"] = True
        save_topics(topics)
        print(f"\n  Marked topic as done in topics.json")

    # Summary
    size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  VIDEO READY!")
    print(f"  File: {video_path}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Duration: {duration:.1f}s")
    print(f"  Metadata: {meta_path}")
    print(f"{'='*50}")
    print(f"\nNext: upload to YouTube Studio, copy title/desc from .txt file")
```

- [ ] **Step 3: Test full pipeline end-to-end**

Start Ollama first if not running:

```bash
ollama serve &
```

Run full pipeline:

```bash
cd /Users/avika/Documents/passive-income-executor
python3 scripts/youtube/make_short.py --next
```

Expected output:
```
Next topic: SwiftUI gradient backgrounds in 3 lines

[1/5] Generating script for: SwiftUI gradient backgrounds in 3 lines
  Title: ...
  Narration: ~100 words
  Code: ~10 lines

[2/5] Generating audio with en-US-AndrewNeural...
  Duration: ~35s

[3/5] Generating code image...
  File: /tmp/youtube_shorts/frame.png

[4/5] Assembling video (35.0s)...
  File: /Users/avika/Documents/passive-income-executor/videos/ready/2026-04-04-swiftui-gradient-backgrounds-in-3-lines.mp4

[5/5] Writing metadata...

==================================================
  VIDEO READY!
  File: videos/ready/2026-04-04-swiftui-gradient-backgrounds-in-3-lines.mp4
  Size: ~1.5 MB
  Duration: ~35s
==================================================
```

Verify output:

```bash
open videos/ready/2026-04-04-*.mp4
cat videos/ready/2026-04-04-*.txt
python3 scripts/youtube/make_short.py --list
```

Expected: video plays in QuickTime, metadata txt has title/desc/tags, first topic shows `[DONE]`.

- [ ] **Step 4: Commit**

```bash
git add scripts/youtube/make_short.py
git commit -m "feat(youtube): complete pipeline — video assembly + metadata (stages 4-5)"
```

---

## Task 6: Add to .gitignore + update CLAUDE.md

**Files:**
- Modify: `.gitignore` — add video output dirs
- Modify: `CLAUDE.md` — add YouTube section

- [ ] **Step 1: Update .gitignore**

Add to `.gitignore`:

```
# YouTube Shorts output
videos/ready/*.mp4
videos/ready/*.txt
videos/archive/
/tmp/youtube_shorts/
```

- [ ] **Step 2: Update CLAUDE.md folder structure**

In the `FOLDER STRUCTURE` section of `CLAUDE.md`, add:

```
├── scripts/
│   ├── youtube/           ← YouTube Shorts generation pipeline
```

And add to the top-level:

```
├── videos/
│   ├── ready/             ← Generated shorts (MP4 + metadata)
│   └── archive/           ← Already uploaded
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore CLAUDE.md
git commit -m "chore: add youtube shorts to gitignore and docs"
```
