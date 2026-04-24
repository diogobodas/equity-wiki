"""Dated Lint — parse `(fonte: X, em: YYYY-MM-DD)` citations across the wiki
and flag claims that are stale, contradictory, or missing dates.

Implemented:
    parse_claims(page_path)               -> list[ClaimCitation]
    scan_wiki(root)                       -> list[ClaimCitation]
    age_threshold_flags(claims, config)   -> list[Flag]
    missing_em_flags(claims, config)      -> list[Flag]
    write_report(flags, report_path)      -> None

Planned (tasks 8-9):
    newer_source_flags(claims, root)      -> list[Flag]
    contradiction_flags(claims)           -> list[Flag]

CLI:
    python tools/lib/dated_lint.py [--severity S] [--page P]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
# (fonte: PATH[, em: YYYY-MM-DD][, ARBITRARY ATTRS])
# Trailing comma-separated attributes (e.g., confiabilidade, §nota) are tolerated
# but not captured. `em:` may appear anywhere after `fonte:` within the parens.
# The fonte group uses greedy `[^,)]+` so it captures the full path up to the
# first comma or closing paren (lazy `+?` caused regression — see Task 6 fixup).
CITATION_RE = re.compile(
    r"\(fonte:\s*(?P<fonte>[^,)]+)"
    r"(?:,[^)]*?em:\s*(?P<em>\d{4}-\d{2}-\d{2}))?"
    r"[^)]*\)"
)
EXCERPT_CHARS_BEFORE = 200


@dataclass
class ClaimCitation:
    page: Path
    line: int
    excerpt: str
    fonte: str
    em: Optional[date]


@dataclass
class Flag:
    claim: ClaimCitation
    rule: str
    severity: str
    detail: str


def parse_claims(page_path: Path) -> list[ClaimCitation]:
    """Extract all `(fonte: ...)` citations from a markdown page.

    Skips fenced code blocks (``` ... ```).
    Returns one ClaimCitation per citation match.
    """
    text = page_path.read_text(encoding="utf-8")
    claims: list[ClaimCitation] = []
    in_code = False
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in CITATION_RE.finditer(line):
            start = max(0, m.start() - EXCERPT_CHARS_BEFORE)
            excerpt = line[start:m.start()].strip()
            em_str = m.group("em")
            em = date.fromisoformat(em_str) if em_str else None
            claims.append(
                ClaimCitation(
                    page=page_path,
                    line=idx,
                    excerpt=excerpt,
                    fonte=m.group("fonte").strip(),
                    em=em,
                )
            )
    return claims


def _read_frontmatter(page_path: Path) -> dict:
    """Extract YAML frontmatter as a dict. Returns empty dict if none found.

    Minimal parser: handles `key: value` scalars and `key: [a, b]` inline arrays
    on single lines. For keys with multi-line YAML list syntax (``sources:``
    followed by ``- item`` lines, common in all real wiki pages), the value
    is silently stored as an empty string — multi-line lists are NOT parsed.

    This is deliberate: `age_threshold_flags` only consumes scalar `type`.
    Rules that need `aliases` or `sources` (e.g., Task 8's newer_source_flags)
    must parse those fields themselves or use a dedicated helper.
    """
    text = page_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fm: dict = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            fm[key] = [s.strip() for s in val[1:-1].split(",") if s.strip()]
        else:
            fm[key] = val
    return fm


def _classify_claim_tipo(claim: ClaimCitation, config: dict) -> str:
    """Decide which threshold bucket applies to a claim.

    Priority chain:
      1. First tipo whose keyword matches the excerpt wins.
      2. Else: first tipo whose `page_types` includes the page's YAML `type:`.
      3. Else: return "default".

    Tie-break: iteration order follows the `tipo_inference` dict in
    `lint_config.json` (Python dicts preserve insertion order since 3.7).
    A page with `type: entity` and no keyword match will therefore classify as
    the first tipo in the config that lists `entity` under `page_types` —
    currently `guidance_corporativo` (6-month threshold). Reorder the config
    if a different default is desired.
    """
    excerpt_lower = claim.excerpt.lower()
    inference = config["tipo_inference"]
    page_type = _read_frontmatter(claim.page).get("type", "")

    for tipo, rules in inference.items():
        for kw in rules.get("keywords", []):
            if kw.lower() in excerpt_lower:
                return tipo

    for tipo, rules in inference.items():
        if page_type in rules.get("page_types", []):
            return tipo

    return "default"


def _months_between(earlier: date, later: date) -> int:
    return (later.year - earlier.year) * 12 + (later.month - earlier.month)


def age_threshold_flags(
    claims: list[ClaimCitation], config: dict, today: Optional[date] = None
) -> list[Flag]:
    """Flag claims whose `em:` is older than the configured threshold for its tipo."""
    if today is None:
        today = date.today()
    thresholds = config["thresholds_months"]
    flags: list[Flag] = []
    for c in claims:
        if c.em is None:
            continue
        tipo = _classify_claim_tipo(c, config)
        threshold = thresholds.get(tipo, thresholds["default"])
        age_months = _months_between(c.em, today)
        if age_months >= threshold:
            flags.append(
                Flag(
                    claim=c,
                    rule="age_threshold",
                    severity="warn",
                    detail=(
                        f"em={c.em.isoformat()} is {age_months} months old "
                        f"(threshold for tipo={tipo} is {threshold})"
                    ),
                )
            )
    return flags


_NUMBER_RE = re.compile(r"\d")


def missing_em_flags(claims: list[ClaimCitation], config: dict) -> list[Flag]:
    """Flag claims without `em:` that contain both a number and a temporal verb."""
    heuristic = config["missing_em_heuristic"]
    verbs = [v.lower() for v in heuristic["temporal_verbs"]]
    requires_number = heuristic.get("requires_number", True)
    flags: list[Flag] = []
    for c in claims:
        if c.em is not None:
            continue
        excerpt_lower = c.excerpt.lower()
        has_verb = any(v in excerpt_lower for v in verbs)
        if not has_verb:
            continue
        if requires_number and not _NUMBER_RE.search(c.excerpt):
            continue
        hit_verb = next(v for v in verbs if v in excerpt_lower)
        flags.append(
            Flag(
                claim=c,
                rule="missing_em",
                severity="hint",
                detail=f'contains temporal verb "{hit_verb}" + number but lacks `em:`',
            )
        )
    return flags


# Files at wiki root that are documentation/audit artifacts, not wiki pages.
# Their `(fonte: ...)` patterns are illustrative examples or log entries, not
# factual claims to lint.
SKIP_FILES = {"SCHEMA.md", "CLAUDE.md", "README.md", "Melnick.md", "log.md", "index.md"}


def scan_wiki(root: Path) -> list[ClaimCitation]:
    """Parse all top-level wiki pages under `root`.

    Excludes infrastructure directories (docs/, sources/, tools/, .git/, etc.)
    and documentation/log files at the root (see SKIP_FILES).
    """
    skip_dirs = {"docs", "sources", "tools", "tests", "logs", ".git", ".obsidian",
                 ".playwright-cli", ".claude", ".pytest_cache", "__pycache__"}
    claims: list[ClaimCitation] = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and entry.name in skip_dirs:
            continue
        if entry.is_file() and entry.suffix == ".md" and entry.name not in SKIP_FILES:
            claims.extend(parse_claims(entry))
    return claims


def write_report(
    flags: list[Flag],
    report_path: Path,
    as_of: Optional[date] = None,
) -> None:
    """Render flags as a markdown report grouped by page then severity."""
    if as_of is None:
        as_of = date.today()
    by_page: dict[Path, list[Flag]] = {}
    for f in flags:
        by_page.setdefault(f.claim.page, []).append(f)

    severity_order = {"action": 0, "warn": 1, "hint": 2}
    lines = [f"# Lint Report — {as_of.isoformat()}\n"]
    total = {"action": 0, "warn": 0, "hint": 0}
    for fl in flags:
        total[fl.severity] = total.get(fl.severity, 0) + 1
    lines.append(
        f"**Totals:** action={total.get('action',0)}  "
        f"warn={total.get('warn',0)}  hint={total.get('hint',0)}\n"
    )
    if not flags:
        lines.append("\nNo flags raised.\n")
    for page in sorted(by_page.keys(), key=lambda p: p.name):
        page_flags = sorted(
            by_page[page],
            key=lambda f: (severity_order.get(f.severity, 9), f.claim.line),
        )
        lines.append(f"\n## {page.name}\n")
        for fl in page_flags:
            lines.append(
                f"- **[{fl.severity}]** line {fl.claim.line} rule=`{fl.rule}` — "
                f"{fl.detail}\n"
            )
            excerpt = fl.claim.excerpt[-140:] if fl.claim.excerpt else ""
            if excerpt:
                lines.append(f"  > ...{excerpt}\n")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run dated-claim lint over the wiki.")
    parser.add_argument("--severity", choices=["action", "warn", "hint"], default="hint",
                        help="Minimum severity to emit (default: hint, emits all).")
    parser.add_argument("--page", default=None, help="Restrict scan to a single page (relative path).")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Wiki root dir.")
    args = parser.parse_args()

    root = Path(args.root)
    config = json.loads((root / "tools" / "lint_config.json").read_text(encoding="utf-8"))

    if args.page:
        page = root / args.page
        if not page.exists():
            print(f"error: page {page} not found", file=sys.stderr)
            return 1
        claims = parse_claims(page)
    else:
        claims = scan_wiki(root)

    all_flags: list[Flag] = []
    all_flags.extend(age_threshold_flags(claims, config))
    all_flags.extend(missing_em_flags(claims, config))

    sev_rank = {"action": 0, "warn": 1, "hint": 2}
    min_rank = sev_rank[args.severity]
    filtered = [f for f in all_flags if sev_rank[f.severity] <= min_rank]

    today = date.today()
    report_path = root / "sources" / "lint_reports" / f"{today.isoformat()}.md"
    write_report(filtered, report_path, as_of=today)

    log_path = root / "log.md"
    counts = {"action": 0, "warn": 0, "hint": 0}
    for f in filtered:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(
            f"[lint] {today.isoformat()} sources/lint_reports/{today.isoformat()}.md "
            f"action={counts['action']} warn={counts['warn']} hint={counts['hint']}\n"
        )
    print(f"Report: {report_path}")
    print(f"Totals: action={counts['action']} warn={counts['warn']} hint={counts['hint']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
