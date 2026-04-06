---
type: setor
source_quality: conceptual
aliases: [Bancos Brasileiros, Banking, Setor Bancário, Bancos]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
updated: 2026-04-05
---

# Bancos Brasileiros

O setor bancário brasileiro opera sob lógica fundamentalmente distinta de empresas corporativas: **o balanço é o negócio**. Crescer significa expandir o balanço (carteira de crédito no ativo, depósitos no passivo). Rentabilidade é ROA × alavancagem. Risco é qualidade do ativo. EBITDA e fluxo de caixa livre são conceitos irrelevantes para análise de bancos.

## Modelo de Negócio

O ciclo básico da intermediação financeira:

```
Captação de recursos
  (depósitos à vista, poupança, CDB, LCI/LCA, Letras Financeiras)
    → Gestão de tesouraria (TVM, derivativos, compulsórios)
      → Concessão de crédito (PF, PJ, agro, imobiliário)
        → Receita de intermediação (juros do crédito)
          → Dedução do custo de captação
            = Margem Financeira Bruta (NII)
              → Dedução de PDD (provisão para inadimplência)
                = Margem Financeira Líquida
```

Além do crédito, bancos geram receita de **serviços e tarifas** (fee income): administração de fundos, cartões, corretagem, assessoria, consórcios. E, para grandes conglomerados, **resultado de seguros/previdência/capitalização**.

### Segmentos de Crédito

| Segmento | Spread Típico | Risco | Capital (RWA) |
|----------|--------------|-------|----------------|
| Consignado (PF) | Baixo (~15-20% a.a.) | Baixo | Baixo |
| Crédito Imobiliário | Muito baixo (IPCA+6-8%) | Muito baixo | Baixo |
| Crédito Rural / Agro | Baixo-médio (subsidiado) | Baixo-médio | Baixo |
| Crédito Pessoal não-consignado | Alto (~35-50% a.a.) | Alto | Alto |
| Cartão de Crédito | Muito alto (>100% a.a.) | Muito alto | Alto |
| Capital de Giro PJ | Médio (~20-30% a.a.) | Médio | Médio |
| Grandes Empresas / Atacado | Baixo (CDI+1-3%) | Baixo | Baixo |

O mix da carteira determina tanto o [[nim]] quanto o [[custo_risco]]. Banco que cresce agro/consignado tem NIM menor mas inadimplência menor. Banco que cresce cartão/pessoal tem NIM maior com custo de crédito muito mais alto.

## Métricas Centrais

| Métrica | Fórmula | Range Típico | O que indica |
|---------|---------|-------------|-------------|
| [[nim]] | NII / Ativos Remunerados Médios | 10-14% a.a. | Rentabilidade dos ativos |
| [[custo_risco]] | PDD anualizado / Carteira média | 2-5% | Qualidade da carteira |
| [[eficiencia_operacional]] | Opex / Receita Total | 35-55% | Alavancagem operacional |
| [[roe_bancario]] | LL anualizado / PL médio | 15-22% | Retorno ao acionista |
| [[cet1]] ratio | Capital Principal / RWA | min ~11,5% (D-SIBs) | Adequação de capital |

## Players no Setor

| Empresa | Ticker | Destaque | Seguros |
|---------|--------|---------|--------|
| [[itau]] | ITUB4 | Líder em eficiência (IE ~39%) e ROE (~22%) | Porto Seguro — equity method (NÃO consolidado) |
| [[bradesco]] | BBDC4 | Em turnaround; Bradesco Seguros consolidada (~25-30% do LL) | Consolidado integralmente |
| Banco do Brasil | BBAS3 | Líder em agro (~60% do crédito rural SFN) | BB Seguridade (BBSE3) — equity method |
| Santander Brasil | SANB11 | Banco de atacado + varejo; menor no agro | Dentro do conglomerado |

## Drivers Macro

- **[[selic]]**: Principal alavanca do NIM. Selic alta → spread de crédito maior; Selic alta também comprime demanda de crédito no médio prazo.
- **[[crescimento_carteira]]**: Volume total da carteira de crédito × spread = NII. PIB + apetite de risco do banco determinam o crescimento.
- **[[nii_clientes]]**: Componente principal do NII — spread sobre a carteira de clientes.
- **[[nii_mercado]]**: Componente de tesouraria — mais volátil.
- **[[custo_risco]]**: Ciclo de crédito, sazonalidade (4T mais pesado), crescimento da carteira.

## Particularidades Contábeis

### Duplo Padrão: COSIF vs IFRS

| Padrão | Para Quem | Modelo de Provisão | Onde Acessar |
|--------|-----------|-------------------|-------------|
| BRGAAP (COSIF) | BCB (regulatório) | Perda incorrida (Res. CMN 2.682/99) | BCB IF.data |
| IFRS (CPC 48/IFRS 9) | CVM (investidores) | ECL — Expected Credit Loss | CVM ITR/DFP |

O mercado usa o **resultado gerencial** publicado nos releases de RI — base IFRS com ajustes próprios (exclui amortização de intangíveis adquiridos em M&A, ajusta efeitos de hedge).

### Tributação Diferenciada

- **CSLL: 20% para IFs** (não 9% como corporativas). Alíquota estatutária total ~45%.
- **JCP (Juros sobre Capital Próprio)**: distribuição dedutível de IR/CSLL. Com JCP, alíquota efetiva cai para ~30-35%.
- **PIS/COFINS**: regime cumulativo para IFs (4,65% sobre serviços, menor sobre receitas financeiras).

Ver [[aliquota_efetiva]] para detalhes.

### Basileia III e Capital

Para D-SIBs (ITUB4, BBDC4, BBAS3, SANB11): CET1 mínimo efetivo ~11,5-14%. Abaixo desse nível, BCB limita automaticamente dividendos, JCP e recompras. **O dividendo bancário é limitado não apenas pelo payout mas pela adequação de capital.**

### PDD: Principal Item de Volatilidade

```
PDD_fluxo(t) = Carteira_credito(t) × Custo_crédito_anualizado / 4
```

Sazonalidade: 4T tipicamente maior (revisão de portfólio, provisões adicionais). 1T tende a ser menor.

## Estrutura DRE Bancária

```
NII (Margem Financeira Bruta)
(-) PDD / PCLD
= Margem Financeira Líquida
(+) Receita de Serviços e Tarifas
(+/-) Resultado de Seguros [apenas bancos com seguros consolidados]
= Receita Total [denominador do Índice de Eficiência]
(-) Despesas de Pessoal e Administrativas
(-) Despesas Tributárias
= Resultado Operacional
(+/-) Equivalência Patrimonial [Porto Seguro para ITUB4; BB Seguridade para BBAS3]
(-) IR / CSLL
= Lucro Líquido
```

## ROE Decomposition (DuPont Bancário)

O [[roe_bancario]] bancário se decompõe em dois fatores fundamentais:

```
ROE = ROA × Multiplicador_Capital
ROA = LL / Ativo_Total
Multiplicador = Ativo_Total / PL
```

Para bancos, os ranges típicos são:
- **ROA**: 1,5-2,5% a.a. (bancos são ativos intensivos; ROA baixo é estrutural)
- **Multiplicador de capital**: 8-12× (alavancagem regulada pelo [[cet1]])
- **ROE resultante**: 15-25%

### Itaú 2025 (referência empírica)

- LL ~R$46,8B / PL ~R$215B → ROE ~24,4%
- LL ~R$46,8B / Ativo Total ~R$2T → ROA ~2,3%
- Multiplicador implícito: 24,4% / 2,3% ≈ **10,6×**

O multiplicador de ~10,6× é relativamente baixo para o setor — reflexo de banco bem capitalizado. Bancos com [[cet1]] mais pressionado operam com multiplicadores maiores.

### Alavancas para crescimento de ROE

**(a) Aumentar ROA** — via NIM maior (mix de carteira mais spreado) ou ganho de eficiência (redução de opex / [[eficiencia_operacional]]).

**(b) Aumentar o multiplicador** — distribuindo capital excedente (payout maior, recompra de ações), o que reduz o PL e eleva a alavancagem implícita.

**Paradoxo do payout alto**: O Itaú pagou payout de ~72% em 2025 (extraordinário, acima do normal de 50-60%) para redistribuir [[cet1]] excedente acumulado. Esse movimento reduz o PL contábil e, matematicamente, sobe o ROE sustentável — desde que o banco mantenha capital suficiente para continuar crescendo a carteira no ritmo desejado. Não é destruição de valor; é otimização de estrutura de capital.

## Capital: Basileia III e Política de Dividendos

### Estrutura de Capital Regulatório

O [[cet1]] (Common Equity Tier 1) é o principal indicador de solidez de capital:

```
CET1 = Capital Principal (ações ordinárias + lucros retidos - deduções) / RWA
RWA = Ativos Ponderados pelo Risco (crédito + mercado + operacional)
```

Para **D-SIBs brasileiras** (Itaú, Bradesco, BB, Santander BR, CEF), o BCB exige buffer adicional de 1-2% sobre o mínimo de Basileia III, resultando em:

| Banco | CET1 Mínimo Efetivo | CET1 4T25 (referência) |
|-------|--------------------|-----------------------|
| ITUB4 | ~11,5% | ~12,3% |
| Demais D-SIBs | ~11,5-12,5% | varia |

O buffer adicional D-SIB penaliza os maiores bancos do sistema, mas também sinaliza importância sistêmica — custo do "too big to fail".

### Mecanismo de Restrição de Dividendos

O dividendo bancário é **duplo-limitado**:

1. **Patamar de capital (CET1)**: Se CET1 cair abaixo do mínimo efetivo, o BCB aciona automaticamente restrições progressivas a JCP, dividendos e recompras (quanto menor o CET1, maior a restrição).
2. **Política de gestão**: Mesmo com CET1 acima do mínimo, o management define um *target* interno de capital (ex.: Itaú opera com ~50-60 bps de folga acima do mínimo regulatório).

```
Espaço para dividendo = CET1_atual - CET1_target
Se CET1_atual >> CET1_target → payout extraordinário ou recompra
Se CET1_atual ≈ CET1_target → payout normal (~50-60%)
Se CET1_atual < CET1_target → corte de payout
```

### Itaú: Interpretação do Payout 2025

- CET1 4T25: ~12,3% — acima do mínimo (~11,5%) mas sem excesso exagerado
- Payout 2025: ~72% (inclui antecipação de dividendos de dez/25, aproveitando folga de CET1)
- Payout "normal" (guidance implícito): 50-60%
- Guidance implícito de ROE 2026: >22% (redução frente aos ~24,4% de 2025, refletindo menor alavancagem pós-distribuição e crescimento do PL orgânico)

A antecipação de dividendos em dez/25 foi possível exatamente porque o [[cet1]] estava folgado — mecanismo de otimização de capital, não sinal de stress.

## Ciclo de Crédito e Onde Estamos em 2026

O ciclo de crédito bancário no Brasil tem padrão recorrente: expansão → deterioração → provisões → normalização. Conhecer a posição no ciclo é central para modelar [[custo_risco]] e [[nim]].

### Histórico Recente

| Período | Dinâmica | Driver Principal |
|---------|----------|-----------------|
| 2020-21 | Expansão de crédito + [[selic]] em mínima histórica (2%) + pico de provisões COVID | Pandemia + estímulo fiscal |
| 2022-23 | Ciclo adverso: Americanas, Light, inadimplência PF pós-COVID + [[selic]] subindo aggressivamente | Normalização monetária + stress PJ |
| 2024-25 | Normalização gradual: NIM elevado (Selic alta), inadimplência PF em queda, PJ estabilizando | Selic alta favorece spread; portfólio saneado |
| 2026 | Selic provavelmente no pico (~14,75%) → benefício NIM pleno; consignado privado como driver de crescimento | Pico do ciclo de juros |

### Diagnóstico 2026

**Positivos**:
- [[selic]] ~14,75% sustenta NIM em nível elevado enquanto durar o ciclo restritivo
- Consignado privado (regulamentado em 2023-24) abre novo mercado de crédito com risco baixo
- Inadimplência PF em queda desde meados de 2023; grandes bancos com portfólio mais saneado

**Vigilâncias**:
- Selic alta por mais tempo comprime fluxo de caixa de PMEs → **inadimplência PJ mid-market pode subir em 2026-27**
- Demanda de crédito corporativo (capital de giro, investimento) pode desacelerar com custo de capital elevado
- Empresas médias (fora do Investment Grade) são o segmento de maior risco sistêmico no ciclo atual

**Implicação para modelagem**: Ao projetar [[custo_risco]] para 2026, o conservadorismo está no segmento PJ mid-market, não no PF. NIM pode se manter elevado mesmo com eventual início de queda da Selic, pela defasagem de reprecificação do passivo.

## Ver Também

- [[nii_clientes]] — componente principal do NII
- [[nii_mercado]] — NII de tesouraria
- [[nim]] — margem de juros líquida
- [[custo_risco]] — qualidade do crédito
- [[eficiencia_operacional]] — índice de eficiência operacional
- [[roe_bancario]] — retorno sobre patrimônio líquido bancário
- [[cet1]] — adequação de capital (Basileia III)
- [[selic]] — driver macro de NIM
- [[crescimento_carteira]] — driver de volume
- [[receita_servicos_tarifas]] — fee income
- [[resultado_seguros]] — para bancos com seguros consolidados
- [[aliquota_efetiva]] — tributação de IFs
- [[itau]] — empresa modelada
- [[bradesco]] — empresa em cobertura
