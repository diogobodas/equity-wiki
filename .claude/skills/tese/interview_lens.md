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

Construa o checkpoint, com citações inline `(fonte: ...)` em cada claim factual seguindo `SCHEMA.md §Source Citations`:

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

Quando o usuário confirmar, **antes de escrever, normalize:**

- **Verdict:** lowercase exato (`compra`, `neutro`, `venda`). Variantes → mapeie ao canônico.
- **Preço:** vírgula → ponto decimal (`30,20` → `30.20`).

### 7a) `{empresa}_tese.md`

1. **Substituir a seção `## Lente` inteira** pelo conteúdo novo (mantendo a estrutura: bullets + `**A tese se quebra se:**` + bullets).
2. **Prepend o checkpoint forçado** após `## Checkpoints`, com `\n\n---\n\n` separando do checkpoint anterior.
3. **Atualizar frontmatter:**
   - `verdict_atual`, `verdict_em`, `preco_em`, prepend em `checkpoints:` (igual modo `checkpoint`).
   - `updated: {hoje}`.
4. **Sincronizar callout:**
   ```markdown
   > **Fact base:** [[{empresa}]] · **Verdict atual:** **{verdict}** (em {hoje} a R$ {preço})
   ```

### 7b) `{empresa}.md`

Atualize callout (igual modo `checkpoint`):
```markdown
> Tese: ver [[{empresa}_tese]] (verdict atual: {verdict} em {hoje}).
```

Bump `updated` no frontmatter de `{empresa}.md`.

### 7c) `log.md`

```
[tese-lens] {hoje} {empresa} — lens rewritten ({resumo do passo 3}); verdict: {verdict} a R$ {preço}
```

## Passo 8 — Validação + confirmação

Valide invariantes do frontmatter (igual modo `checkpoint`):
- `verdict_atual == checkpoints[0].verdict`
- `verdict_em == checkpoints[0].data`
- `preco_em == checkpoints[0].preco`

Se algum não bater, mostre o frontmatter ao usuário e peça correção. Não escreva inconsistente.

Imprima:

```
Pronto. Atualizei:
- equity-wiki/{empresa}_tese.md (Lente reescrita + checkpoint "Mudança de lente")
- equity-wiki/{empresa}.md (callout sincronizado)
- Append em equity-wiki/log.md

Lente: {N pilares} (era {M}).
```
