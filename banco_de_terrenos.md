---
type: concept
aliases: [Landbank, Banco de Terrenos]
sources: [full/tenda/1T26/previa_operacional.md]
created: 2026-04-08
updated: 2026-04-08
---

# Banco de Terrenos

Conjunto de terrenos já adquiridos (ou contratados) por uma incorporadora para lançamentos futuros. Também chamado de *landbank*. É a matéria-prima do negócio: sem banco de terrenos, não há lançamentos futuros.

## Dimensões relevantes

1. **VGV do banco de terrenos** — potencial de venda embutido, calculado pelo número de unidades futuras × preço médio projetado. Medido em R$ bilhões.
2. **Anos de lançamento cobertos** — VGV do banco / VGV anual de lançamentos. Proxy de "runway" da empresa.
3. **Forma de aquisição — permuta vs caixa:**
   - **Permuta** — o terreno é pago em unidades do próprio empreendimento futuro. Não consome caixa no presente, mas dilui o VGV próprio.
   - **Caixa** — pagamento em dinheiro, geralmente com gatilhos atrelados ao registro de incorporação (mitigando risco de pagar terreno que não vira empreendimento).
   - O **% Permuta Total** é uma leitura direta da disciplina de capital: quanto mais alto, menos caixa comprometido no landbank.
4. **% Permuta Financeiro vs % Permuta Unidades** — decomposição do % Permuta Total em "pago com dinheiro futuro" (financeiro) vs "pago com unidades" (unidades).

## Risco

Um landbank grande não é necessariamente bom — terrenos podem ficar *encalhados* se a empresa não consegue obter aprovação ou financiar a obra. Por isso, incorporadoras mais disciplinadas atrelam pagamentos em caixa à aprovação do registro de incorporação.

## Exemplos — Tenda 1T26

A [[tenda]] fechou o 1T26 com banco de terrenos **recorde** consolidado de R$ 29,7 bi em VGV (R$ 23,4 bi Tenda MCMV + R$ 6,2 bi Alea), com 71,2% em permuta e 139 mil unidades potenciais (fonte: structured/tenda/1T26/previa_operacional.json :: canonical.operacional.banco_de_terrenos).

Fato não-trivial: mesmo os terrenos adquiridos em caixa, >90% do pagamento está atrelado à obtenção do registro de incorporação (fonte: full/tenda/1T26/previa_operacional.md §banco_de_terrenos) — é um mitigador estrutural de risco de fluxo de caixa pouco comum no setor.

A Alea tem banco de terrenos 98% em permuta, virtualmente não comprometendo caixa com landbank.

Relacionado: [[vgv]], [[incorporadoras]], [[tenda]]
