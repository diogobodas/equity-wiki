---
type: conceito
source_quality: conceptual
aliases: [Margem Backlog, Margem da Carteira, Backlog Margin, Margem Orçada]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/extraction/CYRE3_backlog_trimestral.json
  - sectors/real_estate/companies/CURY3/outputs/extraction/CURY3_backlog_trimestral.json
  - sectors/real_estate/companies/DIRR3/outputs/extraction/DIRR3_backlog_trimestral.json
  - sectors/real_estate/companies/TEND3/outputs/extraction/TEND3_backlog_trimestral.json
updated: 2026-04-05
---

# Margem Backlog

A **margem backlog** (também chamada de margem da carteira ou margem orçada) é a margem bruta esperada sobre a carteira de vendas contratadas ainda não reconhecidas como receita ([[poc_revenue]]). É o principal **indicador leading** da margem bruta futura em [[incorporadoras]].

## Definição

```
Margem Backlog = (Receita Contratada − Custo Orçado) / Receita Contratada
```

Onde:
- **Receita contratada** = valor de venda de unidades já vendidas, ainda não reconhecidas
- **Custo orçado** = estimativa de custo de construção e entrega no momento do lançamento

A margem é fixada no lançamento do empreendimento (quando o preço e o custo orçado são definidos). Ao longo da construção, desvios de custo real vs orçado impactam a margem realizada.

## Por Que é um Indicador Leading

O ciclo de uma incorporadora tem lag de 2-3 anos entre lançamento e reconhecimento de receita. A margem bruta que aparece na DRE hoje reflete empreendimentos lançados 2-3 anos atrás — a "safra" (vintage) sendo construída.

```
Lançamento (t=0) → Vendas → Construção (18-36 meses) → POC reconhece receita → DRE (t+8 a t+12 trimestres)
```

**Implicação prática:** a margem backlog atual prevê a margem bruta DRE de 2-3 anos à frente. Analistas monitoram a evolução trimestral da margem backlog como antecipação do P&L futuro.

## Gap: Margem Backlog vs Margem Realizada

A margem realizada (DRE) **sistematicamente** fica abaixo da margem backlog. Os principais motivos:

| Fator | Impacto | Quem é mais afetado |
|-------|---------|---------------------|
| Estouro de custo de obra | Reduz margem | Todos |
| INCC acima do orçado | Reduz margem | [[mcmv]] (sem correção de preço) |
| Distratos e vendas com desconto | Reduz margem | Todos |
| AVP (ajuste a valor presente) | Reduz receita reconhecida | Todos (maior impacto em carteira própria) |

**Gap típico por segmento:**
- MCMV puro ([[cury]], [[direcional]] Faixa 1-3): -4 a -6pp
- Alta-renda ([[cyrela]]): ~-3,5pp (protegida parcialmente pelo INCC)

## Como o Modelo Usa a Margem Backlog

No modelo financeiro, **margem bruta % é input direto** — não derivada de fórmula. O analista insere a margem esperada com base em:

1. Margem backlog atual reportada no release trimestral
2. Gap histórico entre backlog e realizado (backtest)
3. Tendência de INCC e custo de MDO
4. Mix de safras sendo reconhecidas no período

```
custo = −receita × (1 − margem_bruta_input / 100)
```

**Nunca** derivar margem bruta como função do backlog margin diretamente — o gap precisa de calibração por backtest.

## Benchmarks Históricos

| Empresa | Margem Backlog | Margem Bruta Realizada | Gap |
|---------|---------------|----------------------|-----|
| [[cury]] | ~43-44% | ~38-40% | ~-4pp |
| [[direcional]] | ~44-46% | ~39-40% | ~-5pp |
| [[cyrela]] | ~35-37% | ~32-34% | ~-3,5pp |

## Fontes de Dados

A margem backlog é reportada nos **releases trimestrais de RI** — não aparece no ITR/DFP padronizado. Cada empresa tem uma tabela de "carteira contratada" no release com:
- Receita a apropriar (backlog de receita)
- Margem estimada da carteira (%)

Algumas empresas detalham margem por segmento (MCMV vs alto padrão), o que permite análise de mix.

## Interpretação Analítica

| Movimento | Sinal | Interpretação |
|-----------|-------|---------------|
| Margem backlog sobe | Positivo | Novos lançamentos com margens mais altas; pricing power |
| Margem backlog cai | Negativo | Pressão de custos, INCC, ou lançamentos de menor margem |
| Gap backlog-realizado se expande | Negativo | Estouro de custos, INCC acima do esperado, distratos |
| Gap backlog-realizado se comprime | Positivo | Execução melhor que o orçado |

## Análise de Safra (Vintage Analysis)

A margem backlog é uma média ponderada de empreendimentos em diferentes fases de construção. Para um analista sofisticado, é importante decompor por "safra":

```
Margem_backlog_total = Σ [Backlog_empreendimento_i × Margem_orçada_i] / Backlog_total
```

**Quando a margem backlog sobe progressivamente:** Novas safras lançadas com margens maiores que as antigas (pricing power, custo de terreno cai, INCC do período menor). A melhora leva 2-3 anos para se materializar no resultado.

**Quando a margem backlog cai abruptamente:** Lançamentos de emergência com desconto, aumento de INCC não reprecificado, ou deterioração de custo de terreno em novas praças.

### Exemplo: Cury em 2025-2026

Decisões calibradas do modelo CURY3 (verificadas):
- Margem backlog ajustada de 39,7% → 40,0% com base no guidance management "40 com 20"
- Histórico recente: 39,2 → 39,7 → 40,0 → 40,3 (tendência de leve alta)
- Gap realizado esperado: ~-4pp → margem bruta DRE ~36-38%

A estabilidade da margem backlog da Cury reflete a homogeneidade do produto (MCMV puro, tickets similares, geografia concentrada em SP/RJ).

## Margem Backlog vs Margem de Novos Lançamentos

A margem backlog é uma **média acumulada histórica**. A margem dos **novos lançamentos** (safra atual) pode ser diferente:

```
Margem_novos_lançamentos ≠ Margem_backlog_total (especialmente em transição de ciclo)
```

Se a empresa está lançando com margem de 45% (vs backlog médio de 40%), a margem backlog vai subir ao longo dos próximos 2-3 anos conforme o backlog antigo (40%) é reconhecido e substituído pelo novo (45%).

**Como identificar:** Comparar a margem orçada dos empreendimentos lançados nos últimos 2 trimestres com a margem backlog total. Se houver gap positivo (novos > média), a margem tende a subir.

## Qualidade da Informação por Empresa

| Empresa | Divulgação | Detalhe |
|---------|-----------|---------|
| [[cury]] | Ótima — margem backlog publicada no release trimestral | Separado por segmento em alguns releases |
| [[direcional]] | Boa — margem backlog consolidada | Riva e DIRR geralmente separados |
| [[cyrela]] | Boa — margem backlog total + por segmento | Vivaz vs alta-renda separados |
| [[tenda]] | Moderada — margem consolidada | Alea e Tenda principal misturados |

## Relação com o Guidance de Margem

O management de incorporadoras frequentemente dá guidance de margem bruta baseado na margem backlog:

**Exemplo típico de guidance:**
> "Esperamos margem bruta de 35-37% no ano 2026, em linha com o backlog atual de 40% ajustado pelo gap histórico."

Quando o management dá guidance de margem bruta diretamente (ex: "40% +/-"), é mais simples — usar diretamente como premissa do modelo.

Quando o guidance é de margem backlog + gap esperado, o analista precisa aplicar o gap histórico calibrado.

## Margem Backlog por Segmento: [[alto_padrao]] vs MCMV

O segmento de [[alto_padrao]] tem estrutura de margem backlog distinta do MCMV:

| Característica | [[alto_padrao]] | MCMV |
|---------------|----------------|------|
| Margem backlog típica | 35-42% | 40-46% |
| Correção de preço | Sim (INCC durante obra) | Não (preço travado) |
| Gap backlog → realizado | ~-2 a -3pp | ~-4 a -6pp |
| Exposição ao [[incc]] | Parcialmente protegida | Totalmente exposta |
| Risco de distrato | Baixo (comprador com equity) | Moderado |

Paradoxalmente, o [[alto_padrao]] tem margem backlog **menor** que o MCMV na tabela, mas gap **menor** — ou seja, realiza mais próximo do orçado. O MCMV tem margem backlog aparentemente alta mas que se degrada mais na execução.

Para [[lavvi]] e segmento Cyrela, a margem backlog de 35-40%+ com gap ~-3pp implica margem bruta realizada de ~32-37% — superior ao MCMV em termos de resultado efetivo.

## Ver Também

- [[vgv_lancamentos]] — volume de lançamentos que alimenta o backlog e define a margem das novas safras
- [[poc_revenue]] — reconhecimento de receita sobre o backlog; timing do gap
- [[incorporadoras]] — hub setorial com contexto de safra/vintage
- [[incc]] — inflação da construção civil que corrói margem MCMV
- [[mcmv]] — segmento mais exposto ao gap de margem (preço travado)
- [[alto_padrao]] — margem backlog menor, mas gap menor também; realização mais próxima do orçado
- [[cyrela]] — margem backlog alta-renda + Vivaz; gap menor
- [[cury]] — MCMV puro; margem backlog ~40%; gap ~-4pp; verificado modelo
- [[direcional]] — MCMV + Riva; gap ~-5-6pp
- [[lavvi]] — player alto padrão SP; margem backlog ~35-40%
- [[capital_de_giro]] — backlog elevado = mais recebíveis = mais capital de giro necessário
