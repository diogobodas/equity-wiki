---
type: concept
aliases: [Velocidade Sobre Oferta, VSO Bruta, VSO Liquida]
sources:
  - sources/digested/cury_release_4T25_summary.md
  - sources/digested/cury_previa_operacional_1T26_summary.md
  - sources/digested/cyrela_previa_4T25_summary.md
  - sources/digested/cyrela_release_4T25_summary.md
  - sources/digested/direcional_release_4T25_summary.md
  - sources/digested/direcional_previa_operacional_1T26_summary.md
  - sources/digested/tenda_release_4T25_summary.md
  - sources/digested/tenda_previa_operacional_1T26_summary.md
  - sources/digested/HB_historical series_4Q25_summary.md
  - sources/digested/cyrela_fatos_relevantes_batch_summary.md
  - sources/digested/cyrela_dados_operacionais_summary.md
  - sources/digested/direcional_call_transcript_3T20_summary.md
  - sources/digested/direcional_call_transcript_4T20_summary.md
  - sources/digested/direcional_call_transcript_1T21_summary.md
  - sources/digested/direcional_call_transcript_2T21_summary.md
  - sources/digested/direcional_call_transcript_3T21_summary.md
  - sources/digested/direcional_call_transcript_4T21_summary.md
  - sources/digested/direcional_call_transcript_1T22_summary.md
  - sources/digested/direcional_call_transcript_2T22_summary.md
  - sources/digested/direcional_call_transcript_3T22_summary.md
  - sources/digested/direcional_call_transcript_4T22_summary.md
  - sources/digested/direcional_call_transcript_1T23_summary.md
  - sources/digested/direcional_call_transcript_2T23_summary.md
  - sources/digested/direcional_call_transcript_3T23_summary.md
  - sources/digested/direcional_call_transcript_4T23_summary.md
  - sources/digested/direcional_call_transcript_1T24_summary.md
  - sources/digested/direcional_call_transcript_2T24_summary.md
  - sources/digested/direcional_call_transcript_3T24_summary.md
  - sources/digested/direcional_call_transcript_4T24_summary.md
  - sources/digested/notion_direcional_18_02_30b00ca3_summary.md
  - sources/digested/notion_direcional_59a00ca3_summary.md
  - sources/digested/notion_direcional_call_pos_4t25_31f00ca3_summary.md
created: 2026-04-08
updated: 2026-04-21
---

# VSO

**Velocidade Sobre Oferta** — indicador de absorção de oferta de uma incorporadora em um período.

**Fórmula:** VSO = Vendas do trimestre / (Estoque do trimestre anterior + Lançamentos do trimestre)

Reportada em dois recortes:

- **VSO Bruta** — considera o total de vendas brutas (antes de distratos) sobre a oferta.
- **VSO Líquida** — considera vendas líquidas (após distratos) sobre a oferta.

A diferença entre as duas é uma leitura direta do impacto dos [[distrato]]s sobre a absorção efetiva.

VSO alta indica demanda forte relativa à oferta disponível; VSO baixa indica acúmulo de estoque. É uma métrica *relativa* — uma VSO de 30% em um trimestre com lançamentos altos pode representar mais volume de venda que uma VSO de 50% em trimestre com baixa oferta, então ela é lida em conjunto com [[vgv]] vendido absoluto.

## Variantes de reporte

Cada empresa reporta VSO com metodologias ligeiramente diferentes:

- **VSO trimestral** — métrica spot do trimestre. Usada por [[tenda]], [[direcional]], [[cury]] (fonte: digested/tenda_previa_operacional_1T26_summary.md).
- **VSO UDM (últimos doze meses)** — suaviza sazonalidade, usada por [[cury]] e [[cyrela]] como métrica principal (fonte: digested/cury_previa_operacional_1T26_summary.md).
- **VSO de lançamentos** — percentual do VGV lançado no trimestre que já foi vendido dentro do próprio período ou em janela curta. [[Cyrela]] reporta esta métrica separadamente (fonte: digested/cyrela_previa_4T25_summary.md).
- **VSO de estoque (ex-lançamentos)** — denominador exclui lançamentos do trimestre corrente, isolando a absorção do estoque preexistente. [[Direcional]] reportou esta variante quando lançamentos se concentraram no fim do trimestre, tornando a VSO total enganosamente baixa (ex.: 3T20: VSO total 16% vs VSO ex-lançamentos 22%) (fonte: digested/direcional_call_transcript_3T20_summary.md).

**Nota definicional:** o denominador é sempre Estoque(t-1) + Lançamentos(t). O numerador varia: vendas brutas (VSO bruta) ou vendas líquidas (VSO líquida). Ao comparar cross-empresa, verificar nota metodológica do release — as bases não são diretamente comparáveis quando uma empresa reporta VSO trimestral e outra reporta VSO UDM.

**Série histórica longa:** a planilha setorial HB cobre dados trimestrais de VSO de ~20 incorporadoras listadas na B3, desde 1T09 até 4T25, permitindo análise de ciclos longos de absorção e comparação cross-company ao longo de 16+ anos (fonte: digested/HB_historical series_4Q25_summary.md).

Para [[cyrela]] especificamente, a planilha proprietária de dados operacionais traz série trimestral própria de 1T06 a 4T25 (~80 trimestres) com lançamentos, vendas e estoque cortados por região (8) e segmento (Alto, Médio, Vivaz Prime, MCMV 2 e 3, MCMV 1) — permite reconstruir VSO histórica da empresa por segmento ao longo de ciclos completos (2008–09, 2014–17, 2020–21, 2022–25). Dados pré-2019 são pro forma para a estrutura societária atual (fonte: digested/cyrela_dados_operacionais_summary.md).

## Direcional — Série histórica de VSO (3T20–4T25)

Série extraída de calls de resultados. Números do transcript (auto-captions); canônicos em releases/ITRs.

| Período | VSO Consol. | VSO Direcional | VSO [[riva]] | Observação |
|---|---|---|---|---|
| 3T20 | 16% | 18% | 15% | Ex-lançamentos fim set.: consol. 22%, DIRR 23%, Riva 16% |
| 4T20 | 17% | 18% | 16% | VSO de estoque (ex-lançamentos do tri): 22% em ambos |
| 1T21 | 17% | n/d | 20% | Sazonal; melhor tri de vendas brutas da história à época |
| 2T21 | 18% | 17% | 26% | Maior VSO consol. dos últimos 5 tri; Riva = 30% das vendas |
| 3T21 | 17% | n/d | 33% | Riva representa 37% das vendas; lançamentos recorde R$ 1,1 bi |
| 4T21 | ~17% | n/d | n/d | Trecho cortado na transcrição; descrito como “sólido e constante” |
| 1T22 | 17% | 19% | ~15–16% | Riva com sazonalidade 1T (lançamentos concentrados no fim do tri) |
| 2T22 | 20% | 23% | 17% | VSO deliberadamente calibrada abaixo do histórico; custo de capital alto |
| 3T22 | 19% | n/d | n/d | Dentro da banda-alvo 18–22% |
| 4T22 | n/d | n/d | n/d | Queda por eleições + Copa do Mundo; jan/fev 2023 superaram 4T22 |
| 1T23 | ~17% | n/d | n/d | +2 p.p. vs 4T22; voltou “acima da média dos últimos trimestres” |
| 2T23 | ~18% | ~18–20% | ~18% | Riva voltando ao patamar de 18% após 12–13% no 2S22 |
| 3T23 | 17% | 15% | 19% | Maior VSO de Riva dos últimos trimestres; DIRR pressionada |
| 4T23 | 19% | 17,2% | n/d | 17,2% ex-Pode Entrar SP; com Pode Entrar (R$ 206 mi VGV) sobe para 19% |
| 1T24 | 22% | 21% | 22% | Salto estrutural; FGTS Futuro entrou em vigor |
| 2T24 | 26% | ~26% | ~26% | Recorde histórico; DIRR e Riva praticamente iguais pela 1ª vez |
| 3T24 | 25% | ~25% | ~25% | Novo patamar considerado “saudável” pela gestão |
| 4T24 | 25% | n/d | n/d | Estável; gestão entregou “mais margem do que VSO” neste ciclo |
| 2T25 | ~25% | n/d | n/d | VSO considerada saudável pela gestão; meta elevada para 28–30% |
| 3T25 | ~25% | n/d | n/d | Patamar consistente; RJ, Salvador e Recife identificadas como praças a recuperar |
| 4T25 | 21% | n/d | n/d | Normalização; shares da Direcional nas vendas totais subiram de 79% para 83% |

(fontes: digested/direcional_call_transcript_3T20_summary.md a digested/direcional_call_transcript_4T24_summary.md; digested/notion_direcional_call_pos_4t25_31f00ca3_summary.md; digested/notion_direcional_59a00ca3_summary.md)

**Nota sobre Riva:** a VSO do segmento Riva foi historicamente mais volátil que a do segmento Direcional MCMV. No pico do ciclo de 2021 chegou a 33% (3T21), puxada por lançamentos com alta demanda no médio padrão. Em 2S22 caiu a ~12–13% com o aperto do crédito SBPE (Riva usa SFH, mais sensível à Selic). A convergência dos dois segmentos para o mesmo patamar de VSO (~22–26%) a partir de 1T24 é um fenômeno novo, atribuído ao FGTS Futuro, ao MCMV Cidades e à maturação da equipe comercial (fonte: digested/direcional_call_transcript_1T24_summary.md; digested/direcional_call_transcript_2T24_summary.md).

## Direcional — Gestão ativa de VSO

A [[direcional]] é a empresa do setor que mais explicitou, em seus calls, uma filosofia de gestão de VSO com faixas-alvo, trade-offs e evolução ao longo do ciclo.

**Nível ótimo — evolução do guidance:**
- **2020–21:** meta de ~20% no médio prazo; administração descreveu 18–20% como “ótimo” — VSO acima disso “tira flexibilidade de preço” (fonte: digested/direcional_call_transcript_3T20_summary.md).
- **2022:** banda-alvo explícita de 18–22%; empresa calibrou VSO “ligeiramente abaixo do histórico” dado custo de capital mais alto; priorizou geração de caixa via giro em vez de margem (fonte: digested/direcional_call_transcript_2T22_summary.md; digested/direcional_call_transcript_3T22_summary.md).
- **2023:** meta para 2024 de elevar VSO para ~20% via melhorias estruturais — treinamento comercial, vendas online, automação — sem descontos e sem aumento de despesa comercial (fonte: digested/direcional_call_transcript_4T23_summary.md).
- **2024:** meta de 20% ultrapassada; VSO 26% no 2T24 (recorde). Gestão passou a considerar ~25% como o novo patamar saudável, definindo-o como o nível em que “100% das unidades estão vendidas próximo ao pico de obra” (fonte: digested/direcional_call_transcript_3T24_summary.md).
- **2025 (ago/nov):** meta elevada para **28–30%**; empresa reconheceu que “tem entregado mais margem do que VSO” e que precisa buscar melhora na velocidade. Diagnóstico por praça: RJ (reset comercial — troca de diretor, melhor mês histórico em junho/25), Salvador (falta produto) e Recife (time em formação). Gestão estimou que resolver as três praças deficientes bastaria para chegar a 28%, sem alterar o restante do portfólio (fonte: digested/notion_direcional_59a00ca3_summary.md).
- **2026:** mudança explícita de filosofia — **prioridade para VSO sobre margem**. Empresa tem R$ 2,4 bi em produtos aprovados prontos para lançar imediatamente e optou por ritmo controlado de lançamentos para priorizar absorção. Qualquer ganho de affordability com ajustes de faixas MCMV deve se traduzir integralmente em VSO, não em preços (fonte: digested/notion_direcional_18_02_30b00ca3_summary.md; digested/notion_direcional_call_pos_4t25_31f00ca3_summary.md).

**Trade-off VSO vs. margem:** no segmento Direcional (MCMV), onde há teto de preço, “a prioridade é VSO + alavancagem operacional, não repasse de preço” — diferentemente da Riva, onde sem teto o repasse é mais fácil (fonte: digested/direcional_call_transcript_3T20_summary.md). No ciclo 2022–23, o CEO declarou que a empresa “aceita margem flat” para priorizar VSO e geração de caixa (fonte: digested/direcional_call_transcript_4T22_summary.md). A partir de 2024, com custos cadentes e margem REF acima de 43%, a empresa elevou simultaneamente VSO e margem bruta — cenário descrito como “de longe o melhor trimestre em termos de resultados da história” (fonte: digested/direcional_call_transcript_1T24_summary.md).

**Alavancas de VSO:** o salto de VSO de 2024 foi atribuído a fatores estruturais, não a descontos: (i) qualificação da equipe comercial e metas com menor dispersão entre praças; (ii) expansão de vendas online; (iii) FGTS Futuro (amplia comprometimento de renda para famílias em produtos abaixo de R$ 200–220 k); (iv) MCMV Cidades (acessa famílias de até 1 salário mínimo em praças como Fortaleza e Recife); (v) amadurecimento de praças (+4 p.p. de margem bruta e -3 p.p. de despesa comercial vs praças recentes) (fonte: digested/direcional_call_transcript_1T24_summary.md; digested/direcional_call_transcript_2T24_summary.md; digested/direcional_call_transcript_3T24_summary.md).

**VSO e retorno de capital:** a gestão estabeleceu ligação direta entre VSO e geração de caixa para dividendos: “3 p.p. de VSO trimestral sobre estoque de ~R$ 5 bi tem impacto muito relevante” (fonte: digested/direcional_call_transcript_4T23_summary.md). No call pós-4T25, a quantificação foi refinada: **cada 1 p.p. de aumento na VSO trimestral gera aproximadamente R$ 100 milhões adicionais de caixa por ano** (fonte: digested/notion_direcional_call_pos_4t25_31f00ca3_summary.md). Em 2024, com VSO de 25–26%, a empresa pagou ~R$ 577 mi em dividendos (≈100% do lucro ajustado, DY ~15% sobre o market cap de jan/24) (fonte: digested/direcional_call_transcript_4T24_summary.md). Em 2025, com ROE recorde de 44% no 4T25, o retorno ao acionista totalizou R$ 1,15 bilhão em dividendos + R$ 26 milhões em recompra de ações (fonte: digested/notion_direcional_call_pos_4t25_31f00ca3_summary.md).

## Comparativo cross-empresa — 4T25 e 1T26

| Empresa | Métrica | 4T25 | 1T26 | Δ T/T |
|---|---|---|---|---|
| [[cury]] | VSO líq. trimestral | 39,3% | 45,1% | +5,8 p.p. |
| [[cury]] | VSO líq. UDM | — | 73,9% | — |
| [[cyrela]] | VSO 12 meses | 45,2% | 45,8% | +0,6 p.p. |
| [[cyrela]] | VSO safra | 38% | 45% | +7,0 p.p. |
| [[direcional]] (consol.) | VSO trimestral | 21% | 24% | +3,0 p.p. |
| [[direcional]] (Direcional) | VSO trimestral | — | 24% | — |
| [[direcional]] ([[riva]]) | VSO trimestral | — | 23% | — |
| [[tenda]] (consol.) | VSO líq. trimestral | — | 27,6% | — |
| [[tenda]] (MCMV) | VSO líq. trimestral | — | 26,9% | +4,3 p.p. |
| [[tenda]] ([[alea]]) | VSO líq. trimestral | 38,0% | 41,6% | +3,6 p.p. |

(fontes: digested/cury_previa_operacional_1T26_summary.md; digested/cyrela_previa_4T25_summary.md; digested/cyrela_fatos_relevantes_batch_summary.md; digested/direcional_previa_operacional_1T26_summary.md; digested/tenda_previa_operacional_1T26_summary.md; digested/direcional_release_4T25_summary.md; digested/tenda_release_4T25_summary.md)

## Leitura dos dados

**[[Cury]]** lidera em absorção com folga: VSO UDM de 73,9% e VSO trimestral de 45,1% no 1T26, refletindo demanda consistente em SP e RJ no segmento [[mcmv]] (fonte: digested/cury_previa_operacional_1T26_summary.md). A empresa vendeu R$ 2,3 bi líquido no trimestre (+9,5% A/A), com landbank recorde de R$ 24,9 bi — ou seja, oferta crescente sendo absorvida a velocidade elevada (fonte: digested/cury_previa_operacional_1T26_summary.md).

**[[Cyrela]]** reporta VSO 12 meses de 45,8% no 1T26, estável vs. 45,2% no 4T25, após queda de 52,6% no 1T25 — reflexo dos lançamentos agressivos de 2025 (R$ 18,6 bi VGV, +43% A/A) que expandiram a oferta (fonte: digested/cyrela_fatos_relevantes_batch_summary.md; digested/cyrela_release_4T25_summary.md). A VSO de safra do 1T26 foi de 45%, recuperação significativa vs. 38% no 4T25, indicando que os lançamentos do trimestre foram melhor absorvidos apesar do VGV lançado ter caído 50% A/A para R$ 2.428 mi (fonte: digested/cyrela_fatos_relevantes_batch_summary.md).

**[[Direcional]]** tem a VSO trimestral mais baixa do grupo (24% no 1T26), mas esse nível é consistente com seu modelo de alto landbank (R$ 60 bi, 246 mil unidades) e ritmo de lançamentos distribuído geograficamente (fonte: digested/direcional_previa_operacional_1T26_summary.md). VSO subiu +250 bps T/T, com o segmento Direcional (24%) ligeiramente acima de [[Riva]] (23%). O nível atual representa uma normalização após o pico de 25–26% de 2024 — o maior patamar histórico em 18 trimestres de série acompanhada desde 3T20 (fonte: digested/direcional_call_transcript_3T24_summary.md; digested/direcional_previa_operacional_1T26_summary.md).

**[[Tenda]]** consolida VSO líquida de 27,6% no 1T26, com aceleração no segmento [[alea]] (41,6%, +23,6 p.p. vs 1T25), que se beneficia de estoque menor e preço mais alto por unidade (fonte: digested/tenda_previa_operacional_1T26_summary.md). O segmento MCMV atingiu VSO líquida de 26,9% (+4,3 p.p. T/T), com vendas brutas recorde de R$ 1.579 mm (fonte: digested/tenda_previa_operacional_1T26_summary.md).

## VSO e distratos

A diferença entre VSO bruta e líquida revela o impacto dos [[distrato]]s. No 1T26, a [[cury]] registrou gap de ~4 p.p. (distratos = 9,0% das vendas brutas, vs 5,4% no 1T25) (fonte: digested/cury_previa_operacional_1T26_summary.md). Na [[tenda]] consolidada o gap foi de 3,0 p.p. (distratos = 9,9% das vendas brutas) (fonte: digested/tenda_previa_operacional_1T26_summary.md). Na [[direcional]], os distratos subiram para 14,8% das vendas brutas no 4T25 (vs 8,3% em 2024), pressionando a VSO líquida implícita (fonte: digested/direcional_release_4T25_summary.md). Em 3T24, os distratos da Direcional subiram de ~8% para 9,4% das vendas brutas — explicado pela gestão como “carrego” do salto de patamar de vendas: distratos refletem vendas de trimestres anteriores em base menor, enquanto as vendas correntes cresceram aceleradamente (fonte: digested/direcional_call_transcript_3T24_summary.md).

Relacionado: [[vgv]], [[distrato]], [[incorporadoras]], [[repasses]], [[banco_de_terrenos]]
