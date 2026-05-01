---
type: digested
empresa: smart
ticker: SMFT3
periodo: 1T24
source_type: itr
source_full: sources/full/smart/1T24/itr.md
source_structured: sources/structured/smart/1T24/itr.json
created: 2026-04-30
---

# SmartFit (SMFT3) — ITR 1T24

## Cabeçalho operacional

- **Academias:** 1.469 (1.164 próprias / 305 franquias) em 15 países da AL; +31 no trim (20 próprias + 11 franquias) e **+238 LTM** — recorde de expansão (fonte: full/smart/1T24/itr.md). Guidance 2024 reiterado: **240–260 aberturas**, ≥80% próprias. 75 obras em andamento + 105 contratos assinados ao final de abril.
- **Studios:** 23 (10 próprias / 13 franquias); +2 no trim. Lançamento "One Pilates" em SP.
- **Clientes:** 4,9 mi total (+16% YoY) e **4,5 mi em academias (+18% YoY)**; +395 mil em academias no trim — 2ª melhor performance histórica. Brasil rompeu 1% da população do país.
- **Ticket médio:** +8% YoY consolidado, suportado por repasses + mix Black (66% no Brasil; 49% no México, 1ª vez com repasse no plano Black).

## Top-line e rentabilidade (ex-IFRS-16, base de gestão)

- **Receita líquida 1T24: R$ 1.259,9 mm**, +28% YoY e +11% QoQ. LTM R$ 4.522,7 mm. Mix internacional 55% (vs 52% 1T23).
  - Brasil R$ 464,8 mm (+21%); México R$ 326,1 mm (+44%, ticket +15% local); Outros AL R$ 367,6 mm (+29%).
- **Margem bruta caixa: 50,4%** (+0,2pp YoY, +0,6pp QoQ). Maduras estáveis em 52% pelo 5º tri consecutivo. Vintage 2022 já em 53% (margem > maduras, custo de ocupação inferior).
- **EBITDA ex-IFRS16: R$ 395,3 mm** (+30% YoY), margem **31,4%** (+0,5pp YoY, +2,0pp QoQ) — **recorde**. EBITDA LTM R$ 1.393,9 mm (margem 30,8%; exclui ganho de R$ 176,6 mm da reavaliação do Panamá no 1T23). Por região: Brasil 39,5% / México 42,1% / Outros AL com pressão pontual de S&M sazonal.
- **Lucro líquido ex-IFRS16: R$ 110,4 mm** (+5% YoY), margem 8,8%. Recorrente R$ 114,8 mm (margem 9,1%). LTM reportado R$ 1.175,0 mm — recorrente R$ 545,9 mm (12,1% margem) ao excluir imposto diferido R$ 483 mm (4T23) + reavaliação Panamá/Costa Rica R$ 146 mm.
- **DRE IFRS (consolidado):** receita R$ 1.259,9 mm, lucro bruto R$ 523,3 mm (margem 41,5%), EBIT R$ 277,8 mm, LL controlador R$ 93,2 mm.

## Caixa, dívida e capex

- **Caixa e garantias: R$ 2.337 mm**; dívida bruta R$ 4.163 mm (82% LP); **dívida líquida ajustada R$ 1.869 mm**; **DLA/EBITDA LTM 0,80x** (1,19x ex-IFRS16 imóveis vs 1,01x no 4T23). Subida de alavancagem reflete capex de expansão.
- **Capex 1T24: R$ 303,3 mm** (+33% YoY) — expansão 245,7 / manutenção 45,6 / corp 12,1. Capex expansão LTM R$ 1.161,4 mm. Manutenção LTM 5,9% da receita bruta das maduras.
- **Geração de caixa operacional R$ 259,0 mm** (vs R$ 367,9 1T23) — variação negativa de capital de giro de R$ 150,5 mm (Fornecedores -7d retomando média + Clientes +4d devido sazonalidade promocional). Conversão LTM EBITDA→caixa: 99%.

## Eventos subsequentes

- **9ª emissão de debêntures (5-abr-2024):** R$ 1.320 mm — 1ª série R$ 720 mm a CDI+1,32% (5y, abr/2029) + 2ª série R$ 600 mm a CDI+1,52% (7y, abr/2031). Recursos usados para resgate total da 6ª emissão em 29-abr; saldo para capital de giro.
- **Aquisição 10% remanescentes Smartfit Peru** via compra de 100% da Latam Gym S.A. (anúncio 2-mai-2024).

## Notas para modelagem

- **IFRS-16:** SmartFit reporta P&L gerencial ex-IFRS16; DRE consolidada formal está com efeito IFRS-16 (lucro bruto e EBIT diferentes). Para comparabilidade vs peers locais, usar ex-IFRS16. EBITDA ajustado IFRS-16 imóveis subtraindo direito-de-uso D&A e juros de arrendamento.
- **Schema gap:** SmartFit é fitness/serviços recorrentes — schema `incorporadora` força operacional=null. Métricas-chave (academias, alunos, ticket, EBITDA por região, vintages, margens caixa) ficam em `company_specific`. Considerar criação de schema `consumer_recorrente` ou `multi_unit_retail` para SMFT3/peers (Aren3, BBSE3 não — diferentes).
- **Sazonalidade:** 1T é historicamente o trimestre mais forte (janeiro = mês recorde de captação), mas com pico de marketing/comissionamento.
