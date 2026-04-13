#!/usr/bin/env python3
"""Extract text from PDF, XLSX, DOCX, PPTX and other files for wiki ingest.
PDFs: opendataloader-pdf first, pdfplumber fallback.
Other formats: markitdown (Microsoft)."""

import argparse
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def json_out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def error_out(msg):
    json_out({"status": "error", "message": msg})
    sys.exit(1)


def extract_pdf_from_zip(zip_path: Path) -> Path:
    """Extract the first PDF found inside a ZIP to a temp file."""
    with zipfile.ZipFile(zip_path) as zf:
        pdf_names = [n for n in zf.namelist() if n.lower().endswith('.pdf')]
        if not pdf_names:
            error_out(f"No PDF found inside {zip_path}")
        data = zf.read(pdf_names[0])
        tmp = Path(tempfile.mktemp(suffix='.pdf', dir=str(zip_path.parent)))
        tmp.write_bytes(data)
        return tmp


def try_opendataloader(pdf_path: Path, output_path: Path) -> bool:
    """Try opendataloader-pdf. Returns True if successful."""
    try:
        result = subprocess.run(
            [
                sys.executable, '-m', 'opendataloader_pdf',
                str(pdf_path),
                '--format', 'markdown',
                '--use-struct-tree',
                '--table-method', 'cluster',
                '-o', str(output_path),
            ],
            capture_output=True, text=True, timeout=300,
        )
        # opendataloader may create a directory instead of a file — check is_file()
        if result.returncode == 0 and output_path.is_file() and output_path.stat().st_size > 100:
            return True
        # Clean up if it created a directory
        if output_path.is_dir():
            import shutil
            shutil.rmtree(output_path, ignore_errors=True)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False


def extract_with_pdfplumber(pdf_path: Path, output_path: Path) -> int:
    """Extract text using pdfplumber. Returns page count."""
    import pdfplumber
    with pdfplumber.open(str(pdf_path)) as pdf:
        pages = []
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ''
            pages.append(f'<!-- PAGE {i + 1} -->\n{text}')
        page_count = len(pdf.pages)
    output_path.write_text('\n\n'.join(pages), encoding='utf-8')
    return page_count


def extract_with_markitdown(input_path: Path, output_path: Path) -> dict:
    """Extract non-PDF files (XLSX, DOCX, PPTX, CSV, HTML) using markitdown."""
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(str(input_path))
    content = result.text_content
    if not content or len(content.strip()) < 10:
        error_out(f"markitdown produced empty output for {input_path}")
    output_path.write_text(content, encoding='utf-8')
    return {"chars": len(content), "method": "markitdown"}


MARKITDOWN_EXTENSIONS = {'.xlsx', '.xls', '.docx', '.pptx', '.csv', '.html', '.htm', '.txt'}


def main():
    parser = argparse.ArgumentParser(description="Extract text from files for wiki ingest")
    parser.add_argument("input", help="Path to PDF or ZIP file")
    parser.add_argument("--output", help="Output markdown path (default: {input}_extracted.md)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        error_out(f"File not found: {input_path}")

    stem = input_path.stem
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{stem}_extracted.md"

    ext = input_path.suffix.lower()

    # Non-PDF formats: use markitdown
    if ext in MARKITDOWN_EXTENSIONS:
        info = extract_with_markitdown(input_path, output_path)
        json_out({
            "status": "ok",
            "output": str(output_path),
            "pages": 1,
            "chars": info["chars"],
            "method": info["method"],
        })
        return

    # Handle ZIP
    tmp_pdf = None
    if input_path.suffix.lower() == '.zip':
        tmp_pdf = extract_pdf_from_zip(input_path)
        pdf_path = tmp_pdf
    else:
        pdf_path = input_path

    # Try opendataloader first
    method = "opendataloader"
    page_count = None
    if not try_opendataloader(pdf_path, output_path):
        method = "pdfplumber"
        try:
            page_count = extract_with_pdfplumber(pdf_path, output_path)
        except Exception as e:
            if tmp_pdf:
                tmp_pdf.unlink(missing_ok=True)
            error_out(f"Both extraction methods failed: {e}")

    if page_count is None:
        content = output_path.read_text(encoding='utf-8')
        page_count = content.count('<!-- PAGE ') or content.count('\n# ') or 1

    chars = output_path.stat().st_size

    if tmp_pdf:
        try:
            tmp_pdf.unlink(missing_ok=True)
        except PermissionError:
            pass  # Windows file lock — temp will be cleaned by OS

    json_out({
        "status": "ok",
        "output": str(output_path),
        "pages": page_count,
        "chars": chars,
        "method": method,
    })


if __name__ == "__main__":
    main()
