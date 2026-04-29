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
2026-04-10 — ingest release 2T25 Direcional. Two candidate files evaluated: DIRR3_2T25_release_916773 was an S&P Global CRI rating report (not an earnings release) — discarded. DIRR3_2T25_release_936206 is the actual 2T25 earnings release (25 pages PT + EN). Produced: sources/full/direcional/2T25/release.md, sources/structured/direcional/2T25/release.json (all 4 canonical blocks filled: operacional, dre, bp, financeiro_ajustado + company_specific with segmentos Direcional/Riva, endividamento detail, contas a receber gerencial, eventos subsequentes), sources/digested/direcional_release_2T25_summary.md. Manifest updated with source entry, coverage (operacional + financeiro_ajustado filled from release), precedence rules.

2026-04-10 — ingest release 1T25 Direcional. Source: DIRR3_1T25_release_901173_extracted.md (25 pages, PT). Produced: sources/full/direcional/1T25/release.md, sources/structured/direcional/1T25/release.json (all 4 canonical blocks filled: operacional, dre, bp, financeiro_ajustado + company_specific with segmentos Direcional/Riva/Legado, endividamento detail, contas a receber gerencial, CRI emissao, carteira gerencial), sources/digested/direcional_release_1T25_summary.md. Manifest updated with source entry, coverage (operacional + financeiro_ajustado filled from release for 1T25), precedence generalized to any period with release.

2026-04-10 — ingest release 1T24 Direcional. Source: DIRR3_1T24_release_760469_extracted.md (26 pages PT + 26 pages EN). Produced: sources/full/direcional/1T24/release.md, sources/structured/direcional/1T24/release.json (all 4 canonical blocks filled: operacional with lancamentos/vendas/distratos/estoque/repasses/entregas/banco_terrenos, dre, bp, financeiro_ajustado + company_specific with segmentos Direcional/Riva/Legado, endividamento detail, DFC, LTM metrics), sources/digested/direcional_release_1T24_summary.md. Manifest updated: source entry added, coverage for 1T24 expanded with operacional + financeiro_ajustado from release.

2026-04-10 — ingest release 4T25 Direcional. Source: DIRR3_4T25_release_1012256_extracted.md (28 pages PT + 28 pages EN). Produced: sources/full/direcional/4T25/release.md, sources/structured/direcional/4T25/release.json (all 4 canonical blocks filled: operacional with lancamentos/vendas/distratos/estoque/repasses/entregas/banco_terrenos, dre quarter, bp end-of-period, financeiro_ajustado + company_specific with segmentos Direcional/Riva annual DRE/BP, endividamento detail by indexador/composicao, DFC annual, carteira gerencial, aquisicoes terrenos, dividendos, dados mercado, evento Riva 15%, evento subsequente CRI R$ 437.5 mm, impacto Lei 15.270/2025), sources/digested/direcional_release_4T25_summary.md. Manifest updated: source entry added, coverage for 4T25 with all 4 blocks (dre, bp, operacional, financeiro_ajustado) filled from release.

2026-04-10 — ingest release 3T24 Direcional. Source: DIRR3_3T24_release_824945_extracted.md (28 pages PT + EN). Produced: sources/full/direcional/3T24/release.md, sources/structured/direcional/3T24/release.json (all 4 canonical blocks filled: operacional with lancamentos/vendas/distratos/estoque/repasses/entregas/banco_terrenos, dre quarter, bp end-of-period, financeiro_ajustado + company_specific with segmentos Direcional/Riva/Legado/Pode Entrar, endividamento detail by indexador/composicao, EBITDA recomposicao, resultado financeiro detalhado, dividendos R$ 357 mm, dados mercado, liquidacao swap acoes), sources/digested/direcional_release_3T24_summary.md. Manifest updated: source entry added, coverage for 3T24 expanded with operacional + financeiro_ajustado from release.

2026-04-10 — ingest release 4T24 Direcional. Two source files evaluated: DIRR3_4T24_release_869519_extracted.md (28 pages, actual earnings release) and DIRR3_4T24_release_890480_extracted.md (6 pages, debenture 8th issuance agent report — NOT a release, discarded). Produced: sources/full/direcional/4T24/release.md, sources/structured/direcional/4T24/release.json (all 4 canonical blocks filled: operacional with lancamentos/vendas/distratos/estoque/repasses/entregas/banco_terrenos, dre quarter, bp end-of-period 31/12/2024, financeiro_ajustado + company_specific with segmentos Direcional/Riva/Pode Entrar/Legado, endividamento detail by indexador, EBITDA recomposicao, LL operacional, dividendos R$ 577 mm/ano, carteira gerencial, evento subsequente CRI R$ 370 mm brAAA), sources/digested/direcional_release_4T24_summary.md. Manifest updated: source entry added, coverage for 4T24 with all 4 blocks filled from release.

2026-04-10 — ingest release 2T24 Direcional. Source: DIRR3_2T24_release_795281_extracted.md (26 pages PT + EN). Produced: sources/full/direcional/2T24/release.md, sources/structured/direcional/2T24/release.json (all 4 canonical blocks filled: operacional with lancamentos/vendas/distratos/estoque/repasses/entregas/banco_terrenos, dre quarter, bp end-of-period 30/06/2024, financeiro_ajustado + company_specific with segmentos Direcional/Riva/Legado, endividamento detail by indexador/composicao, EBITDA recomposicao, LL operacional R$ 135 mm, cessao recebiveis R$ 224 mm, geracao caixa R$ 219 mm, dividendos R$ 277 mm evento subsequente, dados mercado), sources/digested/direcional_release_2T24_summary.md. Manifest updated: source entry added, coverage for 2T24 expanded with operacional + financeiro_ajustado from release.

2026-04-10 — ingest release 3T25 Direcional. Source: DIRR3_3T25_release_968805_extracted.md (27 pages PT + EN). Produced: sources/full/direcional/3T25/release.md, sources/structured/direcional/3T25/release.json (all 4 canonical blocks filled: operacional with lancamentos/vendas/distratos/estoque/repasses/entregas/banco_terrenos, dre quarter, bp end-of-period 30/09/2025, financeiro_ajustado + company_specific with segmentos Direcional/Riva, endividamento detail by indexador/composicao, EBITDA recomposicao, LL operacional R$ 205 mm, geracao caixa R$ 113 mm trimestre / R$ 493 mm 9M25, DL/PL 3,8%, captacao CRI R$ 600 mm, evento subsequente alienacao 15% Riva), sources/digested/direcional_release_3T25_summary.md. Manifest updated: source entry added, coverage for 3T25 expanded with operacional + financeiro_ajustado from release.
2026-04-10 — ingest release 1T24: sources/full/direcional/1T24/release.md, sources/structured/direcional/1T24/release.json, sources/digested/direcional_release_1T24_summary.md
2026-04-10 — ingest release 1T25: sources/full/direcional/1T25/release.md, sources/structured/direcional/1T25/release.json, sources/digested/direcional_release_1T25_summary.md
2026-04-10 — ingest release 2T24: sources/full/direcional/2T24/release.md, sources/structured/direcional/2T24/release.json, sources/digested/direcional_release_2T24_summary.md
2026-04-10 — ingest release 2T25: sources/full/direcional/2T25/release.md, sources/structured/direcional/2T25/release.json, sources/digested/direcional_release_2T25_summary.md
2026-04-10 — ingest release 2T25: sources/full/direcional/2T25/release.md, sources/structured/direcional/2T25/release.json, sources/digested/direcional_release_2T25_summary.md
2026-04-10 — ingest release 3T24: sources/full/direcional/3T24/release.md, sources/structured/direcional/3T24/release.json, sources/digested/direcional_release_3T24_summary.md
2026-04-10 — ingest release 3T25: sources/full/direcional/3T25/release.md, sources/structured/direcional/3T25/release.json, sources/digested/direcional_release_3T25_summary.md
2026-04-10 — ingest release 4T23: sources/full/direcional/4T23/release.md, sources/structured/direcional/4T23/release.json, sources/digested/direcional_release_4T23_summary.md
2026-04-10 — ingest release 4T23: sources/full/direcional/4T23/release.md, sources/structured/direcional/4T23/release.json, sources/digested/direcional_release_4T23_summary.md
2026-04-10 — ingest release 4T24: sources/full/direcional/4T24/release.md, sources/structured/direcional/4T24/release.json, sources/digested/direcional_release_4T24_summary.md
2026-04-10 — ingest release 4T24: sources/full/direcional/4T24/release.md, sources/structured/direcional/4T24/release.json, sources/digested/direcional_release_4T24_summary.md
2026-04-10 — ingest release 4T25: sources/full/direcional/4T25/release.md, sources/structured/direcional/4T25/release.json, sources/digested/direcional_release_4T25_summary.md
2026-04-10 — ingest fato_relevante 1T25: sources/full/direcional/1T25/fato_relevante_874223.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 2T25: sources/full/direcional/2T25/fato_relevante_901482.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 2T25: sources/full/direcional/2T25/fato_relevante_910132.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 2T25: sources/full/direcional/2T25/fato_relevante_910146.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 2T25: sources/full/direcional/2T25/fato_relevante_915858.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 3T24: sources/full/direcional/3T24/fato_relevante_780235.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 3T24: sources/full/direcional/3T24/fato_relevante_805974.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 4T24: sources/full/direcional/4T24/fato_relevante_837816.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 4T24: sources/full/direcional/4T24/fato_relevante_840875.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 4T24: sources/full/direcional/4T24/fato_relevante_842848.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — ingest fato_relevante 4T25: sources/full/direcional/4T25/fato_relevante_980371.md, sources/digested/direcional_fatos_relevantes_batch_summary.md
2026-04-10 — wiki update — created direcional.md entity page from 8 releases (1T24-4T25) + fatos relevantes. Covers DRE, operacional, balanco, REF, proventos, eventos-chave (Riva/Riza, reorganizacao societaria, MCMV Faixa 4). Cited structured/ and full/ sources throughout.
2026-04-11 — wiki update — created concept/entity/comparison pages from tenda+direcional ingests. New: riva.md (entity, Direcional subsidiary), alea.md (entity, Tenda subsidiary), resultado_a_apropriar.md (concept, REF/margem backlog), swap_trs.md (concept, Total Return Swap sobre ações próprias). Updated: incorporadoras.md (sector, added Direcional with side-by-side 2025 table), tenda_vs_direcional.md (comparison, full DRE/operacional/balanço/REF/eventos). Cited structured/ and full/ throughout.
2026-04-11 — ingest release 1T23: sources/full/cury/1T23/release.md, sources/structured/cury/1T23/release.json, sources/digested/cury_release_1T23_summary.md
2026-04-11 — ingest release 1T24: sources/full/cury/1T24/release.md, sources/structured/cury/1T24/release.json, sources/digested/cury_release_1T24_summary.md
2026-04-11 — ingest release 1T24: sources/full/cury/1T24/release.md, sources/structured/cury/1T24/release.json, sources/digested/cury_release_1T24_summary.md
2026-04-11 — ingest release 1T25: sources/full/cury/1T25/release.md, sources/structured/cury/1T25/release.json, sources/digested/cury_release_1T25_summary.md
2026-04-11 — ingest release 1T25: sources/full/cury/1T25/release.md, sources/structured/cury/1T25/release.json, sources/digested/cury_release_1T25_summary.md
2026-04-11 — ingest release 1T25: sources/full/cury/1T25/release.md, sources/structured/cury/1T25/release.json, sources/digested/cury_release_1T25_summary.md
2026-04-11 — ingest release 2T23: sources/full/cury/2T23/release.md, sources/structured/cury/2T23/release.json, sources/digested/cury_release_2T23_summary.md
2026-04-11 — ingest release 2T24: sources/full/cury/2T24/release.md, sources/structured/cury/2T24/release.json, sources/digested/cury_release_2T24_summary.md
2026-04-11 — ingest release 2T24: sources/full/cury/2T24/release.md, sources/structured/cury/2T24/release.json, sources/digested/cury_release_2T24_summary.md
2026-04-11 — ingest release 2T25: sources/full/cury/2T25/release.md, sources/structured/cury/2T25/release.json, sources/digested/cury_release_2T25_summary.md
2026-04-11 — ingest release 3T23: sources/full/cury/3T23/release.md, sources/structured/cury/3T23/release.json, sources/digested/cury_release_3T23_summary.md
2026-04-11 — ingest release 3T24: sources/full/cury/3T24/release.md, sources/structured/cury/3T24/release.json, sources/digested/cury_release_3T24_summary.md
2026-04-11 — ingest release 3T25: sources/full/cury/3T25/release.md, sources/structured/cury/3T25/release.json, sources/digested/cury_release_3T25_summary.md
2026-04-11 — ingest release 4T22: sources/full/cury/4T22/release.md, sources/structured/cury/4T22/release.json, sources/digested/cury_release_4T22_summary.md
2026-04-11 — ingest release 4T22: sources/full/cury/4T22/release.md, sources/structured/cury/4T22/release.json, sources/digested/cury_release_4T22_summary.md
2026-04-11 — ingest release 4T23: sources/full/cury/4T23/release.md, sources/structured/cury/4T23/release.json, sources/digested/cury_release_4T23_summary.md
2026-04-11 — ingest release 4T23: sources/full/cury/4T23/release.md, sources/structured/cury/4T23/release.json, sources/digested/cury_release_4T23_summary.md
2026-04-11 — ingest release 4T23: sources/full/cury/4T23/release.md, sources/structured/cury/4T23/release.json, sources/digested/cury_release_4T23_summary.md
2026-04-11 — ingest release 4T23: sources/full/cury/4T23/release.md, sources/structured/cury/4T23/release.json, sources/digested/cury_release_4T23_summary.md
2026-04-11 — ingest release 4T24: sources/full/cury/4T24/release.md, sources/structured/cury/4T24/release.json, sources/digested/cury_release_4T24_summary.md
2026-04-11 — ingest release 4T24: sources/full/cury/4T24/release.md, sources/structured/cury/4T24/release.json, sources/digested/cury_release_4T24_summary.md
2026-04-11 — ingest release 4T24: sources/full/cury/4T24/release.md, sources/structured/cury/4T24/release.json, sources/digested/cury_release_4T24_summary.md
2026-04-11 — ingest release 4T25: sources/full/cury/4T25/release.md, sources/structured/cury/4T25/release.json, sources/digested/cury_release_4T25_summary.md
2026-04-11 — ingest release 4T25: sources/full/cury/4T25/release.md, sources/structured/cury/4T25/release.json, sources/digested/cury_release_4T25_summary.md
2026-04-11 — ingest fato_relevante 1T26: sources/full/cury/1T26/fato_relevante_1015615.md, sources/digested/cury_fatos_relevantes_batch_summary.md
2026-04-11 — ingest fato_relevante 2T25: sources/full/cury/2T25/fato_relevante_889685.md, sources/digested/cury_fatos_relevantes_batch_summary.md
2026-04-11 — ingest fato_relevante 3T25: sources/full/cury/3T25/fato_relevante_932870.md, sources/digested/cury_fatos_relevantes_batch_summary.md
2026-04-11 — ingest fato_relevante 4T24: sources/full/cury/4T24/fato_relevante_841950.md, sources/digested/cury_fatos_relevantes_batch_summary.md
2026-04-11 — ingest fato_relevante 4T25: sources/full/cury/4T25/fato_relevante_977461.md, sources/digested/cury_fatos_relevantes_batch_summary.md
2026-04-11 — ingest fato_relevante 4T25: sources/full/cury/4T25/fato_relevante_981184.md, sources/digested/cury_fatos_relevantes_batch_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_1T23_itr_126022.md, sources/digested/cury_other_CURY3_1T23_itr_126022_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_1T24_itr_136591.md, sources/digested/cury_other_CURY3_1T24_itr_136591_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_1T25_itr_147489.md, sources/digested/cury_other_CURY3_1T25_itr_147489_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2022_dfp_130992.md, sources/digested/cury_other_CURY3_2022_dfp_130992_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2023_dfp_134624.md, sources/digested/cury_other_CURY3_2023_dfp_134624_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2024_dfp_145292.md, sources/digested/cury_other_CURY3_2024_dfp_145292_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2025_dfp_155237.md, sources/digested/cury_other_CURY3_2025_dfp_155237_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2T23_itr_129820.md, sources/digested/cury_other_CURY3_2T23_itr_129820_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2T24_itr_140423.md, sources/digested/cury_other_CURY3_2T24_itr_140423_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_2T25_itr_150599.md, sources/digested/cury_other_CURY3_2T25_itr_150599_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_3T23_itr_131846.md, sources/digested/cury_other_CURY3_3T23_itr_131846_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_3T24_itr_142960.md, sources/digested/cury_other_CURY3_3T24_itr_142960_summary.md
2026-04-11 — ingest release unknown: sources/full/cury/other/CURY3_3T25_itr_152937.md, sources/digested/cury_other_CURY3_3T25_itr_152937_summary.md
2026-04-11 — ingest previa_operacional 1T26: sources/full/cury/1T26/previa_operacional.md, sources/digested/cury_previa_operacional_1T26_summary.md

## 2026-04-11 — wiki update — CURY3 entity + comparison created from 27 digested sources (4 DFPs, 12 releases 1T23-4T25, fatos relevantes batch, previa 1T26). Created cury.md (entity) and cury_vs_direcional.md (comparison). Updated incorporadoras.md to include Cury in players table with ROE 78,8 percent highlighted. Frontmatter source lists, citations format full/cury/... and structured/cury/... applied throughout.
2026-04-11 — ingest previa_operacional 1T26: sources/full/tenda/1T26/previa_operacional.md, sources/digested/tenda_previa_operacional_1T26_summary.md
2026-04-11 — ingest previa_operacional 1T26: sources/full/direcional/1T26/previa_operacional.md, sources/digested/direcional_previa_operacional_1T26_summary.md
2026-04-12 — ingest itr 1T24: sources/full/tenda/1T24/itr.md, sources/structured/tenda/1T24/itr.json, sources/digested/tenda_itr_1T24_summary.md
2026-04-12 — ingest dfp 2023: sources/full/tenda/2023/dfp.md, sources/structured/tenda/2023/dfp.json, sources/digested/tenda_dfp_2023_summary.md
2026-04-12 — ingest itr 2T24: sources/full/tenda/2T24/itr.md, sources/structured/tenda/2T24/itr.json, sources/digested/tenda_itr_2T24_summary.md
2026-04-12 — ingest itr 3T24: sources/full/tenda/3T24/itr.md, sources/structured/tenda/3T24/itr.json, sources/digested/tenda_itr_3T24_summary.md
2026-04-12 — ingest release 1T24: sources/full/tenda/1T24/release.md, sources/structured/tenda/1T24/release.json, sources/digested/tenda_release_1T24_summary.md
2026-04-12 — ingest release 2T24: sources/full/tenda/2T24/release.md, sources/structured/tenda/2T24/release.json, sources/digested/tenda_release_2T24_summary.md
2026-04-12 — ingest release 3T24: sources/full/tenda/3T24/release.md, sources/structured/tenda/3T24/release.json, sources/digested/tenda_release_3T24_summary.md
2026-04-12 — ingest release 4T23: sources/full/tenda/4T23/release.md, sources/structured/tenda/4T23/release.json, sources/digested/tenda_release_4T23_summary.md
2026-04-12 — ingest release 4T24: sources/full/tenda/4T24/release.md, sources/structured/tenda/4T24/release.json, sources/digested/tenda_release_4T24_summary.md
2026-04-12 — wiki update (tenda 2023-2024 batch): updated tenda.md with Evolucao trimestral 2024 section (4T23-4T24 DRE, Alea, operacional, balanco, REF, guidance tracking, eventos-chave 2023-2024), added 2023-2024 sources to frontmatter, updated limitations. Created pode_entrar.md (concept) and debentures.md (concept). Updated alea.md with 2024 ramp-up trajectory. Updated incorporadoras.md and tenda_vs_direcional.md with 2024 context. Sources: tenda_dfp_2023_summary.md, tenda_itr_{1T24,2T24,3T24}_summary.md, tenda_release_{4T23,1T24,2T24,3T24,4T24}_summary.md.
2026-04-13 — wiki update (incorporadoras sector page): updated incorporadoras.md with Cyrela as fourth covered player (CYRE3: receita R$ 9,4 bi, lucro R$ 2,0 bi, ROE 22,3%). Added backlog/REF comparison table. Updated landbank data to 1T26 prévias (Direcional R$ 60 bi, Tenda R$ 29,7 bi, Cury R$ 24,9 bi). Added Tenda distrato data (9,9% 1T26). New trends: Cyrela MCMV expansion, Alea reestruturação, 1T26 prévia momentum. Expanded debêntures/CRI trend with per-company detail. Sources: all 12 digesteds (cyrela/cury/direcional/tenda × dfp_2025/release_4T25/previa_1T26).
[wiki-queue] 2026-04-13 | generic | other | HB_historical series_4Q25 | sources/digested/HB_historical series_4Q25_summary.md
[wiki-done] 2026-04-13 | batch_20260413_112019
[wiki-queue] 2026-04-13 | generic | other | Texto Reforma tributaria jan-2025 | sources/digested/Texto Reforma tributaria jan-2025_summary.md
[wiki-done] 2026-04-13 | batch_20260413_150326
[wiki-queue] 2026-04-13 | generic | other | notas_mattos_filho_reforma_incorporadoras | sources/digested/notas_mattos_filho_reforma_incorporadoras_summary.md
[wiki-done] 2026-04-13 | batch_20260413_183354
2026-04-13 — ingest previa_operacional 1T26: sources/full/cyrela/1T26/previa_operacional.md, sources/digested/cyrela_fatos_relevantes_batch_summary.md
[wiki-queue] 2026-04-13 | cyrela | previa_operacional | 1T26 | sources/digested/cyrela_fatos_relevantes_batch_summary.md
[wiki-done] 2026-04-13 | batch_20260413_185207
[wiki-queue] 2026-04-13 | generic | other | cyrela_dados_operacionais | sources/digested/cyrela_dados_operacionais_summary.md
[wiki-queue] 2026-04-13 | generic | other | cyrela_lancamentos | sources/digested/cyrela_lancamentos_summary.md
[wiki-done] 2026-04-13 | batch_20260413_195300
[fetch-calls] 2026-04-14 | direcional | 4T24 | https://www.youtube.com/watch?v=Vl_XJnZBFfE | auto_forced
[fetch-calls] 2026-04-14 | direcional | 4T23
 | https://www.youtube.com/watch?v=sZUQrK7v6d8 | auto
[fetch-calls] 2026-04-14 | direcional | 2T23
 | https://www.youtube.com/watch?v=ra6poXDh0sQ | auto
[fetch-calls] 2026-04-14 | direcional | 1T23
 | https://www.youtube.com/watch?v=LuWonb9WPsI | auto
[fetch-calls] 2026-04-14 | direcional | 4T20
 | https://www.youtube.com/watch?v=wL04P85RrnY | auto
[fetch-calls] 2026-04-14 | direcional | 1T22
 | https://www.youtube.com/watch?v=BPAIwspEgkc | auto
[fetch-calls] 2026-04-14 | direcional | 4T21
 | https://www.youtube.com/watch?v=TI0NLQ11Gos | auto
[fetch-calls] 2026-04-14 | direcional | 3T21
 | https://www.youtube.com/watch?v=t5mnc-6mAK4 | auto
[fetch-calls] 2026-04-14 | direcional | 2T21
 | https://www.youtube.com/watch?v=Um8KttUvdeA | auto
[fetch-calls] 2026-04-14 | direcional | 4T25
 | https://www.youtube.com/watch?v=4G24GLp2Z7g | auto
[fetch-calls] 2026-04-14 | direcional | 3T25
 | https://www.youtube.com/watch?v=gpJAQUS0VqA | auto
[fetch-calls] 2026-04-14 | direcional | 2T25
 | https://www.youtube.com/watch?v=dN2kmm3ZMcE | auto
[fetch-calls] 2026-04-14 | direcional | 1T25
 | https://www.youtube.com/watch?v=PGKvfFD5P2s | auto
[fetch-calls] 2026-04-14 | direcional | 3T24
 | https://www.youtube.com/watch?v=2uPIku8YKgM | auto
[fetch-calls] 2026-04-14 | direcional | 2T24
 | https://www.youtube.com/watch?v=uIvWNRQLV14 | auto
[fetch-calls] 2026-04-14 | direcional | 1T24
 | https://www.youtube.com/watch?v=z9B-mRlEL-0 | auto
[fetch-calls] 2026-04-14 | direcional | 3T23
 | https://www.youtube.com/watch?v=ZF_t69gZmFA | auto
[fetch-calls] 2026-04-14 | direcional | 4T22
 | https://www.youtube.com/watch?v=myCwdkvy93Y | auto
[fetch-calls] 2026-04-14 | direcional | 3T22
 | https://www.youtube.com/watch?v=i_xnGGK2lfg | auto
[fetch-calls] 2026-04-14 | direcional | 2T22
 | https://www.youtube.com/watch?v=LdgjowQlvqM | auto
[fetch-calls] 2026-04-14 | direcional | 1T21
 | https://www.youtube.com/watch?v=NmyEfQa-GRg | auto
[fetch-calls] 2026-04-14 | direcional | 3T20
 | https://www.youtube.com/watch?v=clqtXvDvam4 | auto
2026-04-14 — ingest call_transcript 4T24: sources/full/direcional/4T24/call_transcript.md, sources/digested/direcional_call_transcript_4T24_summary.md
[wiki-done] 2026-04-15 | cury.md atualizado: tabela "Proventos e retorno ao acionista" expandida com linha 2026 (parcial); tabela de evolução histórica adicionou coluna 2026; observações adicionadas sobre a antecipação fiscal motivada pelo STF/Lei 15.270/2025. Digest batch de fatos relevantes atualizado com seção 1T26 completa.
[wiki-queue] 2026-04-14 | direcional | call_transcript | 4T24 | sources/digested/direcional_call_transcript_4T24_summary.md
2026-04-14 — ingest call_transcript 1T21: sources/full/direcional/1T21/call_transcript.md, sources/digested/direcional_call_transcript_1T21_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 1T21 | sources/digested/direcional_call_transcript_1T21_summary.md
2026-04-14 — ingest call_transcript 1T22: sources/full/direcional/1T22/call_transcript.md, sources/digested/direcional_call_transcript_1T22_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 1T22 | sources/digested/direcional_call_transcript_1T22_summary.md
2026-04-14 — ingest call_transcript 1T23: sources/full/direcional/1T23/call_transcript.md, sources/digested/direcional_call_transcript_1T23_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 1T23 | sources/digested/direcional_call_transcript_1T23_summary.md
2026-04-14 — ingest call_transcript 1T24: sources/full/direcional/1T24/call_transcript.md, sources/digested/direcional_call_transcript_1T24_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 1T24 | sources/digested/direcional_call_transcript_1T24_summary.md
2026-04-14 — ingest call_transcript 1T25: sources/full/direcional/1T25/call_transcript.md, sources/digested/direcional_call_transcript_1T25_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 1T25 | sources/digested/direcional_call_transcript_1T25_summary.md
2026-04-14 — ingest call_transcript 2T21: sources/full/direcional/2T21/call_transcript.md, sources/digested/direcional_call_transcript_2T21_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 2T21 | sources/digested/direcional_call_transcript_2T21_summary.md
2026-04-14 — ingest call_transcript 2T22: sources/full/direcional/2T22/call_transcript.md, sources/digested/direcional_call_transcript_2T22_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 2T22 | sources/digested/direcional_call_transcript_2T22_summary.md
2026-04-14 — ingest call_transcript 2T23: sources/full/direcional/2T23/call_transcript.md, sources/digested/direcional_call_transcript_2T23_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 2T23 | sources/digested/direcional_call_transcript_2T23_summary.md
2026-04-14 — ingest call_transcript 2T24: sources/full/direcional/2T24/call_transcript.md, sources/digested/direcional_call_transcript_2T24_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 2T24 | sources/digested/direcional_call_transcript_2T24_summary.md
2026-04-14 — ingest call_transcript 2T25: sources/full/direcional/2T25/call_transcript.md, sources/digested/direcional_call_transcript_2T25_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 2T25 | sources/digested/direcional_call_transcript_2T25_summary.md
2026-04-14 — ingest call_transcript 3T20: sources/full/direcional/3T20/call_transcript.md, sources/digested/direcional_call_transcript_3T20_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 3T20 | sources/digested/direcional_call_transcript_3T20_summary.md
2026-04-14 — ingest call_transcript 3T21: sources/full/direcional/3T21/call_transcript.md, sources/digested/direcional_call_transcript_3T21_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 3T21 | sources/digested/direcional_call_transcript_3T21_summary.md
2026-04-14 — ingest call_transcript 3T22: sources/full/direcional/3T22/call_transcript.md, sources/digested/direcional_call_transcript_3T22_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 3T22 | sources/digested/direcional_call_transcript_3T22_summary.md
2026-04-14 — ingest call_transcript 3T23: sources/full/direcional/3T23/call_transcript.md, sources/digested/direcional_call_transcript_3T23_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 3T23 | sources/digested/direcional_call_transcript_3T23_summary.md
2026-04-14 — ingest call_transcript 3T24: sources/full/direcional/3T24/call_transcript.md, sources/digested/direcional_call_transcript_3T24_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 3T24 | sources/digested/direcional_call_transcript_3T24_summary.md
2026-04-14 — ingest call_transcript 3T25: sources/full/direcional/3T25/call_transcript.md, sources/digested/direcional_call_transcript_3T25_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 3T25 | sources/digested/direcional_call_transcript_3T25_summary.md
2026-04-14 — ingest call_transcript 4T20: sources/full/direcional/4T20/call_transcript.md, sources/digested/direcional_call_transcript_4T20_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 4T20 | sources/digested/direcional_call_transcript_4T20_summary.md
2026-04-14 — ingest call_transcript 4T21: sources/full/direcional/4T21/call_transcript.md, sources/digested/direcional_call_transcript_4T21_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 4T21 | sources/digested/direcional_call_transcript_4T21_summary.md
2026-04-14 — ingest call_transcript 4T22: sources/full/direcional/4T22/call_transcript.md, sources/digested/direcional_call_transcript_4T22_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 4T22 | sources/digested/direcional_call_transcript_4T22_summary.md
2026-04-14 — ingest call_transcript 4T23: sources/full/direcional/4T23/call_transcript.md, sources/digested/direcional_call_transcript_4T23_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 4T23 | sources/digested/direcional_call_transcript_4T23_summary.md
2026-04-14 — ingest call_transcript 4T25: sources/full/direcional/4T25/call_transcript.md, sources/digested/direcional_call_transcript_4T25_summary.md
[wiki-queue] 2026-04-14 | direcional | call_transcript | 4T25 | sources/digested/direcional_call_transcript_4T25_summary.md
2026-04-14 — ingest call_transcript 1T24: sources/full/direcional/1T24/call_transcript.md, sources/structured/direcional/1T24/call_transcript.json, sources/digested/direcional_call_transcript_1T24_summary.md

[ingest] 2026-04-15 | cury | ata_cad | 1T26 | sources/full/cury/1T26/rca_dividendos_20260130.md — RCA 30/jan/2026 declarando R$ 140 mm em dividendos (lastro jan–nov/2025, imputados ao mínimo obrigatório do exercício de 2025). Fonte CVM prot 1471377.
[ingest] 2026-04-15 | cury | ata_cad | 1T26 | sources/full/cury/1T26/rca_dividendos_atualizacao_20260330.md — RCA 30/mar/2026 atualiza pagamento: R$ 110 mm em 07/abr/2026 + R$ 30 mm até 31/dez/2026. Fonte CVM prot 1498112.
[wiki-done] 2026-04-16 | batch_20260416_095311
[wiki-queue] 2026-04-16 | smartfit | notion | smartfit_perguntas_diogo_corona_smart_00400ca3 | sources/digested/notion_smartfit_perguntas_diogo_corona_smart_00400ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | x86_vs_arm_02d00ca3 | sources/digested/notion_x86_vs_arm_02d00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_pan_inacio_07400ca3 | sources/digested/notion_banco_pan_inacio_07400ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | conversa_com_unidas_08d00ca3 | sources/digested/notion_conversa_com_unidas_08d00ca3_summary.md
[wiki-queue] 2026-04-16 | nubank | notion | nubank_d_vidas_nubank_souto_28_08_08800ca3 | sources/digested/notion_nubank_d_vidas_nubank_souto_28_08_08800ca3_summary.md
[wiki-queue] 2026-04-16 | nubank | notion | nubank_nubank_feedback_2t25_09d00ca3 | sources/digested/notion_nubank_nubank_feedback_2t25_09d00ca3_summary.md
[wiki-queue] 2026-04-16 | nubank | notion | nubank_pagseguro_call_pos_2t24_22_08_2024_04c00ca3 | sources/digested/notion_nubank_pagseguro_call_pos_2t24_22_08_2024_04c00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | raphael_gouveia_wellhub_04800ca3 | sources/digested/notion_raphael_gouveia_wellhub_04800ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | semianalysis_100k_08a00ca3 | sources/digested/notion_semianalysis_100k_08a00ca3_summary.md
[wiki-queue] 2026-04-16 | smartfit | notion | smartfit_smartfit_03600ca3 | sources/digested/notion_smartfit_smartfit_03600ca3_summary.md
[wiki-queue] 2026-04-16 | totalpass | notion | totalpass_totalpass_country_manager_m_xico_luis_carlos_chapa_04e00ca3 | sources/digested/notion_totalpass_totalpass_country_manager_m_xico_luis_carlos_chapa_04e00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | michelle_nosralla_smartfit_07f00ca3 | sources/digested/notion_michelle_nosralla_smartfit_07f00ca3_summary.md
[wiki-done] 2026-04-16 | batch_20260416_191714
[wiki-queue] 2026-04-16 | armac | notion | armac_armac_1f200ca3 | sources/digested/notion_armac_armac_1f200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_do_brasil_22a00ca3 | sources/digested/notion_banco_do_brasil_22a00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_do_brasil_2t25_29_08_18200ca3 | sources/digested/notion_banco_do_brasil_2t25_29_08_18200ca3_summary.md
[wiki-queue] 2026-04-16 | banco_pan | notion | banco_pan_consignado_privado_banco_pan_27a00ca3 | sources/digested/notion_banco_pan_consignado_privado_banco_pan_27a00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bb_seguridades_07_11_2025_17b00ca3 | sources/digested/notion_bb_seguridades_07_11_2025_17b00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bluefit_respons_vel_por_opera_o_de_lojas_proprias_0b000ca3 | sources/digested/notion_bluefit_respons_vel_por_opera_o_de_lojas_proprias_0b000ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | br_partners_27f00ca3 | sources/digested/notion_br_partners_27f00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_3t24_0de00ca3 | sources/digested/notion_bradesco_bradesco_3t24_0de00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_call_2t24_16a00ca3 | sources/digested/notion_bradesco_bradesco_call_2t24_16a00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_cassiano_2t25_23600ca3 | sources/digested/notion_bradesco_bradesco_cassiano_2t25_23600ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_citi_26200ca3 | sources/digested/notion_bradesco_bradesco_citi_26200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | byd_venda_direta_locadoras_0f600ca3 | sources/digested/notion_byd_venda_direta_locadoras_0f600ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | ceo_talks_osmo_tenda_27e00ca3 | sources/digested/notion_ceo_talks_osmo_tenda_27e00ca3_summary.md
[wiki-queue] 2026-04-16 | cyrela | notion | cyrela_direcional_citi_10800ca3 | sources/digested/notion_cyrela_direcional_citi_10800ca3_summary.md
[wiki-queue] 2026-04-16 | inter | notion | inter_inter_bull_and_bear_26900ca3 | sources/digested/notion_inter_inter_bull_and_bear_26900ca3_summary.md
[wiki-queue] 2026-04-16 | inter | notion | inter_inter_santiago_citi_27a00ca3 | sources/digested/notion_inter_inter_santiago_citi_27a00ca3_summary.md
[wiki-queue] 2026-04-16 | itau | notion | itau_btg_jpm_10f00ca3 | sources/digested/notion_itau_btg_jpm_10f00ca3_summary.md
[wiki-queue] 2026-04-16 | itau | notion | itau_itau_pos_2t25_1a600ca3 | sources/digested/notion_itau_itau_pos_2t25_1a600ca3_summary.md
[wiki-queue] 2026-04-16 | itau | notion | itau_itau_xp_conference_1ef00ca3 | sources/digested/notion_itau_itau_xp_conference_1ef00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | jpm_agri_rj_machado_meyer_27e00ca3 | sources/digested/notion_jpm_agri_rj_machado_meyer_27e00ca3_summary.md
[wiki-queue] 2026-04-16 | localiza | notion | localiza_localiza_citi_23200ca3 | sources/digested/notion_localiza_localiza_citi_23200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | loma_negra_sasson_1d700ca3 | sources/digested/notion_loma_negra_sasson_1d700ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | moura_e_direcional_27f00ca3 | sources/digested/notion_moura_e_direcional_27f00ca3_summary.md
[wiki-queue] 2026-04-16 | movida | notion | movida_camila_movida_27_05_2024_0a600ca3 | sources/digested/notion_movida_camila_movida_27_05_2024_0a600ca3_summary.md
[wiki-queue] 2026-04-16 | movida | notion | movida_igor_movida_venda_de_seminovos_0ca00ca3 | sources/digested/notion_movida_igor_movida_venda_de_seminovos_0ca00ca3_summary.md
[wiki-queue] 2026-04-16 | movida | notion | movida_movida_jpm_23400ca3 | sources/digested/notion_movida_movida_jpm_23400ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | nota_4_de_ago_6_55_pm_18e00ca3 | sources/digested/notion_nota_4_de_ago_6_55_pm_18e00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | nu_mexico_brian_flores_citi_0bb00ca3 | sources/digested/notion_nu_mexico_brian_flores_citi_0bb00ca3_summary.md
[wiki-queue] 2026-04-16 | nubank | notion | nubank_cris_ferraz_nubank_atacado_27900ca3 | sources/digested/notion_nubank_cris_ferraz_nubank_atacado_27900ca3_summary.md
[wiki-queue] 2026-04-16 | nubank | notion | nubank_perguntas_porto_seguro_porto_bank_26100ca3 | sources/digested/notion_nubank_perguntas_porto_seguro_porto_bank_26100ca3_summary.md
[wiki-queue] 2026-04-16 | nvidia | notion | nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3 | sources/digested/notion_nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3_summary.md
[wiki-queue] 2026-04-16 | nvidia | notion | nvidia_nota_3_de_jun_3_51_pm_nome_supercomputer_pais_prop_sito_data_cpu_cores_k_fabricante_gpu_gpus_a_gpu_asp_k_usd_b_g_18b00ca3 | sources/digested/notion_nvidia_nota_3_de_jun_3_51_pm_nome_supercomputer_pais_prop_sito_data_cpu_cores_k_fabricante_gpu_gpus_a_gpu_asp_k_usd_b_g_18b00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | perguntas_smart_rizzardo_pos_3t24_0b500ca3 | sources/digested/notion_perguntas_smart_rizzardo_pos_3t24_0b500ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | reuni_o_milad_consultoria_autu_27d00ca3 | sources/digested/notion_reuni_o_milad_consultoria_autu_27d00ca3_summary.md
[wiki-queue] 2026-04-16 | santander | notion | santander_santander_jpm_20000ca3 | sources/digested/notion_santander_santander_jpm_20000ca3_summary.md
[wiki-queue] 2026-04-16 | santander | notion | santander_santander_mario_le_o_3t24_22b00ca3 | sources/digested/notion_santander_santander_mario_le_o_3t24_22b00ca3_summary.md
[wiki-queue] 2026-04-16 | santander | notion | santander_santander_safra_2025_13a00ca3 | sources/digested/notion_santander_santander_safra_2025_13a00ca3_summary.md
[wiki-queue] 2026-04-16 | smartfit | notion | smartfit_aguilar_bourguignon_franqueado_smartfit_20600ca3 | sources/digested/notion_smartfit_aguilar_bourguignon_franqueado_smartfit_20600ca3_summary.md
[wiki-queue] 2026-04-16 | smartfit | notion | smartfit_priscilla_gavi_es_11a00ca3 | sources/digested/notion_smartfit_priscilla_gavi_es_11a00ca3_summary.md
[wiki-queue] 2026-04-16 | smartfit | notion | smartfit_rodolfo_mexico_0a900ca3 | sources/digested/notion_smartfit_rodolfo_mexico_0a900ca3_summary.md
[wiki-queue] 2026-04-16 | smartfit | notion | smartfit_smartfit_btg_23_01_2025_13100ca3 | sources/digested/notion_smartfit_smartfit_btg_23_01_2025_13100ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | stellantis_descarbonizacao_16200ca3 | sources/digested/notion_stellantis_descarbonizacao_16200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | untitled_12000ca3 | sources/digested/notion_untitled_12000ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | vamos_btg_18900ca3 | sources/digested/notion_vamos_btg_18900ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | vamos_jpm_24a00ca3 | sources/digested/notion_vamos_jpm_24a00ca3_summary.md
[wiki-queue] 2026-04-16 | vamos | notion | vamos_vamos_rodrigo_27e00ca3 | sources/digested/notion_vamos_vamos_rodrigo_27e00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | vibra_jpm_20a00ca3 | sources/digested/notion_vibra_jpm_20a00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | weg_citi_23000ca3 | sources/digested/notion_weg_citi_23000ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | weg_day_2025_28100ca3 | sources/digested/notion_weg_day_2025_28100ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | 2026_01_14t10_50_00_000_03_00_2e800ca3 | sources/digested/notion_2026_01_14t10_50_00_000_03_00_2e800ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | 2026_04_07t17_33_00_000_03_00_33b00ca3 | sources/digested/notion_2026_04_07t17_33_00_000_03_00_33b00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | abecip_bbi_4fc00ca3 | sources/digested/notion_abecip_bbi_4fc00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | abla_reforma_tribut_ria_7e800ca3 | sources/digested/notion_abla_reforma_tribut_ria_7e800ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | agibank_4t25_call_32c00ca3 | sources/digested/notion_agibank_4t25_call_32c00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | agibank_btg_34300ca3 | sources/digested/notion_agibank_btg_34300ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | agibank_ipo_2fa00ca3 | sources/digested/notion_agibank_ipo_2fa00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | atg_claudio_bda00ca3 | sources/digested/notion_atg_claudio_bda00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | automob_c1e00ca3 | sources/digested/notion_automob_c1e00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | b3_68300ca3 | sources/digested/notion_b3_68300ca3_summary.md
[wiki-queue] 2026-04-16 | b3 | notion | b3_b3_call_fernando_pos_4t25_32000ca3 | sources/digested/notion_b3_b3_call_fernando_pos_4t25_32000ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | b3_call_3t25_2a900ca3 | sources/digested/notion_b3_call_3t25_2a900ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | b3_call_4t25_31400ca3 | sources/digested/notion_b3_call_4t25_31400ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | b3_day_2cb00ca3 | sources/digested/notion_b3_day_2cb00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | b3_day_44200ca3 | sources/digested/notion_b3_day_44200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | b3_jpm_8da00ca3 | sources/digested/notion_b3_jpm_8da00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_do_brasil_15_08_2024_bcc00ca3 | sources/digested/notion_banco_do_brasil_15_08_2024_bcc00ca3_summary.md
[wiki-queue] 2026-04-16 | banco_do_brasil | notion | banco_do_brasil_banco_do_brasil_call_4t25_30500ca3 | sources/digested/notion_banco_do_brasil_banco_do_brasil_call_4t25_30500ca3_summary.md
[wiki-queue] 2026-04-16 | banco_do_brasil | notion | banco_do_brasil_banco_do_brasil_laic_2f500ca3 | sources/digested/notion_banco_do_brasil_banco_do_brasil_laic_2f500ca3_summary.md
[wiki-queue] 2026-04-16 | banco_do_brasil | notion | banco_do_brasil_bb_pos_3t25_safra_2c300ca3 | sources/digested/notion_banco_do_brasil_bb_pos_3t25_safra_2c300ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_do_brasil_call_pos_resultado_2t24_6f000ca3 | sources/digested/notion_banco_do_brasil_call_pos_resultado_2t24_6f000ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_do_brasil_citi_7e600ca3 | sources/digested/notion_banco_do_brasil_citi_7e600ca3_summary.md
[wiki-queue] 2026-04-16 | banco_do_brasil | notion | banco_do_brasil_filipe_coelho_research_agro_tesouraria_sicredi_c0700ca3 | sources/digested/notion_banco_do_brasil_filipe_coelho_research_agro_tesouraria_sicredi_c0700ca3_summary.md
[wiki-queue] 2026-04-16 | banco_do_brasil | notion | banco_do_brasil_jpm_bb_4t25_pos_resultado_30500ca3 | sources/digested/notion_banco_do_brasil_jpm_bb_4t25_pos_resultado_30500ca3_summary.md
[wiki-queue] 2026-04-16 | banco_pan | notion | banco_pan_andre_panobianco_30_08_2025_e3000ca3 | sources/digested/notion_banco_pan_andre_panobianco_30_08_2025_e3000ca3_summary.md
[wiki-queue] 2026-04-16 | banco_pan | notion | banco_pan_banco_pan_cadu_15_01_c1400ca3 | sources/digested/notion_banco_pan_banco_pan_cadu_15_01_c1400ca3_summary.md
[wiki-queue] 2026-04-16 | banco_pan | notion | banco_pan_banco_pine_call_4t25_30200ca3 | sources/digested/notion_banco_pan_banco_pine_call_4t25_30200ca3_summary.md
[wiki-queue] 2026-04-16 | banco_pan | notion | banco_pan_picpay_continua_o_2e800ca3 | sources/digested/notion_banco_pan_picpay_continua_o_2e800ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_pine_2e000ca3 | sources/digested/notion_banco_pine_2e000ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | banco_votorantim_24_06_2025_f7e00ca3 | sources/digested/notion_banco_votorantim_24_06_2025_f7e00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3 | sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md
[wiki-queue] 2026-04-16 | bb_seguridade | notion | bb_seguridade_bb_seguridade_xp_conference_2025_30900ca3 | sources/digested/notion_bb_seguridade_bb_seguridade_xp_conference_2025_30900ca3_summary.md
[wiki-queue] 2026-04-16 | bb_seguridade | notion | bb_seguridade_bb_seguridades_call_4t25_30300ca3 | sources/digested/notion_bb_seguridade_bb_seguridades_call_4t25_30300ca3_summary.md
[wiki-queue] 2026-04-16 | bb_seguridade | notion | bb_seguridade_call_ceo_bbse_jpmorgan_2a200ca3 | sources/digested/notion_bb_seguridade_call_ceo_bbse_jpmorgan_2a200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bess_absae_2a700ca3 | sources/digested/notion_bess_absae_2a700ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bess_jesse_catl_54500ca3 | sources/digested/notion_bess_jesse_catl_54500ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bess_weg_citi_3t25_cbre_2ae00ca3 | sources/digested/notion_bess_weg_citi_3t25_cbre_2ae00ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bluefit_diretora_de_expansao_sem_ramis_2e200ca3 | sources/digested/notion_bluefit_diretora_de_expansao_sem_ramis_2e200ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bluefit_renato_bair_o_a8100ca3 | sources/digested/notion_bluefit_renato_bair_o_a8100ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bodytech_e3900ca3 | sources/digested/notion_bodytech_e3900ca3_summary.md
[wiki-queue] 2026-04-16 | generic | notion | bodytech_fev_2026_30200ca3 | sources/digested/notion_bodytech_fev_2026_30200ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_a_fazer_3ae00ca3 | sources/digested/notion_bradesco_a_fazer_3ae00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_19_01_2ed00ca3 | sources/digested/notion_bradesco_bradesco_19_01_2ed00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_2t25_bbf00ca3 | sources/digested/notion_bradesco_bradesco_2t25_bbf00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_3t25_call_pos_resultado_29c00ca3 | sources/digested/notion_bradesco_bradesco_3t25_call_pos_resultado_29c00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_98300ca3 | sources/digested/notion_bradesco_bradesco_98300ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_ab600ca3 | sources/digested/notion_bradesco_bradesco_ab600ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_adb00ca3 | sources/digested/notion_bradesco_bradesco_adb00ca3_summary.md
[wiki-queue] 2026-04-16 | bradesco | notion | bradesco_bradesco_call_3t25_29c00ca3 | sources/digested/notion_bradesco_bradesco_call_3t25_29c00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_call_4t25_2ff00ca3 | sources/digested/notion_bradesco_bradesco_call_4t25_2ff00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_joice_3t25_2cb00ca3 | sources/digested/notion_bradesco_bradesco_joice_3t25_2cb00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_pos_1t25_6f200ca3 | sources/digested/notion_bradesco_bradesco_pos_1t25_6f200ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_reuniao_3t24_73600ca3 | sources/digested/notion_bradesco_bradesco_reuniao_3t24_73600ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_safra_89e00ca3 | sources/digested/notion_bradesco_bradesco_safra_89e00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_vinicius_panaro_diretor_de_contabilidade_ef400ca3 | sources/digested/notion_bradesco_bradesco_vinicius_panaro_diretor_de_contabilidade_ef400ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_bradesco_xp_conference_ec500ca3 | sources/digested/notion_bradesco_bradesco_xp_conference_ec500ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_call_bradesco_financiamento_de_ve_culos_a3600ca3 | sources/digested/notion_bradesco_call_bradesco_financiamento_de_ve_culos_a3600ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_callback_bradesco_2ff00ca3 | sources/digested/notion_bradesco_callback_bradesco_2ff00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_marcelo_noronha_bradesco_a3b00ca3 | sources/digested/notion_bradesco_marcelo_noronha_bradesco_a3b00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_reuniao_bradesco_32e00ca3 | sources/digested/notion_bradesco_reuniao_bradesco_32e00ca3_summary.md
[wiki-queue] 2026-04-17 | bradesco | notion | bradesco_santander_pos_3t25_cfo_gustavo_alejo_29c00ca3 | sources/digested/notion_bradesco_santander_pos_3t25_cfo_gustavo_alejo_29c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | btg_btg_conference_cbc00ca3 | sources/digested/notion_btg_btg_conference_cbc00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | byd_24_05_2024_fad00ca3 | sources/digested/notion_byd_24_05_2024_fad00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | byd_aidilson_05_06_2025_a7b00ca3 | sources/digested/notion_byd_aidilson_05_06_2025_a7b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | byd_aidilson_6c100ca3 | sources/digested/notion_byd_aidilson_6c100ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | byd_aidilson_dumele_bc900ca3 | sources/digested/notion_byd_aidilson_dumele_bc900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | byma_ceo_caja_de_valores_ccd00ca3 | sources/digested/notion_byma_ceo_caja_de_valores_ccd00ca3_summary.md
[wiki-queue] 2026-04-17 | caixa | notion | caixa_caixa_economica_4t25_31a00ca3 | sources/digested/notion_caixa_caixa_economica_4t25_31a00ca3_summary.md
[wiki-queue] 2026-04-17 | caixa | notion | caixa_caixa_seguridades_3t25_2b800ca3 | sources/digested/notion_caixa_caixa_seguridades_3t25_2b800ca3_summary.md
[wiki-queue] 2026-04-17 | caixa | notion | caixa_call_caixa_seguridade_4t25_32000ca3 | sources/digested/notion_caixa_call_caixa_seguridade_4t25_32000ca3_summary.md
[wiki-queue] 2026-04-17 | caixa | notion | caixa_diretor_de_produtos_varejo_caixa_a9a00ca3 | sources/digested/notion_caixa_diretor_de_produtos_varejo_caixa_a9a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_e_mercantil_consignado_diretor_cef_ceo_mercantil_dd100ca3 | sources/digested/notion_caixa_e_mercantil_consignado_diretor_cef_ceo_mercantil_dd100ca3_summary.md
[wiki-queue] 2026-04-17 | caixa | notion | caixa_hailton_bbi_2a700ca3 | sources/digested/notion_caixa_hailton_bbi_2a700ca3_summary.md
[wiki-queue] 2026-04-17 | caixa | notion | caixa_painel_minha_casa_minha_vida_2026_31900ca3 | sources/digested/notion_caixa_painel_minha_casa_minha_vida_2026_31900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_seg_9ea00ca3 | sources/digested/notion_caixa_seg_9ea00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_seguridade_4t24_b4b00ca3 | sources/digested/notion_caixa_seguridade_4t24_b4b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_seguridade_7ba00ca3 | sources/digested/notion_caixa_seguridade_7ba00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_seguridade_9cc00ca3 | sources/digested/notion_caixa_seguridade_9cc00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_seguridades_btg_5fb00ca3 | sources/digested/notion_caixa_seguridades_btg_5fb00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_seguridades_caf_da_manha_17_10_btg_c1d00ca3 | sources/digested/notion_caixa_seguridades_caf_da_manha_17_10_btg_c1d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | caixa_vice_presidente_de_habitacao_67b00ca3 | sources/digested/notion_caixa_vice_presidente_de_habitacao_67b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_b3_pos_4t25_32000ca3 | sources/digested/notion_call_b3_pos_4t25_32000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_cfo_mrv_ricardo_paixao_32200ca3 | sources/digested/notion_call_cfo_mrv_ricardo_paixao_32200ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_com_dylan_patel_semianalysis_66100ca3 | sources/digested/notion_call_com_dylan_patel_semianalysis_66100ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_csd_27_10_2025_29900ca3 | sources/digested/notion_call_csd_27_10_2025_29900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_felipe_32000ca3 | sources/digested/notion_call_felipe_32000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_luis_29_01_2026_2f700ca3 | sources/digested/notion_call_luis_29_01_2026_2f700ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_simpar_b2e00ca3 | sources/digested/notion_call_simpar_b2e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_stone_4t25_31700ca3 | sources/digested/notion_call_stone_4t25_31700ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | call_weg_friday_may_3_2024_def00ca3 | sources/digested/notion_call_weg_friday_may_3_2024_def00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | cambauva_btg_10_12_2025_2c500ca3 | sources/digested/notion_cambauva_btg_10_12_2025_2c500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | capstone_pine_2ea00ca3 | sources/digested/notion_capstone_pine_2ea00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | coisas_a_se_fazer_97f00ca3 | sources/digested/notion_coisas_a_se_fazer_97f00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | conselho_curador_fgts_07_10_28500ca3 | sources/digested/notion_conselho_curador_fgts_07_10_28500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | consignado_privado_bmp_maria_do_socorro_2fd00ca3 | sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | conversa_abinee_leil_o_de_baterias_31000ca3 | sources/digested/notion_conversa_abinee_leil_o_de_baterias_31000ca3_summary.md
[wiki-queue] 2026-04-17 | cury | notion | cury_cfo_tenda_28d00ca3 | sources/digested/notion_cury_cfo_tenda_28d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | cury_citi_33400ca3 | sources/digested/notion_cury_citi_33400ca3_summary.md
[wiki-queue] 2026-04-17 | cury | notion | cury_cury_06_11_2026_2d100ca3 | sources/digested/notion_cury_cury_06_11_2026_2d100ca3_summary.md
[wiki-queue] 2026-04-17 | cury | notion | cury_cury_call_4t25_32000ca3 | sources/digested/notion_cury_cury_call_4t25_32000ca3_summary.md
[wiki-queue] 2026-04-17 | cury | notion | cury_cury_fon_dez_2025_2c500ca3 | sources/digested/notion_cury_cury_fon_dez_2025_2c500ca3_summary.md
[wiki-queue] 2026-04-17 | cury | notion | cury_cury_jan_2026_2e000ca3 | sources/digested/notion_cury_cury_jan_2026_2e000ca3_summary.md
[wiki-queue] 2026-04-17 | cury | notion | cury_cury_pos_previa_btg_1t26_33e00ca3 | sources/digested/notion_cury_cury_pos_previa_btg_1t26_33e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | cxse_80b00ca3 | sources/digested/notion_cxse_80b00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_call_cambauva_btg_1t26_33a00ca3 | sources/digested/notion_cyrela_call_cambauva_btg_1t26_33a00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_call_cyrela_4t25_31900ca3 | sources/digested/notion_cyrela_call_cyrela_4t25_31900ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cambauva_btg_23_01_2025_97c00ca3 | sources/digested/notion_cyrela_cambauva_btg_23_01_2025_97c00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_conversa_cyrela_28_04_2025_b3500ca3 | sources/digested/notion_cyrela_conversa_cyrela_28_04_2025_b3500ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cury_btg_2b700ca3 | sources/digested/notion_cyrela_cury_btg_2b700ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cury_ronaldo_24_04_2025_41800ca3 | sources/digested/notion_cyrela_cury_ronaldo_24_04_2025_41800ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_1a_conversa_c8900ca3 | sources/digested/notion_cyrela_cyrela_1a_conversa_c8900ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_1t25_df700ca3 | sources/digested/notion_cyrela_cyrela_1t25_df700ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_3t25_2ab00ca3 | sources/digested/notion_cyrela_cyrela_3t25_2ab00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_87d00ca3 | sources/digested/notion_cyrela_cyrela_87d00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_9_01_2026_2e300ca3 | sources/digested/notion_cyrela_cyrela_9_01_2026_2e300ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_call_com_miguel_32e00ca3 | sources/digested/notion_cyrela_cyrela_call_com_miguel_32e00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_follow_ups_pos_apresenta_o_50700ca3 | sources/digested/notion_cyrela_cyrela_follow_ups_pos_apresenta_o_50700ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_laic_2f500ca3 | sources/digested/notion_cyrela_cyrela_laic_2f500ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_michel_call_cm_itau_20_01_2025_e0900ca3 | sources/digested/notion_cyrela_cyrela_michel_call_cm_itau_20_01_2025_e0900ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_santander_2b800ca3 | sources/digested/notion_cyrela_cyrela_santander_2b800ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_cyrela_xp_conference_55e00ca3 | sources/digested/notion_cyrela_cyrela_xp_conference_55e00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_duvidas_cyrela_pos_2t25_d8900ca3 | sources/digested/notion_cyrela_duvidas_cyrela_pos_2t25_d8900ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_even_primeira_conversa_8a600ca3 | sources/digested/notion_cyrela_even_primeira_conversa_8a600ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_eztec_btg_conference_4cb00ca3 | sources/digested/notion_cyrela_eztec_btg_conference_4cb00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_lavvi_btg_25_08_34b00ca3 | sources/digested/notion_cyrela_lavvi_btg_25_08_34b00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_mendon_a_bbi_real_estate_primeira_conversa_71600ca3 | sources/digested/notion_cyrela_mendon_a_bbi_real_estate_primeira_conversa_71600ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_mrv_real_estate_btg_ee100ca3 | sources/digested/notion_cyrela_mrv_real_estate_btg_ee100ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_trisul_bbi_28c00ca3 | sources/digested/notion_cyrela_trisul_bbi_28c00ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_unidas_cfo_11_12_2024_c1100ca3 | sources/digested/notion_cyrela_unidas_cfo_11_12_2024_c1100ca3_summary.md
[wiki-queue] 2026-04-17 | cyrela | notion | cyrela_unidas_goldman_28700ca3 | sources/digested/notion_cyrela_unidas_goldman_28700ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | d_vidas_weg_reuni_o_11_10_93900ca3 | sources/digested/notion_d_vidas_weg_reuni_o_11_10_93900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | dataprev_consignado_privado_41400ca3 | sources/digested/notion_dataprev_consignado_privado_41400ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | direcional_18_02_30b00ca3 | sources/digested/notion_direcional_18_02_30b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | direcional_59a00ca3 | sources/digested/notion_direcional_59a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | direcional_btg_d4400ca3 | sources/digested/notion_direcional_btg_d4400ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | direcional_call_pos_4t25_31f00ca3 | sources/digested/notion_direcional_call_pos_4t25_31f00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | direcional_laic_2f600ca3 | sources/digested/notion_direcional_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | duvidas_modelo_loma_sasson_ceb00ca3 | sources/digested/notion_duvidas_modelo_loma_sasson_ceb00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3 | sources/digested/notion_entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | estudo_cfa_level_3_quest_es_do_site_e8300ca3 | sources/digested/notion_estudo_cfa_level_3_quest_es_do_site_e8300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | evernote_pdf_f8c00ca3 | sources/digested/notion_evernote_pdf_f8c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | eztec_btg_3t25_2af00ca3 | sources/digested/notion_eztec_btg_3t25_2af00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | fernando_scatena_ceo_stellantis_am_rica_latina_bofa_67e00ca3 | sources/digested/notion_fernando_scatena_ceo_stellantis_am_rica_latina_bofa_67e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | fgts_conselho_curador_24_03_32d00ca3 | sources/digested/notion_fgts_conselho_curador_24_03_32d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | fw_convite_j_safra_15h_videoconfer_ncia_com_weg_andr_menegueti_salgueiro_diretor_de_finan_as_e_ri_e_felipe_scopel_hoffmann_gerente_de_ri_tuesday_may_7_2024_88700ca3 | sources/digested/notion_fw_convite_j_safra_15h_videoconfer_ncia_com_weg_andr_menegueti_salgueiro_diretor_de_finan_as_e_ri_e_felipe_scopel_hoffmann_gerente_de_ri_tuesday_may_7_2024_88700ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | gabriel_head_neon_consignado_privado_33000ca3 | sources/digested/notion_gabriel_head_neon_consignado_privado_33000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | gabriel_neon_consignado_privado_2ce00ca3 | sources/digested/notion_gabriel_neon_consignado_privado_2ce00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | gabriel_tamayo_klar_chief_banking_officer_mexico_2ea00ca3 | sources/digested/notion_gabriel_tamayo_klar_chief_banking_officer_mexico_2ea00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | gavioes_24_03_2026_32d00ca3 | sources/digested/notion_gavioes_24_03_2026_32d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | hailton_madureira_secret_rio_executivo_do_minist_rio_da_habita_o_a9f00ca3 | sources/digested/notion_hailton_madureira_secret_rio_executivo_do_minist_rio_da_habita_o_a9f00ca3_summary.md
[wiki-queue] 2026-04-17 | ifood | notion | ifood_ifood_diego_xp_5f300ca3 | sources/digested/notion_ifood_ifood_diego_xp_5f300ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_banco_inter_21_05_2024_58e00ca3 | sources/digested/notion_inter_banco_inter_21_05_2024_58e00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_bb_banco_do_brasil_jpm_4bb00ca3 | sources/digested/notion_inter_bb_banco_do_brasil_jpm_4bb00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_call_inter_19_02_pos_resultado_4t25_30c00ca3 | sources/digested/notion_inter_call_inter_19_02_pos_resultado_4t25_30c00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_15_07_34000ca3 | sources/digested/notion_inter_inter_15_07_34000ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_1t25_resultado_33400ca3 | sources/digested/notion_inter_inter_1t25_resultado_33400ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_2t25_89800ca3 | sources/digested/notion_inter_inter_2t25_89800ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_2t25_call_follow_up_be200ca3 | sources/digested/notion_inter_inter_2t25_call_follow_up_be200ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_2t25_fb100ca3 | sources/digested/notion_inter_inter_2t25_fb100ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_4t25_30400ca3 | sources/digested/notion_inter_inter_4t25_30400ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_8ea00ca3 | sources/digested/notion_inter_inter_8ea00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_90100ca3 | sources/digested/notion_inter_inter_90100ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_alexandre_consignado_privado_cac00ca3 | sources/digested/notion_inter_inter_alexandre_consignado_privado_cac00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_almoco_08_08_2024_pos_2t24_b2700ca3 | sources/digested/notion_inter_inter_almoco_08_08_2024_pos_2t24_b2700ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_bbi_04_07_2024_6b400ca3 | sources/digested/notion_inter_inter_bbi_04_07_2024_6b400ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_call_3t25_2aa00ca3 | sources/digested/notion_inter_inter_call_3t25_2aa00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_call_com_citi_pos_1t25_e2400ca3 | sources/digested/notion_inter_inter_call_com_citi_pos_1t25_e2400ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_jpm_3t25_ceo_series_2af00ca3 | sources/digested/notion_inter_inter_jpm_3t25_ceo_series_2af00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_laic_2f600ca3 | sources/digested/notion_inter_inter_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_rafa_17_12_2025_2cc00ca3 | sources/digested/notion_inter_inter_rafa_17_12_2025_2cc00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_rafa_safra_2025_36f00ca3 | sources/digested/notion_inter_inter_rafa_safra_2025_36f00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_resultado_2t24_5c800ca3 | sources/digested/notion_inter_inter_resultado_2t24_5c800ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_reuni_o_pos_1t25_ac900ca3 | sources/digested/notion_inter_inter_reuni_o_pos_1t25_ac900ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_santander_marlos_araujo_31b00ca3 | sources/digested/notion_inter_inter_santander_marlos_araujo_31b00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_inter_santiago_08_07_2d200ca3 | sources/digested/notion_inter_inter_santiago_08_07_2d200ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_nota_sem_t_tulo_6df00ca3 | sources/digested/notion_inter_nota_sem_t_tulo_6df00ca3_summary.md
[wiki-queue] 2026-04-17 | inter | notion | inter_tech_day_inter_13_05_ee200ca3 | sources/digested/notion_inter_tech_day_inter_13_05_ee200ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | iolanda_skyfit_2af00ca3 | sources/digested/notion_iolanda_skyfit_2af00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_abla_itau_bba_29a00ca3 | sources/digested/notion_itau_abla_itau_bba_29a00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_bb_btg_geovanne_cfo_c9200ca3 | sources/digested/notion_itau_bb_btg_geovanne_cfo_c9200ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_call_de_resultados_itub_1t24_f8e00ca3 | sources/digested/notion_itau_call_de_resultados_itub_1t24_f8e00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_call_itau_pos_resultado_2a300ca3 | sources/digested/notion_itau_call_itau_pos_resultado_2a300ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_hailton_ministerio_das_cidades_itau_bba_29c00ca3 | sources/digested/notion_itau_hailton_ministerio_das_cidades_itau_bba_29c00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_hyundai_caf_itau_28c00ca3 | sources/digested/notion_itau_hyundai_caf_itau_28c00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_06_11_2024_e1900ca3 | sources/digested/notion_itau_itau_06_11_2024_e1900ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_11_02_gustavo_pos_4t24_cc200ca3 | sources/digested/notion_itau_itau_11_02_gustavo_pos_4t24_cc200ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_3t25_call_2a200ca3 | sources/digested/notion_itau_itau_3t25_call_2a200ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_4t25_call_2fe00ca3 | sources/digested/notion_itau_itau_4t25_call_2fe00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_50a00ca3 | sources/digested/notion_itau_itau_50a00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_btg_92700ca3 | sources/digested/notion_itau_itau_btg_92700ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_citi_fb200ca3 | sources/digested/notion_itau_itau_citi_fb200ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_day_12600ca3 | sources/digested/notion_itau_itau_day_12600ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_day_2025_eaa00ca3 | sources/digested/notion_itau_itau_day_2025_eaa00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_gustavo_apos_4t25_30300ca3 | sources/digested/notion_itau_itau_gustavo_apos_4t25_30300ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_jpm_d7b00ca3 | sources/digested/notion_itau_itau_jpm_d7b00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_mapa_4_sexta_feira_19_de_abril_de_2024_46600ca3 | sources/digested/notion_itau_itau_mapa_4_sexta_feira_19_de_abril_de_2024_46600ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_monthly_sell_side_financials_28700ca3 | sources/digested/notion_itau_itau_monthly_sell_side_financials_28700ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_pos_1t25_caf_da_manha_cb100ca3 | sources/digested/notion_itau_itau_pos_1t25_caf_da_manha_cb100ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_itau_safra_2025_53700ca3 | sources/digested/notion_itau_itau_safra_2025_53700ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_loma_negra_citi_83d00ca3 | sources/digested/notion_itau_loma_negra_citi_83d00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_loma_negra_ubs_87f00ca3 | sources/digested/notion_itau_loma_negra_ubs_87f00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_on_line_ibba_events_caf_da_manh_ita_unibanco_resultados_1t24_wednesday_may_8_2024_cac00ca3 | sources/digested/notion_itau_on_line_ibba_events_caf_da_manh_ita_unibanco_resultados_1t24_wednesday_may_8_2024_cac00ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_pagbank_citi_f2100ca3 | sources/digested/notion_itau_pagbank_citi_f2100ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_pags_emerson_a_terra_29_04_59000ca3 | sources/digested/notion_itau_pags_emerson_a_terra_29_04_59000ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_pedro_coutinho_safra_30400ca3 | sources/digested/notion_itau_pedro_coutinho_safra_30400ca3_summary.md
[wiki-queue] 2026-04-17 | itau | notion | itau_stone_citi_9a600ca3 | sources/digested/notion_itau_stone_citi_9a600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | joao_braz_consignado_privado_facta_2c500ca3 | sources/digested/notion_joao_braz_consignado_privado_facta_2c500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | jorge_kuri_10_2025_28e00ca3 | sources/digested/notion_jorge_kuri_10_2025_28e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | jpmorgan_dataagro_31900ca3 | sources/digested/notion_jpmorgan_dataagro_31900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | kikos_12_12_a5c00ca3 | sources/digested/notion_kikos_12_12_a5c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | kikos_ricardo_carmo_56700ca3 | sources/digested/notion_kikos_ricardo_carmo_56700ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_call_localiza_nora_2e200ca3 | sources/digested/notion_localiza_call_localiza_nora_2e200ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_1t25_resultado_cc_e0900ca3 | sources/digested/notion_localiza_localiza_1t25_resultado_cc_e0900ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_2t25_8d700ca3 | sources/digested/notion_localiza_localiza_2t25_8d700ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_citi_af800ca3 | sources/digested/notion_localiza_localiza_citi_af800ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_depreciation_day_b1e00ca3 | sources/digested/notion_localiza_localiza_depreciation_day_b1e00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_laic_2f500ca3 | sources/digested/notion_localiza_localiza_laic_2f500ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_pos_3t24_9b100ca3 | sources/digested/notion_localiza_localiza_pos_3t24_9b100ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_resultados_1t24_c3d00ca3 | sources/digested/notion_localiza_localiza_resultados_1t24_c3d00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_rodrigo_tavares_cfo_16_04_2025_a1b00ca3 | sources/digested/notion_localiza_localiza_rodrigo_tavares_cfo_16_04_2025_a1b00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_safra_2025_5ce00ca3 | sources/digested/notion_localiza_localiza_safra_2025_5ce00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_terra_luis_ex_rent_f1700ca3 | sources/digested/notion_localiza_localiza_terra_luis_ex_rent_f1700ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_localiza_xp_conference_e4200ca3 | sources/digested/notion_localiza_localiza_xp_conference_e4200ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_lolcaiza_ex_gerente_de_suprimentos_93800ca3 | sources/digested/notion_localiza_lolcaiza_ex_gerente_de_suprimentos_93800ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_rent_22_05_2024_a7b00ca3 | sources/digested/notion_localiza_rent_22_05_2024_a7b00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_reuni_o_com_unidas_gtf_cbc00ca3 | sources/digested/notion_localiza_reuni_o_com_unidas_gtf_cbc00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_reuni_o_marcelo_gm_f1b00ca3 | sources/digested/notion_localiza_reuni_o_marcelo_gm_f1b00ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_reuniao_leonardo_tosello_volks_ff600ca3 | sources/digested/notion_localiza_reuniao_leonardo_tosello_volks_ff600ca3_summary.md
[wiki-queue] 2026-04-17 | localiza | notion | localiza_unidas_ubs_2e800ca3 | sources/digested/notion_localiza_unidas_ubs_2e800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | loma_negra_e2800ca3 | sources/digested/notion_loma_negra_e2800ca3_summary.md
[wiki-queue] 2026-04-17 | mercantil | notion | mercantil_mercantil_xp_d4c00ca3 | sources/digested/notion_mercantil_mercantil_xp_d4c00ca3_summary.md
[wiki-queue] 2026-04-17 | metal_leve | notion | metal_leve_mahle_metalleve_ceo_dd500ca3 | sources/digested/notion_metal_leve_mahle_metalleve_ceo_dd500ca3_summary.md
[wiki-queue] 2026-04-17 | metal_leve | notion | metal_leve_metal_leve_pos_3t25_2cd00ca3 | sources/digested/notion_metal_leve_metal_leve_pos_3t25_2cd00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | moura_dubeux_2e800ca3 | sources/digested/notion_moura_dubeux_2e800ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_conversa_movida_pos_3t25_2b700ca3 | sources/digested/notion_movida_conversa_movida_pos_3t25_2b700ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_14_8_2024_e4900ca3 | sources/digested/notion_movida_movida_14_8_2024_e4900ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_btg_ef700ca3 | sources/digested/notion_movida_movida_btg_ef700ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_call_4t25_32d00ca3 | sources/digested/notion_movida_movida_call_4t25_32d00ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_call_de_resultado_4f200ca3 | sources/digested/notion_movida_movida_call_de_resultado_4f200ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_citi_ab300ca3 | sources/digested/notion_movida_movida_citi_ab300ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_citi_e9100ca3 | sources/digested/notion_movida_movida_citi_e9100ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_laic_2f600ca3 | sources/digested/notion_movida_movida_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | movida | notion | movida_movida_xp_conference_69a00ca3 | sources/digested/notion_movida_movida_xp_conference_69a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | mrv_2t25_c0c00ca3 | sources/digested/notion_mrv_2t25_c0c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | mrv_bfc00ca3 | sources/digested/notion_mrv_bfc00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | mrv_day_31f00ca3 | sources/digested/notion_mrv_day_31f00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | mrv_ri_perguntas_72200ca3 | sources/digested/notion_mrv_ri_perguntas_72200ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_3_23_pm_nome_pais_data_cpu_cores_k_fabricante_gpu_gpus_gpu_asp_gpu_revenue_k_usd_frontier_eua_2022_56_d3500ca3 | sources/digested/notion_nota_3_de_jun_3_23_pm_nome_pais_data_cpu_cores_k_fabricante_gpu_gpus_gpu_asp_gpu_revenue_k_usd_frontier_eua_2022_56_d3500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_3_24_pm_nome_pais_data_cpu_cores_k_fabricante_gpu_gpus_gpu_asp_gpu_revenue_k_usd_frontier_eua_2022_56_d4500ca3 | sources/digested/notion_nota_3_de_jun_3_24_pm_nome_pais_data_cpu_cores_k_fabricante_gpu_gpus_gpu_asp_gpu_revenue_k_usd_frontier_eua_2022_56_d4500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_6_38_pm_aa300ca3 | sources/digested/notion_nota_3_de_jun_6_38_pm_aa300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_6_39_pm_billions_usd_4q23_capex_major_csps_32_7_equip_spend_19_62_nvidia_revenue_4q23_18_40_of_re_d1000ca3 | sources/digested/notion_nota_3_de_jun_6_39_pm_billions_usd_4q23_capex_major_csps_32_7_equip_spend_19_62_nvidia_revenue_4q23_18_40_of_re_d1000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_9_01_pm_eps_2025_margem_bruta_33_8_72_0_74_5_76_5_tam_gpu_88_000_23_5_24_4_25_2_108_000_27_8_29_f6900ca3 | sources/digested/notion_nota_3_de_jun_9_01_pm_eps_2025_margem_bruta_33_8_72_0_74_5_76_5_tam_gpu_88_000_23_5_24_4_25_2_108_000_27_8_29_f6900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_9_27_pm_35800ca3 | sources/digested/notion_nota_3_de_jun_9_27_pm_35800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_9_35_pm_b1f00ca3 | sources/digested/notion_nota_3_de_jun_9_35_pm_b1f00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_3_de_jun_9_48_pm_e4e00ca3 | sources/digested/notion_nota_3_de_jun_9_48_pm_e4e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_4_de_ago_6_55_pm_ac700ca3 | sources/digested/notion_nota_4_de_ago_6_55_pm_ac700ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_4_de_jun_4_38_pm_ai_accelerator_market_share_cy22_cy23_cy24e_cy25e_cy26e_cy27e_broadcom_bn_1_50_3_00_7_50_9_0_fcc00ca3 | sources/digested/notion_nota_4_de_jun_4_38_pm_ai_accelerator_market_share_cy22_cy23_cy24e_cy25e_cy26e_cy27e_broadcom_bn_1_50_3_00_7_50_9_0_fcc00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_39d00ca3 | sources/digested/notion_nota_sem_t_tulo_39d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_60d00ca3 | sources/digested/notion_nota_sem_t_tulo_60d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_7e000ca3 | sources/digested/notion_nota_sem_t_tulo_7e000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_8e600ca3 | sources/digested/notion_nota_sem_t_tulo_8e600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_97300ca3 | sources/digested/notion_nota_sem_t_tulo_97300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_a6b00ca3 | sources/digested/notion_nota_sem_t_tulo_a6b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_b9500ca3 | sources/digested/notion_nota_sem_t_tulo_b9500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_c7800ca3 | sources/digested/notion_nota_sem_t_tulo_c7800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nota_sem_t_tulo_e2b00ca3 | sources/digested/notion_nota_sem_t_tulo_e2b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | notas_reuniao_mattos_filho_reforma_tributaria_incorporadoras_33e00ca3 | sources/digested/notion_notas_reuniao_mattos_filho_reforma_tributaria_incorporadoras_33e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | now_brazil_ev_series_brazilian_association_of_electric_vehicles_abve_friday_may_3_2024_ee000ca3 | sources/digested/notion_now_brazil_ev_series_brazilian_association_of_electric_vehicles_abve_friday_may_3_2024_ee000ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_banco_inter_e3100ca3 | sources/digested/notion_nubank_banco_inter_e3100ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_capstone_2aa00ca3 | sources/digested/notion_nubank_capstone_2aa00ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_ceo_series_nubank_3t25_jpm_2b000ca3 | sources/digested/notion_nubank_ceo_series_nubank_3t25_jpm_2b000ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_chile_nubank_34700ca3 | sources/digested/notion_nubank_chile_nubank_34700ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_claro_jos_felix_presidente_c1d00ca3 | sources/digested/notion_nubank_claro_jos_felix_presidente_c1d00ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_klar_ceo_citi_29200ca3 | sources/digested/notion_nubank_klar_ceo_citi_29200ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nota_sem_t_tulo_8f000ca3 | sources/digested/notion_nubank_nota_sem_t_tulo_8f000ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nu_us_bofa_28b00ca3 | sources/digested/notion_nubank_nu_us_bofa_28b00ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_02_10_2025_33900ca3 | sources/digested/notion_nubank_nubank_02_10_2025_33900ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_1t24_bab00ca3 | sources/digested/notion_nubank_nubank_1t24_bab00ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_3t25_2c400ca3 | sources/digested/notion_nubank_nubank_3t25_2c400ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_btg_8b300ca3 | sources/digested/notion_nubank_nubank_btg_8b300ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_call_4t25_31200ca3 | sources/digested/notion_nubank_nubank_call_4t25_31200ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_callback_btg_4t25_31300ca3 | sources/digested/notion_nubank_nubank_callback_btg_4t25_31300ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_citi_ec200ca3 | sources/digested/notion_nubank_nubank_citi_ec200ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_lago_7b600ca3 | sources/digested/notion_nubank_nubank_lago_7b600ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_lago_jpm_ap_s_3t24_de400ca3 | sources/digested/notion_nubank_nubank_lago_jpm_ap_s_3t24_de400ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_lago_pos_4t25_31400ca3 | sources/digested/notion_nubank_nubank_lago_pos_4t25_31400ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_laic_2f600ca3 | sources/digested/notion_nubank_nubank_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_mexico_ce200ca3 | sources/digested/notion_nubank_nubank_mexico_ce200ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_souto_almo_o_bba_c1f00ca3 | sources/digested/notion_nubank_nubank_souto_almo_o_bba_c1f00ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_nubank_ximena_salgado_feb00ca3 | sources/digested/notion_nubank_nubank_ximena_salgado_feb00ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_reuni_o_nubank_souto_13_04_2026_34100ca3 | sources/digested/notion_nubank_reuni_o_nubank_souto_13_04_2026_34100ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_reuniao_cfo_csd_daniel_d3200ca3 | sources/digested/notion_nubank_reuniao_cfo_csd_daniel_d3200ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_stone_1t24_af700ca3 | sources/digested/notion_nubank_stone_1t24_af700ca3_summary.md
[wiki-queue] 2026-04-17 | nubank | notion | nubank_stone_jpm_db500ca3 | sources/digested/notion_nubank_stone_jpm_db500ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_650_group_call_networking_switching_76300ca3 | sources/digested/notion_nvidia_650_group_call_networking_switching_76300ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_acquired_tsmc_5ab00ca3 | sources/digested/notion_nvidia_acquired_tsmc_5ab00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_conference_call_chip_distributor_expert_call_with_kevin_wang_fbc00ca3 | sources/digested/notion_nvidia_conference_call_chip_distributor_expert_call_with_kevin_wang_fbc00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_conversa_guilherme_kinea_5d000ca3 | sources/digested/notion_nvidia_conversa_guilherme_kinea_5d000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | nvidia_genial_call_87f00ca3 | sources/digested/notion_nvidia_genial_call_87f00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3 | sources/digested/notion_nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_lisa_su_podcast_7a100ca3 | sources/digested/notion_nvidia_lisa_su_podcast_7a100ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_marvell_investor_relations_54c00ca3 | sources/digested/notion_nvidia_marvell_investor_relations_54c00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_networking_switching_call_f3400ca3 | sources/digested/notion_nvidia_networking_switching_call_f3400ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_3ef00ca3 | sources/digested/notion_nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_3ef00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_85c00ca3 | sources/digested/notion_nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_85c00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_95900ca3 | sources/digested/notion_nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_95900ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_bc000ca3 | sources/digested/notion_nvidia_nota_19_de_mai_1_18_pm_ano_2022_2023_2024_2025_2026_2027_total_server_revenue_usd_billions_95_123_167_197_214_233_non_bc000ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nota_3_de_jun_6_27_pm_ano_2022_2023_1q24_2024_2025_2026_2027_total_server_revenue_usd_billions_95_126_197_218_237_252_d6900ca3 | sources/digested/notion_nvidia_nota_3_de_jun_6_27_pm_ano_2022_2023_1q24_2024_2025_2026_2027_total_server_revenue_usd_billions_95_126_197_218_237_252_d6900ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nvidia_preview_citi_1t24_8a300ca3 | sources/digested/notion_nvidia_nvidia_preview_citi_1t24_8a300ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_nvidia_stewart_ir_director_88600ca3 | sources/digested/notion_nvidia_nvidia_stewart_ir_director_88600ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_reuni_o_virtual_necton_investimentos_monday_april_29_2024_conversa_marcio_aguiar_nvidia_28e00ca3 | sources/digested/notion_nvidia_reuni_o_virtual_necton_investimentos_monday_april_29_2024_conversa_marcio_aguiar_nvidia_28e00ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_reuniao_dj_reddy_microsoft_71600ca3 | sources/digested/notion_nvidia_reuniao_dj_reddy_microsoft_71600ca3_summary.md
[wiki-queue] 2026-04-17 | nvidia | notion | nvidia_tegus_tsmc_nvidia_33000ca3 | sources/digested/notion_nvidia_tegus_tsmc_nvidia_33000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | pags_pos_3t25_safra_2c400ca3 | sources/digested/notion_pags_pos_3t25_safra_2c400ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_former_kikos_ricardo_d8b00ca3 | sources/digested/notion_panobianco_former_kikos_ricardo_d8b00ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_lucas_broggio_coo_panobianco_31700ca3 | sources/digested/notion_panobianco_lucas_broggio_coo_panobianco_31700ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_panobianco_andre_61f00ca3 | sources/digested/notion_panobianco_panobianco_andre_61f00ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_panobianco_andre_89800ca3 | sources/digested/notion_panobianco_panobianco_andre_89800ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_panobianco_antovio_vicentim_franquiado_4d600ca3 | sources/digested/notion_panobianco_panobianco_antovio_vicentim_franquiado_4d600ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_panobianco_bob_ford_2e200ca3 | sources/digested/notion_panobianco_panobianco_bob_ford_2e200ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_panobianco_jessica_master_franquiadaa_b0f00ca3 | sources/digested/notion_panobianco_panobianco_jessica_master_franquiadaa_b0f00ca3_summary.md
[wiki-queue] 2026-04-17 | panobianco | notion | panobianco_panobianco_jessica_menali_25_03_32e00ca3 | sources/digested/notion_panobianco_panobianco_jessica_menali_25_03_32e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | perguntas_smart_pos_1t24_5a000ca3 | sources/digested/notion_perguntas_smart_pos_1t24_5a000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_big_group_meeting_2f100ca3 | sources/digested/notion_picpay_big_group_meeting_2f100ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_btg_caf_da_manh_31100ca3 | sources/digested/notion_picpay_btg_caf_da_manh_31100ca3_summary.md
[wiki-queue] 2026-04-17 | picpay | notion | picpay_call_ceo_picpay_jpm_31900ca3 | sources/digested/notion_picpay_call_ceo_picpay_jpm_31900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_duvidas_2ef00ca3 | sources/digested/notion_picpay_duvidas_2ef00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_investor_relations_2bd00ca3 | sources/digested/notion_picpay_investor_relations_2bd00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_prospecto_05_01_2df00ca3 | sources/digested/notion_picpay_prospecto_05_01_2df00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_rascunho_a7800ca3 | sources/digested/notion_picpay_rascunho_a7800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | picpay_reuni_o_com_management_perguntas_2bd00ca3 | sources/digested/notion_picpay_reuni_o_com_management_perguntas_2bd00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_caixa_seg_bbb00ca3 | sources/digested/notion_porto_seguro_caixa_seg_bbb00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_call_porto_seguro_3t25_2a800ca3 | sources/digested/notion_porto_seguro_call_porto_seguro_3t25_2a800ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_kakinoff_3t25_jpm_2a800ca3 | sources/digested/notion_porto_seguro_kakinoff_3t25_jpm_2a800ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_bank_lou_o_14_05_2025_eb900ca3 | sources/digested/notion_porto_seguro_porto_bank_lou_o_14_05_2025_eb900ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_bank_lou_o_bbi_pos_3t25_2a900ca3 | sources/digested/notion_porto_seguro_porto_bank_lou_o_bbi_pos_3t25_2a900ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_call_resultados_4t25_2fe00ca3 | sources/digested/notion_porto_seguro_porto_call_resultados_4t25_2fe00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_seguro_alexsander_27_05_b4d00ca3 | sources/digested/notion_porto_seguro_porto_seguro_alexsander_27_05_b4d00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_seguro_alexsander_update_byd_e_carro_el_trico_9e500ca3 | sources/digested/notion_porto_seguro_porto_seguro_alexsander_update_byd_e_carro_el_trico_9e500ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_seguro_btg_67c00ca3 | sources/digested/notion_porto_seguro_porto_seguro_btg_67c00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_seguro_citi_efe00ca3 | sources/digested/notion_porto_seguro_porto_seguro_citi_efe00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_seguro_domingos_e_aleksandro_7ab00ca3 | sources/digested/notion_porto_seguro_porto_seguro_domingos_e_aleksandro_7ab00ca3_summary.md
[wiki-queue] 2026-04-17 | porto_seguro | notion | porto_seguro_porto_seguro_jpm_69c00ca3 | sources/digested/notion_porto_seguro_porto_seguro_jpm_69c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | principais_d_vidas_bess_c2600ca3 | sources/digested/notion_principais_d_vidas_bess_c2600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | principais_perguntas_questionamentos_totalpass_33a00ca3 | sources/digested/notion_principais_perguntas_questionamentos_totalpass_33a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | problemas_da_basicfit_ef700ca3 | sources/digested/notion_problemas_da_basicfit_ef700ca3_summary.md
[wiki-queue] 2026-04-17 | resia | notion | resia_mrv_laic_2f600ca3 | sources/digested/notion_resia_mrv_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | resia | notion | resia_resia_impairment_call_cdb00ca3 | sources/digested/notion_resia_resia_impairment_call_cdb00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | resultado_2t24_33a00ca3 | sources/digested/notion_resultado_2t24_33a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | reuni_o_conselho_curador_fgts_da600ca3 | sources/digested/notion_reuni_o_conselho_curador_fgts_da600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | reuni_o_dataprev_bbi_29300ca3 | sources/digested/notion_reuni_o_dataprev_bbi_29300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | reuni_o_moura_dubeux_12h30_diego_villar_33b00ca3 | sources/digested/notion_reuni_o_moura_dubeux_12h30_diego_villar_33b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | reuniao_com_fernanda_stone_pagbank_a4100ca3 | sources/digested/notion_reuniao_com_fernanda_stone_pagbank_a4100ca3_summary.md
[wiki-queue] 2026-04-17 | revolut | notion | revolut_revolut_brasil_ceo_33300ca3 | sources/digested/notion_revolut_revolut_brasil_ceo_33300ca3_summary.md
[wiki-queue] 2026-04-17 | revolut | notion | revolut_revolut_ceo_argentina_xp_28b00ca3 | sources/digested/notion_revolut_revolut_ceo_argentina_xp_28b00ca3_summary.md
[wiki-queue] 2026-04-17 | revolut | notion | revolut_revolut_cfo_m_xico_2fb00ca3 | sources/digested/notion_revolut_revolut_cfo_m_xico_2fb00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | rumo_jpm_df900ca3 | sources/digested/notion_rumo_jpm_df900ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_anp_hauben_31e00ca3 | sources/digested/notion_santander_anp_hauben_31e00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_bruno_franco_bmg_consignado_inss_43600ca3 | sources/digested/notion_santander_bruno_franco_bmg_consignado_inss_43600ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_call_sanb_capstone_sexta_feira_3_de_maio_de_2024_76100ca3 | sources/digested/notion_santander_call_sanb_capstone_sexta_feira_3_de_maio_de_2024_76100ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_call_santander_29b00ca3 | sources/digested/notion_santander_call_santander_29b00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_call_santander_3t25_29b00ca3 | sources/digested/notion_santander_call_santander_3t25_29b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | santander_citi_8dc00ca3 | sources/digested/notion_santander_citi_8dc00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_resultado_1t24_santander_f0a00ca3 | sources/digested/notion_santander_resultado_1t24_santander_f0a00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_reuni_o_santander_01_11_2024_e4f00ca3 | sources/digested/notion_santander_reuni_o_santander_01_11_2024_e4f00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_3t24_38100ca3 | sources/digested/notion_santander_santander_3t24_38100ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_3t25_call_com_eles_pos_resultado_29d00ca3 | sources/digested/notion_santander_santander_3t25_call_com_eles_pos_resultado_29d00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_4t25_call_capstone_e_sanb_2fe00ca3 | sources/digested/notion_santander_santander_4t25_call_capstone_e_sanb_2fe00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_call_2t24_d3900ca3 | sources/digested/notion_santander_santander_call_2t24_d3900ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_call_4t25_2fd00ca3 | sources/digested/notion_santander_santander_call_4t25_2fd00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_call_camila_pos_4t25_2fe00ca3 | sources/digested/notion_santander_santander_call_camila_pos_4t25_2fe00ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_citi_9b300ca3 | sources/digested/notion_santander_santander_citi_9b300ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_pos_2t25_85900ca3 | sources/digested/notion_santander_santander_pos_2t25_85900ca3_summary.md
[wiki-queue] 2026-04-17 | santander | notion | santander_santander_safra_pos_3t25_2c300ca3 | sources/digested/notion_santander_santander_safra_pos_3t25_2c300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | secovi_btg_sp_31300ca3 | sources/digested/notion_secovi_btg_sp_31300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | selfit_vinicius_mendon_a_cfo_03_02_2026_2fc00ca3 | sources/digested/notion_selfit_vinicius_mendon_a_cfo_03_02_2026_2fc00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | sem_t_tulo_4d000ca3 | sources/digested/notion_sem_t_tulo_4d000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | sem_t_tulo_c7c00ca3 | sources/digested/notion_sem_t_tulo_c7c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | sem_t_tulo_de200ca3 | sources/digested/notion_sem_t_tulo_de200ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | sem_t_tulo_e7400ca3 | sources/digested/notion_sem_t_tulo_e7400ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | semianalysis_blackwell_performance_f9400ca3 | sources/digested/notion_semianalysis_blackwell_performance_f9400ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | simpar_1t24_resultados_32000ca3 | sources/digested/notion_simpar_1t24_resultados_32000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | skyfit_franqueada_thais_2c000ca3 | sources/digested/notion_skyfit_franqueada_thais_2c000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | small_group_com_urbano_duarte_former_vp_de_habita_o_na_caixa_economica_federal_e_conselheiro_do_mercado_de_real_estate_29900ca3 | sources/digested/notion_small_group_com_urbano_duarte_former_vp_de_habita_o_na_caixa_economica_federal_e_conselheiro_do_mercado_de_real_estate_29900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | smart_pos_1t25_rizzardo_36900ca3 | sources/digested/notion_smart_pos_1t25_rizzardo_36900ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_alelo_smartfit_totalpass_c3600ca3 | sources/digested/notion_smartfit_alelo_smartfit_totalpass_c3600ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_call_smartfit_4t25_32100ca3 | sources/digested/notion_smartfit_call_smartfit_4t25_32100ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_d_vidas_smartfit_rizzardo_pos_3t25_2af00ca3 | sources/digested/notion_smartfit_d_vidas_smartfit_rizzardo_pos_3t25_2af00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_nota_sem_t_tulo_ca500ca3 | sources/digested/notion_smartfit_nota_sem_t_tulo_ca500ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_perguntas_smartfit_pos_4t25_32000ca3 | sources/digested/notion_smartfit_perguntas_smartfit_pos_4t25_32000ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_renato_gabas_casa_do_fitness_28a00ca3 | sources/digested/notion_smartfit_renato_gabas_casa_do_fitness_28a00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_selfit_17_01_34900ca3 | sources/digested/notion_smartfit_selfit_17_01_34900ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_selfit_2019_cfo_vinicius_9f100ca3 | sources/digested/notion_smartfit_selfit_2019_cfo_vinicius_9f100ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_silvia_totalpass_9f400ca3 | sources/digested/notion_smartfit_silvia_totalpass_9f400ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smart_safra_24_05_2024_a7e00ca3 | sources/digested/notion_smartfit_smart_safra_24_05_2024_a7e00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_15_08_2024_bf700ca3 | sources/digested/notion_smartfit_smartfit_15_08_2024_bf700ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_1t24_resultados_be200ca3 | sources/digested/notion_smartfit_smartfit_1t24_resultados_be200ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_2t25_call_84e00ca3 | sources/digested/notion_smartfit_smartfit_2t25_call_84e00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_2t25_rizzardo_35400ca3 | sources/digested/notion_smartfit_smartfit_2t25_rizzardo_35400ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_3b400ca3 | sources/digested/notion_smartfit_smartfit_3b400ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_46500ca3 | sources/digested/notion_smartfit_smartfit_46500ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_4t24_2d500ca3 | sources/digested/notion_smartfit_smartfit_4t24_2d500ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_call_com_ri_pos_4t24_f3900ca3 | sources/digested/notion_smartfit_smartfit_call_com_ri_pos_4t24_f3900ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_call_resultados_bfd00ca3 | sources/digested/notion_smartfit_smartfit_call_resultados_bfd00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_citi_4ee00ca3 | sources/digested/notion_smartfit_smartfit_citi_4ee00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_edgar_xp_pos_1t25_76e00ca3 | sources/digested/notion_smartfit_smartfit_edgar_xp_pos_1t25_76e00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_jefferies_06_01_2025_5fb00ca3 | sources/digested/notion_smartfit_smartfit_jefferies_06_01_2025_5fb00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_laic_2f500ca3 | sources/digested/notion_smartfit_smartfit_laic_2f500ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_quantidade_de_tp2_da_smart_na_totalpass_31300ca3 | sources/digested/notion_smartfit_smartfit_quantidade_de_tp2_da_smart_na_totalpass_31300ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_rafael_pires_ex_trade_marketing_32d00ca3 | sources/digested/notion_smartfit_smartfit_rafael_pires_ex_trade_marketing_32d00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smartfit_xp_conference_87800ca3 | sources/digested/notion_smartfit_smartfit_xp_conference_87800ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_smft_capstone_nogueira_sexta_feira_19_de_abril_de_2024_8ea00ca3 | sources/digested/notion_smartfit_smft_capstone_nogueira_sexta_feira_19_de_abril_de_2024_8ea00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_sport_city_9b300ca3 | sources/digested/notion_smartfit_sport_city_9b300ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_thiago_bizotto_franquiado_panobianco_7fe00ca3 | sources/digested/notion_smartfit_thiago_bizotto_franquiado_panobianco_7fe00ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_urquiza_bt_ceo_94300ca3 | sources/digested/notion_smartfit_urquiza_bt_ceo_94300ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_videoconfer_ncia_small_group_aguilar_de_jesus_franqueado_smart_fit_monday_may_6_2024_ad300ca3 | sources/digested/notion_smartfit_videoconfer_ncia_small_group_aguilar_de_jesus_franqueado_smart_fit_monday_may_6_2024_ad300ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_wellhub_douglas_demore_5d100ca3 | sources/digested/notion_smartfit_wellhub_douglas_demore_5d100ca3_summary.md
[wiki-queue] 2026-04-17 | smartfit | notion | smartfit_wellhub_raphael_gouveia_3c700ca3 | sources/digested/notion_smartfit_wellhub_raphael_gouveia_3c700ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | stone_call_com_bbi_1t24_ebb00ca3 | sources/digested/notion_stone_call_com_bbi_1t24_ebb00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | stone_laic_2f600ca3 | sources/digested/notion_stone_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | stone_safra_pos_3t25_2c300ca3 | sources/digested/notion_stone_safra_pos_3t25_2c300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | technogym_btg_29c00ca3 | sources/digested/notion_technogym_btg_29c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | tenda_2f500ca3 | sources/digested/notion_tenda_2f500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | tenda_cfo_19_11_2b000ca3 | sources/digested/notion_tenda_cfo_19_11_2b000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | tenda_ri_2e200ca3 | sources/digested/notion_tenda_ri_2e200ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | tiago_loyola_60c00ca3 | sources/digested/notion_tiago_loyola_60c00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | tokio_marine_seguros_63500ca3 | sources/digested/notion_tokio_marine_seguros_63500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | tsea_reuni_o_com_bba_d0600ca3 | sources/digested/notion_tsea_reuni_o_com_bba_d0600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_29b00ca3 | sources/digested/notion_untitled_29b00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_2cc00ca3 | sources/digested/notion_untitled_2cc00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_2ce00ca3 | sources/digested/notion_untitled_2ce00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_4c500ca3 | sources/digested/notion_untitled_4c500ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_74a00ca3 | sources/digested/notion_untitled_74a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_a4800ca3 | sources/digested/notion_untitled_a4800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_c1d00ca3 | sources/digested/notion_untitled_c1d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_d7f00ca3 | sources/digested/notion_untitled_d7f00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | untitled_e3100ca3 | sources/digested/notion_untitled_e3100ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | vamos_citi_3d800ca3 | sources/digested/notion_vamos_citi_3d800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | vamos_citi_75300ca3 | sources/digested/notion_vamos_citi_75300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | vamos_couto_bba_28600ca3 | sources/digested/notion_vamos_couto_bba_28600ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_q_a_call_vamos_3t25_2a900ca3 | sources/digested/notion_vamos_q_a_call_vamos_3t25_2a900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | vamos_resultado_2t24_40400ca3 | sources/digested/notion_vamos_resultado_2t24_40400ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_vamos_14_08_2024_c6d00ca3 | sources/digested/notion_vamos_vamos_14_08_2024_c6d00ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_vamos_22_01_2025_2f000ca3 | sources/digested/notion_vamos_vamos_22_01_2025_2f000ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_vamos_4t25_32f00ca3 | sources/digested/notion_vamos_vamos_4t25_32f00ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_vamos_call_com_rodrigo_30200ca3 | sources/digested/notion_vamos_vamos_call_com_rodrigo_30200ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_vamos_laic_2f600ca3 | sources/digested/notion_vamos_vamos_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | vamos | notion | vamos_vamos_safra_2025_3de00ca3 | sources/digested/notion_vamos_vamos_safra_2025_3de00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | vamos_xp_f4900ca3 | sources/digested/notion_vamos_xp_f4900ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | vibra_capstone_2f600ca3 | sources/digested/notion_vibra_capstone_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_14_08_79400ca3 | sources/digested/notion_weg_14_08_79400ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_2t25_call_eac00ca3 | sources/digested/notion_weg_2t25_call_eac00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_4t25_call_31300ca3 | sources/digested/notion_weg_4t25_call_31300ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_56200ca3 | sources/digested/notion_weg_56200ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_89600ca3 | sources/digested/notion_weg_89600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_call_jpm_28d00ca3 | sources/digested/notion_weg_call_jpm_28d00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_carlos_grillo_e_harry_neto_bess_fbb00ca3 | sources/digested/notion_weg_carlos_grillo_e_harry_neto_bess_fbb00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_cfo_andr_rodrigues_80e00ca3 | sources/digested/notion_weg_cfo_andr_rodrigues_80e00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_direcional_laic_2f600ca3 | sources/digested/notion_weg_direcional_laic_2f600ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | weg_follow_up_pos_resultado_29500ca3 | sources/digested/notion_weg_follow_up_pos_resultado_29500ca3_summary.md
[wiki-queue] 2026-04-17 | wellhub | notion | wellhub_rodrigo_gomes_wellhub_e9800ca3 | sources/digested/notion_wellhub_rodrigo_gomes_wellhub_e9800ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | xp_14_08_2024_42a00ca3 | sources/digested/notion_xp_14_08_2024_42a00ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | xp_a7400ca3 | sources/digested/notion_xp_a7400ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | xp_jpm_4e000ca3 | sources/digested/notion_xp_jpm_4e000ca3_summary.md
[wiki-queue] 2026-04-17 | generic | notion | xp_safra_pos_3t25_2c300ca3 | sources/digested/notion_xp_safra_pos_3t25_2c300ca3_summary.md
[wiki-done] 2026-04-20 | batch_20260420_200411 (resume)
[wiki-done] 2026-04-21 | batch_20260421_005247 (resume)
[wiki-done] 2026-04-21 | batch_20260421_073514 (resume)
[fetch-calls] 2026-04-21 | tenda | 4T25 | https://www.youtube.com/watch?v=REdGd0xt3RI | auto_forced
2026-04-21 — ingest call_transcript 4T25: sources/full/tenda/4T25/call_transcript.md, sources/digested/tenda_call_transcript_4T25_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 4T25 | sources/digested/tenda_call_transcript_4T25_summary.md
[wiki-done] 2026-04-21 | batch_20260421_133924
[fetch-calls] 2026-04-21 | tenda | 2T20 | https://www.youtube.com/watch?v=g7VEYo3rr2o | auto_forced
[fetch-calls] 2026-04-21 | tenda | 3T20 | https://www.youtube.com/watch?v=AzmmBTZfQgM | auto_forced
[fetch-calls] 2026-04-21 | tenda | 4T20 | https://www.youtube.com/watch?v=4GLwN5nHdwI | auto_forced
[fetch-calls] 2026-04-21 | tenda | 1T21 | https://www.youtube.com/watch?v=Fh5chdTOZfQ | auto_forced
[fetch-calls] 2026-04-21 | tenda | 2T21 | https://www.youtube.com/watch?v=wB66nkXcqu8 | auto_forced
[fetch-calls] 2026-04-21 | tenda | 3T21 | https://www.youtube.com/watch?v=bRezmJo5f20 | auto_forced
[fetch-calls] 2026-04-21 | tenda | 4T21 | https://www.youtube.com/watch?v=jMYCXMpoQhM | auto_forced
[fetch-calls] 2026-04-21 | tenda | 1T22 | https://www.youtube.com/watch?v=0ko92y7bNnc | auto_forced
[fetch-calls] 2026-04-21 | tenda | 2T22 | https://www.youtube.com/watch?v=pVqtIlDdLpg | auto_forced
[fetch-calls] 2026-04-21 | tenda | 3T22 | https://www.youtube.com/watch?v=R8KQoOM_qmE | auto_forced
[fetch-calls] 2026-04-21 | tenda | 4T22 | https://www.youtube.com/watch?v=I7jAkySqhIM | auto_forced
[fetch-calls] 2026-04-21 | tenda | 1T23 | https://www.youtube.com/watch?v=QntbUw5YBpM | auto_forced
[fetch-calls] 2026-04-21 | tenda | 2T23 | https://www.youtube.com/watch?v=5U7uzyx-hvk | auto_forced
[fetch-calls] 2026-04-21 | tenda | 3T23 | https://www.youtube.com/watch?v=W8xBCfDUZ9Q | auto_forced
[fetch-calls] 2026-04-21 | tenda | 4T23 | https://www.youtube.com/watch?v=UdwHan9qqrs | auto_forced
[fetch-calls] 2026-04-21 | tenda | 1T24 | https://www.youtube.com/watch?v=blIn3ISLFIo | auto_forced
[fetch-calls] 2026-04-21 | tenda | 2T24 | https://www.youtube.com/watch?v=kgYVGRwZYbw | auto_forced
[fetch-calls] 2026-04-21 | tenda | 3T24 | https://www.youtube.com/watch?v=fTfZYTICsis | auto_forced
[fetch-calls] 2026-04-21 | tenda | 4T24 | https://www.youtube.com/watch?v=EpDxhSBPaKA | auto_forced
[fetch-calls] 2026-04-21 | tenda | 1T25 | https://www.youtube.com/watch?v=GIqIJFrBDUA | auto_forced
[fetch-calls] 2026-04-21 | tenda | 2T25 | https://www.youtube.com/watch?v=F3EBF1xDyDg | auto_forced
[fetch-calls] 2026-04-21 | tenda | 3T25 | https://www.youtube.com/watch?v=n1ObaGDUI8Q | auto_forced
2026-04-21 — ingest call_transcript 1T21: sources/full/tenda/1T21/call_transcript.md, sources/digested/tenda_call_transcript_1T21_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 1T21 | sources/digested/tenda_call_transcript_1T21_summary.md
2026-04-21 — ingest call_transcript 1T22: sources/full/tenda/1T22/call_transcript.md, sources/digested/tenda_call_transcript_1T22_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 1T22 | sources/digested/tenda_call_transcript_1T22_summary.md
2026-04-21 — ingest call_transcript 1T23: sources/full/tenda/1T23/call_transcript.md, sources/digested/tenda_call_transcript_1T23_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 1T23 | sources/digested/tenda_call_transcript_1T23_summary.md
2026-04-21 — ingest call_transcript 1T24: sources/full/tenda/1T24/call_transcript.md, sources/digested/tenda_call_transcript_1T24_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 1T24 | sources/digested/tenda_call_transcript_1T24_summary.md
2026-04-21 — ingest call_transcript 1T25: sources/full/tenda/1T25/call_transcript.md, sources/digested/tenda_call_transcript_1T25_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 1T25 | sources/digested/tenda_call_transcript_1T25_summary.md
2026-04-21 — ingest call_transcript 2T20: sources/full/tenda/2T20/call_transcript.md, sources/digested/tenda_call_transcript_2T20_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2T20 | sources/digested/tenda_call_transcript_2T20_summary.md
2026-04-21 — ingest call_transcript 2T21: sources/full/tenda/2T21/call_transcript.md, sources/digested/tenda_call_transcript_2T21_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2T21 | sources/digested/tenda_call_transcript_2T21_summary.md
2026-04-21 — ingest call_transcript 2T22: sources/full/tenda/2T22/call_transcript.md, sources/digested/tenda_call_transcript_2T22_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2T22 | sources/digested/tenda_call_transcript_2T22_summary.md
2026-04-21 — ingest call_transcript 2T23: sources/full/tenda/2T23/call_transcript.md, sources/digested/tenda_call_transcript_2T23_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2T23 | sources/digested/tenda_call_transcript_2T23_summary.md
2026-04-21 — ingest call_transcript 2T24: sources/full/tenda/2T24/call_transcript.md, sources/digested/tenda_call_transcript_2T24_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2T24 | sources/digested/tenda_call_transcript_2T24_summary.md
2026-04-21 — ingest call_transcript 2T25: sources/full/tenda/2T25/call_transcript.md, sources/digested/tenda_call_transcript_2T25_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2T25 | sources/digested/tenda_call_transcript_2T25_summary.md
2026-04-21 — ingest call_transcript 3T20: sources/full/tenda/3T20/call_transcript.md, sources/digested/tenda_call_transcript_3T20_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 3T20 | sources/digested/tenda_call_transcript_3T20_summary.md
2026-04-21 — ingest call_transcript 3T21: sources/full/tenda/3T21/call_transcript.md, sources/digested/tenda_call_transcript_3T21_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 3T21 | sources/digested/tenda_call_transcript_3T21_summary.md
2026-04-21 — ingest call_transcript 3T22: sources/full/tenda/3T22/call_transcript.md, sources/digested/tenda_call_transcript_3T22_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 3T22 | sources/digested/tenda_call_transcript_3T22_summary.md
2026-04-21 — ingest call_transcript 3T23: sources/full/tenda/3T23/call_transcript.md, sources/digested/tenda_call_transcript_3T23_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 3T23 | sources/digested/tenda_call_transcript_3T23_summary.md
2026-04-21 — ingest call_transcript 3T24: sources/full/tenda/3T24/call_transcript.md, sources/digested/tenda_call_transcript_3T24_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 3T24 | sources/digested/tenda_call_transcript_3T24_summary.md
2026-04-21 — ingest call_transcript 3T25: sources/full/tenda/3T25/call_transcript.md, sources/digested/tenda_call_transcript_3T25_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 3T25 | sources/digested/tenda_call_transcript_3T25_summary.md
2026-04-21 — ingest call_transcript 4T20: sources/full/tenda/4T20/call_transcript.md, sources/digested/tenda_call_transcript_4T20_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 4T20 | sources/digested/tenda_call_transcript_4T20_summary.md
2026-04-21 — ingest call_transcript 4T21: sources/full/tenda/4T21/call_transcript.md, sources/digested/tenda_call_transcript_4T21_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 4T21 | sources/digested/tenda_call_transcript_4T21_summary.md
2026-04-21 — ingest call_transcript 4T22: sources/full/tenda/4T22/call_transcript.md, sources/digested/tenda_call_transcript_4T22_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 4T22 | sources/digested/tenda_call_transcript_4T22_summary.md
2026-04-21 — ingest call_transcript 4T23: sources/full/tenda/4T23/call_transcript.md, sources/digested/tenda_call_transcript_4T23_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 4T23 | sources/digested/tenda_call_transcript_4T23_summary.md
2026-04-21 — ingest call_transcript 4T24: sources/full/tenda/4T24/call_transcript.md, sources/digested/tenda_call_transcript_4T24_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 4T24 | sources/digested/tenda_call_transcript_4T24_summary.md
[wiki-done] 2026-04-21 | batch_20260421_142435
[wiki-done] 2026-04-21 | batch_20260421_183625
[fetch-calls] 2026-04-21 | tenda | 2025 | https://www.youtube.com/watch?v=vtPXrylBc4A | auto_forced
2026-04-21 — ingest call_transcript 2025: sources/full/tenda/2025/call_transcript.md, sources/digested/tenda_call_transcript_2025_summary.md
[wiki-queue] 2026-04-21 | tenda | call_transcript | 2025 | sources/digested/tenda_call_transcript_2025_summary.md
[wiki-done] 2026-04-21 | batch_20260421_190836
[wiki-queue] 2026-04-22 | generic | other | Bernstein Machinery & Electricals The Section 232 metals tariff c | sources/digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md
[wiki-done] 2026-04-22 | batch_20260422_101115
[edit] 2026-04-22 — rename tenda call_transcript/2025 → investor_day/2025 (Tenda Day 2025); updated full, digested, manifest sources[], tenda.md, reforma_tributaria.md
[wiki-queue] 2026-04-22 | generic | other | tenda_estouro_custos_2020_2022_analise | sources/digested/tenda_estouro_custos_2020_2022_analise_summary.md
[wiki-done] 2026-04-22 | batch_20260422_110057
2026-04-22 — ingest release 4T25: sources/full/porto/4T25/release.md, sources/structured/porto/4T25/release.json, sources/digested/porto_release_4T25_summary.md
2026-04-22 — ingest release 4T25: sources/full/porto/4T25/release.md, sources/structured/porto/4T25/release.json, sources/digested/porto_release_4T25_summary.md
2026-04-22 — ingest fato_relevante 1T25: sources/full/porto/1T25/fato_relevante_859709.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T25: sources/full/porto/1T25/fato_relevante_859724.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_1016298.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_1018154.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_998030.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_998121.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_1003567_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_1015167_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_1016297_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_1018255_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_988430_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_992950_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 1T26: sources/full/porto/1T26/fato_relevante_PSSA3_1T26_previa_operacional_998123_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 2T26: sources/full/porto/2T26/fato_relevante_1029267.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 2T26: sources/full/porto/2T26/fato_relevante_PSSA3_2T26_previa_operacional_1028965_extracted.md.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 3T25: sources/full/porto/3T25/fato_relevante_937067.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 4T25: sources/full/porto/4T25/fato_relevante_963148.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest fato_relevante 4T25: sources/full/porto/4T25/fato_relevante_967980.md, sources/digested/porto_fatos_relevantes_batch_summary.md
2026-04-22 — ingest release unknown: sources/full/porto/other/PSSA3_1T25_call_transcript.md, sources/digested/porto_other_PSSA3_1T25_call_transcript_summary.md
2026-04-22 — ingest release unknown: sources/full/porto/other/PSSA3_2T25_call_transcript.md, sources/digested/porto_other_PSSA3_2T25_call_transcript_summary.md
2026-04-22 — ingest release unknown: sources/full/porto/other/PSSA3_3T25_call_transcript.md, sources/digested/porto_other_PSSA3_3T25_call_transcript_summary.md
2026-04-22 — ingest release unknown: sources/full/porto/other/PSSA3_4T25_call_transcript.md, sources/digested/porto_other_PSSA3_4T25_call_transcript_summary.md
2026-04-22 — ingest release unknown: sources/full/porto/other/PSSA3_4T25_data_pack.md, sources/digested/porto_other_PSSA3_4T25_data_pack_summary.md
[wiki-done] 2026-04-22 | batch_20260422_165204
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=1 hint=0
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=1 hint=0
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=0 hint=0
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=0 hint=238
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=0 hint=238
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=0 hint=238
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=0 warn=0 hint=238
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=646 warn=0 hint=238
[lint] 2026-04-23 sources/lint_reports/2026-04-23.md action=416 warn=0 hint=238
[watch] 2026-04-23 hits=0 report=sources/lint_reports/2026-04-23.md
[watch] 2026-04-24 hits=0 report=sources/lint_reports/2026-04-24-watch.md
[lint] 2026-04-24 sources/lint_reports/2026-04-24.md action=416 warn=0 hint=238
[edit] 2026-04-24 | porto_seguro.md | new §Estrutura organizacional e contribuição por entidade legal + 4 digests de subsidiárias (seguros_auto_home, saúde, financeiro, vida_cap_holding) + 15 fulls extraídos de DFs individuais 2025 publicadas em 13/02/2026 no OESP | one-off investigativo — não reingerir periodicamente | consorcio skipped (PDF só-imagem, 37pg PNG, precisa hybrid OCR)
[edit] 2026-04-24 | porto_seguro.md + porto_consorcio.md full + financeiro digest §6 | re-extração consorcio via PyMuPDF+Claude vision (PDF só-imagem 37pg); análise Saúde aprofundada (cascata holding 2 andares, odonto vive na seguradora, Portomed ramp 80× YoY); Bank reconciliado com Consórcio R$ 288mm lucro (2× Portoseg)
[generic-ingest] 2026-04-24 | full/generic/susep_sinistralidade_auto_analise_2010_2026.md | SUSEP export auto mercado 2010-2026 (194 obs mensais, ramos 0520-0553) | análise sazonalidade sinistralidade: regressão OLS com days_biz/carnaval/year FE, decomposição numerador/denominador, rolling 12M; Fev ex-outlier é mediano não baixo; calendário não explica fev/26 do mercado
[new] 2026-04-24 | sinistralidade_auto.md | concept page — sazonalidade + decomposição + rolling 12M; referencia generic susep + porto_seguro
[new] 2026-04-24 | premio_retido_vs_ganho.md | concept page — Emitido→Retido→Ganho + PPNG + sinistros regime competência + outras receitas saúde (coparticipação/ASO)
[edit] 2026-04-24 | porto_seguro.md | wikilinks [[sinistralidade_auto]] e [[premio_retido_vs_ganho]]; §Vertical 1 Auto adiciona interpretação Fev/26 (não é calendário, é outperformance Porto); §Vertical 2 Saúde adiciona "Como ler o DRE" (Retido≈Ganho ciclo mensal + outras receitas coparticipação/ASO)
[lint] 2026-04-24 sources/lint_reports/2026-04-24.md action=418 warn=0 hint=240
[lint] 2026-04-24 sources/lint_reports/2026-04-24.md action=0 warn=0 hint=0
[lint] 2026-04-24 sources/lint_reports/2026-04-24.md action=0 warn=0 hint=0
[lint] 2026-04-24 sources/lint_reports/2026-04-24.md action=0 warn=0 hint=11
[lint] 2026-04-24 sources/lint_reports/2026-04-24.md action=418 warn=0 hint=240
[new] 2026-04-25 | sources/manifests/weg.json | manifest skeleton WEG (WEGE3) — pre-ingest. Setor industrial, youtube_channel @WEGoficial (a verificar local), wiki_page weg.md, related_digests aponta para 16 digesteds Notion existentes. Fetch profile ainda não criado (precisa rodar fetch.sh --discover na máquina local com CVM-API ativa).
[new] 2026-04-25 | sources/structured/_schemas/industrial.json | schema canônico industrial/v1 — DRE, BP, FC, segmentos (eei/gtd/tintas_vernizes/outros) e kpis_industriais (capex/receita, ROIC, dívida líquida/EBITDA, working capital, headcount, mix Brasil/Externo). Modelado a partir do conhecimento qualitativo dos digesteds Notion de WEG; será refinado quando o primeiro ITR for ingerido.
[fetch-plan] 2026-04-25 | empresa=weg ticker=WEGE3 | escopo: 1T24 → 4T25 (8 trimestres). PDFs e transcrições não estão disponíveis neste sandbox (sandbox-egress bloqueia CVM/YouTube/RI da WEG — só permite GitHub). Plano para execução local, em ordem:
  1. cd /caminho/equity-wiki && bash tools/fetch.sh WEGE3 --discover  → cria fetch_profile no manifest após review humano
  2. bash tools/fetch.sh WEGE3 --horizon 2y --types itr,dfp,release,fato_relevante  → baixa para sources/undigested/
     Esperados (8 ITRs + 2 DFPs + 8 releases trimestrais; fatos relevantes filtrados via fetch_profile):
       [ ] ITR 1T24    [ ] release 1T24   [ ] DFP 2024 (anual, cobre 4T24)
       [ ] ITR 2T24    [ ] release 2T24
       [ ] ITR 3T24    [ ] release 3T24
                        [ ] release 4T24 (publicado em fev/2025)
       [ ] ITR 1T25    [ ] release 1T25   [ ] DFP 2025 (anual, cobre 4T25 — sai ~fev/2026)
       [ ] ITR 2T25    [ ] release 2T25
       [ ] ITR 3T25    [ ] release 3T25
                        [ ] release 4T25 (publicado em fev/2026)
  3. bash tools/fetch_calls.sh WEGE3 --discover  → confirma handle do canal (manifest hoje grava @WEGoficial; ajustar se necessário) e gera audit plan trimestral
  4. bash tools/fetch_calls.sh WEGE3  → 8 transcrições esperadas (1T24, 2T24, 3T24, 4T24, 1T25, 2T25, 3T25, 4T25)
  5. WEG Day 2024 e WEG Day 2025: NÃO estão na CVM. Baixar manualmente do site de RI (ri.weg.net) e colocar em sources/undigested/ como weg_apresentacao_weg_day_2024.pdf e weg_apresentacao_weg_day_2025.pdf antes do ingest. Light path (full + digested, sem structured).
  6. bash tools/ingest.sh WEGE3 --concurrency 4  → heavy path (ITR/DFP/release → full/structured/digested) + light (fato_relevante, WEG Day → full/digested)
  7. bash tools/ingest_calls.sh WEGE3  → 8 transcrições → full/digested
  8. bash tools/wiki_update.sh  → mescla digesteds novos com weg.md existente (já há 254 linhas baseadas em digesteds Notion — wiki update vai integrar com números trimestrais oficiais)
  Notas: 4T (release 4T24 e 4T25) deve ser ingerido como release próprio mesmo que a DFP do ano cubra os mesmos números — release vem antes da DFP e tem material gerencial. Próximo resultado WEG sai na semana de 28/abr–02/mai/2026 (1T26) — após esse cold start, ingest 1T26 incremental fica trivial.

[tese-new] 2026-04-27 cury — created cury_tese.md (verdict: neutro a R$ 30,25); 3 pilares de Lente, sem seção legada para migrar

[edit] 2026-04-27 | porto_seguro.md | refinamento §Bank-Consórcio: decomposição da Receita gerencial 2025 em Fee-Based 92% + Receita Financeira Líquida 8% (R$ 105,5 mm); natureza dos R$ 105 mm via NE 20/21 da DF (juros mora R$ 59 mm + TVM próprio R$ 12 mm + atualização judiciais R$ 13 mm − funding R$ 46 mm); explicita que NÃO é spread sobre R$ 5 bi caixa dos grupos (fiduciário Res BCB 352/23, rendimento R$ 435 mm vai pros consorciados); flag de salto +149% YoY como parcialmente reclassificação por Res 4.966/352
[fetch-discover] 2026-04-27 | empresa=weg ticker=WEGE3 | sample=4T25 | profile categories: release_resultado_pt=include, demonstracoes_financeiras_pt=include, demonstracoes_financeiras_en=exclude, fato_relevante=include. Profile aplicado direto no manifest (read REPLY do interactive prompt timeoutou no run em background); discovery agent classificou ok via Sonnet.
[fix] 2026-04-27 | tools/lib/file_extract.py | adicionado flag -q ao subprocess do opendataloader_pdf. Sem ela, no Windows o JAR escreve em stdout bytes cp1252 e o wrapper Python (que le com text=True UTF-8) falha com UnicodeDecodeError, retornando exit !=0 mesmo apos gerar o .md correto. Resultado: ingest fallback no pdfplumber (proibido pelo CLAUDE.md). Confirmado em wege3_4T25_call_transcript.pdf — pre-fix vinha pdfplumber 14p/61911 chars com layout quebrado; pos-fix vem opendataloader 48p/64530 chars com headings preservados.
[ingest-resume] 2026-04-28 | empresa=weg ticker=WEGE3 | run anterior bateu rate-limit (org monthly usage limit) apos processar 11 de 22: ITRs 1T24-3T25, DFPs 2024+2025, releases 1T24/2T24/1T25. Pendentes: 5 releases (3T24,4T24,2T25,3T25,4T25), 2 DFs anuais (4T24,4T25 heavy_other), 4 fatos relevantes. Cleanup parcial: removidos 11 PDFs+extracted dos prontos do undigested/; manifesto NAO foi atualizado pelo run anterior (step 4 nao chegou a rodar); sera reconstruido com manifest_rebuild apos completar.
[fix] 2026-04-28 | tools/ingest.sh | SCHEMA_PATH agora le do manifest (campo setor_schema). Antes era hardcoded sources/structured/_schemas/incorporadora.json — todos os 8 ingests heavy do WEG no run anterior reportaram schema mismatch e tiveram que corrigir manualmente para industrial.json. Fallback para incorporadora.json se manifest nao declarar setor_schema.
2026-04-28 — ingest release 2T25: sources/full/weg/2T25/release.md, sources/structured/weg/2T25/release.json, sources/digested/weg_release_2T25_summary.md
2026-04-28 — ingest release 3T24: sources/full/weg/3T24/release.md, sources/structured/weg/3T24/release.json, sources/digested/weg_release_3T24_summary.md
2026-04-28 — ingest release 3T25: sources/full/weg/3T25/release.md, sources/structured/weg/3T25/release.json, sources/digested/weg_release_3T25_summary.md
2026-04-28 — ingest release 4T24: sources/full/weg/4T24/release.md, sources/structured/weg/4T24/release.json, sources/digested/weg_release_4T24_summary.md
2026-04-28 — ingest release 4T25: sources/full/weg/4T25/release.md, sources/structured/weg/4T25/release.json, sources/digested/weg_release_4T25_summary.md
2026-04-28 — ingest fato_relevante 1T25: sources/full/weg/1T25/fato_relevante_863996.md, sources/digested/weg_fatos_relevantes_batch_summary.md
2026-04-28 — ingest fato_relevante 3T25: sources/full/weg/3T25/fato_relevante_952369.md, sources/digested/weg_fatos_relevantes_batch_summary.md
2026-04-28 — ingest fato_relevante 4T25: sources/full/weg/4T25/fato_relevante_975725.md, sources/digested/weg_fatos_relevantes_batch_summary.md
2026-04-28 — ingest fato_relevante 4T25: sources/full/weg/4T25/fato_relevante_975729.md, sources/digested/weg_fatos_relevantes_batch_summary.md
2026-04-28 — ingest release unknown: sources/full/weg/other/WEGE3_4T24_dfs.md, sources/digested/weg_other_WEGE3_4T24_dfs_summary.md
2026-04-28 — ingest release unknown: sources/full/weg/other/WEGE3_4T25_dfs.md, sources/digested/weg_other_WEGE3_4T25_dfs_summary.md
[fix] 2026-04-28 | tools/ingest.sh | substituido 'rev | cut | rev' por bash parameter expansion (period=${suffix##*_}, tipo=${suffix%_*}) na linha 659. Causa: 'rev' command nao existe no git-bash do Windows (gotcha conhecido em memory). Sintoma: ingest #2 do WEG processou todos 11 itens, manifest_update rodou, mas step 6 (wiki queue) e step 7 (cleanup) abortaram com 'rev: command not found'. Resultado pre-fix: 11 PDFs+extracted ainda em undigested/ + wiki_queue nao populada.
2026-04-28 — ingest call_transcript 1T24: sources/full/weg/1T24/call_transcript.md, sources/digested/weg_call_transcript_1T24_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 1T24 | sources/digested/weg_call_transcript_1T24_summary.md
2026-04-28 — ingest call_transcript 1T25: sources/full/weg/1T25/call_transcript.md, sources/digested/weg_call_transcript_1T25_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 1T25 | sources/digested/weg_call_transcript_1T25_summary.md
2026-04-28 — ingest call_transcript 2T24: sources/full/weg/2T24/call_transcript.md, sources/digested/weg_call_transcript_2T24_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 2T24 | sources/digested/weg_call_transcript_2T24_summary.md
2026-04-28 — ingest call_transcript 2T25: sources/full/weg/2T25/call_transcript.md, sources/digested/weg_call_transcript_2T25_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 2T25 | sources/digested/weg_call_transcript_2T25_summary.md
2026-04-28 — ingest call_transcript 3T24: sources/full/weg/3T24/call_transcript.md, sources/digested/weg_call_transcript_3T24_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 3T24 | sources/digested/weg_call_transcript_3T24_summary.md
2026-04-28 — ingest call_transcript 3T25: sources/full/weg/3T25/call_transcript.md, sources/digested/weg_call_transcript_3T25_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 3T25 | sources/digested/weg_call_transcript_3T25_summary.md
2026-04-28 — ingest call_transcript 4T24: sources/full/weg/4T24/call_transcript.md, sources/digested/weg_call_transcript_4T24_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 4T24 | sources/digested/weg_call_transcript_4T24_summary.md
2026-04-28 — ingest call_transcript 4T25: sources/full/weg/4T25/call_transcript.md, sources/digested/weg_call_transcript_4T25_summary.md
[wiki-queue] 2026-04-28 | weg | call_transcript | 4T25 | sources/digested/weg_call_transcript_4T25_summary.md
[wiki-queue] 2026-04-28 | weg | itr | 1T24 | sources/digested/weg_itr_1T24_summary.md
[wiki-queue] 2026-04-28 | weg | itr | 2T24 | sources/digested/weg_itr_2T24_summary.md
[wiki-queue] 2026-04-28 | weg | itr | 3T24 | sources/digested/weg_itr_3T24_summary.md
[wiki-queue] 2026-04-28 | weg | itr | 1T25 | sources/digested/weg_itr_1T25_summary.md
[wiki-queue] 2026-04-28 | weg | itr | 2T25 | sources/digested/weg_itr_2T25_summary.md
[wiki-queue] 2026-04-28 | weg | itr | 3T25 | sources/digested/weg_itr_3T25_summary.md
[wiki-queue] 2026-04-28 | weg | dfp | 2024 | sources/digested/weg_dfp_2024_summary.md
[wiki-queue] 2026-04-28 | weg | dfp | 2025 | sources/digested/weg_dfp_2025_summary.md
[wiki-queue] 2026-04-28 | weg | release | 1T24 | sources/digested/weg_release_1T24_summary.md
[wiki-queue] 2026-04-28 | weg | release | 2T24 | sources/digested/weg_release_2T24_summary.md
[wiki-queue] 2026-04-28 | weg | release | 3T24 | sources/digested/weg_release_3T24_summary.md
[wiki-queue] 2026-04-28 | weg | release | 4T24 | sources/digested/weg_release_4T24_summary.md
[wiki-queue] 2026-04-28 | weg | release | 1T25 | sources/digested/weg_release_1T25_summary.md
[wiki-queue] 2026-04-28 | weg | release | 2T25 | sources/digested/weg_release_2T25_summary.md
[wiki-queue] 2026-04-28 | weg | release | 3T25 | sources/digested/weg_release_3T25_summary.md
[wiki-queue] 2026-04-28 | weg | release | 4T25 | sources/digested/weg_release_4T25_summary.md
[wiki-queue] 2026-04-28 | weg | dfs | 2024 | sources/digested/weg_dfs_2024_summary.md
[wiki-queue] 2026-04-28 | weg | dfs | 2025 | sources/digested/weg_dfs_2025_summary.md
[wiki-queue] 2026-04-28 | weg | fato_relevante | batch | sources/digested/weg_fatos_relevantes_batch_summary.md
[wiki-done] 2026-04-28 | weg.md | update | digesteds: weg_dfp_2024/2025, weg_dfs_2024/2025, weg_fatos_relevantes_batch, weg_itr_1T24-3T25, weg_release_1T24-4T25, weg_call_transcript_1T24-4T25 | added quarterly financial tables, segment tables, Distribuicao ao Acionista section, 2025 M&A, updated capex/guidance/posicionamento
[wiki-done] 2026-04-28 | batch_20260428_084518
[new] 2026-04-28 | calendario_resultados.md | tracker page de cobertura ativa: 37 empresas em 8 setores (Bancos 10 / Seguros 3 / Incorporadoras 6 / Locacao 6 / Industriais 4 / Saude-Fitness 3 / Bolsa 2 / Outros 3). Pre-populado wiki[[link]] (31 empresas com page existente; 6 sem) e tese (apenas cury_tese). Trimestres 4T25-4T26 com slots por empresa; ✓ marca onde release ja foi ingerido (6 empresas com manifest CVM: CURY3, CYRE3, DIRR3, PSSA3, TEND3, WEGE3). Coluna Atualizada por linha pra rastrear staleness. Index.md atualizado com nova secao Trackers.
[new] 2026-04-28 | tools/refresh_calendario.sh + tools/lib/calendario_refresh.py | automacao do calendario_resultados.md via CVM IPE_9 (Calendario de Eventos Corporativos). Pra cada ticker BR (30): query IPE_9 mais recente em janela 18 meses → download PDF → extract opendataloader → parse regex (sem LLM) datas DRE/ITR/DFP → mapeia pra colunas trimestrais (1T<YY>, 4T<YY-1>) → atualiza tabela markdown preservando edits manuais (so preenche cells vazias, bumpa Atualizada e frontmatter updated). 26/30 sucesso. Ticker overrides para 5 nao-resolvidos (BMEB4, DAYC4, ARML3, BFFT3, LCAM3, INBR32) baseado em search direto no /empresas registry. 4 sem IPE_9 (BFFT3, LCAM3, INBR32, SANB11) — proximo passo: fallback IPE_6 (Comunicado ao Mercado especie ~ Agenda de Divulgacao). Estrangeiros (XP, STLA, SIE.DE, BFIT.NA, LOMA, PICS, NU): fora do escopo, fill manual.
[edit] 2026-04-28 | README.md | adicionadas 5 secoes faltando: Fetch Calls, Fetch Notion, Ingest Calls, Refresh Calendario, Skills Interativas (/tese). Tabela Arquivos Especiais ganhou linhas: calendario_resultados.md, sources/wiki_queue.json, CLAUDE.md. Nota sobre WEG transcripts via site IR (CMS MZIQ) adicionada na secao Fetch Calls. README ainda permanece como tutorial PT-BR estavel; CLAUDE.md continua sendo o manual operacional mais detalhado.
