# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## What this is

An LLM-maintained knowledge wiki **and modeling substrate** for Brazilian listed companies (bancos, incorporadoras, rental, etc.), following Karpathy's LLM-wiki pattern. This is also an Obsidian vault. There is **no code, no build, no tests** — operations are markdown/JSON reads and writes performed by the LLM.

Two complementary uses:
1. **Knowledge wiki** — entity / concept / sector / comparison / synthesis pages with citations.
2. **Modeling substrate** — preserved, structured source material used to build detailed financial models (planilha completa). The wiki carries the *thesis*, the modeling layer carries the *numbers and qualitative footing* (notas explicativas, MD&A).

**Always read `SCHEMA.md` before any wiki operation.** It is the operational contract (layers, page types, frontmatter, citation format, operation steps). `README.md` has the user-facing tutorial in Portuguese.

## Commands

### Fetch filings from CVM

```bash
# Normal mode — downloads missing filings to sources/undigested/
bash tools/fetch.sh TEND3
bash tools/fetch.sh TEND3 --horizon 5y --types dfp,itr,release

# Discovery mode — downloads a sample quarter, classifies docs, creates fetch_profile
bash tools/fetch.sh TEND3 --discover
```

Requires CVM-API running at localhost:8100 (`cd ../CVM-API && uvicorn main:app --reload --port 8100`).

### Fetch call transcripts from YouTube

```bash
# Discover mode — lists channel videos + live streams, scores by period regex, writes audit plan
bash tools/fetch_calls.sh DIRR3 --discover

# Normal mode — downloads high-confidence entries from the plan
bash tools/fetch_calls.sh DIRR3

# Force single video (for ambiguous titles)
bash tools/fetch_calls.sh DIRR3 --url https://www.youtube.com/watch?v=... --period 4T24
```

Requires `youtube_channel` in the empresa's manifest. Lists both `/videos` and `/streams` tabs (earnings calls are often live-streamed). Outputs `{empresa}_call_transcript_{periodo}.md` to `sources/undigested/` with YAML frontmatter and `[mm:ss]` anchors every ~60s.

Caption priority: manual `pt`/`pt-BR` → auto `pt`/`pt-BR` → skip with `[fetch-calls-skip]` log entry.

### Ingest call transcripts (from fetch_calls output)

```bash
bash tools/ingest_calls.sh DIRR3              # default concurrency 4
bash tools/ingest_calls.sh DIRR3 -j 2          # limit concurrency
```

Scans `sources/undigested/{empresa}_call_transcript_*.md`, copies each to `sources/full/{empresa}/{periodo}/call_transcript.md`, invokes the call-transcript ingest prompt to produce `sources/digested/{empresa}_call_transcript_{periodo}_summary.md`, updates the manifest, appends `[wiki-queue]`, and deletes the source from undigested/. No `structured/` file is produced — transcripts are qualitative; numbers belong to release/ITR.

### Ingest files

```bash
# Processes all files in sources/undigested/ for the given ticker
bash tools/ingest.sh TEND3
bash tools/ingest.sh TEND3 --concurrency 4

# Ingest a generic source (spreadsheet, research report, etc.) — no ticker
bash tools/ingest.sh --generic planilha_setor.xlsx
```

Pipeline: PDF extraction → copy extracted to `full/` → `claude --print` agents produce `structured/` + `digested/` → manifest update → append `[wiki-queue]` to `log.md` → cleanup.

**Important:** `ingest.sh` does NOT update wiki pages directly. It appends to the wiki queue. Run `wiki_update.sh` separately.

A manifest must exist for the ticker (created by `fetch.sh --discover` or manually).

### Wiki update — update/create wiki pages

```bash
# First run or rebuild: reads ALL digesteds, ignores queue
bash tools/wiki_update.sh --full

# Incremental: reads only pending [wiki-queue] entries from log.md
bash tools/wiki_update.sh
```

Two-phase architecture:
1. **Planning** — `claude --print` reads all digesteds, existing wiki pages, and empresas list. Produces a JSON plan (which pages to create/update/skip, with mapped digesteds per page).
2. **Execution** — one `claude --print` per page, with targeted context (only relevant digesteds). Order: entity → concept → sector → comparison.

### Re-ingest full/ — fix truncated transcriptions

```bash
# Re-downloads PDFs from CVM and copies directly to full/ (no LLM)
bash tools/reingest_full.sh CURY3 --horizon 3y
```

Downloads directly via `cvm_fetch.py` (bypasses manifest/fetch agent). Does NOT re-generate `structured/` or `digested/`.

### Query data

```bash
bash tools/query.sh "qual o distrato da Cury no 3T24?"
bash tools/query.sh "compare a margem bruta da Direcional vs Cury em 2024"
```

Searches structured/ → full/ → digested/ with spaced-text normalization. Returns cited answers. Never invents data.

### File extraction (standalone)

```bash
python tools/lib/file_extract.py <file.pdf>       # PDF (opendataloader + pdfplumber)
python tools/lib/file_extract.py <file.xlsx>      # Excel (markitdown)
python tools/lib/file_extract.py <file.docx>      # Word (markitdown)
# Returns JSON: {"output": "path/to/extracted.md", ...}
```

### Manifest update (standalone)

```bash
python tools/lib/manifest_update.py --manifest sources/manifests/tenda.json \
    --type itr --period 3T25 \
    --full sources/full/tenda/3T25/itr.md \
    --structured sources/structured/tenda/3T25/itr.json \
    --digested sources/digested/tenda_itr_3T25_summary.md \
    --log log.md
```

### Manifest rebuild (full rescan from disk)

```bash
python tools/lib/manifest_rebuild.py --empresa cyrela            # apply
python tools/lib/manifest_rebuild.py --empresa cyrela --dry-run  # preview only
```

Scans `sources/structured/`, `sources/full/`, `sources/digested/` for the given empresa. Rebuilds `coverage` (canonical keys: bp, dre, operacional, financeiro_ajustado) and `sources[]` (flat registry of all ingested files). Preserves top-level metadata (aliases, fetch_profile, etc.) and `ingested_on` dates from existing entries.

**Caveat:** do NOT use on Tenda — its manifest uses a `data_pack` pattern with grouped `full` lists that the rebuilder doesn't handle. Use surgical edits instead.

## Architecture — five layers under `sources/`

```
sources/
├── undigested/                                 # inbox, deleted after ingest
├── full/{empresa}/{periodo}/{tipo}.md          # direct copy from PDF extraction (the "floor")
├── full/generic/{filename}.md                  # non-CVM sources (planilhas, reports)
├── structured/
│   ├── _schemas/{setor}.json                   # canonical schema per sector (on demand)
│   └── {empresa}/{periodo}/{tipo}.json         # canonical + company_specific (with _schema_path)
├── digested/{name}_summary.md                  # wiki-facing TL;DR
├── manifests/{empresa}.json                    # discovery manifest — coverage, sources, precedence
├── index.md                                    # source registry
└── notion_tracker.md                           # notion ingest state
```

Plus **wiki pages** (`*.md` at repo root) — entity/concept/sector/comparison/synthesis/nota, with YAML frontmatter, `[[wikilinks]]`, and `(fonte: ...)` citations on every factual claim.

Layer details, field semantics, and manifest shape are defined in `SCHEMA.md`.

## Tools architecture

```
tools/
├── fetch.sh                    # orchestrator: CVM fetch → sources/undigested/
├── fetch_calls.sh              # orchestrator: YouTube channel → captions → sources/undigested/
├── ingest.sh                   # orchestrator: undigested/ → full/ + structured/ + digested/ + queue
├── ingest_calls.sh             # orchestrator: call transcripts → full/ + digested/ + queue
├── wiki_update.sh              # orchestrator: digesteds → wiki pages (two-phase: plan + execute)
├── query.sh                    # query agent: answers questions by searching structured/full/digested
├── reingest_full.sh            # re-download PDFs → full/ (no LLM, bypasses manifest)
├── lib/
│   ├── calls_plan.py           # builds sources/manifests/{empresa}_calls_plan.json from yt-dlp output
│   ├── cvm_fetch.py            # CVM-API client (resolve ticker, list docs, download, batch-download)
│   ├── file_extract.py          # PDF/XLSX/DOCX/PPTX → markdown (opendataloader/pdfplumber/markitdown)
│   ├── manifest_rebuild.py     # rebuild manifest coverage+sources[] from disk (handles all empresas except Tenda)
│   ├── manifest_update.py      # programmatic manifest updates (coverage, sources, precedence)
│   ├── pdf_extract.py          # PDF → markdown via pdfplumber (fallback extractor)
│   ├── reingest_download.py    # helper for reingest: downloads docs from CVM list JSON via stdin
│   ├── vtt_to_markdown.py      # WebVTT → markdown with sparse [mm:ss] anchors (used by fetch_calls.sh)
│   └── parallel.sh             # parallel execution helper (parallel_init, parallel_add, parallel_wait)
└── prompts/
    ├── fetch_system.md         # system prompt for fetch agent (normal mode)
    ├── fetch_discover.md       # system prompt for fetch agent (discovery mode)
    ├── ingest_heavy.md         # system prompt for heavy ingest — reads full/, produces structured/ + digested/
    ├── ingest_light.md         # system prompt for light ingest — reads full/, produces digested/ only
    ├── ingest_generic.md       # system prompt for generic (non-CVM) source ingest
    ├── ingest_call_transcript.md # system prompt for call-transcript ingest (qualitative digest)
    ├── wiki_plan.md            # system prompt for wiki update planning phase
    ├── wiki_write.md           # system prompt for wiki page creation/update
    └── query_system.md         # system prompt for data query agent
```

All orchestrators invoke `claude --print` with `--allowedTools "Bash" --permission-mode bypassPermissions`.

### Data flow

```
CVM-API → fetch.sh → sources/undigested/
                          ↓
                    file_extract.py → extracted.md
                          ↓
                    ingest.sh copies → sources/full/ (direct, no LLM)
                          ↓
                    claude --print → sources/structured/ + sources/digested/
                          ↓
                    [wiki-queue] appended to log.md
                          ↓
                    wiki_update.sh (separate step) → wiki pages (*.md at root)
```

### Wiki queue (log.md)

`ingest.sh` appends parseable entries:
```
[wiki-queue] 2026-04-12 | cury | itr | 3T25 | sources/digested/cury_itr_3T25_summary.md
[wiki-queue] 2026-04-12 | generic | sector | planilha | sources/digested/planilha_setor_summary.md
```

`wiki_update.sh` consumes the queue and marks with `[wiki-done] date | batch_id`.

## Current coverage

| Empresa | Ticker | ITR | DFP | Release | Prévias | Fatos Rel. | Calls | Obs |
|---------|--------|-----|-----|---------|---------|------------|-------|-----|
| Cury | CURY3 | 1T23–3T25 | 2022–2025 | 4T22–4T25 | 1T23–1T26 | 11 | — | 2 RCAs (1T26) |
| Cyrela | CYRE3 | 1T23–3T25 | 2023–2025 | 4T22–4T25 | 1T24–1T26 | 6 | — | |
| Direcional | DIRR3 | 1T23–3T25 | 2022–2025 | 4T22–4T25 | 1T24–1T26 | 18 | 22 (3T20–4T25) | |
| Tenda | TEND3 | 1T24–3T25 | 2023–2025 | 4T23–4T25 | 1T26 | 5 | — | histórico 1T11–4T22 via data_pack (planilha) |

## Non-obvious rules

- **Filenames**: `snake_case`, lowercase, Portuguese when natural. **No ticker prefixes** on wiki pages (`itau.md`, not `ITUB4_itau.md`) — tickers go in `aliases`. Period codes: `1T25`, `2T25`, `3T25`, `4T25`, `2025` (annual). Source type tokens: `itr`, `dfp`, `release`, `apresentacao`, `fato_relevante`, `call_transcript`, `previa_operacional`, `rca`, `data_pack`.
- **Frontmatter is mandatory** on every wiki page: `type`, `sources` (paths into `sources/`), `created`, `updated` (and optional `aliases`).
- **`full/` is a direct copy from file_extract.py output.** The LLM does NOT produce `full/` files — they are copied verbatim from the extracted markdown. This guarantees 100% content preservation (notas explicativas, tables, etc.).
- **`structured/` shape**: `{_schema, _schema_path, _empresa, _periodo, _source, canonical, company_specific}`. Missing canonical keys → `null`, never omit. Numbers as reported; normalizations belong to the modeling layer.
- **`manifests/{empresa}.json` is mandatory** — every heavy/light ingest MUST update it. A cold-start modeling agent reads this file first.
- **Citations** — prefer `(fonte: full/itau/3T25/itr.md §nota_18)` for qualitative, `(fonte: structured/itau/3T25/itr.json :: canonical.dre.margem_financeira)` for numeric, `(fonte: url, confiabilidade: nivel)` for web.
- **Never invent numbers** — every figure traces to `structured/`/`full/`/web/notion. Mark stale with `[stale: last verified YYYY-MM-DD]`. When data is missing from `digested/`, **always search `full/` and `structured/` before reporting as unavailable**. Never fill gaps with estimates, interpolations, or "approximate" values — if the number is not in a source, say "n/d" and cite what was searched.
- **Wikilinks** only to pages that exist or should exist. First mention in a section gets linked; subsequent mentions do not.
- **Do not edit files in `sources/`** — sources are immutable. To correct, re-ingest.
- **`log.md` is append-only.** Every operation appends an entry. Wiki queue entries use `[wiki-queue]` / `[wiki-done]` format.
- **One source at a time** during ingest so cross-linking stays coherent.
- **Write-through backfill**: when a query reads `full/` for a structurable fact not in `structured/`, backfill it into `company_specific` before responding (see SCHEMA.md §Query step 6).
