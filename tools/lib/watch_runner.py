"""Watch Runner — check opt-in watched pages for external signal changes.

Public API:
    load_state(state_dir, page_slug)        -> dict
    save_state(state_dir, page_slug, state) -> None
    should_run(cadence, last_run, today)    -> bool
    diff_urls(known, fresh)                 -> list[dict]  (new or updated)
    run_watch(page_path, state_dir, today)  -> list[dict]  (hits)
    scan_wiki(root, today)                  -> list[dict]  (hits across all pages)

CLI:
    python tools/lib/watch_runner.py [--page P] [--force]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]

CADENCE_DAYS = {"weekly": 7, "monthly": 30, "quarterly": 90}


def load_state(state_dir: Path, page_slug: str) -> dict:
    path = state_dir / f"{page_slug}.json"
    if not path.exists():
        return {"page": page_slug, "entries": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state_dir: Path, page_slug: str, state: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / f"{page_slug}.json"
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def should_run(cadence: str, last_run: Optional[date], today: Optional[date] = None) -> bool:
    if today is None:
        today = date.today()
    if last_run is None:
        return True
    days = CADENCE_DAYS.get(cadence, CADENCE_DAYS["monthly"])
    return (today - last_run) >= timedelta(days=days)


def diff_urls(known: dict, fresh: list[dict]) -> list[dict]:
    """Return fresh entries that are new URLs or have a later published_date than known."""
    hits = []
    for f in fresh:
        url = f.get("url")
        if not url:
            continue
        if url not in known:
            hits.append(f)
            continue
        known_pub = known[url].get("published", "")
        fresh_pub = f.get("published_date", "")
        if fresh_pub and fresh_pub > known_pub:
            hits.append(f)
    return hits


def main() -> int:
    # filled in Task 12
    print("not yet implemented", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
