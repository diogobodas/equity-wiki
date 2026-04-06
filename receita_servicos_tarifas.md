---
type: conceito
aliases: [Receita de Serviços e Tarifas, Fee Income, Receita de Serviços, Tarifas Bancárias]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/filings/releases/ITUB4_release_2025.pdf
source_quality: verified
updated: 2026-04-05
learning_loop_notes:
  - "h_002 ACCEPT 2026-04-03: ITUB4 fees growth 7%→4% | MAPE holdout -53.5%"
  - "2026-04-03: dados reais de breakdown de serviços incorporados do Release 4T25 p.17"
---

# Receita de Serviços e Tarifas

A **receita de serviços e tarifas** (ou fee income) é o conjunto de receitas bancárias que não derivam de intermediação financeira (juros). Inclui tarifas de conta, administração de fundos, cartões, corretagem, assessoria, consórcio, câmbio e outros. É a linha de receita mais estável do banco — menos sensível a [[selic]] e a ciclos de crédito — e é componente importante do [[alavancagem_operacional|efeito de alavancagem operacional]] porque escala com pouco custo incremental.

## Como Funciona

Os principais subcomponentes:

| Linha | Drivers | Sensibilidade |
|-------|---------|---------------|
| Cartões (intercâmbio + anuidades) | Volume de consumo, base de cartões | Ciclo econômico |
| Gestão de recursos (fundos) | AuM, taxa de administração | [[selic]] (atrai/repele renda fixa) |
| Administração de contas (tarifas) | Base de clientes ativos | Estável |
| Operações de crédito (IOF, TAC) | Volume de concessões | [[crescimento_carteira]] |
| Consórcio | Carteira de consorciados × taxa admin | Imóvel/auto demanda |
| Corretagem e advisory (Wealth) | Número de clientes, AuM | Mercado de capitais |
| Câmbio e comércio exterior | Volume de operações | PIB + exportações |

### Modelagem

```
Receita_Servicos(t) = Receita_Servicos(t-4) × (1 + g_fee_yoy)
```

`g_fee_yoy` tipicamente 5-8% para bancos grandes brasileiros — crescimento real acima do PIB por conta de expansão de base de clientes e mix shift para wealth management. **Para ITUB4 especificamente**, o YoY observado (2T24-4T25) ficou na média de 2.3%, significativamente abaixo do guidance combinado. O aprendizado do model-learning-loop (h_002) calibrou a premissa para 4.0% — entre a média histórica (2.3%) e o guidance combinado (5-9%).

## No Contexto Brasileiro

- **Regulação de tarifas**: BCB limita certas tarifas (pacote de serviços, transferências). Bancos migraram para modelo "conta digital gratuita + serviços premium", reduzindo tarifa por transação mas aumentando cross-sell.
- **Wealth management**: o grande driver de crescimento de fee income nos últimos 5 anos. AuM da indústria de fundos > R$9T. Grandes bancos capturam via plataformas abertas (XP-like internas).
- **Intercâmbio de cartões**: pressionado pelo Pix (substitui pagamentos de débito/crédito em pequenas transações). Impacto parcialmente compensado pelo crescimento de cartões de crédito nas classes B/C.
- **Consórcio**: produto crescendo acima do setor — imóvel + auto. Banco não corre risco de crédito, apenas cobra taxa de administração (~1,5% a.a. do bem).

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | Fee income R$12.560M/tri em 4T25 (anual **R$46.891M**). Com seguros: R$15.594M/tri (R$58.305M/ano). YoY 2025 vs 2024: +3,9% serviços puros, +6,3% serviços+seguros. Guidance 2026 combinado (serviços + seguros ajustado): +5-9%. Fees puro estimado em ~4% (model-learning-loop h_002). Principais drivers 2025: wealth +14,2%, pagamentos +6,7%, cartões +5,1%, consórcios +30,5%. Conta corrente PF -16,8% — queda estrutural em tarifas básicas. Fonte: Release 4T25, p.17. |
| [[bradesco]] | Em recomposição. Receita de serviços pressionada durante reestruturação. Banco Bocom BBM (atacado) contribui com advisory. |

## Decomposição por Sub-componente: ITUB4 2025

Dados reais extraídos do Release 4T25 ITUB4, tabela "Serviços e Seguros" (p.17). Fonte: verified.

| Linha | 4T25 (R$M) | 3T25 | 4T24 | 2025 (R$M) | 2024 | YoY |
|-------|-----------|------|------|-----------|------|-----|
| **Cartões Emissor** | 3.503 | 3.344 | 3.332 | 13.382 | 12.731 | +5,1% |
| **Pagamentos e Recebimentos** | 2.635 | 2.502 | 2.428 | 9.897 | 9.275 | +6,7% |
| **Administração de Recursos** | 2.146 | 1.879 | 1.826 | 7.616 | 6.666 | +14,2% |
| — Adm. de Fundos | 1.611 | 1.391 | 1.404 | 5.700 | 5.198 | +9,7% |
| — Adm. de Consórcios | 535 | 488 | 422 | 1.916 | 1.468 | +30,5% |
| **Assessoria Econ./Fin. e Corretagem** | 1.437 | 1.227 | 1.125 | 4.635 | 4.870 | -4,8% |
| **Conta Corrente PF** | 689 | 710 | 859 | 2.993 | 3.597 | -16,8% |
| **Operações de Crédito e Garantias** | 625 | 626 | 757 | 2.508 | 2.823 | -11,2% |
| **Outros Brasil** | 472 | 480 | 399 | 1.797 | 1.506 | +19,4% |
| **América Latina (ex-Brasil)** | 1.053 | 987 | 971 | 4.065 | 3.641 | +11,6% |
| **Receitas de Prestação de Serviços** | **12.560** | 11.755 | 11.697 | **46.891** | 45.110 | +3,9% |
| **Resultado de Seguros¹** | 3.034 | 2.977 | 2.599 | 11.414 | 9.755 | +17,0% |
| **Serviços + Seguros (Total)** | **15.594** | 14.732 | 14.296 | **58.305** | 54.866 | +6,3% |

¹ Seguros, Previdência e Capitalização líquidos de despesas com sinistros e comercialização.

> **Nota metodológica**: a partir de 1T25, receitas de adquirência, tarifas PJ de conta e PIX foram reclassificadas para "Pagamentos e Recebimentos" — os períodos anteriores foram ajustados para comparabilidade.

### Composição das Receitas de Serviços (2025)

| Linha | R$M/ano | % do Total Serviços |
|-------|---------|---------------------|
| Cartões Emissor | 13.382 | 28,5% |
| Pagamentos e Recebimentos | 9.897 | 21,1% |
| Administração de Recursos | 7.616 | 16,2% |
| América Latina | 4.065 | 8,7% |
| Assessoria e Corretagem | 4.635 | 9,9% |
| Conta Corrente PF | 2.993 | 6,4% |
| Operações de Crédito | 2.508 | 5,3% |
| Outros | 1.797 | 3,8% |

**Insight**: Cartões + Pagamentos = 50% das receitas de serviços. Administração de Recursos é o segmento de maior crescimento YoY (+14,2% vs 2024), puxado por consórcios (+30,5%). Assessoria e Corretagem caiu -4,8% YoY — mercado de capitais menos ativo em 2025 com Selic alta.

## Wealth Management — Principal Driver de Crescimento

Wealth management é a linha de fee income com maior potencial de crescimento secular para [[itau]] e para o setor bancário brasileiro como um todo.

**Captação e AuM em 2025:**
- Captação líquida de ~R$156B em 2025 — recorde histórico para o Itaú
- AuM total estimado em ~R$1.2–1.3T (crescendo; base exata não divulgada de forma isolada)
- O Itaú opera três camadas: plataforma aberta **íon** (varejo alta renda), **Itaú Private** (Personnalité acima de R$3M), e **Itaú Asset Management** (fundos institucionais)

**Mecânica de fee de gestão:**
- Taxa de administração média estimada: ~0.5–1.0% a.a. dependendo do mix de fundo
- Fundos de renda fixa simples: ~0.2–0.5% a.a. → fee baixo
- Multimercado e equity: ~1.0–2.0% a.a. → fee alto
- Mix shift para multimercado/equity é multiplicador de fee income mesmo sem captação adicional
- Estimativa de impacto: R$156B de captação × ~0.75% médio = ~R$1.2B incremental de fees de gestão por ano — crescimento gradual à medida que os recursos são alocados

**Dinâmica competitiva:**
- Itaú vs [[xp_investimentos|XP]]: concorrência intensa em alta renda (segmento R$300k–R$3M)
- Itaú tem custo de distribuição menor — rede e base de clientes já amortizados
- XP tem modelo de assessor independente mais agressivo em captação
- Tendência: plataformas abertas dentro dos bancões (íon) tentam replicar a proposta de valor da XP sem migrar o cliente

**Por que wealth fee cresce acima do PIB:**
- Expansão de base: classe média alta brasileira em ascensão → mais pessoas elegíveis para produtos wealth
- Migração de produto: renda fixa simples → multimercado → equity → maior taxa de administração
- Sofisticação: advisory e gestão discricionária têm fee maior que fundos passivos

## PIX e o Impacto no Intercâmbio de Cartões

O intercâmbio de cartões foi historicamente a maior linha de fee income dos bancos emissores. O PIX mudou essa dinâmica estruturalmente.

**O que é intercâmbio:**
- Fee pago pelo banco do estabelecimento (banco adquirente) ao banco emissor em cada transação de cartão
- Percentual varia: ~0.5% (débito) a ~1.5–2.0% (crédito parcelado)
- Para o banco emissor, é receita pura de volume — não depende do crédito do cliente

**Mecanismo de substituição pelo PIX:**
- PIX substitui transações de débito e crédito parcelado em valores pequenos (ticket < ~R$200)
- Custo zero para o consumidor e para o estabelecimento → adoção rápida
- Estimativa de impacto: PIX "roubou" ~15–20% das transações de débito entre 2022 e 2024
- Crédito parcelado resistiu melhor — PIX parcelado (BNPL) ainda em estágio inicial

**Compensações parciais:**
- Crescimento de cartão de crédito nas classes B/C — segmento que antes usava débito/dinheiro
- Cartões premium com anuidade alta (Personnalité, Ultrablack) — fee de anuidade substitui parte do intercâmbio perdido
- Parcelado sem juros continua dominante no Brasil — não substituível por PIX simples no curto prazo

**Net para [[itau]]:**
- Intercâmbio crescendo ~2–3% a.a. (vs ~8–10% historicamente pré-PIX)
- Itaú compensa via anuidades premium e crescimento de base — linha de cartões segue crescendo, mas a ritmo mais lento
- Risco futuro: PIX garantia (BNPL nativo) pode pressionar o crédito parcelado — ainda sem data definida pelo BCB

## Por Que Fees Crescem Abaixo do NII

Insight estrutural relevante para modelagem e para entender o gap entre guidance combinado (serviços + seguros) e fees puro.

**Teto regulatório:**
- BCB limita tarifas básicas via Res. CMN 3.919/2010 e atualizações (tarifas padronizadas: TEV, TED, DOC, extratos)
- Pacote "essencial" gratuito obrigatório para pessoas físicas — bancos não podem cobrar por transações básicas
- Crescimento de tarifas de conta esbarrou nesse teto desde ~2017

**Pressão competitiva digital:**
- Fintechs ([[nubank|Nubank]], C6 Bank, Inter) zeraram a tarifa de conta corrente para ganhar base
- Forçou bancões a remover tarifas básicas (manutenção de conta, extratos, transferências) para não perder clientes digitais
- Resultado: receita por cliente de conta caiu; bancos compensaram via cross-sell e mix shift para produtos premium

**Onde o crescimento real vem:**
- Produtos premium de wealth management (fee de gestão, advisory, custódia)
- Volume de cartões de crédito nas classes B/C (crescimento de base)
- Consórcio (produto sem teto regulatório explícito, crescendo em imóvel e auto)
- Não mais de tarifas transacionais básicas

**Implicação para o modelo:**
- Fee income cresce ~4–6% a.a. — em linha com inflação (~4%) + crescimento real de 1–2%
- NII × carteira pode crescer 10–15% com [[selic]] alta e expansão de carteira de crédito
- Isso explica por que [[nii_clientes|NII de clientes]] é o principal alavancador do resultado — fees são estabilizadores, não aceleradores
- Para calibrar premissa de fee growth: guidance combinado (serviços + seguros) tende a superestimar fees puro, pois seguros cresce mais rápido (ver [[resultado_seguros]])

## Ver Também

- [[resultado_seguros]] — outra linha de receita não-NII, complementar ao fee income
- [[alavancagem_operacional]] — fee income escala bem → contribui para alavancagem
- [[eficiencia_operacional]] — ambos fee income e resultado de seguros entram no denominador do IE
- [[nii_clientes]] — NII é a maior linha, fee income é o diversificador
- [[selic]] — taxas altas podem reduzir volume de cartões (crédito mais caro), mas aumentam rendimento em fundos
- [[banking]] — contexto setorial e estrutura da DRE
