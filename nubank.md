---
type: empresa
source_quality: conceptual
aliases: [Nubank, Nu Holdings, NU, Nu Bank, Banco Nu]
sources:
  - sectors/banking/sector_profile.md
  - wiki/banking.md
  - wiki/custo_risco.md
  - wiki/crescimento_carteira.md
  - wiki/carteira_credito.md
updated: 2026-04-05
---

# Nubank

O **Nubank** (Nu Holdings Ltd., ticker: NU na NYSE) é a maior fintech da América Latina e um dos maiores bancos digitais do mundo por número de clientes. Fundada em 2013 em São Paulo por David Vélez (colombiano), Cristina Junqueira e Edward Wible, a empresa revolucionou o setor bancário brasileiro ao oferecer serviços financeiros simples e gratuitos via aplicativo, sem agências físicas.

## Modelo de Negócio

O Nubank opera como **banco digital puro** — 100% digital, sem agências, com aquisição de clientes via indicação (viral). O modelo é baseado em:

1. **Cartão de crédito (Mastercard)**: Produto inicial e ainda o mais rentável. Sem anuidade. Revolving com juros altos (~220-250% a.a.) e cartão com prazo (parcelado sem juros).
2. **Conta digital (NuConta)**: Conta corrente com rendimento automático no CDI. Sem tarifas.
3. **Crédito pessoal**: Empréstimos pessoais, crédito consignado privado (em expansão), refinanciamento.
4. **Investimentos**: Produtos de renda fixa, fundos, ações via Nu Invest.
5. **Seguros**: Produtos seguros de vida, automotivo via parceiros.
6. **Mercado LatAm**: México (Nu Mexico) e Colômbia (Nu Colombia) — em fase de expansão.

## Escala e Crescimento

| Métrica | 2023 | 2025 (estimativa) |
|---------|------|-------------------|
| Clientes totais | ~90M | ~100-110M |
| Carteira de crédito | ~R$50B | ~R$100B+ |
| Receita total | ~R$25B | ~R$40-50B |
| NIM bruto | ~20-25% | ~18-22% |
| Custo de risco | ~8-12% | ~8-10% |
| NIM ajustado | ~10-14% | ~10-12% |

**Nota:** Valores acima são estimativas conceptuais baseadas em conhecimento geral. Verificar nos relatórios Nu Holdings (20-F na SEC) para dados precisos.

## Diferenciais vs Bancos Tradicionais

| Aspecto | Nubank | [[itau]], [[bradesco]] |
|---------|--------|----------------------|
| Agências | Zero | Milhares |
| Custo de aquisição de cliente (CAC) | Baixo (viral) | Médio-alto |
| Custo por cliente/ano | Muito baixo (~R$10-20) | Médio-alto (~R$80-150) |
| NIM bruto | Alto (~20%+) | Médio (~10-12%) |
| Custo de risco | Alto (~8-10%) | Baixo-médio (~3.7-5%) |
| NIM ajustado | Similar (~10-12%) | Similar (~7-8%) para Itaú |
| Escala em crédito | Menor (ainda crescendo) | Enorme (~R$1T+) |

## IPO e Valuation

O Nubank abriu capital na NYSE em dezembro de 2021 a uma avaliação de ~US$41B — a maior fintech da América Latina. O valuation reflete o crescimento acelerado, a optionalidade de LatAm e o prêmio de tecnologia.

**Múltiplos típicos de fintechs de crescimento:** P/E muito elevado (>30×) porque o mercado precifica crescimento futuro, não lucro corrente. Diferente dos bancos tradicionais (ITUB4, BBDC4) que são avaliados via P/BV.

## Riscos e Desafios

1. **Custo de risco elevado**: A base de clientes do Nubank inclui segmentos de maior risco (sem histórico bancário, jovens, baixa renda). O [[custo_risco]] de ~8-10% é 2× o do Itaú.
2. **Competição de grandes bancos**: [[itau]] com [[iti_itau]] e [[ion_itau]], Bradesco com seu digital, Santander — todos investindo em digital.
3. **Rentabilidade do crédito consignado**: O [[consignado_privado]] tem NIM mais baixo mas custo de risco muito menor — mix shift nessa direção comprima o NIM total.
4. **Regulação crescente**: Crescimento acelerado atrai escrutínio do BCB, especialmente em consignado e cartão de crédito.
5. **Risco LatAm**: México e Colômbia estão em fase de queima de caixa — podem pressionar resultado consolidado.

## Contexto Competitivo

O Nubank é o principal concorrente das plataformas digitais dos bancos estabelecidos:
- Concorre diretamente com [[iti_itau]] (digital de entrada do Itaú) em clientes de menor renda
- Concorre com [[ion_itau]] em investimentos (Nu Invest vs Ion)
- Concorre com [[xp_investimentos]] em distribuição de investimentos para clientes de média renda

O BCB monitora a concentração bancária: os cinco maiores bancos (incluindo Nubank em ativos de crédito) representam >70% do SFN.

## Para o Modelo

O Nubank não faz parte da cobertura direta deste projeto. Mas é relevante como:
- **Competidor** que pressiona [[eficiencia_operacional]] e spreads dos grandes bancos
- **Referência de NIM**: NIM alto com custo de risco alto — NIM ajustado similar aos bancos tradicionais
- **Benchmark de digitalização**: IE do Nubank é muito baixo (~25-30%), pressionando os bancos a reduzir custos

## NIM Ajustado: Por Que o Nubank Não É Mais Lucrativo

O Nubank tem NIM bruto muito alto (~20%+) mas NIM ajustado ao risco próximo dos bancos tradicionais. O motivo é o custo de risco elevado:

```
NIM_ajustado = NIM_bruto - Custo_Risco
```

| Banco | NIM Bruto (est.) | Custo Risco (est.) | NIM Ajustado |
|-------|-----------------|-------------------|-------------|
| [[nubank]] | ~20-22% | ~8-10% | ~12% |
| [[itau]] | ~11-12% | ~3,7% | ~7-8% |
| [[sanb11]] | ~11,5% | ~4,8% | ~6,7% |

O Nubank opera com mais risco por unidade de spread — a carteira é de clientes sem histórico bancário e de maior inadimplência. Com maturação da carteira (clientes mais antigos, mix shift para consignado privado), o custo de risco tende a cair — esse é o principal gatilho de lucratividade de longo prazo.

## Ver Também

- [[banking]] — setor bancário brasileiro e dinâmicas competitivas
- [[iti_itau]] — banco digital do Itaú, concorrente direto do Nubank
- [[ion_itau]] — plataforma de investimentos do Itaú
- [[xp_investimentos]] — plataforma de investimentos, concorrente no wealth management
- [[consignado_privado]] — produto que o Nubank está expandindo com NIM mais baixo
- [[custo_risco]] — NIM ajustado vs NIM bruto; onde o Nubank tem desvantagem estrutural
- [[indice_eficiencia]] — IE do Nubank muito baixo (benchmark digital)
- [[itau]] — maior banco privado brasileiro; principal alvo competitivo do Nubank
