---
type: concept
aliases: [Pode Entrar, Programa Habitacional Pode Entrar, Programa Casa Paulistana]
sources:
  - sources/full/tenda/3T24/release.md
  - sources/full/tenda/4T24/release.md
  - sources/structured/tenda/3T24/release.json
  - sources/structured/tenda/1T26/previa_operacional.json
created: 2026-04-12
updated: 2026-04-12
---

# Pode Entrar

**Pode Entrar** (oficialmente Programa Habitacional do Município de São Paulo, também chamado "Casa Paulistana" em algumas versões) é o programa habitacional da **Prefeitura de São Paulo** voltado a famílias de baixa renda. Diferente do [[mcmv|MCMV]] (programa federal via Caixa/FGTS), o Pode Entrar é municipal — financiado com recursos próprios da PMSP, com regras de preço e público-alvo definidos pela Cohab-SP.

## Como funciona

A prefeitura contrata incorporadoras para construir conjuntos habitacionais em terrenos municipais ou privados. O pagamento à incorporadora ocorre por medição de obra (diferente do MCMV, que repassa via Caixa após conclusão). As unidades são vendidas subsidiadas a famílias com renda de até 3 salários mínimos, com prestações proporcionais à renda.

Para as incorporadoras, o Pode Entrar representa **volume concentrado** (contratos grandes, centenas a milhares de unidades por empreendimento) com **margens tipicamente inferiores ao MCMV privado**, dado que os preços são tabelados pela prefeitura e não seguem a lógica de recomposição de preço que o MCMV permite via plafonds da Caixa.

## Impacto na Tenda (TEND3)

O Pode Entrar teve impacto material nos resultados da [[tenda|Tenda]] a partir do 3T24:

- **3T24:** dois contratos assinados — Città Vila Prudente (1.984 unidades) e Guarapiranga (655 unidades, participação Tenda), totalizando R$ 532 mm em [[vgv|VGV]]. Inflou lançamentos (+144% A/A) e vendas líquidas (+68% A/A) no trimestre (fonte: structured/tenda/3T24/release.json :: canonical.operacional).
- **4T24:** impairment de R$ 17,4 mm (CPC 01) sobre os contratos Pode Entrar, pressionando o lucro líquido do trimestre (fonte: structured/tenda/4T24/release.json :: canonical.dre).
- **2025 em diante:** efeito residual nas comparações A/A. A MBA da marca Tenda **ex Pode Entrar** é consistentemente 1-3 p.p. acima da MBA **com** Pode Entrar (ex: 36,4% vs 34,5% no 3T25). A empresa passou a reportar métricas "ex-Pode Entrar" como base de comparação limpa (fonte: structured/tenda/1T26/previa_operacional.json :: company_specific.pode_entrar).

## Para modelagem

Qualquer série temporal que inclua o 3T24 precisa isolar o efeito Pode Entrar — tanto no operacional (VGV lançado e vendido) quanto na DRE (margem inferior ao core MCMV). A Tenda publica o split com/sem Pode Entrar desde o 3T24.

O programa anterior (Estação Tolstói, 216 unidades, R$ 45,3 mm, contratado em 2023) era imaterial (fonte: structured/tenda/2023/dfp.json :: company_specific).

Relacionado: [[tenda]], [[mcmv]], [[incorporadoras]]
