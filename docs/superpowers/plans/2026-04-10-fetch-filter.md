# Fetch Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add document filtering to the fetch agent — human-in-the-loop discovery for first run, automatic filtering after.

**Architecture:** New `--discover` flag triggers a discovery prompt that downloads one quarter of IPE docs, classifies them, and proposes a `fetch_profile` saved to the manifest. Normal mode reads the profile and filters downloads automatically. DFP/ITR bypass filtering entirely.

**Tech Stack:** Bash, Python (cvm-api), Claude CLI (`claude --print`)

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `tools/prompts/fetch_discover.md` | Create | Discovery prompt: inspect downloaded PDFs, classify into categories, output JSON fetch_profile |
| `tools/fetch.sh` | Modify | Add `--discover` flag, discovery flow (download sample → invoke discovery prompt → human approval → save to manifest), temp dir management |
| `tools/prompts/fetch_system.md` | Modify | Add filtering section: when `fetch_profile` exists, classify each IPE doc and apply include/exclude; DFP/ITR bypass |

---

### Task 1: Create `tools/prompts/fetch_discover.md`

**Files:**
- Create: `tools/prompts/fetch_discover.md`

The discovery prompt. The LLM receives a list of downloaded files with their `original_filename` and inspects them to classify into categories.

- [ ] **Step 1: Create the discovery prompt**

Create `tools/prompts/fetch_discover.md` with this content:

```markdown
# Fetch Discovery — System Prompt

You are a document classifier for the equity-wiki fetch agent. Your job is to inspect a sample of downloaded CVM filings and propose a fetch_profile that categorizes them for future filtering.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}
- **Sample period:** {{SAMPLE_PERIOD}}
- **Temp directory:** {{TEMP_DIR}}

## Downloaded files

{{FILE_LIST}}

## Your tools

You have one tool: bash. Use it to inspect the downloaded files:

- `ls -lh {{TEMP_DIR}}/` — list files with sizes
- `python -c "..."` — run Python to read PDF metadata or first pages

To read the first page of a PDF for classification:
```bash
python -c "
from pathlib import Path
import subprocess
f = Path('{{TEMP_DIR}}/filename.pdf')
result = subprocess.run(['python', '-m', 'opendataloader_pdf', str(f), '--format', 'markdown', '--pages', '1'], capture_output=True, text=True)
print(result.stdout[:2000] if result.stdout else 'Could not read PDF')
"
```

If opendataloader-pdf is not available, use pdfplumber or read the filename:
```bash
python -c "
import pdfplumber
with pdfplumber.open('{{TEMP_DIR}}/filename.pdf') as pdf:
    if pdf.pages:
        print(pdf.pages[0].extract_text()[:2000])
"
```

## Algorithm

1. **List** all files in `{{TEMP_DIR}}/` with their sizes.

2. **Inspect** each file:
   - Read the `original_filename` from the filename itself
   - Read the first page to understand the document type
   - Note the language (PT/EN), the document purpose (release, presentation, securitizadora report, etc.)

3. **Classify** each file into a functional category. Common categories for Brazilian companies:
   - `release_resultado_pt` — Earnings release in Portuguese
   - `release_resultado_en` — Earnings release in English (duplicate)
   - `apresentacao_resultado` — Earnings presentation / deck
   - `relatorio_securitizadora` — Securitizadora / fiduciary agent report
   - `press_release_operacional` — Operational press release (prévia)
   - `fato_relevante` — Fatos relevantes (material facts)
   - Create additional categories as needed based on what you find

4. **Propose** a fetch_profile as a JSON object. For each category, recommend `include` or `exclude`:
   - Include: documents useful for financial analysis (PT releases, presentations, fatos relevantes)
   - Exclude: duplicates (EN versions), non-analytical reports (securitizadora)

5. **Output** the profile in EXACTLY this format (the script will parse it):

```
===FETCH_PROFILE_START===
{
  "_created": "{{TODAY}}",
  "_sample_period": "{{SAMPLE_PERIOD}}",
  "categories": {
    "category_name": {
      "action": "include",
      "description": "Human-readable description",
      "sample_files": ["filename1.pdf"]
    }
  }
}
===FETCH_PROFILE_END===
```

After the JSON block, print a human-readable summary:

```
=== Fetch Profile proposto para {{TICKER}} (amostra: {{SAMPLE_PERIOD}}) ===

  [include] category_name  — description (size)
  [exclude] category_name  — description (size)
```

## Rules

- Inspect EVERY file in the temp directory
- Each file must be classified into exactly one category
- Output the JSON block between the markers — the script depends on this
- Use snake_case for category names
- Keep descriptions concise (under 80 chars)
- When in doubt, recommend `include` (better to have too much than miss something)
```

- [ ] **Step 2: Verify all placeholders**

Confirm these placeholders exist in the file: `TICKER`, `EMPRESA`, `SAMPLE_PERIOD`, `TEMP_DIR`, `FILE_LIST`, `TODAY`.

- [ ] **Step 3: Commit**

```bash
git add tools/prompts/fetch_discover.md
git commit -m "feat: add discovery prompt for fetch profile classification"
```

---

### Task 2: Modify `tools/fetch.sh` — add `--discover` mode

**Files:**
- Modify: `tools/fetch.sh`

Add `--discover` flag and the full discovery flow: download sample quarter, invoke discovery prompt, parse profile JSON, human approval, save to manifest.

- [ ] **Step 1: Update the full `tools/fetch.sh`**

Replace the entire file with:

```bash
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
# Get the most recent periodo that has releases (not just fato_relevante)
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

    # Filter docs for the sample period and download each
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
# Validate it's valid JSON
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
            # Save fetch_profile to manifest
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
```

- [ ] **Step 2: Verify `--discover` flag is parsed**

Run:
```bash
bash tools/fetch.sh TEND3 --discover
```

This will trigger the full discovery flow. Verify it:
- Lists recent releases/fatos relevantes
- Identifies a sample period
- Downloads docs to temp dir
- Invokes Claude for classification
- Shows proposed profile
- Prompts for approval

Type `n` to discard for now (this is a verification run).

- [ ] **Step 3: Verify normal mode still works**

Run:
```bash
bash tools/fetch.sh
```
Expected: Usage message (no args).

- [ ] **Step 4: Commit**

```bash
git add tools/fetch.sh
git commit -m "feat: add --discover mode to fetch.sh for fetch profile creation"
```

---

### Task 3: Modify `tools/prompts/fetch_system.md` — add filtering

**Files:**
- Modify: `tools/prompts/fetch_system.md`

Add a filtering section so the normal-mode agent uses `fetch_profile` from the manifest to filter IPE documents.

- [ ] **Step 1: Update `tools/prompts/fetch_system.md`**

Replace the entire file with:

```markdown
# Fetch Agent — System Prompt

You are a data collection agent for the equity-wiki. Your sole job is to identify missing CVM filings for a company and download them to the undigested inbox.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}
- **Cold start:** {{COLD_START}}
- **Horizon from:** {{HORIZON_FROM}}
- **Document types:** {{TYPES}}
- **Undigested path:** {{UNDIGESTED_PATH}}
- **Manifests path:** {{MANIFESTS_PATH}}

## Current manifest

{{MANIFEST_CONTENT}}

## Your tools

You have one tool: bash. Use it ONLY to invoke `python tools/lib/cvm_fetch.py` with these subcommands:

### resolve
```bash
python tools/lib/cvm_fetch.py resolve {{TICKER}}
```
Returns company info (ticker, nome, cvm_code, setor).

### list
```bash
python tools/lib/cvm_fetch.py list {{TICKER}} --types {{TYPES}} --from {{HORIZON_FROM}}
```
Returns a JSON array of documents available on CVM, sorted from most recent to oldest. Each entry has: `tipo`, `periodo`, `num_sequencia`, `num_versao`, `numero_protocolo`, `desc_tipo`.

### download
```bash
python tools/lib/cvm_fetch.py download --num-sequencia <X> --num-versao <Y> --numero-protocolo <Z> --desc-tipo <W> --output <path>
```
Downloads a filing to the specified path. The download response includes `original_filename` which you should use for classification.

Output path for final files: `{{UNDIGESTED_PATH}}/{{TICKER}}_{periodo}_{tipo}_{num_sequencia}.{ext}`

The extension depends on what the CVM returns:
- DFP/ITR (EST documents) → `.zip` (contains XML/XBRL structured data)
- Releases/Fatos relevantes (IPE documents) → `.pdf`

Examples: `{{UNDIGESTED_PATH}}/TEND3_2025_dfp.zip`, `{{UNDIGESTED_PATH}}/TEND3_4T25_release_1010843.pdf`

## Algorithm

1. **Resolve** the company via `cvm_fetch.py resolve` to confirm it exists.

2. **List** available documents via `cvm_fetch.py list`.

3. **Detect gaps** — compare the list against the manifest:
   - For each document type (dfp, itr, release, fato_relevante), iterate from most recent to oldest.
   - A document is a **gap** if its `periodo` + `tipo` combination does not appear in the manifest's `sources[]` array (match on `type` and `asof` fields).
   - **Stop condition per type:** when you find a `periodo` that already exists in the manifest for that type, stop — everything older is assumed covered.
   - If `{{COLD_START}}` is `true`, there is no manifest to compare — everything up to `{{HORIZON_FROM}}` is a gap.

4. **Download and filter** each gap:

   **For DFP/ITR (tipo = dfp or itr):** Always download directly to `{{UNDIGESTED_PATH}}/`. No filtering.

   **For releases/fatos relevantes (tipo = release or fato_relevante):**
   - Check if the manifest has a `fetch_profile` field.
   - **If fetch_profile exists:** Download each doc, then classify it into one of the categories in `fetch_profile.categories` using the `description` and `sample_files` as reference. Check `original_filename` from the download response for clues (language, document type).
     - If the matching category has `"action": "include"` → keep the file in `{{UNDIGESTED_PATH}}/`
     - If the matching category has `"action": "exclude"` → delete the file and report it as filtered
     - If no category matches → keep the file (include by default) and report as "unclassified"
   - **If no fetch_profile:** Download everything to `{{UNDIGESTED_PATH}}/` (no filtering).

5. **Cold-start manifest** — if `{{COLD_START}}` is `true`, create a skeleton manifest:
   ```bash
   cat > {{MANIFESTS_PATH}}/{{EMPRESA}}.json << 'SKELETON'
   {
     "_schema": "manifest/v1",
     "_updated": "{{TODAY}}",
     "empresa": "{{EMPRESA}}",
     "display_name": "{{DISPLAY_NAME}}",
     "aliases": ["{{TICKER}}"],
     "ticker": "{{TICKER}}",
     "setor": "unknown",
     "sources": [],
     "coverage": {},
     "precedence": [],
     "caveats": ["cold-start — manifest criado por fetch agent, pendente ingest"]
   }
   SKELETON
   ```
   Fill `display_name` from the resolve output. Set `setor` to `"unknown"` — the ingest step will correct it.

6. **Report** — print a summary listing:
   - Documents downloaded (tipo, periodo, path, category if classified)
   - Documents filtered out (tipo, periodo, category, reason)
   - Documents unclassified (tipo, periodo — included by default)
   - Documents skipped (already in manifest)
   - Errors (if any)

## Rules

- Do NOT edit wiki pages, structured/, full/, or digested/ files.
- Do NOT run the ingest process.
- Do NOT modify an existing manifest (only create skeleton on cold-start).
- If `cvm_fetch.py` returns `{"status": "error", ...}`, report the error and continue.
- Download only file types listed in `{{TYPES}}`.
- When classifying, use the `description` and `sample_files` in the fetch_profile as your guide. Match by document purpose and language, not by exact filename.
```

- [ ] **Step 2: Verify placeholders are consistent with fetch.sh**

All existing placeholders must still be present: `TICKER`, `EMPRESA`, `COLD_START`, `HORIZON_FROM`, `TYPES`, `UNDIGESTED_PATH`, `MANIFESTS_PATH`, `MANIFEST_CONTENT`, `TODAY`, `DISPLAY_NAME`.

- [ ] **Step 3: Commit**

```bash
git add tools/prompts/fetch_system.md
git commit -m "feat: add fetch_profile filtering to normal-mode system prompt"
```

---

### Task 4: End-to-end verification

- [ ] **Step 1: Clean up previous unfiltered downloads**

First, remove the previously downloaded unfiltered files so we start clean:
```bash
rm -f sources/undigested/TEND3_*_release_*.pdf sources/undigested/TEND3_*_fato_relevante_*.pdf
```
Keep the ITR zips (those are valid downloads).

- [ ] **Step 2: Run discovery for Tenda**

```bash
bash tools/fetch.sh TEND3 --discover
```

Verify:
- Agent downloads sample quarter docs to temp dir
- Classifies them into categories (release_resultado_pt, release_resultado_en, etc.)
- Proposes a fetch_profile with include/exclude
- Prompts for approval

Type `s` to save the profile.

- [ ] **Step 3: Verify fetch_profile was saved to manifest**

```bash
python -c "import json; m=json.load(open('sources/manifests/tenda.json')); print(json.dumps(m.get('fetch_profile',{}), indent=2, ensure_ascii=False))"
```

Expected: JSON with categories, each having action/description/sample_files.

- [ ] **Step 4: Run normal fetch with filter**

```bash
bash tools/fetch.sh TEND3 --horizon 1y --types release,fato_relevante
```

Verify:
- Agent downloads releases/fatos relevantes
- Classifies each one against the fetch_profile
- Includes only docs matching `include` categories
- Filters out `exclude` categories
- Reports summary with included/filtered/unclassified counts

- [ ] **Step 5: Commit**

```bash
git add sources/manifests/tenda.json
git commit -m "feat: add fetch_profile to tenda manifest via discovery"
```
