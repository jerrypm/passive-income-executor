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

    # Stage 2: Generate audio
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = TEMP_DIR / "audio.mp3"
    print(f"\n[2/5] Generating audio with {voice}...")
    duration = generate_audio(script["narration"], audio_path, voice)
    print(f"  Duration: {duration:.1f}s")
    print(f"  File: {audio_path}")

    # Placeholder for stages 3-5 (added in next tasks)
    print("\n[DEBUG] Audio done. Stages 3-5 not yet implemented.")
