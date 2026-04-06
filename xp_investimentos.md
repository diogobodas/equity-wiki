---
type: empresa
source_quality: conceptual
aliases: [XP, XP Investimentos, XP Inc., XPI, Banco XP]
sources:
  - sectors/banking/sector_profile.md
  - wiki/banking.md
  - wiki/itau.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
updated: 2026-04-05
---

# XP Investimentos

A **XP Inc.** (ticker: XPI na Nasdaq) é a maior plataforma de investimentos do Brasil e um dos maiores grupos financeiros independentes da América Latina. Fundada em 2001 por Guilherme Benchimol, a empresa construiu um modelo único de **distribuição aberta (open architecture)** de produtos financeiros, quebrando o oligopólio dos grandes bancos na gestão de patrimônio.

## Modelo de Negócio

Diferente dos bancos tradicionais, a XP não é primariamente uma instituição de crédito — é uma **plataforma de distribuição e gestão de patrimônio**:

1. **Distribuição de investimentos**: Ações, fundos, renda fixa, COEs, previdência — de gestores independentes e próprios
2. **Assessoria financeira via XP Advisors**: Rede de ~15.000 assessores de investimentos independentes (AAIs)
3. **Banco XP**: Banco múltiplo para produtos de crédito (consignado, financiamento, capital de giro)
4. **Gestão própria (XP Asset)**: Fundos multimercado, fundos de renda fixa, FIIs
5. **Corretora de valores**: Renda variável, derivativos, estruturação de ofertas
6. **Seguros XP**: Seguros de vida, previdência privada

## Escala e Posicionamento

| Métrica | Referência |
|---------|-----------|
| Ativos sob custódia (AUC) | ~R$1,1-1,3T (estimativa 2025) |
| Clientes ativos | ~4,5-5M |
| Assessores independentes (AAIs) | ~15.000 |
| Receita líquida | ~R$15-18B/ano (estimativa) |

**Nota:** Valores são estimativas conceptuais. Verificar nos relatórios da XP Inc. (20-F na SEC) para dados exatos.

## Dinâmica Competitiva vs [[itau]]

A XP é o principal rival do Itaú no **wealth management e distribuição de investimentos**:

| Aspecto | XP | [[itau]] (via [[ion_itau]] + Personnalité) |
|---------|----|-----------------------------------------|
| Modelo | Open architecture (qualquer gestor) | Predominantemente produtos próprios |
| Assessores | Independentes (~15k AAIs) | Gerentes de relacionamento (funcionários) |
| Custo do assessor | Variável (comissão sobre AUC) | Fixo (salário + PLR) |
| Perfil de cliente | Desde R$100k (varejo) até Ultra High Net Worth | Personalité (>R$250k), Private (>R$3M) |
| Taxa de administração | Menor (competição forçou queda) | Maior (poder de marca, conveniência) |

**O que a XP quebrou:** Antes da XP, os grandes bancos captavam recursos em produtos próprios com taxas elevadas (fundos de renda fixa com TER de 3-4%). A XP introduziu fundos de gestores independentes com TER de 0,5-1,5%, forçando os bancos a competir em taxas.

## Como a XP Gera Receita

```
Receita_XP = Taxa_corretagem
           + Taxa_distribuição (rebate de gestores)
           + Taxa_assessoria (fee sobre AUC)
           + Spread bancário (Banco XP)
           + Taxa_administração (produtos próprios)
           + Receita_seguros
```

O modelo é baseado em **comissão e fee**, não em spread de crédito — muito mais parecido com um broker/asset manager do que com um banco. Isso torna a XP sensível ao volume de transações (volatilidade de mercado eleva receita de corretagem) e ao crescimento de AUC.

## Riscos Estruturais

1. **Sensibilidade ao ciclo de juros**: Com Selic alta (~13-14%), ativos de renda fixa (LCIs, CDBs) competem com renda variável. Menor interesse em ações = menor corretagem. Com Selic baixa, cliente vai para renda variável = maior volume de corretagem.
2. **Concorrência crescente**: Após o sucesso da XP, surgiram centenas de plataformas (BTG Pactual Digital, Rico, Clear, inter) disputando o mesmo espaço.
3. **Regulação de AAIs**: O BCB e CVM estão endurecendo a regulação de assessores independentes, potencialmente reduzindo a vantagem do modelo da XP.
4. **Churn de AAIs**: Grandes bancos tentam contratar os melhores assessores da XP com pacotes agressivos.
5. **Dependência de mercado bull**: Em bear market prolongado, clientes retiram recursos da bolsa → queda de AUC → queda de receita.

## Relevância para o Modelo de Banking

A XP não faz parte da cobertura direta, mas é relevante como:

- **Benchmark de fee income**: A receita da XP é 100% fee — mostra o potencial de [[receita_servicos_tarifas]] se os bancos conseguirem migrar para open architecture
- **Pressão sobre IE dos bancos**: A XP força os bancos a reduzir taxas de fundos → comprime receita de gestão → pressiona o [[indice_eficiencia]]
- **Contexto competitivo do [[ion_itau]]**: O Ion foi criado como resposta direta à XP — plataforma aberta dentro do ecossistema Itaú

## Itaú vs XP: A Grande Batalha

A relação Itaú-XP foi de investidor (ITUB4 comprou ~49% da XP em 2017-2018, depois saiu) para competidor. O Itaú criou o Ion como resposta competitiva direta. A batalha pelo wealth management brasileiro é um dos drivers de longo prazo da [[receita_servicos_tarifas]] do Itaú.

## Pressão sobre [[receita_servicos_tarifas]] dos Bancos

A XP forçou uma decompressão de taxas que afeta todos os bancos cobertos:

| Produto | Taxa pré-XP | Taxa atual | Impacto nos bancos |
|---------|------------|-----------|-------------------|
| Fundos DI/RF (TER) | 2-4% a.a. | 0,3-1,0% a.a. | Compressão de fee de gestão |
| Corretagem ações | R$20-50/ordem | R$0 (zero) | Queda de receita de corretagem |
| Assessoria financeira | Embutida | Fee explícito | Transparência forçada |

Essa compressão se manifesta no modelo do [[itau]] como menor crescimento de [[receita_servicos_tarifas]] na linha de gestão de patrimônio — ainda que o Ion parcialmente compense ao reter ativos dentro do ecossistema.

## Ver Também

- [[banking]] — setor financeiro e dinâmicas competitivas
- [[ion_itau]] — plataforma de investimentos do Itaú; concorrente direto da XP
- [[itau]] — ITUB4; histórico investidor e agora competidor da XP
- [[receita_servicos_tarifas]] — onde a pressão competitiva da XP aparece no modelo dos bancos
- [[indice_eficiencia]] — XP força queda de taxas que pressiona receitas dos bancos tradicionais
- [[nubank]] — outro competidor digital, mas focado em segmento diferente (massa)
