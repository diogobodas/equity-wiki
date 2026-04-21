"""Acceptance tests for tools/lib/number_guard.py.

Covers the six cases from docs/superpowers/specs/2026-04-16-notion-digest-design.md §Tests.
Each test builds a minimal source file in tmp and a matching digest, then asserts
the expected MatchResult status.

Note on spec test 5 (unit equivalence): the spec example uses "R$ 1,2 bi" vs
"R$ 1.234 milhões". Those differ by 2.8% which exceeds the spec's own ±0,5 %
monetary tolerance. We test the unit-conversion logic (bi vs milhões with mixed
comma/dot separators) using values that do align at the stated tolerance:
"R$ 1,234 bi" vs "R$ 1.234 milhões" — both normalize to 1.234e9 reais.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.lib import number_guard as ng  # noqa: E402


def _prep(tmp_path, source_text: str, digest_body: str, source_name="src.md"):
    """Create source + digest files; return (digest_path, source_relpath).

    The digest body is prepended with a (fonte: <relpath>) anchor line so
    check_digest() can resolve the source file.
    """
    # place source under tmp_path so index_source (which prepends REPO_ROOT for
    # non-absolute paths) works — we use an absolute path in the cite anchor.
    src = tmp_path / source_name
    src.write_text(source_text, encoding="utf-8")
    fm = "---\nsource: notion\n---\n"
    anchor = f"(fonte: {src})\n\n"
    digest = tmp_path / "digest_summary.md"
    digest.write_text(fm + anchor + digest_body, encoding="utf-8")
    return digest, src


# ---------- Test 1 — happy path ----------

def test_strict_match_margin(tmp_path):
    source = "A margem bruta do 3T25 ficou em 28,5% — acima da projeção."
    digest = "A margem bruta reportada foi de 28,5% no 3T25."
    dp, _ = _prep(tmp_path, source, digest)
    results = ng.check_digest(dp)
    assert len(results) == 1
    assert results[0].status == "MATCH_STRICT", results[0]


# ---------- Test 2 — pure invention ----------

def test_no_match_invented(tmp_path):
    source = "A margem bruta do 3T25 ficou em 28,5%."
    digest = "A margem bruta foi de 99,9% no trimestre."
    dp, _ = _prep(tmp_path, source, digest)
    results = ng.check_digest(dp)
    no_match = [r for r in results if r.status == "NO_MATCH"]
    assert any(r.claim.value == 99.9 and r.claim.unit == "%" for r in no_match)
    new = ng.annotate(dp, results)
    assert "99,9% [?]" in new


# ---------- Test 3 — separator agnosticism ----------

def test_separator_agnostic(tmp_path):
    source = "A margem bruta do 3T25 ficou em 28,5% — acima da projeção."
    digest = "Margem bruta no 3T25: 28.5%."
    dp, _ = _prep(tmp_path, source, digest)
    results = ng.check_digest(dp)
    assert any(r.status == "MATCH_STRICT" for r in results)


# ---------- Test 4 — loose match (context differs) ----------

def test_loose_match_context_differs(tmp_path):
    source = "A alíquota efetiva de IR ficou em 28,5% no 3T25."
    digest = "A margem bruta do trimestre foi de 28,5% — nível inédito."
    dp, _ = _prep(tmp_path, source, digest)
    results = ng.check_digest(dp)
    # The sole 28,5% claim should be LOOSE: value matches but keywords differ
    # (IR/alíquota vs margem/bruta/trimestre).
    assert any(r.status == "MATCH_LOOSE" for r in results), [
        (r.status, r.claim.raw, r.reason) for r in results
    ]
    # Annotate should NOT mark [?] on a LOOSE match.
    new = ng.annotate(dp, results)
    assert "[?]" not in new


# ---------- Test 5 — unit equivalence ----------

def test_unit_equivalence_bi_vs_milhoes(tmp_path):
    """R$ 1,234 bi normalizes identically to R$ 1.234 milhões (= 1.234e9 reais)."""
    source = "A dívida bruta encerrou o trimestre em R$ 1.234 milhões."
    digest = "A dívida bruta foi de R$ 1,234 bi ao final do trimestre."
    dp, _ = _prep(tmp_path, source, digest)
    results = ng.check_digest(dp)
    # At least one MATCH_STRICT with value ~1.234e9
    matches = [r for r in results if r.status == "MATCH_STRICT"]
    assert any(abs(r.claim.value - 1.234e9) / 1.234e9 <= 0.005 for r in matches), [
        (r.status, r.claim.raw, r.claim.value) for r in results
    ]


# ---------- Test 6 — parens-negative ----------

def test_parens_negative(tmp_path):
    source = "O prejuízo líquido foi de -245 milhões no 3T22."
    digest = "Prejuízo líquido de R$ (245) mm no 3T22."
    dp, _ = _prep(tmp_path, source, digest)
    results = ng.check_digest(dp)
    # Claim should normalize to -245e6 and match -245e6 from source
    strict_hits = [r for r in results if r.status == "MATCH_STRICT"]
    assert any(abs(r.claim.value - (-245e6)) <= 1.0 for r in strict_hits), [
        (r.status, r.claim.raw, r.claim.value) for r in results
    ]
