---
type: conceito
source_quality: conceptual
aliases: [NII Mercado, NII de Mercado, Margem Financeira de Mercado, Treasury NII, NII Tesouraria]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_historical_gerencial.json
updated: 2026-04-05
---

# NII de Mercado

O **NII de Mercado** (ou NII de Tesouraria) é o componente do [[nim]] gerado pelas operações de tesouraria: portfólio de títulos e valores mobiliários (TVM), derivativos, operações de câmbio e gestão de liquidez. É mais volátil e menos previsível do que o [[nii_clientes]], pois depende de posicionamento tático e condições de mercado.

## Como Funciona

```
NII_Mercado = Resultado_TVM + Resultado_Derivativos + Resultado_Câmbio
            - Custo_Carrego_Compulsórios
```

As principais fontes são:
- **Portfólio de TVM** (títulos públicos federais, debêntures, CRIs): remuneração via NII + ganhos/perdas a mercado (mark-to-market em "negociação")
- **Derivativos**: hedge de risco de taxa de juros, câmbio, crédito; também posições proprietárias
- **Câmbio**: resultado da posição cambial (ativo em moeda estrangeira vs passivo)
- **Compulsórios**: recolhimento obrigatório ao BCB, parcialmente remunerado (reduz NII líquido)

### Relação com a [[selic]]

O NII de Mercado é sensível à [[selic]] de forma diferente do [[nii_clientes]]:
- Selic alta → TVM prefixados em carteira sofrem marcação negativa (preço cai quando yield sobe)
- Selic alta → Posições pós-fixadas (LFT, compromissadas) ganham mais
- Duration do portfólio de TVM determina a sensibilidade: duration longa = mais volátil

**Resultado:** Nos releases, NII Mercado é frequentemente a linha que mais surpreende (para cima ou para baixo) vs consenso, especialmente em trimestres de volatilidade nas taxas de juros.

## No Contexto Brasileiro

**Portfólio típico de TVM dos grandes bancos brasileiros:**
- LFT (Letras Financeiras do Tesouro) — pós-fixadas, baixo risco de mercado
- NTN-B (IPCA+) — intermediárias; expostas à abertura de juro real
- LTN/NTN-F — prefixadas; maior duration, maior risco de mercado
- Debêntures e CRIs — menor liquidez, maior spread de crédito

**Compulsórios:** O BCB exige que bancos depositem parcela dos depósitos como compulsório. São parcialmente remunerados (pós-fixado, mas abaixo do CDI). Esse "custo de carrego" entra negativamente no NII de Mercado.

### Modelagem

Ao contrário do [[nii_clientes]], modelar NII de Mercado por drivers fundamentais é difícil. A prática é:
1. Usar o histórico YoY e guidance do banco
2. Aplicar sensibilidade declarada a movimentos de Selic
3. Tratar como componente mais conservador (menor crescimento nominal vs NII Clientes)

Itaú publica separadamente NII Clientes e NII Mercado em seus releases — facilita a modelagem.

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | Componente menor que NII Clientes, mas relevante. Histórico de gestão de tesouraria eficiente; posição cambial parcialmente hedgeada. NII Mercado publica separado no release. |
| [[bradesco]] | Bradesco Seguros gera um float significativo de prêmios captados → investido em TVM → contribui para NII de Mercado. A consolidação de seguros torna o NII de Mercado de Bradesco proporcionalmente maior. |

## Magnitude e Composição para Itaú

O NII de Mercado representa uma fração pequena mas não desprezível do [[nim]] total do [[itau]]:

- **Proporção**: NII Mercado é ~5-10% do NII total; [[nii_clientes]] responde por ~90-95%
- **Escala 2025**: NII Mercado estimado em ~R$4-6B/ano vs [[nii_clientes]] ~R$100-110B/ano
- **Guidance 2026**: R$2.5-5.5B para o ano — range amplo refletindo sensibilidade do portfólio a condições de mercado (ver seção abaixo)

A composição do NII Mercado do Itaú tem quatro blocos principais:

| Bloco | Descrição |
|-------|-----------|
| (a) Carrego do portfólio de TVM | Rendimento do portfólio de ~R$400-600B em títulos, líquido de funding |
| (b) Resultado de derivativos de hedge | Ganhos/perdas em swaps e futuros usados para gestão de [[duration]] e [[risco_cambial]] |
| (c) Posição cambial líquida | Resultado da exposição cambial residual (ativo LatAm parcialmente hedgeado) |
| (d) Custo dos compulsórios (negativo) | BCB exige recolhimento de ~20-40% dos depósitos à vista/a prazo; parcialmente remunerado via [[selic]]-haircut. Custo líquido estimado: ~R$1-2B/ano de drag no NII Mercado |

O custo dos compulsórios é estrutural — existe independentemente de posicionamento tático — e reduz o NII Mercado bruto do portfólio de TVM.

## Carrego do Portfólio de TVM

O portfólio de TVM dos bancos brasileiros é dominado por títulos pós-fixados, o que limita o risco de [[duration]] mas também o potencial de ganho extraordinário:

- **LFT (Letras Financeiras do Tesouro)**: pós-fixadas [[selic]], sem risco de duration. Rentabilidade acompanha a taxa básica diretamente. Composição preferencial dos grandes bancos.
- **NTN-B (IPCA+)**: exposição ao juro real. Quando a taxa real sobe (inflação normaliza mas Selic permanece elevada), o preço cai → MTM negativo no portfólio. Risco assimétrico em cenário de desinflação.
- **LTN/NTN-F prefixadas**: expostas a mudança de expectativa de Selic. Duration mais longa implica maior oscilação de preço a mercado.

**Posicionamento histórico do Itaú**: preferência por LFT (curto prazo, baixo risco) — resulta em menor volatilidade do NII Mercado trimestral vs pares com maior duration. Estratégia coerente com o perfil de gestão conservadora de [[risco_mercado]] do banco.

**Estratégia pós-2023**: após o ciclo de aperto monetário 2021-2023, o Itaú reduziu ainda mais a duration do portfólio de TVM. Efeito: NII Mercado mais estável e previsível, porém com menor potencial de carrego em cenário de queda de juros. O trade-off é deliberado — o banco prefere previsibilidade de resultado ao ganho tático de posicionamento em curva.

> **Implicação para modelo**: o carrego do portfólio de TVM segue [[selic]] com lag reduzido. Em cenário de Selic 2025 em ~13.25%, o carrego bruto do portfólio é relativamente elevado, mas o guidance conservador de 2026 (midpoint ~R$4.0B) sugere que o banco não antecipa ganhos extraordinários adicionais.

## Por Que o Range de Guidance É Tão Largo (R$2.5-5.5B)

O guidance 2026 do Itaú para NII Mercado (R$2.5-5.5B) tem range de R$3.0B — incomum para uma linha de resultado. A variabilidade estrutural vem de três fontes:

1. **Resultado de derivativos de hedge**: swaps, futuros de DI e contratos de câmbio usados para gestão de [[risco_mercado]]. O resultado desses instrumentos pode variar ±R$1B/ano com movimentos na curva de juros, independentemente da intenção de hedge.

2. **Posição cambial residual após hedge de LatAm**: o Itaú tem operações relevantes na América Latina. O hedge cambial não é perfeito — a posição residual gera resultado positivo ou negativo dependendo da variação do BRL vs moedas locais.

3. **MTM de TVM em "negociação" vs "disponível para venda"**: títulos classificados como "para negociação" são marcados a mercado pelo resultado — uma abertura de curva de 100bps pode gerar perdas de marcação relevantes no trimestre, mesmo sem realização.

**Abordagem de modelagem recomendada:**
- Usar o midpoint do guidance (~R$4.0B/ano, ~R$1.0B/trimestre) como premissa-base
- Aplicar a sensibilidade declarada pelo banco a movimentos de Selic (geralmente publicada no release)
- Não tentar modelar resultado de derivativos de forma bottom-up — é residual da gestão de balanço
- NII Mercado não é driver estratégico do [[itau]]; o risco assimétrico é para baixo (abertura de curva, perdas de MTM) mais do que para cima

> **Nota para analistas**: surpreendentes positivas de NII Mercado tendem a não ser recorrentes — evitar extrapolar para projeções futuras. O banco gerencia ativamente para suavizar o resultado, mas a volatilidade intrínseca do portfólio limita essa capacidade.

## Diferença Bradesco: Float de Seguros

Uma diferença estrutural importante entre [[itau]] e [[bradesco]] no NII de Mercado é o tratamento do negócio de seguros:

**Bradesco Seguros — consolidação integral:**
- O [[bradesco]] consolida a Bradesco Seguros integralmente no balanço consolidado
- O float de prêmios captados (~R$300-400B em reservas técnicas) é investido em TVM pelo grupo segurador
- Esse float gera NII de Mercado adicional relevante, que aparece diretamente na demonstração consolidada do Bradesco
- Resultado: NII de Mercado do Bradesco é proporcionalmente maior como % do NII total

**Porto Seguro — método de equivalência patrimonial para o Itaú:**
- O Itaú detém participação na Porto Seguro, mas contabiliza via [[equivalencia_patrimonial]] (método EP)
- O rendimento das reservas técnicas da Porto Seguro **não aparece no NII Mercado do Itaú**
- Aparece no resultado de EP (linha separada abaixo do EBIT), já líquido de impostos e minorities
- Resultado: NII Mercado do Itaú é estruturalmente menor proporcionalmente do que o do Bradesco

**Implicação para comparação entre bancos**: ao comparar NIM ou NII Mercado entre Itaú e Bradesco, é necessário ajustar para essa diferença estrutural. O NII Mercado "equivalente" do Itaú seria maior se a Porto Seguro fosse consolidada integralmente — mas não é, e os modelos devem refletir a estrutura contábil real.

Ver [[resultado_seguros]] para detalhes sobre o tratamento contábil de seguros no setor bancário.

## Ver Também

- [[nii_clientes]] — NII de crédito (mais estável e previsível)
- [[nim]] — NIM total inclui ambos os componentes
- [[selic]] — driver macro de rendimento do portfólio de TVM
- [[resultado_seguros]] — float de seguros alimenta o portfólio de tesouraria
- [[banking]] — contexto setorial e estrutura DRE
- [[equivalencia_patrimonial]] — tratamento contábil de Porto Seguro no balanço do Itaú
- [[risco_mercado]] — duration, MTM e sensibilidade do portfólio de TVM
- [[compulsorios]] — custo de carrego estrutural no NII Mercado
