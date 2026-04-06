---
type: empresa
source_quality: conceptual
aliases: [Porto Seguro, PSSA3, Porto Seguro Seguros]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_investment_memo.md
  - wiki/itau.md
updated: 2026-04-05
---

# Porto Seguro

A **Porto Seguro** (PSSA3) é a maior seguradora privada independente do Brasil, líder nos ramos de seguros auto e residencial. Opera via joint venture com o [[itau|Itaú Unibanco]], que detém aproximadamente 46% do capital. A participação aparece na DRE do Itaú como **equivalência patrimonial** — não é consolidada integralmente, o que diferencia a estrutura contábil do Itaú em relação ao [[bradesco]] (que consolida a Bradesco Seguros integralmente).

## Como Funciona

Porto Seguro opera como empresa independente listada (PSSA3). O Itaú detém ~46% via JV que inclui:
- Seguros auto
- Seguros residencial
- Seguros PME (empresarial)
- Porto Saúde (saúde)
- Porto Serviços (serviços de assistência)

```
Contribuição para LL Itaú = Lucro_Porto_Seguro × 46% (equity method)
```

Esse resultado aparece na linha de **Equivalência Patrimonial** da DRE do Itaú — abaixo do resultado operacional, portanto **não entra no cálculo do [[eficiencia_operacional|índice de eficiência]]** e **não entra no NII nem na receita total gerencial**.

### Por Que Não É Consolidada

O Itaú não tem controle societário (46% não é maioria). O tratamento correto pelo IFRS (IAS 28) é equity method. Isso significa:
- Receitas e despesas da Porto Seguro **não aparecem** na DRE consolidada do Itaú
- Apenas o resultado líquido proporcional aparece como EP
- O balanço do Itaú mostra "Investimento em Porto Seguro" no ativo como participação permanente

## Estrutura da JV

A joint venture entre Itaú e a família Garfinkel (fundadores da Porto Seguro) foi estruturada para que o Itaú capture os benefícios econômicos da parceria sem assumir o controle operacional.

**Composição acionária aproximada**:
- Família Garfinkel (controladores): ~54%
- [[itau|Itaú Unibanco]]: ~46%
- Free float PSSA3: incorporado na fatia da família via estrutura de holdings

**Governança**:
- Conselho de Administração tem representação do Itaú, mas sem maioria
- Decisões estratégicas (pricing, expansão de ramos, M&A) são prerrogativa dos controladores
- O Itaú não pode consolidar nem direcionar operações — relação é de investidor financeiro com influência significativa (IAS 28), não controlador (IFRS 10)

**Racional da estrutura**:
- Para o Itaú: acesso ao resultado de seguros sem absorver o risco regulatório/operacional de uma seguradora de grande porte no balanço. Evita capital regulatório adicional que consolidação exigiria.
- Para a Porto Seguro: acesso à base de clientes do Itaú (cross-sell via agências e digital) e parceria de distribuição sem perder independência de gestão.
- Para o mercado: duas empresas listadas com teses de investimento distintas — ITUB4 (banco) vs. PSSA3 (seguradora).

## Drivers do Resultado

O resultado que se transforma em EP para o Itaú pode ser decomposto em duas partes:

### Resultado Técnico

```
Resultado_Técnico = Prêmios_Ganhos − Sinistros − Despesas_Comercialização − Despesas_Admin
```

- **Prêmios ganhos**: crescimento de carteira (novos contratos, renovações, inflação de preços)
- **Sinistros**: componente mais volátil — influenciado por frequência de acidentes (auto), clima (residencial), fraudes
- **Índice combinado**: métrica-chave de eficiência técnica. < 100% = rentabilidade técnica positiva

### Resultado Financeiro das Reservas

```
Resultado_Financeiro = Reservas_Técnicas × CDI_médio_período
```

- Reservas técnicas estimadas em ~R$50–60B (estimado)
- Aplicadas majoritariamente em renda fixa (LFTs, NTN-Bs, CDBs) — estruturalmente atreladas ao [[selic|CDI/Selic]]
- Com [[selic|Selic]] em ~13,25% (2025): R$50–60B × 13,25% ≈ R$6,6–7,9B de resultado financeiro bruto (estimado, pré-IR)

### Fórmula Consolidada

```
EP_Itaú = (Resultado_Técnico + Resultado_Financeiro − IR_Porto_Seguro) × 46%
```

**Sensibilidade à [[selic|Selic]]**: variação de +100 bps na Selic implica:
- Reservas ~R$50–60B × 1,0% = ~R$500–600M adicionais de resultado financeiro bruto (estimado)
- Após IR (~34%): ~R$330–400M líquido
- Participação Itaú (46%): ~R$150–180M adicionais no EP (estimado)

Isso torna a Porto Seguro um **amplificador de Selic** para o LL do Itaú — efeito oposto ao de um banco puro (que sofre com Selic alta via inadimplência e custo de funding).

## Por Que 2025 Foi Excepcional (+130% YoY)

O EP de Porto Seguro para o Itaú saltou ~+130% em 2025 versus 2024, atingindo ~R$3,0B no ano. Três fatores simultâneos explicam a magnitude:

1. **Normalização da sinistralidade auto**: Em 2022–2023, o mercado sofreu com anomalia de fraudes (principalmente no ramo auto), que elevou a sinistralidade a níveis historicamente altos. Em 2024–2025, os controles foram reforçados e a frequência de sinistros voltou ao padrão histórico → queda expressiva no índice combinado.

2. **[[selic|Selic]] alta gerando retorno elevado nas reservas**: Com a Selic acima de 13% durante quase todo 2025, o resultado financeiro das reservas (~R$50–60B estimado) ficou substancialmente acima da média histórica dos anos de juro baixo (2020–2021: Selic 2–4,5%).

3. **Crescimento de prêmios ganhos**: Expansão da base de contratos (Porto Saúde, PME, auto) e reajustes de preço acima da inflação — refletindo poder de precificação em mercado concentrado.

A base de comparação era deprimida (2024 ainda sofrendo resíduos das fraudes auto + Selic em processo de alta), o que amplifica o YoY.

## No Contexto Brasileiro

- **Fundada em 1945**, é referência em longevidade e marca no mercado de seguros.
- Ticker **PSSA3** na B3 — tem free float próprio e é acompanhada como ativo independente.
- **Resultado financeiro das reservas técnicas**: Selic alta aumenta o rendimento das reservas → resultado Porto Seguro melhora → EP do Itaú cresce.
- **4T25**: Porto Seguro contribuiu fortemente para o [[resultado_seguros]] do Itaú — EP de ~R$3,0B no ano (+130% YoY em 2025), impulsionado por resultado técnico forte e rendimento de reservas com Selic em 13,25%.
- Sinistralidade auto se normalizou pós-2024 (pós-anomalia de fraudes 2022-23).

## Modelagem no ITUB4

No modelo do [[itau|ITUB4]], o resultado da Porto Seguro entra como linha dedicada `resultado_seguros` (equivalência patrimonial).

**Premissa no grafo**: `in:resultado_seguros`

**Guidance 2026**: ~R$3,0B/ano → **~R$750M/trimestre** como premissa base.

**Como projetar**:
- Usar guidance da administração como premissa primária (quando disponível)
- Fallback: manter nível 2025 com ajuste de Selic esperada (sensibilidade ~R$150–180M por 100 bps, estimado)
- Não modelar de baixo para cima (resultado técnico + financeiro + IR) sem dados granulares da Porto Seguro — complexidade desproporcional ao ganho de precisão

**O que monitorar a cada resultado**:
- Índice combinado da Porto Seguro (divulgado no release PSSA3)
- Variação de Selic esperada para os próximos trimestres
- Crescimento de prêmios emitidos (proxy de crescimento de receita)
- Sinistralidade auto (leading indicator de pressão ou normalização)

**Variável no modelo**: `resultado_seguros` aparece como item abaixo do resultado operacional, somando diretamente ao lucro antes de IR — **não** passa pelo NII nem pela receita de serviços.

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | Detém ~46% da Porto Seguro via JV. Contabiliza como equivalência patrimonial. R$3,0B de EP em 2025 — item material no LL. Não consolidada — importante para análise do IE. |

## Ver Também

- [[resultado_seguros]] — EP do Porto Seguro é o [[resultado_seguros]] do Itaú
- [[eficiencia_operacional]] — Porto Seguro via equity method NÃO entra no cálculo do IE do Itaú
- [[itau]] — empresa que detém ~46% da Porto Seguro
- [[selic]] — Selic alta melhora resultado financeiro das reservas técnicas
- [[banking]] — contexto setorial
