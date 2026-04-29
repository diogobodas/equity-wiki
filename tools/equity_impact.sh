#!/usr/bin/env bash
# Equity Impact Briefing — cruza morning-briefing emails + relatório CVM diário com a cobertura.
# Output read-only: briefings/<YYYY-MM-DD>-impact.md
#
# Usage:
#   bash tools/equity_impact.sh                    # briefing do dia, todas as empresas
#   bash tools/equity_impact.sh --ticker WEGE3     # foco em uma empresa
#   bash tools/equity_impact.sh --debug            # stderr verbose
#   bash tools/equity_impact.sh --no-llm           # JSON context apenas (dry-run)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec env PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python "$SCRIPT_DIR/lib/equity_impact.py" "$@"
