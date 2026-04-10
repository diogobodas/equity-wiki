# Ingest Agent — Design Spec

**Data:** 2026-04-10
**Escopo:** Agente bash+claude que processa arquivos de `sources/undigested/` para produzir todas as camadas da wiki

---

## Objetivo

Um script `ingest.sh` que recebe um ticker, processa todos os arquivos pendentes em `undigested/` para aquela empresa, e produz as camadas completas da wiki: full/ → structured/ → digested/ → wiki pages → manifest → log. Automatiza o que hoje é feito manualmente com subagents.

## Decisões de design

| Decisão | Escolha |
|---------|---------|
| Escopo por invocação | Todos os arquivos de um ticker de uma vez |
| Batching LLM | Um `claude --print` por tipo (ITRs juntos, releases juntos, fatos juntos) + 1 wiki update |
| Pre-processing | `pdf_extract.py` — opendataloader primeiro, fallback pdfplumber |
| Como LLM recebe texto | Lê o arquivo extraído via bash (caminho no prompt) |
| Wiki update | Invocação separada no final, lê digested/ produzidos |
| Manifest/log/cleanup | Determinístico via `manifest_update.py`, sem LLM |

## Estrutura de arquivos

```
tools/
├── fetch.sh                       # (existe) Coleta CVM
├── ingest.sh                      # NOVO — entry point
├── prompts/
│   ├── fetch_system.md            # (existe)
│   ├── fetch_discover.md          # (existe)
│   ├── ingest_heavy.md            # NOVO — ITR/DFP/release → full/ + structured/ + digested/
│   ├── ingest_light.md            # NOVO — fatos relevantes → full/ + digested/
│   └── ingest_wiki_update.md      # NOVO — atualiza wiki pages a partir dos digested/
└── lib/
    ├── cvm_fetch.py               # (existe)
    ├── pdf_extract.py             # NOVO — extrai texto de PDF/ZIP
    └── manifest_update.py         # NOVO — atualiza manifest/log/index
```

## Fluxo completo

```
bash tools/ingest.sh TEND3
  │
  ├─ 1. SCAN — lista arquivos em undigested/ que matcham o ticker
  │     Classifica por tipo baseado no nome do arquivo:
  │     - *_itr.zip / *_dfp.zip → heavy (ITR/DFP)
  │     - *_release_*.pdf → heavy (release)
  │     - *_fato_relevante_*.pdf → light
  │
  ├─ 2. PRE-PROCESS — para cada arquivo:
  │     python tools/lib/pdf_extract.py <arquivo>
  │     → ZIP: extrai PDF interno, depois extrai texto
  │     → PDF: extrai texto direto
  │     → Tenta opendataloader-pdf primeiro, fallback pdfplumber
  │     → Produz: {nome}_extracted.md no mesmo diretório
  │
  ├─ 3. INGEST HEAVY (ITR/DFP) — um claude --print para o batch
  │     Prompt: ingest_heavy.md com lista de arquivos extraídos
  │     O LLM lê cada _extracted.md via bash, produz:
  │     → sources/full/{empresa}/{periodo}/{tipo}.md
  │     → sources/structured/{empresa}/{periodo}/{tipo}.json
  │     → sources/digested/{empresa}_{tipo}_{periodo}_summary.md
  │
  ├─ 4. INGEST HEAVY (releases) — um claude --print para o batch
  │     Mesmo prompt e output que passo 3
  │
  ├─ 5. INGEST LIGHT (fatos) — um claude --print para o batch
  │     Prompt: ingest_light.md
  │     → sources/full/{empresa}/{periodo}/fato_relevante_{seq}.md
  │     → sources/digested/{empresa}_fatos_relevantes_{periodos}_summary.md
  │     (sem structured/)
  │
  ├─ 6. WIKI UPDATE — um claude --print dedicado
  │     Prompt: ingest_wiki_update.md
  │     Lê os digested/ produzidos nos passos 3-5
  │     Atualiza {empresa}.md e páginas relacionadas
  │
  ├─ 7. MANIFEST/LOG — determinístico
  │     python tools/lib/manifest_update.py para cada arquivo ingerido
  │     → sources[], coverage, precedence no manifest
  │     → Append log.md
  │     → Atualiza sources/index.md
  │
  └─ 8. CLEANUP
        → Deleta originais + _extracted.md de undigested/
```

## Componentes

### `pdf_extract.py`

CLI stateless, JSON stdout. Subcomandos implícitos por extensão.

```bash
python tools/lib/pdf_extract.py sources/undigested/TEND3_3T25_itr.zip
→ {"status": "ok", "output": ".../_extracted.md", "pages": 95, "chars": 244926, "method": "opendataloader"}

python tools/lib/pdf_extract.py sources/undigested/TEND3_4T25_release_1010843.pdf
→ {"status": "ok", "output": ".../_extracted.md", "pages": 33, "chars": 86840, "method": "pdfplumber"}
```

- ZIP: extrai o PDF de dentro (procura `*.pdf` no ZIP), depois processa
- Tenta opendataloader-pdf: `python -m opendataloader_pdf <file> --format markdown --use-struct-tree --table-method cluster`
- Se falhar (PDF padded, erro de parsing): fallback pdfplumber (page-by-page `extract_text()`)
- Output: `{nome_sem_extensao}_extracted.md` com `<!-- PAGE N -->` markers
- Erro: `{"status": "error", "message": "..."}`

### `manifest_update.py`

Atualiza manifest, log e index deterministicamente.

```bash
python tools/lib/manifest_update.py \
  --manifest sources/manifests/tenda.json \
  --type itr --period 3T25 \
  --full sources/full/tenda/3T25/itr.md \
  --structured sources/structured/tenda/3T25/itr.json \
  --digested sources/digested/tenda_itr_3T25_summary.md

python tools/lib/manifest_update.py \
  --manifest sources/manifests/tenda.json \
  --type fato_relevante --period 3T25 \
  --full sources/full/tenda/3T25/fato_relevante_930915.md \
  --digested sources/digested/tenda_fatos_relevantes_3T25_summary.md
```

- Adiciona entry em `sources[]` (`type`, `asof`, `ingested_on`, `full`, `structured`, `digested`)
- Atualiza `coverage` para heavy path: `dre`/`bp` → filled (ITR/DFP), `financeiro_ajustado` → filled (release)
- Atualiza `_updated`
- Append em `log.md`: data, tipo, periodo, arquivos produzidos
- Atualiza `sources/index.md`

### Prompts

**`ingest_heavy.md`** — Instrui o LLM a processar ITR/DFP/release:
- Contexto: ticker, empresa, lista de arquivos extraídos com caminhos, schema incorporadora
- O LLM lê cada arquivo via bash, produz full/ (uncut transcription), structured/ (canonical JSON), digested/ (TL;DR)
- Usa DFs consolidadas, números em R$ mm
- Para releases: preenche operacional + financeiro_ajustado (métricas gerenciais)
- Para ITR/DFP: preenche dre + bp + o que encontrar de financeiro_ajustado

**`ingest_light.md`** — Instrui o LLM a processar fatos relevantes:
- Contexto: ticker, empresa, lista de arquivos extraídos
- Produz full/ (transcrição uncut) + digested/ (resumo combinado por período)
- Sem structured/

**`ingest_wiki_update.md`** — Instrui o LLM a atualizar wiki pages:
- Contexto: ticker, empresa, lista de digested/ produzidos nesta sessão
- Lê cada digested/, lê a página wiki atual ({empresa}.md)
- Atualiza/adiciona seções com dados novos + citações corretas
- Format citations: `(fonte: structured/...json :: canonical.dre.receita_liquida)` para numeric, `(fonte: full/...md §section)` para qualitative

### `ingest.sh`

Entry point bash. Responsabilidades:
1. Parse args: ticker obrigatório
2. Scan `undigested/` por arquivos do ticker
3. Classifica por tipo (nome do arquivo)
4. Resolve manifest (como no fetch.sh)
5. Pre-process: loop chamando `pdf_extract.py`
6. Invoca `claude --print` para cada batch (heavy ITR/DFP, heavy release, light fatos)
7. Invoca `claude --print` para wiki update
8. Chama `manifest_update.py` para cada arquivo processado
9. Cleanup undigested/
10. Imprime resumo

## Fora de escopo

- Ingest de data_pack (XLSX) — lógica diferente com delta detection
- Ingest web/notion
- Validação cruzada com data_pack existente (restatement detection)
- Processamento paralelo de múltiplos tickers
- Retry/resiliência — se o `claude --print` falha, o script para
