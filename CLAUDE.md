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

### Ingest files

```bash
# Processes all files in sources/undigested/ for the given ticker
bash tools/ingest.sh TEND3
```

This orchestrates: PDF extraction → heavy/light ingest via `claude --print` agents → manifest update → wiki page update → cleanup. A manifest must exist for the ticker (created by `fetch.sh` or manually).

### PDF extraction (standalone)

```bash
python tools/lib/pdf_extract.py <file.pdf>
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

Layer details, field semantics, and manifest shape are defined in `SCHEMA.md`.

## Tools architecture

```
tools/
├── fetch.sh                    # orchestrator: CVM fetch → sources/undigested/
├── ingest.sh                   # orchestrator: undigested/ → full/ + structured/ + digested/ + wiki
├── lib/
│   ├── cvm_fetch.py            # CVM-API client (resolve ticker, list docs, download)
│   ├── pdf_extract.py          # PDF → markdown via opendataloader-pdf
│   └── manifest_update.py      # programmatic manifest updates (coverage, sources, precedence)
└── prompts/
    ├── fetch_system.md         # system prompt for fetch agent (normal mode)
    ├── fetch_discover.md       # system prompt for fetch agent (discovery mode)
    ├── ingest_heavy.md         # system prompt for heavy ingest (ITR/DFP/release)
    ├── ingest_light.md         # system prompt for light ingest (fato relevante/apresentação)
    └── ingest_wiki_update.md   # system prompt for wiki page update after ingest
```

Both `fetch.sh` and `ingest.sh` invoke `claude --print` as sub-agents with specific prompts and `--permission-mode bypassPermissions`. The orchestrator handles file classification, PDF extraction, and manifest updates; the LLM agents handle content understanding (transcription, structuring, wiki writing).

## Non-obvious rules

- **Filenames**: `snake_case`, lowercase, Portuguese when natural. **No ticker prefixes** on wiki pages (`itau.md`, not `ITUB4_itau.md`) — tickers go in `aliases`. Period codes: `1T25`, `2T25`, `3T25`, `4T25`, `2025` (annual). Source type tokens: `itr`, `dfp`, `release`, `apresentacao`, `fato_relevante`, `call_transcript`.
- **Frontmatter is mandatory** on every wiki page: `type`, `sources` (paths into `sources/`), `created`, `updated` (and optional `aliases`).
- **`full/` is structured-but-uncut.** Reorganize into headings; never summarize, cut, or paraphrase content within a section. Tables remounted in markdown.
- **`structured/` shape**: `{_schema, _schema_path, _empresa, _periodo, _source, canonical, company_specific}`. Missing canonical keys → `null`, never omit. Numbers as reported; normalizations belong to the modeling layer.
- **`manifests/{empresa}.json` is mandatory** — every heavy/light ingest MUST update it. A cold-start modeling agent reads this file first.
- **Citations** — prefer `(fonte: full/itau/3T25/itr.md §nota_18)` for qualitative, `(fonte: structured/itau/3T25/itr.json :: canonical.dre.margem_financeira)` for numeric, `(fonte: url, confiabilidade: nivel)` for web.
- **Never invent numbers** — every figure traces to `structured/`/`full/`/web/notion. Mark stale with `[stale: last verified YYYY-MM-DD]`.
- **Wikilinks** only to pages that exist or should exist. First mention in a section gets linked; subsequent mentions do not.
- **Do not edit files in `sources/`** — sources are immutable. To correct, re-ingest.
- **`log.md` is append-only.** Every operation appends an entry.
- **One source at a time** during ingest so cross-linking stays coherent.
- **Write-through backfill**: when a query reads `full/` for a structurable fact not in `structured/`, backfill it into `company_specific` before responding (see SCHEMA.md §Query step 6).
