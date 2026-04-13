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
created: 2026-04-08
updated: 2026-04-13
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

**Nota definicional:** o denominador é sempre Estoque(t-1) + Lançamentos(t). O numerador varia: vendas brutas (VSO bruta) ou vendas líquidas (VSO líquida). Ao comparar cross-empresa, verificar nota metodológica do release — as bases não são diretamente comparáveis quando uma empresa reporta VSO trimestral e outra reporta VSO UDM.

## Comparativo cross-empresa — 4T25 e 1T26

| Empresa | Métrica | 4T25 | 1T26 | Δ T/T |
|---|---|---|---|---|
| [[cury]] | VSO líq. trimestral | 39,3% | 45,1% | +5,8 p.p. |
| [[cury]] | VSO líq. UDM | — | 73,9% | — |
| [[cyrela]] | VSO 12 meses | 45,2% | — | — |
| [[direcional]] (consol.) | VSO trimestral | 21% | 24% | +3,0 p.p. |
| [[direcional]] (Direcional) | VSO trimestral | — | 24% | — |
| [[direcional]] ([[riva]]) | VSO trimestral | — | 23% | — |
| [[tenda]] (consol.) | VSO líq. trimestral | — | 27,6% | — |
| [[tenda]] (MCMV) | VSO líq. trimestral | — | 26,9% | +4,3 p.p. |
| [[tenda]] ([[alea]]) | VSO líq. trimestral | 38,0% | 41,6% | +3,6 p.p. |

(fontes: digested/cury_previa_operacional_1T26_summary.md; digested/cyrela_previa_4T25_summary.md; digested/direcional_previa_operacional_1T26_summary.md; digested/tenda_previa_operacional_1T26_summary.md; digested/direcional_release_4T25_summary.md; digested/tenda_release_4T25_summary.md)

## Leitura dos dados

**[[Cury]]** lidera em absorção com folga: VSO UDM de 73,9% e VSO trimestral de 45,1% no 1T26, refletindo demanda consistente em SP e RJ no segmento [[mcmv]] (fonte: digested/cury_previa_operacional_1T26_summary.md). A empresa vendeu R$ 2,3 bi líquido no trimestre (+9,5% A/A), com landbank recorde de R$ 24,9 bi — ou seja, oferta crescente sendo absorvida a velocidade elevada (fonte: digested/cury_previa_operacional_1T26_summary.md).

**[[Cyrela]]** reporta VSO 12 meses de 45,2% no 4T25, queda de 55,0% no 4T24 — resultado de lançamentos agressivos em 2025 (R$ 18,6 bi VGV, +43% A/A) que expandiram a oferta mais rápido que as vendas conseguiram absorver (fonte: digested/cyrela_release_4T25_summary.md). A VSO de lançamentos do 4T25 foi de 38%, indicando que produtos novos demoraram mais para girar (fonte: digested/cyrela_previa_4T25_summary.md).

**[[Direcional]]** tem a VSO trimestral mais baixa do grupo (24% no 1T26), mas esse nível é consistente com seu modelo de alto landbank (R$ 60 bi, 246 mil unidades) e ritmo de lançamentos distribuído geograficamente (fonte: digested/direcional_previa_operacional_1T26_summary.md). VSO subiu +250 bps T/T, com o segmento Direcional (24%) ligeiramente acima de [[Riva]] (23%) (fonte: digested/direcional_previa_operacional_1T26_summary.md).

**[[Tenda]]** consolida VSO líquida de 27,6% no 1T26, com aceleração no segmento [[alea]] (41,6%, +23,6 p.p. vs 1T25), que se beneficia de estoque menor e preço mais alto por unidade (fonte: digested/tenda_previa_operacional_1T26_summary.md). O segmento MCMV atingiu VSO líquida de 26,9% (+4,3 p.p. T/T), com vendas brutas recorde de R$ 1.579 mm (fonte: digested/tenda_previa_operacional_1T26_summary.md).

## VSO e distratos

A diferença entre VSO bruta e líquida revela o impacto dos [[distrato]]s. No 1T26, a [[cury]] registrou gap de ~4 p.p. (distratos = 9,0% das vendas brutas, vs 5,4% no 1T25) (fonte: digested/cury_previa_operacional_1T26_summary.md). Na [[tenda]] consolidada o gap foi de 3,0 p.p. (distratos = 9,9% das vendas brutas) (fonte: digested/tenda_previa_operacional_1T26_summary.md). Na [[direcional]], os distratos subiram para 14,8% das vendas brutas no 4T25 (vs 8,3% em 2024), pressionando a VSO líquida implícita (fonte: digested/direcional_release_4T25_summary.md).

Relacionado: [[vgv]], [[distrato]], [[incorporadoras]], [[repasses]], [[banco_de_terrenos]]
