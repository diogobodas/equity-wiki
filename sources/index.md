# Sources Index

<!-- Registry of all sources across the five layers (undigested/full/structured/digested/manifests). -->

## Discovery — start here when modeling

For any modeling or analysis task targeting a specific empresa, **read `sources/manifests/{empresa}.json` first**. It tells you which periods exist, which canonical blocks are populated, which source files to consult, how to resolve source conflicts, and what caveats apply. The per-source registry below is a linear history of ingests; the manifest is the indexed, queryable view.

## Workflow

1. Drop raw files (PDF, XLSX, etc) into `undigested/`.
2. Run ingest — LLM reads source and generates the appropriate layers:
   - **ITR / DFP / release** → `full/` + `structured/` + `digested/`
   - **Apresentação / fato relevante / outros** → `full/` + `digested/`
   - **Web** → inline citations + this registry
   - **Notion** → `digested/notion_{slug}.md` + `notion_tracker.md`
3. Original in `undigested/` is deleted.
4. Entry below is added/updated with paths to every layer produced.

To re-extract anything later, re-read the `full/` file — it is content-lossless. Only re-ingest from a fresh original when `full/` itself is missing or corrupted.

## Registry

| Source | Type | Entity | Period | Layers | Reliability | Notes |
|--------|------|--------|--------|--------|-------------|-------|
| Press-release-Tenda-2026-03-31-gmDwJCdg.pdf | file / previa_operacional | tenda | 1T26 | full/tenda/1T26/previa_operacional.md · structured/tenda/1T26/previa_operacional.json · digested/tenda_previa_operacional_1T26_summary.md | — | Prévia operacional (sem DFs). Criou `_schemas/incorporadora.json` v1. Original apagado após ingest. |
| Press-release-Tenda-2026-04-07-j9Gbh6RN (2).xlsx | file / data_pack | tenda | 1T11–1T26 (as-of 1T26) | full/tenda/data_pack_1T26.md · structured/tenda/{76 períodos}/data_pack.json · digested/tenda_data_pack_1T26_summary.md | — | Data pack histórico de RI (15 anos). Destravou DRE/BP/financeiro histórico. Estendeu `_schemas/incorporadora.json` (aditivo: dre/bp/financeiro_ajustado). 1T26 financeiro vazio (aguarda release). Original apagado. |

