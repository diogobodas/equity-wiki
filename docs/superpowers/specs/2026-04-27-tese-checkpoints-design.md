# Investment Thesis Pages — Lente + Checkpoints datados

**Status:** design aprovado, aguarda plano de implementação
**Autor / analista:** diogobodas
**Data:** 2026-04-27

## Contexto e motivação

A wiki carrega o *thesis* (CLAUDE.md). Hoje a "tese" vive embutida em ~14 entity pages como seção de formato livre ("Tese e Riscos", "Pontos a Monitorar", etc), sem padrão e sem âncora temporal. Problemas:

1. **Não dá para saber quando aquela opinião foi formada.** Ler `bradesco.md` hoje retorna a tese de quando — abr/26? jan/26? nov/25? Sem `em:` no nível da seção, é impossível.
2. **Não dá para auditar evolução do julgamento.** O git log preserva a evolução em diff de prosa, não em estrutura. Olhar para "como minha visão de Cury mudou em 2025-2026" é trabalho manual.
3. **Não dá para saber se a tese serve a hoje.** Investment opinion depende de preço × momento. Sem registro do preço da data de cada opinião, a tese fica "atemporal" — o que é falso.
4. **Não dá para extrair a carteira de teses ativas.** Sem campo padronizado de `verdict`, é impossível responder "quais empresas estou em compra hoje".

A solução é separar **fato** (entity page, fact base, modelo, números, eventos) de **opinião datada** (nova `tese` page, com Lente estável + Checkpoints datados price-aware).

## Decisões de design (com base em entrevista)

| Decisão | Escolha |
|---|---|
| Uso primário | B (decidir hoje) > A (auditoria) > C (carteira) |
| Layout | página separada por empresa (`{empresa}_tese.md`) |
| Estrutura interna | Lente estável (topo) + Stream de Checkpoints (mais recente primeiro) |
| Anatomia do checkpoint | lean / narrativo (header curto + 1-3 parágrafos de prosa) |
| Vocabulário do verdict | trinary simples: `compra` / `neutro` / `venda` |
| Horizonte explícito | não obrigatório — vai na prosa quando relevante |
| Âncora de valuation | nenhuma estrutural (sem TP / IRR / cenários obrigatórios). P/L como múltiplo default; analista escolhe o que faz sentido por setor |
| Cadência | event-driven (release com surpresa, fato relevante, news, price move >15%, releitura com mudança de visão) |
| Migração de páginas legadas | sem fase de migração explícita — skill em modo `new` resolve organicamente conforme analista revisita cada empresa |
| Criação | interativa via skill `/tese {empresa}` — entrevista com analista, não automação cega |

## Escopo

### v1 (este spec)

1. Novo tipo de página `tese` documentado em `SCHEMA.md`.
2. Convenções de frontmatter, vocabulário do verdict, cadência, link entity ↔ tese — em `SCHEMA.md`.
3. Skill `tese` em `equity-wiki/.claude/skills/tese/` com 3 modos: `new`, `checkpoint`, `lens-update`.
4. Comandos auxiliares: `/tese {empresa} --status`, `/tese --carteira`.
5. CLAUDE.md ganha bloco de comandos `### Tese` e bullet em `## Non-obvious rules`.

### Fora de escopo v1

- Migração bulk dos ~14 entity pages com seção legada — feita organicamente via modo `new` quando o analista revisita.
- Lint rule de `tese page staleness` — defer para v2; revisitar quando houver ≥5 teses ativas.
- Página índice gerada (`teses.md`) — substituída por `/tese --carteira` que lê frontmatters on-demand.
- Teses para empresas privadas (ifood, wellhub, revolut) — sem preço público, checkpoint price-aware não cabe.
- Teses para `concept`/`sector` pages (ex: `consignado_privado.md` que tem "Tese de investimento" hoje) — `tese` é exclusivo de entidade investível listada.

## Page type `tese`

### Naming

`{empresa}_tese.md` no root do wiki. Lowercase, snake_case. Exemplos: `cury_tese.md`, `porto_seguro_tese.md`, `bradesco_tese.md`.

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
checkpoints:                        # array, mais recente primeiro, por construção do skill
  - {data: 2026-04-27, verdict: neutro, preco: 30.20}
  - {data: 2026-01-10, verdict: compra, preco: 25.00}
created: 2026-01-10
updated: 2026-04-27
---
```

**Regras:**
- `verdict_atual` e `checkpoints[0].verdict` devem coincidir.
- `verdict_em` e `checkpoints[0].data` devem coincidir.
- `preco_em` e `checkpoints[0].preco` devem coincidir.
- `verdict_atual` ∈ `{compra, neutro, venda}` (lowercase, exato — para extração de carteira).

### Estrutura do corpo

```markdown
# Tese — {Empresa} ({TICKER})

> **Fact base:** [[{empresa}]] · **Verdict atual:** **{verdict}** (em {data} a R$ {preco})
>
> *Esta página carrega a opinião datada. Tudo que é fato (modelo, números, eventos) vive em [[{empresa}]].*

## Lente

3-5 bullets sobre como o analista fundamentalmente entende a empresa.
Estável; muda raramente. Cada bullet com citação.

- Pilar 1 ... (fonte: ...)
- Pilar 2 ... (fonte: ...)

**A tese se quebra se:**
- Condição 1
- Condição 2
- Condição 3

---

## Checkpoints

### YYYY-MM-DD — {Verdict capitalizado} a R$ {preço}

Preço R$ X,XX · P/L LTM X,X× · {múltiplos relevantes}

{1-3 parágrafos: visão atual, lente intacta ou não, o que mudou}

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

- **Entity page** (`cury.md`) ganha callout no topo, **logo após o parágrafo intro**:
  ```markdown
  > Tese: ver [[cury_tese]] (verdict atual: neutro em 2026-04-27).
  ```
- **Tese page** (`cury_tese.md`) tem callout fixo **logo após H1**:
  ```markdown
  > **Fact base:** [[cury]] · **Verdict atual:** **neutro** (em 2026-04-27 a R$ 30,20)
  ```

A linha do entity page é mantida em sincronia pelo skill ao criar/atualizar checkpoints.

### Cadência (norma editorial)

Event-driven. Triggers:
- ITR/DFP/release ingerido com surpresa (vs. expectativa do analista no checkpoint anterior)
- Fato relevante material
- Mudança de preço >15% desde último checkpoint (em qualquer direção)
- News exógena que afeta a tese (regulatória, M&A no setor, etc)
- Releitura espontânea em que a visão do analista mudou

Sem cadência mínima. Páginas podem ficar paradas por 6-9 meses se nada material aconteceu — está ok.

## Skill `tese`

### Localização

`equity-wiki/.claude/skills/tese/`

```
SKILL.md            # description + entrypoint logic
interview_new.md    # prompt para modo new
interview_check.md  # prompt para modo checkpoint
interview_lens.md   # prompt para modo lens-update
```

`SKILL.md` declara o trigger e roteia para um dos 3 modos baseado em flags + presença do arquivo `_tese.md`.

### Modos

| Comando | Modo | Quando |
|---|---|---|
| `/tese {empresa}` | `new` se `_tese.md` não existe; `checkpoint` se existe | default |
| `/tese {empresa} --lens` | `lens-update` | analista quer reescrever a Lente |
| `/tese {empresa} --status` | `status` (read-only) | mostra cabeçalho da tese atual sem entrevistar |
| `/tese --carteira` | `carteira` (read-only) | lista todas as teses com `verdict_atual`, `verdict_em`, `preco_em` (lê todos os frontmatters) |

### Modo `new` — fluxo da entrevista

1. **Carregamento de contexto.** Skill lê:
   - `{empresa}.md` (entity page)
   - `sources/manifests/{empresa}.json`
   - 2-3 digesteds mais recentes do empresa
   - Se houver seção "Tese e Riscos" (ou similar) na entity page: extrai como input.

2. **Lente — entrevista bullet por bullet.**
   - "Em 1 parágrafo, qual é a anomalia central dessa empresa?"
   - "Quais 2-4 pilares sustentam isso?"
   - "O que **quebra** essa lente? Lista 2-3 condições."
   - Após cada resposta, Claude propõe um draft do bullet + citação extraída do contexto carregado, analista confirma ou edita.

3. **Checkpoint inicial — entrevista.**
   - "Preço de fechamento de hoje?" (analista digita)
   - "P/L LTM? P/VP? (ou outro múltiplo relevante para o setor)"
   - "Verdict: compra / neutro / venda?"
   - "1-3 parágrafos: por que esse verdict a esse preço, hoje? Cite o que pesa mais."

4. **Escrita.**
   - Cria `{empresa}_tese.md` com frontmatter + Lente + 1º Checkpoint.
   - **Atualiza `{empresa}.md`** — remove seção "Tese e Riscos" legada (se houver), adiciona callout `> Tese: ver [[{empresa}_tese]] ...` logo após intro.
   - Append `[tese-new]` ao `log.md` para ambos arquivos.

### Modo `checkpoint` — entrevista mais leve

1. **Carregamento.** Skill lê `{empresa}_tese.md` inteira.
2. **Lente check.** Mostra a Lente atual ao analista, pergunta: *"Algum pilar mudou desde o último checkpoint ({data anterior})?"*
3. Se *não*:
   - "Preço hoje? Múltiplos?"
   - "Verdict?"
   - "1-3 parágrafos: rationale + delta vs. último checkpoint."
4. Se *sim*: skill avisa que isso é mudança de lente e oferece rodar `--lens`. Sem confirmação explícita, segue como (3).
5. **Escrita.**
   - Prepend novo checkpoint após `## Checkpoints`.
   - Atualiza frontmatter: `verdict_atual`, `verdict_em`, `preco_em`, prepend em `checkpoints:`, bump `updated`.
   - Atualiza callout em `{empresa}.md` para refletir novo verdict/data.
   - Append `[tese-checkpoint]` ao `log.md`.

### Modo `lens-update` — explicit

1. Mesmo fluxo de `new` mas só na seção Lente. Diff implícito vs. Lente anterior.
2. Após reescrita, força um checkpoint imediato com header `### {data} — Mudança de lente: {breve resumo}` e o body começa com "**Mudança de lente.** {o que mudou no entendimento da empresa}". Resto do checkpoint segue normal.
3. Append `[tese-lens]` ao `log.md`.

### Modo `status` — read-only

Imprime no terminal:
```
Tese: cury_tese.md
Verdict: neutro (em 2026-04-27 a R$ 30,20)
Lente: 4 pilares · última atualização 2026-01-10
Checkpoints: 2 (mais recente 2026-04-27)
```

### Modo `carteira` — read-only

Lê todos os arquivos `*_tese.md` no root, extrai frontmatters, imprime tabela ordenada por `verdict_em` desc:

```
| Empresa | Ticker | Verdict | Em | Preço | Checkpoints |
|---|---|---|---|---|---|
| cury | CURY3 | neutro | 2026-04-27 | 30.20 | 2 |
| bradesco | BBDC4 | compra | 2026-04-25 | 14.80 | 5 |
| ...
```

## SCHEMA.md — adições

1. Tabela `## Page Types` ganha linha:
   ```
   | tese | Investment thesis com Lente estável + Checkpoints datados price-aware (uma por empresa investível). | cury_tese.md, bradesco_tese.md |
   ```

2. Nova seção `## Tese pages` (após `## Page Types`) com tudo de §"Page type `tese`" deste spec.

3. Seção `## Wiki Operations` ganha sub-seção `### Tese (novo / checkpoint)`:
   - Resumo: manual, interativo via skill `/tese`, não passa por queue de wiki_update.
   - Modos do skill em uma linha cada.
   - Log entries: `[tese-new]`, `[tese-checkpoint]`, `[tese-lens]`.

## CLAUDE.md — adições

1. Em `## Commands`, novo bloco depois de `### Lint`:
   ```markdown
   ### Tese (interactive — investment thesis pages)

   /tese {empresa}              # auto-detecta modo (new se não existe, checkpoint se existe)
   /tese {empresa} --status     # mostra cabeçalho da _tese.md
   /tese --carteira             # lista todas as teses ativas (extraído de frontmatters)
   /tese {empresa} --lens       # força modo lens-update

   Skill é interativa — Claude entrevista o analista no terminal.
   Vive em .claude/skills/tese/. Não passa por claude --print (diferente do resto do pipeline).
   ```

2. Em `## Non-obvious rules`, novo bullet:
   ```
   - **Tese ≠ entity.** Investment thesis vive em `{empresa}_tese.md` (type: tese), com Lente estável + Checkpoints datados (frontmatter expõe `verdict_atual` + `verdict_em` para extração via `/tese --carteira`). Entity page (`{empresa}.md`) é fact base e não carrega opinião sobre preço/timing. Criar/atualizar via `/tese {empresa}` (interativo).
   ```

## Validação / smoke test

Antes de declarar v1 pronto:

1. Rodar `/tese cury` em modo `new` ponta-a-ponta. Validar:
   - `cury_tese.md` criado com frontmatter válido + Lente + 1 checkpoint.
   - `cury.md` ganhou callout no topo, perdeu seção legada (se havia).
   - `log.md` tem entrada `[tese-new]`.
2. Rodar `/tese cury --status` — saída legível.
3. Rodar `/tese cury` (segunda vez) — deve cair em modo `checkpoint`. Validar prepend de checkpoint, atualização de frontmatter, atualização do callout em `cury.md`.
4. Rodar `/tese --carteira` — tabela com a única tese existente.
5. Rodar `/tese cury --lens` — forçar lens-update. Validar checkpoint marcado como "Mudança de lente".

## Riscos / open questions futuras

1. **Multi-currency.** Spec atual assume R$ ou USD via campo `preco_em` numérico. Se houver tese em outra moeda (CHF, EUR), pode ser preciso campo `preco_moeda`. Defer.
2. **Variação de tickers.** Empresas com BDR ou ADR (PAGS, NU) — usar ticker primário da bolsa principal. Defer normalização.
3. **Lint integration.** Regra de staleness defer para v2; revisitar quando houver ≥5 teses ativas para calibrar threshold (180d sugerido).
4. **Página `teses.md` index.** Não é v1 — `/tese --carteira` substitui. Pode virar v2 se Obsidian-graph quiser visibilidade.
