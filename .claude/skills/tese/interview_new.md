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
