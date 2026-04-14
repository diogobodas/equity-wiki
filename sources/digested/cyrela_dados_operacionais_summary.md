---
type: digested
source: sources/full/generic/cyrela_dados_operacionais.md
empresa: cyrela
ticker: CYRE3
created: 2026-04-13
updated: 2026-04-13
---

# Cyrela — dados operacionais (série histórica)

## O que é

Planilha proprietária com a **série histórica completa de KPIs operacionais da Cyrela** desde 2005 (anual) e quarterly de **1T06 até 4T25**. Cobre apenas Cyrela (CYRE3) — não há dados de pares. O cabeçalho marca "DADOS A PARTIR DE 2019 (PRO FORMA)", indicando que o histórico pré-2019 foi reconstruído pro forma para a estrutura societária atual.

A planilha tem versões em PT (Lçtos, Vendas, Terrenos, Canteiros, Estoque, Estoque Pronto, Entregas) e EN (Launches, Sales, Landbank, Construction Sites, Inventory, Finished Units Inventory, Deliveries) com o mesmo conteúdo — abas EN são tradução literal das PT.

## Sheets disponíveis

| Sheet | KPI | Cortes | Métrica |
|---|---|---|---|
| Lçtos / Launches | Lançamentos | Por Região, Por Segmento | VGV 100%, VGV %CBR (parte Cyrela) |
| Vendas / Sales | Vendas líquidas (VSO numerador) | Por Região, Por Segmento, **Estoque em construção** | VGV 100%, VGV %CBR |
| Terrenos / Landbank | Banco de terrenos | Por Região, (PSV) | VGV 100%, VGV %CBR |
| Canteiros / Construction Sites | Nº de canteiros ativos | Por Região, **ex-Faixa 1** | Contagem (a partir de 1T12) |
| Estoque / Inventory | Estoque a valor de mercado | Por Região | VGV Estoque 100%, %CBR |
| Estoque Pronto / Finished Units Inventory | Estoque pronto (concluído) | Por Região | VGV Estoque Pronto 100%, %CBR |
| Entregas / Deliveries | Unidades/VGV entregues | Por Região | VGV 100%, %CBR |

### Cortes

- **Por Região** (8): São Paulo, São Paulo - Interior, Rio de Janeiro, Minas Gerais, Espírito Santo, Norte, Centro Oeste, Sul, Nordeste.
- **Por Segmento** (5): Alto, Médio, Vivaz Prime, MCMV 2 e 3, MCMV 1.
- **ex-Faixa 1** (canteiros): exclui MCMV faixa 1 da contagem.
- **Estoque em construção** (vendas): split entre vendas de estoque em construção vs. lançamentos.

### Granularidade temporal

- Anual: 2005, 2006, ..., 2025.
- Trimestral: 1T06, 2T06, ..., 4T25 (≈80 trimestres).
- Cobertura completa para todas as combinações sheet × corte × período (incluindo zeros legítimos onde a operação ainda não existia).

## Por que importa para a wiki

Esta é a **fonte primária** para construir / atualizar:

1. **Página `cyrela.md`**: histórico longo de lançamentos, vendas, landbank, entregas — substitui aproximações trimestrais com série de 20 anos.
2. **VGV / VSO** (`vgv.md`, `vso.md`): permite calcular VSO histórico anualizado (vendas / (estoque inicial + lançamentos)) para Cyrela com profundidade de ciclo completo (2008–09, 2014–17, 2020–21, 2022–25).
3. **Segmentação alta-renda vs MCMV / Vivaz Prime**: a quebra Por Segmento mostra a evolução do mix Cyrela ao longo do tempo — material para análise de margem por segmento e teses de exposição cíclica.
4. **Geografia**: concentração SP/RJ vs expansão Norte/Nordeste/Sul — relevante para discussão de risco geográfico e diversificação.
5. **Banco de terrenos (Landbank)**: VGV potencial por região, base para cálculo de "anos de lançamento" implícitos.

## Limitações

- **Apenas Cyrela** — não cabe em comparações cross-company sem combinar com fontes equivalentes de Cury, Direcional, Tenda etc.
- **Sem decomposição financeira**: não há receita reconhecida (POC), margem bruta, dívida ou caixa. Para isso ver `sources/full/cyrela/{periodo}/{itr,dfp}.md`.
- **Pro forma desde 2019**: números pré-2019 podem divergir de divulgações originais (ajustados retroativamente para a estrutura societária atual da Cyrela; %CBR calibrado para a participação econômica vigente).
- **Tabelas extremamente largas** (~80 colunas por sheet): consultar via `tools/query.sh` ou leitura segmentada por período — não tentar carregar a planilha inteira.

## Referência de uso

- Para extrair número de um trimestre/região/segmento específico: `bash tools/query.sh "qual o VGV lançado pela Cyrela no segmento Alto em SP em 3T24?"`.
- Para construir tabela histórica de VSO: ler sheets Lçtos, Vendas e Estoque na mesma seção temporal.
- Backfill recomendado para `sources/structured/cyrela/`: as séries Por Região e Por Segmento (lançamentos e vendas) devem virar `company_specific.dados_operacionais.serie_historica` quando consultadas.
