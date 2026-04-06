---
type: conceito
source_quality: conceptual
aliases: [VSO, Velocidade de Vendas, Velocidade de Vendas Sobre Oferta, Sales Over Supply]
sources:
  - sectors/real_estate/sector_profile.md
  - sectors/real_estate/companies/CYRE3/outputs/decomposition/CYRE3_dependency_graph_v3.json
  - sectors/real_estate/companies/CURY3/outputs/decomposition/CURY3_dependency_graph_v3.json
  - sectors/real_estate/companies/DIRR3/outputs/decomposition/DIRR3_dependency_graph_v3.json
  - sectors/real_estate/companies/TEND3/outputs/decomposition/TEND3_dependency_graph_v3.json
updated: 2026-04-05
---

# VSO — Velocidade de Vendas Sobre Oferta

O **VSO (Velocidade de Vendas Sobre Oferta)** é a principal métrica de demanda e precificação no setor de [[incorporadoras]]. Mede a velocidade com que o estoque disponível é absorvido pelo mercado em um determinado período.

## Fórmula

```
VSO(t) = Vendas_contratadas(t) / (Estoque_início(t) + Lançamentos(t))
```

Ou equivalentemente:

```
VSO(t) = VGV_vendido(t) / (VGV_oferta_início(t) + VGV_lançado(t))
```

Onde "oferta" = unidades disponíveis para venda = estoque de unidades não vendidas + novas unidades lançadas no período.

## Interpretação

| VSO Trimestral | Sinal | Contexto |
|----------------|-------|---------|
| > 40% | Muito forte | Demanda aquecida; pricing power; pode acelerar lançamentos |
| 30–40% | Saudável | Mercado em equilíbrio; reposição normal |
| 20–30% | Moderado | Absorção razoável; monitorar estoque |
| < 20% | Fraco | Demanda fraca ou oferta excessiva; pressão de desconto |

**Nota:** O nível "saudável" varia por segmento. MCMV puro ([[cury]]) opera com VSO ~44% — acima do que seria normal para alta-renda porque os ciclos são mais curtos e a demanda reprimida é maior.

## VSO na Projeção de Receita

O VSO é o elo entre VGV lançado e o backlog:

```
Vendas_novas(t) = VGV_lançado(t) × VSO(t)  →  alimenta Backlog  →  via POC  →  Receita
```

VSO é **input exógeno** no modelo — calibrado por backtest e ajustado pelo analista com base em:
1. Guidance da gestão ("VSO saudável ~25%", "meta 44%")
2. Dados setoriais (Secovi-SP histórico — usado como sanity check, não como input futuro)
3. Contexto macro: ciclo de [[selic]], desemprego, renda disponível
4. Mix de produto: MCMV tem maior demanda estrutural; alta-renda é mais sensível a juros

## Sazonalidade

VSO é afetado pela sazonalidade de lançamentos:
- **1T:** Menor (menos lançamentos, menos exposição ao mercado)
- **2T e 4T:** Maior (pico de feiras de imóveis; mais lançamentos = mais oferta = mais vendas absolutas)

O POC sazonal captura parte desse padrão indiretamente. O analista deve usar VSO consistente com a sazonalidade histórica por trimestre.

## VSO por Empresa

| Empresa | VSO Típico/tri | Drivers |
|---------|---------------|---------|
| [[cury]] | ~43-44% | MCMV puro, formas de alumínio, tickets pequenos, demanda reprimida SP/RJ |
| [[direcional]] | ~23-25% | Mix econômico + Riva (médio-alto); landbank diversificado |
| [[cyrela]] | ~18-22% | Alta-renda + Vivaz; projetos maiores, ciclo de vendas mais longo |

## VSO vs VGV % Cia

Na projeção do backlog, o que importa é o **VGV 100%** das vendas, não o VGV % Cia. Ver [[vgv_lancamentos]] para a convenção crítica de 100% consolidado.

## Sensibilidades

| Variável | Impacto no VSO |
|----------|---------------|
| Selic sobe +2pp | VSO cai 1-3pp (crédito mais caro, demanda alta-renda recua) |
| [[mcmv]] teto sobe | VSO MCMV sobe (mais compradores elegíveis) |
| Alvarás SP atrasados | VSO aparentemente alto (menos oferta lançada, mesma demanda) |
| Estoque pronto elevado | Pressão de desconto → pode temporariamente reduzir VSO |

## Relação com Outros Indicadores

- **VSO alto + VGV lançado crescendo** → backlog acelera → receita futura sobe
- **VSO alto + VGV lançado flat** → estoque esgota rápido → empresa precisa lançar mais
- **VSO baixo + VGV lançado caindo** → empresa segura lançamentos → backlog cai → receita futura cai

## VSO e Secovi-SP

O Secovi-SP publica dados mensais de VSO por segmento para São Paulo. **Regra de uso:** dados do Secovi são **históricos** — usados como sanity check de market share (~12% ±1pp para Cyrela no segmento SP alta-renda), não como input direto de projeção. Não existe Secovi futuro.

## VSO Ajustado: Distorções a Monitorar

O VSO reportado pode ser distorcido em certas situações:

| Distorção | Causa | Correção |
|-----------|-------|---------|
| VSO artificialmente alto | Empresa reduziu muito os lançamentos → denominador pequeno → mesmo nível de vendas = VSO alto | Analisar VGV vendido absoluto, não só VSO |
| VSO artificialmente baixo | Empresa lançou muito em um trimestre → denominador grande → vendas normais = VSO baixo | Normalizar pelo VGV lançado acumulado |
| Distratos não-líquidos | Alguns relatórios mostram VSO bruto (antes de cancelamentos); cancela VSO pode ser bem menor | Verificar nota de metodologia no release |

**Regra prática:** O VGV vendido absoluto (R$M) é mais estável e comparável do que o VSO percentual. O VSO pode variar muito entre trimestres simplesmente por mudanças no denominador (lançamentos).

## VSO e Affordability: A Demanda Real

A demanda por imóveis depende de:

```
Affordability = (Preço_imóvel / Renda_mensal) × (Prestação / Renda)
```

Para [[mcmv]]: o teto de preço e a taxa de juros subsidiada garantem affordability estável, explicando o VSO mais alto e menos sensível a ciclos de Selic.

Para alto padrão ([[cyrela]]): affordability depende de Selic (custo de financiamento), percepção de valorização e renda da classe A/B. VSO mais sensível a ciclos de mercado.

### Exemplo de Sensibilidade (Alto Padrão)

Um imóvel de R$600k com financiamento SBPE:
- **Selic 10%:** Taxa de financiamento ~10-11% a.a. → Prestação ~R$5.500/mês → comprometimento de renda ~25% (renda de R$22k)
- **Selic 14%:** Taxa de financiamento ~13-14% a.a. → Prestação ~R$6.800/mês → comprometimento de renda ~31% (mesmo perfil) → demanda recua

Para MCMV, o financiamento é via FGTS a taxa fixa (5-8%), então a Selic de mercado é irrelevante para a prestação.

## VSO no Modelo: Calibração e Backtest

O VSO é calibrado por backtest trimestre a trimestre, com meta de erro de receita < 8%:

```
Iteração 1: VSO mecânico = média histórica → calcula receita implícita → compara vs histórico
Iteração 2: Ajusta VSO para minimizar erro → resultado ~MAPE 5-8%
Iteração 3: Ajuste fino + guidance management + contexto macro
```

**Por que o VSO do modelo pode diferir do reportado:** O modelo usa VSO 100% (sobre o VGV 100%), enquanto alguns releases reportam VSO % Cia. Sempre verificar a metodologia do release antes de comparar.

## Benchmarks de VSO por Empresa (Modelo Calibrado)

| Empresa | VSO/tri (model) | Fonte | Notas |
|---------|----------------|-------|-------|
| [[cury]] | ~44% | Decisões calibradas 2026 | Patamar confirmado management "44%"; MCMV puro |
| [[direcional]] | ~23-25% | Backtest | Mix MCMV + Riva; VSO Riva menor |
| [[tenda]] | ~25,8% | Index TEND3 | TENDA principal; Alea ~30,7% (menor base) |
| [[cyrela]] | ~18-22% | Estimativa | Alta-renda; variância alta por projeto |

## Ver Também

- [[vgv_lancamentos]] — volume de oferta que entra no denominador do VSO
- [[margem_backlog]] — margem da carteira gerada pelas vendas
- [[poc_revenue]] — conversão do backlog em receita
- [[incorporadoras]] — hub setorial
- [[mcmv]] — programa que impacta demanda e affordability
- [[selic]] — driver macro de demanda imobiliária (mais relevante para alto padrão)
- [[incc]] — custo durante a obra; indiretamente afeta viabilidade de novos lançamentos
- [[capital_de_giro]] — VSO alto = backlog grande = mais capital de giro necessário
