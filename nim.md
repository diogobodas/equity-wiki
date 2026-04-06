---
type: conceito
source_quality: conceptual
aliases: [NIM, Net Interest Margin, Margem de Juros Líquida, Margem Financeira]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/BBDC4/outputs/model/BBDC4_model.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_historical_gerencial.json
updated: 2026-04-05
---

# Net Interest Margin (NIM)

O **NIM** (Net Interest Margin / Margem de Juros Líquida) é a rentabilidade dos ativos remunerados do banco — a diferença percentual entre o yield médio do ativo (crédito + TVM) e o custo médio do funding. É a métrica de precificação central do negócio bancário.

## Como Funciona

```
NIM = NII_Total / Ativos_Remunerados_Médios
    = (NII_Clientes + NII_Mercado) / Ativos_Remunerados_Médios
```

Onde **Ativos Remunerados** incluem: carteira de crédito + TVM + compulsórios remunerados + aplicações interfinanceiras.

**Decomposição alternativa:**

```
NIM = Yield_Ativo - Custo_Funding
    = (Receita_Intermediação / Ativo_Remunerado) - (Despesa_Intermediação / Passivo_Remunerado)
```

O NIM é portanto determinado por:
1. **Volume**: Ativos remunerados totais (carteira de crédito + TVM)
2. **Mix**: Composição entre segmentos de alto vs baixo spread
3. **Preço**: [[selic]] + spreads específicos por produto

### NIM × NII

NIM é uma porcentagem; NII é o valor monetário. Na modelagem:

```
NII(t) = Ativo_Remunerado_Médio(t) × NIM(t)
```

O NIM pode ficar estável enquanto o NII cresce (se o portfólio cresce). Ou o NIM pode subir enquanto o NII fica estável (se o portfólio encolhe). Sempre analisar os dois conjuntamente.

## No Contexto Brasileiro

**Range típico para grandes bancos (2024-2026):**
- NIM consolidado: 10-14% a.a.
- NIM só carteira de crédito: 12-16% a.a.
- NIM ajustado pelo risco (NIM − custo do crédito): 7-10% a.a.

**NIM ajustado pelo risco** é mais relevante para comparações porque elimina o efeito de bancos que inflam o NIM bruto tomando mais risco de crédito:

```
NIM_ajustado = NIM - Custo_Risco
```

### Drivers de Compressão de NIM

| Driver | Efeito no NIM | Observação |
|--------|--------------|------------|
| Queda da [[selic]] | Comprime (especialmente NII Mercado) | TVM pós-fixado rende menos; spreads caem com concorrência |
| Mix shift para menor risco | Comprime (menor spread) | Ex: mais consignado e menos cartão pessoal |
| Maior crescimento de grandes empresas (atacado) | Comprime (CDI+1-3% vs varejo) | Porém menor [[custo_risco]] |
| Maior concorrência (fintechs) | Comprime (spreads de serviços) | Especialmente em crédito pessoal e PME |
| Alta da [[selic]] | Expande (se ativo reprecia antes) | Depende do repricing gap do banco |

### Sensibilidade a Selic

Os bancos publicam sensibilidade do NII a variações de ±100bps na Selic. Para modelagem de cenário:

```
NII_cenário = NII_base + n_bancos × (ΔSelic_bps / 100) × Sensibilidade_100bps
```

## Variações de Base por Banco

**CRÍTICO**: Cada banco calcula o NIM usando denominadores diferentes. Comparações diretas sem ajustar o denominador são enganosas.

| Banco | Denominador Usado | NIM Resultante | Comentário |
|-------|------------------|---------------|------------|
| [[bradesco]] (BBDC4) | **Saldo médio da carteira** (publicado diretamente no release, p.9 Margem Financeira) | ~9% a.a. NII Clientes / Saldo Médio | Menor porque o denominador é só carteira de crédito; mais transparente |
| [[itau]] (ITUB4) | **Carteira sensível** (reconstruída; inclui operações LatAm e TVM sensíveis a spread) | ~12% a.a. | Maior porque inclui ativos de maior spread no numerador |
| [[sanb11]] (SANB11) | **Carteira ampliada** (inclui avais, garantias, ACC/ACE — ~R$140B a mais) | ~10.7% reportado | NIM implícito sobre carteira pura de crédito: ~11.5% |

**Implicação prática:**
- O NIM de 12% do Itaú não é diretamente comparável com os 9% do Bradesco
- O Itaú inclui no denominador ativos que o Bradesco exclui
- Para comparação justa: calcular NIM sobre carteira de crédito pura para todos os bancos

**Regra de uso no modelo:**
- Para ITUB4: usar o NIM implícito calibrado histórico (~12%), pois o modelo projeta NII via YoY de `nii_clientes`
- Para BBDC4: usar o saldo médio publicado no release diretamente — não precisar reconstruir
- Para SANB11: usar carteira gerencial de crédito (~R$566B) como denominador, não a carteira ampliada

## Por Empresa

| Empresa | NIM (2025) | Base | Característica |
|---------|-----------|------|----------------|
| [[itau]] | ~12% a.a. | Carteira sensível (~R$1.28T) | NIM estável a crescente; mix de carteira equilibrado entre varejo rentável e atacado. Beneficia de patamar de Selic elevado via NII Mercado (tesouraria). |
| [[bradesco]] | ~9% a.a. NII Clientes/Saldo Médio | Saldo médio publicado | NIM em recomposição. Ciclo 2022-23 comprimiu o NIM efetivo. Recuperação via mix shift e redução de [[custo_risco]]. |
| [[sanb11]] | ~10.7% reportado / ~11.5% implícito | Carteira ampliada / carteira crédito | Diferença de denominador explica gap; usar implícito para calibração |

## NIM Histórico ITUB4 (2023-2025)

Série trimestral observada de NIM para [[itau]] (NII_total / Carteira_média, conforme calculado no grafo ITUB4):

| Trimestre | NIM (%) |
|-----------|---------|
| 2T23 | ~11.4% |
| 3T23 | ~11.68% |
| 4T23 | ~11.75% |
| 1T24 | ~11.90% |
| 2T24 | ~12.05% |
| 3T24 | ~12.28% |
| 4T24 | ~12.2% |
| 3T25 | 12.31% |
| 4T25 | 12.05% |

**Leitura da série:**

- Tendência ascendente clara de 2T23 a 3T25: ganho de ~90bps ao longo de ~10 trimestres, refletindo repricing da carteira em ambiente de [[selic]] elevada e melhora de mix (mais varejo rentável, menos atacado).
- **3T25 foi o pico**: 12.31%. O recuo para 12.05% em 4T25 pode ser atribuído a sazonalidade (menor número de dias úteis no 4T, que comprime receita de crédito rotativo) e/ou início de mix shift defensivo.
- **Default do modelo: `in:nim = 12.0%`** — reflete a média recente do range 12.0-12.3% e é conservador dado que a tendência histórica aponta para um piso elevado. Se o Itaú confirmar NIM acima de 12.2% por dois trimestres consecutivos, considerar ajustar premissa para 12.2%.
- **Implicação para modelagem**: o modelo ITUB4 usa YoY de [[nii_clientes]] diretamente. O NIM ascendente ao longo de 2023-2025 já está embutido na base histórica de NII — o crescimento YoY captura implicitamente a expansão de NIM sem precisar modelá-lo explicitamente trimestre a trimestre.

## NIM vs NIM Ajustado pelo Risco para ITUB4

O NIM bruto sozinho não diferencia qualidade de portfólio. A comparação relevante entre bancos é o **NIM ajustado pelo risco** (RAROC simplificado):

```
NIM_ajustado = NIM_bruto - Custo_Risco
```

**Itaú 2025:**

| Componente | Valor |
|------------|-------|
| NIM bruto | ~12.0% |
| [[custo_risco]] | ~3.72% |
| NIM ajustado | ~8.3% |

**Bradesco 2025 (estimativa):**

| Componente | Valor |
|------------|-------|
| NIM bruto | ~10-11% |
| [[custo_risco]] | ~4.5-5.0% |
| NIM ajustado | ~5-6% |

**Por que isso importa:** O [[bradesco]] cobra menos spread bruto E ainda perde mais em crédito — dupla desvantagem. O Itaú ganha ~200-300bps a mais de NIM ajustado, o que ao longo de uma carteira de ~R$1.1T implica uma diferença de ~R$22-33B de NII líquido de risco por ano. Essa é a base estrutural do diferencial de [[roe]] entre os dois bancos.

O NIM ajustado de ~8.3% é o "retorno real" sobre o portfólio de crédito após as perdas esperadas. Este é o KPI que verdadeiramente diferencia qualidade dos bancos: um banco pode ter NIM bruto alto simplesmente por tomar mais risco; o NIM ajustado expurga esse efeito.

## Conexão com a Decomposição Estrutural

Ver também: [[nii_clientes]]

O NIM total pode ser decomposto em duas contribuições:

```
NIM_total = NIM_Sensíveis + NIM_Capital_de_Giro
```

Onde:
- **NIM_Sensíveis**: spread da carteira de crédito e TVM sensíveis a taxa — resultado do pricing ativo do banco.
- **NIM_Capital_de_Giro (NIM_CG)**: contribuição do patrimônio líquido alocado a ativos remunerados — é "automático" e cresce mecanicamente com a [[selic]].

**Estimativa para ITUB4 (~2025):**

```
NIM_CG ≈ PL_médio × CDI / Carteira_média
       ≈ R$220B × 13% / R$1.1T
       ≈ ~2.6% dos ativos remunerados
```

```
NIM_Sensíveis ≈ NIM_total - NIM_CG
              ≈ 12.0% - 2.6%
              ≈ ~9.4%
```

**Interpretação:**

- ~22% do NIM do Itaú (~2.6pp de 12.0pp) é **equity hedge** — mecânico, sobe com Selic sem qualquer decisão de pricing. Quando analistas comemoram "NIM expansion" em ciclo de alta de juros, parte relevante é esse efeito automático.
- ~78% do NIM (~9.4pp) é gerenciado — resulta do spread ativo da carteira de crédito e TVM, e depende de mix, pricing, e [[crescimento_carteira]].
- Implicação para cenário de queda de [[selic]]: se o CDI cair de 13% para 10%, o NIM_CG cai ~0.6pp mecanicamente (~R$6.6B de NII perdido ao ano), antes de qualquer efeito em spreads de crédito. O guidance de "NII Clientes +5-9%" do Itaú tende a absorver parcialmente esse efeito via crescimento de carteira.

Esta decomposição é útil para separar o alfa gerencial (NIM_Sensíveis) da beta macro (NIM_CG) na análise de resultados.

## Modelagem: NIM vs YoY de NII

**Nota técnica sobre a abordagem do modelo ITUB4.**

O modelo [[itau]] usa YoY de [[nii_clientes]] diretamente como premissa de projeção — não projeta NIM separadamente. Essa é a abordagem correta para projeções trimestrais porque:

1. **Sazonalidade**: O NIM varia trimestralmente por dias úteis, sazonalidade de crédito rotativo (cartão explode no 4T), e ritmo de repricing. O YoY captura o efeito anual sem distorções sazonais.
2. **Guidance do Itaú**: O próprio banco não dá guidance de NIM% — dá "NII Clientes +5-9%" em termos absolutos. Modelar com o mesmo metric que o management usa reduz ruído.
3. **Consistência histórica**: O YoY de NII Clientes já embute qualquer expansão ou compressão de NIM ocorrida no período. Se o NIM subiu de 11.4% para 12.0%, esse efeito já está na base de comparação.

**Quando usar NIM explícito em vez de YoY:**

| Situação | Abordagem |
|----------|-----------|
| Análise de sensibilidade de Selic | NIM explícito — modelar NIM_CG separado |
| Comparação cross-banco (Itaú vs Bradesco) | NIM ajustado pelo risco |
| Projeções de longo prazo (5+ anos) | NIM explícito — evita YoY compounding distorcido |
| Verificação de sanidade trimestral | Calcular NIM implícito e comparar com histórico |
| Mudança estrutural de patamar de Selic | Ajustar premissa de NIM em vez de YoY |

**Risco do modelo YoY**: se o NIM mudar estruturalmente (ex: Selic cai 400bps), o YoY histórico de NII subestimará o impacto. Nesse caso, é necessário ajustar a premissa de crescimento de NII Clientes para refletir o novo patamar de NIM — ou migrar para uma projeção de NIM explícito para o período de transição.

**Verificação recomendada pós-modelo**: calcular `NII_projetado / Carteira_média_projetada` e confirmar que o NIM implícito está no range 11.5-12.5% para ITUB4. Desvios acima de 50bps do histórico recente exigem justificativa explícita.

## Ver Também

- [[nii_clientes]] — componente principal do NIM (spread de crédito)
- [[nii_mercado]] — componente de tesouraria
- [[selic]] — driver macro mais importante do NIM
- [[crescimento_carteira]] — volume que multiplica o NIM para gerar NII
- [[custo_risco]] — NIM ajustado pelo risco = NIM − custo de risco
- [[banking]] — contexto setorial e fórmulas completas
- [[itau]] — perfil completo ITUB4 com série histórica de premissas
- [[bradesco]] — comparativo de NIM e NIM ajustado
