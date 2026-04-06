---
type: conceito
source_quality: conceptual
aliases: [Duration, Prazo Médio Ponderado, Duration Modificada, Macaulay Duration]
sources:
  - sectors/banking/sector_profile.md
  - wiki/nii_mercado.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - wiki/risco_mercado.md
updated: 2026-04-05
---

# Duration

A **duration** é o prazo médio ponderado dos fluxos de caixa de um instrumento financeiro, onde os pesos são os valores presentes de cada fluxo. É a principal medida de sensibilidade de preço de um ativo ou passivo a variações na taxa de juros. Quanto maior a duration, maior o risco de mercado associado a variações de taxa.

## Como Funciona

### Macaulay Duration (Duração)

```
D_Macaulay = Σ [t × PV(CF_t)] / Σ [PV(CF_t)]

onde:
  t       = período do fluxo
  CF_t    = fluxo de caixa no período t
  PV(CF_t) = valor presente do fluxo t
```

**Interpretação:** Para um título com Macaulay Duration de 3 anos, o investidor recupera seu capital investido (em termos de valor presente) em média em 3 anos — ponderando todos os cupons e o principal.

### Duration Modificada (Sensibilidade de Preço)

A duration modificada converte a Macaulay Duration em uma elasticidade de preço:

```
D_modificada = D_Macaulay / (1 + y/m)

onde:
  y = yield to maturity (taxa ao período)
  m = frequência de pagamentos por ano
```

**Impacto no preço:**

```
ΔP/P ≈ −D_modificada × Δy

Exemplo: D_mod = 5 anos; Δy = +100bps (1%)
  ΔP/P ≈ −5 × 0,01 = −5%
```

Para um banco com carteira de TVM de R$200B e duration de 5 anos: um choque de +100bps nas taxas de juros implica perda de ~R$10B no valor a mercado dessa carteira.

## No Contexto Bancário: ALM (Asset-Liability Management)

Para bancos, a duration é central na gestão de **ALM (Gestão de Ativos e Passivos)**. O objetivo é administrar o descasamento (gap) entre a duration dos ativos e dos passivos:

```
Duration_Gap = D_Ativo − (Passivo/Ativo) × D_Passivo
```

| Situação | Duration Gap | Efeito em Alta de Juros |
|----------|-------------|------------------------|
| Ativo com duration > Passivo | Positivo | PL do banco cai (ativo perde mais valor que o passivo) |
| Ativo com duration < Passivo | Negativo | PL do banco sobe (passivo perde mais valor) |
| Duration Gap ≈ 0 | Neutro | PL do banco protegido de variações de taxa |

**Maioria dos bancos BR:** Têm ativos de crédito com prazo mais longo que os passivos (depósitos à vista e a prazo curtos). Isso cria duration gap positivo — exposição a alta de juros de longo prazo. Bancos usam derivativos (swaps, futuros de DI) para hedgear essa exposição.

## Duration e NII Mercado

O [[nii_mercado]] dos bancos é sensível à duration da carteira de TVM:

- **Carteira pós-fixada (CDI/Selic):** Duration muito curta (~0,25 anos para título 1 dia). Não tem risco de mercado de taxa mas o NII varia com a Selic.
- **Carteira prefixada:** Duration igual ao prazo; risco de mercado alto mas NII fixo.
- **Carteira IPCA+:** Duration longa (3-10 anos típicos para NTN-Bs); risco de mercado de taxa real.

Para modelagem, a sensibilidade do NII Mercado a variações de Selic depende da composição da carteira por modalidade (pós vs pré vs IPCA):

```
ΔNII_Mercado ≈ Carteira_Pós × ΔSelic × Duração_contratual
             + Carteira_Pré × 0  (NII fixo, mas MTM varia)
             + Carteira_IPCA × Δ(IPCA_realizado)
```

## Duration na Prática Brasileira

### Curva de Juros Doméstica

O Brasil tem uma estrutura de prazo peculiar:
- **Pré-fixado**: Mercado líquido até 3-5 anos; ilíquido além disso
- **IPCA+**: Mercado de NTN-Bs com vencimentos até 2060 — o mais longo da curva brasileira
- **Pós-fixado (Selic/CDI)**: Dominante no curto prazo; duration próxima de zero

**Implicação:** Bancos brasileiros com carteiras de crédito de prazo médio de 2-4 anos têm duration relativamente curta. Portanto, a sensibilidade de preço de portfólio a choque de taxa é menor do que em sistemas bancários de mercados desenvolvidos (onde hipotecas de 30 anos criam duration de 10+ anos).

### Impacto do Ciclo de Juros no Brasil

Em ambientes de alta de Selic (como 2022-2025):
1. **NII pós-fixado sobe mecanicamente** — carteiras CDI/Selic rendem mais
2. **MTM de carteiras prefixadas sofre** — perda de valor a mercado (mas não no resultado se mantidas até o vencimento)
3. **Duration gap management** se torna crítico — bancos que travaram ativos longos a taxas baixas em 2020-21 sofreram em 2022-23

## Por Empresa

| Empresa | Característica de Duration |
|---------|--------------------------|
| [[itau]] | Carteira de TVM diversificada; gestão ativa de ALM com hedges de duration via derivativos de DI. NII Mercado relativamente estável apesar da volatilidade da Selic. |
| [[bradesco]] | Seguradoras do grupo têm carteiras de longa duration (IPCA+, obrigações de seguros de vida). A [[resultado_seguros]] Bradesco Seguros é especialmente sensível ao IPCA e duration da curva longa. |

## Risco de Convexidade

Para duration alta, a aproximação linear subestima o ganho (e superestima a perda) em movimentos grandes de taxa. A **convexidade** é a correção de segunda ordem:

```
ΔP/P ≈ −D_mod × Δy + (1/2) × Convexidade × (Δy)²
```

Para análise prática de bancos brasileiros com carteiras relativamente curtas, a convexidade é secundária. Mas para carteiras de NTN-Bs longas (duration >7 anos), a convexidade positiva protege o investidor em movimentos grandes de taxa (ganha mais em queda de taxa do que perde em alta equivalente).

## Duration no Modelo de Banking: O Que É Modelado

Na prática de modelagem de equity bancário, a **duration raramente é modelada explicitamente**. O que se modela é:

1. **NII Mercado como % do patrimônio** ou como item semi-fixo (ex: R$3-4B/tri para o Itaú)
2. **Sensibilidade a Selic**: NII pós-fixado sobe/cai com Selic via carteira de compulsórios e TVM curto
3. **Mark-to-Market implícito**: Uma alta de Selic comprime o NII Mercado se o banco tem posição pré-fixada travada

A duration é um **input implícito** para entender a magnitude dessas sensibilidades, mas não aparece diretamente no grafo de dependências.

### Por que NII Mercado é Difícil de Modelar

O NII Mercado inclui resultado de:
- Carteira pós-fixada (CDI/Selic): mecanicamente ligado à Selic
- Carteira prefixada: resultado fixo, mas MTM sensível à curva de juros
- Carteira IPCA+: resultado ligado à inflação realizada
- Derivativos de hedge: swaps que compensam exposições
- Compulsórios remunerados pelo Banco Central

A duration **ponderada** dessa carteira determina a sensibilidade total. Como os bancos raramente divulgam a breakdown completa, o analista modela o NII Mercado como item semi-autônomo, calibrado histórico.

### Itaú: NII Mercado Estável

O Itaú gerencia ativamente a duration via hedges, mantendo o NII Mercado relativamente estável (~R$3-4B/tri). O gráfico de sensibilidade divulgado mostra:

```
Choque de Selic +100bps: NII Mercado +R$800M-1.2B (12 meses) — posição líquida pós-fixada
Choque de Selic -100bps: NII Mercado -R$800M-1.2B (12 meses)
```

Esta sensibilidade positiva a alta de Selic indica duration de passivos > duration de ativos na margem — o Itaú beneficia de Selic alta (até certo ponto).

## Duration e Seguros (BBDC4)

Para o [[bradesco]], a [[resultado_seguros]] é especialmente sensível à duration porque:

1. **Seguros de Vida (VGBL/PGBL):** Obrigações de longa duration (10-20 anos). A seguradora investe em NTN-Bs para casar o prazo (Asset-Liability Matching)
2. **Risco de descasamento:** Se a curva longa sobe, o passivo de seguros cai de valor mas o ativo (NTN-B) também cai — se o casamento for bom, o efeito é neutro no PL
3. **Resultado financeiro de seguros:** O resultado de juros da carteira de seguros é positivo em ambiente de juro alto (NTN-Bs rendem mais)

**Benchmark 2025:** Com Selic a 13,25% e IPCA ~5%, as NTN-Bs de longa duration (ex: vencimento 2035) rendem ~6,5% reais — gerando resultado financeiro expressivo para a seguradora.

## Ver Também

- [[nii_mercado]] — NII de tesouraria, diretamente afetado pela duration da carteira de TVM
- [[selic]] — taxa de curto prazo que afeta o NII pós-fixado e a curva de juros
- [[cet1]] — capital adequacy; exigências de capital de mercado (Rban) relacionadas ao risco de taxa
- [[risco_mercado]] — framework mais amplo de riscos de mercado (câmbio, ações, juros)
- [[banking]] — estrutura da DRE e balanço bancário
- [[resultado_seguros]] — para o Bradesco, a seguradora tem carteira longa sensível à duration
- [[itau]] — NII Mercado gerenciado via hedges; sensibilidade +Selic positiva
- [[bradesco]] — seguros com ALM de longa duration em NTN-Bs
