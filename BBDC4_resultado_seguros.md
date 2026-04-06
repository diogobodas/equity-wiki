---
type: conceito
aliases: [Seguros BBDC4, Insurance Result Bradesco]
sources:
  - BBDC4_4T25_release.pdf
  - BBDC4_planilha_RI.xlsx
  - BBDC4_dependency_graph_v3.json
  - BBDC4_modeling_manual.md
  - resultado_seguros.md
updated: 2026-04-05
source_quality: verified
---

# Resultado de Seguros — BBDC4

Decomposição aditiva do resultado de seguros do [[bradesco]] em cinco componentes operacionais do segmento de seguros, previdência e capitalização.

## Fórmula

`resultado_seguros = premios_ganhos + sinistros_retidos + sorteios_resgates + desp_comercializacao_seg + resultado_fin_seguros`

## Calibração Histórica

| Métrica | Valor |
|---------|-------|
| Tipo | Aditivo (identidade contábil) |
| Desvio máximo | 0.02% (arredondamento) |
| N trimestres | 16 (1T22–4T25) |
| Stage 2 | STRUCTURAL_BYPASS (near-identity) |

## Componentes

| Componente | Driver | Comportamento |
|------------|--------|--------------|
| **premios_ganhos** | Crescimento de carteira de seguros | Estável, cresce com base de segurados |
| **sinistros_retidos** | Sinistralidade (sinistros/prêmios) | Mais volátil, sensível a eventos climáticos e fraudes |
| **sorteios_resgates** | Capitalização e previdência | Relativamente estável |
| **desp_comercializacao_seg** | Custo de distribuição | Proporcional a novos prêmios |
| **resultado_fin_seguros** | Float da carteira de reservas × [[selic]] | Sensível a juros — reservas rendem CDI |

## Dados Históricos (R$M)

| Trimestre | Resultado Seguros | Prêmios Ganhos | Sinistros | Sorteios/Resgates | Desp. Comercialização |
|-----------|------------------|----------------|-----------|-------------------|----------------------|
| 4T24 | 5,531 | 16,972 | -10,800 | -1,592 | -1,241 |
| 1T25 | 5,303 | 17,154 | -11,072 | -1,520 | -1,218 |
| 2T25 | 5,650 | 18,099 | -11,781 | -1,647 | -1,059 |
| 3T25 | 5,706 | 19,081 | -12,485 | -1,725 | -1,274 |
| 4T25 | 5,649 | 19,373 | -13,044 | -1,563 | -1,397 |

**Tendências observadas:**
- Prêmios ganhos crescendo ~14% YoY (16.9k → 19.4k entre 4T24 e 4T25)
- Sinistralidade pressionando: sinistros crescem mais rápido que prêmios
- Resultado estável em ~R$5.5-5.7B/tri apesar do crescimento dos componentes

## Projeção no Modelo

O modelo atual projeta `resultado_seguros` como premissa flat de **R$6.0B/tri** para 2026E, sem decompor nos sub-componentes. Isso representa crescimento de ~6-8% YoY sobre 2025A (~R$22.3B anualizado → ~R$24.0B).

**Gap identificado:** Os sub-componentes (prêmios, sinistros, etc.) estão extraídos historicamente mas NÃO são projetados individualmente. A decomposição está no grafo como identidade contábil validada, mas a projeção permanece agregada. Para granularidade futura, cada componente poderia ter seu próprio driver:
- premios_ganhos: crescimento de base de segurados + ticket médio
- sinistros: combined ratio como premissa
- resultado_fin_seguros: reservas técnicas × [[selic]] implícita

## Comparação Cross-Banco

| Banco | Resultado Seguros | % do EBT | Modelo |
|-------|-------------------|----------|--------|
| [[bradesco]] | ~R$5.6B/tri (2025A) | ~25-30% | Premissa flat R$6.0B/tri |
| [[itau]] | Via [[porto_seguro]] (EP) | ~5-8% | [[equity_pickup]] exógena |
| [[sanb11]] | Zurich Santander | ~3-5% | Premissa flat menor |

O [[bradesco]] é o único grande banco brasileiro que consolida integralmente a operação de seguros no DRE gerencial, tornando esta decomposição exclusiva e de alto impacto analítico.

## Relevância para o Modelo

O [[bradesco]] é o maior grupo segurador do Brasil (via Bradesco Seguros). O [[resultado_seguros]] representa ~25-30% do resultado antes de impostos, tornando esta decomposição essencial para projeções precisas. A sensibilidade do `resultado_fin_seguros` à [[selic]] é particularmente importante: queda de juros reduz o float mas pode aumentar prêmios via maior atividade econômica.

## Fonte dos Dados

- Planilha RI BBDC4, aba "21- Oper. de Seg. Prev. Cap."
- Campos no gerencial: `breakdowns.seguros.*`
- Série histórica completa: 16 trimestres (1T22–4T25)

## Ver Também

- [[resultado_seguros]] — conceito geral (cross-banco)
- [[bradesco]] — página da empresa
- [[porto_seguro]] — comparável no setor de seguros
- [[itau]] — seguros via EP (Porto Seguro)
- [[selic]] — impacto no float de reservas técnicas
- [[banking]] — visão setorial
