---
type: generic
title: Análise sazonalidade sinistralidade auto mercado brasileiro — SUSEP 2010-2026
source_primary: SUSEP Estatísticas (resp_premiosesinistros.aspx)
source_export: "C:/Users/diogo.bodas/Downloads/Exporta (1).xls (parsed 2026-04-24)"
source_url_origem: https://www2.susep.gov.br/menuestatistica/ses/principal.aspx
ramos: [0520, 0523, 0524, 0525, 0526, 0531, 0542, 0544, 0553]
periodo: 201001–202602
observacoes_mensais: 194
empresas: todas (mercado agregado)
confiabilidade: oficial
created: 2026-04-24
scripts:
  - analises/sinistralidade_auto/analise.py
  - analises/sinistralidade_auto/addendum.py
  - analises/sinistralidade_auto/grafico.py
---

# Sinistralidade Auto Mercado — Análise Sazonalidade SUSEP 2010–2026

## Fonte dos dados

Export da tela **"Prêmios e Sinistros"** do sistema SUSEP Estatísticas, ramos auto consolidados (0520 Casco, 0523 RC voluntária, 0524 APP, 0525 RCF-DC, 0526 RCF-DM, 0531 Carta Verde, 0542 RC Transportes, 0544 RC Veíc. terrestres não auto, 0553 Assistência 24h). **"Todas"** empresas; 194 observações mensais de jan/2010 a fev/2026.

Colunas relevantes: `Prêmio Emitido`, `Prêmio Retido`, `Prêmio Ganho`, `Sinistro Retido`, `Sinistro Ocorrido`, `Sinistralidade`.

**Nota sobre regime contábil:** a coluna `Sinistro Ocorrido` só é populada de 2014 em diante (mudança IFRS 4 na SUSEP). Antes de 2014 a coluna `Sinistralidade` oficial usava `Sinistro Retido / Prêmio Ganho`. Para a análise ano-a-ano usamos a coluna `Sinistralidade` SUSEP (consistente em todo histórico); para decomposição numerador/denominador limitamos a **2014-2025**.

## Metodologia

1. Sazonalidade descritiva por mês (média, mediana, desvio, ranking) sobre 2014-2025.
2. Decomposição numerador (Sinistro Ocorrido) × denominador (Prêmio Ganho) normalizados pela média anual, para isolar efeito calendário do efeito pricing/trend.
3. Calendário brasileiro: `days_calendar` (dias corridos), `days_biz` (dias úteis BR excluindo feriados nacionais via pacote `holidays`), `has_carnaval` (dummy para mês que contém a terça de Carnaval via `dateutil.easter`).
4. Regressão OLS (numpy lstsq) da sinistralidade mensal contra: dias úteis, dias corridos, dummy Carnaval, fixed effects de mês e ano.
5. Rolling 12M sinistralidade = Σ sinistro_ocorrido_12m / Σ prêmio_ganho_12m — remove sazonalidade, mostra trend estrutural.

## Resultado 1 — Sinistralidade média por mês (2014-2025)

| Mês | Média | Mediana | Desvio | Ranking (1=mais baixo) |
|-----|-------|---------|--------|--------|
| Jan | 0,6358 | 0,635 | 0,038 | 12º |
| Fev | 0,6283 | 0,620 | 0,041 | 7º (neutro) |
| Mar | 0,6233 | 0,615 | 0,066 | 10º |
| Abr | 0,6008 | 0,615 | 0,071 | 2º mais baixo |
| Mai | 0,6192 | 0,615 | 0,081 | 6º |
| Jun | **0,6017** | 0,595 | 0,060 | **1º mais baixo** |
| Jul | 0,6125 | 0,625 | 0,047 | 5º |
| Ago | 0,6150 | 0,605 | 0,052 | 4º |
| Set | 0,6192 | 0,610 | 0,038 | 7º |
| Out | 0,6225 | 0,630 | 0,041 | 9º |
| Nov | 0,6283 | 0,615 | 0,052 | 8º |
| Dez | 0,6158 | 0,605 | 0,048 | 3º |

**Média global 2014-2025: 0,6185.** Spread total entre mês mais alto (Jan 0,636) e mais baixo (Jun 0,602) = apenas 3,5pp. Meses de verão (jan-mar) concentrados no topo; inverno (jun-ago) no fundo.

Fev está em **posição mediana** (7º de 12) — **não é estruturalmente baixa**.

## Resultado 2 — Gap Fev vs outros meses (ex-outlier 2022)

| | Com Fev/22 (chuvas SP) | Ex Fev/22 |
|---|---|---|
| Fev mean (2014-25) | 0,6283 | **0,6182** |
| Outros meses mean | 0,6177 | 0,6177 |
| Gap Fev − outros | +1,07pp | **+0,05pp ≈ zero** |

Fev 2022 teve sinistralidade de 0,7388 (chuvas extremas no Sudeste). Excluindo esse outlier, Fev está **essencialmente em cima da média global** — calendário não produz um "Fev estruturalmente baixo" como intuição sugere.

## Resultado 3 — Decomposição numerador/denominador (normalizado por ano)

| Mês | Prêmio Ganho (idx) | Sinistro Ocorrido (idx) | Dias cal. | Dias úteis |
|-----|---|---|---|---|
| Jan | 0,99 | 1,02 | 31,0 | 21,5 |
| **Fev** | **0,91** | **0,93** | **28,2** | **20,2** |
| Mar | 1,00 | 1,01 | 31,0 | 21,8 |
| Abr | 0,97 | 0,94 | 30,0 | 19,9 |
| Mai | 1,01 | 1,01 | 31,0 | 21,4 |
| Jun | 0,98 | 0,95 | 30,0 | 21,4 |
| Jul | 1,02 | 1,01 | 31,0 | 22,2 |
| Ago | 1,02 | 1,02 | 31,0 | 22,1 |
| Set | 1,00 | 1,00 | 30,0 | 20,8 |
| Out | 1,04 | 1,04 | 31,0 | 21,5 |
| Nov | 1,01 | 1,03 | 30,0 | 19,8 |
| Dez | 1,05 | 1,05 | 31,0 | 21,4 |

Em fev, prêmio ganho cai ~9% vs média anual (efeito 28 dias) e sinistro ocorrido cai ~7%. A queda do numerador é **menor** que a queda do denominador → sinistralidade ligeiramente **acima** da média, não abaixo.

## Resultado 4 — Regressões OLS

| Modelo | Regressores | R² | Coef `days_biz` (t) | Coef carnaval (t) |
|---|---|---|---|---|
| M1 | month FE + year FE | 0,529 | — | — |
| M2 | days_biz + days_cal + carnaval + year FE | 0,550 | +0,01266 (t=+3,97) | -0,00258 (t=-0,20) |
| M3 | days_biz + year FE | 0,536 | +0,00944 (t=+3,41) | — |
| M4 | days_biz + month FE + year FE | 0,610 | +0,01784 (t=+4,97) | — |

**Interpretação:**

- **`days_biz` é significante e positivo**: cada dia útil adicional no mês adiciona **~+0,94 a +1,78pp** de sinistralidade (dependendo do controle). Mês com mais dias úteis = mais exposição a sinistro que não é compensada proporcionalmente pelo prêmio ganho adicional (que escala por dias corridos).
- **Carnaval-em-fev tem efeito nulo** (t=-0,20). Mesmo com mais viagens e exposição, o agregado mensal não mostra sinal estatístico. Lag de aviso (IBNR) pode estar distribuindo o sinistro para março.
- Em M4 (com month FE), o coeficiente de `days_biz` SOBE para +1,78pp — indicando que dummies de mês estavam absorvendo parte do efeito dias úteis. A sazonalidade de mês e dias úteis estão correlacionadas (Fev e Nov têm menos dias úteis), mas são efeitos separáveis.

## Resultado 5 — Fevereiro série anual

| Ano | Prêmio Ganho (R$ mm) | Sinistro Ocorr. (R$ mm) | Sinistr. | Dias úteis | Carnaval/mês |
|-----|----|----|----|----|-----|
| 2014 | 2.296 | 1.493 | 0,650 | 20 | não |
| 2015 | 2.495 | 1.500 | 0,601 | 20 | sim |
| 2016 | 2.604 | 1.663 | 0,639 | 21 | sim |
| 2017 | 2.505 | 1.612 | 0,644 | 20 | sim |
| 2018 | 2.629 | 1.640 | 0,624 | 20 | sim |
| 2019 | 2.759 | 1.680 | 0,609 | 20 | não |
| 2020 | 2.854 | 1.790 | 0,627 | 20 | sim |
| 2021 | 2.771 | 1.646 | 0,594 | 20 | sim |
| 2022 | 3.010 | **2.224** | **0,739** | 20 | não |
| 2023 | 4.024 | 2.479 | 0,616 | 20 | sim |
| 2024 | 4.429 | 2.558 | 0,578 | 21 | sim |
| 2025 | 4.460 | 2.758 | 0,618 | 20 | não |
| **2026** | **4.737** | **2.797** | **0,590** | **20** | **sim** |

- Fev 2026 = **0,590** — 2º Fev mais baixo em 13 anos (menor apenas Fev 2024 = 0,578)
- Média Fev hist (2014-25, ex-22): 0,6182 — Fev 2026 está a **-2,8pp** dessa média, z-score ~-0,7
- Não é estatisticamente extremo, mas é clara leitura positiva

## Resultado 6 — Rolling 12M (trend estrutural)

| Data | Mensal | Rolling 12M |
|------|--------|-------------|
| mar/23 | — | 0,54 (mínimo pós-covid) |
| mai/24 | 0,72 (spike chuvas) | 0,58 |
| dez/24 | 0,58 | 0,59 |
| fev/25 | 0,62 | 0,60 |
| ago/25 | 0,57 | 0,59 |
| dez/25 | 0,62 | 0,60 |
| jan/26 | 0,61 | 0,60 |
| **fev/26** | **0,59** | **0,596** |

**Pico covid/chuvas: ~0,72 em meados 2022.** Vale pós-reprecificação: 0,54 em meados 2023. **Estabilização em ~0,60 desde 18 meses.** Fev 2026 (0,59 mensal) está alinhado com o rolling 12M (0,60) — **confirma patamar estrutural, não é um blip favorável**.

## Conclusão

1. Efeito calendário (dias úteis) **existe e é estatisticamente significante** (~+0,94 a +1,78pp por dia útil adicional), direção: mais dias úteis → mais sinistralidade.
2. Fev NÃO é estruturalmente baixa — ex-outlier 2022, está exatamente na média global do mercado.
3. Fev 2026 em 0,59 (mercado) é bom número, mas **alinhado com rolling 12M** — não é anomalia de calendário, é patamar estável do setor pós-reprecificação 2023-24.
4. Carnaval em fev: efeito estatisticamente nulo.
5. Para tese de equity em seguradoras auto (BBSE, CXSE, Porto/PSSA3), a métrica relevante é rolling 12M, não o ponto mensal isolado.

## Scripts de reprodução

`analises/sinistralidade_auto/analise.py` — principal (descritiva + regressões)  
`analises/sinistralidade_auto/addendum.py` — ex-outlier + rolling 12M + gráficos  
`analises/sinistralidade_auto/grafico.py` — gráficos sazonal

CSVs: `dados_mensais.csv`, `sazonalidade_mensal.csv`, `decomposicao_num_den.csv`, `fevereiro_ano_a_ano.csv`, `rolling_12m.csv`
