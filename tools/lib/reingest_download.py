#!/usr/bin/env python3
"""Download CVM documents from a JSON list on stdin. Used by reingest_full.sh."""

import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Usage: python reingest_download.py <TICKER> <UNDIGESTED_DIR>", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1]
    undigested = sys.argv[2]
    script_dir = Path(__file__).resolve().parent

    docs = json.load(sys.stdin)
    total = len(docs)
    downloaded = 0

    for i, doc in enumerate(docs):
        tipo = doc["tipo"]
        periodo = doc["periodo"]
        seq = doc.get("num_sequencia", "unknown")
        fname = f"{ticker}_{periodo}_{tipo}_{seq}"
        ext = ".zip" if tipo in ("itr", "dfp") else ".pdf"
        outpath = os.path.join(undigested, f"{fname}{ext}")

        if os.path.exists(outpath):
            print(f"  [{i+1}/{total}] Skip (exists): {fname}{ext}")
            continue

        print(f"  [{i+1}/{total}] Downloading: {fname}{ext}")
        r = subprocess.run(
            [
                sys.executable,
                str(script_dir / "cvm_fetch.py"),
                "download",
                "--num-sequencia", str(doc.get("num_sequencia", "")),
                "--num-versao", str(doc.get("num_versao", "")),
                "--numero-protocolo", str(doc.get("numero_protocolo", "")),
                "--desc-tipo", str(doc.get("desc_tipo", "")),
                "--output", outpath,
            ],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(f"    WARNING: download failed — {r.stderr[:100]}")
        else:
            downloaded += 1

    print(f"  Downloaded {downloaded}/{total} files")


if __name__ == "__main__":
    main()
