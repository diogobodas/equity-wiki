---
type: conceito
source_quality: conceptual
aliases: [Carteira Média, Saldo Médio da Carteira, Carteira de Crédito Média]
sources:
  - sectors/banking/sector_profile.md
  - wiki/nii_clientes.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
updated: 2026-04-05
---

# Carteira Média

A **carteira média** é o saldo médio da carteira de crédito durante um período, calculado tipicamente como a média aritmética do saldo inicial e do saldo final do trimestre. É a base sobre a qual se aplica o NIM para calcular o NII e o custo de risco para calcular a PDD.

## Como Funciona

```
Carteira_Média_Trimestral = (Carteira_início_período + Carteira_fim_período) / 2
```

Para cálculos anuais, é mais preciso usar a média dos quatro saldos de fim de trimestre:

```
Carteira_Média_Anual = (Carteira_1T + Carteira_2T + Carteira_3T + Carteira_4T) / 4
```

### Por Que Usar a Média (e Não o Saldo Final)

A carteira média é fundamental porque os resultados financeiros (NII, PDD) fluem ao longo do tempo — não apenas no final do período. Se um banco cresce muito a carteira no último dia do trimestre, o saldo final é inflado mas o NII do trimestre ainda reflete a carteira média ao longo dos 90 dias.

**Exemplo numérico:**

| Data | Carteira |
|------|----------|
| 1 Jan | R$900B |
| 31 Mar | R$1.100B |
| Média aritmética | R$1.000B |

Se o NIM anual é 12%, o NII trimestral esperado é:

```
NII = R$1.000B × 12% / 4 = R$30B
```

Se usássemos o saldo final (R$1.100B), o NII seria R$33B — sobreestimado em 10%.

## Uso no Modelo de Banking

### NII Clientes

```
NII_Clientes = Carteira_Sensível_Média × Spread_Clientes
             + Capital_Próprio_Médio × CDI
```

### Custo de Risco (PDD)

```
PDD_Trimestral = Carteira_Média × Custo_Risco_Anualizado / 4
```

**Implicação crítica:** Um banco que acelera o crescimento de carteira tem PDD automaticamente crescendo mesmo sem qualquer deterioração de qualidade. Isso é chamado de "provisão de crescimento" — é esperado e saudável, mas comprime o lucro no curto prazo.

### NIM vs Carteira Sensível vs Carteira Total

Para o [[itau]], a modelagem distingue:

| Componente | Descrição |
|------------|-----------|
| **Carteira Total** | Inclui todas as modalidades (crédito + TVM + compulsórios) |
| **Carteira Sensível** | Subconjunto com exposição direta a variações de Selic/spread (inclui operações LatAm) |
| **Carteira de Crédito** | Apenas operações de crédito a clientes (PF + PJ + Agro + Imob.) |

O modelo ITUB4 usa `carteira_sensivel` (~R$1.28T em 2025) como base para o [[nii_clientes]], que inclui operações LatAm e TVM sensíveis. A carteira total inclui compulsórios e ativos remunerados a taxas fixas que entram pelo [[nii_mercado]].

## Divulgação por Banco

| Banco | Divulgação | Localização no Release |
|-------|------------|----------------------|
| [[itau]] (ITUB4) | Carteira sensível (~R$1.28T); calculado internamente | Nota explicativa do NII (decomposição NII Clientes) |
| [[bradesco]] (BBDC4) | Saldo médio publicado diretamente (~R$950B) | Release p.9 — Margem Financeira |

**Detalhe Bradesco:** O BBDC4 facilita a modelagem ao publicar o saldo médio explicitamente, separando "saldo médio de operações de crédito" e "saldo médio de TVM". Não é necessário calcular — usar direto do release.

## No Contexto Brasileiro

A carteira de crédito do Sistema Financeiro Nacional (SFN) total soma ~R$6-7T (2025), equivalente a ~60-65% do PIB. Os quatro maiores bancos (ITUB4, BBDC4, BBAS3, Caixa) detêm ~70-75% da carteira total.

**Crescimento histórico:** A carteira do SFN cresceu ~10-15% a.a. nos últimos 10 anos em termos nominais, acima da inflação mas próximo ao crescimento do PIB nominal. Períodos de retração (~2016, ~2020) coincidiram com recessões.

**Taxa de crescimento típica para grandes privados (2025-2026):**
- [[itau]]: +8-10% a.a. (guidance) — foco em pessoas físicas e consignado privado
- [[bradesco]]: +8-12% a.a. — crescimento como ferramenta de recuperação de NII

## Conectando Crescimento de Carteira ao NII

```
NII(t) = Carteira_Média(t) × NIM(t)
       = Carteira_Média(t-1) × (1 + g_carteira) × NIM(t)
```

Se a carteira cresce 10% e o NIM fica estável:

```
NII cresce ~10% YoY — puramente por volume
```

Se o NIM também expande 50bps (de 12.0% para 12.5%):

```
NII cresce ~10% × (12.5/12.0) ≈ ~14,6% YoY — efeito composto volume + pricing
```

Este é o framework central do [[crescimento_carteira]]: separar o crescimento de NII em volume (carteira média) e preço (NIM).

## [[sanb11]] — Diferença de Denominador

Um caso importante de uso da carteira média é o **NIM do Santander**. O banco reporta NIM de ~10,7% usando a carteira ampliada como denominador (que inclui avais, garantias prestadas, ACC/ACE). O modelo interno usa apenas a **carteira gerencial de crédito** (~R$566B) como denominador, resultando em NIM implícito de ~11,5%.

```
NIM_reportado_SANB = NII_Clientes / Carteira_Ampliada ≈ 10,7%
NIM_implicito_modelo = NII_Clientes / Carteira_Crédito_Gerencial ≈ 11,5%
```

Essa diferença de denominador (~R$140B entre carteira ampliada e carteira de crédito) explica integralmente a diferença. O modelo usa o NIM implícito calibrado historicamente (11,5%), não o NIM reportado — mesma base do histórico gerencial que o modelo tem acesso.

## Carteira Média no Grafo de Dependências

No grafo de dependências dos modelos bancários, a carteira média aparece como:
- **Premissa de entrada**: taxa de crescimento YoY da carteira sensível (ex: `g_carteira = 8%`)
- **Variável derivada**: carteira média trimestral = média do saldo fim de trimestre anterior e saldo fim do trimestre atual

```python
# Lógica no compute_banking.py
carteira_sensivel_t = carteira_sensivel_t1 * (1 + g_carteira_yoy / 4)
carteira_media_t    = (carteira_sensivel_t1 + carteira_sensivel_t) / 2
nii_clientes_t      = carteira_media_t * spread_clientes / 4
```

O `spread_clientes` é o NIM aplicável à carteira sensível, diferenciado do NIM total que inclui outras fontes de funding.

### Sensibilidade: Crescimento vs NIM

Para entender o impacto de premissas no NII, é útil separar o efeito volume do efeito preço:

| Premissa | Variação | Impacto no NII Trimestral |
|----------|----------|--------------------------|
| g_carteira (+1pp) | ex: 8% → 9% | +0,25% do NII (efeito marginal trimestral) |
| spread_clientes (+10bps) | ex: 9.5% → 9.6% | +0,25% do NII (carteira × Δspread / 4) |
| Ambos | — | efeito composto (~+0.5%) |

Para carteira de R$1.280T e spread de 9.5%: NII trimestral = R$30,4B. Um crescimento de carteira de +1pp ao ano adiciona ~R$320M de NII no ano.

## Detalhamento por Segmento

A carteira total pode ser dividida por segmento para análise mais granular:

### Itaú Unibanco (ITUB4)

| Segmento | Saldo Estimado (2025) | Spread Típico |
|----------|----------------------|---------------|
| Pessoas Físicas | ~R$480B | 13-15% a.a. |
| Cartões de Crédito | ~R$120B | 25-35% a.a. (risco alto) |
| Pequenas e Médias Empresas | ~R$200B | 10-12% a.a. |
| Grandes Corporates | ~R$180B | 3-5% a.a. (low risk) |
| LatAm | ~R$300B | Variado (câmbio + local rate) |

O spread médio ponderado da `carteira_sensivel` do Itaú fica ~9,0-9,5% ao ano.

### Bradesco (BBDC4)

O Bradesco publica saldo médio por segmento diretamente no release (diferencial em relação ao Itaú que requer reconstrução). O modelo BBDC4 usa esses saldos diretamente como premissa:

```
NII_Clientes = Σ (Saldo_Médio_segmento × Spread_segmento)
```

**Detalhe importante:** Em 2024-2025, o Bradesco está em modo de **repricing da carteira** — após perdas em PME de 2023, está substituindo carteira de maior risco por carteira menor mas mais segura (consignado, crédito imobiliário). Isso reduz o spread médio mas também reduz o custo de risco, melhorando o NII líquido.

## Implicação para o Modelo: Carteira Média vs Carteira Fim

Erro comum em modelos bancários: usar o saldo fim de trimestre como denominador do NIM ao invés do saldo médio. Isso produz:

```
NIM_errado = NII_trimestral / Carteira_fim × 4   (sobreestima NIM se carteira cresceu)
NIM_correto = NII_trimestral / Carteira_média × 4  (correto)
```

Para calibração do histórico, sempre usar carteira média. Para projeção, projetar crescimento da carteira (saldos de fim de período) e derivar a média como (início + fim) / 2.

## Ver Também

- [[nim]] — Net Interest Margin; aplicado sobre a carteira média para gerar NII
- [[nii_clientes]] — componente de spread da carteira de clientes
- [[custo_risco]] — PDD = carteira média × custo de risco anualizado / 4
- [[crescimento_carteira]] — driver de crescimento de NII via volume
- [[banking]] — framework completo da DRE bancária
- [[itau]] — carteira sensível ITUB4 (~R$1.28T em 2025)
- [[bradesco]] — saldo médio publicado no release
- [[sanb11]] — NIM reportado usa carteira ampliada como denominador (metodologia diferente)
- [[spread_clientes]] — spread aplicado à carteira média para calcular NII Clientes
