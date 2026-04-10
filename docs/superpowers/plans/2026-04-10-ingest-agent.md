# Ingest Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `tools/ingest.sh` — a bash agent that processes all files in `sources/undigested/` for a ticker, producing full/, structured/, digested/, updating wiki pages, manifest, and log.

**Architecture:** `ingest.sh` scans undigested/, pre-processes PDFs via `pdf_extract.py`, invokes `claude --print` per batch (heavy ITR/DFP, heavy release, light fatos, wiki update), then updates manifest/log deterministically via `manifest_update.py`.

**Tech Stack:** Bash, Python 3.10+ (pdfplumber, opendataloader-pdf), Claude CLI

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `tools/lib/pdf_extract.py` | Create | Extract text from PDF/ZIP. Opendataloader first, fallback pdfplumber. JSON stdout. |
| `tools/lib/manifest_update.py` | Create | Deterministic manifest/log/index updates. No LLM. |
| `tools/prompts/ingest_heavy.md` | Create | Prompt for ITR/DFP/release → full/ + structured/ + digested/ |
| `tools/prompts/ingest_light.md` | Create | Prompt for fatos relevantes → full/ + digested/ |
| `tools/prompts/ingest_wiki_update.md` | Create | Prompt for updating wiki pages from digested/ |
| `tools/ingest.sh` | Create | Entry point orchestrating the full pipeline |

---

### Task 1: Create `tools/lib/pdf_extract.py`

**Files:**
- Create: `tools/lib/pdf_extract.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""Extract text from PDF or ZIP-containing-PDF. Tries opendataloader-pdf first, falls back to pdfplumber."""

import argparse
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def json_out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def error_out(msg):
    json_out({"status": "error", "message": msg})
    sys.exit(1)


def extract_pdf_from_zip(zip_path: Path) -> Path:
    """Extract the first PDF found inside a ZIP to a temp file. Returns path to extracted PDF."""
    with zipfile.ZipFile(zip_path) as zf:
        pdf_names = [n for n in zf.namelist() if n.lower().endswith('.pdf')]
        if not pdf_names:
            error_out(f"No PDF found inside {zip_path}")
        data = zf.read(pdf_names[0])
        tmp = Path(tempfile.mktemp(suffix='.pdf', dir=str(zip_path.parent)))
        tmp.write_bytes(data)
        return tmp


def try_opendataloader(pdf_path: Path, output_path: Path) -> bool:
    """Try opendataloader-pdf. Returns True if successful."""
    try:
        result = subprocess.run(
            [
                sys.executable, '-m', 'opendataloader_pdf',
                str(pdf_path),
                '--format', 'markdown',
                '--use-struct-tree',
                '--table-method', 'cluster',
                '-o', str(output_path),
            ],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 100:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False


def extract_with_pdfplumber(pdf_path: Path, output_path: Path) -> int:
    """Extract text using pdfplumber. Returns page count."""
    import pdfplumber
    pdf = pdfplumber.open(str(pdf_path))
    pages = []
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ''
        pages.append(f'<!-- PAGE {i + 1} -->\n{text}')
    output_path.write_text('\n\n'.join(pages), encoding='utf-8')
    return len(pdf.pages)


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF/ZIP for wiki ingest")
    parser.add_argument("input", help="Path to PDF or ZIP file")
    parser.add_argument("--output", help="Output markdown path (default: {input}_extracted.md)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        error_out(f"File not found: {input_path}")

    # Determine output path
    stem = input_path.stem
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{stem}_extracted.md"

    # Handle ZIP
    tmp_pdf = None
    if input_path.suffix.lower() == '.zip':
        tmp_pdf = extract_pdf_from_zip(input_path)
        pdf_path = tmp_pdf
    else:
        pdf_path = input_path

    # Try opendataloader first
    method = "opendataloader"
    if not try_opendataloader(pdf_path, output_path):
        # Fallback to pdfplumber
        method = "pdfplumber"
        try:
            page_count = extract_with_pdfplumber(pdf_path, output_path)
        except Exception as e:
            if tmp_pdf:
                tmp_pdf.unlink(missing_ok=True)
            error_out(f"Both extraction methods failed: {e}")
    else:
        page_count = None

    # Count pages if opendataloader succeeded (read the output)
    if page_count is None:
        content = output_path.read_text(encoding='utf-8')
        page_count = content.count('<!-- PAGE ') or content.count('\n# ') or 1

    chars = output_path.stat().st_size

    # Cleanup temp PDF from ZIP
    if tmp_pdf:
        tmp_pdf.unlink(missing_ok=True)

    json_out({
        "status": "ok",
        "output": str(output_path),
        "pages": page_count,
        "chars": chars,
        "method": method,
    })


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test with a PDF**

Create a small test by re-downloading one fato relevante (small file):
```bash
python tools/lib/cvm_fetch.py download --num-sequencia 1025459 --num-versao 1 --numero-protocolo 021148IPE020420260100 --desc-tipo IPE --output sources/undigested/test_extract.pdf
python tools/lib/pdf_extract.py sources/undigested/test_extract.pdf
```
Expected: JSON with `status: ok`, `method: opendataloader` or `pdfplumber`, output file exists.

Then clean up:
```bash
rm -f sources/undigested/test_extract.pdf sources/undigested/test_extract_extracted.md
```

- [ ] **Step 3: Commit**

```bash
git add tools/lib/pdf_extract.py
git commit -m "feat: add pdf_extract.py — text extraction with opendataloader/pdfplumber fallback"
```

---

### Task 2: Create `tools/lib/manifest_update.py`

**Files:**
- Create: `tools/lib/manifest_update.py`

- [ ] **Step 1: Create the file**

```python
#!/usr/bin/env python3
"""Deterministic manifest/log/index updates for the ingest pipeline. No LLM."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Update manifest, log, and index after ingest")
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON")
    parser.add_argument("--type", required=True, choices=["itr", "dfp", "release", "fato_relevante"],
                        help="Document type")
    parser.add_argument("--period", required=True, help="Period code (e.g. 3T25, 2025)")
    parser.add_argument("--full", required=True, help="Path to full/ file produced")
    parser.add_argument("--structured", default=None, help="Path to structured/ file (heavy path only)")
    parser.add_argument("--digested", default=None, help="Path to digested/ file")
    parser.add_argument("--log", default="log.md", help="Path to log file")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(json.dumps({"status": "error", "message": f"Manifest not found: {manifest_path}"}))
        sys.exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    today = date.today().isoformat()

    # Build source entry
    source_entry = {
        "type": args.type,
        "asof": args.period,
        "ingested_on": today,
        "full": args.full,
    }
    if args.structured:
        source_entry["structured"] = [args.structured]
    if args.digested:
        source_entry["digested"] = args.digested

    # Add to sources (avoid duplicates by type+asof+full)
    existing = [s for s in manifest.get("sources", [])
                if s.get("type") == args.type and s.get("asof") == args.period and s.get("full") == args.full]
    if not existing:
        manifest.setdefault("sources", []).append(source_entry)

    # Update coverage for heavy path
    if args.type in ("itr", "dfp") and args.structured:
        coverage = manifest.setdefault("coverage", {}).setdefault(args.period, {})
        for block in ("dre", "bp"):
            coverage[block] = {"status": "filled", "source": args.structured}

    if args.type == "release" and args.structured:
        coverage = manifest.setdefault("coverage", {}).setdefault(args.period, {})
        coverage["financeiro_ajustado"] = {"status": "filled", "source": args.structured}

    # Update timestamp
    manifest["_updated"] = today

    # Write manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write('\n')

    # Append to log
    log_path = Path(args.log)
    log_line = f"{today} — ingest {args.type} {args.period}: {args.full}"
    if args.structured:
        log_line += f", {args.structured}"
    if args.digested:
        log_line += f", {args.digested}"
    log_line += "\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_line)

    print(json.dumps({
        "status": "ok",
        "manifest": str(manifest_path),
        "type": args.type,
        "period": args.period,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify it runs without error (dry concept check)**

```bash
python tools/lib/manifest_update.py --help
```
Expected: Help text with all arguments listed.

- [ ] **Step 3: Commit**

```bash
git add tools/lib/manifest_update.py
git commit -m "feat: add manifest_update.py — deterministic manifest/log updates"
```

---

### Task 3: Create prompts (`ingest_heavy.md`, `ingest_light.md`, `ingest_wiki_update.md`)

**Files:**
- Create: `tools/prompts/ingest_heavy.md`
- Create: `tools/prompts/ingest_light.md`
- Create: `tools/prompts/ingest_wiki_update.md`

- [ ] **Step 1: Create `tools/prompts/ingest_heavy.md`**

```markdown
# Ingest Heavy — System Prompt

You are an ingest agent for the equity-wiki. Your job is to process extracted financial documents (ITR, DFP, or earnings releases) and produce structured wiki layers.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}
- **Document type:** {{DOC_TYPE}}
- **Schema path:** {{SCHEMA_PATH}}

## Files to process

{{FILE_LIST}}

Each file is an extracted markdown at the path shown. Read it via bash:
```bash
cat "path/to/file_extracted.md"
```

For large files, read in sections:
```bash
head -500 "path/to/file_extracted.md"
tail -n +500 "path/to/file_extracted.md" | head -500
```

## Schema

Read the canonical schema for reference:
```bash
cat {{SCHEMA_PATH}}
```

## What to produce for EACH file

### 1. `sources/full/{{EMPRESA}}/{periodo}/{tipo}.md`

Structured-but-uncut transcription. Organize with headings:

**For ITR/DFP:**
- `# {tipo_upper} {periodo} — {display_name}`
- `## Composição do Capital`
- `## DFs Individuais` → sub-headings: BP Ativo, BP Passivo, DRE, DRA, DFC, DMPL, DVA
- `## DFs Consolidadas` → same sub-headings
- `## Comentário do Desempenho`
- `## Notas Explicativas` → each nota as `### Nota N — título`
- `## Pareceres`

**For releases:**
- `# Release de Resultados {periodo} — {display_name}`
- Sections as they appear (Destaques, Operacional, DRE, Balanço, Endividamento, etc.)

Tables in markdown format. Content is UNCUT — transcribe everything.

### 2. `sources/structured/{{EMPRESA}}/{periodo}/{tipo}.json`

Canonical JSON following the incorporadora schema. Use CONSOLIDATED figures.

```json
{
  "_schema": "incorporadora/v1",
  "_schema_path": "{{SCHEMA_PATH}}",
  "_empresa": "{{EMPRESA}}",
  "_periodo": "{periodo}",
  "_source": "sources/full/{{EMPRESA}}/{periodo}/{tipo}.md",
  "canonical": {
    "operacional": null or { ... },
    "dre": { ... },
    "bp": { ... },
    "financeiro_ajustado": { ... }
  },
  "company_specific": { ... }
}
```

**For ITR/DFP:** Fill dre + bp from consolidated DFs. Set operacional to null (comes from release). Fill financeiro_ajustado where extractable (caixa, divida, PL). Numbers in R$ mm (divide R$ mil by 1000), 1 decimal.

**For releases:** Fill ALL blocks — operacional (lancamentos, vendas, etc.), dre, bp, financeiro_ajustado (EBITDA, margens, ROE, divida, etc.). Use QUARTER figures for DRE, end-of-period for BP.

Missing schema keys → null, never omit.

### 3. `sources/digested/{empresa}_{tipo}_{periodo}_summary.md`

Wiki-facing TL;DR, under 400 words. Key financials, trends, notable items.

## Rules

- Read each extracted file fully before producing output
- Use CONSOLIDATED figures, not individual
- Numbers as reported, converted to R$ mm
- Create directories via `mkdir -p` as needed
- Process files ONE AT A TIME — produce all 3 outputs for file 1 before moving to file 2
- Do NOT edit manifest, wiki pages, log, or index — the script handles those
```

- [ ] **Step 2: Create `tools/prompts/ingest_light.md`**

```markdown
# Ingest Light — System Prompt

You are an ingest agent for the equity-wiki. Your job is to process extracted fatos relevantes and produce wiki layers. Light path — no structured/ files.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}

## Files to process

{{FILE_LIST}}

Each file is an extracted text at the path shown. Read it via bash:
```bash
cat "path/to/file_extracted.txt"
```

## What to produce

### For EACH fato relevante:

**1. `sources/full/{{EMPRESA}}/{periodo}/fato_relevante_{seq}.md`**
- Heading: `# Fato Relevante — {título curto do assunto}`
- Full uncut transcription below
- Create directories via `mkdir -p` as needed

### ONE combined digested file per batch:

**2. `sources/digested/{{EMPRESA}}_fatos_relevantes_batch_summary.md`**
- For each fato: date, seq number, one-line summary
- Group by period
- Under 400 words total

## Rules

- Content is UNCUT in full/
- Do NOT create structured/ files
- Do NOT edit manifest, wiki pages, log, or index
- Identify what each fato is about: dividendos, debêntures, recompra, guidance, cessão, governança, etc.
```

- [ ] **Step 3: Create `tools/prompts/ingest_wiki_update.md`**

```markdown
# Wiki Update — System Prompt

You are a wiki update agent for the equity-wiki. Your job is to update the company wiki page with data from recently ingested documents.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}
- **Wiki page:** {{WIKI_PAGE}}

## Recently produced digested files

{{DIGESTED_LIST}}

Read each digested file to understand what's new:
```bash
cat "path/to/digested_file.md"
```

Then read the current wiki page:
```bash
cat "{{WIKI_PAGE}}"
```

## What to do

Update `{{WIKI_PAGE}}` with:

1. **Latest quarterly financials** — add/update tables with key metrics, citing structured/ files
2. **Operational highlights** — lancamentos, vendas, VSO, estoque from releases
3. **Guidance tracking** — any guidance updates from releases or fatos relevantes
4. **Key events** — material facts from fatos relevantes
5. **Update stale claims** — if the page has outdated numbers, update with citations

## Citation format

- Numeric: `(fonte: structured/{empresa}/{periodo}/{tipo}.json :: canonical.dre.receita_liquida)`
- Qualitative: `(fonte: full/{empresa}/{periodo}/{tipo}.md §section_name)`
- Web: `(fonte: url, confiabilidade: nivel)`

## Rules

- Keep existing content that's still valid
- Add new sections as needed
- Every factual claim needs a `(fonte: ...)` citation
- Use `[[wikilinks]]` for first mention of entities/concepts in a section
- Update frontmatter: add new source paths to `sources` list, update `updated` date
- Do NOT edit any files other than `{{WIKI_PAGE}}`
```

- [ ] **Step 4: Verify all placeholders**

Placeholders per file:
- `ingest_heavy.md`: TICKER, EMPRESA, DOC_TYPE, SCHEMA_PATH, FILE_LIST
- `ingest_light.md`: TICKER, EMPRESA, FILE_LIST
- `ingest_wiki_update.md`: TICKER, EMPRESA, WIKI_PAGE, DIGESTED_LIST

- [ ] **Step 5: Commit**

```bash
git add tools/prompts/ingest_heavy.md tools/prompts/ingest_light.md tools/prompts/ingest_wiki_update.md
git commit -m "feat: add ingest prompts — heavy, light, and wiki update"
```

---

### Task 4: Create `tools/ingest.sh`

**Files:**
- Create: `tools/ingest.sh`

The main orchestrator. This is the largest file.

- [ ] **Step 1: Create `tools/ingest.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Usage ---
usage() {
    echo "Usage: bash tools/ingest.sh <TICKER>"
    echo ""
    echo "Processes all files in sources/undigested/ for the given ticker."
    echo "Produces full/, structured/, digested/, updates wiki pages, manifest, and log."
    exit 1
}

[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
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

for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    # Skip already-extracted files
    [[ "$fname" == *_extracted.md ]] && continue
    [[ "$fname" == *_extracted.txt ]] && continue

    if [[ "$fname" == *_itr.zip ]] || [[ "$fname" == *_dfp.zip ]] || [[ "$fname" == *_itr.pdf ]] || [[ "$fname" == *_dfp.pdf ]]; then
        HEAVY_ITR_DFP+=("$f")
    elif [[ "$fname" == *_release_*.pdf ]]; then
        HEAVY_RELEASE+=("$f")
    elif [[ "$fname" == *_fato_relevante_*.pdf ]]; then
        LIGHT_FATOS+=("$f")
    else
        echo "WARN: Unknown file type, skipping: $fname"
    fi
done

echo "Found:"
echo "  ITR/DFP (heavy): ${#HEAVY_ITR_DFP[@]}"
echo "  Releases (heavy): ${#HEAVY_RELEASE[@]}"
echo "  Fatos relevantes (light): ${#LIGHT_FATOS[@]}"
echo ""

if [[ ${#HEAVY_ITR_DFP[@]} -eq 0 && ${#HEAVY_RELEASE[@]} -eq 0 && ${#LIGHT_FATOS[@]} -eq 0 ]]; then
    echo "Nothing to ingest. Exiting."
    exit 0
fi

# --- Pre-process all files ---
echo "=== Pre-processing PDFs ==="
EXTRACTED_ITR_DFP=()
EXTRACTED_RELEASE=()
EXTRACTED_FATOS=()

for f in "${HEAVY_ITR_DFP[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_ITR_DFP+=("$OUTPUT")
done

for f in "${HEAVY_RELEASE[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_RELEASE+=("$OUTPUT")
done

for f in "${LIGHT_FATOS[@]}"; do
    echo "  Extracting: $(basename "$f")"
    RESULT=$(python "$SCRIPT_DIR/lib/pdf_extract.py" "$f")
    OUTPUT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['output'])")
    EXTRACTED_FATOS+=("$OUTPUT")
done

echo ""

# --- Helper: build file list for prompt ---
build_file_list() {
    local arr=("$@")
    local list=""
    for f in "${arr[@]}"; do
        list+="- $f"$'\n'
    done
    echo "$list"
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

# --- Track produced digested files for wiki update ---
DIGESTED_FILES=()

# --- Step 3: Ingest heavy ITR/DFP ---
if [[ ${#EXTRACTED_ITR_DFP[@]} -gt 0 ]]; then
    echo "=== Ingesting ITR/DFP (heavy path) ==="
    FILE_LIST=$(build_file_list "${EXTRACTED_ITR_DFP[@]}")

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "itr/dfp" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FILE_LIST}}" "$FILE_LIST"

    # Collect digested files produced
    for f in "${EXTRACTED_ITR_DFP[@]}"; do
        fname=$(basename "$f")
        # Parse period from filename: TEND3_3T25_itr_extracted.md → 3T25
        period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
        tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
        digested="sources/digested/${EMPRESA}_${tipo}_${period}_summary.md"
        DIGESTED_FILES+=("$digested")

        # Update manifest
        python "$SCRIPT_DIR/lib/manifest_update.py" \
            --manifest "$MANIFEST_PATH" \
            --type "$tipo" --period "$period" \
            --full "sources/full/$EMPRESA/$period/${tipo}.md" \
            --structured "sources/structured/$EMPRESA/$period/${tipo}.json" \
            --digested "$digested" \
            --log "$REPO_ROOT/log.md"
    done
    echo ""
fi

# --- Step 4: Ingest heavy releases ---
if [[ ${#EXTRACTED_RELEASE[@]} -gt 0 ]]; then
    echo "=== Ingesting releases (heavy path) ==="
    FILE_LIST=$(build_file_list "${EXTRACTED_RELEASE[@]}")

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "release" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FILE_LIST}}" "$FILE_LIST"

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
    echo ""
fi

# --- Step 5: Ingest light fatos ---
if [[ ${#EXTRACTED_FATOS[@]} -gt 0 ]]; then
    echo "=== Ingesting fatos relevantes (light path) ==="
    FILE_LIST=$(build_file_list "${EXTRACTED_FATOS[@]}")

    invoke_claude "$SCRIPT_DIR/prompts/ingest_light.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{FILE_LIST}}" "$FILE_LIST"

    FATOS_DIGESTED="sources/digested/${EMPRESA}_fatos_relevantes_batch_summary.md"
    DIGESTED_FILES+=("$FATOS_DIGESTED")

    for f in "${EXTRACTED_FATOS[@]}"; do
        fname=$(basename "$f")
        period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')

        python "$SCRIPT_DIR/lib/manifest_update.py" \
            --manifest "$MANIFEST_PATH" \
            --type fato_relevante --period "$period" \
            --full "sources/full/$EMPRESA/$period/fato_relevante_${seq}.md" \
            --digested "$FATOS_DIGESTED" \
            --log "$REPO_ROOT/log.md"
    done
    echo ""
fi

# --- Step 6: Wiki update ---
echo "=== Updating wiki pages ==="
WIKI_PAGE="${EMPRESA}.md"
DIGESTED_LIST=$(build_file_list "${DIGESTED_FILES[@]}")

invoke_claude "$SCRIPT_DIR/prompts/ingest_wiki_update.md" \
    "{{TICKER}}" "$TICKER" \
    "{{EMPRESA}}" "$EMPRESA" \
    "{{WIKI_PAGE}}" "$WIKI_PAGE" \
    "{{DIGESTED_LIST}}" "$DIGESTED_LIST"

echo ""

# --- Step 7: Cleanup ---
echo "=== Cleanup ==="
for f in "${HEAVY_ITR_DFP[@]}" "${HEAVY_RELEASE[@]}" "${LIGHT_FATOS[@]}"; do
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done
for f in "${EXTRACTED_ITR_DFP[@]}" "${EXTRACTED_RELEASE[@]}" "${EXTRACTED_FATOS[@]}"; do
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done

echo ""
echo "=== Ingest complete ==="
echo "  Processed: $((${#HEAVY_ITR_DFP[@]} + ${#HEAVY_RELEASE[@]} + ${#LIGHT_FATOS[@]})) files"
echo "  Wiki updated: $WIKI_PAGE"
echo "  Manifest updated: $MANIFEST_PATH"
```

- [ ] **Step 2: Verify arg parsing**

```bash
bash tools/ingest.sh
```
Expected: Usage message.

```bash
bash tools/ingest.sh TEND3
```
Expected: "Found: ITR/DFP (heavy): 0, Releases (heavy): 0, Fatos relevantes (light): 0. Nothing to ingest."

- [ ] **Step 3: Commit**

```bash
git add tools/ingest.sh
git commit -m "feat: add ingest.sh — automated processing of undigested/ to wiki layers"
```

---

### Task 5: End-to-end verification

- [ ] **Step 1: Fetch fresh data for testing**

```bash
bash tools/fetch.sh TEND3 --horizon 6m --types itr
```

This should find any new ITR that wasn't already ingested. If nothing new is found (all already ingested), download one manually for testing:
```bash
python tools/lib/cvm_fetch.py download --num-sequencia 152793 --num-versao 1 --numero-protocolo 021148ITR300920250100152793-72 --desc-tipo ITR --output sources/undigested/TEND3_3T25_itr.zip
```

- [ ] **Step 2: Run full ingest**

```bash
bash tools/ingest.sh TEND3
```

Verify:
- Pre-processing extracts text from ZIP/PDF
- LLM produces full/, structured/, digested/
- Wiki page updated
- Manifest updated
- Log appended
- Undigested cleaned

- [ ] **Step 3: Commit results**

```bash
git add -A sources/ tenda.md log.md
git commit -m "test: end-to-end ingest verification"
```
