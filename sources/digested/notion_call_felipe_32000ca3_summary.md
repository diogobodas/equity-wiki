---
type: digested
source: notion
notion_page_id: 32000ca3-2bce-80da-94f6-c0faa5d9ec1f
empresa: generic
created: 2026-04-17
---

# Call Felipe — Painel Copper vs. Optical em AI Data Centers

## Contexto

Transcrição de painel (moderado por Felipe) com dois especialistas: Ayub, gerente de projetos de data centers na AWS, e Jian (GN), arquiteto de redes na Dell Technologies. Discute o mix de conectividade cobre × óptica em clusters de IA, tendências de custo, confiabilidade, thermal limits e posicionamento de empresas. Sem data explícita; nota criada em 2026-03-11.

---

## Deployment mix atual

- Intra-rack: aproximadamente 70–80% cobre (passivo ou ativo), 20–30% óptico (fonte: full/generic/notas/call_felipe_32000ca3.md §Current Deployment Mix)
- Inter-rack: inversão — aproximadamente 70–80% óptico, dominado pelo requisito de distância e largura de banda (fonte: full/generic/notas/call_felipe_32000ca3.md §Current Deployment Mix)
- Hierarquia: chip-to-chip (GPU–GPU, GPU–CPU) = 100% cobre; scale-up (intra-rack) = maioria cobre; scale-out (inter-rack) = 100% óptico; scale-across (DC a DC) = 100% óptico (fonte: full/generic/notas/call_felipe_32000ca3.md §Connectivity Hierarchy)
- Regra geral: "If copper works, use copper wherever it works until it doesn't work, then use optics" (fonte: full/generic/notas/call_felipe_32000ca3.md §Connectivity Hierarchy)

---

## Custo e TCO

- Transceivers ópticos são aproximadamente 10x mais caros do que cobre (fonte: full/generic/notas/call_felipe_32000ca3.md §Cost and Reliability)
- Óptico também é aproximadamente 10x menos confiável do que cobre (fonte: full/generic/notas/call_felipe_32000ca3.md §Cost and Reliability)
- Custo de interconexão como % do custo total do sistema: atualmente ~5%, subindo para ~10% ou mais no futuro próximo, à medida que clusters requerem 500 mil–1 milhão [?] de GPUs interconectados (fonte: full/generic/notas/call_felipe_32000ca3.md §Future Projections)
- TCO óptico vs. cobre considerando sistema completo (não só cabos): estimativa de 2–5x mais caro para óptico, versus 10x quando comparando apenas o transceiver/cabo (fonte: full/generic/notas/call_felipe_32000ca3.md §Cost and Reliability)

---

## Limitações físicas do cobre em velocidades crescentes

- A 200 Gbps por lane: alcance do cobre limitado a ~2 metros (fonte: full/generic/notas/call_felipe_32000ca3.md §Physical and Technical Limitations)
- A 400 Gbps por lane: alcance do cobre provavelmente inferior a 1 metro (fonte: full/generic/notas/call_felipe_32000ca3.md §Physical and Technical Limitations)
- Próxima geração de produtos deverá ainda usar cobre para maioria do scale-up; duas gerações além são difíceis de prever (fonte: full/generic/notas/call_felipe_32000ca3.md §Future Projections)
- "Don't bet against copper" — cobre superou previsões de obsolescência por décadas (fonte: full/generic/notas/call_felipe_32000ca3.md §Future Projections)

---

## Comparativo ACC / AEC / AOC

| Tecnologia | Consumo de energia | Alcance (1.6T aprox.) |
|---|---|---|
| ACC (Active Copper Cable) | Menor | ~2–3 metros |
| AEC (Active Electrical Cable) | Médio | ~5 metros |
| AOC (Active Optical Cable) | Maior | 10–100+ metros |

(fonte: full/generic/notas/call_felipe_32000ca3.md §Active Cable Technologies)

- Transceivers ópticos se aproximando de 30 W por porta ou mais nas gerações mais novas (fonte: full/generic/notas/call_felipe_32000ca3.md §Power Consumption)
- Muitos ambientes de IA já operam muito próximos dos limites térmicos em comparação com racks de cloud tradicional (fonte: full/generic/notas/call_felipe_32000ca3.md §Power Consumption)
- Rack disaggregation está emergindo como tendência para gerir densidade de energia, mas aumenta os requisitos de alcance e pode forçar mais adoção óptica (fonte: full/generic/notas/call_felipe_32000ca3.md §Cooling and Rack Design)
- Liquid cooling é o novo padrão — aplicado não só a GPU trays, mas também a switch trays (fonte: full/generic/notas/call_felipe_32000ca3.md §Cooling and Rack Design)

---

## Confiabilidade e link flaps

- Ranking de confiabilidade (maior para menor): cobre passivo > cobre ativo > óptico (fonte: full/generic/notas/call_felipe_32000ca3.md §Reliability and Failure Modes)
- Modo de falha típico: degradação de rede (banda reduzida, erros de pacote), não falha de compute (fonte: full/generic/notas/call_felipe_32000ca3.md §Reliability and Failure Modes)
- Link flaps (link cai e volta rapidamente) podem interromper treinamento de GPU e forçar restart a partir de checkpoints; ocorrem mais no lado óptico do que no cobre (fonte: full/generic/notas/call_felipe_32000ca3.md §Reliability and Failure Modes)
- Ocorrência estimada de link flaps durante treinamento: menos de 5% (fonte: full/generic/notas/call_felipe_32000ca3.md §Reliability and Failure Modes)
- Google publicou que falha de firmware é um dos três principais modos de falha de transceivers ópticos (fonte: full/generic/notas/call_felipe_32000ca3.md §Reliability and Failure Modes)
- Operadores preferem cobre operacionalmente — óptico é suscetível a contaminação, manuseio incorreto e misuse no chão do data center (fonte: full/generic/notas/call_felipe_32000ca3.md §Reliability and Failure Modes)

---

## Co-Packaged Optics (CPO)

- Interesse crescente à medida que velocidades avançam para 1.6T, motivado por eficiência de energia e integridade de sinal (fonte: full/generic/notas/call_felipe_32000ca3.md §Co-Packaged Optics)
- Pluggables continuarão dominando nos próximos anos por razões de serviceability e confiabilidade operacional (fonte: full/generic/notas/call_felipe_32000ca3.md §Co-Packaged Optics)
- Consenso da indústria: CPO aumentará gradualmente, não da noite para o dia; ambos os modelos coexistirão no curto prazo (fonte: full/generic/notas/call_felipe_32000ca3.md §Co-Packaged Optics)
- NVIDIA pressiona fortemente CPO com Lumentum como parceiro conhecido (fonte: full/generic/notas/call_felipe_32000ca3.md §Co-Packaged Optics)

---

## Empresas e tickers mencionados

- **Credo** (sem ticker explícito) — maior presença em cobre (passivo e ativo); oportunidade em eficiência de energia e integridade de sinal para conectividade elétrica
- **Lumentum** (LITE) — foco em componentes ópticos e escala de custo; parceiro de NVIDIA em CPO; fornecedor de optical circuit switching para Google
- **Coherent** (COHR) — vantagem em manufatura e integração fotônica; também fornecedor de optical circuit switching para Google
- **NVIDIA** (NVDA) — investiu R$ n/d (US$ 2 bilhões por empresa) em Lumentum e Coherent para garantir supply chain óptico (fonte: full/generic/notas/call_felipe_32000ca3.md §Vendor Positioning)
- **Google** (GOOGL) — usa optical circuit switching; publicou que firmware é um dos três principais modos de falha de transceivers ópticos
- **AWS** / **Dell Technologies** — representados pelos painelistas; sem dados financeiros citados

---

## Takeaways para tese

- O mercado de interconnect óptico em AI data centers é estruturalmente crescente, impulsionado pela escala de GPUs e limitações físicas do cobre a velocidades >200G.
- Lumentum e Coherent têm portfólio verticamente integrado (lasers → transceivers → optical circuit switching) e supply chain garantido pelo investimento da NVIDIA — posicionamento diferenciado.
- Cobre não desaparece; a fronteira prática recua progressivamente para dentro do rack. A questão é timing e tecnologia de empacotamento (ACC/AEC/CPO).
- Interconnect como % do TCO total deve crescer de ~5% para ≥10%, o que amplia o mercado endereçável para empresas de óptica.
