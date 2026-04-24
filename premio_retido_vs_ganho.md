---
type: concept
aliases: [Prêmio emitido, Prêmio retido, Prêmio ganho, PPNG, Contraprestação efetiva, Outras receitas seguradora]
sources:
  - sources/full/generic/susep_sinistralidade_auto_analise_2010_2026.md
  - sources/digested/porto_dfp_2024_summary.md
  - sources/digested/porto_dfp_2025_summary.md
  - sources/digested/porto_release_4T25_summary.md
created: 2026-04-24
updated: 2026-04-24
---

# Prêmio Emitido → Retido → Ganho

Contabilização da receita em seguradora brasileira (SUSEP). A mesma apólice gera três valores diferentes na DRE dependendo do regime de reconhecimento:

```
Prêmio Emitido               (valor de face da apólice, cash-in potencial)
(−) Prêmio Resseguro Cedido
= Prêmio Retido              (o que a seguradora mantém sob seu risco)
(−/+) Variação da PPNG
= Prêmio Ganho               (reconhecido como receita no período, pro-rata)
```

## Prêmio Emitido

Valor contratual da apólice no ato da venda/renovação. Reconhecido no ato da emissão, independentemente do período de cobertura. É a métrica de "volume vendido" (análoga a [[vgv]] de incorporadora).

- Para auto tradicional: emissão é **anual**, lumpy (picos em jan por renovações, fev-abril retomada).
- Para saúde suplementar: emissão é **mensal** (mensalidade), smooth.
- Para vida prestamista: emissão é **única** (premium upfront), concentrada em meses de originação de crédito.

## Prêmio de Resseguro Cedido

Parte do prêmio passada ao ressegurador por repartir risco. Varia muito por linha:

| Ramo | Resseguro típico |
|---|---|
| Auto individual | ~0% (risco pulverizado, limite baixo) |
| Saúde suplementar | ~0% (mercado local não faz) |
| Patrimonial commercial | 20-40% (riscos grandes) |
| Aviação/marítimo | 60-90% (tesouraria via facultativo) |
| Vida prestamista | 10-20% |

## Prêmio Retido

= Emitido − Resseguro Cedido. Mede o risco que **fica com a seguradora**. É a base regulatória para cálculo de capital (PLA requerido SUSEP escala com Prêmio Retido e volatilidade por ramo).

## PPNG — Provisão de Prêmios Não Ganhos

Passivo de contrato de seguro que ainda não foi prestado. Mecânica:

- Apólice auto anual R$ 1.200 em 01/jun/25: emissão gera passivo PPNG de R$ 1.200, reduzido diariamente em R$ 1.200/365 = **R$ 3,29/dia**.
- Em 31/dez/25 (213 dias decorridos): PPNG residual = R$ 1.200 × (152/365) = R$ 499,73. Prêmio Ganho acumulado no ano = R$ 700,27.
- Em 31/mai/26: PPNG zera, apólice totalmente ganha.

PPNG é sempre reconhecida **pro-rata temporis em dias corridos** — regra SUSEP vigente; também consistente com IFRS 4 e princípio de competência (IFRS 17 tem mecânica similar via CSM, embora a partição de LIC/LRC seja diferente).

## Prêmio Ganho

= Prêmio Retido − Δ PPNG. Receita reconhecida no período (base do DRE de subscrição).

Relação **Retido → Ganho** varia por ramo:

| Ramo | Retido / Ganho steady-state |
|---|---|
| Auto individual | ≠ (Retido lumpy, Ganho smooth — gap ~10-20% em meses-pico) |
| Saúde suplementar | ≈ (ciclo mensal, PPNG residual) |
| Vida prestamista | ≠ (Retido single-premium, Ganho espalhado pelo período do crédito) |
| Vida tradicional anual | ≠ (semelhante auto) |

### Aplicação em auto (PSSA3 / BBSE / CXSE)

Diferença Retido/Ganho em auto é **material**. O [[porto_seguro|Porto]] reporta Prêmio Retido e Prêmio Ganho separadamente — em 2025, Prêmio Retido consolidado R$ 28,8 bi; parte ainda está em PPNG na virada. (fonte: digested/porto_dfp_2025_summary.md)

### Aplicação em saúde ([[porto_seguro|Porto Saúde]])

Em saúde, a diferença **praticamente não existe**:

1. **Resseguro ~0% em saúde suplementar** (ANS regula, mercado local não opera) → Retido ≈ Emitido.
2. **Ciclo mensal** — contratos PME, corporate, individual são todos mensais. Mensalidade emitida em abril é ganha em abril (PPNG residual = pro-rata de dias intra-mês se fechamento ≠ último dia).

**Retido ≈ Ganho (98-100%)** na Porto Saúde. Gap que aparecer vem tipicamente de cancelamento/estorno do mês ou pequeno ajuste de PPNG residual. Para modelagem, tratar como equivalentes.

## "Outras Receitas Operacionais" — composição em saúde

Em Porto Saúde (e seguradoras de saúde em geral), a linha **Outras Receitas Operacionais** pode somar 8-15% da receita de prêmio. Composição típica:

### 1. Coparticipação (principal)

Usuário paga % do valor do evento (consulta, exame, terapia) no momento do uso — tipicamente 20-40% do custo. Esse pagamento vai **direto à operadora como receita**. Na contrapartida, o sinistro é contabilizado pelo **valor bruto** do evento.

Efeitos no DRE de saúde:
- Infla numerador e denominador da sinistralidade em valores iguais.
- **Reduz** o índice de sinistralidade (denominador maior em % relativo).
- Mitiga moral hazard (usuário paga parte do custo marginal).
- Na Porto Saúde, produtos PME/corporativo têm coparticipação significativa.

### 2. Taxa de administração ASO / autogestão

Empresas grandes que **bancam o próprio risco** contratam seguradoras como TPA (Third Party Administrator). Porto cobra fee de administração (~3-8% do custo assistencial) sem assumir risco. Entra em Outras Receitas porque não é prêmio de risco próprio.

### 3. Glosas recuperadas e descontos negociados com rede

Contas médicas rejeitadas que depois são reembolsadas pelo prestador; descontos retroativos negociados com rede credenciada.

### 4. Pequenos itens

- Taxa de inscrição/adesão (one-off ao entrar no plano)
- Multa/juros de mensalidade atrasada
- Ressarcimento SUS (recuperações)

## Implicação para modelagem

- **Sinistralidade pura**: numerador `sinistro ocorrido bruto`, denominador `prêmio ganho` (**exclua outras receitas do denominador**). Métrica técnica limpa.
- **Margem operacional de saúde**: inclua outras receitas no topo (são lucro real). Porto Saúde reporta **ROL** (Receita Operacional Líquida) = Prêmio Ganho + Outras Receitas − Deduções, e a **Margem EBITDA** sobre essa base.
- **Para BBSE, CXSE**: também têm participação em ramos tradicionais + previdência/VGBL onde Retido/Ganho tem dinâmica própria (previdência tem arrecadação = emitido; resultado do float domina).

## Sinistros — regime de competência (análogo ao prêmio)

Simetria na contabilização do outro lado do DRE:

```
Sinistros Pagos no período
(+) Δ PSL          (Provisão Sinistros a Liquidar — avisados, não pagos)
(+) Δ IBNR         (Incurred But Not Reported — ocorridos, não avisados)
(+) Δ IBNER        (ajuste IBNR após aviso)
(−) Salvados e Ressarcimentos recuperados
(−) Recuperação Resseguro
= Sinistro Ocorrido Retido / Líquido
```

`Sinistro Ocorrido` é a base da [[sinistralidade_auto|sinistralidade]] do período.

Para saúde, terminologia equivalente mas as provisões são:
- **PESL** (Provisão de Eventos Sinistros a Liquidar — como PSL)
- **PEONA** (Provisão de Eventos Ocorridos e Não Avisados — como IBNR)

## Fontes

- Estrutura contábil: Circular SUSEP 517/2015 (tabela contábil padrão). RN ANS 435/2018 para saúde. Porto DFP 2024/2025 para ilustração. (fonte: digested/porto_dfp_2024_summary.md), (fonte: digested/porto_dfp_2025_summary.md)
