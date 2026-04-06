---
type: empresa
source_quality: partial
aliases: [Alea, Alea by Tenda, wood frame]
sources:
  - sectors/real_estate/companies/TEND3/outputs/index.md
  - sectors/real_estate/companies/TEND3/outputs/memory/decisions.md
  - sectors/real_estate/companies/TEND3/outputs/model/TEND3_model.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
  - sectors/real_estate/sector_profile.md
updated: 2026-04-05
---

# Alea

A **Alea** é a subsidiária de inovação da [[tenda]], focada no sistema construtivo **wood frame** (estrutura em madeira engenheirada) aplicado ao segmento econômico/[[mcmv]]. É uma aposta estratégica da Tenda em diferenciação tecnológica dentro de um mercado com tecnologia construtiva bastante homogênea.

## Wood Frame vs Parede de Concreto

| Aspecto | Parede de Concreto (Tenda principal) | Wood Frame (Alea) |
|---------|--------------------------------------|-------------------|
| Velocidade construtiva | Alta (fôrmas industrializadas) | Muito alta (componentes pré-fabricados em fábrica) |
| Custo em escala | Baixo (processo dominado) | Potencialmente baixo, mas requer escala |
| Custo em volume baixo | Alto (fôrmas fixas) | Menor (componentes independem de volume) |
| Percepção de qualidade | Padrão no Brasil | Premium percebido (inovação) |
| Aceitação de mercado | Estabelecida | Em construção |
| Sustentabilidade | Neutra | Positiva (madeira renovável) |

## Status no Modelo (2026)

A Alea está em fase de **turnaround operacional**. Com base no modelo [[tenda]] (dados verificados no index.md do TEND3):

| Premissa Alea | Valor |
|---------------|-------|
| VGV lançado / tri | R$50M |
| VSO | 30,7% |
| Margem bruta | **0,0%** (turnaround; não é erro) |
| Desp. Comerciais / Receita | 15,64% |
| G&A / tri | R$12M |
| Participação de minoritários (% EBT) | 4,5% |

**Nota sobre margem 0%:** A margem bruta da Alea está projetada em zero porque a empresa está na fase de escalonamento da tecnologia. Os primeiros empreendimentos wood frame têm custos de aprendizado elevados. O modelo não projeto margem negativa mas considera que não há contribuição positiva no curto prazo.

## Como a Alea Aparece no Consolidado TEND3

O modelo TEND3 consolida três grafos: TENDA principal + ALEA + CONSOLIDADO. A Alea contribui para o resultado consolidado via:

```
LL_TEND3 = LL_TENDA + LL_ALEA + Ajustes_consolidação − Participação_Minoritários
```

Com LL_ALEA ≈ 0 (ou ligeiramente negativo), o impacto é pequeno mas não nulo:
- **G&A corporativo**: R$12M/tri de custo fixo que pesa no EBIT
- **Receita pequena**: ~R$30M/tri de receita reconhecida via [[poc_revenue]]
- **Minoritários**: A parcela de EBT atribuída a minoritários da Alea reduz o resultado dos controladores

## Ponto de Break-Even

Para a Alea atingir margem bruta positiva, precisa resolver:

1. **Custo de mão de obra pré-fabricada**: A montagem em fábrica é eficiente em escala mas cara per capita abaixo de ~500 unidades/ano
2. **Aceitação de bancos**: CEF (principal agente de crédito MCMV) precisa aceitar wood frame como garantia com LTV normal
3. **Aceitação de compradores**: Percepção de durabilidade e segurança — barreira cultural no Brasil
4. **Cadeia de suprimentos de madeira**: Madeira engenheirada (CLT, LVL) ainda tem supply limitado no Brasil; dependência de importação encarece

**Gatilho de revisão do modelo**: Se a margem bruta da Alea atingir >5% por dois trimestres consecutivos, seria justificável elevar a premissa para 10-15% e revisar a tese de forma mais otimista.

## Wood Frame no Brasil: Contexto

O wood frame representa <1% do mercado de habitação brasileiro (2025). O Brasil tem uma das menores taxas de uso de madeira na construção entre países em desenvolvimento. As razões históricas:

- **Crenças culturais**: "Casa de madeira não é casa de verdade" — herdado de séculos de construção em alvenaria
- **Clima tropical**: Umidade e risco de insetos (cupins) → exige tratamento especial da madeira
- **Regulação**: NBR (normas ABNT) para wood frame são mais recentes e menos conhecidas pelos engenheiros
- **Fogo**: Percepção incorreta de que wood frame tem mais risco de incêndio (na verdade, madeira engenheirada tem comportamento previsível em fogo — carboniza por fora, mantém estrutura por mais tempo que aço)

## Tese de Longo Prazo

Se a Alea escalar e atingir margem bruta de 20-25%+, a Tenda terá dois negócios complementares:
1. **Tenda principal**: alta escala (~R$1.400M VGV/tri), parede de concreto, margem estável ~35%
2. **Alea**: menor volume, maior diferenciação, potencial de margem maior e posicionamento premium dentro do MCMV

O risco principal é que wood frame não ganha tração cultural e regulatória no Brasil dentro do horizonte de investimento. Nesse caso, a Alea permanece como experimento de P&D com custo de oportunidade real para os acionistas da Tenda.

**Bull case Alea**: VGV sobe para R$200-300M/tri (~15-20% do grupo) com margem 20%+ → contribuição de ~R$50-70M de EBIT adicional → ROE do grupo sobe 2-3pp.

**Bear case Alea**: Wood frame não decola, a Tenda descontinua ou vende a subsidiária, e reconhece write-off. Impacto no modelo consolidado: ~R$50-100M de perda extraordinária + eliminação do overhead de G&A (~R$12M/tri) → resultado líquido praticamente neutro.

## Comparação com Alternativas de Inovação no Setor

| Empresa | Aposta de Inovação | Status |
|---------|-------------------|--------|
| Alea (Tenda) | Wood frame (pré-fabricado em madeira) | Turnaround; escala em teste |
| [[cury]] | Formas de alumínio (industrialização do concreto) | Estabelecido e rentável; benchmark de eficiência |
| MRV | Steel frame + AHS internacional | Diversificação para EUA; complexidade adicional |
| [[cyrela]] | BIM + construtora internalizada | Eficiência incremental, não disruptiva |

A diferença da [[cury]] é que as formas de alumínio são uma evolução do mesmo sistema construtivo (concreto), enquanto o wood frame da Alea é uma ruptura tecnológica. A Cury acumula aprendizado incremental; a Alea acumula risco de curva S.

## Impacto no Modelo TEND3 Consolidado (2026E)

O modelo TEND3 projetado para 2026E (audit 2026-04-04) reflete a Alea como segmento marginal:

| Segmento | Receita 26E | MB% | LL 26E | Observação |
|---------|-------------|-----|--------|------------|
| TENDA (principal) | ~R$4.800M | ~35,5% | ~R$700M | Driver dominante |
| ALEA | ~R$120-150M | ~0% | ~0 | Contribuição mínima |
| **Consolidado** | **R$5.078M** | **33,2%** | **R$715.8M** | Margem bruta consolidada > TENDA pura por overhead menor |

A margem bruta consolidada de 33.2% é inferior à margem TENDA pura (35.5%) porque: (1) overhead da Alea diluído no total, (2) G&A corporativo da Alea (~R$12M/tri) pesa como custo fixo.

## Cronograma de Revisão do Modelo

O modelo TEND3 deve ser revisado em relação à Alea quando ocorrer qualquer um dos seguintes:

1. **Margem bruta Alea > 5% por 2 trimestres consecutivos** → elevar premissa para 10% e reavaliar tese
2. **VGV Alea > R$100M/tri** → segmento ganha relevância (~2% do grupo)
3. **CEF aceita wood frame como garantia padrão** → remove barreira estrutural de financiamento MCMV
4. **Wood frame em regulamentação municipal** → alvarás mais rápidos = ciclo mais curto

Nenhum desses gatilhos foi acionado até 2026-04-04.

## Ver Também

- [[tenda]] — empresa controladora; modelo multi-segmento (TENDA + ALEA + consolidado)
- [[mcmv]] — segmento econômico onde a Alea atua
- [[incorporadoras]] — setor e benchmarks de inovação construtiva
- [[vgv_lancamentos]] — driver de receita; VGV Alea (~R$50M/tri) vs Tenda (~R$1.400M/tri)
- [[poc_revenue]] — reconhecimento de receita por avanço de obra; ciclo ~20 meses
- [[margem_backlog]] — margem backlog da Alea ainda não publicada separadamente
- [[cury]] — benchmark de eficiência construtiva via formas de alumínio
- [[aliquota_efetiva]] — RET aplicável à Alea (MCMV qualificado) beneficia alíquota consolidada da Tenda
