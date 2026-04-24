#!/usr/bin/env bash
# Watchlist runner — wraps tools/lib/watch_runner.py
#
# Usage:
#   bash tools/watch.sh                       # respect cadence
#   bash tools/watch.sh --force               # ignore cadence
#   bash tools/watch.sh --page reforma_tributaria.md
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
exec python "$REPO_ROOT/tools/lib/watch_runner.py" "$@"
