#!/usr/bin/env python
"""
Merge multiple wiki_plan JSON files (one per chunk) into a single plan.

Usage:
    python merge_wiki_plans.py chunk_001.json chunk_002.json ... > merged.json

Conflict resolution:
- create + create (same page across chunks): union digesteds, keep first type
- update + update (same page): union digesteds, keep first type
- create + update (same page): prefer CREATE; merge digesteds into create
- skip + (create|update): drop skip
- skip + skip: keep first reason
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: merge_wiki_plans.py <chunk1.json> [chunk2.json ...]\n")
        sys.exit(1)

    merged = {"create": {}, "update": {}, "skip": {}}

    for path in sys.argv[1:]:
        try:
            plan = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as e:
            sys.stderr.write(f"WARN: skipping {path}: {e}\n")
            continue

        for item in plan.get("create", []) or []:
            page = item.get("page")
            if not page:
                continue
            if page not in merged["create"]:
                merged["create"][page] = {
                    "page": page,
                    "type": item.get("type", "unknown"),
                    "digesteds": set(),
                }
            merged["create"][page]["digesteds"].update(item.get("digesteds", []) or [])

        for item in plan.get("update", []) or []:
            page = item.get("page")
            if not page:
                continue
            if page not in merged["update"]:
                merged["update"][page] = {
                    "page": page,
                    "type": item.get("type", "unknown"),
                    "digesteds": set(),
                }
            merged["update"][page]["digesteds"].update(item.get("digesteds", []) or [])

        for item in plan.get("skip", []) or []:
            page = item.get("page")
            if not page:
                continue
            if page not in merged["skip"]:
                merged["skip"][page] = {
                    "page": page,
                    "reason": item.get("reason", ""),
                }

    # Conflict resolution
    # 1. Drop skip if same page is also in update or create
    for page in list(merged["skip"].keys()):
        if page in merged["update"] or page in merged["create"]:
            del merged["skip"][page]

    # 2. If page is in both create and update, prefer create (new page); merge digesteds
    for page in list(merged["update"].keys()):
        if page in merged["create"]:
            merged["create"][page]["digesteds"].update(
                merged["update"][page]["digesteds"]
            )
            del merged["update"][page]

    out = {
        "create": [
            {
                "page": v["page"],
                "type": v["type"],
                "digesteds": sorted(v["digesteds"]),
            }
            for v in merged["create"].values()
        ],
        "update": [
            {
                "page": v["page"],
                "type": v["type"],
                "digesteds": sorted(v["digesteds"]),
            }
            for v in merged["update"].values()
        ],
        "skip": [
            {"page": v["page"], "reason": v["reason"]}
            for v in merged["skip"].values()
        ],
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
