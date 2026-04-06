---
type: conceito
source_quality: conceptual
aliases: [Risco Cambial, FX Risk, Exposição Cambial, Risco de Câmbio]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_investment_memo.md
  - wiki/latam.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
updated: 2026-04-05
---

# Risco Cambial

O **risco cambial** (FX risk) é a exposição de uma empresa a variações nas taxas de câmbio que podem afetar negativamente seus resultados, balanço ou fluxo de caixa. Para bancos com operações internacionais — em especial o [[itau]] com presença significativa na [[latam]] — o risco cambial é um fator material de volatilidade de resultado.

## Como Funciona

O risco cambial surge quando há **descasamento de moeda** entre ativos e passivos, receitas e custos, ou entre o momento da transação e o pagamento:

```
Exposição_Cambial = Ativos_em_Moeda_Estrangeira − Passivos_em_Moeda_Estrangeira
                  = Posição_Comprada − Posição_Vendida
```

- **Posição comprada (long FX):** Mais ativos em moeda estrangeira → ganha com depreciação do BRL
- **Posição vendida (short FX):** Mais passivos em moeda estrangeira → perde com depreciação do BRL

## Tipos de Risco Cambial

| Tipo | Definição | Relevância para Bancos |
|------|-----------|----------------------|
| **Risco de transação** | Variação cambial entre a data da operação e o pagamento | Baixo (operações liquidadas rapidamente) |
| **Risco de conversão (translation)** | Variação no valor em BRL de subsidiárias estrangeiras | Alto para ITUB4 (LatAm) |
| **Risco econômico** | Impacto no valor presente dos fluxos futuros da empresa | Relevante para avaliação |

## Itaú Unibanco: Exposição LatAm

O [[itau]] é o banco com maior exposição cambial entre os grandes privados brasileiros, por conta das operações em outros países da [[latam]]:

| País/Região | Moeda | Peso no Resultado |
|-------------|-------|------------------|
| Argentina | ARS (Peso Argentino) | ~5-8% do LL; altamente volátil |
| Chile | CLP (Peso Chileno) | ~3-5% do LL |
| Colômbia | COP (Peso Colombiano) | ~2-3% do LL |
| Peru | PEN (Sol Peruano) | ~2-3% do LL |
| Brasil | BRL | ~80-85% do LL |

### Argentina: Caso Especial

A Argentina representa o risco cambial mais material. O peso argentino sofreu desvalorização de >90% em 2023 (de ~170 ARS/USD para >900 ARS/USD), afetando o resultado da subsidiária em BRL:

- O LL da subsidiária argentina pode ser positivo em ARS mas negativo em BRL quando convertido
- **Hiperinflação:** A Argentina é classificada como economia hiperinflacionária (CPC 42/IAS 29), exigindo ajuste dos demonstrativos pela inflação local antes da conversão — isso mitiga parcialmente (mas não totalmente) o efeito de desvalorização cambial

**Efeito no modelo:** As projeções do NII LatAm usam crescimento YoY em moeda local. O analista deve ajustar pela depreciação esperada do BRL para estimar o NII em BRL.

## Hedges e Gestão de Risco

Bancos grandes usam derivativos para hedgear parcialmente o risco cambial:

```
NDF (Non-Deliverable Forward): trava a taxa de câmbio para uma data futura
Swap cambial: troca fluxos em moeda estrangeira por fluxos em BRL (a uma taxa)
Opções de câmbio: direito (não obrigação) de comprar/vender moeda estrangeira
```

**Filosofia de hedge do Itaú:**
- O banco não busca hedge completo das operações LatAm — entende que parte da exposição é endógena ao negócio
- Usa hedges estratégicos para a exposição de capital (conversão do investimento), não para o NII corrente
- O resultado de hedge aparece no [[nii_mercado]] como "resultado com derivativos de câmbio"

### Efeito do Hedge no Resultado

O custo do hedge cambial (prêmio de forward/opção) é um custo financeiro que reduz o benefício de uma posição comprada em USD. Com BRL/USD em contango (o que ocorre quando a taxa de juros BR é maior que a americana), hedgear uma posição long USD tem custo de carrego:

```
Custo_hedge ≈ (i_BRL − i_USD) × Valor_Hedgeado × Prazo
```

Com i_BRL ~13% a.a. e i_USD ~5% a.a.: custo de hedge de ~8% a.a. em USD. Isso torna o hedge caro e incentiva exposição parcialmente não-hedgeada.

## Impacto na DRE Bancária

O risco cambial aparece na DRE em três linhas principais:

1. **NII Mercado**: Resultado de posições em moeda estrangeira (TVM internacional, derivativos FX)
2. **Resultado de Participações em Coligadas**: Conversão de LL de subsidiárias LatAm para BRL
3. **Outras Receitas/Despesas Operacionais**: Variação cambial de ativos/passivos operacionais

**Volatilidade:** O risco cambial pode gerar tanto ganhos quanto perdas. Em 2023, quando o BRL apreciou vs algumas moedas LatAm, o resultado de conversão do Itaú foi negativo (subsidiárias valiam menos em BRL). Em 2024, com depreciação de moedas LatAm e BRL, o efeito foi mais neutro.

## Risco Cambial nas Incorporadoras

Para [[incorporadoras]] brasileiras, o risco cambial é geralmente baixo (receitas e custos em BRL). Exceções:

- **Materiais de construção importados:** Aço, alumínio, alguns componentes são dolarizados — alta do USD pressiona custos de obra
- **Dívida em USD:** Algumas incorporadoras de médio/alto padrão com emissões de bonds offshore têm dívida em USD hedgeada

**Cyrela:** A [[cyrela]] e a [[cury]] têm custos de construção com componente dolarizado (via INCC, que inclui materiais importados), mas sem exposição de receita em USD. O risco cambial é indireto via inflação de insumos.

## Para o Modelo

Ao projetar resultado do Itaú com operações LatAm:

```
NII_LatAm_BRL(t) = NII_LatAm_MoedaLocal(t) × (1 / Taxa_câmbio_média(t))

Onde:
  NII_LatAm_MoedaLocal = NII_LatAm_MoedaLocal(t-4) × (1 + g_YoY_MoedaLocal)
  Taxa_câmbio_média = taxa de conversão média do trimestre (não a do último dia)
```

**Simplificação prática:** Dado que Brasil representa ~80-85% do resultado do Itaú, e o risco LatAm é parcialmente hedgeado e diversificado entre moedas, o efeito cambial tende a ser uma fonte de volatilidade de curto prazo mas não um driver estrutural do valuation.

## Ver Também

- [[latam]] — operações internacionais do Itaú e Bradesco na América Latina
- [[risco_mercado]] — framework amplo de riscos de mercado (câmbio + juros + ações)
- [[nii_mercado]] — onde resultado de posições cambiais aparece na DRE
- [[itau]] — maior exposição cambial entre os bancos privados BR (LatAm)
- [[banking]] — estrutura da DRE e gerenciamento de risco
- [[duration]] — risco de taxa de juros (complementar ao cambial)
