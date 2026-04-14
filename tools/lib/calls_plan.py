#!/usr/bin/env python3
"""Build the calls plan JSON from a yt-dlp --flat-playlist output.

Reads env vars set by fetch_calls.sh:
    EMPRESA, TICKER_UPPER, YOUTUBE_CHANNEL, HORIZON, CUTOFF,
    UNDIGESTED_PATH, FULL_PATH, RAW_PATH, PLAN_PATH.

RAW_PATH is a PSV file (`|` separator) with `id|title|upload_date` per line.
Writes PLAN_PATH as a JSON object with all entries enriched + deduplicated.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path


PERIOD_PATTERNS = [
    (re.compile(r"\b([1-4])T\s*(\d{2}|20\d{2})\b", re.I), lambda m: f"{m.group(1)}T{m.group(2)[-2:]}"),
    (re.compile(r"\bQ([1-4])\s*(20\d{2})\b", re.I), lambda m: f"{m.group(1)}T{m.group(2)[-2:]}"),
    (re.compile(r"\b([1-4])º?\s*trimestre\s*(?:de\s*)?(20\d{2})\b", re.I), lambda m: f"{m.group(1)}T{m.group(2)[-2:]}"),
]
KEYWORD_RE = re.compile(r"teleconfer[êe]ncia|resultado|call|divulga[çc][ãa]o", re.I)


def extract_period(title: str) -> str | None:
    for rx, fmt in PERIOD_PATTERNS:
        m = rx.search(title)
        if m:
            return fmt(m)
    return None


def score_confidence(title: str, period: str | None) -> str:
    has_kw = bool(KEYWORD_RE.search(title))
    if period and has_kw:
        return "high"
    if period or has_kw:
        return "medium"
    return "low"


def check_existing(empresa: str, period: str, undigested: Path, full: Path) -> tuple[bool, str | None]:
    if (undigested / f"{empresa}_call_transcript_{period}.md").exists():
        return True, "undigested"
    if (full / empresa / period / "call_transcript.md").exists():
        return True, "full"
    return False, None


def main() -> int:
    empresa = os.environ["EMPRESA"]
    ticker_upper = os.environ["TICKER_UPPER"]
    channel = os.environ["YOUTUBE_CHANNEL"]
    horizon = os.environ["HORIZON"]
    cutoff = os.environ["CUTOFF"]
    undigested = Path(os.environ["UNDIGESTED_PATH"])
    full = Path(os.environ["FULL_PATH"])
    raw_path = Path(os.environ["RAW_PATH"])
    plan_path = Path(os.environ["PLAN_PATH"])

    entries: list[dict] = []
    seen_ids: set[str] = set()
    with raw_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("|", 2)
            if len(parts) < 2:
                continue
            vid = parts[0].strip()
            title = parts[1].strip()
            upload_date = parts[2].strip() if len(parts) >= 3 else ""
            if not vid or not title:
                continue
            if vid in seen_ids:
                continue
            seen_ids.add(vid)
            if upload_date and upload_date != "NA" and upload_date < cutoff:
                continue
            period = extract_period(title)
            confidence = score_confidence(title, period)
            existing, layer = (False, None)
            if period:
                existing, layer = check_existing(empresa, period, undigested, full)
            entries.append({
                "video_id": vid,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "title": title,
                "upload_date": upload_date,
                "period": period,
                "confidence": confidence,
                "existing": existing,
                "existing_layer": layer,
                "duplicate_of": None,
            })

    # Duplicate detection: same period, same high/medium confidence.
    # Keep oldest upload_date as primary; mark rest with duplicate_of.
    by_period: dict[str, list[dict]] = {}
    for e in entries:
        if e["period"] and e["confidence"] in ("high", "medium"):
            by_period.setdefault(e["period"], []).append(e)
    for period, group in by_period.items():
        if len(group) <= 1:
            continue
        group_sorted = sorted(group, key=lambda x: x["upload_date"] or "99999999")
        primary = group_sorted[0]["video_id"]
        for e in group_sorted[1:]:
            e["duplicate_of"] = primary

    plan = {
        "empresa": empresa,
        "ticker": ticker_upper,
        "channel": channel,
        "generated_at": date.today().isoformat(),
        "horizon": horizon,
        "entries": entries,
    }
    with plan_path.open("w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
