---
type: conceito
source_quality: conceptual
aliases: [Risco de Mercado, Market Risk, VaR, Risco de Taxa, Risco de Ações]
sources:
  - sectors/banking/sector_profile.md
  - wiki/cet1.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - wiki/duration.md
updated: 2026-04-05
---

# Risco de Mercado

O **risco de mercado** é a probabilidade de perdas financeiras resultantes de variações adversas em preços de mercado — taxas de juros, taxas de câmbio, preços de ações e preços de commodities. Para bancos, é um dos três pilares de risco (junto com risco de crédito e risco operacional) que determinam os requerimentos de capital regulatório.

## Categorias de Risco de Mercado

| Categoria | Driver | Exemplo Bancário |
|-----------|--------|-----------------|
| **Risco de taxa de juros** | Variações na curva de juros | Carteira de TVM prefixada perde valor quando juros sobem |
| **Risco cambial** | Variações nas taxas de câmbio | Subsidiária LatAm vale menos em BRL quando BRL aprecia |
| **Risco de ações** | Variações em preços de ações | Participações em empresas abertas (marcação a mercado) |
| **Risco de commodities** | Variações em preços de commodities | Carteira de agro com exposição a preços de soja, milho |

Para grandes bancos brasileiros, o risco de taxa de juros e o risco cambial são os mais materiais.

## Medição: Value at Risk (VaR)

A principal métrica de risco de mercado é o **VaR (Value at Risk)**:

```
VaR(99%, 1 dia) = Perda máxima esperada em 1 dia com 99% de probabilidade
```

**Exemplo de leitura:** Se o VaR de 1 dia a 99% é R$500M, significa que há 1% de probabilidade de perder mais de R$500M em um único dia de negociação.

### Limitações do VaR

| Limitação | Descrição |
|-----------|-----------|
| **Tail risk**: O VaR não diz nada sobre a perda quando ela ocorre além do limite — só que é improvável | |
| **Correlações em crise**: Em crises, correlações entre ativos mudam — o VaR histórico subestima o risco |
| **Horizonte**: VaR de 1 dia é relevante para trading book; carteiras de crédito precisam de horizonte maior |

Por isso, reguladores exigem também **Stressed VaR** (usando dados de período de estresse) e **Expected Shortfall (CVaR)** — a perda média nos piores cenários além do VaR.

## Risco de Mercado vs Risco de Crédito

| Aspecto | Risco de Mercado | Risco de Crédito |
|---------|-----------------|-----------------|
| **Driver** | Preços de mercado | Inadimplência de tomadores |
| **Horizonte** | Curto prazo (1 dia a 10 dias) | Médio/longo prazo (meses a anos) |
| **Mensuração** | VaR, Stressed VaR | PD, LGD, EAD; [[custo_risco]] |
| **Portfólio** | Trading book (TVM, derivativos) | Banking book (crédito a clientes) |
| **Capital regulatório** | Rban (Basileia) | RWA crédito |

Para grandes bancos BR (ITUB4, BBDC4), o risco de **crédito** consome muito mais capital do que o risco de mercado — a carteira de crédito (~R$1T+) é muito maior que o trading book.

## Regulação no Brasil: Basileia III

O Banco Central do Brasil (BCB) implementou Basileia III (CMN 4.192/2013 e circulares subsequentes). Para risco de mercado, o banco deve manter capital mínimo calculado como:

```
Capital_Risco_Mercado = max(VaR, Stressed_VaR) × Fator_Multiplicador
```

onde o fator multiplicador (≥3) é determinado pelo regulador com base na qualidade do modelo interno do banco. Se o modelo interno não é aprovado, usa-se a abordagem padronizada do BCB.

O total de capital regulatório ([[cet1]] + Tier 2) deve cobrir:

```
RWA_total = RWA_Crédito + RWA_Mercado + RWA_Operacional
CET1 / RWA_total ≥ 4,5% (mínimo) + buffers
```

## Risco de Taxa de Juros no Banking Book (IRRBB)

Além do VaR do trading book, o BCB regulamenta o **IRRBB (Interest Rate Risk in the Banking Book)** — o risco de que variações de taxa afetem o valor econômico e o NII do banking book (carteira de crédito e depósitos).

```
ΔNII_IRRBB = Σ [Ativos_pós-fixados × ΔSelic] − Σ [Passivos_pós-fixados × ΔSelic]
```

Para o [[itau]], com ~70-80% da carteira de crédito em taxas flutuantes (CDI/TR), a sensibilidade do IRRBB é relativamente baixa — a carteira reprecia rapidamente quando a Selic muda. O maior risco de IRRBB vem da carteira de TVM prefixada e de depósitos a prazo com taxas fixas contratuais.

## NII Mercado e Risco de Mercado

O [[nii_mercado]] dos bancos (resultado de tesouraria) é a manifestação P&L do risco de mercado. As posições de tesouraria podem gerar resultados positivos ou negativos dependendo da direção do mercado:

- **Alta de Selic**: Beneficia posições pós-fixadas; prejudica posições prefixadas
- **Apreciação do BRL**: Beneficia importadores/passivos em USD; prejudica exportadores/ativos em USD
- **Abertura de spreads de crédito**: Desvaloriza carteira de TVM corporativo

**Implication para modelagem:** O [[nii_mercado]] tem volatilidade intrínseca e é mais difícil de modelar do que o [[nii_clientes]]. Para projeções trimestrais, geralmente se usa um nível normalizado (média histórica) com análise de sensibilidade para cenários de Selic diferente.

## Gestão de Risco de Mercado nos Grandes Bancos

Todos os bancos tier-1 têm mesas de trading e tesouraria com limites formais de VaR por mesa, por fator de risco e total:

```
VaR_total_banco = sqrt(Σ VaR_i² + 2 × Σ ρ_ij × VaR_i × VaR_j)
```

**Divulgação:** Os bancos divulgam o VaR total e a sensibilidade do NII a choques de 100bps de Selic nos relatórios de gerenciamento de risco (Pilar 3 do Basileia).

**Exemplo de sensibilidade ITUB4 (estimativa conceptual):**
- Choque de +100bps na Selic → NII total ~+R$1-2B/ano (posição líquida pós-fixada)
- Choque de +10% no USD/BRL → NII LatAm ~-R$1B/ano em conversão (parcialmente hedgeado)

## Por Empresa

| Empresa | Característica de Risco de Mercado |
|---------|-----------------------------------|
| [[itau]] | Posição pós-fixada dominant no banking book; beneficia de Selic alta. Exposição LatAm via [[risco_cambial]] (parcialmente hedgeada). NII Mercado contribui ~R$8-12B/ano. |
| [[bradesco]] | Similar ao Itaú; [[resultado_seguros]] adiciona exposição a risco de mercado de ativos garantidores (IPCA+, ações). |

## Ver Também

- [[duration]] — medida de sensibilidade de preço a variações de taxa de juros
- [[risco_cambial]] — risco específico de variações no câmbio
- [[nii_mercado]] — resultado de tesouraria, manifestação P&L do risco de mercado
- [[cet1]] — capital regulatório que deve cobrir risco de mercado + crédito + operacional
- [[banking]] — framework de risco e regulação bancária
- [[selic]] — principal driver de risco de taxa no Brasil
- [[itau]] — maior banco privado BR; gestão de risco de mercado sofisticada
