#!/usr/bin/env python3
"""
Apify Actor Template — Web Scraper with AI Enhancement

This is a template for creating Apify actors (scrapers) that you can
sell on the Apify marketplace.

Setup:
  1. Create account: https://apify.com/
  2. Install CLI: npm install -g apify-cli
  3. Login: apify login
  4. Create actor: apify create my-scraper
  5. Copy this template into the actor
  6. Deploy: apify push

This template: Scrapes a website and enhances data with Ollama AI.

Actor Input Schema:
  {
    "url": "https://example.com",
    "selector": ".article",
    "aiEnhance": true,
    "maxItems": 10
  }
"""

import json
import urllib.request
import sys
import os
import re
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    """Simple HTML to text converter."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
        if tag in ('p', 'br', 'div', 'h1', 'h2', 'h3', 'h4', 'li'):
            self.text.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data.strip())

    def get_text(self):
        return ' '.join(self.text)


def fetch_page(url):
    """Fetch a web page."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode(errors='replace')


def extract_text(html):
    """Extract text from HTML."""
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()


def extract_links(html, base_url=""):
    """Extract links from HTML."""
    links = re.findall(r'href=["\']([^"\']+)["\']', html)
    return [l if l.startswith('http') else base_url + l for l in links]


def extract_by_pattern(html, pattern):
    """Extract elements matching a CSS-like pattern (simplified)."""
    # Very simplified — supports class and tag matching
    tag_match = re.match(r'\.(\w+)', pattern)
    if tag_match:
        class_name = tag_match.group(1)
        matches = re.findall(
            rf'class=["\'][^"\']*{class_name}[^"\']*["\'][^>]*>(.*?)</\w+>',
            html, re.DOTALL
        )
        return [extract_text(m) for m in matches]

    tag_match = re.match(r'(\w+)', pattern)
    if tag_match:
        tag = tag_match.group(1)
        matches = re.findall(rf'<{tag}[^>]*>(.*?)</{tag}>', html, re.DOTALL)
        return [extract_text(m) for m in matches]

    return []


def ai_enhance(text, prompt="Summarize this text in 2-3 sentences:"):
    """Enhance scraped data with Ollama AI."""
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    data = json.dumps({
        "model": "llama3",
        "prompt": f"{prompt}\n\n{text[:2000]}",
        "stream": False
    }).encode()

    req = urllib.request.Request(
        f"{ollama_url}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result.get("response", "")
    except Exception:
        return ""


def run_scraper(input_data):
    """Main scraper logic."""
    url = input_data.get("url", "")
    selector = input_data.get("selector", "p")
    use_ai = input_data.get("aiEnhance", False)
    max_items = input_data.get("maxItems", 10)

    if not url:
        return {"error": "URL is required"}

    print(f"Scraping: {url}")
    html = fetch_page(url)

    # Extract content
    items = extract_by_pattern(html, selector)[:max_items]

    results = []
    for i, item in enumerate(items):
        entry = {
            "index": i,
            "text": item.strip()[:500],
            "source": url,
        }

        if use_ai and item.strip():
            print(f"  AI enhancing item {i}...")
            entry["ai_summary"] = ai_enhance(item)

        results.append(entry)

    return {
        "url": url,
        "items_found": len(results),
        "data": results,
    }


def main():
    """Run as standalone or as Apify actor."""
    # Check if running in Apify
    apify_input = os.environ.get("APIFY_INPUT_KEY", "")

    if apify_input:
        # Running in Apify — read input from key-value store
        input_path = os.path.join(
            os.environ.get("APIFY_DEFAULT_KEY_VALUE_STORE_DIR", ""),
            "INPUT.json"
        )
        if os.path.exists(input_path):
            with open(input_path) as f:
                input_data = json.load(f)
        else:
            input_data = {"url": "https://example.com"}
    else:
        # Running locally
        if len(sys.argv) > 1:
            input_data = {"url": sys.argv[1], "selector": sys.argv[2] if len(sys.argv) > 2 else "p"}
        else:
            input_data = {
                "url": "https://example.com",
                "selector": "p",
                "aiEnhance": False,
                "maxItems": 5,
            }

    results = run_scraper(input_data)
    print(json.dumps(results, indent=2))

    # If in Apify, save to output
    if apify_input:
        output_dir = os.environ.get("APIFY_DEFAULT_KEY_VALUE_STORE_DIR", "")
        if output_dir:
            with open(os.path.join(output_dir, "OUTPUT.json"), "w") as f:
                json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
