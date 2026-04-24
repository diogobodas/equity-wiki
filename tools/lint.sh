#!/usr/bin/env bash
# Dated-claim lint — wraps tools/lib/dated_lint.py
#
# Usage:
#   bash tools/lint.sh                      # full report, all severities
#   bash tools/lint.sh --severity action    # only action
#   bash tools/lint.sh --page cyrela.md     # single page
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
exec python "$REPO_ROOT/tools/lib/dated_lint.py" "$@"
