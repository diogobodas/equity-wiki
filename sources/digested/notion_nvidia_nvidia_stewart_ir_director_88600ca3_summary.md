---
source: notion
notion_page_id: 88600ca3-2bce-8341-a06e-016085c925f3
empresa: nvidia
type: digested
created: 2026-04-17
---

# NVIDIA — Reunião com Stewart (IR Director)

## Contexto da nota

Nota de reunião com o diretor de Relações com Investidores da NVIDIA (identificado como "Stewart"). Data de criação da página: 2024-06-05. Conteúdo é transcrição/paráfrase de Q&A com IR, com foco em margens brutas, arquitetura de produtos (Blackwell/GB200/NVLink), gargalos de supply chain e estratégia de networking.

Empresas e tickers mencionados: **NVIDIA (NVDA)**.

---

## Fatos e afirmações-chave

### Margens brutas
- Segundo IR, as otimizações de custo devem ajudar as margens brutas a convergirem para **75%** quando considerados os preços médios de venda (ASP). (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)
- A venda não inclui o rack completo — a empresa vende compute e network trays, o que não altera materialmente as margens brutas. (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)

### Arquitetura de produto — HGX/DGX/NVLink
- A empresa está expandindo o HGX para o formato DGX ("making the HGX bigger into a DGX"). (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)
- NVLink é descrito como fundamental para escalar a capacidade de computação; foi a motivação principal para a aquisição da Mellanox.
- O NVLink foi estendido de 8 GPUs (HGX) para conexão de até **72 GPUs** (GB200 NVL 72). (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)
- **576 GPUs** podem ser conectadas via 8 sistemas GB200NVL 72 (calc: 8 × 72 = 576). (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)
- Datacenters estão se tornando progressivamente mais densos.

### Oportunidade de networking
- Oportunidade de networking avaliada em **US$ 60 bilhões**, incluindo DPUs, cabling e transceivers. (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)
- Segundo IR, a NVIDIA não vê outros players de ethernet para datacenter como competidores diretos porque a empresa está fazendo "networking para AI", não networking genérico.

### Estratégia em ASICs
- Questionado sobre entrada no mercado de ASICs, IR respondeu que a empresa se disponibilizaria a ajudar clientes a usar a tecnologia NVIDIA para desenvolver algo muito específico (ex.: para um CSP), mas não anunciou entrada como concorrente de ASICs proprietários. (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)

### Gargalos de supply chain — CoWoS e HBM
- CoWoS e HBM ainda estão apertados (supply tight). (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)
- Blackwell usa um novo tipo de CoWoS e nova memória — por ser uma plataforma nova, a empresa está "starting from day one" e espera ser supply-constrained **neste ano e no próximo** (referência a 2024–2025, dado a data da nota). (fonte: full/generic/notas/nvidia_nvidia_stewart_ir_director_88600ca3.md)

---

## Teses e follow-ups (analista)

- Tese (analista): O mix shift para full-stack rack (GB200 NVL) não comprime margens porque a NVIDIA captura o networking layer (NVLink/Mellanox) — o "rack" é marketing; o produto faturado são compute + network trays.
- Follow-up aberto: Qual a timeline esperada para alivio do supply constraint de CoWoS/HBM no Blackwell? A nota não traz data específica além de "this year and next year".
- Follow-up aberto: Confirmar o tamanho da oportunidade de networking de US$ 60 bi com fontes primárias (earnings calls ou investor day).
