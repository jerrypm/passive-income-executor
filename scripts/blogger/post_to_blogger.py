#!/usr/bin/env python3
"""
JRDevHub Blogger Auto-Poster
Posts HTML articles to Blogger via API v3 with OAuth2.

Usage:
  # Post a single article
  python3 post_to_blogger.py --file ../../articles/001-best-mechanical-keyboards-for-mac.html

  # Post as draft (review before publishing)
  python3 post_to_blogger.py --file ../../articles/001-best-mechanical-keyboards-for-mac.html --draft

  # Post all articles in folder
  python3 post_to_blogger.py --folder ../../articles/

  # List all posts
  python3 post_to_blogger.py --list
"""

import os
import sys
import re
import argparse
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# === CONFIG ===
SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_URL = 'https://www.jrdevhub.com/'
SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = SCRIPT_DIR / 'client_secret.json'
TOKEN_FILE = SCRIPT_DIR / 'token.json'


def authenticate():
    """Authenticate with Google OAuth2 and return Blogger service."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                print(f"[!] Client secret not found: {CLIENT_SECRET_FILE}")
                print("    Download from Google Cloud Console > Credentials")
                sys.exit(1)

            print("[*] Opening browser for Google OAuth login...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print("[+] Token saved to", TOKEN_FILE)

    return build('blogger', 'v3', credentials=creds)


def get_blog_id(service):
    """Get blog ID from URL."""
    result = service.blogs().getByUrl(url=BLOG_URL).execute()
    blog_id = result['id']
    print(f"[+] Blog: {result['name']} (ID: {blog_id})")
    return blog_id


def parse_article_html(filepath):
    """Parse article HTML file and extract metadata from comments."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from HTML comment at the top
    metadata = {}
    comment_match = re.search(r'<!--\s*(.*?)\s*-->', content, re.DOTALL)
    if comment_match:
        comment_text = comment_match.group(1)
        for line in comment_text.strip().split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().upper()] = value.strip()

    title = metadata.get('TITLE', Path(filepath).stem)
    description = metadata.get('SEARCH DESCRIPTION', '')
    labels = [l.strip() for l in metadata.get('LABELS', '').split(',') if l.strip()]

    # Remove the comment block from content (Blogger only needs the HTML body)
    html_content = re.sub(r'<!--.*?-->\s*', '', content, count=1, flags=re.DOTALL).strip()

    return {
        'title': title,
        'description': description,
        'labels': labels,
        'content': html_content,
    }


def post_article(service, blog_id, article, is_draft=False):
    """Post an article to Blogger."""
    body = {
        'kind': 'blogger#post',
        'title': article['title'],
        'content': article['content'],
    }

    if article['labels']:
        body['labels'] = article['labels']

    result = service.posts().insert(
        blogId=blog_id,
        body=body,
        isDraft=is_draft
    ).execute()

    status = "DRAFT" if is_draft else "PUBLISHED"
    print(f"[+] {status}: {article['title']}")
    print(f"    URL: {result.get('url', 'N/A')}")
    print(f"    ID: {result['id']}")
    print(f"    Labels: {', '.join(article['labels']) if article['labels'] else 'none'}")
    return result


def list_posts(service, blog_id, max_results=10):
    """List recent posts."""
    result = service.posts().list(
        blogId=blog_id,
        maxResults=max_results,
        status='LIVE',
        fetchBodies=False
    ).execute()

    posts = result.get('items', [])
    if not posts:
        print("[*] No posts found.")
        return

    print(f"\n{'='*60}")
    print(f"Recent Posts ({len(posts)})")
    print(f"{'='*60}")
    for i, post in enumerate(posts, 1):
        labels = ', '.join(post.get('labels', []))
        print(f"  {i}. {post['title']}")
        print(f"     URL: {post['url']}")
        print(f"     Labels: {labels or 'none'}")
        print(f"     Published: {post['published'][:10]}")
        print()


def main():
    parser = argparse.ArgumentParser(description='JRDevHub Blogger Auto-Poster')
    parser.add_argument('--file', '-f', help='Path to HTML article file')
    parser.add_argument('--folder', help='Path to folder with HTML articles')
    parser.add_argument('--draft', '-d', action='store_true', help='Post as draft')
    parser.add_argument('--list', '-l', action='store_true', help='List recent posts')
    args = parser.parse_args()

    if not any([args.file, args.folder, args.list]):
        parser.print_help()
        sys.exit(1)

    print("[*] Authenticating with Google...")
    service = authenticate()
    blog_id = get_blog_id(service)

    if args.list:
        list_posts(service, blog_id)
        return

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"[!] File not found: {filepath}")
            sys.exit(1)

        article = parse_article_html(filepath)
        print(f"\n[*] Posting: {article['title']}")
        print(f"    Labels: {', '.join(article['labels'])}")
        print(f"    Draft: {args.draft}")

        confirm = input("\n    Proceed? (y/n): ").strip().lower()
        if confirm == 'y':
            post_article(service, blog_id, article, is_draft=args.draft)
        else:
            print("[*] Cancelled.")

    if args.folder:
        folder = Path(args.folder)
        if not folder.exists():
            print(f"[!] Folder not found: {folder}")
            sys.exit(1)

        html_files = sorted(folder.glob('*.html'))
        if not html_files:
            print(f"[*] No HTML files found in {folder}")
            return

        print(f"\n[*] Found {len(html_files)} articles:")
        for i, f in enumerate(html_files, 1):
            article = parse_article_html(f)
            print(f"  {i}. {article['title']}")

        confirm = input(f"\n    Post all {len(html_files)} as {'DRAFT' if args.draft else 'PUBLISHED'}? (y/n): ").strip().lower()
        if confirm == 'y':
            for f in html_files:
                article = parse_article_html(f)
                post_article(service, blog_id, article, is_draft=args.draft)
                print()
        else:
            print("[*] Cancelled.")


if __name__ == '__main__':
    main()
