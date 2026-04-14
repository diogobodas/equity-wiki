# fetch_calls.sh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `tools/fetch_calls.sh`, a deterministic bash orchestrator that pulls earnings-call transcripts from a company's official YouTube channel and drops them in `sources/undigested/` for the standard ingest pipeline.

**Architecture:** Two-phase CLI. Phase 1 (`--discover`) lists the channel with `yt-dlp --flat-playlist`, applies period regex + keyword heuristics to score each video, writes an auditable JSON plan. Phase 2 (default) reads the plan and downloads captions (manual pt → auto pt) via `yt-dlp`, converts VTT to markdown with sparse `[mm:ss]` anchors via a stdlib Python helper, prepends frontmatter, saves under `sources/undigested/`, appends a line to `log.md`. A `--url --period` escape hatch handles ambiguous videos.

**Tech Stack:** Bash, `yt-dlp` (already installed), `jq` (already used in repo), Python 3 stdlib (no new deps), `tools/lib/parallel.sh` if batching is needed (not initially).

**Reference:** spec at `docs/superpowers/specs/2026-04-14-fetch-calls-design.md`.

---

### Task 1: Add `youtube_channel` to the Direcional manifest

**Files:**
- Modify: `sources/manifests/direcional.json` (add one top-level field)

- [ ] **Step 1: Open the manifest and add the field**

Insert `"youtube_channel": "https://www.youtube.com/@direcionalengenharia"` between `"ticker"` and `"setor"` (keeping alphabetical-ish grouping with metadata fields).

After editing, lines 8–13 of the file should look like:

```json
  "aliases": [
    "Direcional",
    "DIRR3"
  ],
  "ticker": "DIRR3",
  "youtube_channel": "https://www.youtube.com/@direcionalengenharia",
  "setor": "incorporadora",
  "setor_schema": "sources/structured/_schemas/incorporadora.json",
```

- [ ] **Step 2: Bump `_updated`**

Change `"_updated": "2026-04-11"` to `"_updated": "2026-04-14"`.

- [ ] **Step 3: Verify JSON is still valid**

Run: `jq '.youtube_channel' sources/manifests/direcional.json`
Expected output: `"https://www.youtube.com/@direcionalengenharia"`

- [ ] **Step 4: Commit**

```bash
git add sources/manifests/direcional.json
git commit -m "manifest: add youtube_channel to direcional for fetch_calls"
```

---

### Task 2: Build `tools/lib/vtt_to_markdown.py`

**Files:**
- Create: `tools/lib/vtt_to_markdown.py`

This is the only unit-testable piece of the feature (pure function, deterministic input/output). It ships with an inline `--self-test` flag.

- [ ] **Step 1: Create the file with CLI skeleton**

```python
#!/usr/bin/env python3
"""Convert a WebVTT subtitle file to clean markdown with sparse [mm:ss] anchors.

Usage:
    python tools/lib/vtt_to_markdown.py --input path/to/captions.vtt > out.md
    python tools/lib/vtt_to_markdown.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass


CUE_TIMESTAMP_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2})\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}"
)
INLINE_TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class Cue:
    start_seconds: int
    text: str


def parse_vtt(vtt_text: str) -> list[Cue]:
    """Parse VTT text → list of (start_seconds, text) cues. Deduplicates repeated lines."""
    cues: list[Cue] = []
    seen_lines: set[str] = set()
    lines = vtt_text.splitlines()
    i = 0
    while i < len(lines):
        m = CUE_TIMESTAMP_RE.match(lines[i])
        if not m:
            i += 1
            continue
        start = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        i += 1
        buf: list[str] = []
        while i < len(lines) and lines[i].strip() != "":
            buf.append(lines[i])
            i += 1
        raw = " ".join(buf)
        clean = INLINE_TAG_RE.sub("", raw).strip()
        clean = re.sub(r"\s+", " ", clean)
        if not clean or clean in seen_lines:
            continue
        seen_lines.add(clean)
        cues.append(Cue(start_seconds=start, text=clean))
    return cues


def format_timestamp(total_seconds: int) -> str:
    return f"[{total_seconds // 60:02d}:{total_seconds % 60:02d}]"


def cues_to_markdown(cues: list[Cue], paragraph_gap_seconds: int = 60) -> str:
    """Group cues into paragraphs; emit [mm:ss] anchor on each paragraph start."""
    if not cues:
        return ""
    paragraphs: list[tuple[int, list[str]]] = []
    current_start = cues[0].start_seconds
    current_buf: list[str] = []
    last_start = cues[0].start_seconds

    for cue in cues:
        if current_buf and cue.start_seconds - last_start >= paragraph_gap_seconds:
            paragraphs.append((current_start, current_buf))
            current_start = cue.start_seconds
            current_buf = []
        current_buf.append(cue.text)
        last_start = cue.start_seconds
    if current_buf:
        paragraphs.append((current_start, current_buf))

    out_lines: list[str] = []
    for start, buf in paragraphs:
        text = " ".join(buf)
        text = re.sub(r"\s+", " ", text).strip()
        out_lines.append(f"{format_timestamp(start)} {text}")
    return "\n\n".join(out_lines) + "\n"


def convert(vtt_text: str) -> str:
    return cues_to_markdown(parse_vtt(vtt_text))


def self_test() -> int:
    sample = """WEBVTT

00:00:00.000 --> 00:00:03.000
Bom dia a todos,

00:00:03.000 --> 00:00:06.000
sejam muito bem-vindos à teleconferência.

00:00:06.000 --> 00:00:09.000
sejam muito bem-vindos à teleconferência.

00:01:05.000 --> 00:01:08.000
<c>Começando pelos destaques</c> do trimestre.
"""
    out = convert(sample)
    expected = (
        "[00:00] Bom dia a todos, sejam muito bem-vindos à teleconferência.\n\n"
        "[01:05] Começando pelos destaques do trimestre.\n"
    )
    if out != expected:
        sys.stderr.write("SELF-TEST FAIL\n")
        sys.stderr.write(f"--- got ---\n{out!r}\n")
        sys.stderr.write(f"--- want ---\n{expected!r}\n")
        return 1
    print("SELF-TEST OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", help="Path to .vtt file. Reads stdin if omitted.")
    ap.add_argument("--self-test", action="store_true", help="Run inline self-test and exit.")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            vtt_text = f.read()
    else:
        vtt_text = sys.stdin.read()
    sys.stdout.write(convert(vtt_text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run self-test to verify**

Run: `python tools/lib/vtt_to_markdown.py --self-test`
Expected output: `SELF-TEST OK`

- [ ] **Step 3: Smoke-test with a real YouTube VTT**

Pick any Direcional call video ID (e.g., `Vl_XJnZBFfE` from the 4T24 call). Download captions to a temp file, convert, inspect:

```bash
mkdir -p /tmp/fetch_calls_smoke
yt-dlp --write-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt \
    -o "/tmp/fetch_calls_smoke/%(id)s.%(ext)s" \
    "https://www.youtube.com/watch?v=Vl_XJnZBFfE" || \
yt-dlp --write-auto-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt \
    -o "/tmp/fetch_calls_smoke/%(id)s.%(ext)s" \
    "https://www.youtube.com/watch?v=Vl_XJnZBFfE"

python tools/lib/vtt_to_markdown.py \
    --input /tmp/fetch_calls_smoke/Vl_XJnZBFfE.pt.vtt \
    | head -20
```

Expected: first ~10 paragraphs from a real earnings call, each prefixed with `[mm:ss]`, clean prose (no tags, no duplicated lines). If yt-dlp fetches `.pt-BR.vtt` instead of `.pt.vtt`, adjust the filename.

- [ ] **Step 4: Commit**

```bash
git add tools/lib/vtt_to_markdown.py
git commit -m "feat: add vtt_to_markdown.py — WebVTT → markdown with [mm:ss] anchors"
```

---

### Task 3: Build `tools/fetch_calls.sh` skeleton (CLI parsing + manifest resolution)

**Files:**
- Create: `tools/fetch_calls.sh`

- [ ] **Step 1: Create the script with arg parsing**

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Defaults ---
HORIZON="5y"
DISCOVER="false"
FORCE_URL=""
FORCE_PERIOD=""

usage() {
    echo "Usage: bash tools/fetch_calls.sh <TICKER> [--discover] [--horizon 5y]"
    echo "       bash tools/fetch_calls.sh <TICKER> --url URL --period PPP"
    echo ""
    echo "Downloads earnings-call transcripts from the company's YouTube channel."
    echo ""
    echo "Options:"
    echo "  --discover        List channel videos, score periods, write audit plan."
    echo "                    Does not download anything."
    echo "  --horizon Ny      Only consider videos uploaded within N years (default: 5y)."
    echo "  --url URL         Force-download a specific video (skips plan)."
    echo "  --period PPP      Period label (e.g., 4T24) for the forced download."
    exit 1
}

[[ $# -lt 1 ]] && usage
TICKER="$1"; shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --discover) DISCOVER="true"; shift ;;
        --horizon)  HORIZON="$2"; shift 2 ;;
        --url)      FORCE_URL="$2"; shift 2 ;;
        --period)   FORCE_PERIOD="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done

if [[ -n "$FORCE_URL" && -z "$FORCE_PERIOD" ]] || [[ -z "$FORCE_URL" && -n "$FORCE_PERIOD" ]]; then
    echo "error: --url and --period must be used together" >&2
    exit 1
fi

# --- Paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFESTS_PATH="$REPO_ROOT/sources/manifests"
UNDIGESTED_PATH="$REPO_ROOT/sources/undigested"
FULL_PATH="$REPO_ROOT/sources/full"
LOG_FILE="$REPO_ROOT/log.md"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

# --- Resolve ticker → empresa slug + youtube_channel ---
resolve_empresa() {
    local ticker_upper="${TICKER^^}"
    local manifest
    manifest=$(grep -l "\"ticker\": \"$ticker_upper\"" "$MANIFESTS_PATH"/*.json 2>/dev/null | head -1 || true)
    if [[ -z "$manifest" ]]; then
        echo "error: ticker $ticker_upper not found in $MANIFESTS_PATH/" >&2
        exit 1
    fi
    EMPRESA=$(jq -r '.empresa' "$manifest")
    YOUTUBE_CHANNEL=$(jq -r '.youtube_channel // empty' "$manifest")
    MANIFEST_PATH="$manifest"
    if [[ -z "$YOUTUBE_CHANNEL" ]]; then
        echo "error: manifest $manifest has no youtube_channel field" >&2
        echo "  Add: \"youtube_channel\": \"https://www.youtube.com/@...\"" >&2
        exit 1
    fi
}

resolve_empresa
echo "empresa=$EMPRESA channel=$YOUTUBE_CHANNEL"

# --- Dispatch (filled in by later tasks) ---
if [[ -n "$FORCE_URL" ]]; then
    echo "TODO force_download (Task 6)"
elif [[ "$DISCOVER" == "true" ]]; then
    echo "TODO discover (Task 4)"
else
    echo "TODO default (Task 5)"
fi
```

- [ ] **Step 2: Make it executable and run**

Run:
```bash
chmod +x tools/fetch_calls.sh
bash tools/fetch_calls.sh DIRR3
```

Expected output:
```
empresa=direcional channel=https://www.youtube.com/@direcionalengenharia
TODO default (Task 5)
```

- [ ] **Step 3: Verify missing-channel path**

Run: `bash tools/fetch_calls.sh CYRE3`
Expected: exit 1 with `error: manifest ... has no youtube_channel field` (since Cyrela's manifest doesn't have it).

- [ ] **Step 4: Verify mismatched force flags fail**

Run: `bash tools/fetch_calls.sh DIRR3 --url https://... `
Expected: exit 1 with `error: --url and --period must be used together`.

- [ ] **Step 5: Commit**

```bash
git add tools/fetch_calls.sh
git commit -m "feat(fetch_calls): CLI skeleton with ticker→manifest resolution"
```

---

### Task 4: Implement `--discover` mode

**Files:**
- Modify: `tools/fetch_calls.sh` (replace the `TODO discover` branch)

- [ ] **Step 1: Replace the discover branch and add helper functions**

Replace the `TODO discover (Task 4)` line with the full discover block. Insert these helper functions between the `resolve_empresa` call and the dispatch section:

```bash
# --- Helpers ---

# Compute horizon cutoff as YYYYMMDD (for comparing with yt-dlp upload_date).
compute_horizon_cutoff() {
    local h="$1"
    local num="${h%y}"
    local year month day
    year=$(date +%Y); month=$(date +%m); day=$(date +%d)
    printf "%04d%02d%02d" $((year - num)) "$((10#$month))" "$((10#$day))"
}

# Extract period from a title. Echoes "NTXX" or empty.
extract_period() {
    local title="$1"
    local py
    py=$(python3 - "$title" <<'PY'
import re, sys
t = sys.argv[1]
patterns = [
    (re.compile(r'\b([1-4])T\s*(\d{2}|20\d{2})\b', re.I), lambda m: f"{m.group(1)}T{m.group(2)[-2:]}"),
    (re.compile(r'\bQ([1-4])\s*(20\d{2})\b', re.I), lambda m: f"{m.group(1)}T{m.group(2)[-2:]}"),
    (re.compile(r'\b([1-4])º?\s*trimestre\s*(?:de\s*)?(20\d{2})\b', re.I), lambda m: f"{m.group(1)}T{m.group(2)[-2:]}"),
]
for rx, fmt in patterns:
    m = rx.search(t)
    if m:
        print(fmt(m))
        break
PY
)
    echo -n "$py"
}

# Score confidence: high | medium | low
score_confidence() {
    local title="$1" period="$2"
    local has_kw="false"
    if echo "$title" | grep -qiE '(teleconferência|teleconferencia|resultado|call|divulgação|divulgacao)'; then
        has_kw="true"
    fi
    if [[ -n "$period" && "$has_kw" == "true" ]]; then echo "high"
    elif [[ -n "$period" || "$has_kw" == "true" ]]; then echo "medium"
    else echo "low"
    fi
}

# Check if a period is already materialized.
check_existing() {
    local period="$1"
    if [[ -f "$UNDIGESTED_PATH/${EMPRESA}_call_transcript_${period}.md" ]]; then
        echo "undigested"
    elif [[ -f "$FULL_PATH/${EMPRESA}/${period}/call_transcript.md" ]]; then
        echo "full"
    else
        echo "no"
    fi
}

do_discover() {
    local cutoff; cutoff=$(compute_horizon_cutoff "$HORIZON")
    local plan_path="$MANIFESTS_PATH/${EMPRESA}_calls_plan.json"
    echo "listing $YOUTUBE_CHANNEL/videos (cutoff: $cutoff)..."

    local raw="$TMP_DIR/channel_list.tsv"
    yt-dlp --flat-playlist --print "%(id)s\t%(title)s\t%(upload_date)s" \
        "$YOUTUBE_CHANNEL/videos" > "$raw" 2>/dev/null

    local entries="[]"
    while IFS=$'\t' read -r vid title upload_date; do
        [[ -z "$vid" || -z "$title" ]] && continue
        [[ -n "$upload_date" && "$upload_date" < "$cutoff" ]] && continue
        local period; period=$(extract_period "$title")
        local conf; conf=$(score_confidence "$title" "$period")
        local existing="no"
        [[ -n "$period" ]] && existing=$(check_existing "$period")
        entries=$(jq --arg vid "$vid" --arg title "$title" --arg up "$upload_date" \
                     --arg period "$period" --arg conf "$conf" --arg existing "$existing" \
                     '. + [{video_id:$vid, url:("https://www.youtube.com/watch?v=" + $vid),
                            title:$title, upload_date:$up,
                            period:(if $period=="" then null else $period end),
                            confidence:$conf,
                            existing:(if $existing=="no" then false else true end),
                            existing_layer:(if $existing=="no" then null else $existing end),
                            duplicate_of:null}]' <<< "$entries")
    done < "$raw"

    # Mark duplicates: same period, high/medium. Keep oldest upload_date as primary.
    entries=$(jq '
      reduce range(0; length) as $i (.;
        .[$i] as $e |
        if ($e.period != null and ($e.confidence=="high" or $e.confidence=="medium")) then
          [range(0; length)] as $all |
          ( [$all[] | select(. != $i) | . as $j | .[$j] | select(.period == $e.period and (.confidence=="high" or .confidence=="medium"))] ) as $peers |
          if ($peers | length) > 0 then
            ( [$e] + $peers | sort_by(.upload_date) | .[0].video_id ) as $primary |
            if $e.video_id != $primary then .[$i].duplicate_of = $primary else . end
          else .
          end
        else .
        end
      )
    ' <<< "$entries")

    jq -n --arg empresa "$EMPRESA" --arg ticker "${TICKER^^}" \
          --arg channel "$YOUTUBE_CHANNEL" --arg gen "$(date +%Y-%m-%d)" \
          --arg hz "$HORIZON" --argjson entries "$entries" \
          '{empresa:$empresa, ticker:$ticker, channel:$channel,
            generated_at:$gen, horizon:$hz, entries:$entries}' > "$plan_path"

    echo ""
    echo "plan written to $plan_path"
    echo ""

    local bucket
    for bucket in high medium low; do
        local count; count=$(jq --arg c "$bucket" '[.entries[] | select(.confidence==$c)] | length' "$plan_path")
        [[ "$count" == "0" ]] && continue
        echo "[$bucket — $count video(s)]"
        jq -r --arg c "$bucket" '
            .entries[] | select(.confidence==$c) |
            "  " + (.period // "n/a") + "  " + .upload_date + "  " + .video_id +
            "  " + (if .existing then "(existing:" + .existing_layer + ")" elif .duplicate_of then "(dup of " + .duplicate_of + ")" else "" end) +
            "  " + .title
        ' "$plan_path"
        echo ""
    done
}
```

Then replace the dispatch:

```bash
if [[ -n "$FORCE_URL" ]]; then
    echo "TODO force_download (Task 6)"
elif [[ "$DISCOVER" == "true" ]]; then
    do_discover
else
    echo "TODO default (Task 5)"
fi
```

- [ ] **Step 2: Run discover on Direcional**

Run: `bash tools/fetch_calls.sh DIRR3 --discover`

Expected:
- A `sources/manifests/direcional_calls_plan.json` is created.
- Stdout shows buckets `[high — N video(s)]`, `[medium — ...]`, `[low — ...]`.
- High bucket contains ~15–20 entries matching quarterly calls (`1T21`–`4T25`).
- No files written to `undigested/` or `full/`.

- [ ] **Step 3: Sanity-check the plan JSON**

Run:
```bash
jq '.entries | map(select(.confidence=="high")) | length' sources/manifests/direcional_calls_plan.json
jq '.entries | map(select(.confidence=="high" and .period != null)) | map(.period) | sort | unique' sources/manifests/direcional_calls_plan.json
```

Expected: the length is 15+, and the unique periods include most of 1T21–4T25. If some quarters are missing, note them — they will need `--url --period` forcing later (Task 6).

- [ ] **Step 4: Verify duplicate detection**

Run: `jq '.entries | map(select(.duplicate_of != null))' sources/manifests/direcional_calls_plan.json`
Expected: either empty list, or entries where `duplicate_of` points at another `video_id` in the plan. Spot-check that the duplicates really are the same quarter.

- [ ] **Step 5: Commit**

```bash
git add tools/fetch_calls.sh
git commit -m "feat(fetch_calls): --discover mode — list channel, score periods, write plan"
```

---

### Task 5: Implement default download mode

**Files:**
- Modify: `tools/fetch_calls.sh` (replace the `TODO default` branch)

- [ ] **Step 1: Add the download helper and replace the default branch**

Insert this helper function alongside `do_discover`:

```bash
# Download captions for a single URL. Echoes the .vtt path on success, empty on skip.
# Sets CAPTION_KIND global to "manual" or "auto".
download_captions() {
    local url="$1"
    local vid; vid=$(python3 -c "import sys,re; m=re.search(r'v=([\w-]+)', sys.argv[1]); print(m.group(1) if m else '')" "$url")
    [[ -z "$vid" ]] && { echo ""; return; }
    local out_dir="$TMP_DIR/captions"
    mkdir -p "$out_dir"
    CAPTION_KIND=""

    # 1. Try manual subs
    yt-dlp --write-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt \
        -o "$out_dir/%(id)s.%(ext)s" "$url" >/dev/null 2>&1 || true
    local vtt
    vtt=$(ls "$out_dir"/"$vid".pt*.vtt 2>/dev/null | head -1 || true)
    if [[ -n "$vtt" ]]; then CAPTION_KIND="manual"; echo "$vtt"; return; fi

    # 2. Fall back to auto
    yt-dlp --write-auto-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt \
        -o "$out_dir/%(id)s.%(ext)s" "$url" >/dev/null 2>&1 || true
    vtt=$(ls "$out_dir"/"$vid".pt*.vtt 2>/dev/null | head -1 || true)
    if [[ -n "$vtt" ]]; then CAPTION_KIND="auto"; echo "$vtt"; return; fi

    echo ""
}

# Write a transcript file with frontmatter.
save_transcript() {
    local period="$1" url="$2" vid="$3" captions="$4" vtt_path="$5"
    local out="$UNDIGESTED_PATH/${EMPRESA}_call_transcript_${period}.md"
    local body; body=$(python3 "$SCRIPT_DIR/lib/vtt_to_markdown.py" --input "$vtt_path")
    {
        echo "---"
        echo "type: call_transcript"
        echo "ticker: ${TICKER^^}"
        echo "empresa: $EMPRESA"
        echo "periodo: $period"
        echo "source_url: $url"
        echo "video_id: $vid"
        echo "captions: $captions"
        echo "fetched: $(date +%Y-%m-%d)"
        echo "---"
        echo ""
        echo "$body"
    } > "$out"
    echo "$out"
}

log_entry() {
    local kind="$1" period="$2" url="$3" note="$4"
    echo "[fetch-calls${kind}] $(date +%Y-%m-%d) | $EMPRESA | $period | $url | $note" >> "$LOG_FILE"
}

do_default() {
    local plan_path="$MANIFESTS_PATH/${EMPRESA}_calls_plan.json"
    if [[ ! -f "$plan_path" ]]; then
        echo "error: $plan_path not found. Run with --discover first." >&2
        exit 1
    fi
    local total=0 downloaded=0 skipped=0 errors=0
    while IFS=$'\t' read -r vid url period; do
        total=$((total + 1))
        echo "fetching $period ($vid)..."
        local vtt; vtt=$(download_captions "$url")
        if [[ -z "$vtt" ]]; then
            echo "  no captions — skipped"
            log_entry "-skip" "$period" "$url" "no_captions"
            skipped=$((skipped + 1))
            continue
        fi
        local saved
        if ! saved=$(save_transcript "$period" "$url" "$vid" "$CAPTION_KIND" "$vtt"); then
            echo "  conversion failed — skipped"
            log_entry "-error" "$period" "$url" "vtt_parse_failed"
            errors=$((errors + 1))
            continue
        fi
        echo "  saved: $saved ($CAPTION_KIND captions)"
        log_entry "" "$period" "$url" "$CAPTION_KIND"
        downloaded=$((downloaded + 1))
    done < <(jq -r '.entries[]
        | select(.confidence=="high" and .existing==false and .duplicate_of==null and .period != null)
        | [.video_id, .url, .period] | @tsv' "$plan_path")

    echo ""
    echo "summary: $downloaded downloaded, $skipped skipped, $errors errors (of $total candidates)"
}
```

Replace the dispatch:

```bash
if [[ -n "$FORCE_URL" ]]; then
    echo "TODO force_download (Task 6)"
elif [[ "$DISCOVER" == "true" ]]; then
    do_discover
else
    do_default
fi
```

- [ ] **Step 2: Run default mode on Direcional**

Run: `bash tools/fetch_calls.sh DIRR3`

Expected:
- Prints `fetching 4T24 ...  saved: ...` lines for each high-confidence, non-existing entry.
- Files land in `sources/undigested/direcional_call_transcript_*.md`.
- `log.md` gains `[fetch-calls]` entries for each success and `[fetch-calls-skip]` for any no-caption cases.
- Final line: `summary: N downloaded, M skipped, 0 errors (of N candidates)`.

- [ ] **Step 3: Spot-check one output file**

Run:
```bash
head -20 sources/undigested/direcional_call_transcript_4T24.md
```

Expected: YAML frontmatter with `type: call_transcript`, `ticker: DIRR3`, `periodo: 4T24`, `captions: manual` or `captions: auto`, `source_url: https://www.youtube.com/watch?v=...`; followed by `[00:00]` and clean paragraphs.

- [ ] **Step 4: Test idempotency**

Run: `bash tools/fetch_calls.sh DIRR3` again.

Expected: `summary: 0 downloaded, 0 skipped, 0 errors (of 0 candidates)` — because `existing=true` filters out everything now. **But wait**: idempotency depends on re-running `--discover` to refresh the plan. Document this by first re-running `--discover`:

```bash
bash tools/fetch_calls.sh DIRR3 --discover
bash tools/fetch_calls.sh DIRR3
```

Second command: `summary: 0 downloaded, ...`.

- [ ] **Step 5: Commit**

```bash
git add tools/fetch_calls.sh log.md
git commit -m "feat(fetch_calls): default mode — download captions, convert, save to undigested"
```

---

### Task 6: Implement `--url --period` force mode

**Files:**
- Modify: `tools/fetch_calls.sh` (replace the `TODO force_download` branch)

- [ ] **Step 1: Add the force handler**

Insert this helper alongside the others:

```bash
do_force() {
    local vid; vid=$(python3 -c "import sys,re; m=re.search(r'v=([\w-]+)', sys.argv[1]); print(m.group(1) if m else '')" "$FORCE_URL")
    if [[ -z "$vid" ]]; then
        echo "error: could not extract video_id from $FORCE_URL" >&2
        exit 1
    fi
    echo "fetching $FORCE_PERIOD ($vid) via --url..."
    local vtt; vtt=$(download_captions "$FORCE_URL")
    if [[ -z "$vtt" ]]; then
        echo "  no captions — aborting"
        log_entry "-skip" "$FORCE_PERIOD" "$FORCE_URL" "no_captions"
        exit 1
    fi
    local saved; saved=$(save_transcript "$FORCE_PERIOD" "$FORCE_URL" "$vid" "$CAPTION_KIND" "$vtt")
    echo "  saved: $saved ($CAPTION_KIND captions, forced)"
    log_entry "" "$FORCE_PERIOD" "$FORCE_URL" "${CAPTION_KIND}_forced"
}
```

Replace the dispatch:

```bash
if [[ -n "$FORCE_URL" ]]; then
    do_force
elif [[ "$DISCOVER" == "true" ]]; then
    do_discover
else
    do_default
fi
```

- [ ] **Step 2: Smoke-test force mode**

Pick any video from the medium bucket of `direcional_calls_plan.json` (or a known URL). Then run:

```bash
bash tools/fetch_calls.sh DIRR3 --url "https://www.youtube.com/watch?v=Vl_XJnZBFfE" --period 4T24
```

Expected: overwrites `sources/undigested/direcional_call_transcript_4T24.md`, prints `saved: ... (manual/auto captions, forced)`, appends a new `[fetch-calls]` line with `${KIND}_forced` note.

- [ ] **Step 3: Commit**

```bash
git add tools/fetch_calls.sh log.md
git commit -m "feat(fetch_calls): --url --period force mode for ambiguous videos"
```

---

### Task 7: Update CLAUDE.md with fetch_calls usage

**Files:**
- Modify: `CLAUDE.md` (add a new subsection under `## Commands`)

- [ ] **Step 1: Add the fetch_calls command block**

Find the `### Fetch filings from CVM` section in `CLAUDE.md`. Immediately after it (before `### Ingest files`), insert:

```markdown
### Fetch call transcripts from YouTube

```bash
# Discover mode — lists channel videos, scores by period regex, writes audit plan
bash tools/fetch_calls.sh DIRR3 --discover

# Normal mode — downloads high-confidence entries from the plan
bash tools/fetch_calls.sh DIRR3

# Force single video (for ambiguous titles)
bash tools/fetch_calls.sh DIRR3 --url https://www.youtube.com/watch?v=... --period 4T24
```

Requires `youtube_channel` in the empresa's manifest. Outputs `{empresa}_call_transcript_{periodo}.md` to `sources/undigested/` with YAML frontmatter and `[mm:ss]` anchors every ~60s.

Caption priority: manual `pt`/`pt-BR` → auto `pt`/`pt-BR` → skip with `[fetch-calls-skip]` log entry.
```

Also extend the `## Tools architecture` tree:
- Under `tools/` add `fetch_calls.sh            # orchestrator: YouTube channel → captions → sources/undigested/`
- Under `tools/lib/` add `vtt_to_markdown.py     # WebVTT → markdown with sparse [mm:ss] anchors`

Also extend the source type tokens bullet in the Non-obvious rules section to note `call_transcript` is produced by `fetch_calls.sh` (it's already listed — just confirm it stays).

- [ ] **Step 2: Verify rendering**

Run: `head -100 CLAUDE.md`
Expected: the new `### Fetch call transcripts from YouTube` section appears cleanly between fetch and ingest sections.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add fetch_calls.sh to CLAUDE.md commands and tool tree"
```

---

### Task 8: End-to-end validation on Direcional

This task is the final integration check. No new code.

- [ ] **Step 1: Clean state and rerun the full pipeline**

```bash
rm -f sources/manifests/direcional_calls_plan.json
rm -f sources/undigested/direcional_call_transcript_*.md
bash tools/fetch_calls.sh DIRR3 --discover
bash tools/fetch_calls.sh DIRR3
ls sources/undigested/direcional_call_transcript_*.md | wc -l
```

Expected: the count matches the high-confidence, non-existing entries in the plan. Typically 15–20 files covering 1T21–4T25 (minus any quarters that are missing from the channel or have no captions).

- [ ] **Step 2: Verify log.md entries**

Run:
```bash
grep -c '^\[fetch-calls\]' log.md
grep '^\[fetch-calls-skip\]' log.md | head
```

Expected: count matches downloaded files; skips (if any) are logged with a reason.

- [ ] **Step 3: Identify missing quarters and force-fetch them**

Run:
```bash
for q in 1T21 2T21 3T21 4T21 1T22 2T22 3T22 4T22 1T23 2T23 3T23 4T23 1T24 2T24 3T24 4T24 1T25 2T25 3T25 4T25; do
  [[ -f "sources/undigested/direcional_call_transcript_$q.md" ]] || echo "missing: $q"
done
```

For each missing quarter, check `direcional_calls_plan.json` for a matching medium-confidence entry. If found, run `fetch_calls.sh DIRR3 --url <url> --period <q>`. If not, log it as a genuine channel gap and move on.

- [ ] **Step 4: Final smoke check on one of the newer files**

Run:
```bash
wc -l sources/undigested/direcional_call_transcript_4T24.md
head -30 sources/undigested/direcional_call_transcript_4T24.md
```

Expected: several hundred lines; frontmatter intact; first paragraphs read like an earnings call opener.

- [ ] **Step 5: No commit needed for validation**

The validation is purely a check. If anything is broken, file it back into the relevant task. If everything works, the feature is done.

---

## Self-Review

**Spec coverage:**
- CLI shape, two-phase flow, manifest field, plan JSON → Tasks 1, 3, 4
- VTT→md converter with `[mm:ss]` anchors → Task 2
- Caption priority (manual → auto → skip) → Task 5 (`download_captions`)
- Frontmatter with `type/ticker/empresa/periodo/source_url/video_id/captions/fetched` → Task 5 (`save_transcript`)
- `log.md` entries (`[fetch-calls]`, `[fetch-calls-skip]`, `[fetch-calls-error]`) → Tasks 5, 6 (`log_entry`)
- Idempotency via `existing` check → Task 4 (`check_existing`), Task 5 (plan filter)
- Force mode `--url --period` → Task 6
- Error handling matrix (missing ticker / missing channel / missing plan / no captions) → Tasks 3, 4, 5
- Docs update → Task 7
- End-to-end validation → Task 8

**Placeholder scan:** Grep-clean — every task has complete code, no "TBD" / "add appropriate handling" / "similar to Task N".

**Type consistency:** Helper names are stable — `extract_period`, `score_confidence`, `check_existing`, `download_captions`, `save_transcript`, `log_entry`, `do_discover`, `do_default`, `do_force`. Globals (`EMPRESA`, `YOUTUBE_CHANNEL`, `CAPTION_KIND`) are declared once and reused consistently.

**One gap found and fixed inline:** Task 5 Step 4 originally assumed single-run idempotency, but the plan file caches `existing=false` at discover time. Added explicit re-run of `--discover` to refresh before the idempotency check.
