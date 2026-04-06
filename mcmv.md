---
type: conceito
source_quality: conceptual
aliases: [MCMV, Minha Casa Minha Vida, Programa de Habitação, Casa Verde e Amarela]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/DIRR3/outputs/decomposition/DIRR3_dependency_graph_v3.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
updated: 2026-04-05
---

# MCMV — Minha Casa Minha Vida

O **Minha Casa Minha Vida (MCMV)** é o principal programa federal de habitação popular do Brasil. Subsidia financiamentos imobiliários para famílias de baixa e média renda via FGTS, com taxas abaixo do mercado livre e tetos de preço por faixa de renda. É o principal driver de demanda para as [[incorporadoras]] focadas no segmento econômico.

## Estrutura do Programa (2024-2026)

| Faixa | Renda Familiar | Teto de Preço (2026) | Taxa de Juros |
|-------|---------------|---------------------|---------------|
| Faixa 1 | até R$2.640/mês | R$190-270k (varia por cidade) | 4-5% a.a. (FGTS) |
| Faixa 2 | R$2.641–4.400/mês | R$264-350k | 5-7% a.a. (FGTS) |
| Faixa 3 | R$4.401–8.000/mês | R$350-500k | 7-8,16% a.a. (FGTS) |
| Faixa 4 | R$8.001–12.000/mês | até R$600k (aprovado mar/2026) | SBPE + subsídio parcial |

A Faixa 4 foi aprovada em março de 2026 e amplia o mercado endereçável para incorporadoras que operam no segmento associativo (ex: [[cury]] usa sistema associativo como vantagem competitiva na Faixa 4).

## A Característica Crítica: Sem Correção de Preço

**Em MCMV, o preço de venda é travado no ato da venda (teto da Caixa).** Não há correção pelo [[incc]] durante a construção, ao contrário do alto e médio padrão:

| Segmento | Correção do Preço Durante Obra |
|----------|-------------------------------|
| MCMV Faixas 1-3 | **Não** — preço travado no contrato |
| Econômico/Médio padrão livre | Sim — correção por INCC |
| Alto padrão | Sim — correção por INCC |

**Implicação para a margem:** toda a variação de custo durante a obra (inflação de MDO, materiais, INCC) recai sobre a incorporadora. Sensibilidade histórica: **+3pp de INCC ≈ -1,5 a -2,0pp de margem bruta realizada** para empresas MCMV puras. Isso é capturado no gap [[margem_backlog]] vs realizado.

## Players com Alta Exposição MCMV

| Empresa | % MCMV | Observação |
|---------|--------|------------|
| [[cury]] | ~100% | MCMV puro; formas de alumínio; SP e RJ |
| [[direcional]] | ~60-70% | Faixas 1-3 (DIRR) + Riva (médio-alto, Faixa 3-4) |
| Tenda | ~100% | MCMV + Alea (wood-frame; tecnologia alternativa) |
| MRV | ~70-80% | MCMV + AHS (alto-padrão) + USA (AHS) |
| [[cyrela]] | ~20-25% | Via Vivaz (subsidiária MCMV/econômico) |

## Financiamento: FGTS vs SBPE

O MCMV é financiado majoritariamente pelo **FGTS (Fundo de Garantia)**:
- Taxas subsidiadas pelo governo (independente da [[selic]])
- **Blindagem parcial de demanda:** MCMV é menos sensível a Selic do que o mercado livre, porque as taxas de financiamento não sobem junto com a Selic — são fixadas pelo programa

Isso diferencia o MCMV do crédito SBPE (Sistema Brasileiro de Poupança e Empréstimo), que segue mais de perto as condições de mercado.

## MCMV como Política Pública — Risco Binário

O programa depende de:
1. **Orçamento federal** — cortes de dotação param obras e aprovações de crédito
2. **Regulamentação de tetos de preço** — aumentos de teto ampliam o mercado endereçável
3. **Regras de subsídio** — mudanças nas faixas de renda alteram elegibilidade

Exemplos de eventos binários históricos:
- 2019-2020: Renomeação para "Casa Verde e Amarela" + cortes de orçamento → queda de lançamentos
- 2023: Relançamento MCMV com aumento de tetos e orçamento R$190bi → boom de lançamentos MCMV
- Mar/2026: Aprovação Faixa 4 (teto R$600k) → amplia mercado endereçável da [[cury]] e [[direcional]] Riva

## Impacto de INCC em Modelos MCMV

O INCC é monitorado trimestralmente pelo analista para estimar o gap de margem:

```
Se INCC_real > INCC_orçado:
    Margem_realizada < Margem_backlog por MCMV% × Delta_INCC × fator_sensibilidade
```

Para [[cury]] (100% MCMV), um INCC de 7% quando o modelo esperava 6% pode reduzir a margem bruta em ~1-1,5pp em empreendimentos em construção.

## Vantagem Competitiva: Formas de Alumínio e Associativo

Algumas empresas MCMV têm vantagens estruturais que protegem margens:
- **[[cury]]:** Formas de alumínio → MDO mais eficiente, paredes lisas sem reboco → custo de construção ~10-15% menor
- **[[cury]] sistema associativo Faixa 4:** Permite usar FGTS de trabalhadores para compra coletiva, viabilizando Faixa 4 sem necessidade de financiamento individual SBPE
- **Tenda Alea:** Wood-frame (pré-fabricado) → ciclo de obra mais rápido, menos MDO

## Orçamento MCMV e Prioridade Política

O MCMV é um dos maiores programas de habitação social do mundo, e sua continuidade é garantida por forte respaldo político bipartidário no Brasil:

- **Governo Lula (2023-):** Relançamento com orçamento de R$190bi para 4 anos; meta 2M de unidades
- **Programa anterior (Bolsonaro):** Renomeado para "Casa Verde e Amarela" com cortes relevantes
- **Histórico Dilma (2009-2016):** Criação do MCMV original; pico de unidades contratadas

**Risco político real:** Corte de orçamento pode acontecer em qualquer governo se o déficit fiscal apertar. O risco não é de extinção do programa, mas de redução de dotação que afeta o fluxo de aprovação de crédito pela CEF.

## Financiamento via CEF: Papel Central

A Caixa Econômica Federal (CEF) é o agente operador do MCMV — toda a operação passa pela CEF:

1. **Aprovação do empreendimento**: A CEF avalia o projeto antes do lançamento (engenharia, regularidade, viabilidade)
2. **Financiamento da obra**: CEF financia parte da construção via repasse de FGTS (agente executor)
3. **Financiamento ao comprador**: CEF concede crédito habitacional ao mutuário final
4. **Medição e repasse**: O dinheiro para a incorporadora é liberado por medição de obra — quanto mais a obra avança, mais a CEF repassa

**Implicação para o capital de giro:** A Cury e outras MCMV puras recebem os recursos da CEF ao longo da obra (diferente do alto padrão onde o comprador paga na entrega). Isso reduz o [[capital_de_giro]] relativo das empresas MCMV — o ciclo de caixa é mais curto.

## FGTS: A Fonte de Funding

O FGTS (Fundo de Garantia por Tempo de Serviço) é a fonte de recursos para os subsídios e o crédito habitacional do MCMV:

- Empresas depositam 8% da folha de pagamento mensal no FGTS de cada trabalhador
- O FGTS é gerido pela CEF e aplicado majoritariamente em habitação e saneamento
- As taxas de juros subsidiadas (4-8%) são financiadas pelo rendimento do FGTS (que rende TR + 3%, inferior às taxas de mercado)

**Sustentabilidade:** O modelo de subsídio via FGTS tem debate técnico sobre sua sustentabilidade — a diferença entre o custo de captação do FGTS e a taxa cobrada do mutuário é subsidiada implicitamente. O BCB monitora.

## Impacto de Mudança de Tetos de Preço

Quando o governo eleva os tetos de preço das faixas MCMV, os efeitos são imediatos:

1. **Amplia mercado endereçável**: Mais famílias se enquadram na faixa → mais demanda potencial
2. **Permite empreendimentos em praças mais caras**: SP e RJ têm terrenos caros; teto baixo limitava viabilidade
3. **Melhora margem dos projetos mais antigos**: Empreendimentos ainda não lançados ganham mais headroom de preço vs custo
4. **Sinaliza prioridade política**: Eleva o confidence level de que o programa continuará

**Mar/2026 — Faixa 4:** Aprovação com teto R$600k é o evento mais recente e representa ~30-40% de ampliação do mercado para empresas que operam no segmento econômico-médio (como a [[cury]] via sistema associativo e a [[direcional]] via Riva).

## Ciclo MCMV: Como Modela o Crescimento de Receita

O crescimento de receita das empresas MCMV segue um ciclo relativamente previsível:

```
Ano 0: Governo expande tetos + orçamento
Ano 0-1: Aprovação de novos empreendimentos + compra de terrenos (landbank)
Ano 1-2: Lançamentos acelerados → VGV sobe → backlog cresce
Ano 2-3: Construção em andamento → POC reconhece receita → receita sobe
Ano 3-4: Pico de entregas → habite-se → transferência CEF → caixa recebido
```

Isso explica por que as empresas MCMV reagiram fortemente ao relançamento do programa em 2023: o VGV lançado acelerou em 2023-24, e a receita está sendo reconhecida em 2025-26.

## Regulação de Margens: O Teto CEF

A CEF tem uma planilha de "custo máximo de construção" (CUB — Custo Unitário Básico + sobretaxas) que limita o custo que a empresa pode apresentar para fins de financiamento. Isso funciona como controle indireto de margem mínima:

- Projeto viável = (Teto de preço da faixa) − (CUB CEF × m²) > Custo real de terreno + lucro mínimo
- Se terrenos sobem muito, novos projetos deixam de ser viáveis no MCMV

Esse é o mecanismo pelo qual a inflação de terrenos (especialmente em SP) comprime o mercado MCMV e aumenta a concentração em empresas com landbank antigo (já comprado a preços mais baixos).

## Ver Também

- [[incc]] — inflação da construção civil que corrói margem MCMV; risco central
- [[incorporadoras]] — hub setorial
- [[margem_backlog]] — gap backlog vs realizado maior em MCMV
- [[vgv_lancamentos]] — teto MCMV define viabilidade de empreendimentos
- [[velocidade_vendas]] — demanda MCMV estruturalmente mais forte e menos cíclica
- [[cury]] — referência de MCMV puro; maior eficiência operacional
- [[direcional]] — MCMV econômico + médio-alto via Riva
- [[tenda]] — MCMV + Alea (wood-frame)
- [[capital_de_giro]] — MCMV tem WC menor por estrutura de repasse CEF
- [[selic]] — taxas MCMV são via FGTS (blindadas da Selic de mercado)
