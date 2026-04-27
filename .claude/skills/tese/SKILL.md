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
| `{empresa} --carteira` ou múltiplas flags | erro | "Uso inválido. Veja /tese {empresa} ou /tese --carteira." |
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

3. **Argumento parece ticker em vez de slug?** Ex: usuário digita `/tese CURY3`. Detecte como possível ticker se o arg casa um destes padrões: B3 (`^[A-Z]{4}\d{1,2}$`, ex: CURY3, BBSE3), US (`^[A-Z]{1,5}$`, ex: AAPL, TSLA), ou simplesmente "todo maiúsculas". Procure em `equity-wiki/*.md` um arquivo cujo frontmatter tenha esse ticker em `aliases`. Se achar exatamente um, sugira: `Você quis dizer /tese {slug encontrado}? (s/n)`. Se múltiplos ou nenhum, peça desambiguação.

## Modo `status` (inline)

0. **Antes de prosseguir, execute os 3 edge cases de §Edge cases.** Se nenhum disparou (entidade existe, é listada, arg é slug), continue para o passo 1.
1. Read `equity-wiki/{empresa}_tese.md`. Se não existe, imprima `Tese para {empresa} ainda não criada. Use /tese {empresa} para começar.` e pare.
2. Parse o frontmatter mentalmente. Conte os bullets na seção `## Lente` antes do bloco `**A tese se quebra se:**` — chame esse número de **N pilares**.

3. Imprima:
   ```
   Tese: equity-wiki/{empresa}_tese.md
   Verdict: {verdict_atual} (em {verdict_em} a R$ {preco_em})
   Lente: {N} pilares · última atualização da página: {updated}
   Checkpoints: {len(checkpoints)} (mais recente {checkpoints[0].data})
   Fact base: equity-wiki/{fact_base}
   ```

## Modo `carteira` (inline)

1. Glob `equity-wiki/*_tese.md`. Para cada arquivo, leia até o segundo `---` (fim do frontmatter); como salvaguarda, leia no mínimo as primeiras 60 linhas. Frontmatters com muitos checkpoints podem passar de 30 linhas.
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
