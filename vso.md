---
type: concept
aliases: [Velocidade Sobre Oferta, VSO Bruta, VSO Liquida]
sources: [full/tenda/1T26/previa_operacional.md]
created: 2026-04-08
updated: 2026-04-08
---

# VSO

**Velocidade Sobre Oferta** — indicador de absorção de oferta de uma incorporadora em um período.

**Fórmula:** VSO = Vendas do trimestre / (Estoque do trimestre anterior + Lançamentos do trimestre)

Reportada em dois recortes:

- **VSO Bruta** — considera o total de vendas brutas (antes de distratos) sobre a oferta.
- **VSO Líquida** — considera vendas líquidas (após distratos) sobre a oferta.

A diferença entre as duas é uma leitura direta do impacto dos [[distrato]]s sobre a absorção efetiva.

VSO alta indica demanda forte relativa à oferta disponível; VSO baixa indica acúmulo de estoque. É uma métrica *relativa* — uma VSO de 30% em um trimestre com lançamentos altos pode representar mais volume de venda que uma VSO de 50% em trimestre com baixa oferta, então ela é lida em conjunto com [[vgv]] vendido absoluto.

## Exemplos — Tenda 1T26

No 1T26, a [[tenda]] reportou (fonte: structured/tenda/1T26/previa_operacional.json :: canonical.operacional.vendas_liquidas.vso_liquida):

- **Tenda (MCMV):** VSO bruta 29,7%, VSO líquida 26,9% (+4,3 p.p. T/T).
- **Alea (SBPE):** VSO bruta 48,2%, VSO líquida 41,6% (+23,6 p.p. vs 1T25).
- **Consolidado:** VSO bruta 30,6%, VSO líquida 27,6%.

**Nota definicional:** o denominador é sempre Estoque(t-1) + Lançamentos(t). O numerador varia: vendas brutas (VSO bruta) ou vendas líquidas (VSO líquida). Algumas empresas reportam VSO UDM (últimos doze meses) que suaviza sazonalidade. Ao comparar cross-empresa, verificar nota metodológica do release.

Relacionado: [[vgv]], [[distrato]], [[incorporadoras]]
