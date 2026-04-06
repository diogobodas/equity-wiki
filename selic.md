---
type: conceito
source_quality: conceptual
aliases: [Taxa Selic, Selic, Taxa Básica de Juros, CDI]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/SANB11/outputs/model/SANB11_model.json
  - sectors/real_estate/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
updated: 2026-04-05
---

# Taxa Selic

A **Taxa Selic** é a taxa básica de juros da economia brasileira, definida pelo Comitê de Política Monetária (COPOM) do Banco Central do Brasil (BCB). É o principal driver macro para o setor bancário — influencia diretamente o [[nim]], o [[crescimento_carteira]] e, indiretamente, o [[custo_risco]].

O CDI (Certificado de Depósito Interbancário) é a taxa do mercado interbancário — na prática, anda a ~0,10pp abaixo da Selic e é usado como referência de remuneração de passivos bancários.

## Como Funciona

O COPOM se reúne a cada ~45 dias para decidir a meta da Selic. A decisão é baseada na inflação corrente vs meta (IPCA), nas expectativas de inflação (Focus/BCB) e no nível de atividade econômica.

```
Transmissão Selic → Bancos:
  Selic ↑ → Taxa de concessão de crédito ↑ → NII bruto ↑ (se ativo reprecia antes do passivo)
  Selic ↑ → Custo de captação ↑ → comprime spread (se passivo reprecia antes)
  Selic ↑ → Custo do crédito ao tomador ↑ → demanda de crédito ↓ → [[crescimento_carteira]] ↓
  Selic ↑ → (médio prazo) inadimplência ↑ → [[custo_risco]] ↑
```

A relação não é linear — o impacto depende do **repricing gap** do banco (prazo médio de ativo vs prazo médio de passivo) e do mix da carteira (pré vs pós-fixado).

### Selic × NIM

- **Bancos com carteira predominantemente pós-fixada (CDI+spread)**: Selic alta → NIM se mantém ou sobe porque o ativo reprecia junto com o passivo, mas com spread fixo.
- **Bancos com carteira pré-fixada longa**: Selic alta → NIM comprime porque o passivo reprecia rapidamente (CDI sobe) mas o ativo está travado a taxa pré.
- **Carteira de consignado**: Taxa pré-fixada no longo prazo — Selic alta é desfavorável para novas concessões (rentabilidade marginal cai).

## Repricing Gap — Por Que o Impacto É Assimétrico

O **repricing gap** mede a diferença entre a duration (prazo médio de repricing) do ativo e do passivo do banco:

```
Repricing Gap = Duration do Ativo − Duration do Passivo
```

O sinal e a magnitude desse gap determinam se uma mudança de Selic beneficia ou prejudica o [[nim]]:

- **Gap negativo (ativo longo pré-fixado + passivo curto pós-fixado)**: quando a Selic sobe, o passivo reprecia rápido (CDI sobe junto), mas o ativo não — o banco está travado na taxa pré. Resultado: **NIM comprime** no curto prazo. Essa é a situação clássica de bancos com grande carteira de consignado INSS de longo prazo.

- **Gap próximo a zero ou positivo (ativo pós-fixado + passivo pós-fixado)**: ambos sobem juntos com a Selic. O **spread permanece estável**, mas o volume absoluto de [[nii_clientes]] sobe mecanicamente porque a taxa base é maior.

### Posicionamento do Itaú

- ~60-70% do portfólio de crédito do [[itau]] é CDI-linked ou de prazo curto → **repricing favorável** em ambiente de Selic alta.
- **Consignado privado é PRÉ-FIXADO**: quando a Selic sobe, a nova produção precifica melhor (spreads mais atrativos na concessão), mas o estoque antigo já está travado a taxas pré mais baixas → comprime a margem do estoque existente.
- Por isso: no **curto prazo**, Selic alta beneficia o NIM de Itaú; no **médio prazo**, o efeito é misto para a carteira de consignado — há drag do estoque antigo até ele vencer e ser renovado a taxas novas.

## Dois Canais de Transmissão Selic → NII

A Selic impacta o [[nii_clientes]] e o [[nii_mercado]] por dois canais distintos, com dinâmicas diferentes:

### Canal 1 — Spread da Carteira (Sensíveis a Spread)

A taxa de concessão de novos créditos sobe com a Selic. Para carteiras pós-fixadas (CDI + spread), o repricing é automático conforme os contratos vencem e são renovados — não é imediato, existe um lag.

- Para [[itau]]: sensibilidade estimada **~+R$1.5-2.0B de NII por +100bps de Selic** via repricing da carteira de crédito (estimado a partir da sensibilidade declarada total).
- O lag de repricing depende do prazo médio da carteira — carteiras com giro rápido (capital de giro, CDC) reprecia em semanas; carteiras longas (imobiliário, consignado) reprecia em meses/anos.

### Canal 2 — Remuneração do Capital de Giro ([[remuneracao_capital_giro]])

Os bancos têm um patrimônio líquido (PL) que precisa ser "investido" em algo. Convencionalmente, o PL é alocado em títulos pós-fixados (LFT, NTN-B) que rendem ~CDI. Quando a Selic sobe, esse PL rende mais — sem risco de crédito adicional.

- [[itau]] PL ~R$220B × CDI
- Cada **+100bps de Selic → ~+R$550M de NII** (mecânico, automático, sem risco de crédito adicional)
- Canal 2 é **instantâneo** — não há lag de repricing, a remuneração sobe na reunião seguinte do COPOM

### Soma dos Canais

```
+100bps Selic →
  Canal 1 (spread carteira):     ~+R$1.5-2.0B NII  (com lag)
  Canal 2 (capital de giro):     ~+R$0.55B NII     (imediato)
  Total estimado NII:            ~+R$2.0-2.5B NII

  Após IR ~30%:                  ~+R$1.4-1.75B LL
  Escalonado para +50bps:        ~+R$0.7-0.9B LL
```

Consistente com a sensibilidade declarada pelo [[itau]]: **+/-50bps NIM → +/-R$2.7B LL** (que implica ~+/-R$3.9B NII pré-tax). A diferença para a estimativa acima reflete que Itaú inclui efeitos de segundo grau (mix de funding, hedge de derivativos) além dos dois canais principais.

> Os dois canais se comportam de forma diferente: Canal 1 tem lag (crédito reprecia conforme vence), Canal 2 é instantâneo. Isso explica por que o NII de Itaú responde gradualmente a mudanças de Selic, não de golpe.

## Ciclo 2026: Onde Estamos

### Histórico Recente do Ciclo

| Período | Selic | Movimento |
|---------|-------|-----------|
| 2020-2021 | 2,0% → 4,5% | Mínimas históricas pós-COVID; início da normalização |
| 2021-2022 | Alta agressiva até 13,75% | Combate à inflação pós-COVID |
| 2023 | 13,75% → 11,75% | Ciclo de cortes |
| 2024 | 10,5% → 12,25% | Novo ciclo de alta por inflação resiliente |
| 2025 | ~13,25% (pico provisório) | Ciclo de aperto continuado |
| 2026E | Pico ~14,75% → cortes 2S26 | Expectativa Focus/BCB |

### Cenário Base para Modelos 2026

- Selic média 2026: **~14,5%** (pico no 1S26, início de cortes graduais no 2S26)
- Guidance [[itau]] para NII Clientes 2026: **+5-9% a/a** (implicitamente baseado em Selic permanecendo elevada em 2026)
- [[nim]] 4T25 = 12,05% (realizado) → deve se manter estável no 1S26 com Selic em patamar alto
- Tailwind de NIM ainda presente no 1S26 via Canal 2; Canal 1 ainda reprecia estoque antigo

### Riscos

- **Risco upside (Selic >15%)**: NIM sobe além do guidance, mas [[custo_risco]] piora — efeito líquido ambíguo. Crescimento de carteira desacelera mais.
- **Risco downside (Selic <12% em 2027)**: NIM comprime estruturalmente, especialmente via Canal 2 (~-R$550M por -100bps no PL remunerado). Para bancos, um ciclo de cortes agressivo pode reduzir NII em R$1.5-2.5B vs pico.
- **Risco de composição**: Selic alta por longo prazo → inadimplência acumulada → [[custo_risco]] sobe com lag de ~6-9 meses → pode mais do que compensar o ganho de NIM.

## No Contexto Brasileiro (2025-2026)

| Período | Nível Selic | Contexto |
|---------|------------|---------|
| 2020-2021 | 2-4,5% (mínimas históricas) | Política monetária expansionista COVID |
| 2021-2022 | Alta agressiva até 13,75% | Combate à inflação pós-COVID |
| 2023 | 13,75% → 11,75% | Início do ciclo de cortes |
| 2024 | 10,5% → 12,25% | Novo ciclo de alta por inflação resiliente |
| 2025-2026 | ~13-14% | Patamar elevado; ciclo de alta ainda em curso |

**Implicação para modelos 2026:** Selic elevada (~13-14%) cria tailwind de NIM no curto prazo para bancos com carteiras de crédito pós-fixadas. Porém, comprime demanda de crédito às PMEs e pessoas físicas de menor renda. [[crescimento_carteira]] deve desacelerar vs 2024-25.

### Sensibilidade NIM a 100bps de Selic

Os releases de [[itau]] e [[bradesco]] publicam sensibilidade NIM/NII a variações de 100bps na Selic. Esse dado é essencial para montar cenários:

```
ΔNII = Sensibilidade_100bps × (ΔSelic / 100)
```

Exemplo: se o banco declara sensibilidade de +R$1,5B por 100bps de alta, uma alta de 200bps → +R$3,0B de NII adicional no ano.

## Por Empresa

| Empresa | Sensibilidade Selic |
|---------|-------------------|
| [[itau]] | Sensibilidade declarada: **±50bps NIM → ±R$2.7B LL** (implica ~±R$3.9B NII pré-tax). Dois canais: (1) repricing da carteira de crédito ~R$1.5-2.0B por 100bps; (2) remuneração do PL ~R$220B × CDI → ~R$550M por 100bps. ~60-70% da carteira é CDI-linked → posição favorável em Selic alta. |
| [[bradesco]] | Estrutura similar; em turnaround, sensibilidade a Selic é um dos pilares da recuperação de NIM. |
| [[sanb11]] | NIM implícito calibrado a 11,5% (modelo). Selic alta mantém NII Clientes elevado; NII Mercado modelado com +250M/tri (posicionamento de tesouraria favorecido por Selic >13%). Um ciclo de cortes para <10% reduziria o NII Mercado do Santander e pressionaria o NIM. |

## Selic × Setor Imobiliário

A Selic impacta o setor de [[incorporadoras]] por canais distintos do banking:

### Canal Crédito Imobiliário

O crédito imobiliário no Brasil usa principalmente o SBPE (Sistema Brasileiro de Poupança e Empréstimo), com taxas de ~8-10% a.a. (mais baixas que a Selic por conta do funding em poupança). Quando a Selic sobe:

1. **SBPE encarece relativamente**: O spread sobre a Selic comprime — a poupança capta mais caro, taxas do SBPE sobem
2. **Demanda de crédito cai**: Compradores de médio padrão ficam fora do alcance financeiro
3. **MCMV isolado**: Crédito habitacional popular (FGTS) não segue a Selic — tem taxa regulada (~7,66% a.a.). Por isso, [[cury]] e [[direcional]] são **defensivas** em cenário de Selic alta

### Impacto por Segmento

| Segmento | Sensibilidade à Selic | Motivo |
|----------|----------------------|--------|
| MCMV (Faixas 1-3) | Baixa | FGTS tem taxa regulada |
| Médio padrão (SBPE) | Alta | Taxa de mercado correlacionada com Selic |
| [[alto_padrao]] | Moderada | Parte compra à vista; mas crédito imobiliário premium usa SBPE |

### Efeito nos Modelos RE

Para [[cyrela]] (CYRE3), a Selic alta em 2025-2026 tem efeito misto:
- Segmento Cyrela (alto padrão): moderado impacto — base de clientes com maior equity próprio
- Segmento Vivaz (MCMV): protegido — crédito FGTS
- Resultado financeiro (despesas financeiras): Selic alta eleva custo da dívida de obra e terrenos

## Ver Também

- [[nii_clientes]] — impacto direto via spread de crédito
- [[nii_mercado]] — impacto via portfólio de TVM e derivativos
- [[nim]] — a Selic é o driver macro mais importante do NIM
- [[crescimento_carteira]] — Selic alta comprime crescimento
- [[custo_risco]] — Selic alta por muito tempo aumenta inadimplência
- [[remuneracao_capital_giro]] — Canal 2 de transmissão Selic → NII (PL × CDI)
- [[banking]] — contexto setorial banking
- [[incorporadoras]] — impacto da Selic no setor de real estate
- [[alto_padrao]] — segmento mais sensível a Selic dentro das incorporadoras
- [[mcmv]] — segmento isolado da Selic (funding FGTS)
- [[sanb11]] — NII Mercado +250M/tri dependente de Selic >13%
