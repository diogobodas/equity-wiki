---
type: digested
fonte: full/generic/Texto Reforma tributaria jan-2025.md
empresa: generic
tema: reforma_tributaria_locadoras
basis: LC 214/2025 com alterações da LC 227/2026
created: 2026-04-30
---

# Mecânica IBS/CBS para Locadoras de Veículos — Modelagem da Transição

Síntese metodológica da carga IBS+CBS sobre locadoras de veículos durante a transição tributária 2026-2033, com foco em [[localiza]] e [[movida]]. Deriva do **Art. 406 da LC 214/2025** ("Da Transição Aplicável aos Bens de Capital") combinado com Arts. 343-348 (alíquotas durante a transição). Documento preparório para apresentação + planilha de modelagem.

## Cronograma de alíquotas

- **2026:** CBS 0,9% (alíquota-teste) + IBS 0,1% (alíquota-teste); ICMS/PIS/Cofins full.
- **2027-2028:** CBS = alíquota referência − 0,1pp; IBS 0,05% estado + 0,05% município (alíquota-teste); ICMS/PIS/Cofins full.
- **2029:** CBS full; IBS alíquota referência (primeiro ano operacional); ICMS reduzido a 0,9; PIS/Cofins reduzidos proporcionalmente.
- **2030-2032:** CBS+IBS full; ICMS reduzindo (0,8 → 0,7 → 0,6).
- **2033+:** CBS+IBS plenos; ICMS = 0; PIS/Cofins = 0 (regime pleno).

Premissa de alíquota IBS+CBS combinada de referência: ~27% (CBS ~8,8% + IBS ~18,2%); pode variar conforme calibragem 2027-2033.

(fonte: full/generic/Texto Reforma tributaria jan-2025.md §§Art. 343-348 LC 214/2025, em: 2026-04-22)

## Crédito de IBS/CBS na compra (regime regular)

Mudança-chave vs sistema atual: crédito **integral e imediato no momento da compra** do veículo (não-cumulatividade plena, art. 47 LC 214/2025), ao invés de creditamento gradual ao longo da depreciação fiscal. Para locadora com alto giro, antecipa o benefício fiscal → efeito positivo no caixa do ano de aquisição.

(fonte: full/generic/Texto Reforma tributaria jan-2025.md §Art. 47 LC 214/2025; full/generic/notas/abla_reforma_tribut_ria_7e800ca3.md, em: 2026-04-22)

## Tributação na venda do seminovo — Art. 406

Aplicável à venda de máquinas, veículos e equipamentos usados que (i) estavam no ativo imobilizado por mais de 12 meses, (ii) foram adquiridos com NF idônea e (iii) foram adquiridos até 31/12/2032.

### CBS (§§1-2)

Redução aplicável **somente** se a aquisição ocorreu até **31/12/2026** com PIS/Cofins positivo. Para aquisições ≥2027 (já no regime CBS): **CBS full sobre o preço de venda total** — a locadora compensa o débito com o crédito CBS já tomado upfront na compra.

Quando aplicável, na revenda a partir de 1/1/2027:

```
CBS_devida = max(0, preço_venda − valor_líquido_aquisição) × alíquota_CBS
```

### IBS (§§3-4)

Redução aplicável se a aquisição ocorreu até **31/12/2032** com ICMS positivo. Escopo mais largo que CBS. Na revenda a partir de 1/1/2029:

```
IBS_devido = max(0, preço_venda − valor_líquido_aquisição × FATOR) × alíquota_IBS
```

**FATOR decrescente** por ano de aquisição: 1,0 (≤2028) → 0,9 (2029) → 0,8 (2030) → 0,7 (2031) → 0,6 (2032).

### Valor líquido de aquisição (§6)

- Aquisições ≤31/12/2026: valor da NF − ICMS − PIS/Cofins efetivamente creditados (presume-se 9,25% se NF não informar).
- Aquisições 1/1/2027 a 31/12/2032: base de cálculo IBS+CBS na NF + ICMS sem crédito. Como locadora no regime regular credita ICMS integral, valor líquido ≈ valor da NF.

### Piso zero

A fórmula com `max(0, ...)` significa que o IBS ou CBS devido na venda **nunca é negativo** (não gera crédito adicional ou ressarcimento sobre venda inferior ao valor líquido).

(fonte: full/generic/Texto Reforma tributaria jan-2025.md §Art. 406 LC 214/2025, em: 2026-04-22)

## Cenários numéricos (premissa: NF R$ 100k, venda R$ 80k, IBS+CBS 27%)

| Cenário | Compra | Venda | CBS | IBS | Carga total |
|---|---|---|---|---|---|
| A — Frota legada | 2025 | 2027 | 0 sobre R$ 80k (≤ líquido R$ 73,75k em alguns casos) | 0,1% sobre 80k = R$ 80 | **~zero** |
| B — Frota nova pós-CBS | 2027 | 2029 | full ~R$ 7,0k | 0 (80k ≤ 100k×1,0) | **só CBS full** |
| C — Fim de transição | 2029 | 2031 | full ~R$ 7,0k | 0 (80k ≤ 100k×0,9 = 90k) | **só CBS full** |
| D — Venda lucrativa | 2027 | 2029 a R$ 110k | full ~R$ 9,7k | (110k−100k)×18,2% = R$ 1,8k | **CBS full + IBS sobre spread** |
| E — Pós-transição plena | 2033 | 2035 | full ~R$ 7,0k | full ~R$ 14,6k | **regime pleno** |

## Implicações para [[localiza]] / [[movida]]

- **Frota legada (≤2026)** vendida 2027-2032: carga IBS+CBS **quase nula** — valida leitura da [[abla|ABLA]] de impacto "muito pouco relevante".
- **Frota nova (≥2027)** vendida durante a transição: **CBS full** sobre venda; **IBS próximo de zero** porque locadoras tipicamente vendem seminovo abaixo do valor líquido de aquisição.
- **Crédito upfront na compra** compensa o débito da venda — sistema economicamente próximo do atual mas com timing favorável ao caixa.
- **Locadoras com alto giro** se beneficiam mais do upfront credit timing.
- **Risco de assimetria**: alíquota efetiva IBS+CBS sobre **receita de locação** é incerta (possível redução setorial, não confirmada). Modelar cenários de 14% (reduzida) vs 27% (full).

## Pontos ainda incertos na regulamentação

1. Alíquota efetiva IBS/CBS sobre receita de **locação** no regime definitivo — ABLA classificou impacto geral como "muito pouco relevante" mas não cita alíquota.
2. Tratamento contábil exato crédito upfront vs débito ao longo do tempo — afeta apresentação de receita líquida e ROIC.
3. Eventual regime específico para locação de veículos (não previsto explicitamente até a redação atual).
4. Tratamento de leasing operacional vs locação simples para fleet B2B.

## Documentação de origem

- LC 214/2025 (Texto Reforma tributária jan-2025.md): texto consolidado em vigor em 2026-04-22.
- LC 227/2026: alterações introduzidas, incluindo §9 do Art. 57 (exclusão de valor de aquisição em casos sem crédito), e revisões nos arts. 343-348.
- ABLA — Reforma Tributária (notion 7e800ca3, 26/07/2024): posição do setor.
- Análise própria 2026-04-30 (esta nota).

(fonte: full/generic/Texto Reforma tributaria jan-2025.md, em: 2026-04-22; full/generic/notas/abla_reforma_tribut_ria_7e800ca3.md)
