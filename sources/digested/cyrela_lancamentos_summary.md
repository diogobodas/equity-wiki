---
type: digested
source: sources/full/generic/cyrela_lancamentos.md
empresa: cyrela
ticker: CYRE3
created: 2026-04-13
---

# Cyrela — Base histórica de lançamentos (2005–2025)

## O que é a fonte

Planilha proprietária da Cyrela (extraída de `cyrela_lancamentos.xlsx`) com a **base completa de lançamentos** projeto a projeto, cobrindo **1T05 a 4T25** (1.332 empreendimentos). Cabeçalho indica **"DADOS A PARTIR DO 4T20 (PRO FORMA)"** — a partir desse trimestre os números refletem o critério pro forma usado pela companhia (consolidando 100% das SPEs em vez de aplicar % de participação para fins gerenciais).

Granularidade por linha:

| Campo | Conteúdo |
|---|---|
| Empreendimento | Nome comercial do projeto |
| Mês | Data de lançamento (mensal) |
| Trimestre | Código `1T05`–`4T25` |
| Local | Praça (SP capital, SP Interior, RJ, Sul, Nordeste, Centro Oeste, MG, ES, Campinas, Goiânia, Fortaleza, Belo Horizonte, Porto Alegre) |
| VGV (R$ MM) | VGV bruto do projeto, em R$ milhões |
| Unidades | Nº de unidades |
| Segmento | Alto Padrão, Médio, MCMV 2 e 3 (antes "CVA 2 e 3"), Vivaz Prime (categoria transitória 1T23) |
| % CBR | Participação econômica da Cyrela na SPE (0–1) |
| Contabilização | Consolidação ou Equivalência |

## Por que importa para o modelo

É o **único insumo bottom-up** capaz de reconstruir a série histórica de lançamentos por segmento, praça e marca. Permite:

1. **Reconciliar o VGV reportado** (`previa_operacional`, ITR) com a soma dos projetos individuais — útil para validar `structured/cyrela/{periodo}/previa_operacional.json`.
2. **Calcular % Cyrela vs %SPE**: cada projeto traz `% CBR`, viabilizando ponderar VGV, ticket médio e unidades pelo share efetivo (alavanca para o modelo de receita).
3. **Mapear mix de segmento ao longo do tempo** — observa-se a entrada da marca **Vivaz** (MCMV) a partir de ~2018 e seu peso crescente até 2025 (várias dezenas de Vivaz/quarter em 4T25).
4. **Mix geográfico** — concentração em São Paulo, mas diversificação relevante em RJ, Sul, Centro Oeste e SP-Interior, com presença pontual em Nordeste/MG/ES desde 2005.
5. **Marcas/JVs identificáveis** nos nomes: `Living` (médio), `Vivaz` (MCMV), `Wish`/`Now`/`Smart` (parcerias regionais — Plano&Plano, MAC, Lavvi, etc.), `RJZ Cyrela` (RJ), `By YOO`/`By Pininfarina`/`By Dolce&Gabbana` (alto padrão design).

## Pontos para roteamento na wiki

- **Página principal**: `cyrela.md` — incorporar série de VGV bruto e %CBR por trimestre/segmento, e atualização da estratégia de mix Alto Padrão vs Médio vs MCMV.
- **Página `vgv.md`**: a base permite ilustrar como construir VGV pro forma vs VGV %Cyrela; bom exemplo metodológico.
- **Página `incorporadoras.md`**: dados de Cyrela ajudam comparações setoriais (concentração geográfica, share de MCMV, ticket médio por segmento).
- **Página `mcmv.md`**: trajetória da marca Vivaz (lançamentos MCMV de Cyrela) é insumo direto.

## Observações de qualidade do dado

- **Estornos** aparecem como linhas com VGV/unidades **negativos** (ex.: `Ville Hibisco` em 4T22, R$ -12,5MM, -66 un.) — provavelmente projeto cancelado ou re-classificado. Tratar como ajuste no agregado, não como duplicidade.
- **Mudança de nomenclatura de segmento**: até 4T22 o econômico aparece como "CVA 2 e 3", a partir de 1T23 passa a "MCMV 2 e 3" (mesma faixa, rebatizada após a volta do programa em 2023). Há ainda "Vivaz Prime" como segmento standalone em 1T23 antes de ser absorvido.
- **Datas em formato `YYYY-MM-01 00:00:00`**: ou seja, mês de competência, não data exata de lançamento.
- **Linha de cabeçalho da planilha gera ruído**: as 4 primeiras linhas trazem `NaN`/Unnamed, fruto da extração do XLSX. Ignorar ao tabular.

## Próximos passos sugeridos

- Não cabe schema canônico (`structured/`) porque é série temporal histórica — manter como referência em `full/generic/`.
- Considerar gerar um **derivado agregado** (`sources/digested/cyrela_lancamentos_por_trimestre.md`) com tabela trimestre × segmento × VGV pro forma e %CBR, para facilitar consultas via `query.sh`.
- Cotejar valores agregados (4T22 em diante) com `structured/cyrela/{periodo}/previa_operacional.json` quando disponível, para validar o critério pro forma.
