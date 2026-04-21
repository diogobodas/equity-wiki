---
source: notion
notion_page_id: 97700ca3-2bce-8362-9160-81ba9a581158
title: "IBBA | Reunião com Capstone e AMD (Teodoro Marena) - 3 de maio de 2024"
empresa: nvidia
tipo: nota_reuniao
digest_date: 2026-04-17
---

# Reunião IBBA + Capstone com AMD (Teodoro Marena) — 3 [?] mai 2024

## Contexto

Reunião de 1 [?] hora (15h–16h, via Zoom) organizada pelo IBBA com Teodoro Marena, executivo da AMD com 25 anos em semicondutores (system-on-chip, storage, GPU, AI). Participantes do lado buy-side: Diogo Bodas e Bernardo Brito Correa Veiga (Capstone). Foco: competitividade da AMD em AI/GPU frente à NVIDIA. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md)

---

## Fatos e afirmações gerenciais

### Contexto macro de AI e CSPs

- ChatGPT foi o ponto de inflexão que levou empresas a internalizar AI em seus negócios. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)
- Tier-2 CSPs (cloud service providers) estão crescendo forte: Microsoft concentra parceiros grandes; organizações menores são atendidas por CSPs de segunda camada. Exemplo citado: NewTenext (hospeda cloud e entrega a aplicação). (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)
- Verticais de adoção citadas: Oil & Gas (HPC → ML-based algorithms), produção de vídeo/conteúdo (custo de produção), manufatura (controle de qualidade), autonomous drive. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)

### MI300 — ramp e supply chain

- AMD está em ramp do MI300; Marena confirma que o produto está sendo entregue, com os solavancos normais de produção. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)
- Principais parceiros OEM: Dell, Supermicro, Oracle, Microsoft — em fases distintas de adoção. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)
- AMD é descrita como o único fornecedor com produto competitivo para second-source de GPU (frente à NVIDIA). (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)
- Gargalo principal: HBM3 — supply chain apertado. Fornecedores atuais: Samsung e SK Hynix; AMD buscando adicionar Micron como terceiro fornecedor. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)
- Design chiplet: a AMD produz todos os componentes simultaneamente e usa a memória disponível quando o conjunto está pronto. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)

### ASICs vs GPUs

- Tese (Marena/AMD): ASICs não devem dominar o mercado de AI porque o mercado está mudando muito rápido — GPUs são mais flexíveis. Maturação de ASICs: talvez em 5–10 anos. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)
- Groq: tinha muito capital, mas parou de fazer hardware; mercado já passou de sua arquitetura. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Mi300)

### ROCm vs CUDA

- PyTorch e TensorFlow abstraem o hardware; AMD tem plugin que permite ao desenvolvedor decidir o backend depois. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Rocm)
- Para código legado CUDA: AMD oferece HIP, ferramenta de tradução CUDA → ROCm. Performance varia conforme tamanho do modelo. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Rocm)
- Para cada biblioteca CUDA existe um equivalente ROCm. Hugging Face abstrai boa parte do trabalho para o usuário. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Rocm)
- NVIDIA bloqueou (~2 meses antes da reunião) o uso do CUDA direcionando para outras arquiteturas, inclusive empresas que faziam tradutores. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Rocm)
- Inferência em AMD após treinamento em NVIDIA: possível. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Rocm)

### Networking — InfinityFabric vs NVLink/InfiniBand

- AMD abriu o InfinityFabric como consórcio (sem NVIDIA); alta velocidade via PCIe, topologia mesh de 8 [?]. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §InfinityFabric)
- Scale-up (dentro do rack/entre racks) vs Scale-out (entre datacenters, majoritariamente Ethernet, InfiniBand para casos muito grandes). (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §InfinityFabric)
- AMD prefere Ethernet como padrão de interconexão; Lenovo, por exemplo, tem sistema MI300X que pode usar InfiniBand da NVIDIA ou Ethernet da Broadcom. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Rocm)

### Rack solutions e OEMs

- Tensão estratégica citada: quanto mais a AMD oferecer como bundle, menos os OEMs querem trabalhar com ela. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)
- Mercado caminhando para liquid cooling (maior densidade); maioria dos data centers ainda usa air cooling. GB200NVL72 da NVIDIA tem apelo a hyperscalers nesse contexto. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)
- AMD prometeu anúncios em breve (Lisa Su na Computex, citada na reunião). (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Thoughts)

### Adoção enterprise

- Empresas preferem usar dados próprios em modelos existentes em vez de treinar do zero. Ciclo: treinamento periódico → inferência → retreinamento — as empresas ainda estão descobrindo como operar esse ciclo. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)
- Budgets para AI estão crescendo. (fonte: full/generic/notas/nvidia_ibba_reuni_o_com_capstone_e_amd_teodoro_marena_sexta_feira_3_de_maio_de_2024_97700ca3.md §Notas)

---

## Empresas e tickers mencionados

- **AMD** (ticker: AMD) — fonte primária da reunião
- **NVIDIA** (ticker: NVDA) — benchmark competitivo central
- **Microsoft** (MSFT) — OEM/CSP parceiro da AMD
- **Dell** (DELL), **Supermicro** (SMCI), **Oracle** (ORCL), **Lenovo** — OEMs do MI300
- **Samsung**, **SK Hynix**, **Micron** (MU) — fornecedores HBM
- **Broadcom** (AVGO) — Ethernet para servidores AMD
- **Groq** — ASIC player citado como cautionary tale
- **Hugging Face**, **PyTorch**, **TensorFlow** — stack de software relevante

---

## Teses e follow-ups

- **Tese (analista/contexto):** AMD é second-source credível para GPU de AI; HBM e software (ROCm vs CUDA) são os dois gargalos a monitorar.
- **Follow-up:** Anúncios de Lisa Su na Computex (mai 2024) — verificar o que foi divulgado sobre novos produtos AMD.
- **Follow-up:** Evolução da adoção de Micron como terceiro fornecedor de HBM para AMD.
- **Follow-up:** Impacto do bloqueio da NVIDIA a tradutores CUDA nos clientes enterprise que usavam HIP/ROCm como ponte.
