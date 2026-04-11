---
type: sector
aliases: [Incorporação imobiliária, Construtoras e incorporadoras, Real estate developers]
sources:
  - sources/full/tenda/1T26/previa_operacional.md
  - sources/full/tenda/2025/dfp.md
  - sources/full/direcional/4T25/release.md
  - sources/full/cury/2025/dfp.md
  - sources/full/cury/4T25/release.md
  - sources/full/cury/1T26/previa_operacional.md
  - sources/structured/tenda/4T25/release.json
  - sources/structured/direcional/4T25/release.json
  - sources/structured/cury/2025/dfp.json
  - sources/structured/cury/4T25/release.json
created: 2026-04-08
updated: 2026-04-11
---

# Incorporadoras

Setor de **incorporação imobiliária residencial** brasileiro — empresas que compram terrenos, lançam, vendem, constroem e entregam unidades residenciais. Ciclo longo de capital (tipicamente 2–4 anos do lançamento à entrega), intensivo em working capital, sensível a juros, inflação de custo de construção (INCC) e demanda imobiliária.

## Segmentações do setor

A principal segmentação é **por faixa de renda do comprador**, que determina o modelo de funding do comprador e a dinâmica de margens:

- **Habitação popular ([[mcmv|MCMV]] Faixa 1/2)** — ticket baixo, demanda subsidiada via MCMV, funding do comprador pela Caixa, [[vso]] alta, margens menores por unidade mas giro alto. Menos sensível à Selic. Players: [[tenda|Tenda]] (pure-play), [[direcional|Direcional]], MRV.
- **Média renda (MCMV Faixa 2/3/4 + [[sbpe|SBPE]])** — ticket intermediário, funding misto, sensibilidade maior a juros. Players: [[cury|Cury]] (SP+RJ, pure MCMV médio), [[riva|Riva]] (subsidiária Direcional), Plano&Plano, MRV, [[alea|Alea]] (subsidiária Tenda — em reestruturação).
- **Alta renda (SBPE puro)** — ticket alto, sem subsídio, funding 100% privado, ciclo longo, alta sensibilidade a juros e confiança do consumidor. Players: Cyrela, EzTec, Even, Helbor, Mitre.

## Métricas operacionais-chave (antes das DFs)

O ciclo de uma incorporadora é lido por métricas operacionais que antecedem o reconhecimento contábil (que segue POC — percentage of completion):

1. **[[vgv]] lançado** — aposta comercial do período.
2. **Vendas brutas** (VGV e unidades) — contratação do período.
3. **[[distrato]]s** — rescisões; diferença entre venda bruta e líquida.
4. **[[vso]] bruta e líquida** — velocidade de absorção da oferta.
5. **[[repasses]]** — momento em que o caixa efetivamente entra.
6. **Entregas** — final do ciclo; libera capital imobilizado na obra.
7. **Obras em andamento** — carteira de execução.
8. **[[banco_de_terrenos]]** — matéria-prima de lançamentos futuros; composição caixa vs permuta é leitura de disciplina de capital.
9. **[[resultado_a_apropriar|Resultado a apropriar (REF)]]** — backlog de margem bruta, indicador antecedente da margem DRE dos próximos trimestres.

Todas essas métricas são publicadas em **prévias operacionais** trimestrais (caminho rápido, 1–2 semanas após o fim do trimestre) antes do release completo com DFs. Para modelagem, a prévia dá a espinha operacional; o release completo fecha o quadro com DRE, BP e FC.

## Drivers setoriais

- **[[selic|Selic]]** — afeta diretamente SBPE/média/alta renda (custo do financiamento do comprador) e indiretamente o MCMV (custo de capital da incorporadora, atratividade de ativos alternativos).
- **INCC** — inflação de custo de construção; pressiona margem bruta, especialmente em Faixa 1 onde os plafonds da Caixa são rígidos.
- **Emprego e renda** — driver direto de demanda e de distratos.
- **Regulação do MCMV** — risco político central para players focados em baixa renda. Mudanças recentes em 2T25: atualização de faixas de renda, criação da [[mcmv_faixa_4|Faixa 4]] (renda até R$ 12 mil, imóvel até R$ 500 mil), ampliação de limites de preço.
- **[[reforma_tributaria|Reforma tributária]]** — CBS a partir de 2027, vista como estruturalmente positiva.
- **Disponibilidade de funding (FGTS, Caixa)** — condição necessária para Faixa 1/2.

## Players cobertos nesta wiki

| Player | Ticker | Foco | Receita 2025 | MBA 2025 | Lucro 2025 | ROE LTM |
|---|---|---|---:|---:|---:|---:|
| [[cury]] | CURY3 | MCMV médio (SP+RJ) + SBPE premium | R$ 5,40 bi | **39,8%** | **R$ 975 mm** | **78,8%** |
| [[tenda]] | TEND3 | MCMV Faixa 1 (pure-play) + [[alea\|Alea]] SBPE | R$ 4,17 bi | 30,1% | R$ 506 mm | 47,1% |
| [[direcional]] | DIRR3 | MCMV Faixa 1/2 + [[riva\|Riva]] média renda | R$ 4,34 bi | 42,1% | R$ 789 mm | 44% |

Fontes: (fonte: structured/cury/2025/dfp.json :: canonical.dre), (fonte: structured/tenda/2025/dfp.json :: canonical.dre), (fonte: structured/direcional/2025/release.json :: canonical.dre).

**Leitura cross-company:** as três empresas estão em patamares de ROE muito acima da média do setor (~15-25%), mas a Cury opera em um nível absolutamente à parte — **ROE 78,8%** é sem precedente para uma incorporadora listada brasileira ou global. A combinação de receita maior (R$ 5,4 bi vs ~R$ 4,2 bi dos pares), margem bruta forte (39,8% — intermediária entre Tenda 30,1% e Direcional 42,1%) e **base de PL deliberadamente baixa** (payout ~138% em 2025, via follow-on + dividendos extraordinários) é o que produz o ROE excepcional. Ver [[cury_vs_direcional]] para comparação detalhada entre os dois modelos de alta rentabilidade no MCMV médio, e [[tenda_vs_direcional]] para análise da Tenda vs Direcional.

## Tendências visíveis nos dados 2025

1. **Turnaround consolidado pós-crise 2021-2023.** Tenda retornou ao lucro (R$ 506 mm vs prejuízo R$ 547 mm em 2022) e Direcional entregou recordes consecutivos. A Cury atravessou o ciclo 2022 (único ano de compressão — margem líquida caiu para 14,6%) e entregou 3 anos consecutivos de expansão de margens (38,0% → 39,8% na bruta, 16,7% → 18,1% na líquida). O ciclo de quase-quebra do setor MCMV Faixa 1 está oficialmente fechado nos nomes líderes (fonte: full/tenda/data_pack_1T26.md, full/direcional/4T25/release.md, full/cury/2025/dfp.md).

2. **Distratos em alta.** Todas as empresas reportaram aumento de distratos em 2025-1T26. Direcional saltou de 8,3% (2024) para 12,8% (2025). Cury subiu de 5,4% (1T25, recorde baixo) para 9,0% no 1T26. Ponto de atenção setorial — reflete base maior de vendas + ambiente de crédito mais seletivo, mas tendência merece monitoramento (fonte: full/direcional/4T25/release.md §distratos, full/cury/1T26/previa_operacional.md §distratos).

3. **Bancos de terrenos recordes.** Direcional com R$ 58,5 bi (87% permuta), Tenda com R$ 28,6 bi (73,9% permuta) e Cury com R$ 24,9 bi (geográfico SP+RJ) em 4T25/1T26, cobrindo 3-9 anos de lançamentos no ritmo atual. Setor bem posicionado para ciclo de crescimento 2026-2028.

4. **Debêntures e CRI como captação padrão.** Ambas as empresas recorreram a emissões de debêntures e cessões pro-soluto de recebíveis (CRIs) como funding primário em 2025. Custo médio 12-14% a.a., duration alongada para 24-64 meses.

5. **Dividendos extraordinários por reforma tributária.** Direcional antecipou R$ 804 mm em dez/2025 por mudança na Lei 15.270/2025, e a Cury distribuiu R$ 1,35 bi no ano (R$ 573 mm em dez/2025) — neste último caso, financiado por follow-on primário de R$ 574 mm (arranjo atípico de reciclagem de equity). Movimento setorial esperado (fonte: full/direcional/4T25/fato_relevante_1.md, full/cury/4T25/fato_relevante_02.md).

6. **MCMV Faixa 4** — Conselho Curador do FGTS criou a nova faixa (renda até R$ 12 mil, imóvel até R$ 500 mil) em 2T25. Beneficia direto [[riva|Riva]] e potencialmente [[alea|Alea]], além de abrir mercado endereçável para players de média renda (fonte: full/direcional/1T25/release.md §mcmv).

## Comparações disponíveis

- [[tenda_vs_direcional]] — comparação detalhada TEND3 vs DIRR3 (margens, operacional, balanço, estratégia).
- [[cury_vs_direcional]] — comparação detalhada CURY3 vs DIRR3, as duas empresas de média renda mais rentáveis do setor.

Relacionado: [[vgv]], [[vso]], [[distrato]], [[repasses]], [[banco_de_terrenos]], [[mcmv]], [[resultado_a_apropriar]]
