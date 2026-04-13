---
type: concept
aliases: [Debêntures, Debentures, CRI, Certificado de Recebíveis Imobiliários]
sources:
  - sources/full/tenda/2025/dfp.md
  - sources/full/tenda/2024/dfp.md
  - sources/full/tenda/2T25/fato_relevante_904079.md
  - sources/full/tenda/3T25/fato_relevante_952757.md
  - sources/structured/tenda/2025/dfp.json
  - sources/full/cyrela/2025/dfp.md
  - sources/full/cyrela/4T25/release.md
  - sources/structured/cyrela/2025/dfp.json
  - sources/full/cury/2025/dfp.md
  - sources/structured/cury/2025/dfp.json
created: 2026-04-12
updated: 2026-04-13
---

# Debêntures

**Debêntures** são títulos de dívida de médio/longo prazo emitidos por empresas brasileiras no mercado de capitais local. Para incorporadoras, são o principal instrumento de captação corporativa (não vinculada a projeto específico), complementando o funding de projeto via SFH/SFI.

## Estrutura típica no setor imobiliário

Incorporadoras listadas emitem debêntures com frequência, geralmente vinculadas a **CRIs (Certificados de Recebíveis Imobiliários)** — securitizações onde os recebíveis da incorporadora servem como lastro. A cadeia típica:

1. Incorporadora emite debêntures (quirografárias ou com garantia real).
2. Securitizadora (ex: Opea, Travessia) adquire as debêntures.
3. Securitizadora emite CRIs lastreados nas debêntures, distribuídos ao mercado.
4. Investidores pessoa física e fundos compram os CRIs (isenção de IR para PF).

Esse arranjo permite à incorporadora captar a taxas menores do que empréstimos bancários diretos, especialmente em ambiente de Selic alta.

## Métricas relevantes

- **Custo médio:** tipicamente CDI + spread (1,5% a 4,0% para investment grade). Players com rating mais alto (ex: brAAA da [[direcional|Direcional]]) captam com spreads menores. A [[cyrela|Cyrela]], líder do setor, capta a 97,9% CDI — abaixo do CDI cheio (fonte: sources/full/cyrela/4T25/release.md).
- **Duration:** prazo médio ponderado da dívida, em meses. Incorporadoras buscam duration > 20 meses para evitar concentração de vencimentos.
- **Covenants:** cláusulas contratuais, tipicamente Dívida Líquida Corporativa / PL < limite (ex: 15% ou 50%). Violação pode acelerar vencimento.

## Caso Cyrela — dívida corporativa investment-grade (2025)

A [[cyrela|Cyrela]] é exemplo de emissora de baixo custo no setor. Em 31/12/2025:

- **Dívida bruta consolidada:** R$ 8,7 bi, sendo empréstimos R$ 3,8 bi + debêntures/CRI R$ 5,0 bi (fonte: sources/full/cyrela/2025/dfp.md §nota_10).
- **Dívida corporativa total:** R$ 5,4 bi (Cyrela R$ 2,6 bi + CashMe R$ 2,8 bi), prazo médio de 4,5 anos e custo médio de **97,9% CDI** — spread negativo, refletindo o rating de crédito da companhia (fonte: sources/full/cyrela/4T25/release.md).
- **Dívida líquida:** R$ 1,7 bi (DL/PL 14,9%; DL ajustada/PL ajustado 21,5% após R$ 1,4 bi em dividendos no ano) (fonte: sources/full/cyrela/2025/dfp.md).
- **Nova emissão dez/2025:** R$ 320 mm a CDI+0,60% — evidência de acesso a funding barato mesmo com Selic elevada (fonte: sources/full/cyrela/2025/dfp.md §nota_10).
- Covenants financeiros cumpridos em 31/12/2025 (fonte: sources/full/cyrela/2025/dfp.md §nota_10).

A Cyrela também capitaliza juros ao estoque (R$ 209 mm em 2025), o que reduz o custo financeiro aparente na DRE mas infla o CMV — a margem bruta ajustada (34,8%) é 220 bps acima da reportada (32,6%) (fonte: digested/cyrela_dfp_2025_summary.md).

## Caso Tenda — 12ª e 13ª emissões (2025)

A [[tenda|Tenda]] passou por ciclo de reestruturação de dívida entre 2022-2025:

- **Pré-crise (2020):** funding a CDI+1,5-2,0%, duration confortável.
- **Crise (2022-2023):** dívida cara (CDI+4,0%, TEND17), covenants renegociados com waiver, custo médio 13% a.a.
- **Recuperação (2024):** prepagou TEND17 (R$ 141,8 mm a CDI+4,0%), emitiu CCB Bradesco a CDI+1,69%. Custo médio caiu de 13,0% para 11,57% a.a. ao longo do ano (fonte: structured/tenda/2024/dfp.json :: company_specific.debentures_detalhe).
- **12ª emissão (mai/2025):** R$ 180 mm, garantia real, CDI+2,10%, via Travessia (fonte: full/tenda/2T25/fato_relevante_904079.md).
- **13ª emissão (out/2025):** R$ 300 mm, quirografárias, via CRI Opea/Bradesco BBI. Séries com taxas de 8,99% a 14,45% a.a. Vencimento bullet 2030/2031/2032 — endereçou necessidade de captação até final de 2026 (fonte: full/tenda/3T25/fato_relevante_952757.md).

Ao final de 2025, debêntures consolidadas da Tenda totalizavam R$ 993 mm (vs R$ 541 mm antes da 13ª emissão). Duration total: 24,2 meses, custo médio nominal 13,67% a.a. Covenants folgados: DL corp / PL de -4,53% vs limite de 15% (fonte: structured/tenda/2025/dfp.json :: company_specific.debentures_detalhe).

## Caso Cury — modelo capital-light com dívida disciplinada (2025)

A [[cury|Cury]] opera com endividamento controlado apesar do forte crescimento:

- **Dívida bruta:** R$ 1.474,9 mm (+49,5% A/A), sendo 79,7% no longo prazo, com vencimentos até 2035 (fonte: sources/structured/cury/2025/dfp.json).
- **Dívida líquida:** negativa em R$ 316 mm — a companhia mantém posição de caixa líquido mesmo após distribuir R$ 1.352 mm em dividendos em 2025 (payout 138% do lucro Cury, usando reservas acumuladas) (fonte: digested/cury_dfp_2025_summary.md).
- **Resultado financeiro:** -R$ 47,8 mm (custo da dívida maior parcialmente compensado por receita financeira sobre o caixa) (fonte: sources/full/cury/2025/dfp.md).

O contraste com a Tenda é instrutivo: enquanto a Tenda opera com custo médio de 13,67% a.a. e DL corp/PL próxima a zero, a Cury mantém DL negativa e ROE de 78,8% — evidência de que o modelo capital-light com SPEs bem financiadas dispensa captação corporativa agressiva (fonte: digested/cury_dfp_2025_summary.md).

## Comparativo de custo de dívida (dez/2025)

| Incorporadora | Deb/CRI (R$ mm) | Custo médio | DL/PL | Duration |
|---|---:|---|---:|---|
| [[cyrela\|Cyrela]] | 5.000 | 97,9% CDI | 14,9% | ~4,5 anos |
| [[tenda\|Tenda]] | 993 | 13,67% a.a. nom. | -4,5% | 24,2 meses |
| [[cury\|Cury]] | 1.475 (total) | n.d. | caixa líquido | 79,7% LP |

(fontes: structured/tenda/2025/dfp.json, full/cyrela/4T25/release.md, structured/cury/2025/dfp.json)

## Cessão pro-soluto de recebíveis

Instrumento complementar às debêntures: a incorporadora vende recebíveis (parcelas a receber de compradores) a um securitizador, **sem direito de regresso** (pro-soluto). Vantagem: transfere risco de crédito e antecipa caixa. Desvantagem: despesa de cessão na DRE (spread do securitizador).

A Tenda acumulou R$ 609,8 mm em saldo de cessões pro-soluto no 3T25, com despesa de cessão crescendo de R$ 29,3 mm (2023) para R$ 52,8 mm (2024) (fonte: full/tenda/2024/dfp.md §nota_4a). A operação tornou-se recorrente via CRI Opea (até R$ 300 mm em integralizações sucessivas).

Relacionado: [[tenda]], [[cyrela]], [[cury]], [[direcional]], [[incorporadoras]], [[resultado_a_apropriar]]
