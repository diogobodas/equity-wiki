---
source: notion
notion_page_id: 02d00ca3-2bce-8230-b623-8114f2dfe398
title: "X86 vs ARM — notas de pesquisa"
type: digested
created: 2024-04-23
empresa: generic
tags:
  - AI
  - semiconductores
---

# X86 vs ARM — Digest

## Contexto da nota

Nota de pesquisa do analista (capstone interna), criada em 23/04/2024, sem empresa específica de cobertura. Trata-se de apontamentos sobre a arquitetura de processadores x86 (Intel/AMD) versus ARM, reunindo referências externas (The Chip Letter, Chips and Cheese) e reflexões históricas sobre a rivalidade Intel–AMD. Não há envolvimento de IR ou management de empresa listada. Natureza: estudo de tema tecnológico, relevante para tese de semicondutores/AI.

## Fatos e dados-chave

- **CISC vs RISC — debate superado:** A nota cita post do Chips and Cheese contrariando "why x86 needs to die", argumentando que ARM moderno já incorpora instruções complexas, e que instruções complexas podem ser mais eficientes do que decomposição em N tarefas simples. Conclusão registrada: *"It's time to let the debate CISC vs RISC die — these are all about their origins."* (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md)

- **Vantagem de compatibilidade do x86:** Intel tem vantagem forte em compatibilidade retroativa. Smartphones baseados em ARM frequentemente têm problemas de compatibilidade com versões antigas do sistema operacional por questões de hardware ARM (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md).

- **AMD e TSMC:** A nota registra a percepção de que grande parte da vantagem que a AMD teve sobre a Intel a partir dos anos 1990 decorreu do uso da TSMC como foundry, não apenas de design (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md).

- **RISC-V e escalabilidade:** Citação direta da fonte: *"A nice thing about RISC-V specifically is that the base ISA scales from tiny microcontrollers all the way up to high-performance cores... I think it would be harder to do so with x86, at least with the same performance on the small implementations."* (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md)

- **Eficiência energética CISC vs RISC:** Referência a paper acadêmico sobre gasto de energia em CISC vs RISC: https://research.cs.wisc.edu/vertical/papers/2013/hpca13-isa-power-struggles.pdf (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md). Conteúdo do paper não sumarizado na nota — apenas linkado.

- **História Intel–AMD (8086 ao 386):** Originalmente compradores exigiam dual-sourcing, o que levou a Intel a dividir o design do 8086 com a AMD. No 386, a Intel decidiu seguir sozinha. A IBM queria internalizar; a AMD não entregou muito no acordo. A AMD vendeu versão do 386 posteriormente com wafer mais eficiente do que a Intel. Um "global settlement" deu à AMD licença perpétua para usar o microcode do 386 (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md).

- **AMD K6-2:** Após a compra da Next Gen, o K6-2 foi bem recebido como boa relação custo-benefício frente ao Pentium 2 (fonte: full/generic/notas/x86_vs_arm_02d00ca3.md).

## Empresas e tickers mencionados

- **Intel** (INTC) — mencionada no contexto histórico e de compatibilidade x86
- **AMD** (AMD) — rivalidade histórica com Intel, estratégia via TSMC
- **TSMC** (TSM) — citada como fator-chave da vantagem competitiva da AMD
- Nenhuma empresa brasileira listada mencionada.

## Teses, dúvidas abertas e follow-ups

**Tese (analista):** A dicotomia CISC/RISC é essencialmente histórica e não define mais o desempenho prático dos chips modernos. A vantagem real do x86 é compatibilidade, não eficiência de ISA.

**Tese (analista):** A vantagem competitiva da AMD sobre a Intel nos anos 1990–2000 foi em grande medida operacional (TSMC) e não apenas de design de ISA.

**Follow-ups implícitos na nota:**
- Ler post completo do The Chip Letter sobre x86 (linkado mas não sumarizado).
- Ler paper sobre energia CISC vs RISC (linkado mas não discutido).
- Aprofundar história do acordo Intel–AMD no 8086/286 [?]/386 e consequências no licenciamento.
- Avaliar relevância do RISC-V como vetor de disrupção frente a x86 e ARM no contexto de AI/data center.
