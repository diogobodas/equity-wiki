# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## What this is

An LLM-maintained knowledge wiki **and modeling substrate** for Brazilian listed companies (bancos, incorporadoras, rental, etc.), following Karpathy's LLM-wiki pattern. This is also an Obsidian vault. The content layer is markdown + JSON — no build, no test suite — but there is a small orchestration layer under `tools/` (bash + Python) that drives CVM discovery, PDF extraction, and ingest by shelling out to `claude --print` with templated prompts. The LLM still does the semantic work; `tools/` just removes boilerplate.

Two complementary uses:
1. **Knowledge wiki** — entity / concept / sector / comparison / synthesis pages with citations.
2. **Modeling substrate** — preserved, structured source material used to build detailed financial models (planilha completa). The wiki carries the *thesis*, the modeling layer carries the *numbers and qualitative footing* (notas explicativas, MD&A).

**Always read `SCHEMA.md` before any wiki operation.** It is the operational contract (layers, page types, frontmatter, citation format, operation steps). `README.md` has the user-facing tutorial in Portuguese.

## Architecture — five layers under `sources/`

```
sources/
├── undigested/                                 # inbox, deleted after ingest
├── full/{empresa}/{periodo}/{tipo}.md          # structured-but-uncut transcription (floor)
├── structured/
│   ├── _schemas/{setor}.json                   # canonical schema per sector (on demand)
│   └── {empresa}/{periodo}/{tipo}.json         # canonical + company_specific (with _schema_path)
├── digested/{name}_summary.md                  # wiki-facing TL;DR
├── manifests/{empresa}.json                    # discovery manifest — coverage, sources, precedence
├── index.md                                    # source registry
└── notion_tracker.md                           # notion ingest state
```

Plus **wiki pages** (`*.md` at repo root) — entity/concept/sector/comparison/synthesis/nota, with YAML frontmatter, `[[wikilinks]]`, and `(fonte: ...)` citations on every factual claim.

### What each layer is for

- **`undigested/`** — inbox. User drops raw files, LLM ingests, LLM deletes original.
- **`full/`** — content-lossless transcription (loses only PDF layout/images). Structured in headings (DRE, BP, FC, DMPL, DVA, Nota 1..N, MD&A). Uncut within each section. **Replaces keeping raw PDFs.** This is the floor the LLM reads when modeling or verifying a claim.
- **`structured/`** — JSON with `canonical` (follows `_schemas/{setor}.json`) + `company_specific` (free-form). Generated only for ITR/DFP/earnings releases/data packs. Feeds the planilha; determinístico; cross-empresa comparable. Every file carries `_schema` (id) and `_schema_path` (filesystem path) — agents never have to infer schema location.
- **`digested/`** — the wiki-facing TL;DR used to write entity pages. Editorial extract.
- **`manifests/`** — **discovery layer**, one JSON per empresa. Lists available periods, coverage per canonical block (filled/empty/partial/na with reason), source inventory, precedence rules when multiple sources cover the same field, and caveats. **A cold-start modeling agent reads this file FIRST.** Generated/updated at the end of every heavy/light ingest.
- **Wiki pages** — synthesis layer on top, with citations pointing into `full/` (qualitative) or `structured/` (numeric).

## Core operations (all defined in SCHEMA.md)

- **Ingest (file — ITR/DFP/release)** — heavy path. Produces `full/` + `structured/` + `digested/` + wiki updates, then deletes original. **PDF sources are pre-processed with `opendataloader-pdf` (`pip install -U "opendataloader-pdf[hybrid]"`) to produce clean markdown before the LLM ingest step.** This eliminates extraction gaps in tables, DMPL, and visual pages. See SCHEMA.md §"PDF pre-processing".
- **Ingest (file — apresentação/fato relevante/outros)** — light path. Same PDF pre-processing applies. Produces `full/` + `digested/` + wiki updates.
- **Ingest (file — data_pack, update)** — when a new-quarter XLSX arrives, re-processes the entire spreadsheet with delta detection against existing structured/ files, flags restatements, overwrites structured/, preserves prior `full/` as historical snapshot. See SCHEMA.md §"Ingest (file — data_pack, update)".
- **Ingest (web)** — WebSearch/WebFetch → classify reliability (`oficial`/`editorial`/`community`) → inline `(fonte: url, confiabilidade: nivel)`. No `full/` or `structured/`.
- **Ingest (notion)** — via `mcp__claude_ai_Notion__*` → `digested/notion_{slug}.md` → update `notion_tracker.md`.
- **Query** — search wiki first; drop into `structured/` for numeric claims; open `full/` for notas/MD&A context.
- **Modeling (planilha)** — **start by reading `sources/manifests/{empresa}.json`** to discover available periods, coverage per block, and precedence rules. Then pull `canonical` series across periods as the deterministic spine; use `company_specific` for gerencial breakdowns; open `full/` to ground projection premises; cross-check wiki for thesis.
- **`promote_nota`** — when a nota explicativa is referenced from 3+ pages, promote it to its own `type: nota` wiki page consolidating the nota across periods.
- **Lint** — dead links, orphans, stale pages, missing cross-refs, contradictions, **schema drift** (`structured/` missing canonical keys), **unpromoted recurring notas**. Report in `log.md`.

Every operation appends an entry to `log.md`.

## Non-obvious rules

- **Filenames**: `snake_case`, lowercase, Portuguese when natural. **No ticker prefixes** on wiki pages (`itau.md`, not `ITUB4_itau.md`) — tickers go in `aliases`. Period codes: `1T25`, `2T25`, `3T25`, `4T25`, `2025` (annual). Source type tokens: `itr`, `dfp`, `release`, `apresentacao`, `fato_relevante`, `call_transcript`.
- **Frontmatter is mandatory** on every wiki page: `type`, `sources` (paths into `sources/`), `created`, `updated` (and optional `aliases`).
- **`full/` is structured-but-uncut.** Reorganize into headings; never summarize, cut, or paraphrase content within a section. Tables remounted in markdown. Images/layout dropped, but captions and chart underlying numbers kept.
- **`structured/` shape**: `{_schema, _schema_path, _empresa, _periodo, _source, canonical, company_specific}`. `_schema_path` is mandatory (filesystem path to the sector schema). Missing canonical keys → `null`, never omit. Gerencial/idiossincrático → `company_specific`. Numbers as reported; normalizations belong to the modeling layer.
- **`manifests/{empresa}.json` is mandatory** — every heavy/light ingest for an empresa MUST update its manifest (coverage matrix, sources list, precedence, caveats). A cold-start modeling agent reads this file first. See SCHEMA.md §"The manifests/ layer".
- **Schemas setoriais created on demand.** First banco creates `_schemas/banco.json`. Versioned (`banco/v1`, `banco/v2`) on breaking changes. A key in `company_specific` that becomes recurrent across players gets promoted into `canonical` — log it.
- **Citations** — prefer `(fonte: full/itau/3T25/itr.md §nota_18)` for qualitative, `(fonte: structured/itau/3T25/itr.json :: canonical.dre.margem_financeira)` for numeric, `(fonte: url, confiabilidade: nivel)` for web.
- **Never invent numbers** — every figure traces to `structured/`/`full/`/web/notion. Mark stale with `[stale: last verified YYYY-MM-DD]`. Flag contradictions explicitly.
- **Wikilinks** only to pages that exist or should exist. First mention in a section gets linked; subsequent mentions do not. Wikilinks are wiki-layer only — `full/`/`structured/` use plain paths.
- **Do not edit files in `sources/`** — sources are immutable. To correct, re-ingest.
- **`log.md` is append-only.**
- **One source at a time** during ingest so cross-linking stays coherent.

## Tooling (`tools/`)

Thin orchestration around the LLM. Every script is a bash/Python wrapper that prepares inputs, invokes `claude --print` with a templated prompt from `tools/prompts/`, then runs deterministic post-processing (manifest/log updates). Nothing here replaces the LLM's judgement — it just removes boilerplate.

```
tools/
├── fetch.sh               # CVM discovery + download → sources/undigested/
├── ingest.sh              # process undigested/ for a ticker → all wiki layers
├── lib/
│   ├── cvm_fetch.py       # CVM-API CLI (resolve/list/download), JSON out
│   ├── pdf_extract.py     # PDF/ZIP → markdown (opendataloader-pdf → pdfplumber fallback)
│   └── manifest_update.py # deterministic manifest/log/index writes (no LLM)
└── prompts/
    ├── fetch_system.md    # prompt used by fetch.sh normal mode
    ├── fetch_discover.md  # prompt used by `fetch.sh --discover`
    ├── ingest_heavy.md    # ITR/DFP/release — produces full/ + structured/ + digested/
    ├── ingest_light.md    # fato relevante — produces full/ + digested/
    └── ingest_wiki_update.md  # final wiki-page refresh step of ingest.sh
```

### Common commands

```bash
# 1. Discover what a new ticker publishes (one-time classification of doc types)
bash tools/fetch.sh TEND3 --discover

# 2. Fetch missing CVM filings into sources/undigested/
bash tools/fetch.sh TEND3                              # default: 3y horizon, dfp+itr+release+fato_relevante
bash tools/fetch.sh TEND3 --horizon 5y --types itr,release

# 3. Ingest everything sitting in sources/undigested/ for that ticker
bash tools/ingest.sh TEND3
```

`ingest.sh` expects an existing `sources/manifests/{empresa}.json` (created by the first `fetch` run or by hand) — it looks up the ticker inside each manifest to resolve `empresa`. It then classifies files in `undigested/` by filename convention (`{TICKER}_{periodo}_{tipo}_*.{pdf,zip}`), pre-extracts PDFs via `tools/lib/pdf_extract.py`, and dispatches to the heavy or light prompt accordingly. Files not matching the convention fall into a "heavy other" bucket.

### Requirements

- `claude` CLI on PATH (scripts shell out to `claude --print --allowedTools Bash --permission-mode bypassPermissions`).
- Python 3 with `opendataloader-pdf` (preferred) and `pdfplumber` (fallback) for PDF extraction; `python-dateutil` for horizon math; whatever `cvm-api` needs for `cvm_fetch.py`.
- `opendataloader-pdf` hybrid mode (OCR via docling) is optional — used when DMPL/visual pages come out as image refs in standard mode. See SCHEMA.md §"PDF pre-processing".

### Non-obvious behaviors

- `fetch.sh` searches `sources/manifests/*.json` for a manifest whose `aliases` contain the ticker. Cold-start (no manifest) resolves via `cvm_fetch.py resolve` and the empresa slug is derived from the first word of the CVM display name, lowercased, NFKD-stripped.
- `ingest.sh` skips `*_extracted.md`, `*_extracted.txt`, and `*.json` in `undigested/` — those are intermediate artifacts from a prior/in-progress run.
- `manifest_update.py` is intentionally LLM-free: it appends source entries, updates `coverage[period][block]`, and writes one-line log entries. Called from `ingest.sh` after each file, not from inside the prompt.
- Prompts in `tools/prompts/` use `{{PLACEHOLDER}}` substitution done by inline Python in `fetch.sh`/`ingest.sh`. If you add a placeholder, make sure the caller passes it.
- `docs/superpowers/{plans,specs}/` hold design notes for bigger changes to the tooling — read those before refactoring the pipeline.
