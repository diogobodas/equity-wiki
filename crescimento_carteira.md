---
type: conceito
aliases: [Crescimento da Carteira de Crédito, Loan Portfolio Growth, Crescimento do Crédito]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/filings/releases/ITUB4_release_2025.pdf
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
source_quality: verified
updated: 2026-04-05
---

# Crescimento da Carteira de Crédito

O **crescimento da carteira de crédito** é a variação percentual YoY do saldo total de operações de crédito de um banco. É o principal driver de volume para projeção do [[nii_clientes]]: mais carteira × spread = mais NII. Junto com a [[selic]] (que determina o spread), é um dos dois eixos centrais da análise bancária.

## Como Funciona

```
Crescimento_Carteira_YoY(t) = Carteira(t) / Carteira(t-4) - 1
```

Na modelagem:

```
NII_Clientes(t) = NII_Clientes(t-4) × (1 + g_yoy)
```

onde `g_yoy` é guiado pelo crescimento da carteira. Não se usa crescimento QoQ composto — a sazonalidade trimestral torna o QoQ enganoso; o correto é sempre comparar com o mesmo trimestre do ano anterior.

### Decompondo o Crescimento

| Alavanca | Descrição |
|----------|-----------|
| Crescimento orgânico de crédito | Novas concessões > amortizações |
| Mix shift para segmentos maiores | Ex: migrar de consignado para capital de giro |
| Crescimento em [[consignado_privado]] | Produto novo com originação acelerando |
| Expansão LatAm ([[latam]]) | Carteira em Chile, Colômbia, Argentina |
| Variação cambial | Carteira LatAm em moeda local × BRL |

## No Contexto Brasileiro

- O BCB publica mensalmente o estoque total de crédito do SFN (Sistema Financeiro Nacional) — cresceu ~10% em 2025.
- **Guidance dos bancos** é a fonte primária para modelagem (mais confiável que extrapolação histórica).
- O crescimento se decompõe em Brasil e LatAm. A maioria dos guidances para 2026 refere-se apenas ao Brasil.
- **Consignado privado CLT** é o produto de maior crescimento estrutural para 2026-2028: regulamentado em 2024, escalando rapidamente.
- Crédito imobiliário (SFH) continua crescendo sustentado por déficit habitacional + FGTS + LCI.

### Sazonalidade

| Trimestre | Padrão Típico |
|-----------|---------------|
| 1T | Mais fraco — pagamento de 13º em 4T reduz demanda de crédito |
| 2T-3T | Recuperação gradual |
| 4T | Pico de concessões (Black Friday, FGTS, natal) |

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | Carteira Brasil dez/25: R$1.084B (sem garantias). Carteira total consolidada (c/ garantias + LatAm): R$1.491B. Crescimento YoY 2025: +6,1% (Brasil). Guidance 2026 Brasil: **+6,5-10,5%**. Consignado CLT e imobiliário são os dois motores de crescimento. Grandes empresas: R$455,9B (+5,2% YoY). PME: R$303,1B (+8,7% YoY). Fonte: Release 4T25, p.21. |
| [[bradesco]] | Em recomposição pós-crise de crédito 2022-23. Crescimento abaixo do setor em 2024-25; retomada gradual esperada para 2026. |

## Carteira Média vs Saldo Final

O [[nii_clientes]] é calculado sobre a **carteira média** do trimestre — aproximação da média dos saldos diários de crédito — não sobre o saldo final de período. Essa distinção tem implicações diretas para a modelagem.

### Fórmula de Aproximação

```
Carteira_Média(t) = (Carteira_Início(t) + Carteira_Fim(t)) / 2
```

onde `Carteira_Início(t) = Carteira_Fim(t-1)`. É uma aproximação razoável para fins de modelagem trimestral; a média real dos saldos diários seria ligeiramente diferente dependendo da distribuição intra-trimestral das concessões.

### Por que Importa: Timing de Crescimento

Um banco que origina R$10B de crédito em janeiro carrega essa carteira por ~90 dias no 1T. Um banco que origina R$10B em março carrega apenas ~30 dias no mesmo trimestre. O saldo final de março é idêntico nos dois casos, mas o NII do trimestre é ~3× maior no primeiro caso.

Implicação: crescimento de carteira acelerado no início do trimestre tem impacto desproporcional no NII daquele trimestre vs crescimento concentrado no fim.

### No Modelo ITUB4

No grafo de dependências do [[itau]]:
- `der:carteira_media` é calculado como média entre o saldo do trimestre atual e o saldo do trimestre anterior
- `der:carteira_media` é o **driver direto** de `der:nii` (via spread implícito)
- O crescimento YoY do NII nem sempre iguala o crescimento YoY da carteira-saldo: o que importa é a variação da **média** de `t` vs a **média** de `t-4`

### Exemplo Numérico

Se a carteira cresceu uniformemente ao longo de 2025 (saldo início: R$1.100B, saldo fim: R$1.200B):
- Carteira média 2025 ≈ R$1.150B
- Se em 2026 o crescimento for concentrado no 4T (saldo fim: ~R$1.280B, mas saldo médio: ~R$1.210B):
- NII 2026 cresce ~5% YoY (média/média), mas a carteira-saldo cresce ~6.7% YoY

O analista que usar crescimento do saldo como proxy de NII estará superestimando o NII neste cenário.

## Decomposição da Carteira Brasil por Segmento

Dados reais do Release 4T25 ITUB4, tabela "Carteira de Crédito com Garantias Financeiras e Títulos Privados" (p.21). Fonte: verified.

| Segmento | Saldo dez/25 (R$B) | QoQ | YoY (vs dez/24) | % do Total Brasil |
|----------|--------------------|-----|-----------------|-------------------|
| **Grandes Empresas** | **455,9** | +4,1% | +5,2% | ~38% |
| **Micro, Peq. e Méd. Empresas (PME)** | **303,1** | +8,8% | +8,7% | ~25% |
| **Cartão de Crédito** | **153,5** | +8,0% | +8,0% | ~13% |
| **Imobiliário (PF)** | **141,7** | +3,4% | +12,8% | ~12% |
| **Consignado** | **75,3** | +4,0% | +1,2% | ~6% |
| **Veículos (PF)** | **36,3** | -0,1% | -0,6% | ~3% |
| **Total Brasil (sem garantias)** | **~1.084** | — | +6,1%* | 100% |

*YoY estimado com base nos saldos divulgados (dez/25 vs dez/24).

> **Total consolidado** (com garantias prestadas + títulos privados + LatAm): **R$1.490,8B** (4T25). Brasil puro ~R$1.084B (carteira sem garantias financeiras e títulos). Diferença = garantias prestadas a terceiros + operações em LatAm (~R$150-160B).

### Dinâmica por Produto (dados reais)

**[[consignado_privado]]** (PF — dentro do Consignado): produto novo regulamentado em 2024. No 4T25, consignado setor privado cresceu **+27,5% QoQ** em função do novo crédito do trabalhador CLT. Contudo, consignado INSS e setor público caíram no canal externo, compensando parcialmente. Estoque total de consignado: R$75,3B (+1,2% YoY — crescimento total modesto, mas mix shift interno acelerado para CLT). Originação em jan/26: R$1,9B/mês (R$1,3B/mês em dez/25). É o maior vetor de crescimento estrutural do banco para 2026-2028.

**Crédito imobiliário** (PF): R$141,7B (+12,8% YoY — destaque de crescimento). Contratações no 4T25: R$12,3B (-27% vs dez/24 mas reflete sazonalidade favorável 4T). LTV médio da carteira: 38,4%. Safra média 64,8% de entrada. Produto de baixo risco e longo prazo; 91% de PF. Sem sinais de desaceleração estrutural.

**Veículos** (PF): R$36,3B (estagnado: -0,1% QoQ, -0,6% YoY). Management sinalizou "rentabilidade duvidosa" em teleconferência 4T25. Banco priorizará outros produtos em 2026. Valor médio financiado: R$53,9k.

**Grandes Empresas** (PJ): R$455,9B (+4,1% QoQ, +5,2% YoY). Maior segmento do banco. Crescimento concentrado em empresas de faturamento R$500M–R$4B. Excluindo variação cambial, crescimento teria sido +7,3% YoY — o BRL forte em 2025 comprimiu o saldo em R$ das operações LatAm dentro desse segmento.

**PME (Micro, Peq. e Méd. Empresas)**: R$303,1B (+8,8% QoQ, +8,7% YoY). Crescimento surpreendentemente forte no 4T25 — médias empresas (+12% QoQ por demanda de crédito de curto prazo); pequenas via programas governamentais. Agronegócio e programas governamentais puxam no YoY.

**Cartão de Crédito**: R$153,5B (+8% QoQ, +8% YoY). Mix 4T25: 87,2% à vista + parcelado s/juros, 7,5% parcelado com juros, 5,3% rotativo. Originação: 75% via rede de agências, 25% Itaú Consignado S.A.

### Estratégia de Mix 2026

A estratégia declarada do [[itau]] para 2026 é acelerar os três produtos de melhor retorno ajustado ao risco: (1) **consignado privado CLT**, (2) **crédito imobiliário**, (3) **grandes empresas**. Veículos crescem abaixo do portfólio (ou estagnados). PME: crescimento seletivo com foco em agronegócio e programas governamentais. Essa composição favorece [[custo_risco]] controlado mesmo com crescimento acelerado da carteira total.

## Bear vs Bull Case do Guidance 6.5–10.5%

O guidance do [[itau]] para crescimento da carteira Brasil em 2026 é **+6,5–10,5% YoY** (consolidado: +5,5–9,5%). A amplitude de 4pp reflete incerteza macroeconômica, especialmente sobre trajetória da [[selic]] e comportamento do crédito PF em ambiente de juros altos.

### Cenários

| Cenário | Crescimento Brasil | Premissas Principais |
|---------|--------------------|----------------------|
| Bear | ~6,5% | Selic alta por tempo longo reprime demanda PF; PJ desacelera por deterioração do ciclo; crédito imobiliário normaliza após anos de crescimento forte; consignado privado cresce mas ainda pequeno no estoque |
| Base | ~8,5% | Consignado privado acelera (R$30-40B de estoque ao final de 2026); imobiliário mantém ritmo; grandes empresas crescem seletivamente; Selic começa a recuar no 2S26 |
| Bull | ~10,5% | Consignado privado escala mais rápido que o esperado (estoque R$50B+); LatAm se beneficia de câmbio favorável (BRL fraco); PF em geral normaliza pós-ciclo de inadimplência; PME recupera |

### Sensitivity: Impacto no NII

Para uma carteira ~R$1.050B (Brasil) e [[nim]] implícito de ~12% ao ano (bruto, sobre carteira gerencial):

- Cada 1pp de crescimento a menos na carteira ≈ **–R$300–400M de NII anual** (~–R$75-100M/trimestre)
- Diferença bear vs bull (4pp) ≈ **–R$1,2–1,6B de NII no ano** — material (~3-4% do NII total)

Esses números são **estimativas (~)** para análise de sensibilidade; o NII real depende também do mix (produtos diferentes têm spreads diferentes) e da dinâmica de reprecificação do portfólio ao longo do ano.

### O Que Monitorar

- Originação mensal de consignado privado (BCB publica com ~45 dias de defasagem)
- Concessões totais de crédito imobiliário (ABECIP, mensal)
- Atas do COPOM: sinalização de corte de Selic antecipa recuperação do PF
- Resultado 1T26: a guidance range costuma ser revisada (estreitada) após o primeiro trimestre

## Sazonalidade Intra-Trimestral

Nota técnica relevante para modelagem e interpretação de saldos.

### Padrão por Trimestre

**4T (outubro–dezembro):** pico de concessões do ano. Black Friday eleva crédito ao consumo e cartões; FGTS aniversário (modalidades saque-aniversário) gera originação de consignado; crédito natalino. Resultado: saldo final de dezembro frequentemente o maior do ano. A carteira média do 4T é inferior ao saldo final — o crescimento se concentra no fim do trimestre.

**1T (janeiro–março):** pagamento do 13º salário em dezembro/janeiro **reduz** a necessidade de crédito rotativo (cartão, crédito pessoal) — famílias quitam dívidas. Crédito imobiliário e consignado mantêm ritmo, mas o portfólio total pode cair QoQ em relação ao pico de dezembro. Saldo final de março frequentemente abaixo de dezembro.

**2T–3T:** recuperação gradual. Demanda retoma com ciclo normal de consumo e investimento.

### Implicação para Modelagem YoY

A abordagem de projetar YoY (mesmo trimestre t vs t-4) **captura a sazonalidade implicitamente**: compara 1T26 com 1T25, ambos com o mesmo padrão sazonal. Isso elimina o ruído da comparação QoQ — um crescimento de carteira de –2% QoQ no 1T pode ser perfeitamente normal e irrelevante.

```
# Correto: YoY remove sazonalidade
Crescimento(1T26) = Carteira(1T26) / Carteira(1T25) - 1  ✓

# Enganoso: QoQ captura sazonalidade como sinal
Crescimento(1T26) = Carteira(1T26) / Carteira(4T25) - 1  ✗
```

### Atenção: Carteira Média vs Saldo Final no 4T

Pelo pico de concessões em dezembro, a **carteira média do 4T** é sistematicamente inferior ao saldo final de dezembro. Isso cria uma armadilha: usar o saldo final de 4T como proxy de carteira média superestima o NII daquele trimestre. O efeito se inverte no 1T: a carteira média do 1T é próxima ao saldo de abertura (dezembro), então o NII do 1T pode ser forte mesmo com saldo final mais baixo. Ver [[carteira_media]] para detalhes.

## Ver Também

- [[nii_clientes]] — volume × spread = NII; crescimento da carteira é o driver de volume
- [[consignado_privado]] — maior vetor de crescimento estrutural 2026-2028
- [[selic]] — driver de spread (preço), complementar ao volume
- [[custo_risco]] — crescer mais rápido eleva risco se o banco baixar critérios de concessão
- [[latam]] — carteira internacional do Itaú (~15% do total)
- [[banking]] — contexto setorial
- [[nim]] — margem financeira líquida; combinação de spread e mix de carteira
- [[carteira_media]] — conceito técnico de average earning assets para cálculo de NII
