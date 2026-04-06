---
type: conceito
aliases: [NII Total BBDC4, Receita Financeira Bradesco]
sources:
  - BBDC4_4T25_release.pdf
  - BBDC4_planilha_RI.xlsx
  - BBDC4_dependency_graph_v3.json
  - BBDC4_modeling_manual.md
  - nii_clientes.md
updated: 2026-04-05
source_quality: verified
---

# NII Total — BBDC4

Decomposição aditiva do NII (Net Interest Income) do [[bradesco]] em dois componentes com drivers distintos.

## Fórmula

`nii_total = nii_clientes + nii_mercado`

## Calibração Histórica

| Métrica | Valor |
|---------|-------|
| Tipo | Aditivo (identidade contábil) |
| Desvio máximo | 0.01% (arredondamento) |
| N trimestres | 16 (1T22–4T25) |
| Stage 2 | STRUCTURAL_BYPASS (near-identity) |

## Componentes

- **[[nii_clientes]]**: spread sobre [[carteira_credito]] e depósitos. Driver principal: volume de carteira × [[nim]] de clientes. Mais previsível, crescimento gradual.
- **[[nii_mercado]]**: resultado de TVM, derivativos e posições proprietárias. Mais volátil, sensível ao cenário macro e à curva de juros ([[selic]]).

## Como o Modelo Projeta

| Componente | Método de Projeção |
|------------|-------------------|
| nii_clientes | `saldo_medio_carteira × NIM_clientes` — [[spread_clientes]] como driver |
| nii_mercado | Premissa absoluta (R$M/tri) — [[nii_mercado]] é volátil demais para modelar por fórmula |

## Dados Históricos e Projeção (R$M)

| Trimestre | NII Clientes | NII Mercado | NII Total | Mix Mercado % |
|-----------|-------------|-------------|-----------|---------------|
| 4T24 | 16,153 | 842 | 16,995 | 5.0% |
| 1T25 | 16,771 | 462 | 17,233 | 2.7% |
| 2T25 | 17,756 | 288 | 18,044 | 1.6% |
| 3T25 | 18,611 | 99 | 18,710 | 0.5% |
| 4T25 | 19,119 | 126 | 19,245 | 0.7% |
| **1T26E** | 19,383 | 250 | 19,633 | 1.3% |
| **2T26E** | 19,871 | 250 | 20,121 | 1.2% |
| **3T26E** | 20,205 | 250 | 20,455 | 1.2% |
| **4T26E** | 20,833 | 250 | 21,083 | 1.2% |

**Tendências:**
- NII clientes cresce ~18% YoY (16.2k → 19.1k entre 4T24 e 4T25) — impulsionado por crescimento de [[carteira_credito]] (~9.5% a.a.) + [[spread_clientes]] estável
- NII mercado comprimido em 2025 (842 → 126): ambiente de juros altos e curva invertida prejudica posições proprietárias. Modelo normaliza para R$250M/tri em 2026E
- Mix mercado caiu de ~5% para <1% — BBDC4 se tornou quase 100% NII clientes em 2025

## Comparação Cross-Banco

| Banco | NII Total (4T25) | Mix Mercado | Método de Projeção NII Mercado |
|-------|-----------------|-------------|-------------------------------|
| [[bradesco]] | R$19.2B | ~1% | Premissa absoluta (R$250M/tri) |
| [[itau]] | ~R$28B | ~8-12% | Premissa como % do NII total |
| [[sanb11]] | ~R$14B | ~5-8% | Premissa absoluta |

O BBDC4 é o banco mais sensível a NII mercado entre os grandes bancos brasileiros — historicamente representava ~10-15% do NII total, mas comprimiu em 2024-2025. A normalização para R$250M/tri em 2026E é conservadora (vs ~R$2-3B/tri no ciclo Selic baixo de 2020-2021).

## Sensibilidade a Cenários de [[selic]]

O NII mercado do [[bradesco]] é particularmente sensível à curva de juros:
- **Selic alta + curva flat/invertida** (cenário 2025): NII mercado comprimido, posições proprietárias perdem valor
- **Selic em queda + curva positiva** (cenário normalizado): NII mercado se recupera, TVM se valorizam, derivativos de taxa ganham
- **Selic estável**: NII mercado se estabiliza em nível normalizado (~R$250-500M/tri)

O modelo projeta NII mercado como premissa flat (não modelada por fórmula) exatamente por essa volatilidade — tentar decompor em TVM/derivativos/CDI seria pseudo-precisão.

## Relevância para o Modelo

Esta decomposição é crítica para capturar o mix de receita do BBDC4. O [[bradesco]] tem historicamente maior dependência de [[nii_mercado]] que o [[itau]], o que gera mais volatilidade trimestral no NII total. A projeção separada permite sensibilidade a cenários de [[selic]] no nii_mercado sem contaminar o nii_clientes.

## Ver Também

- [[nii_clientes]] — componente de spread
- [[nii_mercado]] — componente de tesouraria
- [[nim]] — margem financeira como %
- [[spread_clientes]] — driver do NII clientes
- [[carteira_credito]] — volume que gera NII clientes
- [[selic]] — macro driver do NII mercado
- [[crescimento_carteira]] — crescimento que impulsiona NII clientes
- [[banking]] — visão setorial
- [[bradesco]] — página da empresa
- [[itau]] — benchmark de mix NII
