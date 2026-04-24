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

### Fetch pages from Notion Capstone

```bash
# List pages with no-op (count + first 20)
bash tools/fetch_notion.sh --discover

# Fetch all new-or-edited pages into sources/undigested/
bash tools/fetch_notion.sh

# Only fetch N pages this run (recommended for first batches)
bash tools/fetch_notion.sh --limit 10

# Force a single page by id (bypasses state filter)
bash tools/fetch_notion.sh --page <notion_page_id>
```

Requires `NOTION_TOKEN` in env or `.env` at repo root. Config at `sources/manifests/_notion.json`. State (pages processed, keyed by `last_edited_time`) persists to `sources/manifests/_notion_state.json` — rerunning the fetcher only surfaces pages whose `last_edited_time` is newer than what we've seen. Writes frontmattered markdown to `sources/undigested/notion_<slug>.md`. Does NOT mark pages in Notion; the loop closes locally via state file when `ingest.sh --notion` completes successfully.

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

# Ingest a single Notion page previously staged by fetch_notion.sh
bash tools/ingest.sh --notion sources/undigested/notion_<slug>.md
```

Pipeline: PDF extraction → copy extracted to `full/` → `claude --print` agents produce `structured/` + `digested/` → manifest update → append `[wiki-queue]` to `log.md` → cleanup.

**Important:** `ingest.sh` does NOT update wiki pages directly. It appends to the wiki queue. Run `wiki_update.sh` separately.

A manifest must exist for the ticker (created by `fetch.sh --discover` or manually).

### Wiki update — update/create wiki pages

```bash
# First run or rebuild: reads ALL digesteds, ignores queue
bash tools/wiki_update.sh --full

# Incremental: reads pending entries from sources/wiki_queue.json
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

### Number Guard — validate numbers in a digest against the cited source

```bash
python tools/lib/number_guard.py check sources/digested/notion_<slug>_summary.md
```

Parses every PT-BR number claim in the digest (`28,5%`, `R$ 1,2 bi`, `R$ 1.234 milhões`, `1.234.567`, `(245)` for negatives). For each claim, resolves the nearest preceding `(fonte: full/...)` citation, extracts and normalizes all numbers in that source, and compares:

- **MATCH_STRICT** — value within tolerance AND at least one non-trivial keyword overlaps between claim context and source context.
- **MATCH_LOOSE** — value within tolerance but no keyword overlap. Not marked inline; listed in report.
- **NO_MATCH** — no value within tolerance, or no citation anchor, or source file missing. Inserts ` [?]` after the claim in the digest + appears in report.

Tolerances: `±0,5 pp` absolute for percentuais, `±0,5 %` relative for monetário/inteiro. Unit normalization handles `bi|mm|mil|milhões`, PT-BR thousands-dot + decimal-comma, dot-decimal fallback, and parens-negative `(245) ≡ -245`.

Skipped (reduce false positives): YAML frontmatter, `(fonte: …)` spans, dates (`YYYY-MM-DD`, `DD/MM/YYYY`, standalone years 19xx/20xx), ordered-list and numbered-heading markers (`## 2. …`), bare digits glued to letters (`3T25`, `K6-2`).

Called automatically by `ingest.sh --notion` after the digest is produced, before enqueue. v1 covers Notion only — retrofit for CVM/calls is a future sprint.

Unit tests: `python -m pytest tests/test_number_guard.py` (6 acceptance cases from the design spec).

### Dated-claim lint

```bash
# Full report — all pages, all severities
bash tools/lint.sh

# Filter severity
bash tools/lint.sh --severity action   # only action and above
bash tools/lint.sh --severity hint     # everything

# Single page
bash tools/lint.sh --page cyrela.md
```

Scans every `*.md` at the wiki root for `(fonte: ...)` citations — both dated (with `em:`) and undated — and applies four rules at three severity levels (`hint` < `warn` < `action`): age threshold, newer source available, cross-page contradiction, and missing `em:`. Writes report to `sources/lint_reports/YYYY-MM-DD.md` and appends a `[lint]` audit line to `log.md`. Thresholds live in `tools/lint_config.json`.

### Watchlist

```bash
# Run all eligible watches (respects cadence)
bash tools/watch.sh

# Force all entries regardless of cadence
bash tools/watch.sh --force

# Single page
bash tools/watch.sh --page reforma_tributaria.md
```

Reads `watches:` frontmatter on wiki pages, runs restricted WebSearch via `claude --print`, diffs hits against `sources/watch_state/{page_slug}.json`, emits `[watch-hit]` entries to the next lint report. Never ingests automatically — signals only.

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
├── fetch_notion.sh             # orchestrator: Notion Capstone DB → sources/undigested/
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
│   ├── notion_fetch.py         # Notion API client: list/fetch pages, state tracking, markdown conversion
│   ├── number_guard.py         # number validator: digest claims vs cited source (CLI: check <digest>)
│   ├── pdf_extract.py          # PDF → markdown via pdfplumber (fallback extractor)
│   ├── reingest_download.py    # helper for reingest: downloads docs from CVM list JSON via stdin
│   ├── vtt_to_markdown.py      # WebVTT → markdown with sparse [mm:ss] anchors (used by fetch_calls.sh)
│   ├── wiki_queue.py           # wiki-queue state: enqueue/drain/clear/peek/migrate-from-log
│   └── parallel.sh             # parallel execution helper (parallel_init, parallel_add, parallel_wait)
└── prompts/
    ├── fetch_system.md         # system prompt for fetch agent (normal mode)
    ├── fetch_discover.md       # system prompt for fetch agent (discovery mode)
    ├── ingest_heavy.md         # system prompt for heavy ingest — reads full/, produces structured/ + digested/
    ├── ingest_light.md         # system prompt for light ingest — reads full/, produces digested/ only
    ├── ingest_generic.md       # system prompt for generic (non-CVM) source ingest
    ├── ingest_call_transcript.md # system prompt for call-transcript ingest (qualitative digest)
    ├── ingest_notion.md        # system prompt for Notion-note ingest (qualitative, anti-hallucination rules)
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
                    entry appended to sources/wiki_queue.json (+ audit line in log.md)
                          ↓
                    wiki_update.sh (separate step) → wiki pages (*.md at root)
```

### Wiki queue (sources/wiki_queue.json)

The queue is a JSON array at `sources/wiki_queue.json`. Each entry:
```json
{
  "empresa": "cury",
  "type": "itr",
  "periodo": "3T25",
  "digested": "sources/digested/cury_itr_3T25_summary.md",
  "queued_on": "2026-04-16"
}
```

Managed by `tools/lib/wiki_queue.py` (subcommands: `enqueue`, `drain`, `clear`, `peek`, `migrate-from-log`).

- `ingest.sh` / `ingest_calls.sh` append via `enqueue` (and still write `[wiki-queue]` to log.md as audit trail)
- `wiki_update.sh` drains the queue at the start of an incremental run; on success calls `clear`
- `log.md` entries `[wiki-queue]` / `[wiki-done]` are AUDIT ONLY — not the source of truth anymore

To inspect pending items: `python tools/lib/wiki_queue.py peek`.

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
- **Dated claims** — any claim that can become factually wrong without the period changing (alíquotas, regras fiscais, guidance, metas datadas, valores regulatórios) carries `em: YYYY-MM-DD` in the citation: `(fonte: X, em: 2026-04-10)`. `em:` is the real-world effective date, not the ingest date. See `SCHEMA.md §Dated Claims` for criteria and `SCHEMA.md §Supersession` for update modalities.
- **Never invent numbers** — every figure traces to `structured/`/`full/`/web/notion. Mark stale with `[stale: last verified YYYY-MM-DD]`. When data is missing from `digested/`, **always search `full/` and `structured/` before reporting as unavailable**. Never fill gaps with estimates, interpolations, or "approximate" values — if the number is not in a source, say "n/d" and cite what was searched.
- **Wikilinks** only to pages that exist or should exist. First mention in a section gets linked; subsequent mentions do not.
- **Do not edit files in `sources/`** — sources are immutable. To correct, re-ingest.
- **`log.md` is append-only and audit-only.** Every operation appends an entry. `[wiki-queue]` / `[wiki-done]` lines are historical audit markers — the live queue state lives in `sources/wiki_queue.json`. Do NOT write `[wiki-done]` manually to mark a page edit; use standard `[edit]` / `[update]` entry formats.
- **One source at a time** during ingest so cross-linking stays coherent.
- **Write-through backfill**: when a query reads `full/` for a structurable fact not in `structured/`, backfill it into `company_specific` before responding (see SCHEMA.md §Query step 6).
