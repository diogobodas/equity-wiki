# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## What this is

An LLM-maintained knowledge wiki **and modeling substrate** for Brazilian listed companies (bancos, incorporadoras, rental, etc.), following Karpathy's LLM-wiki pattern. This is also an Obsidian vault. There is **no code, no build, no tests** — operations are markdown/JSON reads and writes performed by the LLM.

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
