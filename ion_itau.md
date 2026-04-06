---
type: empresa
source_quality: conceptual
aliases: [Ion, Ion Itaú, Ion Investimentos, Ion by Itaú, íon Itaú]
sources:
  - sectors/banking/sector_profile.md
  - wiki/banking.md
  - wiki/itau.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
updated: 2026-04-05
source_quality: conceptual
---

# Ion Itaú

O **Ion** é a plataforma de investimentos do [[itau]] Unibanco, lançada em 2020, voltada para clientes de média e alta renda que buscam uma experiência digital de investimento com acesso a produtos diversificados — incluindo de terceiros (open architecture parcial). É a resposta do Itaú à [[xp_investimentos]] no segmento de wealth management digital.

## Proposta de Valor

O Ion posiciona-se como uma plataforma de investimentos completa dentro do ecossistema Itaú:

- **Open architecture**: Acesso a fundos de gestoras externas (além dos produtos Itaú)
- **Interface digital**: App/plataforma web com UX moderno, similar à XP
- **Produtos diversificados**: Ações, FIIs, fundos, ETFs, renda fixa, COEs, previdência
- **Assessoria digital**: Suporte de especialistas sem custo adicional
- **Integração com conta Itaú**: Sem burocracia de cadastro para clientes existentes

## Posicionamento vs [[xp_investimentos]]

| Aspecto | Ion (Itaú) | XP Investimentos |
|---------|-----------|-----------------|
| Modelo | Plataforma aberta com curadoria | Open architecture plena |
| Assessoria | Digital (especialistas Itaú) | Rede de AAIs independentes |
| Base de clientes | Clientes Itaú existentes (facilidade) | Independente (conquista ativa) |
| Produtos Itaú | Ampla presença | Parcial (histórico de conflito) |
| Transferência de recursos | Dentro da conta Itaú (zero atrito) | Requer DOC/TED (atrito maior) |
| Taxa de administração | Competitiva (pressão da XP) | Competitiva |

**Vantagem estrutural do Ion:** A barreira de entrada para converter um cliente Itaú existente é mínima — os recursos já estão na conta. Para a XP capturar esse mesmo cliente, ele precisa transferir ativamente os recursos para fora do Itaú.

**Desvantagem:** O Ion ainda carrega a percepção de "banco tradicional" — parte dos clientes desconfia que os produtos Itaú têm preferência na curadoria.

## Estratégia do Itaú: Defesa do Float

O Ion é principalmente uma **estratégia defensiva**: evitar a migração de ativos dos clientes Itaú para a XP ou BTG. Cada R$1 que sai do Itaú para a XP:
1. Reduz a base de funding do Itaú (passivo barato)
2. Reduz a receita de gestão de patrimônio
3. Reduz o cross-sell de crédito e seguros

Ao oferecer uma plataforma competitiva internamente, o Itaú retém o cliente dentro do ecossistema mesmo que ele queira diversificar os investimentos.

## Impacto no Modelo ITUB4

Como o iti, o Ion não aparece como linha separada nos releases do Itaú — é integrado nos segmentos de Varejo e Personnalité. Sua relevância para o modelo:

1. **Receita de tarifas e gestão**: O Ion contribui para o crescimento de [[receita_servicos_tarifas]] via taxa de administração de fundos e eventual fee de assessoria
2. **Retenção de AUC**: Menor migration de ativos = maior base para fees de gestão
3. **Cross-sell**: Clientes que usam o Ion têm maior probabilidade de contratar seguros, previdência, crédito imobiliário — produtos de maior margem

## Escala (estimativa)

O Itaú não divulga dados separados do Ion. Mas dado que o Itaú tem ~70M de correntistas, e que o Ion é acessível a qualquer um, estima-se que o Ion tem acesso a uma base de clientes potenciais muito maior que a XP — a questão é qual porcentagem está efetivamente ativa na plataforma.

## Impacto no [[receita_servicos_tarifas]] de ITUB4

O crescimento do Ion é um driver direto da linha de fees do Itaú. Canais de contribuição:

1. **Taxa de administração de fundos**: Migração de fundos próprios para o Ion gera retorno via TER (Total Expense Ratio)
2. **Corretagem de renda variável**: Operações de ações e fundos via Ion geram corretagem
3. **Distribuição de COEs e produtos estruturados**: Margem de distribuição para a tesouraria do Itaú
4. **Previdência privada**: Crescimento de AUC em previdência = receita de gestão de longo prazo

O Ion compete com [[xp_investimentos]] por um mercado de R$3-4T em investimentos de pessoas físicas no Brasil. Cada ponto percentual de market share equivale a R$30-40B em AUC adicional, gerando ~R$150-200M/ano em fee income.

## Impacto na Linha de Despesas

O desenvolvimento da plataforma Ion implica custos relevantes de TI, marketing e compliance que pressionam o [[indice_eficiencia]] no curto prazo. O Itaú absorve esses custos como investimento estratégico em retenção de AUC (Assets Under Custody) e fees de longo prazo.

A lógica econômica:
- Custo de manutenção da plataforma: ~R$200-500M/ano (estimativa; não divulgado)
- Fee income gerado: proporcional ao AUC gerenciado e ao volume de transações
- Payback: cada R$1 de fee income no segmento de wealth management tem múltiplo de receita maior que no varejo de crédito (margem líquida mais alta, sem risco de crédito)

O Ion é, portanto, um bet estratégico no crescimento do mercado de capitais brasileiro: se a poupança financeira no Brasil migrar de depósitos bancários para fundos e ações (tendência de longo prazo com Selic mais baixa), o Ion posiciona o Itaú para capturar fees nessa migração em vez de perder receita para a [[xp_investimentos]].

## Benchmark Internacional

Plataformas similares ao Ion em outros países:
- **Merrill Edge (Bank of America)**: Integração de investimentos com conta corrente, evitou perda de AUC para corretoras independentes
- **Chase YouInvest → J.P. Morgan Self-Directed**: Mesmo conceito de retenção de clientes via open architecture
- **Itaú LatAm**: O mesmo modelo é replicado em Chile e Colombia, onde a Selic equivalente é menor e o mercado de capitais cresce mais rápido

## Ver Também

- [[itau]] — empresa controladora; Ion é a plataforma de investimentos do ecossistema
- [[iti_itau]] — banco digital do Itaú para o segmento de massa (diferente do Ion)
- [[xp_investimentos]] — principal concorrente do Ion em wealth management digital
- [[receita_servicos_tarifas]] — linha de DRE onde a receita do Ion aparece
- [[banking]] — estrutura competitiva do setor bancário brasileiro
- [[nubank]] — concorrente no segmento digital, porém mais focado em massa
- [[indice_eficiencia]] — custos de desenvolvimento do Ion pressionam IE no curto prazo
- [[nii_mercado]] — fundos distribuídos pelo Ion geram fee income, não NII
- [[sanb11]] — sem equivalente ao Ion; Santander usa AAIs externos para wealth management
