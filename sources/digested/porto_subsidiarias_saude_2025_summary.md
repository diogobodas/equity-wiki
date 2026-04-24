---
source: porto_seguro_individual_dfs_2025
segment: saude
companies: [porto_seguro_saude, porto_saude_operacoes, porto_saude_participacoes, portomed, porto_odontologicos]
asof: 2025
generated: 2026-04-24
---

# Porto Seguro — Segmento Saúde 2025: Digest de DFs Individuais

## 1. Mapa Estrutural (Hierarquia)

```
Porto Seguro S.A. (PSSA3) — holding listada
    └── Porto Saúde Participações S.A. (CNPJ 46.573.272/0001-81)
            └── Porto Saúde - Operações de Saúde S.A. (CNPJ 46.728.667/0001-06)
                    ├── Porto Seguro - Seguro Saúde S.A. (CNPJ 04.540.010/0001-70) — 100%
                    ├── Portomed - Porto Seguro Serviços de Saúde Ltda (CNPJ 11.565.995/0001-54) — 100%
                    └── Porto Seguro Serviços Odontológicos Ltda (CNPJ 13.991.711/0001-17) — 100%
```

**Porto Saúde Participações S.A.** é a holding do topo do segmento saúde dentro do Grupo Porto, controlada direta da Porto Seguro S.A. Ela detém 100% da **Porto Saúde - Operações de Saúde S.A.**, que por sua vez é a sub-holding operacional e controla as três entidades operadoras abaixo.

**Distinção regulatória e de negócio:**
- **Porto Seguro - Seguro Saúde S.A.** (seguradora): regulada pela ANS como seguradora especializada em saúde (autorizada pela RE ANS nº 2/2001, supervisionada pela SUSEP). Opera via contratos de seguro — emite apólices, cobra prêmios, paga sinistros. Produto principal: seguro saúde individual e coletivo empresarial.
- **Portomed - Porto Seguro Serviços de Saúde Ltda** (operadora ANS): regulada pela ANS como operadora de planos privados de assistência à saúde, exclusivamente empresariais. Opera via contraprestações pecuniárias (plano de saúde), não prêmios. Constituída em 2010.
- **Porto Seguro Serviços Odontológicos Ltda** (operadora odonto ANS): opera planos privados de assistência odontológica. Constituída em 2011. Operação em run-down — sem receitas operacionais relevantes em 2025.
- **Porto Saúde - Operações de Saúde S.A.**: sub-holding pura (constituída junho 2022). Objeto social é participar em sociedades do mercado de saúde. Não opera diretamente; resultado é composto de equivalência patrimonial das três controladas.

**Nota sobre Azul Seguros:** o arquivo `porto_saude_participacoes.md` contém também as DFs da Azul Companhia de Seguros Gerais (CNPJ 33.448.150/0001-11, controlada pela Porto Cia. de Seguros Gerais, não pelo segmento Saúde). Os dados da Azul foram descartados desta análise, que se concentra exclusivamente no segmento Saúde.

---

## 2. Tabela de Referência Rápida (R$ mil)

| Entidade | Receita 2025 | Receita 2024 | Δ% | Sinistros/Eventos 2025 | Índice sinistral./médico | Lucro Líquido 2025 | Lucro Líquido 2024 | PL dez/25 | ROE aprox. |
|---|---|---|---|---|---|---|---|---|---|
| Porto Seguro - Seguro Saúde (seguradora) | 8.171.450 | 6.398.825 | +27,7% | (6.130.975) | 75,9% (sinistralidade sobre prêmios ganhos) | 705.125 | 348.660 | 2.238.068 | ~34% |
| Porto Saúde - Operações de Saúde (sub-holding individual) | 703.246 (equiv. patr.) | 340.565 (equiv. patr.) | +106,5% | — | — | 673.719 | 340.491 | 2.242.555 | ~32% |
| Porto Saúde Participações (holding topo — consolidado) | 8.443.165 | 6.608.194 | +27,8% | (6.901.357) | n/a consolidado | 666.306 | 353.417 | 2.342.005 (consolidado) | ~30% |
| Portomed (operadora planos) | 28.897 | 358 | n/m | (22.499) | ~75,8% (eventos/contraprestações líq.) | (3.922) | (585) | 19.004 | negativo |
| Porto Odonto (operadora odonto) | — | — | — | — | — | (29) | (287) | 504 | negativo |

Fontes: (fonte: full/porto_seguro/2025/subsidiarias/porto_seguro_saude.md), (fonte: full/porto_seguro/2025/subsidiarias/porto_saude_operacoes.md), (fonte: full/porto_seguro/2025/subsidiarias/porto_saude_participacoes.md), (fonte: full/porto_seguro/2025/subsidiarias/portomed.md), (fonte: full/porto_seguro/2025/subsidiarias/porto_odontologicos.md)

---

## 3. Deep Dive por Subsidiária

### 3.1 Porto Seguro - Seguro Saúde S.A.

**O que faz:** seguradora especializada em saúde, regulada pela ANS. Emite apólices de seguro saúde — individual e coletivo empresarial — cobrados como prêmios. É a entidade que concentra a quase totalidade da receita e do resultado do segmento Saúde.

**DRE 2025 vs. 2024 (R$ mil):**
- Prêmios retidos: 8.173.214 (2024: 6.396.901), +27,8%
- Receitas com operações de assistência à saúde: 8.171.450 (2024: 6.398.825), +27,7%
- Prêmios ganhos: 8.078.001 (2024: 6.327.971)
- Sinistros retidos: (6.130.975) (2024: (4.889.691)), +25,4%
  - Sinistros conhecidos/avisados: (5.870.776) (2024: (4.715.192))
  - Variação PEONA: (260.199) (2024: (174.499))
- Resultado das operações c/ planos de assistência: 1.947.026 (2024: 1.438.280), após outras despesas operacionais de (138.777)
- Despesa de comercialização: (598.967) (2024: (514.371))
- Despesa administrativa: (442.090) (2024: (342.772))
- Resultado financeiro: 286.054 (2024: 129.379)
  - Receitas financeiras: 320.686 (2024: 155.592)
  - Despesas financeiras: (34.632) (2024: (26.213))
- Resultado patrimonial: 5.728 (2024: 7.979)
- Resultado antes IR/CSLL: 1.062.780 (2024: 628.896)
- IR + CSLL + diferidos: (258.786) (2024: (228.236))
- Participações sobre o lucro: (98.869) (2024: (52.000))
- **Resultado líquido: 705.125** (2024: 348.660), **+102,2%**

(fonte: full/porto_seguro/2025/subsidiarias/porto_seguro_saude.md)

**Ratios-chave:**
- Sinistralidade (sinistros retidos / prêmios ganhos): 6.130.975 / 8.078.001 = **75,9%** (2024: 77,3%) — melhora de 1,37 pp, confirmada pelo relatório da administração que cita queda de 1,37 pp no índice de sinistralidade
- Índice combinado (conforme relatório da administração): **90,5%** em 2025, queda de 1,78 pp vs. 2024
- Índice combinado ampliado (com resultado financeiro): **87,4%**, queda de 3,02 pp
- Despesas administrativas / prêmios ganhos: 442.090 / 8.078.001 = 5,5% (2024: ~5,4%) — aumento de 0,06 pp
- Taxa efetiva de IR/CSLL: **21,5%** (2024: 22,4%)
- PL: 2.238.068 (2024: 1.683.374)
- ROE: ~34% (resultado líquido / PL médio ≈ 705.125 / ((2.238.068 + 1.683.374)/2))

**Beneficiários:** 831 mil vidas em saúde ao final do 4T25, crescimento de +156 mil vs. 4T24 (+23%)
(fonte: full/porto_seguro/2025/subsidiarias/porto_saude_participacoes.md — relatório da administração da holding)

**Provisões técnicas totais:** R$ 15.297.650 mil bruto de resseguro (2024: R$ 11.887.105 mil), crescimento de +29% reflete o forte crescimento da carteira.
- Provisão de prêmios não ganhos: 12.243.490
- Sinistros e benefícios a liquidar: 2.431.260
- PEONA: 455.511
- Demais: 167.389
(fonte: full/porto_seguro/2025/subsidiarias/porto_seguro_saude.md)

**Eventos estruturais:**
- A Companhia tem empréstimos bancários de R$ 189.680 mil para financiar infraestrutura tecnológica (CCBs com Itaú e Bradesco, CDI + 1,37% a 2,24%)
- A Azul Companhia de Seguros Gerais (controlada pela Porto Cia., não pela vertical Saúde) diminuiu significativamente emissões de apólices em 2025, repassando carteiras para a controladora — isso reflete concentração de negócios similares em verticais; não afeta diretamente esta entidade mas explica movimento de portfólio no grupo.

---

### 3.2 Portomed - Porto Seguro Serviços de Saúde Ltda.

**O que faz:** operadora de planos privados de assistência à saúde exclusivamente empresariais, regulada pela ANS sob RN nº 528/2022. Opera como operadora de autogestão, não seguradora — cobra contraprestações pecuniárias, não prêmios. Única cotista: Porto Saúde - Operações de Saúde S.A. (100%). Está em fase de forte ramp-up de carteira.

**DRE 2025 vs. 2024 (R$ mil):**
- Contraprestações efetivas de planos de assistência: 28.002 (2024: 306) — crescimento explosivo, operação virtualmente inexistente em 2024
- Receita assistência à saúde: 28.897 (2024: 358), +7.973%
- Contraprestações líquidas: 29.753 (2024: 1.154)
- Variação provisões técnicas: (856) (2024: (796))
- Tributos diretos: (895) (2024: (52))
- Eventos indenizáveis líquidos: (22.499) (2024: (422))
  - Sinistros conhecidos/avisados: (20.031) (2024: (379))
  - Variação PEONA: (2.468) (2024: (43))
- Resultado das operações c/ planos: 5.503 (2024: (116))
- Outras despesas operacionais: (2.585) (2024: 197)
- Resultado bruto: 2.918 (2024: 85)
- Despesas de comercialização: (7.365) (2024: (176))
- Despesas administrativas: (881) (2024: (1.441)), redução de 38,9% — melhora de eficiência
- Resultado financeiro: 1.475 (2024: 947)
- Resultado antes IR: (3.853) (2024: (585))
- **Resultado líquido: (3.922)** (2024: (585))

(fonte: full/porto_seguro/2025/subsidiarias/portomed.md)

**Ratios-chave:**
- Índice de eventos indenizáveis / contraprestações líquidas: 22.499 / 29.753 = **75,6%** — estruturalmente alto para uma operadora nova que ainda não tem massa crítica para diluir risco
- Despesas de comercialização são desproporcionalmente altas (R$ 7.365 vs. receita de R$ 28.897) porque incluem comissões diferidas em constituição — nota 12 confirma que débitos de operações referem-se substancialmente a comissões a pagar aos corretores

**Balanço resumido:**
- Total ativo: 43.538 (2024: 9.293) — crescimento de 369%, reflexo do ramp-up
- PL: 19.004 (2024: 7.026) — após aumento de capital de R$ 15.900 em 2025
- Prejuízos acumulados: (30.570) (2024: (26.648))
- Capital social: 49.574 (após aumentos aprovados em 4 tranches em 2025 totalizando R$ 20.900, com R$ 15.900 integralizados e R$ 5.000 a integralizar)

**Gestão de capital / suficiência regulatória:**
- PLA (Patrimônio Líquido Ajustado): 8.938 (deduzidas despesas diferidas de R$ 10.066)
- Capital regulatório exigido: 7.642 (maior entre capital base de 3.182 e capital baseado em risco de 7.642)
- **Suficiência de capital: R$ 1.296 mil** — margem bastante apertada, com PLA apenas R$ 1,3 mm acima do requerimento; o forte crescimento de carteira pressiona capital
(fonte: full/porto_seguro/2025/subsidiarias/portomed.md)

**Notas explicativas relevantes:**
- Partes relacionadas: passivo de R$ 5.305 mil para Porto Saúde (R$ 5.221) e Porto Cia. (R$ 84); despesas totais de R$ 12.209 mil com partes relacionadas (principalmente Porto Saúde com R$ 11.814)
- Receitas de partes relacionadas: R$ 8.166 mil da Porto Serviço — seguros de saúde contratados
- A sócia única Porto Saúde - Operações realizou grupamento de cotas (100 para 1) em setembro de 2025, simplificando a estrutura de capital

---

### 3.3 Porto Saúde - Operações de Saúde S.A.

**O que faz:** sub-holding intermediária constituída em junho de 2022. Objeto social: participar em sociedades que desenvolvam atividades no mercado de saúde. Controlada direta da Porto Saúde Participações S.A. Controla 100% de Porto Seguro - Seguro Saúde, Portomed e Porto Odonto.

**DRE 2025 — Controladora individual (R$ mil):**
- Equivalência patrimonial: 703.246 (2024: 340.565) — única receita relevante
- Despesas administrativas: (78) (2024: (74))
- Despesas com tributos: (28.719) (2024: 0) — este salto é material; deriva provavelmente de IR/CSLL sobre dividendos ou JCP recebidos das controladas
- Lucro operacional antes resultado financeiro: 674.449 (2024: 340.491)
- Resultado financeiro: (1) (negativo mínimo)
- IR/CSLL: (742)
- **Lucro líquido controladora: 673.719** (2024: 340.491), **+97,9%**

(fonte: full/porto_seguro/2025/subsidiarias/porto_saude_operacoes.md)

**Balanço patrimonial (controladora individual, R$ mil):**
- Capital social: 1.750.814 (2024: 1.409.557)
- PL individual: 2.242.555 — reflete investimento nas três controladas pelo método de equivalência patrimonial

**Dividendos e JCP pagos:** Em 2025 a Porto Saúde Operações pagou dividendos e JCP totais de R$ 261.687 mil (contra nenhum em 2024). Recebeu da controladora Porto Saúde Participações aumento de capital de R$ 117.950 mil.

**Eventos estruturais — reorganização societária (nota explicativa de ênfase do auditor da Azul/Participações):**
A Azul Companhia de Seguros Gerais (dentro do arquivo porto_saude_participacoes.md, mas pertencente a outra vertical) diminuiu emissões de apólices em 2025, concentrando negócios similares em verticais. Este evento não afeta diretamente a Porto Saúde Operações, mas é relevante para entender a estratégia de concentração vertical do Grupo.

---

### 3.4 Porto Saúde Participações S.A.

**O que faz:** holding de topo do segmento Saúde, controlada direta da Porto Seguro S.A. Sede: Av. Rio Branco, 1.475, Ed. Guaianazes, 8º andar, Sala 1, São Paulo. Detém 100% da Porto Saúde - Operações de Saúde S.A.

**DRE 2025 — Controladora (R$ mil):**
- Equivalência patrimonial: 693.019 (2024: 353.702) — única receita
- Despesas administrativas: (904) (2024: (285))
- Despesas com tributos: (25.822) (2024: 0)
- Lucro operacional antes financeiro: 666.293 (2024: 353.417)
- Resultado financeiro líquido: 13 (2024: 0)
- **Lucro líquido controladora: 666.306** (2024: 353.417), **+88,5%**

**DRE 2025 — Consolidado (R$ mil):**
- Receita de contrato de seguro: 8.202.759 (2024: 6.398.196)
- Receita de prestação de serviços: 142.829 (2024: 133.967)
- Outras receitas: 97.577 (2024: 76.031)
- **Total receitas consolidadas: 8.443.165** (2024: 6.608.194), **+27,8%**
- Despesas de seguros: (6.901.357) (2024: (5.485.963)), +25,8%
- Despesas administrativas: (617.790) (2024: (466.020))
- Despesas com tributos: (149.227) (2024: (72.435))
- Custo dos serviços: (53.033) (2024: (45.088))
- Outras despesas operacionais: (91.769) (2024: (86.517))
- **Lucro operacional antes financeiro: 629.234** (2024: 450.704)
- Resultado financeiro: 303.591 (= 329.773 receitas - 26.182 despesas) (2024: 132.698)
- Lucro antes IR/CSLL: 932.825 (2024: 583.402)
- IR/CSLL: (266.519) (2024: (229.985))
- **Lucro líquido consolidado: 666.306** (2024: 353.417), **+88,5%**

(fonte: full/porto_seguro/2025/subsidiarias/porto_saude_participacoes.md)

**Balanço patrimonial consolidado (R$ mil):**
- Total ativo: 4.449.759 (2024: 3.317.357)
- PL consolidado: 2.342.005 (2024: 1.754.700) — coincide com o controladora porque a holding não tem ativos operacionais além das participações
- Capital social: 1.750.814 (2024: 1.409.557)
- Reservas de lucros: 592.875 (2024: 342.740)

(fonte: full/porto_seguro/2025/subsidiarias/porto_saude_participacoes.md)

**Dividendos distribuídos em 2025:**
- Dividendos de reservas de lucros (2024): R$ 147.000 mil (27/02/2025)
- Dividendos de lucro do exercício 2025: R$ 97.589 mil (31/10/2025)
- JCP intercalares (2025): R$ 149.824 mil
- **Total saída de caixa a acionistas: R$ 279.902 mil** (contra zero em 2024)

**Reformas de capital:** aumento de capital de R$ 341.257 mil em 2025 (Porto Seguro S.A. injetou capital via Porto Saúde Participações → Porto Saúde Operações → Porto Seguro Saúde).

**Nota sobre Reserva Legal:** R$ 7.219 mil em dez/25 (2024: R$ 129.740 mil) — houve redução de capital de R$ 280.000 em setembro de 2025 seguida de aumento de capital de R$ 129.740, com variação líquida negativa de R$ 150.260 nas ações. Reservas estatutárias: R$ 39.926 (2024: R$ 147.324).

---

### 3.5 Porto Seguro Serviços Odontológicos Ltda.

**O que faz:** operadora de planos privados de assistência odontológica, regulada pela ANS. Constituída em 2011. Em 2025 a operação estava praticamente inativa — sem receitas operacionais de planos reportadas.

**DRE 2025 (R$ mil):**
- Outras despesas de operações de planos de assistência: (11) — sem receitas operacionais
- Resultado bruto: (11)
- Despesas administrativas: (61) (2024: (353)), redução de 82,7% — reflexo de run-down de estrutura
- Resultado financeiro: 43 (2024: 66)
- **Resultado líquido: (29)** (2024: (287)), melhora de 90%

(fonte: full/porto_seguro/2025/subsidiarias/porto_odontologicos.md)

**Balanço (R$ mil):**
- Total ativo: 504 (2024: 533)
- PL: 504 (2024: 533)
- Capital social: 1.675 (estável)
- Prejuízos acumulados: (1.171)

**Beneficiários:** O relatório da administração da Porto Saúde Participações menciona 1.184 mil vidas no seguro Odonto ao final do 4T25 (+189 mil vs. 4T24). Estas vidas, porém, aparecem contabilizadas na Porto Seguro Saúde S.A. (a seguradora), não na Porto Odonto Ltda. — que parece funcionar como veículo regulatório ANS para odonto mas não como operador ativo de carteira.

**Suficiência de capital:**
- PLA: 504 = PL (sem ajustes)
- Capital regulatório exigido: 398 (capital base)
- Suficiência: 106 — confortável dada a inatividade operacional

---

## 4. Achados Cross-Subsidiárias

### 4.1 Qual entidade concentra os lucros do segmento Saúde?

A **Porto Seguro - Seguro Saúde S.A.** concentra a quase totalidade dos resultados. Lucro líquido de R$ 705.125 mil em 2025 contra R$ (3.922) mil da Portomed e R$ (29) mil da Porto Odonto. A Porto Saúde Operações reporta lucro consolidado de R$ 666.306 mil — a diferença (~R$ 39 mm) reflete eliminações intercompany e tributos da sub-holding. A Porto Saúde Participações, no topo, reporta lucro de R$ 673.719 mil, refletindo equivalência sobre as controladas.

(fonte: full/porto_seguro/2025/subsidiarias/porto_seguro_saude.md; full/porto_seguro/2025/subsidiarias/portomed.md)

### 4.2 Seguradora vs. Operadora: quem é mais lucrativo em 2025 e por quê?

A **seguradora** (Porto Seguro Saúde S.A.) é substancialmente mais lucrativa. ROE de ~34% vs. prejuízo na operadora (Portomed). As razões são estruturais:
1. A seguradora tem massa crítica: R$ 8,17 bi em receitas vs. R$ 28,9 mm da Portomed. Portomed está em ramp-up — iniciou operações plenas em 2025.
2. A seguradora conseguiu reduzir sinistralidade de 77,3% para 75,9% em 2025 através de melhor seleção de risco, repricing e combate a fraudes (confirmado no relatório da administração).
3. A Portomed tem estrutura de custos desproporcionalmente alta para sua base de receita: despesas de comercialização de R$ 7.365 mil sobre receita de R$ 28.897 mil = 25,5% de custo de aquisição, reflexo de fase inicial de angariação de carteira.
4. A Portomed tem suficiência de capital apertada (R$ 1.296 mil de folga), o que limita crescimento e exige aportes contínuos.

(fonte: full/porto_seguro/2025/subsidiarias/porto_seguro_saude.md; full/porto_seguro/2025/subsidiarias/portomed.md)

### 4.3 Há cross-subsidização visível?

Sim, há fluxo intercompany bem documentado:

**Aportes de capital:** Em 2025, a cadeia de capitalização foi: Porto Seguro S.A. → Porto Saúde Participações (R$ 116.750 mm recebidos) → Porto Saúde Operações (R$ 117.900 mm recebidos/desembolsados) → Porto Seguro Saúde S.A. (R$ 232.000 mm de aumento de capital). A Portomed também recebeu R$ 15.900 mm de aumento de capital da Porto Saúde Operações. Em termos líquidos, a Porto Seguro Saúde é receptora de capital para suportar seu crescimento de carteira (+R$ 4 bi de provisões técnicas em um ano).

**Dividendos / JCP upstream:** A Porto Saúde Operações pagou R$ 291.305 mm de dividendos/JCP à Porto Saúde Participações, que por sua vez pagou R$ 279.902 mm à Porto Seguro S.A. Ou seja, a seguradora lucrativa (Porto Seguro Saúde) gera caixa → distribui para a sub-holding → que distribui para a holding do segmento → que flui para a Porto Seguro S.A.

**Transações operacionais (Porto Saúde Operações — nota 35):** a Porto Seguro Companhia de Seguros Gerais (a entidade multi-ramo) tem R$ 24.055 mm a receber da Porto Saúde como parte das transações entre partes relacionadas. Há também serviços de seguro saúde contratados entre entidades do grupo.

**Portomed recebe serviços de Porto Saúde (holding):** passivo de R$ 5.221 mil da Portomed para a Porto Saúde em dez/25, e despesas de R$ 11.814 mil com a Porto Saúde em 2025 — demonstra que parte da infraestrutura de gestão é centralizada e rateada.

(fonte: full/porto_seguro/2025/subsidiarias/porto_saude_operacoes.md; full/porto_seguro/2025/subsidiarias/portomed.md; full/porto_seguro/2025/subsidiarias/porto_saude_participacoes.md)

### 4.4 Escala do Odonto em relação ao segmento

A Porto Odonto Ltda. é marginal como entidade jurídica (ativo total de R$ 504 mil), mas o produto odonto do Grupo Porto tem 1.184 mil vidas ao final do 4T25. Isso indica que as apólices odonto são subscritas pela seguradora (Porto Seguro Saúde S.A.) — que tem autorização ampla — e não pela operadora Porto Odonto. A entidade CNPJ 13.991.711 existe provavelmente como veículo de autorização ANS para eventual migração de produto, mas está operacionalmente dormida.

### 4.5 Qual parte do "segmento Saúde" do release vem de qual entidade?

Com base nas DFs individuais:
- ~99%+ do resultado do segmento Saúde vem da **Porto Seguro - Seguro Saúde S.A.**: lucro de R$ 705 mm vs. prejuízo de R$ 4 mm da Portomed e R$ 0,03 mm da Porto Odonto.
- A receita consolidada do segmento (conforme release corporativo) é dominada pelas receitas de prêmios da seguradora (R$ 8,17 bi de R$ 8,44 bi consolidados).
- A **Portomed** representa menos de 0,4% da receita consolidada em 2025, mas é o vetor de crescimento futuro via canal empresarial de planos de saúde ANS — segmento distinto de seguro saúde.
- A **Porto Saúde Participações** e a **Porto Saúde Operações** são veículos de consolidação — seus resultados individuais (equivalência patrimonial) são artefatos da estrutura holding.

### 4.6 Trajetória de custo médico / sinistralidade — alerta

A sinistralidade da Porto Seguro Saúde S.A. melhorou em 2025 (75,9% vs. 77,3%), mas sinistros cresceram 25,4% (de R$ 4,89 bi para R$ 6,13 bi), acompanhando prêmios (+27,7%). O crescimento de provisões técnicas de R$ 11,9 bi para R$ 15,3 bi (+29%) em um único exercício é um sinal de alerta: a carteira está crescendo muito rápido e a PEONA saiu de R$ 384 mm para R$ 456 mm (+19%), sinal de que há volume crescente de sinistros incorridos mas não avisados. Em anos de ramp-up acelerado, a sinistralidade futura pode se revelar superior ao que as provisões contemplam, especialmente se a qualidade da carteira nova for inferior à maturada. O relatório da administração cita "combate a fraudes" e "vendas bem precificadas" como contribuidores, mas não divulga evidência quantitativa de adequação do TAP (Teste de Adequação do Passivo).

Para a Portomed especificamente: o índice de eventos (75,6%) já está em nível preocupante para uma operadora nova — tipicamente, operadoras em ramp-up têm sinistralidade mais alta porque ainda não têm equilíbrio atuarial. Combinado com a suficiência de capital apertada, o perfil regulatório da Portomed requer atenção.

(fonte: full/porto_seguro/2025/subsidiarias/porto_seguro_saude.md; full/porto_seguro/2025/subsidiarias/portomed.md)

---

## 5. Questões em Aberto (não respondidas pelas DFs individuais)

1. **Sinistralidade por produto vs. benchmark de mercado:** as DFs não segmentam sinistralidade por tipo de produto (individual vs. coletivo, PME vs. grandes empresas) nem comparam com ANS ou concorrentes (Bradesco Saúde, SulAmérica Saúde). O release corporativo pode ter essa abertura.

2. **Adequação das provisões técnicas (TAP):** o auditor identificou a mensuração das provisões técnicas como principal assunto de auditoria, mas as DFs individuais não evidenciam o resultado do TAP (aprovado sem ressalva). Para uma carteira crescendo 29% em um ano, a adequação do TAP é crítica.

3. **Ticket médio e mix etário de beneficiários:** as DFs reportam beneficiários em termos agregados (831 mil vidas). Não há abertura por faixa etária, regional ou produto — informação relevante para projetar sinistralidade futura.

4. **Contribuição do segmento Saúde ao resultado consolidado da Porto Seguro S.A.:** o digest cobre as subsidiárias individuais. A reconciliação com o resultado consolidado do Grupo Porto e o "segmento Saúde" do release management accounts requer leitura cruzada com a DFP consolidada de PSSA3.

5. **Estrutura de resseguro:** a Porto Seguro Saúde tem provisões líquidas de resseguro bem inferiores às brutas (R$ 15.135.611 vs. R$ 15.297.650 — diferença pequena de R$ 162 mm). O nível de proteção via resseguro parece baixo para uma carteira de R$ 8 bi; o release pode esclarecer se há coberturas de stop-loss ou XL contratados.

6. **Portomed — estratégia de crescimento:** a operadora está claramente sendo incubada para escalar, mas as DFs não revelam o horizonte de breakeven ou o target de beneficiários. A suficiência regulatória apertada (R$ 1,3 mm de folga) pode sinalizar que um novo aporte de capital está planejado.

7. **Porto Odonto — intenção de ativação:** 1.184 mil vidas no produto odonto mas a operadora CNPJ tem ativos de R$ 504 mil. Não está claro se há plano de migrar a carteira odonto para a entidade regulatória específica ou se o produto continuará sendo subscrito pela seguradora de saúde.
