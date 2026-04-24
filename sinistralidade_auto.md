---
type: concept
aliases: [Sinistralidade auto, Loss ratio auto, Índice de sinistralidade]
sources:
  - sources/full/generic/susep_sinistralidade_auto_analise_2010_2026.md
  - sources/digested/porto_previa_operacional_2T26_summary.md
  - sources/digested/porto_release_4T25_summary.md
created: 2026-04-24
updated: 2026-04-24
---

# Sinistralidade Auto

**Sinistralidade** = `Sinistro Ocorrido / Prêmio Ganho`. Métrica-chave de saúde técnica de uma seguradora auto. Compõe o [[indice_combinado]] junto com custo de aquisição (comissões) e despesas administrativas (IC = sinistralidade + comercialização + adm).

- `Sinistro Ocorrido` = pagos no período + Δ PSL (sinistros a liquidar) + Δ IBNR − recuperação de salvados/ressarcimento/resseguro
- `Prêmio Ganho` = [[premio_retido_vs_ganho|prêmio retido]] reconhecido pro-rata temporis em **dias corridos**

Benchmarks típicos de mercado auto brasileiro: patamar saudável **55%–65%**, deterioração >70%, abaixo de 50% indica cenário de repricing pós-choque (vale por um ciclo).

## Decomposição — numerador vs denominador

Como o denominador (prêmio ganho) é "dia corrido" e o numerador (sinistro) é afetado pela **exposição de trânsito** (concentrada em dia útil + clima), os dois variam com drivers diferentes. Em meses mais curtos (fev) ou com mais feriados (jun/nov), o numerador cai mais que o denominador cairia proporcional — efeito calendário.

Também impactam:
- **FIPE** (tabela de usados) — ~40% do custo de sinistro auto; queda da FIPE **reduz** indenização por perda total. Porto reporta split ~40% FIPE / 60% peças+serviços. (fonte: digested/notion_porto_seguro_porto_seguro_alexsander_update_byd_e_carro_el_trico_9e500ca3_summary.md)
- **Inflação de peças** — câmbio USD/BRL + tarifas de importados (BYD, Tesla, premium europeu); carros elétricos têm custo de bateria e peças específicas divergentes do parque tradicional.
- **Pricing cycle** — [[porto_seguro|Porto]] reporta guerra de preços iniciada no 3T23 (agressor [[allianz]]), duração típica 1–1,5 ano. Final de 2025 começou a mostrar reajustes; 2026 esperado menos competitivo.

## Sazonalidade do mercado brasileiro — SUSEP 2014-2025

**Ranking por mês (1=sinistralidade mais baixa):**

| # | Mês | Sinistr. média | Obs |
|---|-----|---|---|
| 1 | **Jun** | 0,602 | inverno, sem férias escolares no SE |
| 2 | **Abr** | 0,601 | outono estável |
| 3 | Dez | 0,616 | PSL/IBNR infla numerador mas prêmio dez cresce +5% |
| 4 | Ago | 0,615 | inverno, baixa chuva |
| 5 | Jul | 0,613 | férias de julho mas tempo seco |
| 6 | Mai | 0,619 | — |
| 7 | **Fev** | 0,618 (ex-22) | **mediano — calendário e verão se cancelam** |
| 8 | Nov | 0,628 | Black Friday + chuvas |
| 9 | Out | 0,622 | — |
| 10 | Mar | 0,623 | fim de verão, Carnaval em alguns anos |
| 11 | Set | 0,619 | primavera |
| 12 | **Jan** | 0,636 | férias, chuvas SE, prêmio ganho concentrado em renovação |

**Spread total entre mais baixo (Jun) e mais alto (Jan): 3,4pp.** Variação intra-ano é pequena comparada ao trend estrutural (ciclo 0,54 em 2023 → 0,72 em 2022 chuvas).

Média global 2014-2025: **0,619** (fonte: full/generic/susep_sinistralidade_auto_analise_2010_2026.md).

## Efeito calendário — dias úteis

Regressão OLS 2014-25 (N=144 meses): `sinistralidade ~ days_biz + days_cal + carnaval + year FE`:

- **`days_biz` coef = +0,0127 (t=+3,97)**: cada dia útil adicional no mês adiciona **+1,27pp** de sinistralidade. Com month FE (M4), o efeito sobe para **+1,78pp/dia útil**.
- `days_cal` coef = -0,0093 (t=-1,88): cada dia corrido adicional sem adicionar dia útil (fim-de-semana) REDUZ ~0,93pp. Simetria econômica: mais dia de exposição só no numerador, sem atualizar denominador correspondentemente.
- **Carnaval coef = -0,003 (t=-0,20, não significante)**: o mês ter Carnaval (ou não) não move a agulha no agregado mensal. Hipótese: lag de aviso (IBNR) distribui o spike da segunda/terça de Carnaval para março na reserva.

**Fev tem 28 dias corridos e ~20 dias úteis** vs. média mensal ~30,4 / ~21,2. O efeito favorável de dias úteis (~-1,0pp) é compensado por maior frequência de sinistro em verão (chuvas, viagens) → sinistralidade de fev fica **neutra vs média global**.

## Rolling 12M — o que importa para equity

Rolling 12M = `Σ sinistro_12m / Σ prêmio_ganho_12m`. Remove sazonalidade, revela trend estrutural.

| Período | Rolling 12M mercado |
|---|---|
| Mid-2022 (chuvas SP) | **0,72** (pico pós-covid) |
| Mid-2023 (pós-reprecificação) | **0,54** (vale) |
| Desde mid-2024 | **~0,60** (estabilização) |
| Fev 2026 | **0,596** |

Setor está em **patamar estável de ~60% há 18 meses** — 12pp abaixo do pico 2022, 6pp acima do vale 2023. Para [[bb_seguridade|BBSE]], [[caixa_seguridade|CXSE]] e [[porto_seguro|Porto]] (PSSA3), a tese é sobre **persistência desse patamar** vs inflação de FIPE/peças, não sobre leitura de mês isolado.

## Leitura de fev/2026

**Sinistralidade mercado** auto em fev/26: ~0,59 (SUSEP agregado). **NÃO é anomalia de calendário** — Fev historicamente é mês de sinistralidade mediana, ligeiramente acima da média ex-outliers. Está alinhada com o rolling 12M atual (0,596).

**Porto Seguro especificamente** em fev/26: Auto 55,2% no mês (-10,1pp a/a), 56,2% no 2M26 (-6,4pp a/a) — queda muito superior ao mercado ex-Porto (-0,1pp no mês, -1,5pp no 2M26). O gap Porto vs mercado é **outperformance específica** (mix de marcas, pricing, frota), não reflexo de calendário mais favorável a fev. (fonte: digested/porto_previa_operacional_2T26_summary.md)

## Variações do conceito

- **Sinistralidade Direta / Retida**: usa `Sinistro Retido` (antes de resseguro cedido) sobre `Prêmio Retido`. Para ramo auto brasileiro, resseguro é marginal → as duas são ~equivalentes.
- **Sinistralidade Líquida** (gerencial): inclui salvados/ressarcimento já abatidos. Porto reporta essa métrica no release (ex.: 57,7% no 4T25).
- **Sinistralidade IFRS 17**: regime novo (obrigatório 2023+) reconhece parte do sinistro no [[CSM]] e muda timing de reconhecimento. Valores IFRS 17 divergem dos IFRS 4/SUSEP — por isso Porto reporta as duas visões em DFs individuais (SUSEP IFRS 4) vs release gerencial (IFRS 17).
