#!/usr/bin/env python3
"""CLI wrapper over cvm-api for the fetch agent. JSON output, stateless."""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path


def json_out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def error_out(msg):
    json_out({"status": "error", "message": msg})
    sys.exit(1)


# --- Category mapping ---
TYPE_TO_CVM = {
    "dfp": "EST_4",
    "itr": "EST_3",
    "release": "IPE_7_-1_-1",
    "fato_relevante": "IPE_4_-1_-1",
    "previa_operacional": "IPE_6_-1_-1",
}


def normalize_periodo(data_referencia: str, tipo_wiki: str) -> str:
    """Convert CVM data_referencia (DD/MM/YYYY or YYYY-MM-DD) to wiki period format."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(data_referencia, fmt)
            break
        except ValueError:
            continue
    else:
        return data_referencia

    year_short = str(dt.year)[2:]
    if tipo_wiki == "dfp":
        return str(dt.year)
    month_to_quarter = {3: "1T", 6: "2T", 9: "3T", 12: "4T"}
    quarter = month_to_quarter.get(dt.month)
    if quarter:
        return f"{quarter}{year_short}"
    # Fallback for months that don't align to quarter-end (eventuais)
    q = (dt.month - 1) // 3 + 1
    return f"{q}T{year_short}"


# --- Subcommands ---

def cmd_resolve(args):
    from cvm_api import resolve_company, CompanyNotFoundError
    try:
        company = resolve_company(args.ticker)
        json_out({
            "status": "ok",
            "ticker": company.ticker,
            "nome": company.name,
            "cvm_code": company.cvm_code,
            "setor": company.sector,
        })
    except CompanyNotFoundError as e:
        error_out(str(e))


async def _list_docs(args):
    from cvm_api import resolve_company, buscar_documentos, CompanyNotFoundError

    try:
        company = resolve_company(args.ticker)
    except CompanyNotFoundError as e:
        error_out(str(e))

    types = [t.strip() for t in args.types.split(",")]
    date_from = datetime.strptime(args.date_from, "%Y-%m-%d")
    results = []

    for tipo_wiki in types:
        cvm_cat = TYPE_TO_CVM.get(tipo_wiki)
        if not cvm_cat:
            continue
        docs = await buscar_documentos(
            empresa=company.cvm_code,
            categoria=cvm_cat,
            data_de=date_from.strftime("%d/%m/%Y"),
            data_ate=datetime.now().strftime("%d/%m/%Y"),
            periodo="2",
        )
        for doc in docs:
            periodo = normalize_periodo(doc.data_referencia, tipo_wiki)
            results.append({
                "tipo": tipo_wiki,
                "periodo": periodo,
                "data_ref": doc.data_referencia,
                "data_entrega": doc.data_entrega,
                "num_sequencia": doc.num_sequencia,
                "num_versao": doc.num_versao,
                "numero_protocolo": doc.numero_protocolo,
                "desc_tipo": doc.desc_tipo,
                "empresa_cvm": doc.empresa,
                "versao": doc.versao,
            })

    # Sort: most recent first (by data_ref descending)
    def sort_key(r):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(r["data_ref"], fmt)
            except ValueError:
                continue
        return datetime.min
    results.sort(key=sort_key, reverse=True)

    json_out(results)


def cmd_list(args):
    asyncio.run(_list_docs(args))


async def _download(args):
    from cvm_api import baixar_documento

    file_bytes, filename, content_type = await baixar_documento(
        num_sequencia=args.num_sequencia,
        num_versao=args.num_versao,
        numero_protocolo=args.numero_protocolo,
        desc_tipo=args.desc_tipo,
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(file_bytes)
    json_out({
        "status": "ok",
        "path": str(output_path),
        "size_bytes": len(file_bytes),
        "original_filename": filename,
        "content_type": content_type,
    })


def cmd_download(args):
    asyncio.run(_download(args))


async def _batch_download(args):
    """Download multiple documents concurrently."""
    docs = json.loads(args.docs_json)
    concurrency = int(args.concurrency)
    semaphore = asyncio.Semaphore(concurrency)

    async def download_one(doc):
        async with semaphore:
            from cvm_api import baixar_documento
            try:
                file_bytes, filename, content_type = await baixar_documento(
                    num_sequencia=doc["num_sequencia"],
                    num_versao=doc["num_versao"],
                    numero_protocolo=doc["numero_protocolo"],
                    desc_tipo=doc["desc_tipo"],
                )
                output_path = Path(doc["output"])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(file_bytes)
                return {
                    "status": "ok",
                    "path": str(output_path),
                    "size_bytes": len(file_bytes),
                    "original_filename": filename,
                    "content_type": content_type,
                }
            except Exception as e:
                return {
                    "status": "error",
                    "path": doc.get("output", "?"),
                    "message": str(e),
                }

    results = await asyncio.gather(*[download_one(d) for d in docs])
    json_out(list(results))


def cmd_batch_download(args):
    asyncio.run(_batch_download(args))


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="CVM fetch tool for equity-wiki")
    sub = parser.add_subparsers(dest="command", required=True)

    # resolve
    p_resolve = sub.add_parser("resolve", help="Resolve ticker to company info")
    p_resolve.add_argument("ticker", help="e.g. TEND3")

    # list
    p_list = sub.add_parser("list", help="List available documents from CVM")
    p_list.add_argument("ticker", help="e.g. TEND3")
    p_list.add_argument("--types", default="dfp,itr,release,fato_relevante,previa_operacional",
                        help="Comma-separated document types")
    p_list.add_argument("--from", dest="date_from", required=True,
                        help="Start date YYYY-MM-DD")

    # download
    p_dl = sub.add_parser("download", help="Download a specific document")
    p_dl.add_argument("--num-sequencia", required=True)
    p_dl.add_argument("--num-versao", required=True)
    p_dl.add_argument("--numero-protocolo", required=True)
    p_dl.add_argument("--desc-tipo", required=True)
    p_dl.add_argument("--output", required=True, help="Output file path")

    # batch-download
    p_batch = sub.add_parser("batch-download", help="Download multiple documents concurrently")
    p_batch.add_argument("--docs-json", required=True,
                         help='JSON array of {num_sequencia, num_versao, numero_protocolo, desc_tipo, output}')
    p_batch.add_argument("--concurrency", default="6", help="Max concurrent downloads (default: 6)")

    args = parser.parse_args()
    {"resolve": cmd_resolve, "list": cmd_list, "download": cmd_download,
     "batch-download": cmd_batch_download}[args.command](args)


if __name__ == "__main__":
    main()
