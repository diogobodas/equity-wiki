# Fetch Calls Tool Design

## Goal

A CLI tool (`tools/fetch_calls.sh`) that downloads earnings-call transcripts from YouTube for a given ticker and drops them in `sources/undigested/` for the standard ingest pipeline. Uses the company's official YouTube channel as the source of truth, not the RI page.

Target: one command covers a horizon of 20 quarters (1T21–4T25) per empresa, with a discovery pass that is auditable before anything is downloaded.

## Architecture

```
fetch_calls.sh TICKER --discover
    ↓
  reads sources/manifests/{empresa}.json → youtube_channel
    ↓
  yt-dlp --flat-playlist → list {id, title, upload_date}
    ↓
  period extraction + confidence scoring
    ↓
  writes sources/manifests/{empresa}_calls_plan.json
    ↓
  prints audit table to stdout, does NOT download

fetch_calls.sh TICKER
    ↓
  reads {empresa}_calls_plan.json
    ↓
  for each high-confidence entry not already in undigested/ or full/:
      yt-dlp --write-subs pt.* (manual → auto) --skip-download
          ↓
      vtt_to_markdown.py → cleaned markdown with sparse [mm:ss] anchors
          ↓
      prepend frontmatter, save to sources/undigested/{empresa}_call_transcript_{periodo}.md
          ↓
      append [fetch-calls] entry to log.md
```

## Files

- `tools/fetch_calls.sh` — bash orchestrator
- `tools/lib/vtt_to_markdown.py` — VTT → markdown converter with coarse `[mm:ss]` timestamps
- `sources/manifests/{empresa}_calls_plan.json` — per-empresa discovery plan (auditable)

No new prompt template — this tool is deterministic (no LLM agent in the loop).

## Schema change — manifest

Add one optional top-level field to `sources/manifests/{empresa}.json`:

```json
{
  "youtube_channel": "https://www.youtube.com/@direcionalengenharia"
}
```

Absent field → `fetch_calls.sh` refuses to run with a clear error pointing the user at the manifest. Existing manifests are unaffected.

## CLI

```bash
# Discovery pass — lists candidates, writes plan, nothing downloaded
tools/fetch_calls.sh TICKER --discover [--horizon 5y]

# Normal pass — downloads high-confidence entries from the plan
tools/fetch_calls.sh TICKER [--horizon 5y]

# Force single-URL download — bypasses plan, for ambiguous videos
tools/fetch_calls.sh TICKER --url URL --period PPP
```

Flags:
- `--horizon Ny` (default `5y`): filters by `upload_date` (today minus N years). Independent of period extraction — a late-posted 1T20 call won't be downloaded if it's past horizon.
- `--discover`: discovery-only mode (see below).
- `--url URL --period PPP`: force-download a specific video, tagged with the given period. Skips plan entirely, still writes to `undigested/` and `log.md`. Used for medium/low-confidence videos the user wants to salvage.

Positional arg `TICKER` (e.g., `DIRR3`) resolved to `empresa_slug` via manifest lookup (same pattern as `fetch.sh`).

## Discovery flow (`--discover`)

1. Load `sources/manifests/{empresa}.json`; error loud if `youtube_channel` missing.
2. `yt-dlp --flat-playlist --print "%(id)s\t%(title)s\t%(upload_date)s" {youtube_channel}/videos`.
3. For each row:
   - **Period extraction** — try regexes in order, first match wins:
     - `(?i)\b([1-4])T\s*(\d{2}|20\d{2})\b` → `{N}T{YY}`
     - `(?i)\bQ([1-4])\s*(20\d{2})\b` → `{N}T{YY}`
     - `(?i)\b([1-4])º?\s*trimestre\s*(?:de\s*)?(20\d{2})\b` → `{N}T{YY}`
     - None → period = `null`
   - **Confidence scoring**:
     - `high` = period extracted AND title contains one of `teleconferência|teleconferencia|resultado|call|divulgação|divulgacao`
     - `medium` = period extracted OR keyword, but not both
     - `low` = neither
   - **Existing check** — `existing=true` if either `sources/undigested/{empresa}_call_transcript_{periodo}.md` or `sources/full/{empresa}/{periodo}/call_transcript.md` exists.
4. Apply `--horizon` filter on `upload_date`.
5. Detect period collisions (two rows, same period, both high/medium). Keep the oldest `upload_date` as primary; mark the rest with `duplicate_of: <primary_video_id>`.
6. Write plan:

```json
{
  "empresa": "direcional",
  "ticker": "DIRR3",
  "channel": "https://www.youtube.com/@direcionalengenharia",
  "generated_at": "2026-04-14",
  "horizon": "5y",
  "entries": [
    {
      "video_id": "Vl_XJnZBFfE",
      "url": "https://www.youtube.com/watch?v=Vl_XJnZBFfE",
      "title": "Direcional | Teleconferência 4T24",
      "upload_date": "2025-03-06",
      "period": "4T24",
      "confidence": "high",
      "existing": false,
      "duplicate_of": null
    }
  ]
}
```

7. Print audit table to stdout grouped by confidence:

```
[high — will download on default run]
  period  upload_date  video_id      title                            existing
  4T24    2025-03-06   Vl_XJnZBFfE   Teleconferência 4T24             no
  3T24    2024-11-08   ...           ...                              yes (in full/)

[medium — review and use --url to force]
  ...

[low — unlikely calls, ignored]
  ...
```

8. Does NOT download anything. Does NOT modify `log.md`.

## Normal flow (default)

1. Load `{empresa}_calls_plan.json`; error if absent (instruct user to run `--discover`).
2. For each entry where `confidence == "high"`, `existing == false`, `duplicate_of == null`:
   - Caption priority:
     1. `yt-dlp --write-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt -o temp/{video_id}.%(ext)s {url}` (manual subs)
     2. If no manual sub written, fall back to `--write-auto-subs --sub-langs "pt,pt-BR"` (auto-generated).
     3. If still nothing, warn and skip. Append `[fetch-calls-skip] {date} | {empresa} | {period} | {url} | no_captions` to `log.md`.
   - Convert VTT → markdown via `tools/lib/vtt_to_markdown.py` (see below).
   - Prepend frontmatter:
     ```yaml
     ---
     type: call_transcript
     ticker: DIRR3
     empresa: direcional
     periodo: 4T24
     source_url: https://www.youtube.com/watch?v=Vl_XJnZBFfE
     video_id: Vl_XJnZBFfE
     captions: manual  # or auto
     fetched: 2026-04-14
     ---
     ```
   - Save to `sources/undigested/{empresa}_call_transcript_{periodo}.md`.
   - Append `[fetch-calls] {date} | {empresa} | {period} | {url} | {captions}` to `log.md`.
3. Cleanup `temp/` VTT files.

## vtt_to_markdown.py

Deterministic VTT → markdown converter.

**Input**: path to `.vtt` file (stdin or `--input`).
**Output**: markdown on stdout.

Algorithm:
1. Parse VTT cues (start time + text).
2. Deduplicate overlapping cues — YouTube auto-subs emit the same line multiple times with rolling window. Keep first occurrence of each unique line.
3. Strip inline timestamp tags (`<00:00:05.280>`) and styling tags (`<c>...</c>`).
4. Normalize whitespace; collapse runs of blank cues.
5. Emit paragraphs: start a new paragraph every ~60s OR on a sentence boundary (`.?!` followed by capital letter) within a cue.
6. Prepend each paragraph with `[mm:ss]` = start time of the first cue in that paragraph.

Example output:
```
[00:00] Bom dia a todos, sejam muito bem-vindos à teleconferência de resultados da Direcional referente ao 4T24. Eu sou...

[01:03] Começando pelos destaques operacionais do trimestre, os lançamentos atingiram R$ 2,1 bilhões, um aumento de...
```

Python stdlib only (`re`, `argparse`, `sys`). No external deps.

## Idempotency

Default run is idempotent: re-running skips entries already downloaded. The plan file itself is regenerated on every `--discover` and should be treated as cache — safe to delete and rebuild.

Force-download via `--url --period` overwrites the target file and appends a new `log.md` entry (no dedup).

## Error handling

| Scenario | Behavior |
|---|---|
| Ticker not in manifests | Exit 1, `error: ticker DIRR3 not found in sources/manifests/` |
| Manifest has no `youtube_channel` | Exit 1, message points at manifest path |
| Channel URL returns nothing / 404 | Exit 1, loud error |
| Discovery finds zero videos matching regex | Write empty plan, warn, exit 0 |
| Period collision | Keep oldest, mark others `duplicate_of`, log warning |
| No captions available | Warn, skip this video, continue to next |
| `vtt_to_markdown.py` fails on a file | Warn, skip, log `[fetch-calls-error]` entry, continue |
| Plan missing on default run | Exit 1, instruct to run `--discover` |

## log.md integration

New entry types (append-only, consistent with existing `[wiki-queue]` pattern):

```
[fetch-calls] 2026-04-14 | direcional | 4T24 | https://...Vl_XJnZBFfE | manual
[fetch-calls-skip] 2026-04-14 | direcional | 2T22 | https://... | no_captions
[fetch-calls-error] 2026-04-14 | direcional | 1T21 | https://... | vtt_parse_failed
```

No entry for `--discover` runs (plan file itself is the artifact).

## Out of scope

- Automatic ingest trigger — user still runs `tools/ingest.sh TICKER` after downloading.
- Channel discovery — user must fill in `youtube_channel` in the manifest manually. No attempt to guess it from ticker.
- Non-Portuguese captions — only `pt` / `pt-BR` supported for now.
- RI-page scraping as fallback — explicitly rejected in design.
- Speaker diarization — transcripts are flat text with timestamps, no "CEO: / CFO:" labels.

## Testing

Manual smoke test on Direcional:
1. Add `youtube_channel` to `sources/manifests/direcional.json`.
2. Run `tools/fetch_calls.sh DIRR3 --discover`; audit table should list ~20 high-confidence rows covering 1T21–4T25.
3. Run `tools/fetch_calls.sh DIRR3`; inspect 2–3 output files in `undigested/` for clean paragraphs with `[mm:ss]` anchors and correct frontmatter.
4. Re-run same command → should be a no-op (idempotency).
5. Run `tools/ingest.sh DIRR3` end-to-end; confirm transcripts land in `sources/full/direcional/{periodo}/call_transcript.md`.

No automated test suite — consistent with the rest of `tools/` (all orchestrators are manually validated).
