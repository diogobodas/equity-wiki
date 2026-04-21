#!/usr/bin/env python3
"""
Wiki link graph — build adjacency from [[wikilinks]] and compute
candidate pages for incremental wiki updates via BFS subgraph.

The graph is **undirected**: if A links to B, both are neighbours.
This means "pages that link to the changed company" are also candidates,
which is exactly what we want (e.g. incorporadoras.md links to cury.md,
so a new Cury digest should flag incorporadoras.md for update).

Usage (CLI):
    python tools/lib/wiki_graph.py candidates <digest1> [<digest2> ...] [--depth 2]
    # Prints newline-separated list of candidate wiki page filenames.

    python tools/lib/wiki_graph.py show <page.md>
    # Prints neighbours at depth 1 and 2 for inspection/debugging.
"""

import re
import glob
import os
import sys
from collections import defaultdict, deque

SKIP = {'CLAUDE.md', 'README.md', 'SCHEMA.md', 'log.md', 'index.md'}
WIKILINK_RE = re.compile(r'\[\[([^\]|#\n]+)')


def build_graph(wiki_root='.'):
    """Return undirected adjacency: {page.md: set(page.md)}"""
    graph = defaultdict(set)
    for path in glob.glob(os.path.join(wiki_root, '*.md')):
        page = os.path.basename(path)
        if page in SKIP:
            continue
        try:
            text = open(path, encoding='utf-8').read()
        except Exception:
            continue
        for m in WIKILINK_RE.finditer(text):
            raw = m.group(1).strip()
            target = raw.lower().replace(' ', '_')
            if not target.endswith('.md'):
                target += '.md'
            # undirected: both directions
            graph[page].add(target)
            graph[target].add(page)
    return graph


def digest_to_root(digest_name):
    """
    Maps a digested filename to its primary wiki page.

    Examples:
        cury_itr_3T25_summary.md              -> cury.md
        direcional_dfp_2025_summary.md        -> direcional.md
        notion_agibank_btg_34300ca3_summary.md -> agibank.md
        notion_abecip_bbi_4fc00ca3_summary.md  -> None (generic concept)
    """
    base = os.path.basename(digest_name)
    # strip trailing _summary.md or _guard_report.md
    for suffix in ('_summary.md', '_guard_report.md', '.md'):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    parts = base.split('_')
    if not parts:
        return None
    empresa = parts[1] if parts[0] == 'notion' and len(parts) > 1 else parts[0]
    # guard against empty or obviously non-empresa tokens
    if not empresa or len(empresa) < 2:
        return None
    return f"{empresa}.md"


def bfs_subgraph(graph, roots, depth=2):
    """
    BFS from each root page up to `depth` hops (undirected).
    Returns the set of all visited page names.
    """
    visited = set(roots)
    queue = deque((r, 0) for r in roots if r is not None)
    while queue:
        node, d = queue.popleft()
        if d >= depth:
            continue
        for nb in graph.get(node, set()):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, d + 1))
    return visited


def candidates(digests, graph, depth=2, wiki_root='.'):
    """
    Given a list of digest filenames, compute the set of wiki pages that
    are candidates for update (intersection of BFS subgraph with pages
    that actually exist on disk).

    Returns (candidates: list[str], roots: set[str], fallback: bool)
    fallback=True means no roots were found in the graph (new empresa),
    caller should fall back to full page list.
    """
    roots = {digest_to_root(d) for d in digests} - {None}
    existing = {os.path.basename(p) for p in glob.glob(os.path.join(wiki_root, '*.md'))} - SKIP

    # Roots that don't exist yet are new pages (creates) — still include if in graph
    # roots that DO exist seed the BFS
    seeded_roots = roots & (existing | set(graph.keys()))
    fallback = len(seeded_roots) == 0

    if fallback:
        return sorted(existing), roots, True

    subgraph = bfs_subgraph(graph, seeded_roots, depth)
    return sorted(subgraph & existing), roots, False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser(description='Wiki link graph utilities')
    sub = ap.add_subparsers(dest='cmd')

    p_cand = sub.add_parser('candidates', help='List candidate pages for given digests')
    p_cand.add_argument('digests', nargs='+', help='Digest filenames (basename or path)')
    p_cand.add_argument('--depth', type=int, default=2, help='BFS depth (default 2)')
    p_cand.add_argument('--root', default='.', help='Wiki root directory')
    p_cand.add_argument('--show-roots', action='store_true', help='Print root pages to stderr')

    p_show = sub.add_parser('show', help='Show neighbours of a page')
    p_show.add_argument('page', help='Wiki page filename')
    p_show.add_argument('--depth', type=int, default=2)
    p_show.add_argument('--root', default='.')

    args = ap.parse_args()

    if args.cmd == 'candidates':
        g = build_graph(args.root)
        cands, roots, fallback = candidates(args.digests, g, args.depth, args.root)
        if args.show_roots:
            print(f"roots: {sorted(roots)}", file=sys.stderr)
            print(f"fallback={fallback}", file=sys.stderr)
        for p in cands:
            print(p)

    elif args.cmd == 'show':
        g = build_graph(args.root)
        result = bfs_subgraph(g, {args.page}, args.depth)
        result.discard(args.page)
        existing = {os.path.basename(p) for p in glob.glob(os.path.join(args.root, '*.md'))} - SKIP
        print(f"Subgraph of {args.page} (depth={args.depth}):")
        for p in sorted(result & existing):
            print(f"  {p}")
        orphans = result - existing
        if orphans:
            print(f"  [linked but not on disk: {sorted(orphans)}]")

    else:
        ap.print_help()
        sys.exit(1)
