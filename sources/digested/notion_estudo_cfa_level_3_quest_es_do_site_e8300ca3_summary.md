---
type: nota
sources:
  - full/generic/notas/estudo_cfa_level_3_quest_es_do_site_e8300ca3.md
created: 2026-04-17
updated: 2026-04-17
---

# Estudo CFA Level 3 [?] — Questões do Site

## Contexto da nota

Nota de estudo pessoal do analista, criada em 2024-06-10, contendo anotações e observações sobre questões do site do CFA Institute para o exame Level 3. Cobre múltiplos tópicos do currículo; o formato é uma série de lembretes, conceitos-chave e fórmulas marcadas com grau de dificuldade e pontos de atenção em primeira pessoa (fonte: full/generic/notas/estudo_cfa_level_3_quest_es_do_site_e8300ca3.md).

Não há empresas listadas brasileiras ou dados financeiros de companhias nesta nota. Conteúdo é genérico/educacional — não será roteado para páginas de empresas no wiki.

---

## Tópicos cobertos e pontos-chave do analista

### Capital Market Expectations — Macro

Tese (analista): "Errei bastante, bem específico — revisar bias e alguns conceitos e fórmulas macro como Taylor Rule." (fonte: full/generic/notas/estudo_cfa_level_3_quest_es_do_site_e8300ca3.md §Capital Market Expectations - Macro)

- Processo de CME tem 7 [?] etapas: especificar expectativas → pesquisa histórica → modelo/método → fontes → interpretação → output → monitoramento.
- Fórmula de retorno de longo prazo de ações: `Long term Equity Return = ΔNominal GDP + ΔP/E + Dividend Yield + Δ(share of profits % of GDP)`.
- Taylor Rule (forma simplificada): `Neutral rate + 0,5 × (GDP growth forecast – GDP growth trend) + 0,5 × (Inflation forecast – Inflation target)`.
- Biases mais importantes (marcados como MUITO IMPORTANTE): Availability, Status quo, Prudence trap (tendência de ser cauteloso por razões de carreira).
- Shrinkage estimation: média ponderada entre estimativa histórica e outro estimador — o analista anotou não ter entendido matrizes de shrinkage.

### Overview of Asset Allocation

- Black–Litterman e reverse optimization produzem alocações menos concentradas e mais próximas dos pesos globais vs. histórico puro (fonte: full/generic/notas/estudo_cfa_level_3_quest_es_do_site_e8300ca3.md §Overview of asset allocation).
- Risk parity: cada classe de ativo contribui com a mesma quantidade de risco; `w_i × Cov(r_i, r_p) = (1/n)σ²_p`.
- Optimal corridor: mais estreito quando volatilidade é alta; mais largo quando correlação com o resto do portfólio é alta e custos de transação são altos.
- Estratégias: MVO (asset only), Reverse Optimization (usa pesos de mercado global), Black-Litterman (ajusta pesos por visões do gestor), Resampling (sobre-diversifica ativos mais arriscados).
- Modelos institucionais: Norway Model (passivo, público, ESG), Endowment (ativo, ilíquido, externo), Canadian (private equity/real estate, gestão interna), LDI (hedge de seguradoras).

### Asset Allocation with Real-World Constraints

- Representativeness/recency bias: sobreponderar observações recentes (fonte: full/generic/notas/estudo_cfa_level_3_quest_es_do_site_e8300ca3.md §Asset Allocation with Real-World Constraints).
- Mental accounting bias: contas separadas com diferentes tolerâncias a risco.
- Loss-aversion bias: perdas percebidas como mais dolorosas que ganhos equivalentes; ativos em queda são mantidos.
- Retorno incremental de TAA (Tactical Asset Allocation): `(TAA weight – Policy weight) × return do ativo`.
- Corner portfolios: ponto na fronteira eficiente onde o peso de um ativo muda de zero para positivo ou vice-versa.

### Swaps, Forwards e Futures Strategies

- Equity swaps: contratos OTC ilíquidos, sem direito a voto.
- Basis: se positivo, lucro em "sell the basis" (vende o bond, compra o futuro).
- Eurodollar futures: lógica de vender a 99 [?] e recomprar a 98 [?] para ganhar spread.
- Payer swaption: direito de entrar num swap pagando taxa fixa — lucra se juros sobem.

### Currency Management

- Custos de hedge: dealer spreads, prêmio upfront de opções, roll-down costs, custos administrativos.
- Forward contracts vs. futures para hedge cambial: forward é mais flexível (par, data, tamanho), sem margem, mais líquido em grandes volumes.
- Fórmula de variância em moeda doméstica: `σ²(R_DC) ≈ σ²(R_FC) + σ²(R_FX) + 2σ(R_FC)σ(R_FX)ρ`.

### Fixed-Income Portfolio Management e Liability-Driven Strategies

- Imunização para múltiplos passivos: BPV do ativo = BPV do passivo; convexidade do ativo > convexidade do passivo.
- Structural risk é minimizado reduzindo dispersão dos cash flows (bullet > barbell).
- Convexidade: Barbell > Laddered > Bullet.
- Weighted average YTM ≠ cash flow yield do portfólio — o relevante é o cash flow yield.
- Tipo IV de passivo: valor e timing incertos.
- Ladder portfolio: menor risco de reinvestimento.

### Yield Curve Strategies

- `%ΔPV_Full ≈ −(ModDur × ΔYield) + ½ × Convexity × (ΔYield)²`.
- Butterfly spread = `−short + 2×medium − long`; visão positiva de butterfly implica spread caindo.
- Forward rate bias: carry trade — tomar emprestado em moeda de yield menor, investir em maior.

### Fixed Income Active Management: Credit Strategies

- Duração empírica < duração teórica para todos os ratings de crédito.
- `E[ExcessSpread] ≈ Spread₀ – (EffSpreadDur × ΔSpread) – (POD × LGD)`.
- Fase de expansão tardia: crescimento acelerado, pico de lucros, alavancagem estável, queda em defaults.
- Covered bonds: desempenho superior em downturn vs. outros bonds de real estate — investidor tem recurso ao emissor.
- CDOs: analista marcou como área a aprofundar.

### CFA Institute Asset Manager Code

- Gestores não devem participar de boards de empresas que recebem stock options.
- CCO deve ser independente de operações e gestão de investimentos, reportando ao CEO ou board.
- Disclosure de performance aos clientes: mínimo trimestral, idealmente dentro de 30 dias do fim do trimestre.
- Confidencialidade: informações de clientes prospectivos também não podem ser compartilhadas.

---

## Empresas e tickers mencionados

Nenhuma empresa brasileira listada mencionada. Referências a fundos e exemplos genéricos do currículo CFA (Bornelli, SPP, Shipman — são casos fictícios do material CFA).

---

## Dúvidas abertas / follow-ups do analista

- Revisar Taylor Rule e seus parâmetros com precisão (fonte: full/generic/notas/estudo_cfa_level_3_quest_es_do_site_e8300ca3.md §Capital Market Expectations - Macro).
- Entender shrinkage estimators de matrizes de covariância.
- Aprofundar cross-currency swap e a dinâmica de demanda por dólares.
- Revisar CDOs e estruturas de crédito estruturado.
- Revisar tributação de fundos e contas tax exempt.
- Entender o efeito de cheapest-to-deliver em futuros de bonds.
- Revisar rolldown return com precisão.
