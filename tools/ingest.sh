#!/usr/bin/env bash
set -euo pipefail

# --- Usage ---
usage() {
    echo "Usage: bash tools/ingest.sh <TICKER> [--concurrency N]"
    echo ""
    echo "Processes all files in sources/undigested/ for the given ticker."
    echo "Accepts any PDF, ZIP, or XLSX — from fetch agent or dropped manually."
    echo ""
    echo "Options:"
    echo "  --concurrency, -j N   Max parallel ingest agents (default: 4)"
    exit 1
}

[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

CONCURRENCY=4
while [[ $# -gt 0 ]]; do
    case "$1" in
        --concurrency|-j) CONCURRENCY="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/lib/parallel.sh"
UNDIGESTED="$REPO_ROOT/sources/undigested"
MANIFESTS="$REPO_ROOT/sources/manifests"

echo "=== Ingest Agent ==="
echo "Ticker: $TICKER"
echo ""

# --- Resolve manifest ---
EMPRESA=""
MANIFEST_PATH=""
DISPLAY_NAME=""
SCHEMA_PATH="sources/structured/_schemas/incorporadora.json"

for f in "$MANIFESTS"/*.json; do
    [[ -f "$f" ]] || continue
    if grep -q "\"$TICKER\"" "$f" 2>/dev/null; then
        EMPRESA=$(basename "$f" .json)
        MANIFEST_PATH="$f"
        DISPLAY_NAME=$(python -c "import sys,json; print(json.load(open(sys.argv[1])).get('display_name',''))" "$f")
        break
    fi
done

if [[ -z "$EMPRESA" ]]; then
    echo "ERROR: No manifest found for $TICKER. Run fetch first."
    exit 1
fi

echo "Empresa:  $EMPRESA ($DISPLAY_NAME)"
echo "Manifest: $MANIFEST_PATH"
echo ""

# --- Scan undigested/ ---
HEAVY_ITR_DFP=()
HEAVY_RELEASE=()
LIGHT_FATOS=()
HEAVY_OTHER=()

for f in "$UNDIGESTED"/*; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    # Skip already-extracted files
    [[ "$fname" == *_extracted.md ]] && continue
    [[ "$fname" == *_extracted.txt ]] && continue
    # Skip non-ingestable files
    [[ "$fname" == *.json ]] && continue

    # Match ticker-prefixed files (from fetch agent)
    if [[ "$fname" == ${TICKER}_* ]]; then
        if [[ "$fname" =~ _itr[_.] ]] || [[ "$fname" =~ _dfp[_.] ]]; then
            HEAVY_ITR_DFP+=("$f")
        elif [[ "$fname" == *_release_*.pdf ]]; then
            HEAVY_RELEASE+=("$f")
        elif [[ "$fname" == *_fato_relevante_*.pdf ]]; then
            LIGHT_FATOS+=("$f")
        else
            HEAVY_OTHER+=("$f")
        fi
    # Match any other PDF/XLSX/ZIP dropped manually
    elif [[ "$fname" == *.pdf ]] || [[ "$fname" == *.xlsx ]] || [[ "$fname" == *.zip ]]; then
        HEAVY_OTHER+=("$f")
    fi
done

echo "Found:"
echo "  ITR/DFP (heavy): ${#HEAVY_ITR_DFP[@]}"
echo "  Releases (heavy): ${#HEAVY_RELEASE[@]}"
echo "  Fatos relevantes (light): ${#LIGHT_FATOS[@]}"
echo "  Other files (heavy): ${#HEAVY_OTHER[@]}"
echo ""

TOTAL=$((${#HEAVY_ITR_DFP[@]} + ${#HEAVY_RELEASE[@]} + ${#LIGHT_FATOS[@]} + ${#HEAVY_OTHER[@]}))
if [[ $TOTAL -eq 0 ]]; then
    echo "Nothing to ingest. Exiting."
    exit 0
fi

# --- Pre-process all files ---
echo "=== Pre-processing PDFs ==="
EXTRACTED_ITR_DFP=()
EXTRACTED_RELEASE=()
EXTRACTED_FATOS=()

for f in "${HEAVY_ITR_DFP[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_ITR_DFP+=("$OUTPUT")
done

for f in "${HEAVY_RELEASE[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_RELEASE+=("$OUTPUT")
done

for f in "${LIGHT_FATOS[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_FATOS+=("$OUTPUT")
done

EXTRACTED_OTHER=()
for f in "${HEAVY_OTHER[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_OTHER+=("$OUTPUT")
done

echo ""

# --- Helper: build file list for prompt ---
build_file_list() {
    local arr=("$@")
    local list=""
    for f in "${arr[@]}"; do
        list+="- $f"$'\n'
    done
    echo "$list"
}

# --- Helper: build and invoke claude ---
invoke_claude() {
    local template="$1"
    local prompt_file
    prompt_file=$(mktemp "${TMPDIR:-/tmp}/ingest_prompt_XXXXXX.md")

    # Replace placeholders via Python (safe for large content)
    python -c "
import sys
template = open(sys.argv[1]).read()
replacements = {}
i = 2
while i < len(sys.argv) - 1:
    key = sys.argv[i]
    val = sys.argv[i+1]
    replacements[key] = val
    i += 2
for k, v in replacements.items():
    template = template.replace(k, v)
open(sys.argv[-1], 'w', encoding='utf-8').write(template)
" "$template" "${@:2}" "$prompt_file"

    cat "$prompt_file" | claude --print \
        --allowedTools "Bash" \
        --permission-mode bypassPermissions

    rm -f "$prompt_file"
}

# --- Helper: ingest one file (heavy path) ---
ingest_one_heavy() {
    local extracted_file="$1"
    local doc_type="$2"
    local log_prefix="[heavy:$(basename "$extracted_file")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "$doc_type" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FILE_LIST}}" "- $extracted_file"

    echo "$log_prefix Done."
}

# --- Helper: ingest one file (light path) ---
ingest_one_light() {
    local extracted_file="$1"
    local log_prefix="[light:$(basename "$extracted_file")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_light.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{FILE_LIST}}" "- $extracted_file"

    echo "$log_prefix Done."
}

export -f ingest_one_heavy ingest_one_light invoke_claude
export TICKER EMPRESA SCHEMA_PATH SCRIPT_DIR

# --- Track produced digested files for wiki update ---
DIGESTED_FILES=()

# --- Step 3: Parallel ingest ---
echo "=== Parallel ingest (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"

# Heavy: ITR/DFP
for f in "${EXTRACTED_ITR_DFP[@]}"; do
    parallel_add "ingest_one_heavy \"$f\" \"itr/dfp\""
done

# Heavy: releases
for f in "${EXTRACTED_RELEASE[@]}"; do
    parallel_add "ingest_one_heavy \"$f\" \"release\""
done

# Heavy: other
for f in "${EXTRACTED_OTHER[@]}"; do
    parallel_add "ingest_one_heavy \"$f\" \"other\""
done

# Light: fatos relevantes
for f in "${EXTRACTED_FATOS[@]}"; do
    parallel_add "ingest_one_light \"$f\""
done

parallel_wait
echo "=== All ingest agents complete ==="
echo ""

# --- Step 4: Sequential manifest updates ---
echo "=== Updating manifest ==="

for f in "${EXTRACTED_ITR_DFP[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
    digested="sources/digested/${EMPRESA}_${tipo}_${period}_summary.md"
    DIGESTED_FILES+=("$digested")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type "$tipo" --period "$period" \
        --full "sources/full/$EMPRESA/$period/${tipo}.md" \
        --structured "sources/structured/$EMPRESA/$period/${tipo}.json" \
        --digested "$digested" \
        --log "$REPO_ROOT/log.md"
done

for f in "${EXTRACTED_RELEASE[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    digested="sources/digested/${EMPRESA}_release_${period}_summary.md"
    DIGESTED_FILES+=("$digested")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type release --period "$period" \
        --full "sources/full/$EMPRESA/$period/release.md" \
        --structured "sources/structured/$EMPRESA/$period/release.json" \
        --digested "$digested" \
        --log "$REPO_ROOT/log.md"
done

FATOS_DIGESTED="sources/digested/${EMPRESA}_fatos_relevantes_batch_summary.md"
for f in "${EXTRACTED_FATOS[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
    DIGESTED_FILES+=("$FATOS_DIGESTED")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type fato_relevante --period "$period" \
        --full "sources/full/$EMPRESA/$period/fato_relevante_${seq}.md" \
        --digested "$FATOS_DIGESTED" \
        --log "$REPO_ROOT/log.md"
done

for f in "${EXTRACTED_OTHER[@]}"; do
    fname=$(basename "$f")
    stem="${fname%_extracted.*}"
    stem="${stem%.*}"
    digested="sources/digested/${EMPRESA}_other_${stem}_summary.md"
    DIGESTED_FILES+=("$digested")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type release --period "unknown" \
        --full "sources/full/$EMPRESA/other/${stem}.md" \
        --digested "$digested" \
        --log "$REPO_ROOT/log.md" 2>/dev/null || true
done

# Deduplicate DIGESTED_FILES
DIGESTED_FILES=($(printf '%s\n' "${DIGESTED_FILES[@]}" | sort -u))
echo ""

# --- Step 6: Wiki update ---
echo "=== Updating wiki pages ==="
WIKI_PAGE="${EMPRESA}.md"
DIGESTED_LIST=$(build_file_list "${DIGESTED_FILES[@]}")

invoke_claude "$SCRIPT_DIR/prompts/ingest_wiki_update.md" \
    "{{TICKER}}" "$TICKER" \
    "{{EMPRESA}}" "$EMPRESA" \
    "{{WIKI_PAGE}}" "$WIKI_PAGE" \
    "{{DIGESTED_LIST}}" "$DIGESTED_LIST"

echo ""

# --- Step 7: Cleanup ---
echo "=== Cleanup ==="
for f in "${HEAVY_ITR_DFP[@]}" "${HEAVY_RELEASE[@]}" "${LIGHT_FATOS[@]}" "${HEAVY_OTHER[@]}"; do
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done
for f in "${EXTRACTED_ITR_DFP[@]}" "${EXTRACTED_RELEASE[@]}" "${EXTRACTED_FATOS[@]}" "${EXTRACTED_OTHER[@]}"; do
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done

echo ""
echo "=== Ingest complete ==="
echo "  Processed: $TOTAL files"
echo "  Wiki updated: $WIKI_PAGE"
echo "  Manifest updated: $MANIFEST_PATH"
