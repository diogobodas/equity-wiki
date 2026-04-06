---
type: conceito
source_quality: conceptual
aliases: [Capital de Giro, Working Capital, WC, Giro Operacional]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/DIRR3/outputs/decomposition/DIRR3_dependency_graph_v3.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
updated: 2026-04-05
---

# Capital de Giro

O **capital de giro** (WC — Working Capital) é o capital imobilizado no ciclo operacional da empresa: o que está "parado" entre o desembolso de caixa e o recebimento efetivo das vendas. Para [[incorporadoras]], é a principal diferença entre EBIT e geração de caixa livre.

## No Contexto das Incorporadoras

```
Capital de Giro = Recebíveis + Estoques + Terrenos + Adiantamentos a fornecedores
               - Adiantamentos de clientes - Fornecedores a pagar
```

No modelo, cada linha é projetada como **dias de giro** sobre a receita (ou custo), seguindo o Princípio da Continuidade:

| Componente | Driver | Dias Típicos (BR) |
|------------|--------|--------------------|
| Recebíveis | Receita | 120-180 dias |
| Estoques (obras em andamento) | Custo | 180-300 dias |
| Terrenos | Custo | 200-400 dias (ciclo longo) |
| Adiantamentos a fornecedores | Custo | 30-60 dias |
| Adiantamentos de clientes | Receita | (60-120 dias) negativo |

**Var. Capital de Giro = WC(t) − WC(t-1)** aparece na demonstração de fluxo de caixa como uso ou liberação de caixa.

## Por Que o WC é Grande nas Incorporadoras

Incorporadoras constroem o imóvel antes de entregar — o ciclo de conversão de caixa é de **18-36 meses**. Isso significa que:

- Terreno comprado → 12-18 meses de construção → venda e recebimento gradual via [[poc_revenue]] → habite-se → transferência SFH

O ciclo longo é a razão pela qual [[cyrela]], [[direcional]] e [[tenda]] têm WC/receita muito maior que empresas industriais.

## Diferença MCMV vs Alto Padrão

| Segmento | WC Relativo | Por Quê |
|----------|-------------|---------|
| [[mcmv]] (Tenda, Cury, Direcional) | Menor | CEF libera recursos por medição de obra; pré-venda >90% antes do início |
| Médio/Alto Padrão ([[cyrela]]) | Maior | Recebimentos concentrados no habite-se; ciclo mais longo; VGV maior por unidade |

## No Modelo de Banking

Em [[banking]], "capital de giro" tem sentido diferente: é o produto de crédito às empresas para financiar **seus** ciclos operacionais. É uma linha da carteira de crédito, não uma métrica do balanço do banco.

No caso do [[itau]], a decomposição do [[nii_clientes]] inclui:
- Saldo de operações sensíveis a spread (inclui capital de giro PJ) × spread dessa linha
- Saldo de capital próprio × remuneração implícita

Isso ilustra que o mesmo conceito "capital de giro" aparece como **métrica de gestão** nas incorporadoras e como **produto de crédito** nos bancos.

## Modelagem de Capital de Giro: Dias de Giro

No modelo financeiro, cada componente do WC é projetado como número de dias sobre a base relevante (receita ou custo):

```
Recebíveis = (Receita_LTM / 365) × Dias_Recebíveis
Estoques   = (Custo_LTM / 365) × Dias_Estoques
Terrenos   = (Custo_LTM / 365) × Dias_Terrenos
Adiant_for = (Custo_LTM / 365) × Dias_Adiant_Fornecedores
Adiant_cli = (Receita_LTM / 365) × Dias_Adiant_Clientes    [negativo — passivo]
```

Os dias são **calibrados por backtest** usando os dias históricos implícitos:

```
Dias_Recebíveis_histórico(t) = Recebíveis(t) / (Receita_LTM(t) / 365)
```

A média dos últimos 4-8 trimestres é usada como premissa base, ajustada por mudanças estruturais no mix de produto.

### Benchmarks de Dias de Giro

| Empresa | Dias Recebíveis | Dias Estoques | Dias Terrenos | Dias Adiant_CLI |
|---------|----------------|---------------|---------------|----------------|
| [[cury]] | ~100-120 | ~150-200 | ~200-280 | ~(50-70) |
| [[cyrela]] | ~160-200 | ~250-320 | ~350-450 | ~(80-120) |
| [[direcional]] | ~120-150 | ~180-250 | ~250-350 | ~(60-90) |
| [[tenda]] | ~130-150 | ~200-250 | ~280-350 | ~(70-100) |

**Nota:** Cyrela tem dias de WC muito maiores porque opera com alto padrão (ciclos mais longos) e maior ticket médio (menos unidades, maior saldo por contrato).

## Variação de WC no Fluxo de Caixa

A variação do capital de giro (**ΔWC**) aparece na demonstração de fluxo de caixa operacional:

```
FCO = EBITDA − ΔWCL − Impostos pagos ± Outros
```

onde:

```
ΔWCL = WC_fim − WC_início
      = (Recebíveis + Estoques + Terrenos + Adiant_for) − (Adiant_cli + Fornecedores)
```

**Sinal:** ΔWCL positivo = capital imobilizado aumentou = **uso de caixa** (negativo no FCO).

### Fase de Crescimento vs Fase de Maturidade

| Fase | Comportamento do WC | FCO |
|------|--------------------|----|
| Crescimento (lançamentos acelerando) | WC cresce (mais terrenos + recebíveis) | FCO negativo mesmo com LL positivo |
| Estável | WC aproximadamente estável | FCO ≈ EBIT |
| Desaceleração (entregando portfólio antigo) | WC libera caixa (recebíveis cobram, terrenos não repõem) | FCO > EBIT |

Isso explica por que [[cury]], [[cyrela]] e [[direcional]] às vezes geram caixa negativo mesmo com lucro positivo — estão investindo em crescimento via acumulação de WC.

## Capital de Giro e Endividamento

Para as incorporadoras, o endividamento líquido é fortemente correlacionado com o WC:

```
Dívida_líquida = −Caixa_livre
               = −(EBIT − Impostos − ΔWC − Capex − Amortização)
```

Empresas com crescimento acelerado de VGV acumulam WC e precisam financiar esse gap com dívida. O [[cury]] e o [[direcional]] geralmente têm caixa líquido (WC financiado pelo próprio resultado + adiantamentos de clientes). A [[cyrela]] opera com dívida positiva por causa dos ciclos mais longos e produtos mais caros.

### Métricas de Endividamento Específicas para Incorporadoras

Para incorporadoras, as métricas convencionais de alavancagem (Dívida/EBITDA) não são apropriadas porque:
- EBITDA não é o fluxo de caixa relevante (WC é enorme)
- Dívida inclui SFH (financiamento para clientes, não dívida corporativa)

As métricas relevantes são:

```
Dívida_Corporativa_Líquida = Dívida_total − SFH − Caixa
Dívida_Corp/PL = Dívida_Corporativa_Líquida / Patrimônio_Líquido
```

Onde o SFH é a dívida "boa" — está financiando os próprios clientes e é paga quando o habite-se é emitido e o cliente transfere o financiamento para o banco.

## Adiantamentos de Clientes: WC Negativo Favorável

O **adiantamento de clientes** (quando o comprador paga antes da obra avançar o suficiente para reconhecer a receita) é um passivo no balanço mas um **ativo para o caixa**:

```
Adiantamento_Clientes = Caixa_recebido − Receita_POC_reconhecida > 0
```

Para empresas MCMV onde os clientes pagam adiantamentos durante a obra (e a CEF repassa recursos), esse passivo pode ser relevante e reduz o WC líquido. É por isso que o capital de giro das empresas MCMV é sistematicamente menor que o das empresas de alto padrão.

## Ver Também

- [[poc_revenue]] — reconhecimento de receita que gera recebíveis; base do cálculo de WC
- [[incorporadoras]] — setor onde WC é o maior componente de diferença EBIT→FCO
- [[tenda]] — MCMV: WC menor por estrutura CEF + adiantamentos
- [[cyrela]] — multi-segmento: WC maior por ciclos mais longos e tickets altos
- [[cury]] — referência de eficiência de WC no MCMV; ciclo curto de 18m
- [[direcional]] — mix MCMV + Riva; WC intermediário
- [[incc]] — inflação que aumenta o saldo de estoques em andamento
- [[nii_clientes]] — para bancos: capital de giro PJ é produto de crédito, não métrica operacional
- [[vgv_lancamentos]] — VGV crescente implica mais terrenos → mais WC
