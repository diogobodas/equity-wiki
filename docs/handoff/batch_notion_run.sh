#!/usr/bin/env bash
# Batch-run ingest.sh --notion over every file currently in sources/undigested/.
# Sequentially (shared-state files preclude parallelism without refactor).
# Captures per-file Guard stats + total wall time. Summary at the end.
#
# Exit codes:
#   0  - batch completed (per-file failures are logged, not fatal)
#   42 - auth break detected (HTTP 401 / authentication_error) — aborted early
#        so the outer overnight loop can stop retrying instead of burning 1h
#        sleeps on a credential that will stay expired until human refresh.
#   43 - two consecutive immediate failures (< 15s each) with no progress —
#        suggests systemic failure (auth, quota, network) rather than per-file
#        transient errors that take full LLM time to fail.
set -uo pipefail
cd "$(dirname "$0")/../.."

SUMMARY=$(mktemp)
START_TS=$(date +%s)
N=0
OK=0
FAIL=0
CONSEC_FAST_FAILS=0
EXIT=0

for f in sources/undigested/notion_*.md; do
    [[ -f "$f" ]] || continue
    N=$((N+1))
    name=$(basename "$f")
    echo "=== [$N] $name ==="
    t0=$(date +%s)
    log=$(bash tools/ingest.sh --notion "$f" 2>&1)
    rc=$?
    t1=$(date +%s)
    dur=$((t1 - t0))
    guard=$(echo "$log" | grep -E "^Guard:" | head -1)

    if [[ $rc -eq 0 ]]; then
        OK=$((OK+1))
        CONSEC_FAST_FAILS=0
        printf "%-70s | %3ds | %s\n" "$name" "$dur" "$guard" >> "$SUMMARY"
        echo "  OK (${dur}s) | $guard"
        echo ""
        continue
    fi

    # Failure — classify.
    FAIL=$((FAIL+1))
    printf "%-70s | %3ds | FAILED: rc=%d\n" "$name" "$dur" "$rc" >> "$SUMMARY"
    echo "  FAILED rc=$rc (${dur}s)"
    echo "--- last 15 lines of output ---"
    echo "$log" | tail -15
    echo "-------------------------------"
    echo ""

    # Auth break: HTTP 401 / authentication_error from Anthropic API.
    # No point retrying — credential must be refreshed by a human.
    if echo "$log" | grep -q -E "401|authentication_error|Invalid authentication credentials"; then
        echo "!!! AUTH BREAK detected — aborting batch (exit 42)."
        echo "    Refresh Claude Code credentials (claude /login or equivalent)"
        echo "    then rerun overnight_notion.sh to resume."
        EXIT=42
        break
    fi

    # Fast-fail streak — two consecutive failures under 15s suggests systemic
    # issue, not a per-file transient LLM timeout.
    if [[ $dur -lt 15 ]]; then
        CONSEC_FAST_FAILS=$((CONSEC_FAST_FAILS+1))
        if [[ $CONSEC_FAST_FAILS -ge 2 ]]; then
            echo "!!! Two consecutive fast failures (<15s) — likely systemic."
            echo "    Aborting batch (exit 43). Inspect logs, fix, and rerun."
            EXIT=43
            break
        fi
    else
        CONSEC_FAST_FAILS=0
    fi
done

END_TS=$(date +%s)
TOTAL=$((END_TS - START_TS))
echo ""
echo "==================================================================="
echo "BATCH SUMMARY: processed=$N  ok=$OK  failed=$FAIL  total_wall=${TOTAL}s  exit=$EXIT"
echo "==================================================================="
cat "$SUMMARY"
rm -f "$SUMMARY"
exit $EXIT
