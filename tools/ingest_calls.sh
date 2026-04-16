#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: bash tools/ingest_calls.sh <TICKER> [--concurrency N]"
    echo ""
    echo "Ingests call transcripts from sources/undigested/{empresa}_call_transcript_*.md."
    echo "For each transcript: copy to sources/full/{empresa}/{periodo}/call_transcript.md,"
    echo "invoke claude --print to produce sources/digested/{empresa}_call_transcript_{periodo}_summary.md,"
    echo "update manifest, append [wiki-queue] to log.md, delete from undigested/."
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/lib/parallel.sh"
UNDIGESTED="$REPO_ROOT/sources/undigested"
MANIFESTS="$REPO_ROOT/sources/manifests"
FULL_ROOT="$REPO_ROOT/sources/full"
DIGESTED_ROOT="$REPO_ROOT/sources/digested"
LOG_FILE="$REPO_ROOT/log.md"
PROMPT_TEMPLATE="$SCRIPT_DIR/prompts/ingest_call_transcript.md"

echo "=== Ingest Calls Agent ==="
echo "Ticker: $TICKER"

# --- Resolve manifest ---
EMPRESA=""
MANIFEST_PATH=""
DISPLAY_NAME=""
TICKER_UPPER="${TICKER^^}"
for f in "$MANIFESTS"/*.json; do
    [[ -f "$f" ]] || continue
    if grep -q "\"ticker\": \"$TICKER_UPPER\"" "$f" 2>/dev/null; then
        EMPRESA=$(python -c "import sys,json; print(json.load(open(sys.argv[1]))['empresa'])" "$f")
        DISPLAY_NAME=$(python -c "import sys,json; print(json.load(open(sys.argv[1])).get('display_name',''))" "$f")
        MANIFEST_PATH="$f"
        break
    fi
done
[[ -z "$EMPRESA" ]] && { echo "ERROR: ticker $TICKER_UPPER not found in $MANIFESTS/"; exit 1; }

echo "Empresa:  $EMPRESA ($DISPLAY_NAME)"
echo "Manifest: $MANIFEST_PATH"
echo ""

# --- Scan undigested/ for transcripts ---
TRANSCRIPTS=()
for f in "$UNDIGESTED"/${EMPRESA}_call_transcript_*.md; do
    [[ -f "$f" ]] || continue
    TRANSCRIPTS+=("$f")
done

echo "Found ${#TRANSCRIPTS[@]} transcript(s) for $EMPRESA."
echo ""

if [[ ${#TRANSCRIPTS[@]} -eq 0 ]]; then
    echo "Nothing to ingest. Exiting."
    exit 0
fi

# --- Step 1: Copy to full/ ---
echo "=== Copying transcripts to sources/full/ ==="
for f in "${TRANSCRIPTS[@]}"; do
    fname=$(basename "$f")
    # Extract period: everything between "call_transcript_" and ".md"
    period="${fname#${EMPRESA}_call_transcript_}"
    period="${period%.md}"
    full_dir="$FULL_ROOT/$EMPRESA/$period"
    mkdir -p "$full_dir"
    cp "$f" "$full_dir/call_transcript.md"
    echo "  $fname → sources/full/$EMPRESA/$period/call_transcript.md"
done
echo ""

# --- Step 2: Helper to invoke claude with a per-transcript prompt ---
invoke_claude_transcript() {
    local period="$1"
    local full_path="$2"
    local log_prefix="[call:$period]"

    echo "$log_prefix Starting..."
    local prompt_file
    prompt_file=$(mktemp "${TMPDIR:-/tmp}/ingest_call_prompt_XXXXXX.md")
    python -c "
import sys
template = open(sys.argv[1], encoding='utf-8').read()
subs = {
    '{{TICKER}}':      sys.argv[2],
    '{{EMPRESA}}':     sys.argv[3],
    '{{DISPLAY_NAME}}':sys.argv[4],
    '{{PERIOD}}':      sys.argv[5],
    '{{FULL_PATH}}':   sys.argv[6],
}
for k,v in subs.items():
    template = template.replace(k, v)
open(sys.argv[7], 'w', encoding='utf-8').write(template)
" "$PROMPT_TEMPLATE" "$TICKER_UPPER" "$EMPRESA" "$DISPLAY_NAME" "$period" "$full_path" "$prompt_file"

    cat "$prompt_file" | claude --print \
        --allowedTools "Bash" \
        --permission-mode bypassPermissions
    rm -f "$prompt_file"
    echo "$log_prefix Done."
}
export -f invoke_claude_transcript
export TICKER_UPPER EMPRESA DISPLAY_NAME PROMPT_TEMPLATE

# --- Step 3: Parallel ingest ---
echo "=== Parallel ingest (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"
for f in "${TRANSCRIPTS[@]}"; do
    fname=$(basename "$f")
    period="${fname#${EMPRESA}_call_transcript_}"
    period="${period%.md}"
    full_path="$FULL_ROOT/$EMPRESA/$period/call_transcript.md"
    parallel_add "invoke_claude_transcript \"$period\" \"$full_path\""
done
parallel_wait
echo ""

# --- Step 4: Sequential manifest updates + log + cleanup ---
echo "=== Updating manifest + wiki queue ==="
TODAY=$(date +%Y-%m-%d)
for f in "${TRANSCRIPTS[@]}"; do
    fname=$(basename "$f")
    period="${fname#${EMPRESA}_call_transcript_}"
    period="${period%.md}"
    digested="sources/digested/${EMPRESA}_call_transcript_${period}_summary.md"

    if [[ ! -f "$REPO_ROOT/$digested" ]]; then
        echo "  WARN: digested not produced for $period — skipping manifest update"
        continue
    fi

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type call_transcript --period "$period" \
        --full "sources/full/$EMPRESA/$period/call_transcript.md" \
        --digested "$digested" \
        --log "$LOG_FILE"

    echo "[wiki-queue] $TODAY | $EMPRESA | call_transcript | $period | $digested" >> "$LOG_FILE"
    python "$SCRIPT_DIR/lib/wiki_queue.py" enqueue \
        --empresa "$EMPRESA" --type "call_transcript" --periodo "$period" \
        --digested "$digested" >/dev/null
    rm -f "$f"
    echo "  $period queued, undigested removed"
done

echo ""
echo "=== Ingest calls complete ==="
echo "  Run 'bash tools/wiki_update.sh' to update wiki pages."
