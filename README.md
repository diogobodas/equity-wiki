# LLM Wiki — Tutorial

Uma wiki pessoal mantida por LLM, baseada no padrão descrito por [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

A ideia central: em vez de re-derivar conhecimento do zero a cada pergunta (como RAG tradicional), o LLM **constroi e mantém incrementalmente** uma base de conhecimento persistente — um artefato que se acumula ao longo do tempo.

O humano cuida das fontes e faz as perguntas certas. O LLM faz o trabalho pesado de sumarizar, cross-referenciar e manter tudo organizado.

---

## Como funciona

A wiki tem tres camadas:

```
equity-wiki/
├── sources/              # 1. Fontes (ciclo ingest & digest)
│   ├── index.md          #    Registro de todas as fontes
│   ├── undigested/       #    Inbox — arquivos brutos aguardando ingestao
│   └── digested/         #    Summaries exaustivos em markdown (permanentes)
├── *.md                  # 2. Paginas da wiki (mantidas pelo LLM)
├── index.md              #    Catalogo por categoria
├── log.md                #    Historico cronologico de operacoes
├── SCHEMA.md             # 3. Schema (configuracao e convencoes)
└── README.md             #    Este tutorial
```

1. **sources/** — Fontes com ciclo de vida: arquivo bruto entra em `undigested/`, LLM processa, gera summary exaustivo em `digested/`, arquivo original e apagado.
2. **Paginas da wiki** — Markdowns interligados com `[[wikilinks]]`. Sempre citam fontes. O LLM cria, atualiza e interliga.
3. **SCHEMA.md** — O "manual de instrucoes" que o LLM le antes de qualquer operacao.

---

## Operacoes

### 1. Ingest (adicionar conhecimento)

O workflow principal. Voce joga uma fonte, o LLM processa.

**Passo a passo:**

1. Coloque o arquivo na pasta `sources/undigested/` (PDF, markdown, texto, imagem, o que for)
2. Peca ao LLM para processar:

```
Ingere esta fonte: sources/undigested/nome_do_arquivo.pdf
```

3. O LLM vai:
   - Ler a fonte inteira
   - Criar ou atualizar paginas da wiki com as informacoes extraidas
   - Adicionar `[[wikilinks]]` entre paginas relacionadas
   - Gerar summary exaustivo em `sources/digested/` (todas as tabelas, todos os numeros)
   - Apagar o arquivo original de `sources/undigested/`
   - Registrar em `sources/index.md` e no `log.md`

**Se precisar de mais dados depois:** coloque o PDF original de volta em `sources/undigested/` e peca re-extracao direcionada.

### 2. Query (perguntar)

Faca perguntas contra a wiki. O LLM busca nas paginas relevantes e sintetiza a resposta com citacoes.

```
Qual a diferenca entre NIM clientes e NIM total?
```

Se a resposta for valiosa e reutilizavel, o LLM pode promove-la a uma nova pagina da wiki.

### 3. Lint (saude da wiki)

Peca uma verificacao periodica:

```
Faz um lint da wiki.
```

O LLM checa:
- Links mortos (apontam para paginas que nao existem)
- Paginas orfas (ninguem linka para elas)
- Paginas desatualizadas (fonte mais recente que a pagina)
- Cross-references faltando
- Contradicoes (mesmo dado com valores diferentes em paginas distintas)

---

## Anatomia de uma pagina

Toda pagina tem frontmatter YAML + conteudo em markdown:

```markdown
---
type: concept
aliases: [Net Interest Margin]
sources: [ITUB4_release_4T25.pdf, bradesco_release_4T25.pdf]
created: 2026-04-08
updated: 2026-04-08
---

# NIM

Net Interest Margin e a margem liquida de juros...

Relacionado: [[nii_clientes]], [[spread_clientes]], [[selic]]

(fonte: ITUB4_release_4T25.pdf, p.15)
```

**Tipos de pagina:** entity, concept, sector, comparison, synthesis.

---

## Dicas de uso

### Obsidian

Esta wiki e 100% compativel com [Obsidian](https://obsidian.md/). Abra a pasta como vault para:
- Navegar pelos `[[wikilinks]]` clicando
- Ver o graph view (mapa visual das conexoes)
- Identificar hubs (paginas muito conectadas) e orfas
- Usar o plugin Dataview para queries sobre o frontmatter

### Fontes

- Use o [Obsidian Web Clipper](https://obsidian.md/clipper) para converter artigos da web em markdown direto na pasta `sources/`
- Para PDFs, basta copiar o arquivo — o LLM le PDFs nativamente
- Mantenha os nomes originais dos arquivos em `sources/`

### Boas praticas

- **Uma fonte por vez** — ingira fontes individualmente para que o LLM faca um bom trabalho de integracao
- **Deixe o LLM linkar** — nao se preocupe em criar links manualmente; o ingest cuida disso
- **Lint regularmente** — uma vez por semana, peca um lint para manter a saude da wiki
- **Promova respostas** — se uma query gerou uma resposta boa, peca para virar pagina
- **Nao edite sources/** — as fontes sao imutaveis; se precisar corrigir algo, crie uma nova versao

---

## Arquivos especiais

| Arquivo | Proposito |
|---------|-----------|
| `SCHEMA.md` | Convencoes e regras — o LLM le antes de operar |
| `index.md` | Catalogo de todas as paginas, organizado por categoria |
| `log.md` | Historico cronologico (append-only) de todas as operacoes |
| `sources/index.md` | Registro de todas as fontes brutas |
| `README.md` | Este tutorial |

---

## Creditos

Padrão baseado no [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) de Andrej Karpathy.
