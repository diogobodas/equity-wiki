---
type: conceito
aliases: [Fluxo de Caixa, FCO, FCI, FCF, Cash Flow]
sources:
  - PRINCIPLES.md
  - compute_model.py
  - compute_banking.py
  - generate_excel.py
  - capital_de_giro.md
updated: 2026-04-05
---

# Fluxo de Caixa

Demonstrativo financeiro que reconcilia o lucro contábil com a geração efetiva de caixa. Terceiro pilar do modelo trimestral (DRE + BP + FC).

## Estrutura no Modelo

O fluxo de caixa é construído pelo método indireto a partir do lucro líquido:

```
FCO = LL + D&A + EP_não_caixa ± Δ Capital de Giro
FCI = Capex + Aquisições + Investimentos
FCF = FCO + FCI
Δ Dívida = plug (caixa mínima - caixa disponível)
```

## Por Setor

### Incorporadoras (Real Estate)

Para [[incorporadoras]], o fluxo de caixa é dominado pelo [[capital_de_giro]]:
- **Recebíveis**: ciclo longo (financiamento de clientes, repasse bancário)
- **Estoques**: terrenos + obras em andamento (ciclo de 24-36 meses)
- **Adiantamentos de clientes**: reduz necessidade de WC
- **[[equity_pickup]]** não é caixa — somente dividendos recebidos entram no FCO

A modelagem usa **dias-ratios** (dias de recebíveis, dias de estoques, dias de terrenos) calibrados historicamente por empresa.

A dívida é **plug**: quando o caixa projetado fica abaixo do caixa mínimo, o modelo emite dívida nova para cobrir o gap.

### Banking

Para [[banking]], o conceito de fluxo de caixa é menos relevante que para empresas não-financeiras. Os drivers principais são:
- **Crescimento de [[carteira_credito]]**: consome capital
- **PDD vs write-offs**: provisão contábil vs baixa efetiva
- **Dividendos**: payout sobre LL, limitado pelo [[cet1]]
- **Capital regulatório**: Basileia/CET1 como restrição ao crescimento

O modelo bancário não constrói FC explícito — o BP (ativo = passivo) é a reconciliação primária.

## Dívida como Plug

No modelo de [[incorporadoras]], a dívida é variável de fechamento (plug). A lógica:

1. Calcular caixa disponível = caixa_t-1 + FCO + FCI + dividendos
2. Se caixa < caixa_minima → emitir dívida nova = caixa_minima - caixa
3. Se caixa > caixa_minima → amortizar dívida existente (até zero)

Isso resolve a circularidade do modelo: dívida afeta resultado financeiro, que afeta LL, que afeta FC, que afeta dívida. O modelo quebra a circularidade usando saldos de t-1 para o resultado financeiro.

## Por Empresa (Real Estate)

| Empresa | Perfil de FC | Particularidade |
|---------|-------------|-----------------|
| [[cyrela]] | Geração forte, alto [[capital_de_giro]] em terrenos | CashMe (subsidiária financeira) gera caixa adicional |
| [[cury]] | FC positivo consistente, WC leve | Sem investidas, modelo simples |
| [[direcional]] | Riva (partnership) gera minorities relevantes | Alto crescimento pressiona WC |
| [[tenda]] | FC volátil, MCMV tem repasse rápido | Segmento Alea em ramp-up consome caixa |
| [[plano_plano]] | FC apertado em fase de crescimento | Compras de terreno acima da média |

## Particularidades Brasileiras

- **JCP ([[jcp]])**: reduz IR efetivo, aumenta caixa líquido vs lucro contábil. Para [[incorporadoras]], JCP é relevante mas limitado pelo PL (base de cálculo)
- **INCC ([[incc]])**: inflação de construção afeta o valor dos estoques e recebíveis. Contratos de venda de imóveis são corrigidos por INCC, mas custos também sobem — efeito líquido depende do mix
- **Repasse bancário**: transferência de recebíveis para banco financiador gera caixa imediato. Empresas de [[mcmv]] como [[cury]] e [[tenda]] têm repasse mais rápido (80-90% no ato)
- **Regime de caixa vs competência**: Receita POC ([[poc_revenue]]) é contábil; o caixa efetivo depende do andamento físico da obra e das parcelas de clientes

## Armadilhas Comuns

1. **Confundir EP com caixa**: [[equity_pickup]] de investidas (ex: Lavvi, Cury para CYRE3) aparece no DRE mas NÃO gera caixa — somente dividendos recebidos entram no FC
2. **Ignorar sazonalidade**: 4T tipicamente tem mais entregas e repasses → FC mais forte
3. **VGV ≠ caixa**: [[vgv_lancamentos]] é compromisso de venda; o caixa chega ao longo do ciclo de construção (24-36 meses)
4. **WC é o driver, não o LL**: uma incorporadora pode ter lucro crescente e FC negativo se estiver comprando terrenos e crescendo [[velocidade_vendas]]

## Ver Também

- [[capital_de_giro]] — principal driver do FCO para incorporadoras
- [[equity_pickup]] — EP não é caixa
- [[jcp]] — impacto fiscal no fluxo
- [[poc_revenue]] — receita contábil vs caixa
- [[vgv_lancamentos]] — compromisso de venda, não caixa
- [[margem_backlog]] — margem a realizar sobre receita futura
- [[incorporadoras]] — setor onde FC é mais crítico
- [[banking]] — setor onde BP substitui FC como reconciliação
