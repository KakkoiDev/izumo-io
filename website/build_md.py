#!/usr/bin/env python3
"""
Markdown-backed parallel builder.

Loads content from content/ via content_loader, then monkey-patches
build.py's module-level data and redirects output to docs_md/.

This exists only during migration step 2 so we can diff docs/ (legacy,
lessons.py-backed) against docs_md/ (markdown-backed) and prove parity.
Delete after step 3 swaps build.py itself.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import build  # noqa: E402
from content_loader import load_all  # noqa: E402


def main() -> None:
    data = load_all()

    # Swap in markdown-loaded content for the hard-coded dicts/lists in build.py.
    build.LESSONS = data['LESSONS']
    build.TECH_LESSONS = data['TECH_LESSONS']
    build.THEORY_LESSONS = data['THEORY_LESSONS']
    build.TECH_PHASES = data['TECH_PHASES']
    build.UI = data['UI']
    build.VIDEOS = data['VIDEOS']
    build.RESOURCES = data['RESOURCES']

    # Respect LANGS coming from the loader so later we can add 'pt'.
    build.LANGS = data['LANG_CODES']

    # Point output at docs_md so we can diff against docs/ from the legacy build.
    build.OUT = build.ROOT.parent / 'docs_md'

    build.build()


if __name__ == '__main__':
    main()
