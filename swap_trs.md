---
type: concept
aliases: [SWAP TRS, Total Return Swap, Equity swap sobre ações próprias]
sources:
  - sources/full/tenda/2025/dfp.md
  - sources/full/tenda/2024/dfp.md
  - sources/full/tenda/2T25/release.md
  - sources/full/tenda/2T25/fato_relevante_913576.md
  - sources/full/tenda/2T26/fato_relevante_1025459.md
  - sources/full/direcional/4T24/fato_relevante_2.md
created: 2026-04-11
updated: 2026-04-11
---

# SWAP TRS — Total Return Swap sobre ações próprias

**Total Return Swap (TRS)** é um derivativo em que uma parte (tipicamente um banco) entrega à contraparte (empresa) o retorno total de um ativo de referência — no caso das listadas brasileiras, as **próprias ações**. A empresa paga ao banco o CDI + spread sobre o valor nocional, e recebe dividendos + variação de preço das ações.

Economicamente, é uma **posição comprada sintética em ações próprias**: a empresa fica exposta à valorização de suas ações sem efetivamente tê-las em tesouraria. Em contrapartida, em caso de queda da ação, a empresa paga a diferença ao banco.

## Por que incorporadoras usam

1. **Programas de incentivo de longo prazo (ILP / stock grants):** ao invés de comprar ações diretamente e bloquear caixa, a empresa contrata um SWAP que replica a exposição. Na hora de entregar ações a colaboradores (grant/vesting), o SWAP é liquidado e as ações são entregues.
2. **Recompra sintética:** hedge alternativo a programas tradicionais de recompra, com flexibilidade contratual (prazo, tamanho, possibilidade de rolagem).
3. **Efeito caixa defasado:** o desembolso só ocorre na liquidação, permitindo suavização de fluxo.

## Efeito contábil

O SWAP TRS é classificado como **derivativo não-hedge**, portanto marcado a mercado a cada balanço. A variação de valor justo vai direto para o **resultado financeiro**:

- Ação subiu no trimestre → SWAP gera **receita financeira** (ganho mark-to-market).
- Ação caiu no trimestre → SWAP gera **despesa financeira**.

Isso cria **volatilidade no resultado financeiro não correlacionada com operação**. Em trimestres de forte alta da ação, o lucro líquido é inflado artificialmente; em trimestres de queda, é comprimido.

## Caso Tenda — volatilidade explícita

A [[tenda|Tenda]] tem um dos maiores programas de SWAP TRS entre incorporadoras, com contrapartes Itaú, Bradesco e Santander sobre ~12 mm de ações TEND3 no pico.

**Efeito no resultado:**

| Ano | Efeito no resultado financeiro | Observação |
|---|---:|---|
| 2024 | -R$ 28,2 mm | Ação TEND3 caiu no ano, SWAP ficou passivo |
| 2025 | **+R$ 135 mm** (DFP auditado) | Ação TEND3 disparou; 2T25 concentrou +R$ 126,8 mm |
| 9M25 | +R$ 147 mm | — |

Fontes: (fonte: full/tenda/2024/dfp.md §nota_11), (fonte: full/tenda/2025/dfp.md §nota_11), (fonte: full/tenda/2T25/release.md §resultado_financeiro).

O efeito é brutal: o resultado financeiro consolidado 9M25 foi de **+R$ 52 mm**; **excluindo SWAP seria de -R$ 95 mm** (fonte: structured/tenda/3T25/itr.json :: canonical.dre). A empresa passou a divulgar **guidance e métricas ex-SWAP** a partir do 1T25 por reconhecer a distorção.

Para modelagem forward: o resultado financeiro **ex-SWAP coerente com dívida líquida R$ 266 mm a CDI+spread é de cerca de -R$ 130 mm/ano** (fonte: full/tenda/2025/dfp.md §nota_22). Esse é o nível normalizado — qualquer modelagem que usar o resultado financeiro reportado em 2025 como base recorrente irá superestimar lucro.

## Gestão do programa Tenda — liquidações e rolagens

A administração vem reduzindo gradualmente a posição via liquidações parciais, geralmente alinhadas a programas ILP (stock grant):

| Data | Contraparte | Ações liquidadas | Efeito |
|---|---|---:|---|
| Jun/2025 | Itaú (integral) + Bradesco (parcial) | 4,6 mm | Caixa bruto ~R$ 43 mm |
| Ago/2025 | Bradesco | 713.744 | Ganho bruto ~R$ 6,4 mm |
| Mar/2026 | Santander | 385.601 | Stock grant ILP |
| Abr/2026 | Santander (rolagem) | 5.146.499 | Novos contratos até abr/2027; caixa líquido >R$ 60 mm na liquidação dos antigos |

Fontes: (fonte: full/tenda/2T25/fato_relevante_913576.md), (fonte: full/tenda/3T25/fato_relevante_934734.md), (fonte: full/tenda/1T26/fato_relevante_1013789.md), (fonte: full/tenda/2T26/fato_relevante_1025459.md).

Posição remanescente pós-abr/2026: 5.146.499 ações (todo Santander), com rolagem até abr/2027.

## Direcional — equity swap como ferramenta de recompra

A [[direcional|Direcional]] também autorizou celebração de derivativos (equity swap) em seu **programa de recompra** aprovado em dez/2024 — até 10 mm de ações (free float 109,7 mm), prazo de 18 meses (fonte: full/direcional/4T24/fato_relevante_2.md). A estrutura é similar em efeito econômico, mas a magnitude do programa é menor relativa ao float e o efeito contábil tem sido menos material que na Tenda.

## Sinais de atenção para o analista

1. **Ajustar sempre por SWAP quando normalizar resultado financeiro.** É a distorção mais comum em incorporadoras que usam o instrumento.
2. **Rolagens de derivativos são sinal de intenção de manter a posição** — não confundir com liquidação.
3. **Comparar lucro reportado vs lucro ex-SWAP** é o único modo de ler comparações ano-a-ano durante períodos de forte variação cambial do papel.
4. **Risco de crédito:** o SWAP é crédito com o banco contraparte. Em stress, a empresa pode ter que depositar colateral adicional.

Relacionado: [[tenda]], [[direcional]], [[incorporadoras]]
