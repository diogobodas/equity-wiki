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

# --- Generic mode ---
if [[ "$1" == "--generic" ]]; then
    shift
    GENERIC_FILE="${1:-}"
    [[ -z "$GENERIC_FILE" ]] && { echo "Usage: bash tools/ingest.sh --generic <file>"; exit 1; }
    [[ ! -f "$GENERIC_FILE" ]] && { echo "ERROR: File not found: $GENERIC_FILE"; exit 1; }

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

    echo "=== Generic Ingest ==="
    echo "File: $GENERIC_FILE"
    echo ""

    invoke_claude() {
        local template="$1"
        local prompt_file
        prompt_file=$(mktemp "${TMPDIR:-/tmp}/ingest_prompt_XXXXXX.md")
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

    FNAME=$(basename "$GENERIC_FILE")
    STEM="${FNAME%.*}"
    echo "Extracting..."
    python "$SCRIPT_DIR/lib/pdf_extract.py" "$GENERIC_FILE" 2>/dev/null || true
    EXTRACTED="${GENERIC_FILE%.*}_extracted.md"
    [[ ! -f "$EXTRACTED" ]] && EXTRACTED="$GENERIC_FILE"

    mkdir -p "$REPO_ROOT/sources/full/generic"
    cp "$EXTRACTED" "$REPO_ROOT/sources/full/generic/${STEM}.md"
    echo "  Copied → sources/full/generic/${STEM}.md"

    FULL_PATH="$REPO_ROOT/sources/full/generic/${STEM}.md"
    invoke_claude "$SCRIPT_DIR/prompts/ingest_generic.md" \
        "{{FULL_PATH}}" "$FULL_PATH" \
        "{{DIGESTED_NAME}}" "$STEM"

    PRODUCED_DIGESTED=$(ls -t "$REPO_ROOT"/sources/digested/*_summary.md 2>/dev/null | head -1)
    if [[ -n "$PRODUCED_DIGESTED" ]]; then
        DNAME=$(basename "$PRODUCED_DIGESTED")
        TODAY=$(date +%Y-%m-%d)
        echo "[wiki-queue] $TODAY | generic | other | ${STEM} | sources/digested/$DNAME" >> "$REPO_ROOT/log.md"
        echo "  Queued: $DNAME"
    fi

    [[ -f "$EXTRACTED" ]] && [[ "$EXTRACTED" != "$GENERIC_FILE" ]] && rm -f "$EXTRACTED"

    echo ""
    echo "=== Generic ingest complete ==="
    echo "  Full: sources/full/generic/${STEM}.md"
    echo "  Run 'bash tools/wiki_update.sh' to update wiki pages."
    exit 0
fi

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
        elif [[ "$fname" == *_previa_operacional_*.pdf ]]; then
            # Prévia is a subset of release — skip if release exists for this period
            previa_period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
            if [[ -f "$REPO_ROOT/sources/full/$EMPRESA/$previa_period/release.md" ]] || \
               ls "$UNDIGESTED"/${TICKER}_${previa_period}_release_*.pdf >/dev/null 2>&1; then
                echo "  Skipping prévia $fname (release exists for $previa_period)"
                rm -f "$f"
                continue
            fi
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
echo "=== Pre-processing PDFs (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"

for f in "${HEAVY_ITR_DFP[@]}" "${HEAVY_RELEASE[@]}" "${LIGHT_FATOS[@]}" "${HEAVY_OTHER[@]}"; do
    echo "  Queued: $(basename "$f")"
    parallel_add "python \"$SCRIPT_DIR/lib/pdf_extract.py\" \"$f\""
done

parallel_wait
echo ""

# Reconstruct extracted paths (pdf_extract.py uses {stem}_extracted.md by default)
EXTRACTED_ITR_DFP=()
for f in "${HEAVY_ITR_DFP[@]}"; do
    stem="${f%.*}"
    EXTRACTED_ITR_DFP+=("${stem}_extracted.md")
done

EXTRACTED_RELEASE=()
for f in "${HEAVY_RELEASE[@]}"; do
    stem="${f%.*}"
    EXTRACTED_RELEASE+=("${stem}_extracted.md")
done

EXTRACTED_FATOS=()
for f in "${LIGHT_FATOS[@]}"; do
    stem="${f%.*}"
    EXTRACTED_FATOS+=("${stem}_extracted.md")
done

EXTRACTED_OTHER=()
for f in "${HEAVY_OTHER[@]}"; do
    stem="${f%.*}"
    EXTRACTED_OTHER+=("${stem}_extracted.md")
done

# --- Helper: build file list for prompt ---
build_file_list() {
    local arr=("$@")
    local list=""
    for f in "${arr[@]}"; do
        list+="- $f"$'\n'
    done
    echo "$list"
}

# --- Helper: copy extracted file to full/ ---
copy_to_full() {
    local extracted_file="$1"
    local empresa="$2"
    local period="$3"
    local tipo="$4"

    local full_dir="$REPO_ROOT/sources/full/$empresa/$period"
    mkdir -p "$full_dir"
    cp "$extracted_file" "$full_dir/${tipo}.md"
    echo "  Copied → sources/full/$empresa/$period/${tipo}.md"
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
    local full_path="$1"
    local doc_type="$2"
    local log_prefix="[heavy:$(basename "$full_path")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "$doc_type" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FULL_PATH}}" "$full_path"

    echo "$log_prefix Done."
}

# --- Helper: ingest one file (light path) ---
ingest_one_light() {
    local full_path="$1"
    local log_prefix="[light:$(basename "$full_path")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_light.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{FULL_PATH}}" "$full_path"

    echo "$log_prefix Done."
}

export -f ingest_one_heavy ingest_one_light invoke_claude copy_to_full
export TICKER EMPRESA SCHEMA_PATH SCRIPT_DIR REPO_ROOT

# --- Step 2b: Copy extracted files to full/ ---
echo "=== Copying extracted files to full/ ==="

for f in "${EXTRACTED_ITR_DFP[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
    copy_to_full "$f" "$EMPRESA" "$period" "$tipo"
done

for f in "${EXTRACTED_RELEASE[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    copy_to_full "$f" "$EMPRESA" "$period" "release"
done

for f in "${EXTRACTED_FATOS[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    if [[ "$fname" == *_fato_relevante_* ]]; then
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
        copy_to_full "$f" "$EMPRESA" "$period" "fato_relevante_${seq}"
    elif [[ "$fname" == *_previa_operacional_* ]]; then
        copy_to_full "$f" "$EMPRESA" "$period" "previa_operacional"
    else
        copy_to_full "$f" "$EMPRESA" "$period" "fato_relevante"
    fi
done

for f in "${EXTRACTED_OTHER[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    stem="${fname%_extracted.*}"
    stem="${stem%.*}"
    copy_to_full "$f" "$EMPRESA" "$period" "$stem"
done

echo ""

# --- Track produced digested files for wiki update ---
DIGESTED_FILES=()

# --- Step 3: Parallel ingest (LLM produces structured + digested only) ---
echo "=== Parallel ingest (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"

# Heavy: ITR/DFP
for f in "${EXTRACTED_ITR_DFP[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
    full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/${tipo}.md"
    parallel_add "ingest_one_heavy \"$full_path\" \"itr/dfp\""
done

# Heavy: releases
for f in "${EXTRACTED_RELEASE[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/release.md"
    parallel_add "ingest_one_heavy \"$full_path\" \"release\""
done

# Heavy: other
for f in "${EXTRACTED_OTHER[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    stem="${fname%_extracted.*}"
    stem="${stem%.*}"
    full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/${stem}.md"
    parallel_add "ingest_one_heavy \"$full_path\" \"other\""
done

# Light: fatos relevantes / prévias
for f in "${EXTRACTED_FATOS[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    if [[ "$fname" == *_fato_relevante_* ]]; then
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
        full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/fato_relevante_${seq}.md"
    elif [[ "$fname" == *_previa_operacional_* ]]; then
        full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/previa_operacional.md"
    else
        full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/fato_relevante.md"
    fi
    parallel_add "ingest_one_light \"$full_path\""
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

# --- Step 6: Append to wiki queue ---
echo "=== Appending to wiki queue ==="
TODAY=$(date +%Y-%m-%d)
for digested in "${DIGESTED_FILES[@]}"; do
    dname=$(basename "$digested" _summary.md)
    suffix="${dname#${EMPRESA}_}"
    tipo=$(echo "$suffix" | rev | cut -d_ -f2- | rev)
    period=$(echo "$suffix" | rev | cut -d_ -f1 | rev)
    echo "[wiki-queue] $TODAY | $EMPRESA | $tipo | $period | $digested" >> "$REPO_ROOT/log.md"
    echo "  Queued: $digested"
done
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
echo "  Wiki queue: ${#DIGESTED_FILES[@]} entries added to log.md"
echo "  Manifest updated: $MANIFEST_PATH"
echo ""
echo "Run 'bash tools/wiki_update.sh' to update wiki pages."
