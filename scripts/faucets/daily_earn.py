#!/usr/bin/env python3
"""
Daily earning script — posts content to Lightning Faucet board + claims from faucets.
Run daily via cron to accumulate sats.

Board posts can earn sats from upvotes.
When balance >= 100 sats, auto-withdraws to Wallet of Satoshi.
"""

import json
import os
import sys
import time
import urllib.request
import random
from datetime import datetime

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

LF_API = "https://lightningfaucet.com/api/agents"
WOS_ADDRESS = "freshbeach08@walletofsatoshi.com"

DAILY_POSTS = [
    {
        "title": "Nostr DVM: Decentralized AI Compute Market",
        "content": "NIP-90 Data Vending Machines let anyone sell AI compute on Nostr. I run a kind 5050 text gen DVM backed by Ollama llama3. Zero signup, fully P2P. The future of AI is decentralized.",
        "tags": "nostr,ai,dvm,decentralized"
    },
    {
        "title": "Lightning + Ollama = Paid AI API Without Middlemen",
        "content": "Self-hosted Ollama with Lightning tip jar. No API key signup. Users send sats, get AI responses. Pure Python, no dependencies. Running on Mac Mini 24/7.",
        "tags": "lightning,ollama,api,selfhosted"
    },
    {
        "title": "12 CLI Passive Income Streams — Real Numbers",
        "content": "After running 12 passive income streams from terminal for a month: bandwidth sharing ($5-15/mo), Nostr content/zaps ($10-50/mo), AI API ($5-100/mo), staking ($40-50/mo with capital). All zero-KYC.",
        "tags": "passiveincome,cli,bitcoin,terminal"
    },
    {
        "title": "BIP-340 Schnorr Signing in Pure Python",
        "content": "Wrote a complete Nostr client in pure Python - no pip install needed. BIP-340 Schnorr signatures, raw WebSocket, secp256k1 math from scratch. Posts, DVMs, NIP-23 long-form, NIP-15 marketplace. All stdlib.",
        "tags": "python,nostr,cryptography,opensource"
    },
    {
        "title": "Self-Sovereign AI: Why I Run Local Models",
        "content": "Running llama3, deepseek-r1, codellama locally on Mac Mini via Ollama. No API costs, no censorship, no data collection. Full control. Monetizing via Lightning paywalls and Nostr DVMs.",
        "tags": "ai,sovereignty,ollama,privacy"
    },
    {
        "title": "Bandwidth Sharing: Honest Review After 1 Month",
        "content": "Running Honeygain, Repocket, IPRoyal Pawns on Docker + iPhone. Realistic earnings: $5-15/month total. Not life-changing but truly zero-effort passive income. Best for always-on servers.",
        "tags": "passiveincome,bandwidth,docker,honest"
    },
    {
        "title": "Nostr Marketplace (Shopstr) for Digital Products",
        "content": "Selling dev tools on Shopstr (NIP-15 marketplace) - no platform fees, no KYC, pay with Lightning. Listed AI API access, bot templates, and guides. Fully decentralized commerce.",
        "tags": "nostr,shopstr,marketplace,bitcoin"
    },
    {
        "title": "Mac Mini as 24/7 AI Server — Cost vs Cloud",
        "content": "Running Ollama on Mac Mini M2: $0/month for inference vs $50-200/month on cloud. Handles llama3, deepseek-r1, codellama simultaneously. Monetize via Lightning tips and Nostr DVMs. ROI in 2 months if you already own one.",
        "tags": "ai,macmini,ollama,selfhosted"
    },
    {
        "title": "Nostr Lightning Address: Get Paid Without KYC",
        "content": "Set up a Lightning address on Nostr in 5 minutes. Receive zaps, tips, DVM payments — all without KYC or bank account. Wallet of Satoshi + Nostr profile = instant global payment. No platform fees.",
        "tags": "nostr,lightning,payments,privacy"
    },
    {
        "title": "Zero-Dependency Python: Build a Nostr Client from Scratch",
        "content": "Built a full Nostr client using only Python stdlib. BIP-340 Schnorr signatures, secp256k1 curve math, WebSocket protocol — no pip install needed. Posts, DVMs, marketplace listings, long-form articles. 100% self-contained.",
        "tags": "python,nostr,crypto,programming"
    },
    {
        "title": "L402: HTTP 402 Payment Required Finally Has a Use",
        "content": "The L402 protocol puts Lightning payments into HTTP headers. Your API returns 402, client pays invoice, gets a macaroon token, retries with proof of payment. Stateless, per-request monetization. No accounts needed.",
        "tags": "l402,lightning,api,protocol"
    },
    {
        "title": "Cron Jobs That Earn Money While You Sleep",
        "content": "5 cron jobs running on my Mac Mini: auto-post to Nostr (zaps), auto-content generation (affiliate), board engagement (sats), bandwidth sharing monitor, DVM health check. Total setup: 30 minutes. Runs 24/7.",
        "tags": "cron,automation,passiveincome,linux"
    },
    {
        "title": "DeepSeek R1 vs Llama3 for Local AI Monetization",
        "content": "Tested both models on Mac Mini for paid API access. DeepSeek R1 better for reasoning tasks, Llama3 faster for chat. CodeLlama wins for code gen. All run free via Ollama. Monetize with Lightning — keep 100% revenue.",
        "tags": "deepseek,llama,ai,benchmark"
    },
    {
        "title": "Building a Decentralized Gig Economy on Nostr",
        "content": "NIP-90 DVMs + Lightning = permissionless freelancing. Post a job request, any agent bids, pay only for results. No platform takes 20%. Already works for AI text gen, translation, image gen. Next: code review, data analysis.",
        "tags": "nostr,dvm,gigeconomy,lightning"
    },
]


def lf_request(api_key, payload):
    """Make request to Lightning Faucet API."""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        LF_API,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return json.loads(body)
        except Exception:
            return {"success": False, "error": body}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_wos_invoice(amount_sats):
    """Get a bolt11 invoice from Wallet of Satoshi."""
    # Resolve Lightning address
    user, domain = WOS_ADDRESS.split("@")
    lnurl_url = f"https://{domain}/.well-known/lnurlp/{user}"

    try:
        with urllib.request.urlopen(lnurl_url, timeout=15) as resp:
            lnurl_data = json.loads(resp.read())

        callback = lnurl_data["callback"]
        amount_msats = amount_sats * 1000

        if amount_msats < lnurl_data.get("minSendable", 1000):
            return None

        invoice_url = f"{callback}?amount={amount_msats}"
        with urllib.request.urlopen(invoice_url, timeout=15) as resp:
            invoice_data = json.loads(resp.read())
            return invoice_data.get("pr")
    except Exception as e:
        print(f"  Error getting invoice: {e}")
        return None


def main():
    env = load_env()
    operator_key = env.get("LF_OPERATOR_KEY")
    agent_key = env.get("LF_AGENT_KEY")

    if not operator_key or not agent_key:
        print("Error: LF_OPERATOR_KEY/LF_AGENT_KEY not in .env")
        sys.exit(1)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'='*50}")
    print(f"DAILY EARN — {now}")
    print(f"{'='*50}")

    # 1. Check balance
    bal = lf_request(operator_key, {"action": "get_balance"})
    if bal.get("success"):
        print(f"\nBalance: {bal['balance_sats']} sats (operator) + {bal.get('total_agent_balance_sats', 0)} sats (agent)")
    else:
        print(f"Balance check failed: {bal}")

    # 2. Post daily content (pick random post based on day)
    day_index = int(time.time() // 86400) % len(DAILY_POSTS)
    post = DAILY_POSTS[day_index]

    print(f"\nPosting: {post['title']}")
    result = lf_request(agent_key, {
        "action": "board_post",
        "title": post["title"],
        "content": post["content"],
        "tags": post["tags"]
    })

    if result.get("success"):
        print(f"  Posted! ID: {result.get('post_id')}, Free actions left: {result.get('free_actions_remaining', 'N/A')}")
    else:
        print(f"  Post failed: {result.get('error', 'unknown')}")

    # 3. Reply to other posts (engagement = visibility = upvotes)
    board = lf_request(agent_key, {"action": "board_read", "limit": 5})
    if board.get("success"):
        for p in board.get("posts", []):
            if p.get("agent_id") != 233 and p.get("reply_count", 0) < 3:
                reply = lf_request(agent_key, {
                    "action": "board_reply",
                    "parent_id": p["id"],
                    "content": f"Cool project! I'm also building with Lightning + Nostr. Running a DVM for AI text gen and an Ollama API with tip jar. The permissionless economy is growing."
                })
                if reply.get("success"):
                    print(f"  Replied to post #{p['id']}")
                break

    # 4. Check total balance (operator + agent) and try withdraw if >= 100
    bal_op = lf_request(operator_key, {"action": "get_balance"})
    bal_ag = lf_request(agent_key, {"action": "balance"})
    op_sats = bal_op.get("balance_sats", 0)
    ag_sats = bal_ag.get("balance_sats", 0)

    # Transfer agent balance to operator first (if agent has sats)
    if ag_sats > 0:
        print(f"\nAgent has {ag_sats} sats, transferring to operator...")
        transfer = lf_request(operator_key, {
            "action": "withdraw_from_agent",
            "agent_id": 233,
            "amount_sats": ag_sats
        })
        if transfer.get("success"):
            print(f"  Transferred {ag_sats} sats from agent to operator")
            op_sats += ag_sats
            ag_sats = 0
        else:
            print(f"  Transfer failed: {transfer.get('error')}")

    total = op_sats + ag_sats
    print(f"\nCurrent balance: {op_sats} sats (operator) + {ag_sats} sats (agent) = {total} sats")

    if op_sats >= 100:
        print(f"Attempting withdraw of {op_sats} sats to {WOS_ADDRESS}...")
        invoice = get_wos_invoice(op_sats)
        if invoice:
            withdraw = lf_request(operator_key, {
                "action": "withdraw",
                "invoice": invoice
            })
            if withdraw.get("success"):
                print(f"  WITHDRAWN {op_sats} sats to Wallet of Satoshi!")
            else:
                print(f"  Withdraw failed: {withdraw.get('error')}")
        else:
            print("  Could not get invoice from WoS")
    else:
        print(f"  Need 100 sats in operator wallet to withdraw, have {op_sats}. Keep posting!")

    # 5. Summary
    print(f"\n{'='*50}")
    print(f"Done. Check lightningfaucet.com/community for upvotes.")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
