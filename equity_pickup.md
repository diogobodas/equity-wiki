---
type: conceito
source_quality: conceptual
aliases: [Equity Pickup, Equivalência Patrimonial, EP, Equity Method, Resultado de Participações]
sources:
  - sectors/real_estate/sector_profile.md
  - wiki/equivalencia_patrimonial.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/model/CURY3_model.json
  - sectors/real_estate/companies/DIRR3/outputs/model/DIRR3_model.json
updated: 2026-04-05
---

# Equity Pickup

**Equity Pickup** é um sinônimo usado em análise financeira anglófona para o resultado de **equivalência patrimonial (EP)** — o lucro (ou prejuízo) proporcional que uma empresa reconhece de suas participações em outras empresas onde detém influência significativa, mas sem consolidação integral.

## Relação com Equivalência Patrimonial

Os dois termos são intercambiáveis no contexto do equity research brasileiro:

- **Equivalência Patrimonial (EP)**: termo contábil oficial (CPC 18 / IAS 28)
- **Equity Pickup**: terminologia de mercado, vinda do inglês

Para detalhes completos sobre a mecânica contábil, fórmulas e impactos no modelo, ver [[equivalencia_patrimonial]].

## Resumo da Mecânica

```
EP = Participação (%) × LL_investida
```

O resultado é reconhecido na DRE da investidora **independentemente de distribuição de dividendos**. O valor contábil do investimento no balanço sobe com o equity pickup e cai quando dividendos são recebidos.

## Uso no Contexto de Equity Research

O termo "equity pickup" é comum em:

1. **Modelos de banco de investimento:** Linhas de DRE que mostram contribuição de subsidiárias ou coligadas
2. **Análise de conglomerados:** Valuation de grupos com múltiplas participações (soma de partes)
3. **Modelagem de incorporadoras:** [[cyrela]] tem equity pickup relevante via [[cury]], [[lavvi]] e [[plano_plano]]

### Exemplo — Cyrela

A [[cyrela]] tem ~23% da [[cury]] (Cury Construtora) e participações em joint ventures ([[lavvi]], [[plano_plano]]). O equity pickup trimestral pode representar R$150-200M do LL total da Cyrela, tornando-o material para o modelo.

```
EP_Cyrela ≈ 23% × LL_Cury + % × LL_Lavvi + % × LL_P&P
```

### Exemplo — Itaú (Banking)

O [[itau]] tem participações em empresas de tecnologia e alguns negócios via equity method. Para bancos, a [[equivalencia_patrimonial]] é geralmente menos material do que para incorporadoras, mas pode aparecer em:
- Participações em consórcios financeiros
- Investimentos em fintechs estratégicas
- Coligadas no exterior

## Distinção Importante: EP vs Consolidação

| Tipo de Participação | Tratamento | Aparece como |
|---------------------|------------|--------------|
| >50% (controlada) | Consolidação integral | Receitas/custos da controlada entram linha a linha |
| 20-50% (coligada/significativa) | Equity method | Apenas o lucro proporcional na linha "EP" |
| <20% (investimento financeiro) | Custo ou valor justo | Dividendo ou variação de valor justo |

## Equity Pickup no Processo de Modelagem

### Onde Aparece na DRE

```
EBIT
(+/-) Equity Pickup / Equivalência Patrimonial    ← aqui
= EBT
(-) IR/CSLL
= LL
```

O equity pickup entra **após** o EBIT e **antes** do IR. Isso significa que ele não afeta o resultado operacional, mas impacta o resultado antes dos impostos — e portanto o IR sobre o conjunto.

### Tratamento Fiscal

O equity pickup, em si, **não é tributado separadamente**: os dividendos de coligadas já tributadas na fonte são isentos na investidora (princípio da não bitributação). Por isso, o equity pickup de empresas que pagaram IR localmente é excluído da base tributável da investidora, reduzindo a alíquota efetiva consolidada.

**Para o modelo:** O equity pickup geralmente reduz a [[aliquota_efetiva]] porque:
- O lucro da investida já foi tributado "lá dentro"
- A linha EP na DRE entra isenta de IR adicional
- Isso dilui a alíquota média consolidada

### Projeção do Equity Pickup

Para projetar o equity pickup de uma investida listada:

```
EP_trimestral = LL_investida(t) × % Participação

LL_investida = projetar via modelo da investida, ou usar consenso Bloomberg
```

Para a [[cyrela]], com participação em [[cury]] (~18%), [[lavvi]] e [[plano_plano]]:

```
EP_CYRE3 = 18% × LL_CURY3 + %Lavvi × LL_Lavvi + %P&P × LL_P&P
```

**Desafio:** LL de empresas menores ([[lavvi]], [[plano_plano]]) não tem consenso público. Usar guidance de VGV + margem implícita como proxy.

## Quando o Equity Pickup é Negativo

O equity pickup pode ser negativo quando a investida tem prejuízo. No balanço, o valor do investimento cai abaixo de zero — nesse ponto, o investidor para de reconhecer prejuízo adicional (limite do valor contábil do investimento). Qualquer perda adicional da investida é ignorada, a não ser que o investidor tenha garantias ou obrigações com a investida.

**Exemplo prático:** Se a [[alea]] (subsidiária da Tenda, não coligada) tivesse prejuízo maior que o capital investido, a Tenda teria de avaliar se continua injetando capital. Isso é uma decisão de M&A, não contábil automático.

## Exemplo — Direcional (DIRR3)

A [[direcional]] (DIRR3) tem uma dinâmica diferente: a parceria com a Riva (submarca mid-income) é consolidada integralmente (não via equity pickup), mas existem **participações minoritárias** na DRE que funcionam como o inverso — a Riva gera lucro do qual parte vai para minoritários. Isso reduz o LL atribuível à DIRR3.

```
LL_DIRR3 = LL_consolidado − Minoritários_Riva − Minoritários_outros_SPEs
```

A distinção importante: DIRR3 não usa EP (pois a Riva é consolidada, não via equity method), mas o conceito de partilha de resultado entre controladora e sócios é análogo.

## Equity Pickup no Balanço

No balanço patrimonial, o investimento avaliado pelo equity method está registrado no ativo não circulante (investimentos). A evolução do saldo é:

```
Investimento(t) = Investimento(t-1) + EP(t) − Dividendos_recebidos(t)
```

**Sinal de atenção:** Se a investida retém lucro (não distribui dividendos), o investimento cresce no balanço da investidora. Se a investida distribui todo o lucro, o investimento permanece estável. Para fins de fluxo de caixa, apenas dividendos recebidos são FCO — o equity pickup em si não gera caixa.

**Impacto no FCO (Fluxo de Caixa das Operações):**

```
FCO ajustado = LL − EP (adicionado de volta) + Dividendos_recebidos_das_investidas
```

Esta reconciliação aparece na demonstração de fluxo de caixa da investidora.

## Materialidade por Empresa

| Empresa | Investidas | EP Anual Estimado | % do LL Consolidado |
|---------|-----------|-------------------|---------------------|
| [[cyrela]] | [[cury]] (~18%), [[lavvi]] (~30%), [[plano_plano]] (~50%) | ~R$500-600M/ano | ~30-35% do LL |
| [[direcional]] | Sócios em SPEs (minoritários) | N/A (minority interest, não EP) | — |
| [[cury]] | Sem investidas listadas | ~R$0 | — |
| [[itau]] | Porto Seguro (~46%), XP Investimentos, etc. | ~R$3.5-4.5B/ano | ~7-10% do LL |
| [[bradesco]] | Bradesco Seguros (consolidado) | N/A (consolidado) | — |

## Ver Também

- [[equivalencia_patrimonial]] — descrição completa da mecânica contábil e modelagem
- [[cyrela]] — EP relevante via Cury, Lavvi e P&P (~R$550M/ano)
- [[cury]] — principal investida da Cyrela (equity pickup material)
- [[direcional]] — minoridades Riva; análogo ao EP mas pela rota da consolidação
- [[incorporadoras]] — setor onde EP costuma ser material (JVs, SPEs)
- [[itau]] — EP de Porto Seguro (~R$3B/ano); menor materialidade relativa ao LL bancário
- [[porto_seguro]] — investida do Itaú; EP de ~46% do LL da Porto
- [[aliquota_efetiva]] — EP isenta de bitributação reduz alíquota efetiva consolidada
- [[ll]] — EP entra no cálculo do LL como resultado não-operacional pré-IR
- [[fluxo_de_caixa]] — EP não é caixa; somente dividendos recebidos entram no FCO
