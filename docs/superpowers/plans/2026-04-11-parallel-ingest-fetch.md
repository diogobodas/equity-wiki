# Parallel Ingest & Fetch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Parallelize `ingest.sh` (one `claude --print` per file, N concurrent) and `fetch.sh` (parallel CVM downloads), cutting wall-clock time ~Nx.

**Architecture:** Both scripts already have natural isolation — each file produces outputs in its own `{empresa}/{periodo}/` directory. The only shared resources are `manifest.json` (updated by `manifest_update.py`) and `log.md` (append-only). We parallelize the LLM/download phase and keep manifest updates sequential. A `parallel_run` bash helper manages concurrency with a configurable cap (default 4).

**Tech Stack:** Bash (job control, `wait -n`), Python (existing scripts unchanged), `claude --print` (existing invocation pattern)

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `tools/lib/parallel.sh` | Create | Bash helper: `parallel_run` function that manages N concurrent background jobs |
| `tools/ingest.sh` | Modify | Use `parallel_run` for heavy/light ingest phases; keep manifest + wiki sequential |
| `tools/fetch.sh` | Modify | Parallelize downloads in normal mode (Python-level, not LLM) |
| `tools/lib/cvm_fetch.py` | Modify | Add `batch-download` subcommand that downloads N files concurrently |

---

### Task 1: Create `tools/lib/parallel.sh` — concurrency helper

**Files:**
- Create: `tools/lib/parallel.sh`

- [ ] **Step 1: Write the parallel_run function**

```bash
#!/usr/bin/env bash
# parallel.sh — run N commands concurrently, wait for all, collect exit codes.
#
# Usage:
#   source tools/lib/parallel.sh
#   parallel_init 4                    # max 4 concurrent jobs
#   parallel_add "command1 arg1 arg2"
#   parallel_add "command2 arg1 arg2"
#   ...
#   parallel_wait                      # blocks until all done, returns worst exit code

_PAR_MAX=4
_PAR_PIDS=()
_PAR_CMDS=()
_PAR_WORST=0

parallel_init() {
    _PAR_MAX="${1:-4}"
    _PAR_PIDS=()
    _PAR_CMDS=()
    _PAR_WORST=0
}

parallel_add() {
    local cmd="$1"
    # If at capacity, wait for one slot to free up
    while (( ${#_PAR_PIDS[@]} >= _PAR_MAX )); do
        _par_wait_one
    done
    eval "$cmd" &
    _PAR_PIDS+=($!)
    _PAR_CMDS+=("$cmd")
}

_par_wait_one() {
    # Wait for any one child to finish
    wait -n 2>/dev/null || true
    # Reap finished PIDs
    local new_pids=()
    local new_cmds=()
    for i in "${!_PAR_PIDS[@]}"; do
        if kill -0 "${_PAR_PIDS[$i]}" 2>/dev/null; then
            new_pids+=("${_PAR_PIDS[$i]}")
            new_cmds+=("${_PAR_CMDS[$i]}")
        else
            wait "${_PAR_PIDS[$i]}" 2>/dev/null
            local rc=$?
            (( rc > _PAR_WORST )) && _PAR_WORST=$rc
        fi
    done
    _PAR_PIDS=("${new_pids[@]}")
    _PAR_CMDS=("${new_cmds[@]}")
}

parallel_wait() {
    for i in "${!_PAR_PIDS[@]}"; do
        wait "${_PAR_PIDS[$i]}" 2>/dev/null
        local rc=$?
        (( rc > _PAR_WORST )) && _PAR_WORST=$rc
    done
    _PAR_PIDS=()
    _PAR_CMDS=()
    return $_PAR_WORST
}
```

- [ ] **Step 2: Test the helper in isolation**

```bash
source tools/lib/parallel.sh
parallel_init 2
parallel_add "sleep 1 && echo job1"
parallel_add "sleep 1 && echo job2"
parallel_add "sleep 1 && echo job3"
parallel_wait
echo "exit: $?"
```

Expected: job1 and job2 start simultaneously, job3 starts after one finishes. Total ~2s not ~3s.

- [ ] **Step 3: Commit**

```bash
git add tools/lib/parallel.sh
git commit -m "feat: add parallel.sh concurrency helper for ingest/fetch"
```

---

### Task 2: Refactor `ingest.sh` — one `claude --print` per file

**Files:**
- Modify: `tools/ingest.sh`

The key change: instead of passing `FILE_LIST` (all files) to one `claude --print`, we loop over files and launch one agent per file in parallel.

- [ ] **Step 1: Add concurrency flag and source parallel.sh**

At the top of `ingest.sh`, after the existing argument parsing, add:

```bash
# After: TICKER="$1"; shift
CONCURRENCY=4
while [[ $# -gt 0 ]]; do
    case "$1" in
        --concurrency|-j) CONCURRENCY="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; usage ;;
    esac
done

source "$SCRIPT_DIR/lib/parallel.sh"
```

Update `usage()`:

```bash
usage() {
    echo "Usage: bash tools/ingest.sh <TICKER> [--concurrency N]"
    echo ""
    echo "Processes all files in sources/undigested/ for the given ticker."
    echo "Accepts any PDF, ZIP, or XLSX — from fetch agent or dropped manually."
    echo ""
    echo "Options:"
    echo "  --concurrency, -j N   Max parallel ingest agents (default: 4)"
    exit 1
}
```

- [ ] **Step 2: Create `ingest_one_heavy` helper function**

Add this function after the `invoke_claude` function:

```bash
# --- Helper: ingest one file (heavy path) ---
ingest_one_heavy() {
    local extracted_file="$1"
    local doc_type="$2"
    local log_prefix="[heavy:$(basename "$extracted_file")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_heavy.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{DOC_TYPE}}" "$doc_type" \
        "{{SCHEMA_PATH}}" "$SCHEMA_PATH" \
        "{{FILE_LIST}}" "- $extracted_file"

    echo "$log_prefix Done."
}
```

- [ ] **Step 3: Create `ingest_one_light` helper function**

```bash
# --- Helper: ingest one file (light path) ---
ingest_one_light() {
    local extracted_file="$1"
    local log_prefix="[light:$(basename "$extracted_file")]"

    echo "$log_prefix Starting..."

    invoke_claude "$SCRIPT_DIR/prompts/ingest_light.md" \
        "{{TICKER}}" "$TICKER" \
        "{{EMPRESA}}" "$EMPRESA" \
        "{{FILE_LIST}}" "- $extracted_file"

    echo "$log_prefix Done."
}
```

- [ ] **Step 4: Replace the sequential release ingest block with parallel dispatch**

Replace the entire `# --- Step 3: Ingest heavy ITR/DFP ---` through `# --- Step 5: Ingest light fatos ---` blocks (and the other/fatos blocks) with a single parallel dispatch:

```bash
# --- Step 3: Parallel ingest ---
echo "=== Parallel ingest (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"

# Heavy: ITR/DFP
for f in "${EXTRACTED_ITR_DFP[@]}"; do
    parallel_add "ingest_one_heavy \"$f\" \"itr/dfp\""
done

# Heavy: releases
for f in "${EXTRACTED_RELEASE[@]}"; do
    parallel_add "ingest_one_heavy \"$f\" \"release\""
done

# Heavy: other
for f in "${EXTRACTED_OTHER[@]}"; do
    parallel_add "ingest_one_heavy \"$f\" \"other\""
done

# Light: fatos relevantes
for f in "${EXTRACTED_FATOS[@]}"; do
    parallel_add "ingest_one_light \"$f\""
done

parallel_wait
echo "=== All ingest agents complete ==="
echo ""
```

- [ ] **Step 5: Keep manifest updates sequential (after parallel phase)**

The manifest update loop stays sequential AFTER `parallel_wait`. This is already the case in the current code — the `python manifest_update.py` calls happen after `invoke_claude`. Keep them as-is but move them into a clearly-separated "Step 4: Manifest updates" block:

```bash
# --- Step 4: Sequential manifest updates ---
echo "=== Updating manifest ==="

for f in "${EXTRACTED_ITR_DFP[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    tipo=$(echo "$fname" | sed -E 's/^[^_]+_[^_]+_([^_]+)_.*/\1/')
    digested="sources/digested/${EMPRESA}_${tipo}_${period}_summary.md"
    DIGESTED_FILES+=("$digested")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type "$tipo" --period "$period" \
        --full "sources/full/$EMPRESA/$period/${tipo}.md" \
        --structured "sources/structured/$EMPRESA/$period/${tipo}.json" \
        --digested "$digested" \
        --log "$REPO_ROOT/log.md"
done

for f in "${EXTRACTED_RELEASE[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    digested="sources/digested/${EMPRESA}_release_${period}_summary.md"
    DIGESTED_FILES+=("$digested")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type release --period "$period" \
        --full "sources/full/$EMPRESA/$period/release.md" \
        --structured "sources/structured/$EMPRESA/$period/release.json" \
        --digested "$digested" \
        --log "$REPO_ROOT/log.md"
done

FATOS_DIGESTED="sources/digested/${EMPRESA}_fatos_relevantes_batch_summary.md"
for f in "${EXTRACTED_FATOS[@]}"; do
    fname=$(basename "$f")
    period=$(echo "$fname" | sed -E 's/^[^_]+_([^_]+)_.*/\1/')
    seq=$(echo "$fname" | sed -E 's/.*fato_relevante_([0-9]+).*/\1/')
    DIGESTED_FILES+=("$FATOS_DIGESTED")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type fato_relevante --period "$period" \
        --full "sources/full/$EMPRESA/$period/fato_relevante_${seq}.md" \
        --digested "$FATOS_DIGESTED" \
        --log "$REPO_ROOT/log.md"
done

for f in "${EXTRACTED_OTHER[@]}"; do
    fname=$(basename "$f")
    stem="${fname%_extracted.*}"
    stem="${stem%.*}"
    digested="sources/digested/${EMPRESA}_other_${stem}_summary.md"
    DIGESTED_FILES+=("$digested")

    python "$SCRIPT_DIR/lib/manifest_update.py" \
        --manifest "$MANIFEST_PATH" \
        --type release --period "unknown" \
        --full "sources/full/$EMPRESA/other/${stem}.md" \
        --digested "$digested" \
        --log "$REPO_ROOT/log.md" 2>/dev/null || true
done

# Deduplicate DIGESTED_FILES
DIGESTED_FILES=($(printf '%s\n' "${DIGESTED_FILES[@]}" | sort -u))
echo ""
```

- [ ] **Step 6: Fix the ITR/DFP classification regex**

The current regex in the file classification section only matches `*_itr.zip` / `*_dfp.zip`, but the fetch agent produces filenames like `CURY3_1T23_itr_126022.zip`. Fix:

```bash
# Old:
if [[ "$fname" == *_itr.zip ]] || [[ "$fname" == *_dfp.zip ]] || [[ "$fname" == *_itr.pdf ]] || [[ "$fname" == *_dfp.pdf ]]; then

# New:
if [[ "$fname" =~ _itr[_.]  ]] || [[ "$fname" =~ _dfp[_.] ]]; then
```

- [ ] **Step 7: Export functions for subshell visibility**

Because `parallel_add` uses `eval "$cmd" &`, the helper functions must be exported:

```bash
export -f ingest_one_heavy ingest_one_light invoke_claude
export TICKER EMPRESA SCHEMA_PATH SCRIPT_DIR
```

Add these lines right after defining the functions and before the parallel dispatch block.

- [ ] **Step 8: Test with dry run**

```bash
bash tools/ingest.sh CURY3 --concurrency 2
```

Verify: agents launch in pairs, manifest updates happen after all agents finish, wiki update runs at the end.

- [ ] **Step 9: Commit**

```bash
git add tools/ingest.sh
git commit -m "feat: parallel ingest — one claude agent per file, configurable concurrency"
```

---

### Task 3: Add `batch-download` to `cvm_fetch.py`

**Files:**
- Modify: `tools/lib/cvm_fetch.py`

- [ ] **Step 1: Add async batch download function**

Add after the existing `_download` function:

```python
async def _batch_download(args):
    """Download multiple documents concurrently."""
    import aiohttp

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
```

- [ ] **Step 2: Register the subcommand in the CLI parser**

In `main()`, add:

```python
# batch-download
p_batch = sub.add_parser("batch-download", help="Download multiple documents concurrently")
p_batch.add_argument("--docs-json", required=True,
                      help='JSON array of {num_sequencia, num_versao, numero_protocolo, desc_tipo, output}')
p_batch.add_argument("--concurrency", default="6", help="Max concurrent downloads (default: 6)")
```

And in the dispatch dict:

```python
{"resolve": cmd_resolve, "list": cmd_list, "download": cmd_download,
 "batch-download": cmd_batch_download}[args.command](args)
```

- [ ] **Step 3: Test batch-download**

```bash
python tools/lib/cvm_fetch.py batch-download --concurrency 2 --docs-json '[
  {"num_sequencia":"1013143","num_versao":"1","numero_protocolo":"1488437","desc_tipo":"IPE","output":"/tmp/test1.pdf"},
  {"num_sequencia":"1013149","num_versao":"1","numero_protocolo":"1488443","desc_tipo":"IPE","output":"/tmp/test2.pdf"}
]'
```

Expected: JSON array of 2 results, both with `"status": "ok"`.

- [ ] **Step 4: Commit**

```bash
git add tools/lib/cvm_fetch.py
git commit -m "feat: add batch-download to cvm_fetch.py for parallel CVM downloads"
```

---

### Task 4: Parallelize downloads in `fetch.sh`

**Files:**
- Modify: `tools/fetch.sh`
- Modify: `tools/prompts/fetch_system.md`

The fetch agent (claude --print) currently downloads files one at a time via `cvm_fetch.py download`. We give it the `batch-download` command instead.

- [ ] **Step 1: Update `fetch_system.md` to document batch-download**

Add to the "Your tools" section:

```markdown
### batch-download
```bash
python tools/lib/cvm_fetch.py batch-download --concurrency 6 --docs-json '<JSON_ARRAY>'
```
Downloads multiple files concurrently. Input: JSON array where each element has `num_sequencia`, `num_versao`, `numero_protocolo`, `desc_tipo`, `output`. Returns a JSON array of results.

**Use this instead of individual `download` calls.** Build the full list of gaps first, then download all at once.
```

- [ ] **Step 2: Update the Algorithm section in `fetch_system.md`**

Replace step 4 with:

```markdown
4. **Build download batch** — collect all gap documents into a JSON array for `batch-download`:
   ```json
   [
     {"num_sequencia": "X", "num_versao": "Y", "numero_protocolo": "Z", "desc_tipo": "W", "output": "sources/undigested/TICKER_periodo_tipo_seq.ext"},
     ...
   ]
   ```
   Then download all at once:
   ```bash
   python tools/lib/cvm_fetch.py batch-download --concurrency 6 --docs-json '<JSON_ARRAY>'
   ```

5. **Post-download filtering** (releases/fatos only, if fetch_profile exists):
   - For each downloaded release/fato, classify using fetch_profile categories.
   - Delete files matching categories with `"action": "exclude"`.
   - Report unclassified files as "included by default".
```

- [ ] **Step 3: Test fetch with batch-download**

```bash
bash tools/fetch.sh CURY3 --types release --horizon 6m
```

Verify: agent builds a batch JSON and downloads concurrently instead of one-by-one.

- [ ] **Step 4: Commit**

```bash
git add tools/prompts/fetch_system.md tools/fetch.sh
git commit -m "feat: parallel fetch downloads via batch-download in cvm_fetch.py"
```

---

### Task 5: Parallel PDF extraction in `ingest.sh`

**Files:**
- Modify: `tools/ingest.sh`

The PDF extraction phase (`pdf_extract.py` per file) is also sequential. Parallelize it too.

- [ ] **Step 1: Replace sequential extraction loops with parallel dispatch**

Replace all 4 extraction loops (ITR_DFP, RELEASE, FATOS, OTHER) with:

```bash
echo "=== Pre-processing PDFs (concurrency=$CONCURRENCY) ==="
parallel_init "$CONCURRENCY"

# Build ALL_FILES array pairing original → extracted path
ALL_EXTRACTIONS=()

for f in "${HEAVY_ITR_DFP[@]}" "${HEAVY_RELEASE[@]}" "${LIGHT_FATOS[@]}" "${HEAVY_OTHER[@]}"; do
    parallel_add "python \"$SCRIPT_DIR/lib/pdf_extract.py\" \"$f\""
done

parallel_wait
echo ""
```

Then reconstruct the EXTRACTED_* arrays by convention (each original `foo.pdf` → `foo_extracted.md`):

```bash
# Reconstruct extracted paths (pdf_extract.py uses {stem}_extracted.md by default)
EXTRACTED_ITR_DFP=()
for f in "${HEAVY_ITR_DFP[@]}"; do
    stem="${f%.*}"
    EXTRACTED_ITR_DFP+=("${stem}_extracted.md")
done

EXTRACTED_RELEASE=()
for f in "${HEAVY_RELEASE[@]}"; do
    stem="${f%.*}"
    EXTRACTED_RELEASE+=("${stem}_extracted.md")
done

EXTRACTED_FATOS=()
for f in "${LIGHT_FATOS[@]}"; do
    stem="${f%.*}"
    EXTRACTED_FATOS+=("${stem}_extracted.md")
done

EXTRACTED_OTHER=()
for f in "${HEAVY_OTHER[@]}"; do
    stem="${f%.*}"
    EXTRACTED_OTHER+=("${stem}_extracted.md")
done
```

- [ ] **Step 2: Test extraction parallelism**

Drop 4 small PDFs in `sources/undigested/`, run `bash tools/ingest.sh TICKER -j 4`, verify extractions run concurrently (check timestamps in output).

- [ ] **Step 3: Commit**

```bash
git add tools/ingest.sh
git commit -m "feat: parallel PDF extraction in ingest.sh"
```

---

## Summary of changes

| Before | After | Speedup |
|--------|-------|---------|
| 1 `claude --print` for ALL releases | N `claude --print` (1 per file), max 4 concurrent | ~4x on LLM phase |
| Sequential PDF extraction | Parallel extraction, max N concurrent | ~Nx on extraction |
| Sequential CVM downloads (1 per agent tool call) | `batch-download` with asyncio semaphore (6 concurrent) | ~6x on download |
| Manifest updates interleaved | Manifest updates sequential after all agents | Same speed, no race condition |
| Wiki update at end | Wiki update at end (unchanged) | Same |
