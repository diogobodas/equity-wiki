# Tenda — DFP 2025 auditada (TL;DR)

**Source:** `sources/full/tenda/2025/dfp.md` · `sources/structured/tenda/2025/dfp.json`
**Original:** `Tenda-2025-12-31-wPTjC7R6.pdf` (79p, DFs individuais e consolidadas 31/12/2025 + comparativo 2024)
**Ingested:** 2026-04-08

## O que essa fonte destrava

Primeira ingestão de **demonstrações auditadas** da Tenda nesta wiki. Até agora a espinha financeira vinha do `data_pack` gerencial (cobertura 1T11–1T26, mas sem DFC e com notas explicativas inexistentes). O DFP 2025 traz:

1. **DFC completa** — primeira vez que entra no `structured/`. CFO consolidado 2025 R$ 290,3 mm (vs R$ 542,2 mm em 2024 — queda por crescimento forte de WC: Δ contas a receber R$ (559) mm + Δ imóveis R$ (725) mm compensados por Δ obrigações compra imóveis R$ +706 mm).
2. **Notas explicativas completas (1–25)** — base para futuros `promote_nota`: Nota 4 (contas a receber + cessão de créditos), Nota 10 (debêntures com 13ª emissão nova), Nota 11 (SWAPs), Nota 15 (IR + R$ 906,7 mm prejuízo fiscal não reconhecido), Nota 16 (contingências), Nota 17 (PL / dividendos / stock grant), Nota 24 (segmentação on-site vs off-site).
3. **Segmentação contábil on-site (Tenda) vs off-site (Alea)** com BP e DRE completos por segmento. Números impactantes: Tenda segmento **lucrou R$ 636 mm** vs Alea **perdeu R$ 152 mm** (atribuível aos controladores Tenda R$ +636 / Alea R$ -130). Consolidado R$ 505,7 mm.

## Highlights consolidados 2025

| Métrica | 2025 | 2024 | Δ |
|---|---:|---:|---|
| Receita líquida | 4.173,4 | 3.284,4 | +27,1% |
| Lucro bruto | 1.255,4 | 891,4 | +40,8% |
| Margem bruta | 30,1% | 27,1% | +3,0 p.p. |
| Lucro bruto ajustado (+juros cap.) | 1.336,7 | 984,9 | +35,8% |
| Resultado financeiro líquido | +4,4 | (170,8) | **+175 mm turnaround** |
| Lucro líq controladores | **505,7** | 106,4 | +375% |
| LPA básico (R$) | 4,1225 | 0,8645 | +377% |
| EBITDA ajustado (implícito) | 941,5 ann. | ~481 | +96% |
| Dívida líquida | 266,0 | 192,2 | +38% |
| Dívida líquida / PL | 22,1% | 20,1% | +2,0 p.p. |
| PL | 1.204,9 | 956,4 | +26% |
| Caixa + TVM | 1.046,9 | 849,3 | +23% |

## Mudanças relevantes no balanço patrimonial

- **Debêntures 2025**: 13ª emissão R$ 300 mm (31/10/2025) — CRI 96,78% com vencimento out/2030 + caudinhas em 2031/2032. Elevou dívida de debêntures de R$ 541 → R$ 993 mm. Duration da dívida 24,2 meses, custo médio nominal 13,67% a.a.
- **Risco Sacado**: R$ 165,5 mm consolidado (vs R$ 109,9 mm), prazo 121 dias — apresentado em fornecedores, não em dívida. Taxa 1,35–1,55% a.m. Total fornecedores + risco sacado R$ 342,9 mm.
- **Contas a receber** (consolidado, líquido): R$ 1.837 mm (+26% A/A). AVP a taxa de desconto de 4,97% a.a. (vs 7,67% em 2024, reflete queda da curva real implícita na captação).
- **Cessão de créditos**: R$ 603,4 mm (5 operações vigentes, última em 30/06/2025 a CDI+2% mais baixa que as anteriores).
- **Imóveis a comercializar**: R$ 2.829 mm (+25%), com expansão de terrenos (+R$ 430 mm) compatível com +25% de banco de terrenos.
- **Obrigações compra imóveis**: R$ 2.381 mm (+29%), coerente com permuta +67,6% do banco de terrenos.

## Covenants

- Covenant (a) 8ª emissão: (Dívida − SFH − Caixa) / PL ≤ 15%. Em 31/12/2025: **(4,53)%** ✓ (folgadíssimo).
- Covenant (b) 10ª/11ª/12ª/13ª emissões: idem subtraindo saldos CEF não liberados (R$ 1.180 mm). Em 31/12/2025: **(102,92)%** ✓.
- Ambos adimplentes.

## Dividendos

- R$ 150 mm distribuídos sobre lucro 2025 (= 29,7% do lucro líquido consolidado; 31,2% sobre base pós-reserva legal).
- Sequência: R$ 50 mm intercalares (aprovado set/2025, pago 30/12/2025) + R$ 100 mm intercalares (aprovado dez/2025, pago 07/01/2026).
- Saldo a pagar 31/12/2025: R$ 100 mm.

## Pontos não-triviais para modelagem

1. **Prejuízo fiscal não reconhecido R$ 2,67 bi** (crédito fiscal R$ 906,7 mm). Não contabilizado porque RET domina e não há perspectiva de Lucro Real. Implica que **a alíquota efetiva de IR permanece baixa** enquanto a empresa continuar no RET (1,23% em 2025) — um fator de rentabilidade estrutural para modelagem.

2. **On-site lucra, off-site drena**. A segmentação da Nota 24 mostra que, puro, o segmento Tenda MCMV operaria em R$ 636 mm de lucro em 2025. A Alea contribuiu com R$ (152) mm. Qualquer DCF deve modelar os dois segmentos separadamente e não pela margem consolidada (que mascara a operação rentável).

3. **Alea vai "zerar" em 2026 (guidance)**. Empresa guia consumo de caixa Alea R$ 60–80 mm em 2026 (<1,5% da receita consolidada). Se cumprir, lucro consolidado converge para próximo do lucro do segmento Tenda.

4. **EBITDA anualizado 4T25 já dentro do guidance 2026** (R$ 941 vs R$ 950–1.050 mm). Guidance 2026 é baixo se run-rate 4T25 se mantiver — sinal de que a companhia pode estar deixando espaço para upside.

5. **SWAPs atrelados a TEND3** (Nota 11): posição líquida +R$ 52,9 mm. Em 2025 geraram **R$ 135 mm de receita financeira** (vs R$ (45) mm de despesa em 2024) — uma **swing de R$ 180 mm** no resultado financeiro que vem do preço da ação, não do operacional. Nota de cautela: esta receita é não-recorrente em 2026 se TEND3 cair.

6. **Resultado financeiro ex-SWAP**: seria R$ 4,4 − R$ 135,0 = **R$ (130,6) mm**, muito mais alinhado com o passado da companhia e coerente com a dívida líquida de R$ 266 mm a CDI+spread.

7. **Stock grant ativo**: 7,3 mm opções em circulação (plano 2018). Diluição potencial a 5% do capital. LPA diluído 2025 = R$ 4,1193 (vs básico 4,1225) — diluição efetiva irrelevante em 2025 por programa 2014 ter quase zero opções residuais.

8. **Ganho em transação de capital Alea**: R$ 57,3 mm no PL (1T25), relacionado à operação com Good Karma FIP (mudança de percentuais na Alea). Não passa pelo resultado — bom saber ao conciliar DMPL.

## Conexão com data_pack

- `data_pack.json` para 2025 tinha campos preenchidos (operacional, dre, bp, financeiro_ajustado), mas pré-auditoria e sem DFC/notas. Este arquivo **supersedes** o data_pack para: DFC, notas explicativas e BP detalhado auditado. **Cross-check principal** — ambos concordam em:
  - Receita líquida 2025 = R$ 4.173,4 mm ✓
  - Lucro líq consolidado = R$ 505,7 mm ✓
  - PL consolidado = R$ 1.204,9 mm ✓
  - Dívida líquida = R$ 266,0 mm ✓

- Data_pack mantém vantagem em: granularidade gerencial por segmento (séries históricas longas desde 2011), métricas operacionais anuais (VSO, VGV decomposto, distrato %).

## Caveats

- DMPL não foi capturada integralmente pela extração de texto do PDF (página 22 veio em branco — conteúdo visual). O arquivo `full/` indica isso. Os números do PL final são consistentes via BP + DRE.
- Relatório dos auditores, Parecer do Comitê de Auditoria e Parecer do Conselho Fiscal (páginas 67–79) não foram transcritos literalmente — fragmentação da extração. Conteúdo factual chave (sem ressalvas) incorporado ao full/.
