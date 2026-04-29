# LLM Wiki — Tutorial

Uma wiki pessoal mantida por LLM, baseada no padrão descrito por [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), **estendida para servir também como substrato de modelagem financeira**.

A ideia central: em vez de re-derivar conhecimento do zero a cada pergunta (como RAG tradicional), o LLM **constrói e mantém incrementalmente** uma base de conhecimento persistente — um artefato que se acumula ao longo do tempo. Aqui a base tem dois usos complementares:

1. **Wiki de conhecimento** — páginas de empresas, conceitos, setores, comparações e teses.
2. **Substrato de modelagem** — fontes preservadas de forma estruturada para alimentar planilhas/modelos completos (ITR, DFP, releases de resultado, com notas explicativas e MD&A intactos).

O humano cuida das fontes e faz as perguntas certas. O LLM faz o trabalho pesado de transcrever, estruturar, cross-referenciar e manter tudo organizado.

---

## Como funciona

A wiki tem **quatro camadas** dentro de `sources/`, mais a camada de páginas da wiki por cima:

```
equity-wiki/
├── sources/
│   ├── undigested/                              # 1. Inbox — arquivos brutos
│   ├── full/{empresa}/{periodo}/{tipo}.md       # 2. Transcrição estruturada mas sem cortes
│   ├── structured/
│   │   ├── _schemas/{setor}.json                #    Schema canônico por setor (sob demanda)
│   │   └── {empresa}/{periodo}/{tipo}.json      # 3. Dados canonical + company_specific
│   ├── digested/{name}_summary.md               # 4. TL;DR para a wiki
│   ├── index.md                                 #    Registro de fontes
│   └── notion_tracker.md
├── *.md                                         # 5. Páginas da wiki (entity/concept/...)
├── index.md                                     #    Catálogo por categoria
├── log.md                                       #    Histórico append-only
├── SCHEMA.md                                    #    Contrato operacional
└── README.md                                    #    Este tutorial
```

### O que cada camada faz

| Camada | Perda de informação | Para que serve |
|--------|---------------------|----------------|
| `undigested/` | nenhuma | Inbox. Apagado depois do ingest. |
| `full/` | só layout/imagens | **O "chão"** — tudo que o PDF dizia, organizado em headings (DRE, BP, FC, Nota 1..N, MD&A). Literal dentro de cada seção. É daqui que a modelagem relê notas explicativas. Substitui guardar o PDF bruto. |
| `structured/` | só pega DFs + breakdowns | JSON determinístico que alimenta a planilha. `canonical` padronizado por setor + `company_specific` livre para o que cada empresa reporta do seu jeito. |
| `digested/` | editorial | TL;DR usado para escrever as páginas da wiki. |
| Wiki pages | síntese | Tese, conceitos, comparações. Cita as camadas de baixo. |

**Regra de ouro:** depois do ingest, o original em `undigested/` é apagado. `full/` é o novo chão — não existe `raw/`.

---

## Operações

### 1. Ingest de ITR / DFP / release de resultados (caminho pesado)

O workflow mais completo. Gera as quatro camadas.

1. Coloque o arquivo em `sources/undigested/` (PDF ou XLSX).
2. Peça ao LLM:

```
Ingere este ITR: sources/undigested/itau_itr_3T25.pdf
```

3. O LLM vai:
   - Ler a fonte inteira.
   - Gerar `full/itau/3T25/itr.md` — transcrição estruturada mas **sem cortar nada**. Cada nota explicativa vira um heading `## Nota N — título` com conteúdo literal.
   - Gerar `structured/itau/3T25/itr.json` — DRE, BP, FC, segmentos preenchidos no `canonical` (seguindo `_schemas/banco.json`), e breakdowns gerenciais idiossincráticos em `company_specific`. Se o schema setorial ainda não existe, o LLM cria a partir dessa primeira fonte.
   - Gerar `digested/itau_itr_3T25_summary.md` — TL;DR.
   - Atualizar `itau.md`, `bancos.md`, páginas de conceitos relevantes, com citações apontando para `full/` ou `structured/`.
   - Apagar o original de `undigested/`.
   - Registrar em `sources/index.md` e `log.md`.

### 2. Ingest de apresentação / fato relevante / outros (caminho leve)

Igual ao pesado, **sem** a etapa de `structured/`. Gera `full/` + `digested/` + atualiza wiki.

### 3. Ingest de web

```
Pesquisa sobre o ciclo de crédito brasileiro em 2025
```

O LLM usa WebSearch/WebFetch, classifica confiabilidade (`oficial`/`editorial`/`community`) e cita inline — sem gerar `full/` ou `structured/`.

### 4. Ingest de Notion

O LLM puxa via MCP, gera `digested/notion_{slug}.md`, atualiza páginas e `notion_tracker.md`.

### 5. Query (perguntar)

```bash
bash tools/query.sh "Qual foi a margem bruta da Cury no 3T24?"
bash tools/query.sh "Compare o distrato da Direcional vs Cury de 1T23 a 4T25"
bash tools/query.sh "Qual o ROE da Riva nos últimos 4 trimestres?"
```

O `query.sh` invoca um agente LLM com acesso ao Bash que busca a resposta nas três camadas de dados: `structured/` (JSON limpo) → `full/` (texto bruto do PDF) → `digested/` (resumos). Cada dado retornado vem com citação da fonte exata (arquivo + linha ou campo JSON).

O agente sabe lidar com texto espaçado da extração de PDF (ex: `D is tra to s` em vez de `Distratos`) e nunca inventa dados — se não encontrar, diz o que buscou.

### 6. Modelagem (planilha)

```
Monta a espinha histórica do Itaú dos últimos 8 trimestres
```

O LLM puxa `canonical` de todos os `structured/itau/*/itr.json`, usa `company_specific` para gerencial, abre `full/` quando precisa fundamentar uma premissa de projeção, e checa `itau.md` para a tese. Registra a sessão em `log.md`.

### 7. `promote_nota`

Quando uma nota explicativa virar referência recorrente (citada por 3+ páginas), o LLM pode promovê-la a uma página própria, tipo `itau_nota_instrumentos_financeiros.md`, consolidando a nota ao longo dos trimestres.

### 8. Lint datado (saúde de claims datáveis)

```bash
bash tools/lint.sh                        # relatório completo, todas severidades
bash tools/lint.sh --severity action      # só action e acima
bash tools/lint.sh --page cyrela.md       # uma página
```

Varre todas as páginas da wiki em busca de `(fonte: X, em: YYYY-MM-DD)` e aplica quatro regras em três níveis (`hint` < `warn` < `action`):

- **`age_threshold` (warn)** — claim com `em:` mais velho que o limiar configurado (default: 12 meses para legal/regulatório, 6 para guidance, 3 para métrica). Não dispara se `newer_source` já está flaggando o mesmo claim.
- **`newer_source` (action)** — existe `digested/`/`full/` com `ingested_on > em:` na manifest da empresa/conceito da página. Significa "source nova ingerida mas a página ainda não incorporou".
- **`contradiction` (action)** — duas páginas com valores numéricos conflitantes sobre o mesmo item-chave.
- **`missing_em` (hint)** — claim com número + verbo temporal (`vigente`, `a partir de`, `até`) sem `em:`. Candidato a retrofit.

Saída: `sources/lint_reports/YYYY-MM-DD.md` + linha `[lint]` em `log.md`. Thresholds em `tools/lint_config.json`.

**Primeiro run**: `hint` vai ser alto (cada claim legado sem `em:` vira um hint — isso É a lista de retrofit). `action` domina por falsos-positivos de contradição até ~15 páginas terem `em:` populado. Triage sugerido: hint → warn → action.

### 9. Watch (sinais externos — legal, guidance, metas)

```bash
bash tools/watch.sh                       # respeita cadência
bash tools/watch.sh --force               # ignora cadência
bash tools/watch.sh --page reforma_tributaria.md
```

Para páginas opt-in (declaram `watches:` no frontmatter), executa WebSearch restrito a sites confiáveis, compara com estado salvo e sinaliza URLs novas/atualizadas. **Não ingere nada automaticamente** — só avisa.

Use quando a página tem claim volátil **fora do ciclo CVM/Notion/calls** (lei, portaria, guidance corporativo em press release, meta anunciada em Investor Day). Exemplo de declaração no frontmatter:

```yaml
---
type: concept
aliases: [CBS, IBS, LC 214/2025]
watches:
  - query: "LC 214/2025 alteração alíquota"
    sites: [planalto.gov.br, mattosfilho.com.br]
    cadence: weekly
  - query: "reforma tributária incorporadora 2026"
    sites: [valor.globo.com]
    cadence: monthly
sources: [...]
---
```

Cadências: `weekly` (7 dias), `monthly` (30 dias), `quarterly` (90 dias). Estado persiste em `sources/watch_state/{page_slug}.json`. Hits vão para `sources/lint_reports/YYYY-MM-DD-watch.md` (arquivo separado, não é sobrescrito pelo lint).

---

## Ferramentas (CLI)

### Fetch — baixar documentos da CVM

```bash
bash tools/fetch.sh TEND3                          # modo normal
bash tools/fetch.sh TEND3 --horizon 5y --types dfp,itr,release
bash tools/fetch.sh TEND3 --discover               # modo discovery (cria fetch_profile)
```

Requer CVM-API rodando em `localhost:8100`.

### Fetch Calls — transcrições de teleconferência

```bash
bash tools/fetch_calls.sh DIRR3 --discover                  # lista canal YouTube, pontua trimestres, escreve audit plan
bash tools/fetch_calls.sh DIRR3                              # baixa transcrições novas (high-confidence do plan)
bash tools/fetch_calls.sh DIRR3 --url URL --period 4T24      # forçar vídeo específico
```

Requer `youtube_channel` no manifest da empresa. Lista os tabs `/videos` e `/streams` (calls são frequentemente live-streams). Output: `{empresa}_call_transcript_{periodo}.md` em `undigested/` com YAML frontmatter e anchors `[mm:ss]` a cada ~60s. Caption priority: manual `pt`/`pt-BR` → auto `pt`/`pt-BR` → skip com `[fetch-calls-skip]` no log.

**Alternativa para WEG (e empresas em CMS MZIQ)**: transcrição oficial em PDF disponível na Central de Resultados do site IR. Qualidade muito superior a auto-captions YouTube. Drop manual em `undigested/` como `weg_call_transcript_<P>.md` com frontmatter `captions: official_transcript`, depois `ingest_calls.sh`.

### Fetch Notion — puxar páginas do Capstone

```bash
bash tools/fetch_notion.sh --discover         # no-op: count + primeiras 20
bash tools/fetch_notion.sh                    # puxa pages novas/editadas
bash tools/fetch_notion.sh --limit 10         # apenas N pages neste run
bash tools/fetch_notion.sh --page <id>        # forçar uma page específica
```

Requer `NOTION_TOKEN` em `.env`. Config em `sources/manifests/_notion.json`, state persistente em `sources/manifests/_notion_state.json` (chaveado por `last_edited_time` — re-rodar só surfaces pages que foram editadas após o último ingest). Escreve markdown com frontmatter em `undigested/notion_<slug>.md`. Loop fecha localmente quando `ingest.sh --notion` completa.

### Ingest — processar documentos

```bash
bash tools/ingest.sh TEND3                              # processa tudo em sources/undigested/ para o ticker
bash tools/ingest.sh TEND3 --concurrency 4              # controlar paralelismo
bash tools/ingest.sh --generic planilha_setor.xlsx      # ingerir fonte avulsa (sem ticker)
bash tools/ingest.sh --notion sources/undigested/notion_<slug>.md  # ingerir page Notion específica
```

O ingest produz `full/` + `structured/` + `digested/` e registra na fila do wiki update.

### Ingest Calls — processar transcrições

```bash
bash tools/ingest_calls.sh DIRR3                  # padrão concurrency 4
bash tools/ingest_calls.sh DIRR3 -j 2             # limitar paralelismo
```

Scaneia `undigested/{empresa}_call_transcript_*.md`, copia pra `full/{empresa}/{periodo}/call_transcript.md`, gera digest qualitativo via Sonnet, atualiza manifest e wiki queue. **Não produz `structured/`** — números pertencem ao release/ITR.

### Wiki Update — atualizar páginas da wiki

```bash
bash tools/wiki_update.sh --full    # primeira rodada: lê TODOS os digesteds, recria tudo
bash tools/wiki_update.sh           # incremental: processa apenas a fila pendente (sources/wiki_queue.json)

# Com modelo menor para economizar tokens (recomendado para runs completos)
WIKI_CLAUDE_MODEL=sonnet bash tools/wiki_update.sh --full

# Retomar Phase 2 de um plano salvo (se o processo morreu no meio)
bash tools/wiki_resume_phase2.sh --plan logs/wiki_plan_merged_YYYYMMDD.json
```

Duas fases:
1. **Planejamento** — LLM lê os digesteds em chunks e produz um plano JSON (quais páginas criar/atualizar/pular), com merge no final. Tunable: `WIKI_PLAN_CHUNK_SIZE` (default 50), `WIKI_PLAN_CHUNK_TIMEOUT` (default 1200s).
2. **Execução** — LLM escreve cada página com contexto cirúrgico (só os digesteds relevantes). Tunable: `WIKI_WRITE_TIMEOUT` (default 1800s/página), `WIKI_WRITE_CONCURRENCY` (default 4 workers paralelos).

Se a execução (Phase 2) morrer no meio, use `wiki_resume_phase2.sh` com o plano salvo em `logs/`. O script pula pages `create` que já existem no disco e re-roda `update` sempre (idempotente).

### Query — consultar dados

```bash
bash tools/query.sh "qual o distrato da Cury no 3T24?"
bash tools/query.sh "série histórica de VSO da Direcional desde 2019"
```

Busca em `structured/` → `full/` → `digested/` e retorna resposta citada. Lida com texto espaçado de PDFs automaticamente.

### Re-ingest full/ — corrigir transcrições truncadas

```bash
bash tools/reingest_full.sh CURY3 --horizon 3y    # re-baixa PDFs e copia direto para full/
```

Não invoca o LLM. Usado para corrigir fulls que foram truncados pelo pipeline antigo.

### Refresh Calendário — atualizar datas de divulgação

```bash
bash tools/refresh_calendario.sh                       # dry-run: JSON report (sem mudanças)
bash tools/refresh_calendario.sh --apply               # aplica updates ao calendario_resultados.md
bash tools/refresh_calendario.sh --ticker WEGE3 -v     # debug single ticker
```

Pra cada ticker BR coberto, puxa o IPE_9 ("Calendário de Eventos Corporativos") mais recente via CVM-API, parser regex (sem LLM) extrai datas DRE/ITR/DFP, e atualiza `calendario_resultados.md` **preservando edits manuais** — só preenche cells vazias, bumpa `Atualizada` na linha tocada e o frontmatter `updated`. Cobre ~26 de 30 tickers BR (4 sem IPE_9: SANB11, INBR32, BFFT3, LCAM3 → fallback IPE_6 fica como roadmap). Estrangeiros (XP, STLA, SIE.DE, BFIT.NA, LOMA, PICS) ficam manuais. Cadência sugerida: rodar semanalmente conforme empresas filiarem o calendário do novo ano (típico jan-fev).

### Lint datado — validar freshness de claims

```bash
bash tools/lint.sh                        # relatório completo
bash tools/lint.sh --severity action      # só action
bash tools/lint.sh --page cyrela.md       # uma página
```

Quatro regras sobre citações `(fonte: X, em: YYYY-MM-DD)`: `age_threshold` (warn, com dedup contra `newer_source`), `newer_source` (action, usa `manifests/` para cross-referência), `contradiction` (action, heurístico), `missing_em` (hint, para retrofit). Relatório em `sources/lint_reports/YYYY-MM-DD.md`. Thresholds configuráveis em `tools/lint_config.json`. Edge-cases de falso-positivo documentados no próprio `log.md` e em SCHEMA.md §Lint §10.

### Watch — monitorar sinais externos

```bash
bash tools/watch.sh                       # respeita cadência por entrada
bash tools/watch.sh --force               # força re-check de tudo
bash tools/watch.sh --page X.md           # uma página
```

Lê páginas com `watches:` no frontmatter (opt-in por página), roda `claude --print` com WebSearch restrito aos `sites:` declarados, salva estado em `sources/watch_state/{page_slug}.json` e emite `[watch-hit]` em `sources/lint_reports/YYYY-MM-DD-watch.md` quando URLs novas/atualizadas aparecem. Nunca ingere automaticamente — só sinaliza. Bom para: mudanças em lei/portaria, revisão de guidance fora de call, timing de lançamento de produto via press release.

### Fila do wiki update

A fila é gerenciada por `tools/lib/wiki_queue.py` e persiste em `sources/wiki_queue.json`. O `ingest.sh` enfileira via `wiki_queue.py enqueue` e ainda appenda uma linha de auditoria em `log.md`:

```
[wiki-queue] 2026-04-12 | cury | itr | 3T25 | sources/digested/cury_itr_3T25_summary.md
```

O `wiki_update.sh` drena a fila no início do run incremental e chama `clear` ao concluir com sucesso. Para inspecionar itens pendentes:

```bash
python tools/lib/wiki_queue.py peek
```

---

## Anatomia de uma página da wiki

```markdown
---
type: entity
aliases: [Itaú Unibanco, ITUB4]
sources: [full/itau/3T25/itr.md, structured/itau/3T25/itr.json]
created: 2026-04-08
updated: 2026-04-08
---

# Itaú

Maior banco privado do Brasil por ativos...

Margem financeira de R$ 27,3 bi no 3T25 (fonte: structured/itau/3T25/itr.json :: canonical.dre.margem_financeira), impulsionada por [...] (fonte: full/itau/3T25/itr.md §mdna).

Alíquota reduzida em 60% da padrão (fonte: digested/LC_214_2025_summary.md, em: 2025-01-16) — esta linha carrega `em:` porque o valor pode mudar se a lei for alterada. Números com período contábil (margem 3T25, ROE 2024) NÃO levam `em:` — o período já carimba a data.

Relacionado: [[bancos]], [[nim]], [[custo_risco]]
```

**Tipos de página:** entity, concept, sector, comparison, synthesis, nota.

---

## Convenções de nomenclatura

- Filenames: `snake_case.md`, lowercase, português quando natural.
- Sem prefixo de ticker (`itau.md`, não `ITUB4_itau.md`) — tickers no `aliases`.
- Períodos: `1T25`, `2T25`, `3T25`, `4T25`, `2025` (anual).
- Tipos de fonte: `itr`, `dfp`, `release`, `apresentacao`, `fato_relevante`, `call_transcript`.
- **`em: YYYY-MM-DD` em citações** — sinaliza claims datáveis (alíquotas, guidance, metas, regras fiscais). Data = efetividade real, não data do ingest. Não usar em números com período contábil. Ver SCHEMA.md §Dated Claims.

---

## Dicas de uso

### Obsidian

Esta wiki é 100% compatível com [Obsidian](https://obsidian.md/). Abra a pasta como vault para navegar pelos `[[wikilinks]]`, ver o graph view e usar Dataview.

### Fontes

- PDFs de ITR/DFP/release: baixe do site de RI da empresa e solte em `sources/undigested/`.
- Para artigos: use o [Obsidian Web Clipper](https://obsidian.md/clipper) ou peça ingest web.

### Boas práticas

- **Uma fonte por vez** — ingira fontes individualmente para que o LLM faça cross-linking coerente.
- **Deixe o LLM linkar** — não crie wikilinks manualmente.
- **Lint regularmente** — uma vez por semana.
- **Promova respostas** — queries boas viram páginas.
- **Não edite `sources/`** — fontes são imutáveis. Para corrigir, reingira.

---

## Arquivos especiais

| Arquivo | Propósito |
|---------|-----------|
| `SCHEMA.md` | Contrato operacional — o LLM lê antes de qualquer operação |
| `index.md` | Catálogo de páginas da wiki por categoria |
| `log.md` | Histórico append-only |
| `calendario_resultados.md` | Tracker de cobertura — datas de divulgação por trimestre + status wiki/tese (atualizável via `tools/refresh_calendario.sh`) |
| `sources/index.md` | Registro de fontes brutas |
| `sources/structured/_schemas/` | Schemas canônicos por setor |
| `sources/wiki_queue.json` | Fila do wiki update (live state) |
| `README.md` | Este tutorial |
| `CLAUDE.md` | Manual operacional para LLM (mais detalhado/atualizado que o README) |

## Skills interativas

`/tese` vive em `.claude/skills/tese/` — diferente do resto do pipeline, **não passa por `claude --print`**, entrevista o analista no terminal:

```
/tese {empresa}              # auto-detecta modo (new se não existe, checkpoint se existe)
/tese {empresa} --status     # mostra cabeçalho de {empresa}_tese.md
/tese --carteira             # lista todas as teses ativas
/tese {empresa} --lens       # força reescrita da Lente + checkpoint
```

Cria/atualiza `{empresa}_tese.md` (Lente estável + Checkpoints datados). Investment thesis fica isolada da entity page (`{empresa}.md`) — entity é fact base, tese carrega opinião sobre preço/timing. Ver SCHEMA.md §Tese pages.

---

## Créditos

Padrão baseado no [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) de Andrej Karpathy.
