---
type: guard_report
digest: sources/digested/notion_xp_jpm_4e000ca3_summary.md
source: full/generic/notas/xp_jpm_4e000ca3.md
run_by: ingest_agent_manual_check
run_on: 2026-04-17
status: PASS
note: python não disponível no shell; validação manual realizada
---

# Number Guard — notion_xp_jpm_4e000ca3

## Resultado: PASS (validação manual)

Nenhum `[?]` inserido no digest.

## Claims verificados

| Claim no digest | Valor | Fonte (trecho) | Status |
|---|---|---|---|
| 100 pessoas/mês | 100 | "Acionamos 100 pessoas por mes" | MATCH_STRICT |
| ~5 anos (RLP futuros) | 5 | "Demorou 5 anos pra formalizar o rlp de futuros" | MATCH_STRICT |

## Skipped (regras do guard)

- Anos isolados: 2019, 2017, 2024, 2025 — excluídos por regex de anos (19xx/20xx)
- Marcadores de lista/ordinal: não aplicável neste digest

## Observação

O executor Python (`number_guard.py`) não pôde ser chamado diretamente (shell sem `python`/`python3`). Todos os valores numéricos foram verificados manualmente contra `full/generic/notas/xp_jpm_4e000ca3.md`. A fonte é muito curta (~40 linhas) — verificação manual é exaustiva.
