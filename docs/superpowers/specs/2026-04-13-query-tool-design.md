# Query Tool Design

## Goal

A CLI tool (`tools/query.sh`) that answers free-form questions about wiki data by searching structured/, full/, and digested/ sources. Returns answers with source citations.

## Architecture

```
query.sh "pergunta"
    ↓
  bash generates inventory (empresas, períodos, fontes)
    ↓
  substitutes {{QUERY}} and {{INVENTORY}} into prompt template
    ↓
  cat prompt | claude --print --allowedTools "Bash" --permission-mode bypassPermissions
    ↓
  answer with citations (fonte: path)
```

## Files

- `tools/query.sh` — bash orchestrator
- `tools/prompts/query_system.md` — system prompt template

## query.sh

Bash script that:

1. Accepts a single argument: the question string
2. Generates an inventory of available data:
   - For each empresa in `sources/structured/`: list periods and source types (itr.json, dfp.json, release.json)
   - For each empresa in `sources/full/`: list periods and source types (.md files)
   - List generic sources in `sources/full/generic/`
   - List digested summaries in `sources/digested/`
3. Substitutes `{{QUERY}}` and `{{INVENTORY}}` into the prompt template
4. Pipes to `claude --print --allowedTools "Bash" --permission-mode bypassPermissions`
5. Prints the response to stdout

## query_system.md prompt

The prompt instructs the Claude agent to:

### Search order
1. **structured/** first — JSON files with clean numeric data. Use `cat` to read, `python -c` to extract specific fields.
2. **full/** second — raw extracted text from PDFs. This is the authoritative source when structured/ is missing data.
3. **digested/** third — LLM-generated summaries. Useful for context but may be incomplete.
4. **full/generic/** — cross-company spreadsheets and external sources.

### Handling spaced text in full/
PDF extraction sometimes produces text with spaces between characters (e.g., `D is tra to s` instead of `Distratos`). When searching full/ files:
- Use `sed 's/ //g'` or `tr -d ' '` to compress whitespace before matching
- Example: `cat file.md | tr -d ' ' | grep -i "distratos/vendasbrutas"`
- Once the line is found, read the surrounding context from the original file to get the actual values

### Rules
- **NEVER invent data.** Every number must come from a source file.
- If data is not found after searching all three layers, say "não encontrado" and list what was searched (files, grep patterns).
- **Always cite sources:** every data point gets `(fonte: path/to/file)`. For structured/, cite the JSON path. For full/, cite file and line number.
- Answer in Portuguese (pt-BR).
- Be concise — answer the question directly, then provide the citation.

### Available context
The prompt receives:
- `{{QUERY}}` — the user's question
- `{{INVENTORY}}` — list of available empresas, periods, and source types

## Usage

```bash
bash tools/query.sh "qual o distrato da Cury no 3T24?"
bash tools/query.sh "compare a margem bruta da Direcional vs Cury em 2024"
bash tools/query.sh "qual o ROE da Riva nos últimos 4 trimestres?"
bash tools/query.sh "série histórica de VSO da Direcional desde 2019"
```

## CLAUDE.md update

Add a "Query data" section:

```bash
bash tools/query.sh "pergunta em linguagem natural"
```
