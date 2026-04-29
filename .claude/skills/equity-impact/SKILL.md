---
name: equity-impact
description: >
  Lê o morning-briefing de hoje (emails do Outlook das últimas 16h em $TEMP/briefing/) +
  relatório CVM diário e gera um impact report focado nas 37 empresas em cobertura ativa
  (calendario_resultados.md). Output read-only em briefings/<YYYY-MM-DD>-impact.md.
  Use quando o usuário pedir "rodar impact briefing", "ver o que mexe na cobertura hoje",
  "/equity-impact", ou após o cron das 8h35.
user_invocable: true
---

# Equity Impact — Skill

Sempre executa o orchestrator `tools/equity_impact.sh` direto — não tenta replicar a lógica.

## Pré-requisitos (verificar antes de rodar)

1. **Morning briefing já rodou hoje.** O scheduled task `morning-briefing` (8h23) gera os JSONs em `$TEMP/briefing/`. Se o usuário pediu antes das 8h25 ou se Outlook estava fechado, rode `/morning-briefing` manualmente primeiro.

2. **Relatório CVM diário** (opcional). Scheduled task `relatorio-cvm-automtico` (8h04) gera `\\10.10.10.2\Dados\PesquisaBolsa\Diogo\Projeto Servidor\Projetos\_shared\CVM-API\relatorio_<YYYY-MM-DD>.html`. Se faltar, o impact agent pula esses hits sem erro.

## Execução padrão

```bash
bash tools/equity_impact.sh
```

Output: `briefings/<YYYY-MM-DD>-impact.md` (e printa o path no stdout).

## Variantes

```bash
bash tools/equity_impact.sh --ticker WEGE3      # foco em uma empresa
bash tools/equity_impact.sh --debug             # stderr verbose (counts, paths)
bash tools/equity_impact.sh --no-llm            # apenas o JSON context (debug, sem chamar LLM)
```

## Notas

- **Read-only** — não dispara fetch/ingest. Action items são textuais; usuário decide.
- **Notícias NÃO viram sources da wiki.** O briefing diário é ephemeral por design — vive em `briefings/` (root, fora de `sources/`), serve pra chamar atenção no dia, não pra citação em wiki pages.
- Se o usuário pediu briefing de **outro dia** que não hoje, avisar que `briefing_temp.json` é sobrescrito diariamente — só funciona pra `today`.
