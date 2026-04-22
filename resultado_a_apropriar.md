---
type: concept
aliases: [REF, Resultado a apropriar, Margem REF, Backlog de margem]
sources:
  - sources/full/direcional/4T25/release.md
  - sources/full/tenda/3T25/release.md
  - sources/structured/direcional/4T25/release.json
  - sources/structured/tenda/4T25/release.json
  - sources/digested/cury_release_4T25_summary.md
  - sources/digested/cury_itr_3T25_summary.md
  - sources/digested/cyrela_dfp_2025_summary.md
  - sources/digested/cyrela_release_4T25_summary.md
  - sources/digested/tenda_estouro_custos_2020_2022_analise_summary.md
created: 2026-04-11
updated: 2026-04-22
---

# Resultado a apropriar (REF)

**Resultado a apropriar** é o nome em IFRS/BR-GAAP para o *backlog contábil de margem bruta* de uma incorporadora: a diferença entre **receitas a apropriar** (vendas contratadas ainda não reconhecidas pelo POC) e os **custos a apropriar** associados a essas vendas. É a medida *forward-looking* mais importante para projetar margem bruta dos próximos trimestres.

## Mecânica contábil

Incorporadoras reconhecem receita por **POC — percentage of completion**: à medida que a obra avança, parte da receita vendida é trazida para a DRE. O que foi vendido mas ainda não reconhecido fica no **off-balance**, divulgado em nota explicativa sob rubrica "Receitas e custos de vendas de imóveis a apropriar" ou similar.

Composição típica:

| Item | Descrição |
|---|---|
| Receitas a apropriar | VGV contratado (ex-distratos) pendente de reconhecimento |
| Custos a apropriar | Custos orçados proporcionais às receitas acima |
| **Resultado a apropriar** | Receitas − custos. É o lucro bruto forward |
| **Margem REF** | Resultado / Receitas a apropriar |

A **margem REF é a margem bruta que a empresa está contratando hoje**, antes de POC, antes de contingências. Conforme a obra avança, a margem REF migra para a DRE — de onde vem o conceito: a margem bruta corrente **tende a convergir para a margem REF** com um lag de 2-4 trimestres (duração típica do backlog).

## Como ler

- **Margem REF ≥ Margem bruta DRE:** a empresa está contratando novos lançamentos a margens mais altas que o estoque em execução. Sinal positivo para margens forward.
- **Margem REF < Margem bruta DRE:** há pressão sobre preço de venda ou custo de obras futuras. A margem DRE irá recuar.
- **Receitas a apropriar / receita trimestral**: quantos trimestres de "visibilidade" de top-line a empresa tem contratados (tipicamente 2-4 trimestres).

## Ajustes comuns

Muitas incorporadoras reportam **margem REF ajustada**, adicionando de volta encargos financeiros capitalizados (INCC sobre obras, juros de SFH) que em IFRS são levados ao custo. Sempre usar a versão ajustada para comparar ano contra ano e entre empresas.

## Derivada da margem REF como early warning em choques de custo

Em cenários de choque exógeno de insumos (INCC, aço, commodities energéticas), a **derivada trimestral da margem REF** é o sinal antecedente mais confiável de deterioração futura da DRE — geralmente **2–3 trimestres antes** de o estouro aparecer na margem bruta realizada, e até **8 trimestres antes** do fundo (ciclo obra 10–15 meses + lag de POC).

**Caso de referência — Tenda (TEND3) 2020–2022**, único episódio documentado de estouro estrutural no setor MCMV:

| Trimestre | Mg REF (ex-PE) | MB aj DRE | Sinal |
|---|---:|---:|---|
| 2T20 | 37,1% | — | Primeira identificação de pressão em aço/cimento pelo CEO; tese errada ("só afeta ciclo seguinte") |
| 2T21 | 32,7% | — | VSO bruto pico **38,2%** drenou estoque "bom"; empresa continua lançando |
| 3T21 | — (safra nova 27,7% vs antiga 17,9%) | 22,6% | Breakdown explicito de safras: inflexão qualitativa |
| 4T21 | REF antigo 34,8%→**26%** | — | Clímax: troca de CFO + prejuízo R$ 268 mm + reforço de **R$ 350 mm** no REF. Modelo de orçamento passa a incluir inflação projetada |
| 3T22 | — | **5,6%** | Fundo da DRE — ~8 trimestres após primeiro sinal |

(fonte: digested/tenda_estouro_custos_2020_2022_analise_summary.md)

**O que a curva REF da Tenda ensinou:**

- A **derivada cai 1–2 p.p./trimestre** por vários trimestres antes do estouro aparecer na DRE. No caso Tenda, a Mg REF caiu de 37,1% (2T20) para 32,7% (2T21) — ~4,4 p.p. em 4 trimestres — enquanto a MB aj DRE ainda seguia estável acima de 30%. **Esse descolamento da derivada é o sinal.**
- **VSO alto em período de input inflation é contraintuitivamente ruim**: Tenda usou VSO bruto de 38,2% como "vantagem competitiva" e acabou drenando o backlog precificado a custo antigo, deixando o estoque "ruim" (teto MCMV velho + custo novo) para reconhecer na DRE.
- A **quebra do REF por safra** (novo vs antigo) é o divulgação-chave para detectar deterioração cedo — só apareceu na Tenda no 3T21 (safra nova 27,7% vs antiga 17,9%).
- O **% do custo orçado provisionado para inflação** virou, pós-episódio, linha permanente na Tenda: ~0% antes → mínimo 4% a.a. → **11%** hoje. Empresas com este % baixo ou inexistente em contexto de input shock são candidatas naturais ao "2T20 da Tenda".

Ver framework completo em [[playbook_input_shock]].

## Benchmarks recentes

**Direcional (DIRR3):** margem REF ajustada atingiu pico histórico de **45,2% no 3T25**, recuando ligeiramente para 44,6% no 4T25. A MBA DRE do mesmo período foi de 42,1% → 42,8% — o spread de ~2 p.p. favor REF sinaliza sustentação das margens forward. Receitas a apropriar de R$ 3,8 bi = ~3,5 trimestres de receita no ritmo 4T25 (fonte: full/direcional/4T25/release.md §resultado_a_apropriar, structured/direcional/4T25/release.json :: financeiro_ajustado).

**Tenda (TEND3):** margem REF consolidada 37,3% no 4T25, mas o dado útil é a **margem REF da marca Tenda ex-Pode Entrar: 42,0% no 3T25** (pico) → 38,6% no 4T25. O patamar >37% sustenta a expectativa de margens bruta DRE em 36-37% nos próximos trimestres. Note a contaminação da [[alea|Alea]]: margem REF Alea 21,7% no 3T25 arrasta o consolidado (fonte: full/tenda/3T25/release.md §resultado_a_apropriar, structured/tenda/4T25/release.json :: company_specific.resultado_a_apropriar).

**Cury (CURY3):** resultado a apropriar de R$ 3.346,0 mm no 3T25 (+38,6% YTD), com receitas a apropriar de R$ 7.701,1 mm (+38,4% YTD) e **margem REF de 43,4%** — estável e no patamar mais alto entre as incorporadoras listadas (fonte: digested/cury_itr_3T25_summary.md). No 4T25, REF subiu para R$ 3.381,8 mm (+40,0% A/A) com margem REF de 43,3%, praticamente inalterada (fonte: digested/cury_release_4T25_summary.md). A margem bruta DRE de 40,3% no 4T25 (recorde) já está convergindo para o patamar REF — o spread de apenas ~3 p.p. indica que a [[cury|Cury]] opera próxima do teto de sua margem contratada. Receitas a apropriar de R$ 7,7 bi equivalem a ~5,4 trimestres de receita no ritmo 4T25 — visibilidade de top-line excepcionalmente longa.

**Cyrela (CYRE3):** receita líquida a apropriar de **R$ 11,2 bilhões** no 4T25, com **margem REF de 36,0%** (fonte: digested/cyrela_release_4T25_summary.md). A margem bruta DRE reportada foi de 32,3% no 4T25 (ajustada 34,5% no ano) — o spread de ~1,5-3,7 p.p. favor REF sinaliza sustentação das margens forward. Receitas a apropriar de R$ 11,2 bi equivalem a ~3,5 trimestres de receita no ritmo 4T25 (receita trimestral ~R$ 3,2 bi). Nota: a [[cyrela|Cyrela]] capitaliza juros ao custo (R$ 209 mm em 2025), o que infla ligeiramente a margem bruta reportada; a margem REF de 36,0% provavelmente já incorpora esse efeito (fonte: digested/cyrela_dfp_2025_summary.md).

### Tabela comparativa (4T25)

| Empresa | Receitas a apropriar | Resultado a apropriar | Margem REF | Margem bruta DRE | Spread REF→DRE | Trimestres de visibilidade |
|---|---:|---:|---:|---:|---:|---:|
| [[cury\|Cury]] | R$ 7.701 mm* | R$ 3.382 mm | 43,3% | 40,3% | +3,0 p.p. | ~5,4x |
| [[direcional\|Direcional]] | R$ 3.800 mm | — | 44,6% | 42,8% | +1,8 p.p. | ~3,5x |
| [[tenda\|Tenda]] | — | — | 37,3% | ~36% | ~+1 p.p. | — |
| [[cyrela\|Cyrela]] | R$ 11.200 mm | — | 36,0% | 32,3% | +3,7 p.p. | ~3,5x |

\* Receitas a apropriar da Cury referentes ao 3T25 (fonte: ITR).

## Uso em modelagem

1. **Projeção de margem bruta:** ancorar a margem bruta forward na margem REF mais recente, com convergência em 2-4 trimestres.
2. **Projeção de top-line:** usar receitas a apropriar como piso de receita dos próximos 3-4 trimestres (assumindo ritmo de obras estável).
3. **Sinal de qualidade:** verificar se a margem REF está subindo, estável ou caindo trimestre a trimestre — é um indicador antecedente.
4. **Cross-check contra lançamentos:** receitas a apropriar devem crescer aproximadamente ao ritmo dos lançamentos líquidos (lançamentos − distratos − reconhecimento POC do trimestre).

## Limitações

- **Não é GAAP cross-empresa uniforme:** cada companhia define "ajustado" a seu modo. Comparar apenas após normalizar a definição.
- **Efeito mix:** no curto prazo, a margem REF pode subir por efeito de mix de projetos (mais lançamentos Faixa 3/4 em vez de Faixa 1, por exemplo), sem refletir melhora de pricing power.
- **Imune a distratos:** o cálculo é *ex-distratos*, então não captura o risco de deterioração de qualidade da carteira.

Relacionado: [[vgv]], [[distrato]], [[direcional]], [[tenda]], [[cury]], [[cyrela]], [[incorporadoras]], [[playbook_input_shock]]
