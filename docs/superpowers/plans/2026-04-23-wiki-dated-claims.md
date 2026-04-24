# Wiki Dated Claims + Supersession — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-claim dating (`em: YYYY-MM-DD`), explicit supersession modalities, and three detection mechanisms (reactive-at-ingest, periodic lint, optional watchlist) so that stale information on wiki pages is surfaced and new data explicitly updates old claims.

**Architecture:** Three orthogonal detection paths share a common `(fonte: X, em: YYYY-MM-DD)` citation format. Path A edits existing wiki_update prompts; Path B is a new Python lint tool; Path C is a new Python watch runner. No ingest pipeline changes.

**Tech Stack:** Markdown (wiki pages, docs), JSON (config + state), Python 3 stdlib (argparse, re, pathlib, json, dataclasses), Bash (thin CLI wrappers), pytest for tests.

**Working directory:** All commands assume `cwd = equity-wiki/` (the git repo root). `cd` there before starting.

**Spec reference:** `docs/superpowers/specs/2026-04-23-wiki-dated-claims-design.md`

---

## File Map

**Phase 1 — Policy**
- Modify `SCHEMA.md` — add "Dated Claims", "Supersession", "Watchlist" sections; extend "Lint" with §11
- Modify `CLAUDE.md` — document `lint.sh` + `watch.sh` commands; add `em:` rule to non-obvious rules

**Phase 2 — Path A (prompts)**
- Modify `tools/prompts/wiki_plan.md` — add `dated_claims_to_review` to plan JSON
- Modify `tools/prompts/wiki_write.md` — add 3-output logic (reafirmado/silent/estrutural) + `[claim-update]` log entry

**Phase 3 — Path B (dated lint)**
- Create `tools/lint_config.json` — thresholds and type inference keywords
- Create `tools/lib/dated_lint.py` — parser, rules, report generator
- Create `tools/lint.sh` — thin CLI wrapper
- Create `tests/test_dated_lint.py` — unit tests
- Create `sources/lint_reports/.gitkeep` — ensure dir exists in git

**Phase 4 — Path C (watchlist)**
- Create `tools/lib/watch_runner.py` — state I/O, cadence gate, URL diff
- Create `tools/watch.sh` — thin CLI wrapper
- Create `tests/test_watch_runner.py` — unit tests
- Create `sources/watch_state/.gitkeep` — ensure dir exists in git

---

## Phase 1 — Policy

### Task 1: SCHEMA.md policy updates

**Files:**
- Modify: `SCHEMA.md` (one insertion after §Source Citations, one insertion after §Source Citations for Supersession, one insertion after §Wikilinks for Watchlist, one extension in §Lint)

- [ ] **Step 1.1: Read SCHEMA.md §Source Citations section**

Run: `sed -n '230,245p' SCHEMA.md`
Expected: see `## Source Citations` heading and four bullet points ending with "Web" bullet.

- [ ] **Step 1.2: Insert "Dated Claims" subsection after §Source Citations**

Locate the line after the last Source Citations bullet (the "Web" line ending in `confiabilidade: oficial|editorial|community`). Insert this block **after** that bullet and **before** the next H2 heading (`## Wikilinks`):

```markdown

### Dated Claims

Claims that can become factually wrong over time without the period changing carry an explicit `em: YYYY-MM-DD` in the citation:

- `(fonte: digested/Texto Reforma tributaria jan-2025_summary.md, em: 2025-01-16)` — `em:` is the date the information is **true in the real world** (publication date of a law/MP/LC, announcement date of corporate guidance, effective date of a portaria). It is **not** the ingest date.
- Ingest date stays in `manifests/{empresa}.json :: sources[].ingested_on`. Do not replicate it on the claim.

| Claim type | Gets `em:`? | Example |
|---|---|---|
| Alíquota, regra fiscal, dispositivo de lei | yes | `em: 2025-01-16` (LC 214/2025) |
| Guidance corporativo forward-looking | yes | `em: 2026-04-10` |
| Valor regulatório (teto MCMV, faixa) | yes | `em: 2024-10-03` |
| Meta operacional datada (frota, capex) | yes | `em: 2026-03-15` |
| Número de DF por período (margem 3T25, ROE) | no | período já codifica a data |
| Definição conceitual ("CBS substitui PIS/Cofins") | no | atemporal |

Rule of thumb for the LLM when writing a claim: if the claim can be factually wrong tomorrow without the accounting period changing, it carries `em:`. If it is tied to an explicit accounting period or is definitional, it does not.
```

- [ ] **Step 1.3: Insert "Supersession" section between §Source Citations and §Wikilinks**

After the block from Step 1.2 (and before `## Wikilinks`), insert:

```markdown

## Supersession

When new information updates a dated claim, the LLM chooses one of two modalities based on the nature of the change.

### Modality 1 — Silent overwrite (default)

For guidance refreshes, number updates, or effective date changes without regime changes. Old claim removed, new claim written, `em:` updated. History lives in git log.

```
antes: Alíquota reduzida em 50% (fonte: X, em: 2025-01-16)
depois: Alíquota reduzida em 60% (fonte: Y, em: 2026-08-10)
```

### Modality 2 — Structural supersession ("antes × depois")

For regime changes, law amendments with transition rules, or restructured tariffs. The LLM writes an inline table or section comparing the old and new states — because the contrast itself is the analytical content. See [section_232.md](section_232.md):18-29 for an example pattern ("Revisão de abril/2026 — antes × depois").

**Triggers for Modality 2:**
1. The change invalidates an analytical premise (not just the number), OR
2. The old claim is referenced from other pages via wikilink/cross-cite (silent overwrite would break cross-page consistency).

**Not used:** strikethrough inline, HTML-comment history, separate "history" pages. Git log preserves evolution; the page stays readable.
```

- [ ] **Step 1.4: Insert "Watchlist" section after §Wikilinks**

Locate the line ending with `Wikilinks are for the wiki layer only` (the last line of §Wikilinks). Insert **after** that line and **before** the next H2 (`## Quality Principles`):

```markdown

## Watchlist

Opt-in mechanism for pages with claims that can change outside the CVM/Notion/calls ingest pipeline (laws, regulations, corporate forward-looking statements not yet reported in a filing).

### Declaration

Frontmatter gains an optional `watches:` array:

```yaml
---
type: concept
aliases: [CBS, IBS, LC 214/2025]
watches:
  - query: "LC 214/2025 alteração alíquota"
    sites: [planalto.gov.br, mattosfilho.com.br]
    cadence: weekly
  - query: "reforma tributária incorporadora IBS CBS 2026"
    sites: [valor.globo.com, infomoney.com.br]
    cadence: monthly
sources: [...]
updated: 2026-04-22
---
```

Fields: `query` (string for WebSearch), `sites` (domain list restricting the search), `cadence` (`weekly` | `monthly` | `quarterly`).

### Flow

`tools/watch.sh` → `tools/lib/watch_runner.py` → reads pages with `watches:` → checks each entry against its cadence (via `sources/watch_state/{page_slug}.json`) → runs a WebSearch restricted to the `sites:` → diffs results against `known_urls` in state → emits `[watch-hit]` entries to the next lint report.

**Not auto-ingested.** The runner signals only. The human decides whether to pull the hit through `fetch_notion.sh` or `fetch.sh`.
```

- [ ] **Step 1.5: Extend §Lint with item §11**

Locate SCHEMA.md §Lint section (numbered items 1-10). Append a new item §11 before the "Report in `log.md`" closing line:

```markdown
11. **Dated claim staleness** — parse `(fonte: X, em: YYYY-MM-DD)` across all pages and flag:
    - (a) *Age threshold exceeded*: `em_date + threshold < today` and no newer source on the same topic. Severity `warn`. Thresholds: legal/regulatório 12 months, guidance 6 months, metric absoluto 3 months (configurable via `tools/lint_config.json`).
    - (b) *Newer source available*: a `digested/`/`full/`/`structured/` file exists with `ingested_on > em_date` and matches the page's empresa/concept. Severity `action`.
    - (c) *Cross-page contradiction*: two pages with numerically conflicting claims on the same item, different `em:` dates. Severity `action`.
    - (d) *Missing `em:`*: claim contains a number plus a temporal verb (`vigente`, `a partir de`, `até`) but has no `em:`. Severity `hint`.
```

- [ ] **Step 1.6: Verify SCHEMA.md is well-formed**

Run: `grep -nE "^## " SCHEMA.md | head -40`
Expected: See `## Dated Claims` does NOT appear (it's H3 under Source Citations). See `## Supersession` after `## Source Citations`. See `## Watchlist` after `## Wikilinks`.

- [ ] **Step 1.7: Commit**

```bash
git add SCHEMA.md
git commit -m "docs(schema): add Dated Claims, Supersession, Watchlist + Lint §11"
```

---

### Task 2: CLAUDE.md operational updates

**Files:**
- Modify: `CLAUDE.md` (add commands section entry + non-obvious rule)

- [ ] **Step 2.1: Add `lint.sh` command block**

Locate the `### Query data` section header (around CLAUDE.md:138). Insert a new section **before** `### Query data`:

```markdown
### Dated-claim lint

```bash
# Full report — all pages, all severities
bash tools/lint.sh

# Filter severity
bash tools/lint.sh --severity action   # only action and above
bash tools/lint.sh --severity hint     # everything

# Single page
bash tools/lint.sh --page cyrela.md
```

Scans every `*.md` at the wiki root for `(fonte: X, em: YYYY-MM-DD)` citations and applies four rules (age threshold, newer source available, cross-page contradiction, missing `em:`). Writes report to `sources/lint_reports/YYYY-MM-DD.md` and appends a `[lint]` audit line to `log.md`. Thresholds live in `tools/lint_config.json`.

### Watchlist

```bash
# Run all eligible watches (respects cadence)
bash tools/watch.sh

# Force all entries regardless of cadence
bash tools/watch.sh --force

# Single page
bash tools/watch.sh --page reforma_tributaria.md
```

Reads `watches:` frontmatter on wiki pages, runs restricted WebSearch via `claude --print`, diffs hits against `sources/watch_state/{page_slug}.json`, emits `[watch-hit]` entries to the next lint report. Never ingests automatically — signals only.
```

- [ ] **Step 2.2: Add `em:` rule to "Non-obvious rules"**

Locate the bullet list under `## Non-obvious rules` (CLAUDE.md:284-297). After the existing `**Citations**` bullet (the one that describes `(fonte: ...)` format), insert a new bullet:

```markdown
- **Dated claims** — any claim that can become factually wrong without the period changing (alíquotas, regras fiscais, guidance, metas datadas, valores regulatórios) carries `em: YYYY-MM-DD` in the citation: `(fonte: X, em: 2026-04-10)`. `em:` is the real-world effective date, not the ingest date. See `SCHEMA.md §Dated Claims` for criteria and `SCHEMA.md §Supersession` for update modalities.
```

- [ ] **Step 2.3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude-md): document lint.sh, watch.sh, em: rule"
```

---

## Phase 2 — Path A (prompts)

### Task 3: wiki_plan.md — `dated_claims_to_review` field

**Files:**
- Modify: `tools/prompts/wiki_plan.md`

- [ ] **Step 3.1: Extend the "Your task" section**

Locate the "Your task" section (line 29) and the numbered list below it. After item 3 ("Which pages to SKIP"), add a new item 4:

```markdown
4. **Which dated claims on each page may be invalidated** — for every page in `create`/`update`, scan the existing page content (if any) and the digesteds being applied. List every dated claim (citations of the form `(fonte: ..., em: YYYY-MM-DD)`) whose underlying fact could plausibly be changed by the new digest. Include even uncertain matches; it is better to over-flag than miss. Write the field as `dated_claims_to_review: []` (explicit empty) when there are no candidates — never omit.
```

- [ ] **Step 3.2: Update the JSON output example**

Locate the `===WIKI_PLAN_START===` block (around line 50). Replace it with:

```markdown
===WIKI_PLAN_START===
{
  "create": [
    {
      "page": "example.md",
      "type": "entity",
      "digesteds": ["empresa_dfp_2025_summary.md", "empresa_release_4T25_summary.md"],
      "dated_claims_to_review": []
    }
  ],
  "update": [
    {
      "page": "reforma_tributaria.md",
      "type": "concept",
      "digesteds": ["notion_nova_IN_RFB_summary.md"],
      "dated_claims_to_review": [
        {
          "claim_excerpt": "alíquota reduzida em 50%",
          "current_em": "2025-01-16",
          "reason": "digest describes new IN RFB that may alter effective rate"
        }
      ]
    }
  ],
  "skip": [
    {"page": "mcmv.md", "reason": "no new data affecting this concept"}
  ]
}
===WIKI_PLAN_END===
```

- [ ] **Step 3.3: Add a rule about `dated_claims_to_review`**

Append to the `## Rules` section (end of file):

```markdown
- For every `create`/`update` entry, include `dated_claims_to_review` explicitly — empty array if none apply, never omit the field.
- Parse existing pages looking for citations of the form `(fonte: ..., em: YYYY-MM-DD)`. For each, judge whether any of the digesteds being applied could change that claim. If yes, include it in `dated_claims_to_review` with `claim_excerpt` (≤120 chars of surrounding text), `current_em` (the date from the citation), and `reason` (one line).
```

- [ ] **Step 3.4: Commit**

```bash
git add tools/prompts/wiki_plan.md
git commit -m "feat(wiki_plan): surface dated_claims_to_review in plan JSON"
```

---

### Task 4: wiki_write.md — 3-output logic + `[claim-update]` log

**Files:**
- Modify: `tools/prompts/wiki_write.md`

- [ ] **Step 4.1: Add a new section "Dated claims" after the "Citation format" section**

Locate `## Citation format` block (around line 72). After the three bullets (Numeric/Qualitative/Digested), insert:

```markdown

### Dated claims — `em:` marker

Any claim that can become factually wrong without its period changing carries `em: YYYY-MM-DD` in the citation: `(fonte: X, em: 2026-04-10)`. `em:` is the **real-world effective date** (publication date of a law, date of a guidance release, effective date of a portaria), not the ingest date.

Apply `em:` to: alíquotas, regras fiscais, dispositivos de lei, guidance corporativo forward-looking, valores regulatórios (teto MCMV, faixa de renda), metas operacionais datadas.

Do NOT apply `em:` to: definitions, mechanical descriptions, period-coded financial numbers (margem 3T25, ROE 2024), names of laws (the name is immutable).
```

- [ ] **Step 4.2: Add a "Supersession handling" section before "## Rules"**

Locate the `## Rules` heading (near end of file). Insert **before** it:

```markdown

## Supersession handling (when updating dated claims)

If the plan input includes `dated_claims_to_review` (non-empty array), for **each entry** you must:

1. Read the claim in full context (the plan gives you `claim_excerpt` and `current_em`; read the page to find the surrounding paragraph/table).
2. Read the relevant digest(s) (named in the plan's `digesteds` for this page).
3. Decide one of three outcomes:
   - **Reafirmado** — the claim is still true. Bump `em:` to the digest's effective date. No content change beyond the date.
   - **Atualizado silent (Modalidade 1)** — the number/date changed but the regime is the same. Overwrite the value in place, update `em:`. Used for guidance refreshes, incremental rule changes.
   - **Atualizado estrutural (Modalidade 2)** — a regime changed. Write an inline "antes × depois" table or comparison section. Use this when the change invalidates an analytical premise (not just the number) OR the old claim is cross-cited from other pages.
4. Append a `[claim-update]` line to `log.md` for each dated claim touched:

```bash
echo "[claim-update] $(date +%F) {{PAGE_NAME}} \"<claim_excerpt>\" em:<old>→<new> modo:<reafirmado|silent|estrutural>" >> log.md
```

Preserve **existing** dated claims that the plan did NOT flag for review — do not remove or strip their `em:` markers.

When you **introduce new dated claims** during this write (even if the plan did not flag anything), add `em:` per the "Dated claims" guidance above. No log entry is required for freshly-authored claims — `[claim-update]` is for supersession only.
```

- [ ] **Step 4.3: Verify by reading the modified file**

Run: `grep -nE "^## " tools/prompts/wiki_write.md`
Expected: headings in order — Context, Source digesteds, Existing page, All wiki pages, What to produce, Citation format, Supersession handling, Rules.

- [ ] **Step 4.4: Commit**

```bash
git add tools/prompts/wiki_write.md
git commit -m "feat(wiki_write): add em: marker and supersession modalities"
```

---

## Phase 3 — Path B (dated lint)

### Task 5: lint_config.json + reports directory

**Files:**
- Create: `tools/lint_config.json`
- Create: `sources/lint_reports/.gitkeep`

- [ ] **Step 5.1: Create `tools/lint_config.json`**

Create file with exact content:

```json
{
  "thresholds_months": {
    "legal_regulatorio": 12,
    "guidance_corporativo": 6,
    "metric_absoluto": 3,
    "default": 12
  },
  "tipo_inference": {
    "legal_regulatorio": {
      "page_types": ["concept"],
      "keywords": ["alíquota", "LC ", "MP ", "portaria", "decreto", "lei ", "IN ", "RFB", "tarifa", "reforma", "regulação", "vigente"]
    },
    "guidance_corporativo": {
      "page_types": ["entity"],
      "keywords": ["guidance", "meta", "target", "projeção", "capex", "orçamento", "previsão"]
    },
    "metric_absoluto": {
      "page_types": ["entity", "sector"],
      "keywords": ["banco de terrenos", "frota", "funcionários", "lojas", "unidades", "ativos", "caixa"]
    }
  },
  "missing_em_heuristic": {
    "temporal_verbs": ["vigente", "a partir de", "até", "desde", "válido para"],
    "requires_number": true
  }
}
```

- [ ] **Step 5.2: Create `sources/lint_reports/.gitkeep`**

```bash
mkdir -p sources/lint_reports
touch sources/lint_reports/.gitkeep
```

- [ ] **Step 5.3: Commit**

```bash
git add tools/lint_config.json sources/lint_reports/.gitkeep
git commit -m "feat(lint): config file and reports directory"
```

---

### Task 6: Walking skeleton — parser + Age Threshold rule + report + CLI

Goal: end-to-end pipeline with one rule. Subsequent tasks add rules without touching the skeleton.

**Files:**
- Create: `tools/lib/dated_lint.py`
- Create: `tools/lint.sh`
- Create: `tests/test_dated_lint.py`

- [ ] **Step 6.1: Write failing test for `parse_claims`**

Create `tests/test_dated_lint.py`:

```python
"""Tests for tools/lib/dated_lint.py."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.lib import dated_lint as dl  # noqa: E402


def test_parse_claim_with_em(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "# Demo\n\nAlíquota reduzida em 50% (fonte: digested/x_summary.md, em: 2025-01-16).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    assert len(claims) == 1
    c = claims[0]
    assert c.page.name == "demo.md"
    assert c.line == 3
    assert c.fonte == "digested/x_summary.md"
    assert c.em == date(2025, 1, 16)
    assert "Alíquota reduzida em 50%" in c.excerpt


def test_parse_claim_without_em(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "Definição (fonte: digested/defs_summary.md).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    assert len(claims) == 1
    assert claims[0].em is None
    assert claims[0].fonte == "digested/defs_summary.md"


def test_parse_skips_code_blocks(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "Prose (fonte: real.md, em: 2025-01-01).\n"
        "```\n"
        "Not a claim (fonte: fake.md, em: 2024-01-01).\n"
        "```\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    assert len(claims) == 1
    assert claims[0].fonte == "real.md"
```

- [ ] **Step 6.2: Run tests to confirm failure**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: `ModuleNotFoundError: No module named 'tools.lib.dated_lint'`

- [ ] **Step 6.3: Create `tools/lib/dated_lint.py` with parser skeleton**

```python
"""Dated Lint — parse `(fonte: X, em: YYYY-MM-DD)` citations across the wiki
and flag claims that are stale, contradictory, or missing dates.

Public API:
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
CITATION_RE = re.compile(
    r"\(fonte:\s*(?P<fonte>[^,)]+?)(?:,\s*em:\s*(?P<em>\d{4}-\d{2}-\d{2}))?\)"
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


def main() -> int:
    # placeholder; filled in Step 6.9
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 6.4: Run parser tests to confirm they pass**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 3 passed.

- [ ] **Step 6.5: Write failing tests for Age Threshold rule**

Append to `tests/test_dated_lint.py`:

```python
def _load_config():
    cfg = REPO_ROOT / "tools" / "lint_config.json"
    return json.loads(cfg.read_text(encoding="utf-8"))


def test_age_threshold_flags_old_legal_claim(tmp_path):
    page = tmp_path / "reforma_tributaria.md"
    page.write_text(
        "---\ntype: concept\n---\n\nAlíquota reduzida (fonte: x.md, em: 2020-01-01).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    config = _load_config()
    flags = dl.age_threshold_flags(claims, config, today=date(2026, 4, 23))
    assert len(flags) == 1
    assert flags[0].rule == "age_threshold"
    assert flags[0].severity == "warn"


def test_age_threshold_ignores_claims_within_threshold(tmp_path):
    page = tmp_path / "cyrela.md"
    page.write_text(
        "---\ntype: entity\n---\n\nGuidance de capex (fonte: x.md, em: 2026-03-01).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    config = _load_config()
    flags = dl.age_threshold_flags(claims, config, today=date(2026, 4, 23))
    assert flags == []


def test_age_threshold_ignores_claim_without_em(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text("Conceito (fonte: x.md).\n", encoding="utf-8")
    claims = dl.parse_claims(page)
    config = _load_config()
    flags = dl.age_threshold_flags(claims, config, today=date(2026, 4, 23))
    assert flags == []
```

- [ ] **Step 6.6: Run tests to confirm failure**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 3 new tests fail with `AttributeError: module 'tools.lib.dated_lint' has no attribute 'age_threshold_flags'`.

- [ ] **Step 6.7: Implement `age_threshold_flags` + helpers**

Edit `tools/lib/dated_lint.py`. Before `def main()`, insert:

```python
def _read_frontmatter(page_path: Path) -> dict:
    """Extract YAML frontmatter as a dict. Returns empty dict if none found.

    Minimal parser: only `key: value` and `key: [a, b]` on single lines.
    Nested structures (used by `watches:`) are returned as raw string blocks
    under their top-level key and not parsed further here.
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

    Priority: keyword match in excerpt > page_type match > default.
    First tipo whose keyword matches the excerpt wins.
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
        if _months_between(c.em, today) >= threshold:
            flags.append(
                Flag(
                    claim=c,
                    rule="age_threshold",
                    severity="warn",
                    detail=(
                        f"em={c.em.isoformat()} is {_months_between(c.em, today)} months "
                        f"old (threshold for tipo={tipo} is {threshold})"
                    ),
                )
            )
    return flags
```

- [ ] **Step 6.8: Run tests to confirm they pass**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 6 passed.

- [ ] **Step 6.9: Add `scan_wiki`, `write_report`, and `main` CLI**

In `tools/lib/dated_lint.py`, replace the placeholder `main()` and add two new functions above it:

```python
def scan_wiki(root: Path) -> list[ClaimCitation]:
    """Parse all top-level wiki pages under `root` (excluding docs/, sources/, tools/)."""
    skip_dirs = {"docs", "sources", "tools", "tests", "logs", ".git", ".obsidian",
                 ".playwright-cli", ".claude", ".pytest_cache", "__pycache__"}
    claims: list[ClaimCitation] = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and entry.name in skip_dirs:
            continue
        if entry.is_file() and entry.suffix == ".md":
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
```

- [ ] **Step 6.10: Write test for `scan_wiki` + `write_report` integration**

Append to `tests/test_dated_lint.py`:

```python
def test_scan_wiki_skips_sources_and_docs(tmp_path):
    (tmp_path / "sources").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "sources" / "nope.md").write_text(
        "(fonte: x, em: 2020-01-01)\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "also_nope.md").write_text(
        "(fonte: y, em: 2020-01-01)\n", encoding="utf-8"
    )
    (tmp_path / "real.md").write_text(
        "(fonte: z, em: 2020-01-01)\n", encoding="utf-8"
    )
    claims = dl.scan_wiki(tmp_path)
    assert len(claims) == 1
    assert claims[0].fonte == "z"


def test_write_report_empty(tmp_path):
    report = tmp_path / "r.md"
    dl.write_report([], report, as_of=date(2026, 4, 23))
    out = report.read_text(encoding="utf-8")
    assert "Lint Report — 2026-04-23" in out
    assert "No flags raised" in out


def test_write_report_groups_by_page(tmp_path):
    page_a = tmp_path / "a.md"
    page_b = tmp_path / "b.md"
    page_a.write_text("x", encoding="utf-8")
    page_b.write_text("y", encoding="utf-8")
    c_a = dl.ClaimCitation(page=page_a, line=1, excerpt="aa", fonte="f", em=None)
    c_b = dl.ClaimCitation(page=page_b, line=1, excerpt="bb", fonte="g", em=None)
    flags = [
        dl.Flag(claim=c_b, rule="r", severity="warn", detail="d1"),
        dl.Flag(claim=c_a, rule="r", severity="action", detail="d2"),
    ]
    report = tmp_path / "r.md"
    dl.write_report(flags, report)
    out = report.read_text(encoding="utf-8")
    assert out.index("## a.md") < out.index("## b.md")
```

- [ ] **Step 6.11: Run the full test suite**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 9 passed.

- [ ] **Step 6.12: Create `tools/lint.sh` wrapper**

Create file with content:

```bash
#!/usr/bin/env bash
# Dated-claim lint — wraps tools/lib/dated_lint.py
#
# Usage:
#   bash tools/lint.sh                      # full report, all severities
#   bash tools/lint.sh --severity action    # only action
#   bash tools/lint.sh --page cyrela.md     # single page
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
exec python "$REPO_ROOT/tools/lib/dated_lint.py" "$@"
```

Make executable:

```bash
chmod +x tools/lint.sh
```

- [ ] **Step 6.13: Smoke test — run lint on the real wiki**

Run: `bash tools/lint.sh`
Expected: `Report: sources/lint_reports/YYYY-MM-DD.md` followed by totals. No crash. The report will likely be empty (or near-empty) because no existing page has `em:` markers yet — this is expected.

Verify report file exists:
Run: `ls sources/lint_reports/`
Expected: file named `YYYY-MM-DD.md` plus `.gitkeep`.

- [ ] **Step 6.14: Commit**

```bash
git add tools/lib/dated_lint.py tools/lint.sh tests/test_dated_lint.py
git commit -m "feat(lint): skeleton with parser and age_threshold rule"
```

---

### Task 7: Missing `em:` rule

**Files:**
- Modify: `tools/lib/dated_lint.py` (add function + wire into main)
- Modify: `tests/test_dated_lint.py` (add tests)

- [ ] **Step 7.1: Write failing tests**

Append to `tests/test_dated_lint.py`:

```python
def test_missing_em_flag_triggered(tmp_path):
    page = tmp_path / "mcmv.md"
    page.write_text(
        "Teto de R$ 350k vigente para Faixa 3 (fonte: x.md).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    config = _load_config()
    flags = dl.missing_em_flags(claims, config)
    assert len(flags) == 1
    assert flags[0].rule == "missing_em"
    assert flags[0].severity == "hint"


def test_missing_em_ignored_when_em_present(tmp_path):
    page = tmp_path / "mcmv.md"
    page.write_text(
        "Teto vigente R$ 350k (fonte: x.md, em: 2026-01-15).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    config = _load_config()
    flags = dl.missing_em_flags(claims, config)
    assert flags == []


def test_missing_em_requires_number(tmp_path):
    page = tmp_path / "defs.md"
    page.write_text(
        "Regime vigente para incorporadoras (fonte: x.md).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    config = _load_config()
    flags = dl.missing_em_flags(claims, config)
    assert flags == []  # has temporal verb but no number
```

- [ ] **Step 7.2: Run to confirm failure**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 3 new tests fail with `AttributeError: missing_em_flags`.

- [ ] **Step 7.3: Implement `missing_em_flags`**

In `tools/lib/dated_lint.py`, after `age_threshold_flags`, add:

```python
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
```

- [ ] **Step 7.4: Wire into `main()`**

In `main()`, after the line `all_flags.extend(age_threshold_flags(claims, config))`, add:

```python
    all_flags.extend(missing_em_flags(claims, config))
```

- [ ] **Step 7.5: Run tests**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 12 passed.

- [ ] **Step 7.6: Commit**

```bash
git add tools/lib/dated_lint.py tests/test_dated_lint.py
git commit -m "feat(lint): missing_em rule (temporal verb + number + no em:)"
```

---

### Task 8: Newer source available rule

**Files:**
- Modify: `tools/lib/dated_lint.py`
- Modify: `tests/test_dated_lint.py`

- [ ] **Step 8.1: Write failing test**

Append to `tests/test_dated_lint.py`:

```python
def test_newer_source_flag_triggered(tmp_path):
    # Create wiki page with claim em: 2024-01-01 about cyrela
    (tmp_path / "cyrela.md").write_text(
        "---\ntype: entity\naliases: [Cyrela, CYRE3]\n---\n\n"
        "Guidance (fonte: digested/cyrela_dfp_2023_summary.md, em: 2024-01-01).\n",
        encoding="utf-8",
    )
    # Create a newer digest for cyrela
    digested = tmp_path / "sources" / "digested"
    digested.mkdir(parents=True)
    (digested / "cyrela_dfp_2025_summary.md").write_text(
        "newer digest\n", encoding="utf-8"
    )
    # Manifest for cyrela
    manifests = tmp_path / "sources" / "manifests"
    manifests.mkdir(parents=True)
    (manifests / "cyrela.json").write_text(
        json.dumps(
            {
                "empresa": "cyrela",
                "aliases": ["Cyrela", "CYRE3"],
                "sources": [
                    {
                        "type": "dfp",
                        "asof": "2025",
                        "ingested_on": "2026-03-15",
                        "digested": "sources/digested/cyrela_dfp_2025_summary.md",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    page = tmp_path / "cyrela.md"
    claims = dl.parse_claims(page)
    flags = dl.newer_source_flags(claims, tmp_path)
    assert len(flags) == 1
    assert flags[0].rule == "newer_source"
    assert flags[0].severity == "action"


def test_newer_source_ignored_when_no_alias_match(tmp_path):
    (tmp_path / "cyrela.md").write_text(
        "---\ntype: entity\naliases: [Cyrela]\n---\n\n"
        "Claim (fonte: x.md, em: 2024-01-01).\n",
        encoding="utf-8",
    )
    manifests = tmp_path / "sources" / "manifests"
    manifests.mkdir(parents=True)
    (manifests / "tenda.json").write_text(
        json.dumps(
            {
                "empresa": "tenda",
                "aliases": ["Tenda", "TEND3"],
                "sources": [
                    {"type": "dfp", "asof": "2025", "ingested_on": "2026-03-15"}
                ],
            }
        ),
        encoding="utf-8",
    )
    page = tmp_path / "cyrela.md"
    claims = dl.parse_claims(page)
    flags = dl.newer_source_flags(claims, tmp_path)
    assert flags == []
```

- [ ] **Step 8.2: Run to confirm failure**

Run: `python -m pytest tests/test_dated_lint.py::test_newer_source_flag_triggered -v`
Expected: `AttributeError: newer_source_flags`.

- [ ] **Step 8.3: Implement `newer_source_flags`**

In `tools/lib/dated_lint.py`, after `missing_em_flags`, add:

```python
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
    """Flag claims whose page has a matching manifest entry with ingested_on > em."""
    manifests = _load_manifests(root)
    flags: list[Flag] = []
    for c in claims:
        if c.em is None:
            continue
        page_aliases = _page_aliases(c.page)
        newest_ingested: Optional[date] = None
        newest_source: Optional[str] = None
        for m in manifests:
            m_aliases = {str(a).lower() for a in m.get("aliases", [])}
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
                    newest_source = src.get("digested") or src.get("full") or "<unknown>"
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
```

- [ ] **Step 8.4: Wire into `main()`**

In `main()`, after `all_flags.extend(missing_em_flags(claims, config))`, add:

```python
    all_flags.extend(newer_source_flags(claims, root))
```

- [ ] **Step 8.5: Run tests**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 14 passed.

- [ ] **Step 8.6: Commit**

```bash
git add tools/lib/dated_lint.py tests/test_dated_lint.py
git commit -m "feat(lint): newer_source rule using manifests aliases"
```

---

### Task 9: Cross-page contradiction rule

**Files:**
- Modify: `tools/lib/dated_lint.py`
- Modify: `tests/test_dated_lint.py`

- [ ] **Step 9.1: Write failing test**

Append to `tests/test_dated_lint.py`:

```python
def test_contradiction_across_pages(tmp_path):
    (tmp_path / "mcmv.md").write_text(
        "Teto Faixa 3 R$ 350.000 (fonte: x.md, em: 2025-01-01).\n",
        encoding="utf-8",
    )
    (tmp_path / "pode_entrar.md").write_text(
        "Teto Faixa 3 R$ 380.000 (fonte: y.md, em: 2026-03-01).\n",
        encoding="utf-8",
    )
    claims = dl.scan_wiki(tmp_path)
    flags = dl.contradiction_flags(claims)
    # Two claims -> two flags (one per side) OR one combined flag; accept either
    assert len(flags) >= 1
    assert all(f.rule == "contradiction" for f in flags)
    assert all(f.severity == "action" for f in flags)


def test_no_contradiction_when_values_agree(tmp_path):
    (tmp_path / "a.md").write_text(
        "Teto Faixa 3 R$ 350.000 (fonte: x.md, em: 2025-01-01).\n", encoding="utf-8"
    )
    (tmp_path / "b.md").write_text(
        "Teto Faixa 3 R$ 350.000 (fonte: y.md, em: 2026-03-01).\n", encoding="utf-8"
    )
    claims = dl.scan_wiki(tmp_path)
    flags = dl.contradiction_flags(claims)
    assert flags == []
```

- [ ] **Step 9.2: Run to confirm failure**

Run: `python -m pytest tests/test_dated_lint.py::test_contradiction_across_pages -v`
Expected: `AttributeError: contradiction_flags`.

- [ ] **Step 9.3: Implement `contradiction_flags`**

In `tools/lib/dated_lint.py`, after `newer_source_flags`, add:

```python
_KEY_PHRASE_RE = re.compile(r"[A-Za-zÀ-ÿ]{4,}(?:\s+[A-Za-zÀ-ÿ0-9]+){0,3}")
_VALUE_RE = re.compile(
    r"(?:R\$\s*)?([\d]{1,3}(?:[.\s]\d{3})+|\d+)(?:,(\d+))?\s*(bi|mm|mil|milhões|mi|k|%)?",
    re.IGNORECASE,
)


def _normalize_value(match: re.Match) -> Optional[float]:
    """Convert a matched number with unit to a float in canonical units.

    Percentage stays in pct. Monetary is normalized to reais (bi=1e9, mm=1e6, mil=1e3).
    Returns None if parse fails.
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
    if unit == "%":
        return raw
    mult = {"bi": 1e9, "mm": 1e6, "mi": 1e6, "milhões": 1e6, "mil": 1e3, "k": 1e3}.get(unit, 1.0)
    return raw * mult


def _extract_key_phrase(excerpt: str) -> Optional[str]:
    """Pick a 2-5 word key phrase from the excerpt (used as contradiction bucket key).

    Strategy: longest capitalised/alpha phrase near the end of the excerpt.
    """
    candidates = _KEY_PHRASE_RE.findall(excerpt)
    if not candidates:
        return None
    return candidates[-1].strip().lower()


def contradiction_flags(claims: list[ClaimCitation]) -> list[Flag]:
    """Flag pairs of claims on different pages with same key phrase but different values."""
    buckets: dict[str, list[tuple[ClaimCitation, float]]] = {}
    for c in claims:
        m = _VALUE_RE.search(c.excerpt)
        if not m:
            continue
        val = _normalize_value(m)
        if val is None:
            continue
        key = _extract_key_phrase(c.excerpt)
        if not key:
            continue
        buckets.setdefault(key, []).append((c, val))

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
```

- [ ] **Step 9.4: Wire into `main()`**

In `main()`, after `all_flags.extend(newer_source_flags(claims, root))`, add:

```python
    all_flags.extend(contradiction_flags(claims))
```

- [ ] **Step 9.5: Run tests**

Run: `python -m pytest tests/test_dated_lint.py -v`
Expected: 16 passed.

- [ ] **Step 9.6: Commit**

```bash
git add tools/lib/dated_lint.py tests/test_dated_lint.py
git commit -m "feat(lint): contradiction rule across pages"
```

---

## Phase 4 — Path C (watchlist)

### Task 10: State I/O + cadence gate

**Files:**
- Create: `tools/lib/watch_runner.py`
- Create: `tests/test_watch_runner.py`
- Create: `sources/watch_state/.gitkeep`

- [ ] **Step 10.1: Create watch_state directory**

```bash
mkdir -p sources/watch_state
touch sources/watch_state/.gitkeep
```

- [ ] **Step 10.2: Write failing tests for state I/O + cadence**

Create `tests/test_watch_runner.py`:

```python
"""Tests for tools/lib/watch_runner.py."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.lib import watch_runner as wr  # noqa: E402


def test_state_roundtrip_empty(tmp_path):
    state_dir = tmp_path / "watch_state"
    state = wr.load_state(state_dir, page_slug="demo")
    assert state == {"page": "demo", "entries": []}


def test_state_roundtrip_saves_and_reloads(tmp_path):
    state_dir = tmp_path / "watch_state"
    s = {
        "page": "demo",
        "entries": [
            {
                "query": "q",
                "sites": ["a.com"],
                "cadence": "weekly",
                "last_run": "2026-04-01",
                "known_urls": {"https://x": {"title": "t", "snippet": "s", "published": "2026-04-01"}},
            }
        ],
    }
    wr.save_state(state_dir, page_slug="demo", state=s)
    loaded = wr.load_state(state_dir, page_slug="demo")
    assert loaded == s


def test_cadence_gate_blocks_fresh_weekly(tmp_path):
    last = date(2026, 4, 20)
    today = date(2026, 4, 23)
    assert wr.should_run("weekly", last, today=today) is False


def test_cadence_gate_allows_expired_weekly(tmp_path):
    last = date(2026, 4, 10)
    today = date(2026, 4, 23)
    assert wr.should_run("weekly", last, today=today) is True


def test_cadence_gate_monthly_quarterly():
    today = date(2026, 4, 23)
    # monthly
    assert wr.should_run("monthly", date(2026, 4, 1), today=today) is False
    assert wr.should_run("monthly", date(2026, 2, 28), today=today) is True
    # quarterly
    assert wr.should_run("quarterly", date(2026, 2, 1), today=today) is False
    assert wr.should_run("quarterly", date(2025, 12, 1), today=today) is True


def test_cadence_gate_no_last_run():
    assert wr.should_run("weekly", None, today=date(2026, 4, 23)) is True
```

- [ ] **Step 10.3: Run tests to confirm failure**

Run: `python -m pytest tests/test_watch_runner.py -v`
Expected: `ModuleNotFoundError: No module named 'tools.lib.watch_runner'`.

- [ ] **Step 10.4: Create `tools/lib/watch_runner.py`**

```python
"""Watch Runner — check opt-in watched pages for external signal changes.

Public API:
    load_state(state_dir, page_slug)        -> dict
    save_state(state_dir, page_slug, state) -> None
    should_run(cadence, last_run, today)    -> bool
    diff_urls(known, fresh)                 -> list[dict]  (new or updated)
    run_watch(page_path, state_dir, today)  -> list[dict]  (hits)
    scan_wiki(root, today)                  -> list[dict]  (hits across all pages)

CLI:
    python tools/lib/watch_runner.py [--page P] [--force]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]

CADENCE_DAYS = {"weekly": 7, "monthly": 30, "quarterly": 90}


def load_state(state_dir: Path, page_slug: str) -> dict:
    path = state_dir / f"{page_slug}.json"
    if not path.exists():
        return {"page": page_slug, "entries": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state_dir: Path, page_slug: str, state: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / f"{page_slug}.json"
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def should_run(cadence: str, last_run: Optional[date], today: Optional[date] = None) -> bool:
    if today is None:
        today = date.today()
    if last_run is None:
        return True
    days = CADENCE_DAYS.get(cadence, CADENCE_DAYS["monthly"])
    return (today - last_run) >= timedelta(days=days)


def main() -> int:
    # filled in Task 12
    print("not yet implemented", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 10.5: Run tests**

Run: `python -m pytest tests/test_watch_runner.py -v`
Expected: 5 passed.

- [ ] **Step 10.6: Commit**

```bash
git add tools/lib/watch_runner.py tests/test_watch_runner.py sources/watch_state/.gitkeep
git commit -m "feat(watch): state I/O and cadence gate"
```

---

### Task 11: URL diff logic

**Files:**
- Modify: `tools/lib/watch_runner.py`
- Modify: `tests/test_watch_runner.py`

- [ ] **Step 11.1: Write failing tests**

Append to `tests/test_watch_runner.py`:

```python
def test_diff_urls_empty_known():
    fresh = [
        {"url": "https://a", "title": "A", "snippet": "...", "published_date": "2026-04-20"}
    ]
    hits = wr.diff_urls({}, fresh)
    assert len(hits) == 1
    assert hits[0]["url"] == "https://a"


def test_diff_urls_all_known():
    known = {
        "https://a": {"title": "A", "snippet": "...", "published": "2026-04-20"}
    }
    fresh = [
        {"url": "https://a", "title": "A", "snippet": "...", "published_date": "2026-04-20"}
    ]
    hits = wr.diff_urls(known, fresh)
    assert hits == []


def test_diff_urls_new_and_updated():
    known = {
        "https://a": {"title": "A-old", "snippet": "...", "published": "2026-04-10"}
    }
    fresh = [
        # updated publish date
        {"url": "https://a", "title": "A", "snippet": "...", "published_date": "2026-04-20"},
        # brand new
        {"url": "https://b", "title": "B", "snippet": "...", "published_date": "2026-04-22"},
    ]
    hits = wr.diff_urls(known, fresh)
    urls = {h["url"] for h in hits}
    assert urls == {"https://a", "https://b"}
```

- [ ] **Step 11.2: Run to confirm failure**

Run: `python -m pytest tests/test_watch_runner.py -v`
Expected: 3 new fail with `AttributeError: diff_urls`.

- [ ] **Step 11.3: Implement `diff_urls`**

In `tools/lib/watch_runner.py`, before `def main()`, insert:

```python
def diff_urls(known: dict, fresh: list[dict]) -> list[dict]:
    """Return fresh entries that are new URLs or have a later published_date than known."""
    hits = []
    for f in fresh:
        url = f.get("url")
        if not url:
            continue
        if url not in known:
            hits.append(f)
            continue
        known_pub = known[url].get("published", "")
        fresh_pub = f.get("published_date", "")
        if fresh_pub and fresh_pub > known_pub:
            hits.append(f)
    return hits
```

- [ ] **Step 11.4: Run tests**

Run: `python -m pytest tests/test_watch_runner.py -v`
Expected: 8 passed.

- [ ] **Step 11.5: Commit**

```bash
git add tools/lib/watch_runner.py tests/test_watch_runner.py
git commit -m "feat(watch): URL diff logic (new and updated by published date)"
```

---

### Task 12: Watch runner end-to-end + CLI + watch.sh

**Files:**
- Modify: `tools/lib/watch_runner.py` (add `run_watch`, `scan_wiki`, and fill `main`)
- Create: `tools/watch.sh`
- Modify: `tests/test_watch_runner.py`

- [ ] **Step 12.1: Write failing test for `run_watch` (with mocked search)**

Append to `tests/test_watch_runner.py`:

```python
def test_run_watch_integrates_cadence_and_diff(tmp_path, monkeypatch):
    # Page with one watch entry, no prior state
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "type: concept\n"
        "watches:\n"
        "  - query: test query\n"
        "    sites: [example.com]\n"
        "    cadence: weekly\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )
    state_dir = tmp_path / "watch_state"

    def fake_search(query, sites, today):
        return [
            {"url": "https://example.com/a", "title": "A", "snippet": "...",
             "published_date": "2026-04-22"},
        ]

    monkeypatch.setattr(wr, "search_web", fake_search)
    hits = wr.run_watch(page, state_dir, today=date(2026, 4, 23))
    assert len(hits) == 1
    assert hits[0]["url"] == "https://example.com/a"
    # Second run: state now has the URL -> cadence blocks
    hits2 = wr.run_watch(page, state_dir, today=date(2026, 4, 23))
    assert hits2 == []
```

- [ ] **Step 12.2: Run to confirm failure**

Run: `python -m pytest tests/test_watch_runner.py::test_run_watch_integrates_cadence_and_diff -v`
Expected: `AttributeError: run_watch` (and/or `search_web`).

- [ ] **Step 12.3: Implement `run_watch`, `search_web` stub, `scan_wiki`, `main`**

In `tools/lib/watch_runner.py`, replace `def main()` and add everything above it:

```python
_WATCHES_BLOCK_RE = re.compile(
    r"^watches:\s*\n((?:\s{2,}.*\n?)+)", re.MULTILINE
)
_ENTRY_START_RE = re.compile(r"^\s*-\s*query:\s*(.+?)\s*$")
_FIELD_RE = re.compile(r"^\s*(query|sites|cadence):\s*(.+?)\s*$")


def parse_watches_frontmatter(page_path: Path) -> list[dict]:
    """Extract the `watches:` array from a page's YAML frontmatter.

    Limited YAML parser for this specific shape:
        watches:
          - query: "..."
            sites: [a.com, b.com]
            cadence: weekly
    """
    text = page_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---\n", 4)
    if end == -1:
        return []
    fm_text = text[4:end]
    m = _WATCHES_BLOCK_RE.search(fm_text)
    if not m:
        return []
    block = m.group(1)
    entries: list[dict] = []
    current: Optional[dict] = None
    for raw in block.splitlines():
        if not raw.strip():
            continue
        start_match = _ENTRY_START_RE.match(raw)
        if start_match:
            if current is not None:
                entries.append(current)
            current = {"query": start_match.group(1).strip().strip('"').strip("'")}
            continue
        if current is None:
            continue
        field_match = _FIELD_RE.match(raw)
        if not field_match:
            continue
        key, val = field_match.group(1), field_match.group(2).strip()
        if key == "sites" and val.startswith("[") and val.endswith("]"):
            current["sites"] = [s.strip() for s in val[1:-1].split(",") if s.strip()]
        elif key == "cadence":
            current["cadence"] = val
        elif key == "query":
            current["query"] = val.strip('"').strip("'")
    if current is not None:
        entries.append(current)
    return entries


def search_web(query: str, sites: list[str], today: date) -> list[dict]:
    """Invoke `claude --print` with a WebSearch-scoped prompt; return hits.

    Returned shape: [{url, title, snippet, published_date}].
    """
    site_clause = " OR ".join(f"site:{s}" for s in sites) if sites else ""
    full_query = f"{query} {site_clause}".strip()
    prompt = (
        "You are a web search agent. Use WebSearch with this exact query:\n"
        f'"{full_query}"\n\n'
        "Return ONLY a JSON array (no prose, no backticks) of the 10 most recent hits. "
        'Each item: {"url": "...", "title": "...", "snippet": "...", '
        '"published_date": "YYYY-MM-DD"}. If the page does not disclose a publication '
        'date, use the empty string. Today is '
        f"{today.isoformat()}."
    )
    try:
        proc = subprocess.run(
            ["claude", "--print", "--permission-mode", "bypassPermissions"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180,
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"search_web error: {e}", file=sys.stderr)
        return []
    out = proc.stdout.strip()
    m = re.search(r"\[\s*\{.*\}\s*\]", out, re.DOTALL)
    if not m:
        return []
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return []


def run_watch(
    page_path: Path,
    state_dir: Path,
    today: Optional[date] = None,
    force: bool = False,
) -> list[dict]:
    """Run all watch entries for a page; return aggregated hits."""
    if today is None:
        today = date.today()
    entries = parse_watches_frontmatter(page_path)
    if not entries:
        return []
    page_slug = page_path.stem
    state = load_state(state_dir, page_slug)
    existing_by_query: dict[str, dict] = {
        e["query"]: e for e in state.get("entries", [])
    }

    aggregated_hits: list[dict] = []
    new_entries_state: list[dict] = []
    for entry in entries:
        query = entry["query"]
        cadence = entry.get("cadence", "monthly")
        sites = entry.get("sites", [])
        prior = existing_by_query.get(query, {})
        last_run_raw = prior.get("last_run")
        last_run = date.fromisoformat(last_run_raw) if last_run_raw else None
        known_urls: dict = prior.get("known_urls", {})

        if not force and not should_run(cadence, last_run, today=today):
            new_entries_state.append({
                "query": query,
                "sites": sites,
                "cadence": cadence,
                "last_run": last_run_raw,
                "known_urls": known_urls,
            })
            continue

        fresh = search_web(query, sites, today)
        hits = diff_urls(known_urls, fresh)
        for h in hits:
            aggregated_hits.append({
                "page": page_path.name,
                "query": query,
                "cadence": cadence,
                **h,
            })

        updated_known = dict(known_urls)
        for f in fresh:
            url = f.get("url")
            if not url:
                continue
            updated_known[url] = {
                "title": f.get("title", ""),
                "snippet": f.get("snippet", ""),
                "published": f.get("published_date", ""),
            }
        new_entries_state.append({
            "query": query,
            "sites": sites,
            "cadence": cadence,
            "last_run": today.isoformat(),
            "known_urls": updated_known,
        })

    state["entries"] = new_entries_state
    save_state(state_dir, page_slug, state)
    return aggregated_hits


def scan_wiki(root: Path, today: Optional[date] = None, force: bool = False) -> list[dict]:
    if today is None:
        today = date.today()
    skip_dirs = {"docs", "sources", "tools", "tests", "logs", ".git", ".obsidian",
                 ".playwright-cli", ".claude", ".pytest_cache", "__pycache__"}
    state_dir = root / "sources" / "watch_state"
    all_hits: list[dict] = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and entry.name in skip_dirs:
            continue
        if entry.is_file() and entry.suffix == ".md":
            all_hits.extend(run_watch(entry, state_dir, today=today, force=force))
    return all_hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Run watchlist signals for opt-in pages.")
    parser.add_argument("--page", default=None,
                        help="Restrict to a single page (relative path).")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cadence; check all entries.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Wiki root dir.")
    args = parser.parse_args()

    root = Path(args.root)
    today = date.today()
    if args.page:
        page = root / args.page
        if not page.exists():
            print(f"error: page {page} not found", file=sys.stderr)
            return 1
        state_dir = root / "sources" / "watch_state"
        hits = run_watch(page, state_dir, today=today, force=args.force)
    else:
        hits = scan_wiki(root, today=today, force=args.force)

    lint_reports = root / "sources" / "lint_reports"
    lint_reports.mkdir(parents=True, exist_ok=True)
    report_path = lint_reports / f"{today.isoformat()}.md"
    with report_path.open("a", encoding="utf-8") as fh:
        if hits:
            fh.write(f"\n## Watch hits — {today.isoformat()}\n\n")
            for h in hits:
                fh.write(
                    f"- [watch-hit] {h['page']} query=\"{h['query']}\" → {h['url']} "
                    f"(publicado {h.get('published_date','?')}, cadence {h['cadence']})\n"
                )

    log_path = root / "log.md"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(
            f"[watch] {today.isoformat()} hits={len(hits)} "
            f"report=sources/lint_reports/{today.isoformat()}.md\n"
        )
    print(f"Watch: {len(hits)} hits appended to {report_path}")
    return 0
```

- [ ] **Step 12.4: Run tests**

Run: `python -m pytest tests/test_watch_runner.py -v`
Expected: 9 passed (the `run_watch` test passes because `fake_search` is monkeypatched in — no real subprocess call).

- [ ] **Step 12.5: Run full test suite to confirm nothing broke**

Run: `python -m pytest tests/ -v`
Expected: all pass (number_guard + dated_lint + watch_runner).

- [ ] **Step 12.6: Create `tools/watch.sh` wrapper**

Create file with content:

```bash
#!/usr/bin/env bash
# Watchlist runner — wraps tools/lib/watch_runner.py
#
# Usage:
#   bash tools/watch.sh                       # respect cadence
#   bash tools/watch.sh --force               # ignore cadence
#   bash tools/watch.sh --page reforma_tributaria.md
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
exec python "$REPO_ROOT/tools/lib/watch_runner.py" "$@"
```

Make executable:

```bash
chmod +x tools/watch.sh
```

- [ ] **Step 12.7: Smoke test — run watch over the wiki**

Run: `bash tools/watch.sh`
Expected: `Watch: 0 hits appended to sources/lint_reports/YYYY-MM-DD.md`. Zero hits is correct — no page has `watches:` declared yet.

- [ ] **Step 12.8: Commit**

```bash
git add tools/lib/watch_runner.py tools/watch.sh tests/test_watch_runner.py
git commit -m "feat(watch): run_watch + scan_wiki + watch.sh CLI wrapper"
```

---

## Post-implementation — out of this plan's scope

Per spec §Rollout Fase 5, the retrofit of the 5 legal pages ([reforma_tributaria.md](../../../reforma_tributaria.md), [section_232.md](../../../section_232.md), [mcmv.md](../../../mcmv.md), [debentures.md](../../../debentures.md), [pode_entrar.md](../../../pode_entrar.md)) — adding `em:` to dateable claims and seeding `watches:` — is a separate operational task. It is NOT part of this implementation plan.

After this plan completes, the natural next session is: run `bash tools/lint.sh`, observe `hint` entries on those pages (via the `Missing em:` rule), pick one, retrofit it end-to-end, and iterate.
