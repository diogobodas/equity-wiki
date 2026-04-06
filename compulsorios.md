---
type: conceito
source_quality: conceptual
aliases: [Compulsórios, Reservas Compulsórias, Recolhimento Compulsório, Depósitos Compulsórios]
sources:
  - sectors/banking/sector_profile.md
  - wiki/banking.md
  - sectors/banking/companies/SANB11/outputs/model/SANB11_model.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
---

# Compulsórios

Os **compulsórios** (recolhimento compulsório) são reservas obrigatórias que os bancos devem depositar no Banco Central do Brasil (BCB) como percentual de suas captações. São um dos principais instrumentos de política monetária do BCB — ao alterar as alíquotas, o regulador contrai ou expande a liquidez do sistema financeiro.

## Como Funciona

```
Compulsório_a_recolher = Base_de_Cálculo × Alíquota
```

Onde a base de cálculo varia por modalidade de depósito. O banco deve manter esse saldo bloqueado no BCB — não pode usá-lo para empréstimos ou investimentos livremente.

### Alíquotas por Modalidade (Referência 2025)

| Modalidade | Alíquota | Remuneração |
|------------|----------|-------------|
| Depósitos à vista | ~21% | Não remunerado |
| Depósitos a prazo (CDB, etc.) | ~20% | Taxa Selic |
| Depósitos de poupança | ~20% (incl. habitacional) | Taxa Referencial (TR) + 6,17% |
| LCI/LCA | Isento | — |

**Nota:** As alíquotas mudam por decisão do CMN/BCB. Verificar sempre a circular mais recente do BCB para valores exatos.

## Efeito no Multiplicador de Crédito

O compulsório reduz o multiplicador monetário — a capacidade de cada real de base monetária se transformar em crédito via processo de multiplicação bancária.

**Fórmula simplificada do multiplicador:**

```
Multiplicador = 1 / (Reservas_Voluntárias + Alíquota_Compulsório)
```

Com compulsório de 21% e reservas voluntárias mínimas (~5%):

```
Multiplicador ≈ 1 / (0,05 + 0,21) = 1 / 0,26 ≈ 3,8×
```

Ou seja: cada R$1 de depósito à vista gera ~R$3,80 de crédito no sistema. Sem o compulsório (e sem reservas voluntárias), o multiplicador seria teoricamente infinito.

## Impacto na DRE dos Bancos

### Custo de Oportunidade

Para depósitos à vista com compulsório não remunerado (~21%), o banco abre mão de investir esses recursos ao CDI. Com CDI ~13% a.a.:

```
Custo_oportunidade = Depósitos_à_vista × 21% × CDI
```

Para um banco com R$100B em depósitos à vista:

```
Custo_oportunidade ≈ R$100B × 21% × 13% ≈ R$2,7B/ano
```

Este custo não aparece como despesa explícita mas comprime implicitamente o NIM — os depósitos à vista são uma fonte de funding "gratuita" mas obrigam a alocar parte do capital de forma não rentável.

### Compulsório Remunerado

Os compulsórios sobre depósitos a prazo são remunerados à Selic. Esses recursos entram na linha de **NII Mercado** do banco como receita de tesouraria, parcialmente compensando o custo de manutenção do compulsório.

```
NII_compulsório = Compulsório_remunerado × Taxa_Selic
```

## Uso como Instrumento de Política Monetária

O BCB usa os compulsórios como complemento à política de taxa Selic:

| Objetivo do BCB | Ação | Efeito |
|-----------------|------|--------|
| Contrair crédito (combater inflação) | Eleva alíquota | Menos recursos disponíveis para empréstimos → crédito encarece |
| Expandir crédito (estimular economia) | Reduz alíquota | Mais liquidez no sistema → crédito mais barato e acessível |
| Apoiar liquidez em crise | Liberação emergencial | Injeção imediata de liquidez sem mexer na Selic |

**Episódios relevantes:**
- **2020 (COVID):** BCB liberou ~R$1,2T em liquidez potencial via redução de compulsórios + outras medidas. Foi uma das políticas anticrise mais rápidas do ciclo.
- **2010-2013:** Alíquotas elevadas para conter o crescimento acelerado de crédito.
- **2016-2019:** Alíquotas reduziram para estimular economia em recessão.

## No Contexto do Modelo

Os compulsórios aparecem no balanço dos bancos como **"Depósitos no Banco Central"** no ativo. Para o modelo de banking, são relevantes em dois pontos:

1. **Balanço (BP):** Figuram como ativos não crédito; o modelo de banking precisa reconciliar o ativo total incluindo compulsórios.
2. **NII Mercado:** Compulsórios remunerados contribuem para o NII de Tesouraria — são um dos componentes do [[nii_mercado]].

Para o [[itau]] (ITUB4), o volume de compulsórios no BCB é substancial dado o tamanho do balanço (~R$2T em ativos). A remuneração dos compulsórios à Selic contribui positivamente para o NII Mercado em ambiente de Selic elevada.

## Compulsórios vs Requerimentos de Capital

Compulsórios e [[cet1]] são frequentemente confundidos mas são conceitos distintos:

| Conceito | O que é | Para quem | Quem regula |
|----------|---------|-----------|-------------|
| **Compulsório** | Reserva obrigatória sobre captações | Todo banco com depósitos | BCB (política monetária) |
| **CET1 / Capital Mínimo** | Capital próprio mínimo sobre ativos ponderados pelo risco | Todos os bancos | BCB (regulação prudencial, Basileia III) |

O compulsório é uma obrigação de liquidez; o CET1 é uma exigência de solvência. São regulações complementares e independentes.

## Por Banco Coberto

### [[itau]] (ITUB4)
O Itaú é o maior captador de depósitos do Brasil (~R$500B+ em depósitos à vista e a prazo), portanto o volume de compulsórios é material. O NII Mercado do Itaú inclui a remuneração de compulsórios à Selic — em ambiente de Selic elevada (14,25%), esse componente é relevante. O ITUB4 é o banco que mais se beneficia de Selic alta via compulsórios remunerados, dado o tamanho do balanço.

### [[bradesco]] (BBDC4)
O Bradesco também tem base de captação relevante. Com a reestruturação em curso, o management monitorou os compulsórios como fonte de liquidez — liberações emergenciais de compulsórios pelo BCB (como em 2020) foram relevantes para bancos em stress de liquidez.

### [[sanb11]] (SANB11)
O Santander Brasil tem menor base de captação de varejo vs Itaú/Bradesco, com mais dependência de funding via mercado (CDBs institucionais, LCAs, captações externas via controladora espanhola). Isso implica menor volume de compulsórios não remunerados (depósitos à vista), reduzindo o custo de oportunidade do compulsório — mas também menor benefício dos compulsórios remunerados no [[nii_mercado]].

No modelo SANB11, o [[nii_mercado]] foi calibrado em +250M/tri, refletindo o posicionamento de tesouraria favorecido pela [[selic]] elevada (~13-14% em 2026). Os compulsórios remunerados contribuem para esse número: com carteira de crédito de ~R$566B e estrutura de funding menos varejista, o mix do SANB11 tem proporcionalmente menos compulsório não-remunerado que o ITUB4 — o que é um diferencial positivo na margem de tesouraria.

## Compulsórios e Crédito Imobiliário

Um canal menos óbvio dos compulsórios é o impacto no **crédito imobiliário**. O BCB direciona parte dos compulsórios de poupança para financiamento habitacional pelo SBPE (Sistema Brasileiro de Poupança e Empréstimo):

```
Poupança captada → 20% compulsório BCB → BCB direciona para SBPE → crédito imobiliário
```

Isso cria uma conexão entre os compulsórios bancários e as taxas do crédito imobiliário: quando os compulsórios de poupança são reduzidos, o SBPE fica com menos recursos para emprestar → taxas imobiliárias sobem → impacto negativo em [[incorporadoras]] de médio padrão. Para empresas focadas em MCMV (funding via FGTS), esse canal não se aplica.

## Ver Também

- [[banking]] — framework regulatório e DRE bancária completos
- [[selic]] — taxa de remuneração dos compulsórios remunerados
- [[nii_mercado]] — compulsórios remunerados entram no NII Mercado
- [[cet1]] — exigência de capital (diferente dos compulsórios)
- [[crescimento_carteira]] — compulsórios limitam a capacidade de crescer crédito
- [[itau]] — perfil ITUB4 com balanço e composição de ativos
- [[sanb11]] — menor base varejista → menor compulsório não-remunerado
- [[bradesco]] — base de captação de poupança relevante para SBPE
- [[incorporadoras]] — crédito imobiliário (SBPE) afetado indiretamente pelos compulsórios de poupança
