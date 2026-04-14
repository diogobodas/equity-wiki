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
