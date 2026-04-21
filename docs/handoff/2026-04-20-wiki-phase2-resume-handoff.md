# Handoff — Wiki Phase 2 Resume (2026-04-20)

**Status no momento da escrita (~15:05):**
- Phase 1 completa: 13/14 chunks OK, 1 falha (chunk 7 `parse_failed`)
- Merged plan salvo em: `logs/wiki_plan_merged_20260420.json`
- Chunk JSONs salvos em: `logs/chunk_001.json` … `chunk_014.json` (13 arquivos)
- Phase 2 em andamento — ~11 páginas escritas, rodando `caixa_seguridade.md`
- Processo background: PID 25156 / `timeout.exe` 2448 (run termina em ~15h se necessário)

## Plano completo (merged)

`logs/wiki_plan_merged_20260420.json`:
- **create=52** páginas novas
- **update=27** páginas existentes
- **skip=60** páginas sem mudança

Total Phase 2: **79 páginas** a escrever.

## Páginas já escritas (~15:05)

```
agibank.md, armac.md, atg.md, automob.md, banco_do_brasil.md,
banco_pine.md, banco_votorantim.md, bb_seguridade.md, cashme.md, moura_dubeux.md
```
(verificar `find . -maxdepth 1 -name "*.md" -mmin -300 …` para lista atual)

## O que fazer se o processo morrer antes de terminar

### Opção 1 — RECOMENDADA: script de resume

```bash
cd C:/Users/diogo.bodas/Desktop/Equity-wiki/equity-wiki

# Verificar quais páginas já existem (serão puladas automaticamente)
find . -maxdepth 1 -name "*.md" -not -name "CLAUDE.md" -not -name "README.md" \
       -not -name "SCHEMA.md" -not -name "log.md" -not -name "index.md" | sort

# Rodar Phase 2 com skip das já escritas:
LOG="logs/wiki_resume_phase2_$(date +%Y%m%d_%H%M).log"
WIKI_CLAUDE_MODEL=sonnet WIKI_WRITE_TIMEOUT=1800 \
  bash tools/wiki_resume_phase2.sh \
  --plan logs/wiki_plan_merged_20260420.json \
  2>&1 | tee "$LOG"
```

O script `wiki_resume_phase2.sh`:
- Lê o plano salvo
- Pula páginas `create` que já existem no disco
- Re-roda páginas `update` sempre (idempotente)
- Tolerance: falhas por página são logadas, run não aborta
- Usa `WIKI_CLAUDE_MODEL=sonnet` para economizar tokens

### Opção 2 — Re-run completo (mais lento, idempotente)

```bash
LOG="logs/wiki_full_real_$(date +%Y%m%d_%H%M).log"
WIKI_CLAUDE_MODEL=sonnet WIKI_PLAN_CHUNK_SIZE=50 WIKI_PLAN_CHUNK_TIMEOUT=1200 \
  WIKI_WRITE_TIMEOUT=1800 \
  timeout 54000 bash tools/wiki_update.sh --full 2>&1 | tee "$LOG"
```

Repete Phase 1 (~100min) mas é garantidamente correto.

## Verificações antes de retomar

```bash
# 1. Processo original morto?
wmic process where "CommandLine like '%wiki_update%'" get ProcessId

# 2. Auth ok?
echo "ping" | claude --print

# 3. Quantas páginas já no disco?
find . -maxdepth 1 -name "*.md" -not -name "CLAUDE.md" -not -name "README.md" \
       -not -name "SCHEMA.md" -not -name "log.md" -not -name "index.md" | wc -l
# Antes da run havia 37. Se > 37, Phase 2 progrediu.

# 4. Plano salvo ainda existe?
python -c "import json; p=json.load(open('logs/wiki_plan_merged_20260420.json',encoding='utf-8')); print('create='+str(len(p['create']))+' update='+str(len(p['update'])))"
```

## Pós Phase 2: o que resta

1. **Reprocessar chunks falhos** (chunk 7 — 50 digesteds):
   ```bash
   python -c "import json; d=json.load(open('logs/wiki_plan_failures_20260420_132530.json',encoding='utf-8')); [print(r['digesteds_count'], 'digesteds no chunk', r['chunk_idx'], r['reason']) for r in d]"
   ```
   Estratégia: isolar os digesteds do chunk 7 numa lista e rodar `--full` com só eles.

2. **Commit** das mudanças:
   - `tools/wiki_update.sh` (model flag + Phase 2 tolerance)
   - `tools/wiki_resume_phase2.sh` (NEW)
   - `tools/lib/merge_wiki_plans.py` (NEW, da sessão anterior)
   - `tools/lib/record_chunk_failure.py` (NEW, da sessão anterior)
   - Todas as wiki pages geradas (`*.md` na raiz)

## Métricas (run 2026-04-20)

| Fase | Status | Detalhe |
|------|--------|---------|
| Phase 1 | ✅ 13/14 ok | ~70min, chunk 7 parse_failed |
| Phase 2 | 🔄 em progresso | ~79 páginas, ~11 escritas |
| Modelo | sonnet | zero rate-limit failures em Phase 1 |
