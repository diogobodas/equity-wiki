# Fetch Agent — Design Spec

**Data:** 2026-04-10
**Escopo:** Agente LLM que coleta dados financeiros da CVM para alimentar o equity-wiki

---

## Objetivo

Um agente invocado via bash que recebe um ticker, consulta a CVM-API para descobrir documentos disponíveis, compara com o que a wiki já possui (via manifests), e baixa os documentos faltantes para `sources/undigested/`. Não faz ingest — apenas coleta.

## Decisões de design

| Decisão | Escolha |
|---------|---------|
| Tipo de agente | LLM (claude --print) com autonomia para interpretar manifests e decidir gaps |
| Escopo por invocação | Single ticker |
| Cold-start (sem manifest) | Cria manifest esqueleto + busca tudo até o horizonte |
| Tipos de documento (MVP) | DFP, ITR, earnings releases, fatos relevantes |
| Gap detection | Por período/tipo — compara manifest vs. catálogo CVM-API |
| Horizonte temporal | Configurável, default 3 anos |
| Naming em undigested/ | Flat: `{TICKER}_{periodo}_{tipo}.{ext}` (.zip for DFP/ITR, .pdf for IPE) |
| Direção de busca | Do presente para trás — para ao encontrar cobertura existente no manifest |
| Projeto | Vive no equity-wiki, independente do Equity-Analyst-Agent |

## Estrutura de arquivos

```
tools/
├── fetch.sh                # entry point
├── prompts/
│   └── fetch_system.md     # system prompt do agente LLM
└── lib/
    └── cvm_fetch.py        # CLI wrapper sobre a CVM-API
```

## Componentes

### 1. `fetch.sh` — entry point

```bash
bash tools/fetch.sh TEND3 [--horizon 3y] [--types dfp,itr,release,fato_relevante]
```

**Responsabilidades:**
1. Parse args (ticker obrigatório, horizon default `3y`, types default `dfp,itr,release,fato_relevante`)
2. Calcula `HORIZON_FROM` como data absoluta (hoje − horizon)
3. Resolve nome da empresa: faz grep pelo ticker em `sources/manifests/*.json`. Se encontrar, extrai o nome do arquivo (ex: `tenda.json` → `tenda`). Se não achar nenhum manifest com esse ticker, faz `python lib/cvm_fetch.py resolve` para obter o nome e seta `COLD_START=true`
4. Lê o manifest (ou seta `MANIFEST=null`)
5. Monta o prompt final: injeta variáveis no template `fetch_system.md`
6. Invoca `claude --print` com o prompt montado como user message, allowed tools: bash
7. Imprime o output do agente

**Não faz:** ingest, edição de wiki pages, validação de conteúdo.

### 2. `cvm_fetch.py` — CLI wrapper

Wrapper fino e stateless sobre o pacote `cvm-api`. Output sempre JSON. Três subcomandos:

```bash
# Resolve ticker → dados da empresa
python lib/cvm_fetch.py resolve TEND3
→ {"ticker": "TEND3", "nome": "Construtora Tenda S.A.", "cvm_code": "...", "setor": "..."}

# Lista documentos disponíveis na CVM (ordenados do mais recente ao mais antigo)
python lib/cvm_fetch.py list TEND3 --types dfp,itr,release,fato_relevante --from 2023-04-01
→ [{"id": "...", "tipo": "dfp", "periodo": "2025", "data_ref": "2025-12-31", "url": "..."}, ...]

# Baixa um documento
python lib/cvm_fetch.py download <doc_id> --output sources/undigested/TEND3_2025_dfp.pdf
→ {"status": "ok", "path": "sources/undigested/TEND3_2025_dfp.pdf", "size_bytes": 1234567}
```

**Design:**
- Erros retornam `{"status": "error", "message": "..."}` — o LLM decide como reagir
- `list` mapeia tipos CVM → tokens wiki (`dfp`, `itr`, `release`, `fato_relevante`)
- `list` normaliza períodos para formato wiki (`1T25`, `2T25`, `2025` etc.)
- Resultados ordenados do mais recente ao mais antigo (busca reversa)
- Sem estado, sem cache

### 3. `fetch_system.md` — system prompt

**Variáveis injetadas pelo fetch.sh:**
```
TICKER: TEND3
EMPRESA: tenda
MANIFEST: <conteúdo JSON ou "null">
HORIZON_FROM: 2023-04-01
TYPES: dfp,itr,release,fato_relevante
UNDIGESTED_PATH: sources/undigested
MANIFESTS_PATH: sources/manifests
```

**Instruções ao LLM:**
1. Identidade: agente de coleta de dados financeiros da CVM para o equity-wiki
2. Ferramentas: só bash para invocar `cvm_fetch.py`. Não edita wiki, não faz ingest.
3. Algoritmo:
   - Resolver empresa via `cvm_fetch.py resolve`
   - Listar documentos disponíveis via `cvm_fetch.py list`
   - Se tem manifest: iterar do presente para trás, identificar gaps (período/tipo na CVM mas não no manifest), parar ao encontrar cobertura existente ou atingir HORIZON_FROM
   - Se cold-start: tudo é gap até HORIZON_FROM; criar manifest esqueleto
   - Baixar cada gap via `cvm_fetch.py download` para `sources/undigested/{TICKER}_{periodo}_{tipo}.pdf`
4. Output: resumo do que baixou e o que ignorou

## Fluxo completo

```
bash tools/fetch.sh TEND3 --horizon 3y
  │
  ├─ 1. Parse args → TICKER=TEND3, HORIZON_FROM=2023-04-10, TYPES=dfp,itr,release,fato_relevante
  ├─ 2. Busca sources/manifests/tenda.json → encontra → COLD_START=false
  ├─ 3. Injeta variáveis em fetch_system.md
  └─ 4. claude --print
        │
        O LLM:
        ├─ a. cvm_fetch.py resolve TEND3
        ├─ b. cvm_fetch.py list TEND3 --types dfp,itr,release,fato_relevante --from 2023-04-10
        ├─ c. Itera do mais recente para trás:
        │     - 1T26/itr → não está no manifest → GAP → download
        │     - 2025/dfp → está no manifest → STOP para DFP
        │     - (repete por tipo)
        ├─ d. Download dos gaps para sources/undigested/
        └─ e. Imprime resumo
```

## Busca reversa cronológica

O agente itera do presente para o passado, por tipo de documento. Para cada tipo, para quando:
- Encontra um período que já existe no manifest para aquele tipo (cobertura existente), **ou**
- Atinge o `HORIZON_FROM`

No cold-start (sem manifest), varre tudo até o horizonte.

## Manifest esqueleto (cold-start)

Quando não existe manifest para a empresa, o agente cria:

```json
{
  "empresa": "tenda",
  "ticker": "TEND3",
  "setor": "incorporadora",
  "sources": [],
  "coverage": {},
  "precedence": [],
  "caveats": ["cold-start — manifest criado por fetch agent, pendente ingest"]
}
```

O ingest subsequente preenche `sources`, `coverage` e `precedence`.

## Dependências

- `pip install git+https://github.com/diogobodas/CVM-API.git`
- Claude CLI (`claude --print`)
- Python 3.10+

## Fora de escopo (futuro)

- Ingest (operação separada)
- Varredura multi-empresa
- Notícias, transcripts de calls, outras fontes
- Validação de conteúdo dos PDFs
- Retry/resiliência avançada
