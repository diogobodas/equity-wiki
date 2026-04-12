# Design: full/ bypass LLM — extracted.md = full.md

**Date:** 2026-04-12
**Status:** Approved
**Problem:** The `claude --print` ingest agent truncates/summarizes notas explicativas when producing `full/` files. ITR/DFP documents with 100+ pages of notes get condensed to 1-2 lines. This violates the SCHEMA.md contract that full/ is "structured-but-uncut".

## Root cause

The extracted.md (from pdf_extract.py) contains the complete document (~150KB). But `claude --print` cannot produce 100KB+ of reorganized output — it prioritizes numeric DFs and summarizes the qualitative notes to fit its output budget.

## Evidence

| Company | DFP 2025 full/ size | Notes preserved? |
|---------|-------------------|------------------|
| Tenda | 64KB / 1009 lines | Yes (exception) |
| Cyrela | 30KB / 488 lines | Partial |
| Direcional | 24KB / 481 lines | No — "Notas 1-26, 55 páginas" in 1 paragraph |
| Cury | 11KB / 224 lines | No — "Notas 4-26" in 1 line |

## Solution: Approach C — extracted = full, LLM only for structured + digested

### Pipeline change

**Before:**
```
PDF → pdf_extract.py → extracted.md → claude --print → full.md + structured.json + digested.md
```

**After:**
```
PDF → pdf_extract.py → extracted.md
                           ├→ ingest.sh copies directly → full.md (100% preserved)
                           └→ claude --print reads full → structured.json + digested.md
```

### File changes

#### 1. `tools/ingest.sh`

After `pdf_extract.py` runs, add a copy step before invoking `claude --print`:

```bash
# Copy extracted.md → full/{empresa}/{periodo}/{tipo}.md
full_dir="$REPO_ROOT/sources/full/$EMPRESA/$period"
mkdir -p "$full_dir"
cp "$extracted_file" "$full_dir/${tipo}.md"
```

Period and tipo are already extracted from filename via existing regex.

Pass the **full/ path** (not extracted path) to the claude agent.

The same copy-direct logic applies to light ingest files (fato_relevante, prévia_operacional). `ingest.sh` copies extracted → full/ before invoking the light agent.

No size-based validation — the extracted.md may include PDF artifacts (page markers, extra whitespace) that inflate size compared to a hand-cleaned full. With the copy-direct approach, content preservation is guaranteed by construction.

#### 2. `tools/prompts/ingest_heavy.md`

Remove section 1 (producing full.md). Keep sections 2 (structured.json) and 3 (digested.md).

Change instruction from "read extracted file and produce full + structured + digested" to:
- "The full/ file has already been created at the path below. Read it and produce only the structured.json and digested.md."
- Replace `{{FILE_LIST}}` with `{{FULL_PATH}}` pointing to the already-created full.md

#### 3. `tools/prompts/ingest_light.md`

Same change: remove full.md production. The light agent reads the already-created full/ and produces only the digested.md.

#### 4. `tools/lib/pdf_extract.py`

No changes. Works correctly.

#### 5. New: `tools/reingest_full.sh`

Lightweight script for re-generating truncated fulls without re-running LLM:

```bash
# Usage: bash tools/reingest_full.sh <TICKER>
# 1. fetch.sh downloads PDFs/ZIPs to undigested/
# 2. pdf_extract.py extracts → extracted.md
# 3. Copies extracted.md → full/{empresa}/{periodo}/{tipo}.md (overwrites)
# Does NOT re-run claude --print (structured.json and digested.md are kept as-is)
```

### Filename → path mapping

Already handled by existing regex in ingest.sh:

| Filename pattern | full/ path |
|-----------------|------------|
| `CYRE3_1T25_itr_126293.zip` | `sources/full/cyrela/1T25/itr.md` |
| `DIRR3_2025_dfp_147000.zip` | `sources/full/direcional/2025/dfp.md` |
| `CYRE3_3T25_release_969512.pdf` | `sources/full/cyrela/3T25/release.md` |
| `TEND3_1T26_previa_operacional_849975.pdf` | `sources/full/tenda/1T26/previa_operacional.md` |

### Re-ingest scope

Truncated fulls that need re-generation:

- **Cury:** All ITRs (1T23–3T25), all DFPs (2022–2025) — 14 files
- **Direcional:** All ITRs (1T24–3T25), all DFPs (2024–2025) — 8 files
- **Cyrela:** Partial — needs audit per-file to check which are truncated

**Tenda fulls appear complete and should NOT be re-ingested.**

### ACTION REQUIRED: Re-run full/ for 3 companies

After implementing the pipeline change, re-generate all full/ files for:
- **Cury** — all ITRs + DFPs + fatos relevantes
- **Direcional** — all ITRs + DFPs + fatos relevantes
- **Cyrela** — all ITRs + DFPs + fatos relevantes + prévias

Use `tools/reingest_full.sh` for each ticker. This does NOT require re-running the LLM — only fetch → extract → copy.

### All document types affected

The truncation risk applies to all document types, not just ITR/DFP. Verified by inspecting full/ files where notas explicativas, sections, or detail paragraphs are condensed into single-line summaries — content that exists in the extracted.md but is absent from the full/.

**The copy-direct approach applies to ALL document types** — heavy (ITR, DFP, release) AND light (fato relevante, prévia operacional). The LLM produces only structured.json (heavy) or digested.md (both).

### Out of scope

- No changes to structured.json or digested.md generation
- No changes to wiki page update step
- No changes to manifest update
