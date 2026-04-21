#!/usr/bin/env bash
# Overnight orchestrator for the full Notion Capstone backfill.
#
# Workflow:
#   1. Fetch every remaining page from Notion Capstone into sources/undigested/
#      (state file already tracks what's processed — only NEW/EDITED pages show up)
#   2. Ingest loop: run batch_notion_run.sh; if anything fails and stays in
#      undigested/, sleep 1h and retry. Max 24 iterations (= ~24h).
#   3. If all ingests succeed, run wiki_update.sh --full to consolidate.
#
# Designed to survive:
#   - Anthropic rate limits (sleep 1h, retry)
#   - Transient API "overloaded" errors (per-file failure doesn't halt batch)
#   - Interruption (save_state is now atomic; next run picks up where it left)
#
# Run in background:
#   bash docs/handoff/overnight_notion.sh > docs/handoff/overnight.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../.."

STAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "===== overnight_notion.sh start $STAMP ====="

# ---------- Step 1: fetch all remaining ----------
echo ""
echo "===== [step 1] Fetch all remaining Notion pages ====="
bash tools/fetch_notion.sh
FETCH_RC=$?
if [[ $FETCH_RC -ne 0 ]]; then
    echo "WARN: fetch_notion.sh exited $FETCH_RC. Continuing with whatever is in undigested/."
fi

INITIAL_COUNT=$(ls sources/undigested/notion_*.md 2>/dev/null | wc -l)
echo "Initial undigested count: $INITIAL_COUNT"

if [[ $INITIAL_COUNT -eq 0 ]]; then
    echo "Nothing to ingest. Jumping straight to wiki_update --full."
fi

# ---------- Step 2: ingest loop with retry ----------
# - MAX_ITERS * SLEEP = 6 * 4h = 24h total retry window
# - batch_notion_run.sh signals:
#     exit 42 = auth break (credential expired) — abort loop immediately,
#               no point sleeping for hours on a broken credential
#     exit 43 = systemic fast-failure streak (network/quota) — same treatment
MAX_ITERS=6
SLEEP_ON_FAIL=14400   # 4 hours
remaining=$INITIAL_COUNT

for i in $(seq 1 $MAX_ITERS); do
    if [[ $remaining -eq 0 ]]; then
        break
    fi

    echo ""
    echo "===== [step 2.$i/$MAX_ITERS] Ingest batch — $remaining file(s) to go ====="
    date

    bash docs/handoff/batch_notion_run.sh
    batch_rc=$?

    if [[ $batch_rc -eq 42 ]]; then
        echo ""
        echo "!!! Overnight aborting: auth break (credential expired)."
        echo "    Refresh Claude Code credentials and rerun overnight_notion.sh."
        exit 42
    fi
    if [[ $batch_rc -eq 43 ]]; then
        echo ""
        echo "!!! Overnight aborting: systemic fast-failure streak."
        echo "    Inspect batch output, diagnose, and rerun overnight_notion.sh."
        exit 43
    fi

    remaining=$(ls sources/undigested/notion_*.md 2>/dev/null | wc -l)
    echo "After iteration $i: $remaining file(s) still in undigested/"

    if [[ $remaining -gt 0 && $i -lt $MAX_ITERS ]]; then
        echo "Sleeping ${SLEEP_ON_FAIL}s before retry (suspected rate-limit / overload)..."
        sleep $SLEEP_ON_FAIL
    fi
done

# ---------- Step 3: wiki_update --full if clean ----------
echo ""
if [[ $remaining -eq 0 ]]; then
    echo "===== [step 3] All ingested. Running wiki_update.sh --full ====="
    date
    bash tools/wiki_update.sh --full
    WU_RC=$?
    echo ""
    if [[ $WU_RC -eq 0 ]]; then
        echo "===== overnight_notion.sh DONE (all green) at $(date +"%Y-%m-%d %H:%M:%S") ====="
    else
        echo "===== overnight_notion.sh: wiki_update.sh exited $WU_RC ====="
        exit $WU_RC
    fi
else
    echo "===== overnight_notion.sh GAVE UP — $remaining file(s) unprocessed after $MAX_ITERS iterations ====="
    echo "Listing remaining for manual retry:"
    ls sources/undigested/notion_*.md
    echo ""
    echo "NOT running wiki_update.sh --full (partial ingest)."
    echo "Retry manually with: bash docs/handoff/overnight_notion.sh"
    exit 1
fi
