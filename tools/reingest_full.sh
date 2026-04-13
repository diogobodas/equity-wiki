#!/usr/bin/env bash
set -euo pipefail

# Re-generates full/ files by downloading ALL docs directly from CVM,
# extracting PDFs, and copying to full/. Ignores the manifest — downloads
# everything within the horizon, even if already ingested.
#
# Does NOT re-run the LLM (structured.json and digested.md are kept as-is).
# Requires CVM-API running at localhost:8100.

usage() {
    echo "Usage: bash tools/reingest_full.sh <TICKER> [--horizon 5y] [--types dfp,itr,release,fato_relevante,previa_operacional]"
    echo ""
    echo "Re-generates full/ files by downloading ALL docs from CVM (ignores manifest),"
    echo "extracting PDFs, and copying to full/. Does NOT invoke the LLM."
    echo ""
    echo "Requires CVM-API running at localhost:8100."
    exit 1
}

[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

HORIZON="5y"
TYPES="dfp,itr,release,fato_relevante,previa_operacional"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --horizon)  HORIZON="$2"; shift 2 ;;
        --types)    TYPES="$2"; shift 2 ;;
        *)          echo "Unknown arg: $1"; usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFESTS="$REPO_ROOT/sources/manifests"
UNDIGESTED="$REPO_ROOT/sources/undigested"

echo "=== Re-ingest Full ==="
echo "Ticker:  $TICKER"
echo "Horizon: $HORIZON"
echo "Types:   $TYPES"
echo ""

# --- Resolve empresa from manifest ---
EMPRESA=""
for f in "$MANIFESTS"/*.json; do
    [[ -f "$f" ]] || continue
    if grep -q "\"$TICKER\"" "$f" 2>/dev/null; then
        EMPRESA=$(basename "$f" .json)
        break
    fi
done

if [[ -z "$EMPRESA" ]]; then
    echo "ERROR: No manifest found for $TICKER."
    exit 1
fi

echo "Empresa: $EMPRESA"
echo ""

# --- Compute horizon start date ---
compute_horizon_from() {
    local h="$1"
    local num="${h%[ym]}"
    local unit="${h: -1}"
    if [[ "$unit" == "y" ]]; then
        local current_year current_month current_day
        current_year=$(date +%Y)
        current_month=$(date +%m)
        current_day=$(date +%d)
        echo "$((current_year - num))-${current_month}-${current_day}"
    elif [[ "$unit" == "m" ]]; then
        python -c "
from datetime import datetime
from dateutil.relativedelta import relativedelta
d = datetime.now() - relativedelta(months=$num)
print(d.strftime('%Y-%m-%d'))
"
    else
        echo "$(date +%Y-%m-%d)"
    fi
}

HORIZON_FROM=$(compute_horizon_from "$HORIZON")
echo "Date range: $HORIZON_FROM → today"
echo ""

# --- Step 1: List ALL documents from CVM (ignoring manifest) ---
echo "=== Step 1: Listing documents from CVM ==="
LIST_JSON=$(python "$SCRIPT_DIR/lib/cvm_fetch.py" list "$TICKER" --types "$TYPES" --from "$HORIZON_FROM" 2>&1)

# Deduplicate: keep only the latest version per (tipo, periodo)
LIST_JSON=$(echo "$LIST_JSON" | python -c "
import sys, json
docs = json.load(sys.stdin)
seen = {}
for doc in docs:
    key = (doc['tipo'], doc['periodo'])
    if key not in seen:
        seen[key] = doc  # list is already sorted most-recent-first
deduped = list(seen.values())
print(json.dumps(deduped, ensure_ascii=False))
")

DOC_COUNT=$(echo "$LIST_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin)))")
echo "  Found $DOC_COUNT documents (deduplicated by tipo+periodo)"

if [[ "$DOC_COUNT" == "0" ]]; then
    echo "Nothing to re-ingest."
    exit 0
fi

# --- Step 2: Download ALL documents ---
echo "=== Step 2: Downloading $DOC_COUNT documents ==="
mkdir -p "$UNDIGESTED"

# Download all documents (uses separate Python script to avoid MSYS path issues)
echo "$LIST_JSON" | python "$SCRIPT_DIR/lib/reingest_download.py" "$TICKER" "$UNDIGESTED"

echo ""

# --- Step 3: Extract all PDFs/ZIPs ---
echo "=== Step 3: Extracting PDFs ==="
source "$SCRIPT_DIR/lib/parallel.sh"
parallel_init 4

EXTRACT_COUNT=0
for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    [[ "$fname" == *_extracted.md ]] && continue
    [[ "$fname" == *.json ]] && continue

    echo "  Queued: $fname"
    parallel_add "python \"$SCRIPT_DIR/lib/file_extract.py\" \"$f\""
    EXTRACT_COUNT=$((EXTRACT_COUNT + 1))
done

parallel_wait
echo "  Extracted $EXTRACT_COUNT files"
echo ""

# --- Step 4: Copy to full/ ---
echo "=== Step 4: Copying to full/ ==="
COPIED=0
for f in "$UNDIGESTED"/${TICKER}_*_extracted.md; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")

    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    full_dir="$REPO_ROOT/sources/full/$EMPRESA/$period"
    mkdir -p "$full_dir"

    if [[ "$fname" == *_itr_* ]]; then
        dest="$full_dir/itr.md"
    elif [[ "$fname" == *_dfp_* ]]; then
        dest="$full_dir/dfp.md"
    elif [[ "$fname" == *_release_* ]]; then
        dest="$full_dir/release.md"
    elif [[ "$fname" == *_fato_relevante_* ]]; then
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
        dest="$full_dir/fato_relevante_${seq}.md"
    elif [[ "$fname" == *_previa_operacional_* ]]; then
        dest="$full_dir/previa_operacional.md"
    else
        stem="${fname%_extracted.*}"
        dest="$full_dir/${stem}.md"
    fi

    cp "$f" "$dest"
    echo "  → sources/full/$EMPRESA/$period/$(basename "$dest")"
    COPIED=$((COPIED + 1))
done
echo "  Copied $COPIED files to full/"
echo ""

# --- Step 5: Cleanup undigested/ ---
echo "=== Step 5: Cleanup ==="
CLEANED=0
for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    rm -f "$f"
    CLEANED=$((CLEANED + 1))
done
echo "  Removed $CLEANED files from undigested/"

echo ""
echo "=== Re-ingest complete ==="
echo "  Documents found on CVM: $DOC_COUNT"
echo "  Files copied to full/:  $COPIED"
echo "  structured.json and digested.md were NOT changed."
