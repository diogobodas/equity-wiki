"""Number Guard - validates numbers in a digest against the cited source file.

Public API:
    extract_numbers(text, cite_anchor_map=None) -> list[NumberClaim]
    index_source(full_path)                     -> dict[(unit, value)] -> list[SourceNumber]
    match_claim(claim, index)                   -> MatchResult
    check_digest(digest_path)                   -> list[MatchResult]
    annotate(digest_path, results)              -> str (new file content)

Match semantics (per spec):
    MATCH_STRICT - value within tolerance AND at least one non-trivial keyword
                   from the claim context overlaps the source context.
    MATCH_LOOSE  - value within tolerance but no keyword overlap.
    NO_MATCH     - no value within tolerance, OR no citation anchor, OR source
                   file missing.

Tolerances:
    %      - ±0,5 percentage points absolute
    R$/int - ±0,5 % relative

Unit normalization (PT-BR):
    R$ 1,2 bi     -> 1.2 * 1e9   reais
    R$ 1.234 mm   -> 1234 * 1e6  reais
    R$ 1.987 mil  -> 1987 * 1e3  reais
    R$ 1.234,56   -> 1234.56     reais
    (245)         -> -245        (parens-negative convention)
    28,5 ≡ 28.5   (separator-agnostic)
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

STOPWORDS = {
    # PT-BR function words
    "sobre", "para", "esse", "essa", "isso", "deste", "desta", "pelo",
    "pela", "pelos", "pelas", "entre", "muito", "muita", "foram",
    "estão", "estava", "estavam", "havia", "existe", "existem", "quando",
    "quanto", "quantos", "quantas", "como", "onde", "porque", "então",
    "ainda", "depois", "antes", "durante", "mesmo", "mesma", "apenas",
    "todos", "todas", "outro", "outra", "outros", "outras", "nesse",
    "nessa", "naquele", "naquela", "porém", "também", "segundo",
    # Common frame words that don't discriminate context
    "fonte", "full", "notas", "generic", "ponto", "valor", "nota",
    # EN equivalents
    "this", "that", "these", "those", "which", "what", "when", "where",
    "while", "after", "before", "among", "their", "there", "other",
    "with", "from", "they", "have", "been", "were",
}

# Units: %, bi|bilhão|bilhões, mm|milhão|milhões, mil, milhares.
# Negative can be "-123" or "(123)".
_NUMBER_RE = re.compile(
    r"""
    (?P<prefix>R\$\s*)?
    (?P<negparen>\()?
    (?P<neg>-)?
    (?P<num>
        \d{1,3}(?:\.\d{3})+(?:,\d+)?   # 1.234 | 1.234,56 | 1.234.567 (thousands-dot)
      | \d+\.\d{1,2}(?!\d)              # 28.5 | 28.50 (dot-decimal, ≤2 digits)
      | \d+(?:,\d+)?                    # 28 | 28,5 (plain / comma-decimal)
    )
    (?P<negclose>\))?
    (?:
        \s*(?P<unit>
            %
          | billions?                     # 1 billion
          | bilh(?:ão|ões)                # 1 bilhão / 2 bilhões
          | bn(?!\w)                      # 1 bn
          | bi(?!\w)                      # 1 bi
          | millions?                     # 1 million
          | milh(?:ão|ões)                # 1 milhão / 2 milhões
          | mn(?!\w)                      # 1 mn
          | mm(?!\w)                      # 1 mm
          | thousands?                    # 1 thousand
          | milhares(?!\w)                # 2 milhares
          | mil(?!\w)                     # 1 mil
          | k(?!\w)                       # 1k (shorthand)
          | reais(?!\w)                   # 10 reais
          | real(?!\w)                    # 1 real
        )
    )?
    """,
    re.VERBOSE | re.IGNORECASE,
)

_CITE_RE = re.compile(r"\(fonte:\s*([^)§]+?)(?:\s*§[^)]+)?\)", re.IGNORECASE)


@dataclass
class NumberClaim:
    raw: str
    value: float
    unit: str           # '%', 'reais', or '' (bare integer)
    line_no: int        # 1-based
    col_start: int      # 0-based
    context: str        # ±40 chars around match
    cite_path: str | None = None


@dataclass
class SourceNumber:
    raw: str
    value: float
    unit: str
    line_no: int
    context: str


@dataclass
class MatchResult:
    claim: NumberClaim
    status: str                       # 'MATCH_STRICT' | 'MATCH_LOOSE' | 'NO_MATCH'
    matched_with: SourceNumber | None = None
    reason: str = ""


# ---------- Parsing ----------

def _parse_pt_number(raw: str) -> float:
    """Parse a PT-BR-ish number string to float.

    Heuristics:
    - If comma is present: comma is decimal, dots are thousands.
        '1.234,56' -> 1234.56 ; '28,5' -> 28.5
    - If only dot(s): if every dot group has exactly 3 digits, treat as
      thousands separators (PT-BR convention). Otherwise the last dot is
      decimal, earlier dots are thousands.
        '1.234'   -> 1234   (thousands)
        '28.5'    -> 28.5   (decimal)
        '1.234.5' -> 1234.5 (mixed - last is decimal)
    - No separator -> plain integer.
    """
    if "," in raw:
        return float(raw.replace(".", "").replace(",", "."))
    if "." not in raw:
        return float(raw)
    parts = raw.split(".")
    tail = parts[1:]
    if all(len(g) == 3 for g in tail):
        return float("".join(parts))
    integer = "".join(parts[:-1])
    decimal = parts[-1]
    return float(f"{integer}.{decimal}")


_BILLION_UNITS = {"bi", "bilhão", "bilhões", "bn", "billion", "billions"}
_MILLION_UNITS = {"mm", "mn", "milhão", "milhões", "million", "millions"}
_THOUSAND_UNITS = {"mil", "milhares", "k", "thousand", "thousands"}
_REAL_UNITS = {"real", "reais"}  # currency marker w/ factor 1


def _unit_factor(unit: str) -> float:
    u = (unit or "").lower()
    if u == "%":
        return 1.0
    if u in _BILLION_UNITS:
        return 1e9
    if u in _MILLION_UNITS:
        return 1e6
    if u in _THOUSAND_UNITS:
        return 1e3
    return 1.0


def _canonical_unit(prefix: str, unit: str) -> str:
    """Classify a match into one of: '%', 'reais', ''."""
    u = (unit or "").lower()
    if u == "%":
        return "%"
    if (
        prefix
        or u in _BILLION_UNITS
        or u in _MILLION_UNITS
        or u in _THOUSAND_UNITS
        or u in _REAL_UNITS
    ):
        return "reais"
    return ""


def _cite_spans(line: str) -> list[tuple[int, int]]:
    """Return (start, end) spans of every (fonte: ...) marker in the line."""
    return [(m.start(), m.end()) for m in _CITE_RE.finditer(line)]


def _in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    for s, e in spans:
        if s <= pos < e:
            return True
    return False


# Date-like tokens that extract_numbers should skip (not real numeric claims).
# Matches YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, and isolated YYYY appearing as year.
_DATE_SPANS_RE = re.compile(
    r"""
      \b\d{4}-\d{2}-\d{2}\b           # 2026-04-16
    | \b\d{2}/\d{2}/\d{4}\b           # 16/04/2026
    | \b\d{2}/\d{2}/\d{2}\b           # 16/04/26
    | \b\d{2}-\d{2}-\d{4}\b           # 16-04-2026
    | \b\d{4}/\d{2}/\d{2}\b           # 2026/04/16
    | \b(?:19|20)\d{2}\b              # 1995..2099 standalone year
    """,
    re.VERBOSE,
)

# Ordered-list markers and numbered markdown headings — the punctuation [.):]
# is REQUIRED, otherwise plain sentences like "700 million 3T25" get swallowed.
_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*]\s+)?(?:#{1,6}\s+)?\d+(?:\.\d+)*[.):]\s")


def _date_spans(line: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in _DATE_SPANS_RE.finditer(line)]


def _list_marker_end(line: str) -> int:
    m = _LIST_MARKER_RE.match(line)
    return m.end() if m else -1


def _strip_frontmatter(text: str) -> tuple[int, str]:
    """If text starts with a YAML frontmatter block, return (offset_lines, body).

    Otherwise returns (0, text). Line numbers in the returned body are offset_lines
    LOWER than the original — callers must add offset_lines to their line_no.
    """
    if not text.startswith("---"):
        return 0, text
    # find closing --- at start of line
    lines = text.splitlines(keepends=True)
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            end_idx = i
            break
    if end_idx < 0:
        return 0, text
    return end_idx + 1, "".join(lines[end_idx + 1 :])


def _scan_has_letter(line: str, start: int, step: int, max_scan: int = 8) -> bool:
    """Scan outward from `start` in direction `step` through alnum chars.

    Returns True if any letter is found in the contiguous alnum run.
    Stops at the first non-alnum char.
    """
    i = start
    for _ in range(max_scan):
        if i < 0 or i >= len(line):
            return False
        ch = line[i]
        if not ch.isalnum():
            return False
        if ch.isalpha():
            return True
        i += step
    return False


def _boundary_ok(
    line: str,
    start: int,
    end: int,
    has_prefix: bool,
    has_unit: bool,
    has_neg: bool = False,
) -> bool:
    """Reject numbers glued to letters or embedded in identifiers.

    Rejects (all "letter-adjacent" cases, numeric ranges like 90-120 are kept):
    - letters directly before the number with no prefix (e.g. '3T25' -> '25')
    - letters directly after the number with no unit
    - model-identifier patterns with a LETTER in the adjacent alnum run
      (K6-2 -> reject because 'K' precedes; 8086/286 -> accept as numeric range)
    """
    if start > 0 and not has_prefix:
        ch = line[start - 1]
        if has_neg:
            if _scan_has_letter(line, start - 1, -1):
                return False
        else:
            if ch.isalpha():
                return False
            if ch in "-/" and _scan_has_letter(line, start - 2, -1):
                return False
    if end < len(line) and not has_unit:
        ch = line[end]
        if ch.isalpha():
            return False
        if ch in "-/" and _scan_has_letter(line, end + 1, 1):
            return False
    return True


def extract_numbers(
    text: str,
    cite_anchor_map: dict[int, str] | None = None,
    skip_frontmatter: bool = True,
) -> list[NumberClaim]:
    """Scan text and return all number claims with context + optional cite anchor.

    Skipped by design (reduce false positives, not real numeric claims):
    - YAML frontmatter block (opt-out via skip_frontmatter=False)
    - Text inside (fonte: ...) markers
    - Dates (YYYY-MM-DD, DD/MM/YYYY, standalone years 19xx/20xx)
    - Ordered-list markers at line start ("1. ", "12. ")
    - Bare digits glued to letters (period codes like '3T25')
    """
    if skip_frontmatter:
        line_offset, body = _strip_frontmatter(text)
    else:
        line_offset, body = 0, text

    claims: list[NumberClaim] = []
    lines = body.splitlines()
    anchor_lines = sorted(cite_anchor_map.keys()) if cite_anchor_map else []

    for local_line_no, line in enumerate(lines, start=1):
        line_no = local_line_no + line_offset
        skip_spans = _cite_spans(line) + _date_spans(line)
        list_skip_upto = _list_marker_end(line)
        for m in _NUMBER_RE.finditer(line):
            full_start = m.start()
            full_end = m.end()

            if _in_spans(full_start, skip_spans):
                continue
            if full_start < list_skip_upto:
                continue

            num_str = m.group("num")
            unit = (m.group("unit") or "").lower()
            prefix = m.group("prefix") or ""
            has_unit = bool(unit)
            has_prefix = bool(prefix) or bool(m.group("negparen"))
            has_neg = bool(m.group("neg"))

            # Range separator detection: "90-120" is not "90" + "negative 120".
            # If neg matched but the char before the '-' is a digit, treat as range
            # — unless a LETTER lives in that adjacent alnum run (then it's still a
            # compound identifier like "K6-2" and the whole match should be dropped).
            if has_neg and full_start > 0 and line[full_start - 1].isdigit():
                if _scan_has_letter(line, full_start - 1, -1):
                    continue  # compound ID like "K6-2" — drop the match entirely
                has_neg = False

            if not _boundary_ok(line, full_start, full_end, has_prefix, has_unit, has_neg):
                continue

            try:
                base = _parse_pt_number(num_str)
            except ValueError:
                continue
            value = base * _unit_factor(unit)
            if has_neg or (bool(m.group("negparen")) and bool(m.group("negclose"))):
                value = -value
            cu = _canonical_unit(prefix, unit)

            ctx_lo = max(0, full_start - 40)
            ctx_hi = min(len(line), full_end + 40)
            context = line[ctx_lo:ctx_hi]
            raw = line[full_start:full_end].strip()

            cite = None
            if anchor_lines:
                idx = 0
                lo, hi = 0, len(anchor_lines) - 1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if anchor_lines[mid] <= line_no:
                        idx = mid
                        lo = mid + 1
                    else:
                        hi = mid - 1
                if anchor_lines[idx] <= line_no:
                    cite = cite_anchor_map[anchor_lines[idx]]

            claims.append(NumberClaim(
                raw=raw, value=value, unit=cu,
                line_no=line_no, col_start=full_start,
                context=context, cite_path=cite,
            ))
    return claims


def cite_anchors(text: str) -> dict[int, str]:
    """Map {line_no: source_path} for every (fonte: path [§section]) marker in text.

    Last anchor on a given line wins (rare).
    """
    anchors: dict[int, str] = {}
    for ln, line in enumerate(text.splitlines(), start=1):
        for m in _CITE_RE.finditer(line):
            anchors[ln] = m.group(1).strip()
    return anchors


# ---------- Index + matching ----------

def _resolve_source(full_path: str | Path) -> Path | None:
    """Find the referenced source on disk, tolerating the `full/...` vs `sources/full/...` convention."""
    p = Path(full_path)
    if p.is_absolute():
        return p if p.exists() else None
    direct = REPO_ROOT / p
    if direct.exists():
        return direct
    # Citations in digests drop the 'sources/' prefix — prepend and retry.
    first = p.parts[0] if p.parts else ""
    if first in ("full", "structured", "digested"):
        alt = REPO_ROOT / "sources" / p
        if alt.exists():
            return alt
    return None


def index_source(full_path: str | Path) -> dict[tuple[str, float], list[SourceNumber]]:
    """Extract and index every number in the source file by (unit, rounded_value)."""
    p = _resolve_source(full_path)
    if p is None:
        return {}
    text = p.read_text(encoding="utf-8", errors="replace")
    idx: dict[tuple[str, float], list[SourceNumber]] = {}
    for c in extract_numbers(text):
        sn = SourceNumber(
            raw=c.raw, value=c.value, unit=c.unit,
            line_no=c.line_no, context=c.context,
        )
        key = (c.unit, round(c.value, 6))
        idx.setdefault(key, []).append(sn)
    return idx


def _keywords(context: str) -> set[str]:
    toks = re.findall(r"[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ0-9_]{3,}", context)
    return {t.lower() for t in toks if t.lower() not in STOPWORDS}


def _within_tolerance(a: NumberClaim | SourceNumber, b: SourceNumber) -> bool:
    if a.unit != b.unit:
        return False
    if a.unit == "%":
        return abs(a.value - b.value) <= 0.5  # half pp absolute
    denom = max(abs(a.value), abs(b.value), 1.0)
    return abs(a.value - b.value) / denom <= 0.005


def match_claim(
    claim: NumberClaim,
    index: dict[tuple[str, float], list[SourceNumber]],
) -> MatchResult:
    if not index:
        return MatchResult(claim, "NO_MATCH", reason="empty source index")

    candidates: list[SourceNumber] = []
    seen: set[int] = set()
    for (u, _v), sns in index.items():
        if u != claim.unit:
            continue
        for sn in sns:
            if id(sn) in seen:
                continue
            if _within_tolerance(claim, sn):
                candidates.append(sn)
                seen.add(id(sn))

    if not candidates:
        return MatchResult(claim, "NO_MATCH", reason="no value within tolerance")

    claim_kw = _keywords(claim.context)
    for sn in candidates:
        if claim_kw & _keywords(sn.context):
            return MatchResult(claim, "MATCH_STRICT", matched_with=sn)
    return MatchResult(
        claim, "MATCH_LOOSE", matched_with=candidates[0],
        reason="value within tolerance but context differs",
    )


# ---------- End-to-end check ----------

def check_digest(digest_path: str | Path) -> list[MatchResult]:
    dp = Path(digest_path)
    text = dp.read_text(encoding="utf-8")
    anchors = cite_anchors(text)
    claims = extract_numbers(text, cite_anchor_map=anchors)
    results: list[MatchResult] = []
    cache: dict[str, dict] = {}
    for c in claims:
        if not c.cite_path:
            results.append(MatchResult(c, "NO_MATCH", reason="no citation anchor"))
            continue
        if c.cite_path not in cache:
            cache[c.cite_path] = index_source(c.cite_path)
        idx = cache[c.cite_path]
        if not idx:
            results.append(MatchResult(
                c, "NO_MATCH", reason=f"source file not found: {c.cite_path}",
            ))
            continue
        results.append(match_claim(c, idx))
    return results


def annotate(digest_path: str | Path, results: list[MatchResult]) -> str:
    """Return new digest text with ' [?]' inserted after each NO_MATCH claim.

    Idempotent: strips existing ' [?]' markers before re-inserting, so re-running
    the guard on an already-annotated digest produces the same output (not doubled).
    """
    dp = Path(digest_path)
    raw = dp.read_text(encoding="utf-8").replace(" [?]", "")
    # Use splitlines with keepends to preserve EOL exactly
    lines = raw.splitlines(keepends=True)

    # Group NO_MATCH insertions by line, process each line's insertions right-to-left
    by_line: dict[int, list[MatchResult]] = {}
    for r in results:
        if r.status != "NO_MATCH":
            continue
        by_line.setdefault(r.claim.line_no - 1, []).append(r)

    for line_idx, rs in by_line.items():
        line = lines[line_idx]
        eol = ""
        if line.endswith("\r\n"):
            eol = "\r\n"; body = line[:-2]
        elif line.endswith("\n"):
            eol = "\n"; body = line[:-1]
        else:
            body = line
        # Find actual match end columns; sort descending so insertions don't shift earlier indices
        inserts: list[int] = []
        for r in rs:
            col = body.find(r.claim.raw, r.claim.col_start)
            if col < 0:
                col = body.find(r.claim.raw)
            if col < 0:
                continue
            inserts.append(col + len(r.claim.raw))
        inserts.sort(reverse=True)
        for pos in inserts:
            body = body[:pos] + " [?]" + body[pos:]
        lines[line_idx] = body + eol

    return "".join(lines)


def write_report(digest_path: str | Path, results: list[MatchResult]) -> Path:
    dp = Path(digest_path)
    stem = dp.stem
    if stem.endswith("_summary"):
        slug = stem[: -len("_summary")]
    else:
        slug = stem
    out = dp.with_name(f"{slug}_guard_report.md")
    no_match = [r for r in results if r.status == "NO_MATCH"]
    loose = [r for r in results if r.status == "MATCH_LOOSE"]
    strict = [r for r in results if r.status == "MATCH_STRICT"]
    lines = [
        f"# Number Guard Report - {dp.name}",
        "",
        f"- Total claims: {len(results)}",
        f"- STRICT matches: {len(strict)}",
        f"- LOOSE matches: {len(loose)}",
        f"- NO_MATCH (marked `[?]`): {len(no_match)}",
        "",
    ]
    if no_match:
        lines += ["## No Match", "",
                  "| Line | Raw | Value | Unit | Cite | Reason |",
                  "|---|---|---|---|---|---|"]
        for r in no_match:
            lines.append(
                f"| {r.claim.line_no} | `{r.claim.raw}` | {r.claim.value:g} | "
                f"{r.claim.unit or '-'} | {r.claim.cite_path or '-'} | {r.reason} |"
            )
        lines.append("")
    if loose:
        lines += ["## Loose Match (value matches, context differs)", "",
                  "| Line | Raw | Value | Unit | Cite | Source line |",
                  "|---|---|---|---|---|---|"]
        for r in loose:
            sn = r.matched_with
            lines.append(
                f"| {r.claim.line_no} | `{r.claim.raw}` | {r.claim.value:g} | "
                f"{r.claim.unit or '-'} | {r.claim.cite_path or '-'} | "
                f"{sn.line_no if sn else '-'} |"
            )
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---------- CLI ----------

def _cmd_check(args) -> int:
    dp = Path(args.digest_path)
    if not dp.exists():
        print(f"ERROR: digest not found: {dp}", file=sys.stderr)
        return 2
    results = check_digest(dp)
    no_match = [r for r in results if r.status == "NO_MATCH"]
    loose = [r for r in results if r.status == "MATCH_LOOSE"]
    strict = [r for r in results if r.status == "MATCH_STRICT"]

    if no_match:
        new = annotate(dp, results)
        dp.write_text(new, encoding="utf-8")
        report = write_report(dp, results)
        print(
            f"Guard: {len(results)} claims | STRICT={len(strict)} "
            f"LOOSE={len(loose)} NO_MATCH={len(no_match)} "
            f"-> marked [?] + report: {report}"
        )
    elif loose:
        report = write_report(dp, results)
        print(
            f"Guard: {len(results)} claims | STRICT={len(strict)} "
            f"LOOSE={len(loose)} NO_MATCH=0 -> report: {report}"
        )
    else:
        print(
            f"Guard: {len(results)} claims | STRICT={len(strict)} "
            f"LOOSE=0 NO_MATCH=0 -> all clean"
        )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Number Guard - validate digest numbers vs source")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("check", help="check a digest file")
    pc.add_argument("digest_path")
    pc.set_defaults(func=_cmd_check)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
