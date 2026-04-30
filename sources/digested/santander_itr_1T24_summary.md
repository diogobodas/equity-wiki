---
empresa: santander
ticker: SANB11
tipo: itr
periodo: 1T24
data_publicacao: 2024-04-29
norma: BRGAAP-Cosif (Individual) / IFRS-condensado (Consolidado)
source: sources/full/santander/1T24/itr.md
structured: sources/structured/santander/1T24/itr.json
---

# Santander Brasil — ITR 1T24

## Resultado consolidado

- **Lucro líquido consolidado (IFRS):** R$ 3.060,9 mm (1T24) vs R$ 3.047,5 mm (1T23) — flat YoY na base contábil consolidada.
- **Lucro líquido gerencial:** R$ 2.936 mm citado no Comentário do Desempenho, **+42% YoY**, refletindo "antecipação de ciclos de crédito" e efeitos pontuais em PDD do segmento Atacado.
- **ROE gerencial:** 13,64% (anualizado, ex-ágio).
- **Lucro líquido individual (BRGAAP/Cosif):** R$ 3.005,9 mm — base diferente do consolidado por escopo de consolidação.

## Margem financeira e PDD

- **Margem financeira bruta consolidada (IFRS):** R$ 13.386,9 mm (+6,6% YoY vs R$ 12.559,0 mm em 1T23).
- **Resultados de intermediação (managerial):** R$ 8.997 mm — Comentário destaca margem com mercados positiva (curva de juros) e margem com clientes +3,2% QoQ (consignado, financiamento de veículos).
- **PDD líquida (consolidado IFRS):** R$ -6.799,4 mm; recuperação de crédito R$ 722,6 mm.
- **Movimento da provisão (consolidado):** saldo inicial R$ 35.375,1 mm → constituição líquida R$ 5.530,8 mm → baixas R$ -6.109,8 mm → saldo final R$ 34.796,1 mm.

## Carteira de crédito

- **Operações de crédito consolidadas:** R$ 440.324,2 mm (+2,98% QoQ).
- **Carteira BRGAAP total** (op. crédito + outros créditos): R$ 525.592,3 mm.
- **Visão expandida** (com avais, fianças, CPR, debêntures): +22,8% YoY conforme Comentário (stock não disclosado).
- **Pessoa Física:** R$ 307.734,5 mm — destaque consignado (R$ 70,8 bi), financiamento veículos (R$ 64,3 bi), imobiliário (R$ 60,2 bi), cartão (R$ 50,5 bi).
- **Renegociada (consolidado):** R$ 31.695,6 mm; cobertura 54,3%.
- **Concentração top 100:** 23,1% (top 10: 7,5%; maior devedor: 1,3%).

## Balanço (consolidado)

- **Ativo total:** R$ 1.134.125,2 mm (+1,7% QoQ vs R$ 1.115.652,8 mm em 31/12/23).
- **Empréstimos a clientes (custo amortizado):** R$ 527.318,7 mm.
- **Patrimônio líquido consolidado:** R$ 115.831,2 mm (controladora R$ 115.559,5 mm + minoritários R$ 271,7 mm).

## Capital regulatório (Conglomerado Prudencial)

- **Basileia (PR/RWA):** 14,47% (vs 14,51% em 4T23; mínimo 11,50%).
- **Nível 1:** 12,37% (mínimo 9,50%).
- **CET1 / Capital Principal:** 11,38% (mínimo 8,00%).
- **PR Total:** R$ 97.010,7 mm; **RWA Total:** R$ 670.659,6 mm (crédito 575,1 bi + mercado 38,1 bi + operacional 57,5 bi).

## Notable

- **Ação adversa Atacado** mencionada (mas sem nomear caso) como driver da volatilidade de PDD vs período anterior — banco fala em "estratégia de antecipação de ciclos" implementada em períodos anteriores.
- **Reforma tributária + Res. CMN 4.966/2021** entram em vigor 01/01/2025; banco em fase de implementação. PDD passará a critério IFRS 9-like (estágios), com impacto a divulgar.
- **PIX/Pagamentos:** crescimento de 14,2% nas receitas de serviços, com destaque para Seguros, Cartões, Mercados de Capitais.
- **Funcionários (ecossistema):** 55.210.

## Limitações desta peça

- DRE consolidada IFRS-condensada não desagrega despesas tributárias, resultado operacional vs não operacional, nem participações estatutárias — ver `company_specific._individual_brgaap` para visão BRGAAP completa do banco standalone.
- BP consolidado lumpa depósitos clientes + LCI/LCA/LF/COE + debêntures em "Obrigações por TVM ao custo amortizado" (R$ 700,7 bi) — granularidade de funding mix vem do release, não do ITR.
- Indicadores de qualidade de crédito (NPL 90+, cobertura estágio 3, NPL formation) não disclosados — release é a fonte canônica.
