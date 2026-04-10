#!/usr/bin/env bash
set -euo pipefail

# --- Defaults ---
HORIZON="3y"
TYPES="dfp,itr,release,fato_relevante"

# --- Usage ---
usage() {
    echo "Usage: bash tools/fetch.sh <TICKER> [--horizon 3y] [--types dfp,itr,release,fato_relevante]"
    echo ""
    echo "Fetches missing CVM filings for a company and deposits them in sources/undigested/"
    exit 1
}

# --- Parse args ---
[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --horizon) HORIZON="$2"; shift 2 ;;
        --types)   TYPES="$2"; shift 2 ;;
        *)         echo "Unknown arg: $1"; usage ;;
    esac
done

# --- Paths (relative to repo root) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFESTS_PATH="sources/manifests"
UNDIGESTED_PATH="sources/undigested"
PROMPT_TEMPLATE="$SCRIPT_DIR/prompts/fetch_system.md"

# --- Compute HORIZON_FROM as absolute date ---
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
TODAY=$(date +%Y-%m-%d)

echo "=== Fetch Agent ==="
echo "Ticker:   $TICKER"
echo "Horizon:  $HORIZON (from $HORIZON_FROM)"
echo "Types:    $TYPES"
echo ""

# --- Resolve manifest ---
COLD_START="true"
EMPRESA=""
MANIFEST_CONTENT='null (cold-start — no manifest found for this ticker)'
DISPLAY_NAME=""

# Search for manifest containing this ticker
if [[ -d "$REPO_ROOT/$MANIFESTS_PATH" ]]; then
    for f in "$REPO_ROOT/$MANIFESTS_PATH"/*.json; do
        [[ -f "$f" ]] || continue
        if grep -q "\"$TICKER\"" "$f" 2>/dev/null; then
            EMPRESA=$(basename "$f" .json)
            MANIFEST_CONTENT=$(cat "$f")
            COLD_START="false"
            break
        fi
    done
fi

# If no manifest found, resolve via CVM-API
if [[ "$COLD_START" == "true" ]]; then
    echo "No manifest found for $TICKER — cold-start mode"
    RESOLVE_JSON=$(python "$SCRIPT_DIR/lib/cvm_fetch.py" resolve "$TICKER" 2>&1) || {
        echo "ERROR: Could not resolve ticker $TICKER"
        echo "$RESOLVE_JSON"
        exit 1
    }
    DISPLAY_NAME=$(echo "$RESOLVE_JSON" | python -c "import sys,json; print(json.load(sys.stdin)['nome'])")
    EMPRESA=$(echo "$DISPLAY_NAME" | python -c "
import sys, unicodedata
name = sys.stdin.read().strip().split()[0].lower()
name = unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode()
print(name)
")
    echo "Resolved: $DISPLAY_NAME → empresa=$EMPRESA"
else
    DISPLAY_NAME=$(echo "$MANIFEST_CONTENT" | python -c "import sys,json; print(json.load(sys.stdin).get('display_name',''))")
    echo "Found manifest: $MANIFESTS_PATH/$EMPRESA.json"
fi

# --- Build prompt by replacing placeholders ---
USER_PROMPT=$(cat "$PROMPT_TEMPLATE")
USER_PROMPT="${USER_PROMPT//\{\{TICKER\}\}/$TICKER}"
USER_PROMPT="${USER_PROMPT//\{\{EMPRESA\}\}/$EMPRESA}"
USER_PROMPT="${USER_PROMPT//\{\{COLD_START\}\}/$COLD_START}"
USER_PROMPT="${USER_PROMPT//\{\{HORIZON_FROM\}\}/$HORIZON_FROM}"
USER_PROMPT="${USER_PROMPT//\{\{TYPES\}\}/$TYPES}"
USER_PROMPT="${USER_PROMPT//\{\{UNDIGESTED_PATH\}\}/$UNDIGESTED_PATH}"
USER_PROMPT="${USER_PROMPT//\{\{MANIFESTS_PATH\}\}/$MANIFESTS_PATH}"
USER_PROMPT="${USER_PROMPT//\{\{TODAY\}\}/$TODAY}"
USER_PROMPT="${USER_PROMPT//\{\{DISPLAY_NAME\}\}/$DISPLAY_NAME}"
USER_PROMPT="${USER_PROMPT//\{\{MANIFEST_CONTENT\}\}/$MANIFEST_CONTENT}"

echo ""
echo "Invoking Claude agent..."
echo "========================"
echo ""

# --- Invoke Claude ---
claude --print \
    --allowedTools "Bash(command:python*)" \
    -p "$USER_PROMPT"
