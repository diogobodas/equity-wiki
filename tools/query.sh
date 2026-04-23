#!/usr/bin/env bash
set -euo pipefail

# --- Usage ---
usage() {
    echo "Usage: bash tools/query.sh \"pergunta em linguagem natural\""
    echo ""
    echo "Queries the wiki data sources (structured/, full/, digested/) to answer questions."
    exit 1
}

[[ $# -lt 1 ]] && usage
QUERY="$1"

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Generate inventory ---
INVENTORY=""

# Structured data
INVENTORY+="## Structured (JSON):"$'\n'
for d in "$REPO_ROOT"/sources/structured/*/; do
    [[ -d "$d" ]] || continue
    empresa=$(basename "$d")
    [[ "$empresa" == "_schemas" ]] && continue
    periods=""
    for p in "$d"*/; do
        [[ -d "$p" ]] || continue
        period=$(basename "$p")
        types=$(ls "$p"*.json 2>/dev/null | xargs -I{} basename {} .json | tr '\n' ',' | sed 's/,$//')
        periods+="$period($types) "
    done
    INVENTORY+="- $empresa: $periods"$'\n'
done

# Full data
INVENTORY+=$'\n'"## Full (extracted text):"$'\n'
for d in "$REPO_ROOT"/sources/full/*/; do
    [[ -d "$d" ]] || continue
    empresa=$(basename "$d")
    [[ "$empresa" == "generic" ]] && continue
    periods=""
    for p in "$d"*/; do
        [[ -d "$p" ]] || continue
        period=$(basename "$p")
        types=$(ls "$p"*.md 2>/dev/null | xargs -I{} basename {} .md | tr '\n' ',' | sed 's/,$//')
        periods+="$period($types) "
    done
    INVENTORY+="- $empresa: $periods"$'\n'
done

# Generic sources
GENERIC_FILES=$(ls "$REPO_ROOT"/sources/full/generic/*.md 2>/dev/null | xargs -I{} basename {} | tr '\n' ', ' | sed 's/, $//')
if [[ -n "$GENERIC_FILES" ]]; then
    INVENTORY+=$'\n'"## Generic sources (full/generic/):"$'\n'
    INVENTORY+="- $GENERIC_FILES"$'\n'
fi

# Digested summaries
INVENTORY+=$'\n'"## Digested summaries:"$'\n'
DIGESTED_LIST=$(ls "$REPO_ROOT"/sources/digested/*_summary.md 2>/dev/null | xargs -I{} basename {} | tr '\n' ', ' | sed 's/, $//')
INVENTORY+="- $DIGESTED_LIST"$'\n'

# --- Build prompt ---
PROMPT_TEMPLATE="$SCRIPT_DIR/prompts/query_system.md"
PROMPT_FILE=$(mktemp "${TMPDIR:-/tmp}/query_prompt_XXXXXX.md")
INVENTORY_FILE=$(mktemp "${TMPDIR:-/tmp}/query_inventory_XXXXXX.md")
printf '%s' "$INVENTORY" > "$INVENTORY_FILE"

python -c "
import sys
template = open(sys.argv[1], encoding='utf-8').read()
inventory = open(sys.argv[3], encoding='utf-8').read()
template = template.replace('{{QUERY}}', sys.argv[2])
template = template.replace('{{INVENTORY}}', inventory)
open(sys.argv[4], 'w', encoding='utf-8').write(template)
" "$PROMPT_TEMPLATE" "$QUERY" "$INVENTORY_FILE" "$PROMPT_FILE"

rm -f "$INVENTORY_FILE"

# --- Invoke Claude ---
cat "$PROMPT_FILE" | claude --print \
    --allowedTools "Bash" \
    --permission-mode bypassPermissions

rm -f "$PROMPT_FILE"
