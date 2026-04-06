---
type: conceito
source_quality: conceptual
aliases: [POC, Percentage of Completion, Reconhecimento por POC, Avanco de Obra]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/TEND3/outputs/model/TEND3_model.json
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/DIRR3/outputs/decomposition/DIRR3_dependency_graph_v3.json
updated: 2026-04-05
---

# POC — Percentage of Completion (Reconhecimento de Receita)

O **POC (Percentage of Completion)** é o método de reconhecimento de receita adotado pelas [[incorporadoras]] brasileiras conforme IFRS 15 / CPC 47. A receita é reconhecida proporcionalmente ao avanço físico da construção — não no ato da venda.

## A Fórmula Central

```
Receita(t) = Backlog_início(t) × POC_sazonal(t)
```

Onde:
- `Backlog_início(t)` = carteira de vendas contratadas a apropriar no início do trimestre
- `POC_sazonal(t)` = percentual do backlog reconhecido como receita no trimestre (varia por trimestre)

O backlog rollforward garante a consistência entre períodos:

```
Backlog_fim(t) = Backlog_início(t) + Vendas_novas(t) − Receita(t)
```

## Por Que Não Existe POC Flat

O POC varia materialmente por trimestre — nunca use "POC anual / 4". A sazonalidade de construção é real e consistente:

| Trimestre | MCMV puro (Cury/PLPL) | Tenda | Direcional | Alta-renda (Cyrela) |
|-----------|----------------------|-------|------------|---------------------|
| 1T | 22–23% | 36–37% | 37–38% | ~25% |
| 2T | 23–24% | 38–39% | 34–35% | ~25% |
| 3T | 21–22% | 40–41% | 34–35% | ~25% |
| 4T | 20–21% | 41–42% | 35–36% | ~25% |

As diferenças refletem o ritmo de entregas (habite-se) de cada empresa e o mix de ciclos de obra em andamento.

## Como Calibrar o POC

O POC sazonal é **calibrado por backtest** em 3 iterações, com meta de MAPE < 8% sobre receita histórica:

```
POC_calibrado(t) = Receita_histórica(t) / Backlog_início(t)
```

Calcula-se por trimestre histórico, obtendo o perfil sazonal (ex: 1T=22%, 2T=23%, 3T=22%, 4T=21% para CURY3 — soma anual ~88%).

**Regra de calibração:** A soma dos 4 POCs trimestrais implica o POC anual, que deve ser consistente com o ciclo de obra da empresa (ex: ciclo 18 meses → ~55% por ano; ciclo 24 meses → ~40% por ano).

## O Lag entre Venda e Receita

```
Lançamento → Venda → Construção (18-36 meses) → Entrega → Repasse banco
     t=0       t=0      t+6 a t+12 trimestres
```

**Implicação para o analista:** VGV lançado alto hoje não gera receita imediata. O backlog absorve as vendas novas e as libera gradualmente via POC ao longo de 1,5 a 3 anos. Isso cria um efeito de "reservatório" — empresas que lançaram muito em 2023-24 reconhecem receita em 2025-26.

## POC vs Regime de Caixa

| Aspecto | POC (IFRS 15) | Caixa |
|---------|--------------|-------|
| Quando reconhece | Conforme avança a obra | Quando recebe o dinheiro |
| Backlog | Sim (carteira a apropriar) | Não |
| Adiantamento de clientes | Quando pagamento > receita reconhecida | N/A |
| Receita financeira do CRM | Separada do POC | Inclui tudo |

**Adiantamento de clientes** (passivo): ocorre quando o comprador paga à vista ou parcelas grandes antes da obra avançar. A empresa recebe o caixa mas ainda não reconhece receita — gera passivo de adiantamento. O modelo captura via "dias adiantamento clientes".

## AVP — Ajuste a Valor Presente

Os recebíveis de longo prazo (parcelas durante a obra) são ajustados a valor presente (AVP). O AVP:
- Reduz a receita líquida reconhecida
- Reduz o recebível registrado no BP
- Cria gap adicional entre [[margem_backlog]] orçada e margem bruta realizada

No modelo, o AVP é tratado como item de verificação (calibrado no backtest), não como driver explícito da projeção — a margem bruta % já incorpora o efeito histórico do AVP.

## Relevância por Empresa

| Empresa | Ciclo de Obra | POC Anual Típico | Particularidade |
|---------|--------------|-----------------|-----------------|
| [[cury]] | ~18-24 meses | ~80% | POC flat-ish; ciclo curto (formas de alumínio) |
| [[plano_plano]] | ~18 meses | ~90% | MCMV puro SP; ciclo muito curto; flat |
| [[direcional]] | ~24-30 meses | ~140% de POC trimestral (~35%/tri) | Alta sazonalidade; Riva acelera entregas |
| [[tenda]] (TENDA) | ~24 meses | ~90-95% | MCMV puro; ciclo médio; parede de concreto |
| [[alea]] (wood frame) | ~20 meses | ~80% | Pré-fabricado; ciclo mais curto que Tenda principal |
| [[cyrela]] | ~30-36 meses | ~100% anual (~25%/tri) | POC relativamente flat; projetos grandes |

## O Backlog como "Reservatório" de Receita

O backlog funciona como um reservatório que acumula vendas e libera receita de forma suavizada ao longo do tempo:

```
BACKLOG (carteira)
     ↑ entra: Vendas novas = VGV × VSO
     ↓ sai: Receita reconhecida = Backlog × POC_sazonal
     ↓ sai eventualmente: Distratos (cancela vendas antes da obra finalizar)
```

**Quando o backlog cresce:** Vendas novas > Receita reconhecida → empresa lançou muito ou o ciclo de construção está no início

**Quando o backlog encolhe:** Vendas novas < Receita reconhecida → empresa está entregando empreendimentos mais antigos sem repor com novos lançamentos

O analista monitora o **saldo de backlog** como indicador de visibilidade de receita futura. Um backlog de R$10bi com POC médio de 25%/tri gera ~R$2,5bi de receita no próximo trimestre — independentemente dos lançamentos que acontecerem.

## Rollforward Completo do Backlog

```
Backlog_fim(t) = Backlog_início(t)
              + Vendas_novas(t)          [VGV vendido no trimestre × % apropriar]
              − Receita_reconhecida(t)   [Backlog_início × POC_sazonal]
              − Distratos(t)             [cancelas de contratos]
              ± Ajustes_INCC(t)          [correção de preço para alto padrão]
```

Para o modelo financeiro simplificado, distratos são incluídos implicitamente no VSO líquido (muitas empresas reportam VSO já líquido de cancelas).

## POC e a DRE: Reconciliação

O reconhecimento via POC cria diferenças entre o resultado econômico e o fluxo de caixa:

| Item | DRE (POC) | Caixa |
|------|-----------|-------|
| Receita | Por avanço físico | Quando recebe (SFH na entrega) |
| Custo | Por avanço físico (matching) | Quando paga fornecedores |
| Resultado Adiantamento Clientes | Passivo: caixa sem receita | Ativo: caixa já recebido |
| Recebíveis POC | Ativo: receita sem caixa | — |

O **Adiantamento de Clientes** é o passivo que aparece quando o comprador paga parcelas grandes na planta antes da construtora reconhecer a receita proporcionalmente. Para empresas com clientes pagando muito "na planta", esse passivo pode ser relevante.

## Particularidades por Empresa

### Cury (CURY3)

A [[cury]] tem ciclo de obra de ~18-20 meses com formas de alumínio. Com POC anual de ~80%, cada real de backlog vira receita em ~15 meses em média. O backlog da Cury gira mais rápido do que o da Cyrela — menor capital de giro relativo e maior previsibilidade de receita.

**Calibração POC Cury:** ~22-24%/tri nos quatro trimestres (relativamente flat — ciclo curto e linear).

### Direcional (DIRR3)

A [[direcional]] tem POC mais alto e mais sazonal (~35-38%/tri). Isso reflete ciclos de obras mais curtos em cidades do interior/norte (onde opera muito), concentração de entregas no 2S, e o modelo construtivo industrializado da Direcional.

### Cyrela (CYRE3)

A [[cyrela]] tem POC relativamente flat (~25%/tri) porque opera com muitos projetos simultaneamente em diferentes fases. O tamanho do portfólio suaviza a sazonalidade individual dos projetos. Para empreendimentos de alto padrão (ciclo 36 meses), cada trimestre representa ~8% do custo total — POC gradual.

## Impacto de Distratos no Modelo

Os distratos reduzem o backlog retroativamente — o contrato é cancelado e o VGV vendido anteriormente sai do backlog. Para incorporadoras que não publicam distratos separadamente, o analista precisa inferir dos dados de backlog:

```
Distratos_implícitos = Backlog_início + Vendas_novas − Backlog_fim − Receita
```

Taxa de distrato histórica normal: 2-5% das vendas brutas. Em crises (2015-16), chegou a 15-20%. Para o modelo atual, distratos não são premissa explícita — estão embutidos na calibração do VSO líquido.

## Ver Também

- [[margem_backlog]] — margem da carteira (leading indicator de margem futura)
- [[vgv_lancamentos]] — volume que alimenta o backlog
- [[velocidade_vendas]] — VSO, converte VGV lançado em vendas novas
- [[incorporadoras]] — hub setorial com contexto contábil completo
- [[incc]] — inflação que corrói margem durante o período POC
- [[capital_de_giro]] — recebíveis e adiantamentos de clientes; derivados do ciclo POC
- [[cury]] — ciclo curto (~18m); POC mais rápido
- [[plano_plano]] — MCMV SP; ciclo ~18m; POC similar ao Cury
- [[tenda]] — MCMV; ciclo ~24m; multi-segmento (TENDA + ALEA)
- [[cyrela]] — ciclo longo (~36m); backlog maior relativo à receita
- [[direcional]] — sazonalidade maior; Riva concentra entregas no 2S
