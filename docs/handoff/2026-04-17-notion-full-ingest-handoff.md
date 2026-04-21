# Handoff — Notion Capstone full ingest (2026-04-17 tarde)

**Status:** Ingest done (526/527). `wiki_update.sh --full` in progress (background task `b3lid23j1`).

## Bug fixed during this handoff (line 96 of `tools/wiki_update.sh`)

On first `--full` attempt with 656 digests, `python -c` in `invoke_claude` hit Windows argv limit:
```
tools/wiki_update.sh: line 101: python: Argument list too long
```
Because `{{DIGESTED_LIST}}` was a ~45KB string passed as a single argv. Fixed: replacement values now go to temp files; only paths are on the command line. Diff is small and local to the helper function. The ingest.sh `invoke_claude` has the same pattern but never hit this limit (per-page inputs are small), so it was left alone.

## Quick state snapshot

```bash
# Verify
cd /c/Users/diogo.bodas/Desktop/Equity-wiki/equity-wiki
ls sources/undigested/ | wc -l        # expect: 0
python tools/lib/wiki_queue.py peek --count   # ~514 (drained by wiki_update on success)
python -c "import json; print(len(json.load(open('sources/manifests/_notion_state.json'))['processed_pages']))"  # ~526
```

- **526 of 527** Capstone pages ingested → `sources/digested/notion_*_summary.md`
- **1 page** unexplained gap (likely tagged but not yet materialized, or edited_time mismatch) — non-blocking
- **~514 queue entries** waiting for wiki_update
- **Background task `bjfa8o15k`** is running `wiki_update.sh --full` — reads ALL digests + all wiki pages + empresas list, plans pages, executes one-by-one

## How today's work went

### Sprint 1 (Notion pipeline + Number Guard) — already shipped

- `tools/fetch_notion.sh`, `tools/lib/notion_fetch.py` (Commit 1 pre-session)
- `tools/prompts/ingest_notion.md`, `--notion` route in `tools/ingest.sh` (Commit 2)
- `tools/lib/number_guard.py` + 6 unit tests in `tests/test_number_guard.py` (Commit 3)
- Guard integration into `--notion` route (Commit 4)
- CLAUDE.md + spec amendment (Commit 5)
- **See full spec + amendments:** `docs/superpowers/specs/2026-04-16-notion-digest-design.md`
- **Older handoff:** `docs/handoff/2026-04-16-notion-sprint1-progress.md`

### Extractor iterations (during real-data runs)

During 10-page + 50-page + 400-page batches, caught recurring extractor gaps and fixed each:

1. **List-marker filter** was too greedy (swallowed `700 million 3T25` as list item). Now requires `[.):]` punctuation.
2. **Missing units** — added `reais/real`, `k/mn/bn`, English `billion/million/thousand`.
3. **Range detection** — `90-120` was being extracted as `90` + negative `-120`. Now detects digit-before-hyphen as range separator, not sign.
4. **Compound IDs** — `K6-2`, `8086/286` rejected via letter-in-adjacent-run scan (vs. pure-digit ranges which pass through).

All 6 acceptance tests still green after each iteration.

### Wiki-writer prompt hardening

First batch produced 4 wrong wikilinks (`[[unidas|TotalPass]]` etc. — LLM was redirecting to closest existing page rather than creating dangling link for missing entity). Fixed manually + hardened `tools/prompts/wiki_write.md` with explicit rule: "if the entity doesn't have its own page, write `[[entity_name]]` as a dangling link rather than redirecting to an unrelated existing page."

### Overnight infrastructure

- `docs/handoff/batch_notion_run.sh` — sequential ingest driver with:
  - Exit 42 on auth break (HTTP 401) → overnight aborts immediately, no 4h sleeps
  - Exit 43 on systemic fast-failure streak (2 consecutive <15s fails) → same treatment
- `docs/handoff/overnight_notion.sh` — orchestrator:
  - Step 1: fetch all remaining from Notion
  - Step 2: ingest loop, 6 iterations × 4h sleep (24h window total)
  - Step 3: `wiki_update.sh --full` when undigested/ is empty
  - Reads exit codes 42/43 from batch and aborts fast
- `save_state` in `tools/lib/notion_fetch.py` is now atomic (temp file + `os.replace`) so interrupted runs don't corrupt state.

### Execution history (3 limit-break cycles)

| Run | Start state | End state | Processed | Reason stopped |
|---|---:|---:|---:|---|
| overnight v1 (madrugada) | 61 | ~144 | +83 | Claude Code auth expired mid-run |
| overnight v2 (manhã) | 144 | 280 | +136 | `hit your limit` reset 9am SP |
| overnight v3 (manhã 2) | 280 | 361 | +81 | same — rolling 5h window |
| overnight v4 (tarde) | 361 | 464 | +103 | same |
| overnight v5 (atual) | 464 | 526 | +62 | *running* |

Each break was detected by the fast-failure streak logic (exit 43) and script aborted in ~15s instead of burning hours on retry loops.

## What to watch for next

**1. wiki_update.sh --full completion (background task `bjfa8o15k`)**

Check periodically:
```bash
tail -30 "<output-file-path>"
```
Phase 1 (planner) is one big LLM call, can take 15-30 min for ~515 digests. Phase 2 executes one page at a time sequentially. Expected total: 1-2h.

**If wiki_update itself hits the rate limit:** the script doesn't have the same retry logic as `batch_notion_run.sh` — it will error out. Safe to rerun: `bash tools/wiki_update.sh --full` picks up from the current state (rewrites pages idempotently).

**2. Guard stats across the full batch (for diagnosis of systematic gaps)**

```bash
# Total claims by status across all 500+ reports
cd sources/digested
grep -h -E "^- (STRICT|LOOSE|NO_MATCH)" notion_*_guard_report.md | \
  awk '{sum[$2]+=$NF} END {for (k in sum) print k, sum[k]}'
```

Expect: high LOOSE count on tabular data (NVIDIA GPU spec notes, etc. — ~116 LOOSE on a single note). This is a known Guard v1 limitation (keyword context doesn't discriminate between table rows). Follow-up: positional lookup for tables.

**3. Obsidian vault hygiene**

8 dangling wikilinks materialized as empty .md files at vault ROOT (outside equity-wiki/) during today. All moved into equity-wiki/ manually. To prevent future:
- Obsidian → Settings → Files & Links → Default location for new notes → "Same folder as current file" (or pin to equity-wiki/)

**4. Empresa-tag mapping gaps**

Many pages routed to `generic` because their Notion tags don't match `known_empresas` or `tag_to_empresa` in `sources/manifests/_notion.json`. Common gaps spotted in processed digest names:
- `Melnick`, `SBPE`, `Kikos`, `Skyfit`, `Panobianco`, `Sport City`, `Bio Ritmo`
- `XP`, `B3`, `BR Partners`, `Stone`, `PagSeguro` (have processed notes but might not be in map)
- Add them to `sources/manifests/_notion.json` `tag_to_empresa` to get better routing on future fetches.

## Known follow-ups (not blocking)

- **Guard extractor tweaks** (not applied today):
  - Recognize written-out negatives: "menos X%" ↔ "-X%"
  - Accept unaccented units: "milhoes" (no ã) alongside "milhões"
  - Propagate unit across ranges: `350-500k` should apply `k` to both numbers
  - Tabular data: positional matching instead of keyword overlap
- **Parallelize `--notion` ingest** (3-4 at a time): `save_state` is atomic, `wiki_queue.py` is atomic. Only `log.md` appends have race risk (benign).
- **Rotate NOTION_TOKEN** (pasted in chat transcript 2026-04-16) — flagged since Sprint 1.
- **wiki_update --full doesn't clear queue** — on success it should; currently only incremental mode clears. After today's --full run, queue may still show entries (cosmetic; re-runs of --full are idempotent).

## Pointers

- Previous session handoff: `docs/handoff/2026-04-16-notion-sprint1-progress.md`
- Design spec (w/ amendments): `docs/superpowers/specs/2026-04-16-notion-digest-design.md`
- CLAUDE.md Notion pipeline + Number Guard sections: up to date
- Log of all operations: `log.md` (now 900+ lines)
