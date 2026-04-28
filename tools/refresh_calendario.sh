#!/usr/bin/env bash
# Refresh calendario_resultados.md from CVM IPE_9 (Calendário de Eventos Corporativos).
# See tools/lib/calendario_refresh.py for the parser/updater logic.
#
# Usage:
#   bash tools/refresh_calendario.sh                 # dry-run JSON report
#   bash tools/refresh_calendario.sh --apply         # write changes to wiki page
#   bash tools/refresh_calendario.sh --ticker WEGE3  # single ticker (debug)
#   bash tools/refresh_calendario.sh -v --apply      # verbose progress + write
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec env PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python "$SCRIPT_DIR/lib/calendario_refresh.py" "$@"
