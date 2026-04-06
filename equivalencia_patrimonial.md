---
type: conceito
source_quality: conceptual
aliases: [Equivalência Patrimonial, EP, Equity Method, Método de Equivalência Patrimonial, equity_pickup]
sources:
  - sectors/banking/sector_profile.md
  - wiki/porto_seguro.md
  - wiki/resultado_seguros.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CYRE3/outputs/model/CYRE3_model.json
updated: 2026-04-05
---

# Equivalência Patrimonial

A **Equivalência Patrimonial (EP)** é o método contábil pelo qual um investidor reconhece sua participação proporcional no resultado de outra empresa onde exerce influência significativa — mas não controle. No Brasil, é regulada pelo **CPC 18** (equivalente ao IAS 28 do IFRS). Para o [[itau|ITUB4]], a EP da [[porto_seguro|Porto Seguro]] (~46%) é um item material da DRE — contribuiu ~R$3,0B em 2025 (+130% YoY) — e sua posição abaixo do resultado operacional tem implicações diretas para o cálculo do [[eficiencia_operacional|Índice de Eficiência]] e para comparações de NIM entre bancos.

## Definição — Quando Usar EP vs Consolidação Integral

O método de EP se aplica quando o investidor tem **influência significativa** sem ter **controle** sobre o investido.

| Situação | Tratamento Contábil | Norma |
|----------|--------------------|----|
| Controle (>50% de votos ou poder de direcionar políticas) | Consolidação integral (IFRS 10) | CPC 36 / IFRS 10 |
| Influência significativa sem controle (tipicamente 20-50%) | Equivalência Patrimonial | CPC 18 / IAS 28 |
| Participação minoritária sem influência (<20% em geral) | Valor justo via resultado ou OCI | CPC 38 / IFRS 9 |

**Presunção de influência significativa**: participação ≥ 20% presume influência significativa (presunção ilidível). Abaixo de 20%, presume-se ausência — mas outros fatores como representação no conselho, transações relevantes ou fornecimento de informações técnicas podem qualificar a participação para EP mesmo abaixo desse limiar.

**Presunção de controle**: participação >50% de votos geralmente implica controle. Porém o IFRS 10 exige análise substancial — pode haver controle com menos de 50% (via acordos de acionistas, direitos de veto substantivos, poder de fato) ou ausência de controle com mais de 50% (ex: participação fragmentada em entidade estruturada).

```
Regra prática:
  < 20%  → Instrumento financeiro (IFRS 9)
  20-50% → Equivalência Patrimonial (IAS 28)   ← zona do EP
  > 50%  → Consolidação integral (IFRS 10)
  (com exceções em ambos os sentidos)
```

## Mecânica Contábil

### Na DRE

O investidor reconhece como receita (ou despesa) a sua **participação % no lucro líquido (ou prejuízo)** do investido no período:

```
EP_DRE = Lucro_Líquido_Investido × % Participação
```

Se Porto Seguro apura LL de R$6,5B no ano e o Itaú detém 46%:

```
EP_Itaú = R$6,5B × 46% ≈ R$3,0B
```

Esse valor entra na DRE do Itaú como linha dedicada, **abaixo do resultado operacional** — geralmente denominada "Resultado de participações em coligadas e joint ventures" ou equivalente.

### No Balanço Patrimonial

O valor contábil do investimento é ajustado continuamente:

```
Investimento(t) = Investimento(t-1)
                + EP_reconhecida_no_período       (+)
                − Dividendos_recebidos_do_investido (−)
                ± Outros resultados abrangentes (OCI) do investido (±)
```

O investimento nunca fica negativo (exceto se houver obrigação de cobrir prejuízos do investido além do valor do investimento — situação rara, exige garantias formais).

**Goodwill no EP**: ao adquirir a participação acima do valor patrimonial, o excesso é incorporado ao valor contábil do investimento (não segregado como goodwill separado, ao contrário da consolidação integral). Esse goodwill embutido não é amortizado, mas é testado por impairment.

### Exemplo Numérico (ITUB4 × Porto Seguro, estimativa 2025)

| Item | Valor (R$ B) |
|------|-------------|
| LL Porto Seguro (ano) | ~6,5 |
| Participação Itaú | 46% |
| EP reconhecida na DRE Itaú | ~3,0 |
| Dividendos recebidos da Porto Seguro (estimado) | ~1,5–2,0 |
| Ajuste líquido no balanço Itaú (EP − Dividendos) | ~1,0–1,5 |

O saldo do investimento em Porto Seguro no balanço do Itaú cresce ~R$1–1,5B por ano (EP acumulada menos dividendos distribuídos).

## Por Que Porto Seguro Não É Consolidada

O critério não é participação percentual, mas **controle**. Apesar de 46% ser uma fatia expressiva, o Itaú **não tem controle** sobre a Porto Seguro pelos seguintes motivos:

- **Família Garfinkel** detém ~54% do capital votante — maioria absoluta
- O Conselho de Administração não tem maioria de conselheiros indicados pelo Itaú
- Decisões estratégicas (pricing, expansão de ramos, M&A) são prerrogativa dos controladores
- O Itaú não pode direcionar as políticas financeiras e operacionais da Porto Seguro

Portanto, o relacionamento se enquadra em **influência significativa** (IAS 28), não controle (IFRS 10). O equity method é o tratamento correto.

**Implicação contábil**: as receitas e despesas da Porto Seguro **não aparecem linha a linha** na DRE consolidada do Itaú. Apenas o resultado líquido proporcional (a EP) aparece — como um único número.

## Impacto no IE do ITUB4

Esta é a consequência mais importante para análise do [[itau|ITUB4]].

### EP Fora do Cálculo do IE

O [[eficiencia_operacional|Índice de Eficiência]] é calculado como:

```
IE = DNDJ / Receita_Total
   = Despesas_Operacionais / (NII + Fees + Seguros_consolidados)
```

A EP entra **abaixo do resultado operacional** na DRE — portanto:

- **Não entra no denominador** (receita total do IE)
- **Não entra no numerador** (as despesas operacionais da Porto Seguro não aparecem no DNDJ do Itaú)

O IE do Itaú é calculado **sem** Porto Seguro, usando apenas NII + Fees no denominador:

```
IE_Itaú = DNDJ_Itaú / (NII_Itaú + Fees_Itaú)
        ≈ R$67B / R$172B
        ≈ 38,9% (2025E)
```

### Problema de Comparabilidade com Bradesco

O [[bradesco]] consolida integralmente a Bradesco Seguros (controle >50%). Portanto, o IE do Bradesco inclui o resultado de seguros no denominador — denominador maior → IE menor (aparentemente melhor).

Para comparar os dois bancos em base equivalente, o analista deve **ajustar o IE do Itaú** somando o EP da Porto Seguro ao denominador:

```
IE_Itaú_ajustado = DNDJ_Itaú / (NII_Itaú + Fees_Itaú + EP_Porto_Seguro)
                 ≈ R$67B / (R$172B + R$3B)
                 ≈ R$67B / R$175B
                 ≈ ~38,3%   (efeito pequeno, mas metodologicamente correto)
```

Na prática, o ajuste é modesto (~60bps neste exemplo) porque o EP é grande em valor absoluto mas ainda é uma fração menor do denominador total. O ponto metodológico — comparar bancos em base homogênea — é mais importante do que a magnitude.

**Regra prática**: ao comparar IE entre bancos com e sem seguros consolidados, sempre normalizar o denominador para incluir o resultado de seguros (seja consolidado ou EP) de todos os bancos.

### Posição na DRE (Sequência de Linhas)

```
Resultado Operacional (EBIT bancário)
  + NII (NII Clientes + NII Mercado)
  + Receita de Serviços e Tarifas
  − Custo do Crédito (Provisões líquidas + inadimplências)
  − DNDJ (Despesas de Pessoal + Administrativas)
  = Resultado antes de EP e IR
  + Equivalência Patrimonial (Porto Seguro + outras)   ← aqui
  = Resultado antes de IR
  − IR/CSLL
  = Lucro Líquido
```

EP está **abaixo** do ponto de corte onde o IE é calculado. O IE é uma métrica de eficiência operacional; a EP é um resultado de participação — não operacional.

## EP vs Caixa — Accrual vs Realização

A EP é receita **accrual**: o banco reconhece o lucro contabilmente no período em que o investido o apura, independente de receber caixa.

```
EP reconhecida ≠ Caixa recebido

Caixa entra apenas quando o investido distribui dividendos:
  Caixa_recebido = Dividendos_declarados × % Participação
```

**Para o [[itau|ITUB4]] × Porto Seguro (estimativa 2025)**:

| Item | Valor estimado |
|------|----------------|
| EP reconhecida na DRE | ~R$3,0B |
| Dividendos declarados pela Porto Seguro | ~R$3,3B (payout ~90%) |
| Dividendos recebidos pelo Itaú (46%) | ~R$1,5B |
| Diferença EP vs Caixa | EP > Caixa em ~R$1,5B |

**Implicação para análise de caixa**: o LL contábil do Itaú inclui EP que não é caixa naquele período. No fluxo de caixa, a EP aparece como **subtração no FCO** (para eliminar o lucro não caixa), e os dividendos recebidos aparecem como **adição**. A diferença líquida pode ser positiva ou negativa dependendo do payout do investido.

**Por que Porto Seguro tem payout alto**: empresas de seguro com resultado financeiro de reservas elevado tendem a distribuir generosamente — as reservas técnicas são o "capital produtivo" do negócio, não o lucro retido. A Porto Seguro historicamente distribui 80-100% do LL em dividendos/JCP.

**Implicação para o ROE do Itaú**: a EP contabilizada eleva o LL sem exigir capital adicional proporcional (o investimento no balanço cresce, mas menos que a EP reconhecida, já que os dividendos reduzem o saldo). Isso cria um efeito de **alavancagem de capital** — a Porto Seguro "empurra" lucro para o Itaú com baixo consumo incremental de capital regulatório.

## Outros Investimentos EP no ITUB4

Além da [[porto_seguro|Porto Seguro]], o Itaú mantém outras participações contabilizadas por equivalência patrimonial. São menores em magnitude mas compõem o saldo total de EP na DRE:

| Investimento (estimado) | Participação | Setor | Magnitude EP |
|------------------------|-------------|-------|-------------|
| Porto Seguro (PSSA3) | ~46% | Seguros | ~R$3,0B/ano — dominante |
| IRB Brasil RE | Participação histórica | Resseguros | Imaterial (IRB em dificuldades) |
| Rede/Cielo (indireto) | Participações menores | Meios de pagamento | Imaterial após desinvestimentos |
| Outras coligadas | Diversas | Fintechs, clearing | Individualmente imateriais |

O EP total na DRE do Itaú é dominado pela Porto Seguro. As demais participações são residuais para fins de modelagem — usar o EP da Porto Seguro como proxy do EP total, com margem de 5-10% para as demais.

**Como monitorar**: o release de resultados do Itaú discrimina o EP por investida no Anexo de Demonstrações Contábeis (nota de investimentos em coligadas e JV). Nos trimestres com variações anômalas de EP, verificar se há efeito one-off em participações menores.

## Sensibilidade EP a Resultados da Porto Seguro

Como a EP do Itaú é diretamente proporcional ao LL da Porto Seguro:

```
ΔEP_Itaú = ΔLL_Porto_Seguro × 46%
```

**Drivers de variação do LL da Porto Seguro** (e consequentemente do EP do Itaú):

| Driver | Direção | Magnitude |
|--------|---------|-----------|
| Selic +100bps | EP sobe | ~R$150–180M/ano (estimado) |
| Sinistralidade auto +5pp | EP cai | ~R$200–300M/ano (estimado) |
| Crescimento de prêmios +10% | EP sobe | ~R$150–200M/ano (estimado) |
| Evento climático extremo (chuvas, seca) | EP cai | Variável, pode ser material em 1T |

A [[selic]] alta é um **amplificador de EP** para o Itaú — maior retorno das reservas técnicas da Porto Seguro → maior LL Porto Seguro → maior EP Itaú. Esse efeito corre em sentido oposto ao NII_Mercado do banco próprio (que tem sensibilidade negativa a Selic por duration do portfólio de TVM).

## Por Empresa

| Empresa | Tratamento de Seguros | Impacto no IE |
|---------|----------------------|--------------|
| [[itau]] | Porto Seguro (~46%) via EP. ~R$3,0B de EP em 2025. IE calculado sem seguros no denominador (NII + Fees apenas). IE ajustado ~38,3% vs IE reportado ~38,9%. |
| [[bradesco]] | Bradesco Seguros consolidada integralmente (controle >50%). Resultado de seguros entra no denominador do IE. Comparação direta com Itaú exige normalização. |
| Banco do Brasil (BBAS3) | BB Seguridade (BBSE3) via EP (~66% indiretamente, mas BB Seguridade é listada como subsidiária não consolidada). EP material — BB Seguridade lucra ~R$5-6B/ano; contribuição para o LL do BB é expressiva. |
| Santander BR | Mapfre via JV (~50%). Contabilizado como EP. Menor magnitude que Porto Seguro para Itaú. |

## Ver Também

- [[porto_seguro]] — principal investida EP do ITUB4; mecânica detalhada da JV e drivers do resultado
- [[resultado_seguros]] — como o resultado de seguros aparece na DRE (consolidado vs EP)
- [[eficiencia_operacional]] — IE do Itaú calculado sem Porto Seguro no denominador; ajuste para comparação com Bradesco
- [[nim]] — EP não entra no NIM; comparação de NIM entre bancos com e sem seguros consolidados
- [[banking]] — contexto setorial e estrutura da DRE bancária
- [[itau]] — perfil completo ITUB4 com premissas do modelo
