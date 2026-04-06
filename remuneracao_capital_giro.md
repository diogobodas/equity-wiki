---
type: conceito
aliases: [Remuneração do Capital de Giro, Capital de Giro Bancário, Equity Hedge, NII Capital Próprio, Remuneração do PL]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/filings/releases/ITUB4_release_2025.pdf
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
note: "2026-04-03: magnitude NII_CG corrigida com dados reais do release 4T25 (R$3.9B/trim, não R$7B)"
---

# Remuneração do Capital de Giro (Bancário)

A **remuneração do capital de giro** é o sub-componente do [[nii_clientes]] que representa o retorno sobre o **patrimônio líquido** do banco aplicado às taxas de mercado. É o "equity hedge" — a parcela do NII que cresce automaticamente com a [[selic]]/CDI sem requerer crescimento de carteira ou gestão ativa de spread.

Não confundir com "capital de giro" do lado PJ de crédito (que é [[nii_sensiveis_spread]]).

## Como Funciona

```
NII_Capital_Giro ≈ Base_Capital_Alocado × Taxa_Blended_Trimestral / 100
```

**Intuição**: O banco financia parte da sua carteira de crédito com **capital próprio** (equity), não com captações de mercado (CDB, LF, depósitos). Essa parcela não tem custo de funding. O NII gerado por ela equivale a aplicar o equity a uma taxa blended de mercado — e como essa taxa segue a Selic, essa receita sobe automaticamente quando o BCB aumenta os juros.

> **Nota importante sobre o Itaú**: O PL total do banco NÃO entra integralmente no NII_CG reportado na linha "Capital de Giro Próprio e outros" da tabela de Taxas Médias. O Itaú divide o PL em duas parcelas:
> 1. **Capital alocado às áreas de negócio** (exceto tesouraria) + capital de giro da corporação → aparece como "Capital de Giro Próprio e outros" no NII_Clientes (~R$146B, 4T25)
> 2. **Capital na tesouraria** (~R$60B) → aparece no NII_Mercado (não no NII_Clientes)
>
> Portanto, usar o PL total (~R$206B) para estimar o NII_CG de clientes **superestima** significativamente o componente.

### Magnitude para Itaú (dados reais do release)

Fonte: Release 4T25, tabela "Taxas Médias anualizadas da Margem Financeira com Clientes"

| Período | Base "Capital de Giro Próprio" | Taxa anualizada | NII_CG real |
|---------|-------------------------------|-----------------|-------------|
| 3T25 | R$148,582M | 10.7% a.a. (~2.68%/trim) | R$3,850M/trim |
| 4T25 | R$146,248M | 11.2% a.a. (~2.80%/trim) | R$3,975M/trim |

Para referência: o NII Clientes total do Itaú no 4T25 foi R$30,930M. Portanto, a remuneração do capital de giro representa ~**13% do NII Clientes total** — relevante, mas bem menor do que a estimativa anterior de 25-30% sugeria.

A taxa blended (~11.2% a.a.) é superior ao CDI puro (~13.25% Selic → ~12.8% CDI anualizado), o que sugere que a base inclui instrumentos de renda fixa prefixados ou indexados a IPCA além do pós-fixado puro.

## Sensibilidade à Selic

Esta é a característica mais importante deste componente:

| Variação Selic | Impacto NII_CG (Itaú, base ~R$146B) | Nota |
|---------------|--------------------------------------|------|
| +100bps | +~R$730M–1.0B/ano | Sensibilidade efetiva ~50-70% da base × 1% (parte da base é pré-fixada) |
| -100bps | -~R$730M–1.0B/ano | Idem, negativo |
| +200bps | +~R$1.5–2.0B/ano | Ciclo típico de alta |

> **Atenção**: a base real (~R$146B) é significativamente menor do que o PL total (~R$206B). A sensibilidade por 100bps de Selic é ~R$1.46B/ano sobre a base bruta, mas como parte da base é pré-fixada, a sensibilidade efetiva é da ordem de R$730M–1.0B/ano. Estimativas anteriores usando PL total (~R$220B) superestimavam o impacto em ~50%.

**Implicação**: Quando analistas observam que o NIM de Itaú sobe com a Selic, parte desse movimento é **mecânico** (remuneração do equity, não gestão de spread). É importante separar o que é alfa do banco do que é beta da Selic. Porém, a magnitude desse efeito é ~13% do NII_Clientes — relevante, mas não dominante.

## Por Que Isso Importa na Modelagem

O modelo atual (`der:nii = carteira_media × NIM / 100 / 4`) usa um NIM agregado que mistura:
- O spread dos créditos ativos (gerenciável, dependente de mix e ciclo)
- A remuneração do equity (automática, dependente de CDI)

Em ciclos de mudança de Selic, isso **superestima ou subestima** o impacto no NII:
- **Selic subindo**: Modelo pode subestimar a aceleração do NIM (equity hedge acelera sem crescimento de carteira)
- **Selic caindo**: Modelo pode subestimar a desaceleração do NIM

### Graph Patch Proposto

Para decompor corretamente:

```json
{
  "add_inputs": [
    {"id": "in:spread_sensiveis", "label": "Spread carteira sensível (% a.a.)", "default": 10.5},
    {"id": "in:cdi_proxy", "label": "CDI proxy para cálculo equity hedge (% a.a.)", "default": 12.75}
  ],
  "add_derivados": [
    {"id": "der:base_capital_giro", "label": "Base para remuneração do capital (PL médio, R$M)",
     "formula": "= rw:pl_total_t1"},
    {"id": "der:nii_capital_giro", "label": "NII — Remuneração Capital de Giro (R$M)",
     "formula": "= der:base_capital_giro × in:cdi_proxy / 100 / 4"},
    {"id": "der:nii_sensiveis", "label": "NII — Operações Sensíveis a Spread (R$M)",
     "formula": "= der:carteira_media × in:spread_sensiveis / 100 / 4"}
  ],
  "modify_derivados": [
    {"id": "der:nii",
     "old_formula": "= der:carteira_media × in:nim / 100 / 4",
     "new_formula": "= der:nii_sensiveis + der:nii_capital_giro"}
  ]
}
```

**Status**: Hipótese estrutural pendente de extração de dados históricos dos releases PDF (mínimo 4 trimestres). Ver `ITUB4_graph_patch_nii_decomposicao.json`.

## Por Empresa

| Empresa | Base "Capital de Giro" real | NII_CG / NII_Clientes | Nota |
|---------|----------------------------|----------------------|------|
| [[itau]] | R$146–149B (3T25–4T25, Fonte: Release 4T25) | ~13% | Base = capital alocado às áreas (excl. tesouraria). PL total ~R$206B; parcela da tesouraria (~R$60B) vai para NII_Mercado |
| [[bradesco]] | N/A (CG em Margem Mercado) | ~0.6% do NII total | Bradesco classifica Capital de Giro Próprio em Margem com Mercado (R$126M/trim total 4T25). NÃO está em NII Clientes. Não há base de capital de giro equivalente publicada para comparação direta com ITUB4. |

A relação NII_CG/NII_Total é diferente entre bancos por dois fatores: (1) tamanho absoluto do PL, (2) tamanho relativo da carteira de crédito vs PL (alavancagem). No Itaú, o disclosure explícito da tabela de taxas médias permite calibração direta — sem necessidade de estimar pelo PL total.

## Interação com Política de Dividendos

A política de distribuição de capital tem impacto direto e mecânico sobre o NII_CG, criando um trade-off entre retorno ao acionista no curto prazo e geração de NII no longo prazo.

### Mecanismo

Cada R$10B de dividendos pagos (distribuição de PL) reduz o PL médio do ano em ~R$5B (efeito médio, assumindo distribuição ao longo do ano), o que implica redução de NII_CG de ~R$650M/ano (R$5B × 13%). A magnitude exata depende do momento da distribuição:

| Evento | Impacto no PL médio | Impacto no NII_CG |
|--------|--------------------|--------------------|
| R$10B distribuídos no início do ano | -R$10B | -~R$1.3B/ano |
| R$10B distribuídos no meio do ano | -R$5B | -~R$650M/ano |
| R$10B distribuídos no final do ano | -~R$0 no ano corrente | -~R$1.3B no ano seguinte |

**No curto prazo**: payout alto reduz PL e, portanto, comprime o NII_CG do período subsequente.

**No longo prazo**: o banco precisa reter capital para crescer a carteira — o RWA (Risk-Weighted Assets) cresce proporcionalmente à carteira de crédito, exigindo que o CET1 acompanhe. Não é possível sustentar payout de 100% sem perder capital adequacy ao longo do tempo, a menos que o banco esteja em run-off.

### Caso Itaú 2025

O payout de 2025 foi ~72% (extraordinário, com CET1 folgado). Com o PL saindo via dividendos, o NII_CG deve cair ~R$500-700M vs 2024 pela redução da base de PL. Contudo, o [[nii_sensiveis_spread]] cresce com a carteira, de modo que o NII total ainda sobe. O efeito líquido é modesto, mas real para a decomposição:

- NII_CG: pressão negativa pelo PL saindo
- NII_Sensíveis: pressão positiva pelo crescimento de carteira
- NII total: ainda positivo, mas o mix muda — menor proporção de renda passiva, maior proporção de spread ativo

### Implicação para Modelo

Ao projetar NII_CG com PL crescendo organicamente, é necessário descontar o efeito do payout projetado. Um modelo que ignora os dividendos e projeta PL crescendo sempre pelo lucro líquido **superestima o NII_CG** nos anos de payout elevado. A fórmula correta para a base:

```
PL_t = PL_{t-1} + LL_t - Dividendos_t
NII_CG_t = PL_médio_t × CDI_t / 4
```

onde `PL_médio_t = (PL_{t-1} + PL_t) / 2`.

## Ciclo de Queda de Selic: O Risco Oculto

O NII_CG é o componente do NII que **mais perde em magnitude absoluta** quando a Selic cai. Diferente do [[nii_sensiveis_spread]], onde a gestão pode mitigar via repricing de carteira, a queda do NII_CG é mecânica e inevitável.

### Cenário Ilustrativo: Selic de 14.75% para 10%

Expectativa de mercado (abril 2026): pico de ~14.75% em 2026, seguido de ciclo de cortes até ~10% em 2028-2029 (corte acumulado de ~475bps).

Para o Itaú (base de capital de giro ~R$146B, conforme release 4T25; a parcela da tesouraria ~R$60B está no NII_Mercado):

| Cenário Selic | NII_CG estimado (anual, base ~R$146B) | Variação vs pico |
|--------------|---------------------------------------|-----------------|
| 14.75% (pico 2026) | ~R$16.5–17.5B/ano | — |
| 12.75% (intermediário) | ~R$14.6–15.4B/ano | -~R$1.9–2.1B/ano |
| 10.00% (fundo 2028) | ~R$11.5–12.0B/ano | -~R$5.0–5.5B/ano |

> Nota: as estimativas acima usam a base real do release (R$146B) e assume taxa ~= Selic × fator blended (~85%). Os valores anteriores baseados em PL total (~R$220B) estavam ~50% superestimados.

Calculando por incremento de 100bps (sensibilidade efetiva ~R$730M–1.0B/ano por 100bps):
```
-R$730M–1.0B × 4.75 cortes de 100bps = -~R$3.5–4.7B/ano (impacto acumulado)
```

**Este impacto é mecânico** — não há hedge natural simples. A gestão pode tentar fixar parte do equity em títulos de renda fixa prefixados, mas isso cria risco de marcação a mercado.

### Por Que o Mercado Subestima Este Risco

Em ciclos de alta, o NII_CG sobe sem nenhum esforço da gestão, o que melhora o NIM e cria a ilusão de eficiência operacional. Quando a Selic cai, o NIM cai mecanicamente, e analistas que não decompõem corretamente atribuem a queda a deterioração de mix ou pricing — quando é puramente o equity hedge deflando.

**Analistas monitoram a "duration mismatch"**: quanto do NII é fixado (prefixado, indexado a IPCA) vs flutuante à Selic (pós-fixado). Bancos com maior proporção de equity aplicado em taxas flutuantes têm maior sensibilidade negativa em ciclos de queda.

### Implicação para Modelo de Projeção

Em cenários de queda de Selic, o modelo deve reduzir o `in:cdi_proxy` gradualmente trimestre a trimestre, seguindo o cenário macro projetado. Não usar o CDI spot — usar o CDI médio do trimestre. A diferença entre CDI spot e CDI médio pode ser relevante nos trimestres de transição de ciclo.

## Comparação Internacional

O conceito existe globalmente, mas com nomenclatura diferente e magnitude distinta.

### Terminologia Internacional

| Terminologia | Mercado | Descrição |
|-------------|---------|-----------|
| "Benefit from free funds" | EUA/Europa | Retorno sobre equity e depósitos não remunerados aplicados à taxa de mercado |
| "NII rate sensitivity" | EUA/Europa | Sensibilidade do NII total a variações de 100bps (inclui equity hedge + repricing de carteira) |
| "Equity hedge" | Brasil | Remuneração do PL ao CDI — subterfúgio gerencial, nem sempre disclosure explícito |
| "Rate sensitivity position" | Global | Posição líquida de sensibilidade de juros do balanço |

### Por Que o Brasil tem Magnitude Maior

A sensibilidade per unit of assets é ~4× maior no Brasil do que nos EUA, pelos seguintes fatores:

**(a) Taxas absolutas muito mais altas**: CDI 13% vs Fed Funds 5% — o equity hedge gera muito mais NII nominalmente por real de PL do que por dólar de equity nos EUA.

**(b) Capitalização relativa maior**: Bancos brasileiros tendem a ter PL/Carteira maior do que pares americanos (multiplicador de crédito menor), o que amplifica o peso do equity hedge no NII total.

| Banco | Assets | NII rate sensitivity (~100bps) | Sensibilidade por unit of assets |
|-------|--------|-------------------------------|----------------------------------|
| JPMorgan (EUA) | ~$3T | ~$2-3B/ano | ~0.007%/bps |
| Itaú (Brasil) | ~R$2T | ~R$730M–1.0B/ano (Fonte: Release 4T25, base ~R$146B) | ~0.037–0.050%/bps |

> Nota: a sensibilidade efetiva por 100bps é maior do que a estimativa anterior de R$550M, porque a base real do release (~R$146B) é menor que o PL total (~R$220B), mas a taxa blended usada (~11.2%) é superior ao CDI puro, e o cálculo anterior usava uma proporção errada. A sensibilidade bruta pela base seria R$146B × 1% = R$1.46B/ano; ajustando para a parcela pós-fixada efetiva (~50-70%), chega-se a ~R$730M–1.0B/ano.

Itaú é ~**5–7× mais sensível por unidade de ativo** do que JPMorgan — amplificado principalmente pelo nível absoluto de taxas (CDI ~13% vs Fed Funds ~5%). A diferença é explicada quase inteiramente pelo nível absoluto de taxas (13% vs 5%) e pela relação PL/Ativos (maior no Itaú em termos relativos à carteira de crédito).

### Implicação de Valuation Cross-Border

Um analista usando múltiplos P/E de bancos americanos como referência para bancos brasileiros precisa ser cauteloso: em ciclos de alta de juros, o ROE de bancos brasileiros sobe mais (equity hedge maior), e em ciclos de queda, cai mais — a volatilidade do ROE é estruturalmente maior. Isso justifica múltiplos ligeiramente mais baixos no Brasil em condições neutras de juros, mas múltiplos mais altos em picos de ciclo.

## Ver Também

- [[nii_clientes]] — conceito pai
- [[nii_sensiveis_spread]] — o outro sub-componente (spread ativo)
- [[selic]] — driver direto desta linha
- [[nim]] — NIM total inclui ambos os componentes
- [[banking]] — contexto setorial
- [[resultado_seguros]] — outra linha de receita que também se beneficia de Selic alta (VGBL/PGBL)
- [[aliquota_efetiva]] — JCP também usa PL como base de cálculo; payout alto reduz ambos NII_CG e benefício fiscal do JCP
- [[crescimento_carteira]] — carteira crescendo dilui o % de equity no funding total, reduzindo o peso relativo do NII_CG no mix
