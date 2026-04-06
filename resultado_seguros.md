---
type: conceito
source_quality: conceptual
aliases: [Resultado de Seguros, Insurance Result, Resultado Seguros Previdência Capitalização]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/extraction/BBDC4_historical_financials_2022_2025.json
updated: 2026-04-05
---

# Resultado de Seguros

O **resultado de seguros** é a contribuição líquida das operações de seguros, previdência e capitalização (SPC) para o lucro de um banco. Para os grandes conglomerados financeiros brasileiros, seguros é um segundo negócio dentro do banco — diversificador de receita menos sensível à [[selic]] e ao [[custo_risco]] do crédito. A forma de consolidação (integral vs equity method) impacta diretamente a estrutura da DRE.

## Como Funciona

```
Resultado_Seguros = Prêmios_Ganhos
                  - Sinistros
                  - Despesas_de_Comercialização
                  - Despesas_Administrativas_de_Seguros
                  + Resultado_Financeiro_da_Seguradora
```

Métricas-chave do negócio de seguros:

| Métrica | Fórmula | Referência |
|---------|---------|-----------|
| Combined Ratio | (Sinistros + Despesas) / Prêmios | < 100% = lucro técnico |
| Loss Ratio | Sinistros / Prêmios | Varia por ramo |
| Resultado Financeiro | Rendimento das reservas técnicas | Sensível à [[selic]] |

**Nota importante**: resultado financeiro das reservas técnicas é positivamente correlacionado com [[selic]] alta — diferente do crédito, aqui Selic alta ajuda a seguradora.

### Formas de Consolidação na DRE Bancária

| Método | Onde Aparece na DRE | Exemplo |
|--------|---------------------|---------|
| Consolidação integral | Linha "Resultado de Seguros" — dentro da receita total | [[bradesco]] (Bradesco Seguros 100%) |
| Equity method | Linha de equivalência patrimonial — abaixo do resultado operacional | [[itau]] ([[porto_seguro]] ~46%) |

Essa diferença é crítica para comparação de IE entre bancos: o Itaú reporta Porto Seguro na equivalência patrimonial (abaixo da linha), portanto **não** entra no denominador nem no numerador do IE. Bancos com seguros consolidados parecem ter IE pior, mas têm mais receita de seguros incluída.

## No Contexto Brasileiro

- **Ramos principais**: auto, vida, habitacional, rural, saúde, previdência aberta.
- O mercado de seguros brasileiro cresceu ~15% em 2025, beneficiado por penetração ainda baixa e crescimento da classe média.
- **Bancassurance** (venda de seguros pela rede bancária) é o canal dominante para grandes bancos — custo de distribuição baixo, cross-sell de clientes existentes.
- **Porto Seguro** (PSSA3) é o maior player privado independente, com JV com Itaú nos ramos de auto/residencial/PME.
- Resultado financeiro das reservas é sensível à [[selic]]: Selic alta → rendimento das reservas técnicas sobe → resultado financeiro de seguros melhora.

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | [[porto_seguro]] via equity method — ~R$3,0B de equivalência patrimonial em 4T25 (+130% em 2025). Não entra no IE. Impacto material no LL mas invisível no denominador de receitas. |
| [[bradesco]] | Bradesco Seguros consolidada integralmente. ~25-30% do LL consolidado vem de seguros. Entra no IE (melhora a métrica por ser receita eficiente). |

## PGBL/VGBL e Previdência Aberta

Previdência aberta é um ramo distinto de seguros, operado por entidades abertas de previdência complementar (EAPCs), e precisa ser analisado separadamente de auto/residencial.

### Estrutura por banco

**[[itau]]** — Itaú não consolida previdência via [[porto_seguro]]. A Porto Seguro opera nos ramos de auto, residencial e PME. O Itaú tem sua própria operação de previdência aberta, a **Itaú Vida e Previdência**, que é consolidada diretamente na DRE gerencial do conglomerado. O resultado dessa operação está implícito na linha `resultado_seguros` gerencial do [[itau]] — não é segregado em linha separada no release.

**[[bradesco]]** — A Bradesco Seguros é um dos maiores operadores de PGBL/VGBL do Brasil. Essa posição é um diferencial competitivo: a base de reservas acumuladas ao longo de décadas cria um ativo de gestão recorrente (taxa de administração + resultado financeiro das reservas).

### Produtos: PGBL vs VGBL

| Produto | Dedutibilidade IR | Tributação no Resgate | Perfil |
|---------|-------------------|-----------------------|--------|
| PGBL | Sim — até 12% da renda bruta | Sobre valor total resgatado | Declarantes modelo completo |
| VGBL | Não | Apenas sobre rendimento | Declarantes modelo simplificado / isentos |

- VGBL é mais comum em volume de captação por abranger base mais ampla.
- PGBL é mais eficiente para contribuinte que declara IR completo com renda elevada — benefício fiscal explícito durante acumulação.
- Ambos os produtos crescem estruturalmente com renda e com maior conscientização sobre aposentadoria — mercado ainda de baixa penetração relativa ao PIB vs mercados desenvolvidos.

### Implicação para modelagem

Para o [[itau]], o resultado de previdência própria não é premissa autônoma no modelo — está capturado dentro de `in:resultado_seguros`. Para o [[bradesco]], o resultado de previdência está dentro do `resultado_seguros` consolidado, que representa ~25-30% do LL total.

## Sensibilidade à Selic por Canal

Selic afeta o resultado de seguros por dois canais distintos, com sinais diferentes dependendo do produto.

### Canal 1: Porto Seguro (reservas técnicas de curto prazo)

[[porto_seguro]] mantém reservas técnicas substanciais para honrar sinistros futuros. Essas reservas são aplicadas predominantemente em renda fixa (LFTs, NTN-Bs, fundos DI).

- Reservas técnicas estimadas: ~R$50-60B (estimativa — não divulgado desagregado)
- Com [[selic]] a ~13%, rendimento bruto das reservas: ~R$6,5-7,8B/ano
- O **resultado financeiro das reservas** é a diferença entre esse rendimento e o custo dos produtos (atualização de provisões, benefícios garantidos mínimos)
- Itaú recebe ~46% do lucro líquido total da Porto Seguro via [[equivalencia_patrimonial]]

Portanto: Selic alta → rendimento das reservas sobe → LL Porto Seguro sobe → contribuição via EP ao [[itau]] sobe.

### Canal 2: Previdência própria do Itaú (reservas de longo prazo)

Reservas de PGBL/VGBL também são investidas em renda fixa, mas o comportamento da captação nova é diferente:

- **Selic alta → rentabilidade do portfólio existente melhora** (positivo para resultado financeiro das reservas já acumuladas)
- **Selic alta → competição com produtos de curto prazo** (LCI, CDB, fundos DI) — reduz atratividade de novos aportes em previdência de longo prazo, pois o custo de oportunidade do investidor sobe

Portanto: Selic alta é líquido positivo para o resultado do portfólio existente, com leve pressão negativa na captação nova.

### Resumo de sensibilidade

| Canal | Selic Alta | Selic Baixa |
|-------|-----------|-------------|
| Porto Seguro (reservas técnicas) | Positivo — rendimento das reservas sobe | Negativo — rendimento cai |
| Previdência própria (portfólio existente) | Positivo | Negativo |
| Previdência própria (captação nova) | Leve negativo (concorrência de curto prazo) | Positivo (previdência fica mais atrativa) |
| **Resultado líquido para `resultado_seguros`** | **NET POSITIVO** | **NET NEGATIVO** |

Essa dinâmica é **oposta** à do crédito, onde [[selic]] alta aumenta inadimplência e pressiona [[custo_risco]]. Seguros e crédito têm sensibilidades à Selic com sinais opostos — o que torna a combinação dentro do conglomerado bancário um hedge natural parcial.

## Bradesco vs Itaú: Impacto no IE

A diferença de estrutura de consolidação entre [[bradesco]] e [[itau]] cria um viés sistemático na comparação do [[indice_eficiencia]].

### Fórmula do IE por banco

**[[bradesco]]** consolida Bradesco Seguros integralmente:

```
IE_Bradesco = Despesas_DNDJ / (NII + Fees + Resultado_Seguros_Integral)
```

**[[itau]]** usa equity method para [[porto_seguro]]:

```
IE_Itaú = Despesas_DNDJ / (NII + Fees)
         — Porto Seguro não entra no denominador nem no numerador
```

### O viés de comparação

Comparar IE entre os dois sem ajuste distorce a análise:

- O [[bradesco]] tem mais receita no denominador (seguros integral) → IE parece **pior** (maior %)
- O [[itau]] tem denominador menor → IE parece **melhor** (menor %)
- A diferença não reflete eficiência operacional real — reflete apenas convenção contábil

### Ajuste para comparação justa

Para comparar [[eficiencia_operacional]] entre os dois bancos em base equivalente, o analista deve ajustar o IE do [[itau]] adicionando o resultado_seguros (Porto Seguro) ao denominador:

```
IE_Itaú_ajustado = Despesas_DNDJ / (NII + Fees + Resultado_Porto_Seguro_100%)
                 ≈ 35-36% (estimativa — vs ~38-40% reportado sem ajuste)
```

**Regra prática**: sempre que comparar [[indice_eficiencia]] entre bancos com estruturas de seguros diferentes, verificar o método de consolidação antes de concluir sobre eficiência relativa. Esse ajuste deve ser feito explicitamente no relatório de análise — analistas que ignoram essa diferença chegam a conclusões equivocadas sobre competitividade operacional.

## Modelagem: Como Projetar em 2026+

### Premissa atual

A premissa de modelagem para o [[itau]] é `in:resultado_seguros = ~R$3,0B/ano`, guidance-first, equivalente a ~R$750M/trimestre. Essa premissa incorpora tanto a contribuição da [[porto_seguro]] via equity method quanto o resultado de previdência própria.

### Cenários de stress

**Cenário 1 — Selic cai 200bps (para ~11%):**

- [[porto_seguro]] perde ~R$1,0-1,2B de resultado financeiro das reservas (~estimativa)
- EP do [[itau]] cai ~R$460-550M (~estimativa, aplicando ~46% sobre a queda do LL Porto Seguro)
- `resultado_seguros` cai ~15% vs guidance base
- Não há compensação automática via prêmios — o ajuste de premissas depende de crescimento de carteira

**Cenário 2 — Sinistralidade auto volta a subir (fraudes, catástrofes):**

- Combined ratio da [[porto_seguro]] piora ~5pp
- Resultado técnico cai — parcialmente compensado pelo resultado financeiro das reservas
- Impacto depende do mix de prêmios e da velocidade de reprecificação (renovação anual de apólices)
- Histórico relevante: sinistralidade elevada em 2022-23 (fraudes em auto) pressionou margens; normalização em 2024-25 foi parte do +130% YoY em 2025

### Variáveis de monitoramento (KPIs do canal seguros)

| KPI | O que monitora | Fonte |
|-----|----------------|-------|
| Combined ratio Porto Seguro | Eficiência técnica (sinistros + despesas vs prêmios) | Release PSSA3 |
| % reservas em renda fixa | Sensibilidade à [[selic]] do resultado financeiro | ITR Porto Seguro |
| Crescimento de prêmios emitidos | Volume do negócio técnico | Release PSSA3 |
| Captação líquida previdência | Tração de PGBL/VGBL (canal próprio Itaú) | Release ITUB4 |
| EP Porto Seguro na DRE ITUB4 | Resultado realizado na linha de equivalência | Release ITUB4 |

### Sinal de revisão de premissa

Se combined ratio Porto Seguro ultrapassar ~95% por dois trimestres consecutivos, ou se [[selic]] cair abaixo de 11%, revisar `in:resultado_seguros` para ~R$2,5-2,6B e atualizar `decisions.md` com justificativa.

## Decomposição Disponível por Banco

Estado atual dos sub-dados de seguros nas extrações do modelo:

| Banco | Dados disponíveis | Sub-breakdown | Status |
|-------|-------------------|---------------|--------|
| ITUB4 | `resultado_seguros` (flat, ~R$750M/tri) | Não — Porto Seguro via EP, não detalhado | Modelado como flat premissa |
| BBDC4 | `resultado_seguros` (flat, ~R$5.000-5.700M/tri) | Não — Bradesco Seguros consolidada integral, sem sub-linhas extraídas | Gap de extração |

### Gap BBDC4 — Decomposição Não Extraída

O Bradesco publica em seus releases e ITRs sub-linhas da operação de seguros:
- **Prêmios ganhos** — receita técnica bruta
- **Sinistros retidos** — custo técnico
- **Despesas de comercialização** — custos de venda/distribuição
- **Resultado financeiro de seguros** — rendimento das reservas técnicas (sensível à [[selic]])

Essas sub-linhas estão disponíveis no release da Bradesco Seguros S.A. (subsidiária) e no ITR consolidado, mas não foram extraídas para `BBDC4_historical_gerencial.json`. Atualmente o modelo trata `resultado_seguros` como premissa flat (~R$5.500-6.000M/tri) derivada da média histórica.

**Para implementar decomposição completa:**
1. Extrair sub-linhas do release Bradesco Seguros (quadro "Demonstração de Resultado de Seguros")
2. Adicionar `breakdowns.seguros_breakdown` ao gerencial JSON
3. Atualizar `compute_banking.py` com lógica de decomposição (similar ao fee breakdown)
4. Adicionar nodes no `BBDC4_dependency_graph_v3.json`: `in:premios_ganhos`, `in:sinistralidade_pct`, `in:desp_comerciais_seguros_pct`, `in:resultado_fin_seguros`

**Prioridade:** média — impacto no modelo é baixo enquanto margem técnica seguros for estável (~combined ratio 90-92%). Torna-se relevante em cenários de stress de sinistralidade.

## Ver Também

- [[porto_seguro]] — JV do Itaú, maior player privado de seguros no Brasil
- [[receita_servicos_tarifas]] — outra linha de receita não-NII complementar ao resultado de seguros
- [[eficiencia_operacional]] — consolidação integral de seguros afeta o cálculo do IE
- [[indice_eficiencia]] — ajuste necessário para comparação justa entre bancos com estruturas de seguros distintas
- [[selic]] — Selic alta beneficia o resultado financeiro das reservas técnicas
- [[equivalencia_patrimonial]] — método contábil via qual Porto Seguro entra na DRE do Itaú
- [[banking]] — contexto setorial e estrutura da DRE bancária
