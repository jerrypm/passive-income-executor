import json
import logging
import requests
from pathlib import Path
from config import (
    HISTORY_FILE, OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT,
    SCORE_THRESHOLD, SCORING_PROMPT,
)

logger = logging.getLogger(__name__)

def _load_history():
    """Load set of previously seen URLs."""
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text())
            return set(data)
        except (json.JSONDecodeError, TypeError):
            return set()
    return set()

def _save_history(urls):
    """Save URL set to history file."""
    HISTORY_FILE.write_text(json.dumps(sorted(urls), indent=2))

def deduplicate(items):
    """Remove items already in history.

    Args:
        items: list of scraper result dicts

    Returns:
        list of new items not in history
    """
    history = _load_history()
    new_items = [item for item in items if item["url"] not in history]
    logger.info(f"Dedup: {len(items)} total -> {len(new_items)} new ({len(items) - len(new_items)} duplicates)")
    return new_items

def _score_single(item):
    """Score a single item using Ollama.

    Returns:
        dict with score, reason, estimated_monthly, effort — or None on failure
    """
    prompt = SCORING_PROMPT.format(
        title=item["title"],
        source=item["source"],
        snippet=item["snippet"],
        url=item["url"],
    )

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_TIMEOUT,
        )
        resp.raise_for_status()
        response_text = resp.json().get("response", "")

        # Extract JSON from response (Ollama may add extra text)
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(response_text[start:end])
    except requests.exceptions.ConnectionError:
        logger.warning("Ollama not running — skipping AI scoring")
        return None
    except requests.exceptions.Timeout:
        logger.warning(f"Ollama timeout scoring: {item['title'][:50]}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Ollama response parse error: {e}")
        return None

    return None

def score_items(items):
    """Score all items using Ollama AI.

    Args:
        items: list of scraper result dicts

    Returns:
        tuple of (scored_items, ollama_available)
        scored_items: list of dicts with added 'ai_score' key
        ollama_available: bool — False means Ollama was unreachable
    """
    scored = []
    ollama_available = True

    for i, item in enumerate(items):
        logger.info(f"Scoring {i+1}/{len(items)}: {item['title'][:50]}")
        result = _score_single(item)

        if result is None and i == 0:
            # First item failed — Ollama likely down, skip all scoring
            logger.warning("Ollama appears unavailable — sending all items unscored")
            ollama_available = False
            for it in items:
                it["ai_score"] = None
                scored.append(it)
            return scored, ollama_available

        if result:
            item["ai_score"] = result
        else:
            item["ai_score"] = None

        scored.append(item)

    return scored, ollama_available

def filter_and_update_history(scored_items, ollama_available):
    """Filter items by score threshold and update history.

    Args:
        scored_items: list of items with ai_score
        ollama_available: if False, include all items (no filtering)

    Returns:
        list of items that pass the threshold
    """
    history = _load_history()

    # Add all URLs to history regardless of score
    for item in scored_items:
        history.add(item["url"])
    _save_history(history)

    if not ollama_available:
        logger.info(f"Ollama unavailable — returning all {len(scored_items)} items unfiltered")
        return scored_items

    passed = []
    for item in scored_items:
        score_data = item.get("ai_score")
        if score_data and isinstance(score_data.get("score"), (int, float)):
            if score_data["score"] >= SCORE_THRESHOLD:
                passed.append(item)
        else:
            # Scoring failed for this item — include it to be safe
            passed.append(item)

    logger.info(f"Filter: {len(scored_items)} scored -> {len(passed)} passed (threshold {SCORE_THRESHOLD})")
    return passed

def process(items):
    """Full processing pipeline: dedup -> score -> filter.

    Args:
        items: list of raw scraper result dicts

    Returns:
        tuple of (filtered_items, stats)
        stats: dict with raw_count, dedup_count, filtered_count, ollama_available
    """
    stats = {"raw_count": len(items)}

    new_items = deduplicate(items)
    stats["dedup_count"] = len(new_items)

    if not new_items:
        stats["filtered_count"] = 0
        stats["ollama_available"] = True
        return [], stats

    scored, ollama_available = score_items(new_items)
    stats["ollama_available"] = ollama_available

    filtered = filter_and_update_history(scored, ollama_available)
    stats["filtered_count"] = len(filtered)

    return filtered, stats
