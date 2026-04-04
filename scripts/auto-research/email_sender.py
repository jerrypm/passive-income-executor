import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_SENDER, EMAIL_APP_PASSWORD, EMAIL_RECIPIENT

logger = logging.getLogger(__name__)

def _format_item_html(item):
    """Format a single item as HTML."""
    score_data = item.get("ai_score")

    if score_data and isinstance(score_data.get("score"), (int, float)):
        score = score_data["score"]
        reason = score_data.get("reason", "")
        est = score_data.get("estimated_monthly", "?")
        effort = score_data.get("effort", "?")
        return f"""
        <div style="margin-bottom:16px;padding:12px;border-left:4px solid {'#22c55e' if score >= 9 else '#3b82f6'};background:#f8f9fa;">
            <strong>[{score}/10]</strong> {item['title']}<br>
            <span style="color:#666;">Source: {item['source']}</span><br>
            <span style="color:#444;">Why: {reason}</span><br>
            <span style="color:#888;">Est: {est} | Effort: {effort}</span><br>
            <a href="{item['url']}" style="color:#2563eb;">{item['url'][:80]}</a>
        </div>"""
    else:
        return f"""
        <div style="margin-bottom:16px;padding:12px;border-left:4px solid #94a3b8;background:#f8f9fa;">
            <strong>{item['title']}</strong><br>
            <span style="color:#666;">Source: {item['source']}</span><br>
            <span style="color:#444;">{item['snippet'][:150]}</span><br>
            <a href="{item['url']}" style="color:#2563eb;">{item['url'][:80]}</a>
        </div>"""

def _build_html(items, stats, source_results):
    """Build full HTML email body."""
    date_str = datetime.now().strftime("%d %b %Y")
    count = len(items)

    # Separate by score tier
    top_picks = []
    good_finds = []
    unscored = []

    for item in items:
        score_data = item.get("ai_score")
        if score_data and isinstance(score_data.get("score"), (int, float)):
            if score_data["score"] >= 9:
                top_picks.append(item)
            else:
                good_finds.append(item)
        else:
            unscored.append(item)

    # Sort by score descending within tiers
    good_finds.sort(key=lambda x: x.get("ai_score", {}).get("score", 0), reverse=True)

    sections = ""

    if top_picks:
        sections += "<h2 style='color:#22c55e;'>TOP PICKS (Score 9-10)</h2>"
        for item in top_picks:
            sections += _format_item_html(item)

    if good_finds:
        sections += "<h2 style='color:#3b82f6;'>GOOD FINDS (Score 7-8)</h2>"
        for item in good_finds:
            sections += _format_item_html(item)

    if unscored:
        sections += "<h2 style='color:#94a3b8;'>UNSCORED (Ollama unavailable)</h2>"
        for item in unscored:
            sections += _format_item_html(item)

    if not items:
        sections = "<p style='color:#666;font-size:16px;'>No high-score intel today. All items scored below threshold.</p>"

    # Source status
    source_rows = ""
    for name, status in source_results.items():
        icon = "&#9989;" if status > 0 else "&#10060;"
        source_rows += f"<tr><td>{icon} {name}</td><td>{status} items</td></tr>"

    html = f"""
    <html>
    <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:20px;">
        <h1 style="border-bottom:2px solid #333;padding-bottom:8px;">
            Passive Income Intel — {date_str}
        </h1>
        <p style="color:#666;">{count} items passed filter</p>

        {sections}

        <hr style="margin:24px 0;">
        <h3>STATS</h3>
        <table style="border-collapse:collapse;">
            {source_rows}
        </table>
        <p style="color:#888;font-size:12px;">
            Total scraped: {stats.get('raw_count', 0)} |
            After dedup: {stats.get('dedup_count', 0)} |
            After filter: {stats.get('filtered_count', 0)} |
            Ollama: {'ON' if stats.get('ollama_available') else 'OFF (all items sent unfiltered)'}
        </p>
    </body>
    </html>"""

    return html

def send_email(items, stats, source_results):
    """Send digest email via Gmail SMTP.

    Args:
        items: list of filtered items to include
        stats: dict with raw_count, dedup_count, filtered_count, ollama_available
        source_results: dict mapping source name -> item count

    Returns:
        bool — True if sent successfully
    """
    if not EMAIL_SENDER or not EMAIL_APP_PASSWORD or not EMAIL_RECIPIENT:
        logger.error("Email credentials missing in .env — cannot send")
        return False

    date_str = datetime.now().strftime("%d %b %Y")
    count = len(items)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Passive Income Intel — {date_str} ({count} items found)"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    html = _build_html(items, stats, source_results)
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        logger.info(f"Email sent to {EMAIL_RECIPIENT} ({count} items)")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
