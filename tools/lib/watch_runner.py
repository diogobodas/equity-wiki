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


_WATCHES_BLOCK_RE = re.compile(
    r"^watches:\s*\n((?:\s{2,}.*\n?)+)", re.MULTILINE
)
_ENTRY_START_RE = re.compile(r"^\s*-\s*query:\s*(.+?)\s*$")
_FIELD_RE = re.compile(r"^\s*(query|sites|cadence):\s*(.+?)\s*$")


def parse_watches_frontmatter(page_path: Path) -> list[dict]:
    """Extract the `watches:` array from a page's YAML frontmatter.

    Limited YAML parser for this specific shape:
        watches:
          - query: "..."
            sites: [a.com, b.com]
            cadence: weekly
    """
    text = page_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---\n", 4)
    if end == -1:
        return []
    fm_text = text[4:end]
    m = _WATCHES_BLOCK_RE.search(fm_text)
    if not m:
        return []
    block = m.group(1)
    entries: list[dict] = []
    current: Optional[dict] = None
    for raw in block.splitlines():
        if not raw.strip():
            continue
        start_match = _ENTRY_START_RE.match(raw)
        if start_match:
            if current is not None:
                entries.append(current)
            current = {"query": start_match.group(1).strip().strip('"').strip("'")}
            continue
        if current is None:
            continue
        field_match = _FIELD_RE.match(raw)
        if not field_match:
            continue
        key, val = field_match.group(1), field_match.group(2).strip()
        if key == "sites" and val.startswith("[") and val.endswith("]"):
            current["sites"] = [s.strip() for s in val[1:-1].split(",") if s.strip()]
        elif key == "cadence":
            current["cadence"] = val
        elif key == "query":
            current["query"] = val.strip('"').strip("'")
    if current is not None:
        entries.append(current)
    return entries


def search_web(query: str, sites: list[str], today: date) -> list[dict]:
    """Invoke `claude --print` with a WebSearch-scoped prompt; return hits.

    Returned shape: [{url, title, snippet, published_date}].
    """
    site_clause = " OR ".join(f"site:{s}" for s in sites) if sites else ""
    full_query = f"{query} {site_clause}".strip()
    prompt = (
        "You are a web search agent. Use WebSearch with this exact query:\n"
        f'"{full_query}"\n\n'
        "Return ONLY a JSON array (no prose, no backticks) of the 10 most recent hits. "
        'Each item: {"url": "...", "title": "...", "snippet": "...", '
        '"published_date": "YYYY-MM-DD"}. If the page does not disclose a publication '
        'date, use the empty string. Today is '
        f"{today.isoformat()}."
    )
    try:
        proc = subprocess.run(
            ["claude", "--print", "--permission-mode", "bypassPermissions"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180,
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"search_web error: {e}", file=sys.stderr)
        return []
    out = proc.stdout.strip()
    m = re.search(r"\[\s*\{.*\}\s*\]", out, re.DOTALL)
    if not m:
        return []
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return []


def run_watch(
    page_path: Path,
    state_dir: Path,
    today: Optional[date] = None,
    force: bool = False,
) -> list[dict]:
    """Run all watch entries for a page; return aggregated hits."""
    if today is None:
        today = date.today()
    entries = parse_watches_frontmatter(page_path)
    if not entries:
        return []
    page_slug = page_path.stem
    state = load_state(state_dir, page_slug)
    existing_by_query: dict[str, dict] = {
        e["query"]: e for e in state.get("entries", [])
    }

    aggregated_hits: list[dict] = []
    new_entries_state: list[dict] = []
    for entry in entries:
        query = entry["query"]
        cadence = entry.get("cadence", "monthly")
        sites = entry.get("sites", [])
        prior = existing_by_query.get(query, {})
        last_run_raw = prior.get("last_run")
        last_run = date.fromisoformat(last_run_raw) if last_run_raw else None
        known_urls: dict = prior.get("known_urls", {})

        if not force and not should_run(cadence, last_run, today=today):
            new_entries_state.append({
                "query": query,
                "sites": sites,
                "cadence": cadence,
                "last_run": last_run_raw,
                "known_urls": known_urls,
            })
            continue

        fresh = search_web(query, sites, today)
        hits = diff_urls(known_urls, fresh)
        for h in hits:
            aggregated_hits.append({
                "page": page_path.name,
                "query": query,
                "cadence": cadence,
                **h,
            })

        updated_known = dict(known_urls)
        for f in fresh:
            url = f.get("url")
            if not url:
                continue
            updated_known[url] = {
                "title": f.get("title", ""),
                "snippet": f.get("snippet", ""),
                "published": f.get("published_date", ""),
            }
        new_entries_state.append({
            "query": query,
            "sites": sites,
            "cadence": cadence,
            "last_run": today.isoformat(),
            "known_urls": updated_known,
        })

    state["entries"] = new_entries_state
    save_state(state_dir, page_slug, state)
    return aggregated_hits


def scan_wiki(root: Path, today: Optional[date] = None, force: bool = False) -> list[dict]:
    if today is None:
        today = date.today()
    skip_dirs = {"docs", "sources", "tools", "tests", "logs", ".git", ".obsidian",
                 ".playwright-cli", ".claude", ".pytest_cache", "__pycache__"}
    state_dir = root / "sources" / "watch_state"
    all_hits: list[dict] = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and entry.name in skip_dirs:
            continue
        if entry.is_file() and entry.suffix == ".md":
            all_hits.extend(run_watch(entry, state_dir, today=today, force=force))
    return all_hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Run watchlist signals for opt-in pages.")
    parser.add_argument("--page", default=None,
                        help="Restrict to a single page (relative path).")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cadence; check all entries.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Wiki root dir.")
    args = parser.parse_args()

    root = Path(args.root)
    today = date.today()
    if args.page:
        page = root / args.page
        if not page.exists():
            print(f"error: page {page} not found", file=sys.stderr)
            return 1
        state_dir = root / "sources" / "watch_state"
        hits = run_watch(page, state_dir, today=today, force=args.force)
    else:
        hits = scan_wiki(root, today=today, force=args.force)

    lint_reports = root / "sources" / "lint_reports"
    lint_reports.mkdir(parents=True, exist_ok=True)
    report_path = lint_reports / f"{today.isoformat()}.md"
    with report_path.open("a", encoding="utf-8") as fh:
        if hits:
            fh.write(f"\n## Watch hits — {today.isoformat()}\n\n")
            for h in hits:
                fh.write(
                    f"- [watch-hit] {h['page']} query=\"{h['query']}\" → {h['url']} "
                    f"(publicado {h.get('published_date','?')}, cadence {h['cadence']})\n"
                )

    log_path = root / "log.md"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(
            f"[watch] {today.isoformat()} hits={len(hits)} "
            f"report=sources/lint_reports/{today.isoformat()}.md\n"
        )
    print(f"Watch: {len(hits)} hits appended to {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
