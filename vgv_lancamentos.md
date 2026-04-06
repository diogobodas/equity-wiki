---
type: conceito
source_quality: conceptual
aliases: [VGV, Valor Geral de Vendas, VGV Lançado, Lançamentos]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/DIRR3/outputs/decomposition/DIRR3_dependency_graph_v3.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
updated: 2026-04-05
---

# VGV — Valor Geral de Vendas

O **VGV (Valor Geral de Vendas)** é a soma dos preços de tabela de todas as unidades de um empreendimento ao preço de lançamento. É a métrica primária do setor de [[incorporadoras]] porque representa o tamanho do pipeline de receita futura antes do reconhecimento contábil.

## Definição e Fórmula

```
VGV = Número de unidades × Preço médio por unidade (na data de lançamento)
```

O VGV é calculado **no lançamento** e permanece fixo como referência — mesmo que o preço de venda efetivo varie ao longo da obra (correção por INCC para alto/médio padrão; preço travado para [[mcmv]]).

## Convenção Crítica: VGV 100% vs % Cia

**O modelo usa VGV 100% consolidado, não % Cia.**

Quando uma incorporadora lança um empreendimento em parceria (ex: 50/50 com outra empresa), o VGV total do empreendimento é 100%. A participação da empresa no resultado aparece via:
- **Consolidação integral** (se controla a SPE): receita 100% + minoritários deduzidos após o LL
- **Equivalência patrimonial** (se não controla): entra apenas na linha de EP

**Por que importa:** Usar VGV % Cia subestima o backlog e a receita futura. O modelo sempre acumula VGV 100% no backlog rollforward.

## Relação com o Modelo de Receita

O VGV lançado alimenta o pipeline de vendas, que por sua vez alimenta o backlog:

```
Vendas_novas(t) = VGV_lançado(t) × VSO(t)  [VGV 100%]
Backlog_fim(t)  = Backlog_início(t) + Vendas_novas(t) − Receita_reconhecida(t)
Receita(t)      = Backlog_início(t) × POC_sazonal(t)
```

O lag entre lançamento e reconhecimento de receita é de **2 a 3 anos**. Um VGV de lançamentos alto hoje não gera receita imediata — alimenta o backlog que será reconhecido ao longo da construção.

## VGV Lançado vs VGV Vendido (Vendas Contratadas)

| Métrica | Significado |
|---------|-------------|
| VGV Lançado | Valor total das unidades colocadas no mercado no período |
| VGV Vendido (Vendas Contratadas) | Valor das unidades efetivamente vendidas = VGV lançado × VSO |
| Backlog | Carteira acumulada de vendas contratadas ainda não reconhecidas como receita |

## Como Projetar

VGV lançado é **input exógeno** — definido pelo analista com base em:
1. **Guidance da gestão** — pipelines anunciados de projetos e terrenos aprovados
2. **Sazonalidade** — 2T e 4T são historicamente mais fortes; 1T mais fraco
3. **Contexto regulatório** — alvarás municipais, aprovações (ex: liminar SP 2026)
4. **Macro** — ciclo de crédito imobiliário, [[selic]], demanda por segmento

**YoY, não QoQ:** As projeções crescem sobre o mesmo trimestre do ano anterior (YoY), não sobre o trimestre anterior — dado que a sazonalidade é forte e consistente.

## Sazonalidade

```
1T (mais fraco) → 2T (pico 1) → 3T (intermediário) → 4T (pico 2)
```

- Pico em 2T e 4T coincide com feiras de imóveis (Salao do Imóvel SP, etc.)
- 1T fraco: pós-festas, aprovações de projeto ainda em andamento

## Denominadores Corretos

As despesas comerciais são relacionadas ao VGV lançado (não à receita POC):

```
Desp. Comerciais = VGV_Cia_rolling_4Q × % + Fixo/tri
```

**Por que VGV, não receita:** os gastos de marketing/comissão ocorrem no lançamento; a receita POC é reconhecida 2-3 anos depois. Usar receita como denominador subestima a carga comercial sobre o volume de atividade real.

## Benchmarks Históricos

| Empresa | VGV Lançado 100%/tri | Observação |
|---------|---------------------|------------|
| [[cyrela]] | ~R$3-4bi | Alta variância (alta-renda = projetos grandes) |
| [[cury]] | ~R$1,9-2,1bi | Mais estável; tickets menores; foco SP/RJ |
| [[direcional]] | ~R$2,0-2,1bi | Guidance 2026: R$8bi/ano (~R$2bi/tri) |

## Riscos de Projeção

- **Concentração de aprovações** — projetos grandes podem criar spike de VGV em um único trimestre
- **Alvarás** — aprovações municipais atrasam lançamentos (ex: liminar SP 2026 impacta ~15%)
- **Ciclo político MCMV** — mudanças de teto afetam viabilidade de empreendimentos planejados
- **Distratos** — cancelamentos antes da entrega reduzem backlog retroativamente

## VGV e Ticket Médio: Análise de Mix

O VGV pode crescer por duas alavancas independentes:

```
VGV = Número_de_unidades × Ticket_médio
```

**Crescimento por volume:** Lançar mais unidades → reflete capacidade construtiva, terrenos disponíveis, aprovações municipais.

**Crescimento por preço:** Ticket médio sobe (inflação INCC em alto padrão, ou mix shift para projetos maiores) → reflete pricing power e mix de produto.

Para o analista, separar as duas alavancas é importante:
- Crescimento por volume é sustentável se o mercado absorver (VSO se mantém)
- Crescimento por preço é sustentável se a renda do comprador também crescer (affordability)

## Guidances e Comunicação com o Mercado

As incorporadoras comunicam VGV lançado de formas diferentes:

| Tipo de Guidance | Exemplo | Confiabilidade |
|-----------------|---------|---------------|
| Guidance anual confirmado | "VGV lançado 2026: R$8bi" ([[direcional]]) | Alta — company-level commitment |
| Range de guidance | "R$10-12bi em 2026" | Moderada — usa o meio do range |
| Sem guidance formal | Apenas histórico | Usa média histórica ± contexto |
| Por segmento | "Vivaz 40% do total" ([[cyrela]]) | Alta para divisão; média para total |

**Regra de uso no modelo:** Guidance annual / 4 para a base trimestral, ajustado pela sazonalidade histórica. VGV 1T historicamente ~85-90% da média trimestral.

## Landbank: Reserva Estratégica de VGV

O **landbank** (estoque de terrenos) é o pipeline de VGV futuro não lançado. A razão landbank/VGV anual mede a "reserva" de crescimento:

```
Cobertura_landbank = VGV_landbank / VGV_lançado_anual
```

| Empresa | Cobertura Típica | Observação |
|---------|-----------------|------------|
| [[cyrela]] | 3-5 anos | Grande landbank SP diversificado |
| [[cury]] | 2-3 anos | Landbank SP/RJ concentrado; reposição frequente |
| [[direcional]] | 3-4 anos | Nacional; inclui praças menores com aprovação mais rápida |
| [[tenda]] | 2-3 anos | Foco em terrenos com alvará já aprovado (ciclo curto) |

**Análise do landbank** é feita via releases e planilhas de RI (Relações com Investidores) — não está no ITR/DFP padrão.

## VGV e Despesas Comerciais

As despesas de vendas (comissões de corretores, marketing, stand de vendas) são tipicamente calculadas como % do VGV lançado (não da receita reconhecida):

```
Desp_Comerciais ≈ VGV_Cia_rolling_4Q × % Desp_Com + Fixo_por_lançamento
```

**Por que VGV, não receita:** Os gastos de marketing ocorrem no momento do lançamento; a receita POC é reconhecida 2-3 anos depois. A base correta para o custo de aquisição de clientes é o VGV lançado, não a receita contábil.

**Implicação:** Empresas com VGV crescendo mais rápido que receita (backlog em formação) terão desp. comerciais altas como % da receita. Isso é esperado e não é sinal de deterioração — é sinal de que a empresa está crescendo o pipeline futuro.

## Benchmarks de VGV por Empresa (Modelo)

| Empresa | VGV 100%/tri (2026E) | Crescimento YoY | Fonte |
|---------|---------------------|----------------|-------|
| [[cyrela]] | ~R$3.000-4.000M | +5-10% | Guidance 2026 |
| [[cury]] | ~R$1.950M | +10-15% | Modelo calibrado 2026 (1950/tri ajustado) |
| [[direcional]] | ~R$2.000M | +10% | Guidance "R$8bi/ano" 2026 |
| [[tenda]] | ~R$1.450M total (TENDA ~1.400 + ALEA ~50) | +5% | Index TEND3 |
| [[plano_plano]] | ~R$1.150M | Normalização vs 2025 recorde R$18.6B | Modelo PLPL3 calibrado 2026 |

## Ver Também

- [[velocidade_vendas]] — VSO, conversão de VGV em vendas contratadas
- [[margem_backlog]] — margem orçada da carteira; definida no lançamento
- [[poc_revenue]] — reconhecimento de receita sobre o backlog acumulado
- [[mcmv]] — programa que define teto de preço; limita ticket médio para Faixas 1-3
- [[incc]] — correção de preço durante obra (alto/médio padrão); afeta VGV realizado
- [[incorporadoras]] — hub setorial
- [[cyrela]] — maior VGV privado do Brasil; alta variância por projeto
- [[cury]] — VGV MCMV estável e previsível; tickets menores; SP/RJ
- [[plano_plano]] — VGV MCMV SP puro; recorde R$18.6B em 2025; normalização 2026
- [[direcional]] — VGV nacional com landbank 7 anos de runway
- [[tenda]] — multi-segmento TENDA (~R$1.400M) + ALEA (~R$50M)
- [[capital_de_giro]] — VGV crescente = mais terrenos comprados = mais capital de giro
