---
type: conceito
source_quality: conceptual
aliases: [Consignado Privado CLT, Private Payroll Loans, Consignado CLT]
sources:
  - sectors/banking/sector_profile.md
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/SANB11/outputs/decomposition/SANB11_dependency_graph_v3.json
  - sectors/banking/companies/BBDC4/outputs/decomposition/BBDC4_dependency_graph_v3.json
updated: 2026-04-05
---

# Consignado Privado CLT

O **consignado privado CLT** é uma modalidade de crédito com desconto automático em folha de pagamento para trabalhadores do setor privado com carteira assinada (CLT). Regulamentado em 2024 pelo Governo Federal, é o produto de maior crescimento estrutural para o setor bancário brasileiro em 2026-2028. O desconto na fonte praticamente elimina o risco de inadimplência, permitindo taxas significativamente menores que o crédito pessoal convencional.

## Como Funciona

O empregador conveniado autoriza o banco a debitar a parcela diretamente na folha de pagamento antes que o salário seja creditado ao empregado:

```
Parcela máxima = 35% do salário líquido
Taxa típica    = ~2,0-2,8% a.m. (vs ~5-8% a.m. do crédito pessoal)
Prazo          = até 96 meses
Inadimplência  = muito baixa (desconto na fonte)
```

O risco principal não é de inadimplência, mas de **demissão** (o trabalhador perde o emprego e o desconto automático cessa). Por isso, a exposição é calibrada ao histórico de rotatividade do setor do empregador.

### Diferença do Consignado Público

| Aspecto | Consignado Público (INSS/servidor) | Consignado Privado CLT |
|---------|-----------------------------------|------------------------|
| Público | Aposentados INSS, servidores | Trabalhadores CLT |
| Risco de desligamento | Baixíssimo (aposentado / estável) | Médio (rotatividade CLT) |
| Taxa | ~1,5-1,8% a.m. | ~2,0-2,8% a.m. |
| Margem consignável | 35% do benefício | 35% do salário |
| Regulamentação | Anterior a 2004 | 2024 (novo) |

## No Contexto Brasileiro

- **MP 1282/2024** regulamentou o produto. O ecossistema de convênios empregador-banco levou ~12 meses para amadurecer.
- Em **jan/26**: Itaú originou R$1,9B (vs R$1,3B em dez/25) — curva de adoção acelerada.
- Potencial de mercado estimado: ~R$250-300B de carteira estrutural (vs ~R$15-20B hoje).
- Bancos grandes têm vantagem competitiva via rede de convênios com grandes empregadores.
- Fintechs (iFood, C6, Nubank) também competem, mas grandes bancos têm relacionamento com o empregador.
- **Impacto no modelo**: [[crescimento_carteira]] acima do PIB nos próximos 3-4 anos. [[custo_risco]] baixo (~1-2% a.a.) por conta do desconto automático.

## Por Empresa

| Empresa | Característica |
|---------|----------------|
| [[itau]] | R$1,9B originados em jan/26 (+46% vs dez/25). Foco em grandes empregadores. Produto estratégico no guidance de [[crescimento_carteira]] 2026. Impacto ainda pequeno no estoque total da carteira (~R$10-15B), mas crescendo rapidamente. |
| [[bradesco]] | Também presente, mas dados menos detalhados no release 4T25. |

## Runway e TAM

O produto está em estágio inicial de adoção — muito início de curva em relação ao potencial estrutural.

### Estimativa do TAM

```
Trabalhadores CLT formais no Brasil   ~40M
Salário médio CLT                     ~R$3.500/mês
Margem consignável (35%)              ~R$1.225/mês
% que tomaria empréstimo (estimado)   ~40-50%
Prazo médio                           ~60 meses
TAM estrutural (estimado)             ~R$250-300B de carteira
```

### Estágio Atual vs Benchmark de Maturidade

| Referência | Carteira (estimado) |
|------------|---------------------|
| Consignado INSS (maduro) | ~R$700B+ |
| Consignado Privado CLT (2025) | ~R$15-20B |
| Consignado Privado CLT como % do TAM | ~5-8% |

O consignado INSS levou ~15 anos para atingir R$700B. O consignado privado CLT partiu de uma base regulatória zero em 2024 — a consolidação dos convênios empregador-banco deve levar 3-5 anos. **2026-2028 são os anos de ramp estrutural**, não ainda de maturidade. O produto hoje representa ~5-8% do TAM estimado, o que implica runway de 10-15x do estoque atual antes de saturação.

### Dinâmica de Crescimento

- Crescimento é limitado pela velocidade de convênios, não por demanda — o trabalhador quer o produto (taxa menor), mas o banco precisa de contrato com o empregador primeiro.
- Itaú (~R$1,9B originados em jan/26) e grandes bancos têm vantagem competitiva estrutural via capilaridade de relacionamento corporativo (conta salário, benefícios, folha de pagamento).
- Fintechs (Nubank, C6, iFood) competem, mas o próprio Nubank sinalizou restritividade operacional — reconhece o risco de demissão como limitante de originação agressiva.

## Impacto no NIM vs Custo de Risco

O efeito net do consignado privado no resultado bancário é positivo, mesmo com spread bruto menor que crédito pessoal. A lógica é de RAROC (Risk-Adjusted Return on Capital), não de spread bruto.

### Comparativo Quantitativo (estimado)

| Métrica | Crédito Pessoal | Consignado Privado CLT |
|---------|-----------------|------------------------|
| Taxa ao tomador | ~50% a.a. | ~32% a.a. (~2,4% a.m.) |
| CDI referência | ~12,75% a.a. | ~12,75% a.a. |
| Spread bruto sobre CDI | ~37 p.p. | ~19 p.p. |
| Custo de risco (PDD) | ~8-12% a.a. | ~1-2% a.a. |
| Spread líquido de risco | ~25-29 p.p. | ~17-18 p.p. |
| Capital regulatório (RWA) | Maior (risco elevado) | Menor (garantia folha) |
| RAROC relativo | Base | Superior |

### Conclusão do Efeito no NIM

- A migração de portfólio de crédito pessoal → consignado privado **reduz o [[nii_clientes]] bruto** (spread menor), mas **melhora o NIM líquido de risco** (PDD cai mais do que o spread).
- O efeito no [[custo_risco]] consolidado do banco é positivo: mais volume em produto de baixíssima inadimplência dilui o custo médio da carteira.
- Para bancos com NIM geral ~12% (ex: Itaú), consignado privado entra como produto de NIM ~6-8% mas com capital alocado muito menor — resultado: ROE do produto provavelmente acima da média da carteira de varejo.
- **Não há contradição entre "spread menor" e "produto lucrativo"** — a equação correta é RAROC, não spread bruto.

## Risco de Demissão em Detalhe

O risco principal do consignado privado não é inadimplência voluntária, mas **ruptura do vínculo empregatício**.

### Mecanismo de Proteção e Sequência de Perda

```
1. Trabalhador é demitido
2. Desconto automático em folha cessa imediatamente
3. FGTS acumulado é usado para amortizar o saldo devedor (se suficiente)
4. Se FGTS < saldo devedor: banco renegocia → crédito se torna pessoal não garantido
5. Se inadimplência: banco aciona cobrança como qualquer crédito sem garantia real
```

O FGTS atua como buffer parcial — trabalhadores com maior tempo de emprego têm saldo proporcional. Para demitidos com poucos meses de vínculo, a proteção é menor.

### Setores de Maior Risco de Concentração

Exposição ao consignado privado deve ser calibrada por setor do empregador:

| Setor | Rotatividade típica | Risco relativo |
|-------|---------------------|----------------|
| Varejo | Alta | Elevado |
| Construção civil | Alta / sazonal | Elevado |
| Food delivery / logística | Alta | Elevado |
| Indústria | Média | Moderado |
| Serviços financeiros | Baixa | Baixo |
| Utilities / concessões | Muito baixa | Muito baixo |

- Bancos com concentração em grandes empregadores de setores estáveis têm perfil de risco mais próximo ao consignado público.
- **Management do Itaú citou "rotatividade CLT" como principal risco** — implica que a originação foca em empregadores com menor churn histórico.

### Risco Cíclico

O consignado privado tem **risco cíclico embutido**: em ciclos de desemprego elevado (ex: recessão, +2 p.p. na taxa de desemprego), a inadimplência sobe estruturalmente acima do baseline de 1-2% a.a. O produto não é tão defensivo quanto o consignado INSS em cenários macro adversos.

## Impacto no Modelo ITUB4

### Como o Produto Aparece no Grafo Atual

O consignado privado **não está segmentado explicitamente** no `ITUB4_model.json`. Está capturado implicitamente em:

- `in:crescimento_carteira_br` — guidance de +6,5-10,5% para carteira Brasil inclui crescimento do consignado privado como vetor principal.
- `in:custo_risco` — melhoria de mix para consignado privado contribui para [[custo_risco]] consolidado abaixo da média histórica.
- `in:rec_fin_spread` / `in:nii_clientes` — NIM agregado captura o efeito de mix, mas não isola o produto.

### Materialidade Atual vs Futura

```
Carteira ITUB4 total (estimado 2025)      ~R$1.100-1.200B
Estoque consignado privado Itaú (2025)    ~R$10-15B
Participação atual                         ~1-1,5%

Se produto atinge R$50-60B em 2026:
Participação                               ~4-5% da carteira total
Materialidade                              relevante para NIM e custo de risco
```

### Candidato a Graph Patch Futuro

A modelagem atual não captura separadamente o efeito do consignado privado. Um refinamento estrutural seria segmentar a carteira de crédito por produto (ou ao menos por risco relativo), com spreads e custo de risco individuais:

```
carteira_consignado_privado  → spread ~19pp + custo_risco ~1.5%
carteira_credito_pessoal     → spread ~37pp + custo_risco ~10%
carteira_outros_varejo       → spread médio + custo_risco médio
```

Isso permitiria capturar explicitamente o efeito de mix shift no NIM líquido de risco — hoje esse efeito está implícito nos inputs agregados e é invisível no modelo. Candidato a incluir como premissa separada em revisão do grafo ITUB4 pós-2T26, quando houver histórico de estoque suficiente para calibrar os parâmetros.

## Ver Também

- [[crescimento_carteira]] — consignado privado é o maior vetor de crescimento orgânico
- [[custo_risco]] — inadimplência muito baixa neste produto
- [[nii_clientes]] — produto com spread menor que crédito pessoal, mas com muito mais volume
- [[banking]] — contexto setorial
- [[itau]] — empresa com maior detalhe público de originação (jan/26: R$1,9B)
