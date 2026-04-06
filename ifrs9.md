---
type: conceito
source_quality: conceptual
aliases: [IFRS 9, CPC 48, ECL, Expected Credit Loss, Perda de Crédito Esperada]
sources:
  - sectors/banking/sector_profile.md
  - wiki/custo_risco.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
updated: 2026-04-05
---

# IFRS 9 (CPC 48) — Expected Credit Loss

O **IFRS 9** — adotado no Brasil como **CPC 48**, vigente para Instituições Financeiras a partir de 2018 — é a norma contábil internacional para instrumentos financeiros. Substituiu o modelo de perda incorrida do COSIF/BRGAAP por um modelo prospectivo de **ECL (Expected Credit Loss)**, obrigando os bancos a provisionar antecipadamente com base em probabilidade de default, não em atraso observado. É a principal razão pela qual o [[custo_risco]] é mais volátil hoje do que era antes de 2018.

## 1. O Que Mudou vs COSIF

A diferença fundamental é a direção do olhar: COSIF olha para o passado (crédito já venceu?); IFRS 9 olha para o futuro (qual a probabilidade de esse crédito vencer?).

| Dimensão | COSIF / BRGAAP (Res. CMN 2.682/99) | IFRS 9 / CPC 48 |
|----------|-------------------------------------|-----------------|
| **Modelo de provisão** | Perda incorrida (incurred loss) | Perda esperada (expected credit loss — ECL) |
| **Direção temporal** | Backward-looking — provisiona quando o atraso já ocorreu | Forward-looking — provisiona na concessão, aumenta conforme risco evolui |
| **Classificação de risco** | 9 faixas (AA → H) baseadas em dias de atraso e análise da carteira | 3 Stages baseados em deterioração relativa de risco |
| **Gatilho de provisão** | Atraso ≥ 15 dias (nível D) inicia provisionamento significativo | Concessão do crédito — mesmo Stage 1 exige ECL 12 meses imediato |
| **Cenários macro** | Não incorporados explicitamente | PD forward-looking inclui cenários macroeconômicos ponderados por probabilidade |
| **Timing de reconhecimento** | Lento — perda só reconhecida após inadimplência consolidada | Antecipado — recessão esperada eleva PDD antes do default efetivo |
| **Volatilidade da PDD** | Baixa — provisão acumula gradualmente com atraso | Alta — mudança de cenário macro ou de Stage pode gerar salto no trimestre |
| **Base legal** | Resolução CMN 2.682/99 — regulatório BCB | CPC 48 (equivalente ao IFRS 9 IASB) — reportes CVM (ITR/DFP) |

**Implicação prática**: sob COSIF, bancos provisionavam pouco no início de um ciclo adverso e muito depois que a inadimplência já explodia. Sob IFRS 9, o banco provisiona assim que o risco aumenta prospectivamente — o que faz a PDD subir antes do NPL headline, mas também significa que o pico da provisão antecede o pico da inadimplência visível.

## 2. Os 3 Estágios em Detalhe

| Stage | Critério de Classificação | Base de Provisão (ECL) | Accrual de Juros |
|-------|--------------------------|------------------------|-----------------|
| **Stage 1** | Crédito normal — sem deterioração significativa de risco desde a concessão | ECL 12 meses: PD × LGD × EAD para o período de 12 meses | Sobre valor bruto (gross carrying amount) |
| **Stage 2** | Aumento Significativo de Risco de Crédito (SICR) vs concessão — mas ainda não impaired | ECL lifetime: PD × LGD × EAD ao longo de toda a vida esperada do contrato | Sobre valor bruto |
| **Stage 3** | Crédito impaired — default efetivo ou evidência objetiva de impairment | ECL lifetime (igual ao Stage 2, mas com PD = 1 para créditos em default) | Sobre valor líquido (net carrying amount = bruto − provisão) — diferença relevante para reconhecimento de receita de juros |

**Regra do "backstop"**: crédito com atraso > 30 dias **deve** migrar para Stage 2 (presunção refutável). Crédito com atraso > 90 dias **deve** migrar para Stage 3. Esses são gatilhos mínimos — o banco pode antecipar a migração por critérios qualitativos.

### Critérios de SICR (Stage 1 → Stage 2)

- Atraso > 30 dias (gatilho quantitativo mínimo — presunção refutável)
- Deterioração de rating interno em X notches definido pela política interna do banco
- Renegociação de dívida com concessão ao devedor (forbearance / waiver)
- Inclusão em watchlist de monitoração especial
- Deterioração macroeconômica de setor ou segmento específico incorporada ao modelo de PD
- Mudança de perspectiva de negócio do devedor (p.ex., setor em stress severo)

**Nota**: SICR é um julgamento — cada banco define seus thresholds, o que cria heterogeneidade entre instituições e dificulta comparações diretas de % Stage 2.

## 3. Stage Migration como Leading Indicator

A migração entre stages é o **leading indicator mais valioso para prever PDD futura** — mais do que o NPL >90d, que é um indicador lagging.

### Por Que Stage 2 Antecede o NPL

O raciocínio é sequencial:

```
Stage 2 (SICR) sobe
  → maior provisão (ECL lifetime > ECL 12m)
    → PDD sobe (fluxo de constituição)
      → créditos Stage 2 podem piorar para Stage 3 (90d+)
        → NPL >90d headline sobe
          → write-offs aumentam
```

O NPL >90d reflete créditos que **já viraram default**. O Stage 2 reflete créditos que **ainda não viraram default mas têm risco elevado**. A janela de antecedência é tipicamente de **2 a 4 trimestres** entre o pico de % Stage 2 e o pico de NPL formation.

### Dinâmica Conceitual do Ciclo

```
% Stage 2 na Carteira
        ^
        |         /\
        |        /  \
        |       /    \
        |      /      \         PDD (fluxo)
        |     /        \          /\
        |    /          \        /  \
        |   /            \      /    \
        |  /              \    /      \       NPL >90d
        | /                \  /        \        /\
        |/                  \/          \      /  \
        +-----------------------------------> tempo
        T0  T+1  T+2  T+3  T+4  T+5  T+6  T+7  T+8
```

Leitura:
- **Stage 2 lidera**: sinal de alerta ativo. Banco ainda não registra PDD elevada, mas o estoque de risco está crescendo.
- **PDD segue Stage 2**: conforme créditos Stage 2 aumentam, a provisão ECL lifetime sobe — mesmo sem migração para Stage 3.
- **NPL é lagging**: confirma o ciclo adverso quando já está em curso há vários trimestres.

**Implicação para análise**: ao analisar um release bancário, o analista deve **sempre reportar a composição da carteira por stage** — não apenas o NPL. Aumento de Stage 2% mesmo com NPL estável é sinal de deterioração em curso não capturado pelos indicadores tradicionais.

## 4. ECL nos Modelos — Componentes

A fórmula da ECL decompõe a perda esperada em três parâmetros:

```
ECL = PD × LGD × EAD
```

| Parâmetro | Definição | Drivers Principais |
|-----------|-----------|-------------------|
| **PD** (Probability of Default) | Probabilidade de o devedor não honrar a obrigação no horizonte definido (12 meses para Stage 1; lifetime para Stage 2/3) | Histórico de inadimplência do segmento, rating interno, cenário macro forward-looking |
| **LGD** (Loss Given Default) | Percentual da exposição perdida após o default, líquido de recuperações e colateral | Tipo de produto (consignado < cartão), colateral (imóvel > sem garantia), recovery histórico |
| **EAD** (Exposure at Default) | Valor da exposição no momento do default esperado; inclui parcelas não desembolsadas em limites rotativos | Saldo devedor + parcela de comprometimento futuro (credit conversion factor para linhas abertas) |

**Para Stage 1**: `ECL_12m = PD_12m × LGD × EAD`

**Para Stage 2 e Stage 3**: `ECL_lifetime = Σ PD_t × LGD × EAD_t` (soma ao longo da vida esperada do contrato)

A diferença entre Stage 1 e Stage 2 em termos de provisão é **proporcional à vida remanescente do contrato**. Um crédito imobiliário de 20 anos que migra para Stage 2 tem um salto enorme de provisão: de 12 meses de ECL para 20 anos de ECL. Um cartão (revolving, curto prazo) tem salto menor.

### Forward-Looking: Cenários Macro

O IFRS 9 exige que os bancos incorporem cenários macroeconômicos ponderados por probabilidade na estimação de PD:

```
PD_forward_looking = w_base × PD_cenário_base
                   + w_adverso × PD_cenário_adverso
                   + w_otimista × PD_cenário_otimista
```

Quando o banco revisa seus pesos de cenário (p.ex., eleva probabilidade do cenário adverso), a PDD sobe imediatamente, mesmo sem qualquer crédito ter vencido. Esse é um dos mecanismos que tornou o 1T20 (COVID) um trimestre de PDD explosiva — foi inteiramente forward-looking.

## 5. Impacto na Volatilidade da PDD

O IFRS 9 tornou a PDD estruturalmente mais volátil do que era sob o regime COSIF:

### Fontes de Volatilidade

| Fonte | Mecanismo | Quando aparece |
|-------|-----------|---------------|
| **Stage migration** | Crédito Stage 1→2 aumenta provisão de 12m para lifetime em um único trimestre | Quando % Stage 2 sobe (stress setorial, macro adverso) |
| **Revisão de cenários macro** | Aumento de peso do cenário adverso eleva PD forward-looking de toda a carteira | Choques exógenos (pandemia, recessão esperada) |
| **Provisões complementares / adicionais** | Bancos podem constituir provisões acima do mínimo IFRS 9 como buffer discricionário | Gestão conservadora do ciclo; "kitchen sink" de 4T |
| **Reversão de provisões** | Quando ciclo melhora, provisões complementares e ECL podem ser revertidas | Pós-crise, reversão artificialmente eleva lucro |
| **Sazonalidade de write-off** | 4T concentra write-offs e provisões adicionais para "limpar" o portfólio antes do fechamento do ano | Todo 4T; distorce comparação trimestral |

### Caso COVID 2020 — IFRS 9 em Ação

O 1T20 é o exemplo mais nítido do IFRS 9 funcionando como previsto:

- **Antes**: sob COSIF, a PDD de 1T20 seria baixa (inadimplência não havia subido ainda — a maioria das empresas e famílias ainda estava pagando em março/20)
- **Sob IFRS 9**: os bancos elevaram os pesos do cenário adverso prospectivo imediatamente após o lockdown. A PDD disparou em 1T20 **antes** de qualquer inadimplência efetiva — ITUB4 e BBDC4 constituíram provisões adicionais/complementares bilionárias naquele trimestre
- **Resultado**: o pico de PDD foi em 2020; a inadimplência efetiva ficou abaixo do previsto; as provisões complementares foram revertidas em 2021, criando um 2021 artificialmente lucrativo

**Lição para modelagem**: em cenários de stress macro, o analista deve antecipar o salto de PDD **antes** do pico de NPL, não depois. A PDD IFRS 9 antecipa em 2-4 trimestres.

## 6. Diferença para o Modelo ITUB4

O modelo do [[itau]] no projeto é construído sobre a **base gerencial publicada nos releases de RI** — que é alinhada a IFRS com ajustes próprios:

| Base | O que é | Onde usar |
|------|---------|-----------|
| **Gerencial / IFRS (releases RI)** | Base primária do modelo. Exclui amortização de intangíveis adquiridos em M&A; pode ajustar efeitos de hedge accounting. É essa a base que o management discute no guidance. | [[custo_risco]] no modelo ITUB4 |
| **IFRS contábil (CVM ITR/DFP)** | Base regulatória para investidores; inclui todos os itens acima. Pode divergir da gerencial em R$500M-1B por trimestre. | Verificação, backtesting histórico |
| **COSIF (BCB IF.data)** | Base regulatória prudencial para o BCB. Modelo de provisão diferente (perda incorrida — 9 faixas AA-H). Os números de provisão COSIF e IFRS podem divergir significativamente. | Análise histórica regulatória; séries longas pré-2018 |

**Regra operacional**: ao extrair dados históricos de PDD / custo de risco para o ITUB4 a partir de 2018, usar sempre a base gerencial dos releases (IFRS gerencial). Para séries históricas anteriores a 2018, a base disponível é COSIF — **não comparar diretamente** com a série IFRS pós-2018 sem ajuste.

O guidance de provisão de crédito divulgado pelo Itaú (R$38,5-43,5B para 2026) é na base gerencial IFRS, líquido de recuperações. Ver [[custo_risco]] para a decomposição do guidance.

## 7. Por Empresa

### [[itau]] (ITUB4)

- Adotou IFRS 9 / CPC 48 em 2018 como todos os grandes bancos.
- Em 2020: constituiu provisões complementares massivas (COVID forward-looking). Custo de risco ~4,0-4,5% em 2020 vs ~3% de normalidade.
- Em 2021: reversão de provisões complementares → custo artificialmente baixo (~2,5%) — **não usar como referência de normalidade**.
- Em 2022-23: novo ciclo adverso (Americanas, Light, vintages ruins de varejo). Stage 2 subiu antes do NPL headline, confirmando o padrão leading indicator.
- Em 2025: custo de crédito 3,72%. Inadimplência PF em mínimo histórico. Stage 2 estabilizando. Guidance 2026 implica leve melhoria gradual.
- Banco divulga composição da carteira por stage nos releases de RI — acompanhar trimestralmente.

### [[bradesco]] (BBDC4)

- Adotou IFRS 9 / CPC 48 em 2018.
- Em 2022-23: **Stage 2 elevado** — episódio notável. Exposição indireta às renegociações da Americanas e Light, somada a piora no varejo PF, fez o % Stage 2 da carteira subir de forma expressiva. Isso gerou PDD antecipado elevado antes que a inadimplência efetiva se consolidasse em Stage 3.
- Efeito: PDD do Bradesco ficou persistentemente alta em 2022-23, pressionando o ROE abaixo do histórico e gerando o gap de eficiência vs Itaú. O ciclo forward-looking do IFRS 9 amplificou a severidade da pressão sobre o P&L do BBDC4.
- Em 2024-25: normalização em curso. Stage 2 regredindo à medida que os créditos são resolvidos (write-off ou regularização). PDD declinando gradualmente.
- Meta do management: retornar à banda histórica de custo de crédito (~3%) quando o portfólio estiver saneado.

## 8. Ver Também

- [[custo_risco]] — a métrica operacional que materializa o IFRS 9 no P&L; decomposição PDD bruta / líquida / write-off / recuperações
- [[banking]] — estrutura DRE bancária, duplo padrão COSIF vs IFRS, particularidades contábeis
- [[itau]] — empresa com modelo completo; custo de risco 3,72% em 2025
- [[bradesco]] — empresa em cobertura; Stage 2 elevado em 2022-23 como caso concreto de leading indicator
