---
type: conceito
aliases: [Sensíveis a Spread, NII Sensíveis, Operações Sensíveis a Spread, Margem Sensível]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/filings/releases/ITUB4_release_2025.pdf
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
note: "2026-04-03: estimativas ITUB4 substituídas por dados reais do release 4T25 (saldo R$1.279T, NIM 8.6%, NII R$26.955B/trim)"
---

# NII — Operações Sensíveis a Spread

As **operações sensíveis a spread** são o sub-componente do [[nii_clientes]] onde o banco ativamente gerencia o spread cobrado ao tomador acima de uma taxa de referência (CDI, Selic, IPCA). É o componente "gerenciável" do NII Clientes — diferente da [[remuneracao_capital_giro]], que cresce automaticamente com a Selic.

## Decomposição

```
NII_Sensíveis = Carteira_Sensível_Média × Spread_Acima_Benchmark / 100 / 4
```

Onde `Spread_Acima_Benchmark` é a margem que o banco cobra além da taxa de referência do mercado.

### Composição Típica da Carteira Sensível

| Produto | Benchmark | Spread típico | Driver |
|---------|-----------|---------------|--------|
| Capital de giro PJ | CDI | CDI + 2-4% a.a. | Ciclo econômico, covenant |
| Crédito pessoal PF | CDI | CDI + 20-40% a.a. | Risco de crédito, canal |
| Cartão de crédito rotativo | Selic | Selic + 100-150% a.a. | Inadimplência esperada |
| Consignado CLT | Taxa fixa | ~1.8-2.8% a.m. | Regulação INSS/CLT |
| Crédito imobiliário | IPCA | IPCA + 4-8% a.a. | Garantia real, prazo |
| Grandes empresas / Atacado | CDI | CDI + 0.5-2% a.a. | Rating, relacionamento |

## Drivers de Variação

**Volume**: [[crescimento_carteira]] — aceleração ou desaceleração das concessões.

**Spread**: Depende de:
1. **Mix shift** — migração para produtos de maior spread (ex: cartão → consignado = reduz NII mas melhora risco-retorno)
2. **Ciclo de crédito** — recessão contrai spreads (bancos ficam mais seletivos E tomadores migram para colaterizados)
3. **Selic indireta** — Selic alta → custo de funding sobe → passa parte para o tomador, mas passivo reprecia mais rápido que ativo
4. **Concorrência** — fintechs pressionam spread em segmentos de menor risco (consignado digital, crédito imobiliário)

## Sensibilidade à Selic

Ao contrário da [[remuneracao_capital_giro]], a relação com Selic é **não-linear**:
- Selic alta → taxas de concessão sobem → NII_Sensíveis aumenta no curto prazo
- Selic alta por tempo longo → demanda de crédito cai → carteira desacelera → NII_Sensíveis desacelera
- O NIM do componente sensível pode ficar estável (spread acima do CDI não muda) mesmo com Selic variando

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | Mix: ~40% pessoas físicas (consignado, imobiliário, cartão), ~40% PJ (atacado, PMEs), ~15% LatAm, ~5% outros. Consignado privado CLT acelerando (R$1.9B/mês jan/26). NIM_Sensíveis **8.6%** (4T25, divulgado) — abaixo das estimativas anteriores de ~9.4%. NIM total MFC ~8.9% (taxa sobre saldo total incluindo capital de giro). |
| [[bradesco]] | Mix historicamente mais concentrado em cartão/pessoal. Pós-crise 2022: migração para menor risco. NIM em recuperação. |

## Modelagem Aplicada (patch nii_decomposicao, 2026-04-03)

**Anterior** (`in:nim` único):
```
der:nii_clientes = der:carteira_media × in:nim / 100 / 4
```

**Atual** (patch aplicado ao grafo ITUB4 com dados verificados do release):
```
der:nii_sensiveis    = der:carteira_media × in:spread_sensiveis / 100 / 4
der:base_capital_giro = lag(rw:pl_total) × in:cg_ratio
der:nii_capital_giro  = der:base_capital_giro × in:cdi / 100 / 4
der:nii_clientes      = der:nii_sensiveis + der:nii_capital_giro
```

**Parâmetros calibrados (4T25):**

| Parâmetro | Valor modelo | Valor release (p.12) | Diferença |
|-----------|-------------|----------------------|-----------|
| `in:spread_sensiveis` | **10.24%** | 8.6% | Base diferente: modelo usa carteira Brasil ~R$1.053T; release usa R$1.279T (inclui LatAm + estruturadas) |
| `in:cg_ratio` | **0.745** | — | 146,248 / 196,146 (capital alocado às áreas / PL total) |
| `in:cdi` | **14.15%** | — | CDI projetado 2026 (= Selic 14.25% − 0.10pp) |

**Por que `spread_sensiveis = 10.24%` e não 8.6% do release:**
O release aplica a taxa sobre R$1.279T (base "sensível" que inclui LatAm, operações estruturadas de atacado, adquirência). O modelo usa a carteira de crédito Brasil (~R$1.053T). Para produzir o mesmo NII_sensíveis (R$26,955M/tri verificado), o spread implícito é 26,955 / 1,053,074 × 400 = **10.24%**.

**Impacto no modelo 2026E:** LL subiu de R$52,1B (single-NIM) para R$53,5B. A diferença de +R$1,3B reflete que o CDI subiu de ~10,3% (média 4T25) para 14,15% (2026), beneficiando NII_CG: +R$1,2B/quarter (+R$5,5B/ano).

## ITUB4: Carteira Sensível e NIM_Sensíveis (dados reais do release)

Os dados abaixo são extraídos diretamente da tabela "Taxas Médias anualizadas da Margem Financeira com Clientes" do Release 4T25 (página 12). Fonte: Release 4T25 ITUB4.

### Dados Reais por Período

| Período | Saldo médio "Operações Sensíveis" | Margem (R$M/trim) | Taxa anualizada |
|---------|-----------------------------------|-------------------|-----------------|
| 3T25 | R$1,236,781M (~R$1.237T) | R$26,629M | ~8.8% a.a. |
| 4T25 | R$1,279,730M (~R$1.280T) | R$26,955M | **8.6%** a.a. |

> **Nota do release**: o saldo "Operações Sensíveis a Spreads" inclui Brasil, LatAm e operações estruturadas do atacado e margem financeira de adquirência — não é apenas Brasil. Por isso o saldo (~R$1.28T) é substancialmente maior do que a carteira de crédito Brasil pura (~R$1.0-1.1T). A taxa de 8.6% é a taxa efetiva divulgada, não uma estimativa.

### NII Total de Clientes (4T25, dados reais)

| Componente | Saldo médio | Margem (R$M/trim) | Taxa |
|------------|------------|-------------------|------|
| MFC Total | R$1,425,978M | R$30,930M | 8.9% a.a. |
| Operações Sensíveis a Spreads | R$1,279,730M | R$26,955M | 8.6% a.a. |
| Capital de Giro Próprio e outros | R$146,248M | R$3,975M | 11.2% a.a. |

> NII_CG / NII_Clientes total = R$3,975M / R$30,930M = **~13%** (não 25-30% como estimativas anteriores sugeriam)

### Por Que a Carteira "Sensível" é Maior que a Carteira Brasil Pura

A decomposição prévia ("Carteira Brasil − PL ≈ R$880B") estava errada em dois aspectos:
1. **LatAm incluída**: o saldo de R$1.28T inclui LatAm (~R$150-160B), não excluída como se supunha
2. **Definição de "sensível" é diferente de "crédito Brasil"**: inclui operações estruturadas de atacado e adquirência — linhas que não aparecem como crédito contábil mas geram margem de spread

### Decomposição do Spread_Sensíveis (~8.6% taxa real, 4T25)

A taxa divulgada de **8.6% a.a.** (4T25) é a taxa blended efetiva sobre o saldo médio de R$1.28T (inclui Brasil + LatAm + estruturadas). A decomposição estimada por produto (~) é consistente com esse nível:

| Produto | Peso estimado na carteira | Spread estimado (a.a.) | Contribuição ao spread médio |
|---------|--------------------------|------------------------|------------------------------|
| Crédito pessoal não-consignado | ~8-10% | ~35-50% | ~3.5-5.0 p.p. |
| [[consignado_privado]] CLT | ~10-15% | ~25-30% | ~3-4 p.p. |
| Cartão de crédito (rotativo + parcelado) | ~10-12% | ~80-150% | ~8-18 p.p. |
| PME / Mid-market PJ | ~15-20% | ~10-20% | ~2-4 p.p. |
| Atacado / Grandes empresas | ~25-30% | ~3-5% | ~0.8-1.5 p.p. |
| Crédito imobiliário | ~10-12% | ~8-12% | ~0.8-1.4 p.p. |
| Outros (rural, BNDES, veículos, LatAm) | ~10-15% | ~5-10% | ~0.5-1.5 p.p. |

A taxa real divulgada (**8.6%**) é inferior à estimativa anterior de ~9.4%, o que é consistente com a inclusão de LatAm (operações de menor spread relativo) e a maior participação do atacado de grandes empresas (CDI+1-3%). Pequenas mudanças no mix têm efeito desproporcional na média.

### Implicação para Modelagem

Usar o NIM histórico como default (~12% total) subestima a **compressão secular de spread** que ocorre com o mix shift. O NIM_Sensíveis tende a cair lentamente no longo prazo mesmo com a carteira crescendo, pois os produtos de maior spread (cartão rotativo, pessoal não-consignado) perdem participação relativa.

## Mix Shift e Suas Consequências

O Itaú está deliberadamente migrando sua carteira em direção a produtos de menor risco absoluto, aceitando compressão de spread bruto em troca de menor [[custo_risco]].

### Produtos em Crescimento (entrada)

| Produto | Característica | Tendência |
|---------|----------------|-----------|
| [[consignado_privado]] CLT | Baixo spread (~25-30%a.a.), baixíssimo risco (desconto em folha) | Aceleração — R$1.9B/mês jan/26 |
| Crédito imobiliário | Spreads IPCA+, garantia real, baixo risco, longo prazo | Crescimento estrutural |
| Grandes empresas / Atacado | CDI+1-3%, baixo risco, relacionamento | Estável a crescendo |

### Produtos em Retração Relativa (saída)

| Produto | Motivo da saída relativa |
|---------|--------------------------|
| Cartão rotativo | Regulação de teto de juros (2024), alta inadimplência |
| Crédito pessoal não-consignado | Concorrência de fintechs, custo de risco elevado |
| PME mid-market sem garantia | Ciclo adverso PJ, seletividade maior |

### Dinâmica de NIM Bruto vs NIM Ajustado

A consequência central do mix shift é que os dois componentes do NIM divergem:

```
NIM bruto (spread)    → comprime  (produtos de alto spread perdem peso)
Custo de risco        → cai mais  (produtos de baixo risco ganham peso)
NIM ajustado ao risco → estável ou melhora
```

Em termos quantitativos (dados reais + estimados):
- NIM_Sensíveis divulgado 4T25: **8.6%** (Fonte: Release 4T25)
- NIM_Sensíveis divulgado 3T25: **8.8%** (Fonte: Release 4T25)
- NIM_Sensíveis em 3-5 anos: ~7.5-8.5% (compressão secular de ~50-150 bps a partir de 8.6%)
- Custo de risco atual: ~2.5-3.0% da carteira
- Custo de risco em 3-5 anos: potencialmente ~2.0-2.5% (melhora de mix)
- NIM ajustado líquido: relativamente estável

**Implicação para o modelo**: projetar NIM_Sensíveis flat subestima a compressão e superestima o NII bruto no longo prazo. O ajuste correto é um declínio gradual de ~10-20 bps/ano no spread médio (aproximadamente 1-2% ao ano de compressão relativa), compensado parcialmente pelo crescimento de volume.

### Impacto em Receita Absoluta

Mesmo com compressão de spread, o NII_Sensíveis em termos absolutos pode crescer se o volume crescer mais rápido do que o spread comprime:

```
Crescimento NII_Sensíveis ≈ Crescimento_Carteira − Compressão_Spread
                          ≈ ~10-12%a.a. − ~1-2%a.a.
                          ≈ ~8-10%a.a. crescimento líquido (~)
```

Essa é a "math" por trás do guidance conservador de NII Clientes do Itaú em ciclos de queda de [[selic]]: menos capital de giro, mas mais volume em consignado compensa parcialmente.

## Concorrência e Compressão Estrutural

A compressão de spread não é apenas cíclica — há um componente estrutural puxado pela entrada de competidores digitais e pela redução de fricção no sistema financeiro.

### Pressão de Fintechs

**Nubank**: Zeraram tarifas e cobram spread muito baixo em crédito pessoal (cartão e empréstimo). A estratégia foi adquirir clientes pelo preço e monetizar depois. O efeito colateral foi forçar os bancos incumbentes a baixar taxas em segmentos de baixo risco para clientes de boa qualidade — se o cliente tem score alto, o Nubank é uma alternativa real.

**C6 Bank, Inter, XP**: Concorrem em crédito para clientes de renda média-alta (target principal do Itaú Premium e Personnalité). Esses clientes são os mais rentáveis e os mais disputados.

**Plataformas de consignado digital**: Aceleração do consignado privado via plataformas (iConsig, Creditas) criou um leilão de taxas — o tomador compara ofertas em tempo real.

### Defesa Estrutural do Itaú

Apesar da pressão, o Itaú possui defesas estruturais que preservam spread relativo:

1. **Conta salário + folha de pagamento**: Banco que paga o salário tem custo de captação efetivo menor (funding barato via depósito à vista) e acesso à folha para consignado.
2. **Relacionamento profundo**: Clientes com múltiplos produtos (conta, cartão, investimento, seguro) têm menor propensão a migrar por spread marginal.
3. **Mix de clientes (mais alta renda, mais produtos por cliente)**: Cliente Personnalité / Uniclass tem menor elasticidade a preço — valoriza conveniência e relacionamento.
4. **Capacidade de servicing**: Operações complexas (M&A, câmbio corporativo, derivativos) são barreiras reais de entrada para fintechs.

### Conclusão: Compressão Real, Mas Contida

A compressão ocorre, mas de forma gradual e parcialmente compensada:
- **Segmentos atacados pelas fintechs**: pessoal sem garantia, cartão para classe média → spread comprime ~200-400 bps ao longo de 5 anos
- **Segmentos defensáveis**: atacado, consignado (escala), imobiliário (relacionamento) → spread mais estável
- **Net**: Itaú mantém spread relativo vis-à-vis sistema financeiro por conta de mix de clientes; perde margem absoluta de forma lenta

Para a modelagem: o spread_sensíveis do Itaú provavelmente declina ~50-100 bps nos próximos 3 anos (~), com maior risco de baixa do que de alta.

## Ver Também

- [[nii_clientes]] — conceito pai (NII total de clientes)
- [[remuneracao_capital_giro]] — o outro sub-componente (automático, Selic-driven)
- [[crescimento_carteira]] — volume driver
- [[nim]] — NIM total consolidado
- [[custo_risco]] — risco do spread: quanto maior o spread, maior tende a ser a inadimplência
- [[consignado_privado]] — produto de crescimento acelerado, baixo risco, comprime NIM_Sensíveis
- [[selic]] — afeta NIM_CG diretamente e NIM_Sensíveis indiretamente via demanda
- [[banking]] — contexto setorial
