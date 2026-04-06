---
type: conceito
source_quality: conceptual
aliases: [Índice de Eficiência, IE, Cost-to-Income Ratio, Eficiência Bancária, IE Ajustado]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/extraction/ITUB4_investment_memo.md
  - sectors/banking/companies/SANB11/outputs/model/SANB11_model.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
---

# Índice de Eficiência

O **índice de eficiência (IE)** mede quanto o banco gasta para gerar R$1 de receita. É o principal KPI de produtividade operacional dos bancos — quanto menor, mais eficiente. É a métrica mais diretamente controlável pela gestão e reflete a capacidade de escalar receita sem crescer custos proporcionalmente (**alavancagem operacional**).

## Definição e Fórmula

```
IE = Despesas_Operacionais / Receita_Total × 100%

onde:
  Despesas_Operacionais = Despesas de Pessoal + Despesas Administrativas + Outros
  Receita_Total = NII + Tarifas + Seguros + Outras_receitas_operacionais
```

**Leitura:** Um IE de 40% significa que o banco gasta R$0,40 para cada R$1,00 de receita gerada.

**Atenção a diferentes denominadores:** Alguns analistas calculam o IE sobre o NII apenas (excluindo fees); outros incluem o resultado de seguros; outros excluem amortização de intangíveis. Sempre especificar a base usada ao comparar bancos.

### IE Ajustado ao Risco

Uma versão mais completa ajusta o denominador pelo custo de crédito:

```
IE_ajustado = Despesas_Op. / (Receita_Total − Custo_de_Risco) × 100%
```

O IE ajustado captura melhor a eficiência "de verdade" — um banco que tem receitas altas mas alto custo de risco pode parecer eficiente no IE convencional mas ter pouco retorno líquido. Para o [[itau]], com custo de risco de ~3,7%, o IE ajustado é ~5pp maior que o IE reportado.

## No Contexto Brasileiro

**Range típico para grandes bancos (2024-2026):**
- Bancos privados tier-1: **38-45%** — melhor da América Latina
- Bancos públicos (BBAS3): 45-55% — pressão de mandato social
- Bancões LatAm (ex-BR): 50-60%
- Bancos digitais (Nubank) no início: >80% (ainda construindo escala)

**Por que bancos brasileiros são eficientes?**
1. **Escala absoluta**: ITUB4 e BBDC4 têm base de clientes de 90-100M pessoas
2. **Digitalização avançada**: Migração de transações para canais digitais acelerou no Brasil
3. **Oligopólio estrutural**: Concentração bancária preserva pricing power, sustentando receitas altas com custos razoáveis
4. **Automação elevada**: Brasil foi pioneer em automação bancária nos anos 1990 por necessidade (inflação elevada criava demanda por processos rápidos)

## Por Empresa

| Empresa | IE (2025) | Meta | Nota |
|---------|----------|------|------|
| [[itau]] (ITUB4) | ~39-40% | ~39% (guidance) | Best-in-class Brazil; alavancagem operacional positiva (~+5pp receita vs +3pp custo YoY) |
| [[bradesco]] (BBDC4) | ~43-45% | ~40% (meta 2026-27) | Turnaround em andamento; maior em pessoal e TI legado |
| [[sanb11]] (SANB11) | ~47-50% | ~45% (meta médio prazo) | Em processo de recuperação de IE; pressão de custos de TI e pessoal ainda elevada |

### Itaú: Como Sustenta IE de 39%?

O IE baixo do Itaú reflete:
- **Digitalização avançada**: >90% das transações em canais digitais (sem agência)
- **Iti e Ion**: Plataformas digitais com custo unitário marginal muito baixo
- **Receitas de tarifas crescendo mais rápido que custos**: [[receita_servicos_tarifas]] cresce ~8-10% a.a.; custos operacionais crescem ~4-6% a.a.
- **Mix de clientes de alta renda**: Personalité e Private têm receita por cliente muito maior com custo incremental pequeno

### Santander Brasil: Recuperação de IE

O [[sanb11]] partiu de IE elevado (~49-51% em 2023-2024) em função de:
- **Programa Gravity**: investimentos pesados em migração para cloud (~R$400M/ano) que elevam custo no curto prazo mas devem gerar savings estruturais
- **Rede de agências**: base de agências ainda maior do que o volume de negócios justificaria, com racionalização em andamento
- **Headcount**: quadro de pessoal em ajuste; salários bancários corrigidos pelo dissídio anual

Modelo SANB11 (premissas calibradas): IE implícito ~48% em 2025 → trajetória de queda para ~46% em 2026-2027E, com alavancagem operacional positiva conforme receitas crescem (NIM 11,5%, NII Mercado +250M/tri) acima dos custos.

A meta do management Santander Brasil não é explicitamente divulgada como IE, mas a retomada de ROE para 20% (meta interna) implica IE abaixo de 45%.

### Bradesco: Plano de Convergência

O [[bradesco]] tem IE ~4-6pp acima do Itaú. O gap reflete:
1. **Rede física maior**: Mais agências = mais pessoal e custos fixos
2. **TI legado**: Sistemas mais antigos = maiores custos de manutenção
3. **Investimentos de transição**: Modernização exige Capex antes de gerar savings

O plano de turnaround do Bradesco (management novo desde 2024) mira IE ~40% no médio prazo via:
- Racionalização de agências (redução gradual)
- Renegociação de contratos de TI
- Recomposição de mix para produtos de maior margem (receitas crescem mais rápido que custos)

## Alavancagem Operacional

O conceito central ligado ao IE é a **alavancagem operacional**: receitas crescendo mais rápido que custos → IE cai → margem operacional expande.

```
Alavancagem_Operacional > 0  ⟺  g_Receita > g_Custos

Efeito_IE = IE(t-1) × (1 - g_Custos/g_Receita)
```

Para o Itaú 2025: receitas cresceram ~12% YoY; custos cresceram ~6% YoY → alavancagem operacional positiva de ~6pp → IE comprimiu ~2pp no período.

### Guidances Típicos

O management do Itaú tipicamente guia com "crescimento de receita acima do crescimento de custos" sem dar IE explícito. Na prática:
- Receitas: +9-12% a.a. (NII + fees)
- Custos: +4-7% a.a. (inflação + crescimento controlado)
- Delta: +3-5pp de alavancagem operacional

## Modelagem do IE

No modelo de banking, o IE aparece como verificação de sanidade, não como premissa direta. A modelagem é bottom-up:

```
1. Projetar receitas (NII, fees, seguros) → YoY histórico/guidance
2. Projetar despesas operacionais → YoY histórico + fator de eficiência
3. Calcular IE implícito = Despesas / Receitas
4. Verificar vs histórico e guidance — desvio > 2pp exige justificativa
```

**Premissa razoável para ITUB4 2026-2027:** IE ~39-40% (estável em relação a 2025). Qualquer projeção abaixo de 38% (acima do guidance) requer premissa explícita de evento extraordinário (ex: reestruturação de custo).

## Alavancagem Operacional por Cenário

Para modelagem 2026-2027, a alavancagem operacional dos três bancos cobertos implica:

| Banco | g_Receitas 26E | g_Custos 26E | Delta IE | IE implícito |
|-------|---------------|-------------|----------|--------------|
| [[itau]] | ~+11-12% | ~+6-7% | ~-2pp | ~39% |
| [[bradesco]] | ~+10-13% | ~+7-9% | ~-1 a -2pp | ~43% |
| [[sanb11]] | ~+10-14% | ~+6-8% | ~-1 a -2pp | ~47% |

O Santander tem o maior potencial de melhora absoluta de IE mas parte de um nível mais alto — o efeito de alavancagem operacional é similar em tamanho mas o ponto de chegada ainda fica acima dos peers privados.

## Ver Também

- [[eficiencia_operacional]] — página principal sobre o tema com modelagem detalhada
- [[banking]] — DRE bancária e contexto setorial
- [[roe_bancario]] — IE é um dos cinco drivers estruturais do ROE
- [[itau]] — perfil ITUB4; IE best-in-class como moat competitivo
- [[bradesco]] — turnaround em eficiência como alavanca de ROE
- [[sanb11]] — perfil SANB11; IE em recuperação como alavanca de ROE
- [[receita_servicos_tarifas]] — componente de receita que cresce sem custo proporcional
- [[plr_bancario]] — componente de custo de pessoal que varia com o resultado
