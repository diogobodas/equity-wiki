---
source: notion
notion_page_id: 71600ca3-2bce-832b-b93e-015b3d834b76
title: "Reuniao DJ Reddy - Microsoft"
empresa: nvidia
digest_date: 2026-04-17
---

# Digest — Reunião DJ Reddy (Microsoft) sobre AI/Semis

## Contexto

Nota de reunião com DJ Reddy da Microsoft, datada de 2024-05-24. Caráter: conversa com IR/executivo de Microsoft abordando dinâmica de compra de GPUs, networking para AI, competição AMD vs NVIDIA e sovereign AI. Sem interlocutor do lado do analista identificado explicitamente.

(fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md)

---

## Fatos e afirmações-chave

### Adoção de AI por vertical

Microsoft vê investimento em toda a cadeia de fornecimento de AI. Verticais de expansão mencionadas: finanças, saúde (redução de custos e seguros), educação, defesa, cibersegurança, agricultura. Sovereign AI é destacado como vetor relevante — países constroem LLMs em seu próprio idioma e com dados culturais localizados, com dados retidos dentro de sua jurisdição (fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §Sovereign AI).

### GB200 NVL 72 vs B100/GB200 para hyperscalers

Hyperscalers (incluindo Microsoft) não necessitam de toda a memória empacotada no GB200 NVL 72. Preferência por maior flexibilidade de hardware e software stacks. A forma como o GB200 é montado em conjunto ("stacked together") é interpretada como estratégia da NVIDIA para aumentar receita, mas nem sempre alinhada à demanda real dos hyperscalers (fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §GB200 NVL 72).

### Networking: InfiniBand vs Ethernet

- InfiniBand: usado para workloads de alta intensidade; Microsoft faz **poucas** compras dado o custo elevado vs Ethernet (fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §Networking).
- Ethernet: utilizado para workloads de inferência; evolução para 800G torna Ethernet mais viável para ultra-low latency (fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §Networking).
- Fornecedores preferidos na camada Ethernet: **Arista Networks** (AI/low-latency), **Juniper Networks** (favorito de hyperscalers), **NVIDIA Spectrum-X** como alternativa. Cisco tem uso marginal. Intel mencionado como possível player em InfiniBand.
- Critério de seleção: alta performance e baixa latência em primeiro lugar; inovação e disrupção são o último critério.

### Edge AI / Copilot

Microsoft avalia processar parte dos workloads localmente (em PCs Surface, com voice assistant embarcado), fazendo offload para cloud apenas em tarefas complexas — modelo similar ao iCloud. A ideia de liberar uso de GPU do Copilot e alugá-la externamente foi mencionada como possibilidade (fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §Edge AI).

### AMD MI300X

- Avaliado como segundo competidor promissor, com **vantagem de preço** sobre NVIDIA (sem valores explícitos; fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §AMD).
- Problemas encontrados durante ramp-up: performance abaixo do esperado em relação ao H100 apesar de benchmarks iniciais favoráveis; problemas no ecossistema de software (necessidade de reescrever bibliotecas — treino feito em GPUs NVIDIA, inferência em AMD).
- Problema de qualidade de memória identificado.
- Microsoft **não cancelou** o pedido de MI300X, podendo ajustar o timing de entrega (fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §AMD).
- AMD teria cometido erro ao apostar somente na Samsung para memória, o que deve impactar receita no ano (sem período explícito; fonte: full/generic/notas/nvidia_reuniao_dj_reddy_microsoft_71600ca3.md §AMD).

---

## Empresas e tickers mencionados

| Empresa | Ticker | Relevância |
|---------|--------|------------|
| NVIDIA | NVDA | GPU (H100, H200, GB200, Spectrum-X) |
| Microsoft (Azure) | MSFT | Comprador de GPUs; fonte da reunião |
| AMD | AMD | MI300X — competitor #2 |
| Arista Networks | ANET | Networking Ethernet para AI |
| Juniper Networks | JNPR | Networking Ethernet para hyperscalers |
| Cisco | CSCO | Presença marginal em networking |
| Oracle | ORCL | Expandindo footprint de datacenter |
| Intel | INTC | Possível player em InfiniBand |
| Samsung | — | Fornecedor de memória para AMD |

---

## Teses, dúvidas abertas e follow-ups

- **Tese implícita (analista):** Vantagem de networking da NVIDIA pode estar enfraquecendo à medida que Ethernet evolui — Spectrum-X não é lock-in, e Arista/Juniper são preferidos.
- **Dúvida em aberto:** Cronograma de transição H100 → H200 → GB200 no portfolio da Azure.
- **Follow-up sugerido:** Azure AI Enterprise — questão foi levantada mas marcada como "já perguntada" (resposta não registrada na nota).
- **Risco AMD:** Dependência de Samsung para memória HBM pode limitar ramp; ecossistema de software (ROCm/bibliotecas) é obstáculo estrutural de médio prazo.
