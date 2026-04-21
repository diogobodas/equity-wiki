---
type: entity
aliases: [CashMe]
sources:
  - sources/digested/cyrela_release_1T25_summary.md
  - sources/digested/cyrela_release_2T25_summary.md
  - sources/digested/cyrela_release_3T25_summary.md
  - sources/digested/cyrela_release_4T25_summary.md
  - sources/digested/cyrela_itr_3T25_summary.md
created: 2026-04-20
updated: 2026-04-20
---

# CashMe

Fintech de crédito com garantia de imóvel (CGI / home equity) controlada pela [[cyrela]]. Opera como subsidiária financeira do grupo, captando recursos no mercado de capitais e reciclando capital via carteira de recebíveis, com o resultado financeiro consolidado nos demonstrativos da controladora.

## Negócio

CashMe concede crédito colateralizado por imóveis residenciais (home equity), segmento com risco de crédito historicamente baixo no Brasil dado o LTV conservador e a dificuldade cultural de perda do imóvel. A carteira é registrada em títulos e valores mobiliários (TVM) no balanço consolidado da Cyrela; o funding é estruturado via emissões de debêntures e CRI — instrumentos de dívida corporativa separados do funding de obra (SFH/MCMV).

## Contribuição ao resultado Cyrela

### Resultado financeiro (linhas relevantes)

| Período | Res. Financeiro CashMe | Comercial CashMe | G&A CashMe |
|---|---:|---:|---:|
| 1T25 | R$ 58 mm | R$ 28 mm | R$ 15 mm |
| 2T25 | R$ 72 mm | n/d | n/d |
| 3T25 | R$ 61 mm | n/d | n/d |
| 4T25 | R$ 56 mm | n/d | n/d |
| **2025 (ano)** | **R$ 247 mm** | — | — |

(fonte: sources/digested/cyrela_release_1T25_summary.md; sources/digested/cyrela_release_2T25_summary.md; sources/digested/cyrela_release_3T25_summary.md; sources/digested/cyrela_release_4T25_summary.md)

O resultado financeiro da CashMe é o principal driver do resultado financeiro positivo consolidado da Cyrela, que historicamente é negativo para incorporadoras puras. Em 2025, os R$ 247 mm anuais da CashMe explicam boa parte dos R$ 248 mm de resultado financeiro líquido reportado no grupo (fonte: sources/digested/cyrela_dfp_2025_summary.md).

A CashMe também impacta negativamente as despesas comerciais (mídia, estandes próprios de captação) e G&A do consolidado. No 1T25, os impactos foram R$ 28 mm em comercial e R$ 15 mm em G&A (fonte: sources/digested/cyrela_release_1T25_summary.md).

## Carteira e funding

| Período | Carteira TVM | Dívida Corporativa CashMe |
|---|---:|---:|
| 1T25 | n/d | R$ 1.993 mm |
| 2T25 | n/d | R$ 2.200 mm |
| 4T25 | R$ 3.400 mm | R$ 2.800 mm |

(fonte: sources/digested/cyrela_release_1T25_summary.md; sources/digested/cyrela_release_2T25_summary.md; sources/digested/cyrela_release_4T25_summary.md)

A dívida da CashMe é integralmente corporativa (debêntures e CRI) e separada do funding imobiliário da Cyrela. Em 05/05/2025, houve resgate antecipado das debêntures originais da CashMe, zerando a linha de debêntures no balanço consolidado do 3T25 (fonte: sources/digested/cyrela_itr_3T25_summary.md). Novas captações foram realizadas ao longo de 2025 para financiar o crescimento da carteira.

No 4T25, a dívida corporativa total do grupo Cyrela era de R$ 5,4 bi, dividida entre Cyrela holding (R$ 2,6 bi) e CashMe (R$ 2,8 bi), com prazo médio de 4,5 anos e custo médio de 97,9% CDI (fonte: sources/digested/cyrela_release_4T25_summary.md).

## Impacto no balanço e alavancagem consolidada

A Cyrela reporta alavancagem em duas métricas:
- **Dívida Líquida Ajustada / PL Ajustado (padrão):** inclui CashMe.
- **Ex-CashMe:** exclui tanto a carteira de crédito (AVJORA) quanto a dívida de funding da CashMe — métrica relevante para isolar a alavancagem da operação de incorporação.

| Período | DLA/PLA (c/ CashMe) | DLA/PLA (ex-CashMe) |
|---|---:|---:|
| 1T25 | 9,3% | ~15,6% (R$ 1.625 mm / PL) |
| 2T25 | 12,7% | n/d |
| 3T25 | 8,2% | 16,4% |
| 4T25 | 21,5% | n/d |

(fonte: sources/digested/cyrela_release_1T25_summary.md; sources/digested/cyrela_release_2T25_summary.md; sources/digested/cyrela_release_3T25_summary.md; sources/digested/cyrela_release_4T25_summary.md)

A presença da CashMe reduz a alavancagem consolidada reportada porque a carteira de crédito (ativo) é marcada a valor de mercado (AVJORA) e compensa parcialmente a dívida de funding no cálculo ajustado. Analistas que querem ver apenas o risco da incorporação devem usar a métrica ex-CashMe.

## Pontos de atenção

- **Crescimento acelerado:** carteira cresceu de ~R$ 2,0 bi (funding 1T25) para R$ 3,4 bi (carteira 4T25) em quatro trimestres — ritmo exige monitoramento de qualidade de crédito e inadimplência (não divulgados nos releases de incorporação).
- **Custo de funding:** dívida a ~97,9% CDI em ambiente de Selic elevada comprime o spread líquido da carteira; sensibilidade alta a ciclos de juros.
- **Transparência limitada:** resultados da CashMe aparecem de forma agregada nos releases da Cyrela — não há demonstrativo financeiro separado publicado.
- **Separação analítica:** para modelar a Cyrela como incorporadora pura, é necessário excluir o resultado financeiro da CashMe, as despesas operacionais associadas e a dívida/carteira da subsidiária.
