---
type: digested
empresa: porto
ticker: PSSA3
periodo: 2024
tipo: dfp
fonte: sources/full/porto/2024/dfp.md
schema: seguradora/v1
created: 2026-04-22
---

# Porto Seguro — DFP 2024 (consolidado IFRS 17)

## TL;DR

Ano de crescimento de dois dígitos em receita (+13%) e lucro (+17%), puxado por **Saúde** (lucro +96%) e **Bank** (lucro +53%). Vertical seguros tradicional mais defensivo: prêmios +3% ex-saúde, índice combinado mantido em **89%** — estratégia explícita de preservar margem sobre volume. ROAE 20,0%, 18 mm clientes no ecossistema (fonte: full/porto/2024/dfp.md §relatório_administracao).

## Números-chave

| Indicador | 2024 | 2023 | Δ |
|---|---|---|---|
| Receita total (gerencial) | R$ 36.929,7 mm | R$ 32.621,0 mm | +13,2% |
| Prêmio Retido | R$ 27.800,5 mm | R$ 25.066,0 mm | +10,9% |
| Prêmio Ganho | R$ 27.478,6 mm | R$ 24.051,5 mm | +14,2% |
| Lucro Líquido (societário IFRS 17) | R$ 2.644,8 mm | R$ 2.266,1 mm | +16,7% |
| Lucro Líquido Ex-IFRS 17 | R$ 2.653,9 mm | R$ 2.266,4 mm | +17,1% |
| ROAE | 20,0% | 19,6% | +0,3 pp |
| Patrimônio Líquido | R$ 14.145,4 mm | R$ 12.497,8 mm | +13,2% |
| Ativo Total | R$ 47.913,7 mm | R$ 44.239,6 mm | +8,3% |

## Resultado por vertical (gerencial, Ex-IFRS 17)

| Vertical | Lucro Líquido | Δ vs 2023 | Comentário |
|---|---|---|---|
| Porto Seguro (seguros) | R$ 1.643,4 mm | **-13%** | Patrimonial +12%, Vida +9%, Auto +1% (prêmio e frota). Índice combinado 89% mantido. Lucro caiu vs 2023 apesar da preservação de margem — reflete mix e resultado financeiro menor |
| Porto Saúde | R$ 393,6 mm | **+96%** | Vidas saúde +24% (675k), odonto +27% (995k). Receitas +44%. Índice combinado 92% (melhora de 4 pp). Expansão regional (Linha Pro RJ/DF, Porto Bairro SP) |
| Porto Bank | R$ 632,2 mm | **+53%** | Receita +22%. Consórcio +37%, Cartão/Financ +20%. Inadimplência 90d recuou para 5,2% (-1,4 pp), abaixo da média de mercado |
| Porto Serviço | R$ 204,6 mm | n/d (novo) | R$ 2,5 bi de receita, 5,2 mm atendimentos; 24% de vendas B2C/parcerias. Registro CVM em ago/2024 |
| Demais | R$ (219,8) mm | Melhora vs -R$ 241,2 mm | Holding + negócios menores |

## DRE IFRS 17 (consolidada)

| Linha | 2024 |
|---|---|
| Receita de Seguro | R$ 28.363,1 mm |
| Receita ops. de crédito | R$ 3.701,0 mm |
| Receita serviços | R$ 3.084,1 mm |
| Receita cap. | R$ 95,3 mm |
| **Receita Total** | **R$ 35.243,5 mm** |
| Despesas de seguro | R$ (21.614,4) mm |
| Despesas adm./gerais | R$ (6.391,6) mm |
| Resultado operacional | R$ 3.099,5 mm |
| Resultado financeiro | R$ 845,1 mm |
| IR/CSLL | R$ (1.253,8) mm |
| **Lucro líquido consolidado** | **R$ 2.690,8 mm** |
| Atribuído à controladora | R$ 2.644,8 mm |

## Balanço

- **Ativo Total:** R$ 47,9 bi (+8,3%). Crescimento concentrado em aplicações financeiras a custo amortizado (R$ 8,99 bi, +142%) e no circulante de contas a receber (R$ 14,4 bi, dominado pela carteira Porto Bank).
- **Carteira de crédito Bank:** R$ 16,6 bi bruta / R$ 14,9 bi líquida. Provisão sobre carteira caiu de 12,66% para **10,56%**, consistente com narrativa de melhora de qualidade.
- **Provisões técnicas (contrato de seguro):** R$ 10,4 bi (c+nc). Passivos financeiros do Bank: R$ 17,2 bi.
- **PL Consolidado:** R$ 14,1 bi. Dividendos/JCP pagos no ano: R$ 838 mm + R$ 559 mm adicionais propostos + R$ 201 mm de recompra.

## Destaques qualitativos

- **Ecossistema Porto** com 4 verticais: seguros, saúde, bank, serviços. Porto Saúde e Porto Serviço obtiveram registro CVM em ago/2024 — preparando eventual abertura de capital autônoma.
- **20 anos de IPO** em 2024 + inclusão no **Ibovespa**.
- **Rentabilidade da carteira de aplicações (ex-Previdência/ALM):** 85% do CDI — abaixo do CDI, impactada por alocações em ações e pré-fixados. Resultado financeiro líquido: R$ 919 mm (-9,8% vs 2023).
- **IFRS 17** em vigor desde 2023; impacto marginal de R$ (9,1) mm em 2024 vs gerencial.
- **13.169 colaboradores** no grupo; rotatividade 20,96% (+3,38 pp vs 2023).

## Observações para modelagem

1. **Visão gerencial** (Ex-IFRS 17) é o que a administração usa para comunicar resultados e ROAE; IFRS 17 é o societário formal. Diferença é pequena em 2024 mas pode crescer.
2. A **alavancagem operacional ao índice de sinistralidade é alta**: sensibilidade reportada mostra que +5% na sinistralidade dos contratos impactaria em R$ (15,8) bi. Este é o principal risco do modelo.
3. **Bank está ganhando tração**: a melhora da inadimplência (5,2%) em um ano de deterioração sistêmica é um diferencial competitivo — mérito da colateralização (veículos segurados) e da base proprietária de corretores.
4. **Saúde é o motor de crescimento**: 96% de crescimento no lucro com índice combinado caindo para 92% indica ganhos de escala em uma vertical ainda sub-escala vs Hapvida/Unimed.
5. **Seguro auto estagnou** (+1% em prêmios e frota) — preço vs volume, mantendo margem. Em um ciclo de sinistralidade favorável, a decisão de não crescer pode limitar o lucro futuro quando o ciclo virar.

(fonte: full/porto/2024/dfp.md §relatório_administracao, §nota_7_segmentos, §nota_10_emprestimos_recebiveis)
