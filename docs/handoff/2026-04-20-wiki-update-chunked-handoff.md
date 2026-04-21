# Handoff — Notion wiki_update --full chunked (2026-04-20)

**Status no momento da pausa (10:50, sessão pausada por rate limit Anthropic):**

- Background task `byh0cgio5` rodando `bash tools/wiki_update.sh --full` (PID indeterminado)
- 656 digesteds, 14 chunks de 50, Phase 1 chunked
- Estava em **chunk 6/14** quando salvei estado
- 4/14 chunks completos: 1, 2, 3, 5 (chunk 4 falhou parse)
- Phase 2 ainda **não começou**
- 0 escrita destrutiva em wiki pages (só `cury.md` + `cyrela_vs_cury.md` do test prévio)

## O que mudou nesta sessão (commits a fazer)

**Bug diagnóstico:** sex 17/4 às 20:10, `wiki_update.sh --full` foi relançado e travou silenciosamente. Memória estável ~170MB por 2.5 dias. Diagnóstico: planner LLM lê cada digest individualmente via Bash (`cat`); com 515+ digests, vira 515 tool-call turns sequenciais → contexto satura → LLM stalla sem erro. Confirmado empiricamente: 10 digests = ~2min ✓; 100 digests (chunked 2x50) = ~25min ✓; 656 digests = trava.

**Fix implementado (Option A — chunked planner):**

1. **Novo `tools/lib/merge_wiki_plans.py`** — recebe N JSONs (um por chunk), merge dedup:
   - `create` + `create` mesma page: union digesteds, type do primeiro
   - `update` + `update`: idem
   - `create` + `update` mesma page: prefere CREATE, merge digesteds dentro
   - `skip` dropado se page também aparece em update/create
2. **Novo `tools/lib/record_chunk_failure.py`** — persiste falhas de chunk:
   - chunk_idx, reason (`invoke_claude_nonzero` ou `parse_failed`), lista de digesteds, output_tail (4KB)
   - Escreve em `logs/wiki_plan_failures_<ts>.json`
3. **`tools/wiki_update.sh` editado:**
   - `invoke_claude` agora aceita `INVOKE_CLAUDE_TIMEOUT` env var (segurança contra hangs futuros)
   - Phase 1 substituída por loop chunked (linhas ~141-220):
     - Slice `DIGESTED_LIST` em chunks via Python heredoc
     - Loop de chunks com `INVOKE_CLAUDE_TIMEOUT="$CHUNK_TIMEOUT"` exportado
     - Tolerance: chunks falhos são logados mas não derrubam o run
     - Merge final via `merge_wiki_plans.py`
   - Tunables: `WIKI_PLAN_CHUNK_SIZE` (default 50), `WIKI_PLAN_CHUNK_TIMEOUT` (default 1200s)

**Bugs fixados durante a implementação:**

- **Path Windows-bash:** `python -c "open(r'/tmp/...')"` não resolve `/tmp/` quando o path está dentro da string -c (MSYS só converte argv no boundary). Fix: trocar pra `cat "$OUT_FILE" | python -c "json.load(sys.stdin)"`.
- **Argv too long (já fixado em 17/04):** valores grandes em `invoke_claude` agora vão pra arquivo temp; só paths no cmdline.

## Estado salvo em disco (persistente)

```
logs/
├── wiki_full_real_20260420_1008.log          # stdout do real run (chunk progress)
├── wiki_plan_failures_20260420_101022.json   # 1 falha (chunk 4)
└── wiki_plan_partial_20260420_104930/        # backup dos chunks salvos antes de /tmp ser wiped
    ├── chunk_001.json   # OK: c=1 u=3 s=34
    ├── chunk_002.json   # OK: c=2 u=10 s=27
    ├── chunk_003.json   # OK: c=9 u=3 s=12
    └── chunk_005.json   # OK: c=7 u=13 s=23
```

Note: chunk 4 falhou (não tem .json). Os digests dele estão em `wiki_plan_failures_20260420_101022.json`.

## Como retomar quando rate limit voltar

### Opção 1 (RECOMENDADA — simples, idempotente)

Rerun `--full` from scratch quando o limite resetar. Custos:
- Repete o trabalho dos chunks já feitos (4 × ~7min = 28min de Phase 1 redundante)
- Mas é 100% determinístico e não exige nova lógica
- Phase 2 (que ainda não começou) não desperdiça nada

```bash
cd C:/Users/diogo.bodas/Desktop/Equity-wiki/equity-wiki
# Primeiro: confirmar que background task antigo morreu
tasklist | grep claude  # se tiver muitos, kill antes
# Lançar:
LOG="logs/wiki_full_real_$(date +%Y%m%d_%H%M).log"
WIKI_PLAN_CHUNK_SIZE=50 WIKI_PLAN_CHUNK_TIMEOUT=1200 \
  timeout 43200 bash tools/wiki_update.sh --full 2>&1 | tee "$LOG"
```

### Opção 2 (mais eficiente — pula chunks já feitos)

Implementar `--resume-from <partial_dir>` em `wiki_update.sh`:
- Lê chunk_*.json existentes do diretório
- Identifica os digesteds NÃO cobertos por chunks bem-sucedidos
- Roda planner só nesses
- Merge final igual ao normal

Trabalho: ~30min de implementação. Worth it se rate limit reseta cedo e queremos minimizar tempo até Phase 2.

### Opção 3 (intermediária — re-run e rezar)

Mover os chunks salvos pra um novo /tmp dir e ENVIAR pra script — mas script atualmente sempre cria seu próprio tmpdir. Precisaria patch.

## Verificações antes de retomar

```bash
# 1. Background task morto?
tasklist //FI "IMAGENAME eq claude.exe" //FO CSV | wc -l   # se > 5, kill antigos
# Listar:
tasklist //FI "IMAGENAME eq claude.exe" //FO CSV

# 2. Sanity check API auth
echo "ping" | claude --print

# 3. Estado dos digesteds
ls sources/digested/*_summary.md | wc -l   # esperado: 656
ls sources/_digested_stash/ 2>/dev/null    # esperado: vazio (já restaurado)

# 4. Queue (pra wiki_update incremental, não usado em --full)
python tools/lib/wiki_queue.py peek --count   # esperado: ~514
```

## Métricas observadas (sessão 2026-04-20)

| Run | Digests | Chunks | Tempo Phase 1 | Sucesso | Falhas |
|---|---:|---:|---|---|---|
| Test 1 (path bug) | 100 | 2 | crashed após chunk 1 | — | path fix needed |
| Test 2 (post-fix) | 100 | 2 | ~13min | 1/2 chunks | 1 parse_failed |
| Real (parcial) | 656 | 14 | em progresso (chunk 6/14 em ~42min) | 4/14 até agora | 1 parse_failed |

**Pace estimado:** ~7-8min/chunk. Phase 1 completa estimada: ~110min. Phase 2 estimada: 3-10h dependendo do tamanho do plan merged.

## Commits pendentes (não fiz commit ainda)

Mudanças não commitadas em:
- `tools/wiki_update.sh` (chunked Phase 1 + timeout invoke_claude)
- `tools/lib/merge_wiki_plans.py` (NEW)
- `tools/lib/record_chunk_failure.py` (NEW)
- `docs/handoff/2026-04-20-wiki-update-chunked-handoff.md` (este arquivo, NEW)

Sugestão de commit message:
```
feat(wiki_update): chunked Phase 1 planner + failure capture

Phase 1 planner hung silently on 515+ digests because the prompt
instructs the LLM to `cat` each digest via Bash — 515 sequential
tool calls saturate context until the LLM stalls.

Fix: chunk DIGESTED_LIST into bounded batches (default 50), run
planner per chunk, merge JSON plans. Tolerates per-chunk failures
(logged to logs/wiki_plan_failures_*.json for re-processing).

Empirical: 10 digests ~2min ✓, 100 digests (2 chunks) ~25min ✓,
vs 515 digests >2h hang ✗ (pre-fix).
```
