#!/usr/bin/env bash
set -euo pipefail

# --- Usage ---
usage() {
    echo "Usage: bash tools/reingest_full.sh <TICKER> [--horizon 5y] [--types dfp,itr,release,fato_relevante,previa_operacional]"
    echo ""
    echo "Re-generates full/ files by re-downloading PDFs, extracting, and copying."
    echo "Does NOT re-run the LLM (structured.json and digested.md are kept as-is)."
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

# --- Resolve manifest ---
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

# --- Step 1: Fetch (downloads to undigested/) ---
echo "=== Step 1: Fetching from CVM ==="
bash "$SCRIPT_DIR/fetch.sh" "$TICKER" --horizon "$HORIZON" --types "$TYPES"
echo ""

# --- Step 2: Extract all PDFs/ZIPs ---
echo "=== Step 2: Extracting PDFs ==="
COUNT=0
for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    [[ "$fname" == *_extracted.md ]] && continue
    [[ "$fname" == *.json ]] && continue

    echo "  Extracting: $fname"
    python "$SCRIPT_DIR/lib/pdf_extract.py" "$f" 2>/dev/null || echo "    WARNING: extraction failed for $fname"
    COUNT=$((COUNT + 1))
done
echo "  Extracted $COUNT files"
echo ""

# --- Step 3: Copy to full/ ---
echo "=== Step 3: Copying to full/ ==="
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
    echo "  $fname → $dest"
    COPIED=$((COPIED + 1))
done
echo "  Copied $COPIED files to full/"
echo ""

# --- Step 4: Cleanup undigested/ ---
echo "=== Step 4: Cleanup ==="
for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done

echo ""
echo "=== Re-ingest complete ==="
echo "  Files updated in full/: $COPIED"
echo "  structured.json and digested.md were NOT changed."
echo ""
echo "ACTION REQUIRED after re-ingest for all tickers:"
echo "  - Cury:       bash tools/reingest_full.sh CURY3 --horizon 5y"
echo "  - Direcional: bash tools/reingest_full.sh DIRR3 --horizon 5y"
echo "  - Cyrela:     bash tools/reingest_full.sh CYRE3 --horizon 5y"
