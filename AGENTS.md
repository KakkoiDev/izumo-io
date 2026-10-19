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

## Tests: scenarios first, one e2e test each

Same protocol as Pi Workbench and test-core. Every feature of the site, the build and the translator has
Given/When/Then scenarios in `SCENARIOS.md` (`### Scenario: <title>`), and each has one end-to-end test in
`tests/e2e/` named after its title (`@pytest.mark.scenario("<title>")` on `def test_<title in snake case>`): Playwright
for the site, the real command on a scratch copy for the build and the translator. Write the scenario first, see the
test fail, then change the code. Removing a feature removes its scenario and test in the same commit.
Tests are offline (outside requests get stand-ins; the Gemini client is `tests/e2e/stand_ins/`), wait for state never
time, and every Chromium launch passes `--use-mock-keychain --password-store=basic` (`tests/e2e/conftest.py`).

The gate, as `.github/workflows/test.yml` runs it (`pip install -r requirements-dev.txt` once; the browser from
`python -m playwright install chromium`, or point PLAYWRIGHT_CHROMIUM at an existing Chromium):

```sh
python tools/test-core/flaky_lint.py tests
python tools/test-core/e2e_coverage.py --pages 'website/pages/*.html' 'website/templates/*.html' --tests 'tests/e2e/*.py'
python -m pytest --junitxml=.test-output/pytest-junit.xml
python tools/test-core/scenarios.py check SCENARIOS.md --tests tests/e2e/test_*.py --junit .test-output/pytest-junit.xml
```

A new control in a template needs an e2e step; `docs/` must match a fresh `make build` (a test checks it).

## Tests: scenarios first, one e2e test each

Same protocol as Pi Workbench and test-core. Every feature of the site, the build and the translator has
Given/When/Then scenarios in `SCENARIOS.md` (`### Scenario: <title>`), and each has one end-to-end test in
`tests/e2e/` named after its title (`@pytest.mark.scenario("<title>")` on `def test_<title in snake case>`): Playwright
for the site, the real command on a scratch copy for the build and the translator. Write the scenario first, see the
test fail, then change the code. Removing a feature removes its scenario and test in the same commit.
Tests are offline (outside requests get stand-ins; the Gemini client is `tests/e2e/stand_ins/`), wait for state never
time, and every Chromium launch passes `--use-mock-keychain --password-store=basic` (`tests/e2e/conftest.py`).

The gate, as `.github/workflows/test.yml` runs it (`pip install -r requirements-dev.txt` once; the browser from
`python -m playwright install chromium`, or point PLAYWRIGHT_CHROMIUM at an existing Chromium):

```sh
python tools/test-core/flaky_lint.py tests
python tools/test-core/e2e_coverage.py --pages 'website/pages/*.html' 'website/templates/*.html' --tests 'tests/e2e/*.py'
python -m pytest --junitxml=.test-output/pytest-junit.xml
python tools/test-core/scenarios.py check SCENARIOS.md --tests tests/e2e/test_*.py --junit .test-output/pytest-junit.xml
```

A new control in a template needs an e2e step; `docs/` must match a fresh `make build` (a test checks it).

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
