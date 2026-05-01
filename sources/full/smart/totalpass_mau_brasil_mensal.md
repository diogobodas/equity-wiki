---
type: reference_data
empresa: smart
ticker: SMFT3
escopo: TotalPass MAU Brasil — mensal
periodo_coberto: 2022-01 a 2026-03
source: Modelo SmartFit Final - 4T25 (Pesquisa Bolsa/Diogo/Smartfit), sheet "Dados SensorTower MS", linha 15 ("TotalPass MAU - Brazil")
source_origin: Sensor Tower / Morgan Stanley Research
fetched: 2026-05-01
---

# TotalPass MAU Brasil — série mensal Sensor Tower

Monthly Active Users (MAU) da plataforma TotalPass no Brasil, série mensal de jan/2022 a mar/2026. Cobre **toda a rede TotalPass**, não apenas os usuários que frequentam Smart Fit (TotalPass tinha ~32 mil academias parceiras no Brasil em 4T25).

**Uso analítico:** sinal de crescimento da base ativa TP. Usado pra **fatiar a freq% TP anual disclosed** (11% em 2024, 15% em 2025) entre os 4 trimestres do ano via peso mensal. Smart Fit MAU **não** é usado nessa análise porque entrar na academia balcão não exige abrir o app — Sensor Tower não captura.

## Dados mensais (MAU, # usuários ativos)

| Mês | TotalPass MAU BR |
|---|---|
| 2022-01 | 56.016 |
| 2022-02 | 60.420 |
| 2022-03 | 64.964 |
| 2022-04 | 62.770 |
| 2022-05 | 71.017 |
| 2022-06 | 71.105 |
| 2022-07 | 84.632 |
| 2022-08 | 104.021 |
| 2022-09 | 115.686 |
| 2022-10 | 119.422 |
| 2022-11 | 124.851 |
| 2022-12 | 120.108 |
| 2023-01 | 162.563 |
| 2023-02 | 158.209 |
| 2023-03 | 170.654 |
| 2023-04 | 169.716 |
| 2023-05 | 188.580 |
| 2023-06 | 195.697 |
| 2023-07 | 214.422 |
| 2023-08 | 243.411 |
| 2023-09 | 620.953 |
| 2023-10 | 655.143 |
| 2023-11 | 635.367 |
| 2023-12 | 649.056 |
| 2024-01 | 914.783 |
| 2024-02 | 919.313 |
| 2024-03 | 943.212 |
| 2024-04 | 1.011.408 |
| 2024-05 | 1.112.143 |
| 2024-06 | 1.270.681 |
| 2024-07 | 1.317.651 |
| 2024-08 | 1.332.291 |
| 2024-09 | 1.350.567 |
| 2024-10 | 1.570.178 |
| 2024-11 | 1.453.835 |
| 2024-12 | 1.450.829 |
| 2025-01 | 1.865.022 |
| 2025-02 | 1.831.584 |
| 2025-03 | 1.944.460 |
| 2025-04 | 1.925.001 |
| 2025-05 | 1.928.034 |
| 2025-06 | 2.089.796 |
| 2025-07 | 2.138.221 |
| 2025-08 | 2.189.000 |
| 2025-09 | 2.677.354 |
| 2025-10 | 2.957.492 |
| 2025-11 | 2.876.594 |
| 2025-12 | 2.889.637 |
| 2026-01 | 3.732.000 |
| 2026-02 | 3.712.000 |
| 2026-03 | 4.110.000 |

## Agregados trimestrais

| Trimestre | TP MAU sum | YoY % |
|---|---|---|
| 1T22 | 181.400 | — |
| 2T22 | 204.892 | — |
| 3T22 | 304.339 | — |
| 4T22 | 364.381 | — |
| **2022 anual** | 1.055.012 | — |
| 1T23 | 491.426 | +171% |
| 2T23 | 553.993 | +170% |
| 3T23 | 1.078.786 | +254% |
| 4T23 | 1.939.566 | +432% |
| **2023 anual** | 4.063.771 | +285% |
| 1T24 | 2.777.308 | +465% |
| 2T24 | 3.394.232 | +513% |
| 3T24 | 4.000.509 | +271% |
| 4T24 | 4.474.842 | +131% |
| **2024 anual** | 14.646.891 | +260% |
| 1T25 | 5.641.066 | +103% |
| 2T25 | 5.942.831 | +75% |
| 3T25 | 7.004.575 | +75% |
| 4T25 | 8.723.723 | +95% |
| **2025 anual** | 27.312.195 | +86% |
| **1T26** | 11.554.000 | **+105%** |

## Notas

- O salto de **3T23** para frente reflete a explosão de penetração TP no mercado B2B brasileiro — coincidiu com a crise reputacional do Gympass/Wellhub em 2023 e a entrada de grandes contratantes (Carrefour, Bradesco, Nestlé) na plataforma TP.
- Crescimento de **2024→2025** desacelera relativamente (+86% vs +260% em 23→24) mas o ritmo absoluto de adições mantém-se forte.
- **1T26 +105% YoY MAU** mostra que a aceleração continua no início de 2026 — sustenta tese de que TP freq% anual 2026 deve ficar acima dos 15% disclosed em 2025 (extrapolação razoável: 18-20%).

## Calibração com freq% disclosed

| Ano | TP MAU anual (mm) | Freq% TP em SF próprias (disclosed) | Implícito: check-ins/MAU |
|---|---|---|---|
| 2024 | 14,6 | 11% | calibração base |
| 2025 | 27,3 | 15% | +36% relativo (vs +86% MAU) |
| 2026 (TBD) | ~46-50? | **a divulgar** | — |

A relação MAU→freq% é menos que 1:1 (usuários TP vão a outras academias da rede TP além de Smart Fit, e visitam menos vezes/mês que balcão). Esse fator estável de ~0,4 (freq_growth/MAU_growth) sustenta extrapolação 2026 = 18-20% freq.

(fonte: Modelo SmartFit Final - 4T25, sheet "Dados SensorTower MS"; Sensor Tower via Morgan Stanley Research)
