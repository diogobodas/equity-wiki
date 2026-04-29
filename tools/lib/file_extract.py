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


def sanitize_pdf_trailing_padding(pdf_path: Path) -> Path:
    """Strip trailing NUL/whitespace padding after the last %%EOF.

    CVM ITR/DFP zips carry PAdES-style padding (megabytes of \\x00 after the
    last %%EOF, reserved for digital signatures). verapdf — the engine
    behind opendataloader-pdf — refuses to parse those PDFs with
    "Document doesn't contain startxref keyword in the last 1024 bytes".
    pdfplumber tolerates it but produces flat text.

    Returns a path to the sanitized PDF (in same dir as input). If the
    tail is already clean, returns the original path unchanged.
    """
    data = pdf_path.read_bytes()
    eof_idx = data.rfind(b'%%EOF')
    if eof_idx == -1:
        return pdf_path  # not a parseable PDF; let opendataloader fail naturally
    tail = data[eof_idx + 5:]
    # Tail is "clean" if it's empty or only NUL/whitespace bytes
    if not tail or all(b in (0, 0x09, 0x0a, 0x0d, 0x20) for b in tail):
        if not tail:
            return pdf_path
        cleaned = data[:eof_idx + 5] + b'\n'
        out = pdf_path.parent / f"{pdf_path.stem}_sanitized.pdf"
        out.write_bytes(cleaned)
        return out
    # Tail has non-trivial bytes (likely an incremental update / valid trailer);
    # don't touch it.
    return pdf_path


def try_opendataloader(pdf_path: Path, output_path: Path) -> bool:
    """Try opendataloader-pdf. Returns True if successful.

    opendataloader's `-o` is OUTPUT_DIR (not a file path). It writes
    `<input_stem>.md` inside that directory. We point it at a temp dir,
    then copy the generated file to the requested output_path.

    Pre-processes the PDF to strip CVM-style trailing padding so verapdf
    can find the xref table.
    """
    sanitized = sanitize_pdf_trailing_padding(pdf_path)
    sanitized_is_temp = sanitized != pdf_path
    try:
        with tempfile.TemporaryDirectory(prefix='odl_') as tmpdir:
            result = subprocess.run(
                [
                    sys.executable, '-m', 'opendataloader_pdf',
                    str(sanitized),
                    '--format', 'markdown',
                    '--use-struct-tree',
                    '--table-method', 'cluster',
                    '-q',
                    '-o', tmpdir,
                ],
                capture_output=True, text=True, timeout=300,
            )
            if result.returncode != 0:
                return False
            generated = Path(tmpdir) / (sanitized.stem + '.md')
            if not generated.is_file() or generated.stat().st_size < 100:
                return False
            output_path.write_text(
                generated.read_text(encoding='utf-8'), encoding='utf-8'
            )
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
    finally:
        if sanitized_is_temp:
            try:
                sanitized.unlink(missing_ok=True)
            except (PermissionError, OSError):
                pass


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
