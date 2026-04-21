---
source: notion
notion_page_id: d3500ca3-2bce-823a-b775-014d509f5bdf
type: digested
empresa: generic
created: 2026-04-17
---

# Nota Capstone — Tabela de Supercomputadores: GPU Content e Revenue Estimado (jun/2024)

## Contexto da nota

Nota de pesquisa interna (analista), datada de 3 [?] de junho de 2024, contendo uma tabela de supercomputadores de alto desempenho com dados de CPU, GPU e estimativa de receita de GPU por sistema. O objetivo aparente é quantificar o conteúdo de GPU em grandes instalações de HPC (High Performance Computing) como proxy de demanda e receita dos fabricantes de GPU.

## Tabela de supercomputadores — dados brutos

Os dados abaixo são transcritos diretamente da fonte. Números em notação PT-BR (ponto como separador de milhar).

(fonte: full/generic/notas/nota_3_de_jun_3_23_pm_nome_pais_data_cpu_cores_k_fabricante_gpu_gpus_gpu_asp_gpu_revenue_k_usd_frontier_eua_2022_56_d3500ca3.md)

| Nome | País | Ano | CPU Cores (K) | Fabricante GPU | # GPUs | GPU ASP (K USD) | GPU Revenue (K USD) |
|------|------|-----|--------------|----------------|--------|-----------------|---------------------|
| Frontier | EUA | 2022 | 561 | AMD | 36.992 | 15 | 554.880 |
| Aurora | EUA | 2023 | 1.104 | Intel | 63.744 | 10 | 637.440 |
| Eagle | EUA | 2023 | 172 | Nvidia | 14.400 | 25 | 360.000 |
| Fugaku | Japão | 2020 | 7.630 | — | — | — | — |
| LUMI | Europa | 2022 | 186 | AMD | 11.664 | 15 | 174.960 |
| Alps | Suíça | 2024 | 460 | Nvidia | 6.400 | 30 | 192.000 |
| Leonardo | Itália | 2023 | 110 | Ampere | 15.872 | 11 | 174.592 |
| MareNostrum | Espanha | 2023 | 89 | n/d | 4.480 | 25 | 112.000 |
| Summit | EUA | 2018 | 202 | n/d | 27.648 | 25 | 691.200 |
| EOS Nvidia Superpod | EUA | 2023 | 46 | n/d | 3.328 | 25 | 83.200 |

Nota: Fugaku não apresenta dados de GPU na fonte (indicado por `//`). Fabricante GPU de MareNostrum, Summit e EOS Nvidia Superpod não está explícito na fonte para essas linhas.

## Fatos/dados-chave

- **Maior GPU revenue estimado por sistema**: Summit (EUA, 2018) com USD 691.200K [?] (fonte: tabela §Summit), seguido de Aurora (EUA, 2023) com USD 637.440K [?] (fonte: tabela §Aurora).
- **Maior contagem de GPUs**: Aurora com 63.744 [?] GPUs Intel, seguido de Summit com 27.648 [?] GPUs (fonte: tabela §Aurora e §Summit).
- **ASP mais alto**: Alps (Suíça, 2024) — USD 30K [?] por GPU Nvidia (fonte: tabela §Alps), consistente com acelerador de nova geração (possivelmente H100).
- **AMD** aparece em Frontier e LUMI, com ASP de USD 15K [?] por GPU (fonte: tabela §Frontier e §LUMI).
- **Intel** aparece em Aurora, com ASP de USD 10K [?] por GPU e maior contagem de GPUs da lista (fonte: tabela §Aurora).
- **Nvidia** aparece explicitamente em Eagle (USD 25K [?] ASP) e Alps (USD 30K [?] ASP); EOS Nvidia Superpod também é Nvidia pelo nome, com ASP de USD 25K [?] (fonte: tabela).
- **Fugaku** (Japão, 2020) destoa com 7.630K [?] CPU cores e sem dados de GPU — arquitetura não-GPU (fonte: tabela §Fugaku).

## Empresas e tickers mencionados

- **Nvidia** (NVDA) — fabricante GPU em Eagle, Alps, e implicitamente EOS Nvidia Superpod
- **AMD** — fabricante GPU em Frontier e LUMI
- **Intel** — fabricante GPU em Aurora

Nenhuma empresa brasileira listada mencionada. Nota é genérica/setorial (AI/semiconductores).

## Tese (analista)

Tese (analista): A tabela parece ser um exercício de bottom-up para estimar receita de GPU embutida nos maiores supercomputadores mundiais, provavelmente como parte de uma análise de TAM (Total Addressable Market) de GPU para HPC/AI. A variação de ASP entre fabricantes (Intel USD 10K [?], AMD USD 15K [?], Ampere USD 11K [?], Nvidia USD 25 [?]–30K [?]) sugere que Nvidia captura significativamente mais receita por unidade mesmo com menor contagem de GPUs em alguns sistemas. Análise incompleta — fabricantes de MareNostrum e Summit não estão identificados na fonte.
