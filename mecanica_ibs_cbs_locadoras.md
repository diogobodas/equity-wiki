---
type: concept
aliases:
  - Mecânica IBS CBS locadoras
  - Transição reforma tributária locadoras
  - Art. 406 LC 214/2025
sources:
  - sources/digested/nota_mecanica_ibs_cbs_locadoras_summary.md
  - sources/full/generic/Texto Reforma tributaria jan-2025.md
  - sources/digested/Texto Reforma tributaria jan-2025_summary.md
  - sources/digested/notion_abla_reforma_tribut_ria_7e800ca3_summary.md
created: 2026-04-30
updated: 2026-04-30
---

# Mecânica IBS/CBS para Locadoras de Veículos — Transição

> Framework de cálculo da carga IBS+CBS sobre o ciclo de vida da frota das locadoras durante a transição tributária (2026-2033) e regime pleno (2033+). Esta página é o **substrato técnico** para modelagem em planilha — combina os artigos relevantes da [[reforma_tributaria|LC 214/2025]] (com alterações da LC 227/2026) com cenários numéricos aplicados a [[localiza]] e [[movida]]. Também ancora a discussão para apresentações setoriais.

## Índice

1. [Cronograma de alíquotas](#cronograma)
2. [Crédito IBS/CBS na compra do ativo](#credito-compra)
3. [Tributação da venda do seminovo — Art. 406](#venda-art-406)
4. [Cenários numéricos](#cenarios)
5. [Implicações para a tese](#implicacoes)
6. [Especificação para modelagem (Excel/JSON)](#modelo)
7. [Pontos ainda incertos](#incertezas)

---

## 1. Cronograma de alíquotas <a id="cronograma"></a>

A reforma transita PIS/Cofins/ICMS para CBS+IBS gradualmente. A locadora interage com IBS+CBS em três pontos distintos: (i) compra do veículo (geração de crédito), (ii) receita de locação (débito sobre receita), (iii) venda do seminovo (débito sobre venda, com regime especial pelo Art. 406).

| Ano | CBS (federal) | IBS (estadual+municipal) | ICMS | PIS/Cofins |
|---|---|---|---|---|
| 2025 | — | — | full | full |
| 2026 | 0,9% (alíquota-teste, art. 346) | 0,1% estado (alíquota-teste, art. 343) | full | full |
| 2027 | alíquota referência − 0,1pp (art. 347) | 0,05% + 0,05% (art. 344) | full | full |
| 2028 | alíquota referência − 0,1pp | 0,05% + 0,05% | full | full |
| 2029 | full | alíquota referência (primeiro ano operacional) | reduzido fator 0,9 (art. 501) | reduzido proporcionalmente |
| 2030 | full | full | reduzido 0,8 | reduzido |
| 2031 | full | full | reduzido 0,7 | reduzido |
| 2032 | full | full | reduzido 0,6 | reduzido |
| 2033+ | full | full | **0** | **0** |

(fonte: sources/full/generic/Texto Reforma tributaria jan-2025.md §§Arts. 343-348 LC 214/2025, em: 2026-04-22)

**Premissas para modelagem (consenso atual de mercado):**

- Alíquota IBS+CBS combinada de referência: **~27%** (CBS ~8,8% + IBS ~18,2%)
- Spread potencial de calibragem: ±2 pp ao longo de 2027-2033
- PIS/Cofins atuais: 9,25% sobre receita bruta com créditos amplos
- ICMS típico veículos: 12% interestadual / 17-19% interno

---

## 2. Crédito de IBS/CBS na compra do ativo <a id="credito-compra"></a>

A mudança-chave vs. sistema atual é o **timing do crédito** (não o seu montante):

| Sistema | Quando o crédito é tomado |
|---|---|
| **Atual (PIS/Cofins/ICMS)** | Gradualmente, ao longo da depreciação fiscal do veículo (~5 anos) |
| **IBS/CBS pleno** | Integral e imediato no momento da compra (não-cumulatividade plena, art. 47 LC 214/2025) |

### Implicação por ano de compra

| Ano da compra | Crédito gerado |
|---|---|
| ≤2026 | PIS/Cofins/ICMS gradual (sistema atual) |
| 2027 | CBS upfront (alíquota referência − 0,1pp); ICMS gradual; PIS/Cofins gradual residual |
| 2028 | igual ao 2027 |
| 2029 | CBS upfront full; **IBS upfront full** (alíquota referência); ICMS gradual residual (já reduzido 0,9) |
| 2030-2032 | CBS+IBS upfront full; ICMS residual em redução |
| 2033+ | CBS+IBS upfront full; sem ICMS/PIS/Cofins |

Para a locadora com alto giro de frota (Localiza renova ~50% da frota anualmente), isso **antecipa o benefício fiscal** — efeito positivo no caixa do ano de aquisição (vs. sistema atual em que se distribui ao longo de 5 anos).

(fonte: sources/full/generic/Texto Reforma tributaria jan-2025.md §Art. 47 LC 214/2025; sources/digested/notion_abla_reforma_tribut_ria_7e800ca3_summary.md, em: 2026-04-22)

---

## 3. Tributação da venda do seminovo — Art. 406 <a id="venda-art-406"></a>

A venda do veículo usado pela locadora é uma operação tributável por IBS+CBS. **Mas existe um regime transitório especial** que reduz a carga sobre a parcela do preço que corresponde ao "valor líquido de aquisição" original.

### Aplicabilidade (caput Art. 406)

A redução aplica-se à venda de máquinas, **veículos** e equipamentos usados que cumpram **todas** estas condições:

1. Adquiridos até **31/12/2032**
2. Adquiridos com **nota fiscal idônea**
3. Permaneceram no **ativo imobilizado** do vendedor por **mais de 12 meses**

Se qualquer condição falhar → IBS+CBS incidem normalmente sobre o preço de venda total.

### Regra para CBS (§§1-2)

CBS só tem redução se a aquisição:
- Ocorreu até **31/12/2026** (i.e., antes da CBS existir)
- Esteve sujeita a PIS/Cofins com alíquota nominal positiva

**Para aquisições ≥1/1/2027** (já no regime CBS): **a redução NÃO se aplica** → CBS full sobre preço de venda total. A locadora compensa esse débito com o crédito CBS já tomado upfront na compra.

Quando aplicável (frota legada vendida em 2027+):

```
CBS_devida = max(0, preço_venda − valor_líquido_aquisição) × alíquota_CBS
```

### Regra para IBS (§§3-4)

IBS tem redução se a aquisição:
- Ocorreu até **31/12/2032**
- Esteve sujeita a ICMS com alíquota nominal positiva

Escopo mais largo que CBS. Na revenda a partir de 1/1/2029:

```
IBS_devido = max(0, preço_venda − valor_líquido_aquisição × FATOR) × alíquota_IBS
```

**FATOR decrescente** conforme ano de aquisição:

| Ano da aquisição | FATOR |
|---|---|
| ≤2028 | **1,0** |
| 2029 | **0,9** |
| 2030 | **0,8** |
| 2031 | **0,7** |
| 2032 | **0,6** |
| ≥2033 | redução não se aplica (ICMS = 0) |

### Definição de "valor líquido de aquisição" (§6)

Para aquisições **até 31/12/2026**:

```
valor_líquido = valor_NF − (ICMS + PIS + Cofins efetivamente creditados na aquisição)
```

Se a NF não informar PIS+Cofins, presume-se 9,25% (1,65% PIS + 7,6% Cofins).

> **Aproximação prática:** valor_líquido_2026 ≈ valor_NF × (1 − 0,17 − 0,0925) ≈ valor_NF × **0,7375**

Para aquisições **1/1/2027 a 31/12/2032**:

```
valor_líquido = base_cálculo_IBS_CBS_NF + ICMS sem crédito
```

Como a locadora no regime regular toma o crédito ICMS integralmente, "ICMS sem crédito" tende a zero.

> **Aproximação prática:** valor_líquido_2027+ ≈ **valor_NF**

### Piso zero

A fórmula `max(0, ...)` significa que IBS ou CBS devido na venda **nunca é negativo**. Se preço_venda < valor_líquido × FATOR, o tributo é zero — não gera crédito adicional ou ressarcimento.

Como locadoras tipicamente vendem seminovo **abaixo** do valor de NF (depreciação contábil ~20-35% no holding period), o IBS na venda fica em **zero ou muito próximo** durante toda a transição (2029-2032).

(fonte: sources/full/generic/Texto Reforma tributaria jan-2025.md §Art. 406 LC 214/2025 com alterações LC 227/2026, em: 2026-04-22)

---

## 4. Cenários numéricos <a id="cenarios"></a>

**Premissas comuns:**
- Compra: R$ 100.000 na NF
- Venda como seminovo: R$ 80.000 (depreciação 20% no holding period — típico Localiza)
- Venda lucrativa (cenário alternativo): R$ 110.000
- Alíquota CBS = 8,8%; alíquota IBS combinada = 18,2%; total IBS+CBS = 27%

### Cenário A — Frota legada (compra 2025, venda 2027)

- Valor líquido aquisição: R$ 100k − ICMS (R$ 17k) − PIS+Cofins (R$ 9,25k) = **R$ 73.750**
- CBS (§2): max(0, 80k − 73,75k) × 8,8% = **R$ 550**
- IBS em 2027: alíquota-teste 0,1% sobre 80k = **R$ 80**
- **Carga total ≈ R$ 630** (vs ~R$ 6,5k no sistema atual em PIS/Cofins/ICMS sobre venda)

### Cenário B — Frota nova (compra 2027, venda 2029)

- Valor líquido aquisição: ≈ R$ 100k (ICMS creditado)
- CBS: aquisição ≥2027 → §2 não aplica → CBS full sobre R$ 80k = **R$ 7.040**
- IBS (§4, fator 1,0): max(0, 80k − 100k × 1,0) = **R$ 0**
- **Carga total = R$ 7.040** (só CBS na venda)
- Crédito CBS já tomado upfront na compra (R$ 8.800) → líquido **−R$ 1.760 (favorável)**

### Cenário C — Fim de transição (compra 2029, venda 2031)

- Valor líquido aquisição: ≈ R$ 100k
- CBS full sobre R$ 80k = **R$ 7.040**
- IBS (§4, fator 0,9): max(0, 80k − 90k) = **R$ 0**
- **Carga total = R$ 7.040**

### Cenário D — Venda lucrativa (compra 2027, venda 2029 a R$ 110k)

- Valor líquido aquisição: ≈ R$ 100k
- CBS full sobre R$ 110k = **R$ 9.680**
- IBS (fator 1,0): max(0, 110k − 100k) × 18,2% = **R$ 1.820**
- **Carga total = R$ 11.500** (CBS full + IBS sobre o spread)

### Cenário E — Pós-transição (compra 2033, venda 2035)

- §3 inciso II não atendido (ICMS = 0 em 2033) → redução IBS não se aplica
- §1 inciso I não atendido (aquisição ≥2027) → redução CBS não se aplica
- IBS+CBS full sobre R$ 80k × 27% = **R$ 21.600**
- Crédito de IBS+CBS = R$ 27k tomado na compra em 2033 → líquido **−R$ 5.400 (favorável)**

### Tabela-resumo do ciclo de vida

| Período compra → venda | CBS na venda | IBS na venda | Crédito tomado na compra | Net cash impact |
|---|---|---|---|---|
| ≤2026 → 2027-2028 | 0 sobre líq; full no excedente | alíquota-teste irrelevante | PIS/Cofins/ICMS gradual | **Quase neutro** |
| ≤2026 → 2029-2032 | 0 sobre líq; full no excedente | 0 sobre líq×1,0; full no excedente | PIS/Cofins/ICMS gradual | **Quase neutro** |
| 2027-2028 → 2029-2032 | full | 0 sobre líq×1,0; full no excedente | CBS upfront + ICMS gradual + IBS upfront a partir de 2029 | **Mismatch timing positivo** |
| 2029-2032 → ano N+2 | full | 0 sobre líq×{0,9–0,6}; full no excedente | CBS+IBS upfront + ICMS gradual residual | **Mismatch timing** |
| ≥2033 → ano N+2 | full | full | CBS+IBS upfront full | **Neutro** (regime pleno) |

---

## 5. Implicações para a tese <a id="implicacoes"></a>

### Para [[localiza|Localiza]] e [[movida|Movida]]

- **Frota legada (≤2026)** vendida 2027-2032: carga IBS+CBS **quase nula** — valida a leitura da [[abla|ABLA]] ("muito pouco relevante na transição") e cria **vento de cauda fiscal de curto prazo**.
- **Frota nova (≥2027)** vendida durante a transição: **CBS full** sobre venda; **IBS próximo de zero** porque locadoras tipicamente vendem seminovo abaixo do valor líquido de aquisição. O crédito CBS upfront na compra compensa parcialmente o débito da venda.
- **Locadoras com alto giro de renovação** (Localiza renova ~50% ao ano) capturam mais o benefício do upfront credit timing → **vantagem competitiva relativa vs locadoras com frota envelhecida**.
- **Pós-2033**: regime neutro vs sistema atual no longo prazo (o crédito upfront + débito na venda full convergem para a equivalência econômica do PIS/Cofins/ICMS atual). Vantagem é predominantemente **timing de fluxo de caixa**, não margem.

### Risco principal: alíquota efetiva sobre receita de locação

A receita de locação em si é tributada por IBS+CBS. A alíquota efetiva ainda **não foi divulgada oficialmente** — pode ser:

- **Cenário ótimo:** alíquota reduzida setorial (~14%) — neutro ou positivo
- **Cenário neutro:** alíquota geral ~27% mas com créditos amplos (insumos, OPEX) que reduzem efetivo
- **Cenário pessimista:** ~27% sem redução, pressionando preço/volume

Modelar os 3 cenários separadamente para sensibilidade.

### Risco secundário: mismatch de fluxo de caixa pós-2033

No regime pleno (2033+), o débito de IBS+CBS na venda do seminovo **é maior em valor absoluto** que sob o sistema atual de PIS/Cofins/ICMS. Embora o crédito upfront na compra seja simétrico, o **timing entre compra (crédito) e venda (débito)** estende o capital de giro fiscal. Locadoras com alto giro mitigam, mas modelos com holding longo (Fleet) têm efeito mais sentido.

---

## 6. Especificação para modelagem (Excel/JSON) <a id="modelo"></a>

### Inputs do modelo

```
ALIQUOTAS:
  cbs_referencia: 0.088
  ibs_combinada: 0.182
  ibs_aliquota_teste_2026: 0.001
  ibs_aliquota_teste_2027_2028: 0.001
  pis_cofins_atual: 0.0925
  icms_estadual: 0.17

PARAMETROS_LOCADORA:
  preco_compra_nf: depende do mix
  preco_venda_seminovo_pct_nf: 0.65 a 0.80 (típico Localiza)
  holding_period_meses: 18-24 (RAC), 24-36 (Fleet)
  giro_anual_pct_frota: 0.50 (Localiza histórico)

CRONOGRAMA:
  ano_aquisicao -> determina FATOR e regime aplicavel
  ano_venda -> determina alíquotas vigentes
```

### Pseudocódigo

```python
def fator_ibs(ano_compra):
    if ano_compra <= 2028: return 1.0
    elif ano_compra == 2029: return 0.9
    elif ano_compra == 2030: return 0.8
    elif ano_compra == 2031: return 0.7
    elif ano_compra == 2032: return 0.6
    else: return None  # >= 2033, redução não aplica

def valor_liquido_aquisicao(ano_compra, valor_nf, icms_aliq, pis_cofins_aliq=0.0925):
    if ano_compra <= 2026:
        return valor_nf * (1 - icms_aliq - pis_cofins_aliq)
    else:  # 2027-2032
        return valor_nf  # ICMS creditado integralmente

def credito_compra(ano_compra, valor_nf):
    # Sistema atual: gradual ao longo da depreciação (modelar com curva)
    # Sob CBS+IBS: integral upfront
    if ano_compra >= 2033:
        return valor_nf * (cbs + ibs)
    elif ano_compra >= 2029:
        return valor_nf * cbs + valor_nf * ibs + valor_nf * icms_residual_year(ano_compra) / 5  # ICMS gradual
    elif ano_compra >= 2027:
        return valor_nf * cbs + valor_nf * icms / 5 + valor_nf * pis_cofins_residual / 5
    else:
        return valor_nf * (icms + pis_cofins) / 5  # full gradual

def cbs_venda(ano_compra, ano_venda, preco_venda, valor_liquido):
    if ano_venda < 2026: return 0
    if ano_venda == 2026: return preco_venda * 0.009  # alíquota-teste
    if ano_compra <= 2026:
        # §2 reduction applies
        return max(0, preco_venda - valor_liquido) * cbs_aliq(ano_venda)
    else:
        return preco_venda * cbs_aliq(ano_venda)

def ibs_venda(ano_compra, ano_venda, preco_venda, valor_liquido):
    if ano_venda < 2026: return 0
    if ano_venda == 2026: return preco_venda * 0.001
    if ano_venda in (2027, 2028): return preco_venda * 0.001
    # ano_venda >= 2029
    fator = fator_ibs(ano_compra)
    if fator is None:  # ano_compra >= 2033
        return preco_venda * ibs_aliq(ano_venda)
    return max(0, preco_venda - valor_liquido * fator) * ibs_aliq(ano_venda)
```

### Saída esperada — análise por safra de frota

Para cada safra (cohort) por ano de aquisição:
- Crédito tomado na compra (R$)
- Receita de locação acumulada (R$) × IBS+CBS sobre receita
- Débito IBS+CBS na venda do seminovo (R$)
- Net IBS+CBS por safra (R$, presente value)

Comparar com cenário contrafactual de **manutenção do sistema atual** para isolar o impacto da reforma.

---

## 7. Pontos ainda incertos na regulamentação <a id="incertezas"></a>

1. **Alíquota efetiva IBS+CBS sobre a receita de locação** — eventual redução setorial não confirmada. Watch para regulamentação infra-LC 214 e novas LCs.
2. **Tratamento contábil exato** crédito upfront vs débito ao longo do tempo — afeta apresentação de receita líquida e ROIC. Pronunciamento CPC pode ser necessário.
3. **Eventual regime específico para locação de veículos** — não previsto explicitamente até a redação atual, mas precedentes existem (combustíveis, instituições financeiras, planos de saúde, hotelaria têm regimes específicos).
4. **Tratamento de leasing operacional** vs locação simples para fleet B2B — diferença pode ser relevante para Movida (mix maior em Fleet).
5. **Bens adquiridos por importação direta** — regras de IBS+CBS na importação podem afetar a base de cálculo e crédito (relevante para frotas com modelos importados).
6. **Adequação do art. 408+** (disposições finais da transição) ao caso específico de bens de capital de longa vida útil.

---

## Páginas relacionadas

- [[reforma_tributaria]] — visão consolidada da reforma (cronograma, princípios, impactos por setor)
- [[locadoras]] — sector page com competitiva, mix produto, ciclo de seminovos
- [[localiza]] — entity page (RENT3)
- [[movida]] — entity page (MOVI3)
- [[abla]] — entidade representativa do setor (se existir; senão criar)

(fontes: sources/full/generic/Texto Reforma tributaria jan-2025.md §§Arts. 47, 343-348, 406 LC 214/2025 com alterações LC 227/2026; sources/digested/notion_abla_reforma_tribut_ria_7e800ca3_summary.md; sources/digested/nota_mecanica_ibs_cbs_locadoras_summary.md, em: 2026-04-30)
