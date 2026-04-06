---
type: conceito
source_quality: conceptual
aliases: [NIM Clientes, NIM de Crédito, Spread de Clientes, NII Clientes/Carteira]
sources:
  - sectors/banking/sector_profile.md
  - wiki/nii_clientes.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
updated: 2026-04-05
---

# NIM Clientes

O **NIM Clientes** é a componente do [[nim]] total referente exclusivamente às operações de crédito a clientes — separando o resultado da carteira de crédito do resultado de tesouraria ([[nii_mercado]]). É o indicador de pricing do negócio de crédito do banco, independente das decisões de gestão de ativos da tesouraria.

## Conceito

```
NIM_Clientes = NII_Clientes / Carteira_Sensível_Média
            = (Spread_médio × Carteira_média) / Carteira_média
            = Spread_médio
```

Em termos práticos, o NIM Clientes é igual ao **spread médio ponderado** da carteira de crédito a clientes (PF + PJ + Agro + Imob + LatAm). Ele reflete:
1. O mix de produto (cartão de crédito tem spread de 30%+; crédito imobiliário tem spread de 2-3%)
2. O risco médio assumido pelo banco (mais varejo = maior spread mas maior risco)
3. O ambiente competitivo (fintechs comprimem spreads em crédito pessoal)

## Distinção: NIM Clientes vs NIM Total

| Componente | O que inclui | Driver principal |
|------------|-------------|-----------------|
| **NIM Clientes** | Spread da carteira de crédito a clientes | Pricing ativo: mix de produto, risco |
| **NIM Mercado** | Tesouraria: TVM pós/pré/IPCA, compulsórios, hedge | Selic, posicionamento de ALM |
| **NIM Total** | Soma dos dois | Combinação de crédito + tesouraria |

**Por que separar?** O NIM Clientes mede a competência de originação e pricing do banco. O NIM Mercado mede a habilidade de gestão de ALM e a sensibilidade ao ciclo de juros. Misturar os dois dificulta entender a qualidade do negócio core.

## Variações de Base por Banco

**CRÍTICO**: Cada banco usa denominadores diferentes para calcular o NIM/NII Clientes. Comparações diretas são enganosas.

### Bradesco (BBDC4)

O BBDC4 publica o **saldo médio da carteira de crédito** diretamente no release (p.9 — Margem Financeira). O NIM de crédito do Bradesco é calculado sobre esse saldo médio publicado:

```
NIM_Clientes_BBDC4 = NII_Clientes / Saldo_Médio_Carteira_Publicado
                   ≈ 9% a.a. (2025)
```

**Vantagem:** Transparente, não requer reconstrução. O analista usa diretamente os valores do release.

**Limitação:** A base do Bradesco é apenas a carteira de crédito — não inclui TVM sensível ou operações LatAm no denominador. Isso torna o NIM menor em termos percentuais vs bancos que incluem essas exposições.

### Itaú Unibanco (ITUB4)

O Itaú usa a **carteira sensível** como denominador — um conceito mais amplo que inclui operações LatAm e TVM sensíveis a spread, além da carteira de crédito doméstica:

```
Carteira_Sensível_ITUB4 ≈ R$1.28T (2025)
NIM_Clientes_ITUB4 ≈ 9-9.5% × Carteira_Sensível / 4 por trimestre
```

O NIM percentual do Itaú é similar ao Bradesco quando calculado sobre base comparável. A diferença de ~12% vs ~9% reportada em algumas análises reflete diferença de denominador, não necessariamente melhor pricing.

### Santander Brasil (SANB11)

O Santander usa a **carteira ampliada** como denominador, que inclui avais, fianças, ACC/ACE e outros instrumentos não-carteira:

```
Carteira_Ampliada_SANB11 ≈ R$706B (2025)
NIM_reportado_SANB11 ≈ 10.7%

Carteira_Crédito_Gerencial_SANB11 ≈ R$566B (2025)
NIM_implícito_modelo ≈ 11.5%
```

**Regra do modelo SANB11:** Usar a carteira gerencial de crédito (~R$566B), não a carteira ampliada. O NIM calibrado de ~11.5% é o correto para projeção de NII Clientes.

## Como o NIM Clientes Entra no Modelo

### ITUB4

O modelo ITUB4 usa **YoY de NII Clientes** como premissa direta, não NIM explícito:

```python
nii_clientes_t = nii_clientes_t_minus_4 * (1 + g_nii_clientes_yoy)
# Onde g_nii_clientes_yoy é calibrado (~7-9% em 2025-2026)
```

O NIM implícito pode ser verificado como sanidade:
```python
nim_implicito_t = (nii_clientes_t × 4) / carteira_sensivel_media_t
# Deve ficar no range 11.5-12.5%
```

### BBDC4

Para BBDC4, pode-se modelar tanto via YoY quanto via NIM explícito:

```python
# Abordagem via NIM
nii_clientes_t = saldo_medio_carteira_t * nim_clientes / 4

# Abordagem via YoY
nii_clientes_t = nii_clientes_t_minus_4 * (1 + g_nii_clientes_yoy)
```

A abordagem via NIM é mais transparente para o BBDC4 pois o saldo médio é publicado e facilita interpretação econômica.

## Drivers do NIM Clientes

| Driver | Efeito no NIM Clientes | Prazo |
|--------|----------------------|-------|
| Mix shift para varejo (cartão, pessoal) | Expande (maior spread bruto) | Curto prazo |
| Mix shift para crédito imobiliário/consignado | Comprime (menor spread mas maior segurança) | Médio prazo |
| Queda da inadimplência | Permite reduzir spread sem perder NIM ajustado | Médio prazo |
| Alta de [[selic]] | Expande moderadamente (repricing da carteira pós-fixada) | Curto-médio |
| Crescimento de [[consignado_privado]] | Efeito neutro a levemente compressor (spread médio do consignado ~15-20% vs pessoal ~30%) | Médio prazo |
| Concorrência de fintechs | Comprime via competição em crédito pessoal | Gradual |

## Relação com Custo de Risco

O NIM Clientes é o gross spread. O **NIM Clientes ajustado pelo risco** é o spread líquido das perdas esperadas:

```
NIM_Ajustado = NIM_Clientes − Custo_Risco
```

Bancos que inflam NIM via mix de alto risco têm NIM bruto alto mas NIM ajustado baixo. A comparação mais honesta entre bancos é sempre no NIM ajustado.

**Referência 2025:**
- Itaú: NIM bruto ~9.5% - custo risco ~3.7% = NIM ajustado ~5.8%
- Bradesco: NIM bruto ~9% - custo risco ~4.5% = NIM ajustado ~4.5%
- Santander: NIM bruto ~11.5% - custo risco ~5.0% = NIM ajustado ~6.5%

## Ver Também

- [[nim]] — NIM total (Clientes + Mercado); incluindo variações de base por banco
- [[nii_clientes]] — valor monetário absoluto (NIM Clientes × Carteira Média)
- [[carteira_media]] — denominador do NIM Clientes; varia por metodologia de cada banco
- [[custo_risco]] — NIM ajustado = NIM Clientes − Custo Risco; qualidade do portfólio
- [[spread_clientes]] — sinônimo de NIM Clientes; usado no grafo de dependências do ITUB4
- [[itau]] — modelo usa YoY de NII Clientes; NIM implícito ~12%
- [[bradesco]] — saldo médio publicado; NIM ~9% (base saldo_médio)
- [[sanb11]] — usar carteira gerencial (~R$566B); NIM implícito ~11.5%
