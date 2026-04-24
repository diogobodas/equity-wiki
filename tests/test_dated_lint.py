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
