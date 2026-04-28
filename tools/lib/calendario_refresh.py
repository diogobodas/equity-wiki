#!/usr/bin/env python3
"""Refresh calendario_resultados.md from CVM IPE_9 (Calendário de Eventos Corporativos).

Phase 1 (default): print JSON report of dates per ticker, no file changes.
Phase 2 (--apply): update calendario_resultados.md filling empty cells only,
                   preserving manual edits, bumping `Atualizada` per touched row
                   and frontmatter `updated:` if anything changed.
"""
import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
WIKI_PAGE = REPO_ROOT / "calendario_resultados.md"

# B3-listed tickers covered automatically via IPE_9.
# Foreign listings (XP, STLA, SIE.DE, BFIT.NA, LOMA, PICS, NU) are out of scope.
TICKERS_BR = [
    "BBAS3", "BBDC4", "BMEB4", "BPAC11", "DAYC4", "INBR32", "ITUB4", "PINE4", "SANB11",
    "BBSE3", "CXSE3", "PSSA3",
    "CURY3", "CYRE3", "DIRR3", "MDNE3", "MRVE3", "TEND3",
    "ARML3", "LCAM3", "MOVI3", "RENT3", "SIMH3", "VAMO3",
    "LEVE3", "WEGE3",
    "BFFT3", "SMFT3",
    "B3SA3",
    "BMOB3",
]

# Tickers whose resolve_company fails on the cvm-api ticker→CVM code map.
# Resolved manually by name search against /empresas registry on 2026-04-28.
TICKER_TO_CVM_OVERRIDE = {
    "BMEB4":  "001325",   # BCO MERCANTIL DO BRASIL S.A.
    "DAYC4":  "020796",   # BCO DAYCOVAL S.A.
    "ARML3":  "026069",   # ARMAC LOCAÇÃO, LOGÍSTICA E SERVIÇOS S.A.
    "BFFT3":  "026204",   # BLUEFIT ACADEMIAS DE GINÁSTICA E PARTICIPAÇÕES S.A.
    "LCAM3":  "022691",   # COMPANHIA DE LOCAÇÃO DAS AMÉRICAS (Locamerica original)
    "INBR32": "024406",   # BANCO INTER S.A. — controlada que filia CVM (vs 080217 INTER & CO BDR)
}

DATE_RE = re.compile(r"^(\d{2}/\d{2}/\d{4})$")
QUARTER_RE = re.compile(r"Referentes ao (\d)º trimestre", re.UNICODE)


def flatten_table_lines(text):
    """Convert markdown table cells (one per |...|) into flat list of non-empty values."""
    out = []
    for raw in text.split("\n"):
        raw = raw.strip()
        if not raw:
            continue
        # Skip table separator rows like |---| or |---|---|
        if re.match(r"^\|[\s\-:|]+\|$", raw):
            continue
        if raw.startswith("|") and raw.endswith("|"):
            for cell in raw.strip("|").split("|"):
                cell = cell.strip()
                if cell:
                    out.append(cell)
        else:
            out.append(raw)
    return out


def parse_ipe9(text):
    """Extract release dates from IPE_9 calendar text.

    Returns dict keyed like {'itr_1T': '29/04/2026', 'itr_2T': ..., 'dfp_anual': '25/02/2026'}.
    Only ITR (release date) and DFP (annual) sections — skips Apresentação Pública/AGO.
    """
    lines = flatten_table_lines(text)
    result = {}
    section = None
    quarter = None

    for line in lines:
        if "Informações Trimestrais" in line and "ITR" in line:
            section, quarter = "itr", None
            continue
        if "Demonstrações Financeiras" in line and "Anuais" in line:
            section, quarter = "dfp", "anual"
            continue
        if "Apresentação Pública" in line:
            section, quarter = None, None
            continue
        if (
            "Assembleia Geral" in line
            or "Formulário de Referência" in line
            or "Código Brasileiro" in line
        ):
            section, quarter = None, None
            continue

        m = QUARTER_RE.match(line)
        if m and section == "itr":
            quarter = f"{m.group(1)}T"
            continue

        m = DATE_RE.match(line)
        if m and section and quarter:
            key = f"{section}_{quarter}"
            if key not in result:
                result[key] = m.group(1)
            quarter = None  # next "Referentes" sets a new quarter

    return result


def date_to_column(section, quarter, ref_year):
    """Map (section, quarter, ref_year) to wiki column header like '1T26' or '4T25'."""
    if not ref_year:
        return None
    yy = str(ref_year)[2:]
    if section == "itr":
        return f"{quarter[0]}T{yy}"
    if section == "dfp":
        # DFP de exercício Y filed in early Y+1 → fills 4T<Y> column
        return f"4T{str(ref_year - 1)[2:]}"
    return None


def short_date(date_str):
    """DD/MM/YYYY → DD/MM."""
    m = re.match(r"(\d{2})/(\d{2})/\d{4}", date_str)
    return f"{m.group(1)}/{m.group(2)}" if m else date_str


async def fetch_meta(ticker):
    """Resolve ticker + find most recent IPE_9 in last 18 months."""
    from cvm_api import resolve_company, buscar_documentos, CompanyNotFoundError

    cvm_code = TICKER_TO_CVM_OVERRIDE.get(ticker)
    if not cvm_code:
        try:
            company = resolve_company(ticker)
            cvm_code = company.cvm_code
        except CompanyNotFoundError as e:
            return ticker, None, None, f"resolve_failed: {e}"
        except Exception as e:
            return ticker, None, None, f"resolve_error: {e!r}"

    cutoff = (datetime.now() - timedelta(days=540)).strftime("%d/%m/%Y")
    today = datetime.now().strftime("%d/%m/%Y")
    try:
        docs = await buscar_documentos(
            empresa=cvm_code,
            categoria="IPE_9_-1_-1",
            data_de=cutoff,
            data_ate=today,
            periodo="2",
        )
    except Exception as e:
        return ticker, None, None, f"list_error: {e!r}"

    if not docs:
        return ticker, None, None, "no_ipe9"

    d = sorted(docs, key=lambda x: x.data_entrega, reverse=True)[0]
    ref_year = None
    m = re.search(r"(\d{4})", d.data_referencia or "")
    if m:
        ref_year = int(m.group(1))

    return ticker, d, ref_year, None


def download_and_extract(ticker, doc):
    """Download IPE PDF and extract markdown via opendataloader. Returns text or None."""
    tmpdir = Path(tempfile.mkdtemp(prefix=f"cal_{ticker}_"))
    pdf_path = tmpdir / f"{ticker}_ipe9.pdf"
    md_path = tmpdir / f"{ticker}_ipe9_extracted.md"
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    try:
        r = subprocess.run(
            [
                sys.executable, str(SCRIPT_DIR / "cvm_fetch.py"), "download",
                "--num-sequencia", str(doc.num_sequencia or ""),
                "--num-versao", str(doc.num_versao or ""),
                "--numero-protocolo", str(doc.numero_protocolo or ""),
                "--desc-tipo", "IPE",
                "--output", str(pdf_path),
            ],
            capture_output=True, text=True, timeout=120, env=env,
        )
        if r.returncode != 0 or not pdf_path.exists():
            return None

        r = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "file_extract.py"), str(pdf_path)],
            capture_output=True, text=True, timeout=180, env=env,
        )
        if r.returncode != 0 or not md_path.exists():
            return None
        return md_path.read_text(encoding="utf-8")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


async def gather_all(tickers, concurrency=6):
    """Phase 1: parallel resolve + IPE_9 list. Returns list of (ticker, doc, ref_year, error)."""
    sem = asyncio.Semaphore(concurrency)

    async def bounded(t):
        async with sem:
            return await fetch_meta(t)

    return await asyncio.gather(*(bounded(t) for t in tickers))


def build_report(tickers, verbose=False):
    """Run full pipeline. Returns dict {ticker: {status, ref_year, columns, ...}}."""
    metadata = asyncio.run(gather_all(tickers))
    report = {}

    for ticker, doc, ref_year, error in metadata:
        if error or not doc:
            report[ticker] = {"status": "skip", "reason": error or "no_doc"}
            if verbose:
                print(f"  {ticker}: skip ({error})", file=sys.stderr)
            continue

        text = download_and_extract(ticker, doc)
        if not text:
            report[ticker] = {
                "status": "extract_failed",
                "protocolo": doc.numero_protocolo,
                "data_entrega": doc.data_entrega,
            }
            if verbose:
                print(f"  {ticker}: extract_failed", file=sys.stderr)
            continue

        dates = parse_ipe9(text)
        cols = {}
        for key, ds in dates.items():
            section, q = key.split("_", 1)
            col = date_to_column(section, q, ref_year)
            if col:
                cols[col] = short_date(ds)

        report[ticker] = {
            "status": "ok",
            "ref_year": ref_year,
            "data_entrega": doc.data_entrega,
            "columns": cols,
            "raw_dates": dates,
        }
        if verbose:
            print(f"  {ticker}: ok ref={ref_year} cols={cols}", file=sys.stderr)

    return report


def update_wiki(report, dry_run=True):
    """Update calendario_resultados.md filling empty cells only.

    For each table row matching a known ticker (col 2), fill any empty quarter column
    where report has a date. Bump 'Atualizada' to today on touched rows. Returns
    (rows_touched, cells_filled).
    """
    text = WIKI_PAGE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    out_lines = []
    in_table = False
    headers = None
    rows_touched = 0
    cells_filled = 0

    for line in text.split("\n"):
        if line.startswith("| Empresa") and "Ticker" in line and "Atualizada" in line:
            in_table = True
            headers = [c.strip() for c in line.split("|")[1:-1]]
            out_lines.append(line)
            continue

        if in_table and re.match(r"^\|[\s\-:|]+\|$", line):
            out_lines.append(line)
            continue

        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) != len(headers):
                in_table = False
                headers = None
                out_lines.append(line)
                continue
            ticker = cells[1]
            entry = report.get(ticker)
            if entry and entry.get("status") == "ok":
                update_cols = entry.get("columns", {})
                changed = False
                for i, hname in enumerate(headers):
                    if hname in update_cols and not cells[i]:
                        cells[i] = update_cols[hname]
                        changed = True
                        cells_filled += 1
                if changed:
                    rows_touched += 1
                    for i, hname in enumerate(headers):
                        if hname == "Atualizada":
                            cells[i] = today
                    out_lines.append("| " + " | ".join(cells) + " |")
                    continue
            out_lines.append(line)
            continue

        if in_table and not line.startswith("|"):
            in_table = False
            headers = None
        out_lines.append(line)

    new_text = "\n".join(out_lines)
    if rows_touched > 0:
        new_text = re.sub(
            r"^updated: \d{4}-\d{2}-\d{2}",
            f"updated: {today}",
            new_text,
            count=1,
            flags=re.M,
        )

    if not dry_run:
        WIKI_PAGE.write_text(new_text, encoding="utf-8")

    return rows_touched, cells_filled


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true",
                   help="Write changes to calendario_resultados.md (default: report only).")
    p.add_argument("--ticker", action="append",
                   help="Limit to specific ticker(s). Repeatable.")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    tickers = args.ticker if args.ticker else TICKERS_BR
    print(f"Refreshing {len(tickers)} ticker(s) from CVM IPE_9...", file=sys.stderr)

    report = build_report(tickers, verbose=args.verbose)

    # Summary to stderr
    ok = sum(1 for v in report.values() if v.get("status") == "ok")
    skip = sum(1 for v in report.values() if v.get("status") == "skip")
    fail = sum(1 for v in report.values() if v.get("status") == "extract_failed")
    print(f"\nSummary: ok={ok} skip={skip} extract_failed={fail}", file=sys.stderr)

    rows, cells = update_wiki(report, dry_run=not args.apply)
    if args.apply:
        print(f"Wiki updated: {rows} rows touched, {cells} cells filled.", file=sys.stderr)
    else:
        print(f"DRY-RUN: would update {rows} rows, fill {cells} cells "
              f"(re-run with --apply to write).", file=sys.stderr)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
