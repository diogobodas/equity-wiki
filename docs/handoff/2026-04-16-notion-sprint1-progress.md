# Sprint 1 Handoff — Notion Digest + Number Guard

**Status:** Commit 1 (Notion Bridge) implemented + smoke-tested. 4 commits remaining.

**Date:** 2026-04-16

## Where we stopped

Implementation of **Commit 1 (Notion Bridge)** is complete and verified end-to-end against the real Capstone database (527 pending pages detected). The remaining 4 commits from the rollout plan are NOT started.

**Why the handoff:** working directory was a UNC network path (`\10.10.10.2\...`) which triggered Claude Code's "suspicious path" permission checks constantly. User will `git clone` to a local `C:\` path to continue.

## Design context (READ THIS FIRST)

Spec: `docs/superpowers/specs/2026-04-16-notion-digest-design.md` (commit `6faf1eb`).

**Important design change made during implementation (NOT yet reflected in spec):**

The spec assumed the Capstone Notion DB has an `ingest` property (pending/done select) and properties named `empresa`, `tipo`, `data`, `Name`. **None of these exist.**

Actual Capstone schema:
- `Segmento (AI)` — type `title` (this IS the page title despite the weird name)
- `Tags` — type `multi_select` (50+ options: empresa names, sectors, themes)
- `Criado em` — created_time (auto)
- `Atualizado` — last_edited_time (auto)

**Design adapted to schema (user-approved option D):**

- **Ingest trigger:** state tracking via `sources/manifests/_notion_state.json`. Every run lists ALL pages, compares each page's `last_edited_time` against `state.processed_pages[page_id]`. New/edited pages go to pending.
- **Empresa routing:** cross-reference `Tags` with `known_empresas` list + `tag_to_empresa` mapping in config. First match wins. Unknown → `generic`.
- **No Notion writes:** original spec's `mark_done` (PATCH page) was replaced by local `mark_processed(page_id, edited)` which just updates the state file. The loop is closed locally, not in Notion.

The spec still reads like the old design. Phase 5 (docs commit) should add an amendment section or inline correction documenting the change.

## Files already written (Commit 1 candidates — NOT YET COMMITTED)

- `sources/manifests/_notion.json` — database ID, token env name, title/tags property names, `known_empresas` list, `tag_to_empresa` map, rate limit config
- `tools/lib/notion_fetch.py` (381 lines) — full library: load_config/load_state/save_state, HTTP `_request` with rate limit + 429 backoff, `blocks_to_markdown` (supports 11 block types + unsupported warning), `list_new_or_edited`, `fetch_page_blocks`, `_summarize_page`, `extract_empresa`, `_slugify`, `_frontmatter`, `page_to_undigested`, `mark_processed`. Token loaded from env or `.env` fallback.
- `tools/fetch_notion.sh` — orchestrator with flags: `--discover`, `--limit N`, `--page <id>`, default (fetch all pending)
- `.gitignore` — added `.env`, `.env.local`, `*.secret`

Verified:
- Config loads, valid JSON
- Python module imports, syntax OK
- Empresa mapping works (`Cyrela` tag → `cyrela`)
- `list_new_or_edited` against real Capstone returns 527 pages
- `--discover` prints first 20 with empresa inferred correctly

## Next steps after clone

1. **First verify env on new machine:**
   ```
   python -c "import requests, pytest; print(requests.__version__, pytest.__version__)"
   ```
   Install if missing: `pip install requests pytest`.

2. **Copy the `.env` file** (contains `NOTION_TOKEN`) from the original UNC path to the new cloned repo root. `.env` is gitignored so it didn't travel via `git`. Without it, nothing connects to Notion.

   Contents of the `.env` file you need to recreate:
   ```
   NOTION_TOKEN=<your_notion_integration_token_starting_with_ntn_>
   ```
   (Current token is in the chat transcript, but consider rotating it — see security note below.)

3. **Test Commit 1 works in new location:**
   ```
   bash tools/fetch_notion.sh --discover
   ```
   Expected: "Pending: 527 page(s)" and a preview of the first 20 entries.

4. **Commit 2 — Ingest route.** Create `tools/prompts/ingest_notion.md` (model after `tools/prompts/ingest_generic.md`) with the hard rules: "prefer primary numbers from source; never estimate; use n/d for missing data". Then add `--notion <file>` route to `tools/ingest.sh`, mirroring the existing `--generic` branch but:
   - Destination: `sources/full/generic/notas/<slug>.md`
   - Prompt: `ingest_notion.md`
   - Queue type: `notion`
   - On success: call `mark_processed(page_id, last_edited_time)` via `python -c` to update state

5. **Commit 3 — Number Guard.** Create `tools/lib/number_guard.py` with:
   - `extract_numbers(text)` — regex-based PT-BR number claim extractor with cite anchor tracking
   - `index_source(full_path)` — normalizes numbers from a full/ file, indexes by value
   - `match_claim(claim, index)` — MATCH_STRICT | MATCH_LOOSE | NO_MATCH
   - `annotate(digest_path, results)` — rewrites digest inserting `[?]`
   - CLI `check <digest_path>` — runs all three and writes report if any NO_MATCH
   - 6 unit tests in `tests/test_number_guard.py` (see spec for exact test cases)

6. **Commit 4 — Integration.** Plug `number_guard.py check` into the `--notion` route in `ingest.sh`, after digest, before enqueue. Ensure `mark_processed` is the LAST step (only after Guard + enqueue both succeed).

7. **Commit 5 — Docs.** Update `CLAUDE.md` with a new "Notion pipeline" section + "Number Guard" section. Add amendment to spec noting the state-tracking change.

## Batch strategy for 527 pages

Do NOT process all 527 in one run — that's ~4 hours of LLM time and $$. Suggest:
- First batch: `--limit 10` to validate the full pipeline end-to-end
- Then iterative batches of 20-50, checking output quality
- Eventually: full sweep once the pipeline is trusted

## Security note

`NOTION_TOKEN` was pasted into the chat transcript on 2026-04-16. Anyone with access to that transcript can read the token. Recommendation: **rotate the token after Sprint 1 is done** (create a new integration, revoke the old).

## Where things are

- Spec: `docs/superpowers/specs/2026-04-16-notion-digest-design.md`
- This handoff: `docs/handoff/2026-04-16-notion-sprint1-progress.md`
- Config: `sources/manifests/_notion.json`
- Lib: `tools/lib/notion_fetch.py`
- Orchestrator: `tools/fetch_notion.sh`
- (Not committed — local only) `.env` with `NOTION_TOKEN`
- (Will be created on first run of Commit 1) `sources/manifests/_notion_state.json`

