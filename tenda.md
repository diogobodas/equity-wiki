---
type: entity
aliases: [Construtora Tenda, Tenda, TEND3, Alea]
sources: [full/tenda/1T26/previa_operacional.md, structured/tenda/1T26/previa_operacional.json, full/tenda/data_pack_1T26.md, structured/tenda/{1T11..1T26}/data_pack.json, full/tenda/2025/dfp.md, structured/tenda/2025/dfp.json]
created: 2026-04-08
updated: 2026-04-08
---

# Tenda

**Construtora Tenda S.A.** (B3: **TEND3**, Novo Mercado) — uma das principais incorporadoras brasileiras focadas em **habitação popular**, operando predominantemente na [[mcmv|Minha Casa Minha Vida Faixa 1]]. Atua em nove regiões metropolitanas do país (fonte: full/tenda/1T26/previa_operacional.md §sobre_a_tenda).

É a única *pure-play* listada de MCMV Faixa 1 no Brasil — as demais incorporadoras grandes do segmento misturam Faixa 1 com faixas superiores ou SBPE.

## Estrutura — Tenda + Alea

A companhia opera em dois segmentos:

- **Tenda (MCMV Faixa 1)** — core do negócio. Habitação popular subsidiada, preço médio de venda ~R$ 237 mil/unidade no 1T26 (fonte: structured/tenda/1T26/previa_operacional.json :: company_specific.segmentos.tenda_mcmv.vendas_brutas.preco_medio_unidade).
- **Alea (SBPE)** — marca/subsidiária 100% Tenda, criada para diversificar a exposição para fora do MCMV. Atua em classe média-baixa via financiamento SBPE. Ticket médio ~R$ 198 mil/unidade no 1T26.

O consolidado Tenda+Alea é o que a empresa reporta como "Consolidado" em todas as tabelas. Alea representa ~21% do [[banco_de_terrenos|banco de terrenos]] consolidado em VGV (fonte: full/tenda/1T26/previa_operacional.md §destaques_alea).

## Destaques operacionais 1T26

Dados da [[#prévia operacional 1t26|prévia operacional 1T26]], divulgada em 07-abr-2026 (preliminares, sujeitos a revisão).

**Tenda (MCMV) — recordes históricos ex-Pode Entrar:**

- Vendas brutas **recorde** de R$ 1.579,4 mm, +44,3% A/A (fonte: structured/tenda/1T26/previa_operacional.json :: company_specific.segmentos.tenda_mcmv.vendas_brutas.vgv).
- Vendas líquidas **recorde histórico ex-Pode Entrar** de R$ 1.428,0 mm, +44,5% A/A.
- [[vso|VSO líquida]] 26,9% (+4,3 p.p. T/T).
- [[repasses|VGV repassado]] R$ 1.021,2 mm, +43,4% A/A — empresa atribui geração de caixa positiva do trimestre ao alto volume de repasse (fonte: full/tenda/1T26/previa_operacional.md §repasses_entregas_obras).
- [[banco_de_terrenos|Banco de terrenos]] **recorde** de R$ 23,4 bi em VGV (+28,3% A/A), com 60,7% em permuta.
- Lançamentos: 13 empreendimentos, VGV R$ 1.409,2 mm (+72,2% A/A), preço médio R$ 231,7 mil/un (+2,8% A/A).
- Primeiro empreendimento no estado da **Paraíba** (março/2026, 464 unidades, R$ 268,4 mil/un) — expansão geográfica (fonte: full/tenda/1T26/previa_operacional.md §destaques_tenda).

**Alea (SBPE) — VSO acelerando:**

- VSO líquida 41,6% (vs 18,0% no 1T25) — +23,6 p.p. A/A (fonte: structured/tenda/1T26/previa_operacional.json :: company_specific.segmentos.alea_sbpe.vendas_liquidas.vso_liquida).
- Vendas líquidas R$ 105,1 mm (+5,1% A/A).
- Lançamentos retraídos (2 empreendimentos, R$ 47,4 mm, vs R$ 96,0 mm no 1T25).
- Banco de terrenos R$ 6,2 bi, 98% em permuta.

**Consolidado:** VGV lançado R$ 1.456,6 mm, vendas brutas R$ 1.701,0 mm, vendas líquidas R$ 1.533,0 mm, VSO líquida 27,6%, banco de terrenos R$ 29,7 bi.

## Arco histórico 2020–2025 — ciclo de quase-quebra e turnaround

O data pack de RI (fonte: full/tenda/data_pack_1T26.md) cobre 1T11 a 1T26. Os anos fechados mais relevantes para modelagem contam um arco bem marcado:

| Ano | Receita Líq (R$ mm) | Margem Bruta | EBITDA Aj | Lucro Líq | ROE LTM | Dívida Líq |
|---|---:|---:|---:|---:|---:|---:|
| 2020 | 2.282,4 | 31,1% | 330,0 | +200,3 | 14,0% | (148,3) |
| 2021 | 2.540,0 | 17,8% | (4,7) | (191,5) | (14,1%) | 331,8 |
| 2022 | 2.412,6 | 11,4% | (203,8) | **(547,3)** | (57,1%) | 799,9 |
| 2023 | 2.903,1 | 21,0% | 217,5 | (95,8) | (12,2%) | 461,3 |
| 2024 | 3.284,4 | 27,1% | 481,1 | +106,4 | 11,8% | 192,2 |
| 2025 | 4.173,4 | 30,1% | 686,1 | **+505,7** | 47,1% | 266,0 |

Fontes: `structured/tenda/{ano}/data_pack.json :: canonical.dre` e `canonical.financeiro_ajustado`.

**O que aconteceu:**

1. **2020 — base saudável.** ROE 14%, dívida líquida *negativa* (caixa líquido), margem bruta 31%. Era uma Tenda diferente, "normal".
2. **2021–2022 — colapso.** Inflação de custos de construção pós-pandemia (INCC disparando), rigidez de preços no MCMV faixa 1 (plafonds subsidiados pela Caixa mudam devagar), estoque antigo com margem espremida. Margem bruta despenca para 11,4% em 2022; EBITDA ajustado fica negativo em R$ 204 mm; **prejuízo recorde de R$ 547 mm em 2022**; dívida líquida cresce para R$ 800 mm. ROE chega a **−57%**. A companhia precisou fazer **redução de capital** — por isso o schema e o data pack tracking `divida_liquida_ajustada` separado (considerando a obrigação de pagamento por redução de capital) até hoje (fonte: full/tenda/data_pack_1T26.md §consolidado_financeiro :: Dívida Líquida).
3. **2023 — estabilização operacional, resultado ainda negativo.** EBITDA volta a positivo (R$ 217 mm), mas o lucro líquido segue negativo (−R$ 96 mm) por conta de resultado financeiro e desalavancagem ainda incompleta.
4. **2024 — volta ao lucro.** Receita +13%, margem bruta sobe para 27%, EBITDA ajustado mais do que dobra (R$ 481 mm), lucro líquido positivo (R$ 106 mm), dívida líquida cai para R$ 192 mm.
5. **2025 — turnaround completo.** Receita R$ 4,17 bi (+27% A/A), margem bruta 30% (nível 2020), EBITDA ajustado R$ 686 mm (+43%), **lucro líquido R$ 505 mm, ROE LTM 47%**, ROCE LTM 36%. Dívida líquida sobe levemente para R$ 266 mm mas relativamente baixa contra PL de R$ 1,2 bi.

**Implicação para modelagem:** qualquer série histórica pré-2024 é de uma Tenda *estruturalmente diferente* em margem e rentabilidade. Séries de múltiplos históricos são enganosas quando incluem 2021-2023. A base de comparação honesta para premissas forward começa em 2024/2025.

## Pontos não-triviais para modelagem

1. **Exposição a MCMV é estrutural, não opcional.** A tese da Tenda não é "incorporadora que também faz popular" — é uma operação desenhada em torno da logística do MCMV (funding via Caixa, ticket baixo, giro alto, padronização de produto). Isso a protege de ciclos de Selic mas a expõe diretamente a risco político do programa.

2. **Disciplina de capital no landbank.** Tenda declara que mesmo os terrenos adquiridos em caixa têm **>90% do pagamento atrelado à obtenção do registro de incorporação** (fonte: full/tenda/1T26/previa_operacional.md §banco_de_terrenos). É um mitigador estrutural pouco comum no setor — reduz risco de caixa comprometido em terrenos que não viram obra.

3. **Pode Entrar como ruído histórico.** O Programa Habitacional "Pode Entrar" (prefeitura de SP) inflou o 3T24 em R$ 531 mm de vendas brutas e R$ 532 mm de vendas líquidas (fonte: structured/tenda/1T26/previa_operacional.json :: company_specific.pode_entrar). Qualquer série histórica precisa tratar o 3T24 com/sem Pode Entrar — a empresa reporta métricas ex-Pode Entrar como base de comparação "limpa".

4. **Repasse como driver de caixa** — Tenda vincula explicitamente geração de caixa ao volume de repasses, não à margem nominal. Modelar fluxo de caixa operacional usando repasse efetivo, não receita POC.

5. **Alea em "transição de mix"** — lançamentos caindo em VGV mas VSO subindo forte: indica queima de estoque acumulado, não expansão. Atenção para quando o fluxo de lançamentos SBPE será retomado.

## Governança e IR

- Listada no **Novo Mercado** da B3 (nível máximo de governança).
- **CFO / DRI:** Luiz Mauricio de Garcia.
- **Coordenador de RI:** Leonardo Dias Wanderley.
- **Analista de RI:** Felipe Chiavegato Stella.
- Website RI: ri.tenda.com | Contato: ri@tenda.com (fonte: full/tenda/1T26/previa_operacional.md §relações_com_investidores).

## DFP 2025 auditada — o que destravou

A DFP 2025 (fonte: full/tenda/2025/dfp.md) é a **primeira fonte auditada** digerida nesta wiki. Cross-check com o data_pack confirma receita, lucro, PL e dívida líquida ±0. O DFP adiciona:

- **DFC completa** (primeira série no structured/): CFO consolidado 2025 R$ 290,3 mm (vs R$ 542,2 mm em 2024) — queda por forte expansão de capital de giro (Δ contas a receber R$ (559) mm + Δ imóveis R$ (725) mm compensados por Δ obrigações de compra de imóveis R$ +706 mm) (fonte: structured/tenda/2025/dfp.json :: canonical).
- **Notas explicativas 1–25** com: cessão de créditos (Nota 4), SWAPs (Nota 11), debêntures detalhadas com covenants (Nota 10), IR/RET (Nota 15), contingências (Nota 16), PL e stock grant (Nota 17), segmentação (Nota 24).
- **Segmentação contábil auditada on-site vs off-site** (Nota 24): segmento Tenda (on-site) **lucrou R$ 636 mm** em 2025; segmento Alea (off-site) **perdeu R$ 152 mm**. O consolidado de R$ 506 mm é líquido desse arrasto (fonte: full/tenda/2025/dfp.md §nota_24).

**Observações críticas adicionais da DFP 2025:**

1. **Prejuízo fiscal não reconhecido R$ 2,67 bi** (crédito fiscal R$ 906,7 mm). Não contabilizado porque o RET domina e não há perspectiva de Lucro Real. Alíquota efetiva 2025 = **1,23%** — baixa estrutural enquanto mix RET persistir (fonte: full/tenda/2025/dfp.md §nota_15).
2. **SWAP TEND3 inflou o resultado financeiro** em ~R$ 180 mm (receita de SWAP R$ 135 mm em 2025 vs despesa R$ 45 mm em 2024). **Resultado financeiro ex-SWAP**: R$ (130,6) mm — este é o nível forward-looking coerente com dívida líquida R$ 266 mm a CDI+spread (fonte: full/tenda/2025/dfp.md §nota_11 e §nota_22).
3. **13ª emissão de debêntures** em 31/10/2025: R$ 300 mm, vencimento bullet 2030/2031/2032. Elevou debêntures consolidadas de R$ 541 → R$ 993 mm. Duration total da dívida 24,2 meses, custo médio nominal 13,67% a.a. Covenants folgadíssimos: (4,53)% vs limite 15% (fonte: structured/tenda/2025/dfp.json :: company_specific.debentures_detalhe).
4. **Dividendos 2025 totais de R$ 150 mm** (R$ 50 mm pagos em 30/12/2025 + R$ 100 mm pagos em 07/01/2026). Payout 29,7% do lucro líquido consolidado (fonte: full/tenda/2025/dfp.md §nota_17).

## Limitações de cobertura atual nesta wiki

Digeridos até agora:
- **Prévia operacional 1T26** (só operacional, preliminar).
- **Data pack de RI as-of 1T26** — histórico completo 1T11–1T26 de operacional, DRE, BP e financeiro ajustado (consolidado + segmentos). Cobre toda a espinha numérica para modelagem histórica.
- **DFP 2025 auditada** — DFs individuais+consolidadas, DFC, notas explicativas completas e segmentação contábil on-site/off-site.

Ainda faltam:
- **Release completo do 1T26** (MD&A, release narrativo — o data pack não cobre o 1T26 financeiro porque o release fechado ainda não saiu).
- **Apresentações institucionais** e **transcripts de call**.
- **Fluxo de caixa** — não aparece no data pack, só implícito via variação de dívida líquida e caixa. Virá via DFP/ITR.

## Histórico operacional disponível

Série de 9 trimestres (1T24–1T26) de preço médio de lançamento, VGV vendas brutas, VSO bruta, VGV vendas líquidas e VSO líquida — separado por segmento Tenda e Alea, com splits do 3T24 para isolar o Pode Entrar. Armazenado em `structured/tenda/1T26/previa_operacional.json :: company_specific.historico_operacional_tenda_mcmv` e `..._alea_sbpe`.

Relacionado: [[incorporadoras]], [[mcmv]], [[vgv]], [[vso]], [[distrato]], [[repasses]], [[banco_de_terrenos]]
