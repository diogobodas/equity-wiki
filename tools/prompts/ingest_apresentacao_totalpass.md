# Task — Apresentação ingest com foco TotalPass

Você está extraindo dados sobre **TotalPass** de uma apresentação de resultados da Smart Fit (SMFT3). O arquivo a ler é `{{FULL_PATH}}` (período: {{PERIOD}}).

Leia o arquivo via `Read`. Em seguida, produza um digest markdown **focado APENAS em TotalPass** (ignore tudo que não seja TotalPass — academias próprias gerais, EBITDA consolidado, etc).

## O que extrair (se presente)

1. **Escala**: # academias parceiras Brasil/México (mil), cidades, usuários finais
2. **Frequência e receita** dentro da rede SmartFit Brasil (% freq, % receita)
3. **Mix TP1/TP2** ou tier breakdown / desconto médio / repasse
4. **Economics**: contribuição EBITDA TotalPass standalone, breakeven status, alavancagem G&A
5. **Comentários estratégicos**: canais B2B (PAT, Corporation, etc), parceiros novos (Banco do Brasil, Magalu), saída de academias, exclusividades
6. **Eventos corporativos**: M&A, mudança societária (TotalPass México controle), participação minoritária
7. **Disclosures novos** que apareçam pela primeira vez (ex: "primeira vez divulgando X")

## Output

Frontmatter YAML:

```yaml
---
type: apresentacao_totalpass
empresa: smart
periodo: {{PERIOD}}
source: sources/full/smart/{{PERIOD}}/apresentacao.md
ingested_on: 2026-05-01
---
```

Depois `# Apresentação SmartFit {{PERIOD}} — TotalPass digest` e o conteúdo organizado em seções (Escala / Economics / Estratégia conforme o que tiver).

## Regras

- **Cite cada fato** com `(fonte: sources/full/smart/{{PERIOD}}/apresentacao.md)`.
- **Não invente números.** Se um dado não aparece, omita — não estime.
- Se a apresentação **não menciona TotalPass**, produza:
  ```
  # Apresentação SmartFit {{PERIOD}} — TotalPass digest

  Não há disclosure sobre TotalPass nesta apresentação.

  (fonte: sources/full/smart/{{PERIOD}}/apresentacao.md)
  ```
- Sob 500 palavras. Markdown limpo, sem emoji.
- Use `[?]` após qualquer número de baixa confiança (ex: extraído de chart label sem rótulo claro).

## Output destination

Escreva o resultado via `Write` para o caminho:
`sources/digested/smart_apresentacao_{{PERIOD}}_totalpass_summary.md`

Não escreva nada além do que foi instruído. Não atualize manifest, não enfileire, apenas o digest.
