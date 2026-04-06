---
type: conceito
aliases: [NII Clientes, NII de Clientes, Margem Financeira de Clientes, Client NII]
source_quality: partial
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/filings/releases/ITUB4_release_2025.pdf
  - sectors/banking/companies/ITUB4/filings/apresentacoes/ITUB4_apresentacao_4T25.pdf
  - sectors/banking/companies/BBDC4/filings/releases/BBDC4_release_4T25.pdf
  - sectors/banking/companies/BBDC4/filings/series_historicas/BBDC4_series_historicas_4T25.xlsx
updated: 2026-04-05
note: "2026-04-03: BBDC4 taxa_media=9.0% e saldo_medio=R$873,597M extraídos de release p.9 — verified. NIM 12.5% back-calculado substituído. ITUB4: NIM_sensíveis=8.6% (real)"
learning_loop_notes:
  - "wiki_expansion 2026-04-03: decomposição em sensíveis_a_spread + capital_de_giro documentada; graph_patch proposto pendente extração histórica dos PDFs"
  - "wiki_expansion 2026-04-03: seção BBDC4 vs ITUB4 adicionada com decomposição NII_CG/NII_Sensíveis, efeito alavancagem, impacto por 100bps Selic e trajetória histórica Bradesco"
---

# NII de Clientes

O **NII de Clientes** (Net Interest Income — Clientes) é o componente do [[nim]] gerado pelas operações de crédito com clientes: a diferença entre a taxa de concessão de crédito cobrada dos tomadores e o custo de captação de funding pago aos depositantes, multiplicada pelo volume da carteira.

É o principal driver de receita dos grandes bancos brasileiros e o componente mais estável do NII total (em contraste com o [[nii_mercado]], que é mais volátil).

## Como Funciona

```
NII_Clientes = Carteira_Crédito_Média × (Taxa_Concessão - Custo_Captação)
             = Carteira_Crédito_Média × Spread_Clientes
```

Na prática, os releases publicam NII Clientes como linha consolidada. Para modelagem, o driver principal é:

```
NII_Clientes(t) = NII_Clientes(t-4) × (1 + g_yoy)
```

onde `g_yoy` é o crescimento YoY orientado pelo guidance de [[crescimento_carteira]] e pelo movimento da [[selic]].

## Decomposição Estrutural: Sensíveis a Spread + Capital de Giro

Itaú (e outros grandes bancos) decompõe o NII Clientes em dois sub-componentes estruturais nas apresentações de resultado:

```
NII_Clientes = NII_Sensíveis_Spread + NII_Capital_de_Giro
```

| Sub-componente | Driver | Sensibilidade |
|----------------|--------|---------------|
| [[nii_sensiveis_spread]] | Carteira ativa × Spread acima do benchmark | Crescimento de carteira + spread de crédito |
| [[remuneracao_capital_giro]] | Patrimônio líquido × CDI/Selic (funding notional) | Diretamente proporcional à Selic |

### Sensíveis a Spread

São as operações onde o banco ativamente gerencia o spread cobrado do cliente **acima** da taxa de referência (CDI). Incluem:
- Crédito PF: pessoal, cartão, veículos, imobiliário (spread sobre CDI)
- Crédito PJ: capital de giro empresarial, trade finance, grandes empresas
- Consignado: taxa fixa × custo de funding

O driver de longo prazo é o **mix da carteira** (crédito mais arriscado = spread mais alto) e o **repricing gap** (prazo médio dos ativos vs passivos).

### Capital de Giro / Remuneração do Capital Próprio

Representa a remuneração do **patrimônio líquido** do banco aplicado a taxas de mercado (CDI/Selic), ou seja, o "equity hedge" — a parcela do NII que cresce automaticamente com a taxa básica independentemente de movimentos de spread.

Intuição: o banco não precisa captar recursos (tem equity) para financiar parte da carteira. Essa parcela gera NII à taxa CDI sem custo de funding correspondente. Quando [[selic]] sobe, esta parcela sobe proporcionalmente.

```
NII_CG ≈ PL_médio × CDI_trimestral
```

Para Itaú, o dado real do release 4T25 mostra: base "Capital de Giro Próprio e outros" = R$146,248M (não o PL total de ~R$206B), margem = R$3,975M/trim, taxa = 11.2% a.a. — representando ~**13% do NII Clientes total** de R$30,930M (Fonte: Release 4T25).

### Implicações para Modelagem

O modelo atual usa `NIM × carteira_media`, que **não separa** os dois componentes. Isso cria um problema:

- Em ciclos de alta de Selic, o NIM sobe em parte pela remuneração do capital de giro (automático) e em parte por repricing da carteira (gerenciável)
- O modelo trata ambos como um único NIM, não permitindo analisar o impacto de Selic isolado do impacto de spread

Um graph patch estrutural decompondo `in:nim` em `in:spread_sensiveis` + `in:cdi_proxy` com `der:base_capital_giro` (≈ PL médio) permitiria análise de sensibilidade mais precisa.

**Status do patch**: hipótese estrutural identificada. Critério de aprovação: 4+ trimestres de dados dos sub-componentes extraídos dos releases (PDFs). Pendente extração quando pdftoppm estiver disponível. Ver `ITUB4_graph_patch_nii_decomposicao.json`.

### Componentes do Spread

| Componente | Direção com Selic alta | Observação |
|------------|----------------------|------------|
| Taxa de concessão de crédito | Sobe (ativos pós-fixados) | Depende do mix de carteira |
| Custo de captação (depósitos, LF) | Sobe | Passivos pós-fixados reagem mais rápido |
| Spread líquido | Ambíguo (depende do repricing gap) | Maior para bancos com mais crédito pré-fixado |

**Repricing gap:** Bancos com ativo pré-fixado e passivo pós-fixado perdem NIM quando Selic sobe. Bancos com ativo e passivo ambos pós-fixados tendem a manter spread estável.

## No Contexto Brasileiro

- **Consignado** (desconto em folha): spread baixo (~10-15% a.a. líquido do custo de funding), risco baixo, capital leve
- **Cartão de crédito rotativo**: spread altíssimo (>100% a.a.), mas inadimplência enorme — NII bruto é ilusório sem [[custo_risco]]
- **Crédito imobiliário**: spread muito baixo (IPCA+3-5% a.a.), longo prazo, RWA baixo
- **Capital de giro PJ**: spread médio, dependente do ciclo econômico

O **mix shift** entre esses segmentos é um driver silencioso do NII Clientes: banco que migra carteira para produtos de maior spread aumenta NII sem necessariamente crescer o volume.

### Selic e NII Clientes

A relação [[selic]] × NII Clientes é não-linear:
- **Curto prazo**: Selic alta → taxas de concessão sobem → NII Clientes aumenta (se ativos reprecificam mais rápido que passivos)
- **Médio prazo**: Selic alta → demanda de crédito cai → [[crescimento_carteira]] desacelera → NII Clientes desacelera
- **Patamar alto por mais tempo**: NIM se estabiliza, mas inadimplência pode subir (via [[custo_risco]])

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | NII Clientes 4T25: R$30,930M/trim (Fonte: Release 4T25). NIM total MFC 8.9% a.a. Guidance NII Clientes +5-9% em 2026. NII_CG (capital de giro alocado) = R$3,975M/trim (~13% do total) sobre base de R$146B — a parcela da tesouraria (~R$60B do PL) vai para NII_Mercado. NIM_Sensíveis = **8.6%** a.a. (não 9.4% como estimado anteriormente). Mix favorável: consignado privado acelerando (R$1.9B/mês jan/26), grandes empresas, crédito imobiliário. |
| [[bradesco]] | **NII Clientes 4T25: R$19,119M/trim. Saldo médio: R$873,597M. Taxa média: 9.0% a.a. (compound).** (Fonte: Release 4T25 p.9). Em turnaround. Mix shift gradual para menor risco (consignado, imobiliário). Bradesco Seguros não entra no NII. Nota: BBDC4 publica taxa_media e saldo_medio diretamente — usar como inputs verificáveis no modelo (não back-calcular). |

## Por Empresa — Comparação BBDC4 vs ITUB4

### Decomposição NII_CG vs NII_Sensíveis (4T25)

| Métrica | BBDC4 (4T25) | ITUB4 (4T25) |
|---------|-------------|-------------|
| NII Clientes (R$M/trim) | **R$19,119M** (Fonte: Release 4T25 p.9) | **R$30,930M** (Fonte: Release 4T25) |
| Saldo médio carteira (R$M) | **R$873,597M** (Fonte: Release 4T25 p.9) | ~R$1.100B (Brasil); ~R$1.280B (sensíveis incl. LatAm) |
| Taxa média NIM (compound a.a.) | **9.0%** (Fonte: Release 4T25 p.9) | **8.9%** MFC total (Release 4T25) |
| PL Controladores (R$M) | R$172,239M (BP 4T25) | ~R$206B (total); ~R$146B alocado às áreas |
| PL / Saldo médio carteira | ~20% | ~19% |
| **NII_CG** (capital de giro próprio) | Inside Margem Mercado (~R$126M/trim) | **R$3,975M/trim** (Release 4T25, tabela taxas) |
| NII_CG / NII_Clientes total | N/A — CG em Mercado (~0.6%) | **~13%** (real; base R$146B) |
| **NII_Sensíveis** | = NII_Clientes (CG não está aqui) | **R$26,955M/trim** (Release 4T25) |
| **NIM_sensíveis** (divulgado) | **9.0%** (taxa média release = spread líquido) | **8.6%** a.a. (Release 4T25) |
| NIM_CG (taxa capital giro) | N/A (CG vai para Mercado) | **11.2%** a.a. (Release 4T25) |

### Efeito Alavancagem: Por Que o NIM Pode Ser Similar Apesar de Estruturas Diferentes

Os dois bancos têm estruturas de NII distintas — comparar apenas o número agregado é enganoso:

**BBDC4 — taxa_media = 9.0% a.a. (release p.9), NII_CG em Margem Mercado:**
- BBDC4 publica taxa_media e saldo_medio diretamente no release (p.9) — usar como inputs verificáveis
- Capital de Giro Próprio do BBDC4 está classificado em **Margem com Mercado** (~R$126M/trim total de Margem Mercado), NÃO em Margem com Clientes
- Portanto, a taxa_media de 9.0% a.a. representa o spread líquido da carteira de clientes sem componente CG separado
- **Não há NIM_sensíveis separado para BBDC4**: o banco não decompõe sensíveis vs capital de giro na divulgação pública
- NIM_sensíveis implícito estimado previamente (11.8%) era incorreto — baseado em estrutura análoga ao ITUB4 que BBDC4 não adota

**ITUB4 — mais alavancado, spread sensível mais baixo:**
- Com PL/Carteira de ~20%, a contribuição do NII_CG é menor como percentual do total (~13% real vs ~30% estimado anteriormente)
- Crescimento de carteira mais agressivo (grandes empresas, consignado privado, atacado) com spreads CDI+1–3%
- Resultado: NIM_sensíveis **8.6%** a.a. (divulgado 4T25, Fonte: Release 4T25), abaixo do BBDC4 — mas sobre base de carteira muito maior (R$1.28T incl. LatAm)

**Nota sobre NIM ajustado pelo risco**: o maior spread do BBDC4 nos sensíveis é amplamente compensado pelo maior custo de risco histórico (PME inadimplência, ciclo 2022–2024 de compression). Na prática, o NIM ajustado pelo risco dos dois bancos converge, o que explica ROEs similares no pico de ciclo.

### Implicações para Ciclo de Queda de Selic

O NII_CG é diretamente proporcional à Selic. Em um cenário de corte de 100bps na Selic:

```
Impacto NII_CG = Base_capital_giro × (−1%) / 4 por trimestre

BBDC4: NII_CG ≈ R$126M/trim (capital de giro próprio em Margem Mercado) — impacto de 100bps na Selic é mínimo (~R$50M/ano bruto). A linha R$172B (PL controladores) NÃO é a base do NII_CG de clientes; o CG está em Mercado, não em Clientes.
ITUB4: R$146B (base real, Release 4T25) × 1% = ~R$1.46B/ano bruto
       → ajustando pela parcela efetivamente pós-fixada (~50-70%): impacto efetivo ~R$730M–1.0B/ano
       (estimativa anterior de R$550M/ano era baseada em PL total ~R$220B — revisada com dados reais)
```

O Bradesco perde menos em termos absolutos por 100bps de corte de Selic — mas isso reflete a carteira menor, não necessariamente maior imunidade ao ciclo. Em termos relativos ao PL, o impacto percentual é equivalente nos dois bancos (ambos perdem ~1% a.a. do PL por 100bps).

O que diferencia o impacto no ciclo de queda de Selic é a velocidade de repricing da carteira sensível:
- BBDC4: carteira PME reprecia mais rápido (prazos mais curtos) → NIM_sensíveis pode cair em linha com a Selic
- ITUB4: carteira grandes empresas tem mais instrumentos indexados a CDI flat → repricing imediato, mas spread bruto menor, impacto menor em termos absolutos de NIM

### Trajetória Histórica BBDC4: Compression e Recovery

A trajetória do NIM Clientes do Bradesco ilustra o risco de mix e ciclo:

| Período | NII Clientes (R$M/trim) | Taxa Média (Saldo Médio) | Observação |
|---------|------------------------|--------------------------|------------|
| 3T22 | R$17,527M | 10.1% (R$715,965M) | Pico pós-pandemia, carteira PME aquecida |
| 4T23 | R$15,432M | 8.8% (R$718,376M) | Trough nominal (limpeza de carteira PME) |
| 1T24 | R$14,522M | 8.5% (R$710,662M) | Trough de NIM, início do turnaround |
| 4T24 | R$16,153M | 8.4% (R$790,286M) | Recovery gradual |
| 1T25 | R$16,771M | 8.6% (R$812,805M) | |
| 4T25 | R$19,119M | **9.0% (R$873,597M)** | Recovery consolidado. Fonte: Release p.9 (verified) |

*Todos os dados verificados de releases BBDC4 (p.9 tabela "Margem com Clientes"). Taxa Média = compound annualized. Saldo Médio = average portfolio (crédito + similares + passivos sensíveis — base gerencial, maior que carteira_credito_liq do BP).*

A compression 2022–2024 reflete três forças simultâneas: (1) encolhimento deliberado da carteira PME de alto risco, (2) queda do spread de concessão nos novos produtos de menor risco (consignado, imobiliário), e (3) custo de funding ainda alto. A recovery 2024–2025 é mix shift + crescimento de carteira + tail wind de Selic alta via NII_CG.

### Nota sobre Convergência de NIM

Os dois bancos têm NIM de clientes diferentes: BBDC4 taxa_media = **9.0% a.a.** (release p.9, 4T25); ITUB4 ~8.9% MFC total. A comparação direta é enganosa porque o ITUB4 decompõe NII_CG separadamente (em Clientes), enquanto o BBDC4 classifica seu Capital de Giro Próprio em Margem com Mercado (~R$126M/trim total), mas a decomposição por sub-componente é estruturalmente diferente. Isso implica que modelos que projetam NIM como uma única linha são insuficientes para diferenciar o comportamento dos dois bancos em cenários de:
- Queda de Selic (impacto via NII_CG é proporcional ao PL, não à carteira)
- Ciclo de crédito adverso (impacto via spread_sensíveis é maior para quem tem mais PME/PF alto risco)
- Mix shift (migração para consignado/imobiliário reduz NIM_sensíveis mas reduz custo_risco também)

Este é o racional estrutural para o graph patch proposto em `ITUB4_graph_patch_nii_decomposicao.json`, que quando aprovado deve ser replicado para BBDC4.

## Ver Também

- [[nii_sensiveis_spread]] — sub-componente: operações ativas de crédito com spread acima do benchmark
- [[remuneracao_capital_giro]] — sub-componente: equity hedge automático (PL × CDI)
- [[nii_mercado]] — NII de tesouraria (componente mais volátil)
- [[nim]] — NIM total = NII Clientes + NII Mercado / Ativos Remunerados
- [[crescimento_carteira]] — driver de volume do NII Clientes
- [[selic]] — driver de preço (remuneração do capital de giro)
- [[custo_risco]] — risco associado à busca por maior spread
- [[banking]] — contexto setorial
