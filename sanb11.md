---
type: empresa
source_quality: verified
aliases: [Santander Brasil, SANB11, Santander, BSBR]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/SANB11/outputs/model/SANB11_model.json
  - sectors/banking/companies/SANB11/outputs/extraction/SANB11_analyst_mosaic.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
---

# Santander Brasil

O **Banco Santander (Brasil) S.A.** (SANB11) é o terceiro maior banco privado do Brasil por ativos, subsidiária do grupo espanhol Banco Santander S.A. (controlador com ~89% das ações). Difere estruturalmente de [[itau]] e [[bradesco]] por três fatores: controle estrangeiro, ausência de franquia de seguros relevante consolidada, e exposição diferenciada em financiamento de veículos (via Webmotors). Após um ciclo de queda de rentabilidade em 2022-2023, o banco está em trajetória de recuperação — ROE de 17,6% em 4T25 vs meta de >20% para 2027-2028.

## Modelo de Negócio

### Segmentos Operacionais

O Santander Brasil opera em dois segmentos principais:

**1. Varejo (Retail)**
- **PF (Pessoas Físicas)**: produtos de conta corrente, crédito pessoal, consignado, imobiliário, cartão de crédito
- **Select**: segmento de alta renda — principal foco estratégico de crescimento a partir de 2025, com produtos diferenciados e menor inadimplência estrutural
- **PMEs (Pequenas e Médias Empresas)**: capital de giro, crédito, câmbio, seguros PJ; crescimento de +13% em 2025 com foco em clientes de maior valor agregado
- **Financiamento ao Consumo (Santander Financeiras)**: maior financiador de veículos do Brasil, com ~27% de participação nos financiamentos de novos veículos em 2024; integrado com a plataforma **Webmotors** (maior marketplace automotivo do Brasil, subsidiária do grupo)

**2. Atacado (Wholesale/GCB)**
- **Grandes Empresas**: crédito corporativo, operações de câmbio, derivativos, tesouraria
- **Global Corporate Banking (GCB)**: multinationals, operações cross-border com acesso à rede global do grupo espanhol
- Menor presença em agro (diferencial vs Banco do Brasil e [[bradesco]])

### Subsidiárias Relevantes

| Subsidiária | Negócio | Observação |
|-------------|---------|------------|
| Webmotors | Marketplace automotivo + originação de financiamento | Ativo estratégico digital |
| Santander Financeiras | Financiamento de veículos | Líder de mercado ~20%+ |
| Santander Corretora | Distribuição de seguros e previdência | Não consolidada como seguradora |
| Aymoré Crédito | Crédito ao consumidor | Fusionada com Santander Financeiras |

**Nota sobre seguros**: O Santander Brasil NÃO tem uma seguradora consolidada no porte da Bradesco Seguros. Resultado de seguros entra principalmente via comissões de corretagem e produtos distribuídos (não produção própria de risco). Isso é um diferencial estrutural relevante para modelagem — a DRE do Santander é mais "pura" em intermediação financeira vs [[bradesco]].

### Estratégia 2025-2028

Após o ciclo de stress 2022-2023, o banco executou um **repositionamento** de portfólio:
- **Saída de**: baixa renda (PF vulnerável), PME de alto risco, agro
- **Crescimento em**: Select (alta renda PF), PMEs com maior faturamento, cartão de crédito, financiamento de veículos
- **Meta de rentabilidade**: ROE/RoTE >20% até 2027-2028 (Investor Day global fev/2026)
- **Programa "Gravity"**: migração de sistemas para cloud, estimativa de economia de ~R$400M/ano no Brasil
- **Crescimento seletivo**: menor velocidade de expansão de carteira vs Itaú (prioriza retorno ajustado ao risco)
- **ROE 20% adiado**: CEO confirmou (reunião 2026) que meta é factível a partir de 2027, não em 2026

## Disclosure

### Formato do Release Trimestral

O Santander Brasil divulga resultados em **dois padrões**:
- **BRGAAP (COSIF)**: report regulatório para BCB; disponível no site RI e CVM
- **IFRS/Gerencial**: release principal para investidores, base das projeções do modelo

O release gerencial trimestral contém:
- DRE gerencial recorrente (NII Clientes + NII Mercado, PDD, Fees, Despesas, Resultado de Seguros)
- Carteira de crédito ampliada por segmento (PF, PME, Grandes Empresas, Financiamento ao Consumo)
- Inadimplência (90d e 15-90d) por segmento
- Índice de Eficiência (IE) e cobertura
- Capital regulatório (CET1, Basileia)
- Carteira de crédito vencida, cobertura de PDD, inadimplência total

### Onde Encontrar

- **RI oficial**: `www.santander.com.br/ri/resultados` — releases trimestrais em PDF (PT e EN)
- **Planilha RI (séries históricas)**: disponível no site RI, contém séries trimestrais de NII, PDD, Fees, Carteira, Inadimplência desde 2019+
- **CVM (BRGAAP)**: ITR/DFP via `cvmweb.cvm.gov.br` (Banco Santander Brasil SA)
- **SEC (ADR BSBR)**: Form 6-K trimestral via `sec.gov` — em inglês, base IFRS

### Linhas Chave no Release Gerencial

| Linha | Onde Aparece | Observação |
|-------|-------------|------------|
| Margem Financeira c/ Clientes (NII Clientes) | DRE gerencial, linha 1 | Driver principal |
| Margem Financeira c/ Mercado (NII Mercado) | DRE gerencial, linha 2 | Volátil, tesouraria |
| PDD Expandida | DRE gerencial | Inclui recuperação de crédito |
| Receita de Serviços e Tarifas | DRE gerencial | Cartões + tarifas bancárias |
| Resultado de Seguros | DRE gerencial | Distribuição, não produção |
| Despesas não Decorrentes de Juros (DNDJ) | DRE gerencial | Pessoal + administrativo |
| Índice de Eficiência (IE) | Indicadores | = DNDJ / (NII + Fees + Seguros) |
| Inadimplência 90d | Crédito | Indicador de qualidade |
| Cobertura | Crédito | PDD BP / Carteira inadimplente 90d |
| CET1 | Capital | Adequação regulatória |

## Financials Históricos e Projeções

Fonte: releases gerenciais SANB11 / dados públicos. 2026-2027E do modelo interno (SANB11_model.json). Valores em R$ bilhões anuais (estimativas marcadas com *).

| Ano | LL Recorrente (R$B) | ROE | NII Clientes (R$B) | Carteira Crédito (R$B) | Custo Risco |
|-----|---------------------|-----|---------------------|------------------------|-------------|
| 2021 | 16,3 | ~21%* | ~50* | ~480* | ~3,5%* |
| 2022 | 12,9 | ~17%* | ~52* | ~520* | ~5,5%* |
| 2023 | 9,4 | 11,8% | ~55* | ~540* | ~6,0%* |
| 2024 | 13,9 | 15,7% | 59,6 | ~545* | ~4,5%* |
| 2025A | 15,6 | 17,2% | 65,3 | 566 | ~4,5% |
| **2026E** | **17,4** | **17,4%** | **67,7** | **~611** | **4,8%** |
| **2027E** | **19,4** | **17,7%** | **73,1** | **~660** | **4,8%** |

> 2026-2027E: modelo interno (NIM=11,5% implícito, custo_risco=4,8%, aliq.=15%; NII Mercado=**+250M/tri** — cenário normalização Selic 2026H2). 2026E LL acima de 2025A por crescimento de NII Clientes e melhora de NII Mercado vs o pior nível de 2025 (−750M/tri na média).

### Série Trimestral — LL Recorrente (R$M)

| Trim | 2024 | 2025A | 2026E | 2027E |
|------|------|-------|-------|-------|
| 1T | ~3.000* | 3.924 | 4.044 | 4.518 |
| 2T | ~3.300* | 3.612 | 4.294 | 4.786 |
| 3T | ~4.000* | 4.012 | 4.424 | 4.923 |
| 4T | ~3.500* | 4.067 | 4.611 | 5.123 |
| **Ano** | **~13.800*** | **15.615** | **17.373** | **19.350** |

> 2025A verificado via modelo (backtest calibrado). 2024 estimativas. 2026-2027E: modelo SANB11_model.json (NII Mercado = +250M/tri, normalização Selic).

### Narrativa do Ciclo

**2021 — Pico**: LL de R$16,3B, ROE ~21%. O banco operava no "high-teens" de rentabilidade, beneficiado por carteira crescendo pós-pandemia e provisões COVID dissipando.

**2022 — Ruptura**: LL cai 21% para ~R$12,9B. Dois fatores simultâneos: (1) provisões crescendo em linha com inadimplência de PF baixa renda e PMEs, (2) perdas de tesouraria com portfólio de títulos marcado a mercado em ambiente de Selic subindo aggressivamente. O 4T22 foi o pior trimestre, com LL de apenas R$1,7B.

**2023 — Fundo do Ciclo**: LL de R$9,4B, ROE de 11,8% — menor nível em anos. PDD persistentemente alta, NII Clientes estressado. 4T23 sinalizou virada (+30% YoY), mas 2023 como um todo ainda foi o ano de menor rentabilidade recente. Queda de 27,7% no LL vs 2022.

**2024 — Virada**: LL recupera para ~R$13,9B (+47,8% YoY). Provisões normalizando, repositionamento de carteira mostrando efeito. ROE no "mid-teens" (15,7%).

**2025 — Reaceleração Gradual**: LL de R$15,6B (+12,6%), ROE de 17,2%. Crescimento de carteira mais seletivo (+3,7% YoY total, com segmentos como cartão +13%, PME +13%, veículos +13%). Inadimplência voltando a pressionar (NPL 90d subiu para ~3,4% em meados de 2025). Melhor LL trimestral em 4 anos no 4T25 (R$4,1B, ROE 17,6%).

## Drivers Fundamentais

### 1. [[nii_clientes]] — Margem Financeira com Clientes
Principal driver de receita. Determina pelo spread médio da carteira de crédito (NIM clientes) multiplicado pelo volume. O NIM do Santander foi comprimido em 2022-2023 pela combinação de repricing de passivo caro + mix de carteira pior. Em 2025, NII Clientes cresceu +9,5% YoY, com NIM em recuperação. Sensibilidade: +/-50bps no NIM implica ~R$1,5-2,0B no LL.

**Diferencial de mix**: O Santander tem peso relevante em financiamento de veículos (Santander Financeiras + Webmotors) — segmento de spread médio-alto. Em contrapartida, tem menos exposição a agro (spread baixo, mas inadimplência baixa) vs Banco do Brasil e menos consignado público vs [[itau]].

### 2. [[custo_risco]] — PDD / Qualidade de Crédito
O calcanhar-de-aquiles histórico do Santander. Em 2023, o custo de risco foi o mais alto entre os grandes bancos privados. Em 2025, PDD cresceu +8,9% YoY com pressão de inadimplência de PJ (reestruturações) e PF (maior endividamento das famílias). A meta do banco é normalizar para ~4-4,5% anualizado. Sensibilidade: +/-50bps implica ~R$1,5B no LL.

**Monitor crítico**: inadimplência 90d ficou em ~3,4% no 3T25. Trajetória de 2026 (alta vs baixa) é o maior driver de incerteza no modelo.

### 3. [[crescimento_carteira]] — Volume da Carteira de Crédito
Carteira de R$708B em dez/2025. Crescimento 2025 foi seletivo (+3,7% YoY total). Para 2026-2027, banco projeta crescimento abaixo de peers (Itaú ~8-10%, Santander ~5-8%), priorizando retorno ajustado ao risco. Segmentos de maior crescimento: PME, cartão, financiamento veículos; segmentos de redução: baixa renda PF, alguns segmentos de atacado.

### 4. [[indice_eficiencia]] — Eficiência Operacional
IE de ~38,8% no 4T25 — surpreendentemente, o melhor entre os grandes bancos privados em termos de eficiência operacional neste trimestre (Itaú ~38,9%, Bradesco ~46,9%). A vantagem de eficiência é um dos pilares da tese de investimento. Programa "Gravity" deve gerar ~R$400M/ano de savings. Target de crescimento nominal zero de despesas (flat em termos reais).

### 5. [[receita_servicos_tarifas]] — Fee Income
Fees de R$17,5B em 2025 (+3,5% YoY). Cartões foram o destaque (+12,0%), seguidos por seguros (+8,7%). Menor crescimento vs Itaú, refletindo base de clientes menor e mix mais varejo. Oportunidade: crescimento em gestão de investimentos (Select) e serviços para PMEs.

### 6. NII Mercado — Tesouraria
Componente mais volátil. Em 2022, foi o grande vilão (perdas com portfólio de renda fixa marcado a mercado em ambiente de Selic subindo). Em 2025, NII Mercado foi negativo em média −R$867M/tri (pior em 4T25 = −R$1.486M). **Premissa modelo 2026-2027: +R$250M/tri** — baseada em normalização Selic com ciclo de queda esperado em 2026H2, revertendo a pressão de 2025. Esta é a principal diferença vs o modelo conservador anterior (que usava −750M/tri). Sensibilidade: cada +R$250M/tri de NII Mercado = ~+R$1B/ano de LL.

## Posicionamento Competitivo

| Dimensão | SANB11 | [[itau]] (ITUB4) | [[bradesco]] (BBDC4) | BTG Pactual |
|----------|--------|-----------------|---------------------|-------------|
| Porte (Ativos) | ~R$1,0T | ~R$3,1T | ~R$1,7T | ~R$500B |
| Carteira Crédito | ~R$708B | ~R$1,49T | ~R$650B | ~R$200B |
| LL 2025 (R$B) | 15,6 | 46,8 | 24,7 | ~10* |
| LL 2026E (R$B) | 17,4 | 53,7 | 25,6 | ~11* |
| ROE 2025 | 17,2% | 23,4% | 14,8% | ~22%* |
| Índice de Eficiência | ~39% | ~39% | ~47% | ~35%* |
| Custo de Risco | ~4,5%* | ~3,7% | ~5,4% | ~2%* |
| Seguros | Distribuição (não prod.) | Equity method (Porto Seguro) | Consolidado (~25% LL) | Não material |
| Controle | Espanhol (89%) | Brasileiro/Difuso | Brasileiro/Difuso | Brasileiro |
| Foco | Varejo + Veículos + PME | Varejo + Atacado + WM | Varejo + Seguros | Atacado + WM |
| Agro | Mínimo | Moderado | Moderado | Mínimo |

> (*) Estimativas públicas; BTG = referência para atacado, não peer direto no varejo.

**Posicionamento vs Itaú**: Santander tem NIM bruto provavelmente maior (mais exposição a crédito de varejo com spread mais alto), mas ROE inferior — a diferença está no custo de risco histórico mais alto e na menor escala de fee income. O índice de eficiência do Santander é comparável ao Itaú — o Santander não tem o peso de agências físicas que o Bradesco carrega.

**Diferencial Webmotors**: Único entre os grandes bancos a ter um marketplace automotivo próprio. Integração origina financiamentos com custo de aquisição de cliente menor. Vantagem estrutural em financiamento de veículos (27% de participação nas aprovações de novos veículos em 2024).

**Risco de controle estrangeiro**: O banco espanhol detém ~89% das ações. Há especulação recorrente de OPA (oferta pública de aquisição) para fechamento do capital no Brasil — analistas do Citi levantaram o tema em 2026. O free float limitado implica menor liquidez e potencial prêmio de controle.

## Riscos

1. **Controle Espanhol e Risco de Subordinação de Capital**: O grupo espanhol pode priorizar outras geografias (México, EUA, Europa) no alocação de capital, limitando o crescimento orgânico do Brasil. Decisões de dividendos e CET1 target são influenciadas pela controladora, não apenas pela dinâmica local.

2. **Inadimplência Persistente (Ciclo de Crédito)**: O Santander teve o pior ciclo de inadimplência entre os grandes privados em 2022-2023. O repositionamento de carteira mitiga, mas não elimina o risco. Em 2025, o NPL 90d voltou a pressionar em 3,4% no 3T25, antecipando cuidado com PJ mid-market em 2026.

3. **Webmotors / Financiamento Automotivo**: Concentração em veículos (~20%+ da carteira PF) é um risco específico. Ciclos negativos do mercado automotivo (inadimplência de financiamento de carros, compressão de spreads por competição) afetam desproporcionalmente o Santander.

4. **Meta de ROE 20% Adiada**: Guidances sucessivos de ROE >20% não foram entregues (2023 falhou, 2025 falhou, target agora é 2027-2028). Credibilidade do management está sob escrutínio. Cada trimestre de ROE abaixo de 20% mantém o desconto de valuation vs peers.

5. **Transformação Digital vs Fintechs**: O banco compete com [[nubank]] e outras fintechs em produtos de varejo PF (crédito pessoal, cartão). O app do Santander (Super App) e a integração com Webmotors são diferenciais, mas a execução digital é mais lenta que a esperada pelo mercado.

6. **Risco de JCP**: Eliminação do JCP afetaria o Santander de forma similar a outros bancos — alíquota efetiva subiria de ~30-35% para ~38-40%. Impacto estimado de ~R$2-3B no LL anual (estimativa; verificar em modelo).

7. **OPA / Fechamento de Capital**: Especulação de que a controladora espanhola pode lançar OPA para fechar o capital. Para o acionista minoritário, seria positivo (prêmio), mas elimina a opcionalidade de melhora gradual de ROE como tese de investimento em bolsa.

## Para o Modelo

```
- Modelo: sectors/banking/companies/SANB11/outputs/model/SANB11_model.json
- Estrutura: único consolidado (sem EP investidas materiais; Webmotors operacional, não financeira)
- Planilha RI: filings/planilhas/ (séries históricas gerenciais)
- Release: filings/releases/ (releases trimestrais PDF)
- Padrão: gerencial/IFRS (NÃO usar BRGAAP COSIF como base do modelo)
```

### Premissas Calibradas (Modelo 2026-2027E)

| Premissa | Valor Modelo | Calibração Histórica | Fonte do Ajuste |
|----------|-------------|---------------------|-----------------|
| NIM Clientes (implícito) | **11,5%** | 11,1-12,2% em 2024-2025 (avg 2025 ~11,95%) | Mosaic override: corrige denominador diferente do Santander |
| Custo de Risco | **4,8%** | Média 2024-2025 = 4,56% | Mosaic: +0,2pp por NPL 90d em trajetória de alta |
| Alíquota Efetiva | **15,0%** | 2024 normalizado 13,6-14,5%; 2025 distorcido por CMN 4.966/21 | Mosaic: cautela pós-transição DTA |
| Crescimento Carteira | **8,0% YoY** | 2025: +3,7% (seletivo); guidance implícito 8-10% | Graph default: guidance implícito de crescimento |
| Índice de Eficiência (core) | **31,5%** | Média 2024-2025 = 31,4% (ex-desp. tributárias) | Graph default calibrado |
| NII Mercado | **+250 M/tri** | 2025 avg = -867M/tri; 4T25 = -1.486M | Mosaic override: normalização Selic 2026H2 (+R$1,2-1,5T carteira prefixada) |
| Fees crescimento | **6,0% YoY** | Média YoY 2025 = 3,5%; cartão +12% | Graph default: acima da média por mix Select/cartão |

> **Nota metodológica NIM**: O NIM de 10,7% reportado pelo Santander usa denominador diferente (carteira ampliada). O modelo usa carteira gerencial (~R$566B) como base, resultando em NIM implícito de 11,5%. Histórico calibrado confirma 11,1-12,2% — o override via mosaic corrige esta diferença metodológica, não adiciona upside artificial.

### Estrutura DRE Gerencial SANB11

```
NII Clientes (Margem Financeira c/ Clientes)
(+) NII Mercado (Margem Financeira c/ Mercado)
= NII Total (Margem Financeira Bruta)
(-) PDD (Provisão para Perdas de Crédito)
= Margem Financeira Líquida
(+) Receita de Serviços e Tarifas (Fees)
(+) Resultado de Seguros (distribuição)
= Produto Bancário Líquido de PDD
(-) Despesas de Pessoal
(-) Despesas Administrativas
(-) Despesas Tributárias
= Resultado Operacional
(+/-) Outras Receitas/Despesas
(-) IR / CSLL
= Lucro Líquido Recorrente
```

> Santander não tem equivalência patrimonial material (Webmotors é subsidiária operacional, não investida financeira).

## Consenso de Mercado vs Modelo (2026-04-04)

Fonte: Yahoo Finance / BSBR ADR (4 analistas para 2026E, 4 para 2027E). EPS convertido via âncora LL 2025A.

| Métrica | Modelo | Consenso | Gap | Status |
|---------|--------|----------|-----|--------|
| LL 2026E | R$17.373M | ~R$16.813M | **+3,3%** | OK (<15%) |
| LL 2027E | R$19.350M | ~R$18.520M | **+4,5%** | OK (<15%) |
| Receita 2026E | — | R$89,3B | — | Não comparado diretamente |

**Modelo levemente acima do consenso** em ~3-4% — gap atribuído a: NII Mercado premissa +250M/tri (normalização Selic) vs consenso provável mais conservador. Custo de risco 4,8% alinhado com consenso. Gap dentro da faixa de conforto (<15%).

## Tese de Investimento (Modelo 2026-04-04)

**Bull Case**: ROE recovery de 17,2% (2025) para ~20% (2027-2028) via: (1) mix shift para Select e PME comprimindo custo de risco, (2) repricing de carteira elevando NIM, (3) ciclo de queda de [[selic]] liberando NII Mercado (+R$400-600M/ano por -100bps). Desconto vs [[itau]] excessivo se fundamentals convergem.

**Base Case (modelo)**: LL 26E R$17,4B (+11% YoY) — crescimento via NII Clientes +4% e NII Mercado normalizando para +250M/tri (vs -867M/tri em 2025). LL 27E R$19,4B (+11% YoY). ROE 26E 17,4% / 27E 17,7%. Meta de 20%+ em 2027-2028 ainda requer mais crescimento de carteira e compressão de custo de risco.

**Bear Case**: NPL 90d continua subindo para 4,5%+, custo de risco para 5,5%+, meta ROE 20% adiada novamente para 2029. LL 26E < R$13B. Desconto vs Itaú se amplia.

**Principal Gatilho de Upside**: Ciclo de queda de [[selic]] em 2026H2. Cada -100bps de Selic = ~R$100-150M/tri de melhora no NII Mercado (carteira prefixada) = +R$400-600M/ano de LL.

**Principal Risco**: NPL 90d (estava em 3,7% em 4T25). Trajetória 2026 é o maior swing factor do modelo.

## Ver Também

- [[banking]] — perfil do setor bancário brasileiro (DuPont, Basileia, ciclo de crédito)
- [[itau]] — benchmark de rentabilidade e eficiência
- [[bradesco]] — principal peer em varejo, referência de turnaround
- [[nii_clientes]] — driver principal de receita
- [[custo_risco]] — driver de qualidade de crédito e principal risco
- [[carteira_credito]] — volume driver do NII
- [[indice_eficiencia]] — ponto forte estrutural do Santander
- [[nim]] — net interest margin
- [[crescimento_carteira]] — driver de volume
- [[receita_servicos_tarifas]] — fee income
- [[resultado_seguros]] — para bancos com seguros consolidados (não é o caso do SANB11)
- [[cet1]] — adequação de capital (Basileia III)
- [[selic]] — driver macro de NIM e float
- [[nubank]] — competidor digital em produtos de varejo
