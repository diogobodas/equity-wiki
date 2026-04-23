---
type: digest
empresa: porto
ticker: PSSA3
periodo: 1T25
tipo_documento: itr
source: sources/full/porto/1T25/itr.md
structured: sources/structured/porto/1T25/itr.json
created: 2026-04-22
---

# Porto Seguro — ITR 1T25 (Resumo)

**Nota de schema:** Porto Seguro é holding seguradora/financeira (setor=seguradora no manifest), mas o pipeline `ingest.sh` mapeou com schema `incorporadora/v1`. As linhas IFRS comparáveis (receita, despesas operacionais, resultado financeiro, IR, lucro líquido, BP) foram preservadas em `canonical.dre`/`canonical.bp`; todas as métricas específicas de seguro (prêmios, sinistralidade, índice combinado, ROAE, segmentação em Seguro/Saúde/Bank/Serviço, carteira de investimentos, guidance) estão em `company_specific`. Ver `_schema_mismatch_note` no JSON. (fonte: full/porto/1T25/itr.md §DFs Consolidadas)

## Destaques 1T25

- **Receita total gerencial:** R$ 9,9 bi (+14,6% a/a), maior receita recorrente da história. (fonte: full/porto/1T25/itr.md §p.23)
- **Lucro líquido:** R$ 832,3 mi (+27,8% a/a), recorrente igual ao reportado (sem eventos extraordinários). (fonte: full/porto/1T25/itr.md §p.23)
- **ROAE:** 23,9% (+3,0 p.p. a/a) — todas as quatro verticais acima de 22% de rentabilidade. (fonte: full/porto/1T25/itr.md §p.22)
- **Índice de eficiência operacional** (G&A / Receita Total): 10,9% (-0,5 p.p.). (fonte: full/porto/1T25/itr.md §p.23)
- **Clientes:** 18,1 mi (+6,4% a/a); App Porto com 4 mi de usuários (+20%). (fonte: full/porto/1T25/itr.md §p.22)

## Contribuição por vertical (ex-Demais)

| Vertical | Receita (R$ mi) | LL (R$ mi) | Δ LL a/a | ROAE | % do LL consolidado |
|---|---|---|---|---|---|
| Seguro | 5.408,1 | 313,4 | -21,4% | 22,6% | 42% (57% no 1T24) |
| Saúde | 1.964,6 | 179,6 | +70,6% | 39,7% | 24% (15% no 1T24) |
| Bank | 1.732,4 | 192,1 | +29,2% | 27,0% | 26% (21% no 1T24) |
| Serviço | 669,7 | 53,6 | +19,1% | 26,3% | 7% (6% no 1T24) |

**Leitura:** narrativa de diversificação confirmada — Seguro cai de 57% para 42% do lucro, Saúde e Bank ganham peso. Recorrência do resultado vem da combinação das quatro verticais, não mais do Auto isolado. (fonte: full/porto/1T25/itr.md §p.21)

## Seguro — sinistralidade pressionada sazonalmente

- **Auto:** prêmios emitidos R$ 3.985,3 mi (+4,5%), frota 6,17 mi veículos (+2,4%), participação 28,2% em 2M25, sinistralidade 60,1% (+3,9 p.p.). Piora atribuída a frequência levemente maior e a base fraca no 1T24 — management mantém guidance. (fonte: full/porto/1T25/itr.md §p.26, §p.27)
- **Patrimonial:** prêmios +10,1%, itens +22,8%, sinistralidade 35,4% (-0,6 p.p.).
- **Vida:** prêmios +15,8%, vidas +25,0%, sinistralidade 39,1% (+4,7 p.p.).
- **Índice combinado vertical:** 92,7% (+3,8 p.p.); Combinado Ampliado 89,4% (+3,6 p.p.).

## Saúde — tração operacional

- Seguro Saúde 702 mil vidas (+24,7%), Odonto 1.032 mil (+27,2%); 18 trimestres consecutivos de crescimento em Saúde.
- Sinistralidade Seguro Saúde: 70,8% (-1,9 p.p. a/a) — verticalização virtual + combate a fraudes.
- Ajuste de diferimento de comissões (estudo atuarial de Set/24) gerou +2,3 p.p. em despesas de comercialização no 1T25 (R$ 42,1 mi em despesa ou R$ 19,3 mi em LL). (fonte: full/porto/1T25/itr.md §p.32)
- IC 83,6% (-4,3 p.p.); lucro R$ 179,6 mi (+70,6%); ROAE 39,7%.

## Bank — crédito com qualidade em alta

- Carteira média sensível a spread R$ 17.425 mi (+16,8%); cartões 3,56 mi unidades (+13,9%); consórcio 415,7 mil negócios ativos (+32,3%).
- **Inadimplência 90d+ recuou para 6,0%** (-0,5 p.p. a/a; -0,1 p.p. t/t ex-venda de carteira 4T24). (fonte: full/porto/1T25/itr.md §p.22)
- PCLD/carteira 360d: 8,3% (flat a/a); 540d: 9,8% (-1,5 p.p.).
- Previdência migrou de Seguro para Bank a partir do 1T25.

## Resultado financeiro e carteira

- **Resultado financeiro consolidado:** R$ 382,6 mi (+68% a/a). Receita da tesouraria R$ 432,7 mi a 99,4% do CDI; IBOV alto no trimestre com leve impacto negativo da renda variável. (fonte: full/porto/1T25/itr.md §p.46)
- **Carteira de investimentos total:** R$ 21,1 bi (R$ 15,1 bi ex-previdência, rendendo 2,87% ou 96,1% do CDI no trimestre).
- Alocação 1T25: Juro real 41%, juro nominal 31%, crédito pós 19%, ações 3%, outros 6%.

## Consolidado IFRS (DFs)

- Receita Venda Bens/Serviços R$ 9.705,9 mi (1T24: R$ 8.669,7 mi) — dentro inclui Receita de seguro R$ 7.708,6 mi, prestação serviços R$ 872,8 mi, operações de crédito R$ 1.098,1 mi. (fonte: full/porto/1T25/itr.md §DFs Consolidadas / Demonstração do Resultado)
- Lucro líquido consolidado R$ 845,4 mi (controladora R$ 832,3 mi + minoritários R$ 13,2 mi).
- Ativo total R$ 49,5 bi (+3,2% t/t). PL total R$ 13,9 bi (-1,7% t/t — refletindo dividendos adicionais propostos de R$ 559,3 mi e recompras de R$ 193,0 mi).
- Dividendos/JCP a pagar no circulante: R$ 1.400,8 mi.

## Guidance 2025 — mantido

| Vertical | Métrica | Range |
|---|---|---|
| Seguro | Var Prêmio Ganho | +2% a +5% |
| Seguro | Sinistralidade | 51% a 55% |
| Saúde | Var Prêmio Ganho | +25% a +40% |
| Saúde | Sinistralidade | 75% a 80% |
| Bank | Var Receita Total | +14% a +22% |
| Bank | Índice Eficiência | 32,5% a 35% |
| Serviço | Receita Total | R$ 2,5 a 2,8 bi |
| Consolidado | Resultado Financeiro | R$ 1,2 a 1,4 bi |
| Consolidado | Taxa Efetiva IR | 30% a 34% |

(fonte: full/porto/1T25/itr.md §p.47)

## Itens para follow-up

- Sinistralidade Auto e Vida pioraram; monitorar 2T25 para confirmar tese de sazonalidade vs. tendência.
- Saúde crescendo 35% em receita com IC de 83,6% — sustentabilidade da sinistralidade sob a tese de "verticalização virtual" é o ponto-chave para extrapolar o ROAE de 39,7%.
- Capital regulatório (PLA, necessidade, suficiência) reportado em gráfico fragmentado pelo OCR — dados brutos requerem consulta ao release original antes de serem incorporados ao modelo.
- Ajuste não recorrente IFRS 17 foi apenas +R$ 12,3 mi no 1T25 — pequeno, mas precisa ser tratado como recorrente vs. ex-IFRS 17 conforme a abordagem do modelo.
