---
type: empresa
source_quality: conceptual
aliases: [Lavvi Incorporadora, Lavvi, LAVV3]
sources:
  - sectors/real_estate/sector_profile.md
  - wiki/incorporadoras.md
  - wiki/cyrela.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CYRE3/outputs/model/CYRE3_model.json
updated: 2026-04-05
---

# Lavvi Incorporadora

A **Lavvi Incorporadora** (LAVV3) é uma incorporadora focada no segmento de **alto e médio-alto padrão** em São Paulo, fundada como joint venture entre a [[cyrela]] e o grupo Gafisa/Tecnisa (origem dos fundadores). A empresa tem como diferencial a concentração geográfica em São Paulo (especialmente Zona Sul e regiões valorizadas), com produtos de alto ticket médio e margens brutas elevadas.

## Modelo de Negócio

A Lavvi opera exclusivamente em São Paulo, focada em três segmentos de produto:

- **Alto padrão**: Empreendimentos acima de R$15.000/m², tipicamente nos bairros mais valorizados de SP (Jardins, Itaim, Vila Nova Conceição, Moema)
- **Médio-alto**: Produtos de R$8.000-15.000/m², com localização privilegiada
- **Sem MCMV**: Deliberadamente fora do programa habitacional popular — margem bruta mais baixa e ciclo operacional diferente

## Relação com Cyrela

A Lavvi é uma das **EP investidas** da [[cyrela]] — a Cyrela detém participação e registra Equivalência Patrimonial (EP) nos resultados. Essa relação é relevante para o modelo CYRE3:

```
EP_cyrela += Participação_cyrela × LL_lavvi
```

A Cyrela tem parceria estratégica com a Lavvi desde a fundação — acesso à base de clientes Cyrela, compartilhamento de terrenos e expertise operacional. A Lavvi é considerada uma das incorporadoras "premium" do ecossistema Cyrela.

## Características do Negócio

| Métrica | Referência |
|---------|-----------|
| Foco geográfico | São Paulo (único mercado) |
| Ticket médio | ~R$2-4M por unidade (estimativa) |
| Margem bruta típica | ~35-40%+ (alto padrão tem margens superiores) |
| VGV médio por lançamento | ~R$500M-1,5B |
| Estrutura | Capital aberto (LAVV3 na B3) |

**Nota:** Valores são estimativas conceptuais. Verificar releases LAVV3 para dados exatos.

## Diferenças vs Peers

| Aspecto | Lavvi | [[cyrela]] | Direcional |
|---------|-------|---------|-----------|
| Segmento | Alto padrão exclusivo | Alto + médio | Baixo-médio + MCMV |
| Geog. | São Paulo apenas | SP + RJ + outros | Nacional |
| Margem bruta | Alta (35-40%+) | Média-alta (30-35%) | Baixa-média (25-30%) |
| Ciclicidade | Alta vs ciclo econômico | Moderada | Baixa (MCMV é defensivo) |
| VGV por lançamento | Alto | Diversificado | Diversificado |

## Relevância para o Modelo CYRE3

A Lavvi entra no modelo Cyrela pelo canal de **Equivalência Patrimonial**:
- LL Lavvi × % participação Cyrela → EP_lavvi em CYRE3
- EP_lavvi é uma das componentes do EP_total no modelo CYRE3 (ao lado de [[cury]] e outros)

Em períodos de ciclo favorável ao alto padrão (2021-2022, 2025), a Lavvi tende a gerar EP relevante para a Cyrela. Em ciclos adversos (taxa de juros alta afeta crédito imobiliário de alto valor), o impacto é negativo.

## Riscos Específicos

1. **Concentração geográfica**: 100% São Paulo — sem diversificação de ciclo regional
2. **Ciclicidade do alto padrão**: Demanda mais sensível a confiança do consumidor e taxa de juros
3. **Concorrência em SP alto padrão**: Tegra, EZTC3 (especificamente São Paulo), outros players regionais premium
4. **Execution risk em terrenos**: Terrenos em São Paulo são escassos e caros — landbank é o principal gargalo

## Posicionamento vs Mercado de Alto Padrão SP

No segmento de [[alto_padrao]] em São Paulo, a Lavvi compete diretamente com:
- **EzTec (EZTC3)**: maior player puro de alto padrão SP, com landbank próprio diversificado
- **Tegra**: operadora de alto padrão focada em SP e RJ
- **Vitacon/SYN**: nicho de compactos de alto padrão
- **Cyrela diretamente**: a própria Cyrela lança produtos de alto padrão sob a marca Cyrela Living/Cyrela Fit

A diferenciação da Lavvi está na concentração em **poucos empreendimentos de grande porte** (vs carteiras diversificadas) e no acesso ao landbank da Cyrela em localizações prime — que a própria Cyrela prefere alocar para a Lavvi quando o produto exige personalização de luxo.

## Calendário de Reconhecimento vs CYRE3

A contribuição da Lavvi ao EP do CYRE3 é **trimestral e baseada no LL da Lavvi**. Como o ciclo de obra da Lavvi é longo (36+ meses), o LL da Lavvi é mais volátil trimestralmente do que o da Cyrela:

- **Quarters de entrega (batismo)**: LL da Lavvi sobe significativamente quando empreendimentos de alto ticket são entregues e o custo final é reconhecido
- **Quarters de lançamento puro**: LL baixo (receita se acumula no backlog, não flui para a DRE ainda)

Para o modelo CYRE3, o analista deve atentar ao calendário de entregas da Lavvi quando projetar EP_lavvi.

## Ver Também

- [[cyrela]] — sócia fundadora e acionista; EP investida relevante para CYRE3
- [[incorporadoras]] — setor de real estate brasileiro
- [[equivalencia_patrimonial]] — mecanismo pelo qual Lavvi contribui para o resultado Cyrela
- [[vgv_lancamentos]] — principal métrica operacional de incorporadoras
- [[margem_backlog]] — margem sobre VGV contratado
- [[alto_padrao]] — segmento de mercado residencial premium SP (Lavvi é player puro)
- [[poc_revenue]] — reconhecimento de receita pelo método POC
- [[incc]] — correção de preços durante obra protege margem do alto padrão
