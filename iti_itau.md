---
type: empresa
source_quality: conceptual
aliases: [Iti, iti Itaú, Banco Iti, iti by Itaú]
sources:
  - sectors/banking/sector_profile.md
  - wiki/banking.md
  - wiki/itau.md
  - sectors/banking/companies/ITUB4/outputs/decomposition/ITUB4_dependency_graph_v3.json
  - sectors/banking/companies/ITUB4/outputs/model/ITUB4_model.json
updated: 2026-04-05
---

# Iti (Itaú)

O **iti** é o banco digital do [[itau]] Unibanco, lançado em 2019, focado no segmento de clientes jovens, desbancarizados e de menor renda. É a resposta do Itaú ao crescimento dos neobanks — especialmente o [[nubank]] — no segmento de clientes que o banco tradicional não atendia de forma eficiente.

## Proposta de Valor

O iti é um **banco 100% digital** sem tarifas para o usuário básico:

- **Conta digital gratuita**: Sem mensalidade, sem taxa de manutenção
- **Cartão de débito/crédito**: Mastercard sem anuidade
- **Pix gratuito**: Transferências e pagamentos sem custo
- **Rendimento automático**: Saldo rendendo CDI automaticamente
- **Crédito simplificado**: Acesso ao crédito pessoal de forma digital

## Posicionamento Estratégico

O iti serve como **plataforma de entrada** para o ecossistema do Itaú:

```
iti (entrada digital, massa) → migração gradual → Itaú Person (varejo) → Itaú Personnalité (renda alta)
```

A lógica é que um cliente captado no iti a baixo custo pode, ao longo do tempo, migrar para produtos de maior margem dentro do ecossistema Itaú. Isso reduz o custo de aquisição de clientes (CAC) para os segmentos de maior valor futuro.

## Escala (estimativa conceptual)

| Métrica | 2025 (estimativa) |
|---------|------------------|
| Contas ativas | ~10-20M |
| Clientes únicos | ~15-25M |

**Nota:** O Itaú não divulga dados separados do iti nos releases do ITUB4. Os números acima são estimativas sem fonte verificada.

## Como Contribui para o Modelo ITUB4

O iti não aparece como linha separada no modelo [[itau]] — é consolidado dentro dos segmentos de varejo. Sua relevância é indireta:

1. **Crescimento de base de clientes**: iti captura clientes que antes iam para o [[nubank]] ou permaneciam desbancarizados
2. **Crédito de entrada**: Empréstimos pessoais do iti com riscos maiores contribuem para o [[custo_risco]] do portfólio varejo
3. **Eficiência**: Baixo custo unitário por cliente digital — melhora o [[indice_eficiencia]] do Itaú ao servir mais clientes sem custo de agência

## Competição

| Competidor | Produto Equivalente |
|------------|-------------------|
| [[nubank]] | Conta digital + cartão de crédito |
| Mercado Pago | Conta digital + Pix + crédito |
| PicPay | Conta digital + transferências |
| Bradesco Next | Banco digital do Bradesco |

## Contexto Competitivo vs [[nubank]]

O iti foi criado especificamente para competir com o Nubank no segmento de clientes que os bancos tradicionais não atendiam bem — sem tarifas, digital, Pix gratuito. A diferença estratégica:

| Aspecto | iti (Itaú) | [[nubank]] |
|---------|-----------|-----------|
| Origem | Banco tradicional lançando digital | Nativo digital |
| Missão interna | Reter/capturar clientes de massa | Crescimento orgânico |
| Crédito | Acesso ao portfólio Itaú | Portfolio próprio em expansão |
| Rentabilidade | Subsidiada pelo Itaú (CAC tolerado) | Busca sustentabilidade própria |
| Dados de clientes | Compartilhados com Itaú | Independente |

O iti tem vantagem estrutural por poder subsidiar o custo de aquisição via cross-sell futuro dentro do Itaú. O Nubank precisa ser lucrativo por conta própria em cada segmento.

## Estratégia Digital Comparada: Itaú vs Santander vs Bradesco

Os três bancos cobertos têm estratégias distintas para o segmento digital de massa:

| Aspecto | Itaú (iti) | [[sanb11]] (App Santander) | [[bradesco]] (Next) |
|---------|-----------|--------------------------|---------------------|
| Marca | Separada (iti) | Integrada (Santander) | Separada (Next) |
| Status | Ativo e crescendo | Funcional, sem separação de marca | Reduzido/integrado ao app principal |
| Foco | Desbancarizados + jovens | Base de clientes existente | Base existente + jovens |
| Concorrência ao Nubank | Direta | Indireta | Parcial |

O Itaú fez a aposta mais clara com o iti: criar uma marca completamente separada para não canibalizar o banco tradicional e competir de igual para igual com o [[nubank]] no posicionamento de mercado (sem tarifas, 100% digital, Pix, CDI automático).

## Crescimento de Carteira de Crédito via iti

O iti é um canal de crescimento da [[crescimento_carteira]] para o segmento de menor renda:
- Clientes iti têm LTV (lifetime value) inicial baixo mas crescente
- Crédito pessoal e CDC no iti têm spreads maiores (risco de crédito maior) → contribui para o [[nim]] do Itaú
- O risco: [[custo_risco]] maior para esse segmento — inadimplência de clientes iti tende a ser maior que a carteira Personnalité

## Ver Também

- [[itau]] — empresa controladora; iti é subsidiária integral
- [[ion_itau]] — plataforma de investimentos do Itaú (segmento diferente: média-alta renda)
- [[nubank]] — principal concorrente do iti no segmento digital de massa
- [[banking]] — setor bancário e dinâmicas competitivas digitais
- [[indice_eficiencia]] — custo digital baixo melhora IE do Itaú
- [[crescimento_carteira]] — iti contribui como canal de crescimento no segmento de menor renda
- [[custo_risco]] — clientes iti têm maior inadimplência que o core Itaú
- [[nim]] — spreads maiores no crédito pessoal iti elevam o NIM médio da carteira
