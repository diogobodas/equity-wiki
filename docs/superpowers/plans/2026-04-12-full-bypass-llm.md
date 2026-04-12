# full/ bypass LLM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop passing full/ file creation through the LLM. Copy extracted.md directly to full/, and have the LLM only produce structured.json + digested.md.

**Architecture:** `ingest.sh` gains a copy step between pdf_extract and claude invocation. Prompts lose their full/ production instructions. New `reingest_full.sh` script handles re-generating truncated fulls for existing companies.

**Tech Stack:** Bash, existing tools (pdf_extract.py, cvm_fetch.py)

**Spec:** `docs/superpowers/specs/2026-04-12-full-bypass-llm-design.md`

---

### Task 1: Add copy-to-full helper function in ingest.sh

**Files:**
- Modify: `tools/ingest.sh`

This task adds a helper function that copies an extracted.md to the correct `sources/full/` path, and a step between PDF extraction and LLM invocation that calls it for every file type.

- [ ] **Step 1: Add `copy_to_full` helper function after the `build_file_list` function (after line 163)**

Add this function at line 164 of `tools/ingest.sh`, right after the closing `}` of `build_file_list`:

```bash
# --- Helper: copy extracted file to full/ ---
copy_to_full() {
    local extracted_file="$1"
    local empresa="$2"
    local period="$3"
    local tipo="$4"  # itr, dfp, release, fato_relevante_NNN, previa_operacional, etc.

    local full_dir="$REPO_ROOT/sources/full/$empresa/$period"
    mkdir -p "$full_dir"
    cp "$extracted_file" "$full_dir/${tipo}.md"
    echo "  Copied → sources/full/$empresa/$period/${tipo}.md"
}
```

- [ ] **Step 2: Add copy step for HEAVY ITR/DFP files — insert a new section between "Pre-processing PDFs" (line ~128) and "Parallel ingest" (line ~233)**

After the `parallel_wait` that finishes PDF extraction and before `# --- Track produced digested files`, insert:

```bash
# --- Step 2b: Copy extracted files to full/ ---
echo "=== Copying extracted files to full/ ==="

for f in "${EXTRACTED_ITR_DFP[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
    copy_to_full "$f" "$EMPRESA" "$period" "$tipo"
done

for f in "${EXTRACTED_RELEASE[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    copy_to_full "$f" "$EMPRESA" "$period" "release"
done

for f in "${EXTRACTED_FATOS[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    # Fatos: extract seq number for filename
    if [[ "$fname" == *_fato_relevante_* ]]; then
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
        copy_to_full "$f" "$EMPRESA" "$period" "fato_relevante_${seq}"
    elif [[ "$fname" == *_previa_operacional_* ]]; then
        copy_to_full "$f" "$EMPRESA" "$period" "previa_operacional"
    else
        copy_to_full "$f" "$EMPRESA" "$period" "fato_relevante"
    fi
done

for f in "${EXTRACTED_OTHER[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    stem="${fname%_extracted.*}"
    stem="${stem%.*}"
    copy_to_full "$f" "$EMPRESA" "$period" "$stem"
done

echo ""
```

- [ ] **Step 3: Update `ingest_one_heavy` to pass full path instead of extracted path**

Replace the current `ingest_one_heavy` function (lines 195-210) with:

```bash
# --- Helper: ingest one file (heavy path) ---
ingest_one_heavy() {
    local full_path="$1"
    local doc_type="$2"
    local log_prefix="[heavy:$(basename "$full_path")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "$doc_type" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FULL_PATH}}" "$full_path"

    echo "$log_prefix Done."
}
```

- [ ] **Step 4: Update `ingest_one_light` to pass full path instead of extracted path**

Replace the current `ingest_one_light` function (lines 213-225) with:

```bash
# --- Helper: ingest one file (light path) ---
ingest_one_light() {
    local full_path="$1"
    local log_prefix="[light:$(basename "$full_path")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_light.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{FULL_PATH}}" "$full_path"

    echo "$log_prefix Done."
}
```

- [ ] **Step 5: Update parallel ingest section to pass full/ paths instead of extracted paths**

Replace the parallel ingest loop (lines 233-258) with:

```bash
# --- Step 3: Parallel ingest (LLM produces structured + digested only) ---
echo "=== Parallel ingest (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"

# Heavy: ITR/DFP
for f in "${EXTRACTED_ITR_DFP[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
    full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/${tipo}.md"
    parallel_add "ingest_one_heavy \"$full_path\" \"itr/dfp\""
done

# Heavy: releases
for f in "${EXTRACTED_RELEASE[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/release.md"
    parallel_add "ingest_one_heavy \"$full_path\" \"release\""
done

# Heavy: other
for f in "${EXTRACTED_OTHER[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    stem="${fname%_extracted.*}"
    stem="${stem%.*}"
    full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/${stem}.md"
    parallel_add "ingest_one_heavy \"$full_path\" \"other\""
done

# Light: fatos relevantes / prévias
for f in "${EXTRACTED_FATOS[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    if [[ "$fname" == *_fato_relevante_* ]]; then
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
        full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/fato_relevante_${seq}.md"
    elif [[ "$fname" == *_previa_operacional_* ]]; then
        full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/previa_operacional.md"
    else
        full_path="$REPO_ROOT/sources/full/$EMPRESA/$period/fato_relevante.md"
    fi
    parallel_add "ingest_one_light \"$full_path\""
done

parallel_wait
echo "=== All ingest agents complete ==="
echo ""
```

- [ ] **Step 6: Also export `copy_to_full`**

Update the export line (currently line 227) to:

```bash
export -f ingest_one_heavy ingest_one_light invoke_claude copy_to_full
export TICKER EMPRESA SCHEMA_PATH SCRIPT_DIR REPO_ROOT
```

(Note: `REPO_ROOT` is also exported since `copy_to_full` uses it.)

- [ ] **Step 7: Commit**

```bash
git add tools/ingest.sh
git commit -m "fix(ingest): copy extracted.md directly to full/ instead of LLM"
```

---

### Task 2: Update ingest_heavy.md prompt

**Files:**
- Modify: `tools/prompts/ingest_heavy.md`

Remove the full.md production section. The agent now reads an already-created full/ file and only produces structured.json + digested.md.

- [ ] **Step 1: Replace the entire contents of `tools/prompts/ingest_heavy.md`**

```markdown
# Ingest Heavy — System Prompt

You are an ingest agent for the equity-wiki. Your job is to read a full/ transcription and produce structured JSON and a digested summary.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}
- **Document type:** {{DOC_TYPE}}
- **Schema path:** {{SCHEMA_PATH}}

## Source file

The full transcription has already been created at:

{{FULL_PATH}}

Read it via bash:
```bash
cat "{{FULL_PATH}}"
```

For large files, read in sections:
```bash
head -500 "{{FULL_PATH}}"
tail -n +500 "{{FULL_PATH}}" | head -500
```

## Schema

Read the canonical schema for reference:
```bash
cat {{SCHEMA_PATH}}
```

## What to produce

### 1. `sources/structured/{{EMPRESA}}/{periodo}/{tipo}.json`

Canonical JSON following the incorporadora schema. Use CONSOLIDATED figures.

```json
{
  "_schema": "incorporadora/v1",
  "_schema_path": "{{SCHEMA_PATH}}",
  "_empresa": "{{EMPRESA}}",
  "_periodo": "{periodo}",
  "_source": "{{FULL_PATH}}",
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

### 2. `sources/digested/{empresa}_{tipo}_{periodo}_summary.md`

Wiki-facing TL;DR, under 400 words. Key financials, trends, notable items.

## Rules

- Read the full/ file completely before producing output
- Use CONSOLIDATED figures, not individual
- Numbers as reported, converted to R$ mm
- Create directories via `mkdir -p` as needed
- Do NOT produce full/ files — they already exist
- Do NOT edit manifest, wiki pages, log, or index — the script handles those
```

- [ ] **Step 2: Commit**

```bash
git add tools/prompts/ingest_heavy.md
git commit -m "fix(prompt): ingest_heavy reads existing full/, produces only structured + digested"
```

---

### Task 3: Update ingest_light.md prompt

**Files:**
- Modify: `tools/prompts/ingest_light.md`

Remove full.md production. The light agent reads the already-created full/ and produces only the digested.md.

- [ ] **Step 1: Replace the entire contents of `tools/prompts/ingest_light.md`**

```markdown
# Ingest Light — System Prompt

You are an ingest agent for the equity-wiki. Your job is to read a full/ transcription of a fato relevante or prévia operacional and produce a digested summary.

## Context

- **Ticker:** {{TICKER}}
- **Empresa:** {{EMPRESA}}

## Source file

The full transcription has already been created at:

{{FULL_PATH}}

Read it via bash:
```bash
cat "{{FULL_PATH}}"
```

## What to produce

### ONE combined digested file per batch:

**`sources/digested/{{EMPRESA}}_fatos_relevantes_batch_summary.md`**
- For each fato: date, seq number, one-line summary
- Group by period
- Under 400 words total

## Rules

- Read the full/ file completely before producing output
- Do NOT produce full/ files — they already exist
- Do NOT create structured/ files
- Do NOT edit manifest, wiki pages, log, or index
- Identify what each fato is about: dividendos, debêntures, recompra, guidance, cessão, governança, etc.
```

- [ ] **Step 2: Commit**

```bash
git add tools/prompts/ingest_light.md
git commit -m "fix(prompt): ingest_light reads existing full/, produces only digested"
```

---

### Task 4: Create reingest_full.sh

**Files:**
- Create: `tools/reingest_full.sh`

Lightweight script that re-downloads PDFs via fetch, extracts them, and copies to full/ — without invoking the LLM. For fixing the truncated fulls of Cury, Direcional, and Cyrela.

- [ ] **Step 1: Create `tools/reingest_full.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Usage ---
usage() {
    echo "Usage: bash tools/reingest_full.sh <TICKER> [--horizon 5y] [--types dfp,itr,release,fato_relevante,previa_operacional]"
    echo ""
    echo "Re-generates full/ files by re-downloading PDFs, extracting, and copying."
    echo "Does NOT re-run the LLM (structured.json and digested.md are kept as-is)."
    echo ""
    echo "Requires CVM-API running at localhost:8100."
    exit 1
}

[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

HORIZON="5y"
TYPES="dfp,itr,release,fato_relevante,previa_operacional"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --horizon)  HORIZON="$2"; shift 2 ;;
        --types)    TYPES="$2"; shift 2 ;;
        *)          echo "Unknown arg: $1"; usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFESTS="$REPO_ROOT/sources/manifests"
UNDIGESTED="$REPO_ROOT/sources/undigested"

echo "=== Re-ingest Full ==="
echo "Ticker:  $TICKER"
echo "Horizon: $HORIZON"
echo "Types:   $TYPES"
echo ""

# --- Resolve manifest ---
EMPRESA=""
for f in "$MANIFESTS"/*.json; do
    [[ -f "$f" ]] || continue
    if grep -q "\"$TICKER\"" "$f" 2>/dev/null; then
        EMPRESA=$(basename "$f" .json)
        break
    fi
done

if [[ -z "$EMPRESA" ]]; then
    echo "ERROR: No manifest found for $TICKER."
    exit 1
fi

echo "Empresa: $EMPRESA"
echo ""

# --- Step 1: Fetch (downloads to undigested/) ---
echo "=== Step 1: Fetching from CVM ==="
bash "$SCRIPT_DIR/fetch.sh" "$TICKER" --horizon "$HORIZON" --types "$TYPES"
echo ""

# --- Step 2: Extract all PDFs/ZIPs ---
echo "=== Step 2: Extracting PDFs ==="
COUNT=0
for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")
    [[ "$fname" == *_extracted.md ]] && continue
    [[ "$fname" == *.json ]] && continue

    echo "  Extracting: $fname"
    python "$SCRIPT_DIR/lib/pdf_extract.py" "$f" 2>/dev/null || echo "    WARNING: extraction failed for $fname"
    COUNT=$((COUNT + 1))
done
echo "  Extracted $COUNT files"
echo ""

# --- Step 3: Copy to full/ ---
echo "=== Step 3: Copying to full/ ==="
COPIED=0
for f in "$UNDIGESTED"/${TICKER}_*_extracted.md; do
    [[ -f "$f" ]] || continue
    fname=$(basename "$f")

    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    full_dir="$REPO_ROOT/sources/full/$EMPRESA/$period"
    mkdir -p "$full_dir"

    if [[ "$fname" == *_itr_* ]]; then
        dest="$full_dir/itr.md"
    elif [[ "$fname" == *_dfp_* ]]; then
        dest="$full_dir/dfp.md"
    elif [[ "$fname" == *_release_* ]]; then
        dest="$full_dir/release.md"
    elif [[ "$fname" == *_fato_relevante_* ]]; then
        seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
        dest="$full_dir/fato_relevante_${seq}.md"
    elif [[ "$fname" == *_previa_operacional_* ]]; then
        dest="$full_dir/previa_operacional.md"
    else
        stem="${fname%_extracted.*}"
        dest="$full_dir/${stem}.md"
    fi

    cp "$f" "$dest"
    echo "  $fname → $dest"
    COPIED=$((COPIED + 1))
done
echo "  Copied $COPIED files to full/"
echo ""

# --- Step 4: Cleanup undigested/ ---
echo "=== Step 4: Cleanup ==="
for f in "$UNDIGESTED"/${TICKER}_*; do
    [[ -f "$f" ]] || continue
    rm -f "$f"
    echo "  Deleted: $(basename "$f")"
done

echo ""
echo "=== Re-ingest complete ==="
echo "  Files updated in full/: $COPIED"
echo "  structured.json and digested.md were NOT changed."
echo ""
echo "ACTION REQUIRED after re-ingest for all tickers:"
echo "  - Cury:       bash tools/reingest_full.sh CURY3 --horizon 5y"
echo "  - Direcional: bash tools/reingest_full.sh DIRR3 --horizon 5y"
echo "  - Cyrela:     bash tools/reingest_full.sh CYRE3 --horizon 5y"
```

- [ ] **Step 2: Make executable**

```bash
chmod +x tools/reingest_full.sh
```

- [ ] **Step 3: Commit**

```bash
git add tools/reingest_full.sh
git commit -m "feat: add reingest_full.sh for re-generating truncated full/ files"
```

---

### Task 5: Verify the changes work end-to-end with a dry run

**Files:** None (read-only verification)

Verify the modified ingest.sh logic by tracing through a known filename.

- [ ] **Step 1: Trace ITR filename through the new logic**

Manually verify the regex parsing for a known file:

```bash
# Test: CYRE3_1T25_itr_126293_extracted.md
fname="CYRE3_1T25_itr_126293_extracted.md"
period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
echo "period=$period tipo=$tipo"
# Expected: period=1T25 tipo=itr
```

- [ ] **Step 2: Trace DFP filename**

```bash
fname="DIRR3_2025_dfp_147000_extracted.md"
period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
echo "period=$period tipo=$tipo"
# Expected: period=2025 tipo=dfp
```

- [ ] **Step 3: Trace release filename**

```bash
fname="CYRE3_3T25_release_969512_extracted.md"
period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
echo "period=$period"
# Expected: period=3T25
```

- [ ] **Step 4: Trace fato_relevante filename**

```bash
fname="CYRE3_4T25_fato_relevante_983472_extracted.md"
period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
echo "period=$period seq=$seq"
# Expected: period=4T25 seq=983472
```

- [ ] **Step 5: Trace previa_operacional filename**

```bash
fname="TEND3_1T26_previa_operacional_849975_extracted.md"
period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
echo "period=$period"
# Expected: period=1T26
```

- [ ] **Step 6: Commit plan as done**

```bash
git add docs/superpowers/plans/2026-04-12-full-bypass-llm.md
git commit -m "docs: add implementation plan for full/ bypass LLM"
```

---

### Post-implementation: Re-run full/ for 3 companies

After all tasks above are complete and committed, run `reingest_full.sh` for each affected company:

```bash
# Requires CVM-API running at localhost:8100
bash tools/reingest_full.sh CURY3 --horizon 5y
bash tools/reingest_full.sh DIRR3 --horizon 5y
bash tools/reingest_full.sh CYRE3 --horizon 5y
```

**Do NOT re-run for Tenda** — its fulls are already complete.
