#!/usr/bin/env bash
set -euo pipefail

# --- Usage ---
usage() {
    echo "Usage: bash tools/ingest.sh <TICKER>"
    echo ""
    echo "Processes all files in sources/undigested/ for the given ticker."
    echo "Produces full/, structured/, digested/, updates wiki pages, manifest, and log."
    exit 1
}

[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
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

for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    # Skip already-extracted files
    [[ "$fname" == *_extracted.md ]] && continue
    [[ "$fname" == *_extracted.txt ]] && continue

    if [[ "$fname" == *_itr.zip ]] || [[ "$fname" == *_dfp.zip ]] || [[ "$fname" == *_itr.pdf ]] || [[ "$fname" == *_dfp.pdf ]]; then
        HEAVY_ITR_DFP+=("$f")
    elif [[ "$fname" == *_release_*.pdf ]]; then
        HEAVY_RELEASE+=("$f")
    elif [[ "$fname" == *_fato_relevante_*.pdf ]]; then
        LIGHT_FATOS+=("$f")
    else
        echo "WARN: Unknown file type, skipping: $fname"
    fi
done

echo "Found:"
echo "  ITR/DFP (heavy): ${#HEAVY_ITR_DFP[@]}"
echo "  Releases (heavy): ${#HEAVY_RELEASE[@]}"
echo "  Fatos relevantes (light): ${#LIGHT_FATOS[@]}"
echo ""

if [[ ${#HEAVY_ITR_DFP[@]} -eq 0 && ${#HEAVY_RELEASE[@]} -eq 0 && ${#LIGHT_FATOS[@]} -eq 0 ]]; then
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

# --- Track produced digested files for wiki update ---
DIGESTED_FILES=()

# --- Step 3: Ingest heavy ITR/DFP ---
if [[ ${#EXTRACTED_ITR_DFP[@]} -gt 0 ]]; then
    echo "=== Ingesting ITR/DFP (heavy path) ==="
    FILE_LIST=$(build_file_list "${EXTRACTED_ITR_DFP[@]}")

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "itr/dfp" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FILE_LIST}}" "$FILE_LIST"

    # Collect digested files produced
    for f in "${EXTRACTED_ITR_DFP[@]}"; do
        fname=$(basename "$f")
        # Parse period from filename: TEND3_3T25_itr_extracted.md → 3T25
        period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
        tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
        digested="sources/digested/${EMPRESA}_${tipo}_${period}_summary.md"
        DIGESTED_FILES+=("$digested")

        # Update manifest
        python "$SCRIPT_DIR/lib/manifest_update.py" \
            --manifest "$MANIFEST_PATH" \
            --type "$tipo" --period "$period" \
            --full "sources/full/$EMPRESA/$period/${tipo}.md" \
            --structured "sources/structured/$EMPRESA/$period/${tipo}.json" \
            --digested "$digested" \
            --log "$REPO_ROOT/log.md"
    done
    echo ""
fi

# --- Step 4: Ingest heavy releases ---
if [[ ${#EXTRACTED_RELEASE[@]} -gt 0 ]]; then
    echo "=== Ingesting releases (heavy path) ==="
    FILE_LIST=$(build_file_list "${EXTRACTED_RELEASE[@]}")

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "release" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FILE_LIST}}" "$FILE_LIST"

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
    echo ""
fi

# --- Step 5: Ingest light fatos ---
if [[ ${#EXTRACTED_FATOS[@]} -gt 0 ]]; then
    echo "=== Ingesting fatos relevantes (light path) ==="
    FILE_LIST=$(build_file_list "${EXTRACTED_FATOS[@]}")

    invoke_claude "$SCRIPT_DIR/prompts/ingest_light.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{FILE_LIST}}" "$FILE_LIST"

    FATOS_DIGESTED="sources/digested/${EMPRESA}_fatos_relevantes_batch_summary.md"
    DIGESTED_FILES+=("$FATOS_DIGESTED")

    for f in "${EXTRACTED_FATOS[@]}"; do
        fname=$(basename "$f")
        period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')

        python "$SCRIPT_DIR/lib/manifest_update.py" \
            --manifest "$MANIFEST_PATH" \
            --type fato_relevante --period "$period" \
            --full "sources/full/$EMPRESA/$period/fato_relevante_${seq}.md" \
            --digested "$FATOS_DIGESTED" \
            --log "$REPO_ROOT/log.md"
    done
    echo ""
fi

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
for f in "${HEAVY_ITR_DFP[@]}" "${HEAVY_RELEASE[@]}" "${LIGHT_FATOS[@]}"; do
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done
for f in "${EXTRACTED_ITR_DFP[@]}" "${EXTRACTED_RELEASE[@]}" "${EXTRACTED_FATOS[@]}"; do
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done

echo ""
echo "=== Ingest complete ==="
echo "  Processed: $((${#HEAVY_ITR_DFP[@]} + ${#HEAVY_RELEASE[@]} + ${#LIGHT_FATOS[@]})) files"
echo "  Wiki updated: $WIKI_PAGE"
echo "  Manifest updated: $MANIFEST_PATH"
