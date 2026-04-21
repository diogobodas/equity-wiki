---
source: notion
notion_page_id: f3400ca3-2bce-821b-9f5b-812e3e19ea6e
title: "Networking/Switching Call — digest"
empresa: nvidia
tags:
  - AI
  - Semis
  - Nvidia
  - Arista
  - Broadcom
  - Cisco
digested_on: 2026-04-17
---

# Networking/Switching Call — Digest

## Contexto da nota

Call/discussão interna (research note) sobre o mercado de switching e networking para datacenters, com foco em como a NVIDIA pode se sobrepor com Arista e Cisco no contexto de infra de AI. Data da nota: 17/06/2024. Sem identificação de interlocutores externos.

## Estrutura do mercado de Ethernet Switching (front-end)

Quatro grandes players fornecem chips Ethernet para switches:

1. **Broadcom** — dominante, com share próximo de 100% no front-end (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Switching vs Routing)
2. **Cisco** — segundo lugar, mas forte em roteadores; pequeno em switching (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Switching vs Routing)
3. **NVIDIA** — terceiro lugar (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Switching vs Routing)
4. **Marvell** — quarto lugar (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Switching vs Routing)

Arista usa chips Broadcom em seus switches — parceria estabelecida. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Switching vs Routing)

## Back-end Ethernet — estágio inicial

O back-end ethernet para AI ainda está em estágio muito inicial. Hyperscalers querem diversificar exposição a NVIDIA. Meta está fazendo ethernet backend com Arista. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Back-end ethernet)

## Posicionamento dos Cloud Titans

- **CSPs (Amazon, Google)** compravam white box historicamente.
- **Meta e Microsoft** decidiram fazer parceria com Arista para agilidade.
- **Microsoft**: majoritariamente Arista na camada de software; Juniper, white box, Cisco e Arista nas camadas mais baixas.
- **Meta**: usa muito Arista.
- **Cisco** perdeu o ciclo inicial de buildout de infra cloud — share muito pequeno junto aos CSPs. Ponto forte de Cisco é roteamento, não switching. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §History)

## TAM de AI Networking e estimativas de mercado

- **Broadcom** estimou que AI Networking deve valer **$11 bilhões**, incluindo switching e óptica; Broadcom com ~20% de share no segmento ethernet. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Back-end ethernet)
- Desses $11 bi, **$700 milhões** seriam somente Microsoft e Meta. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Back-end ethernet)
- Switching para ethernet e infiniband deve atingir **$10 bilhões até 2027**. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Back-end ethernet)

## NVIDIA — Networking e bundling

- Networking da NVIDIA é predominantemente **InfiniBand**.
- **Jensen Huang** disse que 20% do networking NVIDIA é ethernet. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Nvidia bundle)
- Estratégia de bundling: NVIDIA vai alocar GPUs para quem comprar o bundle completo. Isso dá alavancagem para empurrar networking próprio. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Nvidia bundle)
- Risco para Arista: NVIDIA pode tomar share via bundling — mas a nota questiona o quão defensável é a posição de Arista no longo prazo. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Nvidia bundle)

## Arista — posicionamento e exposição a AI

- Arista tem pouco roteamento, mas é forte em switching.
- Diferencial de software: capacidade de rodar múltiplos workloads em paralelo, visibilidade de rede, predição de falhas. (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Arista)
- Exposição de Arista a AI Networking: questão levantada na nota — **~10% da receita para 2025 CY** (formulada como pergunta, não afirmação conclusiva). (fonte: full/generic/notas/nvidia_networking_switching_call_f3400ca3.md §Arista Specific)

## Empresas e tickers mencionados

- **NVIDIA** (NVDA) — foco principal
- **Broadcom** (AVGO) — dominante em silicon para ethernet switching
- **Arista Networks** (ANET) — principal player em switches para cloud/AI
- **Cisco** (CSCO) — forte em roteadores, fraco em switching cloud/AI
- **Marvell** (MRVL) — 4º lugar em ethernet silicon
- **Microsoft** (MSFT), **Meta** (META), **Google** (GOOGL), **Amazon** (AMZN) — hyperscalers / Cloud Titans

## Dúvidas abertas e follow-ups (analista)

- Como fatiar o mercado para mensurar sobreposição NVIDIA vs Arista vs Cisco?
- Quão defensável é a posição de Arista no longo prazo diante do bundling NVIDIA?
- Players verticalizados em aceleradores (NVIDIA em GPUs, Broadcom em ASICs) têm vantagem competitiva estrutural — por quê?
- O que monitorar para avaliar NVIDIA como ameaça a Arista?
- Exposição de Arista a AI Networking: ~10% para 2025 CY?
