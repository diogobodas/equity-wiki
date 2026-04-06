---
type: empresa
source_quality: conceptual
aliases: [EzTec, EZTC3, EZ Tec, EzTec Empreendimentos]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/EZTC3/company.json
  - sectors/real_estate/companies/EZTC3/outputs/decomposition/EZTC3_dependency_graph_v3.json
  - wiki/incorporadoras.md
  - wiki/cyrela.md
updated: 2026-04-05
---

# EzTec (EZTC3)

A **EzTec Empreendimentos e Participações** (EZTC3) é uma incorporadora brasileira focada nos segmentos **residencial médio-alto** e **comercial** (escritórios, galpões, salas comerciais). Fundada pela família Zarzur, tem atuação concentrada em São Paulo, com portfólio de produtos mais diversificado que incorporadoras puramente residenciais.

**Status no modelo:** Configurada — dependency graph existe, mas sem extração de dados históricos. Ainda não tem modelo financeiro computado.

## Perfil da Empresa

| Atributo | Valor |
|---------|-------|
| Ticker | EZTC3 |
| Segmentos | Residencial médio-alto, comercial (escritórios/galpões) |
| Mercado principal | São Paulo (SP) |
| Controle | Família Zarzur (fundadores) |
| Status modelo | Configurado — sem dados históricos |

## Diferencial Competitivo

A EzTec tem algumas características distintivas no setor:

1. **Diversificação residencial + comercial**: Ao contrário de [[cyrela]] (foco residencial) e [[cury]] (foco MCMV), a EzTec tem portfólio misto. O segmento comercial pode representar 20-40% do VGV em anos de alta demanda por escritórios em SP.

2. **Posição financeira conservadora**: Historicamente, EzTec opera com caixa líquido positivo (dívida líquida negativa) — um diferencial em um setor tipicamente alavancado. O landbank próprio e a gestão conservadora de caixa são traços da gestão familiar.

3. **Geração de caixa superior**: Por operar mais próxima do equilíbrio WC (menor crescimento explosivo que CURY3 ou DIRR3), a EzTec costuma ter FCO mais estável.

4. **Foco em São Paulo e regiões nobres**: Não tem exposição ao programa MCMV. Foco em imóveis de R$500k-R$2M+.

## Segmentos

### Residencial Médio-Alto

Similar à [[cyrela]] no posicionamento, mas em menor escala. Produtos tipicamente:
- Apartamentos entre R$500k e R$2M em SP
- Marca própria EzTec com reputação de qualidade
- VGV por unidade maior que MCMV, menor que ultra-luxo

### Comercial

Diferencial estratégico:
- Escritórios (lajes corporativas e salas)
- Galpões logísticos (cresceu com e-commerce pós-2020)
- Salas comerciais em empreendimentos mistos

O ciclo comercial tem timing diferente do residencial e pode ser um hedge natural para a empresa — quando o residencial desacelera, o comercial pode estar em alta, e vice-versa.

## O Que Falta para o Modelo

Para iniciar a cobertura da EzTec (initiating-coverage), é necessário:

- [ ] **Releases trimestrais** em `sectors/real_estate/companies/EZTC3/filings/releases/` — pelo menos 8 trimestres (2023-2025)
- [ ] **ITR/DFP** da CVM (baixar com `download_cvm_filings.py --ticker EZTC3`)
- [ ] **Extração histórica** (Task 1 do initiating-coverage):
  - `EZTC3_historical_financials_*.json`
  - `EZTC3_historical_operational_*.json`
  - `EZTC3_backlog_trimestral.json`
- [ ] **Decomposição manual** (Task 2): revisar e ajustar `EZTC3_dependency_graph_v3.json` existente para refletir a estrutura real da empresa
- [ ] **Backtest** (Task 3): calibrar premissas vs histórico

## Premissas Preliminares (Estimativas sem Verificação)

ESTIMATIVA NÃO VERIFICADA — Referência conceptual até extração real:

| Premissa | Estimativa | Racional |
|----------|-----------|---------|
| Margem bruta % | ~35-40% | Médio-alto tem margem maior que MCMV (~30%); menor que ultra-luxo |
| VSO trimestral | ~18-25% | Segmento sensível a juros; estimativa conservadora |
| Dias recebíveis | ~180-220 dias | Similar a outras incorporadoras médio-alto |
| g_vgv_lancamentos | +5-10% a.a. | Crescimento moderado conservador |
| Dívida líquida/PL | Negativo (caixa) | Historicamente EzTec opera com caixa líquido |

## Considerações para o Modelo

### Segmento Comercial: Complicação Metodológica

A presença do segmento comercial cria complexidade para o modelo:
- O ciclo de construção e entrega é diferente (galpões mais rápidos; escritórios mais lentos)
- O reconhecimento de receita pelo [[poc_revenue]] tem dinâmica diferente por produto
- A demanda comercial tem drivers macro diferentes (emprego formal, aluguel corporativo, e-commerce)

**Abordagem sugerida:** Modelar separadamente como dois "segmentos" (residencial e comercial) usando `compute_segment.py`, depois consolidar com `consolidate_segments.py`.

### Sem Investidas (EP Zero)

Diferente da [[cyrela]], a EzTec não tem equity pickup relevante — `has_ep_investidas: false`. Simplifica o modelo.

### Backlog: VGV 100% Consolidado

Mesma convenção das outras incorporadoras: usar VGV 100% (não % Cia) no backlog para consistência com o [[poc_revenue]] de receita consolidada.

## Perfil Financeiro Histórico (Estimativas — Sem Extração Real)

As estimativas abaixo são baseadas em análise qualitativa do setor e posicionamento da empresa. **Não usar para modelagem** — substituir por dados reais após extração.

| Ano | Receita (R$M) | MB% | LL (R$M) | ML% | ROE |
|-----|--------------|-----|----------|-----|-----|
| 2022 | ~800-1.000 | ~35-40% | ~150-200 | ~18-22% | ~12-18% |
| 2023 | ~1.000-1.200 | ~36-40% | ~180-230 | ~16-20% | ~13-18% |
| 2024 | ~1.100-1.300 | ~35-39% | ~200-270 | ~17-21% | ~14-19% |
| 2025 | ~1.200-1.500 | ~34-38% | ~220-300 | ~17-21% | ~14-20% |

**IMPORTANTE: São estimativas para referência conceptual. Devem ser substituídas por dados reais do release EZTC3 ao iniciar extração.**

### Por Que a Margem é Alta vs Peers

A EzTec opera com margens brutas acima da média setorial pelos seguintes fatores estruturais:

1. **Landbank próprio e de custo histórico baixo**: A família Zarzur acumulou terrenos em São Paulo ao longo de décadas. O custo contábil desses terrenos é substancialmente abaixo do valor de mercado atual, criando margem "escondida" que aparece quando o terreno é incorporado no custo de um empreendimento ao valor de aquisição original (muito abaixo do VGV potencial).

2. **Produto médio-alto sem MCMV**: Margem bruta de incorporadoras MCMV converge para ~30-33%. EzTec, operando em alto padrão com tickets de R$500k-R$2M+, consegue margens de ~35-40% — a escassez de oferta em regiões premium de SP sustenta preços que mais do que compensam o custo do terreno.

3. **Ausência de alavancagem de volume**: Empresas que crescem explosivamente (CURY3, PLPL3) precisam comprar terrenos ao preço de mercado e financiar capital de giro. A EzTec cresce de forma mais contida, o que preserva a margem mas limita o crescimento de receita.

## Tese de Investimento (Framework)

A EzTec é tipicamente analisada como uma **opção de qualidade** no setor de incorporadoras — performance mais estável do que peers expostas ao MCMV ou à alavancagem operacional alta. A tese tem dois lados:

### Bull Case
- Landbank valioso em SP prime que sustenta decades de lançamentos sem necessidade de recompra de terrenos
- Posição de caixa líquido positivo protege contra ciclos de juros altos
- Diversificação residencial + comercial cria hedge natural de ciclo
- Management conservador com histórico de geração de valor para acionistas no longo prazo

### Bear Case
- Crescimento de receita limitado vs peers de MCMV que lançam volumes exponencialmente maiores
- Exposição ao ciclo de juros no segmento médio-alto: Selic alta em 2026 (~15%) afeta crédito imobiliário acima de R$1M (que sai do SFH e vai para mercado livre com taxas mais altas)
- Segmento comercial tem ciclo próprio: vacância corporativa em SP pode pressionar VGV comercial
- Menor free float e liquidez vs CYRE3, CURY3, DIRR3 — multiple discount por liquidez

## Posição na Cobertura

Na cobertura atual do projeto, a EzTec está na fila de iniciação de cobertura após PLPL3 e TEND3. O dependency graph existe e foi configurado, mas o modelo financeiro aguarda:
1. Download dos releases trimestrais
2. Extração histórica (Task 1 do skill initiating-coverage)
3. Backtest e calibração de premissas

A EzTec é um caso mais simples que a Cyrela (sem EP investidas, sem subsidiária financeira, sem MCMV) — deve ser menos trabalhoso de modelar uma vez que os dados históricos estejam disponíveis.

## Ver Também

- [[incorporadoras]] — hub do setor de incorporação
- [[cyrela]] — concorrente mais próxima no segmento médio-alto SP
- [[lavvi]] — outra incorporadora de alto padrão em SP (EP da Cyrela)
- [[poc_revenue]] — reconhecimento de receita pelo percentual de obras concluídas
- [[capital_de_giro]] — WC como diferença EBIT→FCO; importante para EzTec dada posição conservadora
- [[velocidade_vendas]] — VSO como métrica de demanda; mais sensível a ciclo de juros no médio-alto
- [[vgv_lancamentos]] — VGV lançado como driver de crescimento do backlog
- [[margem_backlog]] — margem sobre VGV contratado; alta para EzTec por landbank barato
