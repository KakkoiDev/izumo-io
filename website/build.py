#!/usr/bin/env python3
"""KakkoiSchool static site builder. Outputs to docs/ for GitHub Pages."""

import os
import re
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from engine import Engine
from content_loader import load_all

ROOT = Path(__file__).parent
TEMPLATES = ROOT / 'templates'
PAGES = ROOT / 'pages'
STATIC = ROOT / 'static'
OUT = ROOT.parent / 'docs'

# All lesson content + metadata comes from content/*.md and content/*.yaml.
# See content_loader.py for the shape.
_DATA = load_all()
LESSONS = _DATA['LESSONS']
TECH_PHASES = _DATA['TECH_PHASES']
TECH_LESSONS = _DATA['TECH_LESSONS']
THEORY_LESSONS = _DATA['THEORY_LESSONS']
UI = _DATA['UI']
VIDEOS = _DATA['VIDEOS']
RESOURCES = _DATA['RESOURCES']
LANGS = _DATA['LANG_CODES']

LANG_LABELS = {'en': 'English', 'ja': '日本語', 'pt': 'Português'}


# -- Content data ----------------------------------------------------------

def t(data, lang):
    """Get localized value with EN fallback. Empty strings fall back too."""
    return data.get(lang) or data.get('en', '')



PAGE_TITLES = {
    'index.html': {'en': '', 'ja': ''},
    'tech-lessons.html': {'en': 'Technical Lessons', 'ja': '\u6280\u8853\u30ec\u30c3\u30b9\u30f3'},
    'theory-lessons.html': {'en': 'Theory & Life Lessons', 'ja': '\u7406\u8ad6\u3068\u30e9\u30a4\u30d5\u30ec\u30c3\u30b9\u30f3'},
    'videos.html': {'en': 'Lesson Videos', 'ja': '\u30ec\u30c3\u30b9\u30f3\u52d5\u753b'},
    'resources.html': {'en': 'Resources', 'ja': '\u30ea\u30bd\u30fc\u30b9'},
}



# -- Build logic ------------------------------------------------------------

def resolve_includes(html):
    """Pre-resolve {% include "file" %} before template rendering."""
    inc_re = re.compile(r'\{%\s*include\s+["\']([^"\']+)["\']\s*%\}')
    while True:
        new = inc_re.sub(lambda m: (TEMPLATES / m.group(1)).read_text(), html)
        if new == html:
            break
        html = new
    return html


_SLUG_SANITIZE_RE = re.compile(
    r'[^a-z0-9\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\u3005]+'
)


def _heading_slug(text):
    """Turn heading text into a URL-safe slug. Keeps Japanese characters."""
    text = re.sub(r'<[^>]+>', '', text).strip().lower()
    slug = _SLUG_SANITIZE_RE.sub('-', text).strip('-')
    return slug


def add_heading_anchors(html, levels=(1, 2, 3)):
    """Add id and clickable anchor link to every heading at the given levels.

    Skips headings that already have an id and headings nested inside an <a>.
    """
    used = {}
    pattern = re.compile(
        r'<(h[' + ''.join(str(l) for l in levels) + r'])([^>]*)>(.*?)</\1>',
        re.DOTALL,
    )

    def in_anchor(start):
        # Look backwards for the most recent unclosed <a ...>
        before = html[:start]
        last_open = before.rfind('<a ')
        last_close = before.rfind('</a>')
        return last_open > last_close

    def replace(match):
        if in_anchor(match.start()):
            return match.group(0)
        tag, attrs, content = match.group(1), match.group(2) or '', match.group(3)
        if re.search(r'\bid\s*=', attrs):
            return match.group(0)
        base = _heading_slug(content)
        if not base:
            return match.group(0)
        count = used.get(base, 0)
        used[base] = count + 1
        slug = base if count == 0 else f'{base}-{count + 1}'
        return (
            f'<{tag}{attrs} id="{slug}">'
            f'<a class="heading-anchor" href="#{slug}">{content}</a>'
            f'</{tag}>'
        )

    return pattern.sub(replace, html)


def localize_list(items, lang):
    """Create localized version of a list of dicts.

    Keys ending in _<lang> (for any lang in LANGS) get merged into a base
    key using the requested language with EN fallback.
    """
    suffixes = tuple(f'_{l}' for l in LANGS)
    result = []
    for item in items:
        loc = {}
        seen = set()
        for key in item:
            if key.endswith(suffixes):
                base = key.rsplit('_', 1)[0]
                if base not in seen:
                    seen.add(base)
                    loc[base] = item.get(f'{base}_{lang}') or item.get(f'{base}_en', '')
            else:
                loc[key] = item[key]
        result.append(loc)
    return result


def _lang_paths(current_lang, is_lesson):
    """Compute the href base each language should link to from the current page.

    Non-EN languages live in a subfolder (docs/ja/, docs/pt/). EN lives at
    the root (docs/). Lesson pages are one level deeper inside lessons/.
    """
    result = {}
    for target in LANGS:
        if not is_lesson:
            if current_lang == target:
                result[target] = './'
            elif current_lang == 'en':
                result[target] = f'{target}/'
            elif target == 'en':
                result[target] = '../'
            else:
                result[target] = f'../{target}/'
        else:
            if current_lang == target:
                result[target] = './'
            elif target == 'en':
                result[target] = '../../lessons/'
            elif current_lang == 'en':
                result[target] = f'../{target}/lessons/'
            else:
                result[target] = f'../../{target}/lessons/'
    return result


def _lang_paths_json(paths):
    """Serialize a {lang: href} dict for use in data-lang-paths."""
    import json
    return json.dumps(paths, ensure_ascii=False, separators=(',', ':'))


def build_context(lang, page_file):
    """Build template context for rendering a page."""
    is_root = lang == 'en'

    ui = {k: t(v, lang) for k, v in UI.items()}

    titles = PAGE_TITLES.get(page_file, {})
    page_title = t(titles, lang)

    tech_phases = localize_list(TECH_PHASES, lang)
    tech_lessons = localize_list(TECH_LESSONS, lang)
    theory_lessons = localize_list(THEORY_LESSONS, lang)
    videos = localize_list(VIDEOS, lang)
    resources = localize_list(RESOURCES, lang)

    lang_options = ''
    for l in LANGS:
        selected = ' selected' if l == lang else ''
        lang_options += f'<option value="{l}"{selected}>{LANG_LABELS[l]}</option>'

    paths = _lang_paths(lang, is_lesson=False)

    return {
        'lang': lang,
        'HTML_LANG': lang,
        'STATIC_PATH': 'static/' if is_root else '../static/',
        'NAV_PREFIX': '',
        'LANG_PATHS_JSON': _lang_paths_json(paths),
        'PAGE_FILE': page_file,
        'PAGE_TITLE': page_title,
        'LANG_OPTIONS': lang_options,
        'HAS_MERMAID': False,
        'COPYRIGHT_YEAR': str(datetime.now().year),
        'DISCORD_URL': 'https://discord.gg/YrtdssGUJa',
        'GITHUB_URL': 'https://github.com/KakkoiDev/izumo-io',
        **ui,
        'tech_phases': tech_phases,
        'tech_lessons': tech_lessons,
        'theory_lessons': theory_lessons,
        'videos': videos,
        'resources': resources,
    }


def build_lesson_context(lang, lesson_id, page_file):
    """Build template context for a lesson page."""
    is_root = lang == 'en'
    ui = {k: t(v, lang) for k, v in UI.items()}

    # Find lesson metadata for title, preferring current lang then EN fallback.
    all_lessons = TECH_LESSONS + THEORY_LESSONS
    lesson_meta = next((l for l in all_lessons if l['id'] == lesson_id), {})
    page_title = (lesson_meta.get(f'title_{lang}')
                  or lesson_meta.get('title_en')
                  or lesson_id)

    is_tech = lesson_id.startswith('T')
    back_url = '../tech-lessons.html' if is_tech else '../theory-lessons.html'
    back_label = ui.get('back_to_tech', '') if is_tech else ui.get('back_to_theory', '')

    # Compute prev/next within same group
    group = [l for l in (TECH_LESSONS if is_tech else THEORY_LESSONS)
             if l.get('status') != 'coming-soon']
    ids = [l['id'] for l in group]
    idx = ids.index(lesson_id) if lesson_id in ids else -1
    prev_url = f'{ids[idx - 1].lower()}.html' if idx > 0 else ''
    next_url = f'{ids[idx + 1].lower()}.html' if 0 <= idx < len(ids) - 1 else ''

    lang_options = ''
    for l in LANGS:
        selected = ' selected' if l == lang else ''
        lang_options += f'<option value="{l}"{selected}>{LANG_LABELS[l]}</option>'

    paths = _lang_paths(lang, is_lesson=True)

    slug = lesson_id.lower()
    return {
        'lang': lang,
        'HTML_LANG': lang,
        'STATIC_PATH': '../static/' if is_root else '../../static/',
        'NAV_PREFIX': '../' ,
        'LANG_PATHS_JSON': _lang_paths_json(paths),
        'PAGE_FILE': f'{slug}.html',
        'PAGE_TITLE': page_title,
        'LANG_OPTIONS': lang_options,
        'HAS_MERMAID': True,
        'COPYRIGHT_YEAR': str(datetime.now().year),
        'DISCORD_URL': 'https://discord.gg/YrtdssGUJa',
        'GITHUB_URL': 'https://github.com/KakkoiDev/izumo-io',
        'back_url': back_url,
        'back_label': back_label,
        'prev_url': prev_url,
        'prev_label': ui.get('prev_lesson', ''),
        'next_url': next_url,
        'next_label': ui.get('next_lesson', ''),
        **ui,
    }


def build():
    # Atomic build: write to temp, then swap
    tmp = Path(tempfile.mkdtemp(dir=OUT.parent, prefix='.docs_build_'))
    try:
        _build_to(tmp)
        old = OUT.with_name('.docs_old') if OUT.exists() else None
        if old:
            OUT.rename(old)
        tmp.rename(OUT)
        if old:
            shutil.rmtree(old)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def _build_to(out):
    out.mkdir(parents=True, exist_ok=True)

    if STATIC.exists():
        shutil.copytree(STATIC, out / 'static')

    engine = Engine()
    placeholder = '<!-- LESSON_CONTENT -->'

    # -- Regular pages --
    for src in sorted(PAGES.glob('*.html')):
        for lang in LANGS:
            html = resolve_includes(src.read_text())
            ctx = build_context(lang, src.name)
            html = engine.render(html, ctx)
            html = add_heading_anchors(html)

            if lang == 'en':
                dest = out / src.name
            else:
                dest = out / lang / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(html)
            print(f'  {dest.relative_to(out)}')

    # -- Lesson pages --
    lesson_tpl_raw = (TEMPLATES / 'lesson.html').read_text()
    lesson_tpl = resolve_includes(lesson_tpl_raw)

    for lesson_id, content in sorted(LESSONS.items()):
        # Skip coming-soon lessons with no content
        if not content.get('en'):
            continue
        slug = lesson_id.lower()
        page_file = f'lessons/{slug}.html'

        for lang in LANGS:
            lesson_html = content.get(lang) or content.get('en', '')
            lesson_html = add_heading_anchors(lesson_html)
            ctx = build_lesson_context(lang, lesson_id, page_file)
            rendered = engine.render(lesson_tpl, ctx)
            rendered = rendered.replace(placeholder, lesson_html)

            if lang == 'en':
                dest = out / 'lessons' / f'{slug}.html'
            else:
                dest = out / lang / 'lessons' / f'{slug}.html'
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(rendered)

        print(f'  lessons/{slug}.html')

    # -- CNAME for custom domain --
    (out / 'CNAME').write_text('school.kakkoi.dev\n')

    # GitHub Pages needs this to skip Jekyll processing
    (out / '.nojekyll').write_text('')
    print(f'-> {out}/')


if __name__ == '__main__':
    build()
