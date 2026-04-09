# YouTube Shorts Auto-Generation Pipeline — Spec

**Date:** 2026-04-04
**Status:** SPEC READY — pending approval

## Overview

Single-command pipeline that generates YouTube Shorts videos from a topic string.
Input: topic → Output: ready-to-upload MP4 (1080x1920, 30-45 sec).

## Command

```bash
python3 scripts/youtube/make_short.py "SwiftUI gradient backgrounds"
```

Optional flags:
- `--voice <name>` — override TTS voice (default: `en-US-AndrewNeural`)
- `--no-cta` — skip call-to-action overlay
- `--list` — list all topics from topics.json
- `--next` — auto-pick next unprocessed topic from topics.json

## Pipeline Steps

### Step 1: Script Generation (Ollama)
- Model: `llama3.2`
- Prompt template generates:
  - `title`: short catchy title (max 50 chars)
  - `narration`: spoken script (~80-120 words = 30-45 sec)
  - `code_snippet`: working code example
  - `cta`: call-to-action text
- Output: JSON with all fields

### Step 2: Text-to-Speech (edge-tts)
- Voice: `en-US-AndrewNeural` (warm, confident)
- Input: narration text from Step 1
- Output: `temp/audio.mp3`
- Get audio duration for video length

### Step 3: Code Image Generation (Pillow)
- Canvas: 1080x1920 (9:16 vertical)
- Dark background (#1e1e2e — Catppuccin Mocha style)
- Layout:
  - Top 15%: Title text (white, bold, 48px)
  - Middle 60%: Code snippet (syntax-highlighted, monospace, 28px)
  - Bottom 15%: CTA text (accent color, 36px)
  - Bottom 10%: padding
- Font: system monospace (Menlo/SF Mono)
- Output: `temp/frame.png`

### Step 4: Video Assembly (ffmpeg)
- Combine static image + audio → MP4
- Format: H.264 video, AAC audio
- Duration: matches audio length
- Resolution: 1080x1920
- FPS: 1 (static image, saves filesize)
- Output: `videos/ready/YYYY-MM-DD-topic-slug.mp4`

### Step 5: Metadata
- Generate `videos/ready/YYYY-MM-DD-topic-slug.txt` with:
  - Title (for YouTube)
  - Description (with links)
  - Tags
  - Ready to copy-paste when uploading

## Content Strategy

### Topic Types (rotate)
1. **SwiftUI tips** (40%) — from Medium series, iOS dev knowledge
2. **iOS dev tricks** (30%) — Xcode, debugging, performance
3. **Product promo** (30%) — Gumroad products, DevToolKit, apps

### Topics File (`scripts/youtube/topics.json`)
```json
[
  {
    "topic": "SwiftUI gradient backgrounds",
    "type": "swiftui",
    "cta": "More SwiftUI tips: link in bio",
    "done": false
  }
]
```

### Promo CTAs
- Nostr AI Toolkit ($19): zerix1.gumroad.com/l/vrblqu
- Ollama API Monetizer ($14): zerix1.gumroad.com/l/pzesvw
- Terminal Income Starter ($9): zerix1.gumroad.com/l/ptikgy
- DevToolKit: devtoolkit-sigma.vercel.app

## File Structure

```
scripts/youtube/
├── make_short.py          # main pipeline script
├── topics.json            # topic queue
└── fonts/                 # fallback fonts if needed

videos/
├── ready/                 # finished MP4 + metadata txt
└── archive/               # already uploaded (move manually)
```

## Dependencies

| Package | Status | Install |
|---------|--------|---------|
| edge-tts | INSTALLED | `pip3 install edge-tts` |
| ffmpeg | INSTALLED | `brew install ffmpeg` |
| Pillow | NEED INSTALL | `pip3 install Pillow` |
| Ollama | INSTALLED | llama3.2 model ready |
| requests | INSTALLED | for Ollama API |

## Upload Workflow (Manual)

1. Run `python3 scripts/youtube/make_short.py --next`
2. Video appears in `videos/ready/`
3. Open YouTube Studio, upload MP4
4. Copy-paste title/description/tags from `.txt` file
5. Move MP4 to `videos/archive/`

Schedule: Mon/Wed/Fri

## Future Upgrades (not now)
- Cron auto-generate batch (Approach C)
- Auto-upload via youtubeuploader (needs Google API audit)
- Animated code typing effect instead of static image
- Multiple scene transitions
- Background music
