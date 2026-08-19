# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

- Add durable project-specific notes here as they are discovered through real work.

## Lessons are trilingual, and the translations are CI-managed

`content/ai/aNN.md` is the English source; `aNN.ja.md` and `aNN.pt.md` (Brazilian) are its siblings.
`scripts/translate_content.py` (Gemini, run by `.github/workflows/translate-content.yml`) fills siblings
that are missing or empty, and ALSO retranslates any sibling whose frontmatter `source_sha` differs from
`sha1(english_source)[:12]`.

Consequence: after editing an English lesson, re-stamp `source_sha` in both translations, or the bot
overwrites hand-written translations on the next run. `translate: false` in frontmatter opts a file out.

Game-lesson convention (a09 and later): the `## The prompt` fenced block stays in English verbatim in all
languages. Lessons a01 to a08 translate it. Mermaid blocks, code, paths and image alt text stay verbatim.

## The site under docs/ is generated

`make build` runs `website/build.py`, which writes into a temp dir and renames it over `docs/`. It is
deterministic, so a rebuild with no content change produces no diff. Commit the regenerated `docs/`
alongside any `content/` change.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
