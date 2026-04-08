# Wiki Schema

This file defines the structure, conventions, and workflows for this wiki.
The LLM agent reads this file before every wiki operation.

## Three-Layer Architecture

1. **sources/** — source material with two-phase lifecycle (see Source Lifecycle below)
2. **Wiki pages** (LLM-maintained) — markdown files with summaries, entity pages, concept pages, comparisons. Always cite sources. Interlinked with `[[wikilinks]]`.
3. **This schema** (configuration) — defines structure, conventions, and workflows.

## Source Lifecycle

Sources follow an **ingest & digest** pattern to keep the wiki lightweight:

```
sources/
├── index.md              # Registry of all sources (pending + digested)
├── undigested/           # Inbox — raw files land here temporarily
│   └── (empty after processing)
└── digested/             # Permanent — exhaustive markdown summaries
    └── {name}_summary.md
```

1. Raw file (PDF, article, data) is placed in `sources/undigested/`
2. LLM reads the full source and creates/updates wiki pages
3. LLM generates an **exhaustive summary** in `sources/digested/{name}_summary.md` — all tables, all numbers, all key text. Not a summary in the editorial sense, but a full structured extraction in markdown.
4. Original file is **deleted** from `undigested/`
5. `sources/index.md` is updated with status = digested and link to summary

If a future task needs data not captured in the summary, the user provides the original file again in `undigested/` for targeted re-extraction.

## Source Types

| Type | Origin | Reliability | Summary Location |
|------|--------|-------------|------------------|
| `file` | Local PDF/document in `undigested/` | — | `digested/{name}_summary.md` |
| `web` | URL fetched via WebSearch/WebFetch | `oficial` / `editorial` / `community` | Inline in wiki page |
| `notion` | Notion page via MCP tools | — | `digested/notion_{slug}.md` |

### Web Source Reliability

| Level | Examples | Trust Level |
|-------|----------|-------------|
| `oficial` | Company IR sites, BCB, CVM, ANBIMA, regulators | High — quantitative data |
| `editorial` | Valor Economico, InfoMoney, Bloomberg, Reuters | Medium — context and analysis |
| `community` | Wikipedia, blogs, forums | Low — conceptual explanations only |

### Notion Tracker

`sources/notion_tracker.md` tracks which Notion pages have been digested. Used during Notion ingest sweeps to enable incremental ingestion.

## Page Types

| Type | Description | Naming Example |
|------|-------------|----------------|
| entity | A company, person, product, or organization | `itau.md`, `cyrela.md` |
| concept | A technique, metric, principle, or idea | `custo_risco.md`, `nim.md` |
| sector | An industry or market segment | `banking.md`, `incorporadoras.md` |
| comparison | Side-by-side analysis of 2+ entities/concepts | `itau_vs_bradesco.md` |
| synthesis | Cross-cutting analysis or thesis | `tese_selic_alta.md` |

## Frontmatter (required)

Every wiki page must have YAML frontmatter:

```yaml
---
type: entity | concept | sector | comparison | synthesis
aliases: [Alternative Name 1, TICKER]  # optional
sources: [source_filename.md, another.pdf]  # which sources informed this page
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Naming Conventions

- Filenames: `snake_case.md`, lowercase, Portuguese when natural
- No ticker prefixes on wiki pages (use `itau.md` not `ITUB4_itau.md`)
- Tickers go in `aliases` frontmatter field
- Sources keep their original names in `sources/`

## Wikilinks

- Use `[[page_name]]` to link between wiki pages (Obsidian-compatible)
- Only link to pages that exist or should exist
- If a link target doesn't exist, it becomes a gap — the next ingest/lint cycle should create it or remove the link
- First mention in a section gets linked; subsequent mentions in the same section do not

## Source Citations

- Every factual claim must trace back to a source
- Inline citation format: `(fonte: source_filename.md)` or `(fonte: source_filename.pdf, p.12)`
- Sources listed in frontmatter are the complete set of sources for that page

## Quality Principles

- Never invent data — every number comes from a source
- Prefer specific over vague: "ROE de 23.4% em 2025" not "ROE alto"
- Flag contradictions explicitly: "Source A says X, Source B says Y — needs reconciliation"
- Stale claims should be marked: `[stale: last verified YYYY-MM-DD]`

## Wiki Operations

### Ingest

Triggered when a new source appears in `sources/undigested/`.

1. Read the source fully
2. Create/update wiki pages with information extracted from the source
3. Add/fix `[[wikilinks]]` for any new entities or concepts mentioned
4. Generate exhaustive summary in `sources/digested/{name}_summary.md`
5. Delete the original file from `sources/undigested/`
6. Update `sources/index.md` with status = digested
7. Append entry to `log.md`

### Ingest from Web

Create new wiki pages from web research, or enrich existing pages during sweeps.

1. Identify topic or gap to research
2. `WebSearch` with targeted queries (3-4 per topic)
3. `WebFetch` on best results (max 3-5 URLs)
4. Classify source reliability (`oficial` / `editorial` / `community`)
5. Create or update wiki pages with inline citations: `(fonte: url, confiabilidade: nivel)`
6. Register each URL in `sources/index.md` with type `web`
7. Append to `log.md`

### Ingest from Notion

Ingest study notes and call transcripts from Notion.

1. Fetch page content via `notion-fetch` or discover via `notion-search`
2. Classify content (study note vs call transcript)
3. Extract facts, data, quotes, insights
4. Create or update wiki pages with citations: `(fonte: notion, "page title")`
5. Generate summary in `sources/digested/notion_{slug}.md`
6. Update `sources/notion_tracker.md`
7. Register in `sources/index.md` with type `notion`
8. Append to `log.md`

### Query

When answering a question using the wiki:

1. Search relevant wiki pages
2. Synthesize answer with citations
3. If the answer is valuable and reusable, promote it to a new wiki page

### Lint

Periodic health check:

1. **Dead links** — `[[wikilinks]]` pointing to non-existent pages
2. **Orphan pages** — pages with zero inbound links
3. **Stale pages** — source is newer than the wiki page that cites it
4. **Missing cross-references** — page mentions a concept that has a wiki page but doesn't link it
5. **Contradictions** — same metric with different values across pages
6. Report findings in `log.md`
