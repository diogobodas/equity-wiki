---
source: notion
notion_page_id: ed500ca3-2bce-825e-90ff-81c6538c1e0a
title: "Digest — Entrevista Dwarkesh Podcast: Mark Zuckerberg"
type: digested
empresa: generic
created: 2026-04-17
---

# Entrevista Dwarkesh Podcast — Mark Zuckerberg

## Contexto da nota

Transcrição/notas de entrevista de Mark Zuckerberg (CEO, Meta) ao podcast Dwarkesh, datada de abril de 2024. A nota cobre estratégia de IA da Meta, infraestrutura de datacenters, política de open-source para os modelos Llama, e desenvolvimento de silicon próprio (ASICs).

Empresas/projetos mencionados: **Meta**, **Llama** (família de modelos), **Azure** (Microsoft), **NVIDIA**.

---

## Fatos e dados-chave

### Infraestrutura e compute

- O modelo predecessor ao Llama 4 foi treinado em **15 trilhões de tokens**. Ao final do treinamento ainda estava aprendendo — foi possível continuar alimentando dados, mas o treinamento foi interrompido para iniciar os testes de hipóteses para o **Llama 4**. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- A razão de **inferência sobre treinamento** (*inference compute vs. training compute*) da Meta é provavelmente mais alta do que em outras empresas, dado o volume de interações nas comunidades Meta (Facebook, Instagram, WhatsApp). (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- Zuckerberg afirma que, no passado, mesmo empresas com capital ilimitado não conseguiam obter GPUs na quantidade desejada; essa restrição começa a se aliviar, mas antes disso o gargalo deverá migrar para **energia elétrica**. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- A Meta compraria clusters ainda maiores do que os que está construindo se pudesse garantir mais energia. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- Um datacenter de **1 GW nunca foi construído** e, na avaliação de Zuckerberg, levará vários anos para isso acontecer. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- Obter energia é muito mais lento do que investir em software e hardware. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

### Futuro dos produtos e agentes de IA

- A visão de Zuckerberg é que o futuro dos produtos envolverá **tarefas mais complexas e maior número de agentes**, em vez de simples chatbots. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- Há expectativa de que criadores de conteúdo possam **treinar IAs próprias** para gerar conteúdo na plataforma. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

- A geração de **dados sintéticos** para alimentar o treinamento tende a crescer de forma contínua. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md)

### Open-source vs. modelo proprietário (a partir de ~1h09min)

- A decisão de manter os modelos Llama como open-source depende de como o mercado evoluir: se o modelo final for vendido como assinatura aos usuários finais, abrir o código não faria sentido — mas a Meta não acredita que esse seja o destino final do setor. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md §open-source)

- A Meta prefere **desenvolver seus próprios modelos** para controlar exatamente o que quer construir, independentemente da demanda de terceiros. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md §open-source)

- A licença open-source tem um **limite para grandes empresas**: companhias que queiram *revender* o modelo Llama (ex: Azure da Microsoft) precisam de acordo com a Meta. Receita potencial de licenciamento para CSPs (Cloud Service Providers) existe, mas Zuckerberg não sabe qual será a magnitude. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md §open-source)

### Silicon próprio (ASICs)

- A Meta já possui **silicon customizado para inferência** em produtos como Reels, Feed de notícias e Ads. Isso liberou as GPUs NVIDIA para treinamento. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md §silicon)

- O **Llama 4 não será treinado em silicon próprio**; a migração de treinamento para ASICs é considerada "em breve" mas não imediata. (fonte: full/generic/notas/entrevista_dwarkesh_podcast_mark_zuckerberg_ed500ca3.md §silicon)

---

## Teses e dúvidas abertas

- Gargalo de energia como novo limitante de escala de IA: mais lento de resolver do que escassez de GPUs.
- Tamanho ótimo do cluster de treinamento ainda é incerto — ninguém sabe por quanto tempo o crescimento exponencial de investimento em GPUs continuará.
- Estratégia open-source da Meta como diferencial competitivo: atrair empresas que não querem depender de modelos fechados, ao mesmo tempo em que preserva controle sobre uso comercial de larga escala.
