---
type: setor
source_quality: conceptual
aliases: [Incorporadoras, Real Estate, Setor Imobiliário, RE]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/DIRR3/outputs/decomposition/DIRR3_dependency_graph_v3.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
updated: 2026-04-05
---

# Incorporadoras Brasileiras

O setor de incorporação imobiliária no Brasil engloba empresas que compram terrenos, planejam empreendimentos, lançam unidades para venda e executam a construção. O ciclo típico dura 3 a 5 anos entre aquisição do terreno e recebimento do saldo do comprador. É um setor intensivo em capital de giro, regulado pela CVM (ITR/DFP), e com modelo de receita baseado em **POC** — não em caixa.

## Modelo de Negócio

O ciclo da incorporação:

```
Aquisição de terreno
  → Aprovação de projeto (licenças, prefeitura)
    → Lançamento comercial (stand de vendas, publicidade)
      → Construção (18–36 meses)
        → Entrega das chaves (habite-se)
          → Repasse ao banco financiador
```

A receita **não** é reconhecida no ato da venda — é reconhecida conforme o avanço percentual da obra ([[poc_revenue]], método POC/IFRS 15/CPC 47). O lag entre venda e receita é de 2 a 3 anos.

### Segmentos do Mercado

| Segmento | Programa | Correção INCC? | Principais Players |
|----------|----------|----------------|-------------------|
| MCMV Faixa 1-3 | [[mcmv]] | **Não** | [[cury]], [[direcional]], Tenda, MRV |
| Econômico / Médio padrão | Livre | Sim | [[direcional]] (Riva), Tenda (Alea) |
| Alto padrão | Livre | Sim | [[cyrela]], [[eztc3]] |

A ausência de correção de preço no MCMV é uma armadilha crítica: se o [[incc]] sobe acima do orçado, toda a erosão de margem recai sobre a incorporadora. Sensibilidade histórica: +3pp de INCC ≈ -1,5 a -2,0pp de margem bruta realizada para empresas MCMV puras.

## Métricas Centrais

### [[vgv_lancamentos]] — Valor Geral de Vendas

Soma dos preços de tabela de todas as unidades de um empreendimento. É a métrica primária de pipeline porque representa receita futura potencial. **Convenção crítica:** o modelo usa VGV 100% consolidado, não % Cia. Minoritários são deduzidos apenas após o lucro líquido.

### [[velocidade_vendas]] — VSO

VSO (Velocidade de Vendas Sobre Oferta) = unidades vendidas / (estoque + lançamentos) no período. Proxy de saúde de demanda e poder de precificação.

### [[margem_backlog]]

Margem orçada da carteira contratada. Indicador leading da margem bruta futura — antecede 2-3 anos a DRE. Gap típico entre margem backlog e realizada: MCMV -4 a -6pp; alta-renda ~-3,5pp.

### [[poc_revenue]] — Percentage of Completion

```
Receita(t) = Backlog_início(t) × POC_sazonal(t)
```

O POC varia por trimestre (sazonalidade real). Nunca use POC flat anual / 4.

## Players Cobertos

| Ticker | Empresa | Segmento | Complexidade |
|--------|---------|----------|--------------|
| CYRE3 | [[cyrela]] | Alta-renda + Vivaz (MCMV) + EP exógena | Máxima |
| CURY3 | [[cury]] | MCMV puro SP/RJ | Mínima (sem investidas) |
| DIRR3 | [[direcional]] | MCMV econômico + Riva (médio-alto) | Média (minoritários relevantes) |
| PLPL3 | Plano & Plano | MCMV SP (subsidiária Cyrela) | Simples |
| TEND3 | Tenda | MCMV + Alea (wood-frame) | Média (Alea em ramp-up) |
| EZTC3 | [[eztc3]] | Alta-renda SP | Configurado |
| MRVE3 | MRV | MCMV + AHS + USA | Configurado |

## Drivers Macro

| Driver | Impacto | Ligação |
|--------|---------|---------|
| [[selic]] | Canal de demanda (crédito imobiliário pós-chaves) e resultado financeiro | 3 canais: demanda, rec_fin, desp_fin |
| [[incc]] | Corrói margem de safras sem correção de preço | MCMV 100% exposto; alta-renda parcialmente protegida |
| [[mcmv]] | Política pública de habitação subsidiada; teto de preço e taxa FGTS | Volume MCMV Faixa 1-3 |
| Taxa de juros imobiliários | SBPE (pós-chaves); crédito habitacional convencional | Demanda alta-renda |

## Particularidades Contábeis

### POC e Backlog Rollforward

```
Backlog_fim = Backlog_início + Vendas_novas − Receita_reconhecida
```

O backlog cresce quando VGV de lançamentos supera receita reconhecida. Margem bruta **é input direto** no modelo — o analista calibra pelo backlog + gap histórico.

### Conceito de Safra (Vintage)

A margem bruta não é função dos lançamentos atuais. É função das margens orçadas nos empreendimentos lançados 2-3 anos atrás (a "safra" sendo construída hoje). A [[margem_backlog]] é o melhor indicador leading.

### AVP — Ajuste a Valor Presente

Recebíveis de longo prazo (parcelas durante a obra) são ajustados a valor presente. Reduz a receita e o recebível registrado. No modelo, entra como item de verificação, não como driver da projeção.

### EBIT, não EBITDA

D&A é imaterial em incorporadoras (sem ativos fixos pesados). Métrica operacional: **EBIT**.

```
EBIT = Lucro Bruto + Desp. Comerciais + G&A + Equiv. Patrimonial + Outras Op.
```

EBITDA não é relevante para o setor. Ver [[banking]] para contraste com setor bancário.

### Equivalência Patrimonial (EP)

Participações em empresas investidas (SPEs, companhias listadas). Dois tipos:
- **Endógena:** SPEs do próprio projeto (parceria 50/50)
- **Exógena:** Participação em empresas listadas (ex: [[cyrela]] em [[cury]], Lavvi, P&P)

### Covenant Setorial

Dívida Líquida / PL (não DL/EBITDA). D&A é imaterial.

## Estrutura do Three-Statement Model

### DRE
```
Receita Líquida (POC sobre backlog)
(−) Custo de Vendas
= Lucro Bruto
(−) Despesas Comerciais  ← % do VGV lançado (não da receita)
(−) Despesas G&A         ← % da receita
(+/−) Equivalência Patrimonial
(+/−) Outras Despesas/Receitas Operacionais
= EBIT
(+) Receitas Financeiras  ← caixa(t-1) × spread × Selic/4
(−) Despesas Financeiras  ← dívida(t-1) × Kd/4
= EBT
(−) IR / CSLL
= Lucro Líquido
(−) Minoritários
= LL Controladores
```

### Balanço Patrimonial
Ativos dominantes: estoques (imóveis + terrenos), contas a receber, terrenos a pagar.
Passivos dominantes: adiantamento de clientes, dívida bruta (SFH + corporativa).

**Dívida como PLUG:** se caixa cairia abaixo de `caixa_mínima`, a dívida bruta sobe automaticamente.

### Capital de Giro (principais drivers)

| Driver | Fórmula | Range |
|--------|---------|-------|
| Dias Recebíveis | recebíveis / (trailing_4Q_receita / 90) | 140–224 dias |
| Dias Estoques | estoques / (trailing_4Q_custo / 90) | 150–970 dias |
| Dias Terrenos a Pagar | terrenos_pagar / (trailing_4Q_custo / 90) | 85–700 dias |
| Dias Adiant. Clientes | adiant_clientes / (trailing_4Q_receita / 90) | 0–60 dias |

## Sazonalidade

- **2T e 4T:** Pico de lançamentos (feiras de imóveis)
- **1T:** Mais fraco (pós-festas, replanejamento)
- VSO do 1T historicamente menor; POC sazonal captura esse padrão

## Riscos Setoriais

- **Distratos:** Cancelamentos antes da entrega; sobem com Selic alta
- **INCC e erosão de margem:** Assimétrico — MCMV 100% exposto
- **Alvarás:** Aprovações municipais podem atrasar lançamentos (ex: liminar SP 2026)
- **Landbank:** Capital imobilizado em terrenos não lançados; dias estoques outlier (DIRR: ~970d)
- **MCMV como política pública:** Mudanças de teto e orçamento são eventos binários

## Valuation de Incorporadoras

Incorporadoras são tipicamente avaliadas por múltiplos de **P/L (preço sobre lucro)** e **P/VPA (preço sobre valor patrimonial)**, com atenção ao **NAV (Net Asset Value)** como âncora de valor intrínseco.

### NAV: A Âncora de Valor

O NAV de uma incorporadora é o valor presente de todos os projetos no landbank a margens esperadas, descontado pelo custo de capital:

```
NAV = PV(backlog × margem_bruta × (1 - impostos)) 
    + PV(landbank_não_lançado × margem_esperada × (1 - impostos))
    + Posição de caixa líquido
    - Dívida corporativa
    + Equivalência Patrimonial (investidas listadas ao valor de mercado)
```

**Problema prático:** O NAV requer premissas de longo prazo sobre VGV futuro, margem e taxa de desconto. Como cada premissa é incerta, o range de NAV é largo — geralmente usado como teto (bull case) mais do que âncora pontual.

### Múltiplos Relevantes

| Múltiplo | Uso | Limitação |
|----------|-----|-----------|
| P/L | Comparação simples; amplamente usado | LL volátil por sazonalidade de POC |
| P/VPA | Referência contábil | Não captura qualidade do landbank |
| P/NAV | Desconto vs valor intrínseco | NAV muito sensível a premissas |
| EV/EBIT | Preferido sobre EV/EBITDA (D&A imaterial) | VGV e ciclo distorcem |
| Dividend Yield | Para empresas com payout alto ([[cury]]) | Não é standard; mais para renda |

**Nível de desconto P/NAV histórico:** Incorporadoras brasileiras negocia tipicamente a 0,6-1,0× NAV. Desconto acima de 40% (P/NAV < 0,6) costuma ser oportunidade — desconfiança de mercado exagerada vs. fundamentos.

## Regime Tributário Especial (RET) para Incorporadoras

A lei brasileira permite às incorporadoras que inscreverem seus empreendimentos em **RET (Regime Especial Tributário)** pagar IR+CS de forma simplificada sobre a receita bruta:

```
RET: IR + CS + PIS + COFINS = 4% da receita bruta (MCMV) ou 6% (demais)
vs.
Regime ordinário: IR (~25%) + CS (~9%) sobre o lucro = ~34% × margem
```

**Quando RET é melhor que o regime ordinário:**
- Margem bruta < ~12% (para RET 4%): RET é melhor pois 4% da receita < 34% × 12% = 4,1%
- Para margens de ~38-40% (como Cury): 4% da receita ≈ 34% × 12% de margem efetiva → **RET é muito mais vantajoso**

O RET é o principal driver da baixa alíquota efetiva de empresas MCMV puras ([[cury]], [[tenda]]): o imposto é calculado sobre a receita (não sobre o lucro), o que em alta margem equivale a alíquota efetiva de ~2-3%.

**Limitação:** Não é todo empreendimento que pode ser inscrito no RET — existem requisitos (patrimônio de afetação, regularidade, entre outros). As grandes incorporadoras geralmente atendem, mas pequenos projetos podem não qualificar.

## Framework para Comparação: Simplicidade vs Complexidade

| Empresa | Complexidade | Por Quê | O Que Monitorar |
|---------|-------------|---------|----------------|
| [[cury]] | Mínima | MCMV puro, SP/RJ, sem EP, sem sub financeira | VGV lançado, VSO, MB, IR (RET) |
| [[tenda]] | Média | Dois segmentos (Tenda + Alea), ambos MCMV | Margem Alea, RET, IR minority |
| [[direcional]] | Média-Alta | Dois segmentos (DIRR + Riva), minorities relevantes | % Riva do VGV, minorities, landbank |
| [[cyrela]] | Máxima | Multi-seg, EP exógena material (~R$550M/ano), CashMe | EP cury/lavvi/P&P, CashMe result, Vivaz VSO |

**Implicação para modelagem:** Quanto mais simples a empresa, menos variáveis no modelo — menor incerteza de projeção. A Cury tem modelo de 6 premissas; a Cyrela tem modelo de 20+ premissas. Isso explica por que o consenso Bloomberg acerta mais a Cury do que a Cyrela.

## Ver Também

- [[vgv_lancamentos]] — métrica primária de pipeline; mede atividade de lançamentos
- [[velocidade_vendas]] — VSO, saúde de demanda
- [[margem_backlog]] — indicador leading de margem bruta (2-3 anos de antecedência)
- [[poc_revenue]] — reconhecimento de receita por avanço de obra
- [[mcmv]] — programa federal de habitação; driver de demanda principal
- [[incc]] — inflação da construção civil; principal risco de custo
- [[capital_de_giro]] — WC intensivo; diferença central entre EBIT e FCO
- [[equivalencia_patrimonial]] — EP endógena (JVs) e exógena (listadas) nas incorporadoras
- [[cyrela]] — maior incorporadora diversificada; modelo mais complexo
- [[cury]] — MCMV puro SP/RJ; modelo mais simples; melhor ROE
- [[direcional]] — MCMV + Riva; minorities relevantes
- [[tenda]] — MCMV + Alea; turnaround wood frame
- [[alea]] — subsidiária da Tenda; wood frame; turnaround operacional
