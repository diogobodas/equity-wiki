#!/usr/bin/env python3
"""
Rebuild manifest coverage + sources[] for one empresa by scanning disk.

Preserves top-level metadata (empresa, display_name, aliases, ticker, setor,
setor_schema, wiki_page, fetch_profile, precedence, caveats, related_digests,
youtube_channel). Rebuilds:
  - coverage: canonical modeling keys per period
  - sources[]: flat registry of ingested source files

Usage:
    python tools/lib/manifest_rebuild.py --empresa cyrela [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STRUCTURED_ROOT = REPO_ROOT / "sources" / "structured"
FULL_ROOT = REPO_ROOT / "sources" / "full"
DIGESTED_ROOT = REPO_ROOT / "sources" / "digested"
MANIFESTS_ROOT = REPO_ROOT / "sources" / "manifests"

# canonical coverage keys we track per period
CANONICAL_KEYS = ("bp", "dre", "operacional", "financeiro_ajustado")

# doc-type precedence: first existing wins for each canonical key
COVERAGE_PRECEDENCE = {
    "bp": ("itr", "release", "dfp"),
    "dre": ("itr", "release", "dfp"),
    "operacional": ("release", "dfp", "itr"),
    "financeiro_ajustado": ("release", "dfp", "itr"),
}


def as_rel(p: Path) -> str:
    return p.relative_to(REPO_ROOT).as_posix()


def scan_structured(empresa: str) -> dict[str, dict[str, Path]]:
    """Return {periodo: {doc_type: path_to_json}} from sources/structured/<empresa>/."""
    base = STRUCTURED_ROOT / empresa
    out: dict[str, dict[str, Path]] = {}
    if not base.exists():
        return out
    for period_dir in sorted(base.iterdir()):
        if not period_dir.is_dir():
            continue
        for f in sorted(period_dir.glob("*.json")):
            doc_type = f.stem  # itr, release, dfp
            out.setdefault(period_dir.name, {})[doc_type] = f
    return out


def scan_full(empresa: str) -> dict[str, list[Path]]:
    """Return {periodo: [paths]} from sources/full/<empresa>/."""
    base = FULL_ROOT / empresa
    out: dict[str, list[Path]] = {}
    if not base.exists():
        return out
    for period_dir in sorted(base.iterdir()):
        if not period_dir.is_dir():
            continue
        paths = sorted(period_dir.glob("*.md"))
        if paths:
            out[period_dir.name] = paths
    return out


def scan_digested(empresa: str) -> list[Path]:
    return sorted(DIGESTED_ROOT.glob(f"{empresa}_*.md"))


def infer_doc_type_from_full(fname: str) -> str:
    """Map a full/*.md filename stem to a doc_type token."""
    stem = Path(fname).stem
    if stem.startswith("fato_relevante"):
        return "fato_relevante"
    if stem.startswith("rca_"):
        return "rca"
    if stem == "previa_operacional":
        return "previa_operacional"
    if stem == "call_transcript":
        return "call_transcript"
    if stem == "itr":
        return "itr"
    if stem == "release":
        return "release"
    if stem == "dfp":
        return "dfp"
    if stem == "notas_explicativas":
        return "notas_explicativas"
    return stem  # fallback — use stem as type


def find_digested_for(
    empresa: str, doc_type: str, periodo: str, digesteds: list[Path]
) -> Path | None:
    """Best-effort match: {empresa}_{doc_type}_{periodo}_summary.md."""
    candidates = [
        f"{empresa}_{doc_type}_{periodo}_summary.md",
        # DFP uses year; doc_type may be 'dfp'
        f"{empresa}_{doc_type}_{periodo.lstrip('4T')}_summary.md"
        if doc_type == "dfp" and periodo.startswith("4T")
        else None,
    ]
    candidates = [c for c in candidates if c]
    for d in digesteds:
        if d.name in candidates:
            return d
    return None


def build_coverage(
    structured: dict[str, dict[str, Path]],
) -> dict[str, dict[str, dict]]:
    """For each (period, canonical_key), pick the preferred source per precedence."""
    coverage: dict[str, dict[str, dict]] = {}
    for periodo, docs in structured.items():
        entry: dict[str, dict] = {}
        for key in CANONICAL_KEYS:
            for doc_type in COVERAGE_PRECEDENCE[key]:
                path = docs.get(doc_type)
                if not path:
                    continue
                # confirm the canonical key actually has data in that file
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                except Exception:
                    continue
                canonical = data.get("canonical") or {}
                if canonical.get(key) is None:
                    continue
                entry[key] = {"status": "filled", "source": as_rel(path)}
                break
        if entry:
            coverage[periodo] = entry
    return coverage


def build_sources(
    empresa: str,
    full: dict[str, list[Path]],
    structured: dict[str, dict[str, Path]],
    digesteds: list[Path],
    today: str,
    existing_sources: list[dict] | None = None,
) -> list[dict]:
    """Flatten full/ + cross-reference structured/ + digested/ into sources[]."""
    # index existing entries by (type, asof, full path) to preserve ingested_on dates.
    # some manifests group files (full is a list) — flatten to tuple so it is hashable.
    def _hashable(v):
        if isinstance(v, list):
            return tuple(v)
        return v

    by_key: dict[tuple, dict] = {}
    for s in existing_sources or []:
        key = (_hashable(s.get("type")), _hashable(s.get("asof")), _hashable(s.get("full")))
        by_key[key] = s

    sources: list[dict] = []
    for periodo in sorted(full):
        for full_path in full[periodo]:
            doc_type = infer_doc_type_from_full(full_path.name)
            key = (doc_type, periodo, as_rel(full_path))
            prior = by_key.get(key, {})
            entry = {
                "type": doc_type,
                "asof": periodo,
                "ingested_on": prior.get("ingested_on", today),
                "full": as_rel(full_path),
            }
            # structured cross-ref
            structured_paths: list[str] = []
            period_structured = structured.get(periodo, {})
            if doc_type in period_structured:
                structured_paths.append(as_rel(period_structured[doc_type]))
            if structured_paths:
                entry["structured"] = structured_paths
            # digested cross-ref
            digested = find_digested_for(empresa, doc_type, periodo, digesteds)
            if digested:
                entry["digested"] = as_rel(digested)
            elif prior.get("digested"):
                entry["digested"] = prior["digested"]
            sources.append(entry)
    return sources


def rebuild(empresa: str, dry_run: bool = False) -> dict:
    manifest_path = MANIFESTS_ROOT / f"{empresa}.json"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(2)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    structured = scan_structured(empresa)
    full = scan_full(empresa)
    digesteds = scan_digested(empresa)
    today = dt.date.today().isoformat()

    coverage = build_coverage(structured)
    sources = build_sources(
        empresa, full, structured, digesteds, today, manifest.get("sources") or []
    )

    # preserve top-level fields, overwrite coverage/sources/_updated
    manifest["coverage"] = coverage
    manifest["sources"] = sources
    manifest["_updated"] = today
    # prune caveat that said cold-start if we now have data
    caveats = manifest.get("caveats") or []
    caveats = [c for c in caveats if "cold-start" not in c.lower()]
    manifest["caveats"] = caveats

    if dry_run:
        summary = {
            "empresa": empresa,
            "periods_covered": sorted(coverage.keys()),
            "n_sources": len(sources),
            "n_coverage_entries": sum(len(v) for v in coverage.values()),
            "doc_type_counts": {},
        }
        for s in sources:
            t = s["type"]
            summary["doc_type_counts"][t] = summary["doc_type_counts"].get(t, 0) + 1
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {manifest_path}")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--empresa", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    rebuild(args.empresa, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
