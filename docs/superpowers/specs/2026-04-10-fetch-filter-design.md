# Fetch Filter — Design Spec

**Data:** 2026-04-10
**Escopo:** Mecanismo de filtragem para o fetch agent — human-in-the-loop na discovery, automático depois

---

## Problema

O fetch agent baixa todos os releases e fatos relevantes da CVM, incluindo duplicatas em inglês, relatórios de securitizadora, e outros documentos irrelevantes. Precisamos de um filtro inteligente.

## Decisões de design

| Decisão | Escolha |
|---------|---------|
| Onde vive o perfil | Campo `fetch_profile` no manifest da empresa |
| Primeira vez | `--discover`: baixa amostra de 1 trimestre, LLM classifica, propõe default, humano aprova |
| Formato | Mapa de categorias → include/exclude com descriptions e sample_files |
| Rodadas seguintes | LLM classifica cada doc novo nas categorias existentes, aplica filtro |
| DFP/ITR | Sempre incluídos, sem filtro (documentos estruturados, não ambíguos) |
| Doc não classificável | Include por default + reporta como unclassified |

## Dois modos de operação

### Modo discovery (`--discover`)

```
bash tools/fetch.sh TEND3 --discover
```

Invocado na primeira vez para uma empresa, ou para re-calibrar o perfil.

**Fluxo:**
1. `fetch.sh` verifica que o manifest não tem `fetch_profile` (ou `--discover` força re-discovery)
2. Resolve o trimestre mais recente com releases via `cvm_fetch.py list --types release,fato_relevante`
3. Baixa TODOS os docs daquele trimestre para um diretório temporário
4. Invoca `claude --print` com prompt de discovery. O LLM:
   - Para cada arquivo, lê o `original_filename` + primeiras páginas (cabeçalho do PDF)
   - Classifica em categorias funcionais
   - Propõe `fetch_profile` com include/exclude + descrições
   - Imprime o perfil proposto formatado para o humano
5. O humano revisa o output no terminal
6. Se aprova, `fetch.sh` salva o `fetch_profile` no manifest
7. Limpa dir temporário

**Output para o humano:**

```
=== Fetch Profile proposto para TEND3 (amostra: 4T25) ===

  [include] release_resultado_pt     — Release de resultados em português (1.5 MB)
  [include] apresentacao_resultado   — Apresentação/earnings deck (10.7 MB)
  [exclude] release_resultado_en     — Release em inglês (duplicata) (1.2 MB)
  [exclude] relatorio_securitizadora — Relatório securitizadora (1.1 MB)
  [include] fato_relevante           — Fatos relevantes corporativos (~100 KB cada)

Salvar este perfil? (s/n/editar)
```

Se `s`, salva no manifest. Se `editar`, abre o JSON no `$EDITOR` ou imprime instruções para ajuste manual.

### Modo normal (com filtro)

```
bash tools/fetch.sh TEND3 --horizon 1y --types release,fato_relevante
```

Quando `fetch_profile` existe no manifest:

1. Lista docs na CVM, detecta gaps (como hoje)
2. Baixa cada gap para diretório temporário
3. LLM classifica o doc numa categoria do `fetch_profile` (usa `description` + `sample_files` como referência)
4. Se `action=include` → move para `sources/undigested/`
5. Se `action=exclude` → deleta
6. Se unclassified → move para `sources/undigested/` + reporta
7. Resumo: X baixados, Y filtrados, Z unclassified

**Sem `fetch_profile`:** comportamento atual (baixa tudo) + warning sugerindo `--discover`.

**DFP/ITR:** bypass total, sempre download direto para `sources/undigested/`. Sem classificação.

## Formato do `fetch_profile` no manifest

Novo campo em `sources/manifests/{empresa}.json`:

```json
{
  "fetch_profile": {
    "_created": "2026-04-10",
    "_sample_period": "4T25",
    "categories": {
      "release_resultado_pt": {
        "action": "include",
        "description": "Release de resultados em português",
        "sample_files": ["TEND3_4T25_release_1010843.pdf"]
      },
      "release_resultado_en": {
        "action": "exclude",
        "description": "Release de resultados em inglês (duplicata)",
        "sample_files": ["TEND3_4T25_release_1010845.pdf"]
      },
      "apresentacao_resultado": {
        "action": "include",
        "description": "Apresentação de resultados / earnings deck",
        "sample_files": ["TEND3_4T25_release_1011039.pdf"]
      },
      "relatorio_securitizadora": {
        "action": "exclude",
        "description": "Relatório de agente fiduciário / securitizadora",
        "sample_files": ["TEND3_4T25_release_1010847.pdf"]
      },
      "fato_relevante": {
        "action": "include",
        "description": "Fatos relevantes corporativos",
        "sample_files": ["TEND3_4T25_fato_relevante_979561.pdf"]
      }
    }
  }
}
```

**Notas:**
- `sample_files` serve de âncora — o LLM usa como referência para classificar docs futuros
- `description` ajuda tanto o humano a entender quanto o LLM a reclassificar
- Categorias são livres — o LLM cria as que fizerem sentido na discovery
- Um doc futuro que não encaixa em nenhuma categoria é reportado como "unclassified" e incluído por default

## Mudanças nos arquivos existentes

| Arquivo | Mudança |
|---------|---------|
| `tools/fetch.sh` | Novo flag `--discover`. Quando presente, invoca prompt de discovery em vez do normal. Lógica de interação humana (s/n/editar). Salva fetch_profile no manifest. |
| `tools/prompts/fetch_system.md` | Adicionar seção de filtro: se `fetch_profile` presente, classificar e filtrar docs IPE. |
| `tools/prompts/fetch_discover.md` | **Novo.** Prompt de discovery: inspecionar docs, classificar, propor perfil. |
| `tools/lib/cvm_fetch.py` | Sem mudança — já retorna `original_filename` no download. |
| `sources/manifests/{empresa}.json` | Novo campo `fetch_profile` adicionado pela discovery. |

## Fora de escopo

- Filtragem por conteúdo semântico profundo (ex: NLP no corpo do fato relevante)
- UI web para seleção — interação é terminal-only
- Perfil compartilhado entre empresas do mesmo setor (cada empresa tem o seu)
