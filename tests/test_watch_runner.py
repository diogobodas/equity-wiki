"""Tests for tools/lib/watch_runner.py."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.lib import watch_runner as wr  # noqa: E402


def test_state_roundtrip_empty(tmp_path):
    state_dir = tmp_path / "watch_state"
    state = wr.load_state(state_dir, page_slug="demo")
    assert state == {"page": "demo", "entries": []}


def test_state_roundtrip_saves_and_reloads(tmp_path):
    state_dir = tmp_path / "watch_state"
    s = {
        "page": "demo",
        "entries": [
            {
                "query": "q",
                "sites": ["a.com"],
                "cadence": "weekly",
                "last_run": "2026-04-01",
                "known_urls": {"https://x": {"title": "t", "snippet": "s", "published": "2026-04-01"}},
            }
        ],
    }
    wr.save_state(state_dir, page_slug="demo", state=s)
    loaded = wr.load_state(state_dir, page_slug="demo")
    assert loaded == s


def test_cadence_gate_blocks_fresh_weekly(tmp_path):
    last = date(2026, 4, 20)
    today = date(2026, 4, 23)
    assert wr.should_run("weekly", last, today=today) is False


def test_cadence_gate_allows_expired_weekly(tmp_path):
    last = date(2026, 4, 10)
    today = date(2026, 4, 23)
    assert wr.should_run("weekly", last, today=today) is True


def test_cadence_gate_monthly_quarterly():
    today = date(2026, 4, 23)
    # monthly
    assert wr.should_run("monthly", date(2026, 4, 1), today=today) is False
    assert wr.should_run("monthly", date(2026, 2, 28), today=today) is True
    # quarterly
    assert wr.should_run("quarterly", date(2026, 2, 1), today=today) is False
    assert wr.should_run("quarterly", date(2025, 12, 1), today=today) is True


def test_cadence_gate_no_last_run():
    assert wr.should_run("weekly", None, today=date(2026, 4, 23)) is True


def test_diff_urls_empty_known():
    fresh = [
        {"url": "https://a", "title": "A", "snippet": "...", "published_date": "2026-04-20"}
    ]
    hits = wr.diff_urls({}, fresh)
    assert len(hits) == 1
    assert hits[0]["url"] == "https://a"


def test_diff_urls_all_known():
    known = {
        "https://a": {"title": "A", "snippet": "...", "published": "2026-04-20"}
    }
    fresh = [
        {"url": "https://a", "title": "A", "snippet": "...", "published_date": "2026-04-20"}
    ]
    hits = wr.diff_urls(known, fresh)
    assert hits == []


def test_diff_urls_new_and_updated():
    known = {
        "https://a": {"title": "A-old", "snippet": "...", "published": "2026-04-10"}
    }
    fresh = [
        # updated publish date
        {"url": "https://a", "title": "A", "snippet": "...", "published_date": "2026-04-20"},
        # brand new
        {"url": "https://b", "title": "B", "snippet": "...", "published_date": "2026-04-22"},
    ]
    hits = wr.diff_urls(known, fresh)
    urls = {h["url"] for h in hits}
    assert urls == {"https://a", "https://b"}
