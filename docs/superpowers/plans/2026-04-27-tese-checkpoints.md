# Investment Thesis Pages (Lente + Checkpoints) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar um novo tipo de página `tese` (uma por empresa investível) com Lente estável + Checkpoints datados price-aware, criada/atualizada via skill interativo `/tese`.

**Architecture:** O skill `/tese` é uma slash-command project-local em `.claude/skills/tese/`. Sua SKILL.md atua como router (detecta modo: `new`/`checkpoint`/`lens-update`/`status`/`carteira`) e delega para um dos prompts irmãos (`interview_*.md`). Diferente do resto do pipeline (`fetch.sh`/`ingest.sh`/`wiki_update.sh`), não usa `claude --print` — roda interativo na sessão do analista. Documentação em `SCHEMA.md` define o page type e as convenções; `CLAUDE.md` adiciona o bloco de comandos.

**Tech Stack:** Markdown (Obsidian-flavored, YAML frontmatter), Claude Code skills (project-local, `.claude/skills/`).

**Spec:** [docs/superpowers/specs/2026-04-27-tese-checkpoints-design.md](../specs/2026-04-27-tese-checkpoints-design.md)

---

## File Structure

| File | Responsibility |
|------|---------------|
| `SCHEMA.md` | (modificado) Adiciona linha do tipo `tese` na tabela de Page Types, nova seção `## Tese pages` com convenções (frontmatter, body, link entity↔tese, cadência), nova sub-seção `### Tese (novo / checkpoint)` em `## Wiki Operations`. |
| `CLAUDE.md` | (modificado) Bloco `### Tese (interactive)` em `## Commands` (após `### Lint`); bullet em `## Non-obvious rules` reforçando "Tese ≠ entity". |
| `.claude/skills/tese/SKILL.md` | Router. YAML frontmatter declara `name: tese` + `description` que o Claude Code usa para reconhecer o slash-command. Body explica modos, lógica de detecção (existência do `_tese.md`, flags), edge cases (entity não existe, ambiguidade), e implementa direto `--status` e `--carteira` (read-only, simples) — delega `new`/`checkpoint`/`lens-update` para os prompts irmãos. |
| `.claude/skills/tese/interview_new.md` | Prompt detalhado para modo `new`. Carrega contexto (entity page, manifest, digesteds), detecta seção legada de tese, conduz entrevista (Lente bullet por bullet + checkpoint inicial), escreve `_tese.md`, atualiza entity page (callout + remoção da seção legada), append `[tese-new]` em `log.md`. |
| `.claude/skills/tese/interview_check.md` | Prompt para modo `checkpoint`. Lê `_tese.md` existente, faz lens check, conduz entrevista leve, prepend novo checkpoint, atualiza frontmatter (com prepend em `checkpoints[]` e bump `updated`), sincroniza callout em entity page, append `[tese-checkpoint]` em `log.md`. |
| `.claude/skills/tese/interview_lens.md` | Prompt para modo `lens-update`. Reescreve só a Lente, força um checkpoint marcado "Mudança de lente: {resumo}", append `[tese-lens]` em `log.md`. |
| `cury_tese.md` | (criado pelo smoke test) Primeira tese real produzida pelo skill. Validação ponta-a-ponta. |
| `cury.md` | (modificado pelo smoke test) Ganha callout `> Tese: ver [[cury_tese]]...` no topo. |
| `log.md` | (modificado pelo smoke test) Recebe entradas `[tese-new]` e `[tese-checkpoint]`. |

**Caminhos absolutos** durante a implementação: o repositório do wiki é `equity-wiki/` (subdiretório do diretório de trabalho). Todos os comandos `git` usam `git -C equity-wiki ...`. Edições e leituras usam paths começando com `equity-wiki/`.

---

## Task 1: SCHEMA.md — adicionar tipo `tese` + seção dedicada

**Files:**
- Modify: `equity-wiki/SCHEMA.md` (3 inserções: linha em Page Types, nova seção `## Tese pages` após Page Types, nova sub-seção em `## Wiki Operations`)

- [ ] **Step 1: Add row to Page Types table**

Open `equity-wiki/SCHEMA.md`, find the table at `## Page Types (wiki layer)` (around line 200). Add a new row after the `nota` row:

```markdown
| tese | Investment thesis com Lente estável + Checkpoints datados price-aware (uma por empresa investível) | `cury_tese.md`, `bradesco_tese.md` |
```

- [ ] **Step 2: Add new `## Tese pages` section**

Insert this section in `equity-wiki/SCHEMA.md` immediately AFTER the Page Types table (i.e., before `## Frontmatter (mandatory)`):

````markdown
## Tese pages

Uma página de tese (`type: tese`) carrega a **opinião datada** sobre uma empresa investível, separada da entity page (que carrega o **fato**: modelo, números, eventos). Estrutura: Lente estável + Stream de Checkpoints datados price-aware, mais recente no topo.

**Quando criar:** uma `_tese.md` é criada quando o analista forma uma opinião sobre a empresa pela primeira vez. Empresas sem opinião não têm `_tese.md`. Empresas privadas (sem preço público) não recebem `_tese.md` — checkpoint price-aware não cabe.

### Naming

`{empresa}_tese.md` no root do wiki (Obsidian-friendly). Lowercase, snake_case. Slug `{empresa}` igual ao do entity page. Exemplos: `cury_tese.md`, `porto_seguro_tese.md`.

### Frontmatter (mandatory)

```yaml
---
type: tese
empresa: cury                       # slug igual ao do entity page
ticker: CURY3                       # ticker B3 ou bolsa estrangeira
fact_base: cury.md                  # caminho relativo para entity page
verdict_atual: neutro               # compra | neutro | venda
verdict_em: 2026-04-27              # data ISO do checkpoint vigente
preco_em: 30.20                     # preço ajustado em R$ (ou USD para ticker estrangeiro)
checkpoints:                        # array, mais recente primeiro
  - {data: 2026-04-27, verdict: neutro, preco: 30.20}
  - {data: 2026-01-10, verdict: compra, preco: 25.00}
created: 2026-01-10
updated: 2026-04-27
---
```

**Regras de invariantes (validar a cada `/tese checkpoint`):**
- `verdict_atual` ∈ `{compra, neutro, venda}` — lowercase, exato (necessário para extração via `/tese --carteira`).
- `verdict_atual` == `checkpoints[0].verdict`.
- `verdict_em` == `checkpoints[0].data`.
- `preco_em` == `checkpoints[0].preco`.

### Body structure

```markdown
# Tese — {Empresa} ({TICKER})

> **Fact base:** [[{empresa}]] · **Verdict atual:** **{verdict}** (em {data} a R$ {preco})
>
> *Esta página carrega a opinião datada. Tudo que é fato (modelo, números, eventos) vive em [[{empresa}]].*

## Lente

3-5 bullets sobre como o analista fundamentalmente entende a empresa.
Estável; muda raramente. Cada bullet com citação para `full/` / `structured/` / `digested/`.

- Pilar 1 ... (fonte: ...)
- Pilar 2 ... (fonte: ...)

**A tese se quebra se:**
- Condição 1
- Condição 2
- Condição 3

---

## Checkpoints

### YYYY-MM-DD — {Verdict capitalizado} a R$ {preço}

Preço R$ X,XX · P/L LTM X,X× · {múltiplos relevantes do setor}

{1-3 parágrafos: visão atual, lente intacta ou não, o que mudou, com (fonte: ...) a cada claim factual}

vs. último ({data anterior}, {verdict anterior} a R$ X): {delta resumido}

(fonte: ...)

---

### YYYY-MM-DD — ... (mais antigo)

[...]

---

## Notas

- Próximo trigger natural: ...
- Watches leves: ...
```

### Convenção de link entity ↔ tese

- **Entity page** (`{empresa}.md`) ganha um callout no topo, **logo após o parágrafo intro**:
  ```markdown
  > Tese: ver [[{empresa}_tese]] (verdict atual: {verdict} em {data}).
  ```
- **Tese page** (`{empresa}_tese.md`) tem callout fixo logo após H1 (ver "Body structure" acima).

A linha do entity page é mantida em sincronia pelo skill `/tese` ao criar/atualizar checkpoints.

### Cadência (norma editorial)

Event-driven. Triggers:
- ITR/DFP/release ingerido com surpresa (vs. expectativa do analista no checkpoint anterior).
- Fato relevante material.
- Mudança de preço >15% desde último checkpoint (em qualquer direção).
- News exógena que afeta a tese (regulatória, M&A no setor, etc).
- Releitura espontânea em que a visão do analista mudou.

Sem cadência mínima. Páginas podem ficar paradas por 6-9 meses se nada material aconteceu.

### Vocabulário do verdict

`compra` / `neutro` / `venda` (lowercase, exato). Conviction e horizonte vão na prosa do checkpoint, sem campo separado.

### Valuation

Sem âncora estrutural (sem TP / IRR / cenários obrigatórios). P/L é o múltiplo default; o analista escolhe o que faz sentido por setor (P/VP para bancos, EV/EBITDA para industriais, etc). Múltiplos vão na linha de header do checkpoint; valuation prose vai no corpo livre.
````

- [ ] **Step 3: Add `## Wiki Operations > Tese (novo / checkpoint)` sub-section**

Find the `## Wiki Operations` section in `equity-wiki/SCHEMA.md` (around line 375). Add this sub-section AFTER the existing `### Lint` sub-section (last in the Operations group, around line 488 onwards):

````markdown
### Tese (novo / checkpoint)

Manual, interativo via skill `/tese {empresa}`. **Não passa pela queue de `wiki_update.sh`** — o skill grava direto.

Modos do skill:
- `/tese {empresa}` — auto-detecta. Se `{empresa}_tese.md` não existe → modo `new` (entrevista de Lente + 1º checkpoint). Se existe → modo `checkpoint` (entrevista leve, prepend de checkpoint).
- `/tese {empresa} --lens` — força modo `lens-update`. Reescreve a Lente + cria checkpoint marcando "Mudança de lente".
- `/tese {empresa} --status` — read-only. Imprime cabeçalho da `_tese.md` (verdict atual, data, preço, # de checkpoints).
- `/tese --carteira` — read-only. Lê todos `*_tese.md` no root, imprime tabela de teses ativas (verdict, data, preço por empresa).

**Log entries:** cada operação que escreve append uma linha ao `log.md`:
- `[tese-new]` — criação de nova `_tese.md` (e atualização da entity page, se houver remoção de seção legada).
- `[tese-checkpoint]` — adição de checkpoint a `_tese.md` existente.
- `[tese-lens]` — reescrita de Lente + checkpoint forçado.

**Cadência:** event-driven (ver §Tese pages > Cadência). Sem disparo automático por cron/cadência.

**Skill não invoca `claude --print`.** É interativa por design — o analista é entrevistado no terminal da sessão atual, com Claude propondo drafts de bullets e o analista confirmando/editando. Diferente do resto do pipeline.
````

- [ ] **Step 4: Verify the inserted content**

Run:
```bash
grep -n "^## Tese pages\|^### Tese (novo\|| tese | Investment" equity-wiki/SCHEMA.md
```

Expected output: 3 lines, one for each inserted section/row.

- [ ] **Step 5: Commit**

```bash
git -C equity-wiki add SCHEMA.md
git -C equity-wiki commit -m "$(cat <<'EOF'
docs(schema): add tese page type — Lente + Checkpoints

Novo tipo de página tese (uma por empresa investível). Estrutura: Lente
estável + Stream de Checkpoints datados price-aware. Frontmatter expõe
verdict_atual / verdict_em / preco_em para extração via /tese --carteira.
Vocabulário trinary (compra/neutro/venda). Cadência event-driven, sem
disparo automático.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: CLAUDE.md — adicionar bloco `### Tese` + bullet em Non-obvious rules

**Files:**
- Modify: `equity-wiki/CLAUDE.md` (2 inserções: bloco em Commands, bullet em Non-obvious rules)

- [ ] **Step 1: Add `### Tese (interactive)` block in `## Commands`**

Open `equity-wiki/CLAUDE.md`. Find the `### Lint` sub-section under `## Commands`. After the closing of that sub-section (just before `### Watchlist`), insert:

````markdown
### Tese (interactive — investment thesis pages)

```bash
/tese {empresa}              # auto-detecta modo (new se não existe, checkpoint se existe)
/tese {empresa} --status     # mostra cabeçalho da _tese.md
/tese --carteira             # lista todas as teses ativas (extraído de frontmatters)
/tese {empresa} --lens       # força modo lens-update
```

Skill é **interativa** — Claude entrevista o analista no terminal da sessão atual.
Vive em `.claude/skills/tese/`. Diferente do resto do pipeline, **não passa por `claude --print`**.

Modos:
- `new` — cria `{empresa}_tese.md` via entrevista de Lente (3-5 pilares + kill-switch) + 1º checkpoint datado.
- `checkpoint` — entrevista leve sobre o que mudou; prepend de checkpoint, atualização de frontmatter.
- `lens-update` — reescreve a Lente + força checkpoint marcando "Mudança de lente".

Log entries: `[tese-new]` / `[tese-checkpoint]` / `[tese-lens]` em `log.md`.

Ver `SCHEMA.md §Tese pages` para convenções de frontmatter, body e cadência.
````

- [ ] **Step 2: Add bullet in `## Non-obvious rules`**

Find the `## Non-obvious rules` section (lines around the bottom of `equity-wiki/CLAUDE.md`). Add this bullet at the end of the list:

```markdown
- **Tese ≠ entity.** Investment thesis vive em `{empresa}_tese.md` (type: tese), com Lente estável + Checkpoints datados (frontmatter expõe `verdict_atual` + `verdict_em` para extração via `/tese --carteira`). Entity page (`{empresa}.md`) é fact base e não carrega opinião sobre preço/timing. Criar/atualizar via `/tese {empresa}` (interativo). Ver `SCHEMA.md §Tese pages`.
```

- [ ] **Step 3: Verify**

Run:
```bash
grep -n "### Tese (interactive\|^- \*\*Tese ≠ entity" equity-wiki/CLAUDE.md
```

Expected: 2 lines, one for each insertion.

- [ ] **Step 4: Commit**

```bash
git -C equity-wiki add CLAUDE.md
git -C equity-wiki commit -m "$(cat <<'EOF'
docs(claude-md): document /tese skill + tese page type

Bloco /tese em ## Commands após ### Lint. Bullet "Tese ≠ entity" em
## Non-obvious rules reforçando separação fato (entity) × opinião datada
(tese).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: SKILL.md — router do skill `/tese`

**Files:**
- Create: `equity-wiki/.claude/skills/tese/SKILL.md`

- [ ] **Step 1: Create the skill directory**

Run:
```bash
mkdir -p equity-wiki/.claude/skills/tese
```

Verify:
```bash
ls -la equity-wiki/.claude/skills/tese/
```

Expected: empty directory exists.

- [ ] **Step 2: Write SKILL.md**

Create `equity-wiki/.claude/skills/tese/SKILL.md` with this exact content:

````markdown
---
name: tese
description: Cria ou atualiza investment thesis pages (Lente + Checkpoints datados) para empresas investíveis listadas. Trigger explícito em /tese {empresa} ou /tese --carteira. Modos automáticos: new (cria nova tese), checkpoint (adiciona checkpoint a tese existente). Modos com flag: --lens (reescreve lente), --status (read-only), --carteira (read-only, lista todas). Diferente do resto do pipeline, é interativa — entrevista o analista no terminal.
---

# Skill `/tese` — investment thesis pages

Você está executando o skill `/tese`. O comando do usuário inclui zero ou mais argumentos. Sua primeira tarefa é decidir o **modo** e roteá-lo.

## Detecção de modo

Argumentos vêm como `{empresa}` (slug, lowercase, snake_case) e/ou flags `--lens`, `--status`, `--carteira`. Aplique a primeira regra que casar:

| Padrão | Modo | Ação |
|---|---|---|
| `--carteira` (sem empresa) | `carteira` | Inline aqui (ver §Modo carteira). |
| `{empresa} --status` | `status` | Inline aqui (ver §Modo status). |
| `{empresa} --lens` | `lens-update` | Carregar `interview_lens.md` e seguir. |
| `{empresa}` (sem flag) e `{empresa}_tese.md` **não existe** | `new` | Carregar `interview_new.md` e seguir. |
| `{empresa}` (sem flag) e `{empresa}_tese.md` **existe** | `checkpoint` | Carregar `interview_check.md` e seguir. |
| Vazio ou ambíguo | erro | Imprimir guia: `/tese {empresa}` ou `/tese --carteira`. |

**Repo root:** o wiki é `equity-wiki/` (relativo ao cwd). Todos os caminhos abaixo são relativos a esse root. Use Glob/Grep/Read com `path: "equity-wiki/"` ou prefixe os caminhos.

## Edge cases (validar antes de qualquer modo que use `{empresa}`)

1. **Entity page existe?** Verifique `equity-wiki/{empresa}.md`. Se não existe, imprima:
   ```
   Erro: equity-wiki/{empresa}.md não existe. Crie a entity page primeiro
   (com type: entity e dados básicos da empresa) antes de criar a tese.
   ```
   Pare.

2. **Empresa privada / não-listada?** Se `{empresa}.md` tem `type: entity` mas o frontmatter não tem `aliases` com ticker (B3, NYSE, NASDAQ — qualquer ticker reconhecível), avise:
   ```
   Aviso: {empresa} parece ser não-listada (sem ticker em aliases).
   Tese page é exclusiva para empresas investíveis com preço público.
   Continuar mesmo assim? (s/n)
   ```
   Se `n`, pare.

3. **Argumento parece ticker em vez de slug?** Ex: usuário digita `/tese CURY3`. Detecte: tudo maiúsculas + dígitos. Procure em `equity-wiki/*.md` um arquivo cujo frontmatter tenha esse ticker em `aliases`. Se achar exatamente um, sugira: `Você quis dizer /tese {slug encontrado}? (s/n)`. Se múltiplos ou nenhum, peça desambiguação.

## Modo `status` (inline)

1. Read `equity-wiki/{empresa}_tese.md`. Se não existe, imprima `Tese para {empresa} ainda não criada. Use /tese {empresa} para começar.` e pare.
2. Parse o frontmatter mentalmente. Imprima:
   ```
   Tese: equity-wiki/{empresa}_tese.md
   Verdict: {verdict_atual} (em {verdict_em} a R$ {preco_em})
   Lente: {N pilares — conte os bullets na seção ## Lente até "**A tese se quebra**" } · última atualização da página: {updated}
   Checkpoints: {len(checkpoints)} (mais recente {checkpoints[0].data})
   Fact base: equity-wiki/{fact_base}
   ```

## Modo `carteira` (inline)

1. Glob `equity-wiki/*_tese.md`. Para cada arquivo, leia só as primeiras ~30 linhas (frontmatter cabe nisso).
2. Parse frontmatter mentalmente: `empresa`, `ticker`, `verdict_atual`, `verdict_em`, `preco_em`, e `len(checkpoints)`.
3. Ordene desc por `verdict_em`.
4. Imprima tabela markdown:
   ```
   | Empresa | Ticker | Verdict | Em | Preço | Checkpoints |
   |---|---|---|---|---|---|
   | cury | CURY3 | neutro | 2026-04-27 | R$ 30,20 | 2 |
   | bradesco | BBDC4 | compra | 2026-04-25 | R$ 14,80 | 5 |
   ```
5. Sob a tabela, conte por verdict: `Total: 2 (1 compra, 1 neutro, 0 venda).`

Se não há nenhum `*_tese.md`, imprima `Nenhuma tese criada ainda. Use /tese {empresa} para começar a primeira.` e pare.

## Modos `new`, `checkpoint`, `lens-update` (delegação)

Carregue o arquivo correspondente do mesmo diretório do skill (`.claude/skills/tese/`):
- `new` → `interview_new.md`
- `checkpoint` → `interview_check.md`
- `lens-update` → `interview_lens.md`

Siga o prompt carregado. Cada um deles é auto-contido e termina escrevendo arquivos + append em `log.md`.

## Princípios gerais (válidos para todos os modos)

- **Você é interativo.** Faça uma pergunta por vez, espere resposta, próxima. Não despeje questionário inteiro.
- **Sempre proponha drafts.** Em vez de "qual é o pilar central?", pergunte "qual é o pilar central?" e depois proponha um draft baseado no contexto carregado, e peça confirmação ou edição.
- **Cite tudo.** Cada bullet de Lente e cada claim factual em checkpoints carrega `(fonte: ...)`. Use o formato do `SCHEMA.md §Source Citations`.
- **Datas em ISO** (`YYYY-MM-DD`). Hoje é a data corrente da sessão — pergunte ao Bash/ambiente se duvidar.
- **Português** no corpo das páginas (Brazilian PT). YAML frontmatter em inglês quando as keys forem técnicas (`type`, `created`, `updated`).
- **YAML compacto para arrays de objetos.** Use `- {data: 2026-04-27, verdict: neutro, preco: 30.20}` em `checkpoints:`, não block style.
- **Não invente números.** Se o analista cita um valor que não está em `sources/`, peça pra ele indicar a fonte. Se não houver, anote `n/d` na prosa do checkpoint.
- **Log append.** Antes de finalizar, append linha ao `equity-wiki/log.md` com formato:
  ```
  [tese-new] 2026-04-27 cury — created cury_tese.md (verdict: neutro)
  [tese-checkpoint] 2026-04-27 cury — added checkpoint (verdict: neutro a R$ 30,20)
  [tese-lens] 2026-04-27 cury — lens rewritten (resumo: ...)
  ```
````

- [ ] **Step 3: Read back and verify acceptance criteria**

Read the file you just wrote. Confirm it covers:
- [ ] YAML frontmatter with `name: tese` and a `description` clear enough for Claude Code's slash-command resolver to trigger it.
- [ ] Mode detection table covers all 5 modes (`new`, `checkpoint`, `lens-update`, `status`, `carteira`) + error case.
- [ ] Edge cases enumerated: missing entity page, private company, ticker-instead-of-slug.
- [ ] `status` and `carteira` are implemented inline (not delegated).
- [ ] `new`/`checkpoint`/`lens-update` delegate to sibling files.
- [ ] General principles (interactivity, drafts, citations, ISO dates, PT prose, YAML style, log append) listed.

If any criterion missing, fix inline.

- [ ] **Step 4: Commit**

```bash
git -C equity-wiki add .claude/skills/tese/SKILL.md
git -C equity-wiki commit -m "$(cat <<'EOF'
feat(skills): add /tese skill router (SKILL.md)

Project-local skill em .claude/skills/tese/. Roteia comando /tese para
um de 5 modos (new, checkpoint, lens-update, status, carteira) com base
em flags + existência do _tese.md. Status e carteira implementam inline;
new/checkpoint/lens delegam para interview_*.md (próximas tasks).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: interview_new.md — modo `new`

**Files:**
- Create: `equity-wiki/.claude/skills/tese/interview_new.md`

- [ ] **Step 1: Write interview_new.md**

Create `equity-wiki/.claude/skills/tese/interview_new.md` with this exact content:

````markdown
# Modo `new` — criar `{empresa}_tese.md` via entrevista

Você foi roteado pelo `SKILL.md` para criar uma nova tese. O usuário digitou `/tese {empresa}` e `{empresa}_tese.md` não existe ainda.

## Pré-condições já validadas pelo router

- `equity-wiki/{empresa}.md` existe e tem `type: entity`.
- A empresa parece listada (tem ticker em `aliases`).
- `equity-wiki/{empresa}_tese.md` ainda não existe.

## Passo 1 — Carregamento de contexto

Antes de fazer qualquer pergunta, leia (em paralelo se possível):

1. `equity-wiki/{empresa}.md` (entity page completa).
2. `equity-wiki/sources/manifests/{empresa}.json` (se existir; ignore erro se não).
3. Os 2-3 digesteds mais recentes da empresa: glob `equity-wiki/sources/digested/{empresa}_*.md` e/ou `equity-wiki/sources/digested/notion_{empresa}_*.md`, ordene por mtime, leia os 2-3 mais recentes.

Se a entity page tem uma seção que se parece com tese — heading começando com `## Tese`, `## Teses`, `## Tese e ...`, `## Tese de ...`, `## Turnaround`, `## Perspectivas e Tese`, `## Alavancas de melhora ... (tese)`, ou similares — note o número da linha de início e fim. Você vai (a) usar como insumo na entrevista e (b) removê-la da entity page no final.

## Passo 2 — Anúncio

Diga ao usuário (no terminal):

```
Vou criar equity-wiki/{empresa}_tese.md para você.

Li {N} fontes: {empresa}.md, manifests/{empresa}.json, e {N} digesteds recentes.
{Se houver seção legada:} Detectei uma seção "## {heading legado}" em {empresa}.md
(linhas L1-L2). Vou usar como ponto de partida e remover de {empresa}.md no final.

Vamos por partes: primeiro a Lente (3-5 pilares + condições de quebra),
depois o checkpoint inicial (preço, verdict, racional). Pode levar 10-15 minutos.

Começando.
```

## Passo 3 — Lente: anomalia central

Pergunte ao usuário:

```
Em 1 frase: qual é a anomalia central dessa empresa? O que ela faz que o
setor não faz, ou faz melhor que o setor?
```

Espere resposta. Use o contexto que você carregou + a resposta do usuário para propor um draft de **bullet 1** da Lente, com citação para `full/` ou `digested/`. Mostre ao usuário:

```
Draft do pilar 1:

- **{Frase central reformulada como pilar}** — {expansão de 1-2 frases com números
  concretos do contexto carregado} (fonte: {arquivo}).

OK assim ou edita?
```

Aceite resposta livre (`ok`, `edita: ...`, ou texto novo).

## Passo 4 — Lente: pilares de sustentação

Pergunte:

```
Quais 2-3 pilares sustentam essa anomalia? Modelo de negócio, vantagem
estrutural, base de clientes, ciclo de capital — o que mantém isso de pé?
```

Para cada pilar mencionado pelo usuário, proponha um draft com citação. Repita o ciclo "draft → ok ou edita". Pare quando o usuário disser "chega" ou após 3 pilares (totalizando 4 com o central).

## Passo 5 — Lente: kill-switches

Pergunte:

```
O que **quebra** essa lente? Lista 2-3 condições — não pequenos riscos,
mas mudanças que invalidariam a tese central.
```

Não há draft aqui — usuário lista, você reformula em bullets curtos e mostra:

```
"A tese se quebra se":

- {Condição 1, reformulada}
- {Condição 2, reformulada}
- {Condição 3, reformulada}

OK assim ou edita?
```

## Passo 6 — Checkpoint inicial

Pergunte uma coisa de cada vez:

1. `Preço de fechamento de hoje (em R$ ou USD para ticker estrangeiro)?`
2. `P/L LTM?`
3. `P/VP? (deixe em branco se não aplicável ao setor — em incorporadora/banco vale, em SaaS por exemplo nem sempre)`
4. `Outro múltiplo relevante para esse setor? (EV/EBITDA, P/Receita, etc — opcional)`
5. `Verdict: compra / neutro / venda?`
6. `Em 1-3 parágrafos: por que esse verdict a esse preço, hoje? O que pesa mais? Não precisa enumerar tudo da Lente — só o que move a agulha agora.`

Após o último, proponha o checkpoint completo (header + corpo + citações que você consiga extrair do contexto carregado), peça confirmação:

```
Draft do checkpoint inicial:

### {hoje} — {Verdict capitalizado} a R$ {preço}

Preço R$ {X,XX} · P/L LTM {X,X}× · P/VP {X,X}× · {outros}

{1-3 parágrafos do usuário, com citações inseridas onde claims factuais aparecem}

(fonte: {citação principal})

OK assim ou edita?
```

## Passo 7 — Escrita do `_tese.md`

Quando o usuário confirmar, escreva `equity-wiki/{empresa}_tese.md` com este template (substituindo placeholders):

```markdown
---
type: tese
empresa: {empresa}
ticker: {TICKER}
fact_base: {empresa}.md
verdict_atual: {verdict}
verdict_em: {hoje}
preco_em: {preço numérico, sem R$, com ponto decimal}
checkpoints:
  - {data: {hoje}, verdict: {verdict}, preco: {preço numérico}}
created: {hoje}
updated: {hoje}
---

# Tese — {Display Name} ({TICKER})

> **Fact base:** [[{empresa}]] · **Verdict atual:** **{verdict}** (em {hoje} a R$ {preço})
>
> *Esta página carrega a opinião datada. Tudo que é fato (modelo, números, eventos) vive em [[{empresa}]].*

## Lente

- {Pilar 1} (fonte: ...)
- {Pilar 2} (fonte: ...)
- {Pilar 3} (fonte: ...)
- {Pilar 4 — opcional} (fonte: ...)

**A tese se quebra se:**
- {Condição 1}
- {Condição 2}
- {Condição 3}

---

## Checkpoints

### {hoje} — {Verdict capitalizado} a R$ {preço}

Preço R$ {X,XX} · P/L LTM {X,X}× · {outros múltiplos}

{prosa do checkpoint}

(fonte: ...)

---

## Notas

- Próximo trigger natural: {se o usuário mencionou um catalisador específico, registre aqui; senão deixe vazio}.
```

## Passo 8 — Atualizar entity page

Edite `equity-wiki/{empresa}.md`:

1. **Adicionar callout no topo:** logo após o parágrafo intro (geralmente termina antes do primeiro `##`), insira uma linha em branco e:
   ```markdown
   > Tese: ver [[{empresa}_tese]] (verdict atual: {verdict} em {hoje}).
   ```

2. **Remover seção legada:** se você detectou no Passo 1 uma seção começando com heading que parece tese, remova as linhas dessa seção (do heading até a próxima linha `## ` ou `---` que delimita a próxima seção). **Pergunte confirmação** antes de remover, mostrando as primeiras 3 linhas removidas.

3. **Bump `updated`** no frontmatter de `{empresa}.md` para `{hoje}`.

## Passo 9 — Append em `log.md`

Append uma linha ao `equity-wiki/log.md`:

```
[tese-new] {hoje} {empresa} — created {empresa}_tese.md (verdict: {verdict} a R$ {preço}); {se removeu seção legada:} migrated legacy section "## {heading}" from {empresa}.md
```

## Passo 10 — Confirmação final

Imprima:

```
Pronto. Criei:
- equity-wiki/{empresa}_tese.md (tese page com Lente + 1 checkpoint)
- Atualizei equity-wiki/{empresa}.md (callout + remoção da seção legada)
- Append em equity-wiki/log.md

Próxima vez que rodar /tese {empresa} sem flag, vai cair em modo checkpoint.
```
````

- [ ] **Step 2: Walkthrough validation**

Read the file you wrote. Trace through it pretending to be Claude executing the prompt with `{empresa}=cury`. Verify:
- [ ] Steps 1-2: context loading is concrete (specific paths, specific patterns to detect legacy section).
- [ ] Steps 3-5: Lente interview has 3 distinct questions (anomalia, pilares, kill-switches), each with draft-then-confirm cycle.
- [ ] Step 6: checkpoint interview asks each item individually (price, multiples, verdict, prose).
- [ ] Step 7: write template has all required frontmatter fields and body sections.
- [ ] Step 8: entity page update specifies WHERE to insert callout (after intro paragraph, before first `##`).
- [ ] Step 8: legacy section removal asks confirmation.
- [ ] Step 9: log.md format is concrete (single line, includes verdict + price).
- [ ] PT-BR throughout the user-facing prompts.

If gaps, fix inline.

- [ ] **Step 3: Commit**

```bash
git -C equity-wiki add .claude/skills/tese/interview_new.md
git -C equity-wiki commit -m "$(cat <<'EOF'
feat(skills): /tese mode new — interview prompt

Fluxo de 10 passos: carrega contexto (entity + manifest + digesteds),
detecta seção legada de tese, entrevista Lente (anomalia + pilares +
kill-switches) e checkpoint inicial (preço + múltiplos + verdict +
racional), escreve _tese.md, atualiza entity page (callout + remoção
da seção legada), append [tese-new] em log.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: interview_check.md — modo `checkpoint`

**Files:**
- Create: `equity-wiki/.claude/skills/tese/interview_check.md`

- [ ] **Step 1: Write interview_check.md**

Create `equity-wiki/.claude/skills/tese/interview_check.md` with this exact content:

````markdown
# Modo `checkpoint` — adicionar checkpoint a `{empresa}_tese.md` existente

Você foi roteado pelo `SKILL.md`. O usuário digitou `/tese {empresa}` (sem flag) e `{empresa}_tese.md` já existe.

## Passo 1 — Carregar a tese existente

Read `equity-wiki/{empresa}_tese.md` inteira. Parse mentalmente:

- Frontmatter: `verdict_atual`, `verdict_em`, `preco_em`, `checkpoints[]`, `created`, `updated`.
- Seção `## Lente`: bullets de pilares e bullets de kill-switches.
- Seção `## Checkpoints`: leia o cabeçalho e o primeiro parágrafo do checkpoint mais recente (`checkpoints[0]`).

## Passo 2 — Anúncio + lens check

Imprima:

```
Tese atual de {empresa}:
- Verdict: {verdict_atual} em {verdict_em} a R$ {preco_em}
- Lente: {N pilares}; última atualização da Lente em {se você conseguir inferir
  do git log ou do `updated`, anote; senão "não rastreado"}.
- Último checkpoint: {data} — {primeiro parágrafo, abreviado}.

Pergunta: algum pilar da Lente mudou desde {verdict_em}? Não pequenos
ajustes — mudança fundamental no entendimento da empresa.
(s/n)
```

Espere resposta.

- Se `s` → imprima:
  ```
  Isso é mudança de lente, não checkpoint. Saia daqui e rode:
  /tese {empresa} --lens
  ```
  Pare. Não escreva nada.

- Se `n` → continue para o Passo 3.

## Passo 3 — Coletar checkpoint

Pergunte uma coisa de cada vez:

1. `Preço de fechamento de hoje?`
2. `P/L LTM? (atualize mesmo que pareça igual ao último)`
3. `Outros múltiplos relevantes que você quer registrar?`
4. `Verdict: compra / neutro / venda?`
5. `Em 1-3 parágrafos: o que mudou desde {verdict_em} (último checkpoint)? Por que esse verdict agora a esse preço?`

## Passo 4 — Draft do delta

Construa um parágrafo curto de delta vs. o checkpoint anterior. Use os campos do `checkpoints[0]` que você leu no Passo 1. Format:

```
vs. último ({checkpoints[0].data}, {checkpoints[0].verdict} a R$ {checkpoints[0].preco}): {síntese de o que mudou — preço Δ%, verdict mudou ou se manteve, fundamento mudou ou não}.
```

## Passo 5 — Mostrar draft completo do checkpoint

```
Draft do checkpoint:

### {hoje} — {Verdict capitalizado} a R$ {preço}

Preço R$ {X,XX} · P/L LTM {X,X}× · {outros}

{prosa do usuário, com citações inseridas onde claims factuais aparecem}

vs. último ({data anterior}, {verdict anterior} a R$ {preço anterior}): {delta}

(fonte: ...)

OK assim ou edita?
```

## Passo 6 — Escrita

Quando o usuário confirmar:

### 6a) Atualizar `{empresa}_tese.md`

1. **Body:** localize a linha `## Checkpoints`. Imediatamente após (com uma linha em branco), insira o novo bloco do checkpoint, depois `\n\n---\n\n`. O efeito é prepend: o novo checkpoint fica logo após o cabeçalho `## Checkpoints` e antes do checkpoint anterior.

2. **Frontmatter:** atualize:
   - `verdict_atual: {novo verdict}`
   - `verdict_em: {hoje}`
   - `preco_em: {novo preço numérico}`
   - `checkpoints:` — prepend o novo checkpoint:
     ```yaml
     checkpoints:
       - {data: {hoje}, verdict: {verdict}, preco: {preço}}
       - {data: {data anterior}, verdict: {verdict anterior}, preco: {preço anterior}}
       ...
     ```
   - `updated: {hoje}`

3. **Callout no body:** atualize a linha após `# Tese — ...`:
   ```markdown
   > **Fact base:** [[{empresa}]] · **Verdict atual:** **{novo verdict}** (em {hoje} a R$ {novo preço})
   ```

### 6b) Atualizar `{empresa}.md` (entity page)

Localize o callout existente (geralmente `> Tese: ver [[{empresa}_tese]] (verdict atual: ...).`). Substitua por:

```markdown
> Tese: ver [[{empresa}_tese]] (verdict atual: {novo verdict} em {hoje}).
```

Bump `updated` no frontmatter de `{empresa}.md` para `{hoje}` também.

### 6c) Append em `log.md`

```
[tese-checkpoint] {hoje} {empresa} — added checkpoint (verdict: {novo verdict} a R$ {novo preço}; vs. {data anterior}: {se verdict mudou: "verdict alterado de X para Y"; senão "verdict mantido"})
```

## Passo 7 — Validar invariantes do frontmatter

Antes de finalizar, releia o frontmatter atualizado e confirme:

- `verdict_atual == checkpoints[0].verdict`
- `verdict_em == checkpoints[0].data`
- `preco_em == checkpoints[0].preco`

Se algum não bater, mostre o frontmatter ao usuário e peça correção. Não escreva inconsistente.

## Passo 8 — Confirmação

```
Pronto. Atualizei:
- equity-wiki/{empresa}_tese.md (novo checkpoint prepend, frontmatter atualizado)
- equity-wiki/{empresa}.md (callout sincronizado)
- Append em equity-wiki/log.md

Total de checkpoints agora: {N}.
```
````

- [ ] **Step 2: Walkthrough validation**

Read and verify:
- [ ] Step 1 specifies what to read and what to extract from each part.
- [ ] Step 2 has lens check question + escape route to `--lens` if changed.
- [ ] Step 3-5 has checkpoint collection + draft cycle.
- [ ] Step 6 has THREE separate write actions (tese page, entity page, log) with concrete instructions for each.
- [ ] Step 6a explicitly handles prepend of new checkpoint AND prepend in `checkpoints:` array.
- [ ] Step 7 validates the 3 invariants.
- [ ] Confirmation message at end.

- [ ] **Step 3: Commit**

```bash
git -C equity-wiki add .claude/skills/tese/interview_check.md
git -C equity-wiki commit -m "$(cat <<'EOF'
feat(skills): /tese mode checkpoint — interview prompt

Fluxo leve: carrega tese existente, lens check (escape para --lens se
mudou), entrevista de delta, prepend do checkpoint na página + no array
checkpoints[] do frontmatter, sincroniza callout em entity page, append
[tese-checkpoint] em log.md. Valida 3 invariantes do frontmatter antes
de finalizar.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: interview_lens.md — modo `lens-update`

**Files:**
- Create: `equity-wiki/.claude/skills/tese/interview_lens.md`

- [ ] **Step 1: Write interview_lens.md**

Create `equity-wiki/.claude/skills/tese/interview_lens.md` with this exact content:

````markdown
# Modo `lens-update` — reescrever Lente + forçar checkpoint de mudança

Você foi roteado pelo `SKILL.md`. O usuário digitou `/tese {empresa} --lens` (explicit). Significa: a Lente atual está incorreta ou desatualizada estruturalmente — não é só uma flutuação de checkpoint.

## Passo 1 — Carregar a tese existente

Read `equity-wiki/{empresa}_tese.md`. Parse:

- Frontmatter completo.
- `## Lente` atual: pilares e kill-switches.
- `## Checkpoints` — primeiro checkpoint (mais recente) para contexto.

Carregue também (em paralelo): entity page `{empresa}.md`, manifest, 1-2 digesteds mais recentes — pode haver fatos novos que justifiquem a mudança de lente.

## Passo 2 — Anúncio

```
Você está reescrevendo a LENTE de {empresa}. Lente atual:

{liste cada pilar atual numerado}

Quebra atual:
{liste cada kill-switch atual}

Mudança de lente é evento raro — só faça se sua compreensão fundamental
da empresa mudou. Pequenos ajustes vão em checkpoint normal.

Vamos por partes: você descreve em 1-2 frases o que mudou no seu entendimento,
depois reescrevemos cada pilar.
```

## Passo 3 — Resumo da mudança

Pergunte:

```
Em 1-2 frases: o que mudou na sua compreensão da empresa? Não a notícia
do trimestre — a interpretação fundamental.
```

Salve essa resposta — você vai usar no header do checkpoint forçado e no commit.

## Passo 4 — Reescrever a Lente

Para cada pilar atual, ofereça as opções: `manter / editar / remover`. Para edição, peça texto novo.

Depois, pergunte se quer **adicionar** novos pilares (ciclo "draft com citação → ok ou edita", igual ao modo `new`).

Mesma coisa para kill-switches: `manter / editar / remover` + opção de adicionar novos.

## Passo 5 — Mostrar Lente nova completa

```
Lente nova:

- {pilar 1 final}
- {pilar 2 final}
- ...

A tese se quebra se:
- {kill 1 final}
- ...

OK assim ou edita?
```

## Passo 6 — Checkpoint forçado

Pergunte uma de cada vez (igual modo `checkpoint`):

1. `Preço de fechamento de hoje?`
2. `Múltiplos relevantes?`
3. `Verdict: compra / neutro / venda?`

NÃO pergunte por prosa — você vai gerar baseado na mudança da Lente.

Construa o checkpoint:

```
### {hoje} — Mudança de lente: {resumo do passo 3, 8-12 palavras}

Preço R$ {X,XX} · P/L LTM {X,X}× · {outros}

**Mudança de lente.** {parágrafo descrevendo o que mudou no entendimento — use a resposta do passo 3 expandida com referências aos pilares editados}.

{verdict capitalizado} a R$ {preço}: {1 parágrafo curto explicando como a nova lente afeta o verdict atual}.

vs. último ({data anterior}, {verdict anterior} a R$ {preço anterior}): {delta — provavelmente focado em "o porquê mudou" mais que "o número mudou"}.

(fonte: ...)
```

Mostre ao usuário, peça `OK assim ou edita?`.

## Passo 7 — Escrita

### 7a) `{empresa}_tese.md`

1. **Substituir a seção `## Lente` inteira** pelo conteúdo novo.
2. **Prepend o checkpoint forçado** após `## Checkpoints`, com `\n\n---\n\n` separando.
3. **Atualizar frontmatter:**
   - `verdict_atual`, `verdict_em`, `preco_em`, prepend em `checkpoints:` (igual modo `checkpoint`).
   - `updated: {hoje}`.
4. **Sincronizar callout:**
   ```markdown
   > **Fact base:** [[{empresa}]] · **Verdict atual:** **{verdict}** (em {hoje} a R$ {preço})
   ```

### 7b) `{empresa}.md`

Atualize callout (igual modo `checkpoint`). Bump `updated`.

### 7c) `log.md`

```
[tese-lens] {hoje} {empresa} — lens rewritten ({resumo do passo 3}); verdict: {verdict} a R$ {preço}
```

## Passo 8 — Validação + confirmação

Valide invariantes do frontmatter (igual modo `checkpoint`):
- `verdict_atual == checkpoints[0].verdict`
- `verdict_em == checkpoints[0].data`
- `preco_em == checkpoints[0].preco`

Imprima:

```
Pronto. Atualizei:
- equity-wiki/{empresa}_tese.md (Lente reescrita + checkpoint "Mudança de lente")
- equity-wiki/{empresa}.md (callout sincronizado)
- Append em equity-wiki/log.md

Lente: {N pilares} (era {M}).
```
````

- [ ] **Step 2: Walkthrough validation**

Read and verify:
- [ ] Step 1: loads tese + entity + recent digesteds (since lens change often triggered by new info).
- [ ] Step 2: warns the user this is a rare event.
- [ ] Step 4: per-pillar manter/editar/remover + add new.
- [ ] Step 6: forced checkpoint header includes "Mudança de lente: {resumo}".
- [ ] Step 6: prose template starts with "**Mudança de lente.**".
- [ ] Step 7: rewrites lens section, prepends checkpoint, updates frontmatter, syncs callout.
- [ ] Step 8: invariant check.

- [ ] **Step 3: Commit**

```bash
git -C equity-wiki add .claude/skills/tese/interview_lens.md
git -C equity-wiki commit -m "$(cat <<'EOF'
feat(skills): /tese mode lens-update — interview prompt

Fluxo: carrega tese + entity + digesteds, anuncia que é evento raro,
reescreve Lente bullet por bullet (manter/editar/remover/adicionar),
força checkpoint marcado "Mudança de lente: {resumo}" com prose
specifica de mudança de lente, sincroniza callouts, append [tese-lens]
em log.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Smoke test — rodar `/tese cury` ponta-a-ponta

**Files:**
- Create (via skill): `equity-wiki/cury_tese.md`
- Modify (via skill): `equity-wiki/cury.md` (adiciona callout)
- Modify (via skill): `equity-wiki/log.md` (entradas `[tese-new]` e `[tese-checkpoint]`)

Este task é **interativo** — o engenheiro precisa estar numa sessão Claude Code com o skill instalado. Os passos abaixo são checklist de validação ponta-a-ponta dos 5 modos.

- [ ] **Step 1: Verificar pré-condições**

```bash
# cury.md existe e é entity page
grep -c "^type: entity" equity-wiki/cury.md
# expected: 1

# cury_tese.md NÃO existe ainda
ls equity-wiki/cury_tese.md 2>/dev/null && echo "EXISTS — aborte e investigue" || echo "OK — não existe"
```

- [ ] **Step 2: Modo `new` — `/tese cury`**

Numa nova sessão Claude Code (no diretório `Desktop\Equity-wiki\`), invoque:
```
/tese cury
```

O skill deve:
1. Detectar que `cury_tese.md` não existe → modo `new`.
2. Anunciar que vai ler entity + manifest + digesteds.
3. Detectar (ou não) seção legada em `cury.md`. (Cury hoje não tem `## Tese e Riscos`; tem conteúdo de tese disperso. O skill deve dizer "nenhuma seção legada detectada" ou similar.)
4. Conduzir a entrevista (Lente em 3 perguntas + checkpoint em 6 perguntas).

**Forneça respostas reais como analista.** Sample answers para validar (use suas próprias se preferir):

- Anomalia central: "ROE LTM de 78,8% em 2025 — sem precedente para incorporadora listada no Brasil ou no mundo."
- Pilares: (1) modelo capital-light via SPEs; (2) disciplina de mix MCMV (95% em 2025); (3) foco geográfico SP/RJ.
- Kill-switches: (1) Faixa 4 do MCMV reabre competição agressiva; (2) Cury sai de SP/RJ e dilui foco; (3) ROE estrutural cai abaixo de 30% por compressão sustentada.
- Preço: 30,20
- P/L LTM: 9,1
- P/VP: 5,4
- Verdict: neutro
- Prose: "ROE ainda em 78% mas a prévia 1T26 mostrou lançamentos -12% YoY, primeiro sinal de desaceleração. A R$ 30 o preço já reflete a tese de 'incorporadora excepcional'. Volto comprador abaixo de R$ 26 ou se a margem bruta segurar >38% no 1T26."

**Validações ao final:**

```bash
# 1. cury_tese.md foi criado
ls -la equity-wiki/cury_tese.md
# expected: arquivo existe

# 2. Frontmatter tem campos esperados
grep -E "^(type|empresa|ticker|fact_base|verdict_atual|verdict_em|preco_em):" equity-wiki/cury_tese.md
# expected: 7 linhas (uma por campo)

# 3. verdict_atual é "neutro"
grep "^verdict_atual:" equity-wiki/cury_tese.md
# expected: "verdict_atual: neutro"

# 4. Tem seção Lente com pilares
grep -c "^## Lente" equity-wiki/cury_tese.md
# expected: 1

# 5. Tem 1 checkpoint
grep -c "^### 2026-04-27" equity-wiki/cury_tese.md
# expected: 1

# 6. cury.md ganhou callout
grep -c "Tese: ver \[\[cury_tese\]\]" equity-wiki/cury.md
# expected: 1

# 7. log.md tem entrada [tese-new]
tail -5 equity-wiki/log.md | grep -c "tese-new"
# expected: 1
```

Se qualquer validação falhar, **não prossiga** — investigue qual passo do prompt falhou e fix antes.

- [ ] **Step 3: Modo `status` — `/tese cury --status`**

Invoque:
```
/tese cury --status
```

Deve imprimir algo como:
```
Tese: equity-wiki/cury_tese.md
Verdict: neutro (em 2026-04-27 a R$ 30,20)
Lente: 3 pilares · última atualização da página: 2026-04-27
Checkpoints: 1 (mais recente 2026-04-27)
Fact base: equity-wiki/cury.md
```

Verifique que os números batem com o que você criou no Step 2.

- [ ] **Step 4: Modo `checkpoint` — `/tese cury` (segunda vez)**

Invoque:
```
/tese cury
```

O skill deve detectar `cury_tese.md` existe → modo `checkpoint`. Vai mostrar a Lente atual e perguntar se algum pilar mudou.

Responda `n` (não mudou). Forneça novos valores:
- Preço: 28,50 (simulando uma queda)
- P/L LTM: 8,6
- Verdict: compra
- Prose: "Preço caiu 5,6% em 2 dias sem newsflow material. Lente intacta. A R$ 28,50 entra no range que eu havia sinalizado no checkpoint anterior — vira compra."

**Validações:**

```bash
# 1. checkpoints[] agora tem 2 entradas
grep -A 5 "^checkpoints:" equity-wiki/cury_tese.md | head -7
# expected: 2 entradas YAML, mais recente primeiro

# 2. verdict_atual mudou para "compra"
grep "^verdict_atual:" equity-wiki/cury_tese.md
# expected: "verdict_atual: compra"

# 3. preco_em mudou
grep "^preco_em:" equity-wiki/cury_tese.md
# expected: "preco_em: 28.50"

# 4. invariantes do frontmatter batem
# (manualmente: confirme que verdict_atual == primeiro item de checkpoints, etc)

# 5. cury.md callout foi atualizado
grep "Tese: ver \[\[cury_tese\]\]" equity-wiki/cury.md
# expected: deve dizer "verdict atual: compra em 2026-04-27" (ou data atual)

# 6. log.md tem [tese-checkpoint]
tail -5 equity-wiki/log.md | grep -c "tese-checkpoint"
# expected: 1
```

- [ ] **Step 5: Modo `carteira` — `/tese --carteira`**

Invoque:
```
/tese --carteira
```

Deve imprimir uma tabela com 1 linha (a Cury). Algo como:
```
| Empresa | Ticker | Verdict | Em | Preço | Checkpoints |
|---|---|---|---|---|---|
| cury | CURY3 | compra | 2026-04-27 | R$ 28,50 | 2 |

Total: 1 (1 compra, 0 neutro, 0 venda).
```

- [ ] **Step 6: Modo `lens-update` — `/tese cury --lens`**

Invoque:
```
/tese cury --lens
```

Deve carregar a Lente atual e perguntar o que mudou no entendimento.

Responda algo simples para testar (não precisa ser tese real):
- Mudança: "Identifiquei que o foco SP/RJ é mais que geográfico — é cultural; a empresa não saberia operar fora dessas duas capitais."
- Para os pilares atuais: edite o pilar 3 ("foco geográfico SP/RJ") para refletir a nova interpretação cultural.
- Sem novos pilares; sem novos kill-switches.
- Preço: 28,50 (mesmo)
- Verdict: compra (mesmo)

**Validações:**

```bash
# 1. checkpoints[] agora tem 3 entradas
grep -A 7 "^checkpoints:" equity-wiki/cury_tese.md | head -9

# 2. checkpoint mais recente tem header "Mudança de lente"
grep -A 2 "^## Checkpoints" equity-wiki/cury_tese.md | head -5
# expected: linha com "### 2026-04-27 — Mudança de lente: ..."

# 3. Pilar 3 da Lente foi atualizado
grep -A 10 "^## Lente" equity-wiki/cury_tese.md | head -12
# expected: pilar 3 reflete a nova interpretação

# 4. log.md tem [tese-lens]
tail -5 equity-wiki/log.md | grep -c "tese-lens"
# expected: 1
```

- [ ] **Step 7: Inspecionar mudanças não-commitadas**

O skill NÃO commita — alinha com o resto do pipeline (fetch.sh/ingest.sh também só escrevem arquivos + append em log.md, commit é manual).

Veja o que foi alterado pelo smoke test:

```bash
git -C equity-wiki status
git -C equity-wiki diff --stat
```

Esperado: `cury_tese.md` novo, `cury.md` modificado (callout), `log.md` modificado (3 entradas novas).

- [ ] **Step 8: Decidir manter ou descartar**

**Opção A — manter como tese real:** se as respostas que você forneceu são suas opiniões reais sobre Cury, commite manualmente:

```bash
git -C equity-wiki add cury_tese.md cury.md log.md
git -C equity-wiki commit -m "$(cat <<'EOF'
feat(cury): tese inicial + smoke test do skill /tese

Primeira tese ativa do wiki. Verdict inicial: neutro a R$ 30,20.
Validou ponta-a-ponta o skill /tese (modos new, status, checkpoint,
carteira, lens-update). Subsequentes mudanças no checkpoint refletem
o smoke test interativo, não decisões reais de carteira.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**Opção B — descartar smoke test:** se foram só dummy answers, reverte as alterações sem commitar (não há nada a fazer git reset, nada foi commitado ainda):

```bash
# Ver o que vai ser descartado
git -C equity-wiki status

# Descartar
git -C equity-wiki restore cury.md log.md      # reverte modificações nesses tracked files
rm equity-wiki/cury_tese.md                    # remove o arquivo novo (untracked)

# Confirmar limpo
git -C equity-wiki status
```

⚠️ **Aviso:** `git restore` descarta mudanças locais nesses arquivos. Confirme com `git diff` antes se quiser reaproveitar parte do conteúdo.

---

## Self-Review

(Run after writing the plan above.)

**Spec coverage check:**

| Spec section | Implemented in |
|---|---|
| §Page type tese (naming, frontmatter, body, link entity↔tese, cadência, vocabulário, valuation) | Task 1 |
| §Skill localização + 5 modos | Task 3 (router) + Tasks 4-6 (modes) |
| §SCHEMA.md adições | Task 1 |
| §CLAUDE.md adições | Task 2 |
| §Validação / smoke test | Task 7 |
| §Fora de escopo v1 (sem migração bulk, sem lint, sem index page) | Não implementado por design |

**Placeholder scan:** nenhum TBD/TODO no plano. Steps de prompts contêm o conteúdo completo dos arquivos.

**Type/naming consistency:**
- Mode names usados consistentemente: `new`, `checkpoint`, `lens-update`, `status`, `carteira`.
- Field names: `verdict_atual`, `verdict_em`, `preco_em`, `checkpoints` — consistentes em SKILL.md, prompts, smoke test.
- Log tags: `[tese-new]`, `[tese-checkpoint]`, `[tese-lens]` — consistentes em SCHEMA.md, CLAUDE.md, prompts.
- File paths: sempre `equity-wiki/` prefix em validações de bash.

**Open issues:** none. Tudo do v1 do spec está mapeado para uma task.
