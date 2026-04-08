# Wiki Operation Log

<!-- Append-only chronological log of all wiki operations. -->
<!-- Format: ## YYYY-MM-DD — operation type — short description -->

## 2026-04-08 — reset — Wiki rebuilt from scratch following Karpathy LLM-wiki pattern. Infrastructure created (SCHEMA.md, CLAUDE.md, README.md, index.md, log.md, _coverage_tracker.md, sources/).

## 2026-04-08 — schema v2 — SCHEMA.md rewritten to four-layer architecture (undigested → full → structured → digested), adding modeling substrate alongside the knowledge wiki. CLAUDE.md, README.md, index.md, sources/index.md propagated. No sources had been digested yet, so no migration needed. Introduced `promote_nota` operation, `type: nota` page type, and per-sector canonical JSON schemas in `sources/structured/_schemas/`.

## 2026-04-08 — schema addition — added `previa_operacional` to the source type tokens list in SCHEMA.md to accommodate incorporadora operational previews that precede full earnings releases.

## 2026-04-08 — design — manifest v1 (discovery layer)

**Problem.** The 4-layer architecture (undigested/full/structured/digested/wiki) works great for ingest and narrative, but a cold-start modeling agent — an LLM agent with no prior context, asked to e.g. "build the full historical model for Tenda 2020-2025" — has to pay a non-trivial discovery cost every time: list directories, open multiple JSONs to infer coverage, guess which of several sources wins for a given period/field, and piece together caveats from prose in entity pages. This cost is paid per agent run, so it scales badly as we cover more empresas or run the same workflow repeatedly.

**Options considered.**
1. **Per-empresa manifest** — one JSON per empresa at `sources/manifests/{empresa}.json`, auto-updated at end of every ingest for that empresa.
2. **Single global manifest** — `sources/_manifest.json` covering all empresas. Simpler read but file grows fast and every ingest touches it (merge conflicts).
3. **Derived at runtime** — document a discovery protocol, no persisted manifest. Zero maintenance but defeats the purpose (cost paid every run).

**Decision.** Option 1 — per-empresa manifest. Manufacturing unit matches ingest unit (one empresa → one manifest), no merge conflicts, precedence/caveats (which are human-curated, non-derivable info) have a clear home.

**Manifest shape.** `_schema: manifest/v1`, empresa metadata, `coverage` map (period → block → {status, source, reason?}), `sources` inventory, `precedence` rules (ordered), `caveats` list, `related_digests`. Status values: `filled | partial | empty | na`. See SCHEMA.md §"The manifests/ layer" for full specification.

**Companion changes.**
- Added **mandatory `_schema_path`** field to all structured JSONs — agents should never have to infer the schema file location from the `_schema` identifier.
- Added **lint item #9: manifest staleness** (stale/rotten/missing/coverage-mismatch checks).
- Added lint item #8: missing `_schema_path`.
- Architecture description bumped from 4 layers to 5 layers throughout SCHEMA.md and CLAUDE.md. Modeling operation now explicitly begins with "read `sources/manifests/{empresa}.json` first".
- Ingest flows (heavy and light) now include an explicit "update manifest" step.

**Explicitly not done (deferred).** An `AGENT_READER.md` reader-focused guide separate from SCHEMA.md — user requested to stay focused on the wiki core for now.

## 2026-04-08 — backfill — applied manifest v1 to existing state (Tenda only)

- Ran one-shot ephemeral script (`%TEMP%/tenda_ingest/backfill_manifest.py`, not committed).
- **Phase 1:** added `_schema_path` field to 77 existing structured JSONs under `sources/structured/tenda/` (76 `data_pack.json` + 1 `previa_operacional.json`). All point to `sources/structured/_schemas/incorporadora.json`.
- **Phase 2:** generated `sources/manifests/tenda.json` from current disk state. Coverage matrix built by inspecting each structured file and classifying each canonical block as filled/partial/empty. Results:
  - 76 periods covered (1T11 → 1T26 quarterly + 2011 → 2025 annual).
  - 1T26: operacional `filled`, dre/bp/financeiro_ajustado `empty` (with `reason: "release completo do 1T26 ainda não publicado"`).
  - 4T25 → 1T12: all four blocks `filled` (data_pack canonical + DRE + BP + financeiro_ajustado).
  - 1T11, 2T11, 2011: operacional/dre/bp `filled`, financeiro_ajustado `partial` — makes sense, management-adjusted metrics like ROE LTM and dívida líquida ajustada weren't tracked in that format back then.
  - 2 sources registered: `previa_operacional` (1 structured file) and `data_pack` (76 structured files, referenced via glob).
  - 3 precedence rules codifying the previa_operacional-vs-data_pack conflict at 1T26 and the data_pack-wins-everywhere-else rule for financial blocks.
  - 6 caveats covering the 2021–2023 crisis arc, Alea history horizon, BP stand-alone gap, 1T26 incompleteness, redução de capital, and Pode Entrar program.
- Updated `sources/index.md` to point at the manifest as the first read for modeling tasks.
- Validated: manifest is internally consistent, all referenced paths exist on disk.

## 2026-04-08 — schema addition — added `data_pack` to the source type tokens in SCHEMA.md. Data packs are RI-maintained historical spreadsheets spanning many periods; full/ path is `full/{empresa}/data_pack_{asof}.md` (no per-period subfolder) since they are single as-of documents, while structured/ gets exploded into per-period files.

## 2026-04-08 — schema extension — `_schemas/incorporadora.json` extended (additive, no version bump) with full DRE, BP and `financeiro_ajustado` blocks after the Tenda data pack ingest. Previously-declared-null financial blocks are now schematized. Revision note added in the schema file itself.

## 2026-04-08 — ingest (file, data_pack) — **Tenda data pack as-of 1T26** (`Press-release-Tenda-2026-04-07-j9Gbh6RN (2).xlsx`). Heavy path, incremental.
- Ingest driven by a one-shot Python script (openpyxl → md/json). Script not committed to the repo — ephemeral tooling in `%TEMP%/tenda_ingest/ingest.py`.
- Source spans 1T11 → 1T26 across 12 sheets (Tenda/Alea/Consolidado × Operacional/Financeiro/DRE + BP for Consolidado and Alea).
- Created `sources/full/tenda/data_pack_1T26.md` — 2296 lines, transposed tables (períodos como linhas, métricas como colunas), chunked em grupos de ≤12 colunas por tabela para legibilidade. Content-lossless transcription of all 12 sheets.
- Created 76 per-period `sources/structured/tenda/{period}/data_pack.json` files covering all quarters 1T11–1T26 and annuals 2011–2025. Each file has `canonical.{operacional, dre, bp, financeiro_ajustado}` + `company_specific.segmentos.{tenda_mcmv, alea_sbpe}`.
- 1T26 data_pack.json has operacional preenchido mas DRE/BP/financeiro em null — release completo do 1T26 ainda não publicado quando a planilha foi gerada. Será preenchido quando o release for ingerido.
- Alea histórico só existe ~2020→1T26; períodos anteriores só têm Tenda MCMV.
- Coexiste com `structured/tenda/1T26/previa_operacional.json` (fonte diferente, ingerido horas antes). Cross-check: vendas líquidas consolidadas 1T26 = R$ 1.533,0 mm em ambas as fontes. ✓
- Updated `tenda.md` com seção "Arco histórico 2020–2025" cobrindo o ciclo de quase-quebra (prejuízo R$ 547 mm em 2022, ROE −57%) e turnaround (lucro R$ 506 mm em 2025, ROE 47%). Crítico para modelagem: pré-2024 é empresa estruturalmente diferente.
- Created `sources/digested/tenda_data_pack_1T26_summary.md`.
- Updated `sources/index.md`. Deleted XLSX from `sources/undigested/`.
- Notas para futuros ingests: (a) o padrão "data pack RI" provavelmente se repete para outros emissores (MRV, Cyrela, Direcional publicam planilhas similares) — reusar o mesmo `_source_type: data_pack` e explodir por período. (b) Script de ingest é rewrite-friendly: quando o próximo data pack chegar (ex: as-of 2T26), o mesmo script pode ser adaptado para reprocessar — o full/ antigo fica preservado como histórico, novo full/tenda/data_pack_2T26.md substitui as-of; structured/ pode ser re-escrito por período. (c) BP consolidado está completo mas stand-alone Tenda MCMV não — BP por segmento virá só via DFP detalhada.

## 2026-04-08 — ingest (file, previa_operacional) — **Tenda 1T26 prévia operacional** (`Press-release-Tenda-2026-03-31-gmDwJCdg.pdf`). Heavy path.
- Created `sources/structured/_schemas/incorporadora.json` (v1) — first incorporadora ingest. Canonical schema centered on operational metrics (lançamentos, vendas brutas/líquidas, distratos, VSO, repasses, entregas, obras, banco de terrenos); DRE/BP/FC declared but null, to be populated on first ITR/release ingest.
- Created `sources/full/tenda/1T26/previa_operacional.md` — structured-but-uncut transcription of the 8-page PDF, including all tables, all 1T26/4T25/1T25 comparatives, and the 9-quarter historical series for Tenda and Alea segments.
- Created `sources/structured/tenda/1T26/previa_operacional.json` — canonical filled with consolidated Tenda+Alea; company_specific holds segment breakdowns (tenda_mcmv, alea_sbpe), Pode Entrar adjustments for 3T24, 9-quarter operational history per segment, and notable events.
- Created `sources/digested/tenda_previa_operacional_1T26_summary.md` — wiki-facing TL;DR.
- Created wiki pages: `tenda.md` (entity), `incorporadoras.md` (sector), `vgv.md`, `vso.md`, `distrato.md`, `banco_de_terrenos.md`, `repasses.md`, `mcmv.md` (concepts).
- Updated `index.md` and `sources/index.md`.
- Deleted original PDF from `sources/undigested/`.
- Notes for future ingests: (a) Alea is Tenda's 100%-owned SBPE brand, not a separate listed entity — keep as segment under `company_specific.segmentos`. (b) The companion `Press-release-Tenda-2026-04-07-j9Gbh6RN (2).xlsx` was left untouched in `undigested/` per the "one source at a time, do not correlate files" rule. (c) Pode Entrar (SP municipal program) is an ongoing footnote in Tenda's historical series — 3T24 was the main impact quarter. (d) First incorporadora schema created; expect canonical to expand when second incorporadora is ingested and new recurring keys emerge.
