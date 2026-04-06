---
type: conceito
aliases: [OPEX BBDC4, Despesas Operacionais Bradesco]
sources:
  - BBDC4_4T25_release.pdf
  - BBDC4_planilha_RI.xlsx
  - BBDC4_dependency_graph_v3.json
  - BBDC4_modeling_manual.md
  - eficiencia_operacional.md
updated: 2026-04-05
source_quality: verified
---

# OPEX (Despesas Operacionais) — BBDC4

Decomposição aditiva das despesas operacionais do [[bradesco]] em três componentes, excluindo despesas tributárias.

## Fórmula

`opex = desp_pessoal + outras_desp_admin + outras_op`

**Nota:** `desp_tributarias` (ISS, PIS, COFINS) é reportada separadamente no gerencial BBDC4 e NÃO integra o opex neste conceito.

## Calibração Histórica

| Métrica | Valor |
|---------|-------|
| Tipo | Aditivo (identidade contábil) |
| Desvio máximo | 0.00% (identidade perfeita) |
| N trimestres | 16 (1T22–4T25) |
| Stage 2 | STRUCTURAL_BYPASS (near-identity) |

## Componentes

| Componente | Conceito | Driver |
|------------|----------|--------|
| **desp_pessoal** | Salários, benefícios, encargos | Headcount × custo médio, reajuste por dissídio |
| **outras_desp_admin** | TI, aluguéis, depreciação, terceiros | [[indice_eficiencia]] como target |
| **outras_op** | Provisões não-crédito, outros | Mais volátil, inclui reestruturações |

## Fronteira com desp_tributarias

| Campo | No opex? | Conceito |
|-------|----------|----------|
| desp_pessoal | Sim | Custo estrutural de pessoal |
| outras_desp_admin | Sim | Custo estrutural admin |
| outras_op | Sim | Outras despesas operacionais |
| desp_tributarias | **NÃO** | Imposto sobre receita (ISS/PIS/COFINS) |

Esta distinção é específica do [[bradesco]] — o [[itau]] reporta opex de forma diferente. O `analyst_review` usa **core IE** (sem outras_op) para o check de [[indice_eficiencia]] do BBDC4, porque o guidance do banco se refere ao índice de eficiência core.

## Dados Históricos (R$M)

| Trimestre | OPEX Total | Desp. Pessoal | Outras Desp. Admin | Outras Op |
|-----------|-----------|---------------|-------------------|-----------|
| 4T24 | -16,418 | -6,773 | -6,315 | -3,330 |
| 1T25 | -15,006 | -6,705 | -5,265 | -3,036 |
| 2T25 | -15,898 | -6,852 | -5,639 | -3,407 |
| 3T25 | -16,488 | -7,126 | -5,778 | -3,584 |
| 4T25 | -16,958 | -7,308 | -6,517 | -3,133 |

**Composição média 2025A:**
- Desp. pessoal: ~43% do opex (salários, encargos, PLR)
- Outras desp. admin: ~36% (TI, aluguéis, depreciação, terceiros)
- Outras op: ~21% (provisões não-crédito, reestruturações)

## Projeção no Modelo

O modelo projeta opex core (desp_pessoal + outras_desp_admin) via [[indice_eficiencia]] aplicado à receita total, e `outras_op` como premissa flat de **R$3.3B/tri**.

| Trimestre | OPEX (core+outras_op) | Outras Op |
|-----------|----------------------|-----------|
| 1T26E | -13,796 | -3,300 |
| 2T26E | -14,196 | -3,300 |
| 3T26E | -14,447 | -3,300 |
| 4T26E | -14,880 | -3,300 |

**Nota sobre IE core vs total:** O guidance do BBDC4 se refere ao índice de eficiência **core** (desp_pessoal + outras_desp_admin como % da receita líquida). O modelo usa IE core de ~38.5% como input, e `outras_op` é adicionada separadamente. O `analyst_review` valida IE core (não total) para evitar falso WARN.

## Comparação Cross-Banco

| Banco | IE Core | IE Total | Desp. Pessoal / Opex |
|-------|---------|----------|---------------------|
| [[bradesco]] | ~38.5% (2026E) | ~47% incluindo outras_op | ~43% |
| [[itau]] | ~38.9% (2025A) | ~39% (opex já inclui tudo) | ~50% |
| [[sanb11]] | ~38-40% | ~40% | ~45% |

O [[bradesco]] é o único grande banco que reporta `outras_op` como linha separada no gerencial, o que exige atenção na comparação de IE entre bancos. Sem essa distinção, o BBDC4 pareceria ter IE de ~47% (muito pior que [[itau]]), quando na realidade o core é competitivo.

## Relevância para o Modelo

O opex total é ~R$15-16B/tri para o BBDC4. A decomposição permite projetar o custo de pessoal (maior componente, ~43%) separadamente das despesas administrativas e outras despesas operacionais, capturando ganhos de [[eficiencia_operacional]] de forma granular. A separação de `outras_op` é crítica para o check de [[indice_eficiencia]] no `analyst_review`.

## Ver Também

- [[eficiencia_operacional]] — conceito de eficiência bancária
- [[indice_eficiencia]] — métrica IE core vs total
- [[bradesco]] — página da empresa
- [[itau]] — comparável (IE benchmark)
- [[sanb11]] — comparável
- [[plr_bancario]] — componente de desp_pessoal
- [[banking]] — visão setorial
