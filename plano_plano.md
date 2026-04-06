---
type: empresa
source_quality: partial
aliases: [Plano e Plano, PLPL3, Plano&Plano]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/PLPL3/outputs/model/PLPL3_model.json
  - sectors/real_estate/companies/PLPL3/outputs/extraction/PLPL3_historical_financials_2023_2025.json
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/PLPL3/outputs/extraction/PLPL3_historical_operational_2023_2025.json
updated: 2026-04-05
---

# Plano & Plano

A **Plano & Plano Desenvolvimento Imobiliário** (PLPL3) é uma incorporadora brasileira focada **exclusivamente no segmento [[mcmv]]** (Minha Casa Minha Vida), atuando principalmente na Grande São Paulo. É uma das construtoras de maior crescimento no MCMV paulistano, com operação concentrada e verticalizada.

## Modelo de Negócio

Plano & Plano opera em um único segmento: **econômico MCMV Faixa 1,5–3**, com ticket médio de R$200–350k. O modelo é simples e altamente focado:

- **Produto**: apartamentos compactos, empreendimentos de alto volume (>500 unidades), terrenos periurbanos em SP
- **Subsídio MCMV**: receitas dependem da elegibilidade dos compradores ao programa federal — vulnerabilidade regulatória
- **Verticalização**: construtora e incorporadora próprias (sem terceirização), o que reduz custos mas concentra riscos operacionais
- **Geração de caixa**: ciclo curto (~18 meses de obra) favorece [[poc_revenue]] e recuperação de capital

## Financials Históricos

| Trimestre | Receita (R$M) | MB% | LL (R$M) | ML% |
|-----------|--------------|-----|----------|-----|
| 1T23 | 390 | 36.1% | 41 | 10.4% |
| 2T23 | 486 | 35.9% | 69 | 14.2% |
| 3T23 | 557 | 32.0% | 76 | 13.6% |
| 4T23 | 640 | 32.8% | 83 | 13.0% |
| 1T24 | 501 | 33.3% | 41 | 8.3% |
| 2T24 | 698 | 32.9% | 95 | 13.7% |
| 3T24 | 719 | 33.1% | 119 | 16.6% |
| 4T24 | 672 | 33.1% | 88 | 13.0% |
| 1T25 | 608 | 32.8% | 67 | 11.0% |
| 2T25 | 784 | 33.6% | 84 | 10.7% |
| 3T25 | 814 | 30.5% | 78 | 9.6% |
| 4T25 | 1,075 | 28.8% | 133 | 12.4% |

**Tendências:** Receita com crescimento acelerado desde 2023 (+175% em 3 anos). [[margem_backlog|Margem bruta]] contraindo de ~36% (2023) para ~29-33% (2024-2025) — reflexo de mix de backlog e curva de aprendizado construtivo.

## Projeções do Modelo (26E/27E)

| Ano | Receita (R$M) | MB% | LL (R$M) | ML% | ROE |
|-----|--------------|-----|----------|-----|-----|
| 26E | 4,393 | 31.4% | 618 | 14.1% | 44.7% |
| 27E | 4,583 | 31.4% | 591 | 12.9% | 37.2% |

**Premissas-chave 26E:**
- [[vgv_lancamentos]]: ~R$1,150M/tri (normalização vs 2025 recorde de ~R$5.3B/ano)
- [[margem_backlog]]: 31.4% (mediana histórica 2024-2025)
- Crescimento receita 26E: +33.9% vs 2025A — reflete backlog robusto acumulado

## Drivers Fundamentais

### 1. VGV Lançamentos
Principal driver de crescimento. Plano & Plano lançou ~R$5.3B em 2025 (recorde). Para 2026, modelo usa ~R$4.6B (normalização). O volume é sensível ao programa MCMV — variações de elegibilidade de renda ou limites de subsídio afetam diretamente a demanda.

### 2. Velocidade de Vendas ([[velocidade_vendas]])
VSO (Vendas Sobre Oferta) historicamente alto no MCMV em SP — demanda estrutural supera oferta. Favorece conversão rápida de lançamentos em backlog.

### 3. Margem Bruta
Comprimida pela inflação de insumos (INCC) e mix de empreendimentos. MCMV não tem correção de preço durante a obra — risco de compressão se INCC acelerar acima do previsto. Target ~31-33%.

### 4. Resultado Financeiro
Dívida usada para capital de giro em obras. Com Selic em 14.25%+, custo financeiro é relevante (~R$30-40M/tri). Pressiona ML abaixo de MB em ~2pp.

## Posicionamento Competitivo

| Aspecto | Plano & Plano | [[direcional]] | [[tenda]] | [[cury]] |
|---------|--------------|---------------|----------|---------|
| Foco | MCMV exclusivo | MCMV+Médio | MCMV (Tenda+Alea) | MCMV exclusivo |
| Mercado | SP (periferia GR SP) | Nacional | SP+RJ+NE | SP (GR SP) |
| ROE | ~35-45% | ~30-40% | ~15-20% | ~40-50% |
| Escala | Média (R$4-5B VGV) | Maior (R$7-9B VGV) | Média | Média |

**Diferencial vs [[cury]]:** Ambas são MCMV em SP, mas Cury tem parceria com [[cyrela]] (Cury é a joint venture). Plano & Plano é mais pura e menor. Cury tem maior visibilidade com investidores por ser filha da Cyrela.

## Riscos

1. **Concentração em MCMV**: qualquer mudança no programa federal afeta toda a receita
2. **Concentração geográfica (SP)**: sem diversificação regional para amortecer ciclos locais
3. **Margem comprimida**: INCC sem reajuste de preço durante obra — risco em cenário de alta de custos
4. **ROE elevado depende de alavancagem**: PL pequeno vs escala de lançamentos; endividamento alto para capital de giro
5. **Liquidez da ação**: PLPL3 tem free float e volume baixos vs peers maiores

## Para o Modelo

- Modelo: `sectors/real_estate/companies/PLPL3/outputs/model/PLPL3_model.json`
- Estrutura: único segmento `economico_mcmv` (sem EP investidas, sem segmentos)
- Premissa-chave: [[vgv_lancamentos]] trimestral, [[margem_backlog]] fixada
- Backlog: `outputs/extraction/PLPL3_backlog_trimestral.json`
- Analyst Review: WARN (receita 26E +33.9% justificado por backlog recorde 2025)

## Ver Também

- [[mcmv]] — programa habitacional base do modelo de negócio
- [[cury]] — concorrente direto, também MCMV em SP
- [[direcional]] — maior player MCMV, nacional
- [[tenda]] — outra MCMV com segmento Alea
- [[poc_revenue]] — método de reconhecimento de receita (% de conclusão)
- [[margem_backlog]] — driver de margem bruta
- [[vgv_lancamentos]] — principal driver de crescimento
- [[incorporadoras]] — setor real estate, visão geral
