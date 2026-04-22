#!/usr/bin/env python3
"""
One-shot extraction from website/lessons.py + website/build.py into
content/*.md + content/*.yaml.

Usage: python3 scripts/extract_content.py

Writes:
  content/phases.yaml
  content/ui.yaml
  content/tech/t01.md          # EN (title + desc in frontmatter, body in markdown)
  content/tech/t01.ja.md       # JA (title + desc in frontmatter, body in markdown)
  content/theory/r01.md / .ja.md
  ... (one pair per lesson)

Idempotent: overwrites existing files. Run once during migration step 1.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'website'))

import build as build_mod
from lessons import LESSONS

CONTENT = ROOT / 'content'
TECH = CONTENT / 'tech'
THEORY = CONTENT / 'theory'


# -------- HTML -> Markdown converter (targeted at the lesson vocabulary) --------

def _decode_entities(s: str) -> str:
    """Decode the handful of entities we produce in lesson HTML."""
    return (
        s.replace('&lt;', '<')
         .replace('&gt;', '>')
         .replace('&amp;', '&')
         .replace('&quot;', '"')
         .replace('&#39;', "'")
    )


def _inline_to_md(s: str) -> str:
    """Convert inline HTML (strong, em, code, a) to markdown."""
    # <code>x</code> -> `x` (decode entities inside code spans first)
    s = re.sub(
        r'<code>(.*?)</code>',
        lambda m: '`' + _decode_entities(m.group(1)) + '`',
        s, flags=re.DOTALL,
    )
    # <strong>x</strong> -> **x**
    s = re.sub(r'<strong>(.*?)</strong>', lambda m: '**' + m.group(1) + '**', s, flags=re.DOTALL)
    # <em>x</em> -> *x*
    s = re.sub(r'<em>(.*?)</em>', lambda m: '*' + m.group(1) + '*', s, flags=re.DOTALL)
    # <a href="URL" ...>text</a> -> [text](URL)
    def _a(m):
        attrs = m.group(1)
        text = m.group(2)
        href_match = re.search(r'href="([^"]*)"', attrs)
        if not href_match:
            return text
        url = href_match.group(1)
        return f'[{text}]({url})'
    s = re.sub(r'<a\s+([^>]*)>(.*?)</a>', _a, s, flags=re.DOTALL)
    # <br> / <br/> -> two-space + newline (markdown line break)
    s = re.sub(r'<br\s*/?>', '  \n', s)
    # Decode remaining entities in plain text (after code spans already decoded).
    s = _decode_entities(s)
    return s


def _list_to_md(html: str, ordered: bool) -> str:
    """Convert <ul>/<ol> to markdown list."""
    items = re.findall(r'<li>(.*?)</li>', html, flags=re.DOTALL)
    out_lines = []
    for i, item in enumerate(items):
        prefix = f'{i+1}.' if ordered else '-'
        content = _inline_to_md(item.strip())
        # Compress internal whitespace in list item
        content = re.sub(r'\s+', ' ', content).strip()
        out_lines.append(f'{prefix} {content}')
    return '\n'.join(out_lines)


def _pre_code_to_md(html: str) -> str:
    """Convert <pre><code>...</code></pre> to fenced code block."""
    m = re.search(r'<pre><code[^>]*>(.*?)</code></pre>', html, flags=re.DOTALL)
    if not m:
        return html
    code = _decode_entities(m.group(1))
    return '```\n' + code + '\n```'


def _mermaid_to_md(html: str) -> str:
    """Convert <div class="mermaid">...</div> to a mermaid fenced block."""
    m = re.search(r'<div class="mermaid">\s*(.*?)\s*</div>', html, flags=re.DOTALL)
    if not m:
        return html
    body = m.group(1)
    return '```mermaid\n' + body + '\n```'


def _takeaways_to_md(html: str) -> str:
    """Keep takeaways as raw HTML - markdown passes it through."""
    return html


def html_to_markdown(html: str) -> str:
    """
    Convert lesson HTML string to markdown.

    The HTML is structured: h1/h2 headings, p (sometimes with class),
    pre/code blocks, ul/ol lists, mermaid divs, takeaways divs. We walk
    the string top-level and convert each block independently.
    """
    s = html.strip()
    out = []
    i = 0
    n = len(s)

    # Pattern matchers for top-level blocks, in order of preference
    block_matchers = [
        # takeaways div: keep as raw HTML
        (re.compile(r'<div class="takeaways">.*?</div>', re.DOTALL), 'takeaways'),
        # mermaid div: convert to fenced block
        (re.compile(r'<div class="mermaid">.*?</div>', re.DOTALL), 'mermaid'),
        # pre/code: convert to fenced block
        (re.compile(r'<pre><code[^>]*>.*?</code></pre>', re.DOTALL), 'pre'),
        # ul / ol
        (re.compile(r'<ul>.*?</ul>', re.DOTALL), 'ul'),
        (re.compile(r'<ol>.*?</ol>', re.DOTALL), 'ol'),
        # headings
        (re.compile(r'<h1>(.*?)</h1>', re.DOTALL), 'h1'),
        (re.compile(r'<h2>(.*?)</h2>', re.DOTALL), 'h2'),
        (re.compile(r'<h3>(.*?)</h3>', re.DOTALL), 'h3'),
        # paragraph with class
        (re.compile(r'<p\s+class="([^"]+)">(.*?)</p>', re.DOTALL), 'p_class'),
        # plain paragraph
        (re.compile(r'<p>(.*?)</p>', re.DOTALL), 'p'),
    ]

    while i < n:
        # Skip whitespace
        ws_end = i
        while ws_end < n and s[ws_end].isspace():
            ws_end += 1
        if ws_end > i:
            i = ws_end
            continue

        # Try each matcher at position i
        matched = False
        best = None
        for pat, kind in block_matchers:
            m = pat.match(s, i)
            if m:
                best = (m, kind)
                break
        if not best:
            # Unrecognized block - find the next '<' and skip to it
            nxt = s.find('<', i + 1)
            if nxt == -1:
                # Trailing text
                leftover = s[i:].strip()
                if leftover:
                    out.append(_inline_to_md(leftover))
                break
            leftover = s[i:nxt].strip()
            if leftover:
                out.append(_inline_to_md(leftover))
            i = nxt
            continue

        m, kind = best
        block = m.group(0)

        if kind == 'takeaways':
            out.append(_takeaways_to_md(block))
        elif kind == 'mermaid':
            out.append(_mermaid_to_md(block))
        elif kind == 'pre':
            out.append(_pre_code_to_md(block))
        elif kind == 'ul':
            out.append(_list_to_md(block, ordered=False))
        elif kind == 'ol':
            out.append(_list_to_md(block, ordered=True))
        elif kind == 'h1':
            out.append('# ' + _inline_to_md(m.group(1).strip()))
        elif kind == 'h2':
            out.append('## ' + _inline_to_md(m.group(1).strip()))
        elif kind == 'h3':
            out.append('### ' + _inline_to_md(m.group(1).strip()))
        elif kind == 'p_class':
            cls = m.group(1).strip()
            txt = _inline_to_md(m.group(2).strip())
            txt = re.sub(r'\s+', ' ', txt).strip()
            # attr_list extension: class attribute for a paragraph must be on
            # the line following the paragraph using `{: .class }` syntax.
            out.append(f'{txt}\n{{: .{cls} }}')
        elif kind == 'p':
            txt = _inline_to_md(m.group(1).strip())
            txt = re.sub(r'\s+', ' ', txt).strip()
            out.append(txt)

        i = m.end()

    return '\n\n'.join(out) + '\n'


# -------- YAML emission (no external deps; we produce a tidy subset) --------

def _yaml_escape(s: str) -> str:
    """Quote a string in YAML if it needs it, otherwise return bare."""
    if s is None:
        return '""'
    # Always quote for safety and consistency
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _write_frontmatter(lines: list[str], keys_ordered: list[tuple[str, object]]) -> str:
    """Emit minimal YAML frontmatter from an ordered list of (key, value) pairs."""
    out = ['---']
    for k, v in keys_ordered:
        if isinstance(v, (int, bool)):
            out.append(f'{k}: {v}')
        elif v is None:
            out.append(f'{k}: ~')
        else:
            out.append(f'{k}: {_yaml_escape(str(v))}')
    out.append('---')
    out.append('')
    return '\n'.join(out)


# -------- Main extraction --------

def extract_lessons() -> None:
    # Combined lesson metadata lookup
    meta_by_id: dict[str, dict] = {}
    for entry in build_mod.TECH_LESSONS:
        meta_by_id[entry['id']] = {**entry, 'kind': 'tech'}
    for entry in build_mod.THEORY_LESSONS:
        meta_by_id[entry['id']] = {**entry, 'kind': 'theory'}

    written = 0
    for lesson_id, langs in sorted(LESSONS.items()):
        if lesson_id not in meta_by_id:
            print(f'WARN: no metadata for {lesson_id}, skipping')
            continue
        meta = meta_by_id[lesson_id]
        kind = meta['kind']
        out_dir = TECH if kind == 'tech' else THEORY
        slug = lesson_id.lower()

        # --- EN file ---
        en_html = langs.get('en', '')
        en_md = html_to_markdown(en_html)
        en_fm_pairs = [('id', lesson_id)]
        if 'phase' in meta:
            en_fm_pairs.append(('phase', meta['phase']))
        if 'status' in meta:
            en_fm_pairs.append(('status', meta['status']))
        en_fm_pairs.append(('title', meta.get('title_en', '')))
        en_fm_pairs.append(('desc', meta.get('desc_en', '')))
        if 'analogy_en' in meta:
            en_fm_pairs.append(('analogy', meta.get('analogy_en', '')))
        fm = _write_frontmatter([], en_fm_pairs)
        (out_dir / f'{slug}.md').write_text(fm + en_md, encoding='utf-8')

        # --- JA file ---
        ja_html = langs.get('ja', '')
        ja_md = html_to_markdown(ja_html) if ja_html else ''
        ja_fm_pairs = [('title', meta.get('title_ja', '')), ('desc', meta.get('desc_ja', ''))]
        if 'analogy_ja' in meta:
            ja_fm_pairs.append(('analogy', meta.get('analogy_ja', '')))
        fm_ja = _write_frontmatter([], ja_fm_pairs)
        (out_dir / f'{slug}.ja.md').write_text(fm_ja + ja_md, encoding='utf-8')

        written += 2
    print(f'Wrote {written} lesson files under content/tech and content/theory')


def extract_phases() -> None:
    out = []
    out.append('# Phase metadata. One record per phase. Each record has')
    out.append('# title / subtitle / analogy in each supported language.')
    out.append('')
    for phase in build_mod.TECH_PHASES:
        out.append(f'- id: {phase["id"]}')
        for field in ('title', 'subtitle', 'analogy'):
            for lang in ('en', 'ja'):
                key = f'{field}_{lang}'
                if key in phase:
                    out.append(f'  {key}: {_yaml_escape(phase[key])}')
        out.append('')
    (CONTENT / 'phases.yaml').write_text('\n'.join(out), encoding='utf-8')
    print(f'Wrote content/phases.yaml ({len(build_mod.TECH_PHASES)} phases)')


def extract_ui() -> None:
    out = []
    out.append('# UI strings. Each key has a value per supported language.')
    out.append('# Site build reads this at compile time.')
    out.append('')
    for key, langmap in build_mod.UI.items():
        out.append(f'{key}:')
        for lang in ('en', 'ja'):
            if lang in langmap:
                out.append(f'  {lang}: {_yaml_escape(langmap[lang])}')
        out.append('')
    (CONTENT / 'ui.yaml').write_text('\n'.join(out), encoding='utf-8')
    print(f'Wrote content/ui.yaml ({len(build_mod.UI)} keys)')


def extract_misc() -> None:
    """Extract VIDEOS and RESOURCES to YAML so they don't stay orphaned in build.py."""
    # VIDEOS
    out = ['# Video gallery entries. Localized title + desc per language.', '']
    for v in build_mod.VIDEOS:
        out.append(f'- youtube_id: {v["youtube_id"]}')
        for field in ('title', 'desc'):
            for lang in ('en', 'ja'):
                k = f'{field}_{lang}'
                if k in v:
                    out.append(f'  {k}: {_yaml_escape(v[k])}')
        out.append('')
    (CONTENT / 'videos.yaml').write_text('\n'.join(out), encoding='utf-8')
    print(f'Wrote content/videos.yaml ({len(build_mod.VIDEOS)} videos)')

    # RESOURCES
    out = ['# External resources shown on the Resources page.', '']
    for r in build_mod.RESOURCES:
        out.append(f'- url: {_yaml_escape(r["url"])}')
        out.append(f'  domain: {_yaml_escape(r["domain"])}')
        for field in ('title', 'desc'):
            for lang in ('en', 'ja'):
                k = f'{field}_{lang}'
                if k in r:
                    out.append(f'  {k}: {_yaml_escape(r[k])}')
        out.append('')
    (CONTENT / 'resources.yaml').write_text('\n'.join(out), encoding='utf-8')
    print(f'Wrote content/resources.yaml ({len(build_mod.RESOURCES)} resources)')


if __name__ == '__main__':
    TECH.mkdir(parents=True, exist_ok=True)
    THEORY.mkdir(parents=True, exist_ok=True)
    extract_lessons()
    extract_phases()
    extract_ui()
    extract_misc()
