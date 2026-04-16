#!/usr/bin/env python3
"""
Wiki queue helper — pending ingests awaiting wiki_update.sh consumption.

The queue lives at sources/wiki_queue.json as an array of entries. Each entry
has: empresa, type, periodo, digested, queued_on.

Commands:
    enqueue --empresa <x> --type <t> --periodo <p> --digested <path>
    drain                # print pending entries as JSON to stdout
    clear                # empty the queue (called after successful consumption)
    peek [--count]       # count or list pending entries
    migrate-from-log     # one-time: read [wiki-queue] lines from log.md after
                         # last [wiki-done], populate queue.json. Idempotent.

Design notes:
- atomic writes via temp file + replace
- dedupe by (empresa, type, periodo, digested) — enqueue is idempotent
- log.md keeps [ingest] audit entries but is no longer the source of truth
  for pending items

Exit codes: 0 = ok, 2 = invalid args, 3 = I/O error
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QUEUE_PATH = REPO_ROOT / "sources" / "wiki_queue.json"
LOG_PATH = REPO_ROOT / "log.md"


def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    try:
        return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: queue file corrupt: {e}", file=sys.stderr)
        sys.exit(3)


def save_queue(entries: list[dict]) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    # atomic write
    fd, tmp = tempfile.mkstemp(dir=QUEUE_PATH.parent, prefix=".queue_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, QUEUE_PATH)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def entry_key(e: dict) -> tuple:
    return (e.get("empresa"), e.get("type"), e.get("periodo"), e.get("digested"))


def cmd_enqueue(args) -> int:
    entries = load_queue()
    new_entry = {
        "empresa": args.empresa,
        "type": args.type,
        "periodo": args.periodo,
        "digested": args.digested,
        "queued_on": args.queued_on or dt.date.today().isoformat(),
    }
    key = entry_key(new_entry)
    for e in entries:
        if entry_key(e) == key:
            print(f"already queued: {key}", file=sys.stderr)
            return 0
    entries.append(new_entry)
    save_queue(entries)
    print(f"queued: {args.empresa} | {args.type} | {args.periodo}")
    return 0


def cmd_drain(_args) -> int:
    entries = load_queue()
    print(json.dumps(entries, indent=2, ensure_ascii=False))
    return 0


def cmd_clear(_args) -> int:
    save_queue([])
    print("queue cleared")
    return 0


def cmd_peek(args) -> int:
    entries = load_queue()
    if args.count:
        print(len(entries))
    else:
        for e in entries:
            print(
                f"- {e.get('empresa','?')} | {e.get('type','?')} | "
                f"{e.get('periodo','?')} | {e.get('digested','?')}"
            )
    return 0


# ---------- migration from legacy log.md markers ----------

_QUEUE_LINE_RE = re.compile(
    r"^\[wiki-queue\] (?P<date>\d{4}-\d{2}-\d{2}) \| (?P<empresa>[^|]+) \| "
    r"(?P<type>[^|]+) \| (?P<periodo>[^|]+) \| (?P<digested>.+)$"
)


def cmd_migrate(_args) -> int:
    if not LOG_PATH.exists():
        print("no log.md to migrate")
        return 0
    lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    # find last [wiki-done] line — everything after it is pending
    last_done_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("[wiki-done]"):
            last_done_idx = i
    pending_lines = lines[last_done_idx + 1 :]
    existing = load_queue()
    existing_keys = {entry_key(e) for e in existing}
    added = 0
    for line in pending_lines:
        m = _QUEUE_LINE_RE.match(line.strip())
        if not m:
            continue
        entry = {
            "empresa": m.group("empresa").strip(),
            "type": m.group("type").strip(),
            "periodo": m.group("periodo").strip(),
            "digested": m.group("digested").strip(),
            "queued_on": m.group("date"),
        }
        if entry_key(entry) in existing_keys:
            continue
        existing.append(entry)
        existing_keys.add(entry_key(entry))
        added += 1
    save_queue(existing)
    print(f"migrated {added} pending entries from log.md (total queue size: {len(existing)})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="wiki_queue — pending wiki updates")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_enq = sub.add_parser("enqueue", help="add an entry")
    p_enq.add_argument("--empresa", required=True)
    p_enq.add_argument("--type", required=True)
    p_enq.add_argument("--periodo", required=True)
    p_enq.add_argument("--digested", required=True)
    p_enq.add_argument("--queued-on", dest="queued_on", help="ISO date; defaults to today")
    p_enq.set_defaults(func=cmd_enqueue)

    p_drain = sub.add_parser("drain", help="print pending entries as JSON")
    p_drain.set_defaults(func=cmd_drain)

    p_clear = sub.add_parser("clear", help="empty queue")
    p_clear.set_defaults(func=cmd_clear)

    p_peek = sub.add_parser("peek", help="list or count pending entries")
    p_peek.add_argument("--count", action="store_true", help="print count only")
    p_peek.set_defaults(func=cmd_peek)

    p_mig = sub.add_parser(
        "migrate-from-log",
        help="one-time: import pending [wiki-queue] lines from log.md",
    )
    p_mig.set_defaults(func=cmd_migrate)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
