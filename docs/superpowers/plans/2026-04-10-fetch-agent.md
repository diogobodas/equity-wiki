# Fetch Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bash-invoked LLM agent that fetches missing CVM filings for a given ticker and deposits them into `sources/undigested/`.

**Architecture:** `fetch.sh` (entry point) resolves context and invokes `claude --print` with a system prompt. The LLM uses `cvm_fetch.py` (Python CLI wrapper over the `cvm-api` package) as its only tool to resolve companies, list available documents, and download files.

**Tech Stack:** Bash, Python 3.10+ (`cvm-api` package), Claude CLI (`claude --print`)

---

## File Structure

| File | Responsibility |
|------|---------------|
| `tools/lib/cvm_fetch.py` | Stateless CLI wrapper: `resolve`, `list`, `download` subcommands. JSON output. Bridges async CVM-API to sync CLI. |
| `tools/prompts/fetch_system.md` | System prompt template with `{{VARIABLE}}` placeholders. Instructs the LLM on gap detection and download logic. |
| `tools/fetch.sh` | Entry point. Parses args, resolves manifest, injects variables into prompt, invokes `claude --print`. |

---

### Task 1: `tools/lib/cvm_fetch.py`

**Files:**
- Create: `tools/lib/cvm_fetch.py`

This is the Python CLI that the LLM agent calls via bash. Three subcommands, all outputting JSON to stdout.

The CVM-API is async-only for `buscar_documentos` and `baixar_documento`, so we use `asyncio.run()` to bridge.

Key mappings:
- CVM category codes: `dfp` → `EST_4`, `itr` → `EST_3`, `release` → `IPE_7_-1_-1`, `fato_relevante` → `IPE_4_-1_-1`
- Period normalization: `data_referencia` (YYYY-MM-DD) → wiki format. For ITR: month 3→1T, 6→2T, 9→3T, 12→4T + short year. For DFP: just the year. For eventuais (release, fato_relevante): derive from `data_referencia` same as ITR/DFP.

- [ ] **Step 1: Create `tools/lib/cvm_fetch.py` with `resolve` subcommand**

```python
#!/usr/bin/env python3
"""CLI wrapper over cvm-api for the fetch agent. JSON output, stateless."""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path


def json_out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def error_out(msg):
    json_out({"status": "error", "message": msg})
    sys.exit(1)


# --- Category mapping ---
TYPE_TO_CVM = {
    "dfp": "EST_4",
    "itr": "EST_3",
    "release": "IPE_7_-1_-1",
    "fato_relevante": "IPE_4_-1_-1",
}


def normalize_periodo(data_referencia: str, tipo_wiki: str) -> str:
    """Convert CVM data_referencia (DD/MM/YYYY or YYYY-MM-DD) to wiki period format."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(data_referencia, fmt)
            break
        except ValueError:
            continue
    else:
        return data_referencia

    year_short = str(dt.year)[2:]
    if tipo_wiki == "dfp":
        return str(dt.year)
    month_to_quarter = {3: "1T", 6: "2T", 9: "3T", 12: "4T"}
    quarter = month_to_quarter.get(dt.month)
    if quarter:
        return f"{quarter}{year_short}"
    # Fallback for months that don't align to quarter-end (eventuais)
    q = (dt.month - 1) // 3 + 1
    return f"{q}T{year_short}"


# --- Subcommands ---

def cmd_resolve(args):
    from cvm_api import resolve_company, CompanyNotFoundError
    try:
        company = resolve_company(args.ticker)
        json_out({
            "status": "ok",
            "ticker": company.ticker,
            "nome": company.name,
            "cvm_code": company.cvm_code,
            "setor": company.sector,
        })
    except CompanyNotFoundError as e:
        error_out(str(e))


async def _list_docs(args):
    from cvm_api import resolve_company, buscar_documentos, CompanyNotFoundError

    try:
        company = resolve_company(args.ticker)
    except CompanyNotFoundError as e:
        error_out(str(e))

    types = [t.strip() for t in args.types.split(",")]
    date_from = datetime.strptime(args.date_from, "%Y-%m-%d")
    results = []

    for tipo_wiki in types:
        cvm_cat = TYPE_TO_CVM.get(tipo_wiki)
        if not cvm_cat:
            continue
        docs = await buscar_documentos(
            empresa=company.cvm_code,
            categoria=cvm_cat,
            data_de=date_from.strftime("%d/%m/%Y"),
            data_ate=datetime.now().strftime("%d/%m/%Y"),
            periodo="2",
        )
        for doc in docs:
            periodo = normalize_periodo(doc.data_referencia, tipo_wiki)
            results.append({
                "tipo": tipo_wiki,
                "periodo": periodo,
                "data_ref": doc.data_referencia,
                "data_entrega": doc.data_entrega,
                "num_sequencia": doc.num_sequencia,
                "num_versao": doc.num_versao,
                "numero_protocolo": doc.numero_protocolo,
                "desc_tipo": doc.desc_tipo,
                "empresa_cvm": doc.empresa,
                "versao": doc.versao,
            })

    # Sort: most recent first (by data_ref descending)
    def sort_key(r):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(r["data_ref"], fmt)
            except ValueError:
                continue
        return datetime.min
    results.sort(key=sort_key, reverse=True)

    json_out(results)


def cmd_list(args):
    asyncio.run(_list_docs(args))


async def _download(args):
    from cvm_api import baixar_documento

    file_bytes, filename, content_type = await baixar_documento(
        num_sequencia=args.num_sequencia,
        num_versao=args.num_versao,
        numero_protocolo=args.numero_protocolo,
        desc_tipo=args.desc_tipo,
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(file_bytes)
    json_out({
        "status": "ok",
        "path": str(output_path),
        "size_bytes": len(file_bytes),
        "original_filename": filename,
        "content_type": content_type,
    })


def cmd_download(args):
    asyncio.run(_download(args))


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="CVM fetch tool for equity-wiki")
    sub = parser.add_subparsers(dest="command", required=True)

    # resolve
    p_resolve = sub.add_parser("resolve", help="Resolve ticker to company info")
    p_resolve.add_argument("ticker", help="e.g. TEND3")

    # list
    p_list = sub.add_parser("list", help="List available documents from CVM")
    p_list.add_argument("ticker", help="e.g. TEND3")
    p_list.add_argument("--types", default="dfp,itr,release,fato_relevante",
                        help="Comma-separated document types")
    p_list.add_argument("--from", dest="date_from", required=True,
                        help="Start date YYYY-MM-DD")

    # download
    p_dl = sub.add_parser("download", help="Download a specific document")
    p_dl.add_argument("--num-sequencia", required=True)
    p_dl.add_argument("--num-versao", required=True)
    p_dl.add_argument("--numero-protocolo", required=True)
    p_dl.add_argument("--desc-tipo", required=True)
    p_dl.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()
    {"resolve": cmd_resolve, "list": cmd_list, "download": cmd_download}[args.command](args)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify `resolve` works**

Run:
```bash
cd "P:/Diogo/Projeto Modelo AI/equity-wiki"
python tools/lib/cvm_fetch.py resolve TEND3
```
Expected: JSON with `{"status": "ok", "ticker": "TEND3", "nome": "Construtora Tenda S.A.", ...}`

- [ ] **Step 3: Verify `list` works**

Run:
```bash
python tools/lib/cvm_fetch.py list TEND3 --types dfp,itr --from 2024-01-01
```
Expected: JSON array of documents sorted by date descending, each with `tipo`, `periodo`, `num_sequencia`, etc.

- [ ] **Step 4: Verify `download` works**

Pick a `num_sequencia`/`num_versao`/`numero_protocolo`/`desc_tipo` from the list output and run:
```bash
python tools/lib/cvm_fetch.py download --num-sequencia <X> --num-versao <Y> --numero-protocolo <Z> --desc-tipo <W> --output sources/undigested/TEST_download.pdf
```
Expected: JSON with `{"status": "ok", "path": "...", "size_bytes": ...}` and a non-empty file on disk. Then delete the test file.

- [ ] **Step 5: Commit**

```bash
git add tools/lib/cvm_fetch.py
git commit -m "feat: add cvm_fetch.py CLI wrapper for fetch agent"
```

---

### Task 2: `tools/prompts/fetch_system.md`

**Files:**
- Create: `tools/prompts/fetch_system.md`

The system prompt template. `fetch.sh` will replace `{{PLACEHOLDERS}}` with actual values before passing to `claude --print`.

- [ ] **Step 1: Create the system prompt**

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
Downloads a filing to the specified path. Output path MUST follow: `{{UNDIGESTED_PATH}}/{{TICKER}}_{periodo}_{tipo}.pdf`

Example: `{{UNDIGESTED_PATH}}/TEND3_4T25_dfp.pdf`

## Algorithm

1. **Resolve** the company via `cvm_fetch.py resolve` to confirm it exists.

2. **List** available documents via `cvm_fetch.py list`.

3. **Detect gaps** — compare the list against the manifest:
   - For each document type (dfp, itr, release, fato_relevante), iterate from most recent to oldest.
   - A document is a **gap** if its `periodo` + `tipo` combination does not appear in the manifest's `sources[]` array (match on `type` and `asof` fields).
   - **Stop condition per type:** when you find a `periodo` that already exists in the manifest for that type, stop — everything older is assumed covered.
   - If `{{COLD_START}}` is `true`, there is no manifest to compare — everything up to `{{HORIZON_FROM}}` is a gap.

4. **Download** each gap:
   - Output path: `{{UNDIGESTED_PATH}}/{{TICKER}}_{periodo}_{tipo}.pdf`
   - If the download returns an error, log it and continue with the next document.

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
   - Documents downloaded (tipo, periodo, path)
   - Documents skipped (already in manifest)
   - Errors (if any)

## Rules

- Do NOT edit wiki pages, structured/, full/, or digested/ files.
- Do NOT run the ingest process.
- Do NOT modify an existing manifest (only create skeleton on cold-start).
- If `cvm_fetch.py` returns `{"status": "error", ...}`, report the error and continue.
- Download only file types listed in `{{TYPES}}`.
```

- [ ] **Step 2: Verify the template renders correctly (manual check)**

Confirm all `{{PLACEHOLDERS}}` match what `fetch.sh` will inject: `TICKER`, `EMPRESA`, `COLD_START`, `HORIZON_FROM`, `TYPES`, `UNDIGESTED_PATH`, `MANIFESTS_PATH`, `MANIFEST_CONTENT`, `TODAY`, `DISPLAY_NAME`.

- [ ] **Step 3: Commit**

```bash
git add tools/prompts/fetch_system.md
git commit -m "feat: add fetch agent system prompt template"
```

---

### Task 3: `tools/fetch.sh`

**Files:**
- Create: `tools/fetch.sh`

Entry point bash script. Parses args, resolves context, injects variables into the prompt template, invokes `claude --print`.

- [ ] **Step 1: Create `tools/fetch.sh`**

```bash
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
# Accepts formats like "3y", "2y", "18m"
compute_horizon_from() {
    local h="$1"
    local num="${h%[ym]}"
    local unit="${h: -1}"
    local now
    now=$(date +%Y-%m-%d)
    if [[ "$unit" == "y" ]]; then
        local year_offset=$((num))
        local current_year current_month current_day
        current_year=$(date +%Y)
        current_month=$(date +%m)
        current_day=$(date +%d)
        echo "$((current_year - year_offset))-${current_month}-${current_day}"
    elif [[ "$unit" == "m" ]]; then
        # Use python for reliable month arithmetic
        python -c "
from datetime import datetime
from dateutil.relativedelta import relativedelta
d = datetime.now() - relativedelta(months=$num)
print(d.strftime('%Y-%m-%d'))
"
    else
        echo "$now"
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
MANIFEST_CONTENT="null (cold-start — no manifest found for this ticker)"

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
    # Extract nome for display_name, lowercase for empresa
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
```

- [ ] **Step 2: Make executable and verify arg parsing**

Run:
```bash
chmod +x tools/fetch.sh
bash tools/fetch.sh
```
Expected: Usage message printed.

Run:
```bash
bash tools/fetch.sh TEND3 --horizon 2y
```
Expected: Resolves manifest, prints context, invokes Claude. Verify the output shows correct ticker, horizon date (~2024-04-10), and "Found manifest: sources/manifests/tenda.json".

- [ ] **Step 3: Test cold-start path**

Run:
```bash
bash tools/fetch.sh CYRE3
```
Expected: "No manifest found for CYRE3 — cold-start mode", resolves via CVM-API, invokes Claude. The agent should create a skeleton manifest and download available filings.

- [ ] **Step 4: Commit**

```bash
git add tools/fetch.sh
git commit -m "feat: add fetch.sh entry point for fetch agent"
```

---

### Task 4: End-to-end verification

- [ ] **Step 1: Run full fetch for existing company (Tenda)**

```bash
bash tools/fetch.sh TEND3 --horizon 1y --types dfp,itr
```

Verify:
- Agent resolves Tenda from manifest
- Lists CVM documents
- Compares with manifest sources (DFP 2025 and 2024 already ingested)
- Downloads only gaps (e.g., ITR 1T25, 2T25, 3T25 if not in manifest)
- Files appear in `sources/undigested/` with correct naming

- [ ] **Step 2: Run cold-start for new company**

```bash
bash tools/fetch.sh CYRE3 --horizon 1y
```

Verify:
- Agent creates skeleton manifest at `sources/manifests/cyrela.json` (or similar)
- Downloads DFP, ITR, releases, fatos relevantes for the last year
- Files appear in `sources/undigested/`

- [ ] **Step 3: Clean up test files**

Remove any test downloads from `sources/undigested/` and any skeleton manifests that were just for testing. Keep only what's intentionally ingested.

- [ ] **Step 4: Final commit**

```bash
git add -A tools/
git commit -m "feat: fetch agent — complete MVP for CVM data collection"
```
