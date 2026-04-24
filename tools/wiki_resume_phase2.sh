#!/usr/bin/env bash
# wiki_resume_phase2.sh — Resume Phase 2 execution from a saved merged plan.
# Skips create pages that already exist on disk. Runs updates always.
# Supports parallel page writes via WIKI_WRITE_CONCURRENCY (default 4).
#
# Usage:
#   bash tools/wiki_resume_phase2.sh --plan logs/wiki_plan_merged_20260420.json
#
# Env tunables:
#   WIKI_CLAUDE_MODEL       model for page writes (default: claude-sonnet-4-6 — Phase 2 is page-scoped)
#   WIKI_WRITE_TIMEOUT      seconds per page (default: 1800)
#   WIKI_WRITE_CONCURRENCY  parallel page writers (default: 4)
set -euo pipefail

usage() {
    echo "Usage: bash tools/wiki_resume_phase2.sh --plan <merged_plan.json>"
    exit 1
}

PLAN_FILE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --plan) PLAN_FILE="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done

[[ -z "$PLAN_FILE" ]] && usage
[[ ! -f "$PLAN_FILE" ]] && echo "ERROR: plan file not found: $PLAN_FILE" && exit 1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

WRITE_TIMEOUT="${WIKI_WRITE_TIMEOUT:-1800}"
CONCURRENCY="${WIKI_WRITE_CONCURRENCY:-4}"
# Phase 2 is page-scoped / template-driven — default to Sonnet.
WIKI_CLAUDE_MODEL="${WIKI_CLAUDE_MODEL:-claude-sonnet-4-6}"

echo "=== Wiki Phase 2 Resume (parallel, concurrency=$CONCURRENCY) ==="
echo "Plan: $PLAN_FILE"
echo ""

# --- Temp dirs ---
STATUS_DIR=$(mktemp -d "${TMPDIR:-/tmp}/wiki_status_XXXXXX")
INPUTS_DIR=$(mktemp -d "${TMPDIR:-/tmp}/wiki_inputs_XXXXXX")
trap "rm -rf '$STATUS_DIR' '$INPUTS_DIR'" EXIT

# --- Helper: invoke claude ---
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

# --- Pre-compute full ALL_PAGES context ---
# Include existing pages + all pages that will be created/updated, so every
# parallel worker has an accurate wikilink context.
ALL_PAGES=$(python -c "
import json, os, glob
plan = json.load(open('$PLAN_FILE', encoding='utf-8'))
existing = {os.path.basename(f) for f in glob.glob('*.md')}
skip = {'CLAUDE.md','README.md','SCHEMA.md','log.md','index.md'}
planned = {i['page'] for i in plan.get('create',[])} | {i['page'] for i in plan.get('update',[])}
all_pages = (existing | planned) - skip
print(','.join(sorted(all_pages)))
")

echo "ALL_PAGES context: $(echo "$ALL_PAGES" | tr ',' '\n' | wc -l) pages"

# --- Collect pages already on disk ---
SKIPPED_EXISTING=0

# --- Build work list: one line per page, written to INPUTS_DIR ---
echo "Building work list..."
WORK_COUNT=0

for PAGE_TYPE in entity concept sector comparison; do
    python -c "
import json
plan = json.load(open('$PLAN_FILE', encoding='utf-8'))
for item in plan.get('create', []):
    if item['type'] == '$PAGE_TYPE':
        print('create|' + item['page'] + '|$PAGE_TYPE|' + ','.join(item['digesteds']))
for item in plan.get('update', []):
    if item['type'] == '$PAGE_TYPE':
        print('update|' + item['page'] + '|$PAGE_TYPE|' + ','.join(item['digesteds']))
" | while IFS='|' read -r ACTION PAGE_NAME PT DIGESTEDS_CSV; do
        # Skip creates that already exist
        if [[ "$ACTION" == "create" ]] && [[ -f "$REPO_ROOT/$PAGE_NAME" ]]; then
            echo "  [skip-exists] $PAGE_NAME"
            continue
        fi

        # Write inputs to a per-page dir
        PAGE_SLUG="${PAGE_NAME//\//_}"
        PAGE_DIR="$INPUTS_DIR/${ACTION}_${PAGE_SLUG}"
        mkdir -p "$PAGE_DIR"
        printf '%s' "$PAGE_NAME"    > "$PAGE_DIR/page_name"
        printf '%s' "$ACTION"       > "$PAGE_DIR/action"
        printf '%s' "$PT"           > "$PAGE_DIR/page_type"
        printf '%s' "$DIGESTEDS_CSV"> "$PAGE_DIR/digesteds_csv"

        PAGE_DIGESTEDS=""
        IFS=',' read -ra DIGS <<< "$DIGESTEDS_CSV"
        for d in "${DIGS[@]}"; do
            PAGE_DIGESTEDS+="- sources/digested/$d"$'\n'
        done
        printf '%s' "$PAGE_DIGESTEDS" > "$PAGE_DIR/page_digesteds"

        EXISTING_CONTENT="(new page — no existing content)"
        if [[ "$ACTION" == "update" ]] && [[ -f "$REPO_ROOT/$PAGE_NAME" ]]; then
            EXISTING_CONTENT=$(cat "$REPO_ROOT/$PAGE_NAME")
        fi
        printf '%s' "$EXISTING_CONTENT" > "$PAGE_DIR/existing_content"

        echo "$PAGE_DIR"
    done >> "$INPUTS_DIR/work_list.txt" 2>&1 || true
done

WORK_COUNT=$(grep -c "^$INPUTS_DIR" "$INPUTS_DIR/work_list.txt" 2>/dev/null || echo 0)
SKIPPED_EXISTING=$(grep -c "skip-exists" "$INPUTS_DIR/work_list.txt" 2>/dev/null || echo 0)

echo "Pages to write: $WORK_COUNT (skipped existing: $SKIPPED_EXISTING)"
echo ""

# --- Parallel execution ---
echo "=== Phase 2: Execution (parallel x$CONCURRENCY) ==="

# Export needed vars for subshells
export SCRIPT_DIR REPO_ROOT WRITE_TIMEOUT WIKI_CLAUDE_MODEL STATUS_DIR ALL_PAGES
export -f invoke_claude

write_page() {
    local PAGE_DIR="$1"
    local PAGE_NAME ACTION PAGE_TYPE PAGE_DIGESTEDS EXISTING_CONTENT
    PAGE_NAME=$(cat "$PAGE_DIR/page_name")
    ACTION=$(cat "$PAGE_DIR/action")
    PAGE_TYPE=$(cat "$PAGE_DIR/page_type")
    PAGE_DIGESTEDS=$(cat "$PAGE_DIR/page_digesteds")
    EXISTING_CONTENT=$(cat "$PAGE_DIR/existing_content")

    echo "  [$ACTION] $PAGE_NAME ($PAGE_TYPE)"

    local WRITE_RC=0
    INVOKE_CLAUDE_TIMEOUT="$WRITE_TIMEOUT" invoke_claude "$SCRIPT_DIR/prompts/wiki_write.md" \
        "{{PAGE_NAME}}" "$PAGE_NAME" \
        "{{ACTION}}" "$ACTION" \
        "{{PAGE_TYPE}}" "$PAGE_TYPE" \
        "{{DIGESTED_LIST}}" "$PAGE_DIGESTEDS" \
        "{{EXISTING_CONTENT}}" "$EXISTING_CONTENT" \
        "{{ALL_PAGES}}" "$ALL_PAGES" > /dev/null || WRITE_RC=$?

    local PAGE_SLUG="${PAGE_NAME//[.\/ ]/_}"
    if [[ "$WRITE_RC" -ne 0 ]]; then
        echo "    FAILED [$ACTION $PAGE_NAME] rc=$WRITE_RC"
        printf 'fail:%s:%s:%s:%s\n' "$PAGE_NAME" "$ACTION" "$PAGE_TYPE" "$WRITE_RC" > "$STATUS_DIR/${PAGE_SLUG}.status" 2>/dev/null || true
    else
        echo "    OK [$ACTION $PAGE_NAME]"
        printf 'ok:%s\n' "$PAGE_NAME" > "$STATUS_DIR/${PAGE_SLUG}.status" 2>/dev/null || true
    fi
}
export -f write_page

# Job pool
ACTIVE_PIDS=()

throttle_jobs() {
    while (( ${#ACTIVE_PIDS[@]} >= CONCURRENCY )); do
        local new_pids=()
        for pid in "${ACTIVE_PIDS[@]}"; do
            if kill -0 "$pid" 2>/dev/null; then
                new_pids+=("$pid")
            else
                wait "$pid" 2>/dev/null || true
            fi
        done
        ACTIVE_PIDS=("${new_pids[@]+"${new_pids[@]}"}")
        if (( ${#ACTIVE_PIDS[@]} >= CONCURRENCY )); then sleep 1; fi
    done
}

if [[ -f "$INPUTS_DIR/work_list.txt" ]]; then
    while IFS= read -r PAGE_DIR; do
        [[ "$PAGE_DIR" == "$INPUTS_DIR"* ]] || continue
        [[ -d "$PAGE_DIR" ]] || continue
        throttle_jobs
        ( trap - EXIT; write_page "$PAGE_DIR" ) &
        ACTIVE_PIDS+=($!)
    done < "$INPUTS_DIR/work_list.txt"
fi

# Wait for remaining jobs
for pid in "${ACTIVE_PIDS[@]+"${ACTIVE_PIDS[@]}"}"; do
    wait "$pid" 2>/dev/null || true
done

# --- Collect results ---
WRITTEN_PAGES=0
FAILED_PAGES=0
FAILED_PAGES_LOG="$REPO_ROOT/logs/wiki_resume_write_failures_$(date +%Y%m%d_%H%M%S).json"
echo '[]' > "$FAILED_PAGES_LOG"

if compgen -G "$STATUS_DIR/*.status" > /dev/null 2>&1; then
    while IFS= read -r status_file; do
        content=$(cat "$status_file")
        if [[ "$content" == ok:* ]]; then
            WRITTEN_PAGES=$((WRITTEN_PAGES+1))
        elif [[ "$content" == fail:* ]]; then
            FAILED_PAGES=$((FAILED_PAGES+1))
            IFS=':' read -r _ page action type rc <<< "$content"
            python -c "
import json
log='$FAILED_PAGES_LOG'
rec={'page':'$page','action':'$action','type':'$type','rc':$rc}
try:
    data=json.load(open(log,encoding='utf-8'))
except Exception:
    data=[]
data.append(rec)
json.dump(data, open(log,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
" 2>/dev/null || true
        fi
    done < <(find "$STATUS_DIR" -name "*.status")
fi

# --- Clear wiki queue ---
BATCH_ID="batch_$(date +%Y%m%d_%H%M%S)"
python "$SCRIPT_DIR/lib/wiki_queue.py" clear >/dev/null 2>&1 || true
echo "[wiki-done] $(date +%Y-%m-%d) | $BATCH_ID (resume)" >> "$REPO_ROOT/log.md"
echo "Queue cleared: $BATCH_ID"

echo ""
echo "=== Resume complete ==="
echo "  Skipped (already existed): $SKIPPED_EXISTING"
echo "  Written: $WRITTEN_PAGES"
echo "  Failed:  $FAILED_PAGES"
if [[ "$FAILED_PAGES" -gt 0 ]]; then
    echo "  Failed-page log: $FAILED_PAGES_LOG"
fi
