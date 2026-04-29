#!/usr/bin/env python3
"""Equity Impact Briefing — cruza morning-briefing emails + relatório CVM diário com a cobertura.

Read-only. LLM-only matching: Python apenas empacota inputs (emails + cobertura + CVM +
calendário do dia); Sonnet faz match, filtragem e síntese em uma passada. Output:
briefings/<YYYY-MM-DD>-impact.md (sem ações automáticas).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
PROMPT_PATH = REPO_ROOT / "tools/prompts/equity_impact.md"
CALENDARIO_PATH = REPO_ROOT / "calendario_resultados.md"
MANIFESTS_DIR = REPO_ROOT / "sources/manifests"
BRIEFINGS_DIR = REPO_ROOT / "briefings"

# Locations the morning-briefing skill writes to (Windows %TEMP%/briefing/).
TEMP_BRIEFING = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "briefing"
BRIEFING_TEMP_JSON = TEMP_BRIEFING / "briefing_temp.json"
BRIEFING_HIGHLIGHTS_JSON = TEMP_BRIEFING / "briefing_highlights.json"

# CVM relatório diário (separate scheduled task — relatorio-cvm-automtico).
CVM_REPORT_DIR = Path(r"\\10.10.10.2\Dados\PesquisaBolsa\Diogo\Projeto Servidor\Projetos\_shared\CVM-API")

DEFAULT_MODEL = "claude-sonnet-4-6"

# Cap per-email body to keep context bounded.
BODY_CHAR_CAP = 6000


# ---------------------- Coverage parsing ----------------------

def parse_coverage():
    """Build coverage list from calendario_resultados.md + manifests aliases.

    Returns:
        list of dicts: [{"ticker": str, "nome": str, "setor": str, "aliases": [str, ...]}, ...]
    """
    coverage = {}

    text = CALENDARIO_PATH.read_text(encoding="utf-8")
    current_setor = None
    in_table = False
    headers = None
    for line in text.split("\n"):
        if line.startswith("## "):
            current_setor = line[3:].strip()
            in_table = False
            continue
        if line.startswith("| Empresa") and "Ticker" in line:
            headers = [c.strip() for c in line.split("|")[1:-1]]
            in_table = True
            continue
        if in_table and re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) != len(headers):
                in_table = False
                continue
            empresa, ticker = cells[0], cells[1]
            coverage[ticker] = {
                "ticker": ticker,
                "nome": empresa,
                "setor": current_setor or "Outros",
                "aliases": {ticker, empresa},
            }
        elif in_table and not line.startswith("|"):
            in_table = False

    # Enrich with manifest aliases / display_name
    for mf in MANIFESTS_DIR.glob("*.json"):
        if mf.stem.startswith("_"):
            continue
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            continue
        ticker = m.get("ticker")
        if not ticker or ticker not in coverage:
            continue
        for a in m.get("aliases", []):
            if a:
                coverage[ticker]["aliases"].add(a)
        dn = m.get("display_name", "")
        if dn:
            coverage[ticker]["aliases"].add(dn)

    out = []
    for t in sorted(coverage):
        info = coverage[t]
        info["aliases"] = sorted({a for a in info["aliases"] if a and len(a) >= 2})
        out.append(info)
    return out


def parse_calendario_today(today_str):
    """Return list of (ticker, empresa, periodo, date_dm) reporting today (DD/MM matches)."""
    text = CALENDARIO_PATH.read_text(encoding="utf-8")
    today_dm = datetime.strptime(today_str, "%Y-%m-%d").strftime("%d/%m")
    hits = []
    in_table = False
    headers = None
    for line in text.split("\n"):
        if line.startswith("| Empresa") and "Ticker" in line:
            headers = [c.strip() for c in line.split("|")[1:-1]]
            in_table = True
            continue
        if in_table and re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) != len(headers):
                in_table = False
                continue
            empresa, ticker = cells[0], cells[1]
            for i, h in enumerate(headers):
                if re.match(r"^[1-4]T\d{2}$", h):
                    val = cells[i].strip().strip("*")
                    if val == today_dm:
                        hits.append({"ticker": ticker, "empresa": empresa, "periodo": h, "data": val})
        elif in_table and not line.startswith("|"):
            in_table = False
    return hits


def extract_body(email):
    """Extract plain text from highlight email body. Strips HTML, caps length."""
    body = email.get("body") or email.get("body_text") or email.get("body_html") or ""
    if not body:
        return ""
    if "<" in body and ">" in body:
        body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
        body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"\s+", " ", body).strip()
    return body[:BODY_CHAR_CAP]


# ---------------------- CVM report parsing ----------------------

def parse_cvm_report(report_path):
    """Strip HTML to plain text. Cap to 30k chars (typical reports are smaller)."""
    if not report_path.exists():
        return ""
    try:
        html = report_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    text = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(?:p|div|tr|li|h[1-6])>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text[:30000]


# ---------------------- Context build ----------------------

def build_context(today, coverage, debug=False):
    """Package all inputs for the LLM. No scoring/filtering — Sonnet handles that."""
    if not BRIEFING_TEMP_JSON.exists():
        sys.exit(
            f"ERROR: morning-briefing input not found at {BRIEFING_TEMP_JSON}\n"
            f"Run /morning-briefing first (or wait for the 8h23 scheduled task).")

    temp_data = json.loads(BRIEFING_TEMP_JSON.read_text(encoding="utf-8"))
    emails_meta = temp_data.get("emails", [])
    metadata = temp_data.get("metadata", {})

    # Highlights JSON has bodies; map by entry_id.
    body_map = {}
    if BRIEFING_HIGHLIGHTS_JSON.exists():
        try:
            hl = json.loads(BRIEFING_HIGHLIGHTS_JSON.read_text(encoding="utf-8"))
            hl_emails = hl.get("emails", []) if isinstance(hl, dict) else hl
            for e in hl_emails:
                eid = e.get("entry_id")
                if eid:
                    body_map[eid] = extract_body(e)
        except Exception as ex:
            print(f"WARN: highlights JSON parse failed: {ex}", file=sys.stderr)

    # Compact email list. entry_id is included so the agent can fetch additional bodies
    # on-demand via outlook.py --fetch-by-id when it needs deeper context.
    emails_compact = []
    for e in emails_meta:
        eid = e.get("entry_id", "")
        item = {
            "date": (e.get("date") or "")[:16],
            "sender": e.get("sender") or "",
            "subject": e.get("subject") or "",
            "entry_id": eid,
        }
        body = body_map.get(eid)
        if body:
            item["body"] = body
        emails_compact.append(item)

    cvm_path = CVM_REPORT_DIR / f"relatorio_{today}.html"
    cvm_text = parse_cvm_report(cvm_path)
    calendar_today = parse_calendario_today(today)

    if debug:
        bodies = sum(1 for e in emails_compact if "body" in e)
        print(f"  emails: {len(emails_compact)} ({bodies} com body)", file=sys.stderr)
        print(f"  CVM: {len(cvm_text)} chars ({'exists' if cvm_path.exists() else 'MISSING'})",
              file=sys.stderr)
        print(f"  calendar today: {len(calendar_today)}", file=sys.stderr)
        ctx_size_estimate = sum(len(json.dumps(e, ensure_ascii=False)) for e in emails_compact)
        print(f"  ~ctx size: {ctx_size_estimate / 1000:.1f}K chars (~{ctx_size_estimate / 4000:.1f}K tokens)",
              file=sys.stderr)

    return {
        "today": today,
        "briefing_metadata": metadata,
        "coverage": coverage,
        "calendar_today": calendar_today,
        "cvm_report_text": cvm_text,
        "cvm_report_exists": cvm_path.exists(),
        "emails": emails_compact,
    }


# ---------------------- LLM invocation ----------------------

def invoke_llm(context, model=None):
    """Pipe prompt + context to claude --print and return markdown body."""
    model = model or os.environ.get("INVOKE_CLAUDE_MODEL") or DEFAULT_MODEL
    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace(
        "{{CONTEXT_JSON}}",
        json.dumps(context, ensure_ascii=False, indent=2),
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(prompt)
        prompt_file = Path(tf.name)

    claude_bin = shutil.which("claude") or shutil.which("claude.cmd") or shutil.which("claude.bat")
    if not claude_bin:
        sys.exit("ERROR: `claude` binary not found in PATH")

    try:
        with open(prompt_file, "r", encoding="utf-8") as fh:
            result = subprocess.run(
                [
                    claude_bin, "--print",
                    "--model", model,
                    "--allowedTools", "Bash,Read",
                    "--permission-mode", "bypassPermissions",
                ],
                stdin=fh,
                capture_output=True, text=True, timeout=900,
                env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
            )
    finally:
        prompt_file.unlink(missing_ok=True)

    if result.returncode != 0:
        sys.exit(
            f"ERROR: claude --print failed (exit {result.returncode})\n"
            f"stderr: {result.stderr}\nstdout (last 500): {result.stdout[-500:]}"
        )
    return result.stdout.strip()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ticker", help="Focus on a single covered ticker.")
    p.add_argument("--debug", action="store_true", help="Verbose stderr.")
    p.add_argument("--no-llm", action="store_true",
                   help="Build and print context JSON, skip LLM call (debug).")
    args = p.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Equity Impact — {today}", file=sys.stderr)

    coverage = parse_coverage()
    if args.debug:
        print(f"  coverage: {len(coverage)} empresas", file=sys.stderr)

    if args.ticker:
        coverage = [c for c in coverage if c["ticker"] == args.ticker]
        if not coverage:
            sys.exit(f"ERROR: ticker {args.ticker} not in coverage list")

    context = build_context(today, coverage, debug=args.debug)

    if args.no_llm:
        print(json.dumps(context, ensure_ascii=False, indent=2))
        return

    body = invoke_llm(context)

    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BRIEFINGS_DIR / f"{today}-impact.md"

    bodies_count = sum(1 for e in context["emails"] if "body" in e)
    frontmatter = (
        "---\n"
        "type: briefing_impact\n"
        f"date: {today}\n"
        "sources_consumed:\n"
        f"  - briefing_temp.json ({len(context['emails'])} emails / "
        f"{bodies_count} com body)\n"
        f"  - relatorio_{today}.html "
        f"({'parsed' if context['cvm_report_exists'] else 'missing'})\n"
        f"coverage_count: {len(context['coverage'])}\n"
        "---\n\n"
    )
    out_path.write_text(frontmatter + body + "\n", encoding="utf-8")
    print(f"Wrote {out_path}", file=sys.stderr)
    print(out_path)


if __name__ == "__main__":
    main()
