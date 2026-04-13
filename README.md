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

```
Qual foi a margem financeira do Itaú no 3T25?
```

O LLM busca na wiki primeiro. Se for pergunta numérica pontual, vai direto em `structured/`. Se precisar de contexto qualitativo (notas, MD&A), abre `full/`.

### 6. Modelagem (planilha)

```
Monta a espinha histórica do Itaú dos últimos 8 trimestres
```

O LLM puxa `canonical` de todos os `structured/itau/*/itr.json`, usa `company_specific` para gerencial, abre `full/` quando precisa fundamentar uma premissa de projeção, e checa `itau.md` para a tese. Registra a sessão em `log.md`.

### 7. `promote_nota`

Quando uma nota explicativa virar referência recorrente (citada por 3+ páginas), o LLM pode promovê-la a uma página própria, tipo `itau_nota_instrumentos_financeiros.md`, consolidando a nota ao longo dos trimestres.

### 8. Lint (saúde da wiki)

```
Faz um lint da wiki.
```

Checa: links mortos, páginas órfãs, páginas desatualizadas, cross-refs faltando, contradições, **schema drift** (`structured/` com chaves canônicas faltando) e notas recorrentes não promovidas.

---

## Ferramentas (CLI)

### Fetch — baixar documentos da CVM

```bash
bash tools/fetch.sh TEND3                          # modo normal
bash tools/fetch.sh TEND3 --horizon 5y --types dfp,itr,release
bash tools/fetch.sh TEND3 --discover               # modo discovery (cria fetch_profile)
```

Requer CVM-API rodando em `localhost:8100`.

### Ingest — processar documentos

```bash
bash tools/ingest.sh TEND3                         # processa tudo em sources/undigested/ para o ticker
bash tools/ingest.sh TEND3 --concurrency 4         # controlar paralelismo
bash tools/ingest.sh --generic planilha_setor.xlsx # ingerir fonte avulsa (sem ticker)
```

O ingest produz `full/` + `structured/` + `digested/` e registra na fila do wiki update.

### Wiki Update — atualizar páginas da wiki

```bash
bash tools/wiki_update.sh --full    # primeira rodada: lê TODOS os digesteds, recria tudo
bash tools/wiki_update.sh           # incremental: processa apenas a fila pendente no log.md
```

Duas fases:
1. **Planejamento** — LLM lê todos os digesteds e produz um plano JSON (quais páginas criar/atualizar)
2. **Execução** — LLM escreve cada página com contexto cirúrgico (só os digesteds relevantes)

### Re-ingest full/ — corrigir transcrições truncadas

```bash
bash tools/reingest_full.sh CURY3 --horizon 3y    # re-baixa PDFs e copia direto para full/
```

Não invoca o LLM. Usado para corrigir fulls que foram truncados pelo pipeline antigo.

### Fila do wiki update (log.md)

O `ingest.sh` appenda entries parseáveis no `log.md`:

```
[wiki-queue] 2026-04-12 | cury | itr | 3T25 | sources/digested/cury_itr_3T25_summary.md
[wiki-queue] 2026-04-12 | generic | sector | planilha | sources/digested/planilha_setor_summary.md
```

O `wiki_update.sh` consome a fila e marca com `[wiki-done]`.

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

Relacionado: [[bancos]], [[nim]], [[custo_risco]]
```

**Tipos de página:** entity, concept, sector, comparison, synthesis, nota.

---

## Convenções de nomenclatura

- Filenames: `snake_case.md`, lowercase, português quando natural.
- Sem prefixo de ticker (`itau.md`, não `ITUB4_itau.md`) — tickers no `aliases`.
- Períodos: `1T25`, `2T25`, `3T25`, `4T25`, `2025` (anual).
- Tipos de fonte: `itr`, `dfp`, `release`, `apresentacao`, `fato_relevante`, `call_transcript`.

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
| `sources/index.md` | Registro de fontes brutas |
| `sources/structured/_schemas/` | Schemas canônicos por setor |
| `README.md` | Este tutorial |

---

## Créditos

Padrão baseado no [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) de Andrej Karpathy.
