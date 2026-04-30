"""
bbg.py — Bloomberg client + cache layer for equity-wiki.

Reuses the shared Flask tunnel client from Projeto Servidor (`_shared/bbg/client.py`),
adds disk-backed cache under `sources/bbg/{empresa}/`, and exposes a CLI.

Design:
    - Reuse > duplication: imports `_shared.bbg.client` directly via sys.path
      so updates on the server propagate without sync. Override location via
      BBG_SHARED_PATH env var.
    - Cache is citable: every snapshot writes a `.meta.json` with `fetched_at`
      so wiki citations carry `em: YYYY-MM-DD`.
    - Manifest-aware: ticker is resolved from `sources/manifests/{empresa}.json`
      (`bbg_ticker` field if present; otherwise `{ticker} BZ Equity`).

CLI:
    python tools/lib/bbg.py snapshot <EMPRESA>           # default fields, cached
    python tools/lib/bbg.py snapshot <EMPRESA> --refresh # force refresh
    python tools/lib/bbg.py snapshot <EMPRESA> --fields=PX_LAST,PE_RATIO
    python tools/lib/bbg.py history <EMPRESA> --field=PX_LAST --since=2024-01-01
    python tools/lib/bbg.py consensus <EMPRESA> --period=1FY
    python tools/lib/bbg.py raw <JSON_PAYLOAD>           # escape hatch (POST /api/)
    python tools/lib/bbg.py field-search <QUERY>         # find BBG mnemonics

Env:
    BBG_SHARED_PATH  override path to `_shared` dir (default: //10.10.10.2/Dados/PesquisaBolsa/Diogo/Projeto Servidor/Projetos/_shared)
    BBG_BASE_URL     override server URL (default from client.py: http://10.10.60.147)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Locate and import shared bbg client
# ---------------------------------------------------------------------------

# The shared client lives at `<PROJETOS>/_shared/bbg/client.py` and is imported
# as `_shared.bbg`. Add the *Projetos* parent dir to sys.path so the package
# resolves. Override with BBG_PROJETOS_PATH if the share moves.
_DEFAULT_PROJETOS = r"\\10.10.10.2\Dados\PesquisaBolsa\Diogo\Projeto Servidor\Projetos"
PROJETOS_PATH = os.environ.get("BBG_PROJETOS_PATH", _DEFAULT_PROJETOS)

if PROJETOS_PATH and PROJETOS_PATH not in sys.path:
    sys.path.insert(0, PROJETOS_PATH)

try:
    from _shared.bbg import (  # type: ignore
        bdp,
        bdh,
        bds,
        ticker_search,
        field_search,
        field_info,
        analyst_recommendations,
        earnings_dates,
        dividend_history,
    )
except ImportError as e:
    print(
        f"[bbg] ERRO: nao consegui importar `_shared.bbg` de {PROJETOS_PATH}.\n"
        f"      {e}\n"
        f"      Verifique se o share esta montado ou ajuste BBG_PROJETOS_PATH.",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths and conventions
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
BBG_DIR = REPO_ROOT / "sources" / "bbg"
MANIFESTS_DIR = REPO_ROOT / "sources" / "manifests"

# Default field bundles
SNAPSHOT_FIELDS_PRICE = [
    "PX_LAST",
    "CHG_PCT_1D",
    "CHG_PCT_5D",
    "CHG_PCT_1M",
    "CHG_PCT_YTD",
    "CUR_MKT_CAP",
    "EQY_SH_OUT",
    "VOLUME_AVG_30D",
]
SNAPSHOT_FIELDS_MULTIPLES = [
    "PE_RATIO",
    "PX_TO_BOOK_RATIO",
    "PX_TO_SALES_RATIO",
    "BEST_PE_NXT_YR",
    "EQY_DVD_YLD_IND",
    "INDX_ADJ_PE",
]
SNAPSHOT_FIELDS_CONSENSUS = [
    "BEST_TARGET_PRICE",
    "TOT_BUY_REC",
    "TOT_HOLD_REC",
    "TOT_SELL_REC",
    "TOT_ANALYST_REC",
]
ESTIMATE_FIELDS = ["BEST_EPS", "BEST_NET_INCOME", "BEST_SALES", "BEST_EBITDA"]
DEFAULT_SNAPSHOT_FIELDS = (
    SNAPSHOT_FIELDS_PRICE + SNAPSHOT_FIELDS_MULTIPLES + SNAPSHOT_FIELDS_CONSENSUS
)

# ---------------------------------------------------------------------------
# Manifest / ticker resolution
# ---------------------------------------------------------------------------

def resolve_ticker(empresa_or_ticker: str) -> tuple[str, str]:
    """
    Resolve `empresa` slug or B3 ticker into (empresa_slug, bbg_ticker).
    Looks up the manifest if it exists; falls back to `{TICKER} BZ Equity`.
    """
    raw = empresa_or_ticker.strip()

    # Try as empresa slug first (e.g., "porto")
    manifest_path = MANIFESTS_DIR / f"{raw.lower()}.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bbg_ticker = manifest.get("bbg_ticker") or f"{manifest['ticker']} BZ Equity"
        return raw.lower(), bbg_ticker

    # Try as B3 ticker (e.g., "PSSA3") — search manifests by ticker field
    ticker_upper = raw.upper()
    if MANIFESTS_DIR.exists():
        for mf in MANIFESTS_DIR.glob("*.json"):
            try:
                data = json.loads(mf.read_text(encoding="utf-8"))
            except Exception:
                continue
            if data.get("ticker", "").upper() == ticker_upper:
                bbg_ticker = data.get("bbg_ticker") or f"{ticker_upper} BZ Equity"
                return mf.stem, bbg_ticker

    # Fallback: assume the input is a B3 ticker, slug = lowercase ticker
    bbg_ticker = f"{ticker_upper} BZ Equity"
    return ticker_upper.lower(), bbg_ticker


def empresa_dir(empresa: str) -> Path:
    d = BBG_DIR / empresa
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _meta_path(d: Path, name: str) -> Path:
    return d / f"{name}.meta.json"


def _is_fresh(meta_path: Path, max_age_hours: float) -> bool:
    if not meta_path.exists():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    fetched = meta.get("fetched_at")
    if not fetched:
        return False
    try:
        ts = datetime.fromisoformat(fetched)
    except ValueError:
        return False
    age = datetime.now(ts.tzinfo) - ts
    return age < timedelta(hours=max_age_hours)


def _write_csv_with_meta(df: pd.DataFrame, d: Path, name: str, meta_extra: dict) -> Path:
    csv_path = d / f"{name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    meta = {
        "fetched_at": _now_iso(),
        "rows": len(df),
        "columns": list(df.columns),
        **meta_extra,
    }
    _meta_path(d, name).write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return csv_path


# ---------------------------------------------------------------------------
# High-level operations
# ---------------------------------------------------------------------------

def snapshot(
    empresa_or_ticker: str,
    fields: list[str] | None = None,
    refresh: bool = False,
    max_age_hours: float = 24.0,
) -> pd.DataFrame:
    """
    Fetch a wide-format snapshot (current price, multiples, consensus).
    Caches under sources/bbg/{empresa}/snapshot.csv. Returns DataFrame.
    """
    empresa, bbg_ticker = resolve_ticker(empresa_or_ticker)
    d = empresa_dir(empresa)
    csv_path = d / "snapshot.csv"
    meta_path = _meta_path(d, "snapshot")

    if not refresh and _is_fresh(meta_path, max_age_hours) and csv_path.exists():
        return pd.read_csv(csv_path)

    fields = fields or DEFAULT_SNAPSHOT_FIELDS

    # Single ref call for all fields
    df = bdp([bbg_ticker], fields)

    # Pivot to wide: one row per ticker, columns = fields
    if not df.empty and "field" in df.columns and "value" in df.columns:
        wide = df.pivot_table(
            index="ticker", columns="field", values="value", aggfunc="first"
        ).reset_index()
        wide = wide[["ticker"] + [f for f in fields if f in wide.columns]]
    else:
        wide = df

    _write_csv_with_meta(
        wide,
        d,
        "snapshot",
        meta_extra={
            "ticker_b3": bbg_ticker.split(" ")[0],
            "ticker_bbg": bbg_ticker,
            "fields_requested": fields,
            "source": "Bloomberg via API_TUNEL",
        },
    )
    return wide


def consensus(
    empresa_or_ticker: str,
    period: str = "1FY",
    fields: list[str] | None = None,
    refresh: bool = False,
    max_age_hours: float = 24.0,
) -> pd.DataFrame:
    """
    Fetch consensus estimates for a forward period (1FY/2FY/1Q/2Q/etc.).
    Caches under sources/bbg/{empresa}/consensus_{period}.csv. Also appends
    to consensus_history.csv for tracking over time.
    """
    empresa, bbg_ticker = resolve_ticker(empresa_or_ticker)
    d = empresa_dir(empresa)
    name = f"consensus_{period}"
    csv_path = d / f"{name}.csv"
    meta_path = _meta_path(d, name)

    if not refresh and _is_fresh(meta_path, max_age_hours) and csv_path.exists():
        return pd.read_csv(csv_path)

    fields = fields or ESTIMATE_FIELDS
    df = bdp([bbg_ticker], fields, BEST_FPERIOD_OVERRIDE=period)

    if not df.empty and "field" in df.columns and "value" in df.columns:
        wide = df.pivot_table(
            index="ticker", columns="field", values="value", aggfunc="first"
        ).reset_index()
    else:
        wide = df

    _write_csv_with_meta(
        wide,
        d,
        name,
        meta_extra={
            "ticker_b3": bbg_ticker.split(" ")[0],
            "ticker_bbg": bbg_ticker,
            "period": period,
            "fields_requested": fields,
            "source": "Bloomberg via API_TUNEL",
        },
    )

    # Append to consensus_history.csv (longitudinal tracking)
    hist_path = d / "consensus_history.csv"
    today = datetime.now().date().isoformat()
    if not wide.empty:
        snap = wide.copy()
        snap["snapshot_date"] = today
        snap["period"] = period
        cols = ["snapshot_date", "period"] + [c for c in snap.columns if c not in ("snapshot_date", "period")]
        snap = snap[cols]
        if hist_path.exists():
            prior = pd.read_csv(hist_path)
            # de-dupe: keep latest per (snapshot_date, period)
            combined = pd.concat([prior, snap], ignore_index=True)
            combined = combined.drop_duplicates(subset=["snapshot_date", "period"], keep="last")
            combined.to_csv(hist_path, index=False, encoding="utf-8")
        else:
            snap.to_csv(hist_path, index=False, encoding="utf-8")

    return wide


def history(
    empresa_or_ticker: str,
    field: str = "PX_LAST",
    start: str = "2024-01-01",
    end: str | None = None,
    refresh: bool = False,
    max_age_hours: float = 24.0,
) -> pd.DataFrame:
    """
    Fetch BDH series. Caches under sources/bbg/{empresa}/{field}_history.csv.
    Dates accepted as YYYY-MM-DD; converted to YYYYMMDD for the API.
    """
    empresa, bbg_ticker = resolve_ticker(empresa_or_ticker)
    d = empresa_dir(empresa)
    name = f"{field.lower()}_history"
    csv_path = d / f"{name}.csv"
    meta_path = _meta_path(d, name)

    if not refresh and _is_fresh(meta_path, max_age_hours) and csv_path.exists():
        return pd.read_csv(csv_path)

    end = end or datetime.now().date().isoformat()
    start_yyyymmdd = start.replace("-", "")
    end_yyyymmdd = end.replace("-", "")

    df = bdh([bbg_ticker], [field], start_yyyymmdd, end_yyyymmdd)

    _write_csv_with_meta(
        df,
        d,
        name,
        meta_extra={
            "ticker_b3": bbg_ticker.split(" ")[0],
            "ticker_bbg": bbg_ticker,
            "field": field,
            "start": start,
            "end": end,
            "source": "Bloomberg via API_TUNEL",
        },
    )
    return df


# ---------------------------------------------------------------------------
# Pretty printing for CLI
# ---------------------------------------------------------------------------

def _format_value(field: str, val) -> str:
    """
    BBG returns:
      - PX_*, BEST_TARGET_PRICE: native currency (reais for BZ)
      - CHG_PCT_*, EQY_DVD_YLD_IND: already as percent (1.79 = 1.79%)
      - CUR_MKT_CAP: raw native currency (32_006_009_970 = R$ 32 bi)
      - BEST_NET_INCOME, BEST_SALES, BEST_EBITDA: in millions (3631.4 = R$ 3,63 bi)
      - EQY_SH_OUT: in millions of shares
    """
    if pd.isna(val):
        return "n/d"
    try:
        v = float(val)
    except (TypeError, ValueError):
        return str(val)
    if "PCT" in field or field == "EQY_DVD_YLD_IND" or "YLD" in field:
        return f"{v:.2f}%"
    if field == "CUR_MKT_CAP":
        return f"R$ {v/1e9:,.2f} bi" if abs(v) >= 1e9 else f"R$ {v/1e6:,.2f} mm"
    if field in ("BEST_NET_INCOME", "BEST_SALES", "BEST_EBITDA"):
        return f"R$ {v/1_000:,.2f} bi" if abs(v) >= 1_000 else f"R$ {v:,.1f} mm"
    if field in ("PX_LAST", "BEST_TARGET_PRICE", "BEST_EPS"):
        return f"R$ {v:,.2f}"
    if field == "EQY_SH_OUT":
        return f"{v:,.1f} mm acoes"
    if field == "VOLUME_AVG_30D":
        return f"{v:,.0f} acoes/dia"
    if field in ("PE_RATIO", "PX_TO_BOOK_RATIO", "PX_TO_SALES_RATIO", "BEST_PE_NXT_YR", "INDX_ADJ_PE"):
        return f"{v:.2f}x"
    if field.startswith("TOT_"):
        return f"{int(v)}"
    return f"{v:,.4f}".rstrip("0").rstrip(".")


def _print_wide(df: pd.DataFrame, title: str) -> None:
    print(f"=== {title} ===")
    if df.empty:
        print("(vazio)")
        return
    row = df.iloc[0]
    for col in df.columns:
        if col == "ticker":
            continue
        print(f"  {col:<28} {_format_value(col, row[col])}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cmd_snapshot(args):
    df = snapshot(args.empresa, fields=args.fields, refresh=args.refresh, max_age_hours=args.max_age)
    _, bbg_ticker = resolve_ticker(args.empresa)
    _print_wide(df, f"Snapshot {bbg_ticker}")
    print(f"\n  Cache: sources/bbg/{resolve_ticker(args.empresa)[0]}/snapshot.csv")


def _cmd_consensus(args):
    df = consensus(args.empresa, period=args.period, fields=args.fields, refresh=args.refresh, max_age_hours=args.max_age)
    _, bbg_ticker = resolve_ticker(args.empresa)
    _print_wide(df, f"Consenso {args.period} {bbg_ticker}")
    print(f"\n  Cache: sources/bbg/{resolve_ticker(args.empresa)[0]}/consensus_{args.period}.csv")
    print(f"  History: sources/bbg/{resolve_ticker(args.empresa)[0]}/consensus_history.csv")


def _cmd_history(args):
    df = history(
        args.empresa,
        field=args.field,
        start=args.since,
        end=args.until,
        refresh=args.refresh,
        max_age_hours=args.max_age,
    )
    _, bbg_ticker = resolve_ticker(args.empresa)
    print(f"=== Historico {args.field} {bbg_ticker} ===")
    if df.empty:
        print("(vazio)")
    else:
        print(df.head(3).to_string(index=False))
        print(f"  ... ({len(df)} pontos)")
        print(df.tail(3).to_string(index=False))
    print(f"\n  Cache: sources/bbg/{resolve_ticker(args.empresa)[0]}/{args.field.lower()}_history.csv")


def _cmd_raw(args):
    """Escape hatch: post any JSON payload to /api/."""
    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        print(f"ERRO: payload nao e JSON valido: {e}", file=sys.stderr)
        sys.exit(2)

    method = payload.pop("method", None)
    if method == "ref":
        df = bdp(payload.get("tickers"), payload.get("flds"), **dict(payload.get("ovrds", [])))
    elif method == "bdh":
        df = bdh(
            payload.get("tickers"),
            payload.get("flds"),
            payload.get("start_date"),
            payload.get("end_date"),
            **dict(payload.get("ovrds", [])),
        )
    elif method == "bulkref":
        df = bds(payload.get("tickers"), payload.get("flds"), **dict(payload.get("ovrds", [])))
    else:
        print(f"ERRO: method '{method}' nao suportado pelo CLI raw (use ref/bdh/bulkref)", file=sys.stderr)
        sys.exit(2)

    print(df.to_csv(index=False))


def _cmd_field_search(args):
    df = field_search(args.query)
    if df.empty:
        print("Nenhum campo encontrado.")
        return
    cols = [c for c in ["mnemonic", "description", "categoryName"] if c in df.columns]
    print(df[cols].head(args.limit).to_string(index=False))


def _cmd_resolve(args):
    empresa, bbg_ticker = resolve_ticker(args.empresa)
    print(f"empresa: {empresa}")
    print(f"bbg_ticker: {bbg_ticker}")


def main():
    parser = argparse.ArgumentParser(prog="bbg", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("empresa", help="empresa slug (ex: porto) ou B3 ticker (ex: PSSA3)")
        p.add_argument("--refresh", action="store_true", help="forca refresh do cache")
        p.add_argument("--max-age", type=float, default=24.0, dest="max_age", help="idade maxima do cache em horas (default 24)")
        p.add_argument(
            "--fields",
            type=lambda s: [x.strip() for x in s.split(",") if x.strip()],
            default=None,
            help="lista de campos separados por virgula (override default)",
        )

    p_snap = sub.add_parser("snapshot", help="snapshot wide (px + multiplos + consenso)")
    add_common(p_snap)
    p_snap.set_defaults(func=_cmd_snapshot)

    p_cons = sub.add_parser("consensus", help="estimativas BEst para um periodo")
    add_common(p_cons)
    p_cons.add_argument("--period", default="1FY", help="BEST_FPERIOD_OVERRIDE (1FY/2FY/1Q/...)")
    p_cons.set_defaults(func=_cmd_consensus)

    p_hist = sub.add_parser("history", help="serie temporal BDH")
    p_hist.add_argument("empresa")
    p_hist.add_argument("--field", default="PX_LAST")
    p_hist.add_argument("--since", default="2024-01-01", help="YYYY-MM-DD")
    p_hist.add_argument("--until", default=None, help="YYYY-MM-DD (default: hoje)")
    p_hist.add_argument("--refresh", action="store_true")
    p_hist.add_argument("--max-age", type=float, default=24.0, dest="max_age")
    p_hist.set_defaults(func=_cmd_history)

    p_raw = sub.add_parser("raw", help="POST direto pra /api/ com payload JSON")
    p_raw.add_argument("payload", help='ex: \'{"method":"ref","tickers":["PSSA3 BZ Equity"],"flds":["PX_LAST"]}\'')
    p_raw.set_defaults(func=_cmd_raw)

    p_fs = sub.add_parser("field-search", help="busca campos BBG por texto")
    p_fs.add_argument("query")
    p_fs.add_argument("--limit", type=int, default=20)
    p_fs.set_defaults(func=_cmd_field_search)

    p_res = sub.add_parser("resolve", help="resolve empresa/ticker → bbg_ticker (debug)")
    p_res.add_argument("empresa")
    p_res.set_defaults(func=_cmd_resolve)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
