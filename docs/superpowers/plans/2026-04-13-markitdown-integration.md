# MarkItDown Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add markitdown as the extractor for non-PDF formats (XLSX, DOCX, PPTX, CSV, HTML) while keeping the existing PDF pipeline (opendataloader + pdfplumber) unchanged.

**Architecture:** Rename `pdf_extract.py` → `file_extract.py`. Route by file extension: PDFs keep existing two-tier extraction; everything else goes through markitdown. The JSON output contract stays identical so `ingest.sh` needs only the filename reference update.

**Tech Stack:** `markitdown[xlsx,docx,pptx]` (Microsoft), Python 3.10+

---

### Task 1: Install markitdown

**Files:**
- Modify: `tools/lib/pdf_extract.py` (will be renamed in Task 2)

- [ ] **Step 1: Install markitdown with relevant extras**

```bash
pip install "markitdown[xlsx,docx,pptx]"
```

- [ ] **Step 2: Verify installation**

```bash
python -c "from markitdown import MarkItDown; md = MarkItDown(); print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Quick smoke test with a real XLSX**

```bash
python -c "
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert('path/to/any/test.xlsx')
print(result.text_content[:500])
"
```

Expected: markdown with table content visible

---

### Task 2: Extend extractor to support non-PDF formats

**Files:**
- Rename: `tools/lib/pdf_extract.py` → `tools/lib/file_extract.py`
- Create: `tools/lib/pdf_extract.py` (thin wrapper for backwards compat)

- [ ] **Step 1: Rename pdf_extract.py → file_extract.py**

```bash
cd tools/lib
git mv pdf_extract.py file_extract.py
```

- [ ] **Step 2: Add markitdown extraction function to file_extract.py**

Add this function after `extract_with_pdfplumber`, before `main()`:

```python
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
```

- [ ] **Step 3: Update main() to route by extension**

Replace the current `main()` function with routing logic. The key change is: PDF/ZIP keep the existing path, everything else uses markitdown.

```python
MARKITDOWN_EXTENSIONS = {'.xlsx', '.xls', '.docx', '.pptx', '.csv', '.html', '.htm', '.txt'}

def main():
    parser = argparse.ArgumentParser(description="Extract text from files for wiki ingest")
    parser.add_argument("input", help="Path to PDF, ZIP, XLSX, DOCX, PPTX, or other file")
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
    if ext == '.zip':
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
            pass

    json_out({
        "status": "ok",
        "output": str(output_path),
        "pages": page_count,
        "chars": chars,
        "method": method,
    })
```

- [ ] **Step 4: Update the module docstring**

```python
"""Extract text from PDF, XLSX, DOCX, PPTX and other files for wiki ingest.
PDFs: opendataloader-pdf first, pdfplumber fallback.
Other formats: markitdown (Microsoft)."""
```

- [ ] **Step 5: Create backwards-compat wrapper at old path**

Create `tools/lib/pdf_extract.py`:

```python
#!/usr/bin/env python3
"""Backwards compatibility — delegates to file_extract.py."""
from file_extract import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Test the new extractor with a PDF (regression)**

```bash
python tools/lib/file_extract.py test_file.pdf
```

Expected: same JSON output as before, method = "opendataloader" or "pdfplumber"

- [ ] **Step 7: Commit**

```bash
git add tools/lib/file_extract.py tools/lib/pdf_extract.py
git commit -m "refactor: rename pdf_extract → file_extract, add markitdown for XLSX/DOCX/PPTX"
```

---

### Task 3: Update ingest.sh references

**Files:**
- Modify: `tools/ingest.sh`

- [ ] **Step 1: Update the extraction call in ingest.sh (ticker mode)**

In `tools/ingest.sh`, line 196, change `pdf_extract.py` → `file_extract.py`:

```bash
# Before:
parallel_add "python \"$SCRIPT_DIR/lib/pdf_extract.py\" \"$f\""

# After:
parallel_add "python \"$SCRIPT_DIR/lib/file_extract.py\" \"$f\""
```

- [ ] **Step 2: Update the extraction call in generic mode**

In `tools/ingest.sh`, line 59, change:

```bash
# Before:
python "$SCRIPT_DIR/lib/pdf_extract.py" "$GENERIC_FILE" 2>/dev/null || true

# After:
python "$SCRIPT_DIR/lib/file_extract.py" "$GENERIC_FILE" 2>/dev/null || true
```

- [ ] **Step 3: Expand accepted file extensions in the file scan**

In `tools/ingest.sh`, line 172, add new extensions:

```bash
# Before:
elif [[ "$fname" == *.pdf ]] || [[ "$fname" == *.xlsx ]] || [[ "$fname" == *.zip ]]; then

# After:
elif [[ "$fname" == *.pdf ]] || [[ "$fname" == *.xlsx ]] || [[ "$fname" == *.xls ]] || \
     [[ "$fname" == *.docx ]] || [[ "$fname" == *.pptx ]] || [[ "$fname" == *.csv ]] || \
     [[ "$fname" == *.zip ]]; then
```

- [ ] **Step 4: Update the usage text**

Line 9:

```bash
# Before:
echo "Accepts any PDF, ZIP, or XLSX — from fetch agent or dropped manually."

# After:
echo "Accepts PDF, XLSX, DOCX, PPTX, CSV, ZIP — from fetch agent or dropped manually."
```

- [ ] **Step 5: Commit**

```bash
git add tools/ingest.sh
git commit -m "feat: ingest.sh uses file_extract.py, accepts DOCX/PPTX/CSV"
```

---

### Task 4: Update reingest_full.sh and any other references

**Files:**
- Modify: `tools/reingest_full.sh` (if it references pdf_extract.py)

- [ ] **Step 1: Search for remaining references to pdf_extract.py**

```bash
grep -r "pdf_extract" tools/
```

- [ ] **Step 2: Update any found references to file_extract.py**

For each file found, replace `pdf_extract.py` with `file_extract.py`.

- [ ] **Step 3: Update CLAUDE.md**

In the "PDF extraction (standalone)" section, update:

```markdown
### File extraction (standalone)

\`\`\`bash
python tools/lib/file_extract.py <file.pdf>       # PDF (opendataloader + pdfplumber)
python tools/lib/file_extract.py <file.xlsx>      # Excel (markitdown)
python tools/lib/file_extract.py <file.docx>      # Word (markitdown)
# Returns JSON: {"output": "path/to/extracted.md", ...}
\`\`\`
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "docs: update references from pdf_extract to file_extract"
```

---

### Task 5: End-to-end test with real XLSX

- [ ] **Step 1: Drop an XLSX into sources/undigested/**

Use any available financial spreadsheet (e.g., sector comparison).

- [ ] **Step 2: Run generic ingest**

```bash
bash tools/ingest.sh --generic sources/undigested/test_planilha.xlsx
```

- [ ] **Step 3: Verify outputs**

Check that:
- `sources/full/generic/test_planilha.md` exists and has readable table markdown
- `sources/digested/*_summary.md` was created
- `log.md` has a `[wiki-queue]` entry

- [ ] **Step 4: Clean up test artifacts if needed**
