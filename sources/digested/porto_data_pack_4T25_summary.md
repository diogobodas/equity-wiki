---
type: digest
empresa: porto
ticker: PSSA3
periodo: 4T25
source_type: data_pack
full: sources/full/porto/4T25/PSSA3_4T25_data_pack.md
structured: sources/structured/porto/4T25/data_pack.json
schema: seguradora/v1
created: 2026-04-22
---

# Porto Seguro — Data Pack 4T25

## O que é

Planilha gerencial (atualização 31/12/2025) com séries históricas trimestrais que não estão no release/ITR: BP/DRE IFRS-4 desde 1T12, DREs gerenciais por vertical desde 1T23 e KPIs operacionais por vertical desde 1T21. **Fonte canônica para modelagem Ex-IFRS 17** — complementa o `release.json` (IFRS 17 oficial) e o `dfp.json` anual (fonte: full/porto/4T25/PSSA3_4T25_data_pack.md).

## Snapshot 4T25 (Ex-IFRS 17)

| Indicador | 4T25 | 4T24 | Δ YoY |
|---|---:|---:|---:|
| Receita Total | R$ 10.627,5 mm | R$ 9.835,0 mm | +8,1% |
| Prêmio Retido | R$ 8.033,9 mm | R$ 7.428,4 mm | +8,2% |
| Lucro IFRS 17 | R$ 838,7 mm | R$ 670,8 mm | **+25,0%** |
| Lucro Ex-IFRS 17 | R$ 832,2 mm | R$ 666,8 mm | +24,8% |
| ROAE | 22,5% | 20,3% | +2,2 p.p. |
| PL Médio | R$ 14.896 mm | R$ 13.233 mm | +12,6% |
| IR efetivo | 14,1% | 33,7% | -19,6 p.p. |

**FY2025:** Receita R$ 41,1 bi (+11,2%), **Lucro R$ 3,38 bi (+27,8%)** recorde, ROAE 22,7%, Ativo Total R$ 69,1 bi, Eficiência 11,0%.

## Lucro por vertical 4T25 (trimestre, Ex-IFRS 17)

| Vertical | Lucro | Δ YoY | ROAE |
|---|---:|---:|---:|
| Porto Seguro | 459,1 | +4,0% | 32,3% |
| Porto Saúde | 169,7 | +22,2% | 32,7% |
| Porto Bank | 219,4 | **+50,2%** | 28,4% |
| Porto Serviço | 83,5 | +41,9% | 36,1% |
| Controladora | (93,1) | — | — |

Não-seguro = **56% do lucro no 4T25** (+9 p.p. YoY); 49% no FY25.

## Indicadores operacionais 4T25

- **Sinistralidade Seguros 51,4%**, IC Seguros 89,5%, IC Ampliado 85,3%
- **Sinistralidade Saúde 73,5%** (-1,7 p.p.), IC Saúde 88,5%
- Auto: 6,23 mi frota (+3,9%), sinistralidade 57,7% (+1,2 p.p.)
- Saúde: 2,02 mi vidas (831k saúde + 1,18 mi odonto)
- Bank: carteira R$ 23,5 bi (+22%), consórcio administrado R$ 107,3 bi (+36%), inadimplência 90d 7,3%, NIM ajustado 3,0%
- **Resultado financeiro R$ 288,7 mm (-24% QoQ)** — rentabilidade **56,4% do CDI** (pior em 8 trim; FY25 75,1%)

## Balanço IFRS-4 em 31/12/2025

**Ativo Total R$ 69,1 bi** (+15% YoY). Instrumentos financeiros R$ 21,7 bi (+11%), prêmios a receber R$ 10,9 bi, operações de crédito R$ 5,95 bi (+32%), custos aquisição diferidos R$ 6,4 bi (+33%). **Passivos financeiros R$ 21,2 bi (+23%)** — funding Porto Bank em expansão. Contratos de seguro R$ 24,4 bi. **PL total R$ 15,6 bi** (+9,4%). ⚠ Linha "Provisões" em -R$ 53,2 mm aparenta anomalia — validar com DFP 2025.

## Séries em `company_specific` para modelagem

- DRE gerencial consolidada trimestral **1T23–4T25** (16 quarters)
- Lucro por vertical trimestral 1T23–4T25
- KPIs operacionais (sinistralidade, IC, eficiência, CDI) 1T24–4T25
- Clientes / itens segurados / cartões / consórcio 1T24–4T25
- BP IFRS-4 4T25 + série longa ativo total 2012–2025
