# Kakkoi Online — handoff

Written for **another agent on another computer** picking this up cold. Read this, then
`kakkoi-online-lessons.md` §10 (the build process). Everything below was true at the last commit.

## What this is

Two things being built together:

1. **A game** — `Kakkoi Online`, a serverless P2P browser game. Live: **https://online.kakkoi.dev**
2. **A lesson track** — lessons **A09–A29** on https://school.kakkoi.dev, continuing the existing AI
   track, teaching a 12–13-year-old to build that game with an AI assistant.

## Two repos

| Repo | Path on the original machine | Remote | Holds |
|---|---|---|---|
| `izumo-io` | `/Users/cyril/Code/izumo-io` | `git@github.com:KakkoiDev/izumo-io.git` | The school site: lessons, planning docs, `docs/` (published) |
| `kakkoi-online` | `/Users/cyril/Code/kakkoi-online` | `git@github.com:KakkoiSchool/kakkoi-online.git` | The game itself |

Clone both. They are independent; the planning docs live in `izumo-io/planning/`.

## Read these first, in order

1. `planning/kakkoi-online-design.md` — why every decision is what it is. **A 42-row decision log with
   six recorded reversals.** Read the log before proposing changes; several "obvious" ideas were already
   tried and rejected for reasons.
2. `planning/kakkoi-online-trd.md` — what to build: data model, network protocol, battle rules,
   milestones, tests.
3. `planning/kakkoi-online-lessons.md` — the 21-lesson track, the **writing standard (§3.5)**, the safety
   lesson, and **§10, the build process you must follow**.
4. `planning/kakkoi-online-sources.md` — every asset pack, library and reference, with licences.

## The rule that matters most

**Docs first, then code, then play it, then fix, then update the docs, and only then write the lesson.**

```
1. Docs current for the milestone
2. Build the slice
3. PLAY IT (two tabs, then with a person)   ← generates the truth
4. Fix what is actually wrong
5. Update the docs to match reality
6. NOW write the lesson, using real failures from FAILURES.md
7. Screenshot + tag aNN-end. Repeat.
```

A lesson written before the code contains invented verification steps and invented AI mistakes, and
students spot it instantly. **`kakkoi-online/FAILURES.md` is collected while building** — every third
lesson shows students a real mistake, and they cannot be reconstructed later.

## State: done

- **Game repo scaffolded and live.** Canvas, fixed-timestep loop (`src/loop.ts`), pure battle rules with
  passing tests (`src/battle/rules.ts`, `tests/rules.test.ts`), `data/*.json` for tuning/type-chart/
  monsters, CI that gates the Pages deploy on `tsc --noEmit` + `bun test`.
- **`online.kakkoi.dev`** — HTTPS enforced, custom domain set **in the Pages API config** (not by the
  `CNAME` file; see gotchas).
- **Lessons A09 and A10 written**, live in EN/JA/PT.
- **AI track split into two phases** (`content/ai-phases.yaml`): Part 1 = using AI (A01–A08),
  Part 2 = the game (A09+). Needed `phase:` frontmatter on the EN AI lesson files, `AI_PHASES` in
  `content_loader.py`, `ai_phases` in `build.py`, and a phase loop in `website/pages/ai-lessons.html`.
- **Translation pipeline fixed** (it had been silently losing every translation since 2026-07-08).

## State: not done

- **`vendor/` and `audio/` in the game repo are empty** except READMEs listing exactly what to put there.
  The two Kenney atlases are **browser downloads from kenney.nl** — an agent cannot fetch them. They gate
  the map and monster lessons (A15–A16), which gates milestone M0.
- **trystero is not vendored yet.** Needs bundling: `bun build --target=browser` (see
  `vendor/README.md`).
- **No game yet** beyond the loop. Next: M0 = tile map + camera → input/movement → monster picker →
  save. Lessons A13–A17.
- Lessons A11–A29 unwritten.

## Environment gotchas (these cost real time)

| Gotcha | Detail |
|---|---|
| **Bun not installed** on the original machine | `curl -fsSL https://bun.com/install \| bash`. Without it you cannot run `bun ./index.html` or `bun test` — the scaffold has only ever been typechecked locally and built by CI |
| **Python 3.9.6 vs `requirements.txt`** | The site build wants `markdown>=3.10`, which needs Python ≥3.10. Local builds were done with `markdown==3.9` in `.venv` (renders fine, not what is pinned). Fix properly: `brew install python@3.12`, recreate `.venv`, `pip install -r requirements.txt` |
| **`make build` needs the venv** | `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. The Makefile prefers `.venv/bin/python` if present |
| **`master` has a ruleset requiring PRs** | "Protect Master"; bypass list = repository admin only. The owner's pushes report "Bypassed rule violations" and succeed. **`github-actions[bot]` cannot push to master** |
| **Actions cannot create PRs** | Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests" is **off**. The translate workflow therefore pushes a branch and prints a PR link in the run summary instead of failing. Enable with `gh api -X PUT repos/KakkoiDev/izumo-io/actions/permissions/workflow -F can_approve_pull_request_reviews=true` if full automation is wanted |
| **`CNAME` file is inert** | For **workflow-based** Pages the custom domain lives in the Pages config, not in a `CNAME` file. `gh api -X PUT repos/OWNER/REPO/pages -f cname=online.kakkoi.dev`, wait for the cert, then `-F https_enforced=true` |
| **Game repo default branch is `main`**, school repo is `master` | Do not assume either |
| **`curl` in the sandbox could not resolve `online.kakkoi.dev`** while `dig` could | Verify with `curl --resolve online.kakkoi.dev:443:185.199.108.153` |

## Publishing a lesson

```bash
# 1. write content/ai/aNN.md   (EN only; frontmatter: id, phase, title, desc — no status field in the AI track)
make build                      # regenerates docs/
git add -A && git commit && git push origin master
# 2. the translate workflow fires on content/**.md, generates JA+PT, rebuilds docs/,
#    pushes a branch and prints a PR link in the run summary. Merge it.
# 3. if you merge locally instead, run `make build` again and push, or the JA/PT
#    pages will keep serving English.
```

The workflow now **fails loudly** if any lesson is missing a `.ja.md`/`.pt.md` sibling, naming the files.

## Decisions a newcomer will be tempted to re-open

All settled, with reasons in the decision log. Do not silently reverse them:

- **No Phaser.** Hand-written canvas. Appendix X7 ports to Phaser *afterwards* as a lesson.
- **No procedural art or audio.** A fixed set of ~6 Kenney CC0 monsters, CC0 audio files, no synthesis.
- **Chat is preset phrases only.** No free text at all — the readers are children and there is no
  moderation possible. Abuse is designed out, not policed.
- **`agy` (Antigravity CLI), not Claude Code**, because A01/A02 already install it, it is free, and it
  keeps GitHub's 13+ as the only account rule.
- **Students start from an empty repo**, never a fork, and read our tagged snapshots in a browser if
  stuck. A fork hands them the finished game.
- **v1 has no levels, no dual types, no cosmetics, no wild encounters, no ghost notes.** Scope is
  deliberately tiny.
- **Lessons must be readable by a 12-year-old** (writing standard §3.5). This outranks completeness.

## Who to ask

The owner is `KakkoiDev` (Cyril), teaching one lesson per week to a small class: one 13-year-old, the
rest adults. Class doubles as the multiplayer play window. Open questions worth raising with him:

- Whether A09/A10's voice and reading level are right (everything after inherits it).
- The Kenney downloads, which nobody else can do.
