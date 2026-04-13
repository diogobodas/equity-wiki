# Design: Global Wiki Update — desacoplado do ingest

**Date:** 2026-04-13
**Status:** Approved
**Problem:** O wiki update atual roda por empresa dentro do `ingest.sh`, produzindo páginas isoladas sem visão cruzada. Falta `cyrela.md`, comparações com Cyrela, e não aceita fontes genéricas (planilhas de setor, análises macro). As wiki pages precisam ser atualizadas de forma interligada.

## Solution

### New command: `bash tools/wiki_update.sh [--full]`

Desacoplado do ingest. Roda quando o usuário quiser.

- `--full`: lê TODOS os digesteds, ignora a fila. Usado na primeira rodada e para rebuilds.
- Sem flag: lê apenas entries pendentes do `log.md` (changelog).

### Two-phase architecture

**Phase 1 — Planning** (`claude --print` with `tools/prompts/wiki_plan.md`):

Input (assembled by bash):
- List of digesteds to process (all or from queue)
- List of existing wiki pages with frontmatter (type, updated, sources)
- List of empresas with structured/ data

Output: JSON plan delimited by `===WIKI_PLAN_START===` / `===WIKI_PLAN_END===`:

```json
{
  "create": [
    {"page": "cyrela.md", "type": "entity", "digesteds": ["cyrela_dfp_2025_summary.md", "..."]}
  ],
  "update": [
    {"page": "incorporadoras.md", "type": "sector", "digesteds": ["cyrela_dfp_2025_summary.md", "cury_dfp_2025_summary.md", "..."]}
  ],
  "skip": [
    {"page": "mcmv.md", "reason": "no new data affecting this concept"}
  ]
}
```

Each entry maps exactly which digesteds are relevant for that page.

**Phase 2 — Execution** (one `claude --print` per page with `tools/prompts/wiki_write.md`):

Input per page:
- The existing page content (if update)
- The mapped digesteds from the plan
- Page type (entity/concept/sector/comparison)
- List of all wiki pages (for valid wikilinks)

Output: writes/updates the .md file directly via bash.

Execution order: entity pages first → concept → sector → comparison. Sequential, not parallel — pages reference each other.

### Queue format in log.md

Ingest operations append parseable entries:

```
[wiki-queue] 2026-04-12 | cury | itr | 3T25 | sources/digested/cury_itr_3T25_summary.md
[wiki-queue] 2026-04-12 | generic | sector | real_estate | sources/digested/sector_real_estate_comparison.md
```

Format: `[wiki-queue] date | empresa_or_generic | tipo | periodo_or_tag | digested_path`

After successful execution, wiki_update.sh appends `[wiki-done] date | batch_id` to mark consumption.

`--full` mode ignores the queue entirely — lists everything in `sources/digested/`.

### Generic ingest

`bash tools/ingest.sh --generic arquivo.xlsx`

Flow:
1. Extract via pdf_extract.py (PDF/XLSX) → extracted.md
2. Copy to `sources/full/generic/{filename}.md`
3. `claude --print` with `tools/prompts/ingest_generic.md` → produces digested in `sources/digested/{descriptive_name}_summary.md`
4. Append `[wiki-queue]` entry with `empresa=generic`

No ticker, no manifest, no structured/. Free-form digested — the LLM identifies what it is and produces a summary the wiki update can consume.

New directory: `sources/full/generic/`

### Changes to existing ingest.sh

1. **Remove wiki update step** — delete step 6 that invokes `ingest_wiki_update.md`
2. **Append to queue** — after each manifest update, append `[wiki-queue]` entries for each digested produced
3. **Delete `tools/prompts/ingest_wiki_update.md`** — replaced by `wiki_plan.md` + `wiki_write.md`

### File changes summary

| File | Action |
|------|--------|
| `tools/wiki_update.sh` | **Create** — new orchestrator |
| `tools/prompts/wiki_plan.md` | **Create** — planning phase prompt |
| `tools/prompts/wiki_write.md` | **Create** — execution phase prompt |
| `tools/prompts/ingest_generic.md` | **Create** — generic source ingest prompt |
| `tools/ingest.sh` | **Modify** — remove wiki update step, add queue append |
| `tools/prompts/ingest_wiki_update.md` | **Delete** — replaced |
| `README.md` | **Update** — add instructions for wiki_update.sh and generic ingest |

### README update

After implementation, update README.md with:
- How to run `wiki_update.sh --full` (first time / rebuild)
- How to run `wiki_update.sh` (incremental from queue)
- How to ingest generic sources
- How the queue in log.md works
