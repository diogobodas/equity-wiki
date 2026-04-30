#!/usr/bin/env bash
# bbg.sh — Bloomberg orchestrator. Thin wrapper over tools/lib/bbg.py with
# log entries and standard composed actions.
#
# Usage:
#   bash tools/bbg.sh <empresa|ticker> --snapshot              # px + multiplos + consenso (default)
#   bash tools/bbg.sh <empresa|ticker> --consensus 1FY,2FY     # estimativas BEst para periodos
#   bash tools/bbg.sh <empresa|ticker> --history --since=2024-01-01 [--field=PX_LAST]
#   bash tools/bbg.sh <empresa|ticker> --full                  # snapshot + consensus 1FY+2FY + px history
#   bash tools/bbg.sh <empresa|ticker> --refresh               # forca refresh do cache
#
# Notes:
#   - Cache em sources/bbg/{empresa}/, citavel via `(fonte: bbg/{empresa}/snapshot.csv, em: YYYY-MM-DD)`
#   - Log entry [bbg-fetch] em log.md
#   - Para queries livres, use diretamente: python tools/lib/bbg.py raw '{...}'

set -euo pipefail

usage() {
    grep '^# ' "$0" | sed 's/^# \?//'
    exit 1
}

[[ $# -lt 1 ]] && usage
[[ "$1" == "-h" || "$1" == "--help" ]] && usage

EMPRESA="$1"
shift

MODE="snapshot"
PERIOD_LIST="1FY"
SINCE="2024-01-01"
UNTIL=""
FIELD="PX_LAST"
REFRESH=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --snapshot)   MODE="snapshot"; shift ;;
        --consensus)  MODE="consensus"; PERIOD_LIST="${2:-1FY}"; shift 2 ;;
        --history)    MODE="history"; shift ;;
        --full)       MODE="full"; shift ;;
        --since=*)    SINCE="${1#*=}"; shift ;;
        --until=*)    UNTIL="${1#*=}"; shift ;;
        --field=*)    FIELD="${1#*=}"; shift ;;
        --refresh)    REFRESH="--refresh"; shift ;;
        *)            echo "Opcao desconhecida: $1" >&2; usage ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PY="python $SCRIPT_DIR/lib/bbg.py"

EMPRESA_SLUG=$($PY resolve "$EMPRESA" 2>/dev/null | awk -F': ' '/^empresa:/{print $2}')
BBG_TICKER=$($PY resolve "$EMPRESA" 2>/dev/null | awk -F': ' '/^bbg_ticker:/{print $2}')

if [[ -z "$EMPRESA_SLUG" ]]; then
    echo "ERRO: nao consegui resolver empresa/ticker '$EMPRESA' — verifique manifest ou conexao com share" >&2
    exit 2
fi

echo "=== BBG ==="
echo "empresa: $EMPRESA_SLUG"
echo "bbg_ticker: $BBG_TICKER"
echo "mode: $MODE"
echo ""

run_snapshot() {
    $PY snapshot "$EMPRESA_SLUG" $REFRESH
}

run_consensus() {
    local periods="$1"
    IFS=',' read -ra arr <<<"$periods"
    for p in "${arr[@]}"; do
        $PY consensus "$EMPRESA_SLUG" --period "$p" $REFRESH
        echo ""
    done
}

run_history() {
    local args=(history "$EMPRESA_SLUG" --since "$SINCE" --field "$FIELD")
    [[ -n "$UNTIL" ]] && args+=(--until "$UNTIL")
    [[ -n "$REFRESH" ]] && args+=($REFRESH)
    $PY "${args[@]}"
}

LOG_TODAY=$(date +%Y-%m-%d)

case "$MODE" in
    snapshot)   run_snapshot ;;
    consensus)  run_consensus "$PERIOD_LIST" ;;
    history)    run_history ;;
    full)
        run_snapshot
        echo ""
        run_consensus "1FY,2FY"
        echo ""
        run_history
        ;;
esac

echo "[bbg-fetch] $LOG_TODAY | $EMPRESA_SLUG ($BBG_TICKER) | mode=$MODE | sources/bbg/$EMPRESA_SLUG/" >> "$REPO_ROOT/log.md"

echo ""
echo "=== Done ==="
echo "  Cache: sources/bbg/$EMPRESA_SLUG/"
echo "  Citacao: (fonte: bbg/$EMPRESA_SLUG/<arquivo>.csv, em: $LOG_TODAY)"
