# Wiki Loop Log

<!-- One entry per wiki:loop run -->

## Run 2026-04-04 (Loop 3 — relevance-driven)

- Budget: 10 páginas
- Estrutura: primeira run com prioridade por relevance score (novo sistema)
- Gaps processados: 1 (alto_padrao CRIAR — gap de lavvi.md)
- Gaps pulados: 1 (ion_itau\ — backslash artifact, já tem ion_itau.md)
- Páginas expandidas: 9 (indice_eficiencia, lavvi, iti, selic, compulsorios, ion_itau, iti_itau, margem_backlog, incc)
- Novos gaps gerados: 0
- Score médio antes: ~0.576 (57 páginas) | Páginas ≥ 0.5: ~41/57
- Score médio depois: 0.615 (58 páginas) | Páginas ≥ 0.5: 52/58 (90%)
- Maiores ganhos: selic +0.144 (0.576→0.720), indice_eficiencia +0.114 (0.487→0.601), compulsorios +0.085 (0.471→0.556)
- Páginas movidas de <0.5 para ≥0.5: indice_eficiencia, ion_itau, compulsorios, iti_itau, lavvi (5 páginas)
- iti.md: ainda <0.5 (0.347) — intencional, é redirect page
- Relevância mais alta da wiki: selic.md (rel=0.719, impact=9) — agora com score 0.720
- Wiki features: relevance scoring implementado (wiki_cli relevance --ticker X + scores com relevance/model_impact)

## Run 2026-04-04 (Loop 2)

- Budget: 10 páginas
- Gaps processados: 3 (carteira_credito CRIAR, lavvi CRIAR, iti redirect)
- Páginas expandidas: 7 (iti_itau, ion_itau, xp_investimentos, nubank, compulsorios, carteira_media, plr_bancario)
- Fontes não consumidas: 0
- Novos gaps gerados: 1 (alto_padrao — mencionado em lavvi.md)
- Gaps restantes: 2 (alto_padrao, ion_itau\ backslash-artifact)
- Score médio antes: ~0.48 | Páginas abaixo de 0.5 antes: 10
- Score médio depois: ~0.51 | Páginas abaixo de 0.5 depois: 11 (iti.md redirect conta como nova página de score baixo intencional)
- Total páginas indexadas: 57

## Run 2026-04-03 (Loop 1)

- Budget: 8 páginas
- Gaps processados: 8 (banking, nii_clientes, custo_risco, eficiencia_operacional, selic, bradesco, nii_mercado, nim)
- Páginas aprofundadas: 0
- Score médio antes: 0.678 (só itau.md)
- Score médio depois: 0.547 (9 páginas — novos gaps têm score menor, puxam a média para baixo)
- Score itau.md antes/depois: 0.678 → 0.718 (links_in agora apontam de volta)
- Gaps restantes na fila: 8 (alavancagem_operacional, aliquota_efetiva, consignado_privado, crescimento_carteira, latam, porto_seguro, receita_servicos_tarifas, resultado_seguros)

## Run 2026-04-03 (Loop 2)

- Budget: 8 páginas
- Gaps processados: 8 (crescimento_carteira, consignado_privado, aliquota_efetiva, alavancagem_operacional, resultado_seguros, receita_servicos_tarifas, porto_seguro, latam)
- Novos gaps descobertos: 0
- Score médio: 0.538 (17 páginas — fila totalmente zerada)
- Score itau.md: 0.718 (estável)
- Gaps restantes na fila: 0

## Run 2026-04-03 (Loop 3)

- Budget: 10 páginas (+ 1 bonus: incc.md por necessidade de links)
- Novas páginas: incorporadoras, cyrela, cury, direcional, vgv_lancamentos, margem_backlog, poc_revenue, mcmv, velocidade_vendas, incc
- Aprofundamento: bradesco (score 0.49 → 0.686; +250 palavras, +5 wikilinks)
- Novos gaps descobertos: 0 (todos os [[wikilinks]] nas novas páginas já existem)
- Score médio: 0.563 (27 páginas — RE sector hub + 3 empresas + 6 conceitos RE novos)
- Score bradesco antes/depois: 0.49 → 0.686 (links_in 15, links_out 12)
- Score incorporadoras.md: 0.627 (hub setorial bem conectado)
- Score cyrela.md: 0.663 | cury.md: 0.659 | direcional.md: 0.666
- Gaps restantes na fila: 0

## Run 2026-04-03 (Loop 4 — post BBDC4 + TEND3 initiating coverage)

- Trigger: BBDC4 e TEND3 model runs completos
- Novas páginas: tenda (CRIAR), alea (gap de tenda), capital_de_giro (gap de tenda)
- Aprofundamento: bradesco (score 0.686 → 0.766; dados reais do modelo: LL 26E R$27,471M, ROE 14.8%, NII R$83,275M, eficiência 44.2%; fontes +2 → 3; nota "base em conhecimento geral" removida)
- Novos gaps descobertos: 2 (alea, capital_de_giro) → preenchidos no mesmo run
- Score médio final: ~0.57 (30 páginas)
- Score bradesco antes/depois: 0.686 → 0.766 (dados reais do modelo integrados)
- Score tenda.md: 0.66 (nova, 3 fontes, links_in/out coerentes)
- Score alea.md, capital_de_giro.md: ~0.45 (novas, conexões iniciais)
- Gaps restantes na fila: 0

## Run 2026-04-03 (Loop 5 — overnight wiki expansion)

- Budget: 100 páginas (overnight)
- **Fase 1 — Gaps**: 14 páginas criadas
  - Conceitos banking: carteira_media, compulsorios, duration, indice_eficiencia, plr_bancario, risco_cambial, risco_mercado, roe, ll
  - Redirects/complementos: equity_pickup (redirect para equivalencia_patrimonial)
  - Empresas fora cobertura: nubank, xp_investimentos, iti_itau, ion_itau
- **Fase 2 — Aprofundamento (score < 0.5)**: 8 páginas expandidas
  - alea: +bull/bear case, modelo verificado, análise wood frame vs formas alumínio
  - capital_de_giro: +dias de giro com benchmarks, ΔWC, endividamento, adiantamentos
  - incc: +exposição acumulada, INCC vs IPCA, estratégias de mitigação por empresa
  - velocidade_vendas: +distorções VSO, affordability, calibração backtest, benchmarks
  - poc_revenue: +backlog como reservatório, rollforward completo, reconciliação DRE vs caixa, por empresa
  - margem_backlog: +análise de safra vintage, margem novos vs média, qualidade da info
  - vgv_lancamentos: +ticket médio vs volume, landbank, tipos de guidance, desp. comerciais
  - mcmv: +orçamento político, papel CEF, FGTS, impacto de tetos, ciclo de reconhecimento
- **Fase 3 — Médias (0.5-0.8)**: incorporadoras expandida (+valuation NAV, RET, framework complexidade)
- **Reindex**: 52 páginas indexadas
- Score médio antes: 0.606 (38 páginas)
- Score médio depois: 0.576 (52 páginas — 14 novas stubs puxam média para baixo)
- Score médio páginas antigas (não novas): ~0.63 (melhora vs ~0.60 antes)
- Páginas ≥ 0.5: 38 de 52 (73%); ≥ 0.7: 8 (15%)
- Commits: a2579c1 (gaps), 2d88e6c (fase 2), 4b3f38b (incorporadoras), bbb87e4 (empresas RE), 982d3ca (equity_pickup+roe), f880af1 (fontes)
- Gaps restantes: 0 (todos preenchidos)
- Score final (após reindex completo): avg=0.594 (52 páginas), páginas ≥ 0.5: 41/52 (79%), ≥ 0.7: 9, ≥ 0.8: 5

