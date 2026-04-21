#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: bash tools/wiki_update.sh [--full]"
    echo ""
    echo "Updates wiki pages based on digested summaries."
    echo ""
    echo "Options:"
    echo "  --full   Read ALL digesteds (ignore queue). Use for first run or rebuild."
    echo "  (none)   Read pending entries from sources/wiki_queue.json."
    exit 1
}

FULL_MODE="false"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --full) FULL_MODE="true"; shift ;;
        -h|--help) usage ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Wiki Update ==="
echo "Mode: $([ "$FULL_MODE" = "true" ] && echo "full (all digesteds)" || echo "incremental (queue)")"
echo ""

# --- Collect digesteds to process ---
DIGESTED_LIST=""

if [[ "$FULL_MODE" == "true" ]]; then
    for f in "$REPO_ROOT"/sources/digested/*_summary.md; do
        [[ -f "$f" ]] || continue
        DIGESTED_LIST+="- $(basename "$f")"$'\n'
    done
else
    # Queue source of truth: sources/wiki_queue.json (managed by wiki_queue.py)
    QUEUE_JSON=$(python "$SCRIPT_DIR/lib/wiki_queue.py" drain)
    QUEUE_COUNT=$(echo "$QUEUE_JSON" | python -c "import json,sys; print(len(json.load(sys.stdin)))")

    if [[ "$QUEUE_COUNT" -eq 0 ]]; then
        echo "No pending wiki-queue entries. Nothing to do."
        echo "Run with --full to rebuild all pages."
        exit 0
    fi

    # Extract unique digested names from the queue
    DIGESTED_LIST=$(echo "$QUEUE_JSON" | python -c "
import json, sys
from pathlib import Path
entries = json.load(sys.stdin)
names = sorted({Path(e['digested']).name for e in entries if e.get('digested')})
for n in names:
    print(f'- {n}')
")$'\n'
fi

DIGESTED_COUNT=$(echo "$DIGESTED_LIST" | grep -c "^-" || true)
echo "Digesteds to process: $DIGESTED_COUNT"

if [[ "$DIGESTED_COUNT" -eq 0 ]]; then
    echo "No digesteds found. Exiting."
    exit 0
fi

# --- Collect existing wiki pages with frontmatter ---
echo "Scanning wiki pages..."
WIKI_PAGES=""
for f in "$REPO_ROOT"/*.md; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    [[ "$fname" == "CLAUDE.md" || "$fname" == "README.md" || "$fname" == "SCHEMA.md" || "$fname" == "log.md" || "$fname" == "index.md" ]] && continue
    page_type=$(grep "^type:" "$f" 2>/dev/null | head -1 | sed 's/type: //' || echo "unknown")
    page_updated=$(grep "^updated:" "$f" 2>/dev/null | head -1 | sed 's/updated: //' || echo "unknown")
    WIKI_PAGES+="- $fname (type: $page_type, updated: $page_updated)"$'\n'
done

# --- Collect empresas with structured data ---
EMPRESAS_LIST=""
for d in "$REPO_ROOT"/sources/structured/*/; do
    [[ -d "$d" ]] || continue
    empresa=$(basename "$d")
    [[ "$empresa" == "_schemas" ]] && continue
    periods=$(ls "$d" | tr '\n' ' ')
    EMPRESAS_LIST+="- $empresa: $periods"$'\n'
done

echo "Wiki pages found: $(echo "$WIKI_PAGES" | grep -c "^-" || true)"
echo "Empresas with structured/: $(echo "$EMPRESAS_LIST" | grep -c "^-" || true)"
echo ""

# --- Helper: invoke claude ---
# Large replacement values (like a 656-line DIGESTED_LIST) would blow argv on Windows.
# Each value is written to a temp file; only the path is passed on the command line.
# Optional timeout via env var INVOKE_CLAUDE_TIMEOUT (seconds; 0 or unset = no timeout).
# Returns the exit code from claude (or timeout 124 if the timeout fires).
invoke_claude() {
    local template="$1"
    shift
    local prompt_file val_dir cmd_timeout
    cmd_timeout="${INVOKE_CLAUDE_TIMEOUT:-0}"
    prompt_file=$(mktemp "${TMPDIR:-/tmp}/wiki_prompt_XXXXXX.md")
    val_dir=$(mktemp -d "${TMPDIR:-/tmp}/wiki_vals_XXXXXX")

    local -a key_paths=()
    local i=0
    while [[ $# -gt 0 ]]; do
        local key="$1" val="$2"
        shift 2
        local path="$val_dir/val_$i"
        printf '%s' "$val" > "$path"
        key_paths+=("$key" "$path")
        i=$((i+1))
    done

    python -c "
import sys
template = open(sys.argv[1], encoding='utf-8').read()
pairs = sys.argv[2:-1]
for j in range(0, len(pairs), 2):
    key = pairs[j]
    val = open(pairs[j+1], encoding='utf-8').read()
    template = template.replace(key, val)
open(sys.argv[-1], 'w', encoding='utf-8').write(template)
" "$template" "${key_paths[@]}" "$prompt_file"

    local model_args=()
    if [[ -n "${WIKI_CLAUDE_MODEL:-}" ]]; then
        model_args=(--model "$WIKI_CLAUDE_MODEL")
    fi

    local rc=0
    if [[ "$cmd_timeout" -gt 0 ]]; then
        cat "$prompt_file" | timeout "$cmd_timeout" claude --print \
            "${model_args[@]}" \
            --allowedTools "Bash" \
            --permission-mode bypassPermissions || rc=$?
    else
        cat "$prompt_file" | claude --print \
            "${model_args[@]}" \
            --allowedTools "Bash" \
            --permission-mode bypassPermissions || rc=$?
    fi

    rm -rf "$val_dir"
    rm -f "$prompt_file"
    return $rc
}

# --- Phase 1: Planning (chunked) ---
# The planner LLM `cat`s each digest individually via Bash. With ~500+ digesteds
# in a single call this hangs (515 sequential tool calls saturate context, LLM
# stalls silently). We chunk the digest list, plan per chunk, then merge.
# Tunable via env: WIKI_PLAN_CHUNK_SIZE (default 50), WIKI_PLAN_CHUNK_TIMEOUT (default 1200s).
echo "=== Phase 1: Planning (chunked) ==="

CHUNK_SIZE="${WIKI_PLAN_CHUNK_SIZE:-50}"
CHUNK_TIMEOUT="${WIKI_PLAN_CHUNK_TIMEOUT:-1200}"
PLAN_TMPDIR=$(mktemp -d "${TMPDIR:-/tmp}/wiki_plan_chunks_XXXXXX")
trap "rm -rf '$PLAN_TMPDIR'" EXIT

# Failures persisted across runs so user can re-process failed chunks later.
FAILURES_LOG="${WIKI_FAILURES_LOG:-$REPO_ROOT/logs/wiki_plan_failures_$(date +%Y%m%d_%H%M%S).json}"
mkdir -p "$(dirname "$FAILURES_LOG")"
echo '[]' > "$FAILURES_LOG"

# Helper: record a chunk failure (chunk_idx, reason, chunk_input_file). Output via stdin.
record_failure() {
    python "$SCRIPT_DIR/lib/record_chunk_failure.py" "$FAILURES_LOG" "$1" "$2" "$3"
}

# Slice DIGESTED_LIST into per-chunk text files via Python (handles newlines cleanly)
NUM_CHUNKS=$(printf '%s' "$DIGESTED_LIST" | CHUNK_SIZE_ENV="$CHUNK_SIZE" python -c "
import sys, os
chunk_size = int(os.environ['CHUNK_SIZE_ENV'])
out_dir = sys.argv[1]
lines = [l for l in sys.stdin.read().splitlines() if l.startswith('-')]
total = len(lines)
n = (total + chunk_size - 1) // chunk_size
for i in range(n):
    chunk = lines[i*chunk_size : (i+1)*chunk_size]
    with open(f'{out_dir}/chunk_{i+1:03d}.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(chunk) + '\n')
print(n)
" "$PLAN_TMPDIR")

echo "Chunking $DIGESTED_COUNT digesteds into $NUM_CHUNKS chunk(s) of up to $CHUNK_SIZE each (per-chunk timeout: ${CHUNK_TIMEOUT}s)"
echo ""

export INVOKE_CLAUDE_TIMEOUT="$CHUNK_TIMEOUT"
SUCCESSFUL_CHUNKS=0
FAILED_CHUNKS=0

for CHUNK_FILE in "$PLAN_TMPDIR"/chunk_*.txt; do
    CHUNK_IDX=$(basename "$CHUNK_FILE" .txt | sed 's/chunk_0*//')
    CHUNK_BATCH=$(cat "$CHUNK_FILE")
    CHUNK_LINES=$(grep -c "^-" "$CHUNK_FILE" 2>/dev/null || echo 0)
    OUT_FILE="${CHUNK_FILE%.txt}.json"

    echo "  [chunk $CHUNK_IDX/$NUM_CHUNKS] $CHUNK_LINES digesteds — invoking planner..."

    if ! CHUNK_OUTPUT=$(invoke_claude "$SCRIPT_DIR/prompts/wiki_plan.md" \
        "{{DIGESTED_LIST}}" "$CHUNK_BATCH" \
        "{{WIKI_PAGES}}" "$WIKI_PAGES" \
        "{{EMPRESAS_LIST}}" "$EMPRESAS_LIST" 2>&1); then
        echo "    FAILED (invoke_claude non-zero, possibly timeout) — skipping chunk"
        printf '%s' "${CHUNK_OUTPUT:-}" | record_failure "$CHUNK_IDX" "invoke_claude_nonzero" "$CHUNK_FILE" || true
        FAILED_CHUNKS=$((FAILED_CHUNKS + 1))
        continue
    fi

    if ! echo "$CHUNK_OUTPUT" | python -c "
import sys, json
text = sys.stdin.read()
start = text.find('===WIKI_PLAN_START===')
end = text.find('===WIKI_PLAN_END===')
if start == -1 or end == -1:
    sys.stderr.write('plan markers missing\n')
    sys.exit(2)
json_text = text[start + len('===WIKI_PLAN_START==='):end].strip()
plan = json.loads(json_text)
print(json.dumps(plan, ensure_ascii=False))
" > "$OUT_FILE" 2>/dev/null; then
        echo "    FAILED parsing chunk JSON — skipping chunk"
        printf '%s' "$CHUNK_OUTPUT" | record_failure "$CHUNK_IDX" "parse_failed" "$CHUNK_FILE" || true
        rm -f "$OUT_FILE"
        FAILED_CHUNKS=$((FAILED_CHUNKS + 1))
        continue
    fi

    CC=$(cat "$OUT_FILE" | python -c "import sys,json; print(len(json.load(sys.stdin).get('create',[])))")
    UC=$(cat "$OUT_FILE" | python -c "import sys,json; print(len(json.load(sys.stdin).get('update',[])))")
    SC=$(cat "$OUT_FILE" | python -c "import sys,json; print(len(json.load(sys.stdin).get('skip',[])))")
    echo "    OK: create=$CC update=$UC skip=$SC"
    SUCCESSFUL_CHUNKS=$((SUCCESSFUL_CHUNKS + 1))
done

unset INVOKE_CLAUDE_TIMEOUT

echo ""
echo "Chunks complete: $SUCCESSFUL_CHUNKS ok, $FAILED_CHUNKS failed"
if [[ "$FAILED_CHUNKS" -gt 0 ]]; then
    echo "Failed-chunk metadata: $FAILURES_LOG"
    echo "  (re-process later by isolating those digesteds and re-running --full)"
fi

if [[ "$SUCCESSFUL_CHUNKS" -eq 0 ]]; then
    echo "ERROR: all chunks failed; cannot proceed"
    exit 1
fi

echo "Merging $SUCCESSFUL_CHUNKS chunk plans..."
PLAN_JSON=$(python "$SCRIPT_DIR/lib/merge_wiki_plans.py" "$PLAN_TMPDIR"/chunk_*.json)

CREATE_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('create',[])))")
UPDATE_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('update',[])))")
SKIP_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('skip',[])))")

echo ""
echo "Merged plan: create=$CREATE_COUNT, update=$UPDATE_COUNT, skip=$SKIP_COUNT"
echo ""

# --- Phase 2: Execution ---
echo "=== Phase 2: Execution ==="
# Tunable: WIKI_WRITE_TIMEOUT (default 1800s per page). Failed pages are logged and skipped.
WRITE_TIMEOUT="${WIKI_WRITE_TIMEOUT:-1800}"
WRITTEN_PAGES=0
FAILED_PAGES=0
FAILED_PAGES_LOG="${WIKI_FAILURES_LOG:-$REPO_ROOT/logs/wiki_plan_failures_$(date +%Y%m%d_%H%M%S).json}_write_failures.json"
echo '[]' > "$FAILED_PAGES_LOG"

ALL_PAGES=$(ls "$REPO_ROOT"/*.md 2>/dev/null | xargs -I{} basename {} | grep -v CLAUDE | grep -v README | grep -v SCHEMA | grep -v log | tr '\n' ', ')

for PAGE_TYPE in entity concept sector comparison; do
    PAGES_OF_TYPE=$(echo "$PLAN_JSON" | python -c "
import sys, json
plan = json.load(sys.stdin)
for item in plan.get('create', []):
    if item['type'] == '$PAGE_TYPE':
        digesteds = ','.join(item['digesteds'])
        print(f\"{item['page']}|create|{digesteds}\")
for item in plan.get('update', []):
    if item['type'] == '$PAGE_TYPE':
        digesteds = ','.join(item['digesteds'])
        print(f\"{item['page']}|update|{digesteds}\")
")

    [[ -z "$PAGES_OF_TYPE" ]] && continue

    while IFS= read -r line; do
        PAGE_NAME=$(echo "$line" | cut -d'|' -f1)
        ACTION=$(echo "$line" | cut -d'|' -f2)
        DIGESTEDS_CSV=$(echo "$line" | cut -d'|' -f3)

        echo "  [$ACTION] $PAGE_NAME ($PAGE_TYPE)"

        PAGE_DIGESTEDS=""
        IFS=',' read -ra DIGS <<< "$DIGESTEDS_CSV"
        for d in "${DIGS[@]}"; do
            PAGE_DIGESTEDS+="- sources/digested/$d"$'\n'
        done

        EXISTING_CONTENT="(new page — no existing content)"
        if [[ "$ACTION" == "update" ]] && [[ -f "$REPO_ROOT/$PAGE_NAME" ]]; then
            EXISTING_CONTENT=$(cat "$REPO_ROOT/$PAGE_NAME")
        fi

        WRITE_RC=0
        INVOKE_CLAUDE_TIMEOUT="$WRITE_TIMEOUT" invoke_claude "$SCRIPT_DIR/prompts/wiki_write.md" \
            "{{PAGE_NAME}}" "$PAGE_NAME" \
            "{{ACTION}}" "$ACTION" \
            "{{PAGE_TYPE}}" "$PAGE_TYPE" \
            "{{DIGESTED_LIST}}" "$PAGE_DIGESTEDS" \
            "{{EXISTING_CONTENT}}" "$EXISTING_CONTENT" \
            "{{ALL_PAGES}}" "$ALL_PAGES" > /dev/null || WRITE_RC=$?

        if [[ "$WRITE_RC" -ne 0 ]]; then
            echo "    FAILED [$ACTION $PAGE_NAME] rc=$WRITE_RC — skipping"
            python -c "
import json, sys
log='$FAILED_PAGES_LOG'; rec={'page':'$PAGE_NAME','action':'$ACTION','type':'$PAGE_TYPE','rc':$WRITE_RC}
try:
    data=json.load(open(log))
except Exception:
    data=[]
data.append(rec)
json.dump(data, open(log,'w'), ensure_ascii=False, indent=2)
" 2>/dev/null || true
            FAILED_PAGES=$((FAILED_PAGES+1))
        else
            WRITTEN_PAGES=$((WRITTEN_PAGES+1))
        fi

        ALL_PAGES+=",$PAGE_NAME"

    done <<< "$PAGES_OF_TYPE"
done

echo ""

# --- Mark queue as consumed ---
# --full processes ALL digesteds, so the queue is fully covered regardless of mode.
BATCH_ID="batch_$(date +%Y%m%d_%H%M%S)"
python "$SCRIPT_DIR/lib/wiki_queue.py" clear >/dev/null
echo "[wiki-done] $(date +%Y-%m-%d) | $BATCH_ID" >> "$REPO_ROOT/log.md"
if [[ "$FULL_MODE" == "true" ]]; then
    echo "Queue cleared (--full run covers all digesteds): $BATCH_ID"
else
    echo "Queue consumed: $BATCH_ID (queue.json cleared)"
fi

echo ""
echo "=== Wiki update complete ==="
echo "  Planned create: $CREATE_COUNT | update: $UPDATE_COUNT | skip: $SKIP_COUNT"
echo "  Phase 2 written: $WRITTEN_PAGES | failed: $FAILED_PAGES"
if [[ "$FAILED_PAGES" -gt 0 ]]; then
    echo "  Failed-page log: $FAILED_PAGES_LOG"
fi
