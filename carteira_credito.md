---
type: conceito
aliases: [Carteira de Crédito, Carteira Ampliada, Portfolio de Crédito, Loan Book]
sources:
  - sectors/banking/sector_profile.md
  - wiki/banking.md
  - wiki/nii_clientes.md
  - wiki/custo_risco.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
updated: 2026-04-05
---

# Carteira de Crédito

A **carteira de crédito** é o conjunto de operações de empréstimo, financiamento e adiantamento de um banco — ou seja, o estoque de crédito concedido e ainda não liquidado. É o principal ativo gerador de receita dos bancos de varejo brasileiros e a base sobre a qual incide o [[nim]] (gerando [[nii_clientes]]) e o [[custo_risco]] (gerando PDD).

## Composição Típica

Os grandes bancos brasileiros divulgam a carteira de crédito por modalidade e segmento:

### Por Segmento de Cliente

| Segmento | Características | NIM típico | Risco típico |
|----------|----------------|-----------|-------------|
| **PF — Consignado** | Desconto em folha, risco baixíssimo | Baixo (~10-12%) | Muito baixo (~1-2%) |
| **PF — Imobiliário** | Colateral imóvel, prazo longo | Baixo (~8-10%) | Baixo (~0,5-1%) |
| **PF — Veículos** | Colateral veículo, prazo médio | Médio (~15-18%) | Médio (~3-5%) |
| **PF — Cartão de crédito** | Rotativo alto risco/retorno | Alto (~30-40% no rotativo) | Alto (~8-12%) |
| **PF — Pessoal/outros** | Sem garantia, risco médio-alto | Médio-alto (~20-25%) | Médio-alto (~5-8%) |
| **PME** | Empresas pequenas/médias, risco variável | Médio (~12-18%) | Médio (~3-6%) |
| **Grandes Empresas/Corp** | Empresas grandes, spread mais apertado | Baixo (~7-10%) | Baixo (~1-2%) |
| **Agro** | Lastreado em recebíveis, regulado (MCR) | Baixo (~8-10%) | Baixo (subsídio implícito) |

### Por Banco Coberto (4T25, R$B)

| Banco | Carteira Total | Mix PF | Mix PJ | Destaques |
|-------|--------------|--------|--------|-----------|
| [[itau]] (ITUB4) | ~R$1.490B | ~55% | ~45% | Consignado privado, cartão, imobiliário |
| [[bradesco]] (BBDC4) | ~R$650B | ~50% | ~50% | Agro, PME, imobiliário |
| [[sanb11]] (SANB11) | ~R$566B | ~55% | ~45% | Veículos (via Santander Financeiras), PME |

## Carteira Ampliada vs Carteira COSIF

Os bancos gerenciam dois conceitos de carteira:

**Carteira COSIF (Contábil):** Operações de crédito conforme o plano de contas do BCB. Base para os demonstrativos contábeis (ITR/DFP). Inclui provisões (PDD) deduzidas para chegar ao saldo líquido.

**Carteira Ampliada (Gerencial):** Inclui operações que economicamente são crédito mas contabilmente não entram na carteira COSIF — principalmente:
- Garantias prestadas
- Avais e fianças
- Debêntures e CRIs/CRAs em carteira de clientes corporativos
- Adiantamentos sobre contratos de câmbio (ACC/ACE)
- Operações compromissadas com clientes

A carteira ampliada é a base dos releases gerenciais e do modelo. O Santander, por exemplo, divulga carteira ampliada de ~R$566B vs carteira COSIF menor.

## Métricas Derivadas

### NIM Implícito
```
NIM_implicito = NII_Clientes_trimestral × 4 / Carteira_Média
```

A carteira média é usada (não o saldo final) porque o NII flui ao longo do trimestre. Ver [[carteira_media]].

### Custo de Risco
```
Custo_Risco_anualizado = PDD_trimestral × 4 / Carteira_Média
```

### Cobertura
```
Cobertura = Saldo_PDD_em_balanço / Carteira_inadimplente_90d
```
Indicador de adequação das provisões. Bancos brasileiros mantêm tipicamente 150-220% de cobertura.

### NPL (Non-Performing Loans)
```
NPL_90d = Carteira_vencida_>90_dias / Carteira_Total
```

## Crescimento de Carteira como Driver

O crescimento da carteira de crédito é o principal driver de volume do [[nii_clientes]]:

```
NII_Clientes(t) ≈ Carteira_Média(t) × NIM(t)
                = Carteira_Média(t-1) × (1 + g) × NIM(t)
```

**Crescimento 2025 por banco:**
- ITUB4: ~+8-10% YoY (guidance implícito)
- BBDC4: ~+8-12% YoY (estratégia de recuperação)
- SANB11: +3,7% YoY em 2025 (crescimento seletivo); guidance 2026 ~8%

## Mix de Carteira como Driver de NIM

O mix de carteira determina o NIM médio da carteira inteira. Bancos com maior peso em:
- **Consignado público** → NIM mais baixo, risco muito baixo (Banco do Brasil)
- **Veículos e cartão** → NIM mais alto, risco mais alto ([[sanb11]], [[nubank]])
- **Imobiliário** → NIM baixo, risco baixo (Itaú tem proporção relevante)
- **Agro** → NIM baixo, risco baixo (Bradesco, Banco do Brasil)

**O Santander é o único grande banco privado com carteira de veículos como item material (~15-20% da carteira PF)**, via Santander Financeiras + Webmotors. Isso eleva o NIM mas também o custo de risco — historicamente o calcanhar de Aquiles do Santander.

## Por Empresa

| Empresa | NIM Implícito (2025) | Custo de Risco (2025) | Mix Diferenciador |
|---------|---------------------|----------------------|------------------|
| [[itau]] | ~11-12% | ~3,7% | Consignado privado, cartão |
| [[bradesco]] | ~10-11% | ~5,4% | Agro, PME, imobiliário |
| [[sanb11]] | ~11,5% (calibrado) | ~4,8% | Veículos (Webmotors), PME, Select |

## Ciclo de Crédito e Impacto no Modelo

O ciclo de crédito afeta tanto o crescimento da carteira quanto a qualidade dos ativos:

**Fase expansionista (Selic em queda):** Bancos expandem carteira, tomam mais risco. NIM cai (mais competição por bons clientes), mas volume compensa. PDD futura sobe com defasagem de 12-18 meses.

**Fase contracionista (Selic em alta, como 2025-2026):** Bancos ficam seletivos, crescem abaixo do PIB. NIM pode subir (repricing de carteira), mas volume desacelera. PDD de safras antigas começa a normalizar.

No modelo, o [[crescimento_carteira]] é premissa YoY sobre mesmo trimestre do ano anterior (não QoQ), capturando sazonalidade. O [[custo_risco]] é premissa como % anualizado da [[carteira_media]].

## Regulação: [[compulsorios]] e Direcionamento

O BCB exige que bancos direcionem parcela da carteira para:
- **Crédito imobiliário**: 65% dos depósitos de poupança → SBPE (taxa regulada)
- **Crédito rural**: 34% dos depósitos à vista → MCR (taxa regulada)
- **Microcrédito**: 2% dos depósitos à vista → MPO (taxa regulada)

Essas exigibilidades comprimem o NIM médio porque forçam alocação em carteiras de spread baixo. Bancos com mais captação em poupança (ex: [[bradesco]], Caixa) têm proporcionalmente mais carteira imobiliária regulada.

Os [[compulsorios]] sobre depósitos (à vista: 21%, poupança: 20%, a prazo: 25%) reduzem o capital disponível para crédito livre, afetando indiretamente o volume total da carteira.

## Ver Também

- [[carteira_media]] — saldo médio, base do cálculo de NIM e custo de risco
- [[nim]] — margem de juros aplicada sobre a carteira
- [[nii_clientes]] — resultado de margem com clientes (carteira × NIM)
- [[custo_risco]] — PDD = carteira × custo de risco
- [[crescimento_carteira]] — driver de volume do NII
- [[compulsorios]] — regulação que afeta alocação de carteira
- [[selic]] — ciclo de juros como driver macro
- [[banking]] — framework completo da DRE bancária
- [[itau]] — maior carteira privada do Brasil
- [[bradesco]] — turnaround via crescimento de carteira
- [[sanb11]] — diferencial em veículos via Webmotors
- [[nubank]] — disruptor digital, carteira de cartão pura
