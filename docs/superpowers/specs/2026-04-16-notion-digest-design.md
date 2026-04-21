# Sprint 1 — Notion Digest Pipeline + Number Guard

**Status:** implemented (2026-04-16). See § Amendments for design changes made during implementation.
**Date:** 2026-04-16
**Owner:** diogobodas

## Context & Motivation

O projeto equity-wiki já tem pipelines de ingestão para CVM (fetch.sh) e YouTube (fetch_calls.sh) mas não absorve notas do analista — reuniões com IR, calls internas, research notes, insights. Essas informações hoje vivem num database Notion chamado Capstone (ID 27800ca32bce808e8d10fc56c074db9b).

A visão de longo prazo é ser assistente de equity research completo, absorvendo todo input relevante para modelagem futura. Este sprint adiciona o Notion como fonte e, oportunisticamente, embute o primeiro mecanismo estrutural anti-alucinação — um validador de números (Number Guard) — já que construir um pipeline novo permite nascer com garantias de qualidade desde o início.

Dor concreta que motiva o Number Guard: agentes inventam números quando não têm o dado explícito na fonte (confirmado em P2-ii da brainstorming session).

## Goals

1. Importar páginas do Notion Capstone para o pipeline de ingest existente, reutilizando ao máximo a mecânica já provada (full/ imutável, digest cita, wiki_queue, wiki_update).
2. Introduzir validação automática de números na saída dos agentes: todo número no digest precisa ter rastro na fonte declarada ou é marcado [?].
3. Manter o design desacoplado — Notion fetch e Number Guard são componentes independentes, testáveis em isolamento.

## Non-Goals (Sprint 1)

- Sync bi-direcional (digesteds → páginas Notion de volta).
- Webhooks do Notion para ingest reativo a edições.
- Captura de histórico de versões Notion.
- Validação semântica de paráfrase (P2-iii) — Guard v1 valida apenas números.
- Retrofit do Number Guard nos pipelines CVM/calls existentes (follow-up separado).
- Detecção de mistura de períodos/empresas (P2-iv).

## Architecture

Fluxo completo:

1. Notion Capstone database → fetch_notion.sh varre DB, acha páginas com ingest=pending.
2. sources/undigested/notion_{slug}.md — markdown + frontmatter YAML.
3. ingest.sh --notion <file>.
4. sources/full/generic/notas/{slug}.md — preservado integral (sempre em generic).
5. claude --print + prompt ingest_notion.md → sources/digested/notion_{slug}_summary.md com citações (fonte: ...).
6. number_guard.py check → números com match ficam; sem match são marcados [?] inline + relatório auxiliar.
7. wiki_queue.py enqueue.
8. Notion API: marca ingest=done (último passo, após sucesso de tudo).
9. wiki_update.sh (existente) consome queue.

Dois componentes claramente separados:

- **Componente 1 — Notion Bridge:** I/O puro, sem LLM. Notion API → markdown no disco.
- **Componente 2 — Number Guard:** validador pós-digest, reutilizável em qualquer pipeline.

## Component 1: Notion Bridge

### Configuration

sources/manifests/_notion.json:

    {
      "database_id": "27800ca32bce808e8d10fc56c074db9b",
      "database_name": "Capstone",
      "integration_token_env": "NOTION_TOKEN",
      "ingest_property": "ingest",
      "pending_value": "pending",
      "done_value": "done",
      "title_property": "Name",
      "tag_properties": ["empresa", "tipo", "data"]
    }

Token Notion lido de NOTION_TOKEN env var. Nunca hardcoded. .gitignore já cobre .env.

### Library: tools/lib/notion_fetch.py

Funções puras e testáveis:

- list_pending(config) → list[dict] — POST /v1/databases/{id}/query com filter ingest=pending.
- fetch_page_blocks(page_id) → list[dict] — GET /v1/blocks/{id}/children recursivo (sub-blocos para toggles e colunas).
- blocks_to_markdown(blocks) → str — converte para markdown. Suporte v1: headings h1-h3, paragraphs, bullets, numbered, tables simples, code, quotes. Blocos não-suportados geram linha "> [bloco não-suportado: {type}]" e aviso stderr. Não falha.
- mark_done(page_id) → bool — PATCH /v1/pages/{id} com properties.ingest=done. Só chamada após ingest completo.

Cliente HTTP: requests (ou httpx reusando dependência de cvm_fetch.py — decidido na implementação, ambos aceitáveis).

Rate limiting: Notion permite 3 req/s. Backoff exponencial em 429.

### Orchestrator: tools/fetch_notion.sh

- bash tools/fetch_notion.sh — processa todas pending.
- bash tools/fetch_notion.sh --page <id> — força página específica.
- bash tools/fetch_notion.sh --discover — lista pending sem baixar (debug).

Para cada página pending:

1. Busca blocos (recursivo).
2. Converte para markdown.
3. Extrai properties para frontmatter YAML com source, notion_page_id, notion_url, title, created, edited, properties (empresa, tipo, data).
4. Grava em sources/undigested/notion_{slug}_{short_id}.md.

Slug: {empresa}_{tipo}_{data} quando properties existem; senão title_slugified_{short_id}. short_id = primeiros 8 chars do page_id.

Não marca ingest=done aqui — só após ingest.sh concluir com sucesso (fecha o loop idempotente: se ingest falha, página volta para pending no próximo fetch).

## Ingest Route

### Prompt: tools/prompts/ingest_notion.md

Variante enxuta do ingest_generic.md, adaptada para notas Notion. Instruções chave:

- Lê frontmatter + body.
- Copia o arquivo inteiro para sources/full/generic/notas/{slug}.md (preservação integral, como todos os ingest).
- Produz sources/digested/notion_{slug}_summary.md com:
  - TL;DR factual com citações no formato (fonte: full/generic/notas/{slug}.md §seção).
  - Para cada claim factual, citação obrigatória inline.
  - Regra explícita: preferir números primários diretamente da fonte; evitar cálculos derivados não-explícitos. Se precisar derivar, cita os inputs.
  - Quando o dado não estiver na fonte, escrever n/d — nunca estimar, aproximar ou interpolar.

### Orchestrator change: tools/ingest.sh --notion <file>

Adiciona nova rota:

    bash tools/ingest.sh --notion sources/undigested/notion_cury_reuniao_ir_2026-04-10.md

Passos:

1. Lê frontmatter para extrair page_id, slug.
2. Copia arquivo para sources/full/generic/notas/{slug}.md (preservação verbatim).
3. Invoca claude --print com ingest_notion.md produzindo sources/digested/notion_{slug}_summary.md.
4. Chama number_guard.py check no digest. Marca números órfãos com [?] in-place. Gera notion_{slug}_guard_report.md apenas se houver [?].
5. Chama wiki_queue.py enqueue.
6. Chama notion_fetch.mark_done(page_id) — último passo, só se tudo acima passou.
7. Remove arquivo de sources/undigested/.

## Component 2: Number Guard

### Library: tools/lib/number_guard.py

Funções puras:

- extract_numbers(text) → list[NumberClaim] — regex PT-BR:
  - Percentuais: 28,5%, 28.5%, 28,50 %
  - Monetário: R$ 1.234,56, R$ 1,2 bi, R$ 1.234 mm, R$ 1.234 milhões, R$ 1.987 mil
  - Inteiros grandes: 1.234.567, (245) para negativos entre parênteses
  - Unidade inferida; valor normalizado em float.
  - Contexto: ±40 chars ao redor.
  - Âncora de citação: última (fonte: ...) que precede a linha da ocorrência.
- index_source(full_path) → SourceIndex — extrai todos números da fonte, indexa por round(value, 6). Cada entrada guarda (line_no, contexto local).
- match_claim(claim, index) → MatchResult — retorna:
  - MATCH_STRICT — valor dentro de tolerância E palavra-chave do contexto do claim aparece no contexto da fonte.
  - MATCH_LOOSE — valor dentro de tolerância mas contextos não sobrepõem.
  - NO_MATCH — valor fora de tolerância em todas as ocorrências.
- annotate(digest_path, results) → str — reescreve o digest in-place inserindo [?] imediatamente após cada número com resultado NO_MATCH. MATCH_LOOSE apenas registra no relatório, não marca [?].

### Tolerance (C1 answer)

- Valores absolutos: tolerância ±0,5 em unidade percentual. Ex: 28,5% matcheia com 28,3% ou 29,0% mas não com 27,9%.
- Valores monetários e inteiros: tolerância ±0,5% relativa (evita match inadvertido). Ex: R$ 1.234 mm matcheia com R$ 1.240 mm mas não com R$ 1.300 mm.
- Normalização prévia:
  - Separadores: 28,5 ≡ 28.5
  - Zeros à direita: 28,5 ≡ 28,50
  - Unidades: R$ 1,2 bi ≡ R$ 1.200 mm ≡ R$ 1.200.000 mil (converte para unidade canônica)
  - Negativos: (245) ≡ -245

### Report generation (C2 answer)

Relatório auxiliar sources/digested/{slug}_guard_report.md é gerado apenas quando há NO_MATCH (pelo menos um [?]). Formato inclui summary (totals), tabela de No Match claims, tabela de Loose Match claims.

### Scope (C3 answer)

Number Guard é chamado apenas na rota ingest.sh --notion no Sprint 1. Retrofit nos pipelines CVM e calls fica como follow-up separado.

### Limitações conscientes

Documentadas no próprio ingest_notion.md como regras pro agente:

- Cálculo derivado: se agente calcula crescimento de 12% de duas receitas, o 12% pode não estar literalmente na fonte. Prompt instrui preferir citar os inputs, não o derivado.
- Dados agregados multi-período: evitar média X% nos últimos 4T. Prefere citar o range.
- Paráfrase sem número: Guard não cobre. Fica para futura iteração com validação semântica.

## Tests

### tests/test_number_guard.py

Seis casos de aceitação, todos implementados antes de integração:

1. Happy path: digest cita 28,5% + fonte menciona margem bruta de 28,5% no 3T25 → MATCH_STRICT, nenhum [?].
2. Invenção pura: digest cita 99,9% + fonte não tem esse número → NO_MATCH, marca [?].
3. Separadores diferentes: digest cita 28.5%, fonte cita 28,5% → MATCH_STRICT.
4. Contexto distante: digest cita 28,5% de margem bruta, fonte tem 28,5% numa seção falando de IR → MATCH_LOOSE, não marca [?] mas entra no report.
5. Unidade equivalente: digest cita R$ 1,2 bi, fonte diz R$ 1.234 milhões → MATCH_STRICT (valor normalizado dentro da tolerância).
6. Negativo: digest cita prejuízo de R$ (245) mm, fonte tem -245 → MATCH_STRICT.

### Manual integration test

Após implementação, testa end-to-end com uma página Capstone real. Valida:

- Notion API responde ok.
- Página chega em undigested/ com frontmatter correto.
- Digest é produzido com citações válidas.
- Guard pega pelo menos um número e valida contra a fonte.
- Página é marcada ingest=done no Notion.

## Rollout Plan

Cinco commits independentes:

1. Notion bridge — notion_fetch.py, fetch_notion.sh, config. Testa listagem da Capstone end-to-end sem ingest.
2. Ingest prompt + route — ingest_notion.md, rota --notion em ingest.sh. Testa fluxo sem Guard.
3. Number Guard — number_guard.py com todos os 6 testes unitários passando.
4. Integração — Guard é invocado em ingest.sh --notion após digest, antes do enqueue.
5. Docs — CLAUDE.md (seção Notion + Guard), link deste spec.

## Risks & Mitigations

- Notion API rate limit (3 req/s): backoff exponencial em 429. Sleep entre requests.
- Blocks→markdown perde nuances (toggles aninhados, databases embarcados): v1 cobre tipos comuns. Blocos não-suportados geram warning stderr. Não falha.
- Página muito grande (>20 MB): trunca com aviso; preserva integral em undigested/ para retry manual.
- Agente escreve número sem citação próxima: Guard sem âncora marca [?] mesmo assim (falha em favor de cautela).
- Falso positivo do Guard (número correto, contexto diferente): modo suave não quebra pipeline; MATCH_LOOSE registra sem marcar. Se incidência alta, ajustar regex de contexto.
- Token Notion vazar: leitor .env obrigatório. .gitignore cobre .env.
- Marcar ingest=done mas processo falhar depois: marcação é o último passo, só após Guard + enqueue. Se falha em etapa anterior, página fica pending para retry.
- Regex numérica PT-BR com edge cases (ex: 1.234,56789, notação científica): suite de testes cobre casos comuns. Casos exóticos: Guard não reconhece como número; prompt instrui agente a citar formatos padrão.

## Deliverables

Arquivos novos:

- tools/lib/notion_fetch.py
- tools/lib/number_guard.py
- tools/fetch_notion.sh
- tools/prompts/ingest_notion.md
- sources/manifests/_notion.json
- tests/test_number_guard.py
- docs/superpowers/specs/2026-04-16-notion-digest-design.md (este doc)

Arquivos modificados:

- tools/ingest.sh — adiciona rota --notion
- CLAUDE.md — seção Notion + Number Guard

## Open Questions

Nenhuma pendente. Todas as decisões (B1, B2, B3, C1, C2, C3, D1) resolvidas na sessão de brainstorming.

## Estimate

~1 dia de implementação + testes. Cinco commits independentes.

## Amendments (post-implementation)

Feitas durante a implementação de 2026-04-16. O spec acima ficou preservado para histórico; estas são as diferenças em relação ao que foi de fato construído.

### A1. State tracking substitui a propriedade `ingest` no Notion (Componente 1)

**Motivo.** O banco Capstone real não tem a propriedade `ingest` (pending/done) nem as propriedades `empresa`, `tipo`, `data` assumidas pelo spec. Schema observado:

- `Segmento (AI)` — tipo `title` (é o campo de título, nome peculiar)
- `Tags` — tipo `multi_select` (50+ opções: empresas, setores, temas)
- `Criado em` — created_time (auto)
- `Atualizado` — last_edited_time (auto)

**Implementação.** Opção D aprovada pelo usuário:

- Trigger de ingest agora é **client-side**, comparando `last_edited_time` de cada página com `sources/manifests/_notion_state.json.processed_pages[page_id]`. Uma página é "pendente" se nunca foi processada ou foi editada desde o último processamento.
- `fetch_notion.sh` lista TODAS as páginas e filtra no cliente. Sem filter no query do Notion.
- `mark_done` (PATCH no Notion) foi trocado por `mark_processed(page_id, last_edited_time)` local — atualiza apenas o state file. Nenhuma escrita no Notion.
- `empresa` é inferido cruzando `Tags` com `known_empresas` + `tag_to_empresa` em `sources/manifests/_notion.json`. Primeiro match vence; sem match → `generic`.
- Frontmatter na nota salva em `sources/undigested/notion_<slug>.md` inclui `notion_page_id`, `notion_url`, `title`, `created`, `edited`, `empresa`, `tags`.

### A2. Destination & queue semantics

- `full/` destination é `sources/full/generic/notas/<slug>.md` (subdir `notas/` conforme spec; `mkdir -p` explícito na rota).
- Queue entry: `type: notion`, `empresa` parseado do frontmatter (não hard-coded como `generic`), `periodo` é o slug. `wiki_update.sh` consome sem precisar conhecer `type: notion` — ele só lê os digesteds.
- Rejeição explícita em `ingest.sh --notion`: exige `source: notion` no frontmatter antes de processar. Evita ingest acidental de arquivos não-Notion.

### A3. Number Guard tolerances — test case 5

O exemplo do spec (`R$ 1,2 bi` vs `R$ 1.234 milhões → MATCH_STRICT`) é inconsistente com a tolerância declarada de ±0,5 % relativa para monetário (a diferença real é ~2,8 %). Duas possibilidades: (a) o spec errou o exemplo, (b) a tolerância deveria ser maior para valores arredondados.

**Resolução.** Implementada a tolerância literal (±0,5 %). O teste 5 em `tests/test_number_guard.py` usa `R$ 1,234 bi` vs `R$ 1.234 milhões` (ambos = 1,234 bi reais exatamente) — testa a lógica de conversão de unidade sob tolerância estrita. A questão "tolerância dinâmica para arredondamentos" fica como follow-up se gerar falsos-negativos no uso real.

### A4. Extractor filters (reduz false positives no uso real)

Adicionados ao `extract_numbers` (não documentados no spec v0):

- **Frontmatter** é pulado por padrão (`skip_frontmatter=True`).
- **Spans de `(fonte: …)`** são excluídos da extração — senão o próprio caminho citado geraria claims falsos (ex: partes numéricas de UUIDs).
- **Datas** (`YYYY-MM-DD`, `DD/MM/YYYY`, anos isolados `19xx`/`20xx`) são puladas.
- **Markers de lista e headings numerados** (`- 1.`, `## 2. …`, `### 3.1 …`) são pulados.
- **Identificadores compostos** (`K6-2`, `8086/286`, `3T25`) são rejeitados via boundary check estendido — letras ou alfanuméricos adjacentes a hyphens/slashes indicam model IDs, não claims numéricos.

### A5. Guard scope & failure semantics

Guard roda em `ingest.sh --notion` após o digest, antes do enqueue. Encontrar NO_MATCH **não falha** o pipeline — marca inline com `[?]`, escreve `{slug}_guard_report.md`, e segue para enqueue + mark_processed. A filosofia é "digest ainda é útil, só que com sinalização explícita do que o leitor deve verificar". Se o guard em si errar (exception), o pipeline para e `mark_processed` não roda — página fica pending para retry.

## Security follow-up

`NOTION_TOKEN` foi colado no transcript de chat em 2026-04-16. Recomendação: criar nova integração Notion e revogar a antiga após a validação do Sprint 1.

