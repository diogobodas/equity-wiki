# Tenda — Data Pack RI as-of 1T26 (summary)

- **Emissor:** Construtora Tenda S.A. (B3: TEND3)
- **Publicado:** 07-abr-2026
- **As-of:** 1T26
- **Tipo:** `data_pack` — planilha histórica mantida pelo RI, atualizada trimestralmente
- **Cobertura:** 1T11 → 1T26 (15 anos, 76 períodos entre trimestres e anuais)
- **Escopo:** Operacional + Financeiro (ajustado/gerencial) + DRE (IFRS) + BP (apenas consolidado e Alea) para Tenda (MCMV), Alea (SBPE, histórico mais curto: ~2020→1T26) e Consolidado
- **Fonte completa:** `full/tenda/data_pack_1T26.md`
- **Structured exploded:** `structured/tenda/{1T11..1T26, 2011..2025}/data_pack.json` — 76 arquivos, um por período

## O que este data pack destrava

Primeiro ingest que traz **espinha financeira histórica** da Tenda. Destravado:

- **DRE completa** (receita, custos, lucro bruto, margem bruta, SG&A, resultado financeiro, IR, lucro líquido) por trimestre e anual desde 1T11.
- **BP consolidado** (ativo/passivo/PL detalhados) por trimestre.
- **Financeiro ajustado** — EBITDA ajustado, dívida líquida (e dívida líquida ajustada por redução de capital), caixa, PL+minoritários, ROE LTM, ROCE LTM, capital empregado, receitas/resultados a apropriar (backlog de margem).
- **Segmentos Tenda MCMV e Alea SBPE** isolados em todas as dimensões acima (company_specific.segmentos).

## Arco histórico visível nos dados

Os anos fechados 2020-2025 contam o ciclo de **quase-quebra e turnaround** da Tenda (detalhado em [[tenda#arco histórico 2020-2025]]):

| Ano | Rec.Líq | Margem Bruta | EBITDA Aj | Lucro Líq | ROE |
|---|---:|---:|---:|---:|---:|
| 2020 | 2.282 | 31% | 330 | +200 | 14% |
| 2021 | 2.540 | 18% | (5) | (192) | (14%) |
| 2022 | 2.413 | 11% | (204) | **(547)** | (57%) |
| 2023 | 2.903 | 21% | 218 | (96) | (12%) |
| 2024 | 3.284 | 27% | 481 | +106 | 12% |
| 2025 | 4.173 | 30% | 686 | **+506** | 47% |

**Implicação crítica:** qualquer série histórica pré-2024 reflete uma empresa *estruturalmente diferente*. Múltiplos e margens médias históricos incluindo 2021-2023 são enganosos.

## Pontos de atenção

1. **1T26 financeiro vazio** — o data pack foi publicado no mesmo dia da prévia operacional, antes do release completo do trimestre. Portanto `structured/tenda/1T26/data_pack.json` tem operacional preenchido mas DRE/BP/financeiro em `null`. Essas lacunas serão preenchidas quando o release completo do 1T26 for ingerido.
2. **Redução de capital histórica** — a Tenda fez uma redução de capital durante o ciclo de crise (2022-2023). O data pack mantém `divida_liquida_ajustada` separada de `divida_liquida` por causa disso. Relevante para análise histórica de alavancagem.
3. **Alea tem histórico curto** — ~2020→1T26. Pré-2020, os structured/ dos períodos antigos só têm dados Tenda MCMV (Alea ausente).
4. **BP apenas consolidado + Alea simplificado** — o data pack não traz BP isolado do segmento Tenda MCMV. A visão stand-alone do MCMV vem só via Operacional + DRE + Financeiro.
5. **Sem fluxo de caixa.** O data pack não traz DFC — apenas variação de dívida líquida e caixa ao longo do tempo. DFC completa virá via DFP/ITR.

## Relação com o `previa_operacional.json` já existente

O data pack e a prévia operacional coexistem como fontes distintas em `structured/tenda/1T26/`:

- `structured/tenda/1T26/previa_operacional.json` — fonte: PDF da prévia operacional, foco operacional detalhado com breakdown Tenda/Alea/Consolidado e histórico de 9 trimestres curados.
- `structured/tenda/1T26/data_pack.json` — fonte: XLSX, dados operacionais (redundantes com a prévia, mas consistentes) + DRE/BP/financeiro (vazios para 1T26, preenchidos para anteriores).

Números operacionais 1T26 batem entre as duas fontes (ex: vendas líquidas consolidadas R$ 1.533,0 mm em ambos) — validação cruzada.
