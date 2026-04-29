---
source: notion
notion_page_id: 2af00ca3-2bce-80c8-907d-f5d96ea77ebf
empresa: generic
tags:
  - Bancos
  - SCR
  - inadimplência
created: 2025-11-18
edited: 2026-03-01
---

# Query SCR — Inadimplência por Modalidade e Porte

## Contexto da nota

Nota técnica (analista interno) registrando uma query SQL para extração de dados do **SCR (Sistema de Informações de Crédito do Banco Central do Brasil)**. A nota não menciona empresa-alvo específica nem data de análise — trata-se de um snippet de código reutilizável para análise setorial de crédito bancário. Tags: `Bancos`. Criada em 2025-11-18, última edição 2026-03-01.

(fonte: full/generic/notas/select_data_tcb_modalidade_porte_sum_vencido_acima_de_15_dias_as_vencido_acima_d_2af00ca3.md)

## Fatos/dados-chave

A nota contém exclusivamente uma query SQL — sem números, afirmações gerenciais ou guidance. O conteúdo integral é:

```sql
SELECT
    Data,
    tcb,
    modalidade,
    porte,
    SUM(vencido_acima_de_15_dias)          AS vencido_acima_de_15_dias,
    SUM(carteira_ativa)                    AS carteira_ativa,
    SUM(carteira_inadimplida_arrastada)    AS carteira_inadimplida_arrastada
FROM
    scr_data
GROUP BY
    Data,
    tcb,
    modalidade,
    porte
ORDER BY
    Data,
    tcb,
    modalidade,
    porte;
```

(fonte: full/generic/notas/select_data_tcb_modalidade_porte_sum_vencido_acima_de_15_dias_as_vencido_acima_d_2af00ca3.md)

**Campos extraídos:**
- `vencido_acima_de_15_dias` — carteira vencida acima de 15 dias (proxy de inadimplência precoce).
- `carteira_ativa` — carteira total ativa.
- `carteira_inadimplida_arrastada` — carteira inadimplida arrastada (conceito de saldo que "arrasta" para próximos ciclos).

**Dimensões de corte:** data, tcb (tipo de crédito bancário), modalidade, porte do tomador.

**Fonte de dados:** tabela `scr_data` — correspondente ao microdado SCR disponibilizado pelo Bacen.

## Empresas e tickers mencionados

Nenhuma empresa ou ticker específico mencionado. Análise aplicável ao setor **Bancos** em geral — útil para comparação de inadimplência por porte/modalidade entre instituições (ex: Banco do Brasil, Itaú, Santander, Bradesco).

## Teses, dúvidas abertas, follow-ups

- Tese (analista): query padronizada para acompanhar evolução da inadimplência precoce (>15 dias) no SCR, segmentada por porte do tomador e modalidade — permite identificar deterioração específica por segmento (PJ grande vs. PJ micro, crédito consignado vs. rotativo, etc.) antes que apareça nos releases trimestrais dos bancos.
- Follow-up implícito: aplicar filtros adicionais (ex: `WHERE tcb = 'X'` ou `WHERE porte = 'PJ_MICRO'`) para análises específicas por instituição ou segmento.
