---
type: conceito
source_quality: conceptual
aliases: [ROE, Return on Equity, Retorno sobre Patrimônio Líquido]
sources:
  - sectors/banking/sector_profile.md
  - wiki/roe_bancario.md
  - sectors/real_estate/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
updated: 2026-04-05
---

# ROE (Return on Equity)

O **ROE (Return on Equity)** é a razão entre o lucro líquido e o patrimônio líquido médio da empresa. É a métrica primária de rentabilidade para acionistas — mede quanto o negócio gera de retorno para cada real de capital próprio investido.

```
ROE = Lucro_Líquido / PL_Médio × 100%
```

## Interpretação

| ROE | Leitura |
|-----|---------|
| ROE > Ke (custo de capital) | Empresa cria valor econômico — vale acima do patrimônio contábil |
| ROE = Ke | Empresa preserva valor — vale exatamente o patrimônio contábil |
| ROE < Ke | Empresa destrói valor — vale menos do que o patrimônio contábil |

**Ke** (custo do capital próprio) é o retorno mínimo exigido pelo acionista dado o risco do negócio. Para empresas brasileiras, Ke típico é 12-16% a.a. (varia por setor e ciclo de Selic).

## ROE no Setor Bancário

Para bancos, o ROE é o KPI de rentabilidade central. A estrutura bancária — alta alavancagem de balanço (Ativos/PL de ~10×) — faz com que um ROA modesto (~1-3%) se transforme em ROE alto (10-25%+). Ver [[roe_bancario]] para análise detalhada com DuPont, sensibilidades e valuation P/BV.

**Range de ROE para grandes bancos brasileiros (2025):**

| Banco | ROE 2025 |
|-------|---------|
| [[itau]] (ITUB4) | ~23-24% |
| Banco do Brasil (BBAS3) | ~20-21% |
| [[bradesco]] (BBDC4) | ~12-14% (turnaround) |

## ROE nas Incorporadoras

Para [[incorporadoras]] brasileiras, o ROE é menos utilizado como KPI primário (EBIT e margem bruta são preferidos), mas é relevante para avaliação de criação de valor:

**Characteristics do ROE para incorporadoras:**
- Mais volátil que banking por ciclo de lançamentos (ROE pode variar muito entre anos)
- Alavancagem financeira menor que banking (D/E de ~0,3-0,8× vs ~9-10× em bancos)
- Impacto relevante de [[equivalencia_patrimonial]] (investidas) para empresas como [[cyrela]]

**Range de ROE para incorporadoras brasileiras (2025):**

| Empresa | ROE 2025 |
|---------|---------|
| [[cury]] | ~30-35% (retorno elevado, baixa imobilização) |
| [[cyrela]] | ~15-20% (capital maior, EP relevante) |
| [[direcional]] | ~20-25% |
| [[tenda]] | ~15-20% |

## Decompondo o ROE (DuPont)

```
ROE = Margem_Líquida × Giro_do_Ativo × Multiplicador_de_Capital

onde:
  Margem_Líquida    = LL / Receita
  Giro_do_Ativo     = Receita / Ativos
  Multiplicador     = Ativos / PL
```

**Para bancos:** O multiplicador domina (~10×), tornando o ROA o fator limitante.
**Para incorporadoras:** Giro do ativo e margem são mais balanceados.

## Armadilhas Comuns

### 1. PL Médio vs PL Final

Usar o PL final (em vez do médio) inflá o ROE quando a empresa distribui muito dividendo durante o ano, reduzindo o PL final. A média aritmética (início + fim) / 2 é o padrão correto.

### 2. PL com Goodwill / Intangíveis

Muitos analistas calculam ROE **excluindo goodwill e intangíveis** do PL (ROTE — Return on Tangible Equity). Para bancos com M&A histórico (Itaú-Unibanco, Bradesco-HSBC), o PL tangível é bem menor que o PL total, inflando o ROTE vs ROE. Sempre especificar qual base.

### 3. ROE Recorrente vs Reportado

Itens não-recorrentes (reestruturações, vendas de ativos, reversão de provisões) inflam ou deflam o LL de um trimestre. O **ROE recorrente** expurga esses efeitos e é a base relevante para valuation.

```
ROE_recorrente = LL_recorrente / PL_médio
LL_recorrente  = LL_reportado ± ajustes_não_recorrentes
```

## ROE vs P/BV (Valuation)

O ROE é a alavanca central do múltiplo **P/BV (Price-to-Book Value)**, especialmente para bancos:

```
P/BV_justo = (ROE − g) / (Ke − g)
```

Ver [[roe_bancario]] para a tabela completa de sensibilidade P/BV × ROE × Ke.

## ROE e Criação de Valor: O Critério do Ke

O ROE só cria valor quando supera o custo de capital próprio (**Ke**):

```
Valor_Criado ∝ (ROE − Ke) × PL

Se ROE > Ke: empresa vale MAIS que o patrimônio contábil (P/BV > 1×)
Se ROE = Ke: empresa vale EXATAMENTE o patrimônio contábil (P/BV = 1×)
Se ROE < Ke: empresa vale MENOS que o patrimônio contábil (P/BV < 1×)
```

**Ke estimado por setor (Brasil, 2026):**
- Bancos: ~13-15% (risco macro + regulatório)
- Incorporadoras: ~14-16% (risco operacional + ciclo imobiliário)
- Empresas industriais: ~12-14%

**Por que bancos brasileiros têm P/BV > 1×:** [[itau]] com ROE ~23-24% vs Ke ~14% → P/BV justo de ~2,7× (modelo Gordon Growth). Ver [[roe_bancario]] para a tabela completa.

## ROE Histórico: Referências do Universo Coberto

| Empresa | Setor | ROE 2026E | Nota |
|---------|-------|----------|------|
| [[cury]] | RE/Incorporadora | ~61% | Excepcional; sem minorities, sem landbank especulativo |
| [[direcional]] | RE/Incorporadora | ~38,7% | Alto; landbank barato + Riva escalando |
| [[tenda]] | RE/Incorporadora | ~37,9% | Alto; RET baixo + ciclo MCMV favorável |
| [[cyrela]] | RE/Incorporadora | ~17,7% | Menor por PL elevado e EP exógena |
| [[itau]] | Banking | ~23-24% | Best-in-class banking; sustentado por IE ~39% |
| [[bradesco]] | Banking | ~12-14% | Turnaround; meta ~20% médio prazo |

**Observação sobre incorporadoras com ROE alto:** ROE > 30% é sustentável apenas enquanto o PL for baixo em relação ao lucro. Se a empresa retiver lucros sem crescer o negócio, o PL cresce, o ROE comprime. A melhor empresa MCMV puro terá ROE comprimindo naturalmente de 60% para 30-40% à medida que escala e o PL se acumula.

## Ver Também

- [[roe_bancario]] — análise completa do ROE bancário, DuPont, P/BV, drivers e sensibilidades
- [[ll]] — Lucro Líquido; numerador do ROE
- [[banking]] — sector onde ROE é o KPI primário; framework DuPont completo
- [[incorporadoras]] — sector onde EBIT/margem bruta é primário; ROE secundário mas relevante
- [[cet1]] — para bancos, CET1 define o denominador mínimo (PL regulatório)
- [[equivalencia_patrimonial]] — EP exógena impacta o LL e, portanto, o ROE das incorporadoras
- [[aliquota_efetiva]] — impacta o LL via impostos → afeta ROE; JCP reduz alíquota bancária
- [[jcp]] — reduz impostos → aumenta LL → aumenta ROE (para bancos com PL grande)
- [[cury]] — ROE ~61%; referência de ROE excepcional por eficiência estrutural
- [[itau]] — ROE ~24%; referência bancária best-in-class no Brasil
