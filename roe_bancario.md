---
type: conceito
source_quality: conceptual
aliases: [ROE, Return on Equity, Retorno sobre Patrimônio Líquido, ROE Bancário]
sources:
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_investment_memo.md
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
updated: 2026-04-05
---

# ROE Bancário

O **ROE** (Return on Equity / Retorno sobre Patrimônio Líquido) é o KPI de rentabilidade primário para bancos. Mede o retorno gerado pelo banco para cada real de capital próprio investido pelos acionistas. É a métrica central para avaliação de qualidade de gestão, pricing relativo (via P/BV) e sustentabilidade do modelo de negócio.

## Definição e Fórmula

```
ROE = Lucro_Líquido_Anualizado / PL_Médio
    = LL_12m / ((PL_início + PL_fim) / 2)
```

**Convenção de anualização:**

Para um trimestre isolado:

```
ROE_trimestral_anualizado = LL_trimestral × 4 / PL_médio_trimestre
```

Para 12 meses acumulados (forma mais usual nas comparações):

```
ROE_12m = LL_LTM / PL_médio_LTM
```

> **Atenção:** Usar PL_médio (e não o PL final) é essencial. Um banco que distribui muito dividendo ao longo do ano reduz o PL final, inflando o ROE calculado sobre o saldo de fim de período. O PL médio captura corretamente o capital efetivamente em operação durante o período.

**Referência ITUB4 2025:**

```
ROE_2025 = R$46,8B / ~R$200B ≈ 23,4% a.a.
```

O Itaú divulga o ROE Recorrente Gerencial nos releases, calculado sobre o PL médio ajustado (excluindo ágio e intangíveis em algumas versões). Usar a mesma base historicamente para evitar quebras de série.

---

## DuPont Bancário

A decomposição DuPont decompõe o ROE em dois fatores: rentabilidade do ativo (ROA) e uso de alavancagem de balanço (Multiplicador de Capital).

```
ROE = ROA × Multiplicador_Capital

onde:
  ROA                  = LL / Ativos_Totais
  Multiplicador_Capital = Ativos_Totais / PL
```

### Por Que Bancos Têm ROA Baixo mas ROE Alto

Bancos são máquinas de alavancagem. O ativo total é financiado majoritariamente por passivos (depósitos, letras financeiras, captações interbancárias) — o PL é apenas uma fatia pequena do funding. Um banco típico opera com PL equivalente a ~8-12% dos ativos; o restante é dívida de terceiros.

Isso cria um perfil de DuPont oposto ao de empresas industriais:
- **Empresa industrial:** ROA alto (~8-15%), alavancagem baixa (1,5-3×) → ROE moderado
- **Banco:** ROA baixo (~1-3%), alavancagem alta (8-12×) → ROE alto

O ROA bancário é comprimido porque o ativo total inclui o denominador de toda a intermediação (carteira de crédito + TVM + compulsórios + interbancário), que é muito maior que o PL. O banco não precisa de ROA alto porque o funding é barato (CDI − spread de captação) e escalável.

### Âncoras ITUB4 2025

| Componente | Valor | Nota |
|-----------|-------|------|
| Lucro Líquido (LL) | R$46,8B | 12 meses 2025 |
| Ativos Totais | ~R$2,0T | Estimativa balanço consolidado |
| PL Médio | ~R$200B | PL médio 2025 |
| **ROA** | **~2,3%** | LL / Ativos |
| **Multiplicador de Capital** | **~10,0×** | Ativos / PL |
| **ROE** | **~23,4%** | ROA × Multiplicador |

**Leitura:** O Itaú converte cada real de ROA em ~10× ROE via alavancagem. Mesmo que o ROA caísse 20bps (de 2,3% para 2,1%), com o mesmo multiplicador o ROE cairia ~2pp (de 23,4% para ~21%). A alavancagem amplifica tanto os ganhos quanto as perdas.

### Decomposição DuPont Estendida

Para uma análise mais granular, o ROE pode ser decomposto em quatro drivers operacionais:

```
ROE = Margem_Líquida × Giro_do_Ativo × Multiplicador_Capital

onde:
  Margem_Líquida   = LL / Receita_Total
  Giro_do_Ativo    = Receita_Total / Ativos
  Multiplicador    = Ativos / PL
```

Esta versão conecta o ROE às alavancas gerenciáveis: precificação (margem), eficiência de uso de ativo (giro) e política de capital (multiplicador). Para análise de bancos, o Giro do Ativo equivale ao [[nim]] — a intensidade com que o ativo gera receita.

---

## Drivers do ROE Bancário

Os cinco drivers estruturais do ROE bancário, em ordem de impacto para grandes bancos brasileiros:

| Driver | Medida | Impacto no ROE | Lever gerencial |
|--------|--------|---------------|-----------------|
| **1. NIM — Volume × Spread** | [[nim]] × [[crescimento_carteira]] | Principal componente do ROA; 12% de NIM × R$1,1T de carteira = ~R$132B de NII | Pricing, mix de produtos, crescimento |
| **2. Custo de Risco** | [[custo_risco]] (%) | Consome ~30-40% do NIM bruto; 1pp de custo adicional = R$11B de despesa | Seleção de risco, concentração, ciclo |
| **3. Eficiência Operacional** | [[eficiencia_operacional]] (IE) | Despesas operacionais como % da receita; 1pp de melhoria no IE = ~R$1-2B de LL | Digitalização, escala, headcount |
| **4. Alíquota Efetiva** | [[aliquota_efetiva]] | Taxa efetiva de IR+CS; JCP reduz a alíquota para ~30% (vs ~34% sem JCP) | Estrutura tributária, JCP, mix geográfico |
| **5. Capital (Multiplicador)** | Ativos / PL | Alavancagem amplifica ROA → ROE; regulação CET1 define o piso de capital | Distribuição de dividendos, crescimento, RWA |

### Como Cada Driver Conecta ao Modelo

O modelo [[itau]] modela diretamente os drivers 1-4 via premissas explícitas. O multiplicador de capital é resultante (não premissa) — é determinado pelo crescimento do PL via retenção de lucros e pela trajetória dos ativos via crescimento de carteira.

---

## ROE Sustentável vs ROE Contábil

O ROE contábil reportado pode ser inflado por fatores temporários ou por opções de distribuição de capital. É fundamental distinguir o ROE sustentável (steady-state) do ROE corrente.

### Efeito do Payout no ROE

Um payout alto reduz o PL ao distribuir mais lucro do que o necessário para sustentar o crescimento. Com PL menor, o multiplicador de capital sobe e o ROE sobe — mas esse ganho não é sustentável sem crescimento de lucro correspondente.

**Ilustração:**

```
Caso Base:
  LL = R$47B; PL = R$210B; ROE = 22,4%
  Payout 50%: dividendos = R$23,5B; PL cresce +R$23,5B/ano → PL cresce com o lucro

Caso Payout Elevado (Itaú 2025: 72%):
  LL = R$47B; dividendos = R$33,8B; retenção = R$13,2B
  PL cresce +R$13,2B/ano (vs +R$23,5B no caso base)
  → PL cresce menos que o lucro → PL médio menor → ROE maior (artificialmente)
```

**Itaú 2025:** Payout de 72% (incluindo dividendos extraordinários). O PL cresce mais devagar que o lucro, sustentando um ROE acima de 23% mesmo sem expansão de margem ou corte de custos. Esse ROE é "inflado" pelo payout — ao normalizar o payout para ~55% (guidance 2026), o PL acumula mais rápido e o ROE tende a comprimir ligeiramente no longo prazo.

### Fórmula do ROE Sustentável

```
ROE_sustentável ≈ ROE_atual × (1 - Payout) + crescimento_orgânico_ROE

Ou simplificando:
  g = ROE × Taxa_de_Retenção = ROE × (1 - Payout)
```

Para o Itaú com ROE = 23,4% e retenção de 28%:

```
g_orgânico ≈ 23,4% × 28% ≈ 6,6% a.a.
```

Este é o crescimento de PL (e portanto de carteira) que o Itaú pode sustentar sem emitir capital novo. Se o banco cresce a carteira acima de 6,6% a.a., precisa ou aceitar redução de capital ratio, ou emitir ações, ou ajustar o payout.

### Quando o ROE é Inflado vs Sustentável

| Situação | ROE inflado? | Causa |
|----------|-------------|-------|
| Payout acima de 65% de forma recorrente | Sim | PL não cresce com o lucro |
| Provisões complementares liberadas | Sim | LL temporariamente elevado |
| Ciclo de crédito benigno (inadimplência mínima histórica) | Parcialmente | Custo de risco abaixo do normalizado |
| Escala + alavancagem operacional genuína | Não | Estrutural e sustentável |
| Crescimento de carteira com qualidade (NIM ajustado estável) | Não | Estrutural e sustentável |

---

## Relação ROE × Valuation (P/BV)

O múltiplo P/BV (Price-to-Book Value) é o múltiplo de valuation natural para bancos, e sua relação com o ROE é matemática — derivada do modelo de Gordon Growth adaptado para empresas que crescem pelo reinvestimento.

### Fórmula P/BV Justo

```
P/BV = (ROE - g) / (Ke - g)

onde:
  ROE = Return on Equity (% a.a.)
  g   = Taxa de crescimento sustentável do LL no longo prazo (% a.a.)
  Ke  = Custo do capital próprio (% a.a.)
```

**Intuição:** Um banco vale exatamente seu valor patrimonial (P/BV = 1×) quando ROE = Ke. Se ROE > Ke, o banco destrói valor ao ser avaliado ao book — merece P/BV > 1×. Se ROE < Ke, deve valer abaixo do book.

### Cálculo P/BV Justo — ITUB4

**Premissas:**
- ROE = 24% (forward, arredondado)
- g = 8% (crescimento nominal de longo prazo: PIB real ~2% + inflação ~5% + mix ~1%)
- Ke = 14% (risk-free Selic longa ~7% + prêmio de risco país ~3% + beta ajustado ~4%)

```
P/BV_justo = (24% - 8%) / (14% - 8%)
           = 16% / 6%
           = 2,67×
```

**Tabela de sensibilidade P/BV × ROE e Ke:**

| ROE \ Ke | 12% | 13% | 14% | 15% | 16% |
|----------|-----|-----|-----|-----|-----|
| **20%** | 2,5× | 2,0× | 1,7× | 1,5× | 1,3× |
| **22%** | 3,5× | 2,8× | 2,3× | 2,0× | 1,7× |
| **24%** | 4,0× | 3,2× | 2,7× | 2,3× | 2,0× |
| **26%** | 4,5× | 3,7× | 3,0× | 2,6× | 2,3× |
| **28%** | 5,0× | 4,2× | 3,3× | 2,9× | 2,5× |

*(g = 8% fixo em todos os casos)*

### Qual o Ke Correto para Bancos Brasileiros?

O custo de capital próprio (Ke) para bancos brasileiros incorpora:

```
Ke = Risk_free + Beta × ERP + Country_Risk_Premium

Estimativa para ITUB4 (2026):
  Risk-free (Selic longa ou NTN-B 10a): ~7,0%
  Beta do setor (1,0-1,1×) × ERP global (5%): ~5,0-5,5%
  CRP adicional (acima do global): ~1,5-2,0%
  ─────────────────────────────────────────────
  Ke: ~13,5-14,5% → midpoint ~14%
```

**Efeito da Selic no Ke:** Em cenário de queda de Selic (risk-free cai de 7% para 5%), o Ke cai ~2pp, o que — mantendo ROE e g constantes — eleva o P/BV justo:

```
P/BV com Ke=12%, ROE=24%, g=8% = (24-8)/(12-8) = 4,0×
```

Ou seja: queda de Selic tem efeito duplo positivo nos bancos — reduz o risco-livre (Ke cai) E pode reduzir inadimplência (ROE sobe). O banco pode ser re-rateado com P/BV muito superior ao atual se a Selic ceder estruturalmente.

### Relação com Preço-Alvo

```
Preço_Alvo = P/BV_justo × BV_por_ação_forward

Exemplo (ITUB4):
  BV por ação 2026E ≈ R$19,50 (estimativa)
  P/BV justo = 2,7×
  Preço_Alvo = R$19,50 × 2,7 = R$52,65
```

---

## Headwinds ao ROE

Os principais fatores que podem comprimir o ROE do Itaú nos próximos ciclos:

| Headwind | Mecanismo | Magnitude estimada |
|---------|-----------|-------------------|
| **Queda da Selic** | Reduz NIM_CG (~R$6B de NII por cada 300bps de queda de CDI) e pressiona spreads via concorrência | ROE −1 a −3pp se Selic cair a 9-10% |
| **Eliminação do JCP** | Alíquota efetiva salta de ~30% para ~38%; impacto ~R$4-5B/ano no LL (~10%) | ROE −2 a −2,5pp |
| **Acumulação de capital acima do target CET1** | PL cresce mais que o LL → multiplicador cai → ROE comprime | −0,5 a −1pp por 50bps de excesso de CET1 |
| **Normalização do custo de risco** | Quando o ciclo de crédito virar, custo pode subir 50-100bps vs 2025 | ROE −1 a −2pp |
| **Desaceleração de carteira** | Menor volume de NII; alavancagem operacional não se materializa | ROE −0,5 a −1pp por 2pp de gap vs guidance |

**Nota sobre JCP:** O Imposto de Renda permite que empresas (incluindo bancos) remunerem o acionista via JCP (Juros sobre Capital Próprio), que é dedutível do lucro tributável. Para o Itaú, com PL de ~R$200B e taxa de JCP regulatória (TJLP/Selic) de ~12%, o benefício fiscal é ~R$4-5B/ano. Qualquer mudança regulatória que elimine o JCP seria um headwind permanente e significativo.

---

## ITUB4 vs Pares

Comparativo de ROE entre grandes bancos listados no Brasil (2025, aproximado):

| Banco | Ticker | ROE 2025 | Fase | Nota |
|-------|--------|---------|------|------|
| [[itau]] | ITUB4 | ~23-24% | Maturidade | Best-in-class; IE de 39%; menor custo de risco entre privados |
| Santander BR | SANB11 | ~18% | Normal | Bom ROE histórico; menor diversificação que Itaú |
| Banco do Brasil | BBAS3 | ~20-21% | Normal | Alta rentabilidade mas desconto de múltiplo por risco político/governança |
| [[bradesco]] | BBDC4 | ~12-14% | Turnaround | Em normalização pós-ciclo adverso; ROE historicamente ~18-20% |

### Por Que o Bradesco Tem ROE Tão Abaixo?

A lacuna Itaú vs [[bradesco]] em ROE reflete três descontos estruturais em 2025:

1. **Custo de risco mais alto:** ~4,5-5% vs ~3,7% para o Itaú → diferença de ~80bps de custo no ROA
2. **[[nim]] menor:** ~10-11% vs ~12% para o Itaú → diferença de ~100-200bps de NIM
3. **Eficiência inferior:** IE ~43-45% vs ~39% do Itaú → mais custo por real de receita

Com ROA de ~1,2-1,4% e multiplicador similar (~10×), o Bradesco entrega ROE ~12-14% — consistente com DuPont. O plano de turnaround (management contratado em 2024) mira ROE de ~18-20% no médio prazo via melhora dos três vetores simultaneamente.

---

## Por Empresa

### [[itau]] (ITUB4)

**Trajetória:**
- 2020: ROE comprimido (~13-14%) por provisões antecipadas COVID
- 2021: Recuperação rápida (~19%), beneficiado por reversão de provisões
- 2022-23: Ciclo adverso de crédito; ROE caiu para ~18-20%
- 2024: Início de recuperação; ROE ~20,1%
- **2025: ROE ~23,4% — melhor nível desde 2019-20 pré-COVID**
- 2026E: ROE ~23,9% (modelo); sustentado por alavancagem operacional e custo de risco controlado
- 2027E: ROE ~23,0% (modelo); leve compressão por payout normalizado e crescimento de PL

**Características estruturais:**
- Maior banco privado do Brasil por ativos e LL
- [[eficiencia_operacional]] best-in-class (IE ~39%): principal motor de sustentabilidade do ROE
- Crescimento de carteira guiado por consignado privado CLT e varejo
- JCP estrutural protege a alíquota efetiva (~29-30%)
- Payout 72% em 2025 (extraordinário); guidance 55% para 2026+

### [[bradesco]] (BBDC4)

**Trajetória:**
- Histórico: ROE ~18-22% em ciclos normalizados (2013-19)
- 2020-21: COVID + provisões, ROE comprimiu para ~14-16%
- 2022-23: Ciclo adverso de crédito; eventos idiossincráticos (Americanas); ROE caiu para ~10-13%
- **2025: ROE ~12-14% — ainda em turnaround**
- Meta de médio prazo: ROE ~18-20% (guidance novo management)

**O que precisa acontecer para o turnaround:**
1. [[custo_risco]] normalizar de ~4,5-5% para ~3-3,5%
2. [[nim]] se expandir via repricing e mix shift
3. Controle de despesas e ganho de [[eficiencia_operacional]]

Cada um desses passos tem um lag de 4-8 trimestres — o mercado precifica a probabilidade e o tempo de convergência. Enquanto o ROE estiver em ~13%, o P/BV justo é apenas ~1,3-1,5× (vs ~2,7× para o Itaú).

---

## Ver Também

- [[banking]] — estrutura da DRE e KPIs setoriais completos
- [[cet1]] — capital adequacy ratio que define o piso de capital e o multiplicador
- [[aliquota_efetiva]] — JCP, IR e CS; risco de eliminação de JCP
- [[eficiencia_operacional]] — índice de eficiência, DNDJ, alavancagem operacional
- [[nii_clientes]] — principal driver de receita que sustenta o ROA
- [[itau]] — perfil completo ITUB4, premissas, drivers e riscos
- [[bradesco]] — trajetória de turnaround e convergência de ROE
- [[custo_risco]] — custo do crédito como destruidor de ROA
- [[nim]] — margem financeira líquida, NIM ajustado pelo risco
