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

## 2026-04-08 — ingest (file, dfp) — **Tenda DFP 2024 auditada** (`Tenda-2024-12-31-B9PKrChn.pdf`). Heavy path.
- Created `sources/full/tenda/2024/dfp.md` — transcrição estruturada-mas-uncut do PDF de 68 páginas auditado por PwC: RA (mensagem da admin, destaques, segmentação 4T24 reportado×Tenda Core Recorrente, lançamentos/vendas/repasses/estoque/banco de terrenos, resultados financeiros, governança), BP individual+consolidado, DRE, DRA, DMPL, DFC, DVA, Notas 1–28. Políticas contábeis materiais (Nota 2.3.x) referenciadas à DFP 2025 já ingerida (substancialmente idênticas) para evitar duplicação. Pareceres finais (CF, Comitê de Auditoria, auditores) anotados mas não transcritos linha-a-linha (texto livre não-numérico).
- Created `sources/structured/tenda/2024/dfp.json` — canonical completo (operacional/dre/bp/dfc/financeiro_ajustado) + company_specific denso: dfs_controladora, segmentos on-site/off-site (DRE+BP), destaques 4T24 (reportado, Tenda Core Recorrente, Pode Entrar), nota_10_dividas_detalhe (cronograma+vencimentos+movimentação), debentures_detalhe (3 emissões vivas: 8a/10a/11a, total principal a pagar 493.571), nota_11_swap_trs (posição líquida -18.607 com 6 operações vivas), nota_15_ir_csll (RET 1,92% + RET 1 0,47% primeira aparição), prejuízos fiscais não contabilizados (consol 2.441.726), demandas judiciais, dividendos 2024 (R$ 21 mm a pagar), capital_e_acoes (123.094.246), stock_grant (programas 2018+Alea), nota_21 (custos por natureza completa), nota_22 (resultado financeiro com obs cross-doc da apresentação consolidada juros+SWAP), nota_25 (obras em construção, resultado a apropriar 774.096), partes relacionadas, eventos subsequentes (SWAP jan/25, recompras, cancelamento de 516.094 ações, subscrição GKP fev/25).
- Created `sources/digested/tenda_dfp_2024_summary.md` — TL;DR com cross-check vs data_pack (±0 em receita/lucro/PL/dívida) + 8 pontos não-triviais (apresentação SWAP mudou 2024→2025, RET 1 primeira aparição, capitalização juros caiu, GKP/Alea mudança societária, cessão de crédito 2x, ações tesouraria zeradas).
- Updated `sources/manifests/tenda.json`: novo source entry `dfp@2024`; coverage 2024 redirecionada para dfp.json em dre/bp/financeiro_ajustado + novos blocos dfc/notas_explicativas (filled); 2 novas precedences (dre/bp/notas at 2024 → dfp supersedes data_pack; dfc at 2024 → dfp única fonte); 5 caveats novas (DFP 2024 auditada, mudança apresentação SWAP entre 2024/2025, SWAP passivo em 31/12/24, GKP/Alea evento subsequente, RET 1 primeira aparição); related_digests atualizado.
- Updated `tenda.md` com nova seção "DFP 2024 auditada — o ano da virada" (8 highlights críticos para modelagem) e atualizou lista de cobertura.
- Updated `sources/index.md` com nova linha de registro.
- Deleted original PDF from `sources/undigested/`.
- Notes: (a) **A DFP 2024 confirma que 2024 é o ponto de inflexão real** — DLcorp/PL vira negativa, lucro líquido vira positivo, waiver dos covenants é encerrado. A virada é puxada 100% pelo segmento on-site (Tenda LL +172,7 mm; Alea LL -71,9 mm). (b) **Apresentação do resultado financeiro é diferente entre DFP 2024 e DFP 2025** — 2024 consolida juros+SWAP, 2025 separa. Cross-check OK (131,7+45,5=177,2). (c) **Schema `incorporadora/v1` permanece adequado** — não foi necessário alterar canonical. (d) Próximo ingest natural: ITR 2023 ou DFP 2023 para fechar a transição do ciclo de quase-quebra para o turnaround.

## 2026-04-08 — backfill — tenda 2025 nota 21 (custos e despesas por natureza)
- Trigger: query do usuário sobre breakdown de custo 2025 forçou leitura de `full/tenda/2025/dfp.md §nota_21` (custos, despesas com vendas, G&A, outras op) — não estava no `structured/`. Regra §Query step 6.
- Key path: `structured/tenda/2025/dfp.json :: company_specific.nota_21_custos_despesas_natureza` — quatro tabelas completas (custos_incorporacao_venda, despesas_vendas, g_and_a, outras_receitas_despesas_liquidas) com 2025 + 2024, mais observação da reclassificação de D&A Alea para custo.
- Fonte preservada via `_fonte: full/tenda/2025/dfp.md §nota_21`.

## 2026-04-08 — backfill — tenda 2025 nota 22 (resultado financeiro)
- Trigger: query do usuário sobre resultado financeiro detalhado 2025 forçou leitura de `full/tenda/2025/dfp.md §nota_22` para abrir receitas/despesas que não estavam em `structured/`. Aplicada regra §Query step 6 (write-through backfill N=1).
- Key path: `structured/tenda/2025/dfp.json :: company_specific.nota_22_resultado_financeiro` — receitas (rendimento aplicações 101.984 + receita SWAP 135.049 = 237.033), despesas (juros líq cap −133.596, cessão −82.109, swap 0, outras −16.958 = −232.663), líquido +4.370, comparativo 2024, encargos capitalizados 82.864.
- Fonte preservada via `_fonte: full/tenda/2025/dfp.md §nota_22`.

## 2026-04-10 — re-ingest (file, dfp) — **Tenda DFP 2025 auditada** (re-ingest com opendataloader-pdf)

PDF pré-processado com `opendataloader-pdf` v2.2.1 (`--format markdown --use-struct-tree --table-method cluster`). Gaps preenchidos vs ingest original:

1. **Nota 25 (empreendimentos em construção)** — tabela completa com custo orçado a apropriar no resultado (R$ 1.861.551 mil), resultado a apropriar (R$ 950.149 mil), custo a apropriar em estoque (R$ 1.337.998 mil), percentual segregação patrimonial (66,60%). Antes tinha "[valor não capturado integralmente na extração]".
2. **Nota 26 (transações não caixa)** — quitação de dividendos R$ 559.981 via partes relacionadas (set/2025). Não existia no full/ anterior.
3. **Nota 27 (eventos subsequentes)** — mútuo R$ 5.000 mil com Ambar Tech Participações (30/01/2026, parte relacionada). Não existia no full/ anterior.
4. **Nota 28 (aprovação DFs)** — aprovação em 05/03/2026, signatários. Não existia no full/ anterior.
5. **Declarações e pareceres** — textos completos das 5 seções (declaração diretores DFs, declaração diretores auditores, parecer conselho fiscal, relatório comitê de auditoria com 3 seções, guidance 2026 completo com tabela). Antes era "[Textos completos não transcritos — extração fragmentada]".
6. **Guidance 2026** — tabela completa com 6 métricas/faixas: EBITDA Tenda R$ 950–1.050 mm, EBITDA Alea R$ (70)–(50) mm, vendas líquidas Tenda R$ 5.000–5.500 mm, vendas líquidas Alea R$ 350–450 mm, LL consolidado R$ 520–600 mm, FCO Alea R$ (80)–(60) mm.
7. **DMPL** — continua sem extração textual (página renderizada como imagem no PDF). Resumo manual preservado. Requer hybrid mode (OCR) para extração completa.

- Updated `sources/full/tenda/2025/dfp.md` — header atualizado refletindo pré-processamento, notas 25-28 completas, pareceres/declarações integral.
- Updated `sources/structured/tenda/2025/dfp.json` — backfill nota 25 completa (14 novos campos em `company_specific.segmentacao_construcao`), guidance 2026 expandido (4 novas métricas/faixas).
- Relatório auditores independentes (KPMG, págs 74-79) — renderizado como imagem no PDF, sem extração textual. Parecer sem ressalvas anotado.

## 2026-04-10 — schema addition — PDF pre-processing with opendataloader-pdf

Added `opendataloader-pdf` as the standard PDF pre-processor for all file ingests. New section "PDF pre-processing" in SCHEMA.md documents the CLI (`opendataloader-pdf <file>.pdf --format markdown --hybrid --use-struct-tree`), lifecycle (intermediate `.md` deleted after ingest), and scope (PDF sources only). Heavy and light ingest paths now include step 0 for PDF conversion. CLAUDE.md updated to reference the new tool. Motivation: eliminate extraction gaps in tables, DMPL, pareceres, and visual-heavy pages that the LLM struggles to read directly from PDF binary.

## 2026-04-10 — schema addition — data pack update protocol

Added formal "Ingest (file — data_pack, update)" operation to SCHEMA.md. Covers the full lifecycle when a new-quarter XLSX data pack arrives: full re-processing (spreadsheet is self-contained by design), delta detection with restatement thresholds (>1% or >R$ 1 mm), structured/ overwrite with logging, prior `full/` preserved as historical snapshot, manifest update, digest generation. CLAUDE.md updated with summary reference. Motivation: the ad-hoc note in the Tenda data_pack ingest log was insufficient — a cold-start agent needs an unambiguous protocol for incorporating new-quarter data packs.

## 2026-04-08 — ingest (file, dfp) — **Tenda DFP 2025 auditada** (`Tenda-2025-12-31-wPTjC7R6.pdf`). Heavy path.
- Created `sources/full/tenda/2025/dfp.md` — structured-but-uncut transcription of the 79-page DFP: Relatório da Administração/MD&A, BP individual+consolidado, DRE, DRA, DFC, DVA, Notas 1–25 (contexto, políticas contábeis, contas a receber + cessão de créditos, imóveis a comercializar, partes relacionadas, imobilizado, intangível, investimentos, empréstimos+debêntures+TVM, derivativos SWAP, arrendamento, fornecedores+risco sacado, obrigações compra imóveis, IR/CSLL+RET+prejuízo fiscal, contingências, PL+dividendos+stock grant, LPA, instrumentos financeiros, receita líquida, custos/despesas por natureza, resultado financeiro, remuneração admin, segmentação on-site/off-site, empreendimentos em construção). DMPL e pareceres finais não capturados integralmente pela extração (conteúdo visual/fragmentado) — anotado no próprio arquivo.
- Created `sources/structured/tenda/2025/dfp.json` — canonical completo (operacional/dre/bp/financeiro_ajustado) + company_specific denso (dfs_controladora, segmentos on-site/off-site com BP e DRE, debêntures detalhe com 5 emissões e covenants, prejuízos fiscais, contingências, dividendos 2025, capital e ações, stock grant, SWAPs, partes relacionadas, segmentação de construção, destaques 4T25 do RA).
- Created `sources/digested/tenda_dfp_2025_summary.md` — TL;DR com cross-check vs data_pack (±0 em receita, lucro, PL, dívida líq) e 8 pontos não-triviais para modelagem (prejuízo fiscal RET, SWAP como ruído de ~R$ 180 mm no financeiro, segmentação Tenda +R$ 636 mm vs Alea −R$ 152 mm, guidance 2026, etc).
- Updated `sources/manifests/tenda.json`: novo source entry `dfp@2025`; coverage 2025 redirecionada para dfp.json em dre/bp/financeiro_ajustado + novos blocos dfc e notas_explicativas (filled); 2 novas precedences (dre/bp/notas at 2025 annual → dfp supersedes data_pack; dfc at 2025 → dfp única fonte); 3 caveats adicionadas (auditado vs gerencial, SWAP ex-financeiro, RET drives alíquota efetiva).
- Updated `tenda.md` com nova seção "DFP 2025 auditada — o que destravou" consolidando as descobertas principais, e atualizou lista de cobertura.
- Updated `sources/index.md` com nova linha de registro.
- Deleted original PDF from `sources/undigested/`.
- Notes for future ingests: (a) schema `incorporadora/v1` segue adequado — DFC entrou via company_specific/canonical (canonical.dre e canonical.bp não tinham DFC declarada; próxima revisão pode promover DFC ao canonical se outras incorporadoras também trouxerem). (b) Separar `dre/bp/dfc/notas_explicativas` como blocos distintos em `coverage` é útil — coverage no manifest agora usa esses novos keys ao lado de `operacional`/`financeiro_ajustado`. (c) Segmentação contábil on-site vs off-site da Nota 24 dá visibilidade que o data_pack gerencial tinha mas agora com rastreabilidade auditada. (d) SWAP TEND3 é material para resultado financeiro 2025 — qualquer projeção forward deve isolar receita de SWAP.
2026-04-10 — ingest ITR 1T25, 2T25, 3T25 Tenda. Produced full/, structured/, digested/ for each. Manifest updated with sources, coverage (dre/bp filled), precedence (ITR > data_pack).
2026-04-10 — ingest releases 1T25, 2T25, 3T25, 4T25 Tenda. Produced full/, structured/, digested/ for each. Manifest updated with sources, financeiro_ajustado coverage, precedence (release > data_pack for operational/adjusted metrics).
2026-04-10 — wiki update — tenda.md updated with ITR+release data (1T25-4T25). Added sections: evolucao trimestral 2025 (DRE, marca Tenda, Alea), destaques operacionais trimestrais, balanco e endividamento, resultado a apropriar, guidance tracking (2025 revisado + 2026), eventos-chave (Alea Freio de Arrumacao, SWAP TRS, Pode Entrar, GKP, MCMV). Updated sources list in frontmatter, cobertura section. All claims cited to structured/ or full/.
2026-04-10 — ingest 19 fatos relevantes Tenda (2T25–2T26). Light path: full/ + digested/ only. Updated tenda.md wiki page with quarterly data from ITRs + releases.
2026-04-10 — ingest fato_relevante 1T25: sources/full/tenda/1T25/fato_relevante_859967.md, sources/digested/tenda_fatos_relevantes_batch_summary.md
2026-04-10 — wiki update — tenda.md updated with fatos relevantes data (2T25–2T26). Added: 12a debentures (R$180M), cessao pro-soluto CRI Opea (R$293M em 3 integralizacoes), cronologia de liquidacoes de derivativos SWAP TRS (jun/25–abr/26), programa de recompra (2M acoes), dividendos 2025 (R$150M), governanca (renuncia conselheiro). Updated frontmatter sources (19 fatos relevantes), removed fatos relevantes from "Limitacoes" section.
2026-04-10 — ingest itr 1T24: sources/full/direcional/1T24/itr.md, sources/structured/direcional/1T24/itr.json, sources/digested/direcional_itr_1T24_summary.md
2026-04-10 — ingest itr 1T25: sources/full/direcional/1T25/itr.md, sources/structured/direcional/1T25/itr.json, sources/digested/direcional_itr_1T25_summary.md
2026-04-10 — ingest dfp 2024: sources/full/direcional/2024/dfp.md, sources/structured/direcional/2024/dfp.json, sources/digested/direcional_dfp_2024_summary.md
2026-04-10 — ingest dfp 2025: sources/full/direcional/2025/dfp.md, sources/structured/direcional/2025/dfp.json, sources/digested/direcional_dfp_2025_summary.md
2026-04-10 — ingest itr 2T24: sources/full/direcional/2T24/itr.md, sources/structured/direcional/2T24/itr.json, sources/digested/direcional_itr_2T24_summary.md
2026-04-10 — ingest itr 2T25: sources/full/direcional/2T25/itr.md, sources/structured/direcional/2T25/itr.json, sources/digested/direcional_itr_2T25_summary.md
2026-04-10 — ingest itr 3T24: sources/full/direcional/3T24/itr.md, sources/structured/direcional/3T24/itr.json, sources/digested/direcional_itr_3T24_summary.md
2026-04-10 — ingest itr 3T25: sources/full/direcional/3T25/itr.md, sources/structured/direcional/3T25/itr.json, sources/digested/direcional_itr_3T25_summary.md
2026-04-10 — ingest itr 1T24: sources/full/direcional/1T24/itr.md, sources/structured/direcional/1T24/itr.json, sources/digested/direcional_itr_1T24_summary.md
2026-04-10 — ingest itr 1T25: sources/full/direcional/1T25/itr.md, sources/structured/direcional/1T25/itr.json, sources/digested/direcional_itr_1T25_summary.md
2026-04-10 — ingest dfp 2024: sources/full/direcional/2024/dfp.md, sources/structured/direcional/2024/dfp.json, sources/digested/direcional_dfp_2024_summary.md
2026-04-10 — ingest dfp 2025: sources/full/direcional/2025/dfp.md, sources/structured/direcional/2025/dfp.json, sources/digested/direcional_dfp_2025_summary.md
2026-04-10 — ingest itr 2T24: sources/full/direcional/2T24/itr.md, sources/structured/direcional/2T24/itr.json, sources/digested/direcional_itr_2T24_summary.md
2026-04-10 — ingest itr 2T25: sources/full/direcional/2T25/itr.md, sources/structured/direcional/2T25/itr.json, sources/digested/direcional_itr_2T25_summary.md
2026-04-10 — ingest itr 3T24: sources/full/direcional/3T24/itr.md, sources/structured/direcional/3T24/itr.json, sources/digested/direcional_itr_3T24_summary.md
2026-04-10 — ingest itr 3T25: sources/full/direcional/3T25/itr.md, sources/structured/direcional/3T25/itr.json, sources/digested/direcional_itr_3T25_summary.md
