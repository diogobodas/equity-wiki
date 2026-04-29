#!/usr/bin/env python3
"""Notion API client for the Capstone digest pipeline.

Public API:
    load_config()                    -> dict
    load_state()                     -> dict
    save_state(state)                -> None
    list_new_or_edited(config)       -> list[dict]  # filters by last_edited_time vs state
    fetch_page_blocks(page_id)       -> list[dict]
    blocks_to_markdown(blocks)       -> str         (pure, no I/O)
    page_to_undigested(meta)         -> Path
    mark_processed(page_id, edited)  -> None        (updates local state, NOT Notion)
    extract_empresa(tags, config)    -> str         (maps multi-select tags to known empresa; "generic" fallback)

Env var required: NOTION_TOKEN.
Config source: sources/manifests/_notion.json.
State file: sources/manifests/_notion_state.json (tracks processed_pages by last_edited_time).

Design note: state-tracking replaces the Notion-property-based pending/done flow
from the original spec (Capstone DB has no ingest property — schema-driven change).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "sources" / "manifests" / "_notion.json"
UNDIGESTED_DIR = REPO_ROOT / "sources" / "undigested"


# ---------- Config / state ----------

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _state_path(config: dict) -> Path:
    rel = config.get("state_file", "sources/manifests/_notion_state.json")
    return REPO_ROOT / rel


def load_state(config: dict | None = None) -> dict:
    if config is None:
        config = load_config()
    p = _state_path(config)
    if not p.exists():
        return {"last_run_at": None, "processed_pages": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(state: dict, config: dict | None = None) -> None:
    """Atomically persist state via temp-file + os.replace.

    Prevents corruption on interrupted writes and is safe under concurrent
    mark_processed() calls (last-writer-wins on os.replace is atomic per POSIX
    and on Windows NTFS as of Python 3.3+).
    """
    import os
    import tempfile
    if config is None:
        config = load_config()
    p = _state_path(config)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix="._notion_state_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        os.replace(tmp, p)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def mark_processed(page_id: str, last_edited_time: str, config: dict | None = None) -> None:
    if config is None:
        config = load_config()
    state = load_state(config)
    state.setdefault("processed_pages", {})[page_id] = last_edited_time
    save_state(state, config)


# ---------- HTTP client ----------

def _token() -> str:
    tok = os.environ.get("NOTION_TOKEN")
    if not tok:
        # fallback: try reading from .env at repo root
        env_path = REPO_ROOT / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("NOTION_TOKEN="):
                    tok = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not tok:
        raise RuntimeError(
            "NOTION_TOKEN not set. Set env var or put NOTION_TOKEN=... in .env"
        )
    return tok


def _headers(config: dict) -> dict:
    return {
        "Authorization": f"Bearer {_token()}",
        "Notion-Version": config.get("api_version", "2022-06-28"),
        "Content-Type": "application/json",
    }


def _request(method: str, url: str, config: dict, json_body: dict | None = None) -> dict:
    max_retries = int(config.get("max_retries", 5))
    rps = float(config.get("rate_limit_rps", 3))
    min_interval = 1.0 / rps if rps > 0 else 0.0

    last_call = getattr(_request, "_last_call", 0.0)
    elapsed = time.time() - last_call
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)

    for attempt in range(max_retries):
        resp = requests.request(
            method, url, headers=_headers(config), json=json_body, timeout=30
        )
        _request._last_call = time.time()  # type: ignore[attr-defined]
        if resp.status_code == 429:
            wait = min(2 ** attempt, 30)
            print(f"WARN: Notion 429, sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        if resp.status_code >= 400:
            raise RuntimeError(
                f"Notion API {method} {url} -> {resp.status_code}: {resp.text[:500]}"
            )
        return resp.json()
    raise RuntimeError(f"Retries exhausted for {method} {url}")


# ---------- Rich text + block conversion ----------

def _rich_text(rich: list[dict]) -> str:
    if not rich:
        return ""
    return "".join(r.get("plain_text", "") for r in rich)


def blocks_to_markdown(blocks: list[dict]) -> str:
    """Convert a flat list of Notion blocks to markdown.

    Supports: heading_1/2/3, paragraph, bulleted_list_item, numbered_list_item,
    code, quote, divider, to_do. Unsupported types emit a warning line and
    log to stderr. Never raises.
    """
    out: list[str] = []
    numbered_counter = 0

    for block in blocks:
        btype = block.get("type", "unknown")
        payload = block.get(btype, {}) or {}
        text = _rich_text(payload.get("rich_text", []))

        if btype == "paragraph":
            out.append(text)
            numbered_counter = 0
        elif btype == "heading_1":
            out.append(f"# {text}")
            numbered_counter = 0
        elif btype == "heading_2":
            out.append(f"## {text}")
            numbered_counter = 0
        elif btype == "heading_3":
            out.append(f"### {text}")
            numbered_counter = 0
        elif btype == "bulleted_list_item":
            out.append(f"- {text}")
            numbered_counter = 0
        elif btype == "numbered_list_item":
            numbered_counter += 1
            out.append(f"{numbered_counter}. {text}")
        elif btype == "code":
            lang = payload.get("language", "")
            out.append(f"```{lang}")
            out.append(text)
            out.append("```")
            numbered_counter = 0
        elif btype == "quote":
            out.append(f"> {text}")
            numbered_counter = 0
        elif btype == "divider":
            out.append("---")
            numbered_counter = 0
        elif btype == "to_do":
            checked = payload.get("checked", False)
            mark = "x" if checked else " "
            out.append(f"- [{mark}] {text}")
            numbered_counter = 0
        elif btype == "callout":
            icon = payload.get("icon", {}).get("emoji", "") or ""
            prefix = f"{icon} " if icon else ""
            out.append(f"> {prefix}{text}")
            numbered_counter = 0
        elif btype == "toggle":
            out.append(f"**{text}**" if text else "")
            numbered_counter = 0
        elif btype == "image":
            url = ""
            if payload.get("type") == "external":
                url = payload.get("external", {}).get("url", "")
            elif payload.get("type") == "file":
                url = payload.get("file", {}).get("url", "")
            caption = _rich_text(payload.get("caption", []))
            out.append(f"![{caption}]({url})" if url else "")
            numbered_counter = 0
        else:
            out.append(f"> [bloco não-suportado: {btype}]")
            print(f"WARN: unsupported Notion block type {btype!r}", file=sys.stderr)
            numbered_counter = 0

    return "\n\n".join(line for line in out if line is not None)


# ---------- Database query + page fetching ----------

def _summarize_page(page: dict, config: dict) -> dict:
    """Flatten a Notion page object to {id, url, title, created, edited, properties, tags}."""
    props = page.get("properties", {})
    title_prop = config.get("title_property", "Name")

    title = ""
    title_data = props.get(title_prop, {})
    if title_data.get("type") == "title":
        title = _rich_text(title_data.get("title", []))

    tags_prop = config.get("tags_property", "Tags")
    tags: list[str] = []
    tags_data = props.get(tags_prop, {})
    if tags_data.get("type") == "multi_select":
        tags = [m.get("name", "") for m in tags_data.get("multi_select", [])]

    empresa = extract_empresa(tags, config)

    return {
        "id": page["id"],
        "url": page.get("url", ""),
        "title": title,
        "created_time": page.get("created_time", ""),
        "last_edited_time": page.get("last_edited_time", ""),
        "tags": tags,
        "empresa": empresa,
    }


def extract_empresa(tags: list[str], config: dict) -> str:
    """Map Notion Tags multi-select to a known empresa; returns 'generic' if no match."""
    if not tags:
        return "generic"
    mapping = {k.lower(): v for k, v in (config.get("tag_to_empresa", {}) or {}).items()}
    known = set(config.get("known_empresas", []) or [])
    for tag in tags:
        norm = tag.lower().strip()
        if norm in mapping and mapping[norm]:
            return mapping[norm]
        if norm in known:
            return norm
    return "generic"


def list_new_or_edited(config: dict | None = None) -> list[dict]:
    """Return list of pages that are new or edited since last ingest (per state file).

    No Notion-side filter — database has no ingest property. We list all pages and
    filter client-side by last_edited_time vs state.processed_pages[page_id].
    """
    if config is None:
        config = load_config()
    state = load_state(config)
    processed = state.get("processed_pages", {}) or {}

    db_id = config["database_id"]
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    body = {"page_size": 100}

    pending: list[dict] = []
    cursor = None
    while True:
        if cursor:
            body["start_cursor"] = cursor
        data = _request("POST", url, config, body)
        for page in data.get("results", []):
            pid = page["id"]
            edited = page.get("last_edited_time", "")
            prev = processed.get(pid)
            if prev is None or edited > prev:
                pending.append(_summarize_page(page, config))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return pending


def fetch_page_blocks(page_id: str, config: dict | None = None) -> list[dict]:
    if config is None:
        config = load_config()
    return list(_iter_blocks(page_id, config))


def _iter_blocks(block_id: str, config: dict):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    cursor = None
    while True:
        q = "?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        data = _request("GET", url + q, config)
        for child in data.get("results", []):
            yield child
            if child.get("has_children"):
                yield from _iter_blocks(child["id"], config)
        if not data.get("has_more"):
            return
        cursor = data.get("next_cursor")


# ---------- Slug + frontmatter + undigested write ----------

_SLUG_RE = re.compile(r"[^a-z0-9_]+")


def _slugify(s: str, max_len: int = 80) -> str:
    """Slugify with length cap. Windows MAX_PATH is 260; long Notion titles
    (e.g. SQL queries) blew past this and made write_text crash. 80 chars
    leaves room for empresa prefix + short_id suffix + path."""
    s = (s or "").lower().strip()
    s = _SLUG_RE.sub("_", s)
    s = s.strip("_") or "untitled"
    if len(s) > max_len:
        s = s[:max_len].rstrip("_")
    return s


def _build_slug(meta: dict) -> str:
    empresa = meta.get("empresa", "") or ""
    title = meta.get("title", "") or ""
    short_id = meta["id"].replace("-", "")[:8]
    if empresa and empresa != "generic":
        return f"{_slugify(empresa)}_{_slugify(title)}_{short_id}"
    return f"{_slugify(title)}_{short_id}"


def _escape_yaml(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def _frontmatter(meta: dict) -> str:
    lines = ["---", "source: notion", f"notion_page_id: {meta['id']}"]
    if meta.get("url"):
        lines.append(f"notion_url: {meta['url']}")
    lines.append(f'title: "{_escape_yaml(meta.get("title", ""))}"')
    if meta.get("created_time"):
        lines.append(f"created: {meta['created_time']}")
    if meta.get("last_edited_time"):
        lines.append(f"edited: {meta['last_edited_time']}")
    if meta.get("empresa"):
        lines.append(f'empresa: {meta["empresa"]}')
    tags = meta.get("tags", []) or []
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f'  - "{_escape_yaml(t)}"')
    lines.append("---")
    return "\n".join(lines)


def page_to_undigested(page_meta: dict, config: dict | None = None) -> Path:
    """Fetch blocks, convert to markdown, write to sources/undigested/notion_<slug>.md.

    Does NOT update state — caller (ingest.sh route) marks processed only after
    the digest pipeline completes successfully.
    """
    if config is None:
        config = load_config()
    blocks = fetch_page_blocks(page_meta["id"], config)
    body_md = blocks_to_markdown(blocks)
    slug = _build_slug(page_meta)
    fm = _frontmatter(page_meta)
    title = (page_meta.get("title") or "").strip()
    heading = f"# {title}\n\n" if title else ""
    content = f"{fm}\n\n{heading}{body_md}\n"
    UNDIGESTED_DIR.mkdir(parents=True, exist_ok=True)
    out = UNDIGESTED_DIR / f"notion_{slug}.md"
    out.write_text(content, encoding="utf-8")
    return out


if __name__ == "__main__":
    sys.exit("notion_fetch.py is a library; use tools/fetch_notion.sh")
