---
source: notion
notion_page_id: 2af00ca3-2bce-80c8-907d-f5d96ea77ebf
notion_url: https://app.notion.com/p/SELECT-Data-tcb-modalidade-porte-SUM-vencido_acima_de_15_dias-AS-vencido_acima_de_15_d-2af00ca32bce80c8907df5d96ea77ebf
title: "SELECT
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
porte;"
created: 2025-11-18T13:13:00.000Z
edited: 2026-03-01T20:53:00.000Z
empresa: generic
tags:
  - "Bancos"
---

# SELECT
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


