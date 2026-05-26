#!/usr/bin/env python3
"""
JRDevHub Daily Autopilot — Fully Automated Blog Income Machine

Runs daily via cron. Generates SEO article with Ollama, inserts affiliate links
and product promotions, auto-posts to Blogger. Zero human intervention.

Setup cron:
  crontab -e
  0 9 * * * cd /Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor/scripts/blogger && /usr/bin/python3 daily_autopilot.py >> /tmp/autopilot.log 2>&1

Manual run:
  /usr/bin/python3 daily_autopilot.py
  /usr/bin/python3 daily_autopilot.py --publish  (langsung publish, bukan draft)
  /usr/bin/python3 daily_autopilot.py --dry-run  (generate only, don't post)
"""

import os
import sys
import json
import random
import re
import urllib.request
import urllib.error
import hashlib
from datetime import datetime, date
from pathlib import Path

# === CONFIG ===
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen3:8b')
SCRIPT_DIR = Path(__file__).parent
ARTICLES_DIR = SCRIPT_DIR.parent.parent / 'articles' / 'auto'
LOG_FILE = SCRIPT_DIR.parent.parent / 'logs' / 'autopilot.log'
HISTORY_FILE = SCRIPT_DIR / '.autopilot_history.json'

# Amazon Affiliate
AMAZON_TAG = 'fullmoonmauli-20'

# CodeCanyon Portfolio
CODECANYON_URL = 'https://codecanyon.net/user/21zerixpm/portfolio'

# === PRODUCT DATABASE ===
PRODUCTS = {
    'gumroad': [
        {
            'name': 'Terminal Income Starter',
            'url': 'https://zerix1.gumroad.com/l/ptikgy',
            'price': '$9',
            'desc': '6 Python scripts for passive income: auto-publish to dev.to/Hashnode/Nostr, crypto staking CLI, bandwidth sharing setup.',
            'tags': ['passive income', 'terminal', 'content', 'publishing', 'python', 'automation', 'staking', 'cli'],
        },
        {
            'name': 'Ollama API Monetizer',
            'url': 'https://zerix1.gumroad.com/l/pzesvw',
            'price': '$14',
            'desc': 'Monetize your local AI models. HTTP API server + RapidAPI wrapper + Lightning Network payments. Zero dependencies.',
            'tags': ['ollama', 'ai', 'api', 'monetize', 'lightning', 'llm', 'local ai', 'rapidapi', 'python'],
        },
        {
            'name': 'Nostr AI Toolkit',
            'url': 'https://zerix1.gumroad.com/l/vrblqu',
            'price': '$19',
            'desc': '8 Python scripts: AI DVM, auto-content bot, Shopstr marketplace, long-form publisher. Pure Python, zero dependencies.',
            'tags': ['nostr', 'ai', 'bot', 'dvm', 'bitcoin', 'decentralized', 'python', 'marketplace'],
        },
        {
            'name': 'InfiXOX Android Game Source',
            'url': 'https://zerix1.gumroad.com/l/pheupx',
            'price': '$14',
            'desc': 'Complete Android puzzle game. Kotlin + Jetpack Compose + Material 3 + AdMob. 24 levels, AI opponent. Published on Play Store.',
            'tags': ['android', 'kotlin', 'jetpack compose', 'game', 'source code', 'admob', 'material3', 'play store'],
        },
    ],
    'codecanyon': {
        'url': CODECANYON_URL,
        'desc': 'Premium mobile app templates: Flutter, SwiftUI, Swift. Cashier app, farming app, news app, barcode scanner, and more.',
        'tags': ['flutter', 'swiftui', 'swift', 'ios', 'android', 'app template', 'source code', 'mobile app'],
    }
}

# === TOPIC DATABASE (200+ topics, organized by category) ===
TOPICS = {
    'ios_swift': [
        "SwiftUI tips every iOS developer should know",
        "How to build a custom TabBar in SwiftUI",
        "Swift concurrency: async/await best practices",
        "Core Data vs SwiftData: which should you use",
        "How to implement push notifications in iOS",
        "Building a REST API client in Swift with URLSession",
        "iOS app architecture: MVVM vs TCA comparison",
        "How to add In-App Purchases to your iOS app",
        "SwiftUI navigation patterns for complex apps",
        "10 Xcode shortcuts that save hours every week",
        "How to use Swift Package Manager effectively",
        "Building offline-first iOS apps with Core Data",
        "UIKit to SwiftUI migration guide",
        "How to implement biometric authentication in iOS",
        "Creating custom animations in SwiftUI",
        "iOS performance optimization techniques",
        "How to handle deep linking in iOS apps",
        "Building a chat interface in SwiftUI",
        "Swift error handling patterns for clean code",
        "How to use Combine framework in real projects",
    ],
    'android_kotlin': [
        "Jetpack Compose beginner guide with examples",
        "Kotlin coroutines: from basics to advanced",
        "How to implement Room database in Android",
        "Material 3 components every Android dev should know",
        "Android app architecture with Clean Architecture",
        "How to add AdMob ads to your Android app",
        "Building a modern Android app with MVVM",
        "Kotlin Flow vs LiveData: when to use which",
        "How to publish your first app on Google Play Store",
        "Android Jetpack libraries every developer needs",
        "How to implement dark mode in Android",
        "Building a todo app with Jetpack Compose",
        "Android testing: unit tests and UI tests guide",
        "How to handle permissions in modern Android",
        "Dependency injection with Hilt in Android",
    ],
    'ai_llm': [
        "How to run AI models locally with Ollama",
        "Building AI agents: a practical guide",
        "Claude API vs OpenAI API comparison",
        "How to fine-tune a language model for your use case",
        "RAG explained: Retrieval Augmented Generation",
        "Building a chatbot with Python and local LLMs",
        "How to use AI for code review automation",
        "Prompt engineering techniques that actually work",
        "Running Llama 3 on your Mac: complete guide",
        "How to build an AI-powered search engine",
        "MCP (Model Context Protocol) explained for developers",
        "How to monetize your AI skills as a developer",
        "Building AI tools with Claude Code and Python",
        "Local AI vs cloud AI: cost and privacy comparison",
        "How to build a document Q&A system with RAG",
    ],
    'developer_tools': [
        "Terminal tools every developer should install",
        "Git advanced techniques: rebase, cherry-pick, bisect",
        "Docker for beginners: the complete guide",
        "How to set up a perfect Mac development environment",
        "VS Code extensions that actually improve productivity",
        "How to automate repetitive tasks with Python",
        "GitHub Actions CI/CD for beginners",
        "Best free APIs every developer should know",
        "How to write better documentation for your projects",
        "Terminal customization: Zsh, Oh My Zsh, Starship",
        "How to use tmux for terminal productivity",
        "Building CLI tools with Python: a practical guide",
        "How to set up a home lab for development",
        "Database tools every developer should know",
        "API testing with curl, httpie, and Postman",
    ],
    'web_dev': [
        "Next.js vs Nuxt.js: which framework to choose",
        "Tailwind CSS tips for cleaner, faster styling",
        "How to build a blog with Next.js and Markdown",
        "TypeScript best practices for 2026",
        "How to deploy a web app for free in 2026",
        "Building REST APIs with FastAPI and Python",
        "Supabase vs Firebase: backend comparison",
        "How to add authentication to any web app",
        "CSS Grid vs Flexbox: when to use which",
        "How to optimize website performance (Core Web Vitals)",
        "Building a SaaS landing page that converts",
        "How to add payments to your web app with Stripe",
        "Progressive Web Apps: complete guide for 2026",
        "SEO for developers: technical optimization guide",
        "How to build a real-time app with WebSockets",
    ],
    'career_money': [
        "How developers can build multiple income streams",
        "Building a developer portfolio that gets noticed",
        "How to sell app templates on CodeCanyon",
        "Freelancing as a developer: getting your first client",
        "How to monetize your tech blog with affiliate marketing",
        "Creating and selling digital products as a developer",
        "How to price your software products and services",
        "Building in public: how sharing your work creates opportunities",
        "How to contribute to open source and build your reputation",
        "Developer side projects that actually generate revenue",
        "How to create a successful Gumroad store for developers",
        "Tech newsletter monetization: from zero to revenue",
        "How to build a personal brand as a developer",
        "Remote work for developers: finding the best opportunities",
        "How to earn passive income with Python scripts",
    ],
    'trending_tech': [
        "Apple Intelligence features developers should know",
        "What WWDC 2026 means for iOS developers",
        "Google Stitch AI design tool: developer review",
        "Cursor vs Claude Code vs GitHub Copilot comparison",
        "The rise of AI coding agents in 2026",
        "Web3 for web2 developers: practical introduction",
        "Edge computing: building apps that run everywhere",
        "How Rust is changing systems programming",
        "The state of cross-platform development in 2026",
        "Wasm (WebAssembly) use cases beyond the browser",
    ],
}

# Amazon product categories for affiliate links
AMAZON_PRODUCTS = {
    'developer_gear': [
        {'name': 'Keychron K2 Pro', 'asin': 'B09MQ36PT7', 'category': 'keyboard'},
        {'name': 'Sony WH-1000XM5', 'asin': 'B0BX2L8PBT', 'category': 'headphones'},
        {'name': 'LG 27UK850-W Monitor', 'asin': 'B078GVTD9N', 'category': 'monitor'},
        {'name': 'Logitech MX Master 3S', 'asin': 'B09HM94VDS', 'category': 'mouse'},
        {'name': 'CalDigit TS4 Dock', 'asin': 'B09GK8LBWS', 'category': 'dock'},
    ],
    'books': [
        {'name': 'Clean Code by Robert Martin', 'asin': 'B001GSTOAM', 'category': 'book'},
        {'name': 'System Design Interview', 'asin': 'B08B3FWYBX', 'category': 'book'},
        {'name': 'Designing Data-Intensive Applications', 'asin': 'B06XPJML5D', 'category': 'book'},
        {'name': 'The Pragmatic Programmer', 'asin': 'B07VRS84D1', 'category': 'book'},
    ],
}


def log(msg):
    """Log with timestamp."""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')


def load_history():
    """Load posted topics history to avoid duplicates."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {'posted': [], 'last_date': None}


def save_history(history):
    """Save history."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def pick_topic(history):
    """Pick a topic that hasn't been posted yet."""
    posted_hashes = set(history.get('posted', []))
    all_topics = []
    for category, topics in TOPICS.items():
        for topic in topics:
            h = hashlib.md5(topic.encode()).hexdigest()[:8]
            if h not in posted_hashes:
                all_topics.append((category, topic, h))

    if not all_topics:
        log("[!] All topics exhausted! Resetting history.")
        history['posted'] = []
        save_history(history)
        return pick_topic(history)

    category, topic, h = random.choice(all_topics)
    log(f"[*] Category: {category} | Topic: {topic}")
    return category, topic, h


def ollama_generate(prompt, temperature=0.7, max_tokens=4000):
    """Generate text using Ollama."""
    url = f"{OLLAMA_URL}/api/generate"
    data = json.dumps({
        'model': OLLAMA_MODEL,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': temperature,
            'num_predict': max_tokens,
        }
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            text = result.get('response', '')
            # Strip thinking tags if model outputs them (qwen3)
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
            return text
    except Exception as e:
        log(f"[!] Ollama error: {e}")
        return None


def generate_meta(topic):
    """Generate SEO title, description, labels."""
    prompt = f"""Generate SEO metadata for a blog article about: "{topic}"

Output EXACTLY in this format (3 lines only, no other text):
TITLE: [engaging click-worthy title, max 60 chars]
DESCRIPTION: [SEO meta description, max 155 chars]
LABELS: [5-7 comma-separated tags]

/no_think"""

    result = ollama_generate(prompt, temperature=0.8, max_tokens=200)
    if not result:
        return {'title': topic, 'description': topic, 'labels': ['tech', 'developer']}

    meta = {'title': topic, 'description': '', 'labels': []}
    for line in result.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('<') or line.startswith('/'):
            continue
        if line.upper().startswith('TITLE:'):
            meta['title'] = line.split(':', 1)[1].strip().strip('"\'')
        elif line.upper().startswith('DESCRIPTION:'):
            meta['description'] = line.split(':', 1)[1].strip().strip('"\'')
        elif line.upper().startswith('LABELS:') or line.upper().startswith('TAGS:'):
            meta['labels'] = [l.strip().strip('"\'') for l in line.split(':', 1)[1].split(',') if l.strip()]

    # Fallback
    if not meta['labels']:
        meta['labels'] = ['tech', 'developer', 'programming']
    if not meta['description']:
        meta['description'] = meta['title']

    return meta


def generate_article_content(topic, category):
    """Generate full HTML article."""
    prompt = f"""You are a senior developer writing for "JR Devhub", a tech blog for iOS/Android/AI developers.

Write a comprehensive blog article about: "{topic}"

STRICT RULES:
- Write in English, professional but conversational
- Output ONLY HTML tags (p, h2, h3, ul, ol, li, strong, em, code, pre, a, table)
- Do NOT output markdown. No # headers, no ** bold, no - lists
- Do NOT include <html>, <head>, <body>, <h1> tags
- Start directly with a <p> tag
- Use <h2> for main sections, <h3> for subsections
- Use <pre><code> for code blocks
- Use <ul><li> for bullet lists, <ol><li> for numbered lists
- Article should be 1000-2000 words
- Include practical code examples where relevant
- Include a conclusion/summary section
- Make it genuinely useful, not generic

/no_think"""

    content = ollama_generate(prompt, temperature=0.7, max_tokens=5000)
    if not content:
        return None

    # Clean up
    content = content.strip()
    # Remove markdown code fences if any
    content = re.sub(r'```html\s*', '', content)
    content = re.sub(r'```\s*$', '', content)
    content = re.sub(r'^```\s*', '', content)
    # Remove any <html>, <body>, <head> tags
    content = re.sub(r'</?(?:html|head|body|!DOCTYPE)[^>]*>', '', content, flags=re.IGNORECASE)
    # Remove h1 tags (Blogger adds title automatically)
    content = re.sub(r'<h1[^>]*>.*?</h1>', '', content, flags=re.IGNORECASE | re.DOTALL)

    return content.strip()


def find_relevant_product(topic, category):
    """Find the most relevant Gumroad product for this topic."""
    topic_lower = topic.lower() + ' ' + category.lower()
    best = None
    best_score = 0

    for product in PRODUCTS['gumroad']:
        score = sum(1 for tag in product['tags'] if tag in topic_lower)
        if score > best_score:
            best_score = score
            best = product

    # If no strong match, pick based on category
    if best_score == 0:
        category_map = {
            'ios_swift': PRODUCTS['gumroad'][3],      # InfiXOX (has iOS relevance via Kotlin comparison)
            'android_kotlin': PRODUCTS['gumroad'][3],  # InfiXOX
            'ai_llm': PRODUCTS['gumroad'][1],          # Ollama API Monetizer
            'developer_tools': PRODUCTS['gumroad'][0], # Terminal Income Starter
            'web_dev': PRODUCTS['gumroad'][0],         # Terminal Income Starter
            'career_money': PRODUCTS['gumroad'][0],    # Terminal Income Starter
            'trending_tech': PRODUCTS['gumroad'][1],   # Ollama API Monetizer
        }
        best = category_map.get(category, random.choice(PRODUCTS['gumroad']))

    return best


def build_product_cta(product, category):
    """Build HTML CTA block for product promotion."""
    cta = f'''<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:24px 28px;border-radius:8px;margin:2em 0;color:#fff;">
<p style="font-family:'Josefin Sans',sans-serif;font-size:18px;font-weight:700;margin:0 0 8px;color:#fff;">Check Out: {product['name']} ({product['price']})</p>
<p style="margin:0 0 14px;font-size:14px;opacity:0.9;line-height:1.6;">{product['desc']}</p>
<a href="{product['url']}" target="_blank" rel="noopener" style="display:inline-block;background:#ff7f24;color:#fff !important;font-family:'Montserrat',sans-serif;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none !important;font-size:13px;text-transform:uppercase;border-bottom:none !important;">Get It on Gumroad</a>'''

    # Add CodeCanyon link for mobile app topics
    if category in ['ios_swift', 'android_kotlin']:
        cta += f'''
<a href="{CODECANYON_URL}" target="_blank" rel="noopener" style="display:inline-block;background:rgba(255,255,255,0.2);color:#fff !important;font-family:'Montserrat',sans-serif;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none !important;font-size:13px;text-transform:uppercase;margin-left:8px;border-bottom:none !important;">More Templates on CodeCanyon</a>'''

    cta += '\n</div>'
    return cta


def build_amazon_section(category):
    """Build Amazon affiliate product recommendation based on category."""
    if category not in ['developer_tools', 'ios_swift', 'android_kotlin', 'trending_tech']:
        return ''

    products = AMAZON_PRODUCTS['developer_gear'][:3]
    if random.random() > 0.5:
        products = AMAZON_PRODUCTS['books'][:3]

    items = ''
    for p in products:
        link = f"https://www.amazon.com/dp/{p['asin']}?tag={AMAZON_TAG}"
        items += f'<li><a href="{link}" target="_blank" rel="nofollow noopener" style="color:#c62641;">{p["name"]}</a></li>\n'

    return f'''<div style="background:#fff8f0;border-left:4px solid #ff7f24;padding:16px 20px;border-radius:0 8px 8px 0;margin:2em 0;">
<p style="font-family:'Josefin Sans',sans-serif;font-size:15px;font-weight:700;margin:0 0 10px;color:#333;">Recommended Developer Gear</p>
<ul style="margin:0;padding-left:20px;font-size:14px;line-height:1.8;">
{items}</ul>
<p style="font-size:11px;color:#999;margin:8px 0 0;">As an Amazon Associate I earn from qualifying purchases.</p>
</div>'''


def build_footer():
    """Standard article footer."""
    return '''<p style="margin-top:2em;padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;font-size:15px;">
<strong>Found this useful?</strong> Share it with a developer friend and drop a comment below.
</p>'''


def build_full_article(meta, content, product_cta, amazon_section, hero_image):
    """Assemble full article HTML with metadata comment."""
    labels_str = ', '.join(meta['labels'])

    html = f"""<!--
TITLE: {meta['title']}
SEARCH DESCRIPTION: {meta['description']}
LABELS: {labels_str}
-->

{hero_image}

{content}

{amazon_section}

{product_cta}

{build_footer()}"""

    # Replace HTML entities that break Blogger XML parser
    html = html.replace('&mdash;', '\u2014')
    html = html.replace('&ndash;', '\u2013')
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&hellip;', '\u2026')

    return html


def get_hero_image(category):
    """Get a relevant Unsplash hero image for the category."""
    images = {
        'ios_swift': ('photo-1512941937669-90a1b58e7e9c', 'iPhone and MacBook development setup'),
        'android_kotlin': ('photo-1607252650355-f7fd0460ccdb', 'Android phone showing app'),
        'ai_llm': ('photo-1677442136019-21780ecad995', 'AI neural network visualization'),
        'developer_tools': ('photo-1629654297299-c8506221ca97', 'Developer workspace with terminal'),
        'web_dev': ('photo-1547658719-da2b51169166', 'Web development code on screen'),
        'career_money': ('photo-1553877522-43269d4ea984', 'Developer working at desk'),
        'trending_tech': ('photo-1620712943543-bcc4688e7485', 'AI brain concept'),
    }

    photo_id, alt = images.get(category, ('photo-1629654297299-c8506221ca97', 'Developer workspace'))

    return f'''<img style="width:100%;border-radius:8px;margin:0 0 1.5em;box-shadow:0 2px 12px rgba(0,0,0,0.08);" src="https://images.unsplash.com/{photo_id}?w=800&q=80" alt="{alt}" />'''


def save_article(html, meta):
    """Save article to file."""
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime('%Y%m%d')
    slug = re.sub(r'[^a-z0-9]+', '-', meta['title'].lower()).strip('-')[:50]
    filename = f"{date_str}-{slug}.html"
    filepath = ARTICLES_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return filepath


def post_to_blogger(filepath, is_draft=True):
    """Post article to Blogger via API."""
    sys.path.insert(0, str(SCRIPT_DIR))
    from post_to_blogger import authenticate, get_blog_id, parse_article_html, post_article

    service = authenticate()
    blog_id = get_blog_id(service)
    article = parse_article_html(filepath)
    result = post_article(service, blog_id, article, is_draft=is_draft)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description='JRDevHub Daily Autopilot')
    parser.add_argument('--publish', action='store_true', help='Publish immediately (default: draft)')
    parser.add_argument('--dry-run', action='store_true', help='Generate only, do not post')
    parser.add_argument('--topic', '-t', help='Override topic (instead of random)')
    parser.add_argument('--category', '-c', help='Override category')
    args = parser.parse_args()

    log("=" * 60)
    log("JRDevHub Daily Autopilot Starting")
    log("=" * 60)

    # Check Ollama
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            models = json.loads(resp.read())
            log(f"[+] Ollama OK. Model: {OLLAMA_MODEL}")
    except Exception as e:
        log(f"[!] Ollama not running: {e}")
        log("    Start with: ollama serve")
        sys.exit(1)

    # Pick topic
    history = load_history()

    if args.topic:
        category = args.category or 'trending_tech'
        topic = args.topic
        topic_hash = hashlib.md5(topic.encode()).hexdigest()[:8]
    else:
        category, topic, topic_hash = pick_topic(history)

    log(f"[*] Topic: {topic}")
    log(f"[*] Category: {category}")

    # Generate meta
    log("[*] Generating SEO metadata...")
    meta = generate_meta(topic)
    log(f"    Title: {meta['title']}")
    log(f"    Labels: {', '.join(meta['labels'])}")

    # Generate content
    log("[*] Generating article content...")
    content = generate_article_content(topic, category)
    if not content:
        log("[!] Failed to generate content. Aborting.")
        sys.exit(1)
    log(f"    Generated {len(content)} chars")

    # Build components
    product = find_relevant_product(topic, category)
    product_cta = build_product_cta(product, category)
    amazon_section = build_amazon_section(category)
    hero_image = get_hero_image(category)

    log(f"    Product CTA: {product['name']}")
    log(f"    Amazon section: {'Yes' if amazon_section else 'No'}")

    # Assemble and save
    full_html = build_full_article(meta, content, product_cta, amazon_section, hero_image)
    filepath = save_article(full_html, meta)
    log(f"[+] Saved: {filepath}")

    # Post to Blogger
    if not args.dry_run:
        is_draft = not args.publish
        log(f"[*] Posting to Blogger ({'DRAFT' if is_draft else 'PUBLISH'})...")
        try:
            result = post_to_blogger(filepath, is_draft=is_draft)
            log(f"[+] Posted! ID: {result.get('id', 'N/A')}")
        except Exception as e:
            log(f"[!] Post failed: {e}")
            log("    Article saved locally. Post manually later.")
    else:
        log("[*] Dry run — not posting to Blogger")

    # Update history
    history['posted'].append(topic_hash)
    history['last_date'] = str(date.today())
    save_history(history)

    log(f"[+] Done! Topics remaining: {sum(len(t) for t in TOPICS.values()) - len(history['posted'])}")
    log("=" * 60)


if __name__ == '__main__':
    main()
