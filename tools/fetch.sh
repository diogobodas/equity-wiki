#!/usr/bin/env bash
set -euo pipefail

# --- Defaults ---
HORIZON="3y"
TYPES="dfp,itr,release,fato_relevante"
DISCOVER="false"

# --- Usage ---
usage() {
    echo "Usage: bash tools/fetch.sh <TICKER> [--horizon 3y] [--types dfp,itr,release,fato_relevante] [--discover]"
    echo ""
    echo "Fetches missing CVM filings for a company and deposits them in sources/undigested/"
    echo ""
    echo "Options:"
    echo "  --discover   Run discovery mode: download a sample quarter, classify documents,"
    echo "               and create a fetch_profile for future filtering"
    echo "  --horizon    How far back to search (default: 3y). Accepts Ny or Nm."
    echo "  --types      Comma-separated document types (default: dfp,itr,release,fato_relevante)"
    exit 1
}

# --- Parse args ---
[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --horizon)  HORIZON="$2"; shift 2 ;;
        --types)    TYPES="$2"; shift 2 ;;
        --discover) DISCOVER="true"; shift ;;
        *)          echo "Unknown arg: $1"; usage ;;
    esac
done

# --- Paths (relative to repo root) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFESTS_PATH="sources/manifests"
UNDIGESTED_PATH="sources/undigested"
PROMPT_TEMPLATE="$SCRIPT_DIR/prompts/fetch_system.md"
DISCOVER_TEMPLATE="$SCRIPT_DIR/prompts/fetch_discover.md"

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
echo "Mode:     $([ "$DISCOVER" = "true" ] && echo "discovery" || echo "normal")"
echo ""

# --- Resolve manifest ---
COLD_START="true"
EMPRESA=""
MANIFEST_CONTENT='null (cold-start — no manifest found for this ticker)'
DISPLAY_NAME=""
MANIFEST_PATH_FULL=""

# Search for manifest containing this ticker
if [[ -d "$REPO_ROOT/$MANIFESTS_PATH" ]]; then
    for f in "$REPO_ROOT/$MANIFESTS_PATH"/*.json; do
        [[ -f "$f" ]] || continue
        if grep -q "\"$TICKER\"" "$f" 2>/dev/null; then
            EMPRESA=$(basename "$f" .json)
            MANIFEST_CONTENT=$(cat "$f")
            MANIFEST_PATH_FULL="$f"
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
    MANIFEST_PATH_FULL="$REPO_ROOT/$MANIFESTS_PATH/$EMPRESA.json"
    echo "Resolved: $DISPLAY_NAME → empresa=$EMPRESA"
else
    DISPLAY_NAME=$(echo "$MANIFEST_CONTENT" | python -c "import sys,json; print(json.load(sys.stdin).get('display_name',''))")
    echo "Found manifest: $MANIFESTS_PATH/$EMPRESA.json"
fi

# --- Temp files ---
PROMPT_FILE=$(mktemp "${TMPDIR:-/tmp}/fetch_prompt_XXXXXX.md")
MANIFEST_FILE=$(mktemp "${TMPDIR:-/tmp}/fetch_manifest_XXXXXX.json")
trap 'rm -f "$PROMPT_FILE" "$MANIFEST_FILE"' EXIT

echo "$MANIFEST_CONTENT" > "$MANIFEST_FILE"

# ===========================================================================
# DISCOVERY MODE
# ===========================================================================
if [[ "$DISCOVER" == "true" ]]; then
    echo "--- Discovery mode ---"

    # 1. Find the most recent quarter with releases
    echo "Listing recent releases/fatos relevantes..."
    LIST_JSON=$(python "$SCRIPT_DIR/lib/cvm_fetch.py" list "$TICKER" --types release,fato_relevante --from "$HORIZON_FROM" 2>&1)

    # Extract the most recent periodo
    SAMPLE_PERIOD=$(echo "$LIST_JSON" | python -c "
import sys, json
docs = json.load(sys.stdin)
if not docs:
    print(''); sys.exit(0)
releases = [d for d in docs if d['tipo'] == 'release']
if releases:
    print(releases[0]['periodo'])
else:
    print(docs[0]['periodo'])
")

    if [[ -z "$SAMPLE_PERIOD" ]]; then
        echo "ERROR: No releases or fatos relevantes found for $TICKER in the given horizon"
        exit 1
    fi
    echo "Sample period: $SAMPLE_PERIOD"

    # 2. Download all docs from that period to a temp dir
    TEMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/fetch_discover_XXXXXX")
    trap 'rm -rf "$TEMP_DIR" "$PROMPT_FILE" "$MANIFEST_FILE"' EXIT

    echo "Downloading all docs from $SAMPLE_PERIOD to temp dir..."

    FILE_LIST=$(echo "$LIST_JSON" | python -c "
import sys, json, subprocess, os

docs = json.load(sys.stdin)
temp_dir = sys.argv[1]
sample = sys.argv[2]
ticker = sys.argv[3]
script_dir = sys.argv[4]

period_docs = [d for d in docs if d['periodo'] == sample]
results = []
for doc in period_docs:
    seq = doc.get('num_sequencia') or 'unknown'
    fname = f\"{ticker}_{sample}_{doc['tipo']}_{seq}.pdf\"
    outpath = os.path.join(temp_dir, fname)
    cmd = [
        'python', os.path.join(script_dir, 'lib', 'cvm_fetch.py'), 'download',
        '--num-sequencia', str(doc.get('num_sequencia', '')),
        '--num-versao', str(doc.get('num_versao', '')),
        '--numero-protocolo', str(doc.get('numero_protocolo', '')),
        '--desc-tipo', str(doc.get('desc_tipo', '')),
        '--output', outpath,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        result = json.loads(r.stdout)
        orig = result.get('original_filename', fname)
        size = result.get('size_bytes', 0)
        results.append(f'{fname} | original: {orig} | size: {size}')
    except:
        results.append(f'{fname} | download error')
print('\n'.join(results))
" "$TEMP_DIR" "$SAMPLE_PERIOD" "$TICKER" "$SCRIPT_DIR")

    echo "$FILE_LIST"
    echo ""
    echo "Downloaded $(echo "$FILE_LIST" | wc -l) files. Invoking discovery agent..."

    # 3. Build discovery prompt
    python -c "
import sys
template = open(sys.argv[1]).read()
replacements = {
    '{{TICKER}}': sys.argv[2],
    '{{EMPRESA}}': sys.argv[3],
    '{{SAMPLE_PERIOD}}': sys.argv[4],
    '{{TEMP_DIR}}': sys.argv[5],
    '{{FILE_LIST}}': sys.argv[6],
    '{{TODAY}}': sys.argv[7],
}
for k, v in replacements.items():
    template = template.replace(k, v)
open(sys.argv[8], 'w', encoding='utf-8').write(template)
" "$DISCOVER_TEMPLATE" "$TICKER" "$EMPRESA" "$SAMPLE_PERIOD" "$TEMP_DIR" \
  "$FILE_LIST" "$TODAY" "$PROMPT_FILE"

    # 4. Invoke Claude for classification
    DISCOVERY_OUTPUT=$(cat "$PROMPT_FILE" | claude --print \
        --allowedTools "Bash" \
        --permission-mode bypassPermissions)

    echo "$DISCOVERY_OUTPUT"

    # 5. Extract JSON profile from output
    PROFILE_JSON=$(echo "$DISCOVERY_OUTPUT" | python -c "
import sys
text = sys.stdin.read()
start = text.find('===FETCH_PROFILE_START===')
end = text.find('===FETCH_PROFILE_END===')
if start == -1 or end == -1:
    print('ERROR: Could not find profile markers in agent output')
    sys.exit(1)
json_text = text[start + len('===FETCH_PROFILE_START==='):end].strip()
import json
profile = json.loads(json_text)
print(json.dumps(profile, ensure_ascii=False, indent=2))
")

    if [[ "$PROFILE_JSON" == ERROR* ]]; then
        echo "$PROFILE_JSON"
        exit 1
    fi

    # 6. Human approval
    echo ""
    echo "================================================"
    echo "Salvar este perfil no manifest? (s/n/editar)"
    echo "  s      → salvar e limpar temp"
    echo "  n      → descartar"
    echo "  editar → salvar JSON em arquivo para edição manual"
    echo "================================================"
    read -r REPLY

    case "$REPLY" in
        s|S|sim|y|yes)
            python -c "
import sys, json
manifest_path = sys.argv[1]
profile_json = sys.argv[2]

profile = json.loads(profile_json)

try:
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
except FileNotFoundError:
    print('ERROR: Manifest not found at ' + manifest_path)
    sys.exit(1)

manifest['fetch_profile'] = profile

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('fetch_profile saved to ' + manifest_path)
" "$MANIFEST_PATH_FULL" "$PROFILE_JSON"
            ;;
        editar|e|edit)
            EDIT_FILE="$REPO_ROOT/tools/fetch_profile_draft.json"
            echo "$PROFILE_JSON" > "$EDIT_FILE"
            echo "Profile saved to $EDIT_FILE"
            echo "Edit it, then run:"
            echo "  python -c \"import json; m=json.load(open('$MANIFEST_PATH_FULL')); m['fetch_profile']=json.load(open('$EDIT_FILE')); json.dump(m, open('$MANIFEST_PATH_FULL','w'), ensure_ascii=False, indent=2)\""
            ;;
        *)
            echo "Discarded."
            ;;
    esac

    exit 0
fi

# ===========================================================================
# NORMAL MODE (existing logic + filter)
# ===========================================================================

# Check for fetch_profile and warn if missing
HAS_PROFILE=$(echo "$MANIFEST_CONTENT" | python -c "
import sys, json
try:
    m = json.load(sys.stdin)
    print('true' if m.get('fetch_profile') else 'false')
except:
    print('false')
" 2>/dev/null || echo "false")

if [[ "$HAS_PROFILE" == "false" && "$COLD_START" == "false" ]]; then
    echo "WARNING: No fetch_profile found. IPE docs (releases, fatos relevantes) will be"
    echo "         downloaded without filtering. Run with --discover to create a profile."
    echo ""
fi

python -c "
import sys
template = open(sys.argv[1]).read()
manifest = open(sys.argv[2]).read()
replacements = {
    '{{TICKER}}': sys.argv[3],
    '{{EMPRESA}}': sys.argv[4],
    '{{COLD_START}}': sys.argv[5],
    '{{HORIZON_FROM}}': sys.argv[6],
    '{{TYPES}}': sys.argv[7],
    '{{UNDIGESTED_PATH}}': sys.argv[8],
    '{{MANIFESTS_PATH}}': sys.argv[9],
    '{{TODAY}}': sys.argv[10],
    '{{DISPLAY_NAME}}': sys.argv[11],
    '{{MANIFEST_CONTENT}}': manifest,
}
for k, v in replacements.items():
    template = template.replace(k, v)
open(sys.argv[12], 'w', encoding='utf-8').write(template)
" "$PROMPT_TEMPLATE" "$MANIFEST_FILE" "$TICKER" "$EMPRESA" "$COLD_START" \
  "$HORIZON_FROM" "$TYPES" "$UNDIGESTED_PATH" "$MANIFESTS_PATH" "$TODAY" \
  "$DISPLAY_NAME" "$PROMPT_FILE"

echo ""
echo "Invoking Claude agent..."
echo "========================"
echo ""

# --- Invoke Claude ---
cat "$PROMPT_FILE" | claude --print \
    --allowedTools "Bash" \
    --permission-mode bypassPermissions
