#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: bash tools/fetch_notion.sh [--discover] [--limit N] [--page <id>]"
    echo ""
    echo "Fetches pages from the Notion Capstone database into sources/undigested/."
    echo "Filters client-side by last_edited_time > state (never re-fetches unchanged)."
    echo ""
    echo "Options:"
    echo "  --discover    List pending pages without writing. Shows count + first 20."
    echo "  --limit N     Only fetch N pages this run (default: all pending)."
    echo "  --page <id>   Force-fetch a single page by id (bypasses state filter)."
    exit 1
}

MODE="fetch_all"
LIMIT=""
FORCE_PAGE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --discover)  MODE="discover"; shift ;;
        --limit)     LIMIT="$2"; shift 2 ;;
        --page)      FORCE_PAGE="$2"; MODE="fetch_one"; shift 2 ;;
        -h|--help)   usage ;;
        *)           echo "Unknown arg: $1" >&2; usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# Load .env if present
if [[ -f .env ]]; then
    set -a; source .env; set +a
fi

echo "=== Notion Fetch ==="
echo "Mode: $MODE  Limit: ${LIMIT:-all}"
echo ""

export MODE LIMIT FORCE_PAGE
python <<'PYEOF'
import os
import sys

from tools.lib.notion_fetch import (
    list_new_or_edited,
    load_config,
    page_to_undigested,
    _summarize_page,
    _request,
)

config = load_config()
mode = os.environ["MODE"]
limit_raw = os.environ.get("LIMIT", "")
limit = int(limit_raw) if limit_raw else None
force_page = os.environ.get("FORCE_PAGE", "")

if mode == "discover":
    pages = list_new_or_edited(config)
    print(f"Pending: {len(pages)} page(s)")
    for p in pages[:20]:
        title = p["title"][:60] if p["title"] else "(no title)"
        print(f"  - {p['id'][:8]} | edited={p['last_edited_time'][:10]} | empresa={p['empresa']:12s} | {title}")
    if len(pages) > 20:
        print(f"  ... and {len(pages) - 20} more")
    sys.exit(0)

if mode == "fetch_one":
    data = _request("GET", f"https://api.notion.com/v1/pages/{force_page}", config)
    meta = _summarize_page(data, config)
    out = page_to_undigested(meta, config)
    print(f"Wrote: {out}")
    sys.exit(0)

# fetch_all (with optional limit)
pages = list_new_or_edited(config)
if limit is not None:
    pages = pages[:limit]
print(f"Processing: {len(pages)} page(s)")
written = errors = 0
for meta in pages:
    try:
        out = page_to_undigested(meta, config)
        print(f"  Wrote: {out.name}")
        written += 1
    except Exception as e:
        print(f"  ERROR on {meta['id'][:8]}: {e}", file=sys.stderr)
        errors += 1
print()
print(f"Total written: {written}/{len(pages)} (errors: {errors})")
print(f"Run 'bash tools/ingest.sh --notion <file>' for each.")
PYEOF
