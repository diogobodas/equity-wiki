---
type: concept
aliases: [Valor Geral de Vendas, VGV]
sources:
  - sources/digested/cury_release_4T25_summary.md
  - sources/digested/cury_previa_operacional_1T26_summary.md
  - sources/digested/cyrela_release_4T25_summary.md
  - sources/digested/direcional_release_4T25_summary.md
  - sources/digested/tenda_release_4T25_summary.md
  - full/tenda/1T26/previa_operacional.md
  - sources/digested/HB_historical series_4Q25_summary.md
  - sources/digested/cyrela_fatos_relevantes_batch_summary.md
  - sources/digested/cyrela_lancamentos_summary.md
  - full/generic/cyrela_lancamentos.md
created: 2026-04-08
updated: 2026-04-13
---

# VGV

**Valor Geral de Vendas** — métrica-chave de incorporadoras brasileiras. É o valor *potencial* de venda de um conjunto de unidades imobiliárias, calculado multiplicando o número de unidades pelo preço médio de venda esperado.

Usado em quatro recortes principais no ciclo de uma incorporadora:

1. **VGV lançado** — potencial de venda dos empreendimentos lançados no período. Indica a aposta comercial da empresa.
2. **VGV vendido (bruto / líquido)** — valor das unidades efetivamente contratadas no período, antes (bruto) e depois (líquido) de [[distrato|distratos]]. É o "top-line" operacional real.
3. **VGV repassado** — valor das unidades cujo financiamento do comprador foi transferido para o banco (Caixa/SBPE). É quando a incorporadora *de fato* recebe o caixa da venda.
4. **VGV do banco de terrenos** — potencial futuro de vendas embutido no landbank. Mede a capacidade de sustentar lançamentos futuros.

A diferença entre VGV vendido e VGV repassado captura o *working capital trapped* em unidades vendidas mas ainda não financiadas — por isso, em incorporadoras focadas em baixa renda como a [[tenda]], volume de [[repasses|repasse]] é o driver direto da geração de caixa (fonte: full/tenda/1T26/previa_operacional.md §repasses_entregas_obras).

## VGV pro forma vs. VGV %Cyrela (% participação)

Como incorporadoras lançam projetos via SPEs com sócios (terrenistas em permuta, parceiros financeiros, JVs operacionais), o VGV pode ser reportado em **dois critérios**:

- **VGV pro forma (100%)** — soma do VGV total de cada empreendimento independentemente da participação econômica da incorporadora na SPE. É a métrica usada para dimensionar o pipeline operacional e a "presença" da empresa no mercado.
- **VGV %Cyrela / %Co / %CBR** — VGV ponderado pela participação econômica da incorporadora em cada SPE (campo `% CBR` na base bottom-up). É a métrica que casa com a receita futura efetivamente apropriável pela companhia.

A [[cyrela]] é o exemplo mais explícito: a base proprietária de lançamentos cobre 1.332 empreendimentos de 1T05 a 4T25, com a marcação **"DADOS A PARTIR DO 4T20 (PRO FORMA)"** — a partir desse trimestre os números reportados refletem 100% das SPEs consolidadas, em vez do critério gerencial anterior baseado em % participação (fonte: digested/cyrela_lancamentos_summary.md). Reconciliar os dois critérios é etapa obrigatória ao construir um modelo de receita: o VGV pro forma vai para indicadores operacionais (VSO, market share, mix de segmento), enquanto o VGV %Cyrela alimenta projeções de receita líquida e EBITDA.

A diferença entre os dois critérios pode ser material em incorporadoras com forte uso de permuta (vide [[direcional]], 87% do landbank em permuta) ou JVs (Cyrela com marcas como `Wish`/`Now`/`Smart` em parceria com Plano&Plano, MAC e Lavvi) (fonte: digested/cyrela_lancamentos_summary.md).

## Comparativo de VGV — incorporadoras listadas (2025)

| Métrica | [[cury|Cury]] | [[cyrela|Cyrela]] | [[direcional|Direcional]] | [[tenda|Tenda]] |
|---|---|---|---|---|
| VGV lançado (ano) | R$ 8,28 bi | R$ 18,6 bi | R$ 6,9 bi | — |
| VGV vendido líquido (ano) | R$ 7,75 bi | R$ 13,2 bi | R$ 6,2 bi | — |
| VGV lançado (4T25) | R$ 1,29 bi | R$ 4,5 bi | R$ 1,9 bi | R$ 1,71 bi |
| VGV vendido líquido (4T25) | R$ 1,56 bi | R$ 3,3 bi | R$ 1,5 bi | R$ 1,10 bi |
| [[vso|VSO]] UDM | 76,3% | 45,2% | 21,0% | — |
| [[banco_de_terrenos|Landbank]] (VGV) | R$ 24,6 bi | R$ 19,8 bi | R$ 58,5 bi | R$ 28,6 bi |

Fontes: (fonte: digested/cury_release_4T25_summary.md), (fonte: digested/cyrela_release_4T25_summary.md), (fonte: digested/direcional_release_4T25_summary.md), (fonte: digested/tenda_release_4T25_summary.md).

## Exemplos por empresa

### Cury

Em 2025, a [[cury]] lançou 37 empreendimentos com VGV total de R$ 8,28 bi (+26% A/A), enquanto vendas líquidas alcançaram R$ 7,75 bi (+26%) — uma [[vso]] UDM de 76,3%, a mais alta entre as listadas (fonte: digested/cury_release_4T25_summary.md). No 1T26, lançamentos atingiram VGV de R$ 2,65 bi (+105% T/T) com preço médio de R$ 330,8 mil/unidade, e o [[banco_de_terrenos]] atingiu recorde de R$ 24,9 bi (fonte: digested/cury_previa_operacional_1T26_summary.md). O perfil [[mcmv]] é dominante: 86,5% das vendas com preço até R$ 500 mil (fonte: digested/cury_previa_operacional_1T26_summary.md).

### Cyrela

A [[cyrela]] lançou R$ 18,6 bi em VGV em 2025 (+43% A/A), o maior volume absoluto entre as listadas. No 4T25, foram R$ 4,5 bi em 21 projetos, com queda de 33% A/A refletindo seletividade e base alta do 4T24 (fonte: digested/cyrela_release_4T25_summary.md). O landbank encerrou em R$ 19,8 bi (94% no Centro-Sudeste), com aquisições de R$ 5,3 bi apenas no trimestre (fonte: digested/cyrela_release_4T25_summary.md).

No 1T26, lançamentos recuaram para R$ 2,43 bi (100%) em 12 empreendimentos — queda de 50% vs. 1T25 (R$ 4,86 bi), possivelmente refletindo calendário de aprovações e sazonalidade. Vendas líquidas foram mais resilientes, em R$ 2,94 bi (−3% A/A), com alta de 2% ex-permuta (%CBR). A VSO 12 meses estabilizou em 45,8% (vs. 45,2% no 4T25), interrompendo a trajetória de queda que vinha desde 52,6% no 1T25. [[mcmv]] ganhou participação no mix de lançamentos, representando ~40% do VGV lançado no trimestre (fonte: digested/cyrela_fatos_relevantes_batch_summary.md).

A base bottom-up de lançamentos da Cyrela (1T05–4T25) permite reconstruir o mix de segmento ao longo do tempo. A entrada da marca **Vivaz** (segmento [[mcmv]]) ocorre por volta de 2018 e ganha peso até 2025, com várias dezenas de lançamentos Vivaz por trimestre no 4T25. A nomenclatura do segmento econômico mudou de "CVA 2 e 3" (até 4T22) para "MCMV 2 e 3" (a partir de 1T23), refletindo o relançamento do programa em 2023 (fonte: digested/cyrela_lancamentos_summary.md). Geograficamente, há concentração em São Paulo (capital + Interior + Campinas), mas com presença relevante em RJ (operação `RJZ Cyrela`), Sul, Centro Oeste, e participações pontuais em Nordeste, MG e ES desde 2005 (fonte: digested/cyrela_lancamentos_summary.md).

### Direcional

A [[direcional]] lançou R$ 6,9 bi em VGV em 2025 (+25% A/A) e vendeu R$ 6,2 bi (+3%), com VSO consolidada de 21% (fonte: digested/direcional_release_4T25_summary.md). Destaque para o landbank de R$ 58,5 bi — o maior entre as [[incorporadoras]] listadas — com 241 mil unidades e 87% adquirido via permuta (custo de aquisição de apenas 11% do VGV). O estoque total era de R$ 5,7 bi (15,8 mil unidades) (fonte: digested/direcional_release_4T25_summary.md). A controlada [[riva]] contribui com parcela relevante dos lançamentos e vendas.

### Tenda

A [[tenda]] lançou R$ 1,71 bi em VGV no 4T25 (14 empreendimentos) e registrou vendas líquidas de R$ 1,10 bi (+19,2% A/A) (fonte: digested/tenda_release_4T25_summary.md). O landbank consolidado atingiu R$ 28,6 bi (775 empreendimentos, 135,7 mil unidades), com 73,9% em permuta. A margem de novas vendas de 36,5% (marca Tenda) e margem REF de 41,9% indicam boa qualidade do VGV contratado recentemente (fonte: digested/tenda_release_4T25_summary.md).

## Contexto setorial — universo amplo de incorporadoras

A série histórica setorial (1T09–4T25) cobre ~20 [[incorporadoras]] listadas e permite situar o VGV das quatro empresas acima no contexto do setor completo (fonte: digested/HB_historical series_4Q25_summary.md).

**Segmentação low-income vs. mid/high-income** — o setor opera em dois clusters distintos de VGV. No segmento popular (low-income), além de Cury, Direcional e Tenda, destacam-se MRV (MRVE3) e Plano&Plano (PLPL3). No mid/high-income, além da Cyrela, atuam EZTec (EZTC3), Even (EVEN3), Lavvi (LAVV3), Moura Dubeux (MDNE3), Melnick (MELK3), Mitre (MTRE3), Trisul (TRIS3) e Helbor (HBOR3) (fonte: digested/HB_historical series_4Q25_summary.md).

**Máximas históricas em low-income** — o segmento popular atingiu níveis recordes de lançamentos em 2024–2025, impulsionado pelo programa [[mcmv]]. A Tenda acelerou para R$ 1,8 bi no 4T25, consolidando a recuperação após a crise de 2022, enquanto Lavvi e Moura Dubeux ultrapassaram R$ 800 mi/tri em lançamentos no mid/high (fonte: digested/HB_historical series_4Q25_summary.md).

**Liderança absoluta em VGV** — Cyrela lidera lançamentos no mid/high com R$ 3,3 bi no 4T25 (100%), acumulando ~R$ 14,4 bi em 2025. No low-income, Cury lidera com R$ 1,2 bi no 4T25 (%Co) e lançamentos anuais superando R$ 7,5 bi. Direcional mantém ritmo consistente de R$ 1,4–1,8 bi/tri no segmento popular (fonte: digested/HB_historical series_4Q25_summary.md).

## Dinâmicas relevantes

**Preço médio como alavanca de VGV** — reajustes de preço dentro do teto [[mcmv]] são a principal alavanca de crescimento de VGV para incorporadoras de baixa renda. A Cury elevou preço médio de vendas para R$ 325,4 mil/unidade no 1T26 (+4,9% A/A) (fonte: digested/cury_previa_operacional_1T26_summary.md).

**Permuta e custo do landbank** — quanto maior a proporção de terrenos adquiridos via permuta, menor o capital investido por R$ de VGV futuro. Direcional (87% permuta) e Tenda (73,9% permuta) operam com landbanks asset-light (fonte: digested/direcional_release_4T25_summary.md) (fonte: digested/tenda_release_4T25_summary.md).

**VGV lançado vs. vendido e estoque** — quando lançamentos superam sistematicamente as vendas, o estoque acumula. A Cyrela lançou R$ 18,6 bi mas vendeu R$ 13,2 bi em 2025, e a [[vso]] 12 meses recuou de 55% para 45% (fonte: digested/cyrela_release_4T25_summary.md). Já a Cury mantém VSO UDM acima de 70%, operando com estoque baixo e giro rápido (fonte: digested/cury_release_4T25_summary.md).

Relacionado: [[vso]], [[distrato]], [[banco_de_terrenos]], [[repasses]], [[incorporadoras]], [[mcmv]], [[resultado_a_apropriar]]
