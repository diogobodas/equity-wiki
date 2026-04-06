---
type: empresa
source_quality: partial
aliases: [Cyrela, CYRE3, Cyrela Brazil Realty]
sources:
  - sectors/real_estate/companies/CYRE3/outputs/model/CYRE3_investment_memo.md
  - sectors/real_estate/companies/CYRE3/outputs/index.md
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CYRE3/outputs/model/CYRE3_model.json
updated: 2026-04-05
---

# Cyrela Brazil Realty (CYRE3)

**Cyrela** é a maior incorporadora diversificada do Brasil por patrimônio e relevância de marca, com presença em alta renda (marca Cyrela), médio padrão (Living), econômico/MCMV (Vivaz) e participações estratégicas em empresas listadas. É o modelo mais complexo do universo coberto por ter EP exógena material e uma subsidiária financeira (CashMe).

## Tese de Investimento

A tese central é a **expansão de Vivaz no segmento privado** (fora MCMV), que compensa a desaceleração do médio-alto padrão em 2026. A empresa tem posição única: participações em [[cury]], [[lavvi]] e [[plano_plano]] geram EP exógena significativa (~R$550M/ano), e a política de não crescer PL garante retorno ao acionista via dividendos + recompra + venda de ações de JVs.

## Modelo de Negócio

### Segmentos Principais

| Segmento | Marca | Foco | INCC Exposição |
|----------|-------|------|----------------|
| Alta-renda | Cyrela | SP (bairros tradicionais: Moema, V. Olímpia, Perdizes) | Protegida |
| Médio-padrão | Cyrela Living | Lajes e locação | Protegida |
| Econômico/MCMV | Vivaz | Periferia SP + outras cidades | 100% exposta (MCMV) |

### EP Exógena — Diferencial Estrutural

Cyrela possui participações em empresas listadas que geram Equivalência Patrimonial trimestral:

| Investida | Participação Aprox. | Resultado EP/ano (estimado) |
|-----------|--------------------|-----------------------------|
| [[cury]] (CURY3) | ~18% (saindo do conselho) | Material |
| [[lavvi]] | Minority stake | Material |
| [[plano_plano]] (PLPL3) | Controlling minority | Material |

**EP total exógena ~R$550M/ano** — é item material da DRE e deve ser decomposto por investida no modelo. A saída gradual do conselho da Cury (2026) implica redução do % de participação reconhecido.

### CashMe — Subsidiária Financeira

A CashMe é uma plataforma de crédito imobiliário (empréstimo com garantia de imóvel — home equity) controlada pela Cyrela. Distorce o resultado financeiro da Cyrela quando analisado de forma consolidada:
- Aumenta as receitas financeiras (carteira de crédito própria)
- Aumenta as despesas financeiras (captação de funding)

**Regra de análise:** Sempre modelar resultado financeiro **ex-CashMe** para entender a dinâmica da incorporadora. A dívida líquida relevante para covenant é **DL/PL ex-CashMe**.

## Métricas-Chave (Modelo 2026E/27E)

| Métrica | 26E | 27E |
|---------|-----|-----|
| Receita Líquida | R$11.026M | R$11.117M |
| EBIT | R$2.597M | R$2.758M |
| Lucro Líquido | R$2.022M | R$2.220M |
| Margem Líquida | 18,3% | 20,0% |
| ROE | 17,1% | 16,3% |

**vs Bloomberg Consensus (14 analistas):**

| Métrica | Modelo 26E | BBG 26E | Diferença |
|---------|-----------|---------|-----------|
| Receita | R$11.026M | R$10.322M | +6,8% |
| EBIT | R$2.597M | R$2.189M | +18,6% |
| LL | R$2.022M | R$1.992M | +1,5% |

O gap de EBIT maior que o gap de receita reflete diferença de convenção (nosso EBIT = LB + opex; BBG pode usar EBITDA − D&A).

## Premissas Principais (2026)

### VGV por Segmento (decomposição no grafo)

O modelo decompõe o VGV lançado em 3 segmentos, permitindo cenários de mix:

| Segmento | Default (R$M/tri) | % do Total | Tendência |
|----------|-------------------|-----------|-----------|
| [[alto_padrao]] (Cyrela) | 2.041 | 56,7% | Core estável; terrenos SP escassos |
| Médio padrão (Living) | 594 | 16,5% | Complementar; volume menor |
| [[mcmv]] (Vivaz) | 965 | 26,8% | Crescendo: de 10% (2022) para 29% (2025) |
| **Total** | **3.600** | **100%** | Guidance XP: R$11,5B/ano (2026E) |

Vivaz Prime descontinuado (0 desde 3T22). Calibração: média 1T24-4T25 sobre 28 trimestres de dados.

### Outras Premissas

| Premissa | Valor | Justificativa |
|----------|-------|---------------|
| Margem bruta % | 33,0% | Histórico estável 32-33%; mix Vivaz crescente favorece |
| VSO 100%/tri | 20,0% | Desaceleração reportada (management mar/2026: 40-50% no 1o mês) |
| Payout | 40% | Objetivo de não crescer PL; mínimo + JVs + venda de ações |
| EP share % | 18% | Saída do conselho Cury; Vivaz 100% consolidado |

## WC e Estrutura Financeira

- **Dias recebíveis:** ~200 dias (alta variância por EP e CashMe)
- **Dias estoques:** ~350 dias (landbank SP, empreendimentos de ciclo longo)
- **Covenant:** DL/PL ex-CashMe (D&A imaterial, não usa EBITDA)
- **Dívida:** Mix SFH + corporativa (debêntures, CRI)

## Riscos Principais

1. **VSO continua caindo:** se desacelerar abaixo de 18%, backlog não repõe e receita cai em 2027
2. **Alvarás SP:** crítico para Vivaz (precisa lançar a cada 30-60 dias); liminar 2026 pode atrasar 15%
3. **PEC 6x1:** impacto maior em alvenaria estrutural (Vivaz/Living); estrutura convencional Cyrela (médio-alto) tem menor impacto
4. **Estoque pronto:** 2025 ruim (-30% vs meta); desconto significativo início 2026
5. **Médio-alto volumes menores:** pipeline difícil de repor após perda de terreno grande

## Sensibilidades

| Variável | Cenário | Impacto LL |
|----------|---------|-----------|
| VSO -2pp (18%) | Mercado piora | -~R$60M |
| Margem +1pp (34%) | Mix Vivaz favorável | +~R$95M |
| Selic +2pp | Custo dívida sobe | -~R$80M |
| Venda ações JVs R$270M | Prejuízo fiscal | +R$270M caixa (sem IR) |

## Fontes do Mosaico

- Reunião com Miguel (CEO) 25/Mar/2026 — VSO, Vivaz, estoque pronto, alvarás, JVs, payout
- Call de Resultados 4T25 (04/Mar/2026)
- Dados CVM ITR/DFP 1T23-3T25 (9 trimestres reais)
- Releases trimestrais 1T23-4T25

## Cyrela vs Peers: Por Que É o Caso Mais Complexo

A Cyrela é fundamentalmente diferente das peers pelo grau de complexidade e pelo nível de capital gerenciado:

| Dimensão | Cyrela | [[cury]] | [[direcional]] | [[tenda]] |
|----------|--------|--------|------------|-------|
| Segmentos | 3 (Alta + Living + Vivaz) | 1 | 2 | 2 |
| EP exógena | ~R$550M/ano (Cury, Lavvi, P&P) | 0 | 0 | 0 |
| Subsidiária financeira | CashMe (crédito imobiliário) | Não | Não | Não |
| Landbank | Grande, SP premium | Médio, SP/RJ | Muito grande, Nacional | Médio, SP/SE |
| Ciclo de obra | 30-36 meses (alta-renda) | 18-20 meses | 24-30 meses | 24-28 meses |

**Consequência para modelagem:** A Cyrela tem ~20 premissas explícitas no modelo vs ~6 da Cury. O consenso Bloomberg erra mais a Cyrela (receita +6,8% vs consenso em 2026E vs -2,8% para Cury). O risco de projeção é estruturalmente maior.

## A Política de Não Crescer PL

O management da Cyrela tem uma filosofia incomum: **não crescer o patrimônio líquido de forma desnecessária**. Em vez de reter lucros para financiar crescimento, a empresa:

1. Distribui dividendos generosamente (payout ~40-50%)
2. Vende participações em JVs quando estão lucrativas (ex: venda de ações CURY3)
3. Recompra ações quando trading abaixo do NAV

**Efeito no valuation:** Com PL relativamente estável, o ROE se mantém elevado (~17-18%). Isso cria um ciclo virtuoso onde a empresa não precisa acumular capital para crescer — usa o balanço eficientemente e distribui o excesso.

**Risco:** Se a empresa precisar crescer investimento em Vivaz (que requer capital para terrenos) sem elevar o PL, pode precisar de mais dívida. O covenant é DL/PL ex-CashMe.

## EP Exógena: A Vantagem Oculta

A EP exógena da Cyrela (~R$550M/ano) é amplamente ignorada pelo mercado, que foca no resultado operacional da incorporação. Mas é um item material:

- **Como % do LL:** R$548M (2025A) / LL total ~R$2.022M (26E) = ~27% do LL vem de EP exógena
- **Sensibilidade:** Se Cury (principal investida) bater guidance, a EP cresce; se decepcionar, a EP cai. Isso cria correlação positiva entre o valuation das duas empresas.
- **Tendência:** A Cyrela está saindo do conselho da Cury progressivamente. Isso pode reduzir o % reconhecido pela equivalência patrimonial no futuro.

**Para o modelo:** A EP exógena deve ser decomposta por investida (Cury, Lavvi, P&P), projetada com base no guidance de cada empresa e na % de participação. Não usar um número consolidado fixo.

## Ver Também

- [[incorporadoras]] — hub setorial; Cyrela como caso de maior complexidade
- [[cury]] — principal investida (EP exógena ~R$550M/ano)
- [[equivalencia_patrimonial]] — mecânica contábil da EP exógena; crítico para Cyrela
- [[equity_pickup]] — sinônimo anglófono de equivalência patrimonial
- [[margem_backlog]] — indicador leading de margem; alto padrão gap ~-3,5pp
- [[poc_revenue]] — ciclo longo ~36 meses; backlog grande relativo à receita
- [[vgv_lancamentos]] — pipeline de receita futura; ~R$3-4bi/tri
- [[velocidade_vendas]] — VSO ~18-22%; driver crítico para 2026
- [[mcmv]] — Vivaz é o braço MCMV da Cyrela; 100% exposta ao INCC
- [[incc]] — corrói margem Vivaz; protege parcialmente Cyrela alta-renda
- [[capital_de_giro]] — WC maior do setor por ciclos longos e tickets altos
- [[ll]] — LL 26E R$2.022M; ~27% vem de EP exógena
