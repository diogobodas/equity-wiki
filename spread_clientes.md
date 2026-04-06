---
type: conceito
source_quality: conceptual
aliases: [Spread Clientes, Spread de Clientes, NIM Clientes, Spread da Carteira]
sources:
  - sectors/banking/sector_profile.md
  - wiki/nim_clientes.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - wiki/carteira_media.md
updated: 2026-04-05
---

# Spread Clientes

O **spread clientes** é o percentual anualizado de margem de juros líquida aplicado sobre a [[carteira_media]] para calcular o [[nii_clientes]]. É o nome técnico dado ao [[nim_clientes]] no contexto dos grafos de dependências dos modelos bancários deste projeto.

```
NII_Clientes = Carteira_Sensível_Média × spread_clientes / 4
```

## Relação com NIM Clientes

Os dois termos são equivalentes no contexto deste projeto:

| Termo | Contexto de Uso |
|-------|----------------|
| `spread_clientes` | Nome do nó no grafo de dependências (`dependency_graph_v3.json`) de ITUB4/BBDC4 |
| **NIM Clientes** | Terminologia mais comum em análise de equity research |
| **Spread de Intermediação** | Terminologia contábil BACEN (mais amplo — inclui captação) |

## Valores de Referência (2025)

| Banco | spread_clientes (modelo) | Base |
|-------|------------------------|------|
| [[itau]] (ITUB4) | ~9.0-9.5% a.a. | Carteira sensível (~R$1.28T) |
| [[bradesco]] (BBDC4) | ~9% a.a. | Saldo médio publicado |
| [[sanb11]] (SANB11) | ~11.5% a.a. | Carteira gerencial de crédito (~R$566B) |

**Atenção à base:** Cada banco usa um denominador diferente. O spread_clientes de 9.5% do Itaú sobre a carteira sensível não é diretamente comparável ao 9% do Bradesco sobre o saldo médio.

## No Grafo de Dependências

No `ITUB4_dependency_graph_v3.json`, o nó `spread_clientes` tem:
```json
{
  "id": "spread_clientes",
  "type": "premissa",
  "default": 0.09,
  "historical_formula": "nii_clientes / (carteira_sensivel * 4)"
}
```

A premissa padrão de 9% é calibrada pelo backtest histórico. Para ajustar, verificar `historico_implicito` que mostra o spread_clientes implícito em cada trimestre histórico.

## Como Projetar o Spread Clientes

O spread clientes é premissa direta no modelo. Para calibrá-lo:

1. **Extrair da série histórica**: `NII_Clientes / (Carteira_Sensível_Média × 4)` — dá o spread implícito por trimestre
2. **Verificar continuidade**: O spread não deve mudar abruptamente entre o último trimestre histórico e o primeiro projetado
3. **Incorporar drivers**: Ciclo de reprecificação da carteira, mix de produto, [[selic]] (afeta spread bruto em carteira pós-fixada)
4. **Alinhar com guidance**: Gestão geralmente comenta sobre tendência de NIM em teleconferências

### Sensibilidades ao Spread

| Mudança | Impacto no NII Clientes | Impacto no LL |
|---------|------------------------|---------------|
| +0.5pp no spread | +~R$1.5B/tri (ITUB4) | +~R$1.0B/tri (após IR) |
| -0.5pp no spread | -~R$1.5B/tri (ITUB4) | -~R$1.0B/tri |
| +R$50B na carteira | ~+R$1.1B/tri (a 9.5% spread) | +~R$0.75B/tri |

Esses números são aproximações para ITUB4 com carteira sensível de ~R$1.28T.

## Relação com Custo de Captação

O **spread bruto** inclui o custo de captação do banco. O `spread_clientes` nos modelos deste projeto é o **spread líquido** (já descontado o custo de captação implícito):

```
Spread Líquido (spread_clientes) ≈ Spread Bruto − Custo de Captação
```

Para um banco como ITUB4 com custo de captação ~9-10% a.a. e spread bruto ~19-20% a.a. sobre a carteira de crédito varejo, o spread líquido sobre a carteira sensível fica em ~9-9.5%.

## BBDC4: Diferença de Denominador

Para o BBDC4, o modelo usa `in:nim_clientes` (não `spread_clientes`) como nome do nó — mas o conceito é idêntico. O denominador do BBDC4 é o **saldo médio da carteira de crédito publicado no release** (não a carteira sensível ampliada do Itaú). Isso torna os percentuais menores em termos absolutos, mas a comparação é apples-to-oranges.

## Comportamento Histórico do Spread

O spread_clientes não é estável — varia com o ciclo de crédito, mix de carteira e nível da Selic. Padrões observados:

### Itaú (ITUB4) — Spread Implícito Histórico

| Período | Spread Implícito | Contexto |
|---------|-----------------|---------|
| 2020-2021 | ~8.5-9.0% | Selic na mínima histórica (2%), carteira migrando para menor risco |
| 2022 | ~9.5-10.0% | Repricing com Selic subindo (13.75%), spreads de crédito ainda reprecificando |
| 2023 | ~9.0-9.5% | Ciclo adverso: banco reduziu apetite de risco, mix migrou para consignado/imobiliário |
| 2024-2025 | ~8.8-9.2% | Normalização: spread em recompressão leve com crescimento em produtos de menor spread |

O spread do Itaú segue um padrão de **compressão no longo prazo** — à medida que a carteira migra para produtos mais seguros (consignado, imobiliário) com spreads intrinsecamente menores, o spread médio da carteira sensível cai levemente. A compensação é o crescimento de volume e a redução do custo de risco.

### Santander (SANB11) — Por Que o Spread é Maior

O SANB11 tem spread implícito ~11.5% vs ~9% do ITUB4, o que pode parecer contraditório dado o menor ROE do Santander. A explicação é o mix de carteira:

- **Maior peso em crédito pessoal e cartão**: spreads de 15-25% que elevam o spread médio
- **Menor peso em grandes corporações investment grade**: que reduzem o spread (CDI + 0.5-1.5%)
- **Custo de risco correspondentemente maior**: spread bruto alto não implica NIM ajustado ao risco superior

A fórmula completa para comparar NIM real entre bancos é:

```
NIM_ajustado_risco = spread_clientes − custo_risco_anualizado
NIM_ajustado_ITUB4  ≈ 9.2% − 3.7% = 5.5%
NIM_ajustado_SANB11 ≈ 11.5% − 5.0% = 6.5%  (estimativa)
```

O SANB11 tem NIM ajustado ligeiramente superior, mas com mais volatilidade — confirma o perfil de maior risco/retorno vs ITUB4.

## Decomposição do Spread por Produto (ITUB4 Referência)

Para entender a trajetória do spread, é útil decompor por produto e pesar pelo mix de carteira:

| Produto | Spread estimado | Peso na carteira | Contribuição |
|---------|----------------|-----------------|-------------|
| Consignado PF | ~8-9% | ~15% | ~1.3pp |
| Crédito imobiliário | ~3-4% | ~13% | ~0.5pp |
| Crédito rural/Agro | ~4-5% | ~12% | ~0.5pp |
| Capital de giro PJ | ~9-12% | ~20% | ~2.2pp |
| Grandes empresas | ~3-5% | ~15% | ~0.6pp |
| Cartão/Pessoal PF | ~18-25% | ~15% | ~3.2pp |
| Outros (veículos, etc.) | ~10-15% | ~10% | ~1.2pp |
| **Total ponderado** | **~9.5%** | **100%** | **~9.5pp** |

Quando o banco acelera consignado (mais seguro, menor spread) em detrimento de cartão (mais arriscado, spread maior), o spread_clientes cai mas o custo de risco também cai — efeito líquido no NIM ajustado pode ser neutro ou positivo.

## Ver Também

- [[nim_clientes]] — descrição completa do conceito (NIM de crédito a clientes)
- [[nii_clientes]] — valor monetário: NII = carteira_média × spread_clientes / 4
- [[carteira_media]] — denominador do spread; metodologia varia por banco
- [[nim]] — NIM total = spread_clientes + contribuição da tesouraria
- [[selic]] — afeta repricing da carteira pós-fixada → pressiona spread em alta de juros
- [[custo_risco]] — NIM ajustado = spread_clientes − custo de inadimplência
- [[nii_sensiveis_spread]] — componente que reage mais ativamente ao spread acima do benchmark
- [[remuneracao_capital_giro]] — componente do NII Clientes que segue a Selic automaticamente
- [[itau]] — ITUB4: spread_clientes ~9.0-9.5% sobre carteira sensível
- [[bradesco]] — BBDC4: spread_clientes ~9% sobre saldo médio publicado
- [[sanb11]] — SANB11: spread ~11.5% sobre carteira gerencial (~R$566B)
