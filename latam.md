---
type: conceito
source_quality: conceptual
aliases: [Operações LatAm, LatAm Operations, América Latina, Internacional Itaú]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - wiki/itau.md
  - ITUB4 4T25 Release (estimativas de participação por geography)
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
updated: 2026-04-05
---

# Operações LatAm

As **operações LatAm** do [[itau|Itaú Unibanco]] são o conjunto de subsidiárias bancárias fora do Brasil, presentes principalmente em Chile, Colômbia, Argentina, Paraguai e Uruguai. Representam ~15% da carteira de crédito total consolidada e são uma fonte de diversificação geográfica, mas introduzem riscos de câmbio e regulatório não capturados no modelo Brasil.

## Como Funciona

O Itaú consolida integralmente as operações internacionais na DRE. O impacto de câmbio aparece em:

1. **Translação**: resultados em moeda local (CLP, COP, ARS, PYG, UYU) convertidos para BRL pela taxa média do período
2. **Crescimento orgânico**: crescimento da carteira em moeda local × variação do BRL

```
Carteira_LatAm_BRL(t) = Carteira_LatAm_Local(t) × Taxa_BRL_Local(t)
NII_LatAm_BRL(t)      = NII_LatAm_Local(t) × Taxa_BRL_Local(t)
```

Quando o BRL se aprecia, a contribuição LatAm em BRL encolhe — mesmo sem mudança no negócio local. Isso torna a modelagem de LatAm menos previsível.

### Presença por País

| País | Posição | Destaque |
|------|---------|---------|
| Chile | Banco Itaú Chile — Top 5 | Carteira relevante, pessoal + empresa |
| Colômbia | Banco Itaú Colombia | Smaller, crescendo |
| Argentina | Banco Itaú Argentina | Alta volatilidade macro/câmbio |
| Paraguai | Banco Itaú Paraguay | Lucrativo, baixo risco relativo |
| Uruguai | Banco Itaú Uruguay | Pequeno, estável |

## No Contexto Brasileiro

- **Argentina** é o maior risco isolado: hiperinflação (>100% a.a.), múltiplos câmbios oficiais vs. paralelos, potencial de perdas contábeis expressivas na conversão. O Itaú mantém operação, mas provisiona para risco país.
- **Chile**: maior operação LatAm em volume absoluto. Mercado maduro, competição intensa com Banco Santander e Banco de Chile.
- **Para modelagem do ITUB4**: o padrão é projetar LatAm no bloco Brasil (YoY), implicitamente assumindo continuidade de câmbio. Analistas mais detalhados separam Brasil vs LatAm, mas a maioria usa o guidance consolidado.
- **Guidance Itaú 2026**: crescimento de carteira é dado apenas para Brasil (+6,5-10,5% YoY). LatAm é residual/implícito no guidance consolidado.
- Risco regulatório: mudanças tributárias no Chile (reforma tributária 2022-23) comprimiram margens temporariamente.

## Contribuição Financeira

Com a carteira total consolidada do [[itau|Itaú]] em ~R$1,0-1,1T (2024-25), o bloco LatAm representa **~R$150-160B estimados** em crédito (15% do total). Essa estimativa é inferida do disclosure de participação percentual; o Itaú não publica breakdown preciso por geográfico na mesma tabela da carteira total.

### Estimativas por País (2025, aproximadas)

| País | Carteira Estimada | Participação LatAm |
|------|------------------|--------------------|
| Chile | ~R$80-90B | ~55-60% do bloco LatAm |
| Colômbia | ~R$20-25B | ~15% do bloco LatAm |
| Argentina | ~R$10-15B | ~8-10% do bloco LatAm |
| Paraguai + Uruguai | ~R$15-20B | ~10-12% do bloco LatAm |

> Nota: estimativas calculadas com base em shares geográficos divulgados pelo Itaú em relatórios anuais e apresentações de resultado. Suscetíveis a variações cambiais significativas entre períodos.

### NIM e Lucro

O [[nim]] do bloco LatAm é estruturalmente **diferente do Brasil** por dois fatores:

1. **Argentina** opera com spreads nominais altíssimos (>50% a.a.) por conta da hiperinflação, mas o lucro em BRL é comprimido pela desvalorização do ARS. O NIM real (deflacionado) é muito menor.
2. **Chile e Colômbia** operam com NIMs mais próximos ao padrão Brasil-corporate (~6-9%), com mix de crédito mais voltado a pessoas jurídicas.

A contribuição estimada de LatAm ao **lucro líquido consolidado** é de ~R$5-8B/ano (estimado ~10-15% do LL total de R$46,8B em 2025), com grande variância por câmbio. O Chile responde pela maior parcela do resultado internacional de forma recorrente.

## Impacto no Modelo

### Como o Modelo ITUB4 Atual Trata LatAm

O modelo `ITUB4_model.json` usa guidance consolidado: a `carteira_credito_bruta` (projetada em ~R$1,08T para 1T26E) inclui **Brasil + LatAm implicitamente**. Não há decomposição no grafo — LatAm está dentro do `der:carteira_total` consolidado.

```
carteira_credito_bruta(t) = carteira_credito_bruta(t-1) × (1 + crescimento_carteira/100)
crescimento_carteira = 8,5%  ← guidance Brasil 6,5-10,5%
```

O `crescimento_carteira` de 8,5% projetado reflete **apenas o guidance Brasil**. A LatAm é um residual implícito — o modelo assume que a contribuição LatAm em BRL cresce em linha com o bloco Brasil, o que é uma simplificação.

### Risco de Distorção Cambial

Quando o BRL se aprecia, o seguinte mecanismo atua:

```
ΔCarteira_LatAm_BRL = ΔCarteira_LatAm_Local × Taxa_atual  +  Carteira_LatAm_Local × ΔTaxa_BRL
```

Se o BRL aprecia 10% vs CLP/COP, a contribuição LatAm em BRL cai ~10% mesmo com crescimento em moeda local de +6%. Isso implica:

- **Brasil no plano** (crescimento carteira 8,5% YoY)
- **LatAm em BRL contraindo** (câmbio desfavorável)
- **Consolidado abaixo do guidance** → [[nii_clientes]] e LL abaixo do modelo

Esse risco é **não capturado explicitamente** no modelo atual. A premissa de crescimento consolidado de 8,5% funcionaria bem se o câmbio se mantiver estável.

### Limitação e Melhoria Possível

Para modelagem mais rigorosa, seria necessário separar:
1. `carteira_brasil` × `crescimento_brasil` (guidance explícito)
2. `carteira_latam_local` × `crescimento_local` × `taxa_cambial` (projeção macro por país)

Na prática, a maioria dos analistas buy-side usa o guidance consolidado (abordagem atual do modelo). Separação Brasil vs LatAm é útil para análise de sensibilidade cambial em cenários de stress (ex: BRL apreciando para R$4,50/USD).

## Argentina — Caso Especial

### Pré-Milei (2019-2023): Contabilidade de Hiperinflação

Durante o período de hiperinflação argentina (inflação >100% a.a. em 2022-23), o Itaú aplicou **IAS 29 — Financial Reporting in Hyperinflationary Economies**. A norma exige:

- Reapresentação dos ativos e passivos monetários pela inflação acumulada do período
- Reconhecimento de **ganho/perda monetária** (resultado de posição monetária líquida) na DRE
- Conversão para BRL pela taxa de fechamento (não pela taxa média do período)

Na prática, o IAS 29 **inflava nominalmente os resultados argentinos** em moeda local, mas a conversão para BRL pela taxa de fechamento comprimia severamente o resultado final consolidado. Para analistas, a Argentina era um "ruído contábil" nos resultados do Itaú — linhas específicas a serem excluídas da análise recorrente.

### Pós-Milei (2024-2025): Normalização Cambial

A chegada de Javier Milei ao governo em dezembro de 2023 marcou uma virada relevante para as operações argentinas do Itaú:

1. **Unificação cambial**: fim do sistema de câmbios múltiplos (oficial, MEP, CCL, blue). O ARS passou a operar em regime mais próximo ao mercado. O dólar oficial convergiu ao paralelo em 2024.
2. **Queda da inflação**: de ~211% a.a. em 2023 para ~120% em 2024 e projeção de queda adicional em 2025. Com inflação abaixo de 100% por 3 anos consecutivos, o **IAS 29 pode deixar de se aplicar** à Argentina — ponto a monitorar nas notas explicativas a partir de 2025-2026.
3. **Impacto nos resultados**: a normalização cambial **reduziu as distorções** de conversão, tornando o resultado argentino mais previsível. A operação saiu de um modo de "gerenciamento de crise" para crescimento seletivo de crédito.

### Como o Itaú Trata Argentina no Modelo

O Itaú não divulga breakdown de Argentina separado na DRE gerencial publicada em releases. A operação fica consolidada em "América Latina" junto com Chile, Colômbia e outros. O analista deve:

- **Monitorar as notas explicativas**: aplicação do IAS 29 (se ainda vigente) altera bases comparativas
- **Desconsiderar Argentina como driver de crescimento recorrente**: mesmo pós-Milei, o ambiente macro é volátil. Tratá-la como optionalidade positiva (normalização) ou risco residual (reversão de política)
- **No modelo atual**: não há ajuste explícito para Argentina. O risco está implícito no guidance consolidado — se a Argentina performar muito abaixo (ou acima), o consolidado desvia do modelo

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | ~15% da carteira total em LatAm. Maior operação fora do Brasil: Chile. Argentina é o maior risco contábil (câmbio/inflação). LatAm não tem guidance separado para crescimento de carteira. |

## Ver Também

- [[crescimento_carteira]] — guidance de crescimento cobre Brasil; LatAm está implícito no consolidado
- [[itau]] — empresa com presença LatAm; ~15% da carteira total em operações internacionais
- [[nii_clientes]] — LatAm contribui para o NII consolidado; câmbio distorce a comparação YoY
- [[nim]] — NIM por país varia significativamente; Argentina tem NIM nominal alto mas real comprimido
- [[banking]] — contexto setorial
- [[aliquota_efetiva]] — IAS 29 (Argentina) afeta a linha de impostos e resultado monetário na DRE
