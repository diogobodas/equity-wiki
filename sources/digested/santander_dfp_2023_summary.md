---
empresa: santander
ticker: SANB11
type: dfp
periodo: 2023
source_full: sources/full/santander/2023/dfp.md
source_structured: sources/structured/santander/2023/dfp.json
ingested_on: 2026-04-30
---

# Santander Brasil — DFP 2023

## Headline (gerencial)

- **Lucro líquido gerencial:** R$ 8.974 mm em 2023, queda de 28,6% vs R$ 12.570 mm em 2022 (fonte: full/santander/2023/dfp.md §Desempenho_Consolidado).
- **ROE:** 10,52% (vs 15,63% em 2022, –5,11 p.p.).
- **Ativos totais (gerencial):** R$ 1.153.196 mm (+9,98% YoY).
- **Carteira de crédito (ampliada):** R$ 427.599 mm (+3,93% YoY); destaque PF +5,3% (cartões), crédito expandido +27,7% YoY (avais, fianças, debêntures, CPR).
- **Captações totais:** R$ 849.335 mm (+14,8% YoY).
- **Basileia:** 14,51% (vs 13,94% em 2022, +0,57 p.p.).
- **JCP/Dividendos pagos no exercício:** R$ 6.200 mm (vs R$ 8.100 mm em 2022).
- **Funcionários:** 55.611 colaboradores.

## Diagnóstico do ano (palavras da administração)

Resultado pressionado por dois efeitos: (i) ciclo macro adverso — Selic acumulada elevada em 2023 prejudicou famílias e exigiu maior provisionamento; (ii) **caso específico no segmento Atacado** ("evento adverso" — referência velada a Americanas) que inflou PDD. Banco mantém estratégia iniciada no 4T21 de antecipação de ciclo de crédito, com maior seletividade em concessão para clientes melhor classificados e linhas com garantia.

## DRE consolidado (BRGAAP CVM, R$ mm)

| Linha | 2023 | 2022 |
|---|---|---|
| Receitas de Intermediação Financeira | 128.282,7 | 115.225,1 |
| Despesas de Intermediação Financeira | -81.398,7 | -67.721,9 |
| **Resultado Bruto Intermediação** | **46.884,0** | **47.503,2** |
| Receitas de tarifas/comissões | 22.454,8 | 21.237,7 |
| Despesas de pessoal | -10.813,9 | -9.897,0 |
| Outras despesas administrativas (total 3.04.04) | -43.128,7 | -37.002,8 |
| — das quais perdas com ativos financeiros (PDD) | -28.008,1 | -24.828,7 |
| Equivalência patrimonial | 239,2 | 199,2 |
| **Resultado antes IR** | **11.921,7** | **19.574,7** |
| IR e CSLL | -2.422,8 | -5.235,3 |
| **Lucro líquido consolidado (CVM)** | **9.498,8** | **14.339,5** |

Nota: a apresentação contábil consolidada CVM (3.03 + 3.04) classifica PDD dentro de "perdas com ativos financeiros líquidas" no grupo 3.04.04.05, **não** dentro das despesas de intermediação. O release/relatório da administração reagrupa em formato BACEN clássico, deslocando PDD para dentro de "Despesas de Intermediação" — por isso o "Resultado Bruto" gerencial (R$ 26.504 mm) difere do CVM (R$ 46.884 mm). Os totais convergem em "Resultado antes IR" = R$ 9.867 mm gerencial vs R$ 11.921,7 mm CVM (diferença é a participação no lucro de R$ 2.099 mm que o gerencial deduz acima da linha).

## BP consolidado (R$ mm, 31/12/2023)

| Item | 2023 | 2022 |
|---|---|---|
| Ativo total | 1.115.652,8 | 985.450,8 |
| Disponibilidades | 23.122,6 | 22.003,4 |
| Ativos financeiros (VJR) | 208.947,0 | 147.256,6 |
| Ativos financeiros (VJORA) | 59.052,1 | 55.425,7 |
| Ativos financeiros (custo amortizado) | 723.710,1 | 663.824,4 |
| Tributos | 52.839,5 | 46.446,0 |
| Outros ativos | 6.910,7 | 8.973,7 |
| Investimentos | 1.609,8 | 1.727,6 |
| Imobilizado | 7.085,6 | 8.190,8 |
| Intangível (inclui goodwill 27.852,6) | 32.375,5 | 31.602,7 |
| Passivos VJR | 49.581,4 | 49.668,3 |
| Passivos custo amortizado | 910.550,5 | 795.284,1 |
| Provisões | 11.473,8 | 9.115,1 |
| Patrimônio líquido | 114.856,4 | 110.680,2 |

Nota: o BP consolidado CVM agrega depósitos, captações no mercado aberto, recursos de aceites e obrigações por empréstimos sob "Passivos financeiros ao custo amortizado" sem subtotal por linha (release-style breakdown não disponível na DFP).

## Pontos de atenção

- **Crédito tributário diferido elevado:** R$ 43.446 mm em 2023 (+12,5% YoY), reflete reconhecimento de IR diferido pelas perdas/PDD do ano (efeito IR diferido de +R$ 6.498 mm na conciliação tributária).
- **Carteira renegociada (consolidada):** R$ 32.761 mm em 2023 (vs R$ 36.922 mm em 2022); cobertura subiu para 53,8% (de 48,9%) — provisão estágio 3 melhor capitalizada apesar do menor saldo nominal.
- **Bridge gerencial vs societário:** R$ 524 mm de diferença entre lucro gerencial (R$ 8.974) e contábil (R$ 9.499) — Santander usa o gerencial como métrica principal em todos os releases trimestrais.
- **JCP**: R$ 5.820 mm de juros sobre capital próprio + R$ 380 mm de dividendos = R$ 6.200 mm distribuídos no ano (4 tranches de JCP entre janeiro e novembro de 2023).
- **Capital social não foi alterado** (R$ 55.000 mm individual, R$ 118.421 mm consolidado); reservas de retenção de lucros cresceram para R$ 34.974 mm.

## Limitações da DFP para modelagem

DFP traz BP/DRE BRGAAP completos mas **não** detalha breakdown gerencial típico do release: (i) margem com clientes vs margem com mercado; (ii) carteira de crédito por segmento (PF/PMEs/Grandes Empresas/Atacado) com saldos em R$ mm; (iii) NPL 90+, 15-90, formation, write-off; (iv) cobertura estágio 3; (v) índice de eficiência calculado pelo banco; (vi) CET1 e RWA detalhado. Esses dados ficam no release 4T23 (não ingerido nesta sprint). Modelo deve usar release como fonte principal para qualidade de crédito e capital; DFP serve como auditoria/reconciliação.

## Auditor e governança

- Auditor: PwC, parecer sem ressalva.
- DFP aprovada pelo Conselho de Administração em 30/01/2024.
- Comitê de Auditoria estatutário (CVM) e Conselho de Administração com 36% de mulheres e 55% de membros independentes (jan/2024).
