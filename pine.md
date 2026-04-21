---
type: entity
aliases:
  - PINE4
  - Banco Pine
sources:
  - sources/digested/notion_capstone_pine_2ea00ca3_summary.md
  - sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md
created: 2026-04-20
updated: 2026-04-20
---

# Banco Pine (PINE4)

Banco de médio porte com base histórica em [[consignado]] público federal e municipal. Desde 2025 executa uma pivot estratégica para o consignado privado (desconto em folha no setor privado), buscando elevar a representatividade desse produto na carteira total.

---

## Estratégia — Pivot para Consignado Privado

Pine vinha com carteira concentrada em consignado público federal e municipal e iniciou preparação para o consignado privado antes de 2026 (fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md).

Em 2025, consignado privado + cartão consignável representavam **22% do total de ativos**. A meta declarada é elevar essa participação para **40%** (fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md).

---

## Produto de Consignado Privado

**Critérios de elegibilidade (definidos internamente):**
- Tomador: CLTista com ≥ 2 anos de emprego no mesmo vínculo
- Empregador: CNPJ com > 5 anos de existência

(fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md)

**Pricing e risco de crédito:**

| Parâmetro | Valor |
|-----------|-------|
| Taxa de operação | 4,5% a 5,5% (base não especificada) |
| Perda esperada (fase inicial) | ~5% |
| Perda esperada (estado estacionário) | ~10% (ceteris paribus) |

(fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md)

O guideline de 5% → 10% reflete consciência de que o risco de crédito do consignado privado é estruturalmente maior que o público — onde o desconto em folha de servidor torna a inadimplência quase nula.

---

## Funding e Capital

- Estrutura de funding via **LF Sênior** (Letra Financeira Sênior) (fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md).
- Corpobans (comitê interno) alinhado na simulação de uma **cota subordinada** para o produto de consignado privado (fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md).
- **Ponto de atenção regulatório:** em junho de 2026 entram em vigor regras mais rígidas do FGC para bancos menores. Pine está enquadrado nessa nova regra — relevante acompanhar se a estrutura atual de LF Sênior é suficiente para o crescimento projetado (fonte: sources/digested/notion_capstone_pine_2ea00ca3_summary.md).

---

## Contexto de Mercado — Consignado Privado

*Dados de mercado colhidos via BMP (Maria do Socorro), referência relevante para calibrar expectativas do produto em que Pine está crescendo.*

- Inadimplência inicial de mercado: **~30%**, atribuída à falta de análise do perfil do empregador nos estágios iniciais (fonte: sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md).
- Após curva de aprendizado (foco na seleção do empregador), inadimplência de mercado migrou para faixa de **15%–18%** — ainda não estabilizada (fonte: sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md).
- Risco específico do produto: **carência de 60 dias** atrasa detecção de inadimplência pós-demissão; desemprego demora ~90 dias para aparecer no crédito (fonte: sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md).
- Bancos grandes estão expandindo presença no segmento onde já têm a folha de pagamento — pressão competitiva crescente (fonte: sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md).
- Produto já é considerado rentável pelo mercado (fonte: sources/digested/notion_consignado_privado_bmp_maria_do_socorro_2fd00ca3_summary.md).

Os critérios de elegibilidade de Pine (CLT ≥ 2 anos + CNPJ > 5 anos) alinham-se com o aprendizado de mercado: selecionar empregadores estáveis é o principal driver de inadimplência controlada.

---

## Demonstrações Financeiras

Dados de balanço, DRE e indicadores de rentabilidade (ROE, NIM, índice de inadimplência própria) não disponíveis nas fontes atuais. Ver `sources/manifests/pine.json` para cobertura futura.

---

## Pontos de Atenção

1. **Prazo regulatório FGC (jun/2026):** nova regra de funding para bancos menores pode exigir captação adicional ou ajuste de mix.
2. **Inadimplência do consignado privado:** meta de 10% é o teto declarado — mercado ainda está acima disso (15%–18%). Seleção rigorosa de empregadores é o mecanismo de controle.
3. **Concentração de pivot:** elevar de 22% → 40% em prazo curto implica risco de execução e de originação em produto ainda em maturação.
4. **Taxa não especificada em base:** 4,5%–5,5% sem indicação se a.m. ou a.a. — verificar em resultados futuros.
5. **Competição de grandes bancos:** entrantes com custo de funding menor e base de folha instalada podem comprimir margens.
