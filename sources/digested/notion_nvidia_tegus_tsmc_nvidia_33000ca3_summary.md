---
source: notion
notion_page_id: 33000ca3-2bce-8316-a8e1-81963b1779ab
title: "Tegus/TSMC/Nvidia"
empresa: nvidia
type: digested
created: 2026-04-17
---

# Tegus/TSMC/Nvidia — Digest

## Contexto da nota

Nota do analista (Capstone) registrada em 2024-07-09. Compila um trecho de entrevista da plataforma Tegus com um expert em semicondutores, focado no processo de fabricação de wafers, a posição de TSMC no mercado de foundry, e implicações para chips da Nvidia (ex: H100). Não há nome de entrevistado identificado na fonte. A nota consiste em imagens (inacessíveis) e um trecho de transcrição textual.

## Processo de fabricação de wafers

Segundo o expert entrevistado via Tegus, o processo percorre as seguintes etapas (fonte: full/generic/notas/nvidia_tegus_tsmc_nvidia_33000ca3.md):

1. Ingot de silício puro → fatiado em wafers → limpeza.
2. Litografia: impressão da máscara no wafer.
3. Limpezas químicas; processo EUV deixa resíduos.
4. Corte do wafer em dies individuais.
5. Posicionamento do chip no substrato; tipicamente chips empilhados para I/O.
6. Empilhamento de chips ("CoWoS" — *Chip on Wafer on Substrate*): estrutura atual limitada a dois andares. Nenhuma empresa conseguiu atingir três andares de forma confiável, pois a alimentação elétrica vem da base e precisa percorrer vias de silício até o topo — empilhamento excessivo degrada a entrega de energia e cria problemas estruturais/mecânicos.

## Economias de yield e modelo contratual

O expert detalha a relação entre yield e custo total de propriedade (TCO) como determinante do preço ao cliente final (fonte: full/generic/notas/nvidia_tegus_tsmc_nvidia_33000ca3.md §CoWoS/yield):

- O exemplo dado: quando a Apple migrou para TSMC, inicialmente o contrato era **por die unitário** (Apple não pagava por wafer até TSMC demonstrar um yield específico); após atingido o patamar de yield, o contrato passou a ser **por wafer**.
- Modelos contratuais distintos (por die vs. por wafer) refletem a maturidade e confiança no yield de cada processo.

## TSMC — vantagem competitiva e desafios no Arizona

Segundo o entrevistado (fonte: full/generic/notas/nvidia_tegus_tsmc_nvidia_33000ca3.md §TSMC):

- A principal vantagem da TSMC no mercado de foundry é manter custos baixos com yields elevados.
- A operação em Taiwan é reconhecida por baixo custo e bons yields.
- O fab de 2nm no Arizona sofreu atrasos porque a TSMC foi surpreendida pelo **alto custo de operar uma fab nos EUA** — controle de custos é significativamente mais difícil do que em Taiwan.

## Nvidia — yield do H100

O expert estimou que, ao fabricar chips como o H100 da Nvidia, é possível obter **aproximadamente 40 chips por wafer ou menos** (fonte: full/generic/notas/nvidia_tegus_tsmc_nvidia_33000ca3.md §yield/H100). O número exato varia conforme as condições do processo e não é dado pela Nvidia ou TSMC publicamente.

## Empresas e tickers mencionados

- **Nvidia** (NVDA) — chip H100, cliente TSMC
- **TSMC** (TSM / 2330 [?].TW) — foundry líder, fabs Taiwan e Arizona
- **Apple** (AAPL) — exemplo de cliente com contrato yield-gated

## Teses e dúvidas abertas

Tese (analista/expert): A vantagem competitiva de TSMC é fundamentalmente operacional — yield e custo — não apenas tecnológica. A expansão nos EUA ameaça esse diferencial de custo. O empilhamento CoWoS está no limite físico do atual paradigma (dois andares), o que pode ser um gargalo para densidades de memória futuras em chips de IA.

Dúvidas abertas: As imagens embutidas na nota (inacessíveis) podem conter dados adicionais (gráficos, slides) que não foram capturados neste digest — revisar fonte original se necessário.
