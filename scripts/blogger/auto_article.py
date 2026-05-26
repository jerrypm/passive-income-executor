#!/usr/bin/env python3
"""
JRDevHub Auto Article Generator & Poster

Generates trending dev articles using Ollama (local AI) and posts to Blogger.
Includes Gumroad product promotions in relevant articles.

Usage:
  # Generate article on a topic
  python3 auto_article.py --topic "best vscode extensions 2026"

  # Generate and auto-post as draft
  python3 auto_article.py --topic "swift concurrency tips" --post --draft

  # Generate from trending topics (random pick)
  python3 auto_article.py --trending --post --draft

  # Schedule with cron (daily at 9am):
  # 0 9 * * * cd /path/to/scripts/blogger && python3 auto_article.py --trending --post --draft
"""

import os
import sys
import json
import random
import argparse
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# === CONFIG ===
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
ARTICLES_DIR = Path(__file__).parent.parent.parent / 'articles'
BLOG_NAME = 'jrdevhub'

# Gumroad products to promote (inserted into relevant articles)
GUMROAD_PRODUCTS = [
    {
        'name': 'Terminal Income Starter',
        'url': 'https://zerix1.gumroad.com/l/ptikgy',
        'price': '$9',
        'description': 'Content publishing, crypto staking, and bandwidth sharing scripts for passive income from your terminal.',
        'keywords': ['passive income', 'terminal', 'content', 'publishing', 'staking', 'python', 'automation'],
    },
    {
        'name': 'Ollama API Monetizer',
        'url': 'https://zerix1.gumroad.com/l/pzesvw',
        'price': '$14',
        'description': 'Turn your local Ollama AI models into a revenue-generating API with Lightning payments and RapidAPI integration.',
        'keywords': ['ollama', 'ai', 'api', 'monetize', 'lightning', 'llm', 'local ai', 'rapidapi'],
    },
    {
        'name': 'Nostr AI Toolkit',
        'url': 'https://zerix1.gumroad.com/l/vrblqu',
        'price': '$19',
        'description': '8 Python scripts to monetize AI on Nostr protocol. DVM, bots, marketplace, and automated content.',
        'keywords': ['nostr', 'ai', 'bot', 'dvm', 'bitcoin', 'decentralized', 'python'],
    },
    {
        'name': 'InfiXOX Android Source Code',
        'url': 'https://zerix1.gumroad.com/l/pheupx',
        'price': '$14',
        'description': 'Complete Android game source code. Kotlin + Jetpack Compose + Material 3 + AdMob. Published on Play Store.',
        'keywords': ['android', 'kotlin', 'jetpack compose', 'game', 'source code', 'admob', 'material3'],
    },
]

# Trending topic pools for auto-generation
TRENDING_TOPICS = [
    # iOS / Swift
    "10 Swift tips every iOS developer should know in 2026",
    "SwiftUI vs UIKit: which should you learn in 2026",
    "How to use async/await in Swift with real examples",
    "Best Xcode extensions for productivity",
    "iOS app architecture patterns compared: MVVM vs TCA vs VIPER",

    # Android / Kotlin
    "Getting started with Jetpack Compose in 2026",
    "Kotlin coroutines explained with practical examples",
    "Best Android libraries every developer should know",
    "How to monetize your Android app with AdMob",
    "Material 3 design system guide for Android developers",

    # Developer Tools
    "10 terminal tools that will boost your productivity",
    "Best mechanical keyboards for programmers",
    "VS Code vs Cursor vs Zed: which editor wins in 2026",
    "Git commands every developer uses daily",
    "Docker for beginners: the only guide you need",

    # AI / LLM
    "How to run AI models locally with Ollama",
    "Building AI-powered tools with Claude API",
    "Local LLMs vs cloud APIs: cost comparison for developers",
    "5 ways developers are using AI to ship faster",
    "How to monetize your local AI setup",

    # Web Dev
    "Next.js 15 features that change everything",
    "Tailwind CSS tips for cleaner code",
    "Best free hosting platforms for developers in 2026",
    "How to build a blog that actually makes money",
    "API design best practices for 2026",

    # Career / Productivity
    "How to build a developer portfolio that gets hired",
    "Passive income ideas for software developers",
    "Best tech certifications worth getting in 2026",
    "How to contribute to open source as a beginner",
    "Developer side projects that actually make money",

    # Nostr / Bitcoin / Web3
    "What is Nostr and why developers should care",
    "How to earn Bitcoin as a developer",
    "Building on Nostr: a developer's guide",
    "Lightning Network for developers explained",
    "Decentralized social media: building with Nostr protocol",
]


def ollama_generate(prompt, model=OLLAMA_MODEL):
    """Generate text using local Ollama."""
    url = f"{OLLAMA_URL}/api/generate"
    data = json.dumps({
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 0.7,
            'num_predict': 4000,
        }
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('response', '')
    except urllib.error.URLError as e:
        print(f"[!] Ollama error: {e}")
        print(f"    Is Ollama running? Try: ollama serve")
        sys.exit(1)


def find_relevant_product(topic):
    """Find the most relevant Gumroad product to promote based on topic keywords."""
    topic_lower = topic.lower()
    best_match = None
    best_score = 0

    for product in GUMROAD_PRODUCTS:
        score = sum(1 for kw in product['keywords'] if kw in topic_lower)
        if score > best_score:
            best_score = score
            best_match = product

    return best_match if best_score > 0 else random.choice(GUMROAD_PRODUCTS)


def generate_product_cta(product):
    """Generate HTML CTA block for a Gumroad product."""
    return f'''
<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:24px 28px;border-radius:8px;margin:2em 0;color:#fff;">
<p style="font-family:'Josefin Sans',sans-serif;font-size:18px;font-weight:700;margin:0 0 8px;color:#fff;">Related: {product['name']} ({product['price']})</p>
<p style="margin:0 0 14px;font-size:14px;opacity:0.9;">{product['description']}</p>
<a href="{product['url']}" target="_blank" rel="noopener" style="display:inline-block;background:#ff7f24;color:#fff;font-family:'Montserrat',sans-serif;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:13px;text-transform:uppercase;">Get It on Gumroad</a>
</div>'''


def generate_article(topic):
    """Generate a full HTML article using Ollama."""
    print(f"[*] Generating article: {topic}")
    print(f"[*] Using model: {OLLAMA_MODEL}")

    prompt = f"""You are a senior software developer writing for a tech blog called "jrdevhub".
Write a comprehensive, engaging blog article about: "{topic}"

Requirements:
- Write in English, professional but conversational tone
- Include practical code examples where relevant (wrap in <pre><code> tags)
- Structure with clear H2 and H3 headings (use <h2> and <h3> tags)
- Include an engaging introduction paragraph
- Include a conclusion/summary section
- Use <p> tags for paragraphs
- Use <ul><li> or <ol><li> for lists
- Use <strong> for emphasis
- Use <code> for inline code
- Article should be 800-1500 words
- Make it genuinely useful, not generic fluff
- Include practical tips the reader can use immediately

Output ONLY the HTML content (no <html>, <head>, <body> tags). Start directly with the first <p> tag.
Do NOT include a <h1> title (Blogger adds this automatically).
Do NOT use markdown. Output pure HTML only."""

    content = ollama_generate(prompt)

    # Clean up any markdown that slipped through
    content = content.strip()
    if content.startswith('```html'):
        content = content[7:]
    if content.startswith('```'):
        content = content[3:]
    if content.endswith('```'):
        content = content[:-3]
    content = content.strip()

    return content


def generate_meta(topic):
    """Generate SEO title and description."""
    prompt = f"""For a blog article about "{topic}", generate:
1. An SEO-optimized, click-worthy title (max 60 chars, engaging)
2. A meta description (max 155 chars, includes keywords)
3. 5-7 relevant labels/tags separated by commas

Output in this EXACT format (no extra text):
TITLE: your title here
DESCRIPTION: your description here
LABELS: tag1, tag2, tag3, tag4, tag5

Output ONLY those 3 lines, nothing else."""

    result = ollama_generate(prompt)

    meta = {'title': topic, 'description': '', 'labels': []}

    for line in result.strip().split('\n'):
        line = line.strip()
        if line.upper().startswith('TITLE:'):
            meta['title'] = line.split(':', 1)[1].strip().strip('"')
        elif line.upper().startswith('DESCRIPTION:'):
            meta['description'] = line.split(':', 1)[1].strip().strip('"')
        elif line.upper().startswith('LABELS:'):
            meta['labels'] = [l.strip() for l in line.split(':', 1)[1].split(',') if l.strip()]

    return meta


def save_article(meta, content, product_cta):
    """Save article as HTML file."""
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

    # Generate filename
    date_str = datetime.now().strftime('%Y%m%d')
    slug = re.sub(r'[^a-z0-9]+', '-', meta['title'].lower()).strip('-')[:50]
    filename = f"{date_str}-{slug}.html"
    filepath = ARTICLES_DIR / filename

    # Build full HTML with metadata comment
    labels_str = ', '.join(meta['labels'])
    full_html = f"""<!--
TITLE: {meta['title']}
SEARCH DESCRIPTION: {meta['description']}
LABELS: {labels_str}
-->

{content}

{product_cta}

<p style="margin-top:2em;padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;font-size:15px;">
<strong>Found this useful?</strong> Share it with a developer friend and drop a comment below.
</p>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"[+] Saved: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description='JRDevHub Auto Article Generator')
    parser.add_argument('--topic', '-t', help='Article topic')
    parser.add_argument('--trending', action='store_true', help='Pick random trending topic')
    parser.add_argument('--post', '-p', action='store_true', help='Auto-post to Blogger after generating')
    parser.add_argument('--draft', '-d', action='store_true', help='Post as draft (use with --post)')
    parser.add_argument('--model', '-m', help=f'Ollama model (default: {OLLAMA_MODEL})')
    args = parser.parse_args()

    if args.model:
        global OLLAMA_MODEL
        OLLAMA_MODEL = args.model

    if not args.topic and not args.trending:
        parser.print_help()
        print("\nExamples:")
        print('  python3 auto_article.py --topic "10 best VS Code extensions"')
        print('  python3 auto_article.py --trending --post --draft')
        sys.exit(1)

    topic = args.topic if args.topic else random.choice(TRENDING_TOPICS)
    print(f"\n{'='*60}")
    print(f"  Topic: {topic}")
    print(f"{'='*60}\n")

    # Generate article
    print("[*] Step 1/3: Generating SEO metadata...")
    meta = generate_meta(topic)
    print(f"    Title: {meta['title']}")
    print(f"    Description: {meta['description']}")
    print(f"    Labels: {', '.join(meta['labels'])}")

    print("\n[*] Step 2/3: Generating article content...")
    content = generate_article(topic)
    print(f"    Generated {len(content)} characters")

    # Find relevant product and generate CTA
    product = find_relevant_product(topic)
    product_cta = generate_product_cta(product)
    print(f"    Product CTA: {product['name']} ({product['price']})")

    print("\n[*] Step 3/3: Saving article...")
    filepath = save_article(meta, content, product_cta)

    # Auto-post if requested
    if args.post:
        print("\n[*] Posting to Blogger...")
        from post_to_blogger import authenticate, get_blog_id, parse_article_html, post_article

        service = authenticate()
        blog_id = get_blog_id(service)
        article = parse_article_html(filepath)
        post_article(service, blog_id, article, is_draft=args.draft)

    print(f"\n{'='*60}")
    print(f"  Done! Article: {filepath.name}")
    if args.post:
        status = "DRAFT" if args.draft else "PUBLISHED"
        print(f"  Status: {status} on Blogger")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
