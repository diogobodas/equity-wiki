---
type: conceito
source_quality: conceptual
aliases: [INCC, Índice Nacional de Custo da Construção, Inflação da Construção Civil]
sources:
  - sectors/real_estate/sector_profile.md
  - wiki/incorporadoras.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
updated: 2026-04-05
---

# INCC — Índice Nacional de Custo da Construção

O **INCC (Índice Nacional de Custo da Construção)** mede a variação dos custos de construção civil no Brasil. É publicado mensalmente pela FGV e é o principal indexador de contratos de incorporação imobiliária para empreendimentos de **médio e alto padrão**. Para o [[mcmv]], o INCC é o principal risco de margem — não o indexador do preço de venda, mas o driver de custo.

## Por Que o INCC Importa para Incorporadoras

O ciclo de uma incorporação dura 18-36 meses entre lançamento e entrega. Durante esse período:

| Segmento | Preço de Venda | Custo de Obra |
|----------|---------------|---------------|
| Alto/médio padrão | Corrigido pelo INCC | Sobe com INCC |
| [[mcmv]] Faixas 1-3 | **Travado** (teto Caixa) | Sobe com INCC |

**Para MCMV:** a incorporadora arca com 100% da alta de custos durante a obra sem poder repassar ao comprador. Sensibilidade histórica: **+3pp de INCC ≈ −1,5 a −2,0pp de margem bruta realizada** para empresas MCMV puras.

**Para alto padrão:** a correção pelo INCC protege parcialmente. O risco é menor, mas ainda existe quando o INCC real supera o INCC orçado no lançamento.

## Composição do INCC

O índice mede variações em:
- **Materiais de construção** (~45% do peso): aço, cimento, revestimentos, hidráulica, elétrica
- **Mão de obra** (~55% do peso): salários e encargos da construção civil

A componente de MDO é mais rígida: reajustes salariais no setor têm negociações coletivas anuais (geralmente acima da inflação geral). A componente de materiais é mais volátil e sensível a câmbio e demanda global (aço importado, cobre).

## Relação com Outros Índices

| Índice | Mede | Relação com INCC |
|--------|------|-----------------|
| INCC | Custo de construção civil | — |
| IPCA | Inflação ao consumidor | INCC normalmente > IPCA em ciclos de crescimento imobiliário |
| IGP-M | Inflação geral (ponderada) | INCC tem correlação com IGP-M (ambos FGV) |
| [[selic]] | Taxa básica | Correlação inversa: Selic alta desaquece construção, reduz pressão de MDO |

## INCC Histórico e Projeções

| Período | INCC 12M | Observação |
|---------|---------|------------|
| 2021 | ~15% | Pandemia: demanda de materiais explodiu, supply chain restrito |
| 2022 | ~8-10% | Normalização de supply chain |
| 2023-24 | ~6-8% | Boom MCMV; MDO aquecida |
| Mar/2026 | **5,81%** | Desaceleração; favorável a margens MCMV |
| Projeção modelo | 6,0% | Input exógeno nas premissas |

## Impacto no Modelo Financeiro

No modelo, o INCC entra de duas formas:

1. **Input exógeno de premissa macro** (Selic, IPCA, INCC): usado na calibração das despesas financeiras e como contexto para margem bruta

2. **Driver implícito de margem bruta:** a [[margem_backlog]] vs margem realizada incorpora historicamente o efeito do INCC. O gap é calibrado por empresa:
   - [[cury]]: gap ~-4pp (100% MCMV; ciclo curto 18-24m reduz exposição)
   - [[direcional]]: gap ~-5-6pp (mix MCMV + AVP material)
   - [[cyrela]] (Vivaz): gap ~-4pp; Cyrela alta-renda ~-3,5pp

## Proteção Parcial: Correção INCC no Alto Padrão

Para médio e alto padrão (exceto MCMV), os contratos de compra e venda têm cláusula de correção pelo INCC. Isso significa que o preço de venda sobe proporcionalmente ao avanço do INCC durante a obra. A proteção é **parcial** porque:
- O custo de obra também sobe com o INCC → proteção líquida é ~0 em cenário base
- Se INCC real > INCC orçado, a diferença entre receita ajustada e custo real é favorável para o construtor
- Se INCC real < INCC orçado, pode haver pressão de demanda (compradores reclamam do reajuste)

## INCC e o Ciclo de Obra: Exposição Acumulada

O risco de INCC não é pontual — é acumulado ao longo de toda a construção. Para um empreendimento MCMV com ciclo de 18 meses:

```
Exposição_INCC = Σ [INCC_mensal(i) × Custo_a_incorrer(i) / Custo_total]
               ≈ INCC_18m × 0,6   (ponderado pelo cronograma físico-financeiro)
```

A exposição não é 100% do INCC do período porque parte do custo já foi incorrido. No início da obra, a exposição é máxima; no final, é mínima. Por isso, o gap de margem é **maior para empreendimentos lançados em ciclos de INCC alto** que ainda têm muito custo pela frente.

**Implicação para o analista:** verificar o INCC acumulado nas "safras" (vintages) que estão sendo reconhecidas no trimestre atual. Um INCC de 8% por 18 meses equivale a acumulado de ~12-13% — se o custo orçado não incluiu esse buffer, a margem vai ser comprimida.

## INCC vs IPCA: Divergência Estrutural

O INCC historicamente supera o IPCA em ciclos de aquecimento do setor:

| Período | INCC Acumulado | IPCA Acumulado | Spread |
|---------|----------------|----------------|--------|
| 2019-2021 | ~22% | ~17% | +5pp |
| 2022-2024 | ~22% | ~23% | −1pp (excepcional: commodities puxaram IPCA) |
| 2025 | ~6% | ~5,5% | +0,5pp (normalizado) |

**O spread INCC-IPCA reflete o mercado de trabalho da construção:** quando a demanda por mão de obra de construção supera a oferta (boom de MCMV), os salários do setor sobem acima da inflação geral. Isso é o maior componente de risco de custo para as incorporadoras.

## Estratégias de Mitigação

As incorporadoras utilizam diferentes estratégias para proteger margens contra o INCC:

### 1. Compra Antecipada de Insumos
Contratos de fornecimento de aço, cimento e outros insumos fechados no lançamento — trava o custo antes do INCC subir. Risco: se INCC cair, perdeu a oportunidade de comprar mais barato.

### 2. Ciclo Mais Curto (Cury com Formas de Alumínio)
A [[cury]] reduz o ciclo de obra para 18-20 meses (vs 24-30 meses de outros). Com ciclo menor, a janela de exposição ao INCC é menor:

```
Exposição_INCC_Cury ≈ INCC_18m  vs  Exposição_geral ≈ INCC_24-30m
```

Isso é uma vantagem competitiva estrutural — a Cury entrega mais rápido e fica menos exposta ao custo de construção inflacionado.

### 3. Landbank com Construção Imediata
Lançar e começar a construção imediatamente (não acumular landbank pronto antes de vender) reduz o período em que o custo fica exposto ao INCC antes de ter qualquer receita reconhecida.

## Impacto por Empresa (Síntese)

| Empresa | Exposição INCC | Mitigação | Gap Histórico |
|---------|---------------|-----------|---------------|
| [[cury]] | Alta (100% MCMV) | Ciclo curto 18-20m; formas alumínio | ~-4pp vs backlog |
| [[direcional]] | Média-alta (70% MCMV) | Diversificação de safras | ~-5-6pp vs backlog |
| [[tenda]] | Alta (100% MCMV) | Ciclo curto; Alea em teste | ~-4-5pp vs backlog |
| [[cyrela]] | Baixa (alto padrão + INCC corrige preço) | Correção de preço; projetos premium | ~-3,5pp vs backlog |
| [[lavvi]] | Baixa (100% alto padrão SP) | Correção integral pelo INCC; landbank premium | ~-2 a -3pp vs backlog |

## Ver Também

- [[mcmv]] — 100% exposto ao INCC (sem correção de preço)
- [[alto_padrao]] — parcialmente protegido pelo INCC via correção de preço no contrato
- [[margem_backlog]] — gap backlog vs realizado é função do INCC acumulado
- [[incorporadoras]] — hub setorial com contexto de INCC em modelos
- [[selic]] — taxa macro correlacionada com ciclo de construção
- [[cury]] — empresa MCMV puro mais sensível ao INCC; ciclo curto como mitigação
- [[direcional]] — mix MCMV econômico + Riva
- [[lavvi]] — alto padrão SP; INCC corrige preço → proteção estrutural
- [[poc_revenue]] — o lag de reconhecimento de receita prolonga a exposição ao INCC
- [[capital_de_giro]] — estoques e recebíveis amplificados pelo ciclo longo de construção
