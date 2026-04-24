# Dated Claims + Supersession — Wiki Staleness Control

**Status:** design approved, awaiting implementation plan.
**Date:** 2026-04-23
**Owner:** diogobodas

## Context & Motivation

Páginas da wiki vêm ficando stale. O caso mais pungente é o de páginas com conteúdo legal/regulatório ([reforma_tributaria.md](../../../reforma_tributaria.md), [section_232.md](../../../section_232.md), [mcmv.md](../../../mcmv.md)) — contêm informação correta **na data do ingest** mas envelhecem em silêncio quando a lei/portaria/MP muda. Problema análogo em páginas de empresa com claims voláteis fora do ciclo CVM (capex anunciado em Investor Day, timing de lançamento de produto, meta de frota) — mudam via press release/news e o pipeline regular (ITR/DFP/release/call) só pega no próximo trimestre.

A wiki hoje tem `updated:` no frontmatter, mas a granularidade é página-inteira e não distingue claims duráveis (definições, mecânica) de claims datáveis (alíquotas, guidance, metas). Ao reescrever uma página, a informação antiga é silenciosamente sobrescrita sem registro de supersession.

Inspiração externa: [LLM Wiki v2 (gist de rohitg00)](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) propõe **confidence scoring com recency, supersession explícita e self-healing lint** como extensões do padrão Karpathy. Esta spec adota as três ideias, mas restringe escopo ao problema de staleness — não implementa knowledge graph, hybrid search, multi-agent, nem os demais pontos do gist.

## Goals

1. **Destacar a data da informação.** Claim datável carrega `em: YYYY-MM-DD` visível ao leitor, parseable por máquina.
2. **Garantir que dado novo atualiza claim antigo.** Três caminhos de detecção complementares — reativo no ingest, lint periódico, watchlist para sinal externo.
3. **Modalidade de supersession explícita.** Mudanças de regime produzem "antes × depois" inline (Modalidade 2); updates rotineiros são silent overwrite + bump de `em:` (Modalidade 1).
4. **Integração com SCHEMA.md e CLAUDE.md** como contrato operacional da wiki.

## Non-Goals

- **Retrofit bulk das ~90 páginas existentes.** Pass manual nas 5 páginas legais de alta prioridade é trabalho separado, fora desta spec.
- **Knowledge graph / hybrid search / multi-agent** do gist — fora de escopo.
- **Automação total do Path C.** `watch.sh` é manual/cron externo; não instala scheduler.
- **Parsing de DOU ou ingestão direta de legislação.** Watchlist é proxy via WebSearch em sites confiáveis, não substitui fetch oficial.
- **Confidence scoring numérico** (ex: `confidence: 0.85`). Recency (via `em:`) já dá o sinal operacional necessário; score numérico seria overkill.
- **Retrofit das regras de Lint §1, §2, §4, §6, §7, §8, §9, §10 do SCHEMA.md** — só §3 (Stale pages), §5 (Contradictions) e o novo §11 (Dated claim staleness) são implementados aqui.

## Architecture

```
                  ┌────────────────────────────────┐
                  │   WIKI PAGE com claims com     │
                  │   (fonte: X, em: YYYY-MM-DD)   │
                  └────────────────────────────────┘
                      ▲           ▲          ▲
         ┌────────────┘           │          └────────────┐
         │                        │                       │
    Path A                    Path B                  Path C
  (reativo)                (periódico)             (opt-in por página)
         │                        │                       │
  wiki_update.sh           tools/lint.sh            tools/watch.sh
    (prompt diff)           (código novo)           (código novo)
         │                        │                       │
  ingest.sh → queue        lint_reports/            watch_state/
  → digest novo             YYYY-MM-DD.md           {page}.json
  → plan identifica         (severidades:            (hits viram
   dated_claims_to_         warn/action/             entrada no
   _review                   hint)                    próximo lint)
```

Três mecanismos ortogonais. Um claim pode ser flaggado/atualizado por qualquer um dos três, de forma independente.

## Component 1 — The `em:` Marker

### Format

Citação existente é estendida com um campo opcional:

```
antes:  (fonte: digested/Texto Reforma tributaria jan-2025_summary.md)
depois: (fonte: digested/Texto Reforma tributaria jan-2025_summary.md, em: 2025-01-16)
```

Regex parse: `\(fonte:\s*([^,)]+)(?:,\s*em:\s*(\d{4}-\d{2}-\d{2}))?\)`.

### Semântica de `em:`

`em:` é a **data em que a informação é verdadeira no mundo**, não a data do ingest. O ingest date continua em `manifests/{empresa}.json :: sources[].ingested_on` e não é replicado no claim.

| Tipo de claim | `em:` é... | Exemplo |
|---|---|---|
| Alíquota, regra fiscal, dispositivo de lei | Data de publicação da norma | `em: 2025-01-16` (LC 214/2025) |
| Guidance de empresa | Data do comunicado/release | `em: 2026-04-10` |
| Valor regulatório (teto MCMV, faixa) | Data da portaria/decreto vigente | `em: 2024-10-03` |
| Meta operacional de empresa (frota, capex) | Data do anúncio/Investor Day | `em: 2026-03-15` |
| Número de balanço (margem 3T25, ROE) | — | **Não leva `em:`** (período codificado) |
| Definição conceitual ("CBS substitui PIS/Cofins") | — | **Não leva `em:`** (atemporal) |

### Criterio de aplicabilidade (regra para o LLM na escrita)

> Se o claim pode ficar *factualmente errado* amanhã sem que o período contábil mude, leva `em:`.
> Se o claim está amarrado a um período contábil explícito (3T25, 2024) ou é definicional/mecânico, não leva.

Claims que **claramente levam `em:`**: alíquotas, tetos regulatórios, faixas de renda, prazos legais, datas de vigência de MP/LC, guidance corporativo forward-looking, metas operacionais datadas, cronogramas de implementação.

Claims que **claramente não levam `em:`**: definições, descrição de mecânica, série histórica com período anotado, números de DFs, nomes de leis (o número da lei é imutável — só o conteúdo muda e carrega seu próprio `em:`).

## Component 2 — Supersession

Dois modos, aplicados por tipo de mudança. Ambos são prescritos no `wiki_write.md` atualizado (ver Path A).

### Modalidade 1 — Silent overwrite (default)

Refresh de guidance, número atualizado, data efetiva mudou sem mudança conceitual. Claim antigo é removido, novo escrito, `em:` atualizado. Histórico vive no git log.

```
antes: Alíquota reduzida em 50% (fonte: X, em: 2025-01-16)
depois: Alíquota reduzida em 60% (fonte: Y, em: 2026-08-10)
```

### Modalidade 2 — Supersession estrutural "antes × depois"

Mudança de lei que cria novo regime, reforma com regra de transição, tarifa reestruturada. LLM escreve tabela ou seção comparativa inline porque o **contraste antes/depois É o conteúdo valioso**. Padrão que [section_232.md](../../../section_232.md):18-29 já usa naturalmente.

Gatilho para o LLM escolher Modalidade 2:
1. A mudança invalida uma premissa analítica (não só o número), OU
2. O claim velho está referenciado em outras páginas via wikilink/citação cruzada (supersession silenciosa quebraria consistência).

### Política explicitamente *não* adotada

- **Strikethrough inline** — polui a leitura em Obsidian sem adicionar info que o git já preserva.
- **HTML comments com histórico** — ilegível.
- **Páginas separadas de "history"** — complexidade sem payoff.

## Component 3 — Path A (Reactive no Ingest)

Mudança em dois prompts; zero código novo.

### `tools/prompts/wiki_plan.md`

A fase de planning do `wiki_update.sh` já lê digesteds novos, páginas existentes e a lista de empresas. Ganha novo campo no JSON de plano, por página:

```json
{
  "page": "reforma_tributaria.md",
  "action": "update",
  "digesteds": ["sources/digested/notion_nova_IN_RFB_summary.md"],
  "dated_claims_to_review": [
    {
      "claim_excerpt": "alíquota reduzida em 50%",
      "current_em": "2025-01-16",
      "reason": "nova IN da RFB pode alterar alíquota efetiva"
    }
  ]
}
```

O planner é forçado a enumerar quais claims datados na página-alvo podem ser invalidados pelo digest novo. Se não houver nenhum, `dated_claims_to_review: []` explícito — não omitir.

### `tools/prompts/wiki_write.md`

Fase de execução, ao receber o plano, para cada entry em `dated_claims_to_review`:

1. Lê o claim inteiro em contexto + o digest novo.
2. Escolhe uma de três saídas:
   - **Reafirmado** — claim ainda válido; bump `em:` para a data do digest novo (reconfirmação).
   - **Atualizado silent (Modalidade 1)** — número/data mudou, sem mudança de regime: overwrite + novo `em:`.
   - **Atualizado estrutural (Modalidade 2)** — mudança de regime: escrever bloco antes×depois.
3. Registra em `log.md` entry `[claim-update]`:
   ```
   [claim-update] 2026-04-23 reforma_tributaria.md "alíquota reduzida em 50%" em:2025-01-16→2026-08-10 modo:silent
   ```

### Cobertura

Todo dado que entra via `ingest.sh` / `ingest_calls.sh` / `fetch_notion.sh`. CVM releases, earnings calls, notas Notion. **Não** pega sinal externo puro (lei nova sem source ingerido) — esse é trabalho do Path C.

## Component 4 — Path B (Dated Lint)

### Arquivos novos

- `tools/lint.sh` — wrapper fino, invoca Python.
- `tools/lib/dated_lint.py` — parser + regras + relatório.
- `tools/lint_config.json` — thresholds configuráveis.

### Parser

Regex sobre todos os `*.md` no root da wiki (exclui `docs/`, `sources/`, `tools/`). Captura tuples:

```
(page_path, line_number, claim_excerpt, fonte_path, em_date_or_null)
```

`claim_excerpt` = texto do parágrafo ou célula de tabela que contém a citação, truncado a 200 chars.

### Regras de flag

| Regra | Condição | Severidade |
|---|---|---|
| **Age threshold** | `em_date + threshold < today` sem source mais novo sobre o tópico | `warn` |
| **Newer source available** | existe `digested/`/`full/`/`structured/` com `ingested_on > em_date` e mesma empresa/conceito | `action` |
| **Cross-page contradiction** | duas páginas com claims numéricos conflitantes sobre o mesmo item, `em:` diferentes | `action` |
| **Missing `em:`** | claim com número + verbo temporal ("vigente", "a partir de", "até") sem `em:` | `hint` |

### Thresholds (lint_config.json)

```json
{
  "thresholds_months": {
    "legal_regulatorio": 12,
    "guidance_corporativo": 6,
    "metric_absoluto": 3,
    "default": 12
  },
  "tipo_inference": {
    "legal_regulatorio": {
      "page_types": ["concept"],
      "keywords": ["alíquota", "LC ", "MP ", "portaria", "decreto", "lei", "IN ", "RFB", "tarifa", "reforma"]
    },
    "guidance_corporativo": {
      "page_types": ["entity"],
      "keywords": ["guidance", "meta", "target", "projeção", "capex", "orçamento"]
    },
    "metric_absoluto": {
      "page_types": ["entity", "sector"],
      "keywords": ["banco de terrenos", "frota", "funcionários", "lojas", "unidades"]
    }
  }
}
```

Inferência do tipo (qual threshold aplicar a um claim): casamento por frontmatter `type:` + keywords no `claim_excerpt`. Primeiro match vence; se nada casar, usa `default`.

### Decisão de "mesmo tópico" para "Newer source available"

1. Empresa: match via frontmatter `aliases:` da página vs. `manifests/{empresa}.json :: sources[]`.
2. Conceito/keyword: match entre termos-chave do `claim_excerpt` e `watches:` da página (se houver) ou `aliases:`.

Match imperfeito é aceitável — é `action` warning, não fix automático.

### Saída

- `sources/lint_reports/YYYY-MM-DD.md` — relatório markdown, agrupado por página, com tabela de flags por severidade.
- Append a `log.md`: `[lint] 2026-04-23 reports/2026-04-23.md warn=N action=M hint=K`.

### Invocação

```bash
bash tools/lint.sh                      # report full
bash tools/lint.sh --severity action    # só action e acima
bash tools/lint.sh --page cyrela.md     # uma página
```

Manual. Nenhuma automação. Ranking de staleness é para humano triagear.

### Relação com SCHEMA.md §Lint

Implementa itens **§3 (Stale pages)** e **§5 (Contradictions)** + novo **§11 (Dated claim staleness)**. Outros itens (dead links, orphans, schema drift) ficam para sprint separado.

## Component 5 — Path C (Watchlist)

### Arquivos novos

- `tools/watch.sh` — wrapper fino.
- `tools/lib/watch_runner.py` — varredura + WebSearch + diff.
- `sources/watch_state/` — diretório novo, `{page_slug}.json` por página.

### Declaração no frontmatter da página

```yaml
---
type: concept
aliases: [CBS, IBS, LC 214/2025]
watches:
  - query: "LC 214/2025 alteração alíquota"
    sites: [planalto.gov.br, normaslegais.com.br, mattosfilho.com.br]
    cadence: weekly
  - query: "reforma tributária incorporadora IBS CBS 2026"
    sites: [valor.globo.com, infomoney.com.br]
    cadence: monthly
sources: [...]
updated: 2026-04-22
---
```

Campos:
- `query` — string literal para WebSearch.
- `sites` — array de domínios; query é restrita a esses domínios (operador `site:` do search engine).
- `cadence` — `weekly` | `monthly` | `quarterly`. Determina se o runner deve checar esta entry na execução atual (comparado com `last_run` no state file).

### Escopo (quem declara `watches:`)

**Não é feature só de página legal.** Qualquer página com claim volátil fora do ciclo CVM/Notion:

| Página típica | Claim vigiado | Por que CVM não pega |
|---|---|---|
| `cyrela.md` | "Capex 2026 de R$ X bi anunciado em Investor Day" | Ajuste via fato relevante/news |
| `tenda.md` | "Alea expandindo para Nordeste em 2026" | Atraso sai em release avulso |
| `unidas.md` | "Meta de frota = 300k até 4T26" | Revisões mensais em press release |
| `nvidia.md` | "H200 ship volume no 2T26" | Mudança via GTC/news |
| `reforma_tributaria.md` | "Alíquota reduzida em 50%" | Via LC/MP, nenhum pipeline |
| `mcmv.md` | "Teto Faixa 3 = R$ 350k" | Portaria muda sem entrar no pipeline |

Opt-in pelo autor. Nenhuma heurística automática adiciona `watches:` — o autor decide onde o risco de staleness justifica o custo.

### Mecânica do runner

Para cada página com `watches:`:

1. Lê `sources/watch_state/{page_slug}.json` (se existir). Shape:
   ```json
   {
     "page": "reforma_tributaria.md",
     "entries": [
       {
         "query": "LC 214/2025 alteração alíquota",
         "sites": ["planalto.gov.br", "..."],
         "cadence": "weekly",
         "last_run": "2026-04-16",
         "known_urls": {
           "https://...": {"title": "...", "snippet": "...", "published": "2026-04-10"}
         }
       }
     ]
   }
   ```
2. Para cada `entry`, se `last_run + cadence < today` (ou `last_run` ausente), roda o check.
3. Check: `claude --print` com prompt enxuto:
   > "Busca na web usando `{query}` restrito aos sites `{sites}`. Retorne JSON com `[{url, title, snippet, published_date}]` dos 10 hits mais recentes."
4. Diff com `known_urls`: URLs novos ou com `published_date` posterior a `last_run` são hits.
5. Atualiza `known_urls` + `last_run` no state file.
6. Hits geram entrada no **próximo lint report** (ou report imediato, opt por flag `--emit-report`):
   ```
   [watch-hit] reforma_tributaria.md query="LC 214/2025 alteração alíquota"
     → https://planalto.gov.br/... (publicado 2026-04-18, cadence weekly)
   ```

**Não ingere nada automaticamente.** Só sinaliza. Você decide se vale chamar `fetch_notion.sh` / `fetch.sh` / adicionar manualmente.

### Invocação

```bash
bash tools/watch.sh                    # roda todas as entries elegíveis pela cadência
bash tools/watch.sh --page cyrela.md   # só uma página
bash tools/watch.sh --force            # ignora cadência, força re-check de tudo
```

Cadência é imposta pelo runner (não roda entries fora de cadência). Execução em si é manual — você chama quando quer. Um eventual cron/scheduled task externa fica fora desta spec.

## File Changes Summary

| Categoria | Arquivo | Mudança |
|---|---|---|
| **Policy** | `SCHEMA.md` | Nova subseção "Dated claims" em §Source Citations; novas seções "Supersession" e "Watchlist"; §Lint ganha item §11 |
| **Policy** | `CLAUDE.md` | Comandos `lint.sh` e `watch.sh` adicionados; bullet novo em "Non-obvious rules" sobre `em:` |
| **Prompt (Path A)** | `tools/prompts/wiki_plan.md` | Campo `dated_claims_to_review` no JSON de plano |
| **Prompt (Path A)** | `tools/prompts/wiki_write.md` | Lógica de 3 saídas (reafirmado / silent / estrutural) + entry `[claim-update]` no log |
| **Código (Path B)** | `tools/lint.sh` | Novo — wrapper CLI |
| **Código (Path B)** | `tools/lib/dated_lint.py` | Novo — parser + regras + relatório |
| **Config (Path B)** | `tools/lint_config.json` | Novo — thresholds e inferência |
| **Código (Path C)** | `tools/watch.sh` | Novo — wrapper CLI |
| **Código (Path C)** | `tools/lib/watch_runner.py` | Novo — runner de WebSearch + state |
| **Estado (Path C)** | `sources/watch_state/` | Novo diretório (gitignore? decidir em plano) |
| **Estado (Path B)** | `sources/lint_reports/` | Novo diretório |

## Validation / Testing

### Path A (reativo)

- **Caso acid test:** tome [reforma_tributaria.md](../../../reforma_tributaria.md), adicione `em: 2025-01-16` a três claims de alíquota. Ingira um source Notion mock descrevendo "LC 227/2026 altera alíquota de imóveis de 50% para 60%". Rode `wiki_update.sh`. Espera-se: plan identifica os três claims, write aplica Modalidade 1 (silent) ou 2 (estrutural) apropriadamente, `[claim-update]` aparece em log.md.

### Path B (lint)

- **Parser unit tests** (`tests/test_dated_lint.py`):
  - Parseia `(fonte: X, em: 2026-01-15)` → tuple correta.
  - Parseia `(fonte: X)` sem `em:` → `em_date = None`.
  - Ignora `(fonte: ...)` em code blocks.
- **Regra "Age threshold":** seed uma página com claim `em: 2024-01-01` (>12 meses), rodar lint com default config, verificar `warn` emitido.
- **Regra "Missing em:":** seed claim com "vigente a partir de 2026" sem `em:`, verificar `hint` emitido.

### Path C (watchlist)

- **State idempotência:** rodar `watch.sh` duas vezes seguidas numa página. Segunda execução é no-op (cadence bloqueia) até `last_run + cadence` expirar.
- **Diff correto:** seed `known_urls` com 3 URLs, mockar WebSearch retornando 4 URLs (uma nova), verificar que só a nova aparece como `[watch-hit]`.

## Rollout

Ordem sugerida (cada fase commitável independente):

1. **Fase 1 — Policy.** Update `SCHEMA.md` + `CLAUDE.md` com Dated claims, Supersession, Watchlist, Lint §11. Zero mudança executável; contrato pronto para os próximos commits se ancorarem.
2. **Fase 2 — Path A (prompts).** Edit `wiki_plan.md` + `wiki_write.md`. Teste manual com uma página-cobaia.
3. **Fase 3 — Path B (lint).** `tools/lint.sh` + `dated_lint.py` + config + unit tests. Primeira run produz baseline report — esperado ser ruidoso, porque 0 das ~90 páginas tem `em:` hoje.
4. **Fase 4 — Path C (watch).** `tools/watch.sh` + `watch_runner.py` + state dir. Seed com 2-3 páginas (reforma_tributaria, cyrela, section_232) pra validar end-to-end.
5. **Fase 5 (fora desta spec) — Retrofit manual.** Pass nas 5 páginas legais de alta prioridade, adicionando `em:` nos claims datáveis. Opcional seguir com páginas de empresa conforme necessidade.

## Open Questions

- **Gitignore de `sources/watch_state/`?** Estado é cache — reinicia sem perda funcional (primeira run após limpeza só gera ruído). Argumento pró-commit: audit de quando cada watch rodou. Decidir no plano.
- **Formato do relatório do lint — markdown só, ou JSON + markdown?** JSON facilita consumo programático (ex: CI check futuro). Markdown é suficiente para triagem humana. Sugestão: começar só markdown, adicionar JSON se surgir consumidor.
- **`em:` em tabelas** — quando uma tabela tem múltiplas linhas com origens diferentes, a citação atual é geralmente uma só abaixo da tabela. Como datar por-linha sem duplicar? Proposta: citação única abaixo da tabela com o `em:` mais recente; se houver origens com datas materialmente diferentes, quebrar em tabelas separadas.
