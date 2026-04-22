#!/usr/bin/env python3
"""
Idempotent translator for the content/ tree.

Rules:
- A markdown sibling file (e.g. t01.ja.md next to t01.md) gets translated
  only when it is MISSING or EMPTY. Never overwrites real content.
- A YAML field (e.g. title_pt next to title_en) gets filled only when
  missing or empty. Never overwrites existing values.
- Manual refresh path: delete the sibling file, or clear the YAML field,
  then push. Pipeline regenerates just that one.

Targets JA and PT; add entries to TARGETS to extend.

Runs as a step in .github/workflows/translate-content.yml but is also
runnable locally if you export GEMINI_API_KEY.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import yaml

try:
    from google import genai  # type: ignore
    from google.genai.errors import APIError  # type: ignore
except ImportError:
    print('install google-genai:  pip install google-genai', file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).parent.parent
CONTENT = ROOT / 'content'

API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    print('GEMINI_API_KEY not set', file=sys.stderr)
    sys.exit(2)

CLIENT = genai.Client(api_key=API_KEY)
MODEL = 'gemini-2.5-flash'

TARGETS = [
    ('ja', 'Japanese'),
    ('pt', 'Portuguese (Brazilian)'),
]


# -------- prompts --------

MD_PROMPT = """\
Translate the following markdown lesson document from English to {lang_name}.

Rules:
- Preserve the YAML frontmatter delimiters `---` at the top and bottom of
  the frontmatter block. Inside the frontmatter, keep the keys exactly
  (do not translate keys). Translate only the string values of the
  `title` and `desc` fields. Leave `id`, `phase`, `status`, `analogy`,
  and any other frontmatter fields untouched.
- Preserve every markdown structure: headings (#, ##), bullet lists,
  ordered lists, tables, fenced code blocks, links, raw HTML tags, and
  attribute-list syntax like `{{: .lesson-intro }}`.
- Do not translate code inside code blocks (```), inline code (`like
  this`), URLs, HTML class names, HTML tag names, or mermaid diagrams.
- Return the full translated document only. No commentary, no fences
  around the whole output.

Source:
{source}
"""

FIELD_PROMPT = """\
Translate the following short text from English to {lang_name}.
Return only the translation, no quotes, no commentary.

Source:
{source}
"""


def _generate_with_retry(prompt: str, attempts: int = 5) -> str:
    """Call the model with backoff. Re-raise after the last attempt."""
    last_err: Exception | None = None
    for i in range(attempts):
        try:
            resp = CLIENT.models.generate_content(model=MODEL, contents=prompt)
            return resp.text or ''
        except APIError as e:
            last_err = e
            # 429 (rate limit) and 5xx (server) are worth retrying.
            status = getattr(e, 'code', None)
            retryable = status in (429, 500, 502, 503, 504)
            if not retryable or i == attempts - 1:
                raise
            sleep = 2 ** i  # 1, 2, 4, 8, 16 seconds
            print(f'  API {status}, retry {i+1}/{attempts-1} in {sleep}s', file=sys.stderr)
            time.sleep(sleep)
    # unreachable
    if last_err:
        raise last_err
    return ''


def translate_md(source: str, lang_name: str) -> str:
    text = _generate_with_retry(MD_PROMPT.format(lang_name=lang_name, source=source))
    return text.strip() + '\n'


def translate_field(source: str, lang_name: str) -> str:
    if not source.strip():
        return ''
    text = _generate_with_retry(FIELD_PROMPT.format(lang_name=lang_name, source=source))
    return text.strip()


# -------- markdown sibling files --------

_FM_RE = re.compile(r'\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z', re.DOTALL)


def _parse_fm(text: str) -> tuple[dict, str]:
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def is_empty_translation(path: Path) -> bool:
    """A translation file counts as 'empty' if it has no body and no title/desc."""
    text = path.read_text(encoding='utf-8')
    meta, body = _parse_fm(text)
    if body.strip():
        return False
    if (meta.get('title') or '').strip():
        return False
    if (meta.get('desc') or '').strip():
        return False
    return True


def _is_source_md(path: Path) -> bool:
    """'t01.md' is a source. 't01.ja.md' / 't01.pt.md' are translations."""
    return '.' not in path.stem


def translate_missing_md() -> tuple[list[Path], list[Path]]:
    created: list[Path] = []
    failed: list[Path] = []
    sources = sorted(p for p in CONTENT.rglob('*.md') if _is_source_md(p))
    for src in sources:
        for code, name in TARGETS:
            sibling = src.with_name(f'{src.stem}.{code}.md')
            if sibling.exists() and not is_empty_translation(sibling):
                continue
            print(f'translate {src.relative_to(ROOT)} -> {sibling.name}', flush=True)
            try:
                translated = translate_md(src.read_text(encoding='utf-8'), name)
                sibling.write_text(translated, encoding='utf-8')
                created.append(sibling)
                # Gentle rate-limiting between successful calls.
                time.sleep(0.5)
            except Exception as e:
                print(f'  FAILED: {e}', file=sys.stderr, flush=True)
                failed.append(sibling)
    return created, failed


# -------- YAML files with _en / _ja / _pt fields --------

def _find_en_fields(record: dict) -> list[str]:
    """Return the BASE names (without _en) of any *_en fields in a record."""
    return [k[:-3] for k in record.keys() if k.endswith('_en')]


def _fill_record(record: dict) -> bool:
    """For each *_en field, fill missing or empty sibling fields for each target."""
    changed = False
    for base in _find_en_fields(record):
        en_val = record.get(f'{base}_en', '')
        if not en_val:
            continue
        for code, name in TARGETS:
            key = f'{base}_{code}'
            existing = record.get(key, '')
            if existing and existing.strip():
                continue
            try:
                translated = translate_field(en_val, name)
                record[key] = translated
                changed = True
                print(f'  yaml: {base}_{code} filled', flush=True)
                time.sleep(0.3)
            except Exception as e:
                print(f'  yaml: {base}_{code} FAILED: {e}', file=sys.stderr, flush=True)
    return changed


def _fill_ui_record(lang_map: dict) -> bool:
    """UI yaml shape: key -> {en, ja, pt}. Fill missing or empty langs."""
    en_val = lang_map.get('en', '')
    if not en_val:
        return False
    changed = False
    for code, name in TARGETS:
        existing = lang_map.get(code, '')
        if existing and existing.strip():
            continue
        try:
            translated = translate_field(en_val, name)
            lang_map[code] = translated
            changed = True
            time.sleep(0.3)
        except Exception as e:
            print(f'  ui: {code} FAILED: {e}', file=sys.stderr, flush=True)
    return changed


def translate_missing_yaml() -> list[Path]:
    updated: list[Path] = []
    for yaml_path in sorted(CONTENT.glob('*.yaml')):
        doc = yaml.safe_load(yaml_path.read_text(encoding='utf-8'))
        if doc is None:
            continue
        changed = False
        if isinstance(doc, list):
            for rec in doc:
                if isinstance(rec, dict):
                    if _fill_record(rec):
                        changed = True
        elif isinstance(doc, dict):
            # If values are dicts with en/ja/pt keys, it's the UI shape.
            # Otherwise, treat the top-level dict as a single record.
            sample = next(iter(doc.values()), None)
            if isinstance(sample, dict) and 'en' in sample:
                for key, lang_map in doc.items():
                    if isinstance(lang_map, dict):
                        if _fill_ui_record(lang_map):
                            changed = True
            else:
                if _fill_record(doc):
                    changed = True
        if changed:
            yaml_path.write_text(
                yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False),
                encoding='utf-8',
            )
            updated.append(yaml_path)
    return updated


def main() -> int:
    created, failed = translate_missing_md()
    updated = translate_missing_yaml()
    print()
    print(f'markdown files created: {len(created)}')
    print(f'markdown files failed:  {len(failed)}')
    print(f'yaml files updated:     {len(updated)}')
    if failed:
        print('  Failed files will be retried on the next workflow run.')
    if not created and not updated and not failed:
        print('Nothing to do.')
    # Always exit 0 so the commit step saves whatever succeeded.
    # The next run picks up the rest thanks to the idempotent skip-if-exists check.
    return 0


if __name__ == '__main__':
    sys.exit(main())
