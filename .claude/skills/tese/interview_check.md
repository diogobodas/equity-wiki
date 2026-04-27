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

Para cada afirmação factual na prosa do analista, insira citação inline `(fonte: ...)` seguindo o formato de `SCHEMA.md §Source Citations`:
- Qualitativo / contexto: `(fonte: full/{empresa}/{periodo}/{tipo}.md §{seção})`
- Numérico: `(fonte: structured/{empresa}/{periodo}/{tipo}.json :: canonical.{path})`
- Legacy / digest-only: `(fonte: digested/{name}_summary.md)`
- Web: `(fonte: url, confiabilidade: oficial|editorial|community)`

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

Quando o usuário confirmar, **antes de escrever, normalize:**

- **Verdict:** converta para lowercase exato (`compra`, `neutro`, `venda`). Se o analista digitou variantes (`Compra`, `comprar`, `BUY`, `buy`, `Vender`, etc), mapeie para o canônico antes de gravar. Variante reconhecida ≠ exata é OK; variante não reconhecida → pergunte ao analista qual dos 3 buckets se aplica.
- **Preço:** se o analista digitou vírgula decimal (PT-BR: `30,20`), converta para ponto decimal antes de gravar (`30.20`). YAML trata `30,20` como string, não como número, e quebra a ordenação numérica em `/tese --carteira`.

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
