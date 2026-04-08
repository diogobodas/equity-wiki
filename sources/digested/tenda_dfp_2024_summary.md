---
type: digested_summary
source: sources/full/tenda/2024/dfp.md
structured: sources/structured/tenda/2024/dfp.json
empresa: tenda
periodo: 2024
created: 2026-04-08
---

# Tenda — DFP 2024 auditada (TL;DR)

**Documento:** DFP exercício findo em 31/12/2024, 68 páginas, auditada (PwC), aprovada pelo CA em 12/03/2025. Comparativo 31/12/2023.

## Os números que importam (consolidado, R$ mm)

| | 2024 | 2023 | Δ |
|---|---:|---:|---:|
| Receita líquida | 3.284,4 | 2.903,1 | +13,1% |
| Lucro bruto | 891,4 | 608,6 | +46,3% |
| **MB%** | **27,1%** | 21,0% | +6,2 p.p. |
| **MB ajustada** | **30,0%** | 23,6% | +6,4 p.p. |
| Lucro operacional (antes RF) | 295,1 | 72,7 | +306% |
| Resultado financeiro | (170,8) | (130,8) | (30,6%) |
| Lucro líquido (controladores) | **106,4** | (95,8) | virou |
| EBITDA ajustado LTM | 481,1 | 217,5 | >100% |
| Dívida bruta | 1.041,5 | 1.180,1 | (11,7%) |
| Caixa total | 849,3 | 718,8 | +18,1% |
| Dívida líquida | **192,2** | 461,3 | (58,4%) |
| **DL/PL** | **20,1%** | 53,4% | (33,3 p.p.) |
| **DL corp/PL** | **−10,3%** | 16,1% | (26,4 p.p.) |
| PL + minoritários | 956,4 | 864,4 | +10,6% |

**Operacional consolidado:** lançamentos R$ 5,46 bi VGV (+57% A/A), vendas líquidas R$ 4,52 bi (+44%), VSO 57,9%, distrato 9,6%, banco de terrenos R$ 22,8 bi VGV (62,4% permuta financeira). Repasses R$ 2,95 bi.

## A virada de 2024

2024 é o ano em que a Tenda **vira página do ciclo de quase-quebra**. Lucro líquido positivo (R$ 106 mm vs prejuízo de R$ 96 mm em 2023). Margem bruta ajustada do segmento Tenda atinge **36,2% no 4T24** (ex-Pode Entrar). Dívida líquida corporativa fica **negativa** pela primeira vez em anos (−10,3% do PL). Waiver de covenants encerrado em 30/06/2024 após 2 trimestres consecutivos abaixo de 15%.

A retomada de dividendos é parte da narrativa: R$ 21 mm provisionados em dez/24 (mínimos obrigatórios + intercalares), pagamento 02/07/2025.

## Segmentação on-site (Tenda) vs off-site (Alea)

| | On-site (Tenda) | Off-site (Alea) | Cons |
|---|---:|---:|---:|
| Receita líquida | 3.023,1 | 261,3 | 3.284,4 |
| Lucro bruto | 869,3 | 22,1 | 891,4 |
| MB% | **28,8%** | **8,5%** | 27,1% |
| Resultado antes RF | 366,1 | (70,9) | 295,1 |
| LL | **172,7** | **(71,9)** | 100,7 |
| Ativo total | 4.633,6 | 715,3 | 5.348,9 |
| PL | 853,8 | 102,5 | 956,4 |

**Tenda gera caixa e lucro; Alea ainda queima.** A virada do consolidado é puxada inteiramente pelo segmento on-site. Alea entrou em 2024 com prejuízo de R$ 72 mm e a empresa anuncia em dez/24 a entrada do GKP (R$ 80 mm de aporte, fechado fev/25, EV R$ 1,1 bi) — o aporte sinaliza que o time não vai matar Alea, vai capitalizar.

## 8 pontos não-triviais para modelagem

1. **Cross-check vs data_pack:** ±0 em receita (3.284,4 ✓), lucro líquido (106,4 ✓), PL (956,4 ✓), dívida líquida (192,2 ✓). **Auditado bate com gerencial em 2024.**

2. **SWAP TEND3 ainda é PASSIVO em 31/12/24.** Posição líquida −R$ 18,6 mm, efeito no resultado 2024 −R$ 28,2 mm. A virada para receita só ocorre em 2025 (efeito 2025: +R$ 135 mm). **Atenção:** o resultado financeiro 2024 (−R$ 170,8 mm) ainda é "puro custo de funding" — não tem o ruído de SWAP positivo que vai aparecer em 2025. Modelagem forward que projete resultado financeiro a partir de 2024 vai subestimar a volatilidade trazida pelo SWAP daqui em diante.

3. **Apresentação do resultado financeiro mudou entre 2024 e 2025.** O DFP 2024 consolida juros + SWAP em uma linha "juros líq capitalização" (R$ 177,2 mm). O DFP 2025 separa as duas. Cross-check: 131,7 (juros 2024 limpo na DFP 2025) + 45,5 (SWAP 2024 separado na DFP 2025) = 177,2 ✓. Qualquer série temporal de "juros sobre captações" precisa harmonizar essas duas apresentações.

4. **RET continua dominando.** Alíquota efetiva consolidada 1,71% (vs nominal 34%). Base RET 1,92% (R$ 1,10 bi) + base RET 1 0,47% (R$ 530 mm — primeira aparição, regulamentado pela IN 2179 em mar/24 para Faixa 1 urbana). **Prejuízo fiscal não contabilizado consolidado: R$ 2,44 bi (crédito fiscal R$ 830 mm)** — não reconhecido por falta de perspectiva de Lucro Real.

5. **Capitalização de juros pesou menos em 2024.** Encargos capitalizados ao estoque caíram para R$ 67,1 mm (vs R$ 100,1 mm em 2023). Apropriado ao resultado: R$ 93,5 mm (vs R$ 75,6 mm). Combinação de obras girando mais rápido + menos saldo em estoque sujeito a capitalização.

6. **Estrutura societária Alea muda em 2024–2025.** Em dez/24 assinado o acordo com GKP: 6,97% por R$ 80 mm, EV R$ 1,1 bi. Aporte 50%/50% (fev/25 + ago/25), com mecanismo de ajuste em 2026 que pode levar a participação para 5,89%–8,11%. Após a entrada, Tenda deixa de ter 100% da Alea — minor passa a aparecer no PL.

7. **Cessão de crédito acelerou em 2024.** Quatro operações vivas em 31/12/24 (vs duas em 31/12/23): saldo cessão consolidado R$ 488 mm (vs R$ 229 mm em 2023). Despesa de cessão na DRE saltou para R$ 52,8 mm (vs R$ 29,3 mm). É uma alavanca de geração de caixa que tem custo marginal próprio — modelagem do funding mix precisa isolar.

8. **Ações em tesouraria zeradas em 31/12/24.** Após vendas em 2022/23. Retomada dos programas de recompra só em jan/25 (eventos subsequentes: 676 mil ações recompradas, 516 mil canceladas → 122,6 mm de ações ordinárias). Base de ações final 31/12/24: **123.094.246**, idêntica a 31/12/23.

## Fontes preservadas

- `full/tenda/2024/dfp.md` — transcrição estruturada-mas-uncut (RA, BP, DRE, DMPL, DFC, DVA, Notas 1-28). Políticas contábeis materiais (Nota 2.3.x) referenciam DFP 2025.
- `structured/tenda/2024/dfp.json` — canonical (operacional/dre/bp/dfc/financeiro_ajustado) + company_specific denso (segmentos on-site/off-site, debêntures, SWAP, IR detalhado, demandas judiciais, dividendos, capital, stock grant, custos por natureza, resultado financeiro, obras em construção, eventos subsequentes).
