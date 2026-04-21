#!/usr/bin/env python
"""
Append a chunk-failure record to the failures log.

Usage:
    cat <chunk_output> | python record_chunk_failure.py <log_path> <chunk_idx> <reason> <chunk_input_file>

Reads the chunk_input_file (the per-chunk text file with the digest list) to capture
which digests were in the failed chunk. Reads the chunk's raw output (e.g. claude
stdout/stderr) from stdin and stores up to 4KB of its tail for diagnosis.

Failures log is a JSON array; this appends one record. File is created if missing.
"""

import json
import os
import sys
from datetime import datetime


def main():
    if len(sys.argv) != 5:
        sys.stderr.write(
            "usage: record_chunk_failure.py <log_path> <chunk_idx> <reason> <chunk_input_file>\n"
        )
        sys.exit(2)

    log_path, chunk_idx, reason, chunk_input_file = sys.argv[1:5]

    digesteds = []
    if os.path.exists(chunk_input_file):
        with open(chunk_input_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("-"):
                    digesteds.append(line.lstrip("- ").strip())

    output_tail = ""
    try:
        if not sys.stdin.isatty():
            data = sys.stdin.read()
            if data:
                output_tail = data[-4000:]
    except Exception:
        pass

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "chunk_idx": int(chunk_idx),
        "reason": reason,
        "digesteds_count": len(digesteds),
        "digesteds": digesteds,
        "output_tail": output_tail,
    }

    failures = []
    if os.path.exists(log_path):
        try:
            with open(log_path, encoding="utf-8") as f:
                failures = json.load(f)
            if not isinstance(failures, list):
                failures = []
        except Exception:
            failures = []

    failures.append(record)

    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(failures, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
