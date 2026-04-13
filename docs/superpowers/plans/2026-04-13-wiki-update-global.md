# Global Wiki Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Decouple wiki page generation from per-company ingest, creating a global wiki update command that reads all digesteds and produces/updates pages with cross-company intelligence.

**Architecture:** `wiki_update.sh` orchestrates two phases: (1) a planning LLM call that reads all digesteds and produces a JSON plan of pages to create/update, (2) sequential LLM calls that write each page with targeted context. Queue-based via `[wiki-queue]` entries in `log.md`.

**Tech Stack:** Bash, `claude --print`, existing `invoke_claude` pattern from ingest.sh

**Spec:** `docs/superpowers/specs/2026-04-13-wiki-update-global-design.md`

---

### Task 1: Create wiki_plan.md prompt

**Files:**
- Create: `tools/prompts/wiki_plan.md`

- [ ] **Step 1: Create the planning prompt**

```markdown
# Wiki Plan — System Prompt

You are a wiki planning agent for the equity-wiki. Your job is to analyze all available digested summaries and produce a JSON plan of wiki pages to create or update.

## Input

### Digesteds to process

{{DIGESTED_LIST}}

Read each digested file to understand what data is available:
```bash
cat "path/to/digested.md"
```

### Existing wiki pages

{{WIKI_PAGES}}

Check the content of existing pages to understand what needs updating:
```bash
cat "page_name.md"
```

### Companies with structured data

{{EMPRESAS_LIST}}

## Your task

Analyze ALL the digesteds and the current state of wiki pages. Produce a JSON plan that specifies:

1. **Which pages to CREATE** — entity pages for companies without one, concept pages for wikilink targets that don't exist, comparison pages when 2+ companies have overlapping data, subsidiary pages (e.g. riva.md, cashme.md, alea.md)
2. **Which pages to UPDATE** — pages whose data is stale vs the digesteds, pages missing a company that now has data
3. **Which pages to SKIP** — pages that are already current

For each page in create/update, list exactly which digested files contain relevant data for that page.

## Page types

- **entity** — one per company/subsidiary (cyrela.md, riva.md, cashme.md)
- **concept** — generic financial/sector concepts (mcmv.md, vso.md, banco_de_terrenos.md)
- **sector** — cross-company sector overview (incorporadoras.md)
- **comparison** — side-by-side analysis (cury_vs_direcional.md, cyrela_vs_cury.md)

## Output format

Produce the plan as JSON between these exact markers:

===WIKI_PLAN_START===
{
  "create": [
    {"page": "example.md", "type": "entity", "digesteds": ["empresa_dfp_2025_summary.md", "empresa_release_4T25_summary.md"]}
  ],
  "update": [
    {"page": "incorporadoras.md", "type": "sector", "digesteds": ["cury_dfp_2025_summary.md", "direcional_dfp_2025_summary.md"]}
  ],
  "skip": [
    {"page": "mcmv.md", "reason": "no new data affecting this concept"}
  ]
}
===WIKI_PLAN_END===

## Rules

- Every entity page should reference the most recent DFP + most recent release digesteds at minimum
- Sector page should reference the most recent DFP of ALL companies
- Comparison pages need data from BOTH companies being compared
- Concept pages only need updating if the digesteds contain new information about that concept
- For subsidiaries (Riva, CashMe, Alea), check if the parent company's digesteds mention them with enough detail to warrant a page
- Digested filenames follow the pattern: {empresa}_{tipo}_{periodo}_summary.md
- Only include digesteds in the list if they are actually relevant to that specific page
- Do NOT create pages for concepts that are too generic or don't have company-specific data to cite
```

- [ ] **Step 2: Commit**

```bash
git add tools/prompts/wiki_plan.md
git commit -m "feat: add wiki_plan.md prompt for global wiki update planning phase"
```

---

### Task 2: Create wiki_write.md prompt

**Files:**
- Create: `tools/prompts/wiki_write.md`

- [ ] **Step 1: Create the execution prompt**

```markdown
# Wiki Write — System Prompt

You are a wiki write agent for the equity-wiki. Your job is to create or update a single wiki page based on digested summaries.

## Context

- **Page:** {{PAGE_NAME}}
- **Action:** {{ACTION}} (create or update)
- **Page type:** {{PAGE_TYPE}} (entity, concept, sector, comparison)

## Source digesteds

{{DIGESTED_LIST}}

Read each digested to gather the data for this page:
```bash
cat "sources/digested/file.md"
```

## Existing page (if update)

{{EXISTING_CONTENT}}

## All wiki pages (for valid wikilinks)

{{ALL_PAGES}}

## What to produce

Write the complete page content to `{{PAGE_NAME}}` using bash:

```bash
cat > "{{PAGE_NAME}}" << 'PAGEEOF'
---
type: {{PAGE_TYPE}}
sources:
  - sources/digested/relevant_file.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Page Title

Content here...
PAGEEOF
```

### By page type

**entity** — Company overview with:
- Key financials table (receita, margens, lucro, ROE) from most recent periods
- Operational highlights (lançamentos, vendas, VSO, estoque, landbank)
- Capital structure (dívida, caixa, alavancagem)
- Key events and guidance
- Links to subsidiary pages if applicable

**concept** — Generic explanation (200-400 words) with:
- Definition and calculation methodology
- How different companies report/use it
- Company-specific examples with citations

**sector** — Cross-company overview with:
- Players table (all companies with key metrics side by side)
- Sector trends visible across the data
- Links to all entity pages

**comparison** — Side-by-side analysis with:
- Quarterly tables comparing the two companies
- Where they differ (strategy, margins, funding, segments)
- Relative strengths/weaknesses

## Citation format

- Numeric: `(fonte: structured/{empresa}/{periodo}/{tipo}.json :: canonical.dre.receita_liquida)`
- Qualitative: `(fonte: full/{empresa}/{periodo}/{tipo}.md §section_name)`
- Digested: `(fonte: digested/{name}_summary.md)`

## Wikilinks

- Use `[[page_name]]` for first mention of an entity/concept in each section
- Only link to pages listed in the ALL_PAGES section above, or pages you know are being created in this batch
- Use `[[page_name|display text]]` when display differs from page name

## Rules

- Every factual claim needs a `(fonte: ...)` citation
- Prefer Portuguese for content, snake_case filenames
- If updating, preserve existing content structure but refresh data and add new sections
- If creating, follow the page type template above
- Keep pages focused — one concept per page, one entity per page
- Numbers as reported in the digesteds
- Set `created` to today's date for new pages, keep original for updates
- Set `updated` to today's date always
```

- [ ] **Step 2: Commit**

```bash
git add tools/prompts/wiki_write.md
git commit -m "feat: add wiki_write.md prompt for wiki page creation/update"
```

---

### Task 3: Create wiki_update.sh orchestrator

**Files:**
- Create: `tools/wiki_update.sh`

- [ ] **Step 1: Create the orchestrator script**

```bash
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
    # Full mode: list everything in sources/digested/
    for f in "$REPO_ROOT"/sources/digested/*_summary.md; do
        [[ -f "$f" ]] || continue
        DIGESTED_LIST+="- $(basename "$f")"$'\n'
    done
else
    # Incremental mode: parse [wiki-queue] entries from log.md not yet consumed
    # Find the last [wiki-done] line number
    LAST_DONE=$(grep -n "\[wiki-done\]" "$REPO_ROOT/log.md" 2>/dev/null | tail -1 | cut -d: -f1)
    LAST_DONE=${LAST_DONE:-0}

    # Get all [wiki-queue] entries after that line
    QUEUE_ENTRIES=$(tail -n +$((LAST_DONE + 1)) "$REPO_ROOT/log.md" | grep "\[wiki-queue\]" || true)

    if [[ -z "$QUEUE_ENTRIES" ]]; then
        echo "No pending wiki-queue entries. Nothing to do."
        echo "Run with --full to rebuild all pages."
        exit 0
    fi

    # Extract unique digested paths
    while IFS= read -r line; do
        digested_path=$(echo "$line" | awk -F'|' '{print $NF}' | xargs)
        digested_name=$(basename "$digested_path")
        DIGESTED_LIST+="- $digested_name"$'\n'
    done <<< "$QUEUE_ENTRIES"

    # Deduplicate
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
    # Skip non-wiki files
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

# Extract JSON plan
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

# Parse plan counts
CREATE_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('create',[])))")
UPDATE_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('update',[])))")
SKIP_COUNT=$(echo "$PLAN_JSON" | python -c "import sys,json; print(len(json.load(sys.stdin).get('skip',[])))")

echo ""
echo "Plan: create=$CREATE_COUNT, update=$UPDATE_COUNT, skip=$SKIP_COUNT"
echo ""

# --- Phase 2: Execution ---
echo "=== Phase 2: Execution ==="

# Get all current wiki pages for wikilink validation
ALL_PAGES=$(ls "$REPO_ROOT"/*.md 2>/dev/null | xargs -I{} basename {} | grep -v CLAUDE | grep -v README | grep -v SCHEMA | grep -v log | tr '\n' ', ')

# Process pages in order: entity → concept → sector → comparison
for PAGE_TYPE in entity concept sector comparison; do
    # Process creates for this type
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

        # Build digested list for this page
        PAGE_DIGESTEDS=""
        IFS=',' read -ra DIGS <<< "$DIGESTEDS_CSV"
        for d in "${DIGS[@]}"; do
            PAGE_DIGESTEDS+="- sources/digested/$d"$'\n'
        done

        # Get existing content if update
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

        # Add to ALL_PAGES for subsequent wikilink validation
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
```

- [ ] **Step 2: Commit**

```bash
git add tools/wiki_update.sh
git commit -m "feat: add wiki_update.sh — global two-phase wiki update orchestrator"
```

---

### Task 4: Create ingest_generic.md prompt

**Files:**
- Create: `tools/prompts/ingest_generic.md`

- [ ] **Step 1: Create the generic ingest prompt**

```markdown
# Ingest Generic — System Prompt

You are an ingest agent for the equity-wiki. Your job is to process a generic source file (not from CVM — could be a sector spreadsheet, research report, macro analysis, etc.) and produce a digested summary.

## Source file

The full transcription has been placed at:

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

## What to produce

### `sources/digested/{{DIGESTED_NAME}}_summary.md`

A wiki-facing summary (under 600 words) that:

1. Identifies what the source is (sector comparison, macro analysis, company deep-dive, etc.)
2. Extracts the key data points, rankings, and conclusions
3. Notes which companies/tickers are mentioned (so the wiki update can route data to the right pages)
4. Highlights cross-company comparisons or sector-level insights

## Rules

- Read the full source completely before producing output
- Create directories via `mkdir -p` as needed
- Do NOT produce structured/ files — generic sources don't follow the canonical schema
- Do NOT edit wiki pages, manifests, or log — the orchestrator handles those
- The digested filename should be descriptive of the content, not the source filename
- Use Portuguese for the summary content
```

- [ ] **Step 2: Commit**

```bash
git add tools/prompts/ingest_generic.md
git commit -m "feat: add ingest_generic.md prompt for non-CVM source ingestion"
```

---

### Task 5: Modify ingest.sh — remove wiki step, add queue entries

**Files:**
- Modify: `tools/ingest.sh`

- [ ] **Step 1: Replace the wiki update step (lines 399-413) with queue append logic**

Remove:
```bash
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
```

Replace with:
```bash
# --- Step 6: Append to wiki queue ---
echo "=== Appending to wiki queue ==="
TODAY=$(date +%Y-%m-%d)
for digested in "${DIGESTED_FILES[@]}"; do
    # Extract tipo and period from digested filename: {empresa}_{tipo}_{periodo}_summary.md
    dname=$(basename "$digested" _summary.md)
    # Remove empresa prefix
    suffix="${dname#${EMPRESA}_}"
    # Split into tipo and period (last segment is period, rest is tipo)
    tipo=$(echo "$suffix" | rev | cut -d_ -f2- | rev)
    period=$(echo "$suffix" | rev | cut -d_ -f1 | rev)
    echo "[wiki-queue] $TODAY | $EMPRESA | $tipo | $period | $digested" >> "$REPO_ROOT/log.md"
    echo "  Queued: $digested"
done
echo ""
```

- [ ] **Step 2: Update the final summary message (lines 428-431)**

Replace:
```bash
echo "=== Ingest complete ==="
echo "  Processed: $TOTAL files"
echo "  Wiki updated: $WIKI_PAGE"
echo "  Manifest updated: $MANIFEST_PATH"
```

With:
```bash
echo "=== Ingest complete ==="
echo "  Processed: $TOTAL files"
echo "  Wiki queue: ${#DIGESTED_FILES[@]} entries added to log.md"
echo "  Manifest updated: $MANIFEST_PATH"
echo ""
echo "Run 'bash tools/wiki_update.sh' to update wiki pages."
```

- [ ] **Step 3: Add --generic flag handling at the top of ingest.sh**

After the existing argument parsing (line 26), add generic mode support. Insert after `done` of the while loop:

```bash
# --- Generic mode ---
if [[ "$TICKER" == "--generic" ]] || [[ "${GENERIC_MODE:-false}" == "true" ]]; then
    GENERIC_FILE="${1:-}"
    [[ -z "$GENERIC_FILE" ]] && { echo "Usage: bash tools/ingest.sh --generic <file>"; exit 1; }
    [[ ! -f "$GENERIC_FILE" ]] && { echo "ERROR: File not found: $GENERIC_FILE"; exit 1; }

    echo "=== Generic Ingest ==="
    echo "File: $GENERIC_FILE"
    echo ""

    # Extract
    FNAME=$(basename "$GENERIC_FILE")
    STEM="${FNAME%.*}"
    echo "Extracting..."
    python "$SCRIPT_DIR/lib/pdf_extract.py" "$GENERIC_FILE" 2>/dev/null || true
    EXTRACTED="${GENERIC_FILE%.*}_extracted.md"
    [[ ! -f "$EXTRACTED" ]] && EXTRACTED="$GENERIC_FILE"

    # Copy to full/generic/
    mkdir -p "$REPO_ROOT/sources/full/generic"
    cp "$EXTRACTED" "$REPO_ROOT/sources/full/generic/${STEM}.md"
    echo "  Copied → sources/full/generic/${STEM}.md"

    # Generate digested
    DIGESTED_NAME="${STEM}"
    FULL_PATH="$REPO_ROOT/sources/full/generic/${STEM}.md"

    invoke_claude "$SCRIPT_DIR/prompts/ingest_generic.md" \
        "{{FULL_PATH}}" "$FULL_PATH" \
        "{{DIGESTED_NAME}}" "$DIGESTED_NAME"

    # Find the produced digested (the LLM chooses the exact name)
    PRODUCED_DIGESTED=$(ls -t "$REPO_ROOT"/sources/digested/*_summary.md 2>/dev/null | head -1)
    if [[ -n "$PRODUCED_DIGESTED" ]]; then
        DNAME=$(basename "$PRODUCED_DIGESTED")
        TODAY=$(date +%Y-%m-%d)
        echo "[wiki-queue] $TODAY | generic | other | ${STEM} | sources/digested/$DNAME" >> "$REPO_ROOT/log.md"
        echo "  Queued: $DNAME"
    fi

    # Cleanup extracted (but keep the original if user wants it)
    [[ -f "$EXTRACTED" ]] && [[ "$EXTRACTED" != "$GENERIC_FILE" ]] && rm -f "$EXTRACTED"

    echo ""
    echo "=== Generic ingest complete ==="
    echo "  Full: sources/full/generic/${STEM}.md"
    echo "  Run 'bash tools/wiki_update.sh' to update wiki pages."
    exit 0
fi
```

This needs to go right after argument parsing but before the manifest resolution. The cleanest insertion point is after line 26 (end of while loop for args). But we also need to handle the case where `$TICKER` is `--generic`. Let me be more precise:

Replace the existing first-argument handling. Currently line 17 is `TICKER="$1"; shift`. We need to intercept `--generic` before that. Replace lines 17-26:

Current:
```bash
TICKER="$1"; shift

CONCURRENCY=4
while [[ $# -gt 0 ]]; do
    case "$1" in
        --concurrency|-j) CONCURRENCY="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done
```

New:
```bash
# Check for --generic mode
if [[ "$1" == "--generic" ]]; then
    shift
    GENERIC_FILE="${1:-}"
    [[ -z "$GENERIC_FILE" ]] && { echo "Usage: bash tools/ingest.sh --generic <file>"; exit 1; }
    [[ ! -f "$GENERIC_FILE" ]] && { echo "ERROR: File not found: $GENERIC_FILE"; exit 1; }

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

    echo "=== Generic Ingest ==="
    echo "File: $GENERIC_FILE"
    echo ""

    # Source invoke_claude helper
    invoke_claude() {
        local template="$1"
        local prompt_file
        prompt_file=$(mktemp "${TMPDIR:-/tmp}/ingest_prompt_XXXXXX.md")
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

    # Extract
    FNAME=$(basename "$GENERIC_FILE")
    STEM="${FNAME%.*}"
    echo "Extracting..."
    python "$SCRIPT_DIR/lib/pdf_extract.py" "$GENERIC_FILE" 2>/dev/null || true
    EXTRACTED="${GENERIC_FILE%.*}_extracted.md"
    [[ ! -f "$EXTRACTED" ]] && EXTRACTED="$GENERIC_FILE"

    # Copy to full/generic/
    mkdir -p "$REPO_ROOT/sources/full/generic"
    cp "$EXTRACTED" "$REPO_ROOT/sources/full/generic/${STEM}.md"
    echo "  Copied → sources/full/generic/${STEM}.md"

    # Generate digested
    FULL_PATH="$REPO_ROOT/sources/full/generic/${STEM}.md"
    invoke_claude "$SCRIPT_DIR/prompts/ingest_generic.md" \
        "{{FULL_PATH}}" "$FULL_PATH" \
        "{{DIGESTED_NAME}}" "$STEM"

    # Find the produced digested
    PRODUCED_DIGESTED=$(ls -t "$REPO_ROOT"/sources/digested/*_summary.md 2>/dev/null | head -1)
    if [[ -n "$PRODUCED_DIGESTED" ]]; then
        DNAME=$(basename "$PRODUCED_DIGESTED")
        TODAY=$(date +%Y-%m-%d)
        echo "[wiki-queue] $TODAY | generic | other | ${STEM} | sources/digested/$DNAME" >> "$REPO_ROOT/log.md"
        echo "  Queued: $DNAME"
    fi

    # Cleanup
    [[ -f "$EXTRACTED" ]] && [[ "$EXTRACTED" != "$GENERIC_FILE" ]] && rm -f "$EXTRACTED"

    echo ""
    echo "=== Generic ingest complete ==="
    echo "  Full: sources/full/generic/${STEM}.md"
    echo "  Run 'bash tools/wiki_update.sh' to update wiki pages."
    exit 0
fi

TICKER="$1"; shift

CONCURRENCY=4
while [[ $# -gt 0 ]]; do
    case "$1" in
        --concurrency|-j) CONCURRENCY="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done
```

- [ ] **Step 4: Commit**

```bash
git add tools/ingest.sh
git commit -m "fix(ingest): remove wiki update step, add queue + generic mode"
```

---

### Task 6: Delete ingest_wiki_update.md and update README.md

**Files:**
- Delete: `tools/prompts/ingest_wiki_update.md`
- Modify: `README.md`

- [ ] **Step 1: Delete the old prompt**

```bash
git rm tools/prompts/ingest_wiki_update.md
```

- [ ] **Step 2: Update README.md — add Tools section after "Operações"**

Add a new section before "Anatomia de uma página da wiki" (around line 117). Insert:

```markdown
## Ferramentas (CLI)

### Fetch — baixar documentos da CVM

```bash
bash tools/fetch.sh TEND3                          # modo normal
bash tools/fetch.sh TEND3 --horizon 5y --types dfp,itr,release
bash tools/fetch.sh TEND3 --discover               # modo discovery (cria fetch_profile)
```

Requer CVM-API rodando em `localhost:8100`.

### Ingest — processar documentos

```bash
bash tools/ingest.sh TEND3                         # processa tudo em sources/undigested/ para o ticker
bash tools/ingest.sh TEND3 --concurrency 4         # controlar paralelismo
bash tools/ingest.sh --generic planilha_setor.xlsx # ingerir fonte avulsa (sem ticker)
```

O ingest produz `full/` + `structured/` + `digested/` e registra na fila do wiki update.

### Wiki Update — atualizar páginas da wiki

```bash
bash tools/wiki_update.sh --full    # primeira rodada: lê TODOS os digesteds, recria tudo
bash tools/wiki_update.sh           # incremental: processa apenas a fila pendente no log.md
```

Duas fases:
1. **Planejamento** — LLM lê todos os digesteds e produz um plano JSON (quais páginas criar/atualizar)
2. **Execução** — LLM escreve cada página com contexto cirúrgico (só os digesteds relevantes)

### Re-ingest full/ — corrigir transcrições truncadas

```bash
bash tools/reingest_full.sh CURY3 --horizon 3y    # re-baixa PDFs e copia direto para full/
```

Não invoca o LLM. Usado para corrigir fulls que foram truncados pelo pipeline antigo.

### Fila do wiki update (log.md)

O `ingest.sh` appenda entries parseáveis no `log.md`:

```
[wiki-queue] 2026-04-12 | cury | itr | 3T25 | sources/digested/cury_itr_3T25_summary.md
[wiki-queue] 2026-04-12 | generic | sector | planilha | sources/digested/planilha_setor_summary.md
```

O `wiki_update.sh` consome a fila e marca com `[wiki-done]`.
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: delete old wiki update prompt, update README with CLI tools section"
```

---

### Task 7: Run `wiki_update.sh --full` for first global update

**Files:** None (execution only)

- [ ] **Step 1: Run the global wiki update**

```bash
bash tools/wiki_update.sh --full
```

This will:
1. Read all ~100 digesteds
2. Produce a plan (should create cyrela.md, cashme.md, update incorporadoras.md, etc.)
3. Execute page by page

- [ ] **Step 2: Verify results**

```bash
# Check that cyrela.md was created
cat cyrela.md | head -20

# Check that incorporadoras.md was updated
grep "cyrela" incorporadoras.md

# Check all pages have valid frontmatter
for f in *.md; do grep -q "^type:" "$f" && echo "OK: $f" || echo "NO FRONTMATTER: $f"; done
```

- [ ] **Step 3: Commit the generated wiki pages**

```bash
git add *.md
git commit -m "wiki: global update — all pages refreshed from 100+ digesteds"
```

- [ ] **Step 4: Push**

```bash
git push
```
