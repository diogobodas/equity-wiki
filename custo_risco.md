---
type: conceito
source_quality: conceptual
aliases: [Custo de Risco, Cost of Risk, Custo do Crédito, PDD ratio]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/extraction/BBDC4_historical_financials_2022_2025.json
updated: 2026-04-05
tags: [banking, credito, pdd, bradesco, itau, custo-risco]
---

# Custo de Risco

O **Custo de Risco** (ou Custo do Crédito) é a métrica normalizada que mede o nível de provisão para perdas em crédito em relação à carteira total. É o principal driver de volatilidade do lucro trimestral dos bancos — equivale ao "custo dos produtos vendidos" em uma empresa corporativa, mas com muito mais incerteza.

## Como Funciona

```
Custo_Risco = PDD_anualizado / Carteira_Crédito_Média
            = (PDD_trimestral × 4) / Carteira_Média
```

O fluxo de PDD em um trimestre é:

```
PDD_fluxo(t) = Carteira_credito(t) × Custo_Crédito_anualizado / 4
```

**Estoque de provisão** (PCLD) é diferente do fluxo: o estoque acumula provisões passadas menos baixas contábeis (write-offs). O **índice de cobertura** (estoque / carteira inadimplente > 90d) mede o "colchão" para ciclos adversos.

### Componentes do Ciclo de Crédito

| Métrica | Fórmula | Interpretação |
|---------|---------|--------------|
| NPL >90d | Créditos vencidos >90d / Carteira | Inadimplência ponta; lags o ciclo |
| NPL Formation | Novas entradas em NPL / Carteira | Leading indicator de PDD futura |
| Write-off líquido | Créditos baixados − recuperações | Saída definitiva do portfólio |
| Índice de Cobertura | Estoque provisão / NPL >90d | Buffer de conservadorismo |

**Sazonalidade:** 4T é tipicamente o trimestre com maior PDD (revisão de portfólio, provisões adicionais, "kitchen sink" de ano). 1T tende a ser menor após o 4T elevado.

## Decomposição do Custo do Crédito

O guidance de custo do crédito divulgado pelos bancos **sempre se refere à base líquida** — não é a PDD bruta constituída. A decomposição completa é:

```
Custo_Crédito_Líquido = PDD_bruta − Recuperações_créditos_baixados
```

Cada componente tem natureza distinta:

| Componente | O que é | Impacto P&L |
|-----------|---------|-------------|
| **PDD bruta** | Provisão constituída no trimestre (fluxo) | Despesa integral |
| **Recuperações de créditos baixados** | Receita sobre créditos já escriturados como perda (write-off passado) | Crédito que reduz a despesa líquida |
| **Write-off** | Baixa contábil de crédito irrecuperável contra o estoque de PCLD | Neutro no P&L (já estava provisionado); reduz estoque e carteira |

**Write-offs não afetam P&L**: a perda econômica já foi reconhecida quando a PDD foi constituída. O write-off apenas "limpa" o balanço — remove o crédito da carteira e baixa o estoque de provisão pelo mesmo valor.

### Implicação para o Guidance do Itaú

O guidance 2026 do [[itau]] de R$38,5-43,5B é **líquido de recuperações**. Com recuperações históricas de ~R$3-4B/ano, a PDD bruta implícita é ~R$42-47B. Para modelagem:

```
PDD_bruta_implícita ≈ Guidance_líquido + Recuperações_esperadas
                    ≈ R$38,5-43,5B + ~R$3-4B ≈ R$42-47B
```

Ao comparar custo de risco entre bancos ou períodos, sempre confirmar se a base é bruta ou líquida — as diferenças podem ser de 50-80bps e distorcem qualquer comparação.

## IFRS 9 Stage Migration — Leading Indicator

O [[ifrs9]] (CPC 48) classifica toda a carteira em três estágios com provisões crescentes:

| Stage | Critério | Base de Provisão |
|-------|---------|-----------------|
| **Stage 1** | Crédito performando normalmente | ECL 12 meses |
| **Stage 2** | Aumento significativo de risco de crédito (SICR) | ECL lifetime |
| **Stage 3** | Impaired — default > 90d ou evidência objetiva de perda | ECL lifetime |

**Critérios de migração Stage 1 → Stage 2 (SICR):**
- Atraso > 30 dias (gatilho quantitativo)
- Deterioração de rating interno em X notches
- Renegociação de dívida (forbearance)
- Deterioração macroeconômica de setor/segmento específico

### Por Que Stage 2 é o Leading Indicator Mais Importante

A migração Stage 1→2 aumenta a PDD **antes** do default aparecer no NPL >90d:
- Um crédito Stage 2 provisiona ECL lifetime (toda a vida esperada do contrato) em vez de apenas 12 meses
- O NPL >90d (Stage 3) reflete perdas que já ocorreram; Stage 2 reflete deterioração que ainda não virou default
- Quando % Stage 2 / Carteira total sobe, a PDD aumenta mesmo sem alta no NPL headline

**Consequência para análise:** Analistas monitoram a composição da carteira por stage trimestralmente. Aumento de Stage 2 é sinal de alerta antecedente de 2-4 trimestres para o pico de custo do crédito.

O [[itau]] divulga nos releases a composição por stage — acompanhar a migração é parte do toolkit de análise de [[banking]].

## Ciclo de Crédito ITUB4 2020-2025

Narrativa do ciclo recente para contextualizar o patamar atual:

### 2020 — Provisões Antecipadas COVID
Custo do crédito ~4,0-4,5%. Os grandes bancos constituíram provisões adicionais/complementares massivas de forma antecipada (provisões forward-looking sob IFRS 9), antes que a inadimplência aflorasse. Esse conservadorismo criou um colchão que sustentou resultados nos anos seguintes.

### 2021 — Liberação de Provisões + Recuperações
Custo ~2,5% (artificialmente baixo). A inadimplência pós-COVID foi menor que o previsto, levando à reversão parcial das provisões complementares constituídas em 2020. Recuperações de créditos baixados também foram elevadas. O custo do crédito desse ano não é representativo da normalidade.

### 2022-2023 — Ciclo Adverso
Custo ~3,5-4,0%. Eventos idiossincráticos (Americanas, Light) combinados com deterioração de varejo, serviços e PF de baixa renda. Crescimento rápido de cartões e crédito pessoal nos anos anteriores gerou vintages ruins. NPL formation disparou. Provisões complementares foram novamente constituídas.

### 2024 — Início de Normalização
PF começando a cair. Inadimplência de grandes grupos corporativos (Americanas, Light) já refletida e write-off parcialmente executado. Mix de carteira sendo rebalanceado em direção a produtos de menor risco.

### 2025 — Consolidação, mas Acima da Normalização Plena
**Custo realizado: 3,72%.** Inadimplência PF em "menor nível histórico" em 4T25, segundo management. O custo ainda está acima do patamar ideal (~3,0%) por:
- Resíduo de ciclo adverso PJ mid-market
- Cartão de crédito ainda com vintages de 2022-23 em digest
- PJ grande: alguns casos individuais ainda em resolução

### 2026 — Guidance de Melhoria Gradual
Guidance provisão R$38,5-43,5B. Com carteira projetada ~R$1,3T (crescendo ~8-10% a.a.), o custo implícito é ~3,2-3,6% — **leve melhoria vs 2025** se a carteira crescer conforme planejado. O midpoint do guidance (~R$41B) com carteira ~R$1,25T implica ~3,3%.

```
Custo_implícito_guidance = R$41B / ~R$1,25T ≈ 3,3%
```

A melhoria é gradual, não um salto — consistente com um ciclo de crédito normalizando, não revertendo abruptamente.

## No Contexto Brasileiro

**Range histórico para grandes bancos:**
- Normal: 2,0-3,5%
- Ciclo adverso (2015-16, 2020, 2023): 4,0-6,0%
- Crise severa: acima de 6,0%

**Diferença COSIF vs IFRS:**
- COSIF (BRGAAP): provisão por perda incorrida — 7 faixas (AA-H por atraso)
- IFRS 9 (CPC 48): ECL — Expected Credit Loss em 3 estágios; provisiona antes do default. IFRS tende a ser mais conservador e volátil.

O mercado usa a base dos **releases gerenciais** (geralmente alinhada a IFRS com ajustes). Sempre especificar a base ao comparar bancos ou comparar com histórico COSIF.

**Provisões adicionais/complementares:** Bancos podem constituir provisões acima do mínimo regulatório como reserva para ciclos adversos. Quando esse colchão é liberado, PDD cai artificialmente e o lucro sobe. Esse efeito distorce o custo do crédito normalizado.

### Relação com Mix de Carteira

O custo de risco é fortemente influenciado pelo mix:
- Consignado: ~0,5-1,5%
- Crédito imobiliário: ~0,2-0,8%
- Capital de giro PJ: ~1,5-3,0%
- Crédito pessoal não-consignado: ~4-8%
- Cartão de crédito rotativo: ~10-20%

Banco que cresce cartão/pessoal tem NIM maior mas custo de risco muito maior — o NII líquido pode ser semelhante ou pior.

## Por Empresa — BBDC4 (Bradesco)

### PDD Expandida Trimestral (R$ M)

| Trimestre | PDD Bruta | Recuperação | PDD Expandida | Obs |
|-----------|-----------|-------------|---------------|-----|
| 1T22 | -7.051 | +1.769 | -4.836 | |
| 2T22 | -8.148 | +1.473 | -5.313 | |
| 3T22 | -8.587 | +1.498 | -7.267 | deterioração acelerada |
| **4T22** | **-10.562** | **+1.131** | **-14.881** | **kitchen-sink quarter** |
| 1T23 | -9.726 | +930 | -9.517 | |
| 2T23 | -10.362 | +1.168 | -10.316 | pico de PDD bruta |
| 3T23 | -9.217 | +1.160 | -9.188 | |
| 4T23 | -9.156 | +1.413 | -10.524 | |
| 1T24 | -8.435 | +1.288 | -7.811 | início de normalização |
| 2T24 | -8.465 | +1.473 | -7.290 | |
| 3T24 | -7.864 | +1.566 | -7.127 | |
| 4T24 | -8.187 | +1.487 | -7.460 | |
| 1T25 | n/d | n/d | -7.642 | normalização em curso |
| 2T25 | n/d | n/d | -8.142 | |
| 3T25 | n/d | n/d | -8.560 | |
| 4T25 | n/d | n/d | -8.828 | custo risco ann. ~5.5% |

> *[Auditado 2026-04-04 contra historical_financials.json 4T25]*

> **Nota 4T22:** PDD expandida (-14.881) é maior em valor absoluto que PDD bruta (-10.562) menos recuperação (+1.131) = -9.431. A diferença de ~-4.319 representa ajuste extraordinário no saldo de provisão (constituição extra + write-offs acima do fluxo normal). Esse é o "kitchen sink" — reconhecimento antecipado agressivo de perdas.

### Saldo de Provisão no Balanço (R$ M)

| Período | Saldo PDD (BP) | Carteira Bruta | Cobertura Saldo/Carteira |
|---------|---------------|----------------|--------------------------|
| 1T22 | -47.149 | 514.785 | 9,2% |
| 4T22 | -57.741 | 542.758 | 10,6% ← pico de estoque |
| 1T23 | **-60.032** | ~544.000 | **~11,0%** ← pico absoluto |
| 4T23 | -53.901 | 525.968 | 10,3% |
| 4T24 | -48.275 | 598.221 | 8,1% ← liberação de provisão |

O saldo de PDD atingiu o pico em 1T23 (R$60,0B) — **um trimestre após** o kitchen-sink do 4T22. Isso reflete que a constituição extra do 4T22 elevou o estoque, que só começou a cair quando as write-offs aceleraram e a constituição arrefeceu ao longo de 2023-24.

### Custo de Risco Anual Consolidado

| Ano | Custo de Risco (avg) | Contexto |
|-----|----------------------|----------|
| 2022 | ~5,6% | Kitchen-sink 4T22 distorce fortemente a média anual |
| 2023 | ~7,6% | Pior ano — ciclo pleno: Selic 13,75%, inadimplência PME/PF, Americanas |
| 2024 | ~5,3% | Normalização: PDD expandida cai de R$9-10B para R$7-7,5B/trimestre |
| 2025 | ~5,5% | Estabilização: PDD reacelerou de R$7,6B (1T25) para R$8,8B (4T25) com crescimento da carteira |

> Custo de risco calculado como `PDD_expandida_anualizada / Carteira_crédito_média`. Trimestres individuais: 4T22 chegou a ~11,0% anualizado (pico da crise).

### A Crise de 2022-2023 no Bradesco

**O kitchen-sink de 4T22** foi o evento de crédito mais severo da história recente do Bradesco:

- **PDD expandida de R$14,9B** em um único trimestre — vs média de R$5-6B nos trimestres anteriores, representando quase **3x a run-rate normal**
- **LL despencou** de ~R$7B (2T22) para ~R$1,6B (4T22) — eliminação quase completa do lucro em um trimestre
- **Índice de cobertura** subiu de 9,2% (1T22) para 10,6% (4T22): o banco reconheceu provisões muito acima das perdas realizadas naquele trimestre para "limpar" o balanço de uma vez

**Causas combinadas:**
1. **Selic 13,75%** pressionando inadimplência de PME sem garantia real e PF de baixa renda — segmentos com maior peso no mix do Bradesco vs Itaú
2. **Americanas** — anúncio da fraude em janeiro/2023 (mas o pré-provisionamento possível já em 4T22, dado que indícios circulavam no mercado), mais R$1,5-2B de exposição estimada
3. **Deterioração de carteira varejo** — vintages de crédito pessoal e cartão originados em 2020-21 (boom pós-COVID) chegando à fase de inadimplência em 2022-23
4. **Decisão estratégica de gestão** — novo CEO (Octávio de Lazari) acelerou o reconhecimento de perdas para "zerar o relógio" e criar base limpa para o turnaround

O pico do **saldo de PDD** no balanço ocorreu em **1T23** (R$60,0B), um trimestre após o kitchen-sink — refletindo que a constituição extraordinária do 4T22 só foi "absorvida" por write-offs ao longo de 2023.

### Comparação BBDC4 vs ITUB4 — Custo de Risco

| Período | BBDC4 | ITUB4 | Spread (bps) | Interpretação |
|---------|-------|-------|--------------|---------------|
| 2022 avg | ~5,6% | ~3,5% | +210bps | crise chegando mais cedo no Bradesco |
| **2023 avg** | **~7,6%** | **~3,5%** | **+410bps** | **divergência máxima** |
| 2024 avg | ~5,3% | ~3,0% | +230bps | normalização parcial BBDC4 |
| 2025 avg | ~5,4% | ~3,7% | +170bps | spread reduzindo, mas persiste |

**Por que a diferença estrutural persiste (~200-400bps)?**

O diferencial não é apenas cíclico — reflete diferenças de mix de carteira:

| Dimensão | BBDC4 | ITUB4 |
|----------|-------|-------|
| Peso PME sem garantia | Alto | Moderado |
| Crédito pessoal PF baixa renda | Alto | Menor |
| Consignado / imobiliário | Menor penetração | Maior penetração |
| Cartões rotativo | Alto percentual | Mais controlado |
| Grandes corporações investment grade | Menor peso | Maior peso |

**O turnaround de crédito do Bradesco** consiste precisamente em migrar o mix de carteira em direção a produtos de menor risco (consignado, crédito imobiliário, grandes empresas investment grade) e reduzir a exposição relativa a PME sem garantia e PF de baixa renda. O custo de risco convergindo gradualmente para ~4-5% (vs histórico pré-crise de ~3-4%) reflete essa migração — mas o processo leva 3-5 anos dado o prazo médio dos contratos.

### O Que é "PDD Expandida" vs "PDD Bruta" — Detalhe BBDC4

O Bradesco divulga o custo do crédito em base **expandida** (líquida de recuperações), que é a métrica do guidance e da DRE gerencial:

```
PDD_expandida = PDD_bruta_constituída − Recuperações_de_créditos_baixados
```

A "expansão" do nome vem do fato de incluir itens que o COSIF tratava separadamente:
- Perdas com garantias executadas
- Descontos concedidos em renegociação (haircut econômico)
- Variação cambial em carteiras dolarizadas com risco de crédito

Para o **4T22 especificamente:**

```
PDD bruta constituída:    -10.562
Recuperações:              +1.131
Subtotal "normal":         -9.431
PDD expandida divulgada:  -14.881
Diferença:                 -4.450  ← ajustes extraordinários (write-offs extras + provisão complementar)
```

Essa diferença de R$4,5B no 4T22 representa o reconhecimento extraordinário que caracteriza o kitchen-sink: baixas contábeis aceleradas (write-offs) e constituição de provisão complementar acima do modelo de ECL padrão.

### Perspectiva 2026+

**Guidance Bradesco:** custo de risco estável sobre carteira expandida, com meta de convergência gradual para a banda histórica (~3-4% no longo prazo).

**O que monitorar:**
- **Safras PME 2023-2025:** crédito originado no pós-kitchen-sink entra em fase de maturação; qualidade dessas safras determina se o custo de risco sobe ou cai em 2026
- **Inadimplência Stage 3 (IFRS 9):** migração de Stage 2 → Stage 3 é leading indicator de 2-4 trimestres; aumento de Stage 2 em 2025 sinalizaria pressão em 2026
- **Mix de carteira:** velocidade da migração para consignado/imobiliário vs crescimento de cartão/PME
- **Americanas:** resolução do processo judicial pode liberar ou exigir provisões adicionais

**Riscos de alta para o custo de risco em 2026:**
- Selic permanecendo elevada por mais tempo (cenário base atual: ~13-14% em 2026) → PME e PF continuam pressionados
- Renegociações (forbearance) que retornam ao portfólio performando → "second default" em ex-Stage 2
- Ciclo de crédito para grandes corporações (infra, energia) se deteriorando no cenário de juros altos

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | Custo 3,72% em 2025. Carteira total ~R$1,2T. Guidance provisão 2026: R$38,5-43,5B → custo implícito ~3,2-3,6% (melhoria gradual vs 2025). Índice de cobertura historicamente >200%. Inadimplência PF em mínimos históricos em 4T25. Maior risco residual em PJ mid-market. Mix favorável (consignado/imobiliário pesam mais que cartão rotativo). |
| [[bradesco]] | Kitchen-sink 4T22: PDD expandida R$14,9B (vs run-rate R$5-6B), LL caiu de R$7B para R$1,6B. Custo de risco pico 2023: ~7,6% (vs ITUB4 ~3,5% = spread +410bps). Normalização gradual: 2024 ~5,3%, 2025 ~5,4%. Saldo PDD no BP: pico R$60,0B (1T23) → R$48,3B (4T24), liberando capital. Meta turnaround: migrar mix para menor risco → convergência gradual ao custo histórico (~3-4%). |

## Ver Também

- [[nii_clientes]] — o NII bruto que o custo de risco consome
- [[eficiencia_operacional]] — outro driver de rentabilidade (opex, não crédito)
- [[selic]] — Selic alta comprime demanda mas pode piorar inadimplência no médio prazo
- [[crescimento_carteira]] — carteira maior gera mais PDD day-1 mesmo sem piora de qualidade
- [[banking]] — contexto setorial e estrutura DRE
- [[ifrs9]] — arcabouço de ECL em 3 estágios que governa o reconhecimento de provisões
