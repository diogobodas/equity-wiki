---
type: concept
sources:
  - sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md
  - sources/digested/notion_bess_absae_2a700ca3_summary.md
  - sources/digested/notion_bess_jesse_catl_54500ca3_summary.md
created: 2026-04-21
updated: 2026-04-21
aliases:
  - Battery Energy Storage System
  - armazenamento de energia
  - ESS
---

# BESS — Battery Energy Storage System

**BESS** (Battery Energy Storage System) é um sistema de armazenamento de energia por baterias, tipicamente de lítio-ferro-fosfato (LFP), capaz de absorver energia elétrica da rede ou de geração própria e despachá-la em momento distinto. No contexto brasileiro, o setor está em fase de formação regulatória, com os primeiros modelos de negócio economicamente viáveis tendo emergido por volta de 2T23–1T24 (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md).

---

## Casos de uso

A CATL identifica 8 aplicações para ESS; as principais são (fonte: sources/digested/notion_bess_jesse_catl_54500ca3_summary.md):

1. **Arbitragem de preço** — caso de uso dominante; traders compram energia barata (horários de baixa demanda) e despacham no pico.
2. **Substituição de peaker plants** — plantas a combustível fóssil substituídas por baterias para atender picos de demanda.
3. **Resiliência de rede** — suporte à estabilidade para geradoras e distribuidoras.
4. **Datacenters** — offset de consumo no horário de pico + backup para geradores; segmento de crescimento acelerado.
5. **Mitigação de curtailment** — projetos solares que pagam TUST proporcional ao pico usam baterias para cortar o pico exportado (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md).
6. **Serviços ancilares** — regulação de frequência, reserva de potência; atualmente mal remunerados no Brasil (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md).

---

## Segmentos de mercado no Brasil

### Frente do medidor (front-of-meter)

Teses ainda majoritariamente teóricas; o principal catalisador é o **Leilão de Reserva de Capacidade (LRK)** (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md). A ONS historicamente não "enxergava" a bateria no modelo de despacho — a MP 304 estabeleceu o arcabouço legal que viabilizou o leilão (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md).

**LRK — parâmetros esperados:**
- Volume: 1–2 GW de potência para 4 horas = 4–8 GWh de armazenamento (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)
- Blocos de 30 MW distribuídos estrategicamente no sistema elétrico
- Modelo de receita garantida por 10 anos com penalidades por performance (semelhante a leilão de transmissão)
- Cronograma: edital digital em abril de 2026; primeiras instalações ~2028 (12–18 meses após contratação)
- Transmissoras são prováveis grandes players pelo modelo de receita garantida
- Risco: possível judicialização por inovações regulatórias e critérios locacionais

### Atrás do medidor (behind-the-meter)

Segmento com teses já em execução (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md):
- **Substituição de geradores a diesel** por baterias de lítio: operacionalização mais rápida + benefício ESG; decisão no breakeven operacional
- **Estabilizadores de frequência** para players com alta sensibilidade operacional (indústrias, hospitais)
- **C&I e GD** (deslocamento de carga) — mercado SIENAI com ~250 MW instalados em 2025 (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)

### Off-grid

Mercado já existente: ~100 mil sistemas na Amazônia (~500 MW instalados); hibridização de usinas térmicas no Amazonas (conta CCC ~R$ 13 bi, compromisso de 10 anos); Programa Luz para Todos (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md).

### Mobilidade elétrica

Garagem com 10% da frota elétrica (~1.000 ônibus) demandaria BESS de ~4–5 MW; financiamento ainda indefinido (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md).

---

## Mercado brasileiro — dimensionamento

| Métrica | Valor | Fonte |
|---|---|---|
| Potencial total do mercado | R$ 77 bilhões | ABSAE/BBI (nov/25) |
| Potencial estimado 2030 | ~4 GW | BBI/Alvarez & Marçal (out/24) |
| Participação projetada na matriz | ~6% da potência do sistema | EPE/ABSAE |
| Mercado instalado 2025 | ~1 GW | ABSAE/BBI |

(fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md; sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md)

A EPE projeta crescimento de 31% na matriz energética brasileira no plano decenal; a expansão de renováveis (eólica + solar) exigirá armazenamento para gerenciar intermitência (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md).

---

## Precificação

### Brasil

| Referência | Custo | Tendência |
|---|---|---|
| Custo instalado médio (2025) | ~R$ 1.200/kWh | queda de ~30% projetada |
| Custo instalado (projeção 2031) | <R$ 1.000/kWh | — |
| Composição do custo | equipamento BESS: 50–55%; instalação + integração + O&M: 10–20% | — |

(fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)

### Internacional (referência CATL, out/24)

| Produto | Preço |
|---|---|
| DC block | 100–130 USD/kWh |
| Solução AC completa (com PCS/inversores) | 150–180 USD/kWh |
| EPC (projeto completo) | 190–200 USD/kWh |
| Spot China | ~60 USD/kWh |

(fonte: sources/digested/notion_bess_jesse_catl_54500ca3_summary.md; sources/digested/notion_bess_absae_2a700ca3_summary.md)

Preços globais caíram ~20% (oversupply na China); mundo instalou ~200 GW em 2024. Demanda firme com projetos contratados até 2027 sustenta preços no curto prazo (fonte: sources/digested/notion_bess_jesse_catl_54500ca3_summary.md).

---

## Tecnologia e cadeia produtiva

- **Tecnologia dominante**: LFP (Lítio-Ferro-Fosfato) — estável, ciclos longos, custo em queda (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)
- **Unidade básica**: DC block (~5 MWh); descarga típica de 2–4 horas dependendo do inversor (fonte: sources/digested/notion_bess_jesse_catl_54500ca3_summary.md)
- **Diferenciador real**: inversor/PCS (Power Conversion System) e software de gestão (SOC/BMS) — não a célula em si (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)
- **Brasil**: sem expertise local para utility-scale; modelo provável é joint venture com fabricantes chineses. MP 304 (isenção de importação) reduziu incentivos para adensamento da cadeia local (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)
- **Depreciação**: fator crítico no modelo econômico — quanto mais ciclos, maior o desgaste (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md)
- **Wait time**: GSU (Grid Step-Up transformer) tem espera de 1,5–2 anos — gargalo de supply chain relevante (fonte: sources/digested/notion_bess_jesse_catl_54500ca3_summary.md)

---

## Players globais

| Player | Papel | Obs |
|---|---|---|
| **CATL** | Maior fabricante de células; vende DC blocks para integradores | Abastece Tesla Megapack |
| **[[byd\|BYD]]** | Fabricante chinês; DC blocks e soluções integradas | Presente no Brasil |
| **Tesla (Megapack)** | Integrador AC; compra células da CATL | Mais caro; software próprio para arbitragem |
| **Sungrow** | Integrador AC; verticalizado em EMS e PCS | Longa presença no mercado |
| **Canadian Solar** | Integrador relevante | — |
| **Fluence (FLNC)** | Integrador premium sem componentes próprios | Caro, entrega lenta |
| **Huawei** | Forte no Brasil (histórico em telecom) | Maior presença mencionada |

(fonte: sources/digested/notion_bess_jesse_catl_54500ca3_summary.md; sources/digested/notion_bess_absae_2a700ca3_summary.md)

---

## Players no Brasil

| Empresa | Ticker | Papel |
|---|---|---|
| [[weg\|WEG]] | WEGE3 | Player local relevante; incapaz de competir em utility-scale sem parceria chinesa |
| [[byd\|BYD]] | BYD34 | Fabricante chinês com presença local |
| Huawei | — | Maior player mencionado; time local estabelecido |
| Eletrobrás | ELET3/ELET6 | Associada ABSAE; papel na hibridização de térmicas no Amazonas |
| Cteep | — | Maior bateria do Brasil (P&D) |
| UCB Power | — | Cofundador da ABSAE; especialista em soluções de armazenamento |
| Matrix / Brasol | — | Comercializadoras operando BaaS no mercado SIENAI |

(fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md; sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md)

---

## Modelos de negócio

- **Arbitragem de preço**: compra energia barata (ex: solar na ponta) e despacha no pico; modelo mais rentável e tese central
- **Serviços ancilares**: regulação de frequência e reserva de potência; mal remunerado no Brasil — regulamentação ainda pendente
- **Receita garantida (LRK)**: modelo de transmissão com contrato de 10 anos; prováveis ganhadores são transmissoras
- **BaaS (Batteries-as-a-Service)**: Matrix e Brasol já operam; dificultado pela SELIC alta (custo de capital comprime o modelo de financiamento) (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md)
- **Atrás do medidor industrial**: tese sustentada pela operação industrial (continuidade, estabilidade de frequência), não apenas pela conta de energia (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md)

---

## Marco regulatório

| Instrumento | Conteúdo |
|---|---|
| **MP 304** | Estabelece conceito, legislação e transversalidade do armazenamento; isenção de importação para projetos de infraestrutura (REIT, até ~R$ 1 bi [?]) |
| **LRK** | Leilão de Reserva de Capacidade; publicação da portaria em 10/11/2025 |
| **ONS** | Historicamente não reconhecia baterias no despacho; mudança em curso com MP 304 |

Ponto não contemplado pela MP 304: figura do agente agregador de serviços energéticos (demanda do setor). Remuneração por ancilares sem regulamentação clara (fonte: sources/digested/notion_bess_absae_2a700ca3_summary.md).

---

## Riscos e pontos em aberto

- Leilão de capacidade sem cronograma definitivo confirmado; risco de judicialização
- Isenção fiscal da MP 304: aplica-se a componentes individuais ou apenas ao BESS completo? Interpretação em debate
- Regulamentação de licenciamento ambiental e segurança contra incêndios ainda pendente
- Opex no Brasil (~5%) muito acima do padrão EUA (~1–2%) — dado incerto, requer verificação independente (fonte: sources/digested/notion_baterias_bbi_alvarez_mar_al_rafael_rodrigues_ea800ca3_summary.md)
- SELIC alta comprime modelos BaaS e aumenta custo de capital para projetos de longa maturação
- Adensamento local improvável enquanto MP 304 zera tarifa de importação
