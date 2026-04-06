---
type: conceito
source_quality: conceptual
aliases: [Crise de Crédito 2022, Crise Americanas, Ciclo de PDD 2022-2023, Banking Credit Crisis 2022]
sources:
  - sectors/banking/companies/BBDC4/outputs/extraction/BBDC4_historical_gerencial.json
  - sectors/banking/companies/BBDC4/outputs/extraction/BBDC4_bp_gerencial.json
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_historical_gerencial.json
  - sectors/banking/companies/SANB11/outputs/extraction/SANB11_historical_gerencial.json
  - sectors/banking/sector_profile.md
updated: 2026-04-05
---

# Crise de Crédito Bancária Brasileira (2022–2023)

A **crise de crédito de 2022-2023** foi o ciclo adverso mais severo do sistema bancário brasileiro desde 2015-2016. Foi resultado da confluência de três fatores simultâneos: (a) ciclo de alta agressiva da [[selic]], (b) fraude contábil das Americanas, e (c) deterioração generalizada de PMEs e pessoas físicas de baixa renda no pós-COVID. O banco mais severamente impactado entre os grandes privados foi o [[bradesco]] (BBDC4).

## O Que Foi a Crise

### Os Três Fatores

**1. Ciclo de Alta do [[selic]] (2021-2022)**

A Selic saiu de um mínimo histórico de 2% em janeiro de 2021 para 13,75% em agosto de 2022 — uma alta de 1.175bps em apenas 18 meses. Para o sistema bancário, o impacto foi bifurcado:

- **Positivo de curto prazo**: NIM beneficiado pelo spread maior e pela remuneração do capital de giro (PL × CDI).
- **Negativo estrutural com lag**: PMEs com dívida em CDI+ viram seu custo de crédito saltar 12-14pp. O fluxo de caixa dessas empresas — ainda fragilizado pelo pós-COVID — não suportou o choque.

**2. Fraude das Americanas (janeiro de 2023)**

Em 11 de janeiro de 2023, o novo CEO das Lojas Americanas, Sérgio Rial, renunciou após apenas 9 dias no cargo ao descobrir inconsistências contábeis da ordem de R$20B que se revelaram — nos dias seguintes — um passivo bancário de R$40-43B camuflado como "risco sacado" (uma espécie de adiantamento sobre recebíveis que os bancos tratavam como ativo e a empresa tratava como contas a pagar, sem registrar a dívida correspondente).

Exposição bancária estimada:

| Banco | Exposição Estimada |
|-------|-------------------|
| Bradesco | ~R$4,8B |
| Santander Brasil | ~R$3,7B |
| Itaú Unibanco | ~R$2,7B |
| BTG Pactual | ~R$1,2B |

O caso gerou:
- Provisão adicional relevante nos releases de 1T23 e 2T23 dos bancos expostos.
- Ruptura de confiança nos balanços corporativos — o mercado questionou quantas outras empresas tinham estruturas similares de risco sacado não transparente.
- Pressão sobre firmas de auditoria e sobre o conceito de "risco sacado" como instrumento de gestão de capital de giro.

**3. Deterioração de PMEs e PF Pós-COVID**

Durante a pandemia (2020-2021), o governo e os bancos estenderam moratórias e créditos emergenciais. Esse colchão foi se exaurindo ao longo de 2022. Com a Selic em 13,75% e o fim dos programas de suporte, dois segmentos quebraram o ciclo de crédito:

- **PMEs**: Empresas de serviços, varejo e construção civil com dívida em CDI viram o custo de seu passivo dobrar. Setores já debilitados (varejo físico, food service, turismo) não conseguiram rolar as dívidas.
- **PF de menor renda / cartão de crédito**: Inadimplência de cartão rotativo e crédito pessoal sem garantia superou 30% em algumas faixas de renda. O patamar de juros do cartão rotativo — que já era alto — tornou a dívida impagável para inadimplentes.

### Timing

| Período | Evento-Chave |
|---------|-------------|
| 1T22 | PDD ainda em nível normal (~R$4,8B/trim no BBDC4). Selic subindo mas crédito emergencial ainda em vigor. |
| 3T22 | Primeiros sinais de deterioração: PDD BBDC4 salta para R$7,3B (+50% vs 1T22). |
| 4T22 | **Kitchen-sink quarter**: BBDC4 provisiona R$14,9B (~3x o nível normal). LL cai 77%. |
| 1T23 | Americanas: provisão adicional em todos os bancos expostos. PDD BBDC4 R$9,5B. |
| 2T23 | Pico de PDD acumulada (BBDC4 4 trimestres seguidos acima de R$9B). |
| 4T23 | Início de normalização; PDD cadente sequencialmente. |
| 2024 | Normalização gradual; saldo de provisão em balanço começando a cair. |

## Selic como Driver Primário

O ciclo de alta da [[selic]] foi o gatilho macro que precipitou tudo o mais:

```
Selic 2% (jan/2021) → 4,25% (jun/2021) → 7,75% (dez/2021) → 10,75% (mar/2022)
                    → 12,75% (jun/2022) → 13,75% (ago/2022)
Mantida em 13,75% até mai/2023 (9 meses no pico)
Cortes a partir de ago/2023 → 10,5% (mai/2024)
Novo ciclo de alta: 10,5% (set/2024) → ~14,75% (2026E)
```

**Por que 13,75% foi disruptivo para PMEs:**

Para uma PME com dívida de capital de giro em CDI+3%, a taxa efetiva:
- Jan/2021: ~5% a.a.
- Ago/2022: ~16,75% a.a. (+12pp em 18 meses)

O custo de serviço da dívida triplicou ou quadruplicou em menos de dois anos. Empresas que contraíram dívidas em 2020-2021 (aproveitando juros baixos) viram o rollover se tornar impossível.

**Inadimplência por segmento no pico (2022-2023):**

- Cartão de crédito rotativo PF: >30% (vencidos >90d)
- Crédito pessoal sem garantia: >15%
- PME capital de giro: >8% em segmentos afetados
- Grandes empresas/Atacado: seletivo; casos Americanas, Light, Marisa concentraram as perdas

## BBDC4 — O Banco Mais Impactado entre os Grandes

O Bradesco sofreu o impacto mais severo entre os grandes bancos privados. Isso decorreu de três fatores estruturais:

1. **Mix histórico mais arriscado**: O banco sempre teve exposição proporcionalmente maior a PMEs e PF de menor renda — segmentos de maior spread mas também maior sensibilidade ao ciclo.
2. **CET1 menor que Itaú**: Com menos buffer de capital, cada perda de crédito se transmitia mais diretamente para o resultado.
3. **Percepção de risk management mais fraco**: O mercado interpretou que o banco havia crescido carteiras de maior risco de forma menos disciplinada nos anos anteriores.

### Dados Quantitativos do Ciclo

#### PDD Expandida Trimestral (R$M, negativo = despesa)

| Trim | 1T | 2T | 3T | 4T | Total Ano |
|------|----|----|----|----|-----------|
| 2022 | -4.836 | -5.313 | -7.267 | **-14.881** | -32.297 |
| 2023 | -9.517 | -10.316 | -9.188 | -10.524 | -39.545 |
| 2024 | -7.811 | -7.290 | -7.127 | -7.460 | -29.688 |
| 2025 | -7.642 | -8.142 | -8.560 | -8.828 | -33.172 |

> **Referência**: R$5B/trim era o nível "normal" pré-crise (1S22). 4T22 com R$14,9B = **~3x o nível normal**.

#### LL Recorrente Trimestral (R$M)

| Trim | 1T | 2T | 3T | 4T | Total Ano |
|------|----|----|----|----|-----------|
| 2022 | 6.821 | **7.041** | 5.223 | **1.595** | 20.680 |
| 2023 | 4.280 | 4.518 | 4.621 | 2.878 | 16.297 |
| 2024 | 4.211 | 4.716 | 5.225 | 5.402 | 19.554 |
| 2025 | 5.864 | 6.067 | 6.205 | 6.516 | 24.652 |

> Queda de 2T22 (pico de R$7,0B) para 4T22 (R$1,6B) = **-77% em 2 trimestres**.

#### Saldo de Provisão (PCLD) no Balanço (R$M, negativo = saldo credor)

| Trim | 1T | 2T | 3T | 4T |
|------|----|----|----|----|
| 2022 | -47.149 | — | — | -57.741 |
| 2023 | -60.032 | — | — | -53.901 |
| 2024 | — | — | — | -48.275 |

> O saldo subiu de R$47,1B (1T22) para R$60,0B (1T23) = +R$12,9B de provisões acumuladas em 4 trimestres. A partir de 4T23 começou a cair (liberação gradual de provisão).

#### Custo de Risco Implícito Trimestral (anualizado)

| Período | PDD Trim | Carteira Bruta | Custo Risco (ann.) |
|---------|----------|----------------|--------------------|
| 1T22 | -4.836 | 514.785 | ~3,8% |
| 3T22 | -7.267 | 539.085 | ~5,4% |
| 4T22 | **-14.881** | 542.758 | **~11,0%** |
| 1T23 | -9.517 | 536.255 | ~7,1% |
| 2T23 | -10.316 | 519.506 | ~7,9% |
| 4T24 | -7.460 | 598.221 | ~5,0% |
| 4T25 | -8.828 | ~650.000 | ~5,4% |

## 4T22: O Kitchen-Sink Quarter

O quarto trimestre de 2022 foi o momento de maior ruptura na história recente do sistema bancário brasileiro. O Bradesco provisionou R$14,9B em PDD expandida — aproximadamente o triplo do nível normal.

**O que é um "kitchen-sink quarter":** Estratégia em que o banco concentra em um único trimestre o reconhecimento de perdas que poderiam ser distribuídas ao longo de vários trimestres. A lógica:

1. Limpeza do balanço de uma vez → os trimestres seguintes mostram melhora sequencial (efeito ótico favorável, mesmo sem melhora operacional real).
2. Troca de gestão costuma acompanhar: a nova liderança tem incentivo para reconhecer perdas do período anterior ("é culpa do antigo management").
3. Provisões adicionais constituídas acima do mínimo regulatório criam reserva para absorver perdas futuras sem impactar resultado.

No caso do BBDC4, o 4T22 coincidiu com a transição anunciada de CEO (Octavio de Lazari → Marcelo Noronha, que assumiu formalmente em outubro de 2023), e com o contexto macro mais adverso: Americanas seria revelada apenas 2 meses depois, mas os bancos provavelmente já tinham sinais da deterioração dos seus maiores clientes PJ.

**Índice de Cobertura:**

| Período | Provisão BP | Carteira | Cobertura Implícita |
|---------|-------------|----------|---------------------|
| 1T22 | 47.149 | 514.785 | ~9,2% |
| 4T22 | 57.741 | 542.758 | ~10,6% |
| 1T23 | 60.032 | 536.255 | ~11,2% (pico) |
| 4T23 | 53.901 | 525.968 | ~10,2% (liberando) |
| 4T24 | 48.275 | 598.221 | ~8,1% |

O pico de cobertura em 1T23 (~11,2%) criou o buffer que permitiu a recuperação gradual: à medida que as perdas se materializaram e foram write-offadas, o saldo de provisão foi consumido sem impactar o P&L.

## Comparação entre Bancos

| Banco | PDD Extra 4T22 (vs normal) | LL 4T22 | Queda LL vs pico | ROE pico-crise |
|-------|---------------------------|---------|------------------|----------------|
| **BBDC4** | ~R$10B acima do normal | R$1,6B | -77% vs 2T22 | ~4% |
| ITUB4 | ~R$3-4B acima do normal | ~R$8B | ~-15% vs pico | ~18% |
| SANB11 | Significativo | Afetado | Material | ~13% |

**Por que Itaú foi muito menos afetado:**
- Mix de carteira: maior proporção de grandes empresas investment grade, consignado, imobiliário.
- CET1 maior: mais buffer para absorver perdas.
- Gestão de risco percebida como mais rigorosa (underwriting mais seletivo em PME).
- Menor exposição relativa a varejo PF de renda baixa.

O Itaú ainda foi impactado — a PDD de 2022-2023 subiu acima do patamar 2020-2021 — mas a magnitude foi proporcionalmente muito menor. O ROE do Itaú em nenhum trimestre caiu abaixo de ~15%, enquanto o Bradesco tocou ~4% em 4T22.

## Recuperação (2024-2025)

A normalização se deu em múltiplas camadas:

### 1. Saldo de Provisão ("Liberação de PDD")

O saldo de PCLD no balanço caiu de R$60,0B (1T23) para R$48,3B (4T24) = **R$11,7B "liberados"** em 6 trimestres. Essa liberação não aparece diretamente no P&L como receita, mas sustenta o resultado indiretamente: à medida que créditos são write-offados, a PDD fluxo necessária para recompor o estoque é menor.

### 2. Normalização do Custo de Risco

A PDD expandida trimestral caiu de ~R$10B/trim (média 2023) para ~R$7-7,5B/trim (2024) e a meta de R$8-8,5B em 2025 (refletindo crescimento de carteira). O custo de risco anualizado está convergindo para ~5,3% (guidance), acima do patamar pré-crise (~4%) mas longe do pico de 11% em 4T22.

### 3. Recuperação do NIM

A recomposição do [[nim]] de 10,97% (1T24, trough) para 12,18% (4T25) = +121bps foi impulsionada por:
- Repricing do ativo: contratos antigos de menor taxa vencendo e sendo renovados a taxas mais altas.
- Mix: maior proporção de consignado privado e cartão (produtos de spread maior que grandes empresas).
- Queda da proporção de créditos problemáticos (que ficam em não-accrual, reduzindo o NII bruto).

### 4. Alavancagem Operacional

Com receitas crescendo e despesas controladas, o índice de eficiência caiu de ~50% (pico) para 46,9% (2025A), com trajetória para 44,2% (2026E). A meta de largo prazo é <40% (alinhada ao Itaú).

### Recuperação Quantificada (BBDC4)

| Métrica | Pico Crise | Trough (2023-24) | 4T25 | Alvo LP |
|---------|-----------|-----------------|------|---------|
| LL Recorrente (trim) | R$7,0B (2T22) | R$1,6B (4T22) | R$6,5B | ~R$8-9B |
| ROE | ~13% | ~10% (2023) | ~14,8% | >20% |
| NIM Clientes | ~13% (2022) | 10,97% (1T24) | 12,18% | ~12-13% |
| Custo Risco (ann.) | 11% (4T22) | 7,5% (2023 médio) | 5,4% | ~4-5% |
| Eficiência | ~48-50% | — | 46,9% | <40% |

## Lições para Modelagem

### 1. Assimetria do Ciclo de PDD

O ciclo de provisão é fundamentalmente assimétrico:
- **Constituição**: rápida (1-2 trimestres concentram o grosso das provisões — kitchen-sink).
- **Liberação**: lenta (4-8 trimestres para normalização, nunca há reversão súbita no estoque).

Consequência para projeções: ao modelar uma saída de crise, o [[custo_risco]] cai gradualmente. Nunca assumir que o custo normaliza de um trimestre para o outro.

### 2. Beta de PDD por Banco

Bancos com mix mais arriscado têm "beta de PDD" maior — ou seja, para o mesmo choque macro, a PDD sobe mais em termos proporcionais:

```
Beta de PDD BBDC4 >> Beta de PDD ITUB4
Mesmo choque de inadimplência PME → PDD/carteira sobe muito mais no Bradesco
```

Isso reflete tanto o mix de carteira quanto o estágio do ciclo e as provisões pré-existentes.

### 3. Kitchen-Sink: Não é Catástrofe, é Estratégia

Quando um banco concentra R$10-15B de provisões em um trimestre, o instinto é de alarme. Mas o kitchen-sink é um ato de gestão: o banco está limpando o balanço e reiniciando do zero. Os trimestres seguintes quase invariavelmente mostram melhora sequencial, mesmo sem melhora do ambiente operacional.

Para análise: focar no **tendência de normalização** (trimestres após o kitchen-sink), não no trimestre do pico.

### 4. Coverage Ratio como Amortecedor

O índice de cobertura (estoque PCLD / carteira inadimplente) é o principal buffer:
- Coverage alto (>10%): banco tem capacidade de absorver perdas futuras sem impactar resultado
- Coverage baixo (<7-8%): banco precisa constituir provisões antes de começar a liberar

O BBDC4 em 1T23 com coverage de ~11% tinha "colchão" suficiente para atravessar 2023-2024 sem eventos adicionais de kitchen-sink.

### 5. Efeito das Americanas no Modelo

O impacto das Americanas não foi uniforme: bancos com maior exposição provisionaram mais em 1T23-2T23 independentemente do ciclo PME/PF. Para modelagem retrospectiva de 2023, é útil separar:
- **PDD estrutural** (ciclo de crédito normal): tendência de queda gradual ao longo de 2023
- **PDD Americanas**: one-off de R$2-3B concentrado no 1T23-2T23

## Implicações para 2025-2026

O novo ciclo de alta da Selic (10,5% em set/2024 → ~14,75% em 2026E) replica algumas condições de 2022, mas com diferenças importantes:

**Fatores de proteção vs 2022:**
- Safras de crédito 2023-2024 são de melhor qualidade (seleção mais rigorosa pós-crise)
- Portfólio mais concentrado em consignado e imobiliário (menor sensibilidade ao ciclo)
- Bancos já com coverage ratio elevado (buffer de provisão)
- Empresas grandes (Americanas, Light) já write-offadas — não há evento similar pendente

**Riscos monitorados:**
- PMEs mid-market: segmento que sofre mais com Selic elevada por longo prazo
- Stage 2 migration ([[ifrs9]]): aumento de Stage 2 antecipa deterioração futura
- Inadimplência PF: cartão rotativo e crédito pessoal sensíveis a emprego e renda disponível
- Concentração PJ: casos individuais grandes (não identificados) podem gerar provisões pontuais

**Guidance BBDC4 2026:**
- [[custo_risco]] estável ~5,3% (guidance explícito da administração)
- Crescimento carteira ~9,5% a.a. (guidance explícito)
- Risco de alta se Selic pressionar PME além do esperado

**Monitor trimestral para o analista:**
1. Índice de cobertura (estoque PCLD / NPL >90d) — trending up é alerta
2. Stage 2 migration ratio — % da carteira em Stage 2
3. PDD/trim vs guidance implied quarterly run rate
4. NPL formation por segmento (PF varejo vs PJ mid-market separados)

## Ver Também

- [[bradesco]] — banco mais impactado; narrativa completa do turnaround
- [[itau]] — menos afetado, mais resiliente; referência de risk management
- [[custo_risco]] — a métrica central da crise
- [[ifrs9]] — framework de provisão (COSIF vs ECL); Stage 2 migration
- [[selic]] — driver macro primário do ciclo
- [[cet1]] — buffer de capital que protegeu bancos mais capitalizados
- [[banking]] — contexto setorial e estrutura DRE bancária
- [[crescimento_carteira]] — desaceleração do crédito como sintoma e resposta à crise
- [[nim]] — NIM como o outro lado da moeda do ciclo (benefício Selic, risco inadimplência)
