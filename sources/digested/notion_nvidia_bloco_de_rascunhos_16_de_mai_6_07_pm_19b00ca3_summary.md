---
type: digested
source: notion
notion_page_id: 19b00ca3-2bce-8275-b6f4-816868b1686a
empresa: nvidia
periodo: 2024-05-16
created: 2026-04-16
---

# Nota Nvidia — GTC Q&A (16 [?] mai 2024)

## Contexto

Bloco de rascunhos de Q&A do GTC (GPU Technology Conference) da Nvidia, datado de 16 [?] de maio de 2024, 18h07. Trata-se de anotações do analista capturando falas de Jensen Huang (ou portavoz da empresa) durante sessão de perguntas e respostas. Formato informal — fragmentos de frases, não transcrição completa.

(fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md)

## Fatos e afirmações gerenciais

### Ethernet vs. NVLink/Spectrum-X

- Ethernet foi desenvolvida para maximizar throughput médio; não é adequada para workloads de AI, onde o gargalo é o último GPU a responder em operações coletivas (all-reduce, all-to-all, all-gather). (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- Para resolver isso, a Nvidia criou o **Spectrum-X** (rede para AI). (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- **NVLink** é considerado chave para inference: "All GPUs act as one." (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- GB200 melhora o espaço para NVLink em relação a gerações anteriores. (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)

### Posicionamento estratégico

- Nvidia se define como "acelerada computing company", não apenas gen AI — gen AI é "a vitrine". (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- Estimativa interna (fonte não especificada na nota): US$ 250 bilhões/ano deveriam ir para aceleração computacional mesmo sem gen AI. (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- Nvidia constrói datacenters inteiros para AI. (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- Hoje está substituindo CPUs; ciclos de substituição de GPUs (ex: Ampere) devem surgir em 5–6 anos — Amperes ainda são produtivos. (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)

### NIMs e mercado

- NIMs (Neural Interface Modules / microservices): "todos os modelos são gratuitos e muito acessíveis." (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- Indústrias pesadas não tiveram grande aumento de produtividade com digitalização — implicação: oportunidade para aceleração computacional. (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)
- Objetivo de expansão de mercado: precificar sistemas Blackwell com TCO adequado a cada segmento, sem fazer média que prejudique penetração. (fonte: full/generic/notas/nvidia_bloco_de_rascunhos_16_de_mai_6_07_pm_19b00ca3.md §GTC Q&A)

## Dúvidas abertas / follow-ups

- Será o B100 o primeiro a gerar receita relevante de substituição do A100? (questão levantada na nota, sem resposta registrada)
- Referência a "POST DO DYLAN SOBRE GANHO DE EFICIENCIA" — conteúdo não incluído na nota; verificar fonte externa.

## Empresas e tickers mencionados

- **Nvidia** (NVDA)

## Tese (analista)

Nota não contém tese estruturada do analista — são anotações brutas de Q&A. A implicação implícita é que NVLink + Spectrum-X diferenciam Nvidia em clusters de AI de larga escala, e que o TAM de aceleração computacional é muito maior do que o mercado de gen AI isoladamente.
