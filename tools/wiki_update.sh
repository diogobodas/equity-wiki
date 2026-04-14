#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: bash tools/wiki_update.sh [--full]"
    echo ""
    echo "Updates wiki pages based on digested summaries."
    echo ""
    echo "Options:"
    echo "  --full   Read ALL digesteds (ignore queue). Use for first run or rebuild."
    echo "  (none)   Read only pending [wiki-queue] entries from log.md."
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
    LAST_DONE=$(grep -n "\[wiki-done\]" "$REPO_ROOT/log.md" 2>/dev/null | tail -1 | cut -d: -f1 || true)
    LAST_DONE=${LAST_DONE:-0}

    QUEUE_ENTRIES=$(tail -n +$((LAST_DONE + 1)) "$REPO_ROOT/log.md" | grep "\[wiki-queue\]" || true)

    if [[ -z "$QUEUE_ENTRIES" ]]; then
        echo "No pending wiki-queue entries. Nothing to do."
        echo "Run with --full to rebuild all pages."
        exit 0
    fi

    while IFS= read -r line; do
        digested_path=$(echo "$line" | awk -F'|' '{print $NF}' | xargs)
        digested_name=$(basename "$digested_path")
        DIGESTED_LIST+="- $digested_name"$'\n'
    done <<< "$QUEUE_ENTRIES"

    DIGESTED_LIST=$(echo "$DIGESTED_LIST" | sort -u)
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
invoke_claude() {
    local template="$1"
    local prompt_file
    prompt_file=$(mktemp "${TMPDIR:-/tmp}/wiki_prompt_XXXXXX.md")

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

# --- Phase 1: Planning ---
echo "=== Phase 1: Planning ==="
PLAN_OUTPUT=$(invoke_claude "$SCRIPT_DIR/prompts/wiki_plan.md" \
    "{{DIGESTED_LIST}}" "$DIGESTED_LIST" \
    "{{WIKI_PAGES}}" "$WIKI_PAGES" \
    "{{EMPRESAS_LIST}}" "$EMPRESAS_LIST")

PLAN_JSON=$(echo "$PLAN_OUTPUT" | python -c "
import sys
text = sys.stdin.read()
start = text.find('===WIKI_PLAN_START===')
end = text.find('===WIKI_PLAN_END===')
if start == -1 or end == -1:
    print('ERROR: Could not find plan markers in agent output')
    sys.exit(1)
json_text = text[start + len('===WIKI_PLAN_START==='):end].strip()
import json
plan = json.loads(json_text)
print(json.dumps(plan, ensure_ascii=False, indent=2))
")

if [[ "$PLAN_JSON" == ERROR* ]]; then
    echo "$PLAN_JSON"
    exit 1
fi

CREATE_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('create',[])))")
UPDATE_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('update',[])))")
SKIP_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('skip',[])))")

echo ""
echo "Plan: create=$CREATE_COUNT, update=$UPDATE_COUNT, skip=$SKIP_COUNT"
echo ""

# --- Phase 2: Execution ---
echo "=== Phase 2: Execution ==="

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

        invoke_claude "$SCRIPT_DIR/prompts/wiki_write.md" \
            "{{PAGE_NAME}}" "$PAGE_NAME" \
            "{{ACTION}}" "$ACTION" \
            "{{PAGE_TYPE}}" "$PAGE_TYPE" \
            "{{DIGESTED_LIST}}" "$PAGE_DIGESTEDS" \
            "{{EXISTING_CONTENT}}" "$EXISTING_CONTENT" \
            "{{ALL_PAGES}}" "$ALL_PAGES" > /dev/null

        ALL_PAGES+=",$PAGE_NAME"

    done <<< "$PAGES_OF_TYPE"
done

echo ""

# --- Mark queue as consumed ---
if [[ "$FULL_MODE" != "true" ]]; then
    BATCH_ID="batch_$(date +%Y%m%d_%H%M%S)"
    echo "[wiki-done] $(date +%Y-%m-%d) | $BATCH_ID" >> "$REPO_ROOT/log.md"
    echo "Queue consumed: $BATCH_ID"
fi

echo ""
echo "=== Wiki update complete ==="
echo "  Created: $CREATE_COUNT pages"
echo "  Updated: $UPDATE_COUNT pages"
echo "  Skipped: $SKIP_COUNT pages"
