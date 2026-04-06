---
type: conceito
source_quality: conceptual
aliases: [LL, Lucro Líquido, Resultado Líquido, Bottom Line, Net Income]
sources:
  - sectors/banking/sector_profile.md
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
---

# Lucro Líquido (LL)

O **Lucro Líquido (LL)** é o resultado final da empresa após todas as receitas, custos, despesas, tributos e participações de minoritários. É o "bottom line" — o que sobra para os acionistas controladores. É o numerador do [[roe]] e a base para dividendos, retenção e crescimento do patrimônio líquido.

```
LL = Receita_Líquida
   − Custos
   − Despesas_Operacionais
   ± Resultado_Financeiro
   ± Equivalência_Patrimonial
   − IR_e_CSLL
   − Participação_Minoritários
```

## LL Reportado vs LL Recorrente

Esta distinção é central para análise de equity research:

```
LL_Recorrente = LL_Reportado ± Itens_Não_Recorrentes
```

**Itens que tornam o LL não-recorrente:**

| Item | Efeito | Exemplos |
|------|--------|---------|
| Ganho/perda em venda de ativos | Inflam/deflam LL | Venda de imóveis próprios, participações |
| Provisões extraordinárias | Deflatem LL | Kitchen sink, provisões complementares |
| Reversão de provisões | Inflam LL | Reversão de PCLD em melhora de ciclo |
| Reestruturação / PLR extraordinário | Deflatem LL | Pacotes de demissão voluntária |
| Efeito fiscal não recorrente | Inflam/deflam | Créditos tributários diferidos, reavaliação de JSCP |
| Resultado de operações descontinuadas | Inflam/deflam | Venda de segmento de negócio |

**Regra prática:** Para valuation, sempre usar o LL recorrente como base. O LL reportado pode conter sinais falsos — um banco que libera provisões para melhorar LL artificialmente pode parecer melhor do que é.

## LL no Setor Bancário

Para bancos, o LL recorrente gerencial (publicado no release) é o ponto de partida. Os grandes bancos publicam a reconciliação explícita no release:

```
LL_Recorrente_Gerencial = LL_Contábil_IFRS
                        − Amortização_de_Intangíveis_de_Aquisição (net de impostos)
                        ± Efeitos_Fiscais_não_recorrentes
                        ± Provisões_complementares
                        ± Outras_ajustes
```

**Referência ITUB4 2025:** LL recorrente gerencial ~R$47B (anualizado a partir do 3T25/4T25). Este é o número central do modelo de banking.

### LL Bancário: Drivers Principais

```
LL_Banco = NII
         − PDD (custo de risco)
         + Fees e Tarifas
         + Resultado de Seguros/Previdência
         − Despesas Operacionais (pessoal + admin)
         ± Outras receitas/despesas
         − IR_e_CSLL
         − Participações minoritárias
```

A sensibilidade do LL bancário aos drivers:

| Driver | Impacto em 1% de variação |
|--------|--------------------------|
| NII Clientes | Alta sensibilidade (~30-40% do top-line) |
| Custo de risco | Alta sensibilidade (~20-30% do top-line) |
| Fees | Média sensibilidade (~15-20% do top-line) |
| Despesas operacionais | Média sensibilidade (~35-45% do top-line) |
| Alíquota efetiva | Menor sensibilidade (já após resultado operacional) |

## LL nas Incorporadoras

Para [[incorporadoras]], o LL tem particularidades:

### Minoritários são Relevantes

Incorporadoras frequentemente operam em joint ventures e SPEs onde não têm 100% do capital. O resultado antes dos minoritários (LAIR) pode diferir significativamente do LL controladores:

```
LL_Controladores = LAIR_Consolidado × (1 - Alíquota) − Resultado_Minoritários
```

Para a [[tenda]], por exemplo, a Alea (joint venture) contribui negativamente para o resultado e a participação de minoritários é deduzida. Para a [[cyrela]], as JVs com Lavvi e P&P têm minoritários relevantes.

### LL vs Geração de Caixa

Para incorporadoras, o LL não é equivalente à geração de caixa — o [[poc_revenue]] reconhece receita antes do recebimento, e o [[capital_de_giro]] (terrenos, estoque, recebíveis) absorve caixa independentemente do LL. A análise do LL deve sempre ser acompanhada da análise do FCO (Fluxo de Caixa Operacional).

### Margem Líquida

A margem líquida (LL / Receita Líquida) é uma métrica relevante para comparação entre incorporadoras:

```
Margem_LL = LL_Controladores / Receita_Líquida × 100%
```

**Ranges típicos para incorporadoras brasileiras:**
- [[cury]]: ~15-18% (alta eficiência MCMV puro)
- [[cyrela]]: ~10-15% (EP relevante eleva LL acima da operação pura)
- [[tenda]]: ~6-10% (transitório; Alea comprime; recuperação em andamento)
- [[direcional]]: ~12-16% (Riva parceria; minorities relevantes)

## LL e Dividendos

O LL é a base para a política de dividendos. Em bancos:

```
Dividendos = LL × Payout_ratio
Payout = Dividendos / LL (ou LL_recorrente)
```

**Referência ITUB4 2025:** Payout ~72% (incluindo dividendos extraordinários). Guidance 2026: ~55%.

O JCP (Juros sobre Capital Próprio) é uma forma de distribuição que reduz a base de IR antes do cálculo do LL. Ver [[jcp]] e [[aliquota_efetiva]] para a mecânica completa.

## Variação do PL (Rolê do Patrimônio Líquido)

O LL é o principal motor da variação do PL:

```
PL_fim = PL_início + LL − Dividendos + Outros_abrangentes ± Variação_de_capital
```

Para o modelo de banking, este é o **rollforward do PL** — verificação de integridade do balanço (balance check). Ver [[banking]] para a checagem de BP vs rollforward de PL.

## Ver Também

- [[roe]] — ROE = LL / PL_médio; principal uso do LL para análise de rentabilidade
- [[roe_bancario]] — análise profunda de ROE bancário e drivers do LL bancário
- [[jcp]] — reduz IR e CSLL, aumentando LL; dedutível da base tributável
- [[aliquota_efetiva]] — alíquota efetiva de IR+CSLL aplicada sobre o LAIR para chegar ao LL
- [[banking]] — DRE bancária completa e drivers do LL
- [[incorporadoras]] — LL nas incorporadoras: ciclo, POC, minoritários
- [[equivalencia_patrimonial]] — componente do LL em empresas com investidas
- [[poc_revenue]] — reconhecimento de receita que determina parte do LL das incorporadoras
