---
type: analysis
empresa: smart
ticker: SMFT3
escopo: KPIs operacionais Smart Fit Brasil próprias + estimativa 1T26
created: 2026-05-01
sources:
  - sources/full/smart/totalpass_mau_brasil_mensal.md
  - sources/full/smart/{1T23,2T23,...,4T25}/release.md
  - sources/full/smart/{1T23,...,4T25}/itr.md
  - analises/smartfit_kpis_1T26_estimate.xlsx
---

# Smart Fit Brasil próprias — KPIs operacionais + estimativa 1T26

Análise de KPIs trimestrais Smart Fit Brasil próprias 1T23-4T25 + estimativa 1T26 antes do release. Métricas: Receita/Loja anualizada, Ticket médio mensal, Alunos/loja média; mais derivações ajustadas por TotalPass (Alunos/loja c/TP, Ticket ex-TP).

## Metodologia

### Inputs por trimestre (do release/ITR/DFP)

1. **Receita Smart Fit Brasil próprias** (R$ mm) — narrativa: "No Brasil, a receita líquida das academias Smart Fit foi de R$ X milhões"
2. **# academias Smart Fit Brasil próprias EoP** — tabela "Por Marca > Smart Fit > Próprias > Brasil" (linha de academias)
3. **# alunos Smart Fit Brasil próprias EoP** (mil) — tabela "Por Marca > Smart Fit > Próprias > Brasil" (linha de clientes)
4. **TP freq%** (% check-ins TP em SF próprias BR) — divulgado anualmente no release do 4T do ano
5. **TP rev%** (% receita SF própria BR via TP) — divulgado anualmente no release do 4T

### Fórmulas

```
acad_média_q   = (acad_EoP_q + acad_EoP_{q-1}) / 2
alunos_média_q = (alunos_EoP_q + alunos_EoP_{q-1}) / 2
R/Loja_anu     = Receita_q × 4 / acad_média_q     [R$ mm]
Ticket_mensal  = Receita_q × 1000 / 3 / alunos_média_q     [R$/mês]
Alunos/loja    = alunos_média_q / acad_média_q     [mil]

Ajustes TotalPass (assume freq de uso TP user = freq de uso balcão):
Alunos/loja c/TP = alunos_média_q / (1 - tp_freq_pct/100) / acad_média_q     [mil]
Ticket ex-TP     = Receita_q × (1 - tp_rev_pct/100) × 1000 / 3 / alunos_média_q     [R$/mês]
```

### Distribuição trimestral do TP freq% / rev%

A empresa só divulga TP freq/rev anualmente. Distribuímos entre os 4 trimestres do ano via peso ponderado de **TP MAU mensal × intensidade sazonal de uso**:

```
tp_freq_q = freq_anual_disclosed × (TP_MAU_q × intensidade_q) / weighted_avg(TP_MAU × intens) sobre o ano
```

Onde:
- TP MAU mensal: Sensor Tower via Morgan Stanley Research (ver `sources/full/smart/totalpass_mau_brasil_mensal.md`)
- Intensidade sazonal de uso (check-ins/usuário ativo):
  - 1T = 1.10× (resolução de ano novo + verão BR)
  - 2T = 0.95× (queda pós-resolução)
  - 3T = 1.05× (inverno, alta retenção)
  - 4T = 0.90× (férias, calor, fim de ano)

Por construção, a média dos 4 trimestres bate o anual disclosed exato.

**Smart Fit MAU NÃO é usado** — entrar na academia balcão não exige abrir o app, Sensor Tower não captura.

## Tabela histórica + estimativa 1T26

| Per | Rec BR (R$mm) | # acad EoP | Alunos EoP | Acad méd | Alunos méd | R/Loja anu | YoY | Ticket mês | YoY | Alunos/loja | YoY | Alunos/loja c/TP | YoY | Ticket ex-TP | YoY | TP freq% | TP rev% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1T23 | 383,5 | 431 | 1.307 | 430 | 1.236 | 3,57 | — | 103,4 | — | 2,87 | — | — | — | — | — | — | — |
| 2T23 | 405,7 | 431 | 1.277 | 431 | 1.292 | 3,77 | — | 104,7 | — | 3,00 | — | — | — | — | — | — | — |
| 3T23 | 413,0 | 448 | 1.316 | 440 | 1.297 | 3,76 | — | 106,2 | — | 2,95 | — | — | — | — | — | — | — |
| 4T23 | 425,1 | 486 | 1.353 | 467 | 1.335 | 3,64 | — | 106,2 | — | 2,86 | — | — | — | — | — | — | — |
| 1T24 | 464,8 | 493 | 1.525 | 490 | 1.439 | 3,80 | +6,5% | 107,7 | +4,1% | 2,94 | +2,3% | 3,24 | — | 100,4 | — | 9,3% | 6,7% |
| 2T24 | 482,0 | 506 | 1.515 | 500 | 1.520 | 3,86 | +2,5% | 105,7 | +1,0% | 3,04 | +1,5% | 3,37 | — | 98,2 | — | 9,8% | 7,1% |
| 3T24 | 503,7 | 525 | 1.559 | 516 | 1.537 | 3,91 | +4,0% | 109,2 | +2,9% | 2,98 | +1,1% | 3,42 | — | 99,1 | — | 12,7% | 9,3% |
| 4T24 | 524,0 | 569 | 1.560 | 547 | 1.560 | 3,83 | +5,2% | 112,0 | +5,5% | 2,85 | -0,2% | 3,25 | — | 102,1 | — | 12,2% | 8,9% |
| 1T25 | 577,5 | 573 | 1.715 | 571 | 1.638 | 4,05 | +6,5% | 117,6 | +9,2% | 2,87 | -2,4% | 3,33 | +2,6% | 104,6 | +4,2% | 13,8% | 11,0% |
| 2T25 | 595,7 | 587 | 1.635 | 580 | 1.675 | 4,11 | +6,4% | 118,5 | +12,2% | 2,89 | -5,1% | 3,30 | -2,1% | 106,7 | +8,6% | 12,5% | 10,0% |
| 3T25 | 605,3 | 605 | 1.620 | 596 | 1.628 | 4,06 | +3,9% | 124,0 | +13,5% | 2,73 | -8,4% | 3,26 | -4,5% | 107,8 | +8,8% | 16,3% | 13,1% |
| 4T25 | 611,7 | 693 | 1.595 | 649 | 1.608 | 3,77 | -1,6% | 126,8 | +13,3% | 2,48 | -13,1% | 3,00 | -7,7% | 109,2 | +7,0% | 17,4% | 13,9% |
| **1T26 (est)** | **697,2** | **703** | **1.860** | **698** | **1.728** | **4,00** | **-1,2%** | **134,5** | **+14,4%** | **2,47** | **-13,7%** | **3,04** | **-8,7%** | **113,0** | **+8,0%** | **18,5%** | **16,0%** |

## Premissas 1T26 (anchor: padrões histórico + Plano Black + sazonalidade resolução)

- **# academias EoP 1T26 = 703** (+10 net adds vs 4T25=693)
- **# alunos EoP 1T26 = 1.860** (+265 net QoQ; +145 YoY vs 1T25=1715; reflete resolução + ramp-up vintage 2025)
- **Ticket ex-TP 1T26 = R$ 113** (+8,0% YoY vs 1T25=104,6; reflete repasse Plano Black + mix tier maturando)
- **TP freq% 1T26 = 18,5%** (anual 2026 anchor ~20% × peso sazonal 1T)
- **TP rev% 1T26 = 16,0%** (anual 2026 anchor ~17% × peso sazonal 1T)
- **Repasse Plano Black:** ocorreu em 1T26 (similar a 1T25), efeito YoY incremental ~neutro do repasse mas mix de novos alunos no tier mais alto continua agregando

## Highlights da estimativa 1T26

1. **Receita BR R$ 697 mm (+20,7% YoY)** — aceleração vs 1T25 (+24%) modesta; impulso de Black + TP mix mais que compensa desaceleração da rede.
2. **R/Loja anualizada R$ 4,00 mm (-1,2% YoY)** — marginalmente negativo, MUITO melhor que sequencial 4T25 (-1,6%). Vintage 2024+2025 ramping.
3. **Ticket consolidado R$ 134,5 (+14,4% YoY)** — driver: TP rev% subindo 11→16% + ticket ex-TP +8% acumulado.
4. **Ticket ex-TP R$ 113 (+8,0% YoY)** — confirma o repasse Plano Black + price ajuste anual. Trajetória 2025: +4,2/+8,6/+8,8/+7,0/+8,0% — consistente.
5. **Alunos/loja c/TP -8,7% YoY** — queda real continua, mas em ritmo desacelerado vs 4T25 (-7,7%). Sinal misto: resolução+ramp ajudam, mas adições recentes pesam.

## Gap freq–rev e % alunos vs 2019 (do modelo)

| Per | Gap freq–rev (pp) | % alunos totais hoje vs 2019 |
|---|---|---|
| 1T24 | 2,5pp | 93,9% |
| 2T24 | 2,7pp | 97,8% |
| 3T24 | 3,5pp | 99,0% |
| 4T24 | 3,3pp | 94,1% |
| 1T25 | 2,8pp | 96,4% |
| 2T25 | 2,5pp | 95,7% |
| 3T25 | 3,3pp | 94,6% |
| 4T25 | 3,5pp | 86,9% |
| 1T26 | **2,5pp** | **88,0%** |

- **Gap freq–rev** se mantém em ~2,5–3,5pp (TP gera receita por visita a desconto vs balcão). Tendência leve de fechamento ao longo do tempo (TP1→TP2 migration + repasse renegociado).
- **% alunos vs 2019** mostra que a base de alunos consolidada está abaixo do nível de 2019 (~88-99% historicamente, queda no 4T25 por aberturas concentradas). A cobertura volta a normalizar conforme vintages 2024-2025 maturam.

## Padrões históricos 3T → 1T (do modelo)

- **Δ Alunos/loja c/TP 3T→1T (2024-2025):** -2,7%. Para 2025-2026: **-6,9%** estimado (queda mais forte por aberturas 4T25).
- **Δ Ticket ex-TP 3T→1T (2024-2025):** +5,5%. Para 2025-2026: **+4,8%** estimado (Plano Black acumulado).
- Nota usuário: **"Teve repasse de preço igual"** entre 1T25 e 1T26 (ambos tiveram Black repasse jan), então o YoY incremental do repasse é ~neutro; a contribuição de ticket vem do mix tier maturando + price ajuste anual.

## Reconciliação com disclosed

| KPI 1T26 estimado | Valor | Sanity check vs disclosed esperado |
|---|---|---|
| Receita SF BR | R$ 697 mm | 1T26 anual: receita BR ≈ 1T25 +20% (gestão sinaliza desaceleração mas Black ajuda) |
| # acad próprias BR | 703 | Guidance 2026: 330-350 net adds, ~80% próprias = ~270 own; 1T tipicamente 25-35 |
| Alunos média | 1.728 | +5% YoY (1T25 = 1638); resolução + base maior |
| TP freq% 1T26 | 18,5% | Acima do anual 2025 (15%); reflete crescimento TP MAU +105% YoY |

(fonte: análise interna baseada em release/ITR/DFP 1T23-4T25 + Modelo SmartFit Pesquisa Bolsa; em: 2026-05-01)
