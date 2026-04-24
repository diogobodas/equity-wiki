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


def test_parse_citation_with_confiabilidade(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "Dado (fonte: https://exemplo.com, confiabilidade: oficial).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    assert len(claims) == 1
    assert claims[0].fonte == "https://exemplo.com"
    assert claims[0].em is None


def test_parse_citation_with_em_and_confiabilidade(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "Dado (fonte: https://exemplo.com, em: 2026-01-15, confiabilidade: oficial).\n",
        encoding="utf-8",
    )
    claims = dl.parse_claims(page)
    assert len(claims) == 1
    assert claims[0].fonte == "https://exemplo.com"
    assert claims[0].em == date(2026, 1, 15)


def test_scan_wiki_skips_documentation_files(tmp_path):
    (tmp_path / "SCHEMA.md").write_text(
        "Doc example (fonte: x.md, em: 2020-01-01).\n", encoding="utf-8"
    )
    (tmp_path / "CLAUDE.md").write_text(
        "Doc (fonte: y.md, em: 2020-01-01).\n", encoding="utf-8"
    )
    (tmp_path / "log.md").write_text(
        "(fonte: z.md, em: 2020-01-01)\n", encoding="utf-8"
    )
    (tmp_path / "real_page.md").write_text(
        "Claim (fonte: real.md, em: 2026-01-15).\n", encoding="utf-8"
    )
    claims = dl.scan_wiki(tmp_path)
    assert len(claims) == 1
    assert claims[0].page.name == "real_page.md"


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


def test_read_frontmatter_multiline_list(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "type: entity\n"
        "aliases:\n"
        "  - Cyrela\n"
        "  - CYRE3\n"
        "  - CURY3\n"
        "sources:\n"
        "  - sources/digested/x_summary.md\n"
        "  - sources/digested/y_summary.md\n"
        "created: 2025-01-01\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )
    fm = dl._read_frontmatter(page)
    assert fm["type"] == "entity"
    assert fm["aliases"] == ["Cyrela", "CYRE3", "CURY3"]
    assert fm["sources"] == ["sources/digested/x_summary.md", "sources/digested/y_summary.md"]
    assert fm["created"] == "2025-01-01"


def test_read_frontmatter_inline_list_still_works(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "---\ntype: concept\naliases: [Reforma, LC 214/2025]\n---\n\nbody\n",
        encoding="utf-8",
    )
    fm = dl._read_frontmatter(page)
    assert fm["aliases"] == ["Reforma", "LC 214/2025"]


def test_newer_source_flag_triggered(tmp_path):
    # Create wiki page with claim em: 2024-01-01 about cyrela
    (tmp_path / "cyrela.md").write_text(
        "---\ntype: entity\naliases:\n  - Cyrela\n  - CYRE3\n---\n\n"
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
        "---\ntype: entity\naliases:\n  - Cyrela\n---\n\n"
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


def test_read_frontmatter_quoted_list_items(tmp_path):
    page = tmp_path / "demo.md"
    page.write_text(
        "---\n"
        "aliases:\n"
        '  - "CBS"\n'
        "  - 'IBS'\n"
        "  - LC 214/2025\n"
        "---\n\nbody\n",
        encoding="utf-8",
    )
    fm = dl._read_frontmatter(page)
    assert fm["aliases"] == ["CBS", "IBS", "LC 214/2025"]


def test_newer_source_handles_scalar_aliases_manifest(tmp_path):
    (tmp_path / "cyrela.md").write_text(
        "---\ntype: entity\naliases:\n  - Cyrela\n---\n\n"
        "Claim (fonte: x.md, em: 2024-01-01).\n",
        encoding="utf-8",
    )
    manifests = tmp_path / "sources" / "manifests"
    manifests.mkdir(parents=True)
    # aliases as scalar string (authoring mistake)
    (manifests / "cyrela.json").write_text(
        json.dumps(
            {
                "empresa": "cyrela",
                "aliases": "Cyrela",
                "sources": [
                    {"type": "dfp", "asof": "2025",
                     "ingested_on": "2026-03-15",
                     "digested": "sources/digested/cyrela_dfp_2025.md"}
                ],
            }
        ),
        encoding="utf-8",
    )
    claims = dl.parse_claims(tmp_path / "cyrela.md")
    flags = dl.newer_source_flags(claims, tmp_path)
    # Even with scalar aliases, matching should succeed (via string guard)
    assert len(flags) == 1
    assert flags[0].rule == "newer_source"


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
    # Two claims → two flags (one per side) OR one combined flag; accept either
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


def test_contradiction_ignores_citation_metadata_fragments(tmp_path):
    # Two pages both have aggregation lines with fonte spans but same prose.
    # The bucket key must come from the prose, not from the fonte path tokens.
    (tmp_path / "a.md").write_text(
        "Receita R$ 100 milhões (fonte: structured/a/release.json :: canonical).\n",
        encoding="utf-8",
    )
    (tmp_path / "b.md").write_text(
        "Receita R$ 200 milhões (fonte: structured/b/release.json :: canonical).\n",
        encoding="utf-8",
    )
    claims = dl.scan_wiki(tmp_path)
    flags = dl.contradiction_flags(claims)
    # Should flag the genuine disagreement (100M vs 200M for "receita"),
    # not be distracted by shared tokens like 'canonical' or 'structured'.
    assert len(flags) >= 1
    assert all(f.rule == "contradiction" for f in flags)


def test_contradiction_ignores_year_tokens(tmp_path):
    # A pattern where year 2026 is adjacent to a tiny value. Without the year
    # guard, finditer+largest-magnitude would pick 2026 as the value and
    # bucket it against other unrelated claims.
    (tmp_path / "a.md").write_text(
        "Guidance 2026: R$ 5 milhões (fonte: x.md, em: 2026-01-01).\n",
        encoding="utf-8",
    )
    (tmp_path / "b.md").write_text(
        "Guidance 2026: R$ 10 milhões (fonte: y.md, em: 2026-02-01).\n",
        encoding="utf-8",
    )
    claims = dl.scan_wiki(tmp_path)
    flags = dl.contradiction_flags(claims)
    # Should flag the genuine disagreement (5M vs 10M), not a year conflict.
    # Both claims must report values in millions, NOT 2026.
    assert len(flags) >= 1
    for f in flags:
        assert "2026.0" not in f.detail, f"Year token leaked into value: {f.detail}"


def test_normalize_value_rejects_bare_year(tmp_path):
    # Unit tests the guard directly: feed a match representing "2025" with no
    # unit/decimal and verify _normalize_value returns None.
    match = dl._VALUE_RE.search("Evento em 2025 teve impacto")
    assert match is not None, "regex should match '2025'"
    result = dl._normalize_value(match)
    assert result is None, "bare year 2025 should be rejected"


def test_age_threshold_deduped_by_newer_source(tmp_path):
    # Create a page with a stale dated claim AND a manifest with a newer ingest
    # for the same empresa. Expected: only the `newer_source` action flag fires,
    # NOT an additional `age_threshold` warn on the same claim.
    (tmp_path / "cyrela.md").write_text(
        "---\ntype: entity\naliases:\n  - Cyrela\n  - CYRE3\n---\n\n"
        "Guidance (fonte: digested/cyrela_dfp_2020_summary.md, em: 2020-01-01).\n",
        encoding="utf-8",
    )
    digested = tmp_path / "sources" / "digested"
    digested.mkdir(parents=True)
    (digested / "cyrela_dfp_2025_summary.md").write_text("newer\n", encoding="utf-8")
    manifests = tmp_path / "sources" / "manifests"
    manifests.mkdir(parents=True)
    (manifests / "cyrela.json").write_text(
        json.dumps({
            "empresa": "cyrela",
            "aliases": ["Cyrela", "CYRE3"],
            "sources": [{"type": "dfp", "asof": "2025",
                         "ingested_on": "2026-03-15",
                         "digested": "sources/digested/cyrela_dfp_2025_summary.md"}],
        }),
        encoding="utf-8",
    )
    claims = dl.parse_claims(tmp_path / "cyrela.md")
    config = _load_config()
    newer_flags = dl.newer_source_flags(claims, tmp_path)
    assert len(newer_flags) == 1
    # Call age_threshold with the exclude_claims set from newer_source
    exclude = {(f.claim.page, f.claim.line) for f in newer_flags}
    age_flags = dl.age_threshold_flags(claims, config, today=date(2026, 4, 23),
                                        exclude_claims=exclude)
    # The claim is stale but has a newer source → age_threshold must skip
    assert age_flags == []
