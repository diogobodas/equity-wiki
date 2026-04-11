#!/usr/bin/env bash
# parallel.sh — run N commands concurrently, wait for all, collect exit codes.
#
# Usage:
#   source tools/lib/parallel.sh
#   parallel_init 4                    # max 4 concurrent jobs
#   parallel_add "command1 arg1 arg2"
#   parallel_add "command2 arg1 arg2"
#   ...
#   parallel_wait                      # blocks until all done, returns worst exit code

_PAR_MAX=4
_PAR_PIDS=()
_PAR_CMDS=()
_PAR_WORST=0

parallel_init() {
    _PAR_MAX="${1:-4}"
    _PAR_PIDS=()
    _PAR_CMDS=()
    _PAR_WORST=0
}

parallel_add() {
    local cmd="$1"
    # If at capacity, wait for one slot to free up
    while (( ${#_PAR_PIDS[@]} >= _PAR_MAX )); do
        _par_wait_one
    done
    eval "$cmd" &
    _PAR_PIDS+=($!)
    _PAR_CMDS+=("$cmd")
}

_par_wait_one() {
    # Wait for any one child to finish
    wait -n 2>/dev/null || true
    # Reap finished PIDs
    local new_pids=()
    local new_cmds=()
    for i in "${!_PAR_PIDS[@]}"; do
        if kill -0 "${_PAR_PIDS[$i]}" 2>/dev/null; then
            new_pids+=("${_PAR_PIDS[$i]}")
            new_cmds+=("${_PAR_CMDS[$i]}")
        else
            wait "${_PAR_PIDS[$i]}" 2>/dev/null
            local rc=$?
            (( rc > _PAR_WORST )) && _PAR_WORST=$rc
        fi
    done
    _PAR_PIDS=("${new_pids[@]}")
    _PAR_CMDS=("${new_cmds[@]}")
}

parallel_wait() {
    for i in "${!_PAR_PIDS[@]}"; do
        wait "${_PAR_PIDS[$i]}" 2>/dev/null
        local rc=$?
        (( rc > _PAR_WORST )) && _PAR_WORST=$rc
    done
    _PAR_PIDS=()
    _PAR_CMDS=()
    return $_PAR_WORST
}
