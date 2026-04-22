---
type: concept
aliases:
  - section_232_tariffs_us
  - tarifas_metais_eua
sources:
  - sources/digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md
created: 2026-04-22
updated: 2026-04-22
---

# Section 232 (tarifas de metais — EUA)

## Definição

**Section 232** é o dispositivo do *Trade Expansion Act of 1962* dos EUA que autoriza o Presidente a impor tarifas a importações por motivo de segurança nacional. Na prática recente, virou o guarda-chuva legal das tarifas sobre **aço, alumínio, cobre e derivados** aplicadas pelo governo americano desde 2018, com revisão material em 06/04/2026 que redefiniu base de cálculo, alíquotas e perímetro (fonte: digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md).

## Revisão de abril/2026 — antes × depois

| Característica | Antes | Depois de 06/04/2026 |
|---|---|---|
| Base de cálculo | % sobre o conteúdo metálico em valor | % sobre o **valor aduaneiro total** do produto |
| Metais brutos | 50% sobre o metal | 50% sobre o valor total |
| Derivados (bens finalizados) | 50% só sobre o metal | **25% sobre valor total** |
| Equipamento de grid elétrico | 50% sobre conteúdo | **15% temporário até 31/12/2027** |
| Metal de origem US | Isento | 10% |
| Baixo conteúdo metálico | Tarifado | **Isento se ≤15% do peso** |

(fonte: digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md)

Três mudanças estruturais:

1. Critério gatilho passou de **% valor → % peso** — se o metal representa ≥15% do peso, a tarifa incide sobre o valor total do produto.
2. A **Section 122** (10% não-aço, sucessora do IEEPA) **não empilha** sobre a 232 — evita dupla tarifação.
3. A tarifa 232 sobre **veículos comerciais** (vigente desde Nov/25) **prevalece** sobre a de metais — neutraliza o hit para OEMs de caminhões classe 8.

## Impacto setorial em Bill of Materials (base BoM = $100)

| Setor | Anualizado | Pro-rata 2026 (pós-1T + colchão de estoque) |
|---|---|---|
| Construção & Agro | **+6%** (headwind) | +3% |
| Caminhões Classe 8 | 0% (neutro) | 0% |
| Equipamento Elétrico | **−17%** (tailwind) | −8% |

Premissas: construção/agro assume 20% aço no BoM; caminhões 20% aço mas coberto pelo 232 setorial; elétricos 10% aço + 60% cobre + 30% não-metal (ex: *switchgear*). (fonte: digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md)

## Framework de 4 fatores para exposição empresa-específica

Bernstein propõe decompor a exposição de qualquer OEM americano por:

1. **% da receita US vinda de importados** (denominador direto do hit).
2. **Já coberto por 232 setorial próprio?** (caminhões sim → insulados via primazia MHDV).
3. **Método de contabilização de estoque** — LIFO reconhece o custo mais rápido que FIFO, acelerando o hit no P&L.
4. **% de importações do setor** — quanto mais concorrentes importam, maior o guarda-chuva de preço disponível ao produtor doméstico.

Benchmarks setoriais de % importações (fonte: digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md):

- Elétrico: 58% · Construção: 41% · Caminhão: 35% · Motores: 34% · Agro: 24% · Mineração/O&G: 16%

## Guias tarifárias das empresas US para 2026 (reportadas no 4T25)

| Ticker | $ Tarifa | % Receita | Hit EPS ($) | % EPS |
|---|---|---|---|---|
| AGCO | $110M | 1% | $1,02 | 17% |
| CAT | $2.600M | 4% | $4,30 | 19% |
| CMI | $178M | 0% | $0,98 | 4% |
| DE | $1.200M | 3% | $3,29 | 18% |
| ETN | $613M | 2% | $1,30 | 10% |
| HUBB | $150M | 2% | $2,19 | 11% |
| OSK | $200M | 2% | $2,41 | 22% |
| PCAR | $75M | 0% | $0,11 | 2% |

(fonte: digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md)

## Ranking de exposição (melhor → pior)

1. **ETN, HUBB** (verde) — elétricos beneficiários, tarifa de 50% → 15%.
2. **PCAR** (neutro) — caminhões insulados pela primazia MHDV; 90%+ fabricação doméstica adiciona upside.
3. **CMI** (levemente negativo) — pode melhorar se motores de caminhão entrarem no guarda-chuva MHDV.
4. **CAT, DE, AGCO, OSK** (vermelho) — construção/agro mais impactados; ordem interna OSK > AGCO > DE > CAT.
5. **URI, LGN, J, PWR** — alternativa defensiva via prestadores de serviço (sem exposição de BoM).

(fonte: digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md)

## Relevância para o universo brasileiro

Nenhum dos tickers cobertos no relatório é brasileiro — a página vive aqui como **nota macro/setorial** sobre regime tarifário US e como **template de framework** para análise de exposição tarifária, potencialmente reaplicável a:

- Exportadoras brasileiras com venda direta aos EUA (aço, máquinas, autopeças).
- Setores onde o preço doméstico US se descola por conta de tarifa e pode puxar preços globais de cobre/aço.
- Empresas com unidades fabris nos EUA que importam insumos tarifados.

Reforma tributária doméstica e regime tarifário US operam em camadas distintas — ver [[reforma_tributaria]] para contexto brasileiro.

## Fontes

- Bernstein — *Machinery & Electricals: The Section 232 metals tariff changes — winners and losers* (Chad Dillard, 16/04/2026). Digerido em `sources/digested/Bernstein Machinery & Electricals The Section 232 metals tariff c_summary.md`.
