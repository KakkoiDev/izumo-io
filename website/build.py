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
from lessons import LESSONS

ROOT = Path(__file__).parent
TEMPLATES = ROOT / 'templates'
PAGES = ROOT / 'pages'
STATIC = ROOT / 'static'
OUT = ROOT.parent / 'docs'

LANGS = ['en', 'ja']
LANG_LABELS = {'en': 'English', 'ja': '\u65e5\u672c\u8a9e'}


# -- Content data ----------------------------------------------------------

def t(data, lang):
    """Get localized value with EN fallback."""
    return data.get(lang, data.get('en', ''))


UI = {
    'site_name': {'en': 'KakkoiSchool', 'ja': 'KakkoiSchool'},
    'site_tagline': {
        'en': 'From zero to full stack developer',
        'ja': '\u30bc\u30ed\u304b\u3089\u30d5\u30eb\u30b9\u30bf\u30c3\u30af\u958b\u767a\u8005\u3078',
    },
    'back_to_tech': {
        'en': 'Back to Tech Lessons',
        'ja': '\u6280\u8853\u30ec\u30c3\u30b9\u30f3\u306b\u623b\u308b',
    },
    'back_to_theory': {
        'en': 'Back to Theory Lessons',
        'ja': '\u7406\u8ad6\u30ec\u30c3\u30b9\u30f3\u306b\u623b\u308b',
    },
    'prev_lesson': {
        'en': 'Previous',
        'ja': '\u524d\u3078',
    },
    'next_lesson': {
        'en': 'Next',
        'ja': '\u6b21\u3078',
    },
    'hero_title': {
        'en': 'Learn to Build the Web',
        'ja': '\u30a6\u30a7\u30d6\u958b\u767a\u3092\u5b66\u307c\u3046',
    },
    'hero_subtitle': {
        'en': 'Hands-on lessons teaching the 20% that covers 80% of real-world development. From your first HTML page to a full-stack AI application.',
        'ja': '\u5b9f\u8df5\u7684\u306a\u30ec\u30c3\u30b9\u30f3\u3067\u3001\u73fe\u5834\u306e80%\u3092\u30ab\u30d0\u30fc\u3059\u308b20%\u3092\u5b66\u3076\u3002\u521d\u3081\u3066\u306eHTML\u30da\u30fc\u30b8\u304b\u3089\u30d5\u30eb\u30b9\u30bf\u30c3\u30afAI\u30a2\u30d7\u30ea\u30b1\u30fc\u30b7\u30e7\u30f3\u307e\u3067\u3002',
    },
    'nav_tech': {
        'en': 'Tech Lessons',
        'ja': '\u6280\u8853\u30ec\u30c3\u30b9\u30f3',
    },
    'nav_theory': {
        'en': 'Theory',
        'ja': '\u7406\u8ad6',
    },
    'nav_videos': {
        'en': 'Videos',
        'ja': '\u52d5\u753b',
    },
    'coming_soon': {
        'en': 'Coming Soon',
        'ja': '\u8fd1\u65e5\u516c\u958b',
    },
    'tech_title': {
        'en': 'Technical Lessons',
        'ja': '\u6280\u8853\u30ec\u30c3\u30b9\u30f3',
    },
    'tech_desc': {
        'en': 'Hands-on lessons from HTML to full-stack AI applications. Build real projects step by step.',
        'ja': 'HTML\u304b\u3089\u30d5\u30eb\u30b9\u30bf\u30c3\u30afAI\u30a2\u30d7\u30ea\u307e\u3067\u306e\u5b9f\u8df5\u30ec\u30c3\u30b9\u30f3\u3002\u30b9\u30c6\u30c3\u30d7\u30d0\u30a4\u30b9\u30c6\u30c3\u30d7\u3067\u5b9f\u969b\u306e\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u69cb\u7bc9\u3002',
    },
    'theory_title': {
        'en': 'Theory & Life Lessons',
        'ja': '\u7406\u8ad6\u3068\u30e9\u30a4\u30d5\u30ec\u30c3\u30b9\u30f3',
    },
    'theory_desc': {
        'en': 'The thinking behind great software and great developers.',
        'ja': '\u512a\u308c\u305f\u30bd\u30d5\u30c8\u30a6\u30a7\u30a2\u3068\u512a\u308c\u305f\u958b\u767a\u8005\u306e\u80cc\u5f8c\u306b\u3042\u308b\u8003\u3048\u65b9\u3002',
    },
    'videos_title': {
        'en': 'Lesson Videos',
        'ja': '\u30ec\u30c3\u30b9\u30f3\u52d5\u753b',
    },
    'videos_desc': {
        'en': 'Watch previous lesson recordings on YouTube.',
        'ja': 'YouTube\u3067\u904e\u53bb\u306e\u30ec\u30c3\u30b9\u30f3\u3092\u8996\u8074\u3002',
    },
    'start_learning': {
        'en': 'Start Learning',
        'ja': '\u5b66\u7fd2\u3092\u59cb\u3081\u308b',
    },
    'philosophy_title': {
        'en': 'Our Approach',
        'ja': '\u79c1\u305f\u3061\u306e\u30a2\u30d7\u30ed\u30fc\u30c1',
    },
    'philosophy_2080': {
        'en': 'Learn the 20% that covers 80% of real-world work',
        'ja': '\u73fe\u5834\u306e80%\u3092\u30ab\u30d0\u30fc\u3059\u308b20%\u3092\u5b66\u3076',
    },
    'philosophy_hands_on': {
        'en': 'Build real projects from day one',
        'ja': '\u521d\u65e5\u304b\u3089\u5b9f\u969b\u306e\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u69cb\u7bc9\u3059\u308b',
    },
    'philosophy_analogies': {
        'en': 'Understand through real-world analogies',
        'ja': '\u73fe\u5b9f\u4e16\u754c\u306e\u30a2\u30ca\u30ed\u30b8\u30fc\u3067\u7406\u89e3\u3059\u308b',
    },
    'philosophy_zero': {
        'en': 'Start from absolute zero, no prerequisites',
        'ja': '\u5b8c\u5168\u306a\u30bc\u30ed\u304b\u3089\u3001\u524d\u63d0\u6761\u4ef6\u306a\u3057',
    },
    'community_title': {
        'en': 'Join the Community',
        'ja': '\u30b3\u30df\u30e5\u30cb\u30c6\u30a3\u306b\u53c2\u52a0',
    },
    'community_desc': {
        'en': 'Learn together, ask questions, share your progress.',
        'ja': '\u4e00\u7dd2\u306b\u5b66\u3073\u3001\u8cea\u554f\u3057\u3001\u9032\u6357\u3092\u5171\u6709\u3057\u3088\u3046\u3002',
    },
    'discord_cta': {
        'en': 'Join our Discord',
        'ja': 'Discord\u306b\u53c2\u52a0\u3059\u308b',
    },
    'nav_resources': {
        'en': 'Resources',
        'ja': '\u30ea\u30bd\u30fc\u30b9',
    },
    'resources_title': {
        'en': 'Resources',
        'ja': '\u30ea\u30bd\u30fc\u30b9',
    },
    'resources_desc': {
        'en': 'Curated tools and platforms to level up your skills.',
        'ja': '\u30b9\u30ad\u30eb\u30a2\u30c3\u30d7\u306e\u305f\u3081\u306e\u53b3\u9078\u30c4\u30fc\u30eb\u3068\u30d7\u30e9\u30c3\u30c8\u30d5\u30a9\u30fc\u30e0\u3002',
    },
}

PAGE_TITLES = {
    'index.html': {'en': '', 'ja': ''},
    'tech-lessons.html': {'en': 'Technical Lessons', 'ja': '\u6280\u8853\u30ec\u30c3\u30b9\u30f3'},
    'theory-lessons.html': {'en': 'Theory & Life Lessons', 'ja': '\u7406\u8ad6\u3068\u30e9\u30a4\u30d5\u30ec\u30c3\u30b9\u30f3'},
    'videos.html': {'en': 'Lesson Videos', 'ja': '\u30ec\u30c3\u30b9\u30f3\u52d5\u753b'},
    'resources.html': {'en': 'Resources', 'ja': '\u30ea\u30bd\u30fc\u30b9'},
}

TECH_PHASES = [
    {
        'id': 1,
        'title_en': 'Phase 1: The Book (HTML/CSS)',
        'title_ja': '\u30d5\u30a7\u30fc\u30ba1: \u672c (HTML/CSS)',
        'subtitle_en': 'Structure and decoration, no JavaScript at all',
        'subtitle_ja': '\u69cb\u9020\u3068\u88c5\u98fe\u3001JavaScript\u306a\u3057',
        'analogy_en': 'Like building a book: skeleton (HTML) and design (CSS)',
        'analogy_ja': '\u672c\u3092\u4f5c\u308b\u3088\u3046\u306b: \u9aa8\u683c (HTML) \u3068\u30c7\u30b6\u30a4\u30f3 (CSS)',
    },
    {
        'id': 2,
        'title_en': 'Phase 2: The Brain (JavaScript)',
        'title_ja': '\u30d5\u30a7\u30fc\u30ba2: \u8133 (JavaScript)',
        'subtitle_en': 'Adding thinking and interaction to the page',
        'subtitle_ja': '\u30da\u30fc\u30b8\u306b\u601d\u8003\u3068\u30a4\u30f3\u30bf\u30e9\u30af\u30b7\u30e7\u30f3\u3092\u52a0\u3048\u308b',
        'analogy_en': 'Like adding muscles and a brain to your book',
        'analogy_ja': '\u672c\u306b\u7b4b\u8089\u3068\u8133\u3092\u52a0\u3048\u308b',
    },
    {
        'id': 3,
        'title_en': 'Phase 3: The Kitchen (Backend)',
        'title_ja': '\u30d5\u30a7\u30fc\u30ba3: \u53a8\u623f (\u30d0\u30c3\u30af\u30a8\u30f3\u30c9)',
        'subtitle_en': 'Servers, APIs, and databases',
        'subtitle_ja': '\u30b5\u30fc\u30d0\u30fc\u3001API\u3001\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9',
        'analogy_en': 'Building the restaurant kitchen that prepares the food',
        'analogy_ja': '\u6599\u7406\u3092\u6e96\u5099\u3059\u308b\u30ec\u30b9\u30c8\u30e9\u30f3\u306e\u53a8\u623f\u3092\u4f5c\u308b',
    },
    {
        'id': 4,
        'title_en': 'Phase 4: The Robot Chef (AI)',
        'title_ja': '\u30d5\u30a7\u30fc\u30ba4: \u30ed\u30dc\u30c3\u30c8\u30b7\u30a7\u30d5 (AI)',
        'subtitle_en': 'Integrating artificial intelligence',
        'subtitle_ja': '\u4eba\u5de5\u77e5\u80fd\u306e\u7d71\u5408',
        'analogy_en': 'Hiring a robot that read millions of books to help in your kitchen',
        'analogy_ja': '\u767e\u4e07\u518a\u306e\u672c\u3092\u8aad\u3093\u3060\u30ed\u30dc\u30c3\u30c8\u3092\u53a8\u623f\u306b\u96c7\u3046',
    },
    {
        'id': 5,
        'title_en': 'Phase 5: Modern Tools',
        'title_ja': '\u30d5\u30a7\u30fc\u30ba5: \u30e2\u30c0\u30f3\u30c4\u30fc\u30eb',
        'subtitle_en': 'Professional frameworks used in the industry',
        'subtitle_ja': '\u696d\u754c\u3067\u4f7f\u308f\u308c\u308b\u30d7\u30ed\u306e\u30d5\u30ec\u30fc\u30e0\u30ef\u30fc\u30af',
        'analogy_en': 'Franchise-grade equipment for scaling your restaurant',
        'analogy_ja': '\u30ec\u30b9\u30c8\u30e9\u30f3\u3092\u62e1\u5927\u3059\u308b\u305f\u3081\u306e\u30d5\u30e9\u30f3\u30c1\u30e3\u30a4\u30ba\u7d1a\u306e\u8a2d\u5099',
    },
]

TECH_LESSONS = [
    # Phase 1: HTML/CSS
    {'id': 'T01', 'phase': 1, 'status': 'available',
     'title_en': 'Hello World',
     'title_ja': 'Hello World',
     'desc_en': 'Your first webpage. Create a file, open it in a browser.',
     'desc_ja': '\u521d\u3081\u3066\u306e\u30a6\u30a7\u30d6\u30da\u30fc\u30b8\u3002\u30d5\u30a1\u30a4\u30eb\u3092\u4f5c\u6210\u3057\u3001\u30d6\u30e9\u30a6\u30b6\u3067\u958b\u304f\u3002'},
    {'id': 'T02', 'phase': 1, 'status': 'available',
     'title_en': 'HTML Tags',
     'title_ja': 'HTML\u30bf\u30b0',
     'desc_en': 'The building blocks: headings, paragraphs, lists, links, images.',
     'desc_ja': '\u57fa\u672c\u8981\u7d20: \u898b\u51fa\u3057\u3001\u6bb5\u843d\u3001\u30ea\u30b9\u30c8\u3001\u30ea\u30f3\u30af\u3001\u753b\u50cf\u3002'},
    {'id': 'T03', 'phase': 1, 'status': 'available',
     'title_en': 'HTML Forms & Blocks',
     'title_ja': 'HTML\u30d5\u30a9\u30fc\u30e0\u3068\u30d6\u30ed\u30c3\u30af',
     'desc_en': 'Interactive HTML: input, select, textarea, validation, details/summary.',
     'desc_ja': '\u30a4\u30f3\u30bf\u30e9\u30af\u30c6\u30a3\u30d6\u306aHTML: input, select, textarea, \u30d0\u30ea\u30c7\u30fc\u30b7\u30e7\u30f3, details/summary\u3002'},
    {'id': 'T04', 'phase': 1, 'status': 'available',
     'title_en': 'CSS Basics',
     'title_ja': 'CSS\u57fa\u790e',
     'desc_en': 'Making things look good: selectors, colors, fonts, box model.',
     'desc_ja': '\u898b\u305f\u76ee\u3092\u6574\u3048\u308b: \u30bb\u30ec\u30af\u30bf\u3001\u8272\u3001\u30d5\u30a9\u30f3\u30c8\u3001\u30dc\u30c3\u30af\u30b9\u30e2\u30c7\u30eb\u3002'},
    {'id': 'T05', 'phase': 1, 'status': 'available',
     'title_en': 'CSS Layout',
     'title_ja': 'CSS\u30ec\u30a4\u30a2\u30a6\u30c8',
     'desc_en': 'Organizing the page: flexbox, grid, responsive design, media queries.',
     'desc_ja': '\u30da\u30fc\u30b8\u306e\u69cb\u6210: flexbox, grid, \u30ec\u30b9\u30dd\u30f3\u30b7\u30d6\u30c7\u30b6\u30a4\u30f3, \u30e1\u30c7\u30a3\u30a2\u30af\u30a8\u30ea\u3002'},
    {'id': 'T06', 'phase': 1, 'status': 'available',
     'title_en': 'CSS to the Limit',
     'title_ja': 'CSS\u306e\u9650\u754c\u306b\u6311\u3080',
     'desc_en': 'Pure CSS interactivity: animations, transitions, :target, accordion/tabs.',
     'desc_ja': 'CSS\u3060\u3051\u306e\u30a4\u30f3\u30bf\u30e9\u30af\u30c6\u30a3\u30d6: \u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3, \u30c8\u30e9\u30f3\u30b8\u30b7\u30e7\u30f3, :target, \u30a2\u30b3\u30fc\u30c7\u30a3\u30aa\u30f3/\u30bf\u30d6\u3002'},
    # Phase 2: JavaScript
    {'id': 'T07', 'phase': 2, 'status': 'available',
     'title_en': 'JavaScript Intro',
     'title_ja': 'JavaScript\u5165\u9580',
     'desc_en': 'First steps with JS: console.log, variables, types, functions.',
     'desc_ja': 'JS\u306e\u7b2c\u4e00\u6b69: console.log, \u5909\u6570, \u578b, \u95a2\u6570\u3002'},
    {'id': 'T08', 'phase': 2, 'status': 'available',
     'title_en': 'DOM Manipulation',
     'title_ja': 'DOM\u64cd\u4f5c',
     'desc_en': 'Controlling the page: querySelector, createElement, events.',
     'desc_ja': '\u30da\u30fc\u30b8\u306e\u5236\u5fa1: querySelector, createElement, \u30a4\u30d9\u30f3\u30c8\u3002'},
    {'id': 'T09', 'phase': 2, 'status': 'available',
     'title_en': 'Forms & Dialog',
     'title_ja': '\u30d5\u30a9\u30fc\u30e0\u3068\u30c0\u30a4\u30a2\u30ed\u30b0',
     'desc_en': 'Handling user input: JS form validation, dialog element.',
     'desc_ja': '\u30e6\u30fc\u30b6\u30fc\u5165\u529b\u306e\u51e6\u7406: JS\u30d5\u30a9\u30fc\u30e0\u30d0\u30ea\u30c7\u30fc\u30b7\u30e7\u30f3, \u30c0\u30a4\u30a2\u30ed\u30b0\u8981\u7d20\u3002'},
    {'id': 'T10', 'phase': 2, 'status': 'available',
     'title_en': 'Data Structures',
     'title_ja': '\u30c7\u30fc\u30bf\u69cb\u9020',
     'desc_en': 'Organizing information: arrays, objects, loops, dynamic lists.',
     'desc_ja': '\u60c5\u5831\u306e\u6574\u7406: \u914d\u5217, \u30aa\u30d6\u30b8\u30a7\u30af\u30c8, \u30eb\u30fc\u30d7, \u52d5\u7684\u30ea\u30b9\u30c8\u3002'},
    {'id': 'T11', 'phase': 2, 'status': 'available',
     'title_en': 'Persistence',
     'title_ja': '\u30c7\u30fc\u30bf\u306e\u6c38\u7d9a\u5316',
     'desc_en': 'Remembering data: localStorage, JSON parse/stringify.',
     'desc_ja': '\u30c7\u30fc\u30bf\u306e\u8a18\u61b6: localStorage, JSON parse/stringify\u3002'},
    {'id': 'T12', 'phase': 2, 'status': 'available',
     'title_en': 'Fetch API',
     'title_ja': 'Fetch API',
     'desc_en': 'Talking to servers: HTTP requests, async/await, promises.',
     'desc_ja': '\u30b5\u30fc\u30d0\u30fc\u3068\u306e\u901a\u4fe1: HTTP\u30ea\u30af\u30a8\u30b9\u30c8, async/await, Promise\u3002'},
    {'id': 'T13', 'phase': 2, 'status': 'available',
     'title_en': 'Dynamic Site: Routing',
     'title_ja': '\u52d5\u7684\u30b5\u30a4\u30c8: \u30eb\u30fc\u30c6\u30a3\u30f3\u30b0',
     'desc_en': 'One page, many views: hash routing, components, state.',
     'desc_ja': '1\u30da\u30fc\u30b8\u3067\u8907\u6570\u306e\u30d3\u30e5\u30fc: \u30cf\u30c3\u30b7\u30e5\u30eb\u30fc\u30c6\u30a3\u30f3\u30b0, \u30b3\u30f3\u30dd\u30fc\u30cd\u30f3\u30c8, \u72b6\u614b\u7ba1\u7406\u3002'},
    {'id': 'T14', 'phase': 2, 'status': 'available',
     'title_en': 'Dynamic Site: Offline',
     'title_ja': '\u52d5\u7684\u30b5\u30a4\u30c8: \u30aa\u30d5\u30e9\u30a4\u30f3',
     'desc_en': 'Works without internet: service workers, PWA, caching.',
     'desc_ja': '\u30a4\u30f3\u30bf\u30fc\u30cd\u30c3\u30c8\u306a\u3057\u3067\u52d5\u4f5c: \u30b5\u30fc\u30d3\u30b9\u30ef\u30fc\u30ab\u30fc, PWA, \u30ad\u30e3\u30c3\u30b7\u30e5\u3002'},
    {'id': 'T15', 'phase': 2, 'status': 'available',
     'title_en': 'Dynamic Site: Polish',
     'title_ja': '\u52d5\u7684\u30b5\u30a4\u30c8: \u4ed5\u4e0a\u3052',
     'desc_en': 'Production quality: performance, lazy loading, error handling.',
     'desc_ja': '\u30d7\u30ed\u30c0\u30af\u30b7\u30e7\u30f3\u54c1\u8cea: \u30d1\u30d5\u30a9\u30fc\u30de\u30f3\u30b9, \u9045\u5ef6\u8aad\u307f\u8fbc\u307f, \u30a8\u30e9\u30fc\u51e6\u7406\u3002'},
    # Phase 3: Backend
    {'id': 'T16', 'phase': 3, 'status': 'available',
     'title_en': 'Node.js Server',
     'title_ja': 'Node.js\u30b5\u30fc\u30d0\u30fc',
     'desc_en': 'Building the kitchen: HTTP server, serving files, request handling.',
     'desc_ja': '\u53a8\u623f\u3092\u4f5c\u308b: HTTP\u30b5\u30fc\u30d0\u30fc, \u30d5\u30a1\u30a4\u30eb\u914d\u4fe1, \u30ea\u30af\u30a8\u30b9\u30c8\u51e6\u7406\u3002'},
    {'id': 'T17', 'phase': 3, 'status': 'available',
     'title_en': 'API Endpoints',
     'title_ja': 'API\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8',
     'desc_en': 'The menu: REST design, JSON responses, routing.',
     'desc_ja': '\u30e1\u30cb\u30e5\u30fc: REST\u8a2d\u8a08, JSON\u30ec\u30b9\u30dd\u30f3\u30b9, \u30eb\u30fc\u30c6\u30a3\u30f3\u30b0\u3002'},
    {'id': 'T18', 'phase': 3, 'status': 'available',
     'title_en': 'JSON Database',
     'title_ja': 'JSON\u30c7\u30fc\u30bf\u30d9\u30fc\u30b9',
     'desc_en': 'The recipe book: read/write files, CRUD with JSON.',
     'desc_ja': '\u30ec\u30b7\u30d4\u30d6\u30c3\u30af: \u30d5\u30a1\u30a4\u30eb\u306e\u8aad\u307f\u66f8\u304d, JSON\u3067CRUD\u3002'},
    {'id': 'T19', 'phase': 3, 'status': 'available',
     'title_en': 'SQLite',
     'title_ja': 'SQLite',
     'desc_en': 'The filing cabinet: SQL, tables, CRUD, schema, foreign keys.',
     'desc_ja': '\u30d5\u30a1\u30a4\u30ea\u30f3\u30b0\u30ad\u30e3\u30d3\u30cd\u30c3\u30c8: SQL, \u30c6\u30fc\u30d6\u30eb, CRUD, \u30b9\u30ad\u30fc\u30de, \u5916\u90e8\u30ad\u30fc\u3002'},
    {'id': 'T20', 'phase': 3, 'status': 'available',
     'title_en': 'Authentication',
     'title_ja': '\u8a8d\u8a3c',
     'desc_en': 'The ID check: sessions, cookies, password hashing, login/logout.',
     'desc_ja': 'ID\u78ba\u8a8d: \u30bb\u30c3\u30b7\u30e7\u30f3, \u30af\u30c3\u30ad\u30fc, \u30d1\u30b9\u30ef\u30fc\u30c9\u30cf\u30c3\u30b7\u30e5, \u30ed\u30b0\u30a4\u30f3/\u30ed\u30b0\u30a2\u30a6\u30c8\u3002'},
    # Phase 4: AI
    {'id': 'T21', 'phase': 4, 'status': 'available',
     'title_en': 'Ollama & Chat',
     'title_ja': 'Ollama\u3068\u30c1\u30e3\u30c3\u30c8',
     'desc_en': 'The robot chef: local LLM setup, chat API, chat interface.',
     'desc_ja': '\u30ed\u30dc\u30c3\u30c8\u30b7\u30a7\u30d5: \u30ed\u30fc\u30ab\u30ebLLM\u306e\u30bb\u30c3\u30c8\u30a2\u30c3\u30d7, \u30c1\u30e3\u30c3\u30c8API, \u30c1\u30e3\u30c3\u30c8\u30a4\u30f3\u30bf\u30fc\u30d5\u30a7\u30fc\u30b9\u3002'},
    {'id': 'T22', 'phase': 4, 'status': 'available',
     'title_en': 'Full Stack AI App',
     'title_ja': '\u30d5\u30eb\u30b9\u30bf\u30c3\u30afAI\u30a2\u30d7\u30ea',
     'desc_en': 'The whole restaurant: connect frontend, backend, AI, and database.',
     'desc_ja': '\u30ec\u30b9\u30c8\u30e9\u30f3\u5168\u4f53: \u30d5\u30ed\u30f3\u30c8\u30a8\u30f3\u30c9, \u30d0\u30c3\u30af\u30a8\u30f3\u30c9, AI, \u30c7\u30fc\u30bf\u30d9\u30fc\u30b9\u3092\u3064\u306a\u3050\u3002'},
    # Phase 5: Coming Soon
    {'id': 'T23', 'phase': 5, 'status': 'coming-soon',
     'title_en': 'React',
     'title_ja': 'React',
     'desc_en': 'Component-based UI development.',
     'desc_ja': '\u30b3\u30f3\u30dd\u30fc\u30cd\u30f3\u30c8\u30d9\u30fc\u30b9\u306eUI\u958b\u767a\u3002'},
    {'id': 'T24', 'phase': 5, 'status': 'coming-soon',
     'title_en': 'TypeScript',
     'title_ja': 'TypeScript',
     'desc_en': 'Type safety for JavaScript.',
     'desc_ja': 'JavaScript\u306e\u578b\u5b89\u5168\u6027\u3002'},
]

THEORY_LESSONS = [
    {'id': 'R01',
     'title_en': 'What is IT?',
     'title_ja': 'IT\u3068\u306f\u4f55\u304b\uff1f',
     'desc_en': 'Everything is information. IT is about collecting, sending, processing, and storing it.',
     'desc_ja': '\u3059\u3079\u3066\u306f\u60c5\u5831\u3002IT\u3068\u306f\u60c5\u5831\u306e\u53ce\u96c6\u3001\u9001\u4fe1\u3001\u51e6\u7406\u3001\u4fdd\u5b58\u3002',
     'analogy_en': 'A post office for data',
     'analogy_ja': '\u30c7\u30fc\u30bf\u306e\u90f5\u4fbf\u5c40'},
    {'id': 'R02',
     'title_en': 'Web Architecture',
     'title_ja': '\u30a6\u30a7\u30d6\u30a2\u30fc\u30ad\u30c6\u30af\u30c1\u30e3',
     'desc_en': 'Clients request, servers respond. Like a restaurant where you order and the kitchen prepares your meal.',
     'desc_ja': '\u30af\u30e9\u30a4\u30a2\u30f3\u30c8\u304c\u30ea\u30af\u30a8\u30b9\u30c8\u3057\u3001\u30b5\u30fc\u30d0\u30fc\u304c\u30ec\u30b9\u30dd\u30f3\u30b9\u3059\u308b\u3002\u6ce8\u6587\u3092\u51fa\u3057\u3066\u53a8\u623f\u304c\u6599\u7406\u3092\u6e96\u5099\u3059\u308b\u30ec\u30b9\u30c8\u30e9\u30f3\u306e\u3088\u3046\u3002',
     'analogy_en': 'Restaurant: customers order, kitchen prepares',
     'analogy_ja': '\u30ec\u30b9\u30c8\u30e9\u30f3: \u5ba2\u304c\u6ce8\u6587\u3001\u53a8\u623f\u304c\u6e96\u5099'},
    {'id': 'R03',
     'title_en': 'Problem Solving',
     'title_ja': '\u554f\u984c\u89e3\u6c7a',
     'desc_en': 'Understand before you build. Most software work is thinking, not typing.',
     'desc_ja': '\u4f5c\u308b\u524d\u306b\u7406\u89e3\u3059\u308b\u3002\u30bd\u30d5\u30c8\u30a6\u30a7\u30a2\u958b\u767a\u306e\u5927\u534a\u306f\u8003\u3048\u308b\u3053\u3068\u3002',
     'analogy_en': 'Doctor: diagnose before prescribing',
     'analogy_ja': '\u533b\u8005: \u51e6\u65b9\u3059\u308b\u524d\u306b\u8a3a\u65ad\u3059\u308b'},
    {'id': 'R04',
     'title_en': 'The 20/80 Rule',
     'title_ja': '20/80\u306e\u6cd5\u5247',
     'desc_en': '20% of knowledge covers 80% of real work. Focus on what matters most.',
     'desc_ja': '20%\u306e\u77e5\u8b58\u3067\u5b9f\u52d9\u306e80%\u3092\u30ab\u30d0\u30fc\u3002\u6700\u3082\u91cd\u8981\u306a\u3053\u3068\u306b\u96c6\u4e2d\u3002',
     'analogy_en': '5 cooking techniques cover most dishes',
     'analogy_ja': '5\u3064\u306e\u8abf\u7406\u6280\u6cd5\u3067\u307b\u3068\u3093\u3069\u306e\u6599\u7406\u3092\u30ab\u30d0\u30fc'},
    {'id': 'R05',
     'title_en': 'Consistency Beats Passion',
     'title_ja': '\u7d99\u7d9a\u306f\u60c5\u71b1\u306b\u52dd\u308b',
     'desc_en': 'Daily practice beats bursts of inspiration. The marathon runner wins in the long run.',
     'desc_ja': '\u6bce\u65e5\u306e\u7df4\u7fd2\u306f\u3072\u3089\u3081\u304d\u306b\u52dd\u308b\u3002\u9577\u3044\u76ee\u3067\u898b\u308c\u3070\u30de\u30e9\u30bd\u30f3\u30e9\u30f3\u30ca\u30fc\u304c\u52dd\u3064\u3002',
     'analogy_en': 'Marathon runner beats the sprinter',
     'analogy_ja': '\u30de\u30e9\u30bd\u30f3\u30e9\u30f3\u30ca\u30fc\u306f\u30b9\u30d7\u30ea\u30f3\u30bf\u30fc\u306b\u52dd\u3064'},
    {'id': 'R06',
     'title_en': 'Path of Least Resistance',
     'title_ja': '\u6700\u5c0f\u62b5\u6297\u306e\u6cd5\u5247',
     'desc_en': 'New tools get adopted when they are easier than the old way. Innovation flows like water.',
     'desc_ja': '\u65b0\u3057\u3044\u30c4\u30fc\u30eb\u306f\u53e4\u3044\u65b9\u6cd5\u3088\u308a\u7c21\u5358\u306a\u6642\u306b\u63a1\u7528\u3055\u308c\u308b\u3002\u30a4\u30ce\u30d9\u30fc\u30b7\u30e7\u30f3\u306f\u6c34\u306e\u3088\u3046\u306b\u6d41\u308c\u308b\u3002',
     'analogy_en': 'Water flows downhill',
     'analogy_ja': '\u6c34\u306f\u4e0b\u308a\u5742\u3092\u6d41\u308c\u308b'},
    {'id': 'R07',
     'title_en': 'Keep Things Super Simple',
     'title_ja': '\u30b7\u30f3\u30d7\u30eb\u306b\u4fdd\u3064',
     'desc_en': 'Simple solutions beat complex ones. A few basic tools beat a Swiss army knife for real work.',
     'desc_ja': '\u30b7\u30f3\u30d7\u30eb\u306a\u89e3\u6c7a\u7b56\u304c\u8907\u96d1\u306a\u3082\u306e\u306b\u52dd\u3064\u3002\u5b9f\u52d9\u3067\u306f\u57fa\u672c\u7684\u306a\u5de5\u5177\u7bb1\u304c\u30b9\u30a4\u30b9\u30a2\u30fc\u30df\u30fc\u30ca\u30a4\u30d5\u306b\u52dd\u308b\u3002',
     'analogy_en': 'Toolbox beats Swiss army knife',
     'analogy_ja': '\u5de5\u5177\u7bb1\u306f\u30b9\u30a4\u30b9\u30a2\u30fc\u30df\u30fc\u30ca\u30a4\u30d5\u306b\u52dd\u308b'},
    {'id': 'R08',
     'title_en': 'Code Quality',
     'title_ja': '\u30b3\u30fc\u30c9\u54c1\u8cea',
     'desc_en': 'Good code works, runs fast, and is easy to change. Three levels like a restaurant.',
     'desc_ja': '\u826f\u3044\u30b3\u30fc\u30c9\u306f\u52d5\u304d\u3001\u901f\u304f\u3001\u5909\u66f4\u3057\u3084\u3059\u3044\u3002\u30ec\u30b9\u30c8\u30e9\u30f3\u306e\u3088\u3046\u306b3\u3064\u306e\u30ec\u30d9\u30eb\u304c\u3042\u308b\u3002',
     'analogy_en': 'Restaurant: edible, delicious, smooth kitchen',
     'analogy_ja': '\u30ec\u30b9\u30c8\u30e9\u30f3: \u98df\u3079\u3089\u308c\u308b\u3001\u7f8e\u5473\u3057\u3044\u3001\u30b9\u30e0\u30fc\u30ba\u306a\u53a8\u623f'},
    {'id': 'R09',
     'title_en': 'How to Learn',
     'title_ja': '\u5b66\u3073\u65b9',
     'desc_en': 'Learning is exploring a map. First you do not know what you do not know.',
     'desc_ja': '\u5b66\u3076\u3068\u306f\u5730\u56f3\u3092\u63a2\u7d22\u3059\u308b\u3053\u3068\u3002\u6700\u521d\u306f\u77e5\u3089\u306a\u3044\u3053\u3068\u3059\u3089\u77e5\u3089\u306a\u3044\u3002',
     'analogy_en': 'Exploring an unknown map',
     'analogy_ja': '\u672a\u77e5\u306e\u5730\u56f3\u3092\u63a2\u7d22\u3059\u308b'},
    {'id': 'R10',
     'title_en': 'KakkoiSchool Case Study',
     'title_ja': 'KakkoiSchool\u30b1\u30fc\u30b9\u30b9\u30bf\u30c7\u30a3',
     'desc_en': 'Analyzing our own course. What decisions were made, what worked, what did not.',
     'desc_ja': '\u79c1\u305f\u3061\u306e\u30b3\u30fc\u30b9\u3092\u5206\u6790\u3002\u4f55\u3092\u6c7a\u5b9a\u3057\u3001\u4f55\u304c\u3046\u307e\u304f\u3044\u304d\u3001\u4f55\u304c\u3046\u307e\u304f\u3044\u304b\u306a\u304b\u3063\u305f\u304b\u3002',
     'analogy_en': 'Learning from our own journey',
     'analogy_ja': '\u81ea\u5206\u305f\u3061\u306e\u65c5\u304b\u3089\u5b66\u3076'},
    {'id': 'R11',
     'title_en': 'Adaptability',
     'title_ja': '\u9069\u5fdc\u529b',
     'desc_en': 'The tech industry rewards those who embrace change. Fundamentals outlast frameworks.',
     'desc_ja': 'IT\u696d\u754c\u306f\u5909\u5316\u3092\u53d7\u3051\u5165\u308c\u308b\u4eba\u3092\u8a55\u4fa1\u3059\u308b\u3002\u57fa\u790e\u306f\u30d5\u30ec\u30fc\u30e0\u30ef\u30fc\u30af\u3088\u308a\u9577\u6301\u3061\u3059\u308b\u3002',
     'analogy_en': 'Foundations outlast any single tool',
     'analogy_ja': '\u57fa\u790e\u306f\u3069\u306e\u30c4\u30fc\u30eb\u3088\u308a\u9577\u6301\u3061\u3059\u308b'},
    {'id': 'R12',
     'title_en': 'Work-Life Balance',
     'title_ja': '\u30ef\u30fc\u30af\u30e9\u30a4\u30d5\u30d0\u30e9\u30f3\u30b9',
     'desc_en': 'A career is a marathon. Sustainable pace beats chronic overwork.',
     'desc_ja': '\u30ad\u30e3\u30ea\u30a2\u306f\u30de\u30e9\u30bd\u30f3\u3002\u6301\u7d9a\u53ef\u80fd\u306a\u30da\u30fc\u30b9\u304c\u6162\u6027\u7684\u306a\u904e\u91cd\u52b4\u50cd\u306b\u52dd\u3064\u3002',
     'analogy_en': 'You cannot sprint a marathon',
     'analogy_ja': '\u30de\u30e9\u30bd\u30f3\u3092\u5168\u529b\u75be\u8d70\u306f\u3067\u304d\u306a\u3044'},
    {'id': 'R13',
     'title_en': 'Workplace Politics',
     'title_ja': '\u8077\u5834\u306e\u4eba\u9593\u95a2\u4fc2',
     'desc_en': 'Navigating office politics, protecting your work, and knowing when to leave.',
     'desc_ja': '\u8077\u5834\u306e\u653f\u6cbb\u3092\u4e57\u308a\u8d8a\u3048\u3001\u4ed5\u4e8b\u3092\u5b88\u308a\u3001\u53bb\u308b\u3079\u304d\u6642\u3092\u77e5\u308b\u3002',
     'analogy_en': 'Document, build alliances, stay focused',
     'analogy_ja': '\u8a18\u9332\u3057\u3001\u5473\u65b9\u3092\u4f5c\u308a\u3001\u96c6\u4e2d\u3059\u308b'},
    {'id': 'R14',
     'title_en': 'Communication & Teamwork',
     'title_ja': '\u30b3\u30df\u30e5\u30cb\u30b1\u30fc\u30b7\u30e7\u30f3\u3068\u30c1\u30fc\u30e0\u30ef\u30fc\u30af',
     'desc_en': 'Technical skills get you hired. Communication skills get you promoted.',
     'desc_ja': '\u6280\u8853\u529b\u3067\u63a1\u7528\u3055\u308c\u3001\u30b3\u30df\u30e5\u30cb\u30b1\u30fc\u30b7\u30e7\u30f3\u529b\u3067\u6607\u9032\u3059\u308b\u3002',
     'analogy_en': 'Brilliant code nobody understands is useless',
     'analogy_ja': '\u8ab0\u306b\u3082\u7406\u89e3\u3067\u304d\u306a\u3044\u512a\u308c\u305f\u30b3\u30fc\u30c9\u306f\u7121\u610f\u5473'},
    {'id': 'R15',
     'title_en': 'Working with AI',
     'title_ja': 'AI\u3068\u306e\u5354\u50cd',
     'desc_en': 'AI is a force multiplier. Learn to work with it, not against it.',
     'desc_ja': 'AI\u306f\u529b\u306e\u500d\u5897\u5668\u3002AI\u306b\u62b5\u6297\u305b\u305a\u3001\u5171\u306b\u50cd\u304f\u3053\u3068\u3092\u5b66\u3076\u3002',
     'analogy_en': 'A robot assistant that read millions of books',
     'analogy_ja': '\u767e\u4e07\u518a\u306e\u672c\u3092\u8aad\u3093\u3060\u30ed\u30dc\u30c3\u30c8\u30a2\u30b7\u30b9\u30bf\u30f3\u30c8'},
    {'id': 'R16',
     'title_en': 'Shipping is a Skill',
     'title_ja': '\u5b8c\u6210\u3055\u305b\u308b\u529b',
     'desc_en': 'Many can code, fewer can ship. Finishing and presenting work professionally is its own skill.',
     'desc_ja': '\u30b3\u30fc\u30c9\u3092\u66f8\u3051\u308b\u4eba\u306f\u591a\u3044\u304c\u3001\u5b8c\u6210\u3055\u305b\u3089\u308c\u308b\u4eba\u306f\u5c11\u306a\u3044\u3002\u4ed5\u4e0a\u3052\u3068\u767a\u8868\u306f\u305d\u308c\u81ea\u4f53\u304c\u30b9\u30ad\u30eb\u3002',
     'analogy_en': 'A finished project beats an impressive unfinished one',
     'analogy_ja': '\u5b8c\u6210\u3057\u305f\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u306f\u5370\u8c61\u7684\u306a\u672a\u5b8c\u6210\u306e\u3082\u306e\u306b\u52dd\u308b'},
]

VIDEOS = [
    {'youtube_id': 'MmaJ_VucH18',
     'title_en': 'KakkoiSchool Season 2 Start',
     'title_ja': 'KakkoiSchool \u30b7\u30fc\u30ba\u30f32\u958b\u59cb',
     'desc_en': 'Wednesday April 16 2026 - KakkoiSchool Season 2 kicks off!',
     'desc_ja': '2026\u5e744\u670816\u65e5\u6c34\u66dc\u65e5 - KakkoiSchool \u30b7\u30fc\u30ba\u30f32\u30b9\u30bf\u30fc\u30c8\uff01'},
]

RESOURCES = [
    {'url': 'https://exercism.org/',
     'domain': 'exercism.org',
     'title_en': 'Exercism',
     'title_ja': 'Exercism',
     'desc_en': 'Free coding exercises in 70+ languages with mentoring. Practice fundamentals through real challenges.',
     'desc_ja': '70\u4ee5\u4e0a\u306e\u8a00\u8a9e\u3067\u7121\u6599\u306e\u30b3\u30fc\u30c7\u30a3\u30f3\u30b0\u6f14\u7fd2\u3068\u30e1\u30f3\u30bf\u30ea\u30f3\u30b0\u3002\u5b9f\u969b\u306e\u8ab2\u984c\u3067\u57fa\u790e\u3092\u7df4\u7fd2\u3002'},
    {'url': 'https://www.w3schools.com/',
     'domain': 'w3schools.com',
     'title_en': 'W3Schools',
     'title_ja': 'W3Schools',
     'desc_en': 'Tutorials and references for HTML, CSS, JavaScript, and more. Great for quick lookups and interactive examples.',
     'desc_ja': 'HTML\u3001CSS\u3001JavaScript\u306a\u3069\u306e\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb\u3068\u30ea\u30d5\u30a1\u30ec\u30f3\u30b9\u3002\u7d20\u65e9\u3044\u691c\u7d22\u3068\u30a4\u30f3\u30bf\u30e9\u30af\u30c6\u30a3\u30d6\u306a\u4f8b\u306b\u6700\u9069\u3002'},
    {'url': 'https://developer.mozilla.org/en-US/',
     'domain': 'developer.mozilla.org',
     'title_en': 'MDN Web Docs',
     'title_ja': 'MDN Web Docs',
     'desc_en': 'The definitive reference for web technologies. In-depth documentation for HTML, CSS, JavaScript, and Web APIs.',
     'desc_ja': 'Web\u6280\u8853\u306e\u6c7a\u5b9a\u7248\u30ea\u30d5\u30a1\u30ec\u30f3\u30b9\u3002HTML\u3001CSS\u3001JavaScript\u3001Web API\u306e\u8a73\u7d30\u306a\u30c9\u30ad\u30e5\u30e1\u30f3\u30c8\u3002'},
    {'url': 'https://www.hellointerview.com/',
     'domain': 'hellointerview.com',
     'title_en': 'Hello Interview',
     'title_ja': 'Hello Interview',
     'desc_en': 'System design and coding interview preparation. Learn how real-world systems are built and evaluated.',
     'desc_ja': '\u30b7\u30b9\u30c6\u30e0\u8a2d\u8a08\u3068\u30b3\u30fc\u30c7\u30a3\u30f3\u30b0\u9762\u63a5\u306e\u6e96\u5099\u3002\u5b9f\u969b\u306e\u30b7\u30b9\u30c6\u30e0\u304c\u3069\u3046\u69cb\u7bc9\u30fb\u8a55\u4fa1\u3055\u308c\u308b\u304b\u3092\u5b66\u3076\u3002'},
]


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


def localize_list(items, lang):
    """Create localized version of a list of dicts.

    Keys ending in _en/_ja get merged into a base key using the
    requested language with EN fallback.
    """
    result = []
    for item in items:
        loc = {}
        seen = set()
        for key in item:
            if key.endswith('_en') or key.endswith('_ja'):
                base = key.rsplit('_', 1)[0]
                if base not in seen:
                    seen.add(base)
                    loc[base] = item.get(f'{base}_{lang}', item.get(f'{base}_en', ''))
            else:
                loc[key] = item[key]
        result.append(loc)
    return result


def build_context(lang, page_file):
    """Build template context for rendering a page."""
    is_ja = lang == 'ja'

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

    return {
        'lang': lang,
        'HTML_LANG': lang,
        'STATIC_PATH': '../static/' if is_ja else 'static/',
        'NAV_PREFIX': '',
        'EN_BASE': '../' if is_ja else './',
        'JA_BASE': './' if is_ja else 'ja/',
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
    is_ja = lang == 'ja'
    ui = {k: t(v, lang) for k, v in UI.items()}

    # Find lesson metadata for title
    all_lessons = TECH_LESSONS + THEORY_LESSONS
    lesson_meta = next((l for l in all_lessons if l['id'] == lesson_id), {})
    title_key = f'title_{lang}' if f'title_{lang}' in lesson_meta else 'title_en'
    page_title = lesson_meta.get(title_key, lesson_id)

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

    slug = lesson_id.lower()
    return {
        'lang': lang,
        'HTML_LANG': lang,
        'STATIC_PATH': '../../static/' if is_ja else '../static/',
        'NAV_PREFIX': '../' ,
        'EN_BASE': '../../lessons/' if is_ja else './',
        'JA_BASE': './' if is_ja else '../../ja/lessons/',
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
            lesson_html = content.get(lang, content.get('en', ''))
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
