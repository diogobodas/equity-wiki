# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## What this is

An LLM-maintained knowledge wiki for Brazilian listed companies (banks, incorporadoras, rental, etc.), following Karpathy's LLM-wiki pattern. This is also an Obsidian vault. There is **no code, no build, no tests** — operations are markdown reads/writes performed by the LLM.

**Always read `SCHEMA.md` before any wiki operation.** It is the operational contract (page types, frontmatter, citation format, operation steps). `README.md` has the user-facing tutorial in Portuguese.

## Architecture — three layers

1. **`sources/`** — source material with a two-phase lifecycle:
   - `sources/undigested/` — inbox for raw files (PDF/md/images). User drops, LLM processes, LLM **deletes** the original.
   - `sources/digested/{name}_summary.md` — exhaustive structured extraction (all tables, all numbers) generated during ingest. Permanent.
   - `sources/index.md` — registry of every source (file / web / notion), with status.
   - `sources/notion_tracker.md` — tracks which Notion pages have been digested (for incremental sweeps).
2. **Wiki pages** (`*.md` at repo root) — entity / concept / sector / comparison / synthesis pages with YAML frontmatter and `[[wikilinks]]`. Every factual claim carries an inline `(fonte: ...)` citation.
3. **`SCHEMA.md`** — conventions, frontmatter spec, operation workflows. `index.md` is the category catalog, `log.md` is the append-only operation history, `_coverage_tracker.md` tracks per-company/period source completeness.

## Core operations (all defined in SCHEMA.md)

- **Ingest (file)** — read source in `undigested/` → create/update wiki pages → write exhaustive `digested/{name}_summary.md` → delete original → update `sources/index.md` + `log.md`.
- **Ingest (web)** — WebSearch/WebFetch → classify reliability (`oficial` / `editorial` / `community`) → inline citation `(fonte: url, confiabilidade: nivel)` → register URL in `sources/index.md`.
- **Ingest (notion)** — via `mcp__claude_ai_Notion__*` tools → write `digested/notion_{slug}.md` → update `notion_tracker.md`.
- **Query** — answer from wiki with citations; promote valuable answers to new pages.
- **Lint** — dead links, orphans, stale pages (source newer than page), missing cross-refs, contradictions. Report in `log.md`.

Every operation must append an entry to `log.md`.

## Non-obvious rules

- **Filenames**: `snake_case`, lowercase, Portuguese when natural. **No ticker prefixes** on wiki pages (`itau.md`, not `ITUB4_itau.md`) — tickers live in the `aliases` frontmatter field.
- **Frontmatter is mandatory** on every wiki page: `type`, `sources`, `created`, `updated` (and optional `aliases`). See SCHEMA.md for the exact template.
- **Never invent numbers** — every figure traces to a source in `sources/`. Mark stale claims with `[stale: last verified YYYY-MM-DD]`. Flag contradictions explicitly rather than silently choosing one value.
- **Wikilinks** only to pages that exist or should exist. First mention in a section gets linked; subsequent mentions in that section do not.
- **Do not edit files in `sources/`** — sources are immutable.
- **`log.md` is append-only**.
- **One source at a time** during ingest so cross-linking stays coherent.
