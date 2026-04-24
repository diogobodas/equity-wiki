"""Dated Lint — parse `(fonte: X, em: YYYY-MM-DD)` citations across the wiki
and flag claims that are stale, contradictory, or missing dates.

Implemented:
    parse_claims(page_path)               -> list[ClaimCitation]
    scan_wiki(root)                       -> list[ClaimCitation]
    age_threshold_flags(claims, config)   -> list[Flag]
    missing_em_flags(claims, config)      -> list[Flag]
    newer_source_flags(claims, root)      -> list[Flag]
    contradiction_flags(claims)           -> list[Flag]
    write_report(flags, report_path)      -> None

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

    Supports three value shapes:
      key: scalar_value
      key: [inline, list, of, items]
      key:
        - multi
        - line
        - list

    Nested maps are NOT parsed; keys under a nested structure are ignored.
    Keys other than the three above are coerced to strings.
    """
    text = page_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    fm: dict = {}
    current_key: Optional[str] = None
    current_list: Optional[list] = None
    for raw in text[4:end].splitlines():
        # Close any in-progress multi-line list when we hit a non-indented or
        # non-list-item line.
        if current_key is not None and current_list is not None:
            stripped = raw.lstrip()
            is_comment = stripped.startswith("#")
            is_list_continuation = stripped.startswith("-") or is_comment
            if (raw and not raw[0].isspace()) or (stripped and not is_list_continuation):
                fm[current_key] = current_list
                current_key = None
                current_list = None

        if not raw.strip():
            continue

        if current_list is not None:
            stripped = raw.lstrip()
            if stripped.startswith("- "):
                item = stripped[2:].strip().strip('"').strip("'")
                current_list.append(item)
                continue
            if stripped == "-":
                continue

        if ":" not in raw:
            continue
        if raw[0].isspace():
            # Indented line that is not part of a tracked multi-line list — ignore.
            continue

        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()

        if val == "":
            # Start of a potential multi-line list. Peek behavior handled
            # on the next iteration via current_list.
            current_key = key
            current_list = []
            continue

        if val.startswith("[") and val.endswith("]"):
            fm[key] = [s.strip() for s in val[1:-1].split(",") if s.strip()]
        else:
            fm[key] = val

    # Close any trailing multi-line list.
    if current_key is not None and current_list is not None:
        fm[current_key] = current_list

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
    claims: list[ClaimCitation],
    config: dict,
    today: Optional[date] = None,
    exclude_claims: Optional[set[tuple[Path, int]]] = None,
) -> list[Flag]:
    """Flag claims whose `em:` is older than the configured threshold for its tipo.

    Per SCHEMA.md §Lint §10(a): only fires when no newer source is available on
    the same topic. Callers pass `exclude_claims` — a set of (page, line) tuples
    for claims that already have a `newer_source` flag — so age_threshold does
    not produce a redundant `warn` on top of the `action` flag.
    """
    if today is None:
        today = date.today()
    if exclude_claims is None:
        exclude_claims = set()
    thresholds = config["thresholds_months"]
    flags: list[Flag] = []
    for c in claims:
        if c.em is None:
            continue
        if (c.page, c.line) in exclude_claims:
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


def _load_manifests(root: Path) -> list[dict]:
    manifest_dir = root / "sources" / "manifests"
    if not manifest_dir.exists():
        return []
    manifests = []
    for path in manifest_dir.glob("*.json"):
        if path.name.startswith("_"):
            continue
        try:
            manifests.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return manifests


def _page_aliases(page_path: Path) -> set[str]:
    """Return aliases of a page as a lowercased set. Includes filename stem."""
    fm = _read_frontmatter(page_path)
    aliases = set()
    raw = fm.get("aliases")
    if isinstance(raw, list):
        aliases.update(a.lower() for a in raw)
    elif isinstance(raw, str) and raw:
        aliases.add(raw.lower())
    aliases.add(page_path.stem.lower())
    return aliases


def newer_source_flags(
    claims: list[ClaimCitation], root: Path
) -> list[Flag]:
    """Flag claims whose page has a matching manifest entry with ingested_on > em.

    Note on breadth: this rule matches any manifest source with `ingested_on > em`,
    regardless of whether the specific source is topically relevant to the
    individual claim. Per the design, the rule surfaces a cross-pipeline signal
    (a newer ingest exists for the same empresa/concept) and leaves topical
    triage to the human. Expect multiple claims on the same page to be flagged
    against the same newest source.
    """
    manifests = _load_manifests(root)
    alias_cache: dict[Path, set[str]] = {}
    flags: list[Flag] = []
    for c in claims:
        if c.em is None:
            continue
        if c.page not in alias_cache:
            alias_cache[c.page] = _page_aliases(c.page)
        page_aliases = alias_cache[c.page]
        newest_ingested: Optional[date] = None
        newest_source: Optional[str] = None
        for m in manifests:
            raw_aliases = m.get("aliases", [])
            if isinstance(raw_aliases, list):
                m_aliases = {str(a).lower() for a in raw_aliases}
            elif isinstance(raw_aliases, str):
                m_aliases = {raw_aliases.lower()}
            else:
                m_aliases = set()
            m_aliases.add(str(m.get("empresa", "")).lower())
            if not (page_aliases & m_aliases):
                continue
            for src in m.get("sources", []):
                ingested_raw = src.get("ingested_on")
                if not ingested_raw:
                    continue
                try:
                    ingested = date.fromisoformat(ingested_raw)
                except (ValueError, TypeError):
                    continue
                if ingested <= c.em:
                    continue
                if newest_ingested is None or ingested > newest_ingested:
                    newest_ingested = ingested
                    newest_source = (
                        src.get("digested")
                        or src.get("full")
                        or src.get("structured")
                        or "<unknown>"
                    )
        if newest_ingested is not None:
            flags.append(
                Flag(
                    claim=c,
                    rule="newer_source",
                    severity="action",
                    detail=(
                        f"source {newest_source} ingested_on={newest_ingested.isoformat()} "
                        f"is newer than claim em={c.em.isoformat()}"
                    ),
                )
            )
    return flags


_KEY_PHRASE_RE = re.compile(r"[A-Za-zÀ-ÿ]{4,}(?:\s+[A-Za-zÀ-ÿ0-9]+){0,3}")
_VALUE_RE = re.compile(
    r"(?:R\$\s*)?([\d]{1,3}(?:[.\s]\d{3})+|\d+)(?:,(\d+))?\s*(bi|mm|mil|milhões|milhão|mi|k|%)?",
    re.IGNORECASE,
)


def _normalize_value(match: re.Match) -> Optional[float]:
    """Convert a matched number with unit to a float in canonical units.

    Percentage stays in pct. Monetary is normalized to reais (bi=1e9, mm=1e6, mil=1e3).
    Returns None if parse fails or the match is a bare year token (1900-2100
    without unit or decimal) — year tokens are excluded to prevent them from
    polluting numeric buckets in contradiction_flags.
    """
    int_part = match.group(1).replace(".", "").replace(" ", "")
    dec_part = match.group(2)
    unit = (match.group(3) or "").lower()
    try:
        raw = float(int_part)
        if dec_part:
            raw += float(f"0.{dec_part}")
    except ValueError:
        return None
    # Year-token guard: bare integer in [1900, 2100] with no unit/decimal is a
    # date, not a claim value.
    if not unit and not dec_part and 1900 <= raw <= 2100 and "." not in match.group(1) and " " not in match.group(1):
        return None
    if unit == "%":
        return raw
    mult = {"bi": 1e9, "mm": 1e6, "mi": 1e6, "milhões": 1e6, "milhão": 1e6, "mil": 1e3, "k": 1e3}.get(unit, 1.0)
    return raw * mult


def _extract_key_phrase(excerpt: str) -> Optional[str]:
    """Pick a 2-5 word key phrase from the excerpt (used as contradiction bucket key).

    Strategy: returns the LAST alphabetic phrase in the excerpt (positional last,
    not longest). The trailing phrase is typically the subject of the citation
    ("teto Faixa 3", "receita bruta", "alíquota IBS"), so using it as the bucket
    key naturally groups claims about the same quantity.
    """
    candidates = _KEY_PHRASE_RE.findall(excerpt)
    if not candidates:
        return None
    return candidates[-1].strip().lower()


_EMBEDDED_CITATION_RE = re.compile(r"\(fonte:[^)]*\)")


def _clean_excerpt_for_contradiction(excerpt: str) -> str:
    """Strip `(fonte: ...)` spans so that source-path tokens don't pollute the
    key-phrase extraction in contradiction_flags (e.g., 'company_specific',
    'canonical', 'operacional' from aggregation lines).
    """
    return _EMBEDDED_CITATION_RE.sub("", excerpt).strip()


def contradiction_flags(claims: list[ClaimCitation]) -> list[Flag]:
    """Flag pairs of claims on different pages with same key phrase but different values.

    Heuristic — groups claims by an extracted "key phrase" (alphabetic word group
    at the end of the claim excerpt) and flags within-group disagreement on
    normalised numeric value. Intentionally imperfect; prefers recall over
    precision at `action` severity. Expect false positives to be triaged by
    human review rather than suppressed in code.

    Pre-processing: strips embedded `(fonte: ...)` spans from the excerpt so that
    source-path tokens (canonical, company_specific, operacional, ...) don't
    become key phrases on multi-citation aggregation lines.
    """
    buckets: dict[str, list[tuple[ClaimCitation, float]]] = {}
    for c in claims:
        cleaned_excerpt = _clean_excerpt_for_contradiction(c.excerpt)
        # Use the largest-magnitude value in the excerpt so that monetary amounts
        # (e.g. R$ 350.000) dominate nearby count/classifier digits (e.g. "3" in
        # "Faixa 3"). re.search would return the leftmost match, which is wrong.
        best_val: Optional[float] = None
        for m in _VALUE_RE.finditer(cleaned_excerpt):
            v = _normalize_value(m)
            if v is None:
                continue
            if best_val is None or abs(v) > abs(best_val):
                best_val = v
        if best_val is None:
            continue
        key = _extract_key_phrase(cleaned_excerpt)
        if not key:
            continue
        buckets.setdefault(key, []).append((c, best_val))

    flags: list[Flag] = []
    for key, items in buckets.items():
        pages = {c.page for c, _ in items}
        if len(pages) < 2:
            continue
        values = {round(v, 4) for _, v in items}
        if len(values) < 2:
            continue
        for c, v in items:
            other_vals = sorted({round(v2, 4) for _, v2 in items if v2 != v})
            flags.append(
                Flag(
                    claim=c,
                    rule="contradiction",
                    severity="action",
                    detail=(
                        f'key="{key}" value={v} conflicts with values {other_vals} '
                        f"on other pages"
                    ),
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

    # Run newer_source first so that age_threshold can dedupe against it
    # (per SCHEMA.md §Lint §10(a): age_threshold fires only when no newer
    # source is available on the same topic).
    newer_source_result = newer_source_flags(claims, root)
    newer_source_keys = {(f.claim.page, f.claim.line) for f in newer_source_result}

    all_flags: list[Flag] = []
    all_flags.extend(age_threshold_flags(claims, config, exclude_claims=newer_source_keys))
    all_flags.extend(missing_em_flags(claims, config))
    all_flags.extend(newer_source_result)
    all_flags.extend(contradiction_flags(claims))

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
