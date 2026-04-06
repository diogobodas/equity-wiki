---
type: conceito
source_quality: conceptual
aliases: [CET1, Common Equity Tier 1, Capital Principal, Índice de Capital]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_investment_memo.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
updated: 2026-04-05
---

# CET1 — Common Equity Tier 1

O **CET1 (Common Equity Tier 1)**, ou Índice de Capital Principal, é a principal métrica de adequação de capital para bancos sob Basileia III. Ele mede a proporção do capital de maior qualidade (ações ordinárias + reservas + lucros retidos, deduzidas as deduções regulatórias) em relação aos ativos ponderados pelo risco (RWA). Para analistas de ações bancárias, o CET1 é o elo entre a geração de lucro, a capacidade de crescimento da carteira e a política de dividendos — os três determinantes do retorno ao acionista.

## O que é CET1 e por que importa

### Fórmula

```
CET1 (%) = Capital Principal / RWA

Capital Principal = Ações ordinárias integralizadas
                 + Reservas de capital e lucros retidos
                 - Deduções regulatórias
                   (ágio em aquisições, ativos intangíveis, créditos tributários diferidos
                    além de limites, instrumentos de capital de outras IFs)

RWA (Risk-Weighted Assets) = RWA_crédito + RWA_mercado + RWA_operacional
```

### Por que importa

O CET1 opera como **restrição dupla** na gestão bancária:

1. **Restrição de crescimento**: cada novo crédito concedido consome RWA. Se o banco cresce a carteira mais rápido do que acumula capital, o CET1 cai. Abaixo de um threshold regulatório, o banco deve frear o crescimento.

2. **Restrição de distribuição**: dividendos, JCP e recompras de ações reduzem o PL — e portanto o numerador do CET1. O BCB limita automaticamente distribuições quando o CET1 cai abaixo de patamares mínimos regulatórios.

Essa dupla restrição torna o CET1 o **pivot central da modelagem de bancos**: ele é simultaneamente o output da DRE (LL retido aumenta o PL) e o input para o crescimento futuro e política de capital.

### Basileia III: contexto

O Acordo de Basileia III (implementado no Brasil pelo BCB a partir de 2013, com phase-in até 2019) estabeleceu três camadas de capital:

| Camada | Composição | Absorção de perdas |
|--------|-----------|-------------------|
| CET1 — Tier 1 Principal | Ações ordinárias, reservas, lucros retidos | Contínua (going concern) |
| AT1 — Tier 1 Adicional | Instrumentos híbridos (CoCos), bônus perpétuos | Going concern |
| Tier 2 | Dívida subordinada, provisões genéricas | Gone concern |

O **CET1 é a camada de mais alta qualidade** e a mais acompanhada pelo mercado. AT1 e Tier 2 existem mas têm relevância analítica secundária para os grandes bancos brasileiros, que operam com folga de CET1 e não precisam emitir instrumentos híbridos para cumprir requerimentos.

## Requerimentos para D-SIBs Brasileiras

### Estrutura de camadas regulatórias

Os requerimentos de CET1 são cumulativos — cada camada se soma sobre a anterior:

| Camada | Patamar | Base normativa |
|--------|---------|---------------|
| Mínimo regulatório (Basileia III) | 4,5% | BCB Circular 3.784/16 |
| Colchão de conservação de capital | +2,5% | Implementado até 2019 |
| Colchão sistêmico (D-SIB surcharge) | +1,0-2,0% | Proporcional à importância sistêmica |
| Colchão discricionário (Pilar 2) | variável | Discricional do BCB por banco |
| **Requerimento efetivo total** | **~11,5-14%** | soma das camadas acima |

### D-SIBs brasileiras: requerimentos e posições recentes

| Banco | Ticker | Surcharge D-SIB | CET1 mín. efetivo | CET1 4T25 (ref.) | Situação |
|-------|--------|-----------------|-------------------|-------------------|---------|
| [[itau]] | ITUB4 | 2,0% | ~11,5% | 12,3% | Acima do mínimo, abaixo de "excessivo" |
| [[bradesco]] | BBDC4 | 1,5% | ~11,0% | ~11,5% (est.) | Em reconstrução pós-2022-23 |
| Banco do Brasil | BBAS3 | 1,5% | ~11,0% | ~13,0% (est.) | Folgado; distribuições elevadas |
| Santander Brasil | SANB11 | 1,0% | ~10,5% | ~13,5% (est.) | Folgado |
| Caixa Econômica | CEF | 1,5% | ~11,0% | — | Capital controlado pelo Tesouro |

> Nota: os valores de surcharge D-SIB são calibrados anualmente pelo BCB com base em métricas de importância sistêmica (tamanho, interconectividade, substituibilidade). ITUB4 carrega o maior surcharge do sistema brasileiro.

### Mecanismo de restrição automática (Capital Conservation Buffer)

Quando o CET1 cai dentro ou abaixo do colchão de conservação, o BCB aciona restrições **progressivas e automáticas** sobre distribuições:

| CET1 (acima do mínimo de 4,5%) | Restrição sobre distribuições |
|--------------------------------|------------------------------|
| 0-25% do colchão (0-0,625pp) | Retém 100% — proibido distribuir |
| 25-50% do colchão (0,625-1,25pp) | Retém ≥80% do LL ajustado |
| 50-75% do colchão (1,25-1,875pp) | Retém ≥60% do LL ajustado |
| 75-100% do colchão (1,875-2,5pp) | Retém ≥40% do LL ajustado |
| >100% do colchão (>2,5pp) | Sem restrição automática |

Na prática, para D-SIBs com surcharge adicional, o threshold de restrição total inclui o surcharge — um banco com surcharge de 2,0% só fica livre de restrições automáticas se CET1 > 4,5% + 2,5% + 2,0% = 9,0% de margem mínima. O que, somado ao piso de 4,5%, implica CET1 total > 9,0%+4,5% = não — a lógica é que o banco deve manter CET1 > mínimo+buffer+surcharge para distribuir livremente. Simplificando: abaixo de ~11,5% (para ITUB4), qualquer distribuição começa a ser restringida.

## Geração e Consumo de Capital

### Equação dinâmica do CET1

O CET1 de um trimestre para o próximo evolui segundo:

```
CET1(t) = CET1(t-1) + ΔCapital_Principal / RWA(t)

ΔCapital_Principal = LL_retido(t) - Deduções_regulatórias_novas(t)
LL_retido(t) = LL(t) × (1 - payout(t))

ΔRWA ≈ Carteira_nova(t) × RWA_density_média - Vencimentos × RWA_density + ΔRWA_mercado + ΔRWA_operacional
```

De forma simplificada, a variação do CET1 pode ser decomposta em:

```
ΔCET1 ≈ [LL_retido / RWA] - [Crescimento_carteira × RWA_density / RWA]
```

O primeiro termo é **geração orgânica de capital** (LL que fica no PL). O segundo é **consumo de capital** pelo crescimento da carteira. Se o banco cresce mais rápido do que gera capital, o CET1 cai; se cresce mais devagar, o CET1 sobe e o banco acumula excesso distribuível.

### Exemplo calibrado (ITUB4 referência)

| Variável | Valor referência |
|----------|-----------------|
| RWA | ~R$1,1T |
| LL 2026E | ~R$52,7B |
| Payout 2026E | ~55% |
| LL retido | ~R$52,7B × 45% ≈ R$23,7B |
| Crescimento carteira | ~8,5% × R$1,1T ≈ R$93,5B de carteira nova |
| RWA density média | ~65% (mix Itaú: imobiliário, consignado, atacado, varejo) |
| ΔRWA por carteira nova | ~R$93,5B × 65% ≈ R$60,8B |
| Efeito líquido CET1 | ~(R$23,7B - R$60,8B) / R$1,1T ≈ -3,4pp |

Esse cálculo bruto indica que o banco consome mais CET1 do que gera quando cresce a 8,5%. Na prática, o RWA de crédito não cresce 1:1 com a carteira (mix muda, provisões IFRS 9 podem reduzir exposição líquida) e o RWA operacional cresce mais devagar. O CET1 realizado tende a ficar estável ou levemente acima do projetado por essa simplificação.

## Pesos RWA por Produto de Crédito

O **RWA density** (consumo de capital por R$ de crédito concedido) varia substancialmente por produto — é o fator que torna o mix da carteira determinante para a geração de capital.

| Produto | RWA density | Raciocínio |
|---------|------------|-----------|
| TVM soberano (NTN-B, LFT) | ~0% | Risco de crédito zero (governo federal) |
| Crédito imobiliário (SFH) | ~35-50% | Garantia real + mitigadores SFH |
| Consignado (PF) | ~75% | Baixo risco, mas não tem garantia real |
| Crédito rural / Agro | ~75% | Apoio governamental, mas risco de safra |
| Capital de giro PJ (PMEs) | ~100% | Sem garantia, risco médio-alto |
| Grandes empresas / Atacado | ~100% | Exposição bruta sem mitigador de garantia |
| Cartão de crédito | ~100-150% | Maior risco; para alguns produtos, fator adicional |
| Crédito pessoal não-consignado | ~100% | Alto risco, sem garantia |
| Derivativos (mark-to-market) | variável | CVA + exposição potencial futura |

**Implicação para modelagem**: um banco que cresce principalmente em imobiliário e consignado consome **metade** do capital que um banco que cresce em capital de giro ou crédito pessoal — pelo mesmo R$ de carteira. Isso explica parcialmente por que o Itaú, com mix diversificado e alto peso em consignado, consegue crescer carteira de 8-10% sem destruir CET1.

### Regra prática para sensibilidade rápida

```
Para cada R$10B de nova carteira de crédito:
  - Se consignado/imobiliário: ~R$3,5-5B de RWA adicional → consume ~0,3-0,5pp de CET1
  - Se capital de giro/varejo: ~R$6-8B de RWA adicional → consume ~0,5-0,7pp de CET1
  - Se mix médio Itaú (~65%): ~R$6,5B de RWA adicional → consume ~0,6pp de CET1
```

## ITUB4 Específico

### Posição de capital 4T25

| Métrica | Valor | Interpretação |
|---------|-------|--------------|
| CET1 | 12,3% | Acima do mínimo efetivo (~11,5%); folga de ~80bps |
| CET1 mínimo efetivo | ~11,5% | Mínimo + conservação + surcharge D-SIB 2,0% |
| Folga acima do mínimo | ~80bps | Equivale a ~R$8,8B de capital excedente |
| Target implícito de gestão | ~12,0-12,5% | Management opera com ~50-100bps de buffer acima do regulatório |

A folga de ~80bps é confortável mas não excessiva — o banco não está acumulando capital de forma expressiva. O payout de 72% em 2025 (vs normal de 50-60%) foi possível exatamente porque o CET1 estava folgado: o banco distribuiu o excesso acima do target implícito em vez de deixá-lo acumular no balanço sem utilidade.

### Implicações para payout 2026

Com CET1 em 12,3% pós-distribuição extraordinária de 2025 e projeção de crescimento de carteira de ~8,5% em 2026:

```
Geração orgânica (LL retido a 45% payout) ≈ +~30bps de CET1
Consumo por crescimento de carteira (8,5% × R$1,1T × 65% density) ≈ -~35bps
Efeito líquido estimado ≈ -5bps por trimestre
```

Isso implica que com payout de ~55% o banco mantém CET1 aproximadamente estável em torno de 12,0-12,3%. Para distribuir mais (payout >60%), precisaria ou crescer menos ou ter LL acima do projetado. O payout 2026 de ~55% é consistente com o equilíbrio de capital.

### Geração orgânica de capital (referência anual 2026E)

```
LL projetado 2026E: R$52,7B
Payout 55%: distribui R$29,0B
LL retido: R$23,7B → aumenta PL em ~R$23,7B
RWA crescimento: ~R$60B adicional (8,5% × R$1,1T × 65% density)
Efeito CET1 líquido: (R$23,7B - R$60B × 12,3%*) / R$1,1T ≈ neutro
```
_(*) O efeito no CET1 = ΔPL / RWA - CET1_atual × ΔRWA / RWA. Simplificação: se RWA cresce 5,5% e LL retido cresce PL em ~R$23,7B sobre PL de ~R$135B (~17,6%), o PL cresce mais rápido que o RWA → CET1 levemente positivo._

## Conexão com Dividendos e Payout

### O "capital waterfall" bancário

O fluxo de uso do lucro líquido bancário segue uma hierarquia:

```
Lucro Líquido (LL)
  │
  ├─ (1) Retenção mínima para sustentar crescimento do RWA
  │       (crescimento_carteira × RWA_density / CET1_target)
  │
  ├─ (2) Retenção para manter CET1 ≥ target interno (buffer regulatório + gestão)
  │
  └─ (3) Excedente distribuível
          → Dividendos ordinários (payout "normal")
          → JCP (otimização tributária — ver [[aliquota_efetiva]])
          → Dividendos extraordinários (quando CET1 > target por folga acima de ~100bps)
          → Recompra de ações (alternativa a dividendos; eleva EPS, reduz PL, sobe ROE)
```

### Dinâmica de payout em diferentes cenários de CET1

| Cenário | CET1 | Sinal | Ação típica do management |
|---------|------|-------|--------------------------|
| CET1 muito folgado (>13,5%) | Excesso expressivo | Positivo/curto prazo | Dividendo extraordinário ou recompra agressiva |
| CET1 confortável (12-13%) | Equilíbrio | Neutro | Payout normal (50-60%), crescimento de carteira |
| CET1 no limite do target (~11,5-12%) | Pressionado | Vigilância | Payout reduzido (40-50%), gestão de RWA |
| CET1 abaixo do mínimo regulatório (<11,5%) | Crítico | Negativo | BCB restringe automaticamente distribuições; banco capta capital ou desacelera crescimento |

### JCP como mecanismo de otimização

O [[jcp]] (Juros sobre Capital Próprio) é a forma preferencial de distribuição dos grandes bancos porque é dedutível de IR/CSLL. Do ponto de vista do CET1, JCP e dividendos têm o mesmo efeito (ambos reduzem o PL), mas o JCP é fiscalmente mais eficiente para o banco — reduz o lucro tributável, gerando menor saída de caixa líquida para o mesmo volume de distribuição ao acionista.

```
Para o acionista: recebe JCP (tributado a 15% na fonte) OU dividendo (isento)
Para o banco: JCP reduz IR/CSLL (~34% de dedução) → custo líquido menor
Resultado: JCP maximiza distribuição total acionista dado um mesmo impacto no CET1
```

## Por Empresa

### [[itau]] — ITUB4

- **CET1 4T25**: 12,3% — confortável, ~80bps acima do mínimo efetivo
- **Target implícito**: ~12,0-12,5% (management opera com buffer ~50-100bps acima do regulatório)
- **Payout 2025**: ~72% (extraordinário — distribuiu excesso de capital acumulado em 2024-25)
- **Payout 2026 projetado**: ~55% (normalização — equilíbrio entre crescimento de RWA e geração orgânica)
- **Surcharge D-SIB**: 2,0% (maior do sistema — reflexo da importância sistêmica do Itaú)
- **Geração orgânica**: LL de R$52,7B retido a 45% ≈ R$23,7B/ano → sustenta crescimento de carteira de ~8,5% sem destruir CET1
- **Sensibilidade**: +1pp de crescimento de carteira acima do projetado consome ~R$7,2B de RWA adicional (65% density × R$11B de carteira), ou ~0,065pp de CET1

### [[bradesco]] — BBDC4

- **CET1 estimado 4T25**: ~11,5% (em recuperação pós-ciclo adverso 2022-23)
- **Surcharge D-SIB**: ~1,5%
- **Situação**: Em reconstrução de capital. O ciclo de inadimplência 2022-23 (Americanas, Light, PMEs) gerou provisões elevadas que deprimiram o LL e, portanto, o LL retido. Com normalização do [[custo_risco]] em 2025-26, o Bradesco reconstrói CET1 organicamente.
- **Implicação para payout**: Com CET1 próximo ao target mínimo, Bradesco tem menor flexibilidade para distribuições extraordinárias. O guidance implícito é payout mais contido (~40-50%) enquanto CET1 não atingir ~12,5%.
- **Diferença estrutural vs ITUB4**: O Bradesco consolida integralmente o Bradesco Seguros (vs Itaú que usa equity method para [[porto_seguro]]). Isso afeta o RWA (seguros têm RWA próprio) e o CET1 comparável — o CET1 do Bradesco incorpora o consumo de capital das operações de seguros integradas.

### Comparativo de reconstrução de capital

O contraste Itaú vs Bradesco é central para entender a diferença de valuation entre os dois:

| Dimensão | ITUB4 | BBDC4 |
|----------|-------|-------|
| CET1 (~4T25) | 12,3% — folgado | ~11,5% — no limite |
| Payout 2025 | 72% (distribuiu excesso) | ~40% (preservou capital) |
| ROE 2025 | ~23,4% | ~10-12% (em recuperação) |
| Fase do ciclo | Pico de geração + distribuição | Reconstrução de capital + ROE |
| Opcionalidade | Dividendos extraordinários | Re-rating quando CET1 normalizar |

O Bradesco é um caso clássico de **opcionalidade de capital**: quando o CET1 se normalizar para ~12,5% e o payout subir para ~50-60%, o múltiplo deve se comprimir (valuation sobe). O risco é que o processo de normalização demore mais do que o mercado espera, ou que o RWA cresça mais rápido do que o LL retido.

## Ver Também

- [[banking]] — contexto setorial (Basileia III, D-SIBs, estrutura DRE bancária)
- [[aliquota_efetiva]] — JCP e alíquota efetiva (dedução tributária que otimiza o capital waterfall)
- [[jcp]] — mecanismo de Juros sobre Capital Próprio
- [[crescimento_carteira]] — consumo de RWA pelo crescimento da carteira
- [[itau]] — empresa modelada (CET1 12,3%, payout 72% em 2025)
- [[bradesco]] — empresa em turnaround (reconstrução de CET1 pós-2022-23)
