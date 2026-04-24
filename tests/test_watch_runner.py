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


def test_run_watch_integrates_cadence_and_diff(tmp_path, monkeypatch):
    # Page with one watch entry, no prior state
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "type: concept\n"
        "watches:\n"
        "  - query: test query\n"
        "    sites: [example.com]\n"
        "    cadence: weekly\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )
    state_dir = tmp_path / "watch_state"

    def fake_search(query, sites, today):
        return [
            {"url": "https://example.com/a", "title": "A", "snippet": "...",
             "published_date": "2026-04-22"},
        ]

    monkeypatch.setattr(wr, "search_web", fake_search)
    hits = wr.run_watch(page, state_dir, today=date(2026, 4, 23))
    assert len(hits) == 1
    assert hits[0]["url"] == "https://example.com/a"
    # Second run: state now has the URL -> cadence blocks
    hits2 = wr.run_watch(page, state_dir, today=date(2026, 4, 23))
    assert hits2 == []


def test_parse_watches_frontmatter_multiline_sites(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "watches:\n"
        "  - query: q1\n"
        "    sites:\n"
        "      - planalto.gov.br\n"
        "      - mattosfilho.com.br\n"
        "    cadence: weekly\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )
    entries = wr.parse_watches_frontmatter(page)
    assert len(entries) == 1
    assert entries[0]["query"] == "q1"
    assert entries[0]["sites"] == ["planalto.gov.br", "mattosfilho.com.br"]
    assert entries[0]["cadence"] == "weekly"


def test_parse_watches_frontmatter_multiple_entries(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "watches:\n"
        "  - query: first\n"
        "    sites: [a.com]\n"
        "    cadence: weekly\n"
        "  - query: second\n"
        "    sites:\n"
        "      - b.com\n"
        "      - c.com\n"
        "    cadence: monthly\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )
    entries = wr.parse_watches_frontmatter(page)
    assert len(entries) == 2
    assert entries[0]["query"] == "first"
    assert entries[0]["sites"] == ["a.com"]
    assert entries[1]["query"] == "second"
    assert entries[1]["sites"] == ["b.com", "c.com"]


def test_run_watch_writes_to_separate_watch_report(tmp_path, monkeypatch):
    # Verify the watch report goes to YYYY-MM-DD-watch.md, NOT YYYY-MM-DD.md
    # (critical fix preventing lint.sh from clobbering watch hits)
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "watches:\n"
        "  - query: q\n"
        "    sites: [example.com]\n"
        "    cadence: weekly\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )

    # Mock search_web to return a hit
    def fake_search(query, sites, today):
        return [{"url": "https://example.com/a", "title": "A", "snippet": "...",
                 "published_date": "2026-04-22"}]
    monkeypatch.setattr(wr, "search_web", fake_search)

    state_dir = tmp_path / "sources" / "watch_state"
    today = date(2026, 4, 23)
    hits = wr.run_watch(page, state_dir, today=today)
    assert len(hits) == 1


def test_search_web_json_extraction_handles_prose_wrapped_array(tmp_path, monkeypatch):
    # Simulate claude --print stdout that includes prose before the JSON array
    class FakeProc:
        def __init__(self, stdout):
            self.stdout = stdout
            self.stderr = ""
            self.returncode = 0

    def fake_run(*args, **kwargs):
        return FakeProc(
            'Here is what I found:\n'
            '[{"url": "https://x", "title": "X", "snippet": "s", "published_date": "2026-04-22"}]\n'
            'That is all.'
        )

    monkeypatch.setattr(wr.subprocess, "run", fake_run)
    out = wr.search_web("q", ["example.com"], date(2026, 4, 23))
    assert len(out) == 1
    assert out[0]["url"] == "https://x"
