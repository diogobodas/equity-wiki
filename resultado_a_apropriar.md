---
type: concept
aliases: [REF, Resultado a apropriar, Margem REF, Backlog de margem]
sources:
  - sources/full/direcional/4T25/release.md
  - sources/full/tenda/3T25/release.md
  - sources/structured/direcional/4T25/release.json
  - sources/structured/tenda/4T25/release.json
created: 2026-04-11
updated: 2026-04-11
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

## Benchmarks recentes

**Direcional (DIRR3):** margem REF ajustada atingiu pico histórico de **45,2% no 3T25**, recuando ligeiramente para 44,6% no 4T25. A MBA DRE do mesmo período foi de 42,1% → 42,8% — o spread de ~2 p.p. favor REF sinaliza sustentação das margens forward. Receitas a apropriar de R$ 3,8 bi = ~3,5 trimestres de receita no ritmo 4T25 (fonte: full/direcional/4T25/release.md §resultado_a_apropriar, structured/direcional/4T25/release.json :: financeiro_ajustado).

**Tenda (TEND3):** margem REF consolidada 37,3% no 4T25, mas o dado útil é a **margem REF da marca Tenda ex-Pode Entrar: 42,0% no 3T25** (pico) → 38,6% no 4T25. O patamar >37% sustenta a expectativa de margens bruta DRE em 36-37% nos próximos trimestres. Note a contaminação da Alea: margem REF Alea 21,7% no 3T25 arrasta o consolidado (fonte: full/tenda/3T25/release.md §resultado_a_apropriar, structured/tenda/4T25/release.json :: company_specific.resultado_a_apropriar).

## Uso em modelagem

1. **Projeção de margem bruta:** ancorar a margem bruta forward na margem REF mais recente, com convergência em 2-4 trimestres.
2. **Projeção de top-line:** usar receitas a apropriar como piso de receita dos próximos 3-4 trimestres (assumindo ritmo de obras estável).
3. **Sinal de qualidade:** verificar se a margem REF está subindo, estável ou caindo trimestre a trimestre — é um indicador antecedente.
4. **Cross-check contra lançamentos:** receitas a apropriar devem crescer aproximadamente ao ritmo dos lançamentos líquidos (lançamentos − distratos − reconhecimento POC do trimestre).

## Limitações

- **Não é GAAP cross-empresa uniforme:** cada companhia define "ajustado" a seu modo. Comparar apenas após normalizar a definição.
- **Efeito mix:** no curto prazo, a margem REF pode subir por efeito de mix de projetos (mais lançamentos Faixa 3/4 em vez de Faixa 1, por exemplo), sem refletir melhora de pricing power.
- **Imune a distratos:** o cálculo é *ex-distratos*, então não captura o risco de deterioração de qualidade da carteira.

Relacionado: [[vgv]], [[distrato]], [[direcional]], [[tenda]], [[incorporadoras]]
