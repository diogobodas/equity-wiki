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

# --- Helpers ---

# Compute horizon cutoff as YYYYMMDD (for comparing with yt-dlp upload_date).
compute_horizon_cutoff() {
    local h="$1"
    local num="${h%y}"
    local year month day
    year=$(date +%Y); month=$(date +%m); day=$(date +%d)
    printf "%04d%02d%02d" $((year - num)) "$((10#$month))" "$((10#$day))"
}

do_discover() {
    local cutoff; cutoff=$(compute_horizon_cutoff "$HORIZON")
    local plan_path="$MANIFESTS_PATH/${EMPRESA}_calls_plan.json"
    echo "listing $YOUTUBE_CHANNEL/videos (cutoff: $cutoff)..."

    local raw="$TMP_DIR/channel_list.tsv"
    : > "$raw"
    for tab in videos streams; do
        yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(upload_date)s" \
            "$YOUTUBE_CHANNEL/$tab" >> "$raw" 2>/dev/null || true
    done

    EMPRESA="$EMPRESA" \
    TICKER_UPPER="${TICKER^^}" \
    YOUTUBE_CHANNEL="$YOUTUBE_CHANNEL" \
    HORIZON="$HORIZON" \
    CUTOFF="$cutoff" \
    UNDIGESTED_PATH="$UNDIGESTED_PATH" \
    FULL_PATH="$FULL_PATH" \
    RAW_PATH="$raw" \
    PLAN_PATH="$plan_path" \
    python "$SCRIPT_DIR/lib/calls_plan.py"

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

# Download captions for a single URL. Sets globals VTT_PATH and CAPTION_KIND.
# VTT_PATH is empty on skip.
download_captions() {
    local url="$1"
    VTT_PATH=""
    CAPTION_KIND=""
    local vid
    vid=$(python -c "import sys,re; m=re.search(r'v=([\w-]+)', sys.argv[1]); print(m.group(1) if m else '')" "$url")
    [[ -z "$vid" ]] && return
    local out_dir="$TMP_DIR/captions"
    mkdir -p "$out_dir"

    yt-dlp --write-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt \
        -o "$out_dir/%(id)s.%(ext)s" "$url" >/dev/null 2>&1 || true
    local vtt
    vtt=$(ls "$out_dir"/"$vid".pt*.vtt 2>/dev/null | head -1 || true)
    if [[ -n "$vtt" ]]; then VTT_PATH="$vtt"; CAPTION_KIND="manual"; return; fi

    yt-dlp --write-auto-subs --sub-langs "pt,pt-BR" --skip-download --sub-format vtt \
        -o "$out_dir/%(id)s.%(ext)s" "$url" >/dev/null 2>&1 || true
    vtt=$(ls "$out_dir"/"$vid".pt*.vtt 2>/dev/null | head -1 || true)
    if [[ -n "$vtt" ]]; then VTT_PATH="$vtt"; CAPTION_KIND="auto"; return; fi
}

# Write a transcript file with frontmatter.
save_transcript() {
    local period="$1" url="$2" vid="$3" captions="$4" vtt_path="$5"
    local out="$UNDIGESTED_PATH/${EMPRESA}_call_transcript_${period}.md"
    local body_path="$TMP_DIR/${vid}.body.md"
    python "$SCRIPT_DIR/lib/vtt_to_markdown.py" --input "$vtt_path" > "$body_path"
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
        cat "$body_path"
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
        download_captions "$url"
        if [[ -z "$VTT_PATH" ]]; then
            echo "  no captions — skipped"
            log_entry "-skip" "$period" "$url" "no_captions"
            skipped=$((skipped + 1))
            continue
        fi
        local saved
        if ! saved=$(save_transcript "$period" "$url" "$vid" "$CAPTION_KIND" "$VTT_PATH"); then
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

do_force() {
    local vid
    vid=$(python -c "import sys,re; m=re.search(r'v=([\w-]+)', sys.argv[1]); print(m.group(1) if m else '')" "$FORCE_URL")
    if [[ -z "$vid" ]]; then
        echo "error: could not extract video_id from $FORCE_URL" >&2
        exit 1
    fi
    echo "fetching $FORCE_PERIOD ($vid) via --url..."
    download_captions "$FORCE_URL"
    if [[ -z "$VTT_PATH" ]]; then
        echo "  no captions — aborting"
        log_entry "-skip" "$FORCE_PERIOD" "$FORCE_URL" "no_captions"
        exit 1
    fi
    local saved; saved=$(save_transcript "$FORCE_PERIOD" "$FORCE_URL" "$vid" "$CAPTION_KIND" "$VTT_PATH")
    echo "  saved: $saved ($CAPTION_KIND captions, forced)"
    log_entry "" "$FORCE_PERIOD" "$FORCE_URL" "${CAPTION_KIND}_forced"
}

# --- Dispatch ---
if [[ -n "$FORCE_URL" ]]; then
    do_force
elif [[ "$DISCOVER" == "true" ]]; then
    do_discover
else
    do_default
fi
