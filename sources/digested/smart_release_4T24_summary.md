---
type: digest
empresa: smart
periodo: 4T24
tipo: release
source: sources/full/smart/4T24/release.md
created: 2026-04-30
---

# Smartfit (SMFT3) — "release" 4T24 — DIGESTÃO

## ⚠️ Avisos críticos antes de citar este conteúdo

1. **Este NÃO é um earnings release.** O documento foi protocolado na CVM sob a categoria "release" (id 828175), mas o conteúdo é uma compilação de **seis Laudos de Avaliação do Valor Contábil do Patrimônio Líquido** elaborados pela Vera Cruz Investimentos, todos com data-base 30/08/2024 e assinados em 30/09/2024. O propósito é **incorporação societária** (arts. 1.116 e 1.117 do Código Civil) de subsidiárias operacionais (academias) pela Smartfit Academia de Ginástica e Dança S.A. (CNPJ 07.594.978/0001-78).
2. **Schema mismatch.** O pipeline atribuiu `incorporadora/v1` ao ingest, mas Smartfit é operadora de academias (fitness/entertainment), não construtora. Os blocos `canonical.operacional`, `canonical.dre`, `canonical.bp` e `canonical.financeiro_ajustado` foram **deixados null** porque o documento não contém quaisquer demonstrações consolidadas da Smartfit — só BPs individuais de seis pequenas subsidiárias absorvidas. Não use este structured/ para alimentar modelagem consolidada.
3. **Cobertura periódica:** o documento não contém DRE 4T24, nem dados operacionais de unidades, nem guidance. Para resultados 4T24 efetivos da Smartfit, é necessário ingerir o release de resultados próprio (não presente no que foi protocolado nesta tranche).

## O que efetivamente está no documento

Seis laudos individuais, cada um seguindo template idêntico (Princípios → Sumário Executivo com BP em BRL → Avaliadores → Metodologia → Conclusão). Avaliador único: **Vera Cruz Investimentos Ltda.** (CNPJ 17.160.120/0001-59), assinado por Marcio Macedo de Almeida, Solange Pascholatti e Antonio Carlos Pascholatti.

| Subsidiária | CNPJ / Sede | PL apurado (BRL) | Data-base |
|---|---|---:|---|
| Academia Cohama Ltda. | 33.879.084/0001-34 — São Luís/MA | 2.937.277,14 | 30/08/2024 |
| Academia de Ginástica Tietê Plaza Ltda. | 29.445.219/0001-86 — São Paulo/SP | 2.937.906,56 | 30/08/2024 |
| Academia Smart Holandeses Ltda. | n/d (full §sumario_executivo) | 4.109.026,06 | 30/08/2024 |
| ACL Academia de Ginástica Ltda. | n/d | 1.596.310,78 | 30/08/2024 |
| Lake Academia de Ginástica Ltda. | n/d | 3.452.493,31 | 30/08/2024 |
| Smartrfe Academia de Ginástica e Dança Ltda. | Recife/PE — Boa Viagem | 34.315.268,97 | 30/08/2024 |
| **Total agregado** |  | **49.348.282,82** |  |

(fonte: full/smart/4T24/release.md §sumario_executivo de cada laudo)

### Padrão de BP das subsidiárias menores (Cohama, Tietê Plaza)

Estrutura típica: ativo dominado por **disponível** (caixa/aplicações ≈ 95% do AC) e **imobilizado de equipamentos de ginástica + imobilizado arrendado** (esteiras, musculação, IFRS 16). Passivo concentra **arrendamentos a pagar (CP+LP)** como maior obrigação. PL composto majoritariamente por capital social + lucro do exercício corrente — Cohama tinha prejuízo acumulado de R$ 484,9k zerado pelo lucro de R$ 895,7k em 2024 YTD.

Cohama: AT R$ 4,61 mm; PL R$ 2,94 mm. Tietê Plaza: AT R$ 3,88 mm; PL R$ 2,94 mm. SmartRFE é claramente a maior do lote (PL R$ 34,3 mm — ~ 70% do total incorporado), mas o documento não traz BP detalhado nesta extração (texto truncado em headers e imagens entre páginas).

## Implicações de leitura

- **Consolidação pós-incorporação**: as seis subsidiárias somam R$ 49,3 mm em PL contábil que já estavam dentro do perímetro de consolidação — a incorporação é uma simplificação societária, não um "M&A" com efeito caixa para a controladora. Eliminação de partes relacionadas pós-incorporação ainda é necessária na consolidação contábil.
- **Não há sinal financeiro novo aqui** para tese SMFT3: este é housekeeping jurídico-contábil. A leitura útil é apenas saber que SmartRFE (Recife) é uma subsidiária operacional materialmente maior que as cinco demais — o que pode ser referência para entender o footprint regional da rede.
- **Para análise fundamentalista 4T24/2024** da Smartfit: buscar o release de resultados próprio (apresentação de earnings, ITR/DFP), que não estão nesta tranche.

## Fontes
- (fonte: full/smart/4T24/release.md, em: 2024-09-30) — laudos individuais
- (fonte: full/smart/4T24/release.md §sumario_executivo da Cohama) — PL R$ 2.937.277,14
- (fonte: full/smart/4T24/release.md §sumario_executivo da Tietê Plaza) — PL R$ 2.937.906,56
- (fonte: full/smart/4T24/release.md §sumario_executivo da Holandeses) — PL R$ 4.109.026,06
- (fonte: full/smart/4T24/release.md §sumario_executivo da ACL) — PL R$ 1.596.310,78
- (fonte: full/smart/4T24/release.md §sumario_executivo da Lake) — PL R$ 3.452.493,31
- (fonte: full/smart/4T24/release.md §sumario_executivo da SmartRFE) — PL R$ 34.315.268,97
