"""
Loads lesson content and site metadata from the content/ tree.

Replaces the hard-coded LESSONS dict + metadata lists previously in
lessons.py / build.py. Everything the rest of the build consumes comes
from disk now.

Produces:
  LESSONS          {id: {lang: html_string}}
  TECH_LESSONS     [{id, phase, status, title_en/ja, desc_en/ja, ...}]
  THEORY_LESSONS   [{id, title_en/ja, desc_en/ja, analogy_en/ja}]
  TECH_PHASES      [{id, title_en/ja, subtitle_en/ja, analogy_en/ja}]
  UI               {key: {lang: string}}
  VIDEOS           [{youtube_id, title_en/ja, desc_en/ja}]
  RESOURCES        [{url, domain, title_en/ja, desc_en/ja}]

LANG_CODES is an ordered list of the language codes to render for.
Add 'pt' to LANG_CODES in step 4 to enable Portuguese output.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml
import markdown as md_lib


ROOT = Path(__file__).parent.parent
CONTENT = ROOT / 'content'

# Languages we render. Ordered: EN first (source of truth), then others.
# EN is authoritative; other languages fall back to EN at render time when a
# string or markdown body is missing/empty.
LANG_CODES = ['en', 'ja', 'pt']


# -------- markdown rendering --------

def render_md(body: str) -> str:
    """Render a lesson markdown body to HTML matching the current style."""
    md = md_lib.Markdown(
        extensions=['fenced_code', 'attr_list', 'tables', 'md_in_html'],
        output_format='html5',
    )
    html = md.convert(body)

    # Mermaid: python-markdown emits `<pre><code class="language-mermaid">...</code></pre>`.
    # Convert to the div the frontend mermaid.js script expects.
    def _mermaid(m: re.Match) -> str:
        inner = m.group(1)
        # Undo HTML escaping inside the code block - mermaid needs raw text.
        inner = (inner
                 .replace('&lt;', '<')
                 .replace('&gt;', '>')
                 .replace('&amp;', '&')
                 .replace('&quot;', '"')
                 .replace('&#39;', "'"))
        return f'<div class="mermaid">\n{inner}\n</div>'

    html = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        _mermaid,
        html,
        flags=re.DOTALL,
    )

    # Open external links in a new tab with safe rel attributes.
    # The legacy lesson HTML hand-wrote these; we re-add them here so the
    # markdown syntax [text](url) stays ergonomic.
    def _ext_link(m: re.Match) -> str:
        attrs = m.group(1)
        href = re.search(r'href="([^"]+)"', attrs)
        if not href:
            return m.group(0)
        url = href.group(1)
        if not url.startswith(('http://', 'https://')):
            return m.group(0)
        if 'target=' in attrs:
            return m.group(0)
        return f'<a {attrs} target="_blank" rel="noopener">'

    html = re.sub(r'<a ([^>]+)>', _ext_link, html)
    return html


# -------- frontmatter --------

_FM_RE = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z', re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    meta_text, body = m.group(1), m.group(2)
    meta = yaml.safe_load(meta_text) or {}
    return meta, body


# -------- lesson loading --------

def _lesson_paths() -> list[Path]:
    """Every .md file under content/tech and content/theory."""
    paths = []
    for sub in ('tech', 'theory'):
        paths.extend((CONTENT / sub).glob('*.md'))
    return sorted(paths)


def _split_slug(path: Path) -> tuple[str, str]:
    """'content/tech/t01.ja.md' -> ('T01', 'ja'). 'content/tech/t01.md' -> ('T01', 'en')."""
    stem = path.stem  # 't01.ja' or 't01'
    if '.' in stem:
        slug, lang = stem.rsplit('.', 1)
    else:
        slug, lang = stem, 'en'
    return slug.upper(), lang


def load_all() -> dict:
    """Load the entire content tree + YAML data files into a single namespace."""
    # -- Lessons ------------------------------------------------------
    # Nested: {lesson_id: {lang: {'meta': {...}, 'body': '...'}}}
    lesson_data: dict[str, dict] = {}
    for p in _lesson_paths():
        lid, lang = _split_slug(p)
        meta, body = parse_frontmatter(p.read_text(encoding='utf-8'))
        lesson_data.setdefault(lid, {})[lang] = {'meta': meta, 'body': body}

    # LESSONS dict expected by the rest of the build: {id: {lang: html_string}}
    LESSONS: dict[str, dict[str, str]] = {}
    for lid, langs in lesson_data.items():
        LESSONS[lid] = {}
        for lang, entry in langs.items():
            LESSONS[lid][lang] = render_md(entry['body'])

    # TECH_LESSONS / THEORY_LESSONS: rebuild the list-of-dict shape the old
    # build.py used. Metadata lives on the EN file (id, phase, status) and
    # on each lang's file (title, desc, analogy).
    tech, theory = [], []
    for lid in lesson_data:
        en_meta = lesson_data[lid].get('en', {}).get('meta', {})
        ja_meta = lesson_data[lid].get('ja', {}).get('meta', {})
        entry = {
            'id': lid,
            'title_en': en_meta.get('title', ''),
            'title_ja': ja_meta.get('title', ''),
            'desc_en': en_meta.get('desc', ''),
            'desc_ja': ja_meta.get('desc', ''),
        }
        if 'phase' in en_meta:
            entry['phase'] = en_meta['phase']
        if 'status' in en_meta:
            entry['status'] = en_meta['status']
        if 'analogy' in en_meta:
            entry['analogy_en'] = en_meta['analogy']
        if 'analogy' in ja_meta:
            entry['analogy_ja'] = ja_meta['analogy']

        if lid.startswith('T'):
            tech.append(entry)
        else:
            theory.append(entry)

    # Order: lessons are numbered in teaching order; sort by numeric suffix.
    def _num(lid: str) -> int:
        m = re.match(r'[A-Z](\d+)', lid)
        return int(m.group(1)) if m else 0

    tech.sort(key=lambda e: _num(e['id']))
    theory.sort(key=lambda e: _num(e['id']))

    # -- YAML data files ---------------------------------------------
    def _y(path):
        p = CONTENT / path
        if not p.exists():
            return []
        return yaml.safe_load(p.read_text(encoding='utf-8')) or []

    tech_phases = _y('phases.yaml')
    videos = _y('videos.yaml')
    resources = _y('resources.yaml')

    ui_raw = yaml.safe_load((CONTENT / 'ui.yaml').read_text(encoding='utf-8')) or {}

    return {
        'LESSONS': LESSONS,
        'TECH_LESSONS': tech,
        'THEORY_LESSONS': theory,
        'TECH_PHASES': tech_phases,
        'VIDEOS': videos,
        'RESOURCES': resources,
        'UI': ui_raw,
        'LANG_CODES': LANG_CODES,
    }
