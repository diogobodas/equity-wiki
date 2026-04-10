#!/usr/bin/env python3
"""Deterministic manifest/log/index updates for the ingest pipeline. No LLM."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Update manifest, log, and index after ingest")
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON")
    parser.add_argument("--type", required=True, choices=["itr", "dfp", "release", "fato_relevante"],
                        help="Document type")
    parser.add_argument("--period", required=True, help="Period code (e.g. 3T25, 2025)")
    parser.add_argument("--full", required=True, help="Path to full/ file produced")
    parser.add_argument("--structured", default=None, help="Path to structured/ file (heavy path only)")
    parser.add_argument("--digested", default=None, help="Path to digested/ file")
    parser.add_argument("--log", default="log.md", help="Path to log file")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(json.dumps({"status": "error", "message": f"Manifest not found: {manifest_path}"}))
        sys.exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    today = date.today().isoformat()

    # Build source entry
    source_entry = {
        "type": args.type,
        "asof": args.period,
        "ingested_on": today,
        "full": args.full,
    }
    if args.structured:
        source_entry["structured"] = [args.structured]
    if args.digested:
        source_entry["digested"] = args.digested

    # Add to sources (avoid duplicates by type+asof+full)
    existing = [s for s in manifest.get("sources", [])
                if s.get("type") == args.type and s.get("asof") == args.period and s.get("full") == args.full]
    if not existing:
        manifest.setdefault("sources", []).append(source_entry)

    # Update coverage for heavy path
    if args.type in ("itr", "dfp") and args.structured:
        coverage = manifest.setdefault("coverage", {}).setdefault(args.period, {})
        for block in ("dre", "bp"):
            coverage[block] = {"status": "filled", "source": args.structured}

    if args.type == "release" and args.structured:
        coverage = manifest.setdefault("coverage", {}).setdefault(args.period, {})
        coverage["financeiro_ajustado"] = {"status": "filled", "source": args.structured}

    # Update timestamp
    manifest["_updated"] = today

    # Write manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write('\n')

    # Append to log
    log_path = Path(args.log)
    log_line = f"{today} — ingest {args.type} {args.period}: {args.full}"
    if args.structured:
        log_line += f", {args.structured}"
    if args.digested:
        log_line += f", {args.digested}"
    log_line += "\n"

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_line)

    print(json.dumps({
        "status": "ok",
        "manifest": str(manifest_path),
        "type": args.type,
        "period": args.period,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
